# ==============================================================================
# Multi-Stage Python Dockerfile Template
# Supports: uv (preferred) or pip
# Pattern: Build stage installs dependencies, runtime stage copies venv
# ==============================================================================

# --- Build Arguments ---------------------------------------------------------
# Customize these at build time: docker build --build-arg PYTHON_VERSION=3.11 .
ARG PYTHON_VERSION=3.12

# ==============================================================================
# Stage 1: Builder
# Installs dependencies into a virtual environment that will be copied to the
# runtime stage. Uses the full Python image so compiled extensions (numpy,
# scipy, etc.) can build against system headers.
# ==============================================================================
FROM python:${PYTHON_VERSION}-slim AS builder

# Install system build dependencies for compiled Python packages.
# Add or remove packages based on your project's needs.
# Common additions: gfortran (scipy), libhdf5-dev (h5py), libpq-dev (psycopg2)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency resolution and installation.
# Remove this block and use pip below if uv is not desired.
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copy dependency specification files first for layer caching.
# Dependencies are only reinstalled when these files change.
COPY pyproject.toml uv.lock ./

# Install production dependencies into the project virtual environment.
# --frozen: use exact versions from uv.lock (no resolution)
# --no-dev: exclude development dependencies
RUN uv sync --frozen --no-dev

# --- Alternative: pip-based installation (uncomment if not using uv) ---------
# COPY requirements.txt .
# RUN python -m venv /opt/venv && \
#     /opt/venv/bin/pip install --no-cache-dir -r requirements.txt
# ENV PATH="/opt/venv/bin:$PATH"
# -----------------------------------------------------------------------------

# Copy the application source code.
# This layer is invalidated on every source change, but dependency installation
# above is cached as long as pyproject.toml/uv.lock do not change.
COPY . .

# ==============================================================================
# Stage 2: Runtime
# Minimal image containing only the Python runtime, installed packages, and
# application code. No compilers, no build tools, no pip cache.
# ==============================================================================
FROM python:${PYTHON_VERSION}-slim AS runtime

# Install only runtime system libraries needed by compiled extensions.
# Check with: ldd /app/.venv/lib/python*/site-packages/<package>/*.so
# Common additions: libopenblas0 (numpy), libhdf5-103 (h5py), libpq5 (psycopg2)
# Remove this block entirely if your project has no compiled extensions.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the virtual environment and application from the builder stage.
COPY --from=builder /app /app

# Add the virtual environment's bin directory to PATH so `python` and
# installed console scripts resolve to the venv versions.
ENV PATH="/app/.venv/bin:$PATH" \
    # Prevent Python from buffering stdout/stderr (important for Docker logging)
    PYTHONUNBUFFERED=1 \
    # Prevent Python from writing .pyc files (reduces image noise)
    PYTHONDONTWRITEBYTECODE=1

# --- Alternative: pip-based venv path (uncomment if not using uv) ------------
# COPY --from=builder /opt/venv /opt/venv
# ENV PATH="/opt/venv/bin:$PATH"
# COPY --from=builder /app /app
# -----------------------------------------------------------------------------

# Create a non-root user and group.
# Running as root in production is a security risk.
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --create-home --shell /bin/false appuser && \
    chown -R 1001:1001 /app

# Switch to non-root user before ENTRYPOINT.
USER 1001

# Document the port this application listens on.
# This does not publish the port -- use -p at runtime.
EXPOSE 8000

# Health check for container orchestrators (Docker Compose, Kubernetes).
# Adjust the endpoint and port to match your application.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# OCI standard labels for image metadata.
# Update these values for your project.
LABEL org.opencontainers.image.title="my-python-app" \
      org.opencontainers.image.description="Description of your Python application" \
      org.opencontainers.image.version="0.1.0" \
      org.opencontainers.image.source="https://github.com/org/repo" \
      org.opencontainers.image.licenses="MIT"

# Use exec form (JSON array) for proper signal handling.
# The container process receives SIGTERM directly, enabling graceful shutdown.
ENTRYPOINT ["python", "-m", "myapp"]
CMD ["--host", "0.0.0.0", "--port", "8000"]

# ==============================================================================
# Multi-Stage CUDA Dockerfile with PyTorch
#
# Pattern: Build stage compiles any custom extensions in the devel image,
# runtime stage uses the smaller cudnn-runtime image.
#
# CUDA / cuDNN Layer Choices:
#   - devel stage: Includes nvcc compiler, CUDA headers, and cuDNN headers.
#     Required for compiling custom CUDA extensions (e.g., flash-attn, apex).
#   - runtime stage: Includes only CUDA runtime libs and cuDNN shared libs.
#     Sufficient for running pre-compiled models. ~2 GB smaller than devel.
#
# Usage:
#   docker build -t my-cuda-app .
#   docker run --gpus all my-cuda-app
#
# Multi-arch note: CUDA images are x86_64/amd64 only. ARM GPU compute
# (e.g., Jetson) uses different base images (nvcr.io/nvidia/l4t-pytorch).
# ==============================================================================

# --- Build Arguments ---------------------------------------------------------
ARG CUDA_VERSION=12.4.1
ARG PYTHON_VERSION=3.12
ARG UBUNTU_VERSION=ubuntu22.04

# ==============================================================================
# Stage 1: Builder
# Uses the devel image which includes nvcc and CUDA/cuDNN headers.
# This stage installs Python dependencies and compiles any CUDA extensions.
# ==============================================================================
FROM nvidia/cuda:${CUDA_VERSION}-cudnn-devel-${UBUNTU_VERSION} AS builder

# Install Python and build tools.
# python3-dev is needed for compiling Python C extensions.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-dev \
        python3-venv \
        build-essential \
        git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create a virtual environment for clean dependency isolation.
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install PyTorch with CUDA support.
# The --index-url points to PyTorch's CUDA-specific wheel repository.
# This ensures we get GPU-enabled wheels, not CPU-only ones.
#
# Why install PyTorch first (before copying source):
#   PyTorch + dependencies are ~2 GB. Installing them in a separate layer
#   means they are cached and not re-downloaded on every source code change.
RUN pip install --no-cache-dir \
    torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cu124

# Copy dependency specification and install project dependencies.
# This layer is cached until pyproject.toml or requirements change.
COPY pyproject.toml requirements.txt* ./
RUN if [ -f requirements.txt ]; then \
        pip install --no-cache-dir -r requirements.txt; \
    else \
        pip install --no-cache-dir .; \
    fi

# Copy the application source code.
COPY . .

# Install the project itself (if it is a Python package).
# Use --no-deps to avoid re-resolving dependencies.
RUN pip install --no-cache-dir --no-deps .

# ==============================================================================
# Stage 2: Runtime
# Uses the smaller cudnn-runtime image. No compilers, no headers, no pip cache.
# cuDNN runtime libs are included for inference and training.
#
# Why cudnn-runtime and not base:
#   - base (~120 MB): Only CUDA runtime. No cuDNN. Cannot run DNN models.
#   - runtime (~800 MB): CUDA runtime + math libs. No cuDNN.
#   - cudnn-runtime (~1.5 GB): Includes cuDNN shared libs. Required for
#     PyTorch/TensorFlow convolutions, attention, and other DNN ops.
# ==============================================================================
FROM nvidia/cuda:${CUDA_VERSION}-cudnn-runtime-${UBUNTU_VERSION} AS runtime

# Install only the Python runtime (no pip, no dev headers).
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the virtual environment from the builder stage.
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application source code.
COPY --from=builder /app /app

# Set environment variables for optimal GPU behavior.
#
# PYTHONUNBUFFERED: Ensures print() output appears immediately in Docker logs.
# PYTHONDONTWRITEBYTECODE: Avoids .pyc files in the container.
# TORCH_CUDA_ARCH_LIST: Optional -- set to your target GPU architecture
#   to avoid JIT compilation overhead. Common values:
#   "7.0" (V100), "8.0" (A100), "8.9" (L40/4090), "9.0" (H100)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Create a non-root user.
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --create-home --shell /bin/false appuser && \
    chown -R 1001:1001 /app

USER 1001

# Expose port if this is a serving application (e.g., model API).
# Remove if this is a batch training job.
EXPOSE 8000

# Health check for serving applications. Remove for batch jobs.
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# OCI metadata labels. Update for your project.
LABEL org.opencontainers.image.title="my-cuda-app" \
      org.opencontainers.image.description="GPU-accelerated application with PyTorch and CUDA" \
      org.opencontainers.image.source="https://github.com/org/repo" \
      org.opencontainers.image.licenses="MIT"

# Use exec form for proper signal handling (graceful shutdown).
ENTRYPOINT ["python3", "-m", "myapp"]
CMD ["--host", "0.0.0.0", "--port", "8000"]

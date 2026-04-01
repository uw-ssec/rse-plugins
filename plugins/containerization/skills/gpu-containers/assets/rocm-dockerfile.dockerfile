# ==============================================================================
# ROCm Dockerfile with PyTorch
#
# Builds a GPU-accelerated application using AMD ROCm and PyTorch.
# ROCm containers use a different device model than NVIDIA:
#   - No --gpus flag. Instead, map /dev/kfd and /dev/dri explicitly.
#   - PyTorch uses torch.cuda.* API with HIP backend (transparent to user code).
#
# Device Mapping:
#   /dev/kfd   -- Kernel Fusion Driver, required for all GPU compute
#   /dev/dri   -- Direct Rendering Infrastructure, contains per-GPU render nodes
#   --group-add video -- Grants access to GPU device nodes
#
# Usage:
#   docker build -t my-rocm-app .
#   docker run --device=/dev/kfd --device=/dev/dri --group-add video my-rocm-app
#
# Multi-GPU:
#   docker run --device=/dev/kfd --device=/dev/dri --group-add video \
#     -e HIP_VISIBLE_DEVICES=0,1 my-rocm-app
#
# Specific GPU only:
#   docker run --device=/dev/kfd --device=/dev/dri/renderD128 \
#     --group-add video my-rocm-app
# ==============================================================================

# --- Build Arguments ---------------------------------------------------------
ARG ROCM_VERSION=6.1

# ==============================================================================
# Stage 1: Builder
# Uses the ROCm dev image which includes compilers and development headers.
# This stage installs Python dependencies and builds any HIP/ROCm extensions.
# ==============================================================================
FROM rocm/dev-ubuntu-22.04:${ROCM_VERSION} AS builder

# Install Python and build tools.
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

# Create virtual environment.
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install PyTorch with ROCm support.
#
# The --index-url points to PyTorch's ROCm-specific wheel repository.
# This installs PyTorch compiled against ROCm/HIP instead of CUDA.
# Despite the "cuda" in the API names (torch.cuda.*), the HIP backend
# translates all calls to ROCm automatically. User code does not change.
RUN pip install --no-cache-dir \
    torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/rocm6.1

# Copy and install project dependencies.
COPY pyproject.toml requirements.txt* ./
RUN if [ -f requirements.txt ]; then \
        pip install --no-cache-dir -r requirements.txt; \
    else \
        pip install --no-cache-dir .; \
    fi

# Copy application source.
COPY . .

# Install the project.
RUN pip install --no-cache-dir --no-deps .

# ==============================================================================
# Stage 2: Runtime
# Uses the same ROCm dev image (ROCm does not publish slim runtime images
# like NVIDIA does). The full image is larger but ensures all ROCm libs
# are available at runtime.
#
# Note: ROCm images are typically larger than NVIDIA equivalents (~5-15 GB).
# This is an inherent characteristic of the ROCm software stack.
# ==============================================================================
FROM rocm/dev-ubuntu-22.04:${ROCM_VERSION} AS runtime

# Install Python runtime.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy virtual environment and application from builder.
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY --from=builder /app /app

# Environment variables.
#
# PYTHONUNBUFFERED: Immediate output in Docker logs.
# HSA_OVERRIDE_GFX_VERSION: Uncomment and set if your GPU architecture
#   is not officially supported by the installed ROCm version.
#   Example: "10.3.0" for gfx1030 (RX 6800/6900 series).
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
    # HSA_OVERRIDE_GFX_VERSION=10.3.0

# Create non-root user.
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --create-home --shell /bin/false appuser && \
    chown -R 1001:1001 /app

# Add user to video group for GPU device access.
# This is the in-container equivalent of --group-add video.
RUN usermod -aG video appuser

USER 1001

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

LABEL org.opencontainers.image.title="my-rocm-app" \
      org.opencontainers.image.description="GPU-accelerated application with PyTorch and ROCm" \
      org.opencontainers.image.source="https://github.com/org/repo" \
      org.opencontainers.image.licenses="MIT"

ENTRYPOINT ["python3", "-m", "myapp"]
CMD ["--host", "0.0.0.0", "--port", "8000"]

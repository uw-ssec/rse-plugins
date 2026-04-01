---
name: gpu-containers
description: GPU-enabled container configuration for NVIDIA CUDA and AMD ROCm workloads including driver compatibility, runtime setup, multi-GPU, and framework-specific images for PyTorch and TensorFlow.
metadata:
  references:
    - references/nvidia-cuda-setup.md
    - references/amd-rocm-setup.md
  assets:
    - assets/cuda-dockerfile.dockerfile
    - assets/rocm-dockerfile.dockerfile
---

# GPU Containers

A comprehensive guide to running GPU-accelerated workloads in containers for research computing. This skill covers NVIDIA CUDA and AMD ROCm container setup, driver compatibility, base image selection, framework-specific images for PyTorch, TensorFlow, and JAX, multi-GPU configuration, and Docker Compose integration. GPU containers are essential for machine learning training, scientific simulation, and any compute-intensive workload that benefits from hardware acceleration.

## Resources in This Skill

This skill includes supporting materials for GPU container tasks:

**References** (detailed guides -- consult the table of contents in each file and read specific sections as needed):
- `references/nvidia-cuda-setup.md` - NVIDIA CUDA setup: nvidia-container-toolkit installation, CUDA version matrix, base image variants (base/runtime/devel), cuDNN and NCCL integration, multi-GPU with CUDA_VISIBLE_DEVICES, profiling in containers, and driver compatibility
- `references/amd-rocm-setup.md` - AMD ROCm setup: ROCm installation, amdgpu driver, ROCm Docker images, HIP compatibility layer, device mapping, and ROCm version matrix

**Assets** (ready-to-use Dockerfile templates):
- `assets/cuda-dockerfile.dockerfile` - Multi-stage CUDA Dockerfile with PyTorch, optimized layer ordering, and commented CUDA/cuDNN choices
- `assets/rocm-dockerfile.dockerfile` - ROCm Dockerfile with PyTorch, device mapping instructions, and HIP compatibility notes

## Quick Reference Card

### CUDA Version Compatibility

| CUDA Version | Minimum Driver | PyTorch | TensorFlow |
|-------------|----------------|---------|------------|
| CUDA 12.4 | 550.54+ | 2.4+ | 2.16+ |
| CUDA 12.1 | 530.30+ | 2.1+ | 2.14+ |
| CUDA 11.8 | 520.61+ | 2.0+ | 2.12+ |
| CUDA 11.7 | 515.43+ | 1.13+ | 2.11+ |

### Quick GPU Check

```bash
# Verify GPU is visible from host
nvidia-smi

# Run a container with GPU access
docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi

# Run with specific GPUs
docker run --rm --gpus '"device=0,1"' nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi

# Run with AMD GPU
docker run --rm --device=/dev/kfd --device=/dev/dri \
  rocm/pytorch:latest rocm-smi
```

### NVIDIA Container Toolkit Install (Quick)

```bash
# Ubuntu/Debian
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
  sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

## When to Use

Use this skill when you need to:

- Run NVIDIA GPU workloads (CUDA) inside Docker containers
- Run AMD GPU workloads (ROCm) inside Docker containers
- Choose the right CUDA base image variant (base, runtime, or devel)
- Build Dockerfiles for PyTorch, TensorFlow, or JAX with GPU support
- Configure multi-GPU access for distributed training
- Set up Docker Compose services with GPU resources
- Debug GPU access issues inside containers (driver mismatch, device not found)
- Profile GPU workloads inside containers
- Run GPU containers on HPC clusters (cross-reference the singularity-apptainer skill)

## NVIDIA CUDA Setup

### nvidia-container-toolkit

The NVIDIA Container Toolkit is the bridge between Docker and your NVIDIA GPUs. It must be installed on the host (not in the container).

**What it provides:**
- `--gpus` flag for `docker run`
- Automatic mounting of GPU drivers into containers
- CUDA library injection so containers do not need to bundle host drivers

**Verify installation:**
```bash
# Check the toolkit is configured
nvidia-ctk --version

# Test GPU access in a container
docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi
```

If `nvidia-smi` inside the container shows your GPUs, the toolkit is working.

See `references/nvidia-cuda-setup.md` for full installation instructions and troubleshooting.

### Driver Compatibility

The host NVIDIA driver must be compatible with the CUDA version used in the container. The NVIDIA Container Toolkit handles forward compatibility (newer driver with older CUDA), but the driver must meet the minimum version for the CUDA toolkit in the container.

**Rule of thumb:** Keep host drivers up to date. A driver from the 550+ series supports all CUDA 12.x containers.

```bash
# Check host driver version
nvidia-smi --query-gpu=driver_version --format=csv,noheader
```

## AMD ROCm Setup

### amdgpu Driver and ROCm Runtime

AMD GPU containers require the `amdgpu` kernel driver on the host and pass devices via `--device` flags (not `--gpus`).

```bash
# Verify AMD GPU on host
rocm-smi

# Run a container with AMD GPU
docker run --rm \
  --device=/dev/kfd \
  --device=/dev/dri \
  --group-add video \
  rocm/pytorch:latest \
  python -c "import torch; print(torch.cuda.is_available())"
```

**Required device mappings:**
- `/dev/kfd` -- Kernel Fusion Driver (compute)
- `/dev/dri` -- Direct Rendering Infrastructure (GPU access)

See `references/amd-rocm-setup.md` for installation and version compatibility.

## Base Image Selection

### NVIDIA CUDA Image Variants

NVIDIA provides three variants of each CUDA version:

| Variant | Contents | Size (approx.) | Use Case |
|---------|----------|-----------------|----------|
| `base` | CUDA runtime only | ~120 MB | Running pre-compiled CUDA apps |
| `runtime` | CUDA runtime + cuDNN | ~1.5 GB | Running ML inference |
| `devel` | runtime + headers + compilers | ~3.5 GB | Compiling CUDA code, building extensions |

```dockerfile
# For inference (no compilation needed)
FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04

# For training with cuDNN (most ML workloads)
FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04

# For compiling custom CUDA extensions
FROM nvidia/cuda:12.4.1-devel-ubuntu22.04
```

**Multi-stage pattern:** Use `devel` to compile, then copy artifacts to `runtime`:

```dockerfile
FROM nvidia/cuda:12.4.1-devel-ubuntu22.04 AS builder
# ... compile CUDA code ...

FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04
COPY --from=builder /app/build/myapp /usr/local/bin/myapp
```

### AMD ROCm Images

```dockerfile
# ROCm base
FROM rocm/dev-ubuntu-22.04:6.1

# ROCm with PyTorch pre-installed
FROM rocm/pytorch:latest

# ROCm with TensorFlow pre-installed
FROM rocm/tensorflow:latest
```

## Framework Images

### PyTorch

**NVIDIA (NGC container):**
```dockerfile
# Pre-built PyTorch with CUDA, cuDNN, NCCL
FROM nvcr.io/nvidia/pytorch:24.04-py3
```

**Custom build with CUDA:**
```dockerfile
FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

**AMD ROCm:**
```dockerfile
FROM rocm/pytorch:latest
# Or install manually
FROM rocm/dev-ubuntu-22.04:6.1
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.1
```

See `assets/cuda-dockerfile.dockerfile` and `assets/rocm-dockerfile.dockerfile` for complete templates.

### TensorFlow

**NVIDIA:**
```dockerfile
# Official TensorFlow GPU image
FROM tensorflow/tensorflow:2.16.1-gpu

# Or NGC container with optimizations
FROM nvcr.io/nvidia/tensorflow:24.04-tf2-py3
```

**AMD ROCm:**
```dockerfile
FROM rocm/tensorflow:latest
```

### JAX

**NVIDIA:**
```dockerfile
FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04
RUN pip install --upgrade "jax[cuda12]"
```

**AMD ROCm:**
```dockerfile
FROM rocm/dev-ubuntu-22.04:6.1
RUN pip install --upgrade "jax[rocm]" -f https://storage.googleapis.com/jax-releases/rocm/jaxlib-latest.html
```

## Multi-GPU Configuration

### Selecting GPUs

Control which GPUs a container can access:

```bash
# All GPUs
docker run --gpus all myapp

# Specific GPUs by index
docker run --gpus '"device=0,2"' myapp

# Specific GPUs by UUID
docker run --gpus '"device=GPU-abc123,GPU-def456"' myapp
```

### CUDA_VISIBLE_DEVICES

Inside the container, use `CUDA_VISIBLE_DEVICES` to further restrict GPU visibility for multi-process workloads:

```bash
# In Docker run
docker run --gpus all -e CUDA_VISIBLE_DEVICES=0,1 myapp

# In Dockerfile
ENV CUDA_VISIBLE_DEVICES=0,1
```

### Distributed Training

For multi-GPU training with PyTorch DDP or Horovod, all GPUs must be visible to the container:

```bash
docker run --gpus all \
  --ipc=host \
  --ulimit memlock=-1 \
  --ulimit stack=67108864 \
  myapp torchrun --nproc_per_node=4 train.py
```

**Key flags for distributed training:**
- `--ipc=host` -- shared memory for inter-process communication (required for PyTorch DataLoader with `num_workers > 0`)
- `--ulimit memlock=-1` -- allow unlimited locked memory (required for NCCL)
- `--ulimit stack=67108864` -- increase stack size for deep models
- `--shm-size=8g` -- alternative to `--ipc=host` for controlling shared memory size

## Docker Compose with GPU

### NVIDIA GPU in Compose

```yaml
services:
  training:
    build: .
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all        # or a specific number: 1, 2
              capabilities: [gpu]
    volumes:
      - ./data:/app/data
    ipc: host
    ulimits:
      memlock: -1
      stack: 67108864
```

### Specific GPUs in Compose

```yaml
services:
  model-a:
    build: .
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              device_ids: ['0']
              capabilities: [gpu]

  model-b:
    build: .
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              device_ids: ['1']
              capabilities: [gpu]
```

### AMD GPU in Compose

```yaml
services:
  training:
    build: .
    devices:
      - /dev/kfd:/dev/kfd
      - /dev/dri:/dev/dri
    group_add:
      - video
```

## Testing GPU Access

### Verification Commands

```bash
# NVIDIA: check GPU visibility
docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi

# NVIDIA: check CUDA version
docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 \
  nvcc --version 2>/dev/null || echo "nvcc not in base image, use devel variant"

# PyTorch GPU check
docker run --rm --gpus all my-pytorch-image \
  python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}, Devices: {torch.cuda.device_count()}')"

# TensorFlow GPU check
docker run --rm --gpus all my-tf-image \
  python -c "import tensorflow as tf; print(f'GPUs: {tf.config.list_physical_devices(\"GPU\")}')"

# AMD: check ROCm
docker run --rm --device=/dev/kfd --device=/dev/dri rocm/pytorch:latest rocm-smi
```

### Common Failures and Fixes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `--gpus` flag unknown | nvidia-container-toolkit not installed | Install the toolkit |
| `nvidia-smi` not found | Wrong base image variant | Use `runtime` or `devel` variant |
| `no CUDA-capable device` | Driver too old for CUDA version | Update host driver |
| CUDA OOM | GPU memory exhausted | Reduce batch size, use gradient checkpointing |
| `shared memory` error | IPC namespace isolated | Add `--ipc=host` or `--shm-size=8g` |

## HPC GPU Containers

For running GPU containers on HPC clusters with Singularity/Apptainer, GPU passthrough works differently than Docker. Singularity automatically binds NVIDIA drivers from the host.

```bash
# Convert Docker image to Singularity
singularity pull docker://nvcr.io/nvidia/pytorch:24.04-py3

# Run with GPU
singularity run --nv pytorch_24.04-py3.sif python train.py

# Apptainer (Singularity successor)
apptainer run --nv pytorch_24.04-py3.sif python train.py
```

See the **singularity-apptainer** skill for complete HPC container guidance.

## Common Mistakes

1. **Installing NVIDIA drivers inside the container** -- The nvidia-container-toolkit injects host drivers at runtime. Installing drivers in the container causes conflicts.

2. **Using the wrong CUDA base image variant** -- `base` does not include cuDNN. Use `runtime` for inference or `devel` for compiling CUDA extensions.

3. **CUDA version mismatch with host driver** -- The container's CUDA version must be compatible with the host's NVIDIA driver. Check the compatibility matrix.

4. **Forgetting `--ipc=host` for training** -- PyTorch DataLoader with multiple workers requires shared memory. Without `--ipc=host` or `--shm-size`, training crashes with bus errors.

5. **Not pinning CUDA versions** -- Using `nvidia/cuda:latest` can break builds when CUDA updates. Pin to specific versions like `12.4.1`.

6. **Using `devel` images in production** -- The `devel` variant includes compilers and headers (~3.5 GB). Use multi-stage builds to compile in `devel` and run in `runtime`.

7. **Ignoring GPU memory limits** -- Unlike CPU containers, GPU memory is not limited by Docker. A single container can consume all GPU memory, starving other containers.

8. **AMD: forgetting device flags** -- AMD GPUs require `--device=/dev/kfd --device=/dev/dri` and `--group-add video`. There is no `--gpus` equivalent for ROCm.

## Best Practices

- [ ] Install nvidia-container-toolkit on the host, never install drivers in containers
- [ ] Pin CUDA and cuDNN versions in your Dockerfile for reproducibility
- [ ] Use multi-stage builds: compile in `devel`, run in `runtime`
- [ ] Verify GPU access with `nvidia-smi` and framework checks before running workloads
- [ ] Use `--ipc=host` or `--shm-size=8g` for PyTorch training workloads
- [ ] Set `CUDA_VISIBLE_DEVICES` to control GPU allocation in multi-GPU systems
- [ ] Use NGC containers (`nvcr.io/nvidia/pytorch`) for optimized framework builds
- [ ] Test on the same CUDA version locally that your production/HPC cluster runs
- [ ] Document minimum driver version requirements in your README
- [ ] For AMD GPUs, always map both `/dev/kfd` and `/dev/dri` devices
- [ ] Use Docker Compose `deploy.resources.reservations.devices` for declarative GPU access
- [ ] Monitor GPU memory usage with `nvidia-smi` or `nvitop` during development

## Resources

### Official Documentation
- **NVIDIA Container Toolkit**: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/
- **NVIDIA CUDA Docker Hub**: https://hub.docker.com/r/nvidia/cuda
- **NVIDIA NGC Catalog**: https://catalog.ngc.nvidia.com/
- **AMD ROCm Docker**: https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/docker.html

### Framework Images
- **PyTorch NGC**: https://catalog.ngc.nvidia.com/orgs/nvidia/containers/pytorch
- **TensorFlow Docker**: https://www.tensorflow.org/install/docker
- **JAX Installation**: https://jax.readthedocs.io/en/latest/installation.html

### Compatibility
- **CUDA Compatibility Matrix**: https://docs.nvidia.com/deploy/cuda-compatibility/
- **cuDNN Support Matrix**: https://docs.nvidia.com/deeplearning/cudnn/support-matrix/
- **ROCm Compatibility**: https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html

### Tools
- **nvitop** (GPU monitoring): https://github.com/XuehaiPan/nvitop
- **gpustat**: https://github.com/wookayin/gpustat

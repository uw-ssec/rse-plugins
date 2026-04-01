# NVIDIA CUDA Setup -- Deep Reference

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| nvidia-container-toolkit Installation | 17-100 | Installation for Ubuntu, RHEL, SUSE, and verification steps |
| CUDA Version Matrix | 102-159 | CUDA to driver version mapping, forward compatibility rules |
| Base Image Variants | 161-238 | base, runtime, devel variants with size and use case comparisons |
| cuDNN and NCCL | 240-308 | cuDNN installation, NCCL for multi-GPU, version selection |
| Multi-GPU with CUDA_VISIBLE_DEVICES | 310-385 | GPU selection, isolation, per-container assignment |
| Profiling in Containers | 387-455 | nsight, nvprof, dcgm-exporter, monitoring tools |
| Driver Compatibility | 457-523 | Forward and backward compatibility, minor version compat, troubleshooting |

---

## nvidia-container-toolkit Installation

### Ubuntu / Debian

```bash
# 1. Add the NVIDIA GPG key
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
  sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

# 2. Add the repository
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# 3. Install
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# 4. Configure Docker runtime
sudo nvidia-ctk runtime configure --runtime=docker

# 5. Restart Docker
sudo systemctl restart docker
```

### RHEL / CentOS / Fedora

```bash
# 1. Add the repository
curl -s -L https://nvidia.github.io/libnvidia-container/stable/rpm/nvidia-container-toolkit.repo | \
  sudo tee /etc/yum.repos.d/nvidia-container-toolkit.repo

# 2. Install
sudo dnf install -y nvidia-container-toolkit

# 3. Configure Docker runtime
sudo nvidia-ctk runtime configure --runtime=docker

# 4. Restart Docker
sudo systemctl restart docker
```

### SUSE / openSUSE

```bash
# 1. Add the repository
sudo zypper ar https://nvidia.github.io/libnvidia-container/stable/rpm/nvidia-container-toolkit.repo

# 2. Install
sudo zypper install -y nvidia-container-toolkit

# 3. Configure and restart
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

### Verification

After installation, verify the toolkit works:

```bash
# Check toolkit version
nvidia-ctk --version

# Verify Docker runtime configuration
# Look for "nvidia" in the runtimes section
docker info | grep -i nvidia

# Run a test container
docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi

# Expected output: a table showing your GPU(s) with driver and CUDA version
```

### Troubleshooting Installation

| Issue | Solution |
|-------|----------|
| `--gpus` flag not recognized | Restart Docker after toolkit install: `sudo systemctl restart docker` |
| `nvidia-container-cli: initialization error` | Check that NVIDIA driver is loaded: `lsmod \| grep nvidia` |
| Permission denied on GPU devices | Add user to `docker` group: `sudo usermod -aG docker $USER` |
| Toolkit installed but not used | Check `/etc/docker/daemon.json` for `nvidia` runtime entry |

---

## CUDA Version Matrix

### CUDA to Minimum Driver Version

| CUDA Toolkit | Minimum Linux Driver | Minimum Windows Driver |
|-------------|---------------------|----------------------|
| CUDA 12.6 | 560.28+ | 560.70+ |
| CUDA 12.5 | 555.42+ | 555.85+ |
| CUDA 12.4 | 550.54+ | 551.61+ |
| CUDA 12.3 | 545.23+ | 546.01+ |
| CUDA 12.2 | 535.54+ | 536.25+ |
| CUDA 12.1 | 530.30+ | 531.14+ |
| CUDA 12.0 | 525.60+ | 527.41+ |
| CUDA 11.8 | 520.61+ | 522.06+ |
| CUDA 11.7 | 515.43+ | 516.01+ |

### Forward Compatibility

The NVIDIA Container Toolkit supports **forward compatibility**: a newer host driver can run containers with older CUDA versions. This means:

- Host driver 550.x can run CUDA 12.4, 12.3, 12.2, ..., 11.x containers
- Host driver 535.x can run CUDA 12.2 and older containers
- A container with CUDA 12.4 **cannot** run on a host with driver 530.x

**Best practice:** Keep host drivers on the latest stable release to maximize container compatibility.

### CUDA Toolkit Components in Containers

The CUDA toolkit in a container includes:
- **CUDA Runtime** (`libcudart.so`): Core CUDA execution library
- **cuBLAS**: GPU-accelerated linear algebra
- **cuFFT**: GPU-accelerated FFT
- **cuRAND**: GPU-accelerated random number generation
- **cuSPARSE**: GPU-accelerated sparse matrix operations
- **cuSOLVER**: GPU-accelerated factorization and solve
- **nvJPEG**: GPU-accelerated JPEG decode

The host driver provides:
- **CUDA Driver API** (`libcuda.so`): Automatically injected by nvidia-container-toolkit
- **NVML** (`libnvidia-ml.so`): GPU management and monitoring

### Checking Versions

```bash
# Host driver version
nvidia-smi --query-gpu=driver_version --format=csv,noheader

# CUDA version supported by driver
nvidia-smi | head -3  # Shows CUDA version in top-right

# CUDA toolkit version in container
nvcc --version  # Only available in devel images

# Runtime CUDA version
python -c "import torch; print(torch.version.cuda)"
```

---

## Base Image Variants

### Overview

NVIDIA publishes CUDA images on Docker Hub under `nvidia/cuda`. Each CUDA version has three variants:

```
nvidia/cuda:<version>-base-<os>
nvidia/cuda:<version>-runtime-<os>
nvidia/cuda:<version>-devel-<os>
```

With optional cuDNN suffix:
```
nvidia/cuda:<version>-cudnn-runtime-<os>
nvidia/cuda:<version>-cudnn-devel-<os>
```

### Variant Comparison

| Variant | Contains | Size | Use Case |
|---------|----------|------|----------|
| `base` | CUDA runtime libraries only | ~120 MB | Run pre-compiled CUDA binaries |
| `runtime` | base + CUDA math libraries | ~800 MB | Run ML inference, scientific computing |
| `cudnn-runtime` | runtime + cuDNN | ~1.5 GB | Run DNN inference (PyTorch, TF) |
| `devel` | runtime + compilers + headers | ~3.5 GB | Compile CUDA code, build PyTorch extensions |
| `cudnn-devel` | devel + cuDNN headers | ~4.0 GB | Compile code using cuDNN APIs |

### Choosing a Variant

**Use `base` when:**
- Running a pre-compiled binary that links against CUDA runtime
- Image size is the top priority
- No deep learning frameworks needed

**Use `runtime` or `cudnn-runtime` when:**
- Running inference with PyTorch, TensorFlow, or other frameworks
- No CUDA compilation needed at build time
- You install frameworks via pip (pre-built wheels include their own CUDA libs)

**Use `devel` or `cudnn-devel` when:**
- Compiling custom CUDA kernels or extensions
- Building PyTorch/TensorFlow from source
- Using `nvcc` compiler
- Building C/C++ code that links against CUDA

### Multi-Stage Pattern

Compile in `devel`, run in `runtime`:

```dockerfile
# Stage 1: Build with full CUDA development tools
FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04 AS builder
RUN apt-get update && apt-get install -y python3-dev python3-pip
WORKDIR /app
COPY . .
RUN pip install --prefix=/install .

# Stage 2: Run with minimal runtime
FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04
RUN apt-get update && apt-get install -y python3 && rm -rf /var/lib/apt/lists/*
COPY --from=builder /install /usr/local
COPY --from=builder /app /app
WORKDIR /app
USER 1001
ENTRYPOINT ["python3", "-m", "myapp"]
```

### OS Base Options

| OS Tag | Base | Python | Notes |
|--------|------|--------|-------|
| `ubuntu22.04` | Ubuntu 22.04 LTS | 3.10 | Most common, widest support |
| `ubuntu24.04` | Ubuntu 24.04 LTS | 3.12 | Latest LTS |
| `rockylinux9` | Rocky Linux 9 | 3.9 | RHEL-compatible |
| `ubi9` | Red Hat UBI 9 | 3.9 | Certified for Red Hat environments |

---

## cuDNN and NCCL

### cuDNN (CUDA Deep Neural Network Library)

cuDNN provides GPU-accelerated primitives for deep neural networks: convolutions, pooling, normalization, activation, and RNN/LSTM operations.

**When you need cuDNN:**
- Running or training any deep learning model with PyTorch or TensorFlow
- Using convolutional neural networks
- Using transformers (attention operations use cuDNN)

**Image selection:**
```dockerfile
# cuDNN included in the image
FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04

# Without cuDNN (for non-DL CUDA workloads)
FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04
```

**cuDNN version check:**
```bash
# In a cudnn-devel container
cat /usr/include/cudnn_version.h | grep CUDNN_MAJOR -A 2

# With Python
python -c "import torch; print(torch.backends.cudnn.version())"
```

### cuDNN Version Compatibility

| cuDNN | CUDA | PyTorch | TensorFlow |
|-------|------|---------|------------|
| 9.x | 12.x | 2.4+ | 2.16+ |
| 8.9 | 12.x, 11.x | 2.0-2.3 | 2.12-2.15 |
| 8.6 | 11.x | 1.12-1.13 | 2.9-2.11 |

### NCCL (NVIDIA Collective Communications Library)

NCCL provides multi-GPU and multi-node collective operations (all-reduce, broadcast, reduce-scatter) optimized for NVIDIA GPUs.

**When you need NCCL:**
- Distributed training across multiple GPUs
- Multi-node training
- Any use of PyTorch DDP, DeepSpeed, or Horovod

**Installation in containers:**
```dockerfile
FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04

# NCCL is often included in devel images, but you can install explicitly:
RUN apt-get update && \
    apt-get install -y libnccl2 libnccl-dev && \
    rm -rf /var/lib/apt/lists/*
```

**NCCL environment variables for multi-GPU:**
```bash
# Use all available NICs for inter-node communication
export NCCL_SOCKET_IFNAME=eth0

# Enable debug logging
export NCCL_DEBUG=INFO

# Use NVLink when available
export NCCL_P2P_LEVEL=NVL
```

---

## Multi-GPU with CUDA_VISIBLE_DEVICES

### GPU Selection Methods

**Method 1: Docker `--gpus` flag (recommended)**
```bash
# All GPUs
docker run --gpus all myapp

# First two GPUs
docker run --gpus 2 myapp

# Specific GPUs by index
docker run --gpus '"device=0,2"' myapp

# Specific GPUs by UUID
docker run --gpus '"device=GPU-abc123"' myapp
```

**Method 2: CUDA_VISIBLE_DEVICES environment variable**
```bash
# Restrict to GPUs 0 and 1
docker run --gpus all -e CUDA_VISIBLE_DEVICES=0,1 myapp
```

**Method 3: NVIDIA_VISIBLE_DEVICES (lower level)**
```bash
docker run -e NVIDIA_VISIBLE_DEVICES=0,1 myapp
```

### GPU Isolation Patterns

**One GPU per container (resource isolation):**
```bash
# Container A gets GPU 0
docker run --gpus '"device=0"' -d myapp-a

# Container B gets GPU 1
docker run --gpus '"device=1"' -d myapp-b
```

**All GPUs for distributed training:**
```bash
docker run --gpus all --ipc=host myapp \
  torchrun --nproc_per_node=$(nvidia-smi -L | wc -l) train.py
```

### GPU Indexing

Inside the container, GPUs are always re-indexed starting from 0, regardless of which host GPUs are mapped:

```bash
# Host has 4 GPUs (0,1,2,3)
# Container sees device=2,3 as device 0,1
docker run --gpus '"device=2,3"' myapp \
  python -c "import torch; print(torch.cuda.device_count())"  # prints 2
```

### Querying GPU Information

```bash
# List all GPUs
nvidia-smi -L

# Query specific properties
nvidia-smi --query-gpu=index,name,memory.total,memory.used,utilization.gpu \
  --format=csv

# Monitor GPU usage continuously
watch -n 1 nvidia-smi

# Or use nvitop for a better TUI
pip install nvitop && nvitop
```

---

## Profiling in Containers

### NVIDIA Nsight Systems

Profile GPU and CPU activity, kernel launches, memory transfers:

```bash
docker run --rm --gpus all \
  --cap-add SYS_ADMIN \
  nvidia/cuda:12.4.1-devel-ubuntu22.04 \
  nsys profile --output report python train.py
```

**Key flags:**
- `--cap-add SYS_ADMIN`: Required for hardware performance counters
- `nsys profile --trace=cuda,nvtx,osrt`: Trace CUDA, NVTX markers, and OS runtime

### NVIDIA Nsight Compute

Profile individual CUDA kernels in detail:

```bash
docker run --rm --gpus all \
  --cap-add SYS_ADMIN \
  nvidia/cuda:12.4.1-devel-ubuntu22.04 \
  ncu --set full python train.py
```

### dcgm-exporter (Monitoring)

Run DCGM exporter as a sidecar container for Prometheus metrics:

```yaml
services:
  dcgm-exporter:
    image: nvcr.io/nvidia/k8s/dcgm-exporter:3.3.5-3.4.1-ubuntu22.04
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    ports:
      - "9400:9400"
```

### PyTorch Profiler in Containers

```python
import torch
from torch.profiler import profile, record_function, ProfilerActivity

with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA]) as prof:
    with record_function("training_step"):
        output = model(input)
        loss = criterion(output, target)
        loss.backward()

print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=10))
prof.export_chrome_trace("trace.json")
```

Mount a volume to retrieve profiling output:
```bash
docker run --gpus all -v ./profiles:/app/profiles myapp
```

---

## Driver Compatibility

### Forward Compatibility (Newer Driver, Older CUDA)

This always works. A host with driver 550.x can run containers using CUDA 12.4, 12.3, 12.0, 11.8, and earlier. The NVIDIA Container Toolkit handles library version negotiation.

### Backward Compatibility (Older Driver, Newer CUDA)

This does **not** work by default. A container with CUDA 12.4 cannot run on a host with driver 525.x (which only supports up to CUDA 12.0).

**CUDA Forward Compatibility Package:** NVIDIA provides a forward compat package that allows newer CUDA toolkit versions to run on older drivers within certain bounds. This is pre-installed in NGC containers.

```bash
# Check if forward compat is available
ls /usr/local/cuda/compat/
```

### Minor Version Compatibility

Within a CUDA major version (e.g., 12.x), minor version compatibility is guaranteed. A binary compiled with CUDA 12.1 runs on a system with CUDA 12.4 drivers.

### Diagnosing Driver Issues

```bash
# Check host driver
nvidia-smi

# Check CUDA version supported by driver (top-right of nvidia-smi output)
# This is the MAXIMUM CUDA version the driver supports

# Inside container, check what CUDA runtime is installed
nvcc --version  # devel images only

# Check if driver is too old for the container's CUDA
# Error: "CUDA driver version is insufficient for CUDA runtime version"
# Solution: update host driver or use an older CUDA base image

# Check driver module is loaded
lsmod | grep nvidia

# Check GPU device files exist
ls -la /dev/nvidia*
```

### Common Driver Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `CUDA driver version is insufficient` | Host driver too old | Update host NVIDIA driver |
| `no CUDA-capable device is detected` | GPU not visible | Check `--gpus` flag, verify driver |
| `CUDA initialization: unexpected error` | Driver/toolkit mismatch | Reinstall nvidia-container-toolkit |
| `nvml: driver not loaded` | Driver module not loaded | `sudo modprobe nvidia` or reboot |
| `all CUDA-capable devices are busy` | GPU in exclusive mode | Check `nvidia-smi -c` compute mode |

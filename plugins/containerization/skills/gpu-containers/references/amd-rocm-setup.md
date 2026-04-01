# AMD ROCm Setup -- Deep Reference

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| ROCm Installation | 16-86 | Host-side ROCm stack installation for Ubuntu and RHEL |
| amdgpu Driver | 88-143 | Kernel driver installation, verification, DKMS setup |
| ROCm Docker Images | 145-223 | Official images, framework images, image variants |
| HIP Compatibility | 225-293 | HIP programming model, CUDA portability, hipify tools |
| Device Mapping | 295-375 | Device flags, permissions, multi-GPU selection |
| ROCm Version Matrix | 377-418 | ROCm to driver, PyTorch, and TensorFlow compatibility |

---

## ROCm Installation

### Ubuntu 22.04 / 24.04

Install the full ROCm stack on the host system. The container runtime uses the host kernel driver, but the ROCm user-space libraries can be either on the host or in the container.

```bash
# 1. Add the ROCm repository
sudo mkdir -p --mode=0755 /etc/apt/keyrings
wget https://repo.radeon.com/rocm/rocm.gpg.key -O - | \
  gpg --dearmor | sudo tee /etc/apt/keyrings/rocm.gpg > /dev/null

echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] \
  https://repo.radeon.com/rocm/apt/6.1 jammy main" | \
  sudo tee /etc/apt/sources.list.d/rocm.list

# 2. Pin ROCm packages (prefer ROCm repo over distro)
echo 'Package: *\nPin: release o=repo.radeon.com\nPin-Priority: 600' | \
  sudo tee /etc/apt/preferences.d/rocm-pin-600

# 3. Install ROCm
sudo apt-get update
sudo apt-get install -y rocm-dev

# 4. Add user to groups
sudo usermod -aG render,video $USER

# 5. Verify installation
rocm-smi
rocminfo
```

### RHEL / CentOS / Rocky Linux

```bash
# 1. Add repository
sudo tee /etc/yum.repos.d/rocm.repo <<EOF
[rocm]
name=ROCm
baseurl=https://repo.radeon.com/rocm/rhel9/6.1/main
enabled=1
gpgcheck=1
gpgkey=https://repo.radeon.com/rocm/rocm.gpg.key
EOF

# 2. Install
sudo dnf install -y rocm-dev

# 3. Add user to groups
sudo usermod -aG render,video $USER

# 4. Verify
rocm-smi
```

### Minimal Host Installation for Docker

If you only need GPU containers and do not develop on the host, install just the kernel driver and container essentials:

```bash
# Minimal install: driver + container support
sudo apt-get install -y amdgpu-dkms rocm-container-runtime

# Add user to groups
sudo usermod -aG render,video $USER

# Verify GPU is accessible
rocm-smi
```

---

## amdgpu Driver

### Kernel Driver Overview

The `amdgpu` kernel driver is the foundation of AMD GPU support on Linux. It provides:
- GPU device nodes (`/dev/dri/card*`, `/dev/dri/renderD*`)
- Kernel Fusion Driver (`/dev/kfd`) for compute operations
- Memory management and scheduling

### Installation via DKMS

DKMS (Dynamic Kernel Module Support) automatically rebuilds the driver when the kernel updates:

```bash
# Install the DKMS driver
sudo apt-get install -y amdgpu-dkms

# Verify the module is loaded
lsmod | grep amdgpu

# Check driver version
modinfo amdgpu | grep version

# If the module is not loaded, load it manually
sudo modprobe amdgpu
```

### Verification

```bash
# Check GPU devices exist
ls -la /dev/kfd
ls -la /dev/dri/

# Expected output:
# /dev/kfd             -- Kernel Fusion Driver (compute)
# /dev/dri/card0       -- Display device
# /dev/dri/renderD128  -- Render device

# Check GPU info with rocm-smi
rocm-smi

# Detailed GPU info
rocminfo | grep -E "Name|Marketing"
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| `/dev/kfd` not found | Load driver: `sudo modprobe amdgpu` |
| Permission denied on `/dev/kfd` | Add user to video/render groups: `sudo usermod -aG render,video $USER` |
| Driver version mismatch | Reinstall: `sudo apt install --reinstall amdgpu-dkms` |
| Kernel update broke driver | Rebuild DKMS: `sudo dkms autoinstall` |

---

## ROCm Docker Images

### Official ROCm Images

AMD publishes Docker images on Docker Hub under the `rocm/` namespace:

```bash
# Base ROCm development image
docker pull rocm/dev-ubuntu-22.04:6.1

# ROCm with PyTorch
docker pull rocm/pytorch:latest

# ROCm with TensorFlow
docker pull rocm/tensorflow:latest
```

### Image Variants

| Image | Contents | Size | Use Case |
|-------|----------|------|----------|
| `rocm/dev-ubuntu-22.04` | ROCm runtime + dev tools | ~5 GB | Building ROCm applications |
| `rocm/pytorch` | ROCm + PyTorch (pre-built) | ~15 GB | ML training and inference |
| `rocm/tensorflow` | ROCm + TensorFlow (pre-built) | ~12 GB | ML training and inference |
| `rocm/rocm-terminal` | Minimal ROCm runtime | ~2 GB | Running pre-compiled HIP apps |

### Running ROCm Containers

```bash
# Basic ROCm container
docker run -it --rm \
  --device=/dev/kfd \
  --device=/dev/dri \
  --group-add video \
  rocm/dev-ubuntu-22.04:6.1 \
  rocm-smi

# PyTorch with AMD GPU
docker run -it --rm \
  --device=/dev/kfd \
  --device=/dev/dri \
  --group-add video \
  rocm/pytorch:latest \
  python -c "import torch; print(torch.cuda.is_available())"
```

Note: PyTorch uses `torch.cuda` API even on AMD GPUs when running with ROCm. The HIP compatibility layer translates CUDA calls to ROCm.

### Version-Pinned Images

```dockerfile
# Pin to specific ROCm version
FROM rocm/dev-ubuntu-22.04:6.1

# Pin PyTorch ROCm version
FROM rocm/pytorch:rocm6.1_ubuntu22.04_py3.10_pytorch_2.4
```

### Custom Dockerfile with ROCm

```dockerfile
FROM rocm/dev-ubuntu-22.04:6.1

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install PyTorch for ROCm
RUN pip3 install torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/rocm6.1

WORKDIR /app
COPY . .
USER 1001
ENTRYPOINT ["python3", "train.py"]
```

---

## HIP Compatibility

### What is HIP?

HIP (Heterogeneous-Compute Interface for Portability) is AMD's programming model that provides a CUDA-like API. Code written in HIP can run on both AMD and NVIDIA GPUs.

**Key concepts:**
- HIP API mirrors CUDA API closely (`hipMalloc` vs `cudaMalloc`)
- HIP code compiles to ROCm on AMD GPUs and to CUDA on NVIDIA GPUs
- PyTorch and TensorFlow use HIP internally when running on ROCm

### CUDA to HIP Translation

```cpp
// CUDA code
cudaMalloc(&d_ptr, size);
cudaMemcpy(d_ptr, h_ptr, size, cudaMemcpyHostToDevice);
myKernel<<<blocks, threads>>>(d_ptr);
cudaFree(d_ptr);

// Equivalent HIP code
hipMalloc(&d_ptr, size);
hipMemcpy(d_ptr, h_ptr, size, hipMemcpyHostToDevice);
hipLaunchKernelGGL(myKernel, blocks, threads, 0, 0, d_ptr);
hipFree(d_ptr);
```

### hipify Tools

Convert CUDA source code to HIP:

```bash
# Install hipify
sudo apt-get install -y hipify-clang

# Convert a single file
hipify-perl cuda_code.cu > hip_code.cpp

# Convert a directory
hipify-perl --inplace src/

# Using hipify-clang (more accurate, requires LLVM)
hipify-clang cuda_code.cu -o hip_code.cpp -- -I/usr/local/cuda/include
```

### HIP in Containers

```dockerfile
FROM rocm/dev-ubuntu-22.04:6.1

WORKDIR /app
COPY . .

# Compile HIP code
RUN hipcc -o myapp main.cpp

USER 1001
ENTRYPOINT ["./myapp"]
```

### Framework Compatibility

| Framework | AMD API | Notes |
|-----------|---------|-------|
| PyTorch | `torch.cuda.*` | Same API, HIP translates internally |
| TensorFlow | `tf.config.list_physical_devices('GPU')` | Transparent HIP backend |
| JAX | `jax.devices()` | ROCm support via XLA |

---

## Device Mapping

### Required Device Flags

AMD GPU containers require explicit device mapping (unlike NVIDIA which uses `--gpus`):

```bash
docker run --rm \
  --device=/dev/kfd \
  --device=/dev/dri \
  --group-add video \
  rocm/pytorch:latest
```

**Device descriptions:**
- `/dev/kfd`: Kernel Fusion Driver -- required for all GPU compute operations
- `/dev/dri`: Direct Rendering Infrastructure -- contains per-GPU render nodes
- `--group-add video`: Ensures the container user has permissions to access GPU devices

### Selecting Specific GPUs

To restrict which GPUs a container can access, map specific render devices:

```bash
# Only GPU 0 (renderD128)
docker run --rm \
  --device=/dev/kfd \
  --device=/dev/dri/renderD128 \
  --group-add video \
  rocm/pytorch:latest

# GPUs 0 and 1 (renderD128 and renderD129)
docker run --rm \
  --device=/dev/kfd \
  --device=/dev/dri/renderD128 \
  --device=/dev/dri/renderD129 \
  --group-add video \
  rocm/pytorch:latest
```

### Identifying GPU Device Nodes

```bash
# List render devices
ls /dev/dri/renderD*

# Map render nodes to GPUs
rocm-smi --showbus
# Output shows Bus ID for each GPU
# renderD128 = first GPU, renderD129 = second GPU, etc.
```

### HIP_VISIBLE_DEVICES

Similar to CUDA_VISIBLE_DEVICES, controls which GPUs are visible to ROCm applications:

```bash
docker run --rm \
  --device=/dev/kfd \
  --device=/dev/dri \
  --group-add video \
  -e HIP_VISIBLE_DEVICES=0,1 \
  rocm/pytorch:latest
```

### Docker Compose with AMD GPU

```yaml
services:
  training:
    image: rocm/pytorch:latest
    devices:
      - /dev/kfd:/dev/kfd
      - /dev/dri:/dev/dri
    group_add:
      - video
    environment:
      - HIP_VISIBLE_DEVICES=0,1
```

---

## ROCm Version Matrix

### ROCm to Driver Compatibility

| ROCm Version | Kernel Driver | Ubuntu | RHEL/Rocky |
|-------------|---------------|--------|------------|
| ROCm 6.2 | amdgpu 6.7.0+ | 22.04, 24.04 | 9.x |
| ROCm 6.1 | amdgpu 6.5.0+ | 22.04, 24.04 | 9.x |
| ROCm 6.0 | amdgpu 6.3.0+ | 22.04 | 9.x |
| ROCm 5.7 | amdgpu 6.1.0+ | 22.04 | 9.x |
| ROCm 5.6 | amdgpu 5.18.0+ | 20.04, 22.04 | 8.x, 9.x |

### Framework Compatibility

| ROCm | PyTorch | TensorFlow | JAX |
|------|---------|------------|-----|
| 6.2 | 2.5+ | 2.17+ | 0.4.30+ |
| 6.1 | 2.4+ | 2.16+ | 0.4.28+ |
| 6.0 | 2.3+ | 2.15+ | 0.4.25+ |
| 5.7 | 2.1+ | 2.14+ | 0.4.20+ |

### Supported GPU Architectures

| GPU Family | Architecture | Example GPUs | Min ROCm |
|-----------|-------------|--------------|----------|
| RDNA 3 | gfx1100, gfx1101 | RX 7900 XTX, RX 7600 | ROCm 5.7+ |
| CDNA 3 | gfx942 | MI300X, MI300A | ROCm 6.0+ |
| CDNA 2 | gfx90a | MI250X, MI210 | ROCm 5.0+ |
| CDNA 1 | gfx908 | MI100 | ROCm 4.0+ |
| RDNA 2 | gfx1030 | RX 6900 XT, RX 6700 XT | ROCm 5.3+ |

### Checking ROCm Version

```bash
# On host
rocm-smi --showversion
apt list --installed 2>/dev/null | grep rocm-dev

# In container
cat /opt/rocm/.info/version
rocminfo | head -5
```

### Upgrading ROCm

When upgrading ROCm on the host:

1. Remove old version: `sudo apt purge rocm-dev amdgpu-dkms`
2. Update repository to new version
3. Install new version: `sudo apt install rocm-dev amdgpu-dkms`
4. Reboot to load new kernel driver
5. Verify: `rocm-smi`

Container images with newer ROCm versions work with the host driver as long as the kernel driver meets the minimum version. Unlike NVIDIA, forward compatibility is more limited -- keep host ROCm and container ROCm versions aligned.

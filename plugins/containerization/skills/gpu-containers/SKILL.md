---
name: gpu-containers
description: Use when the user needs to configure Docker/container environments for GPU workloads, mentions CUDA, ROCm, GPU passthrough, or asks about running PyTorch/TensorFlow in containers. Configures NVIDIA/AMD GPU runtime access, selects compatible base images, and validates single/multi-GPU container execution.
metadata:
  references:
    - references/nvidia-cuda-setup.md
    - references/amd-rocm-setup.md
    - references/gpu-validation-and-operations.md
  assets:
    - assets/cuda-dockerfile.dockerfile
    - assets/rocm-dockerfile.dockerfile
---

# GPU Containers

## Primary Actions

- Configure NVIDIA CUDA or AMD ROCm container runtime access.
- Select compatible CUDA/ROCm base images for framework workloads.
- Configure single- and multi-GPU container execution.
- Configure Docker Compose GPU services.
- Troubleshoot driver/runtime/framework compatibility failures.

## Quick Checks

```bash
# Host visibility
nvidia-smi

# NVIDIA container GPU check
docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi

# AMD ROCm container check
docker run --rm --device=/dev/kfd --device=/dev/dri rocm/pytorch:latest rocm-smi
```

## Compatibility Snapshot

| CUDA Version | Minimum Driver |
|-------------|----------------|
| 12.4 | 550.54+ |
| 12.1 | 530.30+ |
| 11.8 | 520.61+ |

## End-to-End Workflow With Validation Gates

1. Check host GPU driver/tooling.
2. Install/configure container runtime toolkit.
3. Validate GPU visibility in a base container.
4. Build app image and validate framework GPU access.
5. For multi-GPU jobs, validate allocation and IPC/shared memory settings.
6. If any gate fails, fix compatibility/runtime config and retry from step 1.

## Quick Compose Example (NVIDIA)

```yaml
services:
  training:
    build: .
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
```

## Templates

- [assets/cuda-dockerfile.dockerfile](assets/cuda-dockerfile.dockerfile)
- [assets/rocm-dockerfile.dockerfile](assets/rocm-dockerfile.dockerfile)

## Deep References

- NVIDIA CUDA setup and compatibility:
  [references/nvidia-cuda-setup.md](references/nvidia-cuda-setup.md)
- AMD ROCm setup and device mapping:
  [references/amd-rocm-setup.md](references/amd-rocm-setup.md)
- Validation workflow and failure recovery:
  [references/gpu-validation-and-operations.md](references/gpu-validation-and-operations.md)

# GPU Validation and Operations

## End-to-End Validation Workflow

1. **Host driver check**

```bash
nvidia-smi
```

2. **Runtime/toolkit check (NVIDIA)**

```bash
docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi
```

3. **Container build and framework check**

```bash
docker build -t my-gpu-image .
docker run --rm --gpus all my-gpu-image python -c "import torch; print(torch.cuda.is_available())"
```

4. **Multi-GPU / distributed check (if needed)**

```bash
docker run --rm --gpus all --ipc=host my-gpu-image nvidia-smi
```

5. **If any step fails**

- Re-check driver <-> CUDA compatibility.
- Re-check runtime flags (`--gpus`, device mappings).
- Re-check image/framework CUDA build compatibility.

## Common Failure Signatures

1. `--gpus` not recognized -> toolkit/runtime missing or misconfigured.
2. `no CUDA-capable device` -> driver/version mismatch or host visibility issue.
3. ROCm device errors -> missing `/dev/kfd` or `/dev/dri` mapping.
4. Training crashes with DataLoader/shared memory errors -> add `--ipc=host` or larger shm.

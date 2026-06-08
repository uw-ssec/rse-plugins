# Validation and Recovery for Singularity/Apptainer

## Build/Conversion Validation Workflow

1. Build or pull image:

```bash
apptainer build image.sif definition.def
# or
apptainer pull image.sif docker://myrepo/myimage:tag
```

2. Validate metadata and internals:

```bash
apptainer inspect image.sif
apptainer test image.sif
```

3. Runtime smoke test:

```bash
apptainer exec image.sif python --version
```

4. GPU smoke test (if GPU workload):

```bash
apptainer exec --nv image.sif nvidia-smi
```

5. MPI smoke test (if MPI workload):

```bash
mpirun -np 2 apptainer exec image.sif /path/to/app
```

If any checkpoint fails, update definition/runtime bindings and rebuild/retest.

## Common Recovery Moves

1. Build fails due to permissions -> use `--fakeroot` or admin-assisted build path.
2. App fails at runtime -> verify binds and environment variables.
3. GPU not detected -> confirm `--nv` and host driver compatibility.
4. MPI launch errors -> verify host/container MPI model compatibility.

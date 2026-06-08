---
name: singularity-apptainer
description: Use when the user asks about Singularity, Apptainer, HPC containers, running containers on clusters, or converting Docker images for HPC environments. Creates definition files, builds and validates .sif images, configures MPI/GPU execution, and integrates container runs with Slurm.
metadata:
  references:
    - references/definition-files.md
    - references/mpi-containers.md
    - references/hpc-workflow-patterns.md
    - references/validation-and-recovery.md
  assets:
    - assets/basic-definition.def
    - assets/mpi-definition.def
    - assets/gpu-definition.def
---

# Singularity/Apptainer

## Primary Actions

- Create and adjust `.def` definition files for scientific workloads.
- Build, inspect, and test `.sif` images.
- Convert Docker images to `.sif` for HPC use.
- Configure MPI and GPU runtime flags for cluster jobs.
- Provide Slurm-ready execution patterns.

## Quick Command Card

```bash
# Build/pull
apptainer build image.sif definition.def
apptainer pull image.sif docker://python:3.12-slim

# Run/inspect/test
apptainer exec image.sif python --version
apptainer inspect image.sif
apptainer test image.sif

# GPU
apptainer exec --nv image.sif nvidia-smi

# MPI (example)
srun --mpi=pmix apptainer exec image.sif ./my_mpi_app
```

## End-to-End Workflow With Validation Gates

1. Build or convert image.
2. Validate image metadata and `%test` checks.
3. Run a runtime smoke command (`apptainer exec ...`).
4. For GPU jobs, validate with `--nv` and `nvidia-smi`.
5. For MPI jobs, run a small multi-rank test before scaling.
6. If any gate fails, fix definition/runtime config and repeat from step 1.

## Definition File At a Glance

```text
Bootstrap / From
%post
%environment
%runscript
%test
```

## Templates

- [assets/basic-definition.def](assets/basic-definition.def)
- [assets/mpi-definition.def](assets/mpi-definition.def)
- [assets/gpu-definition.def](assets/gpu-definition.def)

## Deep References

- Definition file syntax/details:
  [references/definition-files.md](references/definition-files.md)
- MPI models and launch patterns:
  [references/mpi-containers.md](references/mpi-containers.md)
- Slurm and HPC integration patterns:
  [references/hpc-workflow-patterns.md](references/hpc-workflow-patterns.md)
- Validation checkpoints and recovery playbook:
  [references/validation-and-recovery.md](references/validation-and-recovery.md)

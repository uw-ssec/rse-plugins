---
name: singularity-apptainer
description: HPC containerization with Singularity/Apptainer including definition files, .sif image management, MPI integration, GPU passthrough, Slurm job integration, and Docker image conversion.
metadata:
  references:
    - references/definition-files.md
    - references/mpi-containers.md
    - references/hpc-workflow-patterns.md
  assets:
    - assets/basic-definition.def
    - assets/mpi-definition.def
    - assets/gpu-definition.def
---

# Singularity/Apptainer

A comprehensive guide to HPC containerization with Singularity and Apptainer. This skill covers definition file authoring, building and managing .sif images, MPI integration for multi-node workloads, GPU passthrough for accelerated computing, Slurm job integration, and converting Docker images for use on HPC clusters. These patterns help researchers run reproducible, portable workloads on shared computing infrastructure where Docker is typically unavailable.

## Resources in This Skill

This skill includes supporting materials for HPC container tasks:

**References** (detailed guides -- consult the table of contents in each file and read specific sections as needed):
- `references/definition-files.md` - Complete definition file syntax: all sections (%labels through %startscript), bootstrap sources (docker, library, localimage, shub, oras), multi-stage builds, build arguments, and image signing
- `references/mpi-containers.md` - MPI container patterns: bind model vs hybrid model, OpenMPI/MPICH/Intel MPI setup, PMIx integration, multi-node execution, performance tuning, and troubleshooting fabric issues
- `references/hpc-workflow-patterns.md` - HPC workflow integration: Slurm job scripts with containers, array jobs, GPU jobs, interactive sessions, filesystem performance, pulling images on compute nodes, shared .sif storage, and PBS/SGE integration

**Assets** (ready-to-use definition file templates):
- `assets/basic-definition.def` - Basic Ubuntu-based Apptainer definition file with common scientific packages and explanatory comments
- `assets/mpi-definition.def` - MPI-enabled definition file with OpenMPI, including comments on bind vs hybrid model tradeoffs
- `assets/gpu-definition.def` - CUDA-enabled definition file for GPU workloads, with comments covering both NVIDIA and AMD paths

## Quick Reference Card

### Key Apptainer Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `apptainer build` | Build .sif from def file or URI | `apptainer build image.sif definition.def` |
| `apptainer pull` | Pull image from registry | `apptainer pull docker://ubuntu:24.04` |
| `apptainer exec` | Run a command inside container | `apptainer exec image.sif python script.py` |
| `apptainer run` | Execute the default runscript | `apptainer run image.sif` |
| `apptainer shell` | Open interactive shell | `apptainer shell image.sif` |
| `apptainer instance start` | Start a background instance | `apptainer instance start image.sif myservice` |
| `apptainer instance stop` | Stop a background instance | `apptainer instance stop myservice` |
| `apptainer inspect` | View image metadata | `apptainer inspect --labels image.sif` |
| `apptainer overlay create` | Create writable overlay | `apptainer overlay create --size 500 overlay.img` |
| `apptainer sign` | Sign an image | `apptainer sign image.sif` |
| `apptainer verify` | Verify image signature | `apptainer verify image.sif` |
| `apptainer cache clean` | Remove cached images | `apptainer cache clean` |

### Definition File Structure at a Glance

```
Bootstrap: docker                  # Where to get the base image
From: ubuntu:24.04                 # Base image URI

%labels                            # Image metadata (key-value pairs)
    Author Jane Doe

%files                             # Copy files from host into container at build time
    data/input.csv /opt/data/

%post                              # Commands to run during build (install packages, etc.)
    apt-get update && apt-get install -y python3

%environment                       # Environment variables set at runtime
    export PATH="/opt/software/bin:$PATH"

%runscript                         # Default command when container is "run"
    python3 "$@"

%startscript                       # Command for background instances
    python3 -m http.server 8000

%test                              # Validation commands run after build
    python3 --version
```

## When to Use

Use this skill when you need to:

- Run containers on HPC clusters where Docker is not available
- Write Apptainer/Singularity definition files for research software
- Build .sif images from definition files or Docker images
- Run MPI-parallel workloads across multiple nodes using containers
- Enable GPU acceleration (NVIDIA or AMD) inside containers
- Integrate containerized applications with Slurm, PBS, or SGE schedulers
- Convert existing Docker images for use on HPC systems
- Create reproducible computational environments for shared clusters
- Set up writable overlays for persistent modifications to read-only images
- Manage container image storage and distribution on cluster filesystems

## Singularity vs Apptainer

### Naming and History

Singularity was the original HPC container runtime, created in 2015 at Lawrence Berkeley National Laboratory. In November 2021, the project joined the Linux Foundation and was renamed to **Apptainer**. The commercial fork by Sylabs retained the Singularity name as **SingularityCE** (Community Edition).

| Project | Maintainer | Command Prefix | Status |
|---------|-----------|----------------|--------|
| Apptainer | Linux Foundation | `apptainer` | Active, recommended for new deployments |
| SingularityCE | Sylabs | `singularity` | Active, commercially supported |
| Singularity (original) | -- | `singularity` | Superseded by the above two |

### Compatibility

Apptainer provides a `singularity` compatibility symlink, so existing scripts using `singularity exec`, `singularity run`, etc. continue to work without modification. The .sif image format is identical across both projects.

### Migration

For clusters migrating from Singularity to Apptainer:

- Replace `singularity` with `apptainer` in scripts (or rely on the compatibility symlink)
- Replace `SINGULARITY_` environment variable prefixes with `APPTAINER_` (the old prefixes are still honored but deprecated)
- Definition file syntax is unchanged
- Existing .sif images work without rebuilding

Throughout this document, commands use the `apptainer` prefix. Substitute `singularity` if your cluster has not yet migrated.

## Definition File Structure

Definition files (`.def`) are the Apptainer equivalent of Dockerfiles. They describe how to build a container image.

### Header

The header specifies the bootstrap agent and base image:

```
Bootstrap: docker
From: ubuntu:24.04
```

Common bootstrap agents: `docker` (Docker Hub or registry), `library` (Sylabs Cloud Library), `localimage` (existing .sif), `oras` (OCI registry), `shub` (Singularity Hub, deprecated).

### %labels

Metadata stored in the image, retrievable with `apptainer inspect --labels`:

```
%labels
    Author Jane Doe
    Version 1.0.0
    Description Molecular dynamics simulation environment
    org.opencontainers.image.source https://github.com/org/repo
```

### %post

Commands executed during the build, running as root inside the container. This is where you install packages and compile software:

```
%post
    apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv && \
    rm -rf /var/lib/apt/lists/*

    python3 -m pip install --no-cache-dir numpy scipy matplotlib
```

### %environment

Environment variables set every time the container runs:

```
%environment
    export LC_ALL=C
    export PATH="/opt/software/bin:$PATH"
    export PYTHONPATH="/opt/software/lib/python3/site-packages:$PYTHONPATH"
```

### %runscript

The default command executed when the container is invoked with `apptainer run` or called as an executable:

```
%runscript
    echo "Container was called with arguments: $@"
    python3 "$@"
```

### %test

Validation commands run automatically after a successful build (skipped with `--notest`):

```
%test
    python3 -c "import numpy; print(f'NumPy {numpy.__version__}')"
    python3 -c "import scipy; print(f'SciPy {scipy.__version__}')"
```

### %files

Copy files from the host into the container at build time. Format is `<source> <destination>`:

```
%files
    requirements.txt /opt/
    scripts/run_analysis.py /opt/scripts/
```

### %startscript

Command executed when the container runs as a background instance via `apptainer instance start`:

```
%startscript
    python3 -m http.server 8000
```

See `references/definition-files.md` for complete syntax coverage including multi-stage builds, build arguments, and image signing.

## Building .sif Images

### From a Definition File

```bash
# Standard build (requires root or fakeroot)
sudo apptainer build simulation.sif simulation.def

# Build with fakeroot (no sudo needed if configured by admin)
apptainer build --fakeroot simulation.sif simulation.def

# Build into a sandbox directory (useful for debugging)
apptainer build --sandbox simulation_sandbox/ simulation.def
```

### From Docker Hub or a Registry

```bash
# Pull and convert a Docker image to .sif
apptainer pull docker://python:3.12-slim
# Creates: python_3.12-slim.sif

# Pull with a custom output name
apptainer pull output.sif docker://nvcr.io/nvidia/pytorch:24.01-py3

# Build directly from Docker URI
apptainer build myimage.sif docker://ubuntu:24.04
```

### From Sylabs Cloud Library

```bash
apptainer pull library://ubuntu:24.04
```

## Running Containers

### exec -- Run a Specific Command

```bash
# Run a Python script
apptainer exec image.sif python3 analysis.py --input data.csv

# Run with arguments
apptainer exec image.sif bash -c "echo Hello from the container"
```

### run -- Execute the Default Runscript

```bash
# Invokes the %runscript section
apptainer run image.sif arg1 arg2

# Equivalent: run the .sif as an executable
./image.sif arg1 arg2
```

### shell -- Interactive Session

```bash
# Open a shell inside the container
apptainer shell image.sif

# Shell with writable overlay
apptainer shell --overlay my_overlay.img image.sif
```

### instance -- Background Services

```bash
# Start a persistent instance
apptainer instance start image.sif webserver

# Execute commands against the instance
apptainer exec instance://webserver curl localhost:8000

# Stop the instance
apptainer instance stop webserver

# List running instances
apptainer instance list
```

## Bind Mounts and Filesystem Access

By default, Apptainer automatically binds `$HOME`, `/tmp`, `/proc`, `/sys`, and `/dev`. Additional directories must be explicitly bound.

```bash
# Bind a single directory
apptainer exec --bind /scratch/data:/data image.sif python3 process.py /data

# Bind multiple directories
apptainer exec --bind /scratch/data:/data,/project/config:/config image.sif ./run.sh

# Bind with read-only access
apptainer exec --bind /reference/genome:/genome:ro image.sif analyze.sh

# Use environment variable for persistent binds
export APPTAINER_BIND="/scratch/data:/data,/project/shared:/shared"
apptainer exec image.sif python3 pipeline.py
```

**Key differences from Docker:**
- The host user's identity is preserved inside the container (no root by default)
- Home directory is mounted automatically (disable with `--no-home`)
- The current working directory is preserved (disable with `--no-mount cwd`)

## MPI Integration

Apptainer supports MPI workloads through two models. The choice depends on your cluster's MPI installation and performance requirements.

### Host MPI Bind Model (Recommended for Most Clusters)

The host's MPI installation is bind-mounted into the container at runtime. The container needs compatible MPI headers and libraries at build time, but the host's optimized MPI stack (with InfiniBand, OmniPath, or other fabric support) is used at runtime.

```bash
# Run MPI job -- host mpirun launches processes, each enters the container
mpirun -np 4 apptainer exec --bind /opt/openmpi:/opt/openmpi image.sif ./my_mpi_app

# With Slurm
srun --mpi=pmix apptainer exec image.sif ./my_mpi_app
```

### Hybrid Model

The container ships its own MPI installation. Simpler to set up but may not leverage high-speed interconnects unless network drivers are bind-mounted.

```bash
# Container's internal mpirun is used
apptainer exec image.sif mpirun -np 4 ./my_mpi_app
```

See `references/mpi-containers.md` for detailed setup guides for OpenMPI, MPICH, and Intel MPI, plus PMIx configuration and troubleshooting.

## GPU Support

### NVIDIA GPUs

Use the `--nv` flag to expose NVIDIA GPU devices and driver libraries inside the container:

```bash
# Run GPU-accelerated workload
apptainer exec --nv gpu_image.sif python3 train_model.py

# Verify GPU access
apptainer exec --nv gpu_image.sif nvidia-smi
```

The `--nv` flag automatically:
- Binds the host NVIDIA driver libraries into the container
- Makes GPU device files (`/dev/nvidia*`) available
- Sets `LD_LIBRARY_PATH` to include driver libraries

The container must include CUDA toolkit libraries (matching or compatible with the host driver version).

### AMD GPUs

Use the `--rocm` flag for AMD GPU passthrough:

```bash
apptainer exec --rocm gpu_image.sif python3 train_model.py
apptainer exec --rocm gpu_image.sif rocm-smi
```

See `assets/gpu-definition.def` for a complete CUDA-enabled definition file template.

## Slurm Integration

Apptainer integrates naturally with Slurm because it runs as a regular user process (no daemon required).

### Basic Slurm Job

```bash
#!/bin/bash
#SBATCH --job-name=container-job
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=02:00:00
#SBATCH --output=%x_%j.out

apptainer exec --bind /scratch/$USER:/scratch image.sif \
    python3 analysis.py --threads $SLURM_CPUS_PER_TASK
```

### MPI Slurm Job

```bash
#!/bin/bash
#SBATCH --job-name=mpi-container
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=32
#SBATCH --time=08:00:00
#SBATCH --output=%x_%j.out

srun --mpi=pmix apptainer exec --bind /scratch:/scratch image.sif ./my_mpi_app
```

### GPU Slurm Job

```bash
#!/bin/bash
#SBATCH --job-name=gpu-training
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gpus=4
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=24:00:00
#SBATCH --output=%x_%j.out

apptainer exec --nv --bind /scratch/$USER:/scratch gpu_image.sif \
    python3 train.py --gpus 4
```

See `references/hpc-workflow-patterns.md` for array jobs, interactive sessions, PBS/SGE examples, and filesystem performance patterns.

## Docker-to-Singularity Conversion

Converting Docker images to .sif format is straightforward:

```bash
# Direct conversion from Docker Hub
apptainer pull docker://tensorflow/tensorflow:2.16.1-gpu
# Creates: tensorflow_2.16.1-gpu.sif

# From a private registry
apptainer pull docker://registry.example.com/myproject/myimage:latest

# From a local Docker daemon
apptainer build local_image.sif docker-daemon://myimage:latest

# From a Docker archive tarball
docker save myimage:latest -o myimage.tar
apptainer build local_image.sif docker-archive://myimage.tar
```

**Key considerations when converting:**
- Docker `ENTRYPOINT` maps to `%runscript`
- Docker `ENV` statements are preserved
- Docker `VOLUME` directives are ignored (use `--bind` instead)
- Docker `USER` is ignored (Apptainer uses the host user's identity)
- Multi-layer Docker images are flattened into a single squashfs filesystem

## Overlay and Writable Containers

SIF images are read-only by default. Use overlays to add a writable layer.

### Writable Overlay

```bash
# Create an overlay image (size in MB)
apptainer overlay create --size 500 my_overlay.img

# Run with the overlay -- writes persist in my_overlay.img
apptainer exec --overlay my_overlay.img image.sif pip install new_package

# Shell with overlay for interactive modification
apptainer shell --overlay my_overlay.img image.sif
```

### Writable Sandbox

```bash
# Build as a sandbox (directory instead of .sif)
apptainer build --sandbox my_sandbox/ docker://ubuntu:24.04

# Modify the sandbox (requires fakeroot or sudo)
apptainer shell --fakeroot --writable my_sandbox/

# Convert sandbox back to .sif when done
apptainer build final_image.sif my_sandbox/
```

### Embedded Overlay

```bash
# Add a writable overlay directly into the .sif
apptainer overlay create --size 200 image.sif

# Now writes go into the embedded overlay
apptainer exec --writable image.sif pip install new_package
```

## Common Mistakes

1. **Building without fakeroot or sudo** -- Definition file builds that install packages require root-like privileges. Use `--fakeroot` if your admin has configured it, or `sudo apptainer build`. Pulling pre-built images does not require elevated privileges.

2. **Mismatched MPI versions** -- The container's MPI version must be ABI-compatible with the host's MPI when using the bind model. A mismatch causes segfaults or "MPI_Init failed" errors. Check with `mpirun --version` on both host and container.

3. **Forgetting --nv for GPU jobs** -- Without `--nv`, the container cannot see GPU devices even if CUDA is installed inside. The error typically manifests as "no CUDA-capable device is detected."

4. **Assuming root inside the container** -- Unlike Docker, Apptainer preserves the host user's identity. `apt-get install` inside a running container fails unless you used `--fakeroot` or `--writable` with appropriate permissions.

5. **Not binding scratch/project filesystems** -- HPC data directories like `/scratch`, `/project`, or `/work` are not mounted by default. Jobs fail with "file not found" if you forget `--bind`.

6. **Using Docker VOLUME expectations** -- Docker volumes do not translate to Apptainer. Data persistence is handled through bind mounts and overlays.

7. **Large .sif images on shared filesystems** -- Building or pulling large images in `$HOME` can exceed quotas. Use `APPTAINER_CACHEDIR` and `APPTAINER_TMPDIR` to redirect to scratch.

8. **Ignoring %test** -- Skipping the `%test` section means build problems are discovered at runtime. Add basic import checks and version validation.

9. **Hardcoding paths in def files** -- Use `%environment` to set `PATH` and other variables rather than hardcoding absolute paths in `%runscript`, making the container more flexible.

10. **Not cleaning up package caches** -- Just like Dockerfiles, run `rm -rf /var/lib/apt/lists/*` after `apt-get install` and use `--no-cache-dir` with `pip install` to avoid bloating the image.

## Best Practices

- [ ] Use `apptainer` commands (not `singularity`) for new projects
- [ ] Pin base image versions in definition files (`From: ubuntu:24.04`, not `From: ubuntu:latest`)
- [ ] Include a `%test` section to validate the build
- [ ] Add `%labels` with author, version, and description metadata
- [ ] Clean up package manager caches in `%post` to minimize image size
- [ ] Set `APPTAINER_CACHEDIR` to a scratch directory to avoid filling home quotas
- [ ] Use the bind model for MPI when the host has optimized fabric drivers
- [ ] Test GPU containers with `--nv nvidia-smi` before submitting long jobs
- [ ] Store .sif images on a shared filesystem accessible by all compute nodes
- [ ] Use overlays for persistent modifications instead of rebuilding entire images
- [ ] Bind-mount data directories explicitly rather than relying on automatic mounts
- [ ] Version-control your definition files alongside your research code
- [ ] Use `--no-home` when home directory contents might conflict with container software
- [ ] Sign images with `apptainer sign` for provenance tracking in shared environments

## Resources

### Official Documentation
- **Apptainer User Guide**: https://apptainer.org/docs/user/latest/
- **Apptainer Admin Guide**: https://apptainer.org/docs/admin/latest/
- **Apptainer Definition Files**: https://apptainer.org/docs/user/latest/definition_files.html
- **SingularityCE Documentation**: https://docs.sylabs.io/guides/latest/user-guide/

### MPI and HPC
- **Apptainer MPI Guide**: https://apptainer.org/docs/user/latest/mpi.html
- **Apptainer GPU Support**: https://apptainer.org/docs/user/latest/gpu.html
- **OpenMPI with Containers**: https://www.open-mpi.org/faq/?category=singularity
- **NERSC Shifter/Singularity Guide**: https://docs.nersc.gov/development/containers/

### Registries and Distribution
- **Sylabs Cloud Library**: https://cloud.sylabs.io/library
- **Docker Hub**: https://hub.docker.com/
- **NVIDIA NGC Catalog**: https://catalog.ngc.nvidia.com/
- **BioContainers**: https://biocontainers.pro/

### Tutorials and Community
- **Apptainer GitHub**: https://github.com/apptainer/apptainer
- **HPC Containers Advisory Council**: https://containersinpc.github.io/
- **Singularity Tutorial (NIH HPC)**: https://hpc.nih.gov/apps/singularity.html

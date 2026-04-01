# Definition Files -- Deep Reference

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| Complete Def File Syntax | 16-56 | Overall structure, header fields, section ordering |
| All Sections Explained | 58-262 | %labels, %files, %post, %environment, %runscript, %test, %startscript, %help, %arguments |
| Bootstrap Sources | 264-364 | docker, library, localimage, shub, oras, yum, debootstrap |
| Multi-Stage Definition Files | 366-438 | Multiple stages, COPY --from, build ordering |
| Build Arguments | 440-506 | Parameterizing builds, --build-arg, dynamic base images |
| Signing Images | 508-569 | Key management, signing, verification, key servers |

---

## Complete Def File Syntax

A definition file has two parts: a **header** and one or more **sections**. The header appears at the top without a section marker. Sections begin with `%sectionname` on its own line.

### Header Fields

The header specifies the bootstrap agent and its parameters:

```
Bootstrap: docker
From: ubuntu:24.04
Stage: build
```

| Field | Required | Description |
|-------|----------|-------------|
| `Bootstrap` | Yes | The bootstrap agent to use (docker, library, localimage, etc.) |
| `From` | Yes | The base image URI or path |
| `Stage` | No | Name for this stage (used in multi-stage builds) |
| `Registry` | No | Override the default registry for docker bootstrap |
| `Namespace` | No | Override the namespace for library bootstrap |
| `Fingerprints` | No | Required PGP fingerprints for library images |
| `MirrorURL` | No | Mirror URL for yum/debootstrap bootstraps |
| `OSVersion` | No | OS version for yum/debootstrap bootstraps |
| `Include` | No | Additional packages for debootstrap |

### Section Ordering

Sections can appear in any order in the definition file, but they execute in a fixed order during the build:

1. `%files` -- Copy files from host (before any commands run)
2. `%files from <stage>` -- Copy files from a previous stage
3. `%post` -- Run build commands
4. `%test` -- Validate the build
5. `%environment` -- Recorded for runtime use
6. `%runscript` -- Recorded for `apptainer run`
7. `%startscript` -- Recorded for `apptainer instance start`
8. `%labels` -- Recorded as metadata
9. `%help` -- Recorded as help text

---

## All Sections Explained

### %labels

Key-value metadata stored in the image. Retrievable with `apptainer inspect --labels image.sif`.

```
%labels
    Author Jane Doe <jane@example.com>
    Version 2.1.0
    Description Computational chemistry environment with GROMACS and AMBER
    org.opencontainers.image.source https://github.com/labgroup/chem-container
    org.opencontainers.image.licenses BSD-3-Clause
    Build.Date 2025-01-15
    MPI.Version OpenMPI-4.1.6
```

Labels follow a `Key Value` format (space-separated, no `=` sign). Use OCI label keys for interoperability with container registries.

### %files

Copy files from the host filesystem into the container at build time. Each line specifies `<source> <destination>`. Runs before `%post`, so copied files are available during package installation.

```
%files
    requirements.txt /opt/app/requirements.txt
    scripts/ /opt/scripts/
    config/settings.yml /etc/myapp/settings.yml
```

**Important notes:**
- Source paths are relative to the directory where `apptainer build` is invoked
- Destination paths are absolute paths inside the container
- If the destination directory does not exist, it is created automatically
- Symbolic links are followed and the target file is copied

### %files from \<stage\>

In multi-stage builds, copy files from a previously built stage:

```
%files from build
    /opt/compiled_app /opt/app
    /opt/venv /opt/venv
```

### %post

Shell commands executed during the build. This is where most of the work happens: installing packages, compiling software, downloading data. Commands run as root inside the container.

```
%post
    # Update package lists and install system dependencies
    apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        gfortran \
        libopenblas-dev \
        liblapack-dev \
        python3 \
        python3-pip \
        python3-venv \
        wget \
        git && \
    rm -rf /var/lib/apt/lists/*

    # Create a virtual environment for Python packages
    python3 -m venv /opt/venv
    . /opt/venv/bin/activate

    # Install Python scientific stack
    pip install --no-cache-dir \
        numpy \
        scipy \
        matplotlib \
        pandas \
        h5py

    # Compile a custom application
    cd /opt
    git clone --depth 1 --branch v2.0 https://github.com/org/simulation.git
    cd simulation
    cmake -B build -DCMAKE_BUILD_TYPE=Release
    cmake --build build --parallel $(nproc)
    cmake --install build --prefix /opt/software

    # Clean up build artifacts to reduce image size
    rm -rf /opt/simulation
```

**Best practices for %post:**
- Chain commands with `&&` to fail fast on errors
- Remove package manager caches in the same section
- Clean up source code and build directories after installation
- Use `--no-cache-dir` with pip
- Set `DEBIAN_FRONTEND=noninteractive` for unattended apt installs

### %environment

Environment variables set at runtime (not during build). These are sourced every time the container starts via `exec`, `run`, or `shell`.

```
%environment
    export PATH="/opt/software/bin:/opt/venv/bin:$PATH"
    export LD_LIBRARY_PATH="/opt/software/lib:$LD_LIBRARY_PATH"
    export PYTHONPATH="/opt/venv/lib/python3.12/site-packages"
    export OMP_NUM_THREADS=${OMP_NUM_THREADS:-1}
    export LC_ALL=C
```

**Note:** To set environment variables during the build (in `%post`), export them directly in `%post`. Variables defined in `%environment` are not available during `%post`.

### %runscript

The default command invoked by `apptainer run image.sif` or `./image.sif`. Arguments passed on the command line are available as `$@`.

```
%runscript
    echo "=== Simulation Container v2.1.0 ==="
    echo "Running with arguments: $@"

    if [ $# -eq 0 ]; then
        echo "Usage: ./simulation.sif <input_file> [options]"
        echo "Run 'apptainer run-help simulation.sif' for detailed help."
        exit 1
    fi

    exec /opt/software/bin/simulate "$@"
```

**Tips:**
- Use `exec` to replace the shell process with the target command (proper signal handling)
- Provide a usage message when no arguments are given
- Validate required arguments before running

### %test

Commands run automatically after a successful build to validate the image. A non-zero exit code fails the build. Skip with `apptainer build --notest`.

```
%test
    # Verify critical binaries are present and executable
    /opt/software/bin/simulate --version

    # Verify Python packages imported correctly
    python3 -c "import numpy; print(f'NumPy {numpy.__version__}')"
    python3 -c "import scipy; print(f'SciPy {scipy.__version__}')"
    python3 -c "import h5py; print(f'h5py {h5py.__version__}')"

    # Run a quick smoke test
    echo "1 2 3" > /tmp/test_input.dat
    /opt/software/bin/simulate --check /tmp/test_input.dat
    rm -f /tmp/test_input.dat

    echo "All tests passed."
```

### %startscript

The command run when the container is started as a persistent background instance with `apptainer instance start`. Useful for services, databases, or long-running daemons.

```
%startscript
    exec /opt/software/bin/server --port 8080 --config /etc/myapp/settings.yml
```

### %help

Free-form text displayed by `apptainer run-help image.sif`. Use it to document usage, required bind mounts, and expected environment variables.

```
%help
    Molecular Dynamics Simulation Container v2.1.0

    Usage:
        apptainer run simulation.sif <input.mdp> [--nsteps N] [--output dir]

    Required bind mounts:
        --bind /scratch/$USER:/scratch   Scratch space for intermediate files

    Environment variables:
        OMP_NUM_THREADS   Number of OpenMP threads (default: 1)

    GPU support:
        Use --nv flag for NVIDIA GPU acceleration

    Examples:
        apptainer run --nv --bind /scratch/$USER:/scratch simulation.sif input.mdp
```

### %arguments

Define build-time arguments that can be overridden with `--build-arg`:

```
%arguments
    PYTHON_VERSION=3.12
    MPI_VERSION=4.1.6

%post
    # Use the arguments
    apt-get install -y python{{ PYTHON_VERSION }}
```

---

## Bootstrap Sources

### docker

Pull from Docker Hub or any OCI-compatible registry. The most commonly used bootstrap source.

```
Bootstrap: docker
From: ubuntu:24.04
```

```
Bootstrap: docker
From: nvcr.io/nvidia/pytorch:24.01-py3
```

```
# Private registry with authentication
Bootstrap: docker
From: registry.example.com/myproject/base:2.0
Registry: registry.example.com
```

Authentication uses `apptainer remote login` or Docker's `~/.docker/config.json`.

### library

Pull from the Sylabs Cloud Library or a self-hosted library:

```
Bootstrap: library
From: ubuntu:24.04
```

```
# Specific entity/collection
Bootstrap: library
From: user/collection/image:tag
```

```
# Require signed image with specific fingerprint
Bootstrap: library
From: user/collection/image:tag
Fingerprints: ABCDEF1234567890
```

### localimage

Build from an existing local .sif file or sandbox directory. Useful for layered builds.

```
Bootstrap: localimage
From: /path/to/base_image.sif
```

```
# From a sandbox directory
Bootstrap: localimage
From: /path/to/sandbox_directory/
```

### shub (Deprecated)

Pull from Singularity Hub. No longer recommended for new projects:

```
Bootstrap: shub
From: user/repo:tag
```

### oras

Pull from OCI registries using the ORAS protocol. Useful for registries like GitHub Container Registry:

```
Bootstrap: oras
From: ghcr.io/org/container:latest
```

### yum / debootstrap / arch / busybox

Build a distribution from scratch using a package manager. Rarely needed when Docker base images are available.

```
# Build a CentOS/RHEL base from scratch
Bootstrap: yum
OSVersion: 9
MirrorURL: https://mirror.stream.centos.org/%{OSVERSION}-stream/BaseOS/$basearch/os/
Include: dnf
```

```
# Build a Debian/Ubuntu base from scratch
Bootstrap: debootstrap
OSVersion: noble
MirrorURL: http://archive.ubuntu.com/ubuntu/
Include: apt-transport-https,ca-certificates
```

---

## Multi-Stage Definition Files

Multi-stage builds let you compile software in one stage and copy only the resulting artifacts to a final minimal stage, reducing image size.

### Syntax

Each stage has its own header and sections. Stages are separated by being listed sequentially in the file, each with their own `Bootstrap`/`From`/`Stage` header:

```
# ===========================================================================
# Stage 1: Build environment
# ===========================================================================
Bootstrap: docker
From: ubuntu:24.04
Stage: build

%post
    apt-get update && apt-get install -y --no-install-recommends \
        build-essential cmake gfortran libopenblas-dev && \
    rm -rf /var/lib/apt/lists/*

    cd /opt
    git clone --depth 1 --branch v3.0 https://github.com/org/solver.git
    cd solver
    cmake -B build -DCMAKE_BUILD_TYPE=Release
    cmake --build build --parallel $(nproc)
    cmake --install build --prefix /opt/solver

# ===========================================================================
# Stage 2: Runtime (final image)
# ===========================================================================
Bootstrap: docker
From: ubuntu:24.04
Stage: runtime

%files from build
    /opt/solver /opt/solver

%post
    apt-get update && apt-get install -y --no-install-recommends \
        libopenblas0 libgomp1 && \
    rm -rf /var/lib/apt/lists/*

%environment
    export PATH="/opt/solver/bin:$PATH"
    export LD_LIBRARY_PATH="/opt/solver/lib:$LD_LIBRARY_PATH"

%runscript
    exec solver "$@"

%test
    solver --version

%labels
    Author Research Computing Team
    Version 3.0.0
```

### How Stages Work

1. Stages are built in the order they appear in the definition file
2. `%files from <stage>` copies files from a previously completed stage
3. Only the last stage becomes the final .sif image
4. Earlier stages are discarded after their artifacts are copied

### When to Use Multi-Stage

- Compiling C/C++/Fortran code that requires a large build toolchain
- Installing Python packages with compiled extensions that need build-essential
- Building software from source when the source repo is large
- Any case where build dependencies significantly outweigh runtime dependencies

---

## Build Arguments

### Defining Arguments

Use `%arguments` to define variables that can be overridden at build time:

```
%arguments
    PYTHON_VERSION=3.12
    UBUNTU_VERSION=24.04
    OPENMPI_VERSION=4.1.6
    INSTALL_GPU=false

Bootstrap: docker
From: ubuntu:{{ UBUNTU_VERSION }}

%post
    apt-get update && apt-get install -y python{{ PYTHON_VERSION }}

    if [ "{{ INSTALL_GPU }}" = "true" ]; then
        # Install CUDA toolkit
        apt-get install -y nvidia-cuda-toolkit
    fi
```

### Overriding at Build Time

```bash
# Use default values
apptainer build image.sif definition.def

# Override specific arguments
apptainer build --build-arg PYTHON_VERSION=3.11 image.sif definition.def
apptainer build --build-arg UBUNTU_VERSION=22.04 --build-arg INSTALL_GPU=true image.sif definition.def
```

### Templating Syntax

Build arguments use the `{{ variable }}` syntax inside sections:

```
%post
    echo "Building with Python {{ PYTHON_VERSION }}"
    pip install numpy=={{ NUMPY_VERSION }}

%labels
    Python.Version {{ PYTHON_VERSION }}
    Build.GPU {{ INSTALL_GPU }}
```

### Dynamic Base Images

Build arguments in the header enable building the same definition file against different base images:

```
%arguments
    BASE_IMAGE=ubuntu:24.04

Bootstrap: docker
From: {{ BASE_IMAGE }}
```

```bash
apptainer build --build-arg BASE_IMAGE=rockylinux:9 image.sif definition.def
```

---

## Signing Images

### Key Management

Apptainer uses PGP keys for image signing and verification.

```bash
# Generate a new PGP key for signing
apptainer key newpair

# List local keys
apptainer key list

# Push public key to a key server
apptainer key push <fingerprint>

# Search for a key on a key server
apptainer key search <name_or_email>

# Pull a public key for verification
apptainer key pull <fingerprint>
```

### Signing an Image

```bash
# Sign with your default key
apptainer sign image.sif

# Sign with a specific key
apptainer sign --keyidx 1 image.sif
```

Signing adds a PGP signature block to the .sif file. The image content is unchanged, so the image still runs on systems that do not verify signatures.

### Verifying an Image

```bash
# Verify signature
apptainer verify image.sif

# Verify and require a specific fingerprint
apptainer verify --url https://keys.example.com image.sif
```

Verification confirms that:
1. The image has not been modified since signing
2. The signature matches a trusted public key

### Verification in Production

For production HPC environments, enforce signature verification:

```bash
# In apptainer.conf (admin configuration)
# require signature verification = yes

# Users must verify before running
apptainer verify image.sif && apptainer exec image.sif ./run.sh
```

**Best practice:** Sign all images used in shared HPC environments and publish your public key to a key server so collaborators can verify authenticity.

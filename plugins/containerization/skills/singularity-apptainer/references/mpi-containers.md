# MPI Containers -- Deep Reference

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| Bind Model vs Hybrid Model | 18-91 | Architecture comparison, tradeoffs, decision criteria |
| OpenMPI Setup | 93-191 | Container build, host compatibility, run commands |
| MPICH Setup | 193-269 | MPICH-based container builds, ABI compatibility |
| Intel MPI | 271-345 | Intel MPI in containers, licensing, fabric auto-detection |
| PMIx Integration | 347-419 | Process management interface, Slurm PMIx, version matching |
| Multi-Node Execution | 421-498 | Cross-node container MPI, shared filesystems, SSH transport |
| Performance Tuning | 500-592 | Fabric selection, binding, memory, bandwidth optimization |
| Troubleshooting Fabric Issues | 594-694 | Common errors, diagnostics, driver binding, workarounds |

---

## Bind Model vs Hybrid Model

### Bind Model

In the bind model, the host's MPI installation is bind-mounted into the container at runtime. The container is built with MPI headers and libraries for compilation, but the actual MPI used at runtime comes from the host system.

```
┌──────────────────────────────────────────────────┐
│  Host System                                     │
│  ┌─────────────────┐                             │
│  │ Host MPI        │ ──bind-mount──┐             │
│  │ (InfiniBand,    │               │             │
│  │  OmniPath, etc.)│               ▼             │
│  └─────────────────┘    ┌──────────────────┐     │
│                         │  Container       │     │
│  mpirun / srun ────────►│  Application     │     │
│                         │  (linked against │     │
│                         │   host MPI)      │     │
│                         └──────────────────┘     │
└──────────────────────────────────────────────────┘
```

**Advantages:**
- Full access to high-speed interconnects (InfiniBand, Slingshot, OmniPath)
- Optimal performance -- uses the vendor-tuned MPI stack
- Smaller container images (no full MPI installation inside)

**Disadvantages:**
- Container must be built with an ABI-compatible MPI version
- Tightly coupled to the host's MPI installation
- Less portable between clusters with different MPI stacks

### Hybrid Model

In the hybrid model, the container ships its own complete MPI installation. The MPI inside the container is used for all communication.

```
┌──────────────────────────────────────────────────┐
│  Host System                                     │
│                                                  │
│  apptainer exec ────►┌──────────────────┐        │
│                      │  Container       │        │
│                      │  ┌────────────┐  │        │
│                      │  │ MPI (own)  │  │        │
│                      │  └────────────┘  │        │
│                      │  Application     │        │
│                      └──────────────────┘        │
└──────────────────────────────────────────────────┘
```

**Advantages:**
- Fully self-contained -- works on any cluster
- No MPI version compatibility concerns with the host
- Simpler to build and test

**Disadvantages:**
- May not leverage high-speed interconnects without explicit driver binding
- Larger container images (includes full MPI installation)
- Single-node only unless SSH or PMIx is configured for cross-node communication

### Decision Criteria

| Criterion | Bind Model | Hybrid Model |
|-----------|-----------|--------------|
| InfiniBand / OmniPath needed | Yes | Requires driver binding |
| Portability across clusters | Low | High |
| Performance optimization | Maximum | Good (TCP default) |
| Ease of setup | Moderate | Simple |
| Image size | Smaller | Larger |
| Host MPI required | Yes | No |

**Recommendation:** Use the bind model for production HPC workloads where performance matters. Use the hybrid model for development, testing, or when portability is the priority.

---

## OpenMPI Setup

### Container Definition (Bind Model)

Build the container with OpenMPI headers for compilation, but the host's OpenMPI will be used at runtime:

```
Bootstrap: docker
From: ubuntu:24.04

%post
    apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gfortran \
        libopenmpi-dev \
        openmpi-bin \
        openssh-client && \
    rm -rf /var/lib/apt/lists/*

    # Compile MPI application
    cd /opt
    mpicc -o my_mpi_app my_mpi_app.c -lm

%environment
    export PATH="/opt:$PATH"

%runscript
    exec /opt/my_mpi_app "$@"
```

### Container Definition (Hybrid Model)

Install a specific OpenMPI version from source for full control:

```
Bootstrap: docker
From: ubuntu:24.04

%post
    apt-get update && apt-get install -y --no-install-recommends \
        build-essential gfortran wget ca-certificates \
        libibverbs-dev librdmacm-dev && \
    rm -rf /var/lib/apt/lists/*

    # Build OpenMPI from source with InfiniBand support
    OPENMPI_VERSION=4.1.6
    cd /tmp
    wget https://download.open-mpi.org/release/open-mpi/v4.1/openmpi-${OPENMPI_VERSION}.tar.gz
    tar xzf openmpi-${OPENMPI_VERSION}.tar.gz
    cd openmpi-${OPENMPI_VERSION}
    ./configure --prefix=/opt/openmpi \
        --with-verbs \
        --with-pmix=internal \
        --with-slurm
    make -j $(nproc)
    make install
    rm -rf /tmp/openmpi*

    # Compile application against container's MPI
    export PATH="/opt/openmpi/bin:$PATH"
    export LD_LIBRARY_PATH="/opt/openmpi/lib:$LD_LIBRARY_PATH"
    cd /opt
    mpicc -o my_mpi_app my_mpi_app.c -lm

%environment
    export PATH="/opt/openmpi/bin:/opt:$PATH"
    export LD_LIBRARY_PATH="/opt/openmpi/lib:$LD_LIBRARY_PATH"
```

### Running OpenMPI Containers

```bash
# Bind model: host mpirun launches, bind host MPI into container
mpirun -np 16 apptainer exec \
    --bind /opt/openmpi:/opt/openmpi \
    --bind /etc/libibverbs.d:/etc/libibverbs.d \
    image.sif /opt/my_mpi_app

# Bind model with Slurm
srun --mpi=pmix -n 128 apptainer exec \
    --bind /opt/openmpi:/opt/openmpi \
    image.sif /opt/my_mpi_app

# Hybrid model: container's internal mpirun
apptainer exec image.sif mpirun -np 4 /opt/my_mpi_app
```

### Version Compatibility

For the bind model, the container's OpenMPI headers must be ABI-compatible with the host's OpenMPI libraries:

| Container Built With | Compatible Host Versions |
|---------------------|------------------------|
| OpenMPI 4.1.x | OpenMPI 4.1.x |
| OpenMPI 5.0.x | OpenMPI 5.0.x |

Major version mismatches (e.g., container 4.x with host 5.x) will cause runtime failures. Minor version differences within the same major version are generally safe.

---

## MPICH Setup

### MPICH ABI Compatibility

MPICH maintains a stable ABI across versions within the same major release, making it more forgiving for bind-model deployments. Several vendor MPI implementations (Cray MPICH, Intel MPI) are ABI-compatible with MPICH.

### Container Definition

```
Bootstrap: docker
From: ubuntu:24.04

%post
    apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gfortran \
        mpich \
        libmpich-dev \
        openssh-client && \
    rm -rf /var/lib/apt/lists/*

    # Compile application
    cd /opt
    mpicc -o my_mpi_app my_mpi_app.c -lm

%environment
    export PATH="/opt:$PATH"
```

### Building MPICH from Source

```
%post
    MPICH_VERSION=4.2.0
    cd /tmp
    wget https://www.mpich.org/static/downloads/${MPICH_VERSION}/mpich-${MPICH_VERSION}.tar.gz
    tar xzf mpich-${MPICH_VERSION}.tar.gz
    cd mpich-${MPICH_VERSION}
    ./configure --prefix=/opt/mpich \
        --with-device=ch4:ofi \
        --with-libfabric=embedded \
        --enable-fast=all,O3
    make -j $(nproc)
    make install
    rm -rf /tmp/mpich*

%environment
    export PATH="/opt/mpich/bin:$PATH"
    export LD_LIBRARY_PATH="/opt/mpich/lib:$LD_LIBRARY_PATH"
```

### Running MPICH Containers

```bash
# Bind model with Slurm (Cray MPICH systems)
srun -n 64 apptainer exec \
    --bind /opt/cray:/opt/cray \
    image.sif /opt/my_mpi_app

# Hybrid model
apptainer exec image.sif mpirun -np 4 /opt/my_mpi_app
```

### ABI-Compatible Implementations

The following MPI implementations share the MPICH ABI:

| Implementation | Vendor | Notes |
|---------------|--------|-------|
| MPICH | Argonne | Reference implementation |
| Cray MPICH | HPE/Cray | Optimized for Slingshot/Aries |
| Intel MPI | Intel | Supports both MPICH and custom ABI |
| MVAPICH | Ohio State | Optimized for InfiniBand |

Containers built with MPICH headers can use any of these at runtime via the bind model.

---

## Intel MPI

### Container Definition

```
Bootstrap: docker
From: intel/oneapi-hpckit:2024.1-devel-ubuntu22.04

%post
    # Intel MPI is pre-installed in the oneapi-hpckit image
    # Compile application
    . /opt/intel/oneapi/setvars.sh
    cd /opt
    mpiicc -o my_mpi_app my_mpi_app.c -lm

%environment
    . /opt/intel/oneapi/setvars.sh

%runscript
    exec /opt/my_mpi_app "$@"
```

### Minimal Intel MPI Installation

For smaller images, install only the MPI runtime:

```
Bootstrap: docker
From: ubuntu:24.04

%post
    apt-get update && apt-get install -y --no-install-recommends \
        wget gnupg ca-certificates && \
    rm -rf /var/lib/apt/lists/*

    # Add Intel repository
    wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | \
        gpg --dearmor -o /usr/share/keyrings/intel.gpg
    echo "deb [signed-by=/usr/share/keyrings/intel.gpg] https://apt.repos.intel.com/oneapi all main" \
        > /etc/apt/sources.list.d/intel-oneapi.list

    apt-get update && apt-get install -y --no-install-recommends \
        intel-oneapi-mpi-devel && \
    rm -rf /var/lib/apt/lists/*

%environment
    . /opt/intel/oneapi/setvars.sh 2>/dev/null
```

### Running Intel MPI Containers

```bash
# With Slurm
srun --mpi=pmi2 -n 64 apptainer exec image.sif /opt/my_mpi_app

# Direct mpirun (hybrid model)
apptainer exec image.sif mpirun -np 4 /opt/my_mpi_app
```

### Fabric Auto-Detection

Intel MPI automatically detects available fabrics at runtime. Control fabric selection with environment variables:

```bash
# Force specific fabric
export I_MPI_FABRICS=shm:ofi

# Force TCP (useful for debugging)
export I_MPI_FABRICS=shm:tcp

# Pass to container
apptainer exec --env I_MPI_FABRICS=shm:ofi image.sif mpirun -np 4 ./app
```

---

## PMIx Integration

### What is PMIx

PMIx (Process Management Interface for Exascale) is the standard interface between MPI implementations and resource managers (Slurm, PBS). It handles process launch, key-value exchange, and collective operations during MPI_Init.

### PMIx with Slurm

Modern Slurm installations use PMIx to launch MPI processes. The PMIx version in the container must be compatible with Slurm's PMIx plugin.

```bash
# Check Slurm's PMIx support
srun --mpi=list
# Typical output: pmix, pmix_v4, pmi2, none

# Launch with PMIx
srun --mpi=pmix -n 64 apptainer exec image.sif ./my_mpi_app

# Specify PMIx version if multiple are available
srun --mpi=pmix_v4 -n 64 apptainer exec image.sif ./my_mpi_app
```

### Building with PMIx Support

```
%post
    # Install PMIx from source for version control
    PMIX_VERSION=4.2.9
    cd /tmp
    wget https://github.com/openpmix/openpmix/releases/download/v${PMIX_VERSION}/pmix-${PMIX_VERSION}.tar.gz
    tar xzf pmix-${PMIX_VERSION}.tar.gz
    cd pmix-${PMIX_VERSION}
    ./configure --prefix=/opt/pmix
    make -j $(nproc)
    make install
    rm -rf /tmp/pmix*

    # Build OpenMPI with external PMIx
    cd /tmp
    wget https://download.open-mpi.org/release/open-mpi/v5.0/openmpi-5.0.3.tar.gz
    tar xzf openmpi-5.0.3.tar.gz
    cd openmpi-5.0.3
    ./configure --prefix=/opt/openmpi \
        --with-pmix=/opt/pmix \
        --with-slurm
    make -j $(nproc)
    make install
    rm -rf /tmp/openmpi*
```

### Version Matching

| Slurm PMIx Plugin | Container PMIx Version | Compatible |
|-------------------|----------------------|------------|
| pmix_v4 | PMIx 4.x | Yes |
| pmix_v3 | PMIx 3.x | Yes |
| pmix_v4 | PMIx 3.x | No |
| pmix (auto) | Depends on Slurm build | Check with admin |

**Diagnosing version mismatches:**

```bash
# Check Slurm's PMIx version
srun --mpi=pmix hostname 2>&1 | head -5

# Check container's PMIx version
apptainer exec image.sif pmix_info --version

# Check container's OpenMPI PMIx support
apptainer exec image.sif ompi_info --parsable | grep pmix
```

---

## Multi-Node Execution

### With Slurm (Recommended)

Slurm's `srun` handles process placement across nodes. Each process launches an independent container instance.

```bash
#!/bin/bash
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=32
#SBATCH --time=08:00:00

# srun launches 128 processes across 4 nodes
# Each process enters the container independently
srun --mpi=pmix apptainer exec \
    --bind /scratch:/scratch \
    image.sif /opt/my_mpi_app --input /scratch/data.h5
```

### Shared Filesystem Requirements

For multi-node container MPI, the .sif image must be accessible from all nodes:

```bash
# Good: image on shared filesystem
srun apptainer exec /shared/images/simulation.sif ./app

# Bad: image only on the submission node's local disk
srun apptainer exec /tmp/simulation.sif ./app  # Fails on other nodes
```

Common shared filesystem locations:

| Filesystem | Typical Mount | Use For |
|-----------|---------------|---------|
| Lustre | `/scratch`, `/work` | Large images, high-throughput I/O |
| GPFS/Spectrum Scale | `/project`, `/data` | Persistent image storage |
| NFS | `/home`, `/shared` | Small images (beware metadata load) |
| BeeGFS | `/beegfs` | Balanced performance |

### SSH Transport (Without Slurm)

If Slurm is not available, use SSH-based MPI launch:

```bash
# Create a hostfile
cat > hostfile.txt << EOF
node001 slots=32
node002 slots=32
node003 slots=32
node004 slots=32
EOF

# Launch with mpirun and SSH
mpirun --hostfile hostfile.txt -np 128 \
    apptainer exec --bind /shared:/shared image.sif /opt/my_mpi_app
```

**Requirements for SSH transport:**
- Passwordless SSH between all nodes
- Apptainer installed on all nodes
- .sif image accessible from all nodes
- Consistent paths across nodes

### Process Binding

Ensure MPI processes are bound to specific CPU cores for optimal performance:

```bash
# Slurm handles binding
srun --mpi=pmix --cpu-bind=cores -n 128 apptainer exec image.sif ./app

# OpenMPI binding
mpirun -np 128 --map-by slot --bind-to core \
    apptainer exec image.sif ./app
```

---

## Performance Tuning

### Fabric Selection

The interconnect fabric has the largest impact on MPI performance. Ensure the correct fabric is used.

```bash
# Check available fabrics inside the container
apptainer exec --bind /opt/openmpi:/opt/openmpi image.sif fi_info -l

# OpenMPI: select fabric explicitly
mpirun -np 64 --mca btl_tcp_if_include ib0 \
    apptainer exec image.sif ./app

# OpenMPI: use UCX for InfiniBand
mpirun -np 64 --mca pml ucx --mca btl ^vader,tcp,openib \
    apptainer exec image.sif ./app
```

### InfiniBand Bind Mounts

For the bind model with InfiniBand, mount the required device and driver paths:

```bash
apptainer exec \
    --bind /dev/infiniband:/dev/infiniband \
    --bind /etc/libibverbs.d:/etc/libibverbs.d \
    --bind /usr/lib/x86_64-linux-gnu/libibverbs:/usr/lib/x86_64-linux-gnu/libibverbs \
    image.sif ./app
```

### Process and Memory Binding

```bash
# Bind processes to NUMA domains
srun --mpi=pmix --cpu-bind=cores --mem-bind=local -n 128 \
    apptainer exec image.sif ./app

# OpenMPI NUMA-aware placement
mpirun -np 64 --map-by numa --bind-to core \
    apptainer exec image.sif ./app
```

### Shared Memory Optimization

Within a node, MPI processes communicate through shared memory. Ensure `/dev/shm` is large enough:

```bash
# Check shared memory size
df -h /dev/shm

# Increase if needed (admin)
# mount -o remount,size=64G /dev/shm
```

Apptainer mounts `/dev/shm` from the host by default, so intra-node shared memory performance is preserved.

### Message Size Tuning

```bash
# OpenMPI: tune eager/rendezvous threshold
mpirun -np 64 \
    --mca btl_openib_eager_limit 65536 \
    --mca btl_openib_rndv_eager_limit 65536 \
    apptainer exec image.sif ./app

# UCX: tune rendezvous threshold
export UCX_RNDV_THRESH=65536
mpirun -np 64 --mca pml ucx apptainer exec image.sif ./app
```

### Collective Algorithm Tuning

```bash
# OpenMPI: select collective algorithms
mpirun -np 256 \
    --mca coll_tuned_use_dynamic_rules 1 \
    --mca coll_tuned_allreduce_algorithm 3 \
    apptainer exec image.sif ./app
```

### Benchmark Inside Containers

Always benchmark MPI performance inside the container to compare with bare-metal:

```bash
# OSU Micro-Benchmarks
apptainer exec image.sif /opt/osu-benchmarks/mpi/pt2pt/osu_latency
apptainer exec image.sif /opt/osu-benchmarks/mpi/pt2pt/osu_bw
apptainer exec image.sif /opt/osu-benchmarks/mpi/collective/osu_allreduce
```

---

## Troubleshooting Fabric Issues

### Common Error Messages

**"No such file or directory" for libibverbs:**
```
libibverbs: Warning: couldn't open config directory '/etc/libibverbs.d'
```

Fix: Bind-mount the InfiniBand configuration:
```bash
apptainer exec --bind /etc/libibverbs.d:/etc/libibverbs.d image.sif ./app
```

**"OPAL ERROR: Open of shared memory backing file failed":**
```
OPAL ERROR: Open of shared memory backing file /dev/shm/... failed
```

Fix: Ensure `/dev/shm` is mounted and has sufficient space:
```bash
apptainer exec --bind /dev/shm:/dev/shm image.sif ./app
```

**"MPI_Init failed -- no PMIx server found":**
```
PMIX ERROR: PMIX_ERR_INVALID_NAMESPACE
```

Fix: Use the correct `--mpi` flag with `srun`:
```bash
srun --mpi=pmix apptainer exec image.sif ./app
# or
srun --mpi=pmi2 apptainer exec image.sif ./app
```

**"Segfault during MPI_Init":**

Usually indicates an MPI version mismatch between container and host. Verify versions:
```bash
# Host MPI version
mpirun --version

# Container MPI version
apptainer exec image.sif mpirun --version
```

### Diagnostic Commands

```bash
# List available network interfaces inside container
apptainer exec image.sif ip addr show

# Check InfiniBand devices
apptainer exec --bind /dev/infiniband image.sif ibstat

# Check libfabric providers
apptainer exec image.sif fi_info -l

# Verbose MPI output for debugging
mpirun -np 2 --mca mpi_show_mca_params all \
    apptainer exec image.sif ./app 2>&1 | head -100

# UCX diagnostic
UCX_LOG_LEVEL=info mpirun -np 2 --mca pml ucx \
    apptainer exec image.sif ./app 2>&1 | grep ucx
```

### Driver Binding Checklist

When MPI fabric detection fails, ensure these paths are bound:

| Component | Typical Host Path | Purpose |
|-----------|------------------|---------|
| InfiniBand devices | `/dev/infiniband/` | RDMA device files |
| Verbs config | `/etc/libibverbs.d/` | User-space driver plugins |
| Verbs libraries | `/usr/lib/*/libibverbs*` | RDMA libraries |
| UCX libraries | `/usr/lib/*/ucx/` | UCX transport plugins |
| libfabric | `/usr/lib/*/libfabric/` | OFI provider plugins |
| NVIDIA GPU Direct | `/dev/nvidia*` | GPU-Direct RDMA |
| Shared memory | `/dev/shm` | Intra-node communication |

### Fallback to TCP

When high-speed fabrics are not available or not working, fall back to TCP for debugging:

```bash
# OpenMPI: force TCP
mpirun -np 4 --mca btl tcp,self --mca btl_tcp_if_include eth0 \
    apptainer exec image.sif ./app

# MPICH: force TCP via OFI
export FI_PROVIDER=tcp
mpirun -np 4 apptainer exec image.sif ./app

# Intel MPI: force TCP
export I_MPI_FABRICS=shm:tcp
mpirun -np 4 apptainer exec image.sif ./app
```

If the application works over TCP but not over the high-speed fabric, the issue is with driver binding or version compatibility, not with the application or container itself.

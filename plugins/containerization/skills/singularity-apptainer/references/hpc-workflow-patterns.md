# HPC Workflow Patterns -- Deep Reference

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| Slurm Job Scripts with Containers | 18-110 | Basic patterns, environment passing, module integration |
| Array Jobs | 112-206 | Parameter sweeps, task-specific inputs, output organization |
| GPU Jobs | 208-336 | Single-GPU, multi-GPU, multi-node GPU, NCCL configuration |
| Interactive Sessions | 338-404 | Interactive Slurm allocations, debugging, X11 forwarding |
| Filesystem Performance | 406-479 | Overlay vs bind, Lustre tuning, tmpdir strategies |
| Pulling Images on Compute Nodes | 481-551 | Cache management, pre-staging, avoiding build on compute |
| Shared .sif Storage Patterns | 553-631 | Central repositories, versioning, access control |
| PBS/SGE Integration | 633-753 | PBS Pro, Torque, SGE job scripts with containers |

---

## Slurm Job Scripts with Containers

### Basic Pattern

A Slurm job script runs `apptainer exec` just like any other command. The container executes as the submitting user with no special privileges.

```bash
#!/bin/bash
#SBATCH --job-name=analysis
#SBATCH --partition=normal
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err

# Load any required modules (e.g., for Apptainer itself)
module load apptainer/1.3

# Define paths
IMAGE="/shared/containers/analysis_v2.1.sif"
INPUT="/scratch/$USER/data/experiment_001"
OUTPUT="/scratch/$USER/results/$SLURM_JOB_ID"

mkdir -p "$OUTPUT"

# Run the analysis inside the container
apptainer exec \
    --bind "$INPUT":/data:ro \
    --bind "$OUTPUT":/output \
    "$IMAGE" \
    python3 /opt/app/analyze.py \
        --input /data \
        --output /output \
        --threads "$SLURM_CPUS_PER_TASK"

echo "Job $SLURM_JOB_ID completed at $(date)"
```

### Passing Environment Variables

Apptainer passes most host environment variables into the container by default. Slurm variables (`SLURM_JOB_ID`, `SLURM_CPUS_PER_TASK`, etc.) are available inside the container without extra configuration.

```bash
# Pass additional variables explicitly
apptainer exec --env MY_PARAM=42 --env RANDOM_SEED=12345 image.sif ./run.sh

# Pass all SLURM_ variables (already done by default)
apptainer exec image.sif bash -c 'echo "Running on $SLURM_NODELIST with $SLURM_CPUS_PER_TASK CPUs"'

# Clean environment (start fresh, only container's %environment)
apptainer exec --cleanenv image.sif ./run.sh

# Clean environment but pass specific variables
apptainer exec --cleanenv --env OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK image.sif ./run.sh
```

### Module Integration

On clusters that use environment modules, load modules before invoking the container. For bind-model MPI, this ensures the correct MPI paths are set:

```bash
#!/bin/bash
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=32

# Load cluster MPI module (sets PATH, LD_LIBRARY_PATH, etc.)
module load openmpi/4.1.6
module load apptainer/1.3

# srun uses the module-loaded MPI; container binds host MPI
srun --mpi=pmix apptainer exec \
    --bind "$OPENMPI_DIR":/opt/openmpi \
    image.sif /opt/my_mpi_app
```

### Job Output Organization

Structure output directories using Slurm variables for traceability:

```bash
OUTPUT_DIR="/scratch/$USER/results/${SLURM_JOB_NAME}_${SLURM_JOB_ID}"
mkdir -p "$OUTPUT_DIR"

apptainer exec --bind "$OUTPUT_DIR":/output image.sif ./run.sh

# Copy key results to persistent storage after job completes
cp "$OUTPUT_DIR/summary.csv" "/project/$USER/results/"
```

---

## Array Jobs

### Parameter Sweeps

Array jobs run the same container with different parameters. Use `$SLURM_ARRAY_TASK_ID` to select inputs or parameters.

```bash
#!/bin/bash
#SBATCH --job-name=sweep
#SBATCH --array=0-99
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=01:00:00
#SBATCH --output=logs/sweep_%A_%a.out

IMAGE="/shared/containers/simulation.sif"
OUTPUT="/scratch/$USER/sweep/${SLURM_ARRAY_JOB_ID}/task_${SLURM_ARRAY_TASK_ID}"

mkdir -p "$OUTPUT"

apptainer exec \
    --bind "$OUTPUT":/output \
    "$IMAGE" \
    python3 /opt/app/simulate.py \
        --seed "$SLURM_ARRAY_TASK_ID" \
        --output /output/result.h5
```

### Task-Specific Input Files

Map array task IDs to specific input files using a parameter file:

```bash
#!/bin/bash
#SBATCH --job-name=batch-process
#SBATCH --array=1-50
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=16G
#SBATCH --time=02:00:00
#SBATCH --output=logs/batch_%A_%a.out

# Read the input file for this task from a list
PARAM_FILE="/project/$USER/experiments/input_list.txt"
INPUT_FILE=$(sed -n "${SLURM_ARRAY_TASK_ID}p" "$PARAM_FILE")

if [ -z "$INPUT_FILE" ]; then
    echo "ERROR: No input file for task $SLURM_ARRAY_TASK_ID"
    exit 1
fi

OUTPUT="/scratch/$USER/batch/${SLURM_ARRAY_JOB_ID}/${SLURM_ARRAY_TASK_ID}"
mkdir -p "$OUTPUT"

apptainer exec \
    --bind "$(dirname "$INPUT_FILE")":/input:ro \
    --bind "$OUTPUT":/output \
    /shared/containers/processor.sif \
    python3 /opt/app/process.py \
        --input "/input/$(basename "$INPUT_FILE")" \
        --output /output/
```

### Throttling Array Tasks

Limit the number of simultaneously running array tasks to avoid overwhelming the filesystem or licenses:

```bash
#SBATCH --array=0-999%50    # Run at most 50 tasks at a time
```

### Aggregating Results

After all array tasks complete, run a final aggregation job:

```bash
#!/bin/bash
#SBATCH --job-name=aggregate
#SBATCH --dependency=afterok:12345    # Wait for array job 12345
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=64G
#SBATCH --time=00:30:00

apptainer exec \
    --bind /scratch/$USER/sweep/12345:/data:ro \
    --bind /project/$USER/results:/output \
    /shared/containers/analysis.sif \
    python3 /opt/app/aggregate.py --input-dir /data --output /output/summary.csv
```

---

## GPU Jobs

### Single-GPU Job

```bash
#!/bin/bash
#SBATCH --job-name=gpu-inference
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gpus=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --output=logs/%x_%j.out

module load apptainer/1.3

apptainer exec --nv \
    --bind /scratch/$USER:/scratch \
    /shared/containers/pytorch_24.01.sif \
    python3 /scratch/inference.py --model /scratch/model.pt
```

### Multi-GPU Single-Node

```bash
#!/bin/bash
#SBATCH --job-name=training
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gpus=4
#SBATCH --cpus-per-task=32
#SBATCH --mem=128G
#SBATCH --time=48:00:00
#SBATCH --output=logs/%x_%j.out

module load apptainer/1.3

apptainer exec --nv \
    --bind /scratch/$USER:/scratch \
    /shared/containers/pytorch_24.01.sif \
    torchrun --nproc_per_node=4 \
        /scratch/train.py \
        --batch-size 256 \
        --epochs 100 \
        --output /scratch/checkpoints/
```

### Multi-Node Multi-GPU

For distributed training across multiple GPU nodes:

```bash
#!/bin/bash
#SBATCH --job-name=dist-training
#SBATCH --partition=gpu
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=4
#SBATCH --cpus-per-task=32
#SBATCH --mem=256G
#SBATCH --time=72:00:00
#SBATCH --output=logs/%x_%j.out

module load apptainer/1.3

# Determine master address and port
MASTER_ADDR=$(scontrol show hostnames "$SLURM_JOB_NODELIST" | head -n 1)
MASTER_PORT=29500

export MASTER_ADDR MASTER_PORT

srun apptainer exec --nv \
    --bind /scratch/$USER:/scratch \
    --env MASTER_ADDR="$MASTER_ADDR" \
    --env MASTER_PORT="$MASTER_PORT" \
    --env WORLD_SIZE="$SLURM_NTASKS" \
    /shared/containers/pytorch_24.01.sif \
    torchrun \
        --nnodes="$SLURM_NNODES" \
        --nproc_per_node=4 \
        --rdzv_id="$SLURM_JOB_ID" \
        --rdzv_backend=c10d \
        --rdzv_endpoint="$MASTER_ADDR:$MASTER_PORT" \
        /scratch/train.py --batch-size 1024
```

### NCCL Configuration

NVIDIA Collective Communications Library (NCCL) handles GPU-to-GPU communication. Configure it for optimal performance:

```bash
# Use InfiniBand for inter-node GPU communication
export NCCL_IB_DISABLE=0
export NCCL_NET_GDR_LEVEL=5     # Enable GPU Direct RDMA

# Debug NCCL issues
export NCCL_DEBUG=INFO
export NCCL_DEBUG_SUBSYS=ALL

# Specify network interface
export NCCL_SOCKET_IFNAME=ib0

# Pass NCCL variables into container
apptainer exec --nv \
    --env NCCL_IB_DISABLE=0 \
    --env NCCL_NET_GDR_LEVEL=5 \
    image.sif torchrun ...
```

### AMD GPU Jobs

```bash
#!/bin/bash
#SBATCH --job-name=rocm-job
#SBATCH --partition=amd-gpu
#SBATCH --nodes=1
#SBATCH --gpus=4
#SBATCH --time=24:00:00

apptainer exec --rocm \
    --bind /scratch/$USER:/scratch \
    /shared/containers/rocm_pytorch.sif \
    python3 /scratch/train.py
```

---

## Interactive Sessions

### Interactive Slurm Allocation

```bash
# Get an interactive allocation
salloc --nodes=1 --cpus-per-task=8 --mem=32G --time=02:00:00

# Shell into the container
apptainer shell --bind /scratch/$USER:/scratch /shared/containers/analysis.sif

# Or run commands directly
apptainer exec /shared/containers/analysis.sif python3
```

### Interactive GPU Session

```bash
salloc --partition=gpu --gpus=1 --cpus-per-task=8 --mem=32G --time=04:00:00

# Verify GPU access
apptainer exec --nv /shared/containers/pytorch.sif nvidia-smi

# Start a Jupyter session
apptainer exec --nv \
    --bind /scratch/$USER:/scratch \
    /shared/containers/pytorch.sif \
    jupyter lab --ip=0.0.0.0 --port=8888 --no-browser
```

### X11 Forwarding

For GUI applications (visualization, plotting):

```bash
# Connect to cluster with X11 forwarding
ssh -X user@cluster

# Get interactive allocation
salloc --x11 --nodes=1 --time=01:00:00

# Run GUI application in container
apptainer exec --bind /tmp/.X11-unix:/tmp/.X11-unix \
    --env DISPLAY=$DISPLAY \
    /shared/containers/paraview.sif paraview
```

### Debugging with Shell

Use `apptainer shell` to debug issues interactively:

```bash
# Shell into the container to inspect the environment
apptainer shell image.sif
Apptainer> which python3
Apptainer> python3 -c "import numpy; print(numpy.__file__)"
Apptainer> ls /opt/software/
Apptainer> exit

# Shell with same bind mounts as the failing job
apptainer shell \
    --bind /scratch/$USER:/scratch \
    --bind /project/data:/data:ro \
    image.sif
```

---

## Filesystem Performance

### Overlay vs Bind

| Method | Read Performance | Write Performance | Use Case |
|--------|-----------------|-------------------|----------|
| Bind mount | Native filesystem speed | Native filesystem speed | Most workloads |
| SIF (squashfs) | Excellent (compressed, cached) | N/A (read-only) | Application binaries |
| Overlay (ext3) | Good | Moderate | Persistent writable layer |
| Sandbox (directory) | Native | Native | Development/debugging |

### Lustre Tuning

On Lustre filesystems, align I/O patterns with stripe settings for optimal throughput:

```bash
# Check stripe settings for an image file
lfs getstripe /shared/containers/image.sif

# Set optimal striping for a large .sif file
lfs setstripe -c 4 -S 4M /shared/containers/

# For output directories with many small files
lfs setstripe -c 1 /scratch/$USER/output/

# For output directories with large files
lfs setstripe -c 8 -S 8M /scratch/$USER/large_output/
```

### Tmpdir Strategies

Some applications create many temporary files. Redirect them to fast local storage:

```bash
#!/bin/bash
#SBATCH --tmp=100G    # Request local SSD scratch space

# Use node-local SSD for temporary files
export TMPDIR="/tmp/job_${SLURM_JOB_ID}"
mkdir -p "$TMPDIR"

apptainer exec \
    --bind "$TMPDIR":/tmp \
    --env TMPDIR=/tmp \
    image.sif python3 analysis.py

# Clean up
rm -rf "$TMPDIR"
```

### Avoiding Metadata Storms

Containers with many small files (e.g., Python environments with thousands of .py files) perform well because the squashfs format in .sif images serves these files from a single file, avoiding metadata operations on the parallel filesystem.

**Anti-pattern:** Using a sandbox directory on Lustre for production workloads. The thousands of small files in a Python environment cause severe metadata load.

**Best practice:** Always use .sif (squashfs) format on parallel filesystems. Reserve sandboxes for local-disk development.

### Overlay for Write-Heavy Workloads

```bash
# Create overlay on fast local storage
apptainer overlay create --size 10000 /tmp/work_overlay.img

# Run with overlay for write-heavy operations
apptainer exec \
    --overlay /tmp/work_overlay.img \
    --bind /scratch/$USER/input:/input:ro \
    image.sif python3 process.py

# Copy results from overlay to shared filesystem after job
```

---

## Pulling Images on Compute Nodes

### Cache Management

Apptainer caches downloaded layers in `$HOME/.apptainer/cache` by default. On HPC clusters, this can fill home directory quotas quickly.

```bash
# Redirect cache to scratch space
export APPTAINER_CACHEDIR="/scratch/$USER/.apptainer_cache"
export APPTAINER_TMPDIR="/scratch/$USER/.apptainer_tmp"
mkdir -p "$APPTAINER_CACHEDIR" "$APPTAINER_TMPDIR"

# Pull an image
apptainer pull docker://tensorflow/tensorflow:2.16.1-gpu

# Clean the cache after pulling
apptainer cache clean --force
```

### Pre-Staging Images

Pull images on the login node and store on a shared filesystem. Never build or pull on compute nodes during jobs.

```bash
# On login node: pull and store
cd /shared/containers/
apptainer pull docker://nvcr.io/nvidia/pytorch:24.01-py3
# Creates: pytorch_24.01-py3.sif

# In job scripts: use the pre-staged image
apptainer exec /shared/containers/pytorch_24.01-py3.sif python3 train.py
```

### Automated Pre-Staging Script

```bash
#!/bin/bash
# pre-stage-images.sh -- Run on login node to update shared container images

CONTAINER_DIR="/shared/containers"
export APPTAINER_CACHEDIR="/scratch/$USER/.apptainer_cache"

images=(
    "docker://python:3.12-slim"
    "docker://nvcr.io/nvidia/pytorch:24.01-py3"
    "docker://tensorflow/tensorflow:2.16.1-gpu"
)

for img in "${images[@]}"; do
    echo "Pulling: $img"
    apptainer pull --dir "$CONTAINER_DIR" "$img"
done

apptainer cache clean --force
echo "All images pre-staged in $CONTAINER_DIR"
```

### Build on Login Nodes

If you need to build from a definition file, do it on the login node (or a dedicated build node), never on compute nodes during a job:

```bash
# On login node (with --fakeroot or sudo)
apptainer build --fakeroot /shared/containers/custom.sif custom.def

# In job script: use the pre-built image
#SBATCH ...
apptainer exec /shared/containers/custom.sif ./run.sh
```

---

## Shared .sif Storage Patterns

### Central Repository

Maintain a shared directory of approved container images accessible by all users:

```
/shared/containers/
├── README.txt              # Inventory and usage notes
├── python_3.12-slim.sif
├── pytorch_24.01-py3.sif
├── tensorflow_2.16.1-gpu.sif
├── gromacs_2024.1.sif
├── custom/
│   ├── labgroup_analysis_v2.1.sif
│   └── labgroup_analysis_v2.0.sif
└── deprecated/
    └── pytorch_23.07-py3.sif
```

### Versioning Strategy

Include version information in the filename and in `%labels`:

```bash
# Naming convention: <software>_<version>.sif
pytorch_24.01-py3.sif
gromacs_2024.1.sif
custom_pipeline_v3.2.sif

# Symlink for "latest"
ln -sf pytorch_24.01-py3.sif pytorch_latest.sif
```

### Access Control

Use Unix groups to control who can read, write, and manage shared images:

```bash
# Set group ownership
chgrp -R hpc-users /shared/containers/
chmod -R g+rX /shared/containers/

# Only admins can write
chmod -R o-w /shared/containers/

# Group-writable directory for lab-specific images
mkdir -p /shared/containers/labgroup/
chgrp labgroup /shared/containers/labgroup/
chmod g+rwx /shared/containers/labgroup/
```

### Image Inventory

Maintain a simple inventory of available images:

```bash
# Generate inventory from image labels
for sif in /shared/containers/*.sif; do
    echo "=== $(basename "$sif") ==="
    apptainer inspect --labels "$sif" 2>/dev/null
    echo "Size: $(du -h "$sif" | cut -f1)"
    echo ""
done > /shared/containers/inventory.txt
```

### Garbage Collection

Remove old images to reclaim storage:

```bash
# Find .sif images not accessed in 90 days
find /shared/containers/ -name "*.sif" -atime +90 -ls

# Move to deprecated before deleting
mv /shared/containers/old_image.sif /shared/containers/deprecated/
```

---

## PBS/SGE Integration

### PBS Pro Job Script

```bash
#!/bin/bash
#PBS -N container-job
#PBS -l select=1:ncpus=8:mem=32gb
#PBS -l walltime=04:00:00
#PBS -o logs/
#PBS -e logs/
#PBS -j oe

cd "$PBS_O_WORKDIR"

module load apptainer/1.3

IMAGE="/shared/containers/analysis.sif"
OUTPUT="/scratch/$USER/results/$PBS_JOBID"
mkdir -p "$OUTPUT"

apptainer exec \
    --bind "$OUTPUT":/output \
    "$IMAGE" \
    python3 /opt/app/analyze.py --output /output/
```

### PBS MPI Job

```bash
#!/bin/bash
#PBS -N mpi-container
#PBS -l select=4:ncpus=32:mpiprocs=32
#PBS -l walltime=08:00:00

cd "$PBS_O_WORKDIR"

module load openmpi/4.1.6
module load apptainer/1.3

mpirun apptainer exec \
    --bind /scratch:/scratch \
    /shared/containers/simulation.sif \
    /opt/my_mpi_app --input /scratch/data.h5
```

### PBS GPU Job

```bash
#!/bin/bash
#PBS -N gpu-training
#PBS -l select=1:ncpus=16:ngpus=4:mem=128gb
#PBS -l walltime=24:00:00

cd "$PBS_O_WORKDIR"

module load apptainer/1.3

apptainer exec --nv \
    --bind /scratch/$USER:/scratch \
    /shared/containers/pytorch.sif \
    torchrun --nproc_per_node=4 /scratch/train.py
```

### PBS Array Job

```bash
#!/bin/bash
#PBS -N sweep
#PBS -J 0-99
#PBS -l select=1:ncpus=4:mem=8gb
#PBS -l walltime=01:00:00

cd "$PBS_O_WORKDIR"

OUTPUT="/scratch/$USER/sweep/${PBS_ARRAY_ID}"
mkdir -p "$OUTPUT"

apptainer exec \
    --bind "$OUTPUT":/output \
    /shared/containers/simulation.sif \
    python3 /opt/app/simulate.py --seed "$PBS_ARRAY_INDEX" --output /output/
```

### SGE (Sun Grid Engine) Job Script

```bash
#!/bin/bash
#$ -N container-job
#$ -pe smp 8
#$ -l h_rt=04:00:00
#$ -l h_vmem=4G
#$ -cwd
#$ -o logs/
#$ -e logs/

module load apptainer/1.3

apptainer exec \
    --bind /scratch/$USER:/scratch \
    /shared/containers/analysis.sif \
    python3 /opt/app/analyze.py --threads "$NSLOTS"
```

### SGE Array Job

```bash
#!/bin/bash
#$ -N sweep
#$ -t 1-100
#$ -l h_rt=01:00:00
#$ -cwd

OUTPUT="/scratch/$USER/sweep/${JOB_ID}/task_${SGE_TASK_ID}"
mkdir -p "$OUTPUT"

apptainer exec \
    --bind "$OUTPUT":/output \
    /shared/containers/simulation.sif \
    python3 /opt/app/simulate.py --seed "$SGE_TASK_ID" --output /output/
```

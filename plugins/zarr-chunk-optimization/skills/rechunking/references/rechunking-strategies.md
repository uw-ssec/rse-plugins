# Rechunking Strategies — Deep Reference

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| In-Place vs Copy Rechunking | 16–61 | Trade-offs between overwriting source and writing to a new location |
| Chunk-at-a-Time Processing | 62–96 | Memory-bounded approach for datasets that exceed RAM |
| Intermediate Storage Patterns | 97–147 | Temporary stores required by the rechunker library for cloud workflows |
| Parallel Rechunking | 148–193 | Using Dask to parallelize rechunking across workers |
| Cost Estimation Formula | 194–239 | Time estimation based on Nguyen et al. (2023) findings |
| Monitoring Progress | 240–310 | Progress bars, ETA calculation, and memory tracking during rechunking |

---

## In-Place vs Copy Rechunking

### Copy Rechunking (Recommended)

Copy rechunking writes the rechunked data to a **new location**, leaving the original dataset untouched. This is the default and recommended approach.

**Advantages:**

- **Rollback safety.** If rechunking fails (OOM, network error, disk full), the original data is unaffected.
- **Validation before swap.** You can compare the rechunked output against the original before replacing it.
- **Atomic swap.** Renaming directories or S3 prefixes is nearly instantaneous.

**Disadvantages:**

- **Requires 2x storage.** You need enough space for both the original and the rechunked copy simultaneously.
- **Egress costs (cloud).** Reading the entire dataset from cloud storage incurs egress charges.

**Workflow:**

```bash
# 1. Rechunk to new location
python rechunk.py --input /data/original.zarr --output /data/rechunked.zarr --chunks "50,512,512"

# 2. Validate
python -c "import zarr; o=zarr.open('/data/original.zarr','r'); r=zarr.open('/data/rechunked.zarr','r'); assert o.shape==r.shape"

# 3. Swap
mv /data/original.zarr /data/original_backup.zarr
mv /data/rechunked.zarr /data/original.zarr

# 4. Clean up after confirming production stability
rm -rf /data/original_backup.zarr
```

### In-Place Rechunking (Dangerous)

In-place rechunking overwrites the source data directly. This approach is almost never appropriate.

**Risks:**

- **Unrecoverable data loss.** An interrupted rechunk leaves the dataset in a partially-written, inconsistent state.
- **No rollback.** Once chunks are overwritten, the original data is gone.
- **Corruption on failure.** OOM kills, network timeouts, or disk errors during writing corrupt the dataset permanently.

**The only scenario where in-place rechunking might be acceptable** is when the dataset is easily reproducible (e.g., derived from a pipeline that can regenerate it) and storage constraints make a copy impossible. Even then, prefer deleting the original and rechunking from the upstream source.

## Chunk-at-a-Time Processing

When the `rechunker` library is not available, the `rechunk.py` script falls back to a chunk-at-a-time copy strategy. This approach reads one target chunk's worth of data from the source and writes it to the output, keeping peak memory usage proportional to a single chunk.

### How It Works

1. **Create output array.** Open a new Zarr store with the target chunk shape, copying dtype, compressor, fill value, and array order from the source.
2. **Copy metadata.** Transfer all user-defined attributes from source to output.
3. **Iterate over target chunks.** Generate all chunk start indices from the target chunk grid. For each chunk, compute the slice boundaries and copy the data.
4. **Report progress.** Log completion percentage every 10% of chunks processed.

### Memory Profile

Peak memory usage during chunk-at-a-time processing is approximately:

```
peak_memory ≈ chunk_elements × bytes_per_element × 2
```

The factor of 2 accounts for holding both the source slice (read buffer) and the output slice (write buffer) simultaneously. For a target chunk of shape `(50, 512, 512)` with `float32` dtype:

```
peak_memory ≈ 50 × 512 × 512 × 4 × 2 = 104,857,600 bytes ≈ 100 MB
```

### When Chunk-at-a-Time Is Slower

Chunk-at-a-time processing can be significantly slower than the `rechunker` library because:

- **No parallelism.** Chunks are processed sequentially, one at a time.
- **No execution planning.** The rechunker library optimizes the read/write order to minimize redundant reads when source and target chunk grids are misaligned.
- **No intermediate buffering.** When chunk grids are misaligned, chunk-at-a-time may read the same source chunks multiple times for different target chunks.

**Recommendation:** Install the `rechunker` library (`pip install rechunker`) for production rechunking. The chunk-at-a-time fallback is adequate for small datasets and testing.

## Intermediate Storage Patterns

The `rechunker` library uses a two-phase approach: it first writes data to an intermediate store in a layout that aligns with the target chunk grid, then copies from the intermediate store to the final output. This design avoids reading the same source data multiple times.

### Local Intermediate Storage

For local-to-local rechunking, the `rechunk.py` script creates a temporary directory using Python's `tempfile.mkdtemp()`:

```python
import tempfile
temp_store = tempfile.mkdtemp(prefix='rechunker_')
```

This directory is cleaned up automatically after rechunking completes. Ensure the filesystem hosting `/tmp` (or the configured temp directory) has sufficient space — the intermediate store can be as large as the dataset itself.

### Cloud Intermediate Storage

For cloud-to-cloud rechunking, there are two options:

**Option 1: Local intermediate (default).** The intermediate store is written to local disk. This is simpler but requires local storage equal to the dataset size and incurs egress charges for reading from cloud.

**Option 2: Cloud intermediate.** Specify a cloud path for the intermediate store:

```python
import rechunker
plan = rechunker.rechunk(
    source_array,
    target_chunks=(50, 512, 512),
    max_mem="4GB",
    target_store="s3://bucket/output.zarr",
    temp_store="s3://bucket/tmp/rechunk_intermediate"
)
plan.execute()
```

This avoids local disk requirements but doubles the cloud write operations. Clean up the intermediate store after rechunking:

```bash
aws s3 rm --recursive s3://bucket/tmp/rechunk_intermediate
```

### Storage Requirements Summary

| Scenario | Intermediate Location | Extra Storage Needed |
|----------|----------------------|---------------------|
| Local → Local | Local temp dir | 1x dataset size on local disk |
| Cloud → Local | Local temp dir | 1x dataset size on local disk |
| Local → Cloud | Local temp dir | 1x dataset size on local disk |
| Cloud → Cloud (local temp) | Local temp dir | 1x dataset size on local disk |
| Cloud → Cloud (cloud temp) | Cloud bucket | 1x dataset size in cloud storage |

## Parallel Rechunking

The `rechunker` library integrates with Dask to parallelize rechunking across multiple workers. This can reduce wall-clock time significantly for large datasets.

### Setting Up Dask for Rechunking

```python
from dask.distributed import Client
import rechunker
import zarr

# Start a local Dask cluster
client = Client(n_workers=4, threads_per_worker=2, memory_limit="4GB")

# Open source data
source = zarr.open("s3://bucket/source.zarr", mode="r")

# Plan rechunking (Dask-aware)
plan = rechunker.rechunk(
    source,
    target_chunks=(50, 512, 512),
    max_mem="4GB",
    target_store="s3://bucket/output.zarr",
    temp_store="/tmp/rechunk_temp"
)

# Execute with Dask
plan.execute()
```

### Worker Configuration Guidelines

| Dataset Size | Workers | Memory per Worker | Expected Speedup |
|-------------|---------|-------------------|------------------|
| < 10 GB | 1–2 | 2 GB | Minimal |
| 10–100 GB | 4–8 | 4 GB | 2–4x |
| 100 GB–1 TB | 8–16 | 8 GB | 4–8x |
| > 1 TB | 16–32 | 8–16 GB | 6–12x |

### Caveats

- **Diminishing returns.** Beyond a certain worker count, the storage backend (disk IOPS or network bandwidth) becomes the bottleneck, not CPU.
- **Memory coordination.** Each worker's memory limit must be set independently. The `max_mem` parameter in rechunker controls the per-plan memory, not per-worker.
- **Cloud rate limits.** Many parallel workers writing small chunks can exceed S3 PUT rate limits (3,500 PUT/s per prefix). Monitor for throttling errors.
- **Task graph overhead.** Very small chunks produce very large task graphs, which can overwhelm the Dask scheduler. For datasets with millions of chunks, consider increasing the chunk size or using fewer workers.

## Cost Estimation Formula

Nguyen et al. (2023) measured rechunking times for the OVRO-LWA dataset across a range of chunk configurations. Their findings provide a rough cost model.

### Observed Time Range

| Target Chunk Size | Measured Rechunking Time |
|-------------------|------------------------|
| Large (e.g., 100 MB/chunk) | ~6 minutes |
| Medium (e.g., 10 MB/chunk) | ~1–4 hours |
| Small (e.g., 1 MB/chunk) | ~10–46 hours |

### Factors in the Cost Model

The total rechunking time is influenced by:

1. **Number of target chunks.** More chunks means more individual read/write operations.

   ```
   num_chunks = product(ceil(shape[i] / target_chunks[i]) for i in range(ndim))
   ```

2. **Per-chunk overhead.** Each chunk incurs fixed overhead for opening, writing, and closing the chunk file/object. For cloud storage, this includes HTTP request latency (~50–200 ms per request).

3. **Data volume.** Total bytes that must be read and written:

   ```
   total_bytes = product(shape) × dtype.itemsize
   ```

4. **Chunk grid misalignment.** When source and target chunk grids do not align, some source chunks must be read multiple times. The rechunker library minimizes this through its intermediate storage strategy.

5. **Compression overhead.** Compressed data must be decompressed on read and recompressed on write. CPU-intensive codecs (e.g., zstd level 9) increase per-chunk processing time.

### Rough Estimate

A conservative estimate for local rechunking:

```
time_seconds ≈ num_target_chunks × time_per_chunk
```

Where `time_per_chunk` ranges from 0.01 seconds (local SSD, large chunks, no compression) to 0.5 seconds (cloud storage, small chunks, heavy compression).

**The `rechunk.py` script does not attempt a precise estimate.** Instead, it reports the Nguyen et al. range (6 minutes to 46 hours) because actual time depends heavily on storage backend, network conditions, and compression settings that cannot be measured before the operation begins.

## Monitoring Progress

### Built-in Progress Reporting

The `rechunk.py` script logs progress at 10% intervals during chunk-at-a-time processing:

```
2024-03-08 14:23:01 - INFO - Progress: 100/1000 chunks (10%)
2024-03-08 14:25:47 - INFO - Progress: 200/1000 chunks (20%)
```

### ETA Calculation

To estimate remaining time from progress logs:

```python
import time

start_time = time.perf_counter()
chunks_processed = 0
total_chunks = 1000

for chunk in chunk_iterator:
    process_chunk(chunk)
    chunks_processed += 1

    elapsed = time.perf_counter() - start_time
    rate = chunks_processed / elapsed  # chunks per second
    remaining = (total_chunks - chunks_processed) / rate
    print(f"ETA: {remaining / 60:.1f} minutes remaining")
```

### Memory Tracking

Monitor memory usage during rechunking to detect leaks or excessive consumption:

```python
import tracemalloc

tracemalloc.start()

# ... rechunking operation ...

current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

print(f"Current memory: {current / 1024**2:.1f} MB")
print(f"Peak memory: {peak / 1024**2:.1f} MB")
```

For continuous monitoring during long rechunking operations, use `psutil`:

```python
import psutil
import os

process = psutil.Process(os.getpid())
memory_mb = process.memory_info().rss / 1024**2
print(f"RSS: {memory_mb:.1f} MB")
```

### Verbose Mode

Use the `--verbose` flag with `rechunk.py` for debug-level logging that includes per-chunk timing and memory snapshots:

```bash
python rechunk.py --input /data/source.zarr \
                  --output /data/output.zarr \
                  --chunks "50,512,512" \
                  --verbose
```

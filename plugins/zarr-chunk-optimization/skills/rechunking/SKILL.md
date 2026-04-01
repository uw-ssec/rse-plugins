---
name: rechunking
description: Safely apply chunking configurations to Zarr datasets with validation, progress reporting, memory-bounded execution, and rollback safety. Supports local and cloud storage backends.
metadata:
  references:
    - references/rechunking-strategies.md
    - references/validation-safety.md
  scripts:
    - scripts/rechunk.py
  assets:
    - assets/rechunk-config-example.json
---

# Rechunking Zarr Datasets

**Rechunking is one of the most expensive operations you can perform on a Zarr dataset.** Depending on chunk size and dataset volume, rechunking can take anywhere from approximately 6 minutes to over 46 hours (Nguyen et al., 2023, [DOI: 10.1002/essoar.10511054.2](https://doi.org/10.1002/essoar.10511054.2)). The operation rewrites every byte of data, and an interrupted or misconfigured rechunk can corrupt an entire dataset. This skill wraps the `rechunk.py` script with a safety-first workflow: validate inputs, estimate costs, rechunk to a new location, verify outputs, and only then swap the result into place.

## Resources in This Skill

- **[references/rechunking-strategies.md](references/rechunking-strategies.md):** Deep reference on in-place vs copy rechunking, chunk-at-a-time processing, parallel rechunking with Dask, and cost estimation formulas.
- **[references/validation-safety.md](references/validation-safety.md):** Deep reference on pre- and post-rechunk validation, sample-first strategies, rollback patterns, and common failure modes.
- **[scripts/rechunk.py](scripts/rechunk.py):** CLI tool that performs the actual rechunking operation with validation, progress reporting, and summary output.
- **[assets/rechunk-config-example.json](assets/rechunk-config-example.json):** Example JSON configuration file showing all supported rechunking parameters.

## Quick Reference Card

```bash
# Basic rechunk (local)
python rechunk.py --input /data/source.zarr \
                  --output /data/rechunked.zarr \
                  --chunks "50,512,512"

# Rechunk with memory limit
python rechunk.py --input /data/source.zarr \
                  --output /data/rechunked.zarr \
                  --chunks "100,256,256" \
                  --max-mem "4GB"

# Rechunk cloud data
python rechunk.py --input s3://bucket/source.zarr \
                  --output s3://bucket/rechunked.zarr \
                  --chunks "50,512,512" \
                  --max-mem "4GB"

# Overwrite existing output
python rechunk.py --input /data/source.zarr \
                  --output /data/rechunked.zarr \
                  --chunks "200,128,128" \
                  --overwrite

# Save summary to specific path
python rechunk.py --input /data/source.zarr \
                  --output /data/rechunked.zarr \
                  --chunks "50,512,512" \
                  --summary results/rechunk_report.json

# Verbose mode for debugging
python rechunk.py --input /data/source.zarr \
                  --output /data/rechunked.zarr \
                  --chunks "50,512,512" \
                  --verbose
```

**CLI flags:**

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--input`, `-i` | Yes | — | Input Zarr store path (local or `s3://`) |
| `--output`, `-o` | Yes | — | Output Zarr store path (local or `s3://`) |
| `--chunks`, `-c` | Yes | — | Target chunk shape, comma-separated (e.g., `"50,512,512"`) |
| `--max-mem` | No | `2GB` | Maximum memory for rechunker library |
| `--overwrite` | No | `false` | Overwrite output if it exists |
| `--summary` | No | auto-generated | Path for JSON summary file |
| `--verbose`, `-v` | No | `false` | Enable debug-level logging |

## When to Use

Use this skill when:

1. **Benchmarking has validated an improvement.** The chunking-strategy skill has identified a better chunk configuration, and you are ready to apply it to the full dataset.
2. **Access patterns have changed.** Your workload has shifted (e.g., from spatial-dominant to time-series-dominant access), and the current chunking no longer serves the primary use case.
3. **Migrating between storage backends.** Moving data from local disk to S3/GCS (or vice versa) is an opportunity to rechunk for the target storage characteristics.
4. **Consolidating after incremental writes.** Appended data may have inconsistent chunk boundaries that degrade read performance.

**Do not use this skill** if you have not first benchmarked the proposed chunk configuration. Rechunking is expensive and irreversible without a backup.

## Rechunking Cost Estimation

Nguyen et al. (2023) measured rechunking times across a range of chunk sizes for multi-dimensional scientific datasets stored in cloud object stores:

| Chunk Size Category | Approximate Time | Example Shape |
|---------------------|-----------------|---------------|
| Large chunks | ~6 minutes | `(100, 1024, 1024)` |
| Medium chunks | ~1–4 hours | `(50, 512, 512)` |
| Small chunks | ~10–46 hours | `(1, 64, 64)` |

**Factors affecting rechunking cost:**

- **Dataset total size:** Linear relationship — 2x data means roughly 2x time.
- **Target chunk size:** Smaller target chunks produce more individual files/objects, increasing overhead per chunk.
- **Storage backend latency:** Cloud object stores (S3, GCS) add per-request latency compared to local NVMe.
- **Compression codec:** Compressed data requires decompression during read and recompression during write.
- **Network bandwidth:** For cloud stores, network throughput caps the maximum rechunking speed.
- **Available memory:** More memory allows larger intermediate buffers, reducing the number of read/write cycles.

The `rechunk.py` script reports the Nguyen et al. range (6 minutes to 46 hours) as a guideline because precise estimation requires knowing the specific storage backend and network conditions.

## Using the Rechunk Script

The `scripts/rechunk.py` script performs the following steps automatically:

1. **Validate input** — confirms the source Zarr store exists and is readable, reports shape, chunks, dtype, and compressor.
2. **Validate target chunks** — checks that the target chunk dimensions match the array dimensions, warns if any chunk size exceeds the array extent.
3. **Validate output** — checks whether the output path already exists (requires `--overwrite` to proceed).
4. **Estimate cost** — reports the Nguyen et al. time range and estimated output size.
5. **Rechunk** — uses the `rechunker` library if available (preferred), falls back to manual chunk-by-chunk copy via `zarr.copy`.
6. **Validate output** — confirms shape, chunks, and total element count match the source.
7. **Write summary** — saves a JSON file with timing, validation results, and configuration details.

### Invocation Examples

```bash
# Standard local rechunk
python scripts/rechunk.py \
    --input /data/observations.zarr \
    --output /data/observations_rechunked.zarr \
    --chunks "50,512,512"

# Cloud-to-cloud with increased memory budget
python scripts/rechunk.py \
    --input s3://my-bucket/raw/data.zarr \
    --output s3://my-bucket/optimized/data.zarr \
    --chunks "100,256,256" \
    --max-mem "8GB"
```

## Safety Protocol

Follow this four-step protocol for every rechunking operation:

### Step 1: Sample First

Rechunk a small subset of the data to verify the configuration works before committing to the full dataset.

```bash
# Extract a sample (e.g., first 10 time steps)
python -c "
import zarr
src = zarr.open('/data/full.zarr', 'r')
sample = zarr.open('/tmp/sample.zarr', 'w',
                   shape=(10,) + src.shape[1:],
                   chunks=src.chunks, dtype=src.dtype)
sample[:] = src[:10]
"

# Rechunk the sample
python scripts/rechunk.py \
    --input /tmp/sample.zarr \
    --output /tmp/sample_rechunked.zarr \
    --chunks "5,512,512"
```

### Step 2: Validate the Sample

Inspect the rechunked sample to confirm data integrity:

```python
import zarr
import numpy as np

source = zarr.open('/tmp/sample.zarr', 'r')
result = zarr.open('/tmp/sample_rechunked.zarr', 'r')

assert source.shape == result.shape, "Shape mismatch"
assert source.dtype == result.dtype, "Dtype mismatch"
assert np.array_equal(source[:], result[:]), "Data mismatch"
print("Sample validation passed")
```

### Step 3: Rechunk the Full Dataset

Once the sample passes validation, rechunk the full dataset to a **new path** (never in place):

```bash
python scripts/rechunk.py \
    --input /data/full.zarr \
    --output /data/full_rechunked.zarr \
    --chunks "50,512,512" \
    --max-mem "4GB"
```

### Step 4: Verify and Swap

After the full rechunk completes, verify the output and then swap it into the production path:

```bash
# Verify (the script does basic validation automatically)
# For extra safety, spot-check a few values:
python -c "
import zarr, numpy as np
src = zarr.open('/data/full.zarr', 'r')
dst = zarr.open('/data/full_rechunked.zarr', 'r')
# Check random slices
for idx in [0, len(src)//2, len(src)-1]:
    assert np.array_equal(src[idx], dst[idx]), f'Mismatch at index {idx}'
print('Spot-check passed')
"

# Swap
mv /data/full.zarr /data/full_backup.zarr
mv /data/full_rechunked.zarr /data/full.zarr
```

## Memory-Bounded Execution

The `--max-mem` flag controls how much memory the rechunker library is allowed to use. This is critical for large datasets that do not fit in RAM.

**How it works:**

- When the `rechunker` library is available, `--max-mem` is passed directly to `rechunker.rechunk()`, which plans an execution graph that respects the memory bound.
- When falling back to manual chunk-by-chunk copying, the script processes one target chunk at a time, keeping memory usage proportional to a single chunk size.

**Guidelines for setting `--max-mem`:**

| System Memory | Recommended `--max-mem` | Reasoning |
|---------------|------------------------|-----------|
| 8 GB | `2GB` | Leave headroom for OS and other processes |
| 16 GB | `4GB` | Safe default for most workloads |
| 64 GB | `16GB` | HPC nodes with dedicated rechunking jobs |
| 128+ GB | `32GB` | Large-scale production rechunking |

**Warning:** Setting `--max-mem` too high can cause OOM kills. Setting it too low increases the number of read/write cycles and slows down the operation. Start conservative and increase if rechunking is too slow.

## Cloud Storage Rechunking

When rechunking data stored in S3 or GCS, additional considerations apply:

### Intermediate Storage

The `rechunker` library requires an intermediate (temporary) storage location. The script automatically creates a temporary directory for this purpose. For cloud-to-cloud rechunking, the intermediate store is created locally by default. To use cloud intermediate storage:

```python
# In custom scripts, specify cloud intermediate storage
import rechunker
plan = rechunker.rechunk(
    source, target_chunks=chunks,
    max_mem="4GB",
    target_store="s3://bucket/output.zarr",
    temp_store="s3://bucket/tmp/rechunk_temp"
)
plan.execute()
```

### S3/GCS Considerations

- **Egress costs:** Rechunking reads every byte. For large datasets, this can incur significant egress charges if reading cross-region.
- **Request rate limits:** Small target chunks generate many PUT requests. S3 has a per-prefix request rate limit (5,500 GET/s, 3,500 PUT/s). Use larger chunks or partition across prefixes.
- **Consistency:** S3 provides strong read-after-write consistency. GCS provides strong consistency for all operations. Both are safe for rechunking.
- **Credentials:** The script uses `s3fs` for S3 access. Ensure AWS credentials are configured (`~/.aws/credentials` or environment variables).

## Validation Steps

### Before Rechunking (Pre-Validation)

1. **Check source integrity:** Open the source store and confirm it is readable.
2. **Verify chunk compatibility:** Ensure target chunk dimensions match the array dimensions.
3. **Check disk space:** Estimate the output size and confirm sufficient space is available at the output path.
4. **Review the plan:** The script logs the rechunking plan (source shape, source chunks, target chunks, estimated size) before proceeding.

### After Rechunking (Post-Validation)

The script automatically validates:

1. **Shape match:** Output array shape equals source array shape.
2. **Chunk match:** Output chunks equal the requested target chunks.
3. **Size match:** Total number of elements is preserved.

For additional validation beyond what the script provides:

```python
import zarr
import numpy as np

src = zarr.open("source.zarr", "r")
dst = zarr.open("output.zarr", "r")

# Dtype check
assert src.dtype == dst.dtype, "Dtype mismatch"

# Metadata check
for key in src.attrs:
    assert key in dst.attrs, f"Missing attribute: {key}"
    assert src.attrs[key] == dst.attrs[key], f"Attribute mismatch: {key}"

# Value sampling (spot-check random positions)
rng = np.random.default_rng(42)
for _ in range(100):
    idx = tuple(rng.integers(0, s) for s in src.shape)
    assert src[idx] == dst[idx], f"Value mismatch at {idx}"
```

## Rollback Strategy

The safest approach to rechunking follows a write-verify-swap pattern:

1. **Write to a new location.** Never rechunk in place. Always write to a separate output path.
2. **Verify the output.** Run shape, dtype, element count, and value-sampling checks.
3. **Swap paths.** Rename the original to a backup path, rename the rechunked output to the original path.
4. **Keep the backup.** Retain the original dataset until you have confirmed the rechunked version works in production.
5. **Clean up.** Delete the backup only after thorough validation in production.

```bash
# Swap pattern
mv /data/dataset.zarr /data/dataset_backup.zarr
mv /data/dataset_rechunked.zarr /data/dataset.zarr

# After validation in production
rm -rf /data/dataset_backup.zarr
```

For cloud storage, use versioned buckets or copy to a backup prefix before swapping.

## Common Mistakes

1. **Not benchmarking first.** Rechunking without benchmarking is guessing. Use the chunking-strategy skill to identify the optimal configuration before rechunking.
2. **Insufficient disk space.** Rechunking requires enough space for both the source and the output (and possibly intermediate storage). Check available space before starting.
3. **No post-rechunk validation.** The script validates shape, chunks, and element count, but does not verify individual values. Always spot-check data values after rechunking.
4. **Rechunking in place.** Overwriting the source data during rechunking risks total data loss if the operation fails. Always write to a new location.
5. **Ignoring memory limits.** Not setting `--max-mem` appropriately can cause OOM errors that corrupt the output. Start conservative.
6. **Skipping the sample step.** Rechunking a 10 TB dataset without first testing on a sample wastes hours if the configuration is wrong.

## Best Practices

- **Always benchmark first.** Use the chunking-strategy skill to validate that the proposed chunk configuration actually improves performance for your access patterns.
- **Rechunk to a new path.** Never use `--overwrite` on the source path. Write to a separate output and swap after validation.
- **Validate on a sample.** Rechunk a small subset first to catch configuration errors quickly.
- **Monitor memory.** Use `--verbose` to watch memory usage during rechunking. If the process is killed by OOM, reduce `--max-mem`.
- **Save the summary.** Use `--summary` to keep a record of every rechunking operation for reproducibility.
- **Keep backups.** Retain the original dataset until the rechunked version is validated in production.
- **Use the rechunker library.** Install `rechunker` for better memory management and execution planning. The fallback chunk-by-chunk copy works but is slower and less memory-efficient.

## Resources

### Research Papers
- Nguyen et al. (2023): [DOI 10.1002/essoar.10511054.2](https://doi.org/10.1002/essoar.10511054.2) — Impact of chunk size on read performance, rechunking time estimates.

### Tools
- **rechunker:** https://rechunker.readthedocs.io/ — Memory-bounded rechunking library for Zarr.
- **Zarr:** https://zarr.readthedocs.io/ — Chunked, compressed N-dimensional array storage.
- **s3fs:** https://s3fs.readthedocs.io/ — Pythonic file interface to S3.

### Related Skills
- **chunking-strategy:** Benchmark chunk configurations before rechunking.

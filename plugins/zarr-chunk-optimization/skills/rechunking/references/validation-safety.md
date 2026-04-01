# Validation & Safety — Deep Reference

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| Pre-Rechunk Validation | 16–107 | Checks to perform before starting a rechunking operation |
| Post-Rechunk Validation | 108–184 | Verifying that the rechunked output matches the source |
| Sample-First Strategy | 185–261 | Rechunking a subset before committing to the full dataset |
| Rollback Patterns | 262–331 | Atomic swap, backup strategies, and recovery procedures |
| Data Integrity Checks | 332–403 | Checksum comparison and statistical validation methods |
| Common Failure Modes | 404–484 | OOM during rechunk, interrupted writes, and corrupted chunks |

---

## Pre-Rechunk Validation

Before starting any rechunking operation, validate the following conditions. The `rechunk.py` script performs steps 1–3 automatically; steps 4–6 require manual verification.

### 1. Source Integrity

Confirm the source Zarr store is readable and contains valid data:

```python
import zarr

source = zarr.open("/data/source.zarr", mode="r")
assert isinstance(source, zarr.Array), "Source is not a Zarr array"
print(f"Shape: {source.shape}")
print(f"Chunks: {source.chunks}")
print(f"Dtype: {source.dtype}")
print(f"Compressor: {source.compressor}")
```

If the source is a Zarr group containing multiple arrays, verify each array independently.

### 2. Disk Space

Estimate the output size and confirm sufficient free space:

```python
import numpy as np
import shutil

source = zarr.open("/data/source.zarr", mode="r")
uncompressed_bytes = np.prod(source.shape) * source.dtype.itemsize
estimated_gb = uncompressed_bytes / (1024**3)

# Check available space at output location
free_gb = shutil.disk_usage("/data").free / (1024**3)

print(f"Estimated output size: {estimated_gb:.1f} GB (uncompressed)")
print(f"Available disk space: {free_gb:.1f} GB")

# Need space for output + intermediate store
assert free_gb > estimated_gb * 2.5, "Insufficient disk space (need 2.5x dataset size)"
```

The 2.5x multiplier accounts for the output (1x) plus intermediate storage (1x) plus headroom (0.5x).

### 3. Chunk Compatibility

Verify that target chunk dimensions match the array dimensions:

```python
target_chunks = (50, 512, 512)
assert len(target_chunks) == len(source.shape), \
    f"Dimension mismatch: target has {len(target_chunks)} dims, source has {len(source.shape)}"

for i, (chunk, extent) in enumerate(zip(target_chunks, source.shape)):
    assert chunk > 0, f"Chunk size must be positive (dim {i}: {chunk})"
    if chunk > extent:
        print(f"Warning: chunk size {chunk} exceeds extent {extent} for dim {i}")
```

### 4. Compression Compatibility

If specifying a different compressor for the output, verify it is installed:

```python
import numcodecs
compressor = numcodecs.Blosc(cname='zstd', clevel=3)
test_data = np.random.rand(100).astype(source.dtype)
compressed = compressor.encode(test_data)
decompressed = compressor.decode(compressed)
assert np.array_equal(test_data, np.frombuffer(decompressed, dtype=source.dtype))
```

### 5. Cloud Credentials

For S3/GCS sources or outputs, verify credentials before starting:

```python
import s3fs
fs = s3fs.S3FileSystem()
assert fs.exists("s3://bucket/source.zarr/.zarray"), "Cannot access source in S3"
```

### 6. Output Path Safety

Confirm the output path does not contain valuable data that would be overwritten:

```bash
# Check if output path exists
ls -la /data/output.zarr 2>/dev/null && echo "WARNING: Output path exists" || echo "Output path is clear"
```

## Post-Rechunk Validation

After rechunking completes, validate the output thoroughly before swapping it into production.

### Automatic Validation (Built into rechunk.py)

The `rechunk.py` script automatically checks:

1. **Shape match:** `output.shape == source.shape`
2. **Chunk match:** `output.chunks == target_chunks`
3. **Element count:** `output.size == source.size`

These checks catch gross errors (wrong dimensions, truncated data) but do not verify individual values.

### Manual Validation (Recommended)

#### Dtype Verification

```python
source = zarr.open("/data/source.zarr", "r")
output = zarr.open("/data/output.zarr", "r")

assert source.dtype == output.dtype, \
    f"Dtype mismatch: source={source.dtype}, output={output.dtype}"
```

#### Metadata Preservation

```python
# Check all user-defined attributes were preserved
for key in source.attrs:
    assert key in output.attrs, f"Missing attribute: {key}"
    assert source.attrs[key] == output.attrs[key], \
        f"Attribute mismatch for '{key}': {source.attrs[key]} != {output.attrs[key]}"
```

#### Value Sampling

Spot-check values at random positions to detect data corruption:

```python
import numpy as np

rng = np.random.default_rng(42)
num_samples = 1000

for _ in range(num_samples):
    idx = tuple(rng.integers(0, s) for s in source.shape)
    src_val = source[idx]
    dst_val = output[idx]

    if np.isnan(src_val) and np.isnan(dst_val):
        continue  # NaN == NaN is False, but both being NaN is correct

    assert src_val == dst_val, f"Value mismatch at {idx}: {src_val} != {dst_val}"

print(f"Value sampling passed ({num_samples} random positions)")
```

#### Full Comparison (Small Datasets Only)

For datasets that fit in memory, perform a full element-wise comparison:

```python
# Only for datasets that fit in RAM
assert np.array_equal(source[:], output[:]), "Full data comparison failed"
```

For large datasets, compare slice by slice:

```python
for i in range(source.shape[0]):
    assert np.array_equal(source[i], output[i]), f"Mismatch at index {i}"
    if i % 100 == 0:
        print(f"Validated slice {i}/{source.shape[0]}")
```

## Sample-First Strategy

Always rechunk a small sample before processing the full dataset. This catches configuration errors, estimates actual rechunking speed, and validates the output format — all within minutes instead of hours.

### Creating a Sample

Extract a representative subset of the source data:

```python
import zarr
import numpy as np

source = zarr.open("/data/full_dataset.zarr", mode="r")

# Take the first N elements along the first dimension
sample_size = min(20, source.shape[0])
sample_shape = (sample_size,) + source.shape[1:]

sample = zarr.open(
    "/tmp/rechunk_sample.zarr", mode="w",
    shape=sample_shape,
    chunks=source.chunks,
    dtype=source.dtype,
    compressor=source.compressor
)
sample[:] = source[:sample_size]
sample.attrs.update(source.attrs)
```

### Rechunking the Sample

```bash
python rechunk.py \
    --input /tmp/rechunk_sample.zarr \
    --output /tmp/rechunk_sample_output.zarr \
    --chunks "10,512,512"
```

### Validating the Sample

```python
source_sample = zarr.open("/tmp/rechunk_sample.zarr", "r")
output_sample = zarr.open("/tmp/rechunk_sample_output.zarr", "r")

# Full comparison is feasible for small samples
assert source_sample.shape == output_sample.shape
assert source_sample.dtype == output_sample.dtype
assert np.array_equal(source_sample[:], output_sample[:])
print("Sample validation passed")
```

### Estimating Full Rechunk Time

Use the sample timing to estimate the full dataset rechunking time:

```python
import json

with open("rechunk_summary_*.json") as f:
    summary = json.load(f)

sample_time = summary["actual_time_seconds"]
sample_elements = np.prod(summary["array_shape"])
full_elements = np.prod(source.shape)

estimated_full_time = sample_time * (full_elements / sample_elements)
print(f"Estimated full rechunk time: {estimated_full_time / 3600:.1f} hours")
```

### Decision Criteria

After validating the sample:

- **Proceed** if: shape/dtype/values match, estimated time is acceptable, memory usage is within budget.
- **Abort** if: values differ, memory usage exceeds budget, estimated time is unacceptable.
- **Adjust** if: rechunking works but is too slow — try larger `--max-mem` or install the `rechunker` library for parallel execution.

## Rollback Patterns

### Pattern 1: Atomic Swap (Recommended)

Write to a new location, verify, then swap paths atomically:

```bash
# Step 1: Rechunk to new path
python rechunk.py --input /data/dataset.zarr \
                  --output /data/dataset_new.zarr \
                  --chunks "50,512,512"

# Step 2: Verify (automated + manual checks)
python validate.py --source /data/dataset.zarr --target /data/dataset_new.zarr

# Step 3: Atomic swap
mv /data/dataset.zarr /data/dataset_old.zarr
mv /data/dataset_new.zarr /data/dataset.zarr

# Step 4: Keep backup until production is confirmed stable
# (days or weeks later)
rm -rf /data/dataset_old.zarr
```

**On Linux/macOS,** `mv` within the same filesystem is atomic at the directory level. Cross-filesystem moves are not atomic — use `rsync` followed by `rm` instead.

### Pattern 2: Versioned Backups

For datasets that are rechunked periodically, use versioned paths:

```bash
/data/dataset_v1.zarr          # Original
/data/dataset_v2.zarr          # First rechunk
/data/dataset_v3.zarr          # Second rechunk
/data/dataset_current.zarr -> dataset_v3.zarr  # Symlink to current version
```

Update the symlink atomically:

```bash
ln -sfn /data/dataset_v3.zarr /data/dataset_current.zarr
```

### Pattern 3: Cloud Versioning

For S3-hosted datasets, enable bucket versioning to provide automatic rollback:

```bash
aws s3api put-bucket-versioning \
    --bucket my-bucket \
    --versioning-configuration Status=Enabled
```

With versioning enabled, overwritten objects can be restored to previous versions. This provides a safety net but should not replace the write-verify-swap pattern.

### Pattern 4: Copy-on-Write Filesystems

On ZFS or Btrfs, use filesystem snapshots before rechunking:

```bash
# ZFS
zfs snapshot tank/data@before-rechunk

# Rechunk
python rechunk.py --input /data/dataset.zarr --output /data/dataset_new.zarr --chunks "50,512,512"

# If something goes wrong
zfs rollback tank/data@before-rechunk
```

## Data Integrity Checks

### Checksum Comparison

Compute checksums of the source and output data for definitive integrity verification:

```python
import hashlib
import zarr
import numpy as np

def compute_array_checksum(path: str) -> str:
    """Compute SHA-256 checksum of all data in a Zarr array."""
    arr = zarr.open(path, mode="r")
    hasher = hashlib.sha256()

    # Process slice by slice to avoid loading entire array into memory
    for i in range(arr.shape[0]):
        data = arr[i]
        hasher.update(data.tobytes())

    return hasher.hexdigest()

source_hash = compute_array_checksum("/data/source.zarr")
output_hash = compute_array_checksum("/data/output.zarr")

assert source_hash == output_hash, "Checksum mismatch — data corruption detected"
print(f"Checksum match: {source_hash}")
```

### Statistical Validation

For very large datasets where full checksum comparison is too slow, use statistical methods:

```python
source = zarr.open("/data/source.zarr", "r")
output = zarr.open("/data/output.zarr", "r")

# Compare summary statistics per slice
for i in range(source.shape[0]):
    src_slice = source[i]
    dst_slice = output[i]

    assert np.isclose(np.mean(src_slice), np.mean(dst_slice), rtol=1e-7), \
        f"Mean mismatch at slice {i}"
    assert np.isclose(np.std(src_slice), np.std(dst_slice), rtol=1e-7), \
        f"Std mismatch at slice {i}"
    assert np.nanmin(src_slice) == np.nanmin(dst_slice), \
        f"Min mismatch at slice {i}"
    assert np.nanmax(src_slice) == np.nanmax(dst_slice), \
        f"Max mismatch at slice {i}"
```

### NaN and Special Value Handling

Rechunking should preserve NaN, Inf, and other special floating-point values:

```python
src_data = source[0]
dst_data = output[0]

# Check NaN positions match
assert np.array_equal(np.isnan(src_data), np.isnan(dst_data)), "NaN positions differ"

# Check Inf positions match
assert np.array_equal(np.isinf(src_data), np.isinf(dst_data)), "Inf positions differ"

# Check finite values match
finite_mask = np.isfinite(src_data)
assert np.array_equal(src_data[finite_mask], dst_data[finite_mask]), "Finite values differ"
```

## Common Failure Modes

### 1. Out-of-Memory (OOM) During Rechunking

**Symptoms:** Process killed by OS (exit code 137 on Linux), `MemoryError` exception, system becomes unresponsive.

**Causes:**
- `--max-mem` set too high for available system memory.
- Target chunk size is very large, causing individual chunks to exceed available RAM.
- Memory leak in compression codec (rare but possible with certain Blosc configurations).

**Prevention:**
- Set `--max-mem` to no more than 25% of system RAM.
- Verify that individual target chunks fit in memory: `chunk_elements × bytes_per_element < available_RAM / 4`.
- Monitor memory usage with `--verbose` during the sample rechunk.

**Recovery:** The output is likely incomplete or corrupted. Delete it and restart with a lower `--max-mem` value.

### 2. Interrupted Writes

**Symptoms:** Rechunking process terminated (Ctrl+C, network disconnect, system crash) before completion.

**Causes:**
- User interruption during a long rechunking operation.
- Network timeout during cloud storage write.
- System shutdown or crash.

**Prevention:**
- Use the write-to-new-location pattern so the source is never affected.
- For cloud storage, use a reliable network connection and consider running on a cloud instance in the same region as the storage.

**Recovery:** Delete the incomplete output and restart. The source data is safe (assuming you wrote to a new location).

### 3. Corrupted Chunks

**Symptoms:** `zarr.open()` succeeds but reading specific chunks raises exceptions (`ValueError`, `RuntimeError` from the compressor).

**Causes:**
- Partial write to a chunk file (interrupted during compression or flush).
- Disk full during write (chunk file created but truncated).
- Cloud storage eventual consistency issues (mostly historical — modern S3 is strongly consistent).

**Detection:**

```python
import zarr

arr = zarr.open("/data/output.zarr", mode="r")
errors = []

for i in range(arr.shape[0]):
    try:
        _ = arr[i]
    except Exception as e:
        errors.append((i, str(e)))

if errors:
    print(f"Found {len(errors)} corrupted slices:")
    for idx, msg in errors[:10]:
        print(f"  Slice {idx}: {msg}")
```

**Recovery:** Delete the corrupted output and rechunk again. If corruption is in the source, restore from backup or upstream pipeline.

### 4. Metadata Loss

**Symptoms:** Rechunked dataset is missing user-defined attributes (units, coordinate labels, provenance).

**Causes:**
- Fallback chunk-by-chunk copy correctly transfers attributes via `output_array.attrs.update(source_array.attrs)`, but custom scripts may omit this step.
- Zarr group-level attributes may not be copied when rechunking individual arrays within a group.

**Prevention:** Always verify metadata preservation as part of post-rechunk validation (see Post-Rechunk Validation section above).

**Recovery:** Copy attributes from the source to the output manually:

```python
source = zarr.open("/data/source.zarr", "r")
output = zarr.open("/data/output.zarr", "r+")
output.attrs.update(source.attrs)
```

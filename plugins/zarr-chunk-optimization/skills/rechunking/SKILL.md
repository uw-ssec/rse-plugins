---
name: rechunking
description: Safely applies chunking configurations to Zarr datasets with validation, progress reporting, memory-bounded execution, and rollback safety. Supports local, S3, and GCS storage backends. Use when the user needs to rechunk a .zarr dataset, change chunk sizes, optimize Zarr storage layout, or apply a chunk configuration identified by benchmarking.
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

Rechunking rewrites every byte of a dataset. Depending on target chunk size and dataset volume, it can take 6 minutes to 46+ hours (Nguyen et al., 2023). **Always benchmark before rechunking** — use the `chunking-strategy` skill to identify the optimal configuration first.

## Resources

| Resource | Purpose |
|----------|---------|
| [references/rechunking-strategies.md](references/rechunking-strategies.md) | In-place vs copy, parallel rechunking with Dask, cost estimation, progress monitoring |
| [references/validation-safety.md](references/validation-safety.md) | Pre/post validation, sample-first strategy, rollback patterns, failure modes |
| [scripts/rechunk.py](scripts/rechunk.py) | CLI tool: validation, progress reporting, memory-bounded execution, JSON summary |
| [assets/rechunk-config-example.json](assets/rechunk-config-example.json) | Example config with all supported parameters |

## CLI Reference

```bash
# Local rechunk
python scripts/rechunk.py --input /data/source.zarr --output /data/rechunked.zarr --chunks "50,512,512"

# Cloud rechunk with memory limit
python scripts/rechunk.py --input s3://bucket/source.zarr --output s3://bucket/rechunked.zarr \
  --chunks "100,256,256" --max-mem "4GB"

# With JSON summary saved to a specific path
python scripts/rechunk.py --input /data/source.zarr --output /data/rechunked.zarr \
  --chunks "50,512,512" --summary results/rechunk_report.json
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--input`, `-i` | Yes | — | Source Zarr store (local or `s3://`/`gs://`) |
| `--output`, `-o` | Yes | — | Output Zarr store (must differ from input) |
| `--chunks`, `-c` | Yes | — | Target chunk shape, comma-separated |
| `--max-mem` | No | `2GB` | Memory budget for rechunker library |
| `--overwrite` | No | false | Overwrite output if it exists |
| `--summary` | No | auto | Path for JSON summary file |
| `--verbose`, `-v` | No | false | Debug-level logging |

## Safety Protocol

Every rechunking operation follows four steps. Do not skip steps.

**Step 1 — Sample first.** Rechunk a small subset to catch configuration errors cheaply:

```bash
python -c "
import zarr
src = zarr.open('/data/full.zarr', 'r')
s = zarr.open('/tmp/sample.zarr', 'w', shape=(10,)+src.shape[1:], chunks=src.chunks, dtype=src.dtype)
s[:] = src[:10]
"
python scripts/rechunk.py --input /tmp/sample.zarr --output /tmp/sample_rechunked.zarr --chunks "5,512,512"
```

**Step 2 — Validate the sample:**

```python
import zarr, numpy as np
src = zarr.open('/tmp/sample.zarr', 'r')
dst = zarr.open('/tmp/sample_rechunked.zarr', 'r')
assert src.shape == dst.shape and src.dtype == dst.dtype
assert np.array_equal(src[:], dst[:])
print("Sample OK")
```

**Step 3 — Rechunk the full dataset to a new path** (never in place):

```bash
python scripts/rechunk.py --input /data/full.zarr --output /data/full_rechunked.zarr \
  --chunks "50,512,512" --max-mem "4GB"
```

**Step 4 — Verify and swap:**

```bash
# Spot-check values
python -c "
import zarr, numpy as np
src = zarr.open('/data/full.zarr', 'r')
dst = zarr.open('/data/full_rechunked.zarr', 'r')
for i in [0, len(src)//2, len(src)-1]:
    assert np.array_equal(src[i], dst[i]), f'Mismatch at {i}'
print('Spot-check passed')
"
# Swap
mv /data/full.zarr /data/full_backup.zarr
mv /data/full_rechunked.zarr /data/full.zarr
# Delete backup only after confirming rechunked version works in production
```

For cloud storage: use versioned buckets or copy to a backup prefix before swapping. See [rechunking-strategies.md](references/rechunking-strategies.md) for intermediate storage patterns and Dask parallelism.

## Memory Budget

Set `--max-mem` to ≈25% of available system RAM to leave headroom for OS and I/O buffers. The `rechunker` library uses this budget to plan a memory-safe execution graph; the fallback chunk-by-chunk copy processes one target chunk at a time.

## What the Script Validates Automatically

1. Source store exists and is readable
2. Target chunk dimensions match array dimensions
3. Output path does not already exist (unless `--overwrite`)
4. Post-rechunk: shape, chunk shape, and total element count match source

See [validation-safety.md](references/validation-safety.md) for additional value-sampling and checksum checks to run manually.

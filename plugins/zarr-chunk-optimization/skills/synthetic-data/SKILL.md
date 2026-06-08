---
name: synthetic-data
description: Generates synthetic Zarr datasets with configurable dimensions, shapes, data types, and compression for controlled chunking benchmarks. Supports local and cloud storage backends (S3, GCS). Use when the user needs to create test Zarr datasets for benchmarking, generate synthetic array data for performance testing, or create reproducible benchmark inputs without access to production data.
metadata:
  references:
    - references/dataset-design.md
  scripts:
    - scripts/synthetic_data.py
  assets:
    - assets/synthetic-config-example.json
---

# Synthetic Data Generation for Chunking Benchmarks

Generate controlled Zarr datasets for benchmarking chunking strategies when production data is unavailable or unsuitable.

## Resources

| Resource | Purpose |
|----------|---------|
| [references/dataset-design.md](references/dataset-design.md) | Dimensions, dtypes, compression codecs, storage backends, scaling, reproducibility — all design decisions in depth |
| [scripts/synthetic_data.py](scripts/synthetic_data.py) | CLI tool: configurable shape, chunks, dtype, compression, data patterns, cloud output, sampling from existing stores |
| [assets/synthetic-config-example.json](assets/synthetic-config-example.json) | Example JSON config with all parameters |

## Generate and Validate (Workflow)

**Step 1 — Generate:**

```bash
# General benchmark dataset
python scripts/synthetic_data.py --output /tmp/test.zarr \
    --shape 1000,2048,2048 --chunks 50,256,256 --seed 42

# Climate-like (spatial gradients + temporal variation)
python scripts/synthetic_data.py --output /tmp/climate.zarr \
    --shape 3650,180,360 --chunks 365,90,180 \
    --dims time,lat,lon --pattern temperature --dtype float32 --seed 42

# Radio astronomy (complex Gaussian noise)
python scripts/synthetic_data.py --output /tmp/radio.zarr \
    --shape 1000,2048,2048 --chunks 50,256,256 \
    --dims time,frequency,baseline --pattern radio --seed 42

# To S3 (requires AWS credentials)
python scripts/synthetic_data.py --output s3://bucket/synthetic.zarr \
    --shape 500,1024,1024 --chunks 50,256,256 --compression zstd --seed 42

# Sample from an existing Zarr store
python scripts/synthetic_data.py --sample-from /data/full.zarr \
    --output /tmp/sample.zarr --target-size 8

# No compression (isolate raw I/O)
python scripts/synthetic_data.py --output /tmp/raw.zarr \
    --shape 500,512,512 --chunks 50,128,128 --compression none --seed 42
```

**Step 2 — Validate before benchmarking:**

```python
import zarr
import numpy as np

z = zarr.open("/tmp/test.zarr", mode="r")
assert z.shape == (1000, 2048, 2048), f"Shape mismatch: {z.shape}"
assert z.chunks == (50, 256, 256), f"Chunks mismatch: {z.chunks}"
assert z.dtype == np.float32, f"Dtype mismatch: {z.dtype}"
print(f"Shape: {z.shape} | Chunks: {z.chunks} | Dtype: {z.dtype}")
print(f"Pattern: {z.attrs.get('pattern_type')} | Seed: {z.attrs.get('random_seed')}")

# Spot-check values are finite and non-constant
sample = z[0:5]
assert np.all(np.isfinite(sample)), "Non-finite values found"
assert np.std(sample) > 0, "Data appears constant (check --pattern)"
```

**If validation fails:**
- Shape/chunks mismatch → check that `--shape` and `--chunks` have the same number of dimensions.
- Non-finite values → use `--pattern temperature` or `--pattern radio` instead of `--pattern random` for domain-realistic ranges.
- `std == 0` → `--pattern constant` was used unintentionally; switch to `--pattern random` or `--pattern temperature`.

## CLI Reference

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--output`, `-o` | Yes | — | Output path (local or `s3://`) |
| `--shape` | Yes* | — | Comma-separated array shape |
| `--chunks` | Yes* | — | Comma-separated chunk shape |
| `--dims` | No | `dim_0,...` | Comma-separated dimension names |
| `--dtype` | No | `float32` | Array data type |
| `--compression` | No | `zstd` | Codec: `zstd`, `blosc`, `gzip`, `none` |
| `--compression-level` | No | `3` | Compression level |
| `--pattern` | No | `random` | `random`, `temperature`, `radio`, `constant` |
| `--seed` | No | `42` | Random seed for reproducibility |
| `--overwrite` | No | false | Overwrite existing output |
| `--sample-from` | No | — | Sample from existing Zarr store |
| `--target-size` | No | `8.0` | Target sample size in GB |
| `--verbose`, `-v` | No | false | Debug logging |

*Required when not using `--sample-from`.

## Key Design Rules

- Match `--dtype` to your production data (`float32` is the most common scientific dtype — using `float64` doubles chunk size and skews results).
- Always set `--seed` explicitly and record it; default is `42`.
- Generate datasets with and without compression to isolate codec overhead.
- Keep chunk dimensions as even divisors of the array shape to avoid partial edge chunks.

See [dataset-design.md](references/dataset-design.md) for dimension selection, scaling strategies, storage backend configuration, and compression codec guidance.

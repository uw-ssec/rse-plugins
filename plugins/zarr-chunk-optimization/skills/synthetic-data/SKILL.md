---
name: synthetic-data
description: Generate synthetic Zarr datasets with configurable dimensions, shapes, data types, and compression for controlled chunking benchmarks. Supports local and cloud storage backends (S3, GCS).
metadata:
  references:
    - references/dataset-design.md
  scripts:
    - scripts/synthetic_data.py
  assets:
    - assets/synthetic-config-example.json
---

# Synthetic Data Generation for Chunking Benchmarks

Controlled benchmarking requires controlled data. When evaluating chunking strategies, using production datasets introduces variables that obscure results: irregular shapes, missing values, network variability, and access restrictions. Synthetic data eliminates these confounders by giving you full control over dimensions, shapes, data types, compression, and statistical patterns. Tests become reproducible across environments, no credentials or cloud access are needed for initial exploration, and you can systematically vary one parameter at a time to isolate its effect on performance.

## Resources in This Skill

- **[references/dataset-design.md](references/dataset-design.md):** Deep reference on choosing dimensions, shapes, data types, compression codecs, scaling strategies, and reproducibility practices for synthetic benchmark datasets.
- **[scripts/synthetic_data.py](scripts/synthetic_data.py):** CLI tool that generates synthetic Zarr arrays with configurable shape, chunks, dtype, compression, and data patterns. Also supports creating representative samples from existing Zarr stores.
- **[assets/synthetic-config-example.json](assets/synthetic-config-example.json):** Example JSON configuration template showing all available parameters for synthetic dataset generation.

## Quick Reference Card

```bash
# Generate a 3D dataset with default settings (random pattern, zstd compression)
python synthetic_data.py --output /tmp/test.zarr \
    --shape 1000,2048,2048 --chunks 50,256,256

# Generate climate-like data with named dimensions
python synthetic_data.py --output /tmp/climate.zarr \
    --shape 3650,180,360 --chunks 365,90,180 \
    --dims time,lat,lon --pattern temperature --dtype float32

# Generate radio telescope-like data
python synthetic_data.py --output /tmp/radio.zarr \
    --shape 1000,2048,2048 --chunks 50,256,256 \
    --dims time,frequency,baseline --pattern radio

# Write to S3
python synthetic_data.py --output s3://bucket/synthetic.zarr \
    --shape 500,1024,1024 --chunks 50,256,256 --compression zstd

# Create a sample from an existing Zarr store
python synthetic_data.py --sample-from /data/full.zarr \
    --output /tmp/sample.zarr --target-size 8

# No compression (useful for measuring raw I/O)
python synthetic_data.py --output /tmp/raw.zarr \
    --shape 500,512,512 --chunks 50,128,128 --compression none
```

## When to Use

- No production data is available yet and you need to begin benchmarking
- You want controlled experiments where only one variable changes at a time
- You need reproducible benchmarks that any collaborator can regenerate without data access
- You are testing chunking configurations before committing to cloud storage costs
- You want to compare compression codec performance on data with known statistical properties
- You need to validate your benchmarking pipeline before running it on real data

## Dataset Design Considerations

Designing a useful synthetic dataset means matching the characteristics that matter for chunking performance while keeping generation fast and storage small.

### Dimensions and Shapes

Choose dimensions that mirror your production data structure. The number of dimensions and their relative sizes directly affect how many chunks each access pattern touches.

- **3D datasets** are the most common benchmark target: `(time, spatial_1, spatial_2)` or `(time, frequency, baseline)`
- **4D datasets** add complexity: `(time, level, lat, lon)` for atmospheric models
- Keep at least one dimension large enough that it must be chunked (hundreds to thousands of elements)
- Make dimensions different sizes to test asymmetric chunking strategies

### Chunk Sizes

Chunk shape determines the unit of I/O. When designing test configurations:

- Target individual chunk sizes between **1 MB and 100 MB** for cloud object stores
- For local disk, chunks between **100 KB and 50 MB** are typical
- Ensure chunk dimensions evenly divide the array shape when possible to avoid partial chunks
- Test multiple chunk shapes that favor different access patterns

### Data Types

The dtype determines bytes per element and directly affects chunk size in bytes:

| dtype | Bytes per element | 256x256 chunk size |
|-------|------------------|--------------------|
| float32 | 4 | 256 KB |
| float64 | 8 | 512 KB |
| int16 | 2 | 128 KB |
| complex64 | 8 | 512 KB |

Use `float32` as the default unless your production data uses a different type. Using `float64` when your real data is `float32` will double chunk sizes and skew benchmark results.

## Using the Synthetic Data Script

### CLI Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--output, -o` | Yes | — | Output path (local or `s3://...`) |
| `--shape` | Yes* | — | Comma-separated array shape |
| `--chunks` | Yes* | — | Comma-separated chunk shape |
| `--dims` | No | `dim_0,dim_1,...` | Comma-separated dimension names |
| `--dtype` | No | `float32` | Array data type |
| `--compression` | No | `zstd` | Codec: `zstd`, `blosc`, `gzip`, `none` |
| `--compression-level` | No | `3` | Compression level |
| `--pattern` | No | `random` | Data pattern: `random`, `temperature`, `radio`, `constant` |
| `--seed` | No | `42` | Random seed for reproducibility |
| `--overwrite` | No | `false` | Overwrite existing output |
| `--sample-from` | No | — | Path to existing Zarr to sample from |
| `--target-size` | No | `8.0` | Target sample size in GB |
| `--verbose, -v` | No | `false` | Enable verbose logging |

*Required when not using `--sample-from`.

### Common Invocations

**Small test dataset for quick iteration:**
```bash
python synthetic_data.py -o /tmp/small.zarr \
    --shape 100,256,256 --chunks 10,64,64
```

**Production-scale test (several GB):**
```bash
python synthetic_data.py -o /tmp/large.zarr \
    --shape 5000,2048,2048 --chunks 100,512,512 \
    --dtype float32 --compression zstd
```

**Multiple compression comparison (run sequentially):**
```bash
for codec in zstd blosc gzip none; do
    python synthetic_data.py -o /tmp/test_${codec}.zarr \
        --shape 1000,1024,1024 --chunks 50,256,256 \
        --compression $codec --overwrite
done
```

**Create a manageable sample from a large existing dataset:**
```bash
python synthetic_data.py --sample-from s3://bucket/full_data.zarr \
    --output /tmp/sample.zarr --target-size 4
```

## Storage Backend Configuration

### Local Filesystem

Local storage is the default. Provide any valid filesystem path:

```bash
python synthetic_data.py -o /data/benchmarks/test.zarr \
    --shape 500,1024,1024 --chunks 50,256,256
```

Local storage is best for initial development and pipeline validation. Disk I/O characteristics differ significantly from cloud object stores, so local benchmarks should not be used to predict cloud performance.

### Amazon S3

Provide an `s3://` URL. The script uses `s3fs` and requires AWS credentials configured via environment variables, `~/.aws/credentials`, or IAM role:

```bash
export AWS_PROFILE=my-profile
python synthetic_data.py -o s3://my-bucket/benchmarks/test.zarr \
    --shape 1000,1024,1024 --chunks 50,256,256
```

Ensure the bucket region matches your compute region to minimize latency.

### Google Cloud Storage

GCS support requires `gcsfs` to be installed. Provide a `gcs://` URL:

```bash
python synthetic_data.py -o gcs://my-bucket/benchmarks/test.zarr \
    --shape 1000,1024,1024 --chunks 50,256,256
```

Note: GCS support is listed in the script interface but requires additional implementation. Verify `gcsfs` is installed and authentication is configured before use.

## Generating Domain-Specific Test Data

The `--pattern` flag controls the statistical structure of generated data. Matching the pattern to your domain improves the realism of compression benchmarks, since compression ratios depend on data regularity.

### Climate Grid Data

Climate and weather datasets typically have strong spatial structure and temporal periodicity:

```bash
python synthetic_data.py -o /tmp/climate.zarr \
    --shape 3650,180,360 --chunks 365,90,180 \
    --dims time,lat,lon --pattern temperature --seed 42
```

The `temperature` pattern generates spatial gradients with sinusoidal temporal variation, mimicking surface temperature fields.

### Radio Astronomy

Radio interferometer visibilities are complex-valued with noise-dominated statistics:

```bash
python synthetic_data.py -o /tmp/visibilities.zarr \
    --shape 1000,2048,2048 --chunks 50,256,256 \
    --dims time,frequency,baseline --pattern radio --seed 42
```

The `radio` pattern generates visibility-amplitude-like data from complex Gaussian noise.

### Compression Testing

For isolating compression codec behavior, use the `constant` pattern (high redundancy) or `random` pattern (low compressibility):

```bash
# High compressibility — tests codec best-case
python synthetic_data.py -o /tmp/constant.zarr \
    --shape 500,512,512 --chunks 50,128,128 --pattern constant

# Low compressibility — tests codec worst-case
python synthetic_data.py -o /tmp/random.zarr \
    --shape 500,512,512 --chunks 50,128,128 --pattern random
```

## Validation

After generating synthetic data, verify the output matches expectations before running benchmarks.

### Verify with Python

```python
import zarr
import numpy as np

z = zarr.open("/tmp/test.zarr", mode="r")
print(f"Shape:       {z.shape}")
print(f"Chunks:      {z.chunks}")
print(f"Dtype:       {z.dtype}")
print(f"Dimensions:  {z.attrs.get('dimensions')}")
print(f"Pattern:     {z.attrs.get('pattern_type')}")

# Check data statistics
sample = z[0:10]
print(f"Sample mean: {np.mean(sample):.4f}")
print(f"Sample std:  {np.std(sample):.4f}")
print(f"Min/Max:     {np.min(sample):.4f} / {np.max(sample):.4f}")
```

### Verify on Disk

```bash
# Check directory structure
ls -la /tmp/test.zarr/

# Check total size
du -sh /tmp/test.zarr/
```

### Verify Reproducibility

Regenerate with the same seed and confirm identical output:

```python
z1 = zarr.open("/tmp/test_run1.zarr", mode="r")
z2 = zarr.open("/tmp/test_run2.zarr", mode="r")
assert np.array_equal(z1[:], z2[:]), "Data differs between runs"
```

## Common Mistakes

- **Mismatched dimensionality:** Providing a shape with 3 dimensions but chunks with 2 (or vice versa). The script will raise a `ValueError` but this is easily overlooked when constructing commands.
- **Unrealistically small datasets:** Generating a few megabytes of data when your production dataset is hundreds of gigabytes. Benchmarks on tiny data will be dominated by overhead, not I/O.
- **Unrealistically large datasets:** Generating terabytes of synthetic data when a few gigabytes would suffice. Use the `--target-size` flag with `--sample-from` to stay within resource limits.
- **Forgetting compression:** Running benchmarks with `--compression none` when your production data uses `zstd`. Compression changes both chunk sizes on disk and CPU cost during reads.
- **Ignoring the seed:** Omitting `--seed` or using different seeds across runs makes results non-reproducible. Always record the seed used.
- **Wrong dtype:** Using `float64` for benchmarks when production data is `float32`. This doubles memory and I/O, distorting benchmark results.
- **Partial chunks at boundaries:** Choosing chunk sizes that do not evenly divide the array shape creates smaller edge chunks with different performance characteristics.

## Best Practices

- **Match production shapes:** Use dimension sizes and aspect ratios representative of your actual data, even if the total volume is smaller.
- **Test multiple sizes:** Generate 2-3 datasets at different scales (e.g., 1 GB, 8 GB, 50 GB) to understand how performance scales with data volume.
- **Document parameters:** Record the exact command used to generate each test dataset. The script stores `pattern_type` and `created_by` in Zarr attributes, but also keep a log.
- **Use consistent seeds:** Default seed is 42. Keep it consistent across all runs in a benchmarking campaign for reproducibility.
- **Test with and without compression:** Generate identical datasets with `--compression zstd` and `--compression none` to isolate compression overhead.
- **Start local, then move to cloud:** Validate your benchmarking pipeline on local synthetic data before paying for cloud storage and egress.
- **Clean up:** Synthetic datasets can be large. Delete them after benchmarking to reclaim disk space.

## Resources

- **Zarr documentation:** https://zarr.readthedocs.io/
- **xarray Zarr backend:** https://docs.xarray.dev/en/stable/user-guide/io.html#zarr
- **Blosc compressors:** https://www.blosc.org/
- **Nguyen et al. (2023):** [DOI 10.1002/essoar.10511054.2](https://doi.org/10.1002/essoar.10511054.2) — chunk size impact on Zarr read performance
- **Chunking Strategy skill:** See the sibling `chunking-strategy` skill for running benchmarks on generated data

---
description: Generate a synthetic Zarr dataset for controlled chunking benchmarks with configurable dimensions and compression
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
---

# /generate-synthetic - Generate Synthetic Zarr Dataset

Generate a synthetic Zarr dataset with configurable dimensions, chunk sizes, dtype, and compression for use in controlled chunking benchmarks. Useful when real data is unavailable, too large, or when you need a reproducible baseline for testing.

## Usage

```bash
# Interactive — agent will ask for dimensions, shape, dtype
/generate-synthetic

# With config file
/generate-synthetic config.json

# With inline dimension spec
/generate-synthetic --shape 1000,2048,2048 --dims time,lat,lon

# With full specification
/generate-synthetic --shape 500,1024,1024 --dims time,y,x --dtype float32 --chunks 50,256,256 --compressor zstd --output /data/synthetic.zarr
```

## Arguments

`$ARGUMENTS` — Optional configuration file path (JSON) or inline dimension specification flags.

## Input Handling

### If a config JSON file is provided:

Load the JSON file and extract dataset parameters. Expected format:

```json
{
  "shape": [1000, 2048, 2048],
  "dims": ["time", "latitude", "longitude"],
  "dtype": "float32",
  "chunks": [50, 256, 256],
  "compressor": "zstd",
  "compressor_level": 3,
  "fill_pattern": "random",
  "seed": 42,
  "output_path": "./synthetic_benchmark.zarr"
}
```

### If no arguments are provided:

Ask the user for the following information:

1. **Dimension names** — e.g., `time, latitude, longitude`
2. **Shape** — size along each dimension, e.g., `1000, 2048, 2048`
3. **Dtype** — data type, default `float32`
4. **Initial chunk shape** — default: auto-calculated for ~5 MB chunks
5. **Compression** — codec and level, default `zstd level 3`
6. **Output location** — default: `./synthetic_benchmark.zarr`

## Information Gathering

Before generating the dataset, confirm or collect:

| Parameter | Default | Notes |
|-----------|---------|-------|
| Dimensions | (ask user) | Names for each axis |
| Shape | (ask user) | Size per dimension |
| Dtype | `float32` | Must match production data type for realistic benchmarks |
| Chunks | Auto (~5 MB) | Initial chunk shape; will be varied during benchmarking |
| Compressor | `zstd level 3` | Compression codec and level |
| Fill pattern | `random` | `random`, `zeros`, `gradient`, or `realistic` |
| Seed | `42` | Random seed for reproducibility |
| Output path | `./synthetic_benchmark.zarr` | Local path for the generated dataset |

## Action Steps

1. **Validate parameters**
   - Confirm shape has the same number of elements as dims
   - Confirm chunk shape divides evenly into dataset shape (or is smaller)
   - Estimate uncompressed size and warn if > 50 GB
   - Check output path does not already exist (or confirm overwrite)

2. **Run synthetic_data.py**
   - Locate the script at `skills/synthetic-data/scripts/synthetic_data.py`
   - Pass validated parameters
   - Monitor progress and report estimated completion time

3. **Verify output**
   - Open the generated Zarr store and confirm shape, dtype, chunks, and compression match
   - Report actual on-disk size (compressed)
   - Verify data is readable with `xarray.open_zarr()`

4. **Report results**
   - Display dataset summary table
   - Suggest next step: run `/benchmark` on the generated dataset

## Output Summary

After successful generation, display:

| Property | Value |
|----------|-------|
| Dataset path | `[OUTPUT_PATH]` |
| Shape | `[SHAPE]` |
| Dtype | `[DTYPE]` |
| Chunks | `[CHUNKS]` |
| Compression | `[COMPRESSOR]` |
| Uncompressed size | `[SIZE_GB]` GB |
| Compressed size | `[COMPRESSED_GB]` GB |
| Compression ratio | `[RATIO]`x |

## Important Notes

- **Start small:** For initial testing, use shapes that produce datasets under 1 GB. Scale up once the benchmark pipeline is validated.
- **Match production dtype:** Use the same dtype as your real data. Compression ratios and memory usage differ significantly between `float32` and `float64`.
- **Document the seed:** Always record the random seed so the exact same dataset can be regenerated. Default seed is `42`.
- **Fill pattern matters:** Random data compresses poorly (worst case for I/O benchmarks). Use `realistic` fill pattern if you want compression behavior closer to real scientific data.
- **Disk space:** Ensure sufficient disk space for both the generated dataset and any rechunked copies that will be created during benchmarking.

## When to Use

- No real dataset is available yet
- Real dataset is too large for iterative benchmark testing
- Need a reproducible baseline that does not depend on external data
- Testing the benchmark pipeline before running on production data

## When NOT to Use

- Real dataset is available and appropriately sized — benchmark directly on it
- Testing compression codec selection — compression behavior on synthetic data may not represent real data
- Evaluating write performance — this generates read-benchmark data only

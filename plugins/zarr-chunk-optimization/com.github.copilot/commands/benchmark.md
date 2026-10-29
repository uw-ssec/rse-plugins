---
description: Run comprehensive chunking benchmarks on Zarr dataset and generate performance report with recommendations
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# /benchmark - Comprehensive Chunking Benchmarking

Run complete benchmarking workflow: sample or generate data, test candidate chunk configurations, measure performance across access patterns, generate report with recommendations based on Nguyen et al. (2023) methodology.

## Usage

```bash
# Benchmark existing dataset
/benchmark s3://bucket/data.zarr

# Benchmark with specific access patterns
/benchmark /data/local.zarr --patterns spatial,time-series

# Benchmark with candidate configurations
/benchmark s3://bucket/data.zarr --configs "10,256,256" "50,512,512" "100,1024,1024"

# Benchmark with memory budget constraint
/benchmark /data/climate.zarr --memory-budget 8GB

# Generate synthetic data and benchmark
/benchmark --synthetic --shape 1000,2048,2048 --dims time,lat,lon
```

## What This Command Does

1. Reads dataset metadata or generates synthetic data
2. Asks about access patterns if not specified (use **access-pattern-profiler** skill if user is unsure)
3. Generates candidate chunk configurations varying one dimension at a time
4. Samples data to manageable size for benchmarking (or uses full synthetic dataset)
5. Invokes **chunking-strategy-benchmark** skill to execute benchmarks
6. Invokes **performance-reporter** skill to analyze results and generate markdown report
7. Saves report to `.agents/benchmark-report-[name]-[timestamp].md`
8. Presents summary with recommendation

## Skills Invoked

- **synthetic-data-generation** (if `--synthetic` flag used)
- **access-pattern-profiler** (if user unsure about access patterns)
- **chunking-strategy-benchmark** (always)
- **performance-reporter** (always)

## Inputs Accepted

**Required:** Either dataset path OR `--synthetic` flag

**Dataset path formats:**
- Local: `/data/mydata.zarr`
- S3: `s3://bucket/path/to/data.zarr`
- GCS: `gs://bucket/path/to/data.zarr`

**Access patterns:** User describes workflow; agent translates to spatial/time-series/spectral patterns

## Optional Arguments

`--patterns PATTERNS` — Comma-separated list (spatial, time-series, spectral, all). Default: all

`--configs CONFIGS` — Space-separated chunk shapes in format "t,f,b". Auto-generated if not provided.

`--memory-budget SIZE` — Maximum acceptable peak memory (e.g., "8GB"). Flags configs exceeding limit.

`--runs N` — Runs per configuration per pattern. Minimum 5, default 10.

`--synthetic` — Generate synthetic test data (requires `--shape` and `--dims`)

`--shape SHAPE` — Shape for synthetic data (comma-separated integers)

`--dims DIMS` — Dimension names for synthetic data (comma-separated strings)

`--sample-size SIZE` — Elements to sample from first dimension for very large datasets

## Constraints

- Minimum 5 runs per configuration for statistical validity (enforced by benchmark script)
- Must clear OS cache between runs (macOS: `purge`, Linux: `drop_caches`)
- Always measure both wall-clock time AND peak memory
- Report must include mean, std, min, max for all metrics
- Calculate performance bias (max_time/min_time across patterns) for all configs
- Benchmark on sample data first, never directly on full production dataset
- Save all reports to `.agents/` directory with timestamp

## What User Gets

- Markdown report with results tables for each access pattern
- Performance bias analysis showing balanced vs specialized strategies
- Memory analysis with peak usage per configuration
- Recommendation with reasoning based on Nguyen et al. findings
- Trade-off explanations when patterns conflict
- Next steps: review full report, use `/tradeoffs` to explore, use `/rechunk` to apply

## When to Use

- Starting new project with multi-dimensional Zarr data
- Migrating existing data to cloud storage
- Access patterns are slow and chunking might be suboptimal
- Choosing between multiple chunking strategies
- Understanding trade-offs before rechunking large dataset

## When NOT to Use

- Format conversion (use ingestion tools)
- Compression codec selection (use zarr-xarray-integration plugin)
- Write-path optimization (this benchmarks reads only)

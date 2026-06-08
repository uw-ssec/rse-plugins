---
name: chunking-strategy
description: Benchmarks and optimizes Zarr chunking strategies for multi-dimensional scientific datasets, measuring wall-clock time, peak memory, and I/O metrics across spatial, time-series, and spectral access patterns following Nguyen et al. (2023) methodology. Use when the user asks about Zarr chunk sizing, storage layout optimization, benchmarking array access patterns, or choosing chunk configurations for scientific data on S3, GCS, or local storage.
metadata:
  references:
    - references/access-patterns.md
    - references/memory-constraints.md
    - references/nguyen-2023.md
    - references/benchmarking-methodology.md
    - references/cloud-storage-patterns.md
    - references/performance-interpretation.md
  scripts:
    - scripts/benchmark_runner.py
  assets:
    - assets/benchmark-config-example.json
    - assets/report-template.md
---

# Chunking Strategy Benchmarking

Benchmark Zarr chunk configurations against real access patterns before committing to a rechunking operation. Based on Nguyen et al. (2023) ([DOI: 10.1002/essoar.10511054.2](https://doi.org/10.1002/essoar.10511054.2)).

## Required Inputs

| Input | Example |
|-------|---------|
| Dataset path | `s3://bucket/data.zarr` or `/data/local.zarr` |
| Dimension names | `['time', 'lat', 'lon']` |
| Current chunk shape | `(1, 721, 1440)` (from `ds.chunks`) |
| Access pattern priorities | `spatial`, `temporal`, `spectral`, or `mixed` |
| Memory budget (optional) | `8 GB` — filters configs exceeding RAM |
| Number of runs (optional) | `5` minimum; increase for high-variance networks |

## Benchmarking Workflow

1. **Collect inputs** — gather dataset path, dimension names, current chunks, and access pattern weights.
2. **Generate candidate configurations** — vary one dimension at a time across the dominant access dimension; add user-specified shapes.
3. **Validate memory budget** — for each candidate, estimate chunk size × chunks-per-read. Discard any configuration that exceeds the memory budget before running a single benchmark.
4. **Clear caches and run benchmarks** — clear OS and fsspec caches before every run; execute 5+ repetitions per configuration per access pattern.
5. **Validate statistical stability** — if std/mean > 0.3 for any metric, increase run count or investigate variance source before interpreting results.
6. **Generate report** — compute Performance Bias scores, select 1-3 recommendations, fill `assets/report-template.md`.

**Validation gate after step 3:** No candidate exceeds the memory budget. If all candidates exceed budget, reduce spatial dimensions or sample a smaller time slice.

**Validation gate after step 5:** std/mean ≤ 0.3 for all reported metrics. If a metric fails, take recovery action (see Feedback Loops below).

## Running the Benchmark Script

```bash
# Single configuration, all default access patterns
python scripts/benchmark_runner.py \
  --dataset s3://bucket/data.zarr \
  --configs "50,512,512" \
  --runs 5

# Multiple configurations, explicit access pattern dimensions
python scripts/benchmark_runner.py \
  --dataset /local/era5.zarr \
  --configs "1,721,1440" "50,256,256" "100,128,128" \
  --slice-dims 0 \
  --traverse-dims 1 2 \
  --runs 10

# Output: JSON results file + prints mean±std for each metric per config
```

See `scripts/benchmark_runner.py` docstring for full argument reference.

## Cache Clearing (Critical)

Clear caches between every run to measure cold-cache performance.

**macOS:** `sudo purge`

**Linux:** `sync && sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'`

**fsspec (all platforms):**
```python
fsspec.config.conf['cache_storage'] = None  # disable between runs
```

## Measurement Code

**Timing** — use `time.perf_counter()`, not `time.time()`:
```python
start = time.perf_counter()
result = ds.sel(time=42).compute()
wall_time = time.perf_counter() - start
```

**Peak memory** — always report peak, not mean:
```python
import tracemalloc
tracemalloc.start()
result = ds.sel(time=42).compute()
_, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
```

Report **mean ± std** and **[min, max]** across all runs. Minimum 5 runs per configuration per access pattern.

## Performance Bias Score

Performance Bias (PB) = max(pattern times) / min(pattern times) for a given configuration.

- **PB ≈ 1.0–1.5** — balanced; suitable for mixed workloads.
- **PB > 2.0** — specialized; good for a single dominant pattern but penalizes others.
- **PB > 5.0** — highly specialized; only acceptable when one pattern represents ≥ 90% of access.

## Feedback Loops

| Situation | Recovery Action |
|-----------|----------------|
| std/mean > 0.3 | Increase runs to 10+; check for background network I/O; test at a different time |
| Configuration OOM mid-run | Remove it from the candidate set; reduce spatial dimensions by 2× |
| All candidates show similar performance | Widen the search grid (double or halve one dimension); check if data is already cached |
| Results inconclusive (PB ≈ 1.0 for all) | Current chunk shape may already be near-optimal; validate with real workload profiling |
| Cloud read times dominate | See [cloud-storage-patterns.md](references/cloud-storage-patterns.md) for request batching and prefetch tuning |

## Progressive Disclosure References

| Reference | Load When |
|-----------|----------|
| [access-patterns.md](references/access-patterns.md) | User needs to define or understand access pattern types |
| [memory-constraints.md](references/memory-constraints.md) | Memory budget filtering or all-or-nothing constraint questions |
| [benchmarking-methodology.md](references/benchmarking-methodology.md) | Statistical validity, reproducibility, pitfall avoidance |
| [cloud-storage-patterns.md](references/cloud-storage-patterns.md) | S3/GCS-specific latency, caching, or cost optimization |
| [performance-interpretation.md](references/performance-interpretation.md) | Reading results tables, PB scores, translating to recommendations |
| [nguyen-2023.md](references/nguyen-2023.md) | Methodology justification or research basis questions |

## Limitations

- Read performance only — does not benchmark write or rechunk operations.
- Sample-based — full dataset performance may differ slightly from sampled benchmarks.
- No compression benchmarking — assumes codec is already chosen.

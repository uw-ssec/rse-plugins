# Memory Constraints in Zarr Chunking — Deep Reference

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| The All-or-Nothing Constraint | 16–43 | Why reading any value requires loading the entire chunk |
| Why Peak Memory is a First-Class Metric | 44–57 | Comparing strategies with similar I/O but different memory footprints |
| How to Interpret Memory Measurements | 58–87 | Peak vs mean memory, overhead factors, and memory budgets |
| Measuring Peak Memory | 88–126 | Practical methods using tracemalloc, memory_profiler, and Dask |
| Common Memory Issues | 127–154 | Diagnosing OOM kills, swapping, and inconsistent measurements |
| Recommendations for This Plugin | 155–173 | Reporting both wall-clock time and peak memory in benchmarks |

---

## The All-or-Nothing Constraint

Zarr's chunking model imposes a fundamental constraint: **you cannot read part of a chunk**. To access any single value within a chunk, the entire chunk must be:

1. **Fetched** from storage (local disk or S3)
2. **Loaded** into RAM
3. **Decompressed** (if compression is enabled)

This is called the **all-or-nothing constraint**.

### Example

Consider a Zarr array with chunk shape `(100, 1000, 1000)` and dtype `float32`:

- Chunk size in bytes: `100 × 1000 × 1000 × 4 = 400,000,000 bytes = ~381 MB`

If your analysis code runs:
```python
ds.isel(time=50, frequency=500, baseline=500).compute()
```

Even though you're only accessing **one scalar value**, Zarr must:
- Load the entire 381 MB chunk containing that value
- Decompress the entire chunk (if compressed)
- Hold it in memory long enough to extract the single value

**Implication:** Peak memory usage is determined by the **size of the largest chunk accessed**, not the amount of data you actually need.

## Why Peak Memory is a First-Class Metric

When benchmarking chunking strategies, wall-clock time is not sufficient. Two chunking strategies might have similar I/O times but vastly different memory footprints:

| Config | Chunk Shape | Wall Time | Peak Memory | Usable on 8 GB System? |
|--------|-------------|-----------|-------------|------------------------|
| A      | (10, 100, 100) | 12.3 s | 400 MB | ✅ Yes |
| B      | (100, 1000, 1000) | 10.1 s | 3.8 GB | ⚠️  Tight |
| C      | (500, 2000, 2000) | 8.7 s | 15.3 GB | ❌ No (OOM) |

**Config C** has the fastest wall time but is **unusable** on systems with limited RAM. It will trigger out-of-memory (OOM) errors or excessive swapping, making real-world performance far worse than the benchmark suggests.

**Config A** is slower but fits comfortably in memory, making it more practical for most users.

## How to Interpret Memory Measurements

### 1. Peak Memory vs Mean Memory

- **Peak memory** is the maximum RAM usage at any point during the operation
- **Mean memory** is the average RAM usage over time

**Always report peak memory** in benchmarking. Mean memory can be misleading—a brief spike that causes OOM will crash the program regardless of the mean.

### 2. Memory Overhead

Python and xarray add overhead beyond the raw chunk size:

- Python object overhead (~100-200 bytes per object)
- NumPy array metadata
- Dask task graph metadata (if using Dask)
- Compression codecs (temporary decompression buffers)

**Rule of thumb:** Expect actual peak memory to be **1.5-2× the uncompressed chunk size** due to overhead.

### 3. Memory Budget

When recommending chunking strategies, consider the user's typical analysis environment:

- **Interactive analysis (Jupyter notebook):** Often runs on personal laptops (8-16 GB RAM)
- **HPC compute node:** May have 64-512 GB RAM
- **Cloud VM (t2.medium):** 4 GB RAM

A chunking strategy optimized for HPC may be unusable for interactive analysis.

## Measuring Peak Memory

### Using `tracemalloc` (Python standard library)
```python
import tracemalloc

tracemalloc.start()

# Run benchmark operation
result = ds.sel(time=42).compute()

current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

print(f"Peak memory: {peak / 1024**2:.1f} MB")
```

### Using `memory_profiler` (more accurate)
```python
from memory_profiler import memory_usage

def benchmark_operation():
    result = ds.sel(time=42).compute()
    return result

mem_usage = memory_usage(benchmark_operation, interval=0.1, max_usage=True)
print(f"Peak memory: {mem_usage:.1f} MB")
```

### Using Dask diagnostics
```python
from dask.distributed import performance_report

with performance_report(filename="dask-report.html"):
    result = ds.sel(time=42).compute()

# Open dask-report.html to see memory usage over time
```

## Common Memory Issues

### Issue 1: "Killed" with No Error Message

**Symptom:** Program terminates abruptly with no Python exception.

**Cause:** Linux OOM killer terminated the process due to excessive memory usage.

**Solution:** Reduce chunk size or use a machine with more RAM.

### Issue 2: System Becomes Unresponsive

**Symptom:** Program continues running but system swaps heavily, making everything slow.

**Cause:** Peak memory exceeds physical RAM, forcing the OS to swap to disk.

**Solution:** Reduce chunk size to fit in RAM.

### Issue 3: Inconsistent Memory Measurements

**Symptom:** Peak memory varies widely between runs (e.g., 2 GB, 4 GB, 3 GB, 6 GB).

**Cause:** OS page cache or Python garbage collection timing.

**Solution:**
- Clear OS cache between runs (`purge` on macOS, `drop_caches` on Linux)
- Force garbage collection before measurement: `gc.collect()`

## Recommendations for This Plugin

When generating benchmark reports, **always include both metrics**:

1. **Wall-clock time** (efficiency metric)
2. **Peak memory** (feasibility metric)

Present them together in the summary table. Flag configurations where peak memory exceeds common system limits (e.g., 8 GB, 16 GB) with warnings.

Example report format:
```markdown
| Config | Chunk Shape | Wall Time | Peak Memory | 8GB OK? | 16GB OK? |
|--------|-------------|-----------|-------------|---------|----------|
| A      | (10, 100, 100) | 12.3 s ± 0.8 s | 0.4 GB | ✅ | ✅ |
| B      | (100, 500, 500) | 8.1 s ± 0.5 s | 3.8 GB | ✅ | ✅ |
| C      | (100, 1000, 1000) | 6.7 s ± 0.3 s | 12.2 GB | ❌ | ✅ |
```

This makes it immediately clear which configurations are practical for different environments.

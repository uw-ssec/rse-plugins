# Benchmarking Methodology for Zarr Chunking

Best practices for running **reproducible, statistically valid** chunking benchmarks. Following this methodology ensures benchmark results are reliable and actionable.

## Core Principles

### 1. Minimum 5 Runs Per Configuration

**Never report single-run results.** I/O performance is inherently variable due to:

- Network jitter (for cloud storage)
- CPU scheduler behavior
- Background processes
- OS page cache state

**Minimum recommended:** 5 runs per configuration

**Better:** 10 runs

**Report:** Mean, standard deviation, min, and max across all runs

Example:
```
Spatial access (100, 512, 512): 8.3 s ± 0.7 s [min: 7.4 s, max: 9.6 s]
```

### 2. Clear Caching Between Runs

Caching can mask real I/O performance, leading to artificially fast subsequent runs.

#### OS Page Cache

**macOS:**
```bash
sudo purge
```

**Linux:**
```bash
sync
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'
```

**When to clear:** Between every benchmark run to ensure cold-cache performance.

#### fsspec Cache

Python's `fsspec` library (used by xarray for remote data access) maintains its own cache.

**Disable fsspec caching:**
```python
import fsspec

# Option 1: Disable caching entirely
ds = xr.open_zarr(
    fsspec.get_mapper("s3://bucket/data.zarr",
                      client_kwargs={'config': Config(signature_version=UNSIGNED)},
                      cache_storage=None)  # Disable cache
)

# Option 2: Clear cache between runs
fsspec.config.conf['cache_storage'] = '/tmp/fsspec_cache'
# Then manually delete /tmp/fsspec_cache between runs
```

**When to clear:** Between runs, or disable entirely for benchmarking.

### 3. Vary One Parameter at a Time

To understand the impact of each dimension, **vary only one chunk dimension per test**:

**Good experimental design:**
```
Base: (50, 256, 256)
Test time:   (10, 256, 256), (50, 256, 256), (100, 256, 256), (200, 256, 256)
Test freq:   (50, 64, 256), (50, 128, 256), (50, 256, 256), (50, 512, 256)
Test base:   (50, 256, 64), (50, 256, 128), (50, 256, 256), (50, 256, 512)
```

**Bad experimental design:**
```
(10, 64, 64), (50, 128, 128), (100, 256, 256), (200, 512, 512)
```
**Why bad?** Cannot isolate which dimension caused performance changes.

### 4. Controlled Environment

**Critical environmental factors:**

- **Network conditions:** For cloud storage (S3), use a consistent network connection. Avoid running benchmarks during known high-traffic periods.
- **CPU availability:** Disable background jobs. For HPC systems, request dedicated nodes.
- **I/O load:** Don't run benchmarks while other processes are heavily reading/writing.

**Record environmental context:**
```python
import platform
import psutil

env_info = {
    'python_version': platform.python_version(),
    'os': platform.system(),
    'os_version': platform.release(),
    'cpu_count': psutil.cpu_count(logical=False),
    'total_ram_gb': psutil.virtual_memory().total / 1024**3,
    'network_type': 'AWS us-east-1 to S3 (same region)',  # Example
    'instance_type': 't2.xlarge'  # If running on cloud
}
```

### 5. Representative Data Samples

**Problem:** Benchmarking the entire dataset may be too slow during testing.

**Solution:** Use representative samples, but ensure they're large enough to reflect real performance:

- **Too small:** Single chunk reads dominate, doesn't reflect multi-chunk access patterns
- **Too large:** Benchmarking takes too long, iteration is impractical

**Recommendation:** Sample size should require accessing **at least 10-20 chunks** for each access pattern.

**Example:**
```python
# If chunk shape is (50, 256, 256) and data shape is (10000, 2048, 2048)
# Sample: 500 time steps (10 chunks), full spatial extent
sample_ds = full_ds.isel(time=slice(0, 500))
```

### 6. Timing Methodology

**Use `time.perf_counter()`**, not `time.time()`:

```python
import time

start = time.perf_counter()
result = ds.sel(time=42).compute()
end = time.perf_counter()

wall_time = end - start
```

**Why not `time.time()`?** System clock can jump backward due to NTP adjustments.

**Include compute() call:** Ensure Dask actually executes. Without `.compute()`, xarray returns lazy objects.

### 7. Warm-Up Runs

**Problem:** First run may include Python import overhead, JIT compilation, etc.

**Solution:** Run 1-2 warm-up iterations before starting timed runs.

```python
# Warm-up (not timed)
_ = ds.sel(time=0).compute()
gc.collect()

# Timed runs
times = []
for i in range(5):
    clear_cache()  # OS and fsspec
    start = time.perf_counter()
    result = ds.sel(time=i).compute()
    end = time.perf_counter()
    times.append(end - start)
```

## Common Pitfalls to Avoid

### Pitfall 1: Not Clearing OS Cache

**Symptom:** First run is slow (10 s), subsequent runs are fast (0.5 s).

**Cause:** OS page cache is serving data from RAM instead of reading from S3.

**Fix:** Clear cache between every run (see section 2).

### Pitfall 2: Testing on Unrealistically Small Data

**Symptom:** All chunking strategies perform similarly in benchmarks, but differ greatly in production.

**Cause:** Test data is too small (e.g., single chunk). Performance differences only emerge with multi-chunk access.

**Fix:** Use samples large enough to access 10+ chunks per operation.

### Pitfall 3: Forgetting `.compute()`

**Symptom:** Operations complete in microseconds.

**Cause:** xarray returned a lazy Dask object without executing. Timing only measured graph construction, not actual I/O.

**Fix:** Always call `.compute()` inside the timed block.

### Pitfall 4: Network Variability on Shared Instances

**Symptom:** Huge variance in run times (e.g., 5 s, 12 s, 6 s, 15 s).

**Cause:** Cloud VM is sharing network bandwidth with other tenants.

**Fix:** Use dedicated instances, or increase run count to average out variability (e.g., 20 runs instead of 5).

### Pitfall 5: Mixing Rechunking with Access Benchmarks

**Symptom:** Benchmark times include rechunking overhead, masking access performance.

**Cause:** Rechunking the sample data **inside** the benchmark loop.

**Fix:** Rechunk **once** before benchmarking, then run access pattern benchmarks on the pre-rechunked data.

```python
# Correct approach
for config in chunk_configs:
    # Rechunk sample (not timed)
    rechunked = sample_ds.chunk(config)
    rechunked.to_zarr(f"temp_rechunked_{config}.zarr")

    # Benchmark access patterns (timed)
    test_ds = xr.open_zarr(f"temp_rechunked_{config}.zarr")
    for run in range(5):
        # ... timed access operations ...
```

### Pitfall 6: Not Recording Configuration Details

**Symptom:** Cannot reproduce results later.

**Cause:** Missing metadata about Python versions, library versions, instance type, etc.

**Fix:** Record full environment at the start of each benchmark session:

```python
benchmark_metadata = {
    'date': '2024-03-08',
    'python': '3.11.7',
    'xarray': '2024.1.0',
    'zarr': '2.17.0',
    'dask': '2024.1.0',
    'fsspec': '2024.1.0',
    'instance_type': 't2.xlarge',
    'storage_backend': 'AWS S3 us-east-1',
    'data_shape': (10000, 2048, 2048),
    'data_dtype': 'float32',
    'compression': 'zstd level 3'
}
```

Save this metadata with the benchmark results.

## Recommended Workflow

1. **Define access patterns** matching real user workflows
2. **Generate candidate chunking configurations** (vary one dimension at a time)
3. **Prepare sample data** (large enough to access 10+ chunks per operation)
4. **Rechunk sample data** to each candidate configuration
5. **Run warm-up iterations** (1-2 runs, not timed)
6. **For each configuration:**
   - For each access pattern:
     - For each run (minimum 5):
       - Clear OS cache
       - Clear fsspec cache (if applicable)
       - Time the operation with `time.perf_counter()`
       - Measure peak memory with `tracemalloc` or `memory_profiler`
       - Record metrics
7. **Aggregate results:** Compute mean, std, min, max for each config × pattern
8. **Generate report** with all metrics and recommendations

## Output Format

Report results in structured markdown tables:

```markdown
## Spatial Access Pattern (load full frequency×baseline at single time)

| Chunk Shape | Wall Time (mean ± std) | Min | Max | Peak Memory | HTTP Requests |
|-------------|------------------------|-----|-----|-------------|---------------|
| (10, 512, 512) | 8.3 s ± 0.7 s | 7.4 s | 9.6 s | 1.2 GB | 142 |
| (50, 512, 512) | 9.1 s ± 0.9 s | 8.0 s | 10.8 s | 6.3 GB | 28 |
| (100, 512, 512) | 10.2 s ± 1.1 s | 8.9 s | 12.1 s | 12.5 GB | 14 |
```

Include similar tables for each access pattern, followed by a **Recommendations** section explaining which configuration(s) to use based on the user's priorities.

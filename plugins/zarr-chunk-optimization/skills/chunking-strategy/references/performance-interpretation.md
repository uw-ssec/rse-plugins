# Performance Interpretation — Deep Reference

| Section | Lines | Description |
|---------|-------|-------------|
| Understanding Benchmark Metrics | 14-89 | Wall-clock time, TTFB, peak memory, throughput, chunk utilization |
| Performance Bias Metric | 91-154 | Formula, ranges, and interpretation from Nguyen et al. |
| Reading Benchmark Reports | 156-202 | How to compare configurations, identifying winners |
| Common Performance Patterns | 204-251 | Spatial-optimized, temporal-optimized, balanced configurations |
| When Results Are Inconclusive | 253-313 | Noise, insufficient runs, environmental factors |
| Translating Results to Recommendations | 315-381 | Choosing between configs, priority weighting |

---

## Understanding Benchmark Metrics

Benchmark reports produced by this skill contain several metrics. Each measures a different aspect of read performance and matters for different use cases.

### Wall-Clock Time

**Definition**: Total elapsed time from the start of a read operation to completion, measured with `time.perf_counter()`.

**What it captures**: Everything — network latency, data transfer, decompression, memory allocation, and any framework overhead (xarray, Dask).

**When it matters**: Always. This is the primary metric for comparing chunk configurations. Users experience wall-clock time directly.

**Interpretation**:
- Lower is better
- Report as `mean +/- std` across all runs
- Compare relative differences: a 20% reduction in wall-clock time is meaningful; a 2% reduction may be noise

### Time to First Byte (TTFB)

**Definition**: Time from issuing the first read request to receiving the first byte of chunk data.

**What it captures**: Network latency, request routing, and storage backend processing time. Does not include data transfer or decompression.

**When it matters**: For interactive workloads where perceived responsiveness matters (e.g., visualization tools that need to show partial data quickly).

**Interpretation**:
- Dominated by per-request overhead on cloud storage (~20-100 ms)
- Largely independent of chunk size
- High variance indicates network instability

### Peak Memory

**Definition**: Maximum memory allocated during the read operation, measured with `tracemalloc` or `memory_profiler`.

**What it captures**: The worst-case memory footprint including decompressed chunk buffers, intermediate arrays, and framework overhead.

**When it matters**: When operating under memory constraints (laptops, shared HPC nodes, containers with memory limits). A configuration that exceeds available memory will cause swapping or OOM errors.

**Interpretation**:
- Must be below the specified memory budget
- Scales roughly with `product(chunk_shape) * dtype.itemsize * number_of_concurrent_chunks`
- Dask can spill to disk, making peak memory less of a hard constraint but introducing performance penalties

### Throughput

**Definition**: Data volume processed per unit time, typically reported in MB/s or GB/s.

**What it captures**: The effective data processing rate, accounting for all overhead.

**Calculation**:
```
throughput = total_bytes_read / wall_clock_time
```

**When it matters**: For bulk processing workloads where you need to process the entire dataset. Higher throughput means faster batch jobs.

**Interpretation**:
- Higher is better
- Compare against theoretical maximum (network bandwidth, disk bandwidth)
- If throughput is far below theoretical max, overhead is the bottleneck

### Chunk Utilization

**Definition**: The fraction of data in each loaded chunk that is actually used by the access pattern.

**Calculation**:
```
utilization = bytes_needed / bytes_loaded
```

**When it matters**: Indicates wasted I/O. Low utilization means the chunk shape is misaligned with the access pattern — the system reads much more data than needed.

**Interpretation**:
- 1.0 (100%) is ideal — every byte loaded is used
- Below 0.5 indicates poor alignment; consider reshaping chunks
- Example: Loading a single time step from chunks of shape `(100, 512, 512)` gives utilization of `1/100 = 0.01` for the time dimension

## Performance Bias Metric

The Performance Bias metric, introduced by Nguyen et al. (2023), quantifies how evenly a chunk configuration performs across different access patterns. It helps identify whether a configuration is a specialist (fast for one pattern, slow for others) or a generalist (reasonably fast for all patterns).

### Formula

```
Performance Bias (PB) = max(T_patterns) / min(T_patterns)
```

Where `T_patterns` is the set of mean wall-clock times for each access pattern tested with a given chunk configuration.

### Detailed Calculation

For a chunk configuration tested against three access patterns:

```
T_spatial  = mean wall-clock time for spatial access
T_temporal = mean wall-clock time for temporal access
T_spectral = mean wall-clock time for spectral/band access

PB = max(T_spatial, T_temporal, T_spectral) / min(T_spatial, T_temporal, T_spectral)
```

### Interpretation Ranges

| PB Value | Interpretation | Use Case Fit |
|----------|---------------|--------------|
| 1.0 | Perfectly balanced | Ideal for mixed workloads |
| 1.0 - 1.5 | Well-balanced | Good for mixed workloads |
| 1.5 - 3.0 | Moderately biased | Acceptable if primary pattern is known |
| 3.0 - 10.0 | Highly biased | Only suitable for single-pattern workloads |
| > 10.0 | Extremely biased | Strongly optimized for one pattern at expense of others |

### Example

Given these benchmark results for a chunk shape `(10, 1024, 1024)`:

```
Spatial access:  6.1 s (fastest)
Temporal access: 18.4 s (slowest)
Spectral access: 12.7 s

PB = 18.4 / 6.1 = 3.02
```

This configuration is highly biased toward spatial access. It would be a poor choice for workloads that mix spatial and temporal queries.

### Comparing Configurations by PB

When choosing between configurations:

1. **If access pattern is known**: Choose the configuration with the best performance for that specific pattern, regardless of PB.
2. **If workload is mixed**: Prefer configurations with PB < 1.5, then compare their worst-case performance.
3. **If workload is unknown**: Choose the lowest PB configuration that meets memory constraints.

### Limitations of PB

- PB does not account for how frequently each access pattern is used. A weighted version may be more appropriate:
  ```
  Weighted PB = max(w_i * T_i) / min(w_i * T_i)
  ```
  where `w_i` is the relative frequency of pattern `i`.
- PB treats all patterns equally. In practice, a 2x slowdown on a rarely-used pattern may be acceptable.

## Reading Benchmark Reports

The benchmark report presents results in structured tables. Here is how to interpret them effectively.

### Configuration Comparison Table

The summary table ranks configurations by a primary metric (usually wall-clock time for the priority access pattern):

```
| Config | Spatial (s) | Temporal (s) | Spectral (s) | PB   | Peak Mem (GB) |
|--------|-------------|--------------|--------------|------|---------------|
| A      | 6.1 +/- 0.5| 18.4 +/- 1.2 | 12.7 +/- 0.8| 3.02 | 10.2          |
| B      | 8.3 +/- 0.7| 11.2 +/- 0.9 | 10.1 +/- 0.6| 1.35 | 3.8           |
| C      | 15.1 +/- 1.0| 5.8 +/- 0.4 | 9.3 +/- 0.5 | 2.60 | 5.1           |
```

### Identifying the Winner

There is rarely a single "best" configuration. Follow this decision process:

1. **Eliminate infeasible configs**: Remove any configuration whose peak memory exceeds the budget.
2. **Check the primary access pattern**: If the user specified a priority pattern, rank by that column.
3. **Check PB for mixed workloads**: If no single pattern dominates, prefer lower PB.
4. **Consider secondary metrics**: Between two similar configs, prefer lower memory usage.

### Statistical Significance

Two configurations are meaningfully different only if their confidence intervals do not overlap substantially:

- Config A: `6.1 +/- 0.5 s` (range: 5.6 - 6.6)
- Config B: `6.8 +/- 0.6 s` (range: 6.2 - 7.4)

These ranges overlap (6.2 - 6.6), so the difference may not be significant. Increase run count or use a statistical test (e.g., Mann-Whitney U) to confirm.

### Per-Pattern Detail Tables

Each access pattern has its own detailed table showing all runs:

```
| Run | Wall Time (s) | Peak Mem (GB) | Chunks Read | Utilization |
|-----|---------------|---------------|-------------|-------------|
| 1   | 6.3           | 10.1          | 16          | 0.95        |
| 2   | 5.8           | 10.2          | 16          | 0.95        |
| ...                                                              |
```

Check for **outliers** (runs with times 2x+ the mean) which may indicate interference from other processes or network issues.

## Common Performance Patterns

Certain chunk shape categories produce predictable performance profiles. Recognizing these patterns helps validate benchmark results.

### Spatial-Optimized Configuration

**Chunk shape**: Large spatial dimensions, small time dimension.
Example: `(1, 2048, 2048)` for a `(time, y, x)` dataset.

**Expected performance**:
- Spatial access: Fast (each chunk contains a large spatial region; few chunks needed)
- Temporal access: Slow (reading a time series requires loading many chunks, each contributing one time step)
- PB: High (typically 3-10+)

**Memory profile**: High peak memory per chunk but few chunks loaded concurrently.

### Temporal-Optimized Configuration

**Chunk shape**: Large time dimension, small spatial dimensions.
Example: `(1000, 64, 64)` for a `(time, y, x)` dataset.

**Expected performance**:
- Spatial access: Slow (a spatial slice requires many small chunks)
- Temporal access: Fast (each chunk contains a long time series for a spatial point)
- PB: High (inverse of spatial-optimized)

**Memory profile**: Moderate memory per chunk; many chunks needed for spatial access.

### Balanced Configuration

**Chunk shape**: Moderate size in all dimensions.
Example: `(50, 512, 512)` for a `(time, y, x)` dataset.

**Expected performance**:
- Spatial access: Moderate (more chunks than spatial-optimized, but each is reasonably sized)
- Temporal access: Moderate (more data per chunk than temporal-optimized per time step)
- PB: Low (typically 1.0-2.0)

**Memory profile**: Moderate and predictable.

### When Patterns Break

Unexpected results may indicate:

- **Compression effects**: Highly compressible data may make larger chunks faster than expected (fewer objects after compression)
- **Dask scheduling overhead**: Very many small chunks can overwhelm the Dask scheduler
- **Network contention**: Cloud benchmarks may show irregular patterns due to shared infrastructure
- **Cache contamination**: If caches were not properly cleared, repeated reads may appear artificially fast

## When Results Are Inconclusive

Sometimes benchmark results do not clearly favor one configuration. Recognize and address these situations.

### High Variance (Noise)

**Symptom**: Standard deviation exceeds 30% of the mean for one or more configurations.

**Causes**:
- Network variability (cloud storage)
- Background processes competing for resources
- OS-level caching not properly cleared
- Garbage collection pauses

**Remedies**:
- Increase run count to 15-20
- Pin the benchmark process to specific CPU cores
- Run during off-peak hours
- Use a dedicated instance (no shared workloads)

### Insufficient Runs

**Symptom**: Confidence intervals overlap for most configurations, making rankings unreliable.

**Remedy**: Increase `num_runs`. Use power analysis to estimate needed sample size:

```python
# Rough estimate: to detect a 10% difference with 95% confidence
# and observed CV (coefficient of variation) of 0.15:
import math
cv = 0.15  # std / mean
effect_size = 0.10  # 10% difference to detect
z_alpha = 1.96  # 95% confidence
z_beta = 0.84   # 80% power
n = (2 * (cv / effect_size)**2 * (z_alpha + z_beta)**2)
print(f"Runs needed: {math.ceil(n)}")  # ~36
```

### Environmental Factors

**Symptom**: Results differ substantially between benchmark sessions (different days, different instances).

**Causes**:
- Different instance types or generations
- Different network conditions
- Software version differences
- Different data regions or endpoints

**Remedies**:
- Always record environment metadata (instance type, region, software versions)
- Run all configurations in the same session
- Use relative comparisons (ratios) rather than absolute timings across sessions

### Tied Configurations

**Symptom**: Two or more configurations have statistically indistinguishable performance on the primary metric.

**Resolution**:
1. Break the tie using secondary metrics (memory usage, PB score)
2. Prefer the configuration with smaller chunks (more flexibility for future access patterns)
3. Prefer the configuration closer to common community conventions

## Translating Results to Recommendations

The final step is converting benchmark data into actionable recommendations for the user.

### Decision Framework

Apply this priority order when selecting a recommended configuration:

1. **Memory feasibility**: Must fit within the stated memory budget. Eliminate all configurations that exceed it.
2. **Primary pattern performance**: If the user has a clear primary access pattern, optimize for it.
3. **Performance bias**: For mixed workloads, prefer PB < 1.5.
4. **Secondary pattern performance**: Among candidates, prefer better worst-case performance.
5. **Practical considerations**: Prefer chunk sizes that align with common tooling defaults.

### Priority Weighting

When the user specifies access pattern priorities, apply weights:

```python
# Example: 60% spatial, 30% temporal, 10% spectral
weights = {'spatial': 0.6, 'temporal': 0.3, 'spectral': 0.1}

weighted_score = sum(
    weights[pattern] * mean_time[config][pattern]
    for pattern in weights
)
```

Rank configurations by `weighted_score` (lower is better). This accounts for the fact that a 2x slowdown on a rarely-used pattern matters less than a 10% slowdown on the primary pattern.

### Recommendation Structure

Always structure recommendations as:

1. **Primary recommendation**: Best overall configuration with reasoning
2. **Alternative for specific use case**: If a specialist configuration is dramatically better for one pattern
3. **What to avoid**: Configurations that are dominated (worse on all metrics) by others

### Example Recommendation

```
## Recommendation

**For your mixed spatial + temporal workload (70%/30% split):**

Use chunk shape (50, 512, 512):
- Weighted score: 9.2 s (best among feasible configs)
- Spatial access: 8.3 s +/- 0.7 s
- Temporal access: 11.2 s +/- 0.9 s
- PB: 1.35 (well-balanced)
- Peak memory: 3.8 GB (within 8 GB budget)

**If spatial access is the only concern:**

Consider (10, 1024, 1024):
- Spatial access: 6.1 s +/- 0.5 s (26% faster for spatial)
- But temporal access degrades to 18.4 s (64% slower)
- Peak memory: 10.2 GB (exceeds 8 GB laptop budget)
```

### When Not to Rechunk

Sometimes the benchmark shows the current chunking is already near-optimal. Recommend keeping the current configuration when:

- The best alternative improves performance by less than 10%
- Rechunking cost (time + storage) exceeds the cumulative benefit
- The dataset is rarely accessed (rechunking overhead is not amortized)

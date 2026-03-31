---
name: chunking-strategy
description: Benchmark and optimize Zarr chunking strategies for multi-dimensional scientific datasets. Measures wall-clock time, peak memory, and I/O metrics across spatial, time-series, and spectral access patterns. Generates recommendations based on empirical performance data following Nguyen et al. (2023) methodology.
license: MIT
metadata:
  references:
    - ./references/access-patterns.md
    - ./references/memory-constraints.md
    - ./references/nguyen-2023.md
    - ./references/benchmarking-methodology.md
  scripts:
    - ./scripts/benchmark_runner.py
    - ./scripts/rechunk.py
    - ./scripts/synthetic_data.py
---

# Chunking Strategy Benchmarking

**Benchmark and optimize Zarr chunking strategies** for multi-dimensional datasets stored in cloud object stores (S3, GCS) or local filesystems. This skill helps you determine the optimal chunk configuration for your specific access patterns before committing to a rechunking operation.

**Research basis:** Nguyen et al. (2023), "Impact of Chunk Size on Read Performance of Zarr Data in Cloud-based Object Stores" ([DOI: 10.1002/essoar.10511054.2](https://doi.org/10.1002/essoar.10511054.2))

## Inputs This Skill Expects

When the user invokes this skill, collect the following information:

### Required Inputs

1. **Dataset location:**
   - Local path: `/data/mydata.zarr`
   - S3: `s3://bucket/path/to/data.zarr`
   - GCS: `gs://bucket/path/to/data.zarr`

2. **Dimension names:** E.g., `['time', 'frequency', 'baseline']`

3. **Current chunk shape:** E.g., `(1, 2048, 2048)` (query with `ds.chunks`)

4. **Access pattern priorities:** Which patterns matter most?
   - "Primarily spatial access" → optimize for spatial
   - "Mixed workload" → find balanced strategy
   - "Don't know" → test all three and report trade-offs

### Optional Inputs

5. **Memory budget:** E.g., "8 GB" (typical laptop), "64 GB" (HPC node)
   - Used to filter out configurations that exceed available RAM

6. **Sample size:** How much data to benchmark?
   - Default: Subset that requires 10-20 chunks per access pattern
   - User can override: "Use first 500 time steps"

7. **Candidate configurations:** User can suggest specific chunk shapes to test
   - Default: Generate grid by varying one dimension at a time

8. **Number of runs:** Minimum 5 (default), can increase for high-variance networks

## Outputs This Skill Produces

### 1. Structured Markdown Report

**Sections:**
- **Dataset Summary:** Shape, dtype, current chunking, total size
- **Benchmark Environment:** Python version, instance type, network conditions
- **Results Tables:** One per access pattern with mean/std/min/max for each config
- **Performance Bias Analysis:** Which configs are balanced vs specialized
- **Memory Analysis:** Which configs fit within specified memory budget
- **Recommendation:** 1-3 suggested chunk configurations with reasoning

**Example recommendation:**
```markdown
## Recommendation

**For mixed workloads (spatial + time-series access):**

Use chunk shape **(50, 512, 512)**:
- Spatial access: 8.3 s ± 0.7 s (23% slower than optimal)
- Time-series access: 11.2 s ± 0.9 s (18% slower than optimal)
- Performance bias: 1.35 (well-balanced)
- Peak memory: 3.8 GB (fits in 8 GB budget)

**For spatial-only workloads:**

Use chunk shape **(10, 1024, 1024)** if memory permits:
- Spatial access: 6.1 s ± 0.5 s (optimal for this pattern)
- Peak memory: 10.2 GB (requires 16 GB system)
```

### 2. Environment Metadata (JSON)

Saved alongside the report for reproducibility:
```json
{
  "date": "2024-03-08",
  "python_version": "3.11.7",
  "xarray_version": "2024.1.0",
  "zarr_version": "2.17.0",
  "instance_type": "t2.xlarge",
  "storage_backend": "AWS S3 us-east-1"
}
```

### 3. (Optional) Dask Performance Report

If using Dask, generate `dask-report.html` showing task graphs and memory usage over time.

## Implementation Notes for the Agent

### Benchmarking Script Structure

The agent should use the helper scripts in `scripts/`:

- **`benchmark_runner.py`**: Core benchmarking loop (5+ runs, timing, memory measurement)
- **`rechunk.py`**: Rechunking utilities for generating test configurations
- **`synthetic_data.py`**: Generate synthetic Zarr data if no real dataset is available

### Cache Clearing

**Critical:** Clear caches between every run to measure cold-cache performance.

**macOS:**
```bash
sudo purge
```

**Linux:**
```bash
sync
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'
```

**fsspec:**
```python
# Disable or clear between runs
fsspec.config.conf['cache_storage'] = None
```

**See [references/benchmarking-methodology.md](references/benchmarking-methodology.md)** for complete methodology.

### Statistical Validity

- Minimum **5 runs** per configuration per access pattern
- Report **mean ± std** and **[min, max]** for each metric
- If std/mean > 0.3, increase run count or investigate variance source

### Memory Measurement

Use `tracemalloc` (built-in) or `memory_profiler` (more accurate):

```python
import tracemalloc

tracemalloc.start()
result = ds.sel(time=42).compute()
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
```

**Always report peak memory**, not mean.

### Timing

Use `time.perf_counter()` (not `time.time()`):

```python
import time

start = time.perf_counter()
result = ds.sel(time=42).compute()
wall_time = time.perf_counter() - start
```

## Progressive Disclosure References

The `references/` folder contains detailed documentation the agent should load on-demand:

- **[README.md](references/README.md)**: Table of contents describing when to load each reference
- **[nguyen-2023.md](references/nguyen-2023.md)**: Research paper summary and findings
- **[access-patterns.md](references/access-patterns.md)**: Detailed explanation of the three access patterns
- **[memory-constraints.md](references/memory-constraints.md)**: All-or-nothing constraint and memory measurement
- **[benchmarking-methodology.md](references/benchmarking-methodology.md)**: Best practices, pitfalls, and reproducibility

**Load references only when needed** to avoid context bloat. The README.md serves as a table of contents for progressive disclosure.

## Domain-Agnostic Design

Designed to work with **any multi-dimensional Zarr dataset**:

- Climate data: `time × latitude × longitude`
- Medical imaging: `patient × slice × x × y`
- Hyperspectral: `x × y × wavelength`

The user defines their dimension names and which dimensions are sliced vs loaded for each access pattern.

## Limitations

- **Read performance only:** This skill does not benchmark write operations or rechunking performance
- **Cloud storage focus:** Optimized for S3/GCS access patterns; local disk I/O may have different characteristics
- **Sample-based:** Benchmarks use data samples for speed; full dataset performance may differ slightly
- **No compression benchmarking:** Assumes compression codec is already chosen (handled by separate plugin)

## Resources and References

### Research Papers
- Nguyen et al. (2023): [DOI 10.1002/essoar.10511054.2](https://doi.org/10.1002/essoar.10511054.2)
- Lee et al. (2025): [DOI 10.48550/arXiv.2503.18037](https://doi.org/10.48550/arXiv.2503.18037)

### Tools
- **xarray**: https://docs.xarray.dev/
- **Zarr**: https://zarr.readthedocs.io/
- **rechunker**: https://rechunker.readthedocs.io/

### Related Work
- OVRO-LWA Portal: https://github.com/uw-ssec/ovro-lwa-portal
- AgentSkills.io: https://agentskills.io

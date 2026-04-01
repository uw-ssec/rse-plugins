# Report Generation — Deep Reference

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| Report Sections and Their Purpose | 18–33 | Overview of each report section and why it exists |
| Dataset Summary Block | 36–81 | Shape, dtype, chunks, storage, size — what to include and formatting |
| Environment Metadata | 84–143 | Platform, Python version, fsspec, network — recording reproducibility context |
| Configuration Comparison Tables | 146–189 | Formatting, units, highlighting winners, sorting, and column definitions |
| Per-Pattern Performance Tables | 192–231 | Time, memory, throughput per config per pattern with statistical detail |
| Performance Bias Summary | 234–270 | Bias per config, ranked, with classification and interpretation |
| Recommendation Writing | 273–338 | Primary with reasoning, alternatives, configs to avoid |
| Methodology Notes | 341–380 | Run count, cache clearing, statistical method, and reproducibility |

---

## Report Sections and Their Purpose

A performance report converts raw benchmark data into a structured document that supports decision-making. Each section serves a specific purpose:

1. **Dataset Summary** — Establishes what was tested. Without this, readers cannot judge whether results apply to their data.
2. **Environment Metadata** — Establishes where and how tests ran. Required for reproducibility and cross-session comparisons.
3. **Configuration Comparison Table** — The central decision-support artifact. Provides side-by-side ranking of all configurations.
4. **Per-Pattern Performance Tables** — Detailed statistical breakdown for readers who need to verify results or understand variance.
5. **Performance Bias Summary** — Quantifies how balanced each configuration is across access patterns.
6. **Recommendations** — Translates data into action. The section most stakeholders read first.
7. **Methodology Notes** — Documents how benchmarks were conducted for auditability and reproducibility.

Each section should be self-contained enough that a reader can skip to it directly. Use internal cross-references (e.g., "see Configuration Comparison Table above") when sections depend on each other.

The report template in `assets/comparison-table-template.md` and `assets/recommendation-template.md` provides the canonical structure. Fill in placeholders with actual benchmark data.

---

## Dataset Summary Block

The dataset summary appears at the top of the report, immediately after the title and date line. It establishes the subject of the benchmarks.

### Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| Path | Location of the dataset (local, S3, GCS) | `s3://climate-data/era5.zarr` |
| Shape | Full array dimensions | `(10000, 2048, 2048)` |
| Dtype | NumPy data type | `float32` |
| Current chunks | Chunk shape before benchmarking | `(1, 2048, 2048)` |
| Compression | Codec and level | `zstd level 3` |
| Total size | Uncompressed size | `156.3 GB` |

### Formatting Guidelines

Present as a two-column markdown table with "Property" and "Value" headers:

```markdown
| Property | Value |
|----------|-------|
| Path | s3://climate-data/era5.zarr |
| Shape | (10000, 2048, 2048) |
| Dtype | float32 |
| Current chunks | (1, 2048, 2048) |
| Compression | zstd level 3 |
| Total size | 156.3 GB |
```

### Calculating Total Size

```python
import numpy as np

total_size_bytes = np.prod(shape) * np.dtype(dtype).itemsize
total_size_gb = total_size_bytes / (1024 ** 3)
```

### Optional Fields

- **Number of variables** — for multi-variable datasets
- **Dimension names** — e.g., `time, latitude, longitude`
- **Sample size used** — if benchmarks ran on a subset, state the subset shape
- **Storage class** — e.g., S3 Standard, S3 Intelligent-Tiering

---

## Environment Metadata

Environment metadata ensures benchmark results are reproducible and interpretable. Record this at the start of each benchmark session.

### Required Fields

| Field | How to Obtain | Example |
|-------|---------------|---------|
| Platform | `platform.system()` | `Linux` |
| OS version | `platform.release()` | `5.15.0-91-generic` |
| Python version | `platform.python_version()` | `3.11.7` |
| xarray version | `xarray.__version__` | `2024.1.0` |
| zarr version | `zarr.__version__` | `2.17.0` |
| dask version | `dask.__version__` | `2024.1.0` |
| fsspec version | `fsspec.__version__` | `2024.1.0` |
| Instance type | Cloud provider metadata or manual | `t2.xlarge` |
| Storage backend | Manual | `AWS S3 us-east-1` |

### Collection Code

```python
import platform
import xarray
import zarr
import dask
import fsspec

env_metadata = {
    "platform": platform.system(),
    "os_version": platform.release(),
    "python_version": platform.python_version(),
    "xarray_version": xarray.__version__,
    "zarr_version": zarr.__version__,
    "dask_version": dask.__version__,
    "fsspec_version": fsspec.__version__,
    "instance_type": "FILL_IN",
    "storage_backend": "FILL_IN",
    "network_note": "FILL_IN"
}
```

### Formatting in Report

Present as a JSON block at the end of the report and as a summary table near the top:

```markdown
## Benchmark Environment

| Property | Value |
|----------|-------|
| Platform | Linux 5.15.0-91-generic |
| Python | 3.11.7 |
| xarray | 2024.1.0 |
| zarr | 2.17.0 |
| Instance type | t2.xlarge |
| Storage backend | AWS S3 us-east-1 |
| Runs per config | 10 |
| Memory budget | 8 GB |
```

---

## Configuration Comparison Tables

The comparison table is the most important artifact in the report. It enables direct side-by-side evaluation of all tested configurations.

### Column Definitions

| Column | Content | Unit | Sort Direction |
|--------|---------|------|----------------|
| Config | Label or letter identifier | — | — |
| Chunk Shape | Tuple notation | — | — |
| Spatial | Mean wall-clock time for spatial access | seconds | Ascending |
| Temporal | Mean wall-clock time for temporal access | seconds | Ascending |
| Spectral | Mean wall-clock time for spectral access | seconds | Ascending |
| PB | Performance bias ratio | ratio | Ascending |
| Peak Mem | Maximum memory across all patterns | GB | Ascending |
| Status | PASS or FAIL against memory budget | — | — |

### Formatting Rules

1. **Times**: One decimal place with standard deviation: `8.3 +/- 0.7`
2. **Memory**: One decimal place in GB: `3.8`
3. **PB**: Two decimal places: `1.35`
4. **Status**: `PASS` if peak memory <= budget, `FAIL` otherwise
5. **Winner highlighting**: Bold the best value in each numeric column

### Sorting

Default sort order: by the user's primary access pattern time (ascending). If no primary pattern specified, sort by PB (ascending).

### Example

```markdown
| Config | Chunk Shape | Spatial (s) | Temporal (s) | Spectral (s) | PB | Peak Mem (GB) | Status |
|--------|-------------|-------------|--------------|---------------|----|---------------|--------|
| B | (50, 512, 512) | 8.3 +/- 0.7 | 11.2 +/- 0.9 | 10.1 +/- 0.6 | **1.35** | **3.8** | PASS |
| C | (100, 256, 256) | 9.1 +/- 0.8 | 9.8 +/- 0.7 | 11.5 +/- 0.9 | 1.42 | 5.1 | PASS |
| A | (10, 1024, 1024) | **6.1 +/- 0.5** | 18.4 +/- 1.2 | 12.7 +/- 0.8 | 3.02 | 10.2 | FAIL |
| D | (200, 128, 128) | 15.3 +/- 1.1 | **5.8 +/- 0.4** | 14.2 +/- 1.0 | 2.64 | 4.3 | PASS |
```

### When Patterns Are Omitted

If the user benchmarked fewer than three patterns, include only the tested pattern columns. Set PB to 1.0 for single-pattern benchmarks and note this in the methodology section.

---

## Per-Pattern Performance Tables

Each access pattern gets its own detailed table showing all configurations with full statistical detail.

### Table Structure

```markdown
## Spatial Access Pattern

**Operation:** Load full frequency x baseline plane at a single time index

| Config | Mean (s) | Std (s) | Min (s) | Max (s) | Peak Mem (GB) | Chunks Read | Utilization |
|--------|----------|---------|---------|---------|---------------|-------------|-------------|
| A | 6.1 | 0.5 | 5.4 | 6.9 | 10.2 | 16 | 0.95 |
| B | 8.3 | 0.7 | 7.4 | 9.6 | 3.8 | 32 | 0.88 |
```

### Required Columns

- **Mean** — average across all timed runs
- **Std** — standard deviation across all timed runs
- **Min / Max** — range boundaries for identifying outliers
- **Peak Mem** — maximum memory observed across all runs for this config and pattern
- **Chunks Read** — number of chunk objects accessed
- **Utilization** — fraction of loaded bytes actually used

### Statistical Notes

- If `std / mean > 0.3`, add a footnote flagging high variance
- If `max > 2 * mean`, note the outlier run and consider excluding it
- Report the number of runs in the methodology section

### Operation Description

Each pattern table should begin with a one-line description of the operation being timed:

- **Spatial:** "Load full Y x X plane at a single time index"
- **Temporal:** "Load full time series at a single spatial point"
- **Spectral:** "Load full frequency/wavelength axis at a single spatial-temporal point"

---

## Performance Bias Summary

The bias summary table provides a quick view of how balanced each configuration is across access patterns.

### Table Structure

```markdown
## Performance Bias Summary

| Config | Chunk Shape | Best Pattern | Worst Pattern | PB | Classification |
|--------|-------------|-------------|---------------|-----|----------------|
| B | (50, 512, 512) | Spatial (8.3 s) | Temporal (11.2 s) | 1.35 | Balanced |
| C | (100, 256, 256) | Temporal (9.8 s) | Spectral (11.5 s) | 1.17 | Balanced |
| D | (200, 128, 128) | Temporal (5.8 s) | Spatial (15.3 s) | 2.64 | Moderate |
| A | (10, 1024, 1024) | Spatial (6.1 s) | Temporal (18.4 s) | 3.02 | Biased |
```

### Classification Key

| PB Range | Classification |
|----------|---------------|
| < 1.5 | Balanced |
| 1.5–3.0 | Moderate |
| 3.0–10.0 | Biased |
| > 10.0 | Extreme |

### Sorting

Sort by PB ascending (most balanced first). This ordering helps readers quickly identify generalist configurations.

### Interpretation Guidance

Include a brief paragraph after the table explaining what PB means for the user's specific workload:

- If workload is mixed: "Configurations with PB < 1.5 (Balanced) will perform consistently regardless of which access pattern is used."
- If workload is single-pattern: "Performance bias is less important for your use case. Focus on the primary pattern column in the comparison table."

---

## Recommendation Writing

The recommendation section is the most-read part of the report. Write it to be self-contained — a reader should understand the recommendation without reading the detailed tables.

### Primary Recommendation

Structure:

1. **Context** — one sentence restating the user's workload description
2. **Recommendation** — chunk shape in bold, with key metrics inline
3. **Reasoning** — why this configuration wins (PB, memory, pattern times)

Example:

```markdown
### Primary Recommendation

**For your mixed spatial + temporal workload (70%/30% split):**

Use chunk shape **(50, 512, 512)**:
- Weighted score: 9.2 s (best among feasible configs)
- Spatial access: 8.3 s +/- 0.7 s
- Temporal access: 11.2 s +/- 0.9 s
- Performance bias: 1.35 (Balanced)
- Peak memory: 3.8 GB (within 8 GB budget)

This configuration provides the best balance between spatial and temporal performance
while staying well within the memory budget. Although Config A is 27% faster for
spatial access, it exceeds the memory budget and has a PB of 3.02.
```

### Alternative Recommendation

Present when a specialist configuration is significantly better (>25% faster) for one pattern:

```markdown
### Alternative

**If spatial access is the only concern:**

Consider chunk shape **(10, 1024, 1024)**:
- Spatial access: 6.1 s +/- 0.5 s (27% faster than primary recommendation)
- Trade-off: Temporal access degrades to 18.4 s (64% slower)
- Peak memory: 10.2 GB (exceeds 8 GB budget — requires 16 GB system)
```

### Configurations to Avoid

List dominated or infeasible configurations with specific reasons:

```markdown
### Configurations to Avoid

- **(1, 2048, 2048)**: Extremely biased (PB = 12.4). Temporal access takes 45.2 s,
  making it impractical for any workload that includes time-series queries.
- **(200, 64, 64)**: Peak memory of 14.8 GB exceeds the 8 GB budget. Additionally,
  spatial access is 3x slower than the best feasible configuration.
```

### Tone and Style

- Be direct: "Use X" not "You might consider X"
- Include specific numbers: "27% faster" not "significantly faster"
- State trade-offs explicitly: "faster for spatial, but temporal degrades"
- Never recommend without stating the reasoning

---

## Methodology Notes

The methodology section ensures the benchmark is auditable and reproducible.

### Required Content

1. **Timing method**: Always `time.perf_counter()` (wall-clock)
2. **Memory measurement**: `tracemalloc` or `memory_profiler` — state which
3. **Cache clearing**: Method used (e.g., `sudo purge` on macOS, `echo 3 > /proc/sys/vm/drop_caches` on Linux)
4. **Run count**: Number of timed runs per configuration per pattern
5. **Warm-up**: Number of warm-up iterations performed before timing
6. **PB formula**: `max(T) / min(T)` per Nguyen et al. (2023)
7. **Statistical method**: How mean and std were computed (e.g., `numpy.mean`, `numpy.std(ddof=1)`)
8. **Outlier handling**: Whether any runs were excluded and why

### Example

```markdown
## Methodology Notes

- All timings measured with `time.perf_counter()` (wall-clock)
- Peak memory measured with `tracemalloc`
- OS page cache cleared between runs (`sudo purge` on macOS)
- fsspec caching disabled during benchmark session
- 2 warm-up iterations per configuration (not included in results)
- 10 timed runs per configuration per access pattern
- Performance bias calculated as max(T) / min(T) per Nguyen et al. (2023)
- Standard deviation computed with ddof=1 (sample standard deviation)
- No outlier runs excluded; all runs within 2x of mean
```

### Reproducibility Checklist

Before finalizing the methodology section, verify:

- [ ] Environment metadata JSON is included at the end of the report
- [ ] Run count is stated
- [ ] Cache clearing method is documented
- [ ] Any deviations from standard methodology are noted
- [ ] Library versions are recorded

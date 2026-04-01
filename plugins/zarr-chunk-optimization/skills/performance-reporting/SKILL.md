---
name: performance-reporting
description: Generate structured benchmark reports with configuration comparisons, performance bias analysis, ranked recommendations, and trade-off explanations from Zarr chunking benchmark results.
metadata:
  references:
    - references/report-generation.md
    - references/visualization-patterns.md
  assets:
    - assets/comparison-table-template.md
    - assets/recommendation-template.md
---

# Performance Reporting

Translate raw benchmark numbers into **actionable, structured reports** that help researchers and engineers choose the right Zarr chunking configuration. This skill takes timing data, memory measurements, and access pattern results produced by the chunking-strategy skill and produces markdown reports with comparison tables, performance bias analysis, ranked recommendations, and clear trade-off explanations. The goal is to move from "here are 200 numbers" to "here is what you should do and why."

## Resources in This Skill

- **[references/report-generation.md](references/report-generation.md)** — Deep reference on report sections, formatting, dataset summaries, environment metadata, comparison tables, per-pattern tables, bias summaries, recommendation writing, and methodology notes.
- **[references/visualization-patterns.md](references/visualization-patterns.md)** — Deep reference on bar charts, heatmaps, radar charts, scatter plots, and bias visualizations with matplotlib/hvPlot code examples.
- **[assets/comparison-table-template.md](assets/comparison-table-template.md)** — Ready-to-fill markdown template for benchmark comparison tables.
- **[assets/recommendation-template.md](assets/recommendation-template.md)** — Ready-to-fill markdown template for the recommendation section of a report.

## Quick Reference Card

### Report Structure Overview

1. **Dataset Summary** — shape, dtype, chunks, compression, total size
2. **Benchmark Environment** — platform, Python version, library versions, instance type, network
3. **Configuration Comparison Table** — all configs ranked with key metrics side by side
4. **Per-Pattern Results** — detailed tables for each access pattern (spatial, temporal, spectral)
5. **Performance Bias Summary** — bias score per config with classification
6. **Recommendations** — primary, alternative, configs to avoid
7. **Methodology Notes** — run count, cache clearing, statistical method

### Key Metrics at a Glance

| Metric | Unit | Direction | Primary Use |
|--------|------|-----------|-------------|
| Wall-clock time | seconds | Lower is better | Overall performance comparison |
| Time to first byte (TTFB) | milliseconds | Lower is better | Interactive responsiveness |
| Peak memory | GB | Lower is better | Feasibility under memory budgets |
| Throughput | MB/s | Higher is better | Bulk processing efficiency |
| Chunk utilization | 0.0–1.0 | Higher is better | I/O efficiency alignment |
| Performance bias (PB) | ratio | Closer to 1.0 | Workload balance assessment |

## When to Use

- **After benchmarks complete** — transform raw timing and memory data into a structured report
- **When comparing configurations** — rank and score multiple chunk shapes across access patterns
- **When presenting results to stakeholders** — produce clear tables, bias analysis, and recommendations that non-specialists can act on
- **Before rechunking** — confirm the recommended configuration with documented reasoning

## Report Structure

### Dataset Summary

Every report begins with a summary of the dataset under test. Include:

- **Path** — local, S3, or GCS URI
- **Shape** — full array dimensions (e.g., `(10000, 2048, 2048)`)
- **Dtype** — data type (e.g., `float32`)
- **Current chunks** — chunk shape before any rechunking
- **Compression** — codec and level (e.g., `zstd level 3`)
- **Total size** — uncompressed size in GB

### Environment Metadata

Record the full benchmarking environment so results are reproducible:

- Platform and OS version
- Python version
- Key library versions (xarray, zarr, dask, fsspec)
- Instance type (if cloud) or hardware specs (if local)
- Storage backend and region
- Network conditions (same-region, cross-region, local disk)

### Configuration Comparison Table

The central table of the report. Each row is a chunk configuration; columns show mean time per access pattern, performance bias, peak memory, and pass/fail status against the memory budget.

Mark the **winner** for each column. Use the comparison table template in `assets/comparison-table-template.md`.

### Per-Pattern Results

One detailed table per access pattern (spatial, temporal, spectral). Each table shows per-configuration statistics: mean, standard deviation, min, max, chunks read, and chunk utilization.

### Performance Bias Summary

A table showing each configuration's best pattern, worst pattern, PB score, and classification (Balanced, Moderate, Biased, Extreme).

### Recommendations

Structured as primary recommendation, alternative, and configurations to avoid. See the recommendation template in `assets/recommendation-template.md`.

## Performance Metrics Explained

### Wall-Clock Time

Total elapsed time from read start to completion. Measured with `time.perf_counter()`. This is the primary ranking metric because it captures everything the user experiences: network latency, data transfer, decompression, memory allocation, and framework overhead.

### Time to First Byte (TTFB)

Time from issuing the first read request to receiving the first byte of data. Matters for interactive workloads (visualization, exploratory analysis) where perceived responsiveness is important. Largely independent of chunk size; dominated by per-request overhead on cloud storage (20–100 ms typical).

### Peak Memory

Maximum memory allocated during the read operation. Measured with `tracemalloc` or `memory_profiler`. Configurations exceeding the stated memory budget must be flagged as infeasible. Peak memory scales roughly with `product(chunk_shape) * dtype.itemsize * concurrent_chunks`.

### Throughput

Effective data processing rate in MB/s or GB/s. Calculated as `total_bytes_read / wall_clock_time`. Useful for bulk processing workloads. Compare against theoretical maximums (network bandwidth, disk bandwidth) to identify bottlenecks.

### Chunk Utilization

Fraction of loaded data actually used by the access pattern. Calculated as `bytes_needed / bytes_loaded`. A utilization of 1.0 means every byte loaded is used. Below 0.5 indicates poor alignment between chunk shape and access pattern.

## Performance Bias Calculation

### Formula

```
Performance Bias (PB) = max(T_patterns) / min(T_patterns)
```

Where `T_patterns` is the set of mean wall-clock times across all tested access patterns for a given configuration.

### Ranges and Interpretation

| PB Value | Classification | Interpretation |
|----------|---------------|----------------|
| 1.0 | Perfectly balanced | Equal performance across all patterns |
| 1.0–1.5 | Balanced | Good for mixed workloads |
| 1.5–3.0 | Moderate | Acceptable if primary pattern is known |
| 3.0–10.0 | Biased | Only suitable for single-pattern workloads |
| > 10.0 | Extreme | Heavily optimized for one pattern at expense of others |

### Interpretation Guidelines

- **Mixed workloads** — prefer PB < 1.5
- **Known primary pattern** — tolerate higher PB if the primary pattern is fast enough
- **Unknown workload** — choose lowest PB that meets memory constraints
- **Weighted variant** — when pattern frequencies are known, use `Weighted PB = max(w_i * T_i) / min(w_i * T_i)`

## Generating Comparison Tables

1. Collect mean wall-clock time per configuration per access pattern
2. Calculate PB for each configuration
3. Record peak memory per configuration
4. Mark pass/fail against memory budget
5. Sort by primary metric (user's priority pattern time, or weighted score, or PB)
6. Highlight the winner in each column
7. Use consistent units: seconds for time, GB for memory, ratio for PB

Format numbers consistently: times to one decimal place with standard deviation (e.g., `8.3 +/- 0.7`), memory to one decimal place, PB to two decimal places.

## Ranking Configurations

### Scoring Methodology

Rank configurations using a weighted composite score:

```
score(config) = sum(weight_pattern * mean_time(config, pattern)) for each pattern
```

Default weights are equal across patterns. When the user specifies priorities (e.g., "70% spatial, 30% temporal"), apply those weights.

### Weighted Priorities

1. Apply user-specified weights to mean times per pattern
2. Sum weighted times to produce a single composite score
3. Rank by composite score (lower is better)
4. Break ties using: (a) lower PB, (b) lower peak memory, (c) smaller chunk size

### Elimination Rules

Before ranking, eliminate configurations that:
- Exceed the stated memory budget
- Have any single-pattern time more than 5x the best configuration for that pattern
- Show coefficient of variation (std/mean) > 0.3, indicating unreliable measurements

## Writing Recommendations

### Primary Recommendation

State the recommended chunk shape, the composite score or primary pattern time, PB classification, peak memory, and a one-sentence reasoning. Always include the specific numbers.

### Alternative Recommendation

Identify when a specialist configuration is significantly better (>25% faster) for one pattern. Present it as an alternative with the trade-off clearly stated.

### Configurations to Avoid

List any configurations that are dominated (worse on all metrics than another config) or that exceed memory constraints. State the specific reason for each.

## Confidence Assessment

### Run Count

- Minimum 5 runs required for any recommendation
- 10+ runs recommended for production decisions
- If fewer than 5 runs, flag the report as preliminary

### Variance Analysis

- Calculate coefficient of variation (CV = std/mean) for each configuration
- CV < 0.10: High confidence
- CV 0.10–0.20: Moderate confidence
- CV 0.20–0.30: Low confidence, consider more runs
- CV > 0.30: Unreliable, increase runs or investigate environment

### Environmental Noise

- Flag if benchmarks were run on shared infrastructure
- Note if network conditions varied during the session
- Record whether OS cache was cleared between runs
- Document any anomalous runs (>2x mean) that may indicate interference

## Common Mistakes

- **Reporting single-run results** — always require minimum 5 runs with mean and standard deviation
- **Ignoring memory constraints** — a fast configuration that exceeds RAM causes swapping or OOM, making it slower in practice
- **Comparing across sessions** — absolute timings from different days or instances are not directly comparable; use ratios
- **Omitting environment metadata** — without it, results are not reproducible
- **Choosing by PB alone** — a PB of 1.0 with slow absolute times is worse than PB of 1.5 with fast times
- **Forgetting to classify PB** — raw numbers without interpretation are not actionable
- **Not highlighting winners** — tables without visual emphasis force readers to scan every cell

## Best Practices

- Always include both the comparison table and per-pattern detail tables
- State the memory budget and mark infeasible configurations clearly
- Include methodology notes so results can be reproduced
- Use the templates in `assets/` for consistent formatting
- Calculate and report PB for every configuration, even if only one pattern was tested (PB = 1.0 trivially)
- Present recommendations in priority order: primary, alternative, avoid
- Include a confidence assessment based on run count and variance
- Load `references/report-generation.md` for formatting details and `references/visualization-patterns.md` when the user requests plots

## Resources

### Internal References

- [Report Generation — Deep Reference](references/report-generation.md)
- [Visualization Patterns — Deep Reference](references/visualization-patterns.md)

### Templates

- [Comparison Table Template](assets/comparison-table-template.md)
- [Recommendation Template](assets/recommendation-template.md)

### Related Skills

- **chunking-strategy** — produces the benchmark data this skill consumes
- **access-pattern-analysis** — identifies which access patterns to test
- **rechunking** — applies the recommended configuration

### External References

- Nguyen et al. (2023): [DOI 10.1002/essoar.10511054.2](https://doi.org/10.1002/essoar.10511054.2) — Performance bias metric and benchmarking methodology
- matplotlib: https://matplotlib.org/ — Plotting library for visualizations
- hvPlot: https://hvplot.holoviz.org/ — Interactive plotting for xarray datasets

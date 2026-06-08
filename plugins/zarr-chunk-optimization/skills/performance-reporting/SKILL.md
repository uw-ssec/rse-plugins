---
name: performance-reporting
description: Generates structured benchmark reports with configuration comparison tables, performance bias analysis, ranked recommendations, and trade-off explanations from Zarr chunking benchmark results. Use when the user has Zarr chunking benchmark data to analyze, needs to compare chunk configurations, wants performance recommendations for Zarr storage, or needs to present chunking strategy results to stakeholders.
metadata:
  references:
    - references/report-generation.md
    - references/visualization-patterns.md
  assets:
    - assets/comparison-table-template.md
    - assets/recommendation-template.md
---

# Performance Reporting

Transform raw Zarr chunking benchmark data into structured markdown reports with comparison tables, bias analysis, and ranked recommendations.

## Resources

| Resource | Purpose |
|----------|---------|
| [references/report-generation.md](references/report-generation.md) | Deep reference: section formatting, dataset summaries, environment metadata, table layout, recommendation writing |
| [references/visualization-patterns.md](references/visualization-patterns.md) | Bar charts, heatmaps, radar charts, scatter plots with matplotlib/hvPlot code |
| [assets/comparison-table-template.md](assets/comparison-table-template.md) | Ready-to-fill comparison table template |
| [assets/recommendation-template.md](assets/recommendation-template.md) | Ready-to-fill recommendation section template |

## Report Structure

1. **Dataset Summary** — path, shape, dtype, current chunks, compression, total size
2. **Benchmark Environment** — platform, Python/library versions, instance type, storage backend, network
3. **Configuration Comparison Table** — all configs ranked with key metrics side by side
4. **Per-Pattern Results** — detailed tables for each access pattern (spatial, temporal, spectral)
5. **Performance Bias Summary** — PB score and classification per config
6. **Recommendations** — primary, alternative, configs to avoid
7. **Methodology Notes** — run count, cache clearing, statistical method

**Validation checkpoint after generating:** Verify (a) every configuration appears in the comparison table, (b) each config has a winner highlight in at least one column, (c) memory budget pass/fail is marked for every config, (d) PB score is present for every config.

## Key Metrics

| Metric | Unit | Direction | Note |
|--------|------|-----------|------|
| Wall-clock time | s | Lower | Primary ranking metric |
| TTFB | ms | Lower | Interactive responsiveness |
| Peak memory | GB | Lower | Feasibility under budget |
| Throughput | MB/s | Higher | Bulk processing |
| Chunk utilization | 0–1 | Higher | I/O alignment (< 0.5 = poor fit) |
| Performance Bias (PB) | ratio | → 1.0 | Balance across patterns |

## Generating the Comparison Table (Python)

```python
import pandas as pd

def build_comparison_table(results: dict, memory_budget_gb: float) -> pd.DataFrame:
    """
    results = {
        "config_label": {
            "spatial_mean": float, "temporal_mean": float, "spectral_mean": float,
            "peak_memory_gb": float
        }, ...
    }
    """
    rows = []
    for label, m in results.items():
        times = [v for k, v in m.items() if k.endswith("_mean")]
        pb = max(times) / min(times) if min(times) > 0 else float("inf")
        rows.append({
            "Config": label,
            "Spatial (s)": f"{m['spatial_mean']:.1f}",
            "Temporal (s)": f"{m['temporal_mean']:.1f}",
            "Peak Mem (GB)": f"{m['peak_memory_gb']:.1f}",
            "PB": f"{pb:.2f}",
            "Within Budget": "✓" if m["peak_memory_gb"] <= memory_budget_gb else "✗",
        })
    df = pd.DataFrame(rows)
    # Mark winner per numeric column
    for col in ["Spatial (s)", "Temporal (s)", "Peak Mem (GB)"]:
        idx = df[col].astype(float).idxmin()
        df.loc[idx, col] = f"**{df.loc[idx, col]}**"
    return df.sort_values("PB")
```

## Performance Bias Score

```
PB = max(mean_time per pattern) / min(mean_time per pattern)
```

| PB | Classification | When acceptable |
|----|---------------|----------------|
| 1.0–1.5 | Balanced | Mixed workloads |
| 1.5–3.0 | Moderate | Known primary pattern |
| 3.0–10.0 | Biased | Single-pattern only |
| > 10.0 | Extreme | Rarely acceptable |

For weighted workloads: `Weighted PB = max(w_i × T_i) / min(w_i × T_i)`.

## Ranking and Elimination

**Eliminate before ranking** configurations that:
- Exceed the memory budget
- Have any single-pattern time > 5× the best config for that pattern
- Show CV (std/mean) > 0.3 (unreliable measurements)

**Score remaining configs:**
```
composite_score = sum(weight_i × mean_time_i)  # default: equal weights
```
Tie-break order: (1) lower PB, (2) lower peak memory, (3) smaller chunk size.

## Writing Recommendations

**Primary:** State chunk shape, composite score or dominant-pattern time, PB classification, peak memory, and one-sentence reasoning.

**Alternative:** Include when a specialist config is >25% faster on one pattern. State the trade-off explicitly.

**Avoid:** List dominated configs (worse on all metrics) or budget-exceeding configs with specific reasons.

See `assets/recommendation-template.md` for the fill-in-the-blank format.

## Progressive Disclosure

- Load [report-generation.md](references/report-generation.md) for detailed formatting, section-by-section guidance, confidence assessment, and common mistakes.
- Load [visualization-patterns.md](references/visualization-patterns.md) when the user requests charts or plots.

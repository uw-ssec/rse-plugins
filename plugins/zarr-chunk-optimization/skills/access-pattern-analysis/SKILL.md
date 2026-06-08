---
name: access-pattern-analysis
description: Identifies, formalizes, and prioritizes data access patterns for multi-dimensional Zarr datasets, translating user workflow descriptions into weighted, benchmark-ready pattern definitions with xarray operation mappings. Use when defining or optimizing access patterns before benchmarking chunk configurations, when translating informal user workflow descriptions ("I make maps", "I need time series") into xarray operations, when assigning weights to mixed access patterns for a shared dataset, or when diagnosing slow reads caused by a mismatch between chunk layout and access pattern.
metadata:
  references:
    - references/pattern-identification.md
    - references/workflow-mapping.md
  assets:
    - assets/pattern-definitions-template.json
    - assets/workflow-questionnaire.md
---

# Access Pattern Analysis

Access pattern analysis is the foundation of effective chunk optimization. Chunk shape must reflect how data is actually read — not how it was written. Benchmarking without identifying patterns first produces chunk configurations optimized for artificial workloads that fail in production.

## Resources

| Resource | Purpose |
|----------|---------|
| `references/pattern-identification.md` | Deep reference: spatial, temporal, spectral, diagonal patterns with domain examples |
| `references/workflow-mapping.md` | Translating user descriptions and xarray operations into formal definitions |
| `assets/pattern-definitions-template.json` | JSON template for benchmark-ready weighted pattern definitions |
| `assets/workflow-questionnaire.md` | Structured interview questions for eliciting access patterns |

## Workflow

1. **Interview** — use `assets/workflow-questionnaire.md`; listen for keyword signals (see table below).
2. **Identify patterns** — map keywords to one or more patterns from the quick reference.
3. **Write pattern definitions** — fill out a JSON for each pattern (name, description, xarray operation, weight).
4. **Validate weights** — all weights must sum to exactly 1.0; each weight must reflect frequency, latency sensitivity, and user count.
5. **Run benchmark** — pass the completed JSON to the chunking benchmark.

**Validation gate after step 4:** Weights sum to 1.0. Every pattern has an executable xarray operation string. No pattern weight is assigned based solely on assumption — mark it `ASSUMPTION` and collect evidence before finalising.

## Quick Reference

| Pattern | Slice Shape | xarray Operation | Ideal Chunk |
|---------|------------|-----------------|-------------|
| Spatial | `(1, lat, lon)` | `ds.sel(time="2020-01-01")` | `(1, 256, 256)` |
| Temporal | `(time, 1, 1)` | `ds.sel(lat=45.0, lon=-90.0)` | `(1000, 1, 1)` |
| Spectral | `(1, 1, freq)` | `ds.sel(time="2020-01-01", lat=45.0)` | `(1, 1, 4096)` |
| Diagonal | `(time_sub, lat_sub, lon_sub)` | `ds.sel(time=slice(...), lat=slice(...))` | balanced |

Full pattern descriptions, chunk alignment rules, and domain examples: [pattern-identification.md](references/pattern-identification.md).

## Keyword → Pattern Mapping

| User Says | Pattern |
|-----------|---------|
| "I make maps" / "I visualize fields" | Spatial |
| "I look at trends" / "time series at stations" | Temporal |
| "I compare across bands" / "spectral analysis" | Spectral |
| "I compute regional averages over time" | Mixed (spatial + temporal) |
| "I do anomaly detection on subregions" | Diagonal |

## Pattern Definition (complete example)

```json
{
  "dataset": {
    "name": "era5-daily-2m-temp",
    "dimensions": ["time", "lat", "lon"],
    "shape": [14600, 721, 1440],
    "current_chunks": [1, 721, 1440],
    "storage_backend": "s3"
  },
  "patterns": [
    {
      "name": "spatial_single_timestep",
      "description": "Full 2D temperature field at one date. Used for map visualization.",
      "xarray_operation": "ds['t2m'].sel(time='2020-06-15')",
      "weight": 0.60,
      "expected_bytes_per_read": 8294400
    },
    {
      "name": "temporal_single_point",
      "description": "Full time series at a single station location. Used for trend analysis.",
      "xarray_operation": "ds['t2m'].sel(lat=45.0, lon=-90.0, method='nearest')",
      "weight": 0.25,
      "expected_bytes_per_read": 116800
    },
    {
      "name": "diagonal_regional_mean",
      "description": "Monthly spatial subset averaged over region. Used for climate indices.",
      "xarray_operation": "ds['t2m'].sel(lat=slice(30,60), lon=slice(-120,-60), time=slice('2000','2020')).mean(dim=['lat','lon'])",
      "weight": 0.15,
      "expected_bytes_per_read": 120000000
    }
  ],
  "metadata": {
    "analyst": "jane.smith",
    "date": "2024-03-15",
    "method": "interview",
    "stakeholders": ["climate-team", "viz-team"]
  }
}
```

Use `assets/pattern-definitions-template.json` as the starting scaffold. See [workflow-mapping.md](references/workflow-mapping.md) for weighting guidance.

## Mixed-Pattern Strategies

When no single chunk shape satisfies all patterns:

- **Compromise chunking** — mediocre for all, optimal for none; use when patterns are evenly weighted.
- **Sharding (Zarr v3)** — outer shards align with dominant pattern; inner chunks align with secondary.
- **Rechunking with virtual layers** — Kerchunk/VirtualiZarr reference for the secondary layout; doubles storage.
- **Separate stores** — two copies chunked differently; practical only when storage cost is negligible.

## Common Mistakes

- Benchmarking without identifying patterns first.
- Assuming a single pattern; most datasets serve multiple workflows.
- Confusing write patterns with read patterns — chunk for reads.
- Over-weighting rare patterns relative to daily-use patterns.

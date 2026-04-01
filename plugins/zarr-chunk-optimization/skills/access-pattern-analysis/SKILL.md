---
name: access-pattern-analysis
description: Identify, formalize, and prioritize data access patterns for multi-dimensional Zarr datasets. Translates user workflow descriptions into benchmark-ready pattern definitions with xarray operation mappings.
metadata:
  references:
    - references/pattern-identification.md
    - references/workflow-mapping.md
  assets:
    - assets/pattern-definitions-template.json
    - assets/workflow-questionnaire.md
---

Access pattern analysis is the foundation of effective chunk optimization. The shape and size of Zarr chunks must reflect how data is actually read -- not how it is stored or how it was originally written. A chunk layout optimized for spatial queries will punish temporal access with orders-of-magnitude slowdowns, and vice versa. Before running any benchmark, you must know which access patterns matter, how often each occurs, and how to express them as concrete xarray operations. Skipping this step means benchmarking against the wrong workload, which produces chunk configurations that feel fast in testing and fail in production.

## Resources in This Skill

| Resource | Purpose |
|----------|---------|
| `references/pattern-identification.md` | Deep reference on spatial, temporal, spectral, and diagonal access patterns with domain examples |
| `references/workflow-mapping.md` | Translating user descriptions and xarray operations into formal pattern definitions |
| `assets/pattern-definitions-template.json` | JSON template for defining benchmark-ready access patterns with weights |
| `assets/workflow-questionnaire.md` | Structured interview questions to elicit access patterns from users |

## Quick Reference Card

| Pattern | Typical Slice Shape | Example xarray Operation | Dominant Dimension |
|---------|---------------------|--------------------------|-------------------|
| Spatial | `(1, lat, lon)` | `ds.sel(time="2020-01-01")` | lat, lon |
| Temporal | `(time, 1, 1)` | `ds.sel(lat=45.0, lon=-90.0)` | time |
| Spectral | `(1, 1, freq)` | `ds.sel(time="2020-01-01", lat=45.0)` | frequency/channel |
| Diagonal | `(time_sub, lat_sub, lon_sub)` | `ds.sel(time=slice(...), lat=slice(...))` | multiple partial |

## When to Use

- **Before benchmarking.** Always run access pattern analysis before defining chunk configurations to test. Benchmarking without it produces misleading results.
- **When a user describes their workflow in general terms.** Phrases like "I mostly look at maps" or "I need time series at stations" are informal pattern descriptions that need formalization.
- **When optimizing for mixed workloads.** If multiple users or pipelines hit the same dataset with different access patterns, you need to quantify the mix and weight patterns accordingly.
- **When performance complaints arise.** Slow reads often indicate a mismatch between chunk layout and the dominant access pattern.

## The Three Primary Access Patterns

### Spatial Access

Spatial access retrieves a full 2D (or higher-dimensional) spatial field at a single point in another dimension, typically time. This is the most common pattern in visualization, mapping, and spatial analysis.

```
Time axis:  [T0] [T1] [T2] [T3] ...
             |
             v
            +--+--+--+--+
            |  |  |  |  |   Entire lat/lon plane
            +--+--+--+--+   at one timestep
            |  |  |  |  |
            +--+--+--+--+
```

**Ideal chunk shape:** Large spatial dimensions, small time dimension (e.g., `(1, 256, 256)`).

**Common xarray operations:**
- `ds.sel(time="2020-06-15")` -- single timestep map
- `ds.isel(time=0)` -- first timestep
- `ds.sel(time="2020-06-15").plot()` -- visualization

### Temporal Access

Temporal access retrieves a full time series at a single spatial location or small spatial region. This pattern dominates trend analysis, station-based validation, and point forecasting.

```
Lat/Lon grid:
    +--+--+--+--+
    |  |  |  |  |
    +--+--+--+--+
    |  | X|  |  |   Single pixel, all timesteps
    +--+--+--+--+
         |
         v
    [T0, T1, T2, T3, T4, T5, ...]
```

**Ideal chunk shape:** Large time dimension, small spatial dimensions (e.g., `(1000, 1, 1)`).

**Common xarray operations:**
- `ds.sel(lat=45.0, lon=-90.0)` -- point time series
- `ds.sel(lat=45.0, lon=-90.0).resample(time="1M").mean()` -- monthly means at a point
- `ds.sel(lat=45.0, lon=-90.0).groupby("time.year")` -- annual grouping

### Spectral/Frequency Access

Spectral access retrieves data across a frequency, wavelength, or channel dimension at a fixed spatial and/or temporal position. This pattern appears in radio astronomy, hyperspectral remote sensing, and multi-band analysis.

```
Frequency axis:
    [F0] [F1] [F2] [F3] [F4] ...
     |    |    |    |    |
     v    v    v    v    v
    All frequencies at one (time, position) point
```

**Ideal chunk shape:** Large frequency dimension, small spatial and time dimensions (e.g., `(1, 1, 1, 4096)`).

**Common xarray operations:**
- `ds.sel(time="2020-01-01", lat=45.0, lon=-90.0)` -- full spectrum at a point
- `ds.mean(dim=["lat", "lon"])` -- spatially averaged spectrum

## Identifying Patterns from User Workflows

The goal is to translate informal workflow descriptions into one or more formal access patterns. Use the questionnaire in `assets/workflow-questionnaire.md` and listen for keyword signals:

| User Says | Likely Pattern |
|-----------|---------------|
| "I make maps" / "I visualize fields" | Spatial |
| "I look at trends over time" / "time series at stations" | Temporal |
| "I compare across bands" / "spectral analysis" | Spectral |
| "I compute regional averages over time" | Mixed (spatial + temporal) |
| "I do anomaly detection on subregions" | Diagonal |

### Interview Approach

1. Ask what the final output looks like (map, line plot, table).
2. Ask which dimensions are sliced versus aggregated.
3. Ask how much data is touched per operation.
4. Ask how often each operation runs.

## Formalizing Patterns for Benchmarking

Once identified, translate each pattern into a concrete xarray slicing operation that benchmarks can execute repeatedly. Use the template in `assets/pattern-definitions-template.json`.

A well-formed pattern definition includes:
- **Name** -- short identifier (e.g., `spatial_single_timestep`)
- **Description** -- one sentence explaining the access
- **xarray operation** -- exact code string that benchmarks will call
- **Weight** -- relative importance (0.0 to 1.0, all weights must sum to 1.0)
- **Expected data volume** -- approximate bytes read per operation

## Pattern Priority Weighting

When a dataset serves multiple access patterns, assign weights based on:

1. **Frequency of use** -- How often is each pattern executed? Daily spatial maps outweigh monthly temporal extractions.
2. **Latency sensitivity** -- Interactive visualization (spatial) demands low latency more than batch processing (temporal).
3. **User count** -- Patterns used by many users get higher weight than single-user workflows.
4. **Data volume** -- Patterns that touch more data benefit more from chunk alignment.

Example weighting for a climate reanalysis dataset:

| Pattern | Frequency | Users | Weight |
|---------|-----------|-------|--------|
| Spatial (daily maps) | 50/day | 20 | 0.60 |
| Temporal (station validation) | 10/day | 5 | 0.25 |
| Diagonal (regional monthly means) | 2/day | 3 | 0.15 |

## Mixed-Pattern Strategies

When no single chunk shape satisfies all patterns:

- **Compromise chunking** -- Choose a shape that is mediocre for all patterns rather than optimal for one. Useful when patterns are evenly weighted.
- **Rechunking with virtual layers** -- Store data in one layout, provide a Kerchunk or VirtualiZarr reference for the other. Doubles storage but optimizes both.
- **Sharding (Zarr v3)** -- Use shards that align with the dominant pattern and inner chunks that align with the secondary pattern.
- **Separate stores** -- Maintain two copies chunked differently. Practical only when storage is cheap relative to compute.

## Domain-Specific Pattern Examples

### Climate Science
- **Primary:** Spatial (daily/monthly map visualization)
- **Secondary:** Temporal (station comparison, trend analysis)
- **Tertiary:** Diagonal (regional time-averaged anomalies)

### Radio Astronomy
- **Primary:** Spectral (per-baseline spectrum extraction)
- **Secondary:** Temporal (time-frequency waterfalls per baseline)
- **Tertiary:** Spatial (imaging requires all baselines at one time/frequency)

### Genomics
- **Primary:** Row-based (single gene across all samples)
- **Secondary:** Column-based (all genes for one sample)
- **Considerations:** Sparse access patterns, high dimensionality

### Remote Sensing
- **Primary:** Spatial (scene-level analysis, tile retrieval)
- **Secondary:** Temporal (change detection at fixed locations)
- **Tertiary:** Spectral (multi-band indices like NDVI)

## Common Mistakes

- **Benchmarking without identifying patterns first.** This produces chunk shapes optimized for artificial workloads that do not reflect real usage.
- **Assuming a single pattern.** Most real datasets serve multiple access patterns. Ignoring secondary patterns causes unexpected slowdowns for some users.
- **Confusing write patterns with read patterns.** Data is often written sequentially along time but read spatially. Chunk for reads, not writes.
- **Over-weighting rare patterns.** A pattern used once a month should not dominate chunk shape decisions over a pattern used hundreds of times daily.
- **Ignoring network and cache effects.** Access patterns interact with object storage request overhead and local cache behavior. A pattern that reads many small chunks may be slower than one that reads fewer large chunks even if total bytes are similar.

## Best Practices

- **Interview users before touching configuration.** Use the workflow questionnaire to systematically capture access patterns.
- **Quantify pattern frequency.** Instrument existing code or review logs to count how often each pattern executes.
- **Express patterns as executable xarray code.** Ambiguous descriptions lead to ambiguous benchmarks.
- **Assign explicit weights.** Force stakeholders to prioritize. Unweighted patterns lead to unresolvable debates during optimization.
- **Revisit patterns after optimization.** Access patterns evolve as users discover new capabilities. Re-evaluate quarterly.
- **Document everything.** Record the identified patterns, their weights, and the rationale in the pattern definitions file for reproducibility.

## Resources

- `references/pattern-identification.md` -- Detailed guidance on identifying and classifying access patterns across scientific domains.
- `references/workflow-mapping.md` -- Techniques for translating user workflows and xarray operations into formal pattern definitions.
- `assets/pattern-definitions-template.json` -- Ready-to-use JSON template for defining weighted access patterns.
- `assets/workflow-questionnaire.md` -- Structured questionnaire for eliciting access patterns from users and stakeholders.

# Workflow Mapping — Deep Reference

## Contents

| Section | Line |
|---------|------|
| [From User Description to Formal Pattern](#from-user-description-to-formal-pattern) | 16 |
| [xarray Operation to Pattern Mapping](#xarray-operation-to-pattern-mapping) | 73 |
| [Common Scientific Workflows](#common-scientific-workflows) | 128 |
| [Dask Task Graph Analysis](#dask-task-graph-analysis) | 187 |
| [Quantifying Pattern Mix](#quantifying-pattern-mix) | 246 |
| [Documenting Access Patterns](#documenting-access-patterns) | 301 |

---

## From User Description to Formal Pattern

Users rarely describe their access patterns in terms of chunk shapes or array slicing. They talk about their science -- "I compare SST maps across decades" or "I pull spectra for each pointing." Your job is to translate these descriptions into formal pattern definitions that benchmarks can execute.

### Interview Technique

Use the questionnaire in `assets/workflow-questionnaire.md` as a starting point, but adapt your approach based on the user's level of technical detail.

**For domain scientists (low xarray familiarity):**
1. Ask what the final product looks like. "Is it a map, a time series plot, a table?"
2. Ask what varies and what stays fixed. "Do you look at one time and all locations, or one location and all times?"
3. Ask about data volume. "Do you load the whole dataset or a subset?"
4. Ask about frequency. "How many times a day/week do you do this?"

**For data engineers (high xarray familiarity):**
1. Ask for representative code snippets or notebooks.
2. Ask which `.sel()` / `.isel()` calls are most common.
3. Ask about Dask usage and typical cluster size.
4. Ask about caching behavior and repeat access.

### Keyword Mapping

Listen for keywords that signal specific patterns:

| Keyword / Phrase | Pattern | Confidence |
|------------------|---------|------------|
| "map," "field," "snapshot," "image," "scene" | Spatial | High |
| "time series," "trend," "historical," "evolution" | Temporal | High |
| "spectrum," "bandpass," "channels," "SED" | Spectral | High |
| "regional average," "bounding box," "subset" | Diagonal | Medium |
| "anomaly," "climatology," "departure" | Mixed (spatial + temporal) | Medium |
| "mosaic," "composite," "stacking" | Spatial (multi-file) | Medium |
| "correlation," "regression" | Depends on dimensions | Low |
| "machine learning," "training data" | Diagonal (batch loading) | Low |

### Translating Descriptions to Patterns

**User says:** "I compute monthly mean SST maps for the tropical Pacific."

**Translation:**
1. "monthly mean" -> temporal aggregation (`.resample(time="1M").mean()`)
2. "SST maps" -> output is spatial (2D map)
3. "tropical Pacific" -> spatial subset (`.sel(lat=slice(-30, 30), lon=slice(120, 280))`)

**Formal pattern:** Diagonal access with spatial-dominant output. The read touches a spatial subset across all timesteps within each month, then reduces along time.

**User says:** "I extract light curves for each source in my catalog."

**Translation:**
1. "light curves" -> time series output
2. "each source" -> iteration over spatial points
3. "catalog" -> many point locations

**Formal pattern:** Temporal access, repeated across spatial points. The dominant I/O pattern is temporal even though many points are accessed, because each individual read is a time series extraction.

---

## xarray Operation to Pattern Mapping

The most reliable way to identify access patterns is to examine the actual xarray operations in user code. Each operation implies a specific read pattern against the underlying Zarr store.

### Selection Operations

| Operation | Pattern | Notes |
|-----------|---------|-------|
| `ds.sel(time=scalar)` | Spatial | Fixes time, reads full spatial extent |
| `ds.sel(lat=scalar, lon=scalar)` | Temporal | Fixes space, reads full time extent |
| `ds.sel(freq=scalar)` | Non-spectral slice | Depends on remaining dims |
| `ds.sel(time=scalar, lat=scalar)` | 1D slice | Single dimension remains |
| `ds.isel(time=0)` | Spatial | Same as scalar sel on time |
| `ds.sel(time=slice(...))` | Partial temporal | Subset of time dimension |
| `ds.sel(lat=slice(...), lon=slice(...))` | Partial spatial | Spatial bounding box |

### Aggregation Operations

| Operation | Read Pattern | Output Pattern |
|-----------|-------------|----------------|
| `ds.mean(dim="time")` | Full dataset | Spatial |
| `ds.mean(dim=["lat", "lon"])` | Full dataset | Temporal |
| `ds.mean(dim="freq")` | Full dataset | Non-spectral |
| `ds.resample(time="1M").mean()` | Full time per month | Spatial per month |
| `ds.groupby("time.season").mean()` | Full dataset | Spatial per season |
| `ds.rolling(time=30).mean()` | Temporal windows | Same shape |

### Computation Operations

| Operation | Read Pattern | Notes |
|-----------|-------------|-------|
| `ds["var1"] - ds["var2"]` | Aligned full read | Pattern depends on subsequent sel/agg |
| `ds["var"].differentiate("time")` | Temporal | Needs contiguous time chunks |
| `ds["var"].interp(lat=new_lats)` | Spatial | Interpolation along spatial axes |
| `xr.apply_ufunc(func, ds)` | Full dataset | Pattern determined by func internals |

### Compound Operations

Many real workflows chain multiple operations. The access pattern is determined by the first operation that touches the store (before Dask optimization):

```python
# Pattern: Spatial (initial read is full spatial at each time)
ds["temp"].sel(lat=slice(30, 50), lon=slice(-100, -80)).mean(dim=["lat", "lon"])

# Pattern: Temporal (initial read is time series at each point)
ds["temp"].sel(lat=45.0, lon=-90.0).resample(time="1M").mean()

# Pattern: Full scan (no early selection)
ds["temp"].mean(dim="time")
```

**Key insight:** Dask and xarray may reorder operations for optimization. The logical pattern in user code may differ from the physical I/O pattern. When in doubt, profile the actual chunk access.

---

## Common Scientific Workflows

This section maps common end-to-end scientific workflows to their constituent access patterns and recommended chunk strategies.

### Climate Downscaling

**Workflow:** Read coarse-resolution global data, interpolate to fine grid, write regional output.

**Access patterns:**
1. Spatial read of each timestep (dominant, ~70%)
2. Temporal reads for boundary condition interpolation (~20%)
3. Diagonal reads for regional subsetting (~10%)

**Recommended chunk shape:** Spatial-dominant, e.g., `(24, 128, 128)` for `(time, lat, lon)`.

### Trend Analysis

**Workflow:** Read full time series at each grid cell, fit linear trend, produce trend map.

**Access patterns:**
1. Temporal read at each spatial point (dominant, ~90%)
2. Spatial read for visualization of results (~10%)

**Recommended chunk shape:** Temporal-dominant, e.g., `(1000, 16, 16)` for `(time, lat, lon)`.

### Climatological Anomaly Computation

**Workflow:** Compute long-term mean for each day-of-year, subtract from daily data.

**Access patterns:**
1. Grouped temporal read (`groupby("time.dayofyear")`) — touches all times at each spatial point (~60%)
2. Spatial read for anomaly map output (~40%)

**Recommended chunk shape:** Balanced, e.g., `(365, 64, 64)` for `(time, lat, lon)`.

### Radio Interferometric Calibration

**Workflow:** Read visibility data per baseline per frequency, solve for antenna gains.

**Access patterns:**
1. Spectral read per baseline per time integration (dominant, ~80%)
2. Temporal read per baseline per frequency channel (~15%)
3. Full baseline read at one time-frequency point for imaging (~5%)

**Recommended chunk shape:** Spectral-dominant, e.g., `(1, 1, 4096)` for `(time, baseline, frequency)`.

### Satellite Change Detection

**Workflow:** Load time stack for a spatial tile, compute temporal statistics, classify change.

**Access patterns:**
1. Diagonal read — spatial tile across all times (dominant, ~75%)
2. Spatial read for single-date reference images (~15%)
3. Temporal read at validation points (~10%)

**Recommended chunk shape:** Balanced with spatial bias, e.g., `(50, 256, 256)` for `(time, y, x)`.

---

## Dask Task Graph Analysis

When users run xarray operations backed by Dask, the task graph reveals the actual I/O pattern regardless of how the user describes their workflow. Analyzing task graphs is the most objective method for pattern identification.

### Reading Task Graphs

```python
import dask

# Visualize the task graph
result = ds["temp"].sel(time="2020-01-01").mean(dim="lat")
result.visualize(filename="task_graph.png")
```

**Spatial pattern graph characteristics:**
- Wide, shallow graph (many parallel chunk reads at one time index).
- Tasks are labeled with chunk coordinates that vary in spatial dimensions but share a time index.
- Minimal inter-chunk dependencies.

**Temporal pattern graph characteristics:**
- Narrow, deep graph (sequential reads along time at one spatial index).
- Tasks are labeled with chunk coordinates that vary in time but share spatial indices.
- Aggregation tasks at the end (e.g., mean, sum).

**Diagonal pattern graph characteristics:**
- Moderately wide and moderately deep.
- Chunk coordinates vary across multiple dimensions.
- More complex dependency structure than pure spatial or temporal.

### Profiling Chunk Access

Use Zarr's built-in diagnostics or custom instrumentation:

```python
import zarr

store = zarr.open("dataset.zarr", mode="r")
# Count chunk reads per operation
# Compare chunks_read vs chunks_needed (read amplification)
```

### Dask Performance Reports

```python
from dask.distributed import Client, performance_report

client = Client()

with performance_report(filename="report.html"):
    result = ds["temp"].sel(time="2020-01-01").load()
```

The performance report shows:
- Number of tasks (correlates with chunks read).
- Data transfer volume (indicates read amplification).
- Task duration distribution (skewed distributions suggest chunk misalignment).

---

## Quantifying Pattern Mix

Real workloads are rarely a single pattern. Quantifying the mix allows you to assign weights in the pattern definitions template and make informed chunk shape decisions.

### Measurement Methods

**1. Operation counting:**
Review all scripts, notebooks, and pipeline code that access the dataset. Categorize each data-touching operation by pattern type. Count occurrences.

```
Spatial operations: 45
Temporal operations: 23
Diagonal operations: 8
Total: 76

Spatial weight: 45/76 = 0.59
Temporal weight: 23/76 = 0.30
Diagonal weight: 8/76 = 0.11
```

**2. Byte-weighted counting:**
Weight each operation by the data volume it reads. A spatial read of a global field at one timestep might read 50 MB, while a temporal read at one point might read 500 KB. Byte-weighted counts reflect storage system load more accurately.

```
Spatial bytes: 45 * 50 MB = 2250 MB
Temporal bytes: 23 * 0.5 MB = 11.5 MB
Diagonal bytes: 8 * 20 MB = 160 MB
Total: 2421.5 MB

Spatial weight: 2250/2421.5 = 0.93
Temporal weight: 11.5/2421.5 = 0.005
Diagonal weight: 160/2421.5 = 0.066
```

**3. Latency-weighted counting:**
Weight each operation by its latency impact. Interactive operations (visualization, exploration) demand low latency and should be weighted higher than batch operations that tolerate minutes-long waits.

### Choosing a Weighting Scheme

| Scenario | Recommended Scheme |
|----------|--------------------|
| All users do similar work | Simple operation counting |
| Dataset serves API with SLOs | Latency-weighted |
| Storage I/O is the bottleneck | Byte-weighted |
| Mixed interactive + batch | Hybrid (latency for interactive, byte for batch) |

### Validating Weights

After assigning weights, sanity-check with stakeholders:
- Does the highest-weighted pattern match what users consider "most important"?
- Would optimizing for the top pattern at the expense of others be acceptable?
- Are any patterns missing from the analysis?

---

## Documenting Access Patterns

Thorough documentation ensures that chunk optimization decisions are reproducible, auditable, and revisable as workloads evolve.

### What to Document

1. **Dataset description:** Name, dimensions, shape, dtype, current chunk layout, storage backend.
2. **Identified patterns:** Each pattern with name, description, example xarray operation, and weight.
3. **Data sources:** How patterns were identified (interviews, log analysis, code review, profiling).
4. **Conflict decisions:** Which patterns conflict, which resolution strategy was chosen, and why.
5. **Stakeholder sign-off:** Who agreed to the weights and priorities.
6. **Review schedule:** When patterns should be re-evaluated.

### Documentation Format

Use the `assets/pattern-definitions-template.json` template for machine-readable pattern definitions. Supplement with a human-readable summary that captures rationale and context.

### Example Documentation Block

```markdown
## Access Pattern Analysis for ERA5 Temperature Dataset

**Date:** 2025-03-15
**Analyst:** J. Smith
**Stakeholders:** Climate team (A. Jones), Validation team (B. Chen)

### Identified Patterns

1. **Spatial (weight: 0.55)** — Daily map visualization for operational forecasting.
   Frequency: ~200 ops/day across 15 users.
   Operation: `ds["t2m"].sel(time="2020-01-01")`

2. **Temporal (weight: 0.30)** — Station validation against observations.
   Frequency: ~80 ops/day across 8 users.
   Operation: `ds["t2m"].sel(lat=51.5, lon=-0.1, method="nearest")`

3. **Diagonal (weight: 0.15)** — Regional monthly means for climate indices.
   Frequency: ~20 ops/day across 3 users.
   Operation: `ds["t2m"].sel(lat=slice(30,50), lon=slice(-100,-80), time=slice("2010","2020")).mean(dim=["lat","lon"]).resample(time="1M").mean()`

### Conflicts and Resolution

Spatial vs. temporal conflict resolved with compromise chunking `(48, 128, 128)`.
Spatial access will read 128x128 chunks (aligned). Temporal access will read
48-step chunks (acceptable, ~150 chunks for 20 years of 6-hourly data).

### Review Schedule

Re-evaluate patterns at next dataset version release or if user complaints arise.
```

### Version Control

Store pattern documentation alongside the dataset metadata or in the optimization repository. Track changes over time so that chunk layout decisions can be traced back to the pattern analysis that motivated them.

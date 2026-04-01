# Pattern Identification — Deep Reference

## Contents

| Section | Line |
|---------|------|
| [Spatial Access Patterns](#spatial-access-patterns) | 16 |
| [Temporal Access Patterns](#temporal-access-patterns) | 73 |
| [Spectral/Frequency Access Patterns](#spectralfrequency-access-patterns) | 131 |
| [Diagonal/Mixed Access Patterns](#diagonalmixed-access-patterns) | 182 |
| [Identifying Dominant Patterns](#identifying-dominant-patterns) | 240 |
| [Pattern Conflict Resolution](#pattern-conflict-resolution) | 289 |

---

## Spatial Access Patterns

Spatial access retrieves a complete 2D (or higher-dimensional) spatial slice at a single coordinate along one or more non-spatial dimensions. This is the most commonly encountered pattern in geoscience, remote sensing, and atmospheric modeling, where users need to visualize or analyze a full field at a particular moment in time.

### Characteristics

- **Slice shape:** All spatial dimensions are fully read; non-spatial dimensions are fixed or narrowly sliced.
- **Chunk alignment requirement:** Chunks should be large along spatial dimensions and small (ideally 1) along the dimension being sliced.
- **I/O signature:** Few, large contiguous reads when chunks are aligned; many scattered small reads when they are not.

### Examples Across Domains

**Climate / Weather:**
```python
# Full global temperature field at a single timestep
ds["temperature"].sel(time="2020-06-15")

# Surface pressure map at forecast hour 24
ds["sp"].isel(step=24)
```

**Remote Sensing:**
```python
# Full scene at one timestamp, all bands
ds.sel(time="2021-03-01")

# Single band, single time — pure spatial
ds["B04"].sel(time="2021-03-01")
```

**Radio Astronomy:**
```python
# Visibility grid at one frequency channel and one time integration
ds["visibilities"].sel(frequency=1.4e9, time="2023-01-01T00:00:00")
```

**Genomics (matrix context):**
```python
# All genomic positions for a single sample (row slice)
ds["expression"].sel(sample="SAMPLE_001")
```

### Diagnostic Signals

You are dealing with a spatial pattern when:
- The output is a 2D map or image.
- The user says "snapshot," "frame," "scene," or "map."
- Profiling shows large contiguous reads along lat/lon or x/y axes.
- Most of the dataset's spatial extent is touched per operation.

### Anti-Patterns

- Chunking with large time dimensions and small spatial dimensions forces spatial access to open many chunks and read a sliver from each.
- Using `chunks="auto"` without specifying access patterns often produces balanced chunks that are suboptimal for spatial access.

---

## Temporal Access Patterns

Temporal access retrieves a full time series at a single spatial location or small spatial neighborhood. This pattern dominates station-based analysis, point-level validation, trend detection, and any workflow where the user follows a single location through time.

### Characteristics

- **Slice shape:** The time dimension is fully read; spatial dimensions are fixed or narrowly sliced.
- **Chunk alignment requirement:** Chunks should be large along the time dimension and small along spatial dimensions.
- **I/O signature:** When chunks are aligned, reads are sequential along the time axis. When misaligned, each timestep requires opening a separate chunk.

### Examples Across Domains

**Climate / Weather:**
```python
# Temperature time series at a weather station
ds["temperature"].sel(lat=51.5, lon=-0.1, method="nearest")

# Monthly mean precipitation at a point
ds["precip"].sel(lat=35.0, lon=-106.0, method="nearest").resample(time="1M").mean()
```

**Oceanography:**
```python
# Sea surface temperature at a mooring location
ds["sst"].sel(lat=0.0, lon=-140.0, method="nearest")

# Mixed layer depth time series
ds["mld"].sel(lat=-60.0, lon=30.0, method="nearest")
```

**Remote Sensing:**
```python
# NDVI time series at a field site
ndvi = (ds["B08"] - ds["B04"]) / (ds["B08"] + ds["B04"])
ndvi.sel(x=500000, y=4500000, method="nearest")
```

**Radio Astronomy:**
```python
# Amplitude vs. time for a single baseline and frequency (light curve)
ds["visibilities"].sel(baseline="ANT1-ANT2", frequency=1.4e9)
```

### Diagnostic Signals

You are dealing with a temporal pattern when:
- The output is a line plot with time on the x-axis.
- The user says "trend," "time series," "historical," or "evolution."
- Operations include `.resample()`, `.rolling()`, `.groupby("time.year")`.
- Only a handful of spatial points are accessed per operation.

### Anti-Patterns

- Chunking with small time dimensions (e.g., one chunk per file in a daily file archive) forces temporal access to open thousands of chunks.
- Large spatial chunks waste bandwidth when only a single pixel is needed per chunk.

---

## Spectral/Frequency Access Patterns

Spectral access retrieves data across a frequency, wavelength, channel, or band dimension at a fixed point in other dimensions. This pattern is central to radio astronomy, hyperspectral remote sensing, and any domain with a dense spectral axis.

### Characteristics

- **Slice shape:** The spectral dimension is fully read; spatial and temporal dimensions are fixed.
- **Chunk alignment requirement:** Chunks should be large along the spectral/frequency dimension and small along other dimensions.
- **I/O signature:** Sequential reads along the spectral axis when aligned; scattered reads across many chunks when not.

### Examples Across Domains

**Radio Astronomy:**
```python
# Full spectrum at one baseline and one time integration
ds["visibilities"].sel(baseline="ANT1-ANT2", time="2023-01-01T00:00:00")

# Bandpass calibration — full frequency range per antenna
ds["gains"].sel(antenna="ANT1")
```

**Hyperspectral Remote Sensing:**
```python
# Full spectral signature at one pixel
ds.sel(x=500000, y=4500000, method="nearest")

# Spectral angle mapping requires all bands at each pixel
ds.sel(x=slice(499000, 501000), y=slice(4499000, 4501000))
```

**Atmospheric Chemistry:**
```python
# Absorption spectrum at a single altitude and location
ds["absorption"].sel(lat=45.0, lon=-90.0, altitude=10.0)
```

### Diagnostic Signals

You are dealing with a spectral pattern when:
- The output is a spectrum plot (intensity vs. frequency/wavelength).
- The user says "spectrum," "bandpass," "channels," or "spectral signature."
- Operations iterate or aggregate across the frequency/band dimension.
- The spectral dimension is large (hundreds to millions of channels).

### Anti-Patterns

- Chunking that splits the spectral axis into many small pieces forces spectral access to reassemble data from numerous chunks.
- Ignoring spectral patterns in radio astronomy datasets almost guarantees poor calibration performance.

---

## Diagonal/Mixed Access Patterns

Diagonal access retrieves subsets across multiple dimensions simultaneously -- neither a full spatial slice nor a full temporal series, but a partial read along two or more axes. This pattern appears in regional time series analysis, spatiotemporal subsetting, and any workflow that applies bounding boxes in multiple dimensions at once.

### Characteristics

- **Slice shape:** Multiple dimensions are partially sliced (none fully read, none fully fixed).
- **Chunk alignment requirement:** No single chunk shape perfectly serves diagonal access. Compromise or sharding strategies are required.
- **I/O signature:** Reads touch a moderate number of chunks, reading a moderate fraction of each.

### Examples Across Domains

**Climate Science:**
```python
# Regional monthly mean — subsets both space and time
ds["temperature"].sel(
    lat=slice(30, 50),
    lon=slice(-100, -80),
    time=slice("2010", "2020")
).mean(dim=["lat", "lon"]).resample(time="1M").mean()
```

**Remote Sensing:**
```python
# Tile-level time series for change detection
ds.sel(
    x=slice(499000, 501000),
    y=slice(4499000, 4501000),
    time=slice("2019", "2021")
)
```

**Oceanography:**
```python
# Transect through ocean — partial lat, full depth, single time
ds["temperature"].sel(
    lat=slice(-60, 60),
    lon=-30.0,
    time="2020-01-15"
)
```

### Diagnostic Signals

You are dealing with a diagonal pattern when:
- The user specifies bounding boxes or ranges in two or more dimensions.
- The output is a reduced-dimension aggregate (e.g., regional mean time series).
- Operations combine `.sel()` with slices on multiple dimensions.
- Neither dimension is fully traversed.

### Optimization Strategies

- Use chunk sizes that balance across the involved dimensions rather than maximizing one.
- Consider sharding (Zarr v3) with outer shards aligned to the dominant dimension and inner chunks balanced.
- For regularly repeated diagonal patterns, precompute and cache the result.

---

## Identifying Dominant Patterns

Most datasets serve multiple access patterns, but one or two patterns typically account for the majority of reads. Identifying the dominant pattern is essential because chunk shape optimization yields the largest gains when aligned with the most frequent access.

### Usage Frequency Analysis

Quantify how often each pattern occurs. Methods include:

1. **Log analysis.** If the data is served through a web API or object storage with access logging, parse logs to count requests by access shape.
2. **User interviews.** Ask each user or user group to estimate how many times per day/week they execute each type of query. Use the questionnaire in `assets/workflow-questionnaire.md`.
3. **Code review.** Scan analysis scripts and notebooks for `.sel()`, `.isel()`, `.mean()`, and `.groupby()` calls. Categorize each by pattern type.
4. **Dask dashboard.** Monitor task graphs during typical workloads. Spatial access produces wide, shallow graphs; temporal access produces narrow, deep graphs.

### Profiling Approaches

**Manual profiling:**
```python
import time

# Time spatial access
start = time.time()
ds["var"].sel(time="2020-01-01").load()
spatial_time = time.time() - start

# Time temporal access
start = time.time()
ds["var"].sel(lat=45.0, lon=-90.0).load()
temporal_time = time.time() - start
```

**Automated profiling with cachey or zarr diagnostics:**
- Count the number of chunks read per operation.
- Measure bytes read vs. bytes used (read amplification).
- High read amplification indicates chunk misalignment with the access pattern.

### Building a Pattern Profile

Summarize findings in a pattern profile table:

| Pattern | Frequency (ops/day) | Users | Avg Data Volume | Read Amplification | Weight |
|---------|---------------------|-------|-----------------|-------------------|--------|
| Spatial | 200 | 15 | 50 MB | 1.2x | 0.55 |
| Temporal | 80 | 8 | 5 MB | 8.5x | 0.30 |
| Diagonal | 20 | 3 | 20 MB | 3.0x | 0.15 |

High read amplification on a frequent pattern is the strongest signal that chunk layout needs to change.

---

## Pattern Conflict Resolution

Two access patterns conflict when the optimal chunk shape for one is the worst-case shape for the other. The most common conflict is spatial vs. temporal: spatial access wants `(1, large, large)` chunks and temporal access wants `(large, 1, 1)` chunks.

### Resolution Strategies

**1. Weight and accept the tradeoff.**
If one pattern is far more frequent, optimize for it and accept slower performance on the other. Document the decision and the expected impact.

**2. Compromise chunking.**
Choose a balanced chunk shape like `(100, 64, 64)` that is acceptable for both patterns. Neither will be optimal, but neither will be catastrophically slow. This works when patterns are roughly equally weighted.

**3. Sharding (Zarr v3).**
Use shards aligned with the dominant pattern and inner chunks aligned with the secondary pattern. For example, shards of `(1, 512, 512)` with inner chunks of `(1, 64, 64)` optimize for spatial access while keeping inner chunk boundaries useful for partial spatial reads.

**4. Dual-store approach.**
Maintain two copies of the dataset chunked differently. Route queries to the appropriate store based on detected access pattern. This doubles storage cost but eliminates the conflict entirely.

**5. Virtual references (Kerchunk / VirtualiZarr).**
Store data once with one physical chunk layout. Create virtual reference files that present the data as if it were chunked differently. Useful when one pattern is read-heavy and the other is analysis-heavy.

### Decision Framework

```
Is one pattern >3x more frequent than all others?
  YES → Optimize for dominant pattern, accept penalty on others.
  NO  → Are patterns roughly equal (within 2x)?
    YES → Use compromise chunking or sharding.
    NO  → Consider dual-store if storage budget allows.
```

### Documenting Conflict Decisions

Record every conflict resolution decision in the pattern definitions file. Include:
- Which patterns conflict.
- What weights were assigned.
- Which resolution strategy was chosen and why.
- Expected performance impact on each pattern.
- Conditions under which the decision should be revisited.

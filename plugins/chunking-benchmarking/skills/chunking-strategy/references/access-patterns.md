# Access Patterns for Multi-Dimensional Zarr Data — Deep Reference

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| Pattern 1: Spatial Access | 18–42 | Reading complete spatial slices at a single time step |
| Pattern 2: Time-Series Access | 43–64 | Reading all time steps at a single spatial location |
| Pattern 3: Spectral Access | 65–87 | Reading all frequency values at a fixed spatial-temporal point |
| The Trade-Off Problem | 88–97 | Why optimal chunking for all patterns is mutually exclusive |
| How This Plugin Uses Access Patterns | 98–104 | Workflow from user input to chunking recommendation |
| Domain-Agnostic Design | 105–113 | Applying the framework beyond radio astronomy |

---

**Three access patterns** represent common ways scientists read multi-dimensional data. Understanding these patterns is essential for choosing appropriate chunking strategies.

## Pattern 1: Spatial Access

### Definition
Reading a complete 2D or 3D spatial slice at a **single time step** (or other non-spatial coordinate value).

### Example Operations
```python
# OVRO-LWA radio telescope data (time × frequency × baseline)
ds = xr.open_zarr("s3://bucket/data.zarr")

# Load all frequencies and baselines at time index 42
spatial_slice = ds.sel(time=42).compute()

# Or using isel for positional indexing
spatial_slice = ds.isel(time=42).compute()
```

### Optimal Chunking
- **Small chunks** along the slicing dimension (time)
- **Large chunks** along the loaded dimensions (frequency, baseline)

**Example:** For time×frequency×baseline data, optimal might be `(1, 1024, 512)` — one time step per chunk, but large frequency and baseline chunks.

**Why this works:** Xarray/Zarr only loads chunks that intersect the requested time slice. Small time chunks mean fewer unneeded chunks are loaded. Large frequency/baseline chunks mean fewer HTTP requests to assemble the full spatial extent.

## Pattern 2: Time-Series Access

### Definition
Reading **all time steps** at a single spatial location (or subset of spatial coordinates).

### Example Operations
```python
# Load time series for a specific baseline across all times
time_series = ds.sel(baseline=123).compute()

# Or load multiple baselines
time_series = ds.sel(baseline=[10, 20, 30]).compute()
```

### Optimal Chunking
- **Large chunks** along the slicing dimension (time)
- **Small chunks** along the loaded dimensions (baseline, frequency)

**Example:** For time×frequency×baseline data, optimal might be `(512, 64, 1)` — many time steps per chunk, but small baseline chunks.

**Why this works:** Large time chunks mean each HTTP request retrieves many time steps, reducing total request count. Small baseline chunks mean Zarr doesn't load unneeded baselines when accessing a single location.

## Pattern 3: Spectral Access

### Definition
Reading **all values along the frequency axis** (or similar spectral/wavelength dimension) at a single spatial-temporal location.

### Example Operations
```python
# Load full spectrum at a specific time and baseline
spectrum = ds.sel(time=42, baseline=123).compute()

# Access the frequency dimension
frequencies = spectrum['frequency']
intensities = spectrum['data']
```

### Optimal Chunking
- **Large chunks** along the frequency dimension
- **Small chunks** along time and baseline dimensions

**Example:** For time×frequency×baseline data, optimal might be `(1, 2048, 1)` — maximize frequency chunk size.

**Why this works:** Similar to time-series access, but optimizing for frequency instead of time. Large frequency chunks mean the full spectrum is retrieved with fewer requests.

## The Trade-Off Problem

**Critical insight:** These three patterns have **mutually exclusive** optimal chunking strategies.

- Spatial access wants: small time, large frequency, large baseline
- Time-series access wants: large time, small frequency, small baseline
- Spectral access wants: small time, large frequency, small baseline

You **cannot optimize for all three simultaneously**. Chunking is a trade-off.

## How This Plugin Uses Access Patterns

1. **User specifies workflow:** Which access pattern(s) dominate their analysis?
2. **Benchmark each pattern:** Measure wall time, memory, HTTP requests for each candidate chunking strategy
3. **Analyze trade-offs:** Identify configurations that favor specific patterns or balance across all three
4. **Recommend chunking:** Based on user priorities (optimize for one pattern, or compromise across multiple)

## Domain-Agnostic Design

While the examples above use OVRO-LWA dimensions (time, frequency, baseline), this plugin is **domain-agnostic**:

- Climate data: `time × latitude × longitude` → spatial (maps), time-series (station data)
- Medical imaging: `patient × slice × x × y` → spatial (full scan), patient-series (longitudinal)
- Hyperspectral imagery: `x × y × wavelength` → spatial (images), spectral (material signatures)

Users define their own dimension names and which dimensions are sliced vs loaded for each pattern.

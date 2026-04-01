---
name: zarr-xarray-integration
description: Integrate Zarr with xarray and Dask for labeled, multi-dimensional scientific data workflows. Covers reading and writing Zarr stores with xarray, append and region-write operations, multi-file virtual datasets, Dask chunk alignment with Zarr chunks, encoding configuration, consolidated metadata, and performance optimization for large-scale analysis.
metadata:
  references:
    - references/patterns.md
    - references/examples.md
    - references/common-issues.md
---

# Zarr + xarray Integration

Use **xarray** as the high-level interface for reading, writing, and analyzing Zarr datasets. xarray adds labeled dimensions, coordinates, and metadata to Zarr's chunked array storage, while **Dask** provides parallel and out-of-core computation. This skill covers the full xarray-Zarr workflow: opening stores, writing with encoding, appending data, region writes, chunk alignment, and performance optimization.

**xarray Documentation**: https://docs.xarray.dev/

**Zarr Documentation**: https://zarr.readthedocs.io/

**Dask Documentation**: https://docs.dask.org/

## Quick Reference Card

### Installation & Setup

```bash
# Using pixi (recommended)
pixi add xarray zarr dask numpy netcdf4

# Using pip
pip install xarray[complete] zarr dask[complete]

# For cloud-hosted Zarr stores
pixi add s3fs gcsfs fsspec
pip install zarr[remote]
```

### Essential Operations

```python
import xarray as xr

# ── Read a Zarr store ──
ds = xr.open_zarr("data.zarr")                       # local
ds = xr.open_zarr("s3://bucket/data.zarr")            # S3 (public)
ds = xr.open_zarr("gs://bucket/data.zarr")            # GCS

# ── Read with explicit Dask chunks ──
ds = xr.open_zarr("data.zarr", chunks={"time": 30, "lat": 90, "lon": 180})

# ── Write to Zarr ──
ds.to_zarr("output.zarr")

# ── Write with encoding ──
encoding = {
    "temperature": {"chunks": {"time": 30, "lat": 90, "lon": 180}, "dtype": "float32"},
    "precipitation": {"chunks": {"time": 30, "lat": 90, "lon": 180}, "dtype": "float32"},
}
ds.to_zarr("output.zarr", encoding=encoding)

# ── Append along a dimension ──
ds_new.to_zarr("output.zarr", append_dim="time")

# ── Write to a specific region ──
ds_chunk.to_zarr("output.zarr", region={"time": slice(100, 200)})

# ── Consolidated metadata (faster cloud opens) ──
ds.to_zarr("output.zarr", consolidated=True)
ds = xr.open_zarr("output.zarr", consolidated=True)
```

### Quick Decision Tree

```
Want to read an existing Zarr store?
├── Local path → xr.open_zarr("path.zarr")
├── Cloud URL → xr.open_zarr("s3://...", storage_options={"anon": True})
└── Need specific chunks → add chunks= parameter

Want to write xarray data to Zarr?
├── New store → ds.to_zarr("out.zarr")
├── With compression → ds.to_zarr("out.zarr", encoding={...})
├── Append time steps → ds.to_zarr("out.zarr", append_dim="time")
└── Parallel region writes → ds.to_zarr("out.zarr", region={...})

Performance issues?
├── Slow open → Use consolidated=True
├── Slow compute → Align Dask chunks with Zarr chunks
└── Memory blow-up → Use compute=False or write in regions
```

## When to Use This Skill

Use this skill when:

- Reading Zarr stores into xarray Datasets for analysis
- Writing xarray Datasets or DataArrays to Zarr format
- Appending new data to an existing Zarr store over time
- Writing output from parallel Dask computations to Zarr
- Configuring per-variable compression, dtype, and chunk encoding
- Aligning Dask chunks with Zarr chunks for optimal performance
- Converting between NetCDF and Zarr via xarray
- Working with cloud-hosted Zarr stores through xarray

## Core Concepts

### 1. Reading Zarr with xarray

xarray provides `open_zarr()` as the primary entry point for reading Zarr stores.

```python
import xarray as xr

# ── Basic local read ──
ds = xr.open_zarr("climate_data.zarr")
print(ds)

# ── Cloud read (S3, anonymous) ──
ds = xr.open_zarr(
    "s3://cmip6-pds/CMIP6/CMIP/NOAA-GFDL/GFDL-ESM4/historical/r1i1p1f1/Omon/tos/gn/v20190726/",
    storage_options={"anon": True},
    consolidated=True,
)

# ── With explicit Dask chunks (lazy loading) ──
ds = xr.open_zarr(
    "large_dataset.zarr",
    chunks={"time": 30, "lat": 90, "lon": 180},
)
# Data is NOT loaded — ds.temperature is a Dask array
print(ds["temperature"].data)  # dask.array<...>

# ── Using open_dataset with engine="zarr" (equivalent) ──
ds = xr.open_dataset("data.zarr", engine="zarr", chunks={})
```

**Key parameters for `open_zarr`:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `chunks` | `"auto"` | Dask chunk sizes; `{}` = use Zarr chunks; `None` = load eagerly |
| `consolidated` | `None` | Read consolidated metadata (faster for v2 cloud stores) |
| `storage_options` | `None` | Passed to fsspec (e.g., `{"anon": True}` for public S3) |
| `decode_cf` | `True` | Decode CF conventions (times, units, masks) |
| `decode_times` | `True` | Decode time coordinates |
| `group` | `None` | Open a specific group within the store |

### 2. Writing xarray Datasets to Zarr

```python
import xarray as xr
import numpy as np

# ── Create a sample Dataset ──
ds = xr.Dataset(
    {
        "temperature": (["time", "lat", "lon"], np.random.randn(365, 180, 360).astype("float32")),
        "precipitation": (["time", "lat", "lon"], np.random.rand(365, 180, 360).astype("float32")),
    },
    coords={
        "time": np.arange(365),
        "lat": np.linspace(-89.5, 89.5, 180),
        "lon": np.linspace(0.5, 359.5, 360),
    },
    attrs={"title": "Sample Climate Dataset"},
)

# ── Basic write ──
ds.to_zarr("output.zarr", mode="w")

# ── Write with encoding (recommended) ──
encoding = {
    "temperature": {
        "chunks": {"time": 30, "lat": 90, "lon": 180},
        "dtype": "float32",
        "compressor": None,  # use Zarr default (Zstd for v3)
    },
    "precipitation": {
        "chunks": {"time": 30, "lat": 90, "lon": 180},
        "dtype": "float32",
    },
}
ds.to_zarr("output.zarr", mode="w", encoding=encoding, consolidated=True)

# ── Write to cloud ──
ds.to_zarr(
    "s3://my-bucket/output.zarr",
    storage_options={"key": "...", "secret": "..."},
    mode="w",
)
```

### 3. Appending and Region Writes

Zarr supports two patterns for incrementally adding data: **append** (grow a dimension) and **region** (write to a specific slice).

```python
import xarray as xr
import numpy as np

# ── Append along a dimension ──
# First write: create the store
ds_initial = xr.Dataset({
    "temperature": (["time", "lat", "lon"], np.random.randn(30, 180, 360).astype("float32")),
}, coords={"time": np.arange(30), "lat": np.linspace(-89.5, 89.5, 180), "lon": np.linspace(0.5, 359.5, 360)})
ds_initial.to_zarr("timeseries.zarr", mode="w")

# Subsequent writes: append new time steps
for month in range(1, 12):
    ds_month = xr.Dataset({
        "temperature": (["time", "lat", "lon"], np.random.randn(30, 180, 360).astype("float32")),
    }, coords={"time": np.arange(month * 30, (month + 1) * 30), "lat": np.linspace(-89.5, 89.5, 180), "lon": np.linspace(0.5, 359.5, 360)})
    ds_month.to_zarr("timeseries.zarr", append_dim="time")

# ── Region writes (parallel-safe) ──
# Pre-allocate the full store
ds_full = xr.Dataset({
    "temperature": (["time", "lat", "lon"], np.full((365, 180, 360), np.nan, dtype="float32")),
}, coords={"time": np.arange(365), "lat": np.linspace(-89.5, 89.5, 180), "lon": np.linspace(0.5, 359.5, 360)})
ds_full.to_zarr("parallel_output.zarr", mode="w", compute=False)

# Each worker writes its own region
def write_region(day_start, day_end):
    data = np.random.randn(day_end - day_start, 180, 360).astype("float32")
    ds_chunk = xr.Dataset({
        "temperature": (["time", "lat", "lon"], data),
    }, coords={
        "time": np.arange(day_start, day_end),
        "lat": np.linspace(-89.5, 89.5, 180),
        "lon": np.linspace(0.5, 359.5, 360),
    })
    ds_chunk.to_zarr("parallel_output.zarr", region={"time": slice(day_start, day_end)})

# Safe for concurrent writes from multiple workers
write_region(0, 30)
write_region(30, 60)
```

### 4. Multi-File Virtual Datasets

Combine multiple files into a single virtual Zarr store without copying data.

```python
import xarray as xr

# ── open_mfdataset with Zarr files ──
ds = xr.open_mfdataset(
    ["year_2020.zarr", "year_2021.zarr", "year_2022.zarr"],
    engine="zarr",
    concat_dim="time",
    combine="nested",
    chunks={"time": 365},
)

# ── VirtualiZarr for reference-based access ──
# Creates virtual references to existing files (no data copy)
from virtualizarr import open_virtual_dataset

vds_list = []
for path in ["data_2020.nc", "data_2021.nc", "data_2022.nc"]:
    vds = open_virtual_dataset(path)
    vds_list.append(vds)

combined = xr.concat(vds_list, dim="time")
combined.virtualize.to_zarr("combined_refs.zarr")  # write virtual store
```

### 5. Dask Chunk Alignment

Dask chunks **must** align with Zarr chunks for optimal performance. Misaligned chunks cause redundant reads and wasted memory.

```python
import xarray as xr

# ── Check current Zarr chunk sizes ──
ds = xr.open_zarr("data.zarr", chunks={})  # use Zarr's native chunks
for var in ds.data_vars:
    encoding = ds[var].encoding
    print(f"{var}: Zarr chunks = {encoding.get('chunks')}")
    print(f"{var}: Dask chunks = {ds[var].data.chunksize}")

# ── Align Dask chunks = Zarr chunks (best practice) ──
ds = xr.open_zarr("data.zarr", chunks={})  # empty dict = match Zarr chunks

# ── Use multiples of Zarr chunks ──
# If Zarr chunks are (30, 90, 180), these are aligned:
ds = xr.open_zarr("data.zarr", chunks={"time": 60, "lat": 90, "lon": 360})
# 60 = 2 * 30 ✓, 90 = 1 * 90 ✓, 360 = 2 * 180 ✓

# ── Misaligned chunks (avoid!) ──
# ds = xr.open_zarr("data.zarr", chunks={"time": 45})  # 45 is not a multiple of 30
```

**Alignment rules:**
- Dask chunk size should be an **exact multiple** of the Zarr chunk size along each dimension
- Use `chunks={}` (empty dict) to automatically match Zarr chunks
- If you must use larger Dask chunks, ensure they are multiples: `dask_chunk = N * zarr_chunk`

### 6. Encoding Configuration

The `encoding` dict controls how each variable is stored in Zarr.

```python
encoding = {
    "temperature": {
        "chunks": {"time": 30, "lat": 90, "lon": 180},  # Zarr chunk sizes
        "dtype": "float32",                                # on-disk dtype
        "compressor": None,                                # use default (Zstd)
        "_FillValue": -9999.0,                             # fill value
    },
    "time": {
        "chunks": {"time": 365},
        "dtype": "int64",
    },
}
ds.to_zarr("encoded.zarr", encoding=encoding)
```

**Common encoding fields:**

| Field | Purpose |
|-------|---------|
| `chunks` | Zarr chunk sizes (dict or tuple) |
| `dtype` | On-disk data type |
| `compressor` | Compression codec (numcodecs object or None) |
| `_FillValue` | Fill value for missing data |
| `scale_factor` / `add_offset` | CF packing parameters |

### 7. Performance Optimization

```python
import xarray as xr

# ── Use consolidated metadata for fast cloud opens ──
ds.to_zarr("s3://bucket/data.zarr", consolidated=True)
ds = xr.open_zarr("s3://bucket/data.zarr", consolidated=True)

# ── Avoid loading data unnecessarily ──
# compute=False writes only metadata (for pre-allocation)
ds.to_zarr("preallocated.zarr", compute=False)

# ── Use Dask for parallel writes ──
ds_lazy = xr.open_zarr("input.zarr", chunks={"time": 30})
result = ds_lazy["temperature"].mean(dim="time")
result.to_dataset(name="temp_mean").to_zarr("mean_output.zarr")

# ── Rechunk before writing if needed ──
ds_rechunked = ds_lazy.chunk({"time": 365, "lat": 45, "lon": 45})
ds_rechunked.to_zarr("rechunked.zarr")
```

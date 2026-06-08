---
name: xarray-for-multidimensional-data
description: Use when the user asks about Xarray, xarray datasets, NetCDF files, multidimensional labeled arrays, or scientific/climate data analysis in Python. Work with labeled multidimensional arrays for scientific data analysis using Xarray. Covers NetCDF/HDF5/Zarr I/O, Dask integration for large datasets, DataTree, and geospatial raster operations with rioxarray.
metadata:
  references:
    - references/common-issues.md
    - references/examples.md
    - references/patterns.md
---

# Xarray for Multidimensional Data

## Quick Reference Card

### Installation
```bash
pixi add xarray netcdf4 dask zarr h5netcdf   # core
pixi add rioxarray xesmf                       # geospatial
```

### Essential Operations
```python
import xarray as xr
import numpy as np
import pandas as pd

# DataArray: single labeled N-D array
da = xr.DataArray(
    data=np.random.randn(365, 10, 20),
    dims=["time", "lat", "lon"],
    coords={"time": pd.date_range("2024-01-01", periods=365),
            "lat": np.linspace(-90, 90, 10),
            "lon": np.linspace(-180, 180, 20)},
    attrs={"units": "Celsius"}
)

# Dataset: dict of DataArrays sharing dimensions
ds = xr.Dataset({"temperature": da,
                 "precipitation": (["time", "lat", "lon"],
                                   np.random.rand(365, 10, 20))})

# Selection
ds.sel(time="2024-01-15")                        # by label
ds.sel(lat=40.5, method="nearest")               # nearest
ds.sel(time=slice("2024-01", "2024-03"))         # range
ds.isel(time=0)                                  # by position
ds.where(ds["temperature"] > 20, drop=True)      # conditional

# Aggregation
ds.mean(dim="time")
ds.groupby("time.month").mean()
ds.resample(time="1ME").mean()                   # monthly resample
ds.rolling(time=7, center=True).mean()

# I/O
ds.to_netcdf("data.nc")
ds = xr.open_dataset("data.nc", chunks={"time": 100})   # lazy + Dask
ds.to_zarr("data.zarr")
ds = xr.open_zarr("data.zarr")
ds = xr.open_mfdataset("data_*.nc", combine="by_coords") # multi-file
```

### Module / Tool Decision Tree
```
Need to...
├─ Work with labeled N-D arrays        → xarray (DataArray / Dataset)
├─ Organize hierarchical data          → xr.DataTree
├─ Handle data > memory                → chunks= + Dask
├─ Read/write NetCDF or HDF5           → xr.open_dataset / .to_netcdf
├─ Read/write Zarr (cloud-friendly)    → xr.open_zarr / .to_zarr
├─ Geospatial rasters + CRS            → rioxarray (.rio accessor)
└─ Regrid between grids                → xESMF
```

---

## Patterns and Reference

| Topic | patterns.md section |
|-------|---------------------|
| Creating DataArrays / Datasets | Pattern 1 |
| NetCDF, Zarr, CSV I/O | Pattern 2 |
| Selection and indexing (.sel, .isel, .where) | Pattern 3 |
| Computation, groupby, rolling, resample | Pattern 4 |
| Combining datasets (concat, merge, align) | Pattern 5 |
| Dask integration (chunking, parallelism) | Pattern 6 |
| Interpolation and regridding | Pattern 7 |
| Custom functions with apply_ufunc | Pattern 8 |
| DataTree (hierarchical data) | Pattern 9 |
| Geospatial operations with rioxarray | Pattern 10 |

Non-obvious gotchas:
- **Lazy loading**: `xr.open_dataset` with `chunks=` returns a Dask-backed Dataset — no data is read until `.compute()` or `.load()` is called. Forgetting `.compute()` means you're passing a graph, not values.
- **Area-weighted mean**: `ds.mean(dim=["lat", "lon"])` gives equal weight to every cell regardless of size. For correct global averages use `ds.weighted(np.cos(np.deg2rad(ds.lat))).mean(["lat", "lon"])`.
- **Chunking direction matters**: chunk along the dimension you're *not* reducing (e.g., chunk by space when doing time reductions, chunk by time when doing spatial reductions) to minimise cross-chunk communication.
- **rioxarray CRS must be set before reprojecting**: if the source file lacks an embedded CRS, call `da.rio.write_crs("EPSG:XXXX")` before `da.rio.reproject()` or you'll get a `CRSError`.
- **DataTree coordinate inheritance**: child node dimensions must align with inherited parent coordinates — a length mismatch raises an error at construction time, not at computation time.
- **Time coordinate precision**: floating-point coordinate values (e.g. lat=40.7128) rarely match exactly — always use `method="nearest"` or `tolerance=` with `.sel()` for continuous coordinates.

See `references/common-issues.md` for full error messages and fixes.  
See `references/examples.md` for seven complete worked examples (climate analysis, satellite NDVI, oceanography, ensemble analysis, time-series decomposition, DataTree ensemble, rioxarray Landsat pipeline).

---

## Workflow: Loading and Processing a Large Dataset with Dask

```python
import xarray as xr
import numpy as np

# ── Step 1: Open lazily ──────────────────────────────────────────────────────
ds = xr.open_mfdataset(
    "climate_*.nc",
    combine="by_coords",
    chunks={"time": 365, "lat": 90, "lon": 90},  # ~100 MB chunks
)

# Checkpoint 1: inspect without loading
print(ds)                        # shows Dask arrays, not values
print(ds.dims, ds.data_vars)
assert "temperature" in ds.data_vars, "Expected variable missing"

# ── Step 2: Subset to region / time of interest ───────────────────────────────
ds_sub = ds.sel(
    time=slice("1990-01-01", "2020-12-31"),
    lat=slice(-60, 60),          # tropics + mid-latitudes
)

# Checkpoint 2: verify subset is reasonable
print(f"Subset shape: {ds_sub['temperature'].shape}")
assert ds_sub.sizes["time"] > 0, "Time slice returned nothing — check dates"

# ── Step 3: Compute area-weighted global mean ─────────────────────────────────
weights = np.cos(np.deg2rad(ds_sub.lat))
weights.name = "weights"
global_mean = (
    ds_sub["temperature"]
    .weighted(weights)
    .mean(dim=["lat", "lon"])
)  # still lazy

# ── Step 4: Trigger computation ───────────────────────────────────────────────
result = global_mean.compute()   # or .load() to keep as DataArray

# Checkpoint 3: sanity-check output
assert result.notnull().all(), "NaNs in output — check masking or fill values"
print(f"Global mean range: {float(result.min()):.2f} to {float(result.max()):.2f} °C")

# ── Step 5: Save ──────────────────────────────────────────────────────────────
result.to_netcdf("global_mean_temperature.nc")
```

---

## Workflow: Reproject and Save a Geospatial Raster with rioxarray

```python
import xarray as xr
import rioxarray          # registers .rio accessor

# ── Step 1: Open raster ───────────────────────────────────────────────────────
da = rioxarray.open_rasterio("satellite_image.tif", masked=True)

# Checkpoint 1: confirm CRS is present
if da.rio.crs is None:
    raise ValueError("No CRS found — set it with da.rio.write_crs('EPSG:XXXX')")
print(f"Source CRS: {da.rio.crs}")
print(f"Bounds: {da.rio.bounds()}, Resolution: {da.rio.resolution()}")

# ── Step 2: Clip to area of interest ─────────────────────────────────────────
da_clipped = da.rio.clip_box(minx=-122.5, miny=37.5, maxx=-121.5, maxy=38.5,
                              crs="EPSG:4326")

# Checkpoint 2: clipped data should be non-empty
assert da_clipped.size > 0, "Clip returned empty array — check bounding box vs CRS"
print(f"Clipped shape: {da_clipped.shape}")

# ── Step 3: Reproject ─────────────────────────────────────────────────────────
TARGET_CRS = "EPSG:3857"
da_reprojected = da_clipped.rio.reproject(TARGET_CRS)

# Checkpoint 3: verify CRS changed
assert str(da_reprojected.rio.crs) != str(da_clipped.rio.crs), \
    "CRS unchanged after reproject"
print(f"Target CRS: {da_reprojected.rio.crs}")

# ── Step 4: Save ──────────────────────────────────────────────────────────────
da_reprojected.rio.to_raster("output_3857.tif", compress="lzw")
print("Saved output_3857.tif")
```

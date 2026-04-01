# Zarr + xarray Integration Patterns

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| Pattern 1: Reading a Cloud-Hosted Zarr Store with xarray | 14–70 | Open remote Zarr data with lazy Dask-backed arrays |
| Pattern 2: Writing with Per-Variable Encoding | 71–145 | Configure chunks, dtype, and compression per variable |
| Pattern 3: Appending Time Steps to an Existing Zarr Store | 146–220 | Grow a dataset incrementally along the time dimension |
| Pattern 4: Region Writes for Parallel Output | 221–305 | Pre-allocate and write slices from concurrent workers |
| Pattern 5: Aligning Dask Chunks with Zarr Chunks | 306–375 | Ensure Dask computation chunks match on-disk layout |
| Pattern 6: Consolidated Metadata for Fast Cloud Opens | 376–430 | Speed up initial open of large cloud-hosted stores |

---

## Pattern 1: Reading a Cloud-Hosted Zarr Store with xarray

**Description:** Open a Zarr store on S3 or GCS as a lazy, Dask-backed xarray Dataset. No data is downloaded until computation is triggered.

**When to use:**
- Exploring large cloud-hosted scientific datasets
- Running analysis on subsets without downloading the full store
- Working with CMIP6, ERA5, or other analysis-ready cloud data

**Code example:**

```python
import xarray as xr

# ── Open a public CMIP6 dataset on S3 ──
ds = xr.open_zarr(
    "s3://cmip6-pds/CMIP6/CMIP/NOAA-GFDL/GFDL-ESM4/historical/r1i1p1f1/Omon/tos/gn/v20190726/",
    storage_options={"anon": True},
    consolidated=True,
)
print(ds)

# Data is lazy — nothing downloaded yet
print(f"temperature type: {type(ds['tos'].data)}")  # dask.array

# ── Select a subset (only fetches needed chunks) ──
subset = ds["tos"].sel(time="2000", lat=slice(-30, 30))
print(f"Subset shape: {subset.shape}")

# ── Trigger computation (downloads data) ──
mean_sst = subset.mean(dim=["lat", "lon"]).compute()
print(f"Tropical mean SST: {mean_sst.values}")

# ── With explicit Dask chunks ──
ds = xr.open_zarr(
    "s3://cmip6-pds/...",
    storage_options={"anon": True},
    chunks={"time": 120, "lat": 90, "lon": 180},
)
```

---

## Pattern 2: Writing with Per-Variable Encoding

**Description:** Write an xarray Dataset to Zarr with customized encoding for each variable — controlling chunk sizes, data types, compression, and fill values.

**When to use:**
- Writing production datasets where storage efficiency matters
- Different variables need different chunk layouts (e.g., time-heavy vs space-heavy access)
- Downcasting float64 to float32 for 50% storage savings

**Code example:**

```python
import xarray as xr
import numpy as np

# ── Create a multi-variable Dataset ──
ds = xr.Dataset(
    {
        "temperature": (["time", "lat", "lon"], np.random.randn(365, 180, 360).astype("float64")),
        "precipitation": (["time", "lat", "lon"], np.random.rand(365, 180, 360).astype("float64")),
        "elevation": (["lat", "lon"], np.random.rand(180, 360).astype("float64")),
    },
    coords={
        "time": xr.cftime_range("2024-01-01", periods=365, freq="D"),
        "lat": np.linspace(-89.5, 89.5, 180),
        "lon": np.linspace(0.5, 359.5, 360),
    },
)

# ── Define per-variable encoding ──
encoding = {
    "temperature": {
        "chunks": {"time": 30, "lat": 90, "lon": 180},
        "dtype": "float32",       # downcast to save space
        "_FillValue": -9999.0,
    },
    "precipitation": {
        "chunks": {"time": 30, "lat": 90, "lon": 180},
        "dtype": "float32",
        "_FillValue": -9999.0,
    },
    "elevation": {
        "chunks": {"lat": 180, "lon": 360},  # single chunk (static field)
        "dtype": "float32",
    },
}

# ── Write ──
ds.to_zarr("encoded_dataset.zarr", mode="w", encoding=encoding, consolidated=True)

# ── Verify encoding was applied ──
ds_check = xr.open_zarr("encoded_dataset.zarr")
print(f"temperature dtype on disk: {ds_check['temperature'].encoding['dtype']}")
print(f"temperature chunks: {ds_check['temperature'].encoding['chunks']}")
```

---

## Pattern 3: Appending Time Steps to an Existing Zarr Store

**Description:** Incrementally grow a Zarr store by appending new data along the time dimension. This is the standard pattern for operational data pipelines that produce data continuously.

**When to use:**
- Daily or hourly data ingestion pipelines
- Streaming sensor data into a growing archive
- Building up a dataset over multiple processing runs

**Code example:**

```python
import xarray as xr
import numpy as np

# ── Initial write (create the store) ──
coords = {
    "lat": np.linspace(-89.5, 89.5, 180),
    "lon": np.linspace(0.5, 359.5, 360),
}

ds_jan = xr.Dataset(
    {"temperature": (["time", "lat", "lon"], np.random.randn(31, 180, 360).astype("float32"))},
    coords={"time": xr.cftime_range("2024-01-01", periods=31, freq="D"), **coords},
)
encoding = {"temperature": {"chunks": {"time": 31, "lat": 90, "lon": 180}}}
ds_jan.to_zarr("growing_dataset.zarr", mode="w", encoding=encoding)

# ── Append February ──
ds_feb = xr.Dataset(
    {"temperature": (["time", "lat", "lon"], np.random.randn(29, 180, 360).astype("float32"))},
    coords={"time": xr.cftime_range("2024-02-01", periods=29, freq="D"), **coords},
)
ds_feb.to_zarr("growing_dataset.zarr", append_dim="time")

# ── Append March ──
ds_mar = xr.Dataset(
    {"temperature": (["time", "lat", "lon"], np.random.randn(31, 180, 360).astype("float32"))},
    coords={"time": xr.cftime_range("2024-03-01", periods=31, freq="D"), **coords},
)
ds_mar.to_zarr("growing_dataset.zarr", append_dim="time")

# ── Verify ──
ds_all = xr.open_zarr("growing_dataset.zarr")
print(f"Total time steps: {len(ds_all.time)}")  # 31 + 29 + 31 = 91
print(f"Time range: {ds_all.time.values[0]} to {ds_all.time.values[-1]}")
```

---

## Pattern 4: Region Writes for Parallel Output

**Description:** Pre-allocate a Zarr store and then write to specific regions (slices) from multiple parallel workers. This avoids the append-dimension coordination problem and is safe for concurrent writes when regions do not overlap.

**When to use:**
- Parallel processing where each worker produces a spatial or temporal tile
- Dask-based workflows writing output without `to_zarr(compute=True)`
- HPC batch jobs where each node processes a different region

**Code example:**

```python
import xarray as xr
import numpy as np

# ── Step 1: Pre-allocate the full store (metadata only) ──
n_time, n_lat, n_lon = 365, 180, 360
ds_template = xr.Dataset(
    {
        "temperature": (["time", "lat", "lon"],
                        np.full((n_time, n_lat, n_lon), np.nan, dtype="float32")),
    },
    coords={
        "time": xr.cftime_range("2024-01-01", periods=n_time, freq="D"),
        "lat": np.linspace(-89.5, 89.5, n_lat),
        "lon": np.linspace(0.5, 359.5, n_lon),
    },
)
encoding = {"temperature": {"chunks": {"time": 30, "lat": 90, "lon": 180}}}
ds_template.to_zarr("parallel_output.zarr", mode="w", encoding=encoding, compute=False)

# ── Step 2: Each worker writes its region ──
def process_and_write(time_start, time_end):
    """Simulate a worker that processes and writes a time slice."""
    n_t = time_end - time_start
    data = np.random.randn(n_t, n_lat, n_lon).astype("float32")
    ds_region = xr.Dataset(
        {"temperature": (["time", "lat", "lon"], data)},
        coords={
            "time": xr.cftime_range("2024-01-01", periods=n_time, freq="D")[time_start:time_end],
            "lat": np.linspace(-89.5, 89.5, n_lat),
            "lon": np.linspace(0.5, 359.5, n_lon),
        },
    )
    ds_region.to_zarr(
        "parallel_output.zarr",
        region={"time": slice(time_start, time_end)},
    )

# These can run concurrently (non-overlapping regions)
process_and_write(0, 90)
process_and_write(90, 180)
process_and_write(180, 270)
process_and_write(270, 365)

# ── Step 3: Verify ──
ds = xr.open_zarr("parallel_output.zarr")
print(f"NaN count: {ds['temperature'].isnull().sum().compute().values}")
```

---

## Pattern 5: Aligning Dask Chunks with Zarr Chunks

**Description:** Ensure that Dask computation chunks are exact multiples of Zarr on-disk chunks. Misalignment forces Zarr to read extra chunks and discard unused data, degrading performance.

**When to use:**
- Before any Dask computation on a Zarr-backed Dataset
- When writing Dask results back to Zarr
- Diagnosing unexpectedly slow reads or high memory usage

**Code example:**

```python
import xarray as xr

# ── Inspect Zarr chunk layout ──
ds = xr.open_zarr("data.zarr", chunks={})
for var in ds.data_vars:
    zarr_chunks = ds[var].encoding.get("chunks")
    dask_chunks = ds[var].data.chunksize if hasattr(ds[var].data, "chunksize") else "eager"
    print(f"{var}: zarr_chunks={zarr_chunks}, dask_chunks={dask_chunks}")

# ── Use chunks={} to auto-match Zarr chunks (recommended default) ──
ds = xr.open_zarr("data.zarr", chunks={})

# ── Use exact multiples when you need larger Dask chunks ──
# Zarr chunks: (30, 90, 180)
ds = xr.open_zarr("data.zarr", chunks={"time": 60, "lat": 180, "lon": 360})
# 60 = 2×30 ✓   180 = 2×90 ✓   360 = 2×180 ✓

# ── Rechunk a Dask array to align before writing ──
ds_misaligned = xr.open_zarr("data.zarr", chunks={"time": 45})  # bad: 45 % 30 != 0
ds_aligned = ds_misaligned.chunk({"time": 30})  # fix alignment
ds_aligned.to_zarr("output.zarr")

# ── Diagnostic: check if chunks are aligned ──
def check_alignment(ds):
    for var in ds.data_vars:
        zarr_chunks = ds[var].encoding.get("chunks")
        if zarr_chunks is None:
            continue
        dask_chunks = ds[var].data.chunksize
        for dim_idx, (dc, zc) in enumerate(zip(dask_chunks, zarr_chunks)):
            if dc % zc != 0:
                dim_name = ds[var].dims[dim_idx]
                print(f"⚠ {var}.{dim_name}: Dask chunk {dc} not aligned with Zarr chunk {zc}")
            else:
                dim_name = ds[var].dims[dim_idx]
                print(f"✓ {var}.{dim_name}: {dc} = {dc // zc}×{zc}")

check_alignment(ds)
```

---

## Pattern 6: Consolidated Metadata for Fast Cloud Opens

**Description:** Write and read consolidated metadata so that opening a large cloud-hosted Zarr store requires a single HTTP request for all metadata instead of one request per array.

**When to use:**
- Writing Zarr v2 stores to cloud storage
- Stores with many variables or deeply nested groups
- Any cloud-hosted store that will be opened frequently

**Code example:**

```python
import xarray as xr
import zarr

# ── Write with consolidated metadata ──
ds.to_zarr("s3://bucket/data.zarr", consolidated=True, mode="w")

# ── Consolidate an existing store ──
zarr.consolidate_metadata("s3://bucket/data.zarr")

# ── Read with consolidated metadata (fast open) ──
ds = xr.open_zarr("s3://bucket/data.zarr", consolidated=True)

# ── IMPORTANT: Re-consolidate after appends ──
ds_new.to_zarr("s3://bucket/data.zarr", append_dim="time")
zarr.consolidate_metadata("s3://bucket/data.zarr")  # must re-consolidate!

# ── Check if a store has consolidated metadata ──
import json
import fsspec
fs = fsspec.filesystem("s3", anon=True)
has_consolidated = fs.exists("s3://bucket/data.zarr/.zmetadata")
print(f"Consolidated metadata: {has_consolidated}")
```

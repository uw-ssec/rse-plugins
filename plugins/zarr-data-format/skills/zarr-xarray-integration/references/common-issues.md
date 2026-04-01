# Common Issues and Solutions

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| Issue 1: Chunk Size Mismatch Between Dask and Zarr | 18–80 | Silent performance degradation from misaligned chunks |
| Issue 2: Conflicting Sizes When Appending | 81–140 | ValueError from shape or coordinate mismatches on append |
| Issue 3: Encoding Not Applied | 141–200 | Compression or dtype settings ignored during write |
| Issue 4: Memory Blow-Up on to_zarr | 201–260 | OOM when writing large Dask-backed Datasets |
| Issue 5: Consolidated Metadata Stale After Append | 261–315 | Old metadata causes missing or incorrect data after appends |
| Issue 6: Coordinate Variables Written as Data Variables | 316–370 | Coordinates appear in data_vars instead of coords after roundtrip |
| Issue 7: dtype Mismatch Between In-Memory and On-Disk | 371–430 | Unexpected type promotion or precision loss |

---

## Issue 1: Chunk Size Mismatch Between Dask and Zarr

**Symptoms:**
- Reads are much slower than expected
- Dask task graph has many more tasks than expected
- Memory usage per worker is higher than the chunk size suggests
- Profile shows time spent in "rechunking" or redundant reads

**Cause:** Dask chunks are not aligned with Zarr chunks. For example, if Zarr chunks are `(30, 90, 180)` and Dask chunks are `(45, 90, 180)`, each Dask task must read two Zarr chunks (0–30 and 30–60) and discard the unused portion.

**Solution:**

```python
import xarray as xr

# ── Diagnose: Check alignment ──
ds = xr.open_zarr("data.zarr", chunks={"time": 45})
for var in ds.data_vars:
    zarr_c = ds[var].encoding.get("chunks", "unknown")
    dask_c = ds[var].data.chunksize
    print(f"{var}: zarr={zarr_c}, dask={dask_c}")

# ── Fix 1: Use chunks={} to auto-match Zarr layout ──
ds = xr.open_zarr("data.zarr", chunks={})

# ── Fix 2: Use exact multiples ──
# Zarr chunks = (30, 90, 180)
ds = xr.open_zarr("data.zarr", chunks={"time": 60, "lat": 90, "lon": 360})

# ── Fix 3: Rechunk before computation ──
ds = xr.open_zarr("data.zarr", chunks={"time": 45})
ds = ds.chunk({"time": 30})  # realign to Zarr chunks
```

---

## Issue 2: Conflicting Sizes When Appending

**Symptoms:**
- `ValueError: conflicting sizes for dimension 'lat': length X on the data but length Y on variable 'lat'`
- `ValueError: variable 'temperature' already exists with different shape`

**Cause:** The new data being appended has different non-append dimensions than the existing store, or coordinate values don't match along non-append dimensions.

**Solution:**

```python
import xarray as xr
import numpy as np

# ── Diagnose: Compare shapes ──
ds_existing = xr.open_zarr("timeseries.zarr")
print(f"Existing dims: {dict(ds_existing.dims)}")
print(f"Existing lat: {ds_existing.lat.values[:3]}...")

# ── Fix 1: Ensure non-append dimensions match exactly ──
ds_new = xr.Dataset(
    {"temperature": (["time", "lat", "lon"], new_data)},
    coords={
        "time": new_times,
        "lat": ds_existing.lat.values,  # reuse exact coordinates
        "lon": ds_existing.lon.values,
    },
)
ds_new.to_zarr("timeseries.zarr", append_dim="time")

# ── Fix 2: Ensure variables match ──
# The new dataset must have the same data variables
print(f"Existing vars: {list(ds_existing.data_vars)}")
# Do not include extra variables in the append

# ── Fix 3: Check dtypes match ──
for var in ds_existing.data_vars:
    print(f"{var}: existing={ds_existing[var].dtype}, new={ds_new[var].dtype}")
```

---

## Issue 3: Encoding Not Applied

**Symptoms:**
- On-disk dtype is float64 despite specifying float32 in encoding
- Chunks on disk differ from what was specified
- Compression ratio is lower than expected
- `encoding` dict keys don't match variable names

**Cause:** Common mistakes: (1) encoding dict keys don't match Dataset variable names exactly; (2) using `chunks` as a tuple instead of a dict; (3) encoding parameter passed to the wrong function.

**Solution:**

```python
import xarray as xr

# ── Diagnose: Check what encoding was actually applied ──
ds = xr.open_zarr("output.zarr")
for var in ds.data_vars:
    print(f"{var}: {ds[var].encoding}")

# ── Fix 1: Ensure encoding keys match variable names ──
print(f"Dataset variables: {list(ds.data_vars)}")
# encoding keys must be in this list

encoding = {
    "temperature": {"chunks": {"time": 30, "lat": 90, "lon": 180}, "dtype": "float32"},
    # ✗ "temp" would be silently ignored if the variable is named "temperature"
}

# ── Fix 2: Use dict for chunks (not tuple) in xarray ──
encoding = {
    "temperature": {
        "chunks": {"time": 30, "lat": 90, "lon": 180},  # ✓ dict
        # "chunks": (30, 90, 180),  # also works but less clear
    },
}

# ── Fix 3: Pass encoding to to_zarr, not to_netcdf ──
ds.to_zarr("output.zarr", encoding=encoding)  # ✓
```

---

## Issue 4: Memory Blow-Up on to_zarr

**Symptoms:**
- `MemoryError` or OOM kill when calling `ds.to_zarr()`
- System memory fills up rapidly during write
- Dask dashboard shows all tasks being executed simultaneously

**Cause:** If the Dataset is backed by Dask arrays and the Dask scheduler tries to materialize too many chunks in memory at once. This commonly happens with the default threaded scheduler on a machine with limited RAM.

**Solution:**

```python
import xarray as xr

# ── Fix 1: Use the distributed scheduler with memory limits ──
from dask.distributed import Client
client = Client(memory_limit="4GB")  # per worker
ds.to_zarr("output.zarr")

# ── Fix 2: Write in stages using region writes ──
ds_template = ds.isel(time=slice(0, 1)).broadcast_like(ds)
ds_template.to_zarr("output.zarr", compute=False)

chunk_size = 30
for start in range(0, len(ds.time), chunk_size):
    end = min(start + chunk_size, len(ds.time))
    ds.isel(time=slice(start, end)).to_zarr(
        "output.zarr", region={"time": slice(start, end)}
    )

# ── Fix 3: Rechunk to smaller pieces before writing ──
ds_small_chunks = ds.chunk({"time": 10, "lat": 45, "lon": 90})
ds_small_chunks.to_zarr("output.zarr")
```

---

## Issue 5: Consolidated Metadata Stale After Append

**Symptoms:**
- After appending data, `xr.open_zarr(..., consolidated=True)` shows old shape
- New time steps are missing from the opened Dataset
- `KeyError` on new variables added after consolidation

**Cause:** `consolidated=True` reads metadata from a single `.zmetadata` file that was written at consolidation time. Appending data updates the actual chunk metadata but does not update `.zmetadata`.

**Solution:**

```python
import xarray as xr
import zarr

# ── Fix: Re-consolidate after every append ──
ds_new.to_zarr("data.zarr", append_dim="time")
zarr.consolidate_metadata("data.zarr")  # update .zmetadata

# ── Or: Read without consolidated metadata ──
ds = xr.open_zarr("data.zarr", consolidated=False)

# ── Best practice: consolidate in the write pipeline ──
def append_and_consolidate(ds_new, store_path, append_dim="time"):
    ds_new.to_zarr(store_path, append_dim=append_dim)
    zarr.consolidate_metadata(store_path)
```

---

## Issue 6: Coordinate Variables Written as Data Variables

**Symptoms:**
- After writing to Zarr and reading back, coordinates appear in `ds.data_vars` instead of `ds.coords`
- `ds.lat` raises `KeyError` but `ds["lat"]` works
- CF-compliant coordinate metadata is lost

**Cause:** xarray determines coordinate vs. data variable status from the `coordinates` encoding attribute or from dimension coordinates. If this metadata is lost during the Zarr roundtrip, variables may be reclassified.

**Solution:**

```python
import xarray as xr

# ── Diagnose ──
ds = xr.open_zarr("data.zarr")
print(f"Coords: {list(ds.coords)}")
print(f"Data vars: {list(ds.data_vars)}")

# ── Fix 1: Set coordinates explicitly when writing ──
ds = ds.set_coords(["lat", "lon", "time"])
ds.to_zarr("data.zarr", mode="w")

# ── Fix 2: Use the coordinates encoding attribute ──
ds.to_zarr("data.zarr", mode="w")
# xarray should preserve this automatically, but verify:
ds_check = xr.open_zarr("data.zarr")
assert "lat" in ds_check.coords

# ── Fix 3: Restore coordinates on read ──
ds = xr.open_zarr("data.zarr")
ds = ds.set_coords(["lat", "lon"])
```

---

## Issue 7: dtype Mismatch Between In-Memory and On-Disk

**Symptoms:**
- Values are slightly different after writing and reading back
- Float precision loss (float64 → float32 silently)
- Integer overflow for large values
- `_FillValue` comparisons fail due to type mismatch

**Cause:** The encoding dict specifies a different dtype than the in-memory array, causing implicit casting. Or, xarray's CF decoding converts types during read.

**Solution:**

```python
import xarray as xr
import numpy as np

# ── Diagnose: Compare in-memory vs on-disk dtypes ──
ds = xr.open_zarr("data.zarr")
for var in ds.data_vars:
    mem_dtype = ds[var].dtype
    disk_dtype = ds[var].encoding.get("dtype", "unknown")
    print(f"{var}: memory={mem_dtype}, disk={disk_dtype}")

# ── Fix 1: Explicit dtype in encoding ──
encoding = {
    "temperature": {"dtype": "float32"},  # intentional downcast
    "count": {"dtype": "int32"},
}
ds.to_zarr("output.zarr", encoding=encoding)

# ── Fix 2: Cast before writing to avoid surprises ──
ds["temperature"] = ds["temperature"].astype("float32")
ds.to_zarr("output.zarr")

# ── Fix 3: Disable CF decoding if it causes type changes ──
ds = xr.open_zarr("data.zarr", decode_cf=False)

# ── Fix 4: Match fill values to the on-disk dtype ──
encoding = {
    "temperature": {
        "dtype": "float32",
        "_FillValue": np.float32(-9999.0),  # match dtype
    },
}
```

---
name: data-migration
description: Migrates data between formats with a focus on converting HDF5 and NetCDF datasets to Zarr. Covers xarray-based conversion, direct zarr.copy operations, VirtualiZarr for reference-based virtual Zarr stores, kerchunk for legacy workflows, validation strategies, and batch migration pipelines. Use when the user asks about converting HDF5 or NetCDF files to Zarr, migrating scientific datasets, or working with VirtualiZarr or kerchunk for virtual stores.
metadata:
  references:
    - references/patterns.md
    - references/examples.md
    - references/common-issues.md
---

# Data Migration to Zarr

Migrate HDF5, NetCDF, and other formats to Zarr using xarray, h5py, VirtualiZarr, or kerchunk.

## Resources

| Resource | Purpose |
|----------|---------|
| [references/patterns.md](references/patterns.md) | Full patterns: single-file, multi-file, virtual refs, incremental batch, post-migration validation |
| [references/examples.md](references/examples.md) | Real-world migration examples |
| [references/common-issues.md](references/common-issues.md) | HDF5 features unsupported in Zarr, metadata loss, memory errors, fill-value mismatches |
| [assets/hdf5-to-zarr-migration.py](assets/hdf5-to-zarr-migration.py) | Runnable migration script |

## Strategy Selection

| Strategy | Data Copy | Best For |
|----------|-----------|----------|
| xarray conversion | Full copy | Simple files, rechunking needed, CF metadata |
| h5py + zarr.copy | Full copy | Complex HDF5 group hierarchies |
| VirtualiZarr | No copy | Large archives, cloud-hosted sources |
| kerchunk | No copy | Legacy workflows, existing JSON refs |

```
Migrating to Zarr?
├── Single file, simple structure → xr.open_dataset() → ds.to_zarr()
├── Many files, same structure   → xr.open_mfdataset() → ds.to_zarr()
├── No data copy wanted          → VirtualiZarr (modern) or kerchunk (legacy)
├── Complex HDF5 group hierarchy → h5py + zarr group copy
└── Need rechunking              → xarray with chunks= and encoding=
```

## HDF5 to Zarr

**Step 1 — Open and inspect:**
```python
import xarray as xr
ds = xr.open_dataset("simulation_output.h5", engine="h5netcdf")
print(ds)
```

**Step 2 — Convert with encoding:**
```python
encoding = {var: {"chunks": {"time": 30, "x": 100, "y": 100}} for var in ds.data_vars}
ds.to_zarr("simulation_output.zarr", encoding=encoding, consolidated=True)
```

**Step 3 — Validate:**
```python
ds_zarr = xr.open_zarr("simulation_output.zarr")
xr.testing.assert_allclose(ds, ds_zarr)
print("Validation passed")
```

For complex HDF5 group hierarchies, use h5py recursion — see [patterns.md Pattern 4](references/patterns.md).

## NetCDF to Zarr

**Single file:**
```python
ds = xr.open_dataset("climate_model_output.nc", chunks={"time": 30})
encoding = {
    "temperature":   {"chunks": {"time": 30, "lat": 90, "lon": 180}, "dtype": "float32"},
    "precipitation": {"chunks": {"time": 30, "lat": 90, "lon": 180}, "dtype": "float32"},
}
ds.to_zarr("climate_output.zarr", encoding=encoding, consolidated=True)
# Validate
ds_zarr = xr.open_zarr("climate_output.zarr")
assert dict(ds.dims) == dict(ds_zarr.dims), "Dimension mismatch"
xr.testing.assert_allclose(ds, ds_zarr)
```

**Multiple NetCDFs → single store:**
```python
from pathlib import Path
ds = xr.open_mfdataset(sorted(Path("netcdf_archive/").glob("*.nc")),
                       combine="nested", concat_dim="time", chunks={"time": 30})
ds.to_zarr("combined_archive.zarr", encoding=encoding, consolidated=True)
```

See [patterns.md Pattern 5](references/patterns.md) for incremental migration with checkpointing for large archives.

## VirtualiZarr (No Data Copy)

```python
from virtualizarr import open_virtual_dataset
import xarray as xr
from pathlib import Path

# Single file
vds = open_virtual_dataset("large_data.nc")

# Multiple files
vds_list = [open_virtual_dataset(str(p)) for p in sorted(Path("archive/").glob("*.nc"))]
combined = xr.concat(vds_list, dim="time")

# Write virtual store (only references, no data copy)
combined.virtualize.to_zarr("virtual_archive.zarr")

# Read back normally
ds = xr.open_zarr("virtual_archive.zarr")
```

Note: reads resolve to the original source files — keep source files accessible.

## Kerchunk (Legacy)

```python
import json
from kerchunk.hdf import SingleHdf5ToZarr
from kerchunk.combine import MultiZarrToZarr
import fsspec

# Scan each file
url = "s3://bucket/file_001.nc"
with fsspec.open(url, mode="rb", anon=True) as f:
    refs = SingleHdf5ToZarr(f, url).translate()
with open("refs_001.json", "w") as f:
    json.dump(refs, f)

# Combine reference files
refs_list = [json.load(open(rf)) for rf in ["refs_001.json", "refs_002.json"]]
combined_refs = MultiZarrToZarr(refs_list, concat_dims=["time"]).translate()
with open("combined_refs.json", "w") as f:
    json.dump(combined_refs, f)

# Open virtual dataset
mapper = fsspec.get_mapper("reference://", fo="combined_refs.json")
ds = xr.open_zarr(mapper)
```

## Validation

Run after every migration before deleting the source:

```python
import xarray as xr
import numpy as np

def validate_migration(source_path, zarr_path, engine="netcdf4"):
    ds_src = xr.open_dataset(source_path, engine=engine)
    ds_dst = xr.open_zarr(zarr_path)
    errors = []
    if dict(ds_src.dims) != dict(ds_dst.dims):
        errors.append(f"Dims: {dict(ds_src.dims)} vs {dict(ds_dst.dims)}")
    missing = set(ds_src.data_vars) - set(ds_dst.data_vars)
    if missing:
        errors.append(f"Missing variables: {missing}")
    for var in set(ds_src.data_vars) & set(ds_dst.data_vars):
        src, dst = ds_src[var].values, ds_dst[var].values
        if not np.allclose(src.astype(dst.dtype), dst, equal_nan=True, rtol=1e-5):
            errors.append(f"{var}: max diff = {np.nanmax(np.abs(src.astype(dst.dtype) - dst))}")
    if errors:
        for e in errors: print(f"  ✗ {e}")
        return False
    print("Validation passed")
    return True
```

If validation fails: check encoding dtype mismatches → see [common-issues.md](references/common-issues.md).

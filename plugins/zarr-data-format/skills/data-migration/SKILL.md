---
name: data-migration
description: Migrate data between formats with a focus on converting HDF5 and NetCDF datasets to Zarr. Covers xarray-based conversion, direct zarr.copy operations, VirtualiZarr for reference-based virtual Zarr stores, kerchunk for legacy workflows, validation strategies, and batch migration pipelines.
metadata:
  references:
    - references/patterns.md
    - references/examples.md
    - references/common-issues.md
---

# Data Migration to Zarr

Migrate existing datasets from **HDF5**, **NetCDF**, and other formats to **Zarr**. This skill covers the full spectrum of migration approaches: **xarray-based conversion** for labeled scientific data, **direct copy operations** for group-level migration, **VirtualiZarr** for creating virtual Zarr stores without copying data, and **kerchunk** for legacy reference-based workflows. You will also learn validation strategies to ensure data integrity after migration.

**Zarr Documentation**: https://zarr.readthedocs.io/

**xarray Documentation**: https://docs.xarray.dev/

**VirtualiZarr Documentation**: https://virtualizarr.readthedocs.io/

**kerchunk Documentation**: https://fsspec.github.io/kerchunk/

**h5py Documentation**: https://docs.h5py.org/

## Quick Reference Card

### Installation & Setup

```bash
# Core tools
pixi add zarr xarray h5py netcdf4 numpy

# Using pip
pip install zarr xarray h5py netCDF4

# VirtualiZarr (virtual references)
pip install virtualizarr

# kerchunk (legacy reference approach)
pip install kerchunk

# For cloud sources
pip install fsspec s3fs gcsfs
```

### Essential Operations

```python
import xarray as xr

# ── NetCDF to Zarr (simplest path) ──
ds = xr.open_dataset("input.nc")
ds.to_zarr("output.zarr")

# ── HDF5 to Zarr via xarray ──
ds = xr.open_dataset("input.h5", engine="h5netcdf")
ds.to_zarr("output.zarr")

# ── Multiple NetCDFs to single Zarr ──
ds = xr.open_mfdataset("data_*.nc", chunks={"time": 30})
ds.to_zarr("combined.zarr", encoding={...})

# ── VirtualiZarr (no data copy) ──
from virtualizarr import open_virtual_dataset
vds = open_virtual_dataset("input.nc")
vds.virtualize.to_zarr("virtual_output.zarr")

# ── Validate migration ──
ds_src = xr.open_dataset("input.nc")
ds_dst = xr.open_zarr("output.zarr")
xr.testing.assert_allclose(ds_src, ds_dst)
```

### Quick Decision Tree

```
Migrating data to Zarr?
├── Single file, simple structure?
│   └── xr.open_dataset() → ds.to_zarr()
├── Many files, same structure?
│   └── xr.open_mfdataset() → ds.to_zarr()
├── Don't want to copy data?
│   ├── Modern approach → VirtualiZarr
│   └── Legacy approach → kerchunk
├── Complex HDF5 groups/hierarchies?
│   └── h5py + zarr.copy_store or manual group iteration
├── Need to rechunk during migration?
│   └── xarray with chunks= and encoding=
└── Need validation?
    └── xr.testing.assert_allclose() + shape/dtype checks
```

## When to Use This Skill

Use this skill when:

- Converting HDF5 files to Zarr for cloud storage
- Migrating NetCDF archives to Zarr for faster access
- Creating virtual Zarr references for existing files (no data copy)
- Combining many small files into a single consolidated Zarr store
- Rechunking data during format conversion
- Validating that migrated data matches the original source
- Building automated migration pipelines for large archives

## Core Concepts

### 1. Migration Strategy Overview

| Strategy | Data Copy | Speed | Storage Cost | Best For |
|----------|-----------|-------|-------------|----------|
| **xarray conversion** | Full copy | Medium | 2× during migration | Simple files, rechunking needed |
| **zarr.copy_store** | Full copy | Fast | 2× during migration | Preserving exact HDF5 group structure |
| **VirtualiZarr** | No copy | Very fast | Minimal (refs only) | Large archives, cloud-hosted sources |
| **kerchunk** | No copy | Fast | Minimal (JSON refs) | Legacy workflows, existing JSON refs |

**Decision factors:**
- **Need rechunking?** → xarray conversion (can specify new chunks)
- **Need to keep source files?** → VirtualiZarr (references, no copy)
- **Migrating to cloud?** → Full copy (eliminates dependency on source)
- **One-time vs ongoing?** → Full copy for one-time; virtual for growing archives

### 2. HDF5 to Zarr

**Via xarray (recommended for scientific data):**

```python
import xarray as xr

# ── Single HDF5 file ──
ds = xr.open_dataset("simulation_output.h5", engine="h5netcdf")
print(ds)

# Write to Zarr with optimized chunks
encoding = {var: {"chunks": {"time": 30, "x": 100, "y": 100}} for var in ds.data_vars}
ds.to_zarr("simulation_output.zarr", encoding=encoding)

# ── HDF5 with groups ──
# xarray reads one group at a time
ds_group1 = xr.open_dataset("data.h5", group="experiment/run_001")
ds_group1.to_zarr("data.zarr", group="experiment/run_001")
```

**Via h5py + zarr (for complex hierarchies):**

```python
import h5py
import zarr
import numpy as np

# ── Copy entire HDF5 structure to Zarr ──
with h5py.File("complex_data.h5", "r") as h5f:
    root = zarr.open_group("complex_data.zarr", mode="w")

    def copy_group(h5_group, zarr_group):
        # Copy attributes
        zarr_group.attrs.update(dict(h5_group.attrs))

        for key in h5_group:
            item = h5_group[key]
            if isinstance(item, h5py.Group):
                zg = zarr_group.create_group(key)
                copy_group(item, zg)
            elif isinstance(item, h5py.Dataset):
                chunks = item.chunks or item.shape
                zarr_group.create_array(
                    key,
                    data=item[:],
                    chunks=chunks,
                    dtype=item.dtype,
                )
                zarr_group[key].attrs.update(dict(item.attrs))

    copy_group(h5f, root)
```

### 3. NetCDF to Zarr

```python
import xarray as xr

# ── Single NetCDF file ──
ds = xr.open_dataset("climate_model_output.nc", chunks={"time": 30})
encoding = {
    "temperature": {"chunks": {"time": 30, "lat": 90, "lon": 180}, "dtype": "float32"},
    "precipitation": {"chunks": {"time": 30, "lat": 90, "lon": 180}, "dtype": "float32"},
}
ds.to_zarr("climate_output.zarr", encoding=encoding, consolidated=True)

# ── Multiple NetCDF files → single Zarr store ──
ds = xr.open_mfdataset(
    sorted(Path("netcdf_archive/").glob("*.nc")),
    combine="nested",
    concat_dim="time",
    chunks={"time": 30},
)
ds.to_zarr("combined_archive.zarr", encoding=encoding, consolidated=True)

# ── Preserving CF metadata ──
# xarray automatically preserves CF attributes (units, long_name, etc.)
# Verify after conversion:
ds_zarr = xr.open_zarr("climate_output.zarr")
for var in ds_zarr.data_vars:
    print(f"{var}: units={ds_zarr[var].attrs.get('units', 'N/A')}")
```

### 4. VirtualiZarr

VirtualiZarr creates a Zarr store that contains only **references** (byte offsets) pointing to data in the original files. No data is copied — reads go directly to the source files.

```python
from virtualizarr import open_virtual_dataset
import xarray as xr

# ── Create virtual references for a single file ──
vds = open_virtual_dataset("large_data.nc")
print(vds)

# ── Combine multiple files into a virtual dataset ──
vds_list = []
for path in sorted(Path("archive/").glob("*.nc")):
    vds = open_virtual_dataset(str(path))
    vds_list.append(vds)

combined = xr.concat(vds_list, dim="time")

# ── Write virtual Zarr store (only writes references, not data) ──
combined.virtualize.to_zarr("virtual_archive.zarr")

# ── Read the virtual store like a normal Zarr store ──
ds = xr.open_zarr("virtual_archive.zarr")
print(f"Shape: {dict(ds.dims)}")
# Data reads go to the original .nc files

# ── Write virtual references to Icechunk (versioned) ──
from icechunk import IcechunkStore, StorageConfig
storage = StorageConfig.s3_from_env(bucket="my-bucket", prefix="virtual.zarr")
store = IcechunkStore.open_or_create(storage=storage, mode="w")
combined.virtualize.to_zarr(store)
store.commit("Virtual references from NetCDF archive")
```

### 5. Kerchunk (Legacy)

Kerchunk scans existing files and produces JSON reference files that allow Zarr to read the original data without copying.

```python
import json
from kerchunk.hdf import SingleHdf5ToZarr
from kerchunk.combine import MultiZarrToZarr
import fsspec

# ── Scan a single HDF5/NetCDF file ──
url = "s3://noaa-data/file_001.nc"
with fsspec.open(url, mode="rb", anon=True) as f:
    refs = SingleHdf5ToZarr(f, url).translate()

# Save references to JSON
with open("refs_001.json", "w") as f:
    json.dump(refs, f)

# ── Combine multiple reference files ──
ref_files = ["refs_001.json", "refs_002.json", "refs_003.json"]
refs_list = []
for rf in ref_files:
    with open(rf) as f:
        refs_list.append(json.load(f))

combined_refs = MultiZarrToZarr(
    refs_list,
    concat_dims=["time"],
).translate()

with open("combined_refs.json", "w") as f:
    json.dump(combined_refs, f)

# ── Open the virtual dataset ──
import xarray as xr
mapper = fsspec.get_mapper("reference://", fo="combined_refs.json")
ds = xr.open_zarr(mapper)
```

### 6. Validation

Always validate after migration to ensure data integrity.

```python
import xarray as xr
import numpy as np

def validate_migration(source_path, zarr_path, engine="netcdf4"):
    """Compare source dataset with migrated Zarr store."""
    ds_src = xr.open_dataset(source_path, engine=engine)
    ds_dst = xr.open_zarr(zarr_path)

    errors = []

    # Check dimensions
    if dict(ds_src.dims) != dict(ds_dst.dims):
        errors.append(f"Dimension mismatch: {dict(ds_src.dims)} vs {dict(ds_dst.dims)}")

    # Check variables
    src_vars = set(ds_src.data_vars)
    dst_vars = set(ds_dst.data_vars)
    if src_vars != dst_vars:
        errors.append(f"Variable mismatch: missing={src_vars - dst_vars}, extra={dst_vars - src_vars}")

    # Check values
    for var in src_vars & dst_vars:
        src_data = ds_src[var].values
        dst_data = ds_dst[var].values
        if src_data.dtype != dst_data.dtype:
            # Allow float64 → float32 if encoding was applied
            src_data = src_data.astype(dst_data.dtype)
        if not np.allclose(src_data, dst_data, equal_nan=True, rtol=1e-5):
            max_diff = np.nanmax(np.abs(src_data - dst_data))
            errors.append(f"{var}: max difference = {max_diff}")

    # Check attributes
    for var in src_vars & dst_vars:
        for attr in ds_src[var].attrs:
            if attr not in ds_dst[var].attrs:
                errors.append(f"{var}: missing attribute '{attr}'")

    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  ✗ {e}")
    else:
        print("VALIDATION PASSED: source and target match")

    return len(errors) == 0
```

### 7. Batch Migration Pipelines

```python
import xarray as xr
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def batch_migrate(
    source_dir: str,
    zarr_path: str,
    pattern: str = "*.nc",
    concat_dim: str = "time",
    encoding: dict | None = None,
):
    """Migrate a directory of NetCDF files to a single Zarr store."""
    source_files = sorted(Path(source_dir).glob(pattern))
    if not source_files:
        raise FileNotFoundError(f"No files matching {pattern} in {source_dir}")

    logger.info(f"Found {len(source_files)} files to migrate")

    # Open all files lazily
    ds = xr.open_mfdataset(
        source_files,
        combine="nested",
        concat_dim=concat_dim,
        chunks={concat_dim: "auto"},
    )
    logger.info(f"Combined dataset: {dict(ds.dims)}")

    # Write to Zarr
    ds.to_zarr(zarr_path, mode="w", encoding=encoding, consolidated=True)
    logger.info(f"Wrote to {zarr_path}")

    # Validate
    ds_zarr = xr.open_zarr(zarr_path)
    assert dict(ds.dims) == dict(ds_zarr.dims), "Dimension mismatch!"
    logger.info("Validation passed")

    return ds_zarr
```

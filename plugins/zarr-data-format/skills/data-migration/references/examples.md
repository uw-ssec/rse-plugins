# Real-World Examples

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| Example 1: Migrating a Climate Model Archive | 14–110 | Convert a directory of monthly NetCDF files to a single Zarr store |
| Example 2: Virtual Zarr References for NASA Earthdata HDF5 | 111–200 | Create virtual references for cloud-hosted HDF5 files |
| Example 3: HDF5 Instrument Data to Cloud Zarr with Rechunking | 201–300 | Migrate and rechunk instrument data for cloud-optimized access |
| Example 4: Validating a Large Migration | 301–390 | Comprehensive source-vs-target validation pipeline |

---

## Example 1: Migrating a Climate Model Archive

**Dataset description:** A 10-year climate model simulation stored as 120 monthly NetCDF files, each containing daily temperature, precipitation, and wind speed on a 180×360 grid.

**Problem:** The many-small-files format is slow to open and expensive on cloud storage. You need to combine everything into a single consolidated Zarr store with cloud-optimized chunks.

**Code:**

```python
import xarray as xr
import numpy as np
from pathlib import Path

# ── Create synthetic monthly NetCDF files (simulating the archive) ──
archive_dir = Path("climate_archive")
archive_dir.mkdir(exist_ok=True)

rng = np.random.default_rng(42)
months_per_year = 12
years = range(2010, 2020)
days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

for year in years:
    for month in range(1, 13):
        n_days = days_in_month[month - 1]
        ds = xr.Dataset(
            {
                "temperature": (["time", "lat", "lon"],
                    rng.normal(15.0, 10.0, (n_days, 180, 360)).astype("float32")),
                "precipitation": (["time", "lat", "lon"],
                    rng.exponential(2.0, (n_days, 180, 360)).astype("float32")),
            },
            coords={
                "time": xr.cftime_range(f"{year}-{month:02d}-01", periods=n_days, freq="D"),
                "lat": np.linspace(-89.5, 89.5, 180),
                "lon": np.linspace(0.5, 359.5, 360),
            },
        )
        ds.to_netcdf(archive_dir / f"{year}-{month:02d}.nc")

print(f"Created {len(list(archive_dir.glob('*.nc')))} NetCDF files")

# ── Combine and migrate to Zarr ──
files = sorted(archive_dir.glob("*.nc"))
ds_combined = xr.open_mfdataset(
    files,
    combine="nested",
    concat_dim="time",
    chunks={"time": 31, "lat": 90, "lon": 180},
    parallel=True,
)
print(f"Combined: {dict(ds_combined.dims)}")
print(f"Total size: {ds_combined.nbytes / 1e9:.1f} GB")

# ── Write with optimized encoding ──
encoding = {
    "temperature": {"chunks": {"time": 30, "lat": 90, "lon": 180}, "dtype": "float32"},
    "precipitation": {"chunks": {"time": 30, "lat": 90, "lon": 180}, "dtype": "float32"},
}
ds_combined.to_zarr(
    "climate_10yr.zarr",
    mode="w",
    encoding=encoding,
    consolidated=True,
)

# ── Verify ──
ds_zarr = xr.open_zarr("climate_10yr.zarr", consolidated=True)
print(f"Zarr store: {len(ds_zarr.time)} time steps")
print(f"Time range: {ds_zarr.time.values[0]} to {ds_zarr.time.values[-1]}")
print(f"Variables: {list(ds_zarr.data_vars)}")
```

---

## Example 2: Virtual Zarr References for NASA Earthdata HDF5

**Dataset description:** A collection of HDF5 files from NASA's Earthdata archive (e.g., MODIS Level 2 products) stored on S3. Each granule is ~100 MB and there are thousands of granules.

**Problem:** Copying all granules to Zarr would require terabytes of storage and days of transfer time. Instead, create virtual Zarr references that point to the original HDF5 files, enabling Zarr-compatible reads without any data copying.

**Code:**

```python
from virtualizarr import open_virtual_dataset
import xarray as xr
import fsspec

# ── List source files (example: MODIS granules on S3) ──
# In practice, use earthaccess or CMR API to discover files
source_files = [
    "s3://podaac-data/MODIS/L2/2024/001/granule_001.h5",
    "s3://podaac-data/MODIS/L2/2024/001/granule_002.h5",
    "s3://podaac-data/MODIS/L2/2024/001/granule_003.h5",
]

# ── Create virtual references for each granule ──
vds_list = []
for i, url in enumerate(source_files):
    vds = open_virtual_dataset(
        url,
        reader_options={"storage_options": {"anon": False}},
    )
    vds_list.append(vds)
    print(f"[{i+1}/{len(source_files)}] Scanned: {url.split('/')[-1]}")

# ── Combine into a single virtual dataset ──
# For swath data, combine along the "along_track" or "scanline" dimension
combined = xr.concat(vds_list, dim="scanline")
print(f"Virtual dataset: {dict(combined.dims)}")

# ── Write virtual Zarr store ──
combined.virtualize.to_zarr("modis_virtual.zarr")
print("Virtual store created (no data copied)")

# ── Use it like a normal Zarr store ──
ds = xr.open_zarr("modis_virtual.zarr")
print(f"Available variables: {list(ds.data_vars)}")

# Reads go directly to the original HDF5 files on S3
subset = ds["radiance"].sel(scanline=slice(0, 100)).compute()
print(f"Loaded subset: {subset.shape}")
```

---

## Example 3: HDF5 Instrument Data to Cloud Zarr with Rechunking

**Dataset description:** A 50 GB HDF5 file from a high-energy physics detector with deeply nested groups, multiple resolution levels, and time-series data chunked for sequential write during data acquisition.

**Problem:** The original HDF5 chunking (optimized for writing during acquisition) is terrible for analytical reads. You need to rechunk for time-slice access and upload to S3 for shared analysis.

**Code:**

```python
import h5py
import zarr
import numpy as np

# ── Inspect the source HDF5 structure ──
with h5py.File("detector_run_2024.h5", "r") as f:
    def print_tree(group, indent=0):
        for key in group:
            item = group[key]
            prefix = "  " * indent
            if isinstance(item, h5py.Dataset):
                print(f"{prefix}{key}: shape={item.shape}, chunks={item.chunks}, dtype={item.dtype}")
            elif isinstance(item, h5py.Group):
                print(f"{prefix}{key}/")
                print_tree(item, indent + 1)
    print_tree(f)

# ── Migrate with rechunking ──
# Original chunks: (100000, 1) — optimized for appending one channel at a time
# Target chunks: (1000, 256) — optimized for reading time slices across channels
with h5py.File("detector_run_2024.h5", "r") as h5f:
    store = zarr.storage.FsspecStore.from_url("s3://physics-data/detector_2024.zarr")
    root = zarr.open_group(store=store, mode="w")

    # Copy metadata
    root.attrs.update(dict(h5f.attrs))

    # Migrate the main data arrays with new chunk layout
    for group_name in ["detectors", "triggers", "calibration"]:
        if group_name not in h5f:
            continue

        zg = root.create_group(group_name)
        zg.attrs.update(dict(h5f[group_name].attrs))

        for ds_name in h5f[group_name]:
            h5_ds = h5f[group_name][ds_name]
            if not isinstance(h5_ds, h5py.Dataset):
                continue

            # Calculate cloud-optimized chunks (~5 MB per chunk)
            item_size = h5_ds.dtype.itemsize
            target_bytes = 5 * 1024 * 1024  # 5 MB
            if h5_ds.ndim == 2:
                rows_per_chunk = max(1, target_bytes // (h5_ds.shape[1] * item_size))
                new_chunks = (min(rows_per_chunk, h5_ds.shape[0]), h5_ds.shape[1])
            else:
                new_chunks = (min(target_bytes // item_size, h5_ds.shape[0]),)

            # Create the Zarr array
            arr = zg.create_array(
                ds_name,
                shape=h5_ds.shape,
                chunks=new_chunks,
                dtype=h5_ds.dtype,
            )
            arr.attrs.update(dict(h5_ds.attrs))

            # Copy data in chunks to manage memory
            read_chunk = h5_ds.chunks[0] if h5_ds.chunks else h5_ds.shape[0]
            for start in range(0, h5_ds.shape[0], read_chunk):
                end = min(start + read_chunk, h5_ds.shape[0])
                arr[start:end] = h5_ds[start:end]

            print(f"  {group_name}/{ds_name}: {h5_ds.chunks} → {new_chunks}")

print("Migration with rechunking complete")
```

---

## Example 4: Validating a Large Migration

**Dataset description:** A multi-terabyte climate dataset that was migrated from 500 NetCDF files to a single Zarr store. The migration took 8 hours and you need to verify data integrity before deleting the source files.

**Problem:** You cannot load the entire dataset into memory for comparison. Validation must work chunk-by-chunk, reporting any discrepancies with their exact location.

**Code:**

```python
import xarray as xr
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_chunked(source_files, zarr_path, concat_dim="time", rtol=1e-5):
    """Validate a large migration by comparing chunk-by-chunk."""
    ds_zarr = xr.open_zarr(zarr_path, chunks={})
    errors = []
    total_checks = 0

    # Compare each source file against the corresponding slice in Zarr
    time_offset = 0
    for filepath in sorted(source_files):
        ds_src = xr.open_dataset(filepath)
        n_time = len(ds_src[concat_dim])

        for var in ds_src.data_vars:
            if var not in ds_zarr:
                errors.append(f"Missing variable {var} in Zarr store")
                continue

            # Extract the corresponding slice from Zarr
            zarr_slice = ds_zarr[var].isel(
                {concat_dim: slice(time_offset, time_offset + n_time)}
            ).compute()

            src_vals = ds_src[var].values
            zarr_vals = zarr_slice.values

            # Handle dtype differences
            if src_vals.dtype != zarr_vals.dtype:
                src_vals = src_vals.astype(zarr_vals.dtype)

            if not np.allclose(src_vals, zarr_vals, equal_nan=True, rtol=rtol):
                diff = np.abs(src_vals - zarr_vals)
                max_diff = float(np.nanmax(diff))
                max_loc = np.unravel_index(np.nanargmax(diff), diff.shape)
                errors.append(
                    f"{filepath.name}/{var}: max_diff={max_diff:.2e} at {max_loc}"
                )
            total_checks += 1

        time_offset += n_time
        ds_src.close()
        logger.info(f"Validated {filepath.name} (offset={time_offset})")

    # Check total size matches
    expected_time = time_offset
    actual_time = len(ds_zarr[concat_dim])
    if expected_time != actual_time:
        errors.append(f"Time dimension: expected {expected_time}, got {actual_time}")

    ds_zarr.close()

    # Report
    print(f"\n{'='*50}")
    print(f"Validation complete: {total_checks} checks")
    if errors:
        print(f"FAILED with {len(errors)} errors:")
        for e in errors:
            print(f"  - {e}")
    else:
        print("ALL CHECKS PASSED")
    print(f"{'='*50}")

    return len(errors) == 0


# ── Usage ──
# source_files = sorted(Path("netcdf_archive/").glob("*.nc"))
# validate_chunked(source_files, "migrated.zarr")
```

#!/usr/bin/env python3
"""
HDF5 to Zarr Migration Demo
============================

Demonstrates the complete HDF5-to-Zarr migration workflow:
1. Create a sample HDF5 file with h5py
2. Convert to Zarr via xarray
3. Validate the conversion (shape, dtype, values)
4. Print a validation report

Requirements:
    pip install zarr xarray h5py numpy netCDF4
    # or: pixi add zarr xarray h5py numpy netcdf4

Usage:
    python hdf5-to-zarr-migration.py
"""

import shutil
import tempfile
from pathlib import Path

import h5py
import numpy as np
import xarray as xr


def main():
    work_dir = Path(tempfile.mkdtemp(prefix="hdf5_zarr_migration_"))
    h5_path = work_dir / "source_data.h5"
    zarr_path = str(work_dir / "migrated_data.zarr")
    print(f"Working directory: {work_dir}\n")

    # ── 1. Create a sample HDF5 file ──
    print("=" * 60)
    print("1. Create sample HDF5 file")
    print("=" * 60)
    rng = np.random.default_rng(42)
    n_time, n_lat, n_lon = 90, 180, 360

    with h5py.File(h5_path, "w") as f:
        f.attrs["title"] = "Sample Climate Dataset"
        f.attrs["source"] = "Synthetic data for migration demo"

        # Coordinate arrays
        f.create_dataset("time", data=np.arange(n_time, dtype="float64"))
        f["time"].attrs["units"] = "days since 2024-01-01"
        f.create_dataset("lat", data=np.linspace(-89.5, 89.5, n_lat))
        f["lat"].attrs["units"] = "degrees_north"
        f.create_dataset("lon", data=np.linspace(0.5, 359.5, n_lon))
        f["lon"].attrs["units"] = "degrees_east"

        # Data variables
        temp = rng.normal(15.0, 10.0, (n_time, n_lat, n_lon)).astype("float32")
        f.create_dataset("temperature", data=temp, chunks=(30, 90, 180))
        f["temperature"].attrs["units"] = "Celsius"
        f["temperature"].attrs["long_name"] = "Air Temperature"

        precip = rng.exponential(2.0, (n_time, n_lat, n_lon)).astype("float32")
        f.create_dataset("precipitation", data=precip, chunks=(30, 90, 180))
        f["precipitation"].attrs["units"] = "mm/day"
        f["precipitation"].attrs["long_name"] = "Daily Precipitation"

    print(f"  Created: {h5_path}")
    print(f"  Size: {h5_path.stat().st_size / 1e6:.1f} MB")
    print()

    # ── 2. Convert to Zarr via xarray ──
    print("=" * 60)
    print("2. Convert HDF5 to Zarr")
    print("=" * 60)
    ds = xr.open_dataset(h5_path, engine="h5netcdf", chunks={"time": 30})
    print(f"  Source dataset: {dict(ds.dims)}")
    print(f"  Variables: {list(ds.data_vars)}")

    encoding = {
        "temperature": {"chunks": {"time": 30, "lat": 90, "lon": 180}, "dtype": "float32"},
        "precipitation": {"chunks": {"time": 30, "lat": 90, "lon": 180}, "dtype": "float32"},
    }
    ds.to_zarr(zarr_path, mode="w", encoding=encoding)
    print(f"  Wrote Zarr store: {zarr_path}")
    print()

    # ── 3. Validate the conversion ──
    print("=" * 60)
    print("3. Validate migration")
    print("=" * 60)
    ds_zarr = xr.open_zarr(zarr_path)

    checks_passed = 0
    checks_failed = 0

    # Check dimensions
    if dict(ds.dims) == dict(ds_zarr.dims):
        print(f"  PASS: Dimensions match: {dict(ds.dims)}")
        checks_passed += 1
    else:
        print(f"  FAIL: Dimensions differ: {dict(ds.dims)} vs {dict(ds_zarr.dims)}")
        checks_failed += 1

    # Check variables
    if set(ds.data_vars) == set(ds_zarr.data_vars):
        print(f"  PASS: Variables match: {list(ds.data_vars)}")
        checks_passed += 1
    else:
        print(f"  FAIL: Variables differ")
        checks_failed += 1

    # Check values
    for var in ds.data_vars:
        src_vals = ds[var].values
        dst_vals = ds_zarr[var].values
        if np.allclose(src_vals, dst_vals, equal_nan=True, rtol=1e-6):
            print(f"  PASS: {var} values match")
            checks_passed += 1
        else:
            max_diff = np.nanmax(np.abs(src_vals - dst_vals))
            print(f"  FAIL: {var} max difference = {max_diff}")
            checks_failed += 1

    # Check attributes
    for var in ds.data_vars:
        for attr in ["units", "long_name"]:
            if ds[var].attrs.get(attr) == ds_zarr[var].attrs.get(attr):
                print(f"  PASS: {var}.{attr} = '{ds[var].attrs[attr]}'")
                checks_passed += 1
            else:
                print(f"  FAIL: {var}.{attr} differs")
                checks_failed += 1

    print()
    print(f"Results: {checks_passed} passed, {checks_failed} failed")
    print()

    # ── Cleanup ──
    ds.close()
    ds_zarr.close()
    shutil.rmtree(work_dir)
    print(f"Cleaned up {work_dir}")
    print("Done.")


if __name__ == "__main__":
    main()

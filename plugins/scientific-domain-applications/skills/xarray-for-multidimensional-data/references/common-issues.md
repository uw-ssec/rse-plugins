# Common Issues and Solutions

## Issue 1: Memory Errors with Large Datasets

**Problem:** `MemoryError` when loading large NetCDF files.

**Solution:** Use chunking and lazy loading:
```python
# Don't do this
ds = xr.open_dataset("large_file.nc")  # Loads everything

# Do this instead
ds = xr.open_dataset("large_file.nc", chunks={"time": 100})
result = ds.mean(dim="time").compute()  # Lazy evaluation
```

## Issue 2: Misaligned Coordinates

**Problem:** Operations fail due to coordinate mismatch.

**Solution:** Use alignment or reindexing:
```python
# Automatic alignment
result = ds1 + ds2  # Xarray aligns automatically

# Manual alignment with specific join
ds1_aligned, ds2_aligned = xr.align(ds1, ds2, join="inner")

# Reindex to match
ds2_reindexed = ds2.reindex_like(ds1, method="nearest")
```

## Issue 3: Slow Operations on Chunked Data

**Problem:** Operations are slower with Dask than expected.

**Solution:** Optimize chunking strategy:
```python
# Bad: chunks too small
ds = ds.chunk({"time": 1})  # Too much overhead

# Good: reasonable chunk size
ds = ds.chunk({"time": 100})  # Better balance

# Rechunk for specific operation
ds_rechunked = ds.chunk({"time": -1, "lat": 50})  # All time, chunked space
```

## Issue 4: Coordinate Precision Issues

**Problem:** `.sel()` doesn't find exact coordinate values.

**Solution:** Use nearest neighbor or tolerance:
```python
# Fails if exact match not found
ds.sel(lat=40.7128)  # Might fail

# Use nearest neighbor
ds.sel(lat=40.7128, method="nearest")

# Use tolerance
ds.sel(lat=40.7128, method="nearest", tolerance=0.01)
```

## Issue 5: Dimension Order Confusion

**Problem:** Operations produce unexpected results due to dimension order.

**Solution:** Explicitly specify dimensions:
```python
# Ambiguous
result = ds.mean()  # Means over all dimensions

# Clear
result = ds.mean(dim=["lat", "lon"])  # Spatial mean
result = ds.mean(dim="time")  # Temporal mean
```

## Issue 6: Broadcasting Errors

**Problem:** Operations fail with dimension mismatch errors.

**Solution:** Use broadcasting or alignment:
```python
# Error: dimensions don't match
weights = xr.DataArray([1, 2, 3], dims="location")
result = ds * weights  # Fails if ds has different dims

# Solution: broadcast explicitly
weights_broadcast = weights.broadcast_like(ds)
result = ds * weights_broadcast

# Or use align
ds_aligned, weights_aligned = xr.align(ds, weights, join="outer")
```

## Issue 7: Encoding Issues When Saving

**Problem:** Data types or attributes cause errors when saving to NetCDF.

**Solution:** Set encoding explicitly:
```python
# Specify encoding for each variable
encoding = {
    "temperature": {
        "dtype": "float32",
        "zlib": True,
        "complevel": 4,
        "_FillValue": -999.0
    }
}

ds.to_netcdf("data.nc", encoding=encoding)
```

## Issue 8: Time Coordinate Parsing Issues

**Problem:** Time coordinates not recognized or parsed incorrectly.

**Solution:** Use pandas datetime and set calendar:
```python
# Ensure proper datetime format
import pandas as pd

time = pd.date_range("2024-01-01", periods=365, freq="D")
ds = ds.assign_coords(time=time)

# For non-standard calendars (climate models)
import cftime
time_noleap = xr.cftime_range("2024-01-01", periods=365, calendar="noleap")
```


# Real-World Examples

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| Example 1: Processing CMIP6 Climate Data from Cloud Zarr | 14–105 | Read cloud-hosted CMIP6 data, compute regional means with Dask |
| Example 2: Building a Time Series with Incremental Appends | 106–195 | Simulate a daily ingestion pipeline that grows a Zarr store |
| Example 3: Parallel Analysis Pipeline with Dask and Zarr | 196–300 | Distributed computation writing results to Zarr with region writes |
| Example 4: Converting NetCDF Files to a Single Zarr Store | 301–390 | Combine a directory of NetCDF files into one consolidated Zarr store |

---

## Example 1: Processing CMIP6 Climate Data from Cloud Zarr

**Dataset description:** CMIP6 historical sea surface temperature (tos) from the GFDL-ESM4 model, stored as Zarr on AWS S3 as part of the Pangeo CMIP6 cloud collection.

**Problem:** You need to compute the global annual mean SST time series from 1850 to 2014 without downloading the entire dataset (~50 GB). The analysis should use Dask for parallel computation.

**Code:**

```python
import xarray as xr
import numpy as np

# ── Open the cloud-hosted Zarr store ──
ds = xr.open_zarr(
    "s3://cmip6-pds/CMIP6/CMIP/NOAA-GFDL/GFDL-ESM4/historical/r1i1p1f1/Omon/tos/gn/v20190726/",
    storage_options={"anon": True},
    consolidated=True,
    chunks={"time": 120},
)
print(ds)

# ── Inspect the data (lazy — no download yet) ──
tos = ds["tos"]
print(f"Shape: {tos.shape}")
print(f"Dask chunks: {tos.data.chunksize}")
print(f"Size: {tos.nbytes / 1e9:.1f} GB")

# ── Compute area-weighted global mean ──
# Use cosine of latitude as a simple area weight
weights = np.cos(np.deg2rad(ds.lat))
weights = weights / weights.sum()

# Weighted mean over lat/lon (still lazy)
global_mean = tos.weighted(weights).mean(dim=["lat", "lon"])

# Resample to annual means
annual_mean = global_mean.resample(time="YE").mean()

# ── Trigger computation (downloads only needed chunks) ──
result = annual_mean.compute()
print(f"Annual means shape: {result.shape}")
print(f"First 5 years: {result.values[:5]}")

# ── Save result locally ──
result.to_dataset(name="tos_global_annual_mean").to_zarr("cmip6_annual_sst.zarr")
print("Saved annual SST means to cmip6_annual_sst.zarr")
```

---

## Example 2: Building a Time Series with Incremental Appends

**Dataset description:** A synthetic weather station network producing hourly temperature and humidity readings. New data arrives daily and is appended to a growing Zarr store.

**Problem:** Build an operational data pipeline that appends daily batches to an existing Zarr store, handling the initial creation and subsequent appends with the same code path.

**Code:**

```python
import xarray as xr
import numpy as np
from pathlib import Path

# ── Configuration ──
store_path = "station_timeseries.zarr"
n_stations = 100
hours_per_day = 24
rng = np.random.default_rng(42)

# ── Helper: create one day of data ──
def generate_daily_data(date_str, n_stations):
    times = xr.cftime_range(date_str, periods=hours_per_day, freq="h")
    ds = xr.Dataset(
        {
            "temperature": (["time", "station"], rng.normal(20.0, 5.0, (hours_per_day, n_stations)).astype("float32")),
            "humidity": (["time", "station"], rng.uniform(30.0, 95.0, (hours_per_day, n_stations)).astype("float32")),
        },
        coords={
            "time": times,
            "station": [f"STN-{i:04d}" for i in range(n_stations)],
        },
        attrs={"source": "Weather Station Network", "frequency": "hourly"},
    )
    return ds

# ── Ingest pipeline ──
encoding = {
    "temperature": {"chunks": {"time": 24, "station": 100}, "dtype": "float32"},
    "humidity": {"chunks": {"time": 24, "station": 100}, "dtype": "float32"},
}

dates = ["2024-06-01", "2024-06-02", "2024-06-03", "2024-06-04", "2024-06-05"]

for i, date in enumerate(dates):
    ds_day = generate_daily_data(date, n_stations)

    if i == 0:
        # First day: create the store
        ds_day.to_zarr(store_path, mode="w", encoding=encoding)
        print(f"Created store with {date}")
    else:
        # Subsequent days: append
        ds_day.to_zarr(store_path, append_dim="time")
        print(f"Appended {date}")

# ── Verify the complete dataset ──
ds_all = xr.open_zarr(store_path)
print(f"\nFinal dataset:")
print(f"  Time steps: {len(ds_all.time)} (expected {len(dates) * 24})")
print(f"  Stations: {len(ds_all.station)}")
print(f"  Time range: {ds_all.time.values[0]} to {ds_all.time.values[-1]}")
print(f"  Mean temperature: {ds_all['temperature'].mean().compute().values:.1f}°C")
```

---

## Example 3: Parallel Analysis Pipeline with Dask and Zarr

**Dataset description:** A large global ocean temperature dataset (365 days × 720 lat × 1440 lon) stored in Zarr. The analysis computes monthly climatology and anomalies using Dask for parallelism.

**Problem:** Process a dataset that does not fit in memory by using Dask for lazy computation and writing results back to Zarr with region writes for parallel output.

**Code:**

```python
import xarray as xr
import numpy as np
import dask

# ── Create a synthetic large dataset ──
n_time, n_lat, n_lon = 365, 720, 1440
ds = xr.Dataset(
    {
        "sst": (["time", "lat", "lon"],
                dask.array.random.random((n_time, n_lat, n_lon), chunks=(30, 180, 360)).astype("float32")),
    },
    coords={
        "time": xr.cftime_range("2024-01-01", periods=n_time, freq="D"),
        "lat": np.linspace(-89.875, 89.875, n_lat),
        "lon": np.linspace(0.125, 359.875, n_lon),
    },
)
# Write the source dataset
encoding = {"sst": {"chunks": {"time": 30, "lat": 180, "lon": 360}}}
ds.to_zarr("ocean_sst_source.zarr", mode="w", encoding=encoding)

# ── Open with aligned Dask chunks ──
ds = xr.open_zarr("ocean_sst_source.zarr", chunks={})

# ── Compute monthly climatology (lazy) ──
climatology = ds["sst"].groupby("time.month").mean(dim="time")
print(f"Climatology shape: {climatology.shape}")  # (12, 720, 1440)

# ── Compute anomalies (lazy) ──
anomalies = ds["sst"].groupby("time.month") - climatology
print(f"Anomalies shape: {anomalies.shape}")  # (365, 720, 1440)

# ── Write climatology (small, can compute directly) ──
clim_ds = climatology.to_dataset(name="sst_climatology")
clim_ds.to_zarr("ocean_sst_climatology.zarr", mode="w")
print("Wrote climatology")

# ── Write anomalies (large, use Dask-aware to_zarr) ──
anom_ds = anomalies.to_dataset(name="sst_anomaly")
encoding_anom = {"sst_anomaly": {"chunks": {"time": 30, "lat": 180, "lon": 360}}}
anom_ds.to_zarr("ocean_sst_anomalies.zarr", mode="w", encoding=encoding_anom)
print("Wrote anomalies")

# ── Verify ──
ds_anom = xr.open_zarr("ocean_sst_anomalies.zarr")
print(f"Anomaly mean (should be ~0): {ds_anom['sst_anomaly'].mean().compute().values:.6f}")
```

---

## Example 4: Converting NetCDF Files to a Single Zarr Store

**Dataset description:** A directory of monthly NetCDF4 files from a climate model output, each containing one month of daily data for temperature, precipitation, and wind speed.

**Problem:** Combine 12 monthly NetCDF files into a single consolidated Zarr store with optimized chunks for both time-series and spatial access patterns.

**Code:**

```python
import xarray as xr
import numpy as np
from pathlib import Path

# ── Create synthetic monthly NetCDF files ──
output_dir = Path("monthly_netcdf")
output_dir.mkdir(exist_ok=True)

days_per_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
rng = np.random.default_rng(42)

for month, n_days in enumerate(days_per_month, start=1):
    ds = xr.Dataset(
        {
            "temperature": (["time", "lat", "lon"], rng.normal(15.0, 10.0, (n_days, 180, 360)).astype("float32")),
            "precipitation": (["time", "lat", "lon"], rng.exponential(2.0, (n_days, 180, 360)).astype("float32")),
        },
        coords={
            "time": xr.cftime_range(f"2024-{month:02d}-01", periods=n_days, freq="D"),
            "lat": np.linspace(-89.5, 89.5, 180),
            "lon": np.linspace(0.5, 359.5, 360),
        },
        attrs={"source": "Synthetic Climate Model", "month": month},
    )
    ds.to_netcdf(output_dir / f"2024-{month:02d}.nc")
print(f"Created {len(days_per_month)} NetCDF files")

# ── Combine into a single Zarr store ──
# open_mfdataset lazily concatenates all files
ds_combined = xr.open_mfdataset(
    sorted(output_dir.glob("*.nc")),
    combine="nested",
    concat_dim="time",
    chunks={"time": 31, "lat": 90, "lon": 180},
)
print(f"Combined shape: time={len(ds_combined.time)}, lat={len(ds_combined.lat)}, lon={len(ds_combined.lon)}")

# ── Write to Zarr with optimized encoding ──
encoding = {
    "temperature": {"chunks": {"time": 30, "lat": 90, "lon": 180}, "dtype": "float32"},
    "precipitation": {"chunks": {"time": 30, "lat": 90, "lon": 180}, "dtype": "float32"},
}
ds_combined.to_zarr("annual_combined.zarr", mode="w", encoding=encoding, consolidated=True)
print("Wrote combined Zarr store")

# ── Verify ──
ds_zarr = xr.open_zarr("annual_combined.zarr", consolidated=True)
print(f"Zarr store: {len(ds_zarr.time)} time steps")
print(f"  temperature range: [{ds_zarr['temperature'].min().compute().values:.1f}, {ds_zarr['temperature'].max().compute().values:.1f}]")
print(f"  variables: {list(ds_zarr.data_vars)}")
```

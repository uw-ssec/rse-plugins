# Real-World Examples

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| Example 1: Accessing a Public S3 Zarr Dataset | 14–100 | Read CMIP6 climate data from the Pangeo AWS S3 catalog |
| Example 2: Writing a Large Dataset to GCS with obstore | 101–185 | Generate and write a multi-variable dataset to GCS using the Rust-based backend |
| Example 3: Setting Up Icechunk for Versioned Data on S3 | 186–290 | Create a version-controlled dataset with branching and commit history |
| Example 4: Multi-Backend Data Pipeline | 291–380 | Read from S3, process, and write results to Azure Blob |

---

## Example 1: Accessing a Public S3 Zarr Dataset

**Dataset description:** CMIP6 climate model output hosted on AWS S3 as part of the Pangeo CMIP6 cloud data collection. The dataset contains global monthly sea surface temperature (tos) from the GFDL-ESM4 model.

**Problem:** You need to read a cloud-hosted Zarr store, inspect its structure, select a spatial subset, and compute a time-series mean — all without downloading the entire dataset.

**Code:**

```python
import zarr
from zarr.storage import FsspecStore
import numpy as np

# ── Open the store (anonymous access) ──
url = "s3://cmip6-pds/CMIP6/CMIP/NOAA-GFDL/GFDL-ESM4/historical/r1i1p1f1/Omon/tos/gn/v20190726/"
store = FsspecStore.from_url(url, storage_options={"anon": True})
root = zarr.open_group(store=store, mode="r")

# ── Inspect the store ──
print(root.tree())
print()

# ── Read coordinate arrays ──
lat = root["lat"][:]
lon = root["lon"][:]
time = root["time"][:]
print(f"Shape: time={len(time)}, lat={len(lat)}, lon={len(lon)}")

# ── Select a spatial region (North Atlantic: 30-60N, 80-10W) ──
lat_mask = (lat >= 30) & (lat <= 60)
lon_mask = (lon >= 280) & (lon <= 350)  # 280-350E = 80-10W
lat_idx = np.where(lat_mask)[0]
lon_idx = np.where(lon_mask)[0]

# ── Read only the subset (Zarr fetches just the needed chunks) ──
tos = root["tos"]
subset = tos[:, lat_idx[0]:lat_idx[-1]+1, lon_idx[0]:lon_idx[-1]+1]
print(f"Subset shape: {subset.shape}")
print(f"Mean SST: {np.nanmean(subset):.2f} K")

# ── Compute annual means ──
n_years = len(time) // 12
annual_means = []
for yr in range(n_years):
    year_data = subset[yr*12:(yr+1)*12]
    annual_means.append(np.nanmean(year_data))
print(f"First 5 annual means: {annual_means[:5]}")
```

---

## Example 2: Writing a Large Dataset to GCS with obstore

**Dataset description:** A 10 GB synthetic remote sensing dataset with 4 spectral bands at 10 m resolution, written to Google Cloud Storage using the high-performance obstore backend.

**Problem:** You need to write a large, multi-variable Zarr store to GCS with maximum throughput, configuring appropriate chunk sizes for cloud storage.

**Code:**

```python
import zarr
import numpy as np
from obstore.store import GCSStore

# ── Configure the GCS backend ──
obs = GCSStore.from_url(
    "gs://my-research-bucket/sentinel2-mosaic.zarr",
    config={"GOOGLE_SERVICE_ACCOUNT": "/path/to/key.json"},
)
store = zarr.storage.ObjectStore(obs)

# ── Create the root group with metadata ──
root = zarr.open_group(store=store, mode="w")
root.attrs.update({
    "title": "Sentinel-2 Regional Mosaic",
    "spatial_resolution": "10m",
    "crs": "EPSG:32610",
    "date_range": "2024-06-01/2024-08-31",
})

# ── Define array dimensions ──
n_bands = 4
n_y = 10980  # ~110 km at 10m
n_x = 10980
band_names = ["B02_Blue", "B03_Green", "B04_Red", "B08_NIR"]

# ── Chunk size: ~5 MB per chunk (good for cloud I/O) ──
# 512 * 512 * 2 bytes (uint16) = 512 KB per chunk per band
chunk_y, chunk_x = 512, 512

# ── Create band arrays ──
for i, name in enumerate(band_names):
    arr = root.create_array(
        name,
        shape=(n_y, n_x),
        chunks=(chunk_y, chunk_x),
        dtype="uint16",
        fill_value=0,
    )
    arr.attrs["long_name"] = name
    arr.attrs["units"] = "reflectance_scaled"

    # Write data in tiles to avoid loading entire array into memory
    rng = np.random.default_rng(seed=i)
    for y_start in range(0, n_y, chunk_y * 4):
        y_end = min(y_start + chunk_y * 4, n_y)
        tile = rng.integers(0, 10000, size=(y_end - y_start, n_x), dtype="uint16")
        arr[y_start:y_end, :] = tile

print(f"Wrote {n_bands} bands, {n_y}x{n_x} pixels to GCS")
```

---

## Example 3: Setting Up Icechunk for Versioned Data on S3

**Dataset description:** A continuously updated air quality monitoring dataset that needs version history for regulatory compliance. Each daily update adds new observations and the full history must be queryable.

**Problem:** You need a Zarr-compatible store that supports atomic commits, branching for experimental processing, and the ability to read data as it existed at any past snapshot.

**Code:**

```python
import zarr
import numpy as np
from icechunk import IcechunkStore, StorageConfig

# ── Initialize versioned store on S3 ──
storage = StorageConfig.s3_from_env(
    bucket="air-quality-data",
    prefix="monitoring-v2.zarr",
    region="us-east-1",
)
store = IcechunkStore.open_or_create(storage=storage, mode="w")

# ── Create initial structure ──
root = zarr.open_group(store=store, mode="w")
root.attrs["dataset"] = "Urban Air Quality Monitoring Network"
root.attrs["version_policy"] = "Daily commits, monthly tags"

# Station metadata
n_stations = 50
stations = root.create_group("stations")
station_ids = stations.create_array("id", shape=(n_stations,), chunks=(n_stations,), dtype="<U10")
station_lat = stations.create_array("latitude", shape=(n_stations,), chunks=(n_stations,), dtype="float64")
station_lon = stations.create_array("longitude", shape=(n_stations,), chunks=(n_stations,), dtype="float64")

rng = np.random.default_rng(42)
station_ids[:] = [f"STN-{i:04d}" for i in range(n_stations)]
station_lat[:] = rng.uniform(40.0, 42.0, n_stations)
station_lon[:] = rng.uniform(-74.5, -73.5, n_stations)

# Measurement arrays (initially one day)
measurements = root.create_group("measurements")
pm25 = measurements.create_array(
    "pm25", shape=(24, n_stations), chunks=(24, n_stations), dtype="float32",
)
pm25[:] = rng.uniform(5.0, 35.0, (24, n_stations)).astype("float32")
pm25.attrs["units"] = "µg/m³"
pm25.attrs["long_name"] = "PM2.5 Concentration"

# ── Commit the initial data ──
commit_1 = store.commit("Initial station setup with day-1 PM2.5 data")
print(f"Commit 1: {commit_1}")

# ── Simulate adding a second day ──
pm25_day2 = rng.uniform(5.0, 35.0, (24, n_stations)).astype("float32")
pm25 = zarr.open_array(store=store, path="measurements/pm25", mode="r+")
pm25.resize((48, n_stations))
pm25[24:48, :] = pm25_day2

commit_2 = store.commit("Add day-2 PM2.5 observations")
print(f"Commit 2: {commit_2}")

# ── Read data from the first commit (time-travel) ──
store_v1 = IcechunkStore.open_existing(
    storage=storage, mode="r", snapshot_id=commit_1,
)
root_v1 = zarr.open_group(store=store_v1, mode="r")
print(f"Day-1 snapshot shape: {root_v1['measurements/pm25'].shape}")  # (24, 50)

# ── Tag a monthly release ──
store.tag("2024-01", snapshot_id=commit_2)
print("Tagged 2024-01")
```

---

## Example 4: Multi-Backend Data Pipeline

**Dataset description:** A processing pipeline that reads raw satellite data from an S3 archive, applies corrections, and writes results to Azure Blob Storage for downstream consumption by an Azure-based analytics platform.

**Problem:** You need to read from one cloud provider and write to another, using appropriate backends for each, while managing memory for a dataset that does not fit in RAM.

**Code:**

```python
import zarr
import numpy as np
from zarr.storage import FsspecStore

# ── Source: Read raw data from S3 ──
src_store = FsspecStore.from_url(
    "s3://satellite-archive/raw/2024-Q1.zarr",
    storage_options={"anon": True},
)
src = zarr.open_group(store=src_store, mode="r")
print(f"Source groups: {list(src.keys())}")

# ── Destination: Write to Azure Blob ──
dst_store = FsspecStore.from_url(
    "az://processed-data/corrected/2024-Q1.zarr",
    storage_options={
        "account_name": "analyticsstorage",
        "account_key": "base64key==",
    },
)
dst = zarr.open_group(store=dst_store, mode="w")
dst.attrs.update(dict(src.attrs))
dst.attrs["processing"] = "bias-corrected"

# ── Process each variable in chunks to manage memory ──
for var_name in ["radiance_band1", "radiance_band2", "radiance_band3"]:
    src_arr = src[var_name]
    dst_arr = dst.create_array(
        var_name,
        shape=src_arr.shape,
        chunks=src_arr.chunks,
        dtype="float32",
    )
    # Copy attributes
    dst_arr.attrs.update(dict(src_arr.attrs))

    # Process in row-chunks to limit memory
    chunk_rows = src_arr.chunks[0]
    for row_start in range(0, src_arr.shape[0], chunk_rows):
        row_end = min(row_start + chunk_rows, src_arr.shape[0])
        data = src_arr[row_start:row_end, :]

        # Apply bias correction (example: subtract per-row mean offset)
        correction = np.nanmean(data, axis=1, keepdims=True) * 0.02
        corrected = data - correction

        dst_arr[row_start:row_end, :] = corrected.astype("float32")

    print(f"Processed {var_name}: {src_arr.shape}")

print("Pipeline complete: S3 → process → Azure Blob")
```

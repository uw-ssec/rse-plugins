# Real-World Examples

## Contents

| Example | Description |
|---------|-------------|
| 1. Scientific Dataset from Scratch | Climate-like dataset with coordinates and CF metadata |
| 2. Reading a Remote Zarr Store | Access public cloud-hosted data and extract subsets |
| 3. Hierarchical Multi-Instrument Store | Organize multi-resolution, multi-instrument data |
| 4. Structured and Ragged Arrays | Compound dtypes and variable-length data |

---

## Example 1: Scientific Dataset from Scratch

**Problem:** Create a self-describing, cloud-ready Zarr store with CF-compliant metadata consumable by xarray.

```python
import zarr
import numpy as np

n_time, n_lat, n_lon = 365, 180, 360
root = zarr.open_group("global_climate_2024.zarr", mode="w")
root.attrs.update({
    "Conventions": "CF-1.8", "title": "Global Daily Climate 2024",
    "institution": "Climate Research Institute",
})

# Coordinates
time = root.create_array("time", shape=(n_time,), chunks=(n_time,), dtype="float64")
time[:] = np.arange(n_time, dtype="float64")
time.attrs.update({"units": "days since 2024-01-01", "calendar": "standard"})

lat = root.create_array("lat", shape=(n_lat,), chunks=(n_lat,), dtype="float64")
lat[:] = np.linspace(-89.5, 89.5, n_lat)
lat.attrs["units"] = "degrees_north"

lon = root.create_array("lon", shape=(n_lon,), chunks=(n_lon,), dtype="float64")
lon[:] = np.linspace(0.5, 359.5, n_lon)
lon.attrs["units"] = "degrees_east"

# Data variables
rng = np.random.default_rng(42)
for name, units, gen in [
    ("temperature", "K", lambda: rng.normal(280, 15, (n_time, n_lat, n_lon))),
    ("precipitation", "kg m-2 s-1", lambda: rng.exponential(1e-5, (n_time, n_lat, n_lon))),
]:
    arr = root.create_array(name, shape=(n_time, n_lat, n_lon),
                            chunks=(30, 90, 180), dtype="float32")
    arr[:] = gen().astype("float32")
    arr.attrs.update({"units": units, "long_name": name.replace("_", " ").title()})

print(root.tree())
```

---

## Example 2: Reading a Remote Zarr Store

**Problem:** Access a public cloud-hosted Zarr dataset, inspect structure, select a subset, and compute statistics without downloading the full store.

```python
import zarr
from zarr.storage import FsspecStore
import numpy as np

url = "s3://cmip6-pds/CMIP6/CMIP/NOAA-GFDL/GFDL-ESM4/historical/r1i1p1f1/Omon/tos/gn/v20190726/"
store = FsspecStore.from_url(url, storage_options={"anon": True})
root = zarr.open_group(store=store, mode="r")
print(root.tree())

# Read coordinate arrays
lat = root["lat"][:]
lon = root["lon"][:]

# Select North Atlantic subset (only needed chunks fetched)
lat_mask = (lat >= 30) & (lat <= 60)
lon_mask = (lon >= 280) & (lon <= 350)
lat_idx = np.where(lat_mask)[0]
lon_idx = np.where(lon_mask)[0]

tos = root["tos"]
subset = tos[:, lat_idx[0]:lat_idx[-1]+1, lon_idx[0]:lon_idx[-1]+1]
print(f"Subset shape: {subset.shape}, Mean SST: {np.nanmean(subset):.2f} K")
```

---

## Example 3: Hierarchical Multi-Instrument Store

**Problem:** Organize data from multiple instruments at different resolutions in a single Zarr store.

```python
import zarr
import numpy as np

root = zarr.open_group("multi_instrument.zarr", mode="w")
root.attrs["project"] = "Ocean Monitoring Campaign 2024"

rng = np.random.default_rng(42)

# High-frequency sonar (1 Hz, 1D)
sonar = root.create_group("sonar")
sonar.attrs["sample_rate_hz"] = 1
depth = sonar.create_array("depth", shape=(86400,), chunks=(3600,), dtype="float32")
depth[:] = rng.uniform(10, 200, 86400).astype("float32")
depth.attrs["units"] = "meters"

# Medium-frequency CTD (every 10 seconds, multi-param)
ctd = root.create_group("ctd")
ctd.attrs["sample_rate_hz"] = 0.1
for param, unit in [("temperature", "Celsius"), ("salinity", "PSU"), ("pressure", "dbar")]:
    arr = ctd.create_array(param, shape=(8640,), chunks=(864,), dtype="float32")
    arr[:] = rng.normal(15, 5, 8640).astype("float32")
    arr.attrs["units"] = unit

# Low-frequency satellite (daily, 2D grid)
sat = root.create_group("satellite")
sst = sat.create_array("sst", shape=(1, 720, 1440), chunks=(1, 360, 720), dtype="float32")
sst[:] = rng.normal(290, 10, (1, 720, 1440)).astype("float32")
sst.attrs.update({"units": "K", "long_name": "Sea Surface Temperature"})

print(root.tree())
```

---

## Example 4: Structured and Ragged Arrays

**Problem:** Store tabular-like data with compound dtypes and handle variable-length records.

```python
import zarr
import numpy as np

# ── Compound dtype (like a database row) ──
dt = np.dtype([("x", "float32"), ("y", "float32"), ("value", "float64"),
               ("quality_flag", "uint8")])

z = zarr.create_array(store="observations.zarr", shape=(10000,), chunks=(1000,), dtype=dt)

data = np.zeros(10000, dtype=dt)
rng = np.random.default_rng(42)
data["x"] = rng.uniform(-180, 180, 10000).astype("float32")
data["y"] = rng.uniform(-90, 90, 10000).astype("float32")
data["value"] = rng.normal(0, 1, 10000)
data["quality_flag"] = rng.integers(0, 4, 10000, dtype="uint8")
z[:] = data

# Read individual fields
x_coords = z["x"]
high_quality = z[:][z[:]["quality_flag"] == 0]
print(f"High-quality observations: {len(high_quality)}")
```

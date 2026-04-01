# Zarr Fundamentals Patterns

## Contents

| Pattern | Description |
|---------|-------------|
| 1. Hierarchical Scientific Data Store | Multi-group Zarr store with CF metadata |
| 2. Opening Remote Zarr Data | Access arrays on S3, GCS, HTTP |
| 3. Appending Data to Existing Arrays | Grow arrays with resize/append |
| 4. Advanced Indexing | Orthogonal, coordinate, mask, block indexing |
| 5. Sharding in Zarr v3 | Reduce cloud object count |
| 6. Concurrent Access | Thread-safe and process-safe I/O |

---

## Pattern 1: Hierarchical Scientific Data Store

**When to use:** Organizing multi-variable scientific data (climate, weather, simulations) with CF metadata.

```python
import zarr
import numpy as np

n_time, n_lat, n_lon = 365, 180, 360

root = zarr.open_group("climate_dataset.zarr", mode="w")
root.attrs.update({"Conventions": "CF-1.8", "title": "Global Daily Climate Dataset"})

# Coordinate arrays (single-chunk for fast full reads)
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
temp = root.create_array("temperature", shape=(n_time, n_lat, n_lon),
                         chunks=(30, 90, 180), dtype="float32")
temp.attrs.update({"units": "K", "long_name": "Air Temperature", "standard_name": "air_temperature"})

print(root.tree())
```

---

## Pattern 2: Opening Remote Zarr Data

**When to use:** Accessing Zarr stores on cloud object storage or HTTP endpoints.

```python
import zarr
from zarr.storage import FsspecStore

# S3 (anonymous)
store = FsspecStore.from_url("s3://bucket/data.zarr", storage_options={"anon": True})
root = zarr.open_group(store=store, mode="r")

# GCS
store = FsspecStore.from_url("gs://bucket/data.zarr", storage_options={"token": "anon"})

# Azure
store = FsspecStore.from_url("az://container/data.zarr",
                             storage_options={"account_name": "acct", "account_key": "key"})

# obstore (Rust-based, faster)
from obstore.store import S3Store
obs = S3Store.from_url("s3://bucket/data.zarr", config={"AWS_REGION": "us-west-2"})
store = zarr.storage.ObjectStore(obs, read_only=True)

# Read a subset (only needed chunks are fetched)
z = zarr.open_array(store=store, mode="r")
subset = z[0:100, 0:100]
```

→ See **cloud-storage-backends** skill for complete auth patterns and caching.

---

## Pattern 3: Appending Data to Existing Arrays

**When to use:** Growing a dataset over time (daily ingestion, streaming sensors).

```python
import zarr
import numpy as np

# Create initial array
z = zarr.create_array(store="timeseries.zarr", shape=(100, 10), chunks=(50, 10), dtype="float32")
z[:] = np.random.randn(100, 10).astype("float32")

# Append along axis 0
new_data = np.random.randn(50, 10).astype("float32")
z.append(new_data, axis=0)
print(f"New shape: {z.shape}")  # (150, 10)

# Resize explicitly (for pre-allocation)
z.resize(200, 10)
z[150:200, :] = np.random.randn(50, 10).astype("float32")
```

**For xarray-based appends**, see the **zarr-xarray-integration** skill (append_dim, region writes).

---

## Pattern 4: Advanced Indexing

**When to use:** Non-contiguous data access — scattered points, boolean masks, or chunk-aligned bulk reads.

```python
import zarr
import numpy as np

z = zarr.open_array("data.zarr", mode="r")  # shape (10000, 10000), chunks (1000, 1000)

# ── Coordinate selection (scattered points) ──
rows, cols = [0, 10, 20], [5, 15, 25]
values = z.vindex[rows, cols]       # shape (3,) — values at (0,5), (10,15), (20,25)

# ── Orthogonal selection (Cartesian product) ──
values = z.oindex[rows, cols]       # shape (3, 3) — all row×col combinations

# ── Mask selection ──
mask = np.zeros(z.shape, dtype=bool)
mask[0:100, 0:100] = True
values = z.vindex[mask]             # 1D array of True-masked values

# ── Block selection (by chunk index) ──
block = z.blocks[0, 0]             # shape (1000, 1000) — first chunk
block = z.blocks[0:2, 0:3]        # shape (2000, 3000) — 2×3 chunk region

# ── Field selection (structured dtype) ──
# z_struct["field_name"] — extracts one field from a compound dtype
```

---

## Pattern 5: Sharding in Zarr v3

**When to use:** Reducing object count on cloud stores where listing/managing thousands of small files is expensive.

```python
import zarr
import numpy as np

# Sharded array: outer chunks (shards) contain inner chunks
z = zarr.create_array(
    store="sharded.zarr",
    shape=(10000, 10000),
    chunks=(2500, 2500),     # shard size (4 shard files)
    shards=(500, 500),       # inner chunk size (25 chunks per shard)
    dtype="float32",
)

z[:] = np.random.randn(10000, 10000).astype("float32")

# Reading a 500×500 region only decompresses one inner chunk
subset = z[0:500, 0:500]

# Object count comparison:
# No sharding:  100,000 objects (10000/100)²
# With sharding: 4 shard files + metadata
```

**Trade-off:** Shards are the minimum write unit — the full shard must fit in memory. Target 100 MB–1 GB shard sizes.

---

## Pattern 6: Concurrent Access

**When to use:** Multi-threaded or multi-process workflows reading/writing the same store.

```python
import zarr
import numpy as np
from multiprocessing import Pool

# ── Concurrent reads: always safe, no locks needed ──
z = zarr.open_array("data.zarr", mode="r")
# Multiple threads/processes can read simultaneously

# ── Concurrent writes: safe IF writing to non-overlapping chunks ──
def write_chunk(args):
    idx, path = args
    z = zarr.open_array(path, mode="r+")
    start = idx * 1000
    z[start:start+1000] = np.random.randn(1000).astype("float32")

z = zarr.create_array(store="parallel.zarr", shape=(10000,), chunks=(1000,), dtype="float32")
with Pool(4) as pool:
    pool.map(write_chunk, [(i, "parallel.zarr") for i in range(10)])

# ── CRITICAL for Blosc + multiprocessing ──
from numcodecs import blosc
blosc.use_threads = False  # prevents silent data corruption
```

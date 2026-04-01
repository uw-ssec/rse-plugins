# Cloud Storage Backend Patterns

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| Pattern 1: S3 Backend with fsspec | 14–75 | Read and write Zarr on S3 with anonymous and authenticated access |
| Pattern 2: GCS Backend with fsspec | 76–135 | Access Zarr stores on Google Cloud Storage |
| Pattern 3: Azure Blob Backend with fsspec | 136–195 | Work with Zarr on Azure Blob Storage |
| Pattern 4: High-Performance Cloud I/O with obstore | 196–270 | Use the Rust-based obstore library for maximum throughput |
| Pattern 5: Icechunk Versioned Storage on S3 | 271–365 | Version-controlled Zarr datasets with branching and time-travel |
| Pattern 6: Read-Through Caching for Remote Stores | 366–430 | Cache cloud data locally for repeated reads |

---

## Pattern 1: S3 Backend with fsspec

**Description:** Access Zarr stores on Amazon S3 using the fsspec/s3fs backend. Supports anonymous access for public datasets, environment-based credentials, named profiles, and explicit keys.

**When to use:**
- Reading public datasets hosted on S3 (NOAA, NASA, Pangeo, CMIP6)
- Writing research outputs to an S3 bucket
- Standard AWS credential chain (env vars, profiles, IAM roles)

**Code example:**

```python
import zarr
from zarr.storage import FsspecStore
import numpy as np

# ── Read a public dataset anonymously ──
store = FsspecStore.from_url(
    "s3://noaa-goes16/ABI-L2-CMIPF/2024/001/00/",
    storage_options={"anon": True},
)
root = zarr.open_group(store=store, mode="r")
print(root.tree())

# ── Write to a private bucket (credentials from environment) ──
store = FsspecStore.from_url("s3://my-research-bucket/experiment-001.zarr")
root = zarr.open_group(store=store, mode="w")
arr = root.create_array(
    "results",
    shape=(10000, 500),
    chunks=(1000, 500),
    dtype="float64",
)
arr[:] = np.random.randn(10000, 500)
root.attrs["experiment"] = "turbulence-sim-001"
print(f"Wrote {arr.nbytes / 1e6:.1f} MB to S3")

# ── Read with a named AWS profile ──
store = FsspecStore.from_url(
    "s3://shared-bucket/team-data.zarr",
    storage_options={"profile": "research-team"},
)
root = zarr.open_group(store=store, mode="r")

# ── S3-compatible endpoint (MinIO, Ceph, etc.) ──
store = FsspecStore.from_url(
    "s3://local-bucket/data.zarr",
    storage_options={
        "key": "minioadmin",
        "secret": "minioadmin",
        "client_kwargs": {"endpoint_url": "http://localhost:9000"},
    },
)
```

---

## Pattern 2: GCS Backend with fsspec

**Description:** Access Zarr stores on Google Cloud Storage using the fsspec/gcsfs backend. Supports anonymous access, service account keys, and application default credentials.

**When to use:**
- Reading public GCS-hosted datasets (Google Earth Engine exports, ARCO-ERA5)
- Writing outputs to a GCS bucket from a Compute Engine VM or Cloud Run job

**Code example:**

```python
import zarr
from zarr.storage import FsspecStore

# ── Anonymous access to public data ──
store = FsspecStore.from_url(
    "gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3",
    storage_options={"token": "anon"},
)
root = zarr.open_group(store=store, mode="r")
print(root.tree())

# ── Service account JSON key ──
store = FsspecStore.from_url(
    "gs://my-project-bucket/output.zarr",
    storage_options={"token": "/path/to/service-account.json"},
)

# ── Application default credentials (gcloud auth application-default login) ──
store = FsspecStore.from_url(
    "gs://my-project-bucket/output.zarr",
    storage_options={"token": "google_default"},
)
root = zarr.open_group(store=store, mode="w")
arr = root.create_array("data", shape=(5000, 5000), chunks=(500, 500), dtype="float32")
```

---

## Pattern 3: Azure Blob Backend with fsspec

**Description:** Access Zarr stores on Azure Blob Storage using the fsspec/adlfs backend. Supports connection strings, account keys, SAS tokens, and managed identity.

**When to use:**
- Reading or writing Zarr data in Azure Blob containers
- Running workloads on Azure VMs, AKS, or Azure Functions with managed identity

**Code example:**

```python
import zarr
from zarr.storage import FsspecStore

# ── Connection string (from Azure Portal) ──
store = FsspecStore.from_url(
    "az://my-container/data.zarr",
    storage_options={
        "connection_string": "DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...;EndpointSuffix=core.windows.net"
    },
)
root = zarr.open_group(store=store, mode="r")

# ── Account name + key ──
store = FsspecStore.from_url(
    "az://my-container/data.zarr",
    storage_options={
        "account_name": "mystorageaccount",
        "account_key": "base64key==",
    },
)

# ── SAS token ──
store = FsspecStore.from_url(
    "az://my-container/data.zarr",
    storage_options={
        "account_name": "mystorageaccount",
        "sas_token": "sv=2021-06-08&ss=b&srt=sco&sp=rl&se=...",
    },
)

# ── Managed identity (Azure VM, AKS) ──
store = FsspecStore.from_url(
    "az://my-container/data.zarr",
    storage_options={"account_name": "mystorageaccount", "anon": False},
)
```

---

## Pattern 4: High-Performance Cloud I/O with obstore

**Description:** Use the Rust-based obstore library for maximum throughput when reading or writing large Zarr datasets on cloud storage. obstore provides native async I/O, automatic connection pooling, and lower per-request overhead than Python-based fsspec implementations.

**When to use:**
- Large-scale analysis pipelines that are I/O bound
- Need lower latency per request (Rust-native HTTP stack)
- Already using obstore in other parts of a pipeline (e.g., with GeoParquet)

**Code example:**

```python
import zarr
import numpy as np
from obstore.store import S3Store, GCSStore, AzureStore

# ── S3 with obstore ──
obs_s3 = S3Store.from_url(
    "s3://my-bucket/data.zarr",
    config={"AWS_REGION": "us-west-2"},
)
store = zarr.storage.ObjectStore(obs_s3, read_only=True)
root = zarr.open_group(store=store, mode="r")

# ── GCS with obstore ──
obs_gcs = GCSStore.from_url(
    "gs://my-bucket/data.zarr",
    config={"GOOGLE_SERVICE_ACCOUNT": "/path/to/key.json"},
)
store = zarr.storage.ObjectStore(obs_gcs, read_only=True)
root = zarr.open_group(store=store, mode="r")

# ── Azure with obstore ──
obs_az = AzureStore.from_url(
    "az://my-container/data.zarr",
    config={
        "AZURE_STORAGE_ACCOUNT_NAME": "mystorageaccount",
        "AZURE_STORAGE_ACCOUNT_KEY": "base64key==",
    },
)
store = zarr.storage.ObjectStore(obs_az, read_only=True)
root = zarr.open_group(store=store, mode="r")

# ── Write with obstore ──
obs_w = S3Store.from_url("s3://my-bucket/output.zarr")
store = zarr.storage.ObjectStore(obs_w)
root = zarr.open_group(store=store, mode="w")
arr = root.create_array("field", shape=(5000, 5000), chunks=(500, 500), dtype="float32")
arr[:] = np.random.randn(5000, 5000).astype("float32")

# ── Client tuning ──
obs = S3Store.from_url(
    "s3://my-bucket/data.zarr",
    client_options={"timeout": "60s", "connect_timeout": "5s"},
)
```

---

## Pattern 5: Icechunk Versioned Storage on S3

**Description:** Use Icechunk to create version-controlled Zarr stores on cloud object storage. Icechunk adds Git-like semantics — commits, branches, tags, and time-travel reads — on top of standard cloud backends.

**When to use:**
- Datasets that are updated incrementally and you need to track each revision
- Collaborative workflows where multiple writers need atomic commits
- Regulatory or reproducibility requirements (read data as it was at a specific time)

**Code example:**

```python
import zarr
import numpy as np
from icechunk import IcechunkStore, StorageConfig

# ── Create a versioned store on S3 ──
storage = StorageConfig.s3_from_env(
    bucket="my-bucket",
    prefix="versioned-climate.zarr",
    region="us-west-2",
)
store = IcechunkStore.open_or_create(storage=storage, mode="w")

# ── Write initial data ──
root = zarr.open_group(store=store, mode="w")
temp = root.create_array(
    "temperature",
    shape=(365, 180, 360),
    chunks=(30, 90, 180),
    dtype="float32",
)
temp[:] = np.random.randn(365, 180, 360).astype("float32")
root.attrs["source"] = "CESM2 Model Output"

# ── Commit (like git commit) ──
first_commit = store.commit("Initial temperature data for 2024")
print(f"Committed: {first_commit}")

# ── Update data on a branch ──
store.new_branch("bias-correction")
store.checkout(branch="bias-correction")
temp = zarr.open_array(store=store, path="temperature", mode="r+")
temp[:] = temp[:] - 0.5  # apply bias correction
store.commit("Apply -0.5K bias correction")

# ── Read from main (original data unchanged) ──
store_main = IcechunkStore.open_existing(storage=storage, mode="r")
store_main.checkout(branch="main")
root_main = zarr.open_group(store=store_main, mode="r")
print(f"Main branch mean: {root_main['temperature'][:10, 0, 0].mean():.3f}")

# ── Tag a release ──
store.checkout(branch="main")
store.tag("v1.0", snapshot_id=first_commit)
```

---

## Pattern 6: Read-Through Caching for Remote Stores

**Description:** Use fsspec's built-in caching protocols to cache cloud-hosted Zarr chunks on local disk, avoiding repeated downloads during iterative analysis.

**When to use:**
- Repeatedly reading the same subsets of a large cloud dataset
- Working with cloud data on a machine with good local disk but limited bandwidth
- Prototyping analysis on a remote dataset before scaling to cloud compute

**Code example:**

```python
import zarr
from zarr.storage import FsspecStore

# ── Simple cache (download once, keep until process exits) ──
store = FsspecStore.from_url(
    "simplecache::s3://noaa-goes16/ABI-L2-CMIPF/2024/001/00/data.zarr",
    storage_options={
        "s3": {"anon": True},
        "simplecache": {"cache_storage": "/tmp/zarr-cache"},
    },
)
root = zarr.open_group(store=store, mode="r")

# ── File cache with expiry (persistent across sessions) ──
store = FsspecStore.from_url(
    "filecache::s3://my-bucket/data.zarr",
    storage_options={
        "s3": {"anon": True},
        "filecache": {
            "cache_storage": "/data/zarr-cache",
            "expiry_time": 86400,  # re-check remote after 24 hours
            "same_names": True,    # preserve original filenames in cache
        },
    },
)

# ── Block cache (cache individual byte ranges, useful for partial reads) ──
store = FsspecStore.from_url(
    "blockcache::s3://my-bucket/data.zarr",
    storage_options={
        "s3": {"anon": True},
        "blockcache": {
            "cache_storage": "/tmp/zarr-block-cache",
            "block_size": 1_048_576,  # 1 MB blocks
        },
    },
)
```

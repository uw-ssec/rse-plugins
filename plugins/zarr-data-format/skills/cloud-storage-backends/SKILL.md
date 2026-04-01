---
name: cloud-storage-backends
description: Configure Zarr stores on cloud object storage services. Covers S3, GCS, Azure Blob backends via fsspec (s3fs, gcsfs, adlfs), the high-performance Rust-based obstore library, Icechunk for versioned cloud storage, authentication patterns, caching strategies, and performance tuning for remote I/O.
metadata:
  references:
    - references/patterns.md
    - references/examples.md
    - references/common-issues.md
---

# Cloud Storage Backends for Zarr

Configure Zarr to read and write arrays on cloud object storage — **Amazon S3**, **Google Cloud Storage (GCS)**, and **Azure Blob Storage**. This skill covers the full range of backend options: **fsspec**-based stores (s3fs, gcsfs, adlfs), the high-performance Rust-based **obstore** library, and **Icechunk** for versioned, transactional cloud storage. You will learn authentication patterns, caching strategies, and performance tuning for remote I/O.

**Zarr Documentation**: https://zarr.readthedocs.io/

**fsspec Documentation**: https://filesystem-spec.readthedocs.io/

**obstore Documentation**: https://developmentseed.org/obstore/

**Icechunk Documentation**: https://icechunk.io/

## Quick Reference Card

### Installation & Setup

```bash
# Using pixi (recommended for scientific projects)
pixi add zarr numpy

# fsspec-based cloud backends
pixi add s3fs gcsfs adlfs fsspec

# Using pip
pip install zarr[remote]          # includes fsspec + s3fs + gcsfs + adlfs

# High-performance Rust-based backend
pip install obstore

# Versioned cloud storage
pip install icechunk
```

### Essential Imports and Operations

```python
import zarr
from zarr.storage import FsspecStore

# ── S3 via fsspec ──
store = FsspecStore.from_url(
    "s3://my-bucket/data.zarr",
    storage_options={"anon": True},  # anonymous access for public data
)
root = zarr.open_group(store=store, mode="r")

# ── GCS via fsspec ──
store = FsspecStore.from_url("gs://my-bucket/data.zarr")
root = zarr.open_group(store=store, mode="r")

# ── Azure via fsspec ──
store = FsspecStore.from_url("az://my-container/data.zarr")
root = zarr.open_group(store=store, mode="r")

# ── obstore (Rust-based, high performance) ──
from obstore.store import S3Store
import zarr

obs = S3Store.from_url("s3://my-bucket/data.zarr", config={"AWS_REGION": "us-west-2"})
store = zarr.storage.ObjectStore(obs, read_only=True)
root = zarr.open_group(store=store, mode="r")

# ── Icechunk (versioned storage) ──
from icechunk import IcechunkStore, StorageConfig

storage = StorageConfig.s3_from_env(bucket="my-bucket", prefix="data.zarr")
store = IcechunkStore.open_or_create(storage=storage, mode="w")
root = zarr.open_group(store=store, mode="w")
```

### Quick Decision Tree

```
Need to access cloud Zarr data?
├── Public dataset, read-only?
│   └── FsspecStore.from_url with anon=True
├── Authenticated access?
│   ├── Already using fsspec elsewhere?
│   │   └── FsspecStore.from_url with storage_options
│   ├── Need maximum throughput?
│   │   └── obstore (Rust-based, async I/O)
│   └── Need versioning / transactions?
│       └── Icechunk
├── Which cloud provider?
│   ├── AWS S3 → s3fs or obstore S3Store
│   ├── Google GCS → gcsfs or obstore GCSStore
│   └── Azure Blob → adlfs or obstore AzureStore
└── Need caching for repeated reads?
    └── fsspec with simplecache or filecache
```

## When to Use This Skill

Use this skill when:

- Reading Zarr arrays hosted on S3, GCS, or Azure Blob Storage
- Writing new Zarr stores to cloud object storage
- Choosing between fsspec, obstore, and Icechunk backends
- Configuring authentication (credentials, IAM roles, service accounts)
- Optimizing read/write performance for remote Zarr stores
- Setting up local caching for cloud-hosted data
- Working with versioned datasets using Icechunk

## Core Concepts

### 1. Store Backend Overview

Zarr decouples array logic from storage through a **Store** interface. Any object that implements the Zarr store protocol can serve as a backend.

| Backend | Library | Async | Speed | Versioning | Best For |
|---------|---------|-------|-------|------------|----------|
| LocalStore | zarr (built-in) | No | Fastest | No | Local disk, NFS |
| FsspecStore | zarr + fsspec | Yes | Good | No | Broad cloud support, caching |
| ObjectStore | zarr + obstore | Yes | Very Fast | No | High-throughput cloud I/O |
| IcechunkStore | icechunk | Yes | Fast | Yes | Versioned cloud datasets |

```python
# LocalStore (default when passing a path string)
root = zarr.open_group("local_data.zarr", mode="w")

# FsspecStore (any fsspec-supported URL)
from zarr.storage import FsspecStore
store = FsspecStore.from_url("s3://bucket/path.zarr")

# ObjectStore (obstore backend)
from obstore.store import S3Store
obs = S3Store.from_url("s3://bucket/path.zarr")
store = zarr.storage.ObjectStore(obs)

# IcechunkStore (versioned)
from icechunk import IcechunkStore, StorageConfig
storage = StorageConfig.s3_from_env(bucket="bucket", prefix="path.zarr")
store = IcechunkStore.open_or_create(storage=storage, mode="w")
```

### 2. S3 Backend

**Via fsspec (s3fs):**

```python
from zarr.storage import FsspecStore

# Anonymous access (public buckets)
store = FsspecStore.from_url(
    "s3://noaa-goes16/ABI-L2-CMIPF/2024/001/00/",
    storage_options={"anon": True},
)

# Authenticated via environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
store = FsspecStore.from_url("s3://my-bucket/data.zarr")

# Explicit credentials
store = FsspecStore.from_url(
    "s3://my-bucket/data.zarr",
    storage_options={
        "key": "AKIAIOSFODNN7EXAMPLE",
        "secret": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        "endpoint_url": "https://s3.us-west-2.amazonaws.com",
    },
)

# Using a named AWS profile
store = FsspecStore.from_url(
    "s3://my-bucket/data.zarr",
    storage_options={"profile": "research-account"},
)
```

**Via obstore (Rust-based, higher throughput):**

```python
from obstore.store import S3Store
import zarr

# Credentials from environment or instance metadata (IAM role)
obs = S3Store.from_url(
    "s3://my-bucket/data.zarr",
    config={"AWS_REGION": "us-west-2"},
)
store = zarr.storage.ObjectStore(obs, read_only=True)
root = zarr.open_group(store=store, mode="r")
```

### 3. GCS Backend

```python
from zarr.storage import FsspecStore

# Anonymous access
store = FsspecStore.from_url(
    "gs://public-bucket/data.zarr",
    storage_options={"token": "anon"},
)

# Service account JSON key
store = FsspecStore.from_url(
    "gs://my-bucket/data.zarr",
    storage_options={"token": "/path/to/service-account.json"},
)

# Application default credentials (gcloud auth application-default login)
store = FsspecStore.from_url(
    "gs://my-bucket/data.zarr",
    storage_options={"token": "google_default"},
)
```

### 4. Azure Blob Backend

```python
from zarr.storage import FsspecStore

# Connection string
store = FsspecStore.from_url(
    "az://my-container/data.zarr",
    storage_options={"connection_string": "DefaultEndpointsProtocol=https;..."},
)

# Account key
store = FsspecStore.from_url(
    "az://my-container/data.zarr",
    storage_options={
        "account_name": "mystorageaccount",
        "account_key": "base64-encoded-key",
    },
)

# Managed identity (Azure VM, AKS, Functions)
store = FsspecStore.from_url(
    "az://my-container/data.zarr",
    storage_options={"account_name": "mystorageaccount", "anon": False},
)
```

### 5. Icechunk — Versioned Cloud Storage

Icechunk adds Git-like versioning on top of any cloud store, enabling branches, tags, time-travel reads, and atomic commits.

```python
from icechunk import IcechunkStore, StorageConfig
import zarr

# Create a versioned store on S3
storage = StorageConfig.s3_from_env(
    bucket="my-bucket",
    prefix="versioned-data.zarr",
    region="us-west-2",
)
store = IcechunkStore.open_or_create(storage=storage, mode="w")

# Write data
root = zarr.open_group(store=store, mode="w")
arr = root.create_array("temperature", shape=(365, 180, 360), chunks=(30, 90, 180), dtype="float32")
arr[:] = 0.0

# Commit changes (like git commit)
store.commit("Initial temperature array")

# Read at a specific snapshot
snapshot_id = store.snapshot_id
store_at_snapshot = IcechunkStore.open_existing(
    storage=storage, mode="r", snapshot_id=snapshot_id
)

# Branch workflow
store.new_branch("experiment-1")
store.checkout(branch="experiment-1")
```

### 6. Caching Strategies

fsspec provides built-in caching to avoid repeated downloads of the same chunks.

```python
from zarr.storage import FsspecStore

# Simple cache — downloads to local temp directory
store = FsspecStore.from_url(
    "simplecache::s3://my-bucket/data.zarr",
    storage_options={
        "s3": {"anon": True},
        "simplecache": {"cache_storage": "/tmp/zarr-cache"},
    },
)

# File cache — persistent, checks remote for updates
store = FsspecStore.from_url(
    "filecache::s3://my-bucket/data.zarr",
    storage_options={
        "s3": {"anon": True},
        "filecache": {
            "cache_storage": "/data/zarr-cache",
            "expiry_time": 3600,  # seconds
        },
    },
)
```

### 7. Performance Tuning

Key factors for remote I/O performance:

| Factor | Recommendation |
|--------|----------------|
| Chunk size | 1–10 MB per chunk for cloud (too small = too many requests) |
| Concurrent requests | Increase `max_concurrency` in storage_options |
| Connection pooling | obstore handles this automatically; for s3fs set `config_kwargs` |
| Consolidated metadata | Use `zarr.consolidate_metadata()` for v2 stores |
| Read pattern | Sequential access is faster than random access on cloud |

```python
# Increase S3 concurrency with fsspec
store = FsspecStore.from_url(
    "s3://my-bucket/data.zarr",
    storage_options={
        "anon": True,
        "config_kwargs": {"max_pool_connections": 50},
    },
)

# obstore automatically manages connection pooling and async I/O
from obstore.store import S3Store
obs = S3Store.from_url(
    "s3://my-bucket/data.zarr",
    client_options={"timeout": "30s", "connect_timeout": "5s"},
)
```

---
name: cloud-storage-backends
description: Configures Zarr stores on cloud object storage, covering S3, GCS, and Azure Blob backends via fsspec (s3fs, gcsfs, adlfs), the high-performance Rust-based obstore library, and Icechunk for versioned cloud storage. Covers authentication patterns, caching strategies, and performance tuning for remote I/O. Use when the user asks about reading or writing Zarr data on S3, GCS, or Azure, or mentions fsspec, obstore, or Icechunk for remote Zarr access.
metadata:
  references:
    - references/patterns.md
    - references/examples.md
    - references/common-issues.md
---

# Cloud Storage Backends for Zarr

Configure Zarr to read and write arrays on Amazon S3, Google Cloud Storage, and Azure Blob Storage using fsspec, obstore, or Icechunk.

## Resources

| Resource | Purpose |
|----------|---------|
| [references/patterns.md](references/patterns.md) | Full code patterns: S3, GCS, Azure, obstore, Icechunk, caching |
| [references/examples.md](references/examples.md) | Real-world end-to-end examples (CMIP6, multi-backend pipeline) |
| [references/common-issues.md](references/common-issues.md) | Auth failures, slow reads, timeouts, CORS, cost optimization |

## Installation

```bash
pip install zarr[remote]          # fsspec + s3fs + gcsfs + adlfs
pip install obstore               # Rust-based high-performance backend
pip install icechunk              # versioned cloud storage
```

## Backend Decision Tree

```
Need cloud Zarr access?
├── Public read-only dataset? → FsspecStore.from_url with anon=True
├── Need versioning/transactions? → IcechunkStore
├── Need maximum throughput? → obstore (ObjectStore)
└── Standard authenticated access? → FsspecStore.from_url with storage_options
    ├── AWS S3 → s3fs / obstore S3Store
    ├── GCS   → gcsfs / obstore GCSStore
    └── Azure → adlfs / obstore AzureStore
```

## Quick Reference

```python
from zarr.storage import FsspecStore
import zarr

# S3 — anonymous (public data)
store = FsspecStore.from_url("s3://my-bucket/data.zarr", storage_options={"anon": True})

# S3 — authenticated (env vars, IAM role, or profile)
store = FsspecStore.from_url("s3://my-bucket/data.zarr",
    storage_options={"profile": "research-account"})

# GCS — application default credentials
store = FsspecStore.from_url("gs://my-bucket/data.zarr",
    storage_options={"token": "google_default"})

# Azure — connection string
store = FsspecStore.from_url("az://my-container/data.zarr",
    storage_options={"connection_string": "DefaultEndpointsProtocol=https;..."})

# obstore — high-throughput S3
from obstore.store import S3Store
obs = S3Store.from_url("s3://my-bucket/data.zarr", config={"AWS_REGION": "us-west-2"})
store = zarr.storage.ObjectStore(obs, read_only=True)

# Icechunk — versioned S3
from icechunk import IcechunkStore, StorageConfig
storage = StorageConfig.s3_from_env(bucket="my-bucket", prefix="data.zarr", region="us-west-2")
store = IcechunkStore.open_or_create(storage=storage, mode="w")

# Caching — avoid repeated remote downloads
store = FsspecStore.from_url("simplecache::s3://my-bucket/data.zarr",
    storage_options={"s3": {"anon": True},
                     "simplecache": {"cache_storage": "/tmp/zarr-cache"}})
```

## Verify Connection Before Proceeding

Always test store connectivity before running analysis:

```python
import zarr
from zarr.storage import FsspecStore
from botocore.exceptions import ClientError, NoCredentialsError

def open_store_safe(url: str, **storage_options):
    try:
        store = FsspecStore.from_url(url, storage_options=storage_options)
        root = zarr.open_group(store=store, mode="r")
        # Force a real read to verify credentials and connectivity
        _ = dict(root.info)
        return root
    except (PermissionError, ClientError) as e:
        raise PermissionError(f"Auth failed for {url}: {e}. "
            "Check credentials or use anon=True for public data.") from e
    except FileNotFoundError:
        raise FileNotFoundError(f"Store not found at {url}. "
            "Verify the bucket name, prefix, and region.") from None
    except Exception as e:
        raise RuntimeError(f"Could not open {url}: {e}") from e
```

Common error signals:
- `403 Forbidden` / `NoCredentialsError` → wrong or missing credentials; see [common-issues.md](references/common-issues.md)
- `FileNotFoundError` → wrong path/prefix or bucket does not exist
- Slow first open → no consolidated metadata; run `zarr.consolidate_metadata(store)` on v2 stores

## Performance Quick Reference

| Factor | Recommendation |
|--------|----------------|
| Chunk size | 1–10 MB per chunk for cloud (too small = too many requests) |
| Metadata | Run `zarr.consolidate_metadata(store)` on v2 stores |
| Concurrency | Use obstore for automatic async connection pooling |
| Repeated reads | Use `simplecache` or `filecache` (see caching pattern above) |
| Icechunk commit | Call `store.commit("message")` after every logical write batch |

See [patterns.md](references/patterns.md) for full auth options per provider and [common-issues.md](references/common-issues.md) for slow-read and timeout diagnostics.

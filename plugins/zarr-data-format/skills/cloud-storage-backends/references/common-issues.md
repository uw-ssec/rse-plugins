# Common Issues and Solutions

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| Issue 1: Authentication Failures on S3 | 18–80 | Wrong credentials, expired tokens, or missing permissions |
| Issue 2: Slow Reads from Cloud Storage | 81–145 | Poor performance due to chunk size or missing caching |
| Issue 3: fsspec vs obstore — When to Use Which | 146–205 | Choosing the right backend library for your workload |
| Issue 4: Icechunk Version Conflicts | 206–265 | Concurrent writes to the same branch causing commit failures |
| Issue 5: CORS Errors When Accessing from Browser | 266–315 | Cross-origin errors when using browser-based Zarr clients |
| Issue 6: Connection Timeout on Large Stores | 316–375 | Timeout when opening stores with many chunks and no consolidated metadata |
| Issue 7: Cost Optimization for Cloud Zarr | 376–430 | Reducing cloud storage and request costs |

---

## Issue 1: Authentication Failures on S3

**Symptoms:**
- `ClientError: An error occurred (403) when calling the HeadObject operation: Forbidden`
- `NoCredentialsError: Unable to locate credentials`
- `ExpiredTokenException` after running for a while
- Works locally but fails on EC2 or in a container

**Cause:** The S3 credential chain is not finding valid credentials. Common reasons: environment variables not set, AWS profile not configured, IAM role not attached to the instance, or temporary credentials have expired.

**Solution:**

```python
from zarr.storage import FsspecStore

# ── Check which credentials s3fs is using ──
import s3fs
fs = s3fs.S3FileSystem()
print(f"Using credentials: {fs.storage_options}")

# ── Fix 1: Set environment variables ──
# export AWS_ACCESS_KEY_ID=AKIA...
# export AWS_SECRET_ACCESS_KEY=...
# export AWS_DEFAULT_REGION=us-west-2

# ── Fix 2: Use explicit credentials ──
store = FsspecStore.from_url(
    "s3://my-bucket/data.zarr",
    storage_options={
        "key": "AKIAIOSFODNN7EXAMPLE",
        "secret": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        "client_kwargs": {"region_name": "us-west-2"},
    },
)

# ── Fix 3: For public data, use anonymous access ──
store = FsspecStore.from_url(
    "s3://public-bucket/data.zarr",
    storage_options={"anon": True},
)

# ── Fix 4: For EC2/ECS, attach an IAM role and just use defaults ──
store = FsspecStore.from_url("s3://my-bucket/data.zarr")
# s3fs automatically uses instance metadata credentials

# ── Fix 5: Refresh expired session tokens ──
# Use `aws sts get-session-token` or configure credential_process in ~/.aws/config
```

---

## Issue 2: Slow Reads from Cloud Storage

**Symptoms:**
- Reading a small subset takes much longer than expected
- Network I/O dominates wall-clock time
- Cloud egress costs are unexpectedly high
- CPU utilization is low while reading

**Cause:** The most common causes are: (1) chunk sizes too small, generating thousands of HTTP requests for small objects; (2) no caching, so repeated reads re-download the same chunks; (3) sequential I/O instead of concurrent requests.

**Solution:**

```python
from zarr.storage import FsspecStore

# ── Diagnose: Check chunk sizes ──
import zarr
root = zarr.open_group("s3://my-bucket/data.zarr", mode="r")
arr = root["temperature"]
chunk_bytes = arr.dtype.itemsize
for c in arr.chunks:
    chunk_bytes *= c
print(f"Chunk size: {chunk_bytes / 1e6:.2f} MB")
# Target: 1–10 MB per chunk for cloud storage

# ── Fix 1: Re-chunk to larger sizes ──
# If chunks are too small, rechunk the data (one-time cost)
import numpy as np
src = zarr.open_array("s3://my-bucket/small-chunks.zarr", mode="r")
dst = zarr.create_array(
    store="s3://my-bucket/large-chunks.zarr",
    shape=src.shape,
    chunks=(1000, 1000),  # larger chunks
    dtype=src.dtype,
)

# ── Fix 2: Enable caching for repeated reads ──
store = FsspecStore.from_url(
    "simplecache::s3://my-bucket/data.zarr",
    storage_options={
        "s3": {"anon": True},
        "simplecache": {"cache_storage": "/tmp/zarr-cache"},
    },
)

# ── Fix 3: Use obstore for higher throughput ──
from obstore.store import S3Store
obs = S3Store.from_url("s3://my-bucket/data.zarr")
store = zarr.storage.ObjectStore(obs, read_only=True)

# ── Fix 4: Increase s3fs concurrency ──
store = FsspecStore.from_url(
    "s3://my-bucket/data.zarr",
    storage_options={
        "config_kwargs": {"max_pool_connections": 50},
    },
)
```

---

## Issue 3: fsspec vs obstore — When to Use Which

**Symptoms:**
- Uncertainty about which backend library to choose
- Performance differences between the two
- Feature gaps when switching backends

**Cause:** Both fsspec and obstore provide cloud storage access for Zarr, but they have different strengths and trade-offs.

**Solution:**

| Factor | fsspec (s3fs/gcsfs/adlfs) | obstore |
|--------|---------------------------|---------|
| **Language** | Pure Python | Rust (Python bindings) |
| **Throughput** | Good | Better (native async) |
| **Caching** | Built-in (simplecache, filecache) | No built-in caching |
| **Ecosystem** | Broad (pandas, Dask, xarray) | Growing |
| **Auth flexibility** | Many options (profiles, tokens, etc.) | Env vars, config dict |
| **S3-compatible** | Yes (endpoint_url) | Yes |
| **Maturity** | Very mature | Newer, rapidly improving |

```python
# Use fsspec when:
# - You need caching
# - You need broad auth options (profiles, SAS tokens)
# - You're already using fsspec elsewhere (Dask, xarray)

# Use obstore when:
# - Maximum throughput is critical
# - You're building a high-performance pipeline
# - You want lower per-request latency

# Use Icechunk when:
# - You need versioning, branching, or time-travel
# - Multiple writers need atomic commits
# - Regulatory requirements demand audit trails
```

---

## Issue 4: Icechunk Version Conflicts

**Symptoms:**
- `ConflictError` when calling `store.commit()`
- Commits succeed but data appears corrupted
- Two writers overwrite each other's changes

**Cause:** Two processes attempted to commit to the same branch simultaneously. Icechunk uses optimistic concurrency — the second commit will fail if the branch moved since the store was opened.

**Solution:**

```python
from icechunk import IcechunkStore, StorageConfig

storage = StorageConfig.s3_from_env(bucket="my-bucket", prefix="data.zarr")

# ── Fix 1: Retry with rebase ──
import time

def commit_with_retry(store, message, max_retries=3):
    for attempt in range(max_retries):
        try:
            return store.commit(message)
        except Exception as e:
            if "conflict" in str(e).lower() and attempt < max_retries - 1:
                print(f"Conflict on attempt {attempt + 1}, rebasing...")
                store.rebase()  # pull latest changes and reapply local changes
                time.sleep(0.5 * (attempt + 1))
            else:
                raise

# ── Fix 2: Use separate branches for parallel writers ──
# Writer 1
store1 = IcechunkStore.open_existing(storage=storage, mode="w")
store1.new_branch("writer-1")
store1.checkout(branch="writer-1")
# ... write data ...
store1.commit("Writer 1 batch")

# Writer 2
store2 = IcechunkStore.open_existing(storage=storage, mode="w")
store2.new_branch("writer-2")
store2.checkout(branch="writer-2")
# ... write data ...
store2.commit("Writer 2 batch")

# Merge branches later (application-level merge)
```

---

## Issue 5: CORS Errors When Accessing from Browser

**Symptoms:**
- `Access to XMLHttpRequest has been blocked by CORS policy`
- JavaScript Zarr clients (zarr.js, xarray-js) cannot read the store
- Works from Python but fails from a web application

**Cause:** The cloud storage bucket does not have CORS configured to allow requests from the web application's origin.

**Solution:**

```json
// S3 CORS configuration (set via AWS Console or CLI)
// aws s3api put-bucket-cors --bucket my-bucket --cors-configuration file://cors.json
{
    "CORSRules": [
        {
            "AllowedHeaders": ["*"],
            "AllowedMethods": ["GET", "HEAD"],
            "AllowedOrigins": ["https://my-app.example.com"],
            "ExposeHeaders": ["ETag", "Content-Length", "Content-Range"],
            "MaxAgeSeconds": 3600
        }
    ]
}
```

```bash
# GCS CORS configuration
# gsutil cors set cors.json gs://my-bucket

# Azure Blob CORS — set via Azure Portal > Storage Account > CORS
```

---

## Issue 6: Connection Timeout on Large Stores

**Symptoms:**
- `TimeoutError` or `ConnectionError` when opening a Zarr group
- Opening the store takes minutes before any data can be read
- `zarr.open_group()` hangs on stores with millions of chunks

**Cause:** Without consolidated metadata (v2) or a small metadata footprint (v3 with sharding), opening a large Zarr store requires listing all objects in the store, which can be extremely slow on cloud storage.

**Solution:**

```python
import zarr

# ── Fix 1: Consolidate metadata (Zarr v2 stores) ──
# Run once after creating or updating the store
zarr.consolidate_metadata("s3://my-bucket/data.zarr")

# Then open with consolidated metadata
root = zarr.open_consolidated("s3://my-bucket/data.zarr", mode="r")

# ── Fix 2: Use Zarr v3 with sharding ──
# Sharding reduces object count dramatically
arr = zarr.create_array(
    store="s3://my-bucket/sharded.zarr",
    shape=(100000, 100000),
    chunks=(100, 100),
    shards=(10000, 10000),  # 100x100 chunks per shard
    dtype="float32",
)

# ── Fix 3: Increase timeout for initial listing ──
from zarr.storage import FsspecStore
store = FsspecStore.from_url(
    "s3://my-bucket/data.zarr",
    storage_options={
        "config_kwargs": {"connect_timeout": 60, "read_timeout": 120},
    },
)
```

---

## Issue 7: Cost Optimization for Cloud Zarr

**Symptoms:**
- Unexpectedly high cloud storage bills
- S3 GET request costs dominate (not storage costs)
- Egress charges from reading data across regions

**Cause:** Cloud storage costs come from three sources: (1) storage volume, (2) number of requests (GET/PUT), and (3) data transfer (egress). Small Zarr chunks generate many requests; cross-region reads incur egress charges.

**Solution:**

```python
# ── Strategy 1: Increase chunk size to reduce request count ──
# 100x100 float32 chunks = 40 KB each = too many requests
# 1000x1000 float32 chunks = 4 MB each = better
arr = zarr.create_array(
    store="s3://my-bucket/cost-optimized.zarr",
    shape=(50000, 50000),
    chunks=(1000, 1000),  # ~4 MB per chunk
    dtype="float32",
)

# ── Strategy 2: Use sharding to reduce object count ──
arr = zarr.create_array(
    store="s3://my-bucket/sharded.zarr",
    shape=(50000, 50000),
    chunks=(100, 100),
    shards=(5000, 5000),  # few large shard files
    dtype="float32",
)

# ── Strategy 3: Use S3 Intelligent-Tiering for infrequently accessed data ──
# Configure via S3 bucket lifecycle policy (not Zarr-specific)

# ── Strategy 4: Co-locate compute and storage ──
# Run analysis in the same region as the data to avoid egress
# e.g., use us-west-2 EC2 for data stored in us-west-2 S3

# ── Strategy 5: Use compression to reduce storage and transfer ──
arr = zarr.create_array(
    store="s3://my-bucket/compressed.zarr",
    shape=(50000, 50000),
    chunks=(1000, 1000),
    dtype="float32",
    compressors=zarr.codecs.ZstdCodec(level=5),  # good ratio
)
```

# Cloud Storage Patterns — Deep Reference

| Section | Lines | Description |
|---------|-------|-------------|
| Object Store Fundamentals | 15-51 | S3/GCS semantics, eventual consistency, request pricing |
| Zarr on Cloud Storage | 53-109 | How Zarr maps chunks to objects, key naming conventions |
| Latency vs Throughput | 111-167 | Per-request overhead, optimal request size, parallel reads |
| Authentication and Configuration | 169-253 | boto3/s3fs config, GCS credentials, fsspec setup |
| Caching Strategies | 255-313 | fsspec cache, block cache, local staging |
| Cost Optimization | 315-362 | Request minimization, storage class selection, egress |
| Benchmarking on Cloud vs Local | 364-429 | Network variability, warm-up effects, region selection |

---

## Object Store Fundamentals

Cloud object stores (Amazon S3, Google Cloud Storage) provide flat key-value storage where each "object" is identified by a unique key string within a bucket. Unlike POSIX filesystems, there are no true directories — the `/` delimiter in keys is purely conventional.

### Key Semantics

- **PUT**: Upload an entire object atomically. Objects are immutable once written; updates require a full replacement.
- **GET**: Retrieve an entire object or a byte range within an object.
- **LIST**: Enumerate keys matching a prefix. Can be expensive at scale (paginated, 1000 keys per page).
- **DELETE**: Remove an object. Deletion is eventual.

### Consistency Model

- **S3**: Strong read-after-write consistency for PUT and DELETE operations (since December 2020). All GET requests after a successful PUT will return the new data.
- **GCS**: Strong global consistency for all operations.

Despite strong consistency guarantees, metadata operations (LIST) may still show stale results briefly in edge cases. For benchmarking purposes, ensure all objects are fully written before starting reads.

### Request Pricing

Object store pricing has two components relevant to chunking:

1. **Per-request cost**: Each GET/PUT request incurs a fixed cost (e.g., $0.0004 per 1,000 GET requests on S3 Standard).
2. **Data transfer cost**: Egress charges apply when data crosses region boundaries or leaves the cloud provider.

**Chunking implication**: Smaller chunks mean more objects, which means more GET requests for the same volume of data. A dataset with 100,000 tiny chunks costs 100x more in request fees than one with 1,000 larger chunks, even if total bytes transferred are identical.

### Storage Classes

| Class | Use Case | Retrieval Penalty |
|-------|----------|-------------------|
| S3 Standard / GCS Standard | Frequent access | None |
| S3 Intelligent-Tiering | Variable access | None (auto-manages) |
| S3 Infrequent Access | Rarely read | Per-GB retrieval fee |
| S3 Glacier | Archival | Minutes to hours |

For active benchmarking, always use Standard class to avoid retrieval delays contaminating timing measurements.

## Zarr on Cloud Storage

Zarr stores multi-dimensional arrays as collections of compressed chunk files arranged in a directory hierarchy. On cloud object stores, each chunk becomes a separate object.

### Directory Layout (Zarr v2)

A Zarr array with shape `(1000, 2048, 2048)` and chunks `(100, 512, 512)` stored at `s3://bucket/data.zarr/` creates:

```
s3://bucket/data.zarr/
  .zarray          # Array metadata (shape, chunks, dtype, compressor)
  .zattrs          # User attributes
  0.0.0            # Chunk at index (0, 0, 0)
  0.0.1            # Chunk at index (0, 0, 1)
  0.0.2
  0.0.3
  0.1.0
  ...
  9.3.3            # Chunk at index (9, 3, 3)
```

Total number of chunk objects: `(1000/100) * (2048/512) * (2048/512) = 10 * 4 * 4 = 160`

### Key Naming Convention

Chunk keys use `.` as the dimension separator by default in Zarr v2:

```
{dim0_index}.{dim1_index}.{dim2_index}
```

Zarr v3 uses `/` as the separator, creating a deeper key hierarchy:

```
c/0/0/0
c/0/0/1
```

### Metadata Objects

- **`.zarray`**: JSON containing shape, chunks, dtype, fill_value, order, compressor, and filters. Read once at array open time.
- **`.zattrs`**: JSON containing arbitrary user metadata. Also read once at open time.
- **`.zgroup`**: For Zarr groups (directories), identifies a group node.

### Impact on LIST Operations

Opening a Zarr dataset triggers LIST operations to discover available arrays and groups. With many arrays or deeply nested groups, this can add significant latency at open time. Consolidating metadata with `zarr.consolidate_metadata()` reduces this to a single GET for the `.zmetadata` file.

### Chunk Size on Disk

The on-disk (in-object) size of a chunk depends on:

1. **Uncompressed size**: `prod(chunk_shape) * dtype.itemsize`
2. **Compression ratio**: Depends on data entropy and compressor choice
3. **Typical range**: Scientific data often compresses 2x-10x

For cloud storage, target chunk objects between **1 MB and 100 MB** after compression. This balances per-request overhead against parallelism.

## Latency vs Throughput

Understanding the difference between latency and throughput is critical for choosing chunk sizes on cloud storage.

### Per-Request Overhead

Every S3/GCS GET request incurs fixed overhead:

- **DNS resolution**: ~1 ms (cached after first request)
- **TCP connection**: ~5-15 ms (reused with connection pooling)
- **TLS handshake**: ~10-30 ms (reused with connection pooling)
- **S3 request processing**: ~5-20 ms
- **First-byte latency**: ~20-100 ms total

This means a 1 KB chunk and a 10 MB chunk both pay the same ~50 ms overhead before data starts flowing. Small chunks are therefore latency-dominated.

### Optimal Request Size

Based on S3 benchmarks (including Nguyen et al. 2023):

| Chunk Size (compressed) | Overhead Fraction | Throughput Efficiency |
|--------------------------|-------------------|----------------------|
| 10 KB | ~80% overhead | ~20% efficient |
| 100 KB | ~50% overhead | ~50% efficient |
| 1 MB | ~10% overhead | ~90% efficient |
| 10 MB | ~1% overhead | ~99% efficient |
| 100 MB | ~0.1% overhead | ~99.9% efficient |

**Rule of thumb**: Aim for compressed chunk sizes of at least 1 MB to achieve good throughput efficiency.

### Parallel Reads

Cloud object stores support massive parallelism. A single S3 bucket can handle thousands of concurrent GET requests. Strategies:

- **Thread pool**: Use `concurrent.futures.ThreadPoolExecutor` with 8-64 workers
- **Dask**: Automatic parallelism via task graph scheduling
- **fsspec**: Built-in async support with `aiohttp`

The optimal number of parallel requests depends on:

1. **Network bandwidth**: Each connection gets a share of available bandwidth
2. **Number of chunks needed**: More chunks means more potential parallelism
3. **Instance network limits**: Cloud instances have per-instance bandwidth caps

**Trade-off**: Many small chunks enable high parallelism but suffer from per-request overhead. Fewer large chunks reduce overhead but limit parallelism. The sweet spot depends on access patterns.

### Bandwidth Estimation

```python
# Estimate time to read N chunks of size S with P parallel connections
latency_per_request = 0.050  # 50 ms
bandwidth_per_connection = 100e6  # 100 MB/s per connection (typical)
total_bandwidth = min(P * bandwidth_per_connection, instance_bandwidth_cap)
transfer_time = (N * S) / total_bandwidth
overhead_time = (N / P) * latency_per_request
total_time = transfer_time + overhead_time
```

## Authentication and Configuration

### boto3 / S3 Configuration

For S3 access, configure credentials and region:

```python
import s3fs

# Option 1: Environment variables (recommended for benchmarking)
# AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION

# Option 2: Explicit configuration
fs = s3fs.S3FileSystem(
    key='AKIAIOSFODNN7EXAMPLE',
    secret='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
    client_kwargs={'region_name': 'us-west-2'}
)

# Option 3: AWS profiles
fs = s3fs.S3FileSystem(profile='my-profile')
```

### S3 Performance Tuning

```python
import botocore.config

config = botocore.config.Config(
    max_pool_connections=50,       # Increase connection pool
    retries={'max_attempts': 3},   # Retry on transient failures
    s3={'addressing_style': 'virtual'},  # Virtual-hosted addressing
)
```

### GCS Configuration

```python
import gcsfs

# Option 1: Application default credentials
fs = gcsfs.GCSFileSystem()

# Option 2: Service account key file
fs = gcsfs.GCSFileSystem(token='/path/to/service-account.json')

# Option 3: Anonymous access (public buckets)
fs = gcsfs.GCSFileSystem(token='anon')
```

### fsspec Configuration

fsspec provides a unified interface for multiple storage backends:

```python
import fsspec

# S3
fs = fsspec.filesystem('s3', anon=False)

# GCS
fs = fsspec.filesystem('gcs', token='cloud')

# Local (for comparison benchmarks)
fs = fsspec.filesystem('file')

# Open Zarr with any backend
import xarray as xr
ds = xr.open_zarr(
    fsspec.get_mapper('s3://bucket/data.zarr', anon=False),
    consolidated=True
)
```

### Region Configuration

**Critical for benchmarking**: Ensure compute and storage are in the same region. Cross-region reads add 20-200 ms of latency and incur egress charges.

```python
# Verify bucket region
import boto3
s3 = boto3.client('s3')
response = s3.get_bucket_location(Bucket='my-bucket')
print(response['LocationConstraint'])  # e.g., 'us-west-2'
```

## Caching Strategies

Caching can dramatically affect benchmark results. Understand and control caching at every level.

### fsspec Block Cache

fsspec can cache object data locally to avoid repeated downloads:

```python
fs = fsspec.filesystem(
    'blockcache',
    target_protocol='s3',
    cache_storage='/tmp/fsspec_cache',
    target_options={'anon': False}
)
```

**For benchmarking**: Disable or clear this cache between runs to measure true read performance.

### Operating System Page Cache

The OS caches recently read file data in memory. For local Zarr stores, this makes repeated reads artificially fast.

**Clear before each benchmark run:**

```bash
# macOS
sudo purge

# Linux
sync && sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'
```

### Local Staging

For reproducible cloud benchmarks, consider staging data locally first:

```python
# Download once, benchmark repeatedly
import shutil
fs = fsspec.filesystem('s3', anon=False)
fs.get('s3://bucket/data.zarr', '/local/data.zarr', recursive=True)
```

This isolates chunking effects from network variability but does not reflect production cloud access performance.

### Zarr Chunk Cache

Zarr itself can cache decompressed chunks in memory via `zarr.LRUStoreCache`:

```python
import zarr

store = zarr.storage.FSStore('s3://bucket/data.zarr')
cache = zarr.LRUStoreCache(store, max_size=2**30)  # 1 GB cache
root = zarr.open(cache, mode='r')
```

**For benchmarking**: Do not use LRU caching. Each run should read from storage.

## Cost Optimization

Chunk size directly affects cloud storage costs. Understanding the cost model helps justify rechunking investments.

### Request Minimization

Fewer, larger chunks reduce the number of GET requests:

```
Cost per access = (num_chunks_read * cost_per_GET) + (bytes_read * cost_per_GB)
```

Example for reading a single time slice from a 3D dataset:

| Chunk Shape | Chunks Read | GET Cost | Data Cost | Total |
|-------------|-------------|----------|-----------|-------|
| (1, 2048, 2048) | 1 | $0.0000004 | $0.000015 | $0.000015 |
| (1, 512, 512) | 16 | $0.0000064 | $0.000015 | $0.000022 |
| (1, 64, 64) | 1,024 | $0.0004 | $0.000015 | $0.000415 |

At scale (millions of accesses), these differences become significant.

### Storage Class Selection

Choose storage classes based on access frequency:

- **Standard**: Data accessed multiple times per month
- **Infrequent Access**: Data accessed less than once per month (30-day minimum storage)
- **Intelligent Tiering**: When access patterns are unpredictable

### Egress Costs

Data leaving a cloud provider incurs egress charges ($0.05-0.09/GB on AWS). Strategies to minimize:

1. **Co-locate compute and storage**: Run benchmarks in the same region as the data
2. **Use cloud-native compute**: Process data within the cloud rather than downloading
3. **Compress effectively**: Better compression reduces bytes transferred
4. **Read only needed chunks**: Proper chunking alignment avoids reading unnecessary data

### Cost-Benefit of Rechunking

Rechunking has a one-time cost (read all data + write all data). Calculate break-even:

```python
rechunk_cost = 2 * dataset_size_gb * egress_cost_per_gb  # read + write
savings_per_access = old_access_cost - new_access_cost
break_even_accesses = rechunk_cost / savings_per_access
```

## Benchmarking on Cloud vs Local

Cloud benchmarking introduces variability not present in local testing. Account for these factors.

### Network Variability

Cloud network performance varies due to:

- **Shared infrastructure**: Other tenants compete for bandwidth
- **Time of day**: Peak usage patterns affect performance
- **Endpoint load**: S3 partitions may be unevenly loaded

**Mitigation**: Run more benchmark iterations (10-20 instead of 5) and report confidence intervals.

### Warm-Up Effects

The first few requests to an S3 prefix may be slower due to:

- **Connection pool initialization**: First requests establish TCP/TLS connections
- **S3 request routing**: S3 optimizes routing after initial requests to a prefix
- **DNS caching**: First lookup is slower

**Mitigation**: Perform 2-3 warm-up reads before starting timed measurements. Discard warm-up timings.

```python
# Warm-up phase
for _ in range(3):
    _ = ds.isel(time=0).compute()

# Timed phase
timings = []
for i in range(num_runs):
    start = time.perf_counter()
    _ = ds.isel(time=i).compute()
    timings.append(time.perf_counter() - start)
```

### Region Selection

Choose a benchmark region based on:

1. **Data location**: Always benchmark in the same region as the data
2. **Instance availability**: Some instance types are region-limited
3. **Consistency**: Use the same region for all benchmark runs in a comparison

### Instance Selection

For reproducible benchmarks, document and fix:

- **Instance type**: CPU count, memory, network bandwidth
- **EBS vs instance store**: Instance store has lower latency for local staging
- **Enhanced networking**: Ensure enabled for high-throughput instances

### Comparing Cloud and Local Results

Cloud and local benchmarks measure different things:

| Factor | Local | Cloud |
|--------|-------|-------|
| Latency per chunk | ~0.1 ms | ~50 ms |
| Bandwidth | 500-3000 MB/s (SSD) | 100-1000 MB/s (network) |
| Variability | Low | Medium-High |
| Cache effects | Strong (OS cache) | Minimal (remote) |
| Cost sensitivity | None | Per-request + egress |

**Recommendation**: If the production workload runs on cloud storage, benchmark on cloud storage. Local benchmarks are useful for isolating chunk-shape effects from network effects.

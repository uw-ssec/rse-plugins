---
name: zarr-fundamentals
description: Work with the Zarr array storage format for chunked, compressed, N-dimensional arrays. Covers array creation, hierarchical groups, metadata/attributes, advanced indexing modes, data types, thread/process safety, sharding, and Zarr v2 vs v3 differences.
metadata:
  references:
    - references/patterns.md
    - references/examples.md
    - references/common-issues.md
---

# Zarr Fundamentals

Master **Zarr**, the cloud-native format for chunked, compressed, N-dimensional arrays. This skill covers the full Zarr-Python 3 API for both v2 and v3 format specifications.

**Official Documentation**: https://zarr.readthedocs.io/
**Zarr Specification**: https://zarr-specs.readthedocs.io/
**GitHub**: https://github.com/zarr-developers/zarr-python

## Quick Reference Card

### Installation

```bash
pixi add zarr numpy numcodecs        # pixi (recommended)
pip install zarr[extra]               # pip
pip install zarr[remote]              # cloud backends
```

### Essential Operations

```python
import zarr
import numpy as np

# Create array (v3 format, default)
z = zarr.create_array(store="data.zarr", shape=(10000, 10000), chunks=(1000, 1000), dtype="float32")
z[:] = np.random.randn(10000, 10000).astype("float32")

# Open existing
z = zarr.open_array("data.zarr", mode="r")
subset = z[0:100, 0:100]

# Groups
root = zarr.open_group("experiment.zarr", mode="w")
obs = root.create_group("observations")
arr = obs.create_array("temperature", shape=(365, 180, 360), chunks=(30, 90, 180), dtype="float32")

# Metadata
root.attrs["project"] = "Climate Study 2025"
arr.attrs["units"] = "Celsius"
print(root.tree())
```

### Decision Tree

```
Working with chunked N-dimensional arrays? → Zarr is ideal
Need cloud-native storage (S3/GCS/Azure)?  → Zarr + cloud backend (see cloud-storage-backends skill)
Need parallel read/write?                   → Zarr supports concurrent access natively
Need versioning / ACID transactions?        → Icechunk with Zarr
Need to reduce object count on cloud?       → Zarr v3 sharding
Working with existing v2 data?              → zarr-python 3 supports both v2 and v3
```

## Zarr v2 vs v3 Differences

| Feature | v2 | v3 |
|---------|----|----|
| Metadata file | `.zarray`, `.zgroup`, `.zattrs` | `zarr.json` (single) |
| Default compressor | Blosc | Zstd |
| Sharding | No | Yes (ZEP 0002) |
| Async I/O | No | Yes (native asyncio) |
| Python | 3.10+ | 3.11+ |
| Chunk key format | `0.0.0` (dot) | `c/0/0/0` (path) |
| Codec system | Single compressor + filters | Composable pipeline |

**Default to v3** for new projects. Use `zarr_format=2` only for backward compatibility.

## Core Concepts

### 1. Array Creation

```python
z = zarr.create_array(store="data.zarr", shape=(5000, 5000), chunks=(500, 500), dtype="float64",
                      fill_value=0.0, compressors=zarr.codecs.ZstdCodec(level=3))

# Convenience: zarr.zeros(), zarr.ones(), zarr.full(), zarr.empty()
```

### 2. I/O Modes

| Mode | Description |
|------|-------------|
| `'r'` | Read-only (error if not found) |
| `'r+'` | Read/write (must exist) |
| `'w'` | Write (overwrite if exists) |
| `'w-'` | Create (error if exists) |
| `'a'` | Append (create or open) |

### 3. Group Management

Groups provide HDF5-like hierarchical organization. Create with `root.create_group("name")`, navigate with `root["path/to/child"]`, list with `root.keys()`, and inspect with `root.tree()`.

### 4. Metadata and Attributes

Every array and group has `.attrs` for key-value metadata. Use CF Conventions attributes (`units`, `long_name`, `standard_name`) for scientific data. Use `.info` for quick summaries and `.info_complete()` for detailed stats (slow on large arrays).

### 5. Indexing Modes

| Mode | Syntax | Returns |
|------|--------|---------|
| Basic slicing | `z[0:100, 0:100]` | Contiguous subarray |
| Coordinate | `z.vindex[rows, cols]` | Values at (row, col) pairs |
| Mask | `z.vindex[bool_mask]` | 1D array of True-masked values |
| Orthogonal | `z.oindex[rows, cols]` | Cartesian product (rows × cols) |
| Block | `z.blocks[0, 0]` | Entire chunk blocks by index |
| Field | `z["field_name"]` | Structured dtype field |

→ See [references/patterns.md](references/patterns.md) Pattern 4 for detailed indexing examples.

### 6. Data Types

Zarr supports: all NumPy numeric types (int8–int64, uint8–uint64, float16–float64, complex64/128), bool, fixed-length strings (`S10`), datetime64, timedelta64, structured/compound dtypes, and variable-length strings (v2 only via `VLenUTF8`).

### 7. Thread and Process Safety

- **Reads**: Thread-safe without synchronization
- **Writes**: Safe when writing to non-overlapping chunks (no locks needed)
- **Overlapping writes**: Use `ThreadSynchronizer` (v2) or `ProcessSynchronizer` (v2)
- **Blosc + multiprocessing**: Set `blosc.use_threads = False` to prevent silent corruption
- **v3 async**: Configure with `zarr.config.set({"async.concurrency": 64})`

### 8. Sharding (v3 Only)

Groups multiple chunks into larger shard files to reduce object count on cloud stores.

```python
z = zarr.create_array(store="sharded.zarr", shape=(10000, 10000),
                      chunks=(2500, 2500), shards=(500, 500), dtype="float32")
```

- Without sharding: 100 GB @ 1 MB chunks = 100,000 objects
- With sharding (1 GB shards): same data = 100 objects
- Reads still access individual inner chunks via byte-range requests

## Best Practices

| Area | Guidance |
|------|----------|
| Chunk size | 1–10 MB for cloud, 100 KB–1 MB for local |
| Fill value | Use `np.nan` for floats, not 0 if 0 is valid |
| Precision | Prefer float32 over float64 when possible (2× savings) |
| Metadata | Always set `units`, `long_name`; follow CF Conventions |
| Cloud | Use sharding (v3) + consolidated metadata |
| Concurrency | Write to non-overlapping chunks; set `blosc.use_threads = False` |
| Safety | Use `mode="r"` for reads, `mode="w-"` to prevent overwrites |

## References

- **Patterns**: [references/patterns.md](references/patterns.md) — hierarchical stores, remote access, appending, indexing, sharding, concurrency
- **Examples**: [references/examples.md](references/examples.md) — full working examples with real-world datasets
- **Common Issues**: [references/common-issues.md](references/common-issues.md) — v2/v3 confusion, metadata persistence, memory errors, concurrency bugs
- **Quickstart Script**: [assets/zarr-quickstart.py](assets/zarr-quickstart.py) — runnable demo

## External Links

- **Zarr docs**: https://zarr.readthedocs.io/
- **Zarr spec**: https://zarr-specs.readthedocs.io/
- **numcodecs**: https://numcodecs.readthedocs.io/
- **xarray Zarr I/O**: https://docs.xarray.dev/en/stable/user-guide/io.html#zarr
- **Cloud-Native Zarr Guide**: https://guide.cloudnativegeo.org/zarr/

---
name: zarr-fundamentals
description: Work with the Zarr array storage format for chunked, compressed, N-dimensional arrays. Covers array creation, hierarchical groups, metadata/attributes, advanced indexing modes, data types, thread/process safety, sharding, and Zarr v2 vs v3 differences. Use when the user asks about Zarr arrays, .zarr files, zarr-python, zarr stores, chunked array storage, or cloud-optimized scientific array storage.
metadata:
  references:
    - references/patterns.md
    - references/examples.md
    - references/common-issues.md
---

# Zarr Fundamentals

Zarr-Python 3 API for chunked, compressed, N-dimensional array storage in both v2 and v3 formats.

**Docs**: https://zarr.readthedocs.io/ | **Spec**: https://zarr-specs.readthedocs.io/ | **numcodecs**: https://numcodecs.readthedocs.io/

## Resources

| Resource | Purpose |
|----------|---------|
| [references/patterns.md](references/patterns.md) | Patterns: hierarchical stores, remote access, appending, advanced indexing, sharding, concurrency |
| [references/examples.md](references/examples.md) | Full working examples with real-world datasets |
| [references/common-issues.md](references/common-issues.md) | v2/v3 confusion, metadata persistence, memory errors, concurrency bugs |
| [assets/zarr-quickstart.py](assets/zarr-quickstart.py) | Runnable quickstart demo |

## Installation

```bash
pixi add zarr numpy numcodecs   # pixi
pip install zarr[extra]          # pip (includes numcodecs + optional deps)
pip install zarr[remote]         # adds cloud backends (s3fs, gcsfs, adlfs)
```

## Core Operations

```python
import zarr
import numpy as np

# Create (v3 default)
z = zarr.create_array("data.zarr", shape=(10000, 10000), chunks=(1000, 1000), dtype="float32")
z[:] = np.random.randn(10000, 10000).astype("float32")

# Open existing (read-only)
z = zarr.open_array("data.zarr", mode="r")
subset = z[0:100, 0:100]

# Groups
root = zarr.open_group("experiment.zarr", mode="w")
obs = root.create_group("observations")
arr = obs.create_array("temperature", shape=(365, 180, 360), chunks=(30, 90, 180), dtype="float32")
root.attrs["project"] = "Climate Study 2025"
arr.attrs["units"] = "Celsius"
print(root.tree())
```

## I/O Modes

| Mode | Description |
|------|-------------|
| `'r'` | Read-only (error if not found) |
| `'r+'` | Read/write (must exist) |
| `'w'` | Write (overwrite if exists) |
| `'w-'` | Create (error if exists — safe default for new stores) |
| `'a'` | Append (create or open) |

## Zarr v2 vs v3

| Feature | v2 | v3 |
|---------|----|----|
| Metadata file | `.zarray` / `.zgroup` / `.zattrs` | `zarr.json` (single file) |
| Default compressor | Blosc | Zstd |
| Sharding | No | Yes |
| Async I/O | No | Yes (native asyncio) |
| Chunk key format | `0.0.0` (dot-separated) | `c/0/0/0` (path) |
| Codec system | Single compressor + filters | Composable pipeline |

Default to v3 for new projects. Use `zarr_format=2` only for backward compatibility.

## Indexing Modes

| Mode | Syntax | Returns |
|------|--------|---------|
| Basic slicing | `z[0:100, 0:100]` | Contiguous subarray |
| Coordinate | `z.vindex[rows, cols]` | Values at (row, col) pairs |
| Mask | `z.vindex[bool_mask]` | 1D array of True-masked values |
| Orthogonal | `z.oindex[rows, cols]` | Cartesian product (rows × cols) |
| Block | `z.blocks[0, 0]` | Entire chunk blocks by index |

## Thread and Process Safety

- Reads: thread-safe without synchronization.
- Writes to **non-overlapping chunks**: safe concurrently.
- Writes to the **same chunk**: use `ThreadSynchronizer` (v2) or partition work so chunks don't overlap.
- Blosc + multiprocessing: always set `blosc.use_threads = False` before forking to prevent silent data corruption.
- v3 async concurrency: `zarr.config.set({"async.concurrency": 64})`.

**Safe concurrent write workflow:**
```python
from numcodecs import blosc
blosc.use_threads = False  # set before any forked workers start

# Partition by non-overlapping index ranges, then write concurrently
# e.g. worker 0 writes z[0:500, :], worker 1 writes z[500:1000, :]
```

## Sharding (v3 Only)

Reduces cloud object count by grouping multiple inner chunks into larger shard files.

```python
z = zarr.create_array("sharded.zarr", shape=(10000, 10000),
                      chunks=(2500, 2500), shards=(500, 500), dtype="float32")
# 100 GB @ 1 MB inner chunks: 100,000 objects without sharding → ~100 with sharding
```

## Best Practices

| Area | Guidance |
|------|----------|
| Chunk size | 1–10 MB for cloud, 100 KB–1 MB for local |
| Fill value | Use `np.nan` for floats when 0 is a valid data value |
| Precision | Prefer float32 over float64 when sufficient (2× storage savings) |
| Metadata | Set `units`, `long_name`; follow CF Conventions for scientific data |
| Cloud | Use sharding (v3) + `zarr.consolidate_metadata()` for v2 |
| Safety | Use `mode="r"` for reads; `mode="w-"` to prevent accidental overwrites |

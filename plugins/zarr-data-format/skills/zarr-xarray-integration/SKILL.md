---
name: zarr-xarray-integration
description: Integrates Zarr with xarray and Dask for labeled, multi-dimensional scientific data workflows. Covers reading and writing Zarr stores with xarray, append and region-write operations, multi-file virtual datasets, Dask chunk alignment with Zarr chunks, encoding configuration, consolidated metadata, and performance optimization. Use when the user asks about reading or writing Zarr stores with xarray, aligning Dask chunks with Zarr arrays, or optimizing large-scale multi-dimensional data pipelines.
metadata:
  references:
    - references/patterns.md
    - references/examples.md
    - references/common-issues.md
---

# Zarr + xarray Integration

Use xarray as the high-level interface for reading, writing, and analyzing Zarr datasets, with Dask for parallel out-of-core computation.

## Resources

| Resource | Purpose |
|----------|---------|
| [references/patterns.md](references/patterns.md) | Full patterns: cloud reads, encoding, append, region writes, chunk alignment, consolidated metadata |
| [references/examples.md](references/examples.md) | Real-world workflows |
| [references/common-issues.md](references/common-issues.md) | Chunk mismatch, append errors, memory OOM, stale consolidated metadata |
| [assets/xarray-zarr-roundtrip.py](assets/xarray-zarr-roundtrip.py) | Runnable roundtrip demo |

## Installation

```bash
pixi add xarray zarr dask numpy     # pixi
pip install xarray[complete] zarr dask[complete]  # pip
pip install zarr[remote]             # adds s3fs/gcsfs for cloud
```

## Read

```python
import xarray as xr

ds = xr.open_zarr("data.zarr")                                    # local, lazy (Dask)
ds = xr.open_zarr("s3://bucket/data.zarr", storage_options={"anon": True},
                  consolidated=True)                               # cloud, public
ds = xr.open_zarr("data.zarr", chunks={"time": 30, "lat": 90})   # explicit Dask chunks
ds = xr.open_dataset("data.zarr", engine="zarr", chunks={})       # alternative form
```

| `open_zarr` parameter | Default | Description |
|-----------------------|---------|-------------|
| `chunks` | `"auto"` | `{}` = match Zarr chunks exactly; `None` = load eagerly |
| `consolidated` | `None` | Read consolidated metadata (faster cloud opens) |
| `storage_options` | `None` | fsspec kwargs (e.g. `{"anon": True}` for public S3) |
| `decode_cf` | `True` | Decode CF conventions (times, units, masks) |
| `group` | `None` | Open a specific group within the store |

## Write

```python
# Basic write
ds.to_zarr("output.zarr", mode="w")

# With per-variable encoding (recommended)
encoding = {
    "temperature":   {"chunks": {"time": 30, "lat": 90, "lon": 180}, "dtype": "float32"},
    "precipitation": {"chunks": {"time": 30, "lat": 90, "lon": 180}, "dtype": "float32"},
}
ds.to_zarr("output.zarr", mode="w", encoding=encoding, consolidated=True)

# To cloud
ds.to_zarr("s3://bucket/output.zarr", storage_options={"key": "...", "secret": "..."}, mode="w")
```

## Append

**Step 1 — Create initial store:**
```python
ds_initial.to_zarr("timeseries.zarr", mode="w")
```
**Step 2 — Append subsequent batches:**
```python
ds_new.to_zarr("timeseries.zarr", append_dim="time")
```
**Step 3 — Validate:**
```python
ds_check = xr.open_zarr("timeseries.zarr")
expected_len = len(ds_initial.time) + len(ds_new.time)
assert ds_check.dims["time"] == expected_len, f"Expected {expected_len}, got {ds_check.dims['time']}"
```

Note: non-appended dimensions must match exactly. See [common-issues.md](references/common-issues.md) Issue 2 for conflict errors. After appending, re-consolidate metadata if `consolidated=True` was used on initial write.

## Region Writes (Parallel-Safe)

**Step 1 — Pre-allocate with `compute=False`:**
```python
ds_full.to_zarr("parallel_output.zarr", mode="w", compute=False)
```
**Step 2 — Each worker writes its own non-overlapping region:**
```python
ds_chunk.to_zarr("parallel_output.zarr", region={"time": slice(day_start, day_end)})
```
**Step 3 — Validate after all workers complete:**
```python
ds_out = xr.open_zarr("parallel_output.zarr")
assert not ds_out["temperature"].isnull().all(), "Some regions were not written"
assert ds_out.dims["time"] == 365, f"Expected 365 time steps, got {ds_out.dims['time']}"
```

Region writes require a pre-existing store (step 1). Regions must not overlap between workers.

## Dask Chunk Alignment

Dask chunks must be exact multiples of Zarr chunks to avoid redundant reads:

```python
# Best: use Zarr's native chunks
ds = xr.open_zarr("data.zarr", chunks={})

# Check alignment
for var in ds.data_vars:
    zarr_chunks = ds[var].encoding.get("chunks")
    dask_chunks = ds[var].data.chunksize
    print(f"{var}: zarr={zarr_chunks}, dask={dask_chunks}")

# Misaligned example to avoid:
# Zarr chunks = (30, 90, 180); Dask chunks = (45, ...) — 45 is not a multiple of 30
```

See [common-issues.md](references/common-issues.md) Issue 1 for performance symptoms of misaligned chunks.

## Encoding Fields

| Field | Purpose |
|-------|---------|
| `chunks` | Zarr chunk sizes (dict or tuple) |
| `dtype` | On-disk data type |
| `compressor` | Compression codec (numcodecs object or `None` for default) |
| `_FillValue` | Fill value for missing data |
| `scale_factor` / `add_offset` | CF packing parameters |

See [patterns.md Pattern 2](references/patterns.md) for complete encoding examples including CF packing.

## Performance Quick Reference

| Symptom | Fix |
|---------|-----|
| Slow cloud open | Use `consolidated=True` on write and read |
| Memory OOM on `to_zarr` | Pass Dask-backed (lazy) Dataset; do not call `.compute()` first |
| Slow reads | Align Dask chunks with Zarr chunks (`chunks={}`) |
| Stale metadata after append | Call `zarr.consolidate_metadata("store.zarr")` after each append |

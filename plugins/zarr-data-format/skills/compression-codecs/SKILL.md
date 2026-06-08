---
name: compression-codecs
description: Configures and optimizes compression for Zarr arrays. Covers all numcodecs compressors (Blosc, Zstd, LZ4, Gzip, LZMA, BZ2), pre-compression filters (Delta, Quantize, FixedScaleOffset, PackBits), codec pipelines, Blosc thread safety, and the trade-offs between compression speed and ratio. Use when the user asks about configuring compression for Zarr arrays, choosing numcodecs compressors, optimizing compression settings for chunked array storage, or debugging codec-related corruption or performance issues.
metadata:
  references:
    - references/patterns.md
    - references/examples.md
    - references/common-issues.md
---

# Compression Codecs for Zarr

Configure, select, and optimize compression codecs for Zarr arrays using **numcodecs**.

## Resources

| Resource | Purpose |
|----------|---------|
| [references/patterns.md](references/patterns.md) | Full code patterns: Blosc, LZ4, LZMA, filter pipelines, per-variable config, Dask safety |
| [references/examples.md](references/examples.md) | Real-world benchmarking and codec selection examples |
| [references/common-issues.md](references/common-issues.md) | Data corruption, poor ratio, codec-not-found, v2/v3 confusion |
| [assets/codec-comparison.py](assets/codec-comparison.py) | Runnable codec comparison benchmark script |

## Codec Selection

| Codec | Speed (compress) | Speed (decompress) | Ratio | Best For |
|-------|------------------|--------------------|-------|----------|
| Blosc+LZ4 | Very Fast | Very Fast | Low-Med | Real-time analysis, frequent reads |
| Blosc+Zstd | Medium | Fast | High | General purpose (v2 default) |
| Zstd standalone | Medium | Fast | High | Zarr v3 default |
| Blosc+LZ4HC | Slow | Very Fast | Medium | Write-once, read-many |
| Gzip | Slow | Medium | Med-High | Interop with non-Python tools |
| LZ4 standalone | Very Fast | Very Fast | Low | Maximum throughput |
| LZMA | Very Slow | Very Slow | Very High | Archival only |

## Decision Tree

```
Primary constraint?
├── STORAGE SIZE → Zstd level 9 or LZMA (archival only)
├── READ SPEED   → Blosc+LZ4 with SHUFFLE (numerical) or LZ4 standalone
├── WRITE SPEED  → LZ4(acceleration=10) or Blosc+LZ4 clevel=1
├── BALANCED     → Blosc+Zstd clevel=3 (v2) or Zstd level=3 (v3)
├── INTEROP      → Gzip (universal) or Zlib (NetCDF compat)
└── DATA TYPE
    ├── Monotonic → Delta filter + any compressor
    ├── Boolean   → PackBits + LZ4
    ├── Integer   → Blosc BITSHUFFLE
    └── Limited precision float → Quantize filter + Zstd
```

## Blosc (v2 Default)

Blosc wraps internal algorithms and adds byte-shuffling — the single most impactful setting for numerical data. Shuffle rearranges bytes to expose patterns, yielding 10–40× better ratios.

```python
from numcodecs import Blosc
Blosc(cname='zstd', clevel=5, shuffle=Blosc.SHUFFLE)    # balanced
Blosc(cname='lz4', clevel=1, shuffle=Blosc.SHUFFLE)     # max speed
Blosc(cname='zstd', clevel=9, shuffle=Blosc.BITSHUFFLE) # max ratio
```

| Parameter | Options | Default |
|-----------|---------|---------|
| `cname` | `blosclz`, `lz4`, `lz4hc`, `snappy`, `zlib`, `zstd` | `blosclz` |
| `clevel` | 0–9 | 5 |
| `shuffle` | `NOSHUFFLE` (0), `SHUFFLE` (1), `BITSHUFFLE` (2) | `SHUFFLE` |

## Blosc Thread Safety (CRITICAL)

Blosc's internal threading is **not fork-safe**. Multi-process use (Dask workers, `multiprocessing`, joblib) causes **silent data corruption**.

```python
from numcodecs import blosc
blosc.use_threads = False  # set before forking, in every worker process

# Dask distributed workers:
client.run(lambda: setattr(__import__('numcodecs').blosc, 'use_threads', False))
```

## Standalone Codecs

| Codec | Import | Key Config |
|-------|--------|------------|
| Zstd (v3 default) | `from numcodecs import Zstd` | `Zstd(level=3)` — levels 1–22 |
| LZ4 | `from numcodecs import LZ4` | `LZ4(acceleration=1)` |
| Gzip | `from numcodecs import GZip` | `GZip(level=5)` — levels 1–9 |
| Zlib | `from numcodecs import Zlib` | `Zlib(level=4)` — levels 1–9 |
| BZ2 | `from numcodecs import BZ2` | `BZ2(level=5)` — levels 1–9 |
| LZMA | `from numcodecs import LZMA` | `LZMA(preset=6)` — presets 0–9 |

## Pre-Compression Filters

| Filter | Use Case | Example |
|--------|----------|---------|
| **Delta** | Monotonic data (timestamps, indices) | `Delta(dtype='int64')` |
| **Quantize** | Reduce float precision | `Quantize(digits=3, dtype='float64')` |
| **FixedScaleOffset** | Convert floats to ints | `FixedScaleOffset(offset=273.15, scale=100, dtype='float64', astype='int32')` |
| **PackBits** | Boolean arrays (8× reduction) | `PackBits()` |

```python
# v2: filters + compressor
z = zarr.open_array('data.zarr', mode='w', shape=(10000,), dtype='int64', chunks=(1000,),
                    filters=[Delta(dtype='int64')], compressor=Blosc(cname='zstd', clevel=5))
```

## Zarr v3 Codec Pipeline

```python
# v3 default (Zstd built-in)
z = zarr.create_array(store='data.zarr', shape=(1000, 1000), chunks=(100, 100),
                      dtype='float64', zarr_format=3)

# v3 explicit compressor
z = zarr.create_array(store='data.zarr', shape=(1000, 1000), chunks=(100, 100),
                      dtype='float64', compressors=zarr.codecs.ZstdCodec(level=5))
```

## Verify Compression is Working

After creating an array, confirm compression is applied and check efficiency:

```python
import zarr

z = zarr.open_array('data.zarr', mode='r')
print(z.info)                          # shows compressor, filters, chunk shape

# Check compression ratio
ratio = z.nbytes / z.nbytes_stored
print(f"Compression ratio: {ratio:.1f}×")
# ratio < 1.1 → compression is not helping; consider different codec or shuffle setting
# ratio > 100 → check for constant data or wrong pattern

# Integrity check: read a sample and verify no NaN/Inf (indicates corruption)
import numpy as np
sample = z[0] if z.ndim > 1 else z[:100]
assert np.all(np.isfinite(sample)), "Non-finite values detected — possible corruption"
```

If corruption is suspected with Blosc, see [common-issues.md](references/common-issues.md) Issue 1.

## Key Rules

- Always use `SHUFFLE` for floats, `BITSHUFFLE` for integers
- Never use LZMA/BZ2 for frequently-read data
- Set `blosc.use_threads = False` in any multi-process environment
- Compression level has diminishing returns above 5 for most codecs
- Benchmark on real data — synthetic data gives misleading compression ratios

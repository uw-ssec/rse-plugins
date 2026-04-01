---
name: compression-codecs
description: Configure and optimize compression for Zarr arrays. Covers all numcodecs compressors (Blosc, Zstd, LZ4, Gzip, LZMA, BZ2), pre-compression filters (Delta, Quantize, FixedScaleOffset, PackBits), codec pipelines, Blosc thread safety, and the trade-offs between compression speed and ratio.
metadata:
  references:
    - references/patterns.md
    - references/examples.md
    - references/common-issues.md
---

# Compression Codecs for Zarr

Configure, select, and optimize compression codecs for Zarr arrays using **numcodecs**. This skill covers every compressor and filter in the Zarr ecosystem, thread safety for multi-process workloads, codec pipelines in Zarr v3, and performance trade-offs.

**Zarr Performance Guide**: https://zarr.readthedocs.io/en/latest/user-guide/performance/
**numcodecs Reference**: https://numcodecs.readthedocs.io/
**GitHub**: https://github.com/zarr-developers/numcodecs

## Quick Reference: Codec Selection

| Codec | Speed (compress) | Speed (decompress) | Ratio | Best For |
|-------|-------------------|---------------------|-------|----------|
| Blosc+LZ4 | Very Fast | Very Fast | Low-Med | Real-time analysis, frequent reads |
| Blosc+Zstd | Medium | Fast | High | General purpose (v2 default) |
| Zstd standalone | Medium | Fast | High | Zarr v3 default |
| Blosc+LZ4HC | Slow | Very Fast | Medium | Write-once, read-many |
| Gzip | Slow | Medium | Med-High | Interop with non-Python tools |
| LZ4 standalone | Very Fast | Very Fast | Low | Maximum throughput |
| LZMA | Very Slow | Very Slow | Very High | Archival only |

## When to Use This Skill

- Selecting a codec for a new Zarr array or dataset
- Optimizing storage size vs read/write speed
- Configuring pre-compression filters (Delta, Quantize, etc.)
- Debugging compression issues (thread safety, poor ratio, codec not found)
- Migrating between v2 and v3 codec configuration

## Core Concepts

### 1. Blosc: The Meta-Compressor (v2 Default)

Blosc wraps internal algorithms and adds **byte-shuffling** — the single most impactful setting for numerical data compression. Shuffle rearranges bytes to expose patterns, yielding 10–40× better ratios.

| Parameter | Options | Default |
|-----------|---------|---------|
| `cname` | `blosclz`, `lz4`, `lz4hc`, `snappy`, `zlib`, `zstd` | `blosclz` |
| `clevel` | 0 (none) – 9 (max) | 5 |
| `shuffle` | `NOSHUFFLE` (0), `SHUFFLE` (1), `BITSHUFFLE` (2) | `SHUFFLE` |

```python
from numcodecs import Blosc
Blosc(cname='zstd', clevel=5, shuffle=Blosc.SHUFFLE)    # balanced
Blosc(cname='lz4', clevel=1, shuffle=Blosc.SHUFFLE)     # max speed
Blosc(cname='zstd', clevel=9, shuffle=Blosc.BITSHUFFLE) # max ratio
```

### 2. Blosc Thread Safety (CRITICAL)

Blosc's internal threading is **not fork-safe**. Multi-process use (Dask workers, `multiprocessing`, joblib) can cause **silent data corruption**.

```python
from numcodecs import blosc
blosc.use_threads = False  # ALWAYS set this in multi-process environments

# For Dask distributed:
client.run(lambda: setattr(__import__('numcodecs').blosc, 'use_threads', False))
```

### 3. Standalone Codecs

| Codec | Import | Key Config |
|-------|--------|------------|
| Zstd (v3 default) | `from numcodecs import Zstd` | `Zstd(level=3)` — levels 1–22 |
| LZ4 | `from numcodecs import LZ4` | `LZ4(acceleration=1)` |
| Gzip | `from numcodecs import GZip` | `GZip(level=5)` — levels 1–9 |
| Zlib | `from numcodecs import Zlib` | `Zlib(level=4)` — levels 1–9 |
| BZ2 | `from numcodecs import BZ2` | `BZ2(level=5)` — levels 1–9 |
| LZMA | `from numcodecs import LZMA` | `LZMA(preset=6)` — presets 0–9 |

### 4. Pre-Compression Filters

Filters transform data before compression to improve ratios. Applied in order.

| Filter | Use Case | Example |
|--------|----------|---------|
| **Delta** | Monotonic data (timestamps, indices) | `Delta(dtype='int64')` |
| **Quantize** | Reduce float precision | `Quantize(digits=3, dtype='float64')` |
| **FixedScaleOffset** | Convert floats to ints | `FixedScaleOffset(offset=273.15, scale=100, dtype='float64', astype='int32')` |
| **PackBits** | Boolean arrays (8× reduction) | `PackBits()` |
| **Categorize** | String→integer encoding | `Categorize(labels=['a','b','c'], dtype='U10', astype='u1')` |

```python
# v2: filters + compressor
z = zarr.open_array('data.zarr', mode='w', shape=(10000,), dtype='int64', chunks=(1000,),
                    filters=[Delta(dtype='int64')], compressor=Blosc(cname='zstd', clevel=5))

# Chain: Delta → Quantize → compressor
filters=[Delta(dtype='float64'), Quantize(digits=3, dtype='float64')]
```

### 5. Zarr v3 Codec Pipeline

v3 replaces `compressor` + `filters` with a unified pipeline: array→array → array→bytes → bytes→bytes.

```python
import zarr

# v3 with default Zstd
z = zarr.create_array(store='data.zarr', shape=(1000, 1000), chunks=(100, 100),
                      dtype='float64', zarr_format=3)

# v3 with explicit compressor
z = zarr.create_array(store='data.zarr', shape=(1000, 1000), chunks=(100, 100),
                      dtype='float64', compressors=zarr.codecs.ZstdCodec(level=5))

# No compression
z = zarr.create_array(store='data.zarr', shape=(1000, 1000), chunks=(100, 100),
                      dtype='float64', compressors=None)
```

### 6. Codec Selection Decision Tree

```
Primary constraint?
├── STORAGE SIZE → Zstd level 9 or LZMA (archival only)
├── READ SPEED  → Blosc+LZ4 with SHUFFLE (numerical) or LZ4 standalone
├── WRITE SPEED → LZ4(acceleration=10) or Blosc+LZ4 clevel=1
├── BALANCED    → Blosc+Zstd clevel=3 (v2) or Zstd level=3 (v3)
├── INTEROP     → Gzip (universal) or Zlib (NetCDF compat)
└── DATA TYPE
    ├── Monotonic → Delta filter + any compressor
    ├── Boolean   → PackBits + LZ4
    ├── Integer   → Blosc BITSHUFFLE
    └── Limited precision float → Quantize filter + Zstd
```

## Best Practices

- **Start with defaults** (Blosc+Zstd for v2, Zstd for v3) — only change if benchmarks justify it
- **Always use shuffle** for numerical data (SHUFFLE for floats, BITSHUFFLE for ints)
- **Never use LZMA/BZ2** for frequently-read data
- **Set `blosc.use_threads = False`** in any multi-process environment
- **Benchmark on real data** — synthetic data gives misleading results
- **For cloud storage**, prioritize decompression speed over compression ratio
- Compression level has diminishing returns above level 5 for most codecs

## References

- **Patterns**: [references/patterns.md](references/patterns.md) — codec configs, filter pipelines, per-variable encoding
- **Examples**: [references/examples.md](references/examples.md) — benchmarking, real-world codec selection
- **Common Issues**: [references/common-issues.md](references/common-issues.md) — corruption, poor ratio, codec errors
- **Benchmark Script**: [assets/codec-comparison.py](assets/codec-comparison.py) — runnable codec comparison

## External Links

- **numcodecs**: https://numcodecs.readthedocs.io/
- **Blosc**: https://www.blosc.org/
- **Zstandard**: https://facebook.github.io/zstd/
- **Squash Benchmark**: https://quixdb.github.io/squash-benchmark/

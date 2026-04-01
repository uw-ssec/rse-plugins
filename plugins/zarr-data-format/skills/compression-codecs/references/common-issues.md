# Common Issues and Solutions

## Contents

| Issue | Description |
|-------|-------------|
| 1. Silent Data Corruption with Blosc | Multi-process threading conflict |
| 2. Poor Compression Ratio | Wrong codec or missing shuffle |
| 3. Slow Decompression | Using archival codecs for active data |
| 4. Codec Not Found | Missing codec in target environment |
| 5. v2 vs v3 Codec Configuration Confusion | Different parameter names |
| 6. Filter Order Matters | Wrong filter chain order |
| 7. Shuffle Mode Selection | SHUFFLE vs BITSHUFFLE for different dtypes |

---

## Issue 1: Silent Data Corruption with Blosc in Multi-Process

**Symptoms:** Arrays contain wrong values; checksums don't match; corruption is intermittent and hard to reproduce.

**Cause:** Blosc's internal threading conflicts with Python `fork()`. When a forked child process shares Blosc thread state from the parent, concurrent compression operations corrupt each other's buffers.

**Solution:**

```python
from numcodecs import blosc
blosc.use_threads = False  # SET THIS BEFORE ANY ZARR OPERATIONS

# For multiprocessing.Pool:
def worker_init():
    from numcodecs import blosc
    blosc.use_threads = False

pool = multiprocessing.Pool(4, initializer=worker_init)

# For Dask distributed:
client.run(lambda: setattr(__import__('numcodecs').blosc, 'use_threads', False))
```

This is the **#1 source of subtle Zarr bugs** in production systems.

---

## Issue 2: Poor Compression Ratio

**Symptoms:** Compressed size is nearly the same as raw; ratio below 2×; storage costs not reduced as expected.

**Cause:** Most commonly: shuffle is disabled (`NOSHUFFLE`) for numerical data; or using a standalone codec (Zstd, LZ4) instead of Blosc which adds shuffle.

**Solution:**

```python
from numcodecs import Blosc

# WRONG: standalone Zstd without shuffle (typically 4-8× ratio)
from numcodecs import Zstd
compressor = Zstd(level=5)

# RIGHT: Blosc + Zstd with shuffle (typically 50-200× ratio on numerical data)
compressor = Blosc(cname='zstd', clevel=5, shuffle=Blosc.SHUFFLE)

# For integer data, try BITSHUFFLE:
compressor = Blosc(cname='zstd', clevel=5, shuffle=Blosc.BITSHUFFLE)
```

---

## Issue 3: Slow Decompression

**Symptoms:** Reading data takes much longer than expected; CPU is pegged during reads.

**Cause:** Using archival codecs (LZMA, BZ2) or very high compression levels on frequently-read data.

**Solution:**

```python
# Decompression speed ranking (fastest → slowest):
# LZ4 > Blosc+LZ4 > Zstd > Gzip > Zlib > BZ2 >> LZMA

# For frequently-read data:
from numcodecs import Blosc
compressor = Blosc(cname='lz4', clevel=1, shuffle=Blosc.SHUFFLE)
```

---

## Issue 4: Codec Not Found

**Symptoms:** `ValueError: codec not available: 'blosc'` when opening a store created elsewhere.

**Cause:** The codec used to create the data is not installed in the current environment.

**Solution:**

```python
import numcodecs
print(list(numcodecs.codec_registry))  # check what's available

# Install: pip install numcodecs  (includes Blosc, Zstd, LZ4, Gzip, etc.)
# Inspect a store's codec: z = zarr.open_array("data.zarr", mode="r"); print(z.metadata)
```

---

## Issue 5: v2 vs v3 Codec Configuration

**Symptoms:** `TypeError` from wrong parameter names; compression not applied.

**Cause:** v2 uses `compressor=` (singular) + `filters=[]`, v3 uses `compressors=` (plural).

```python
# v2: compressor (singular)
z = zarr.open_array('v2.zarr', mode='w', shape=(1000,), dtype='float32',
                    zarr_format=2, compressor=Blosc(cname='zstd'))

# v3: compressors (plural)
z = zarr.create_array(store='v3.zarr', shape=(1000,), dtype='float32',
                      compressors=zarr.codecs.ZstdCodec(level=5))
```

---

## Issue 6: Filter Order Matters

**Symptoms:** Compression ratio not improved by filters; unexpected data after roundtrip.

**Cause:** Filters are applied in list order. Wrong ordering can add noise instead of reducing it.

```python
# For monotonic float data: Delta FIRST, then Quantize
filters = [Delta(dtype='float64'), Quantize(digits=3, dtype='float64')]  # ✓

# WRONG: Quantize before Delta (destroys monotonic pattern)
# filters = [Quantize(...), Delta(...)]  # ✗
```

---

## Issue 7: Shuffle Mode Selection

**Symptoms:** Suboptimal compression ratio; unsure which shuffle mode to use.

| Data Type | Best Shuffle | Why |
|-----------|-------------|-----|
| float32/float64 | `SHUFFLE` | Exponent bytes cluster at byte level |
| Small integers (uint8/int16) | `BITSHUFFLE` | Many zero high bits cluster |
| int32/int64 with small values | `BITSHUFFLE` | Same — unused high bits |
| int32/int64 with full range | `SHUFFLE` | No bit-level advantage |
| bool | Use `PackBits` filter instead | 1-bit data, shuffle irrelevant |

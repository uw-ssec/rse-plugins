# Real-World Examples

## Contents

| Example | Description |
|---------|-------------|
| 1. Benchmarking Codecs on Climate Data | Compare codecs on realistic scientific data |
| 2. Delta Filter for Monotonic Data | Timestamps and cumulative sums |
| 3. Per-Variable Compression in xarray | Different codecs per variable |
| 4. Optimizing Integer Count Data | Satellite observation counts |

---

## Example 1: Benchmarking Codecs on Climate Data

**Problem:** Choose the best codec for a float32 temperature dataset by benchmarking compression ratio, compress time, and decompress time.

```python
import time
import numpy as np
from numcodecs import Blosc, Zstd, GZip, LZ4, Zlib, BZ2

# Generate realistic correlated float32 data
rng = np.random.default_rng(42)
data = np.cumsum(rng.normal(0, 0.1, (1000, 1000)), axis=0).astype("float32")
raw_size = data.nbytes

codecs = {
    "Blosc+LZ4 SHUFFLE": Blosc(cname='lz4', clevel=1, shuffle=Blosc.SHUFFLE),
    "Blosc+Zstd SHUFFLE": Blosc(cname='zstd', clevel=5, shuffle=Blosc.SHUFFLE),
    "Zstd(3)": Zstd(level=3),
    "GZip(5)": GZip(level=5),
    "LZ4": LZ4(),
}

print(f"{'Codec':<25} {'Ratio':>8} {'Compress':>10} {'Decompress':>12}")
print("-" * 60)

for name, codec in codecs.items():
    t0 = time.perf_counter()
    compressed = codec.encode(data)
    t_compress = time.perf_counter() - t0

    t0 = time.perf_counter()
    codec.decode(compressed)
    t_decompress = time.perf_counter() - t0

    ratio = raw_size / len(compressed)
    print(f"{name:<25} {ratio:>7.1f}x {t_compress:>9.3f}s {t_decompress:>11.3f}s")
```

→ See [assets/codec-comparison.py](../assets/codec-comparison.py) for a more comprehensive benchmark script.

---

## Example 2: Delta Filter for Monotonic Data

**Problem:** Compress a monotonically increasing timestamp array. Without Delta, the compressor sees large values with small differences; with Delta, it sees small constant-ish values.

```python
import zarr
import numpy as np
from numcodecs import Delta, Blosc

# Simulated timestamps (nanoseconds since epoch, monotonically increasing)
timestamps = np.cumsum(np.random.randint(1_000_000, 10_000_000, 1_000_000)).astype("int64")

# Without Delta filter
z_no_delta = zarr.open_array('no_delta.zarr', mode='w', shape=timestamps.shape,
                             dtype='int64', chunks=(100_000,),
                             compressor=Blosc(cname='zstd', clevel=5))
z_no_delta[:] = timestamps

# With Delta filter
z_delta = zarr.open_array('with_delta.zarr', mode='w', shape=timestamps.shape,
                          dtype='int64', chunks=(100_000,),
                          filters=[Delta(dtype='int64')],
                          compressor=Blosc(cname='zstd', clevel=5))
z_delta[:] = timestamps

print(f"Without Delta: ratio from info")
print(f"With Delta: dramatically better ratio for monotonic data")
```

---

## Example 3: Per-Variable Compression in xarray

**Problem:** A climate dataset has float32 temperatures (benefits from shuffle), uint16 observation counts (benefits from BITSHUFFLE), and boolean cloud masks (benefits from PackBits).

```python
import xarray as xr
import numpy as np
from numcodecs import Blosc, PackBits

rng = np.random.default_rng(42)
ds = xr.Dataset({
    "temperature": (["time", "lat", "lon"],
                    rng.normal(280, 15, (365, 180, 360)).astype("float32")),
    "obs_count": (["time", "lat", "lon"],
                  rng.integers(0, 100, (365, 180, 360), dtype="uint16")),
    "cloud_mask": (["time", "lat", "lon"],
                   rng.integers(0, 2, (365, 180, 360), dtype="bool")),
}, coords={
    "time": np.arange(365), "lat": np.linspace(-89.5, 89.5, 180),
    "lon": np.linspace(0.5, 359.5, 360),
})

encoding = {
    "temperature": {
        "compressor": Blosc(cname='zstd', clevel=5, shuffle=Blosc.SHUFFLE),
        "chunks": {"time": 30, "lat": 90, "lon": 180},
    },
    "obs_count": {
        "compressor": Blosc(cname='zstd', clevel=5, shuffle=Blosc.BITSHUFFLE),
        "chunks": {"time": 30, "lat": 90, "lon": 180},
    },
    "cloud_mask": {
        "compressor": Blosc(cname='lz4', clevel=1),
        "filters": [PackBits()],
        "chunks": {"time": 30, "lat": 90, "lon": 180},
    },
}
ds.to_zarr("optimized_climate.zarr", encoding=encoding)
```

---

## Example 4: Optimizing Integer Count Data

**Problem:** Satellite pixel count data (uint32, range 0–10000) has lots of bit-level redundancy. BITSHUFFLE exposes this for better compression.

```python
import zarr
import numpy as np
from numcodecs import Blosc

rng = np.random.default_rng(42)
counts = rng.poisson(50, (10000, 10000)).astype("uint32")

configs = {
    "NOSHUFFLE": Blosc(cname='zstd', clevel=5, shuffle=Blosc.NOSHUFFLE),
    "SHUFFLE": Blosc(cname='zstd', clevel=5, shuffle=Blosc.SHUFFLE),
    "BITSHUFFLE": Blosc(cname='zstd', clevel=5, shuffle=Blosc.BITSHUFFLE),
}

for name, comp in configs.items():
    compressed = comp.encode(counts[:1000, :1000])
    ratio = counts[:1000, :1000].nbytes / len(compressed)
    print(f"{name:<12}: ratio={ratio:.1f}x")
# BITSHUFFLE typically wins for integer data with limited range
```

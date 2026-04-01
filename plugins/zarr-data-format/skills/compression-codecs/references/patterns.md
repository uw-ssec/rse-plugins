# Compression Codec Patterns

## Contents

| Pattern | Description |
|---------|-------------|
| 1. Default Codec (Blosc+Zstd) | General-purpose starting point |
| 2. Maximum Speed (Blosc+LZ4) | Lowest latency reads |
| 3. Maximum Compression | Archival with LZMA or Zstd level 9 |
| 4. Filter + Compressor Pipeline | Delta + Blosc for sequential data |
| 5. Per-Variable Codec Config | Different codecs per variable in xarray |
| 6. Blosc Thread Safety in Multi-Process | Correct Blosc config for Dask/multiprocessing |

---

## Pattern 1: Default Codec Configuration (Blosc+Zstd)

**When to use:** Starting a new project; general-purpose numerical arrays; balanced read/write workloads.

```python
import zarr
import numpy as np
from numcodecs import Blosc

# v2: Blosc wrapping Zstd with byte shuffle
compressor = Blosc(cname='zstd', clevel=5, shuffle=Blosc.SHUFFLE)
z = zarr.open_array('data.zarr', mode='w', shape=(5000, 5000),
                    dtype='float64', chunks=(500, 500), compressor=compressor)
z[:] = np.random.randn(5000, 5000)
print(z.info)

# v3: Zstd is the default — no explicit config needed
z_v3 = zarr.create_array(store='data_v3.zarr', shape=(5000, 5000),
                         chunks=(500, 500), dtype='float64')
```

---

## Pattern 2: Maximum Speed Configuration (Blosc+LZ4)

**When to use:** Real-time analysis, interactive exploration, latency-sensitive pipelines.

```python
from numcodecs import Blosc

# LZ4 with shuffle for fast decompression of numerical data
compressor = Blosc(cname='lz4', clevel=1, shuffle=Blosc.SHUFFLE)
z = zarr.open_array('fast.zarr', mode='w', shape=(10000, 10000),
                    dtype='float32', chunks=(1000, 1000), compressor=compressor)

# For maximum raw speed (skip shuffle):
compressor_raw = Blosc(cname='lz4', clevel=1, shuffle=Blosc.NOSHUFFLE)
# Trade-off: ~10-40× worse compression ratio without shuffle
```

---

## Pattern 3: Maximum Compression

**When to use:** Archival storage, rarely read data, minimizing cloud storage costs.

```python
from numcodecs import LZMA, Zstd, Blosc

# Option 1: LZMA (maximum ratio, very slow read/write)
z = zarr.open_array('archive.zarr', mode='w', shape=(5000, 5000),
                    dtype='float64', chunks=(500, 500), compressor=LZMA(preset=9))

# Option 2: Zstd high level (better speed than LZMA, still high ratio)
z = zarr.open_array('archive.zarr', mode='w', shape=(5000, 5000),
                    dtype='float64', chunks=(500, 500), compressor=Zstd(level=19))

# Option 3: Blosc+Zstd with BITSHUFFLE (best ratio for numerical data)
z = zarr.open_array('archive.zarr', mode='w', shape=(5000, 5000),
                    dtype='float64', chunks=(500, 500),
                    compressor=Blosc(cname='zstd', clevel=9, shuffle=Blosc.BITSHUFFLE))
```

---

## Pattern 4: Filter + Compressor Pipeline

**When to use:** Monotonic/sequential data (timestamps, indices), or limited-precision floats.

```python
import zarr
import numpy as np
from numcodecs import Delta, Quantize, Blosc, PackBits

# ── Delta + compressor for monotonic integer data ──
z = zarr.open_array('timestamps.zarr', mode='w', shape=(1_000_000,),
                    dtype='int64', chunks=(100_000,),
                    filters=[Delta(dtype='int64')],
                    compressor=Blosc(cname='zstd', clevel=5))
z[:] = np.cumsum(np.random.randint(1, 100, 1_000_000))

# ── Quantize + compressor for reducing float precision ──
z = zarr.open_array('approx.zarr', mode='w', shape=(5000, 5000),
                    dtype='float64', chunks=(500, 500),
                    filters=[Quantize(digits=3, dtype='float64')],
                    compressor=Blosc(cname='zstd', clevel=5))

# ── PackBits for boolean masks ──
z = zarr.open_array('mask.zarr', mode='w', shape=(100_000,),
                    dtype='bool', chunks=(10_000,),
                    filters=[PackBits()],
                    compressor=Blosc(cname='lz4', clevel=1))
```

---

## Pattern 5: Per-Variable Codec Configuration

**When to use:** xarray Datasets where different variables benefit from different codecs (e.g., float temperature vs integer count data vs boolean masks).

```python
import xarray as xr
import numpy as np
from numcodecs import Blosc, Delta

ds = xr.Dataset({
    "temperature": (["time", "lat", "lon"], np.random.randn(365, 180, 360).astype("float32")),
    "precipitation": (["time", "lat", "lon"], np.random.rand(365, 180, 360).astype("float32")),
    "cloud_mask": (["time", "lat", "lon"], np.random.randint(0, 2, (365, 180, 360), dtype="bool")),
})

encoding = {
    "temperature": {
        "compressor": Blosc(cname='zstd', clevel=5, shuffle=Blosc.SHUFFLE),
        "chunks": {"time": 30, "lat": 90, "lon": 180},
    },
    "precipitation": {
        "compressor": Blosc(cname='zstd', clevel=5, shuffle=Blosc.SHUFFLE),
        "chunks": {"time": 30, "lat": 90, "lon": 180},
    },
    "cloud_mask": {
        "compressor": Blosc(cname='lz4', clevel=1),
        "chunks": {"time": 30, "lat": 90, "lon": 180},
    },
}
ds.to_zarr("multi_codec.zarr", encoding=encoding)
```

---

## Pattern 6: Blosc Thread Safety in Multi-Process

**When to use:** Any multi-process environment — Dask distributed, `multiprocessing.Pool`, joblib with `loky` backend.

```python
from numcodecs import blosc

# ── Option 1: Global disable (simplest) ──
blosc.use_threads = False

# ── Option 2: Per-worker init for multiprocessing ──
import multiprocessing

def worker_init():
    from numcodecs import blosc
    blosc.use_threads = False

pool = multiprocessing.Pool(4, initializer=worker_init)

# ── Option 3: Dask distributed ──
from dask.distributed import Client
client = Client(n_workers=4)
client.run(lambda: setattr(__import__('numcodecs').blosc, 'use_threads', False))
```

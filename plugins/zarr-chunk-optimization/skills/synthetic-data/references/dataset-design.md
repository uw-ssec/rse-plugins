# Dataset Design — Deep Reference

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| Choosing Dimensions and Shapes | 18–47 | Match production data characteristics for representative benchmarks |
| Data Type Selection | 48–78 | Impact of float32 vs float64 and other dtypes on chunk size and performance |
| Compression Codec Impact | 79–122 | Benchmarking with blosc, zstd, lz4, gzip, and without compression |
| Scaling Test Data | 123–154 | Representative samples vs full-scale generation strategies |
| Reproducibility | 155–204 | Random seeds, metadata recording, and deterministic generation |
| Storage Backend Considerations | 205–249 | Local vs cloud latency, object store semantics, and regional placement |

---

Designing synthetic datasets for chunking benchmarks requires intentional choices about every parameter. A poorly designed test dataset can produce misleading benchmark results that do not translate to production performance. This reference covers the key design decisions in depth.

## Choosing Dimensions and Shapes

The number of dimensions and their relative sizes determine how chunking strategies interact with access patterns. A dataset shaped `(10, 10, 10)` will not reveal the trade-offs visible in a `(10000, 2048, 2048)` dataset.

### Match Production Aspect Ratios

If your production data has shape `(50000, 4096, 4096)`, the first dimension is roughly 12x smaller than the others. Preserve this ratio in synthetic data even when reducing total volume:

- Good: `(1000, 4096, 4096)` — preserves spatial dimensions, reduces time
- Bad: `(100, 100, 100)` — destroys the aspect ratio that drives chunking decisions

### Dimension Count

Common configurations by domain:

| Dimensions | Example Shape | Domain |
|-----------|---------------|--------|
| 2D | `(4096, 4096)` | Single images, spatial grids |
| 3D | `(1000, 2048, 2048)` | Time-series of spatial data, radio visibilities |
| 4D | `(365, 50, 180, 360)` | Atmospheric models (time, level, lat, lon) |
| 5D | `(100, 4, 50, 180, 360)` | Ensemble forecasts (member, time, level, lat, lon) |

### Minimum Sizes for Meaningful Benchmarks

Each dimension should be large enough that multiple chunks span it. A dimension of size 10 with chunk size 10 produces a single chunk along that axis, eliminating any chunking trade-off. Rules of thumb:

- At least **10 chunks** along the primary access dimension
- At least **4 chunks** along secondary dimensions
- Total dataset size of at least **1 GB** for local benchmarks, **5 GB** for cloud benchmarks

## Data Type Selection

The dtype determines the number of bytes per array element, which directly controls the in-memory and on-disk size of each chunk.

### Bytes Per Element

| dtype | Bytes | Typical Use |
|-------|-------|-------------|
| `int8` | 1 | Flags, masks, categorical |
| `int16` | 2 | Satellite radiance, elevation |
| `int32` | 4 | Counts, indices |
| `float16` | 2 | ML inference, reduced precision |
| `float32` | 4 | Most scientific data |
| `float64` | 8 | High-precision computation |
| `complex64` | 8 | Radio visibilities (real + imaginary float32) |
| `complex128` | 16 | High-precision complex data |

### Impact on Chunk Size

For a chunk shape of `(50, 256, 256)`:

- `float32`: 50 x 256 x 256 x 4 bytes = **12.5 MB** per chunk
- `float64`: 50 x 256 x 256 x 8 bytes = **25.0 MB** per chunk
- `int16`: 50 x 256 x 256 x 2 bytes = **6.25 MB** per chunk

Cloud object stores perform best with individual object sizes between 5 MB and 50 MB. Choosing the wrong dtype can push chunks outside this optimal range.

### Recommendation

Always use the same dtype as your production data. If you do not yet have production data, use `float32` as the default. It is the most common type in scientific computing and produces chunk sizes in the optimal range for most configurations.

## Compression Codec Impact

Compression affects benchmarks in two ways: it reduces the amount of data transferred from storage (faster I/O) but adds CPU cost for decompression (slower processing). The net effect depends on the data pattern, compression ratio, and storage bandwidth.

### Available Codecs

The `synthetic_data.py` script supports:

| Codec | Flag Value | Characteristics |
|-------|-----------|-----------------|
| Zstandard | `zstd` | Best ratio-to-speed balance; default choice |
| Blosc/LZ4 | `blosc` | Fastest decompression; lower ratios |
| Gzip | `gzip` | Wide compatibility; slower than blosc/zstd |
| None | `none` | No compression; measures raw I/O |

### Compression Ratios by Data Pattern

Different data patterns compress differently. This directly affects chunk sizes on disk:

| Pattern | zstd (level 3) | blosc/lz4 | gzip |
|---------|----------------|-----------|------|
| `constant` | 100–1000x | 50–500x | 80–800x |
| `temperature` | 2–5x | 1.5–3x | 2–4x |
| `radio` | 1.2–2x | 1.1–1.5x | 1.2–1.8x |
| `random` | 1.0–1.1x | 1.0–1.05x | 1.0–1.1x |

### Benchmarking With and Without Compression

To isolate the effect of compression on benchmark results, generate identical datasets with and without compression:

```bash
# With compression
python synthetic_data.py -o /tmp/compressed.zarr \
    --shape 1000,1024,1024 --chunks 50,256,256 \
    --compression zstd --seed 42

# Without compression
python synthetic_data.py -o /tmp/uncompressed.zarr \
    --shape 1000,1024,1024 --chunks 50,256,256 \
    --compression none --seed 42
```

Compare the results to determine whether compression is a net win for your storage backend and access pattern. On fast local SSDs, compression overhead may outweigh the I/O savings. On high-latency cloud storage, compression almost always helps.

## Scaling Test Data

Benchmark datasets must be large enough to produce meaningful results but small enough to generate and store practically.

### Sizing Guidelines

| Purpose | Recommended Size | Rationale |
|---------|-----------------|-----------|
| Pipeline validation | 100 MB – 1 GB | Quick generation, fast iteration |
| Local benchmarks | 1 GB – 10 GB | Large enough to measure I/O patterns |
| Cloud benchmarks | 5 GB – 50 GB | Must amortize request overhead |
| Production simulation | 50 GB – 500 GB | Full-scale performance prediction |

### Reducing Along One Dimension

The `synthetic_data.py` script and its `calculate_sample_shape` function reduce the first dimension (typically time) while preserving full resolution in other dimensions. This strategy maintains representative chunk access patterns:

- Full production shape: `(50000, 4096, 4096)` — ~3 TB at float32
- Benchmark sample: `(500, 4096, 4096)` — ~30 GB at float32
- Quick test: `(50, 4096, 4096)` — ~3 GB at float32

### Using --sample-from

If you have an existing large Zarr dataset, use the sampling feature rather than regenerating:

```bash
python synthetic_data.py --sample-from /data/full.zarr \
    --output /tmp/sample.zarr --target-size 8
```

This preserves the source dataset's chunk shape, compression, and metadata while extracting a manageable subset.

## Reproducibility

Benchmarking requires exact reproducibility. Two runs with the same parameters must produce bitwise-identical datasets.

### Random Seeds

The `--seed` flag controls all random number generation. Default is `42`. The script passes `seed + batch_offset` to `numpy.random.seed` for each batch to ensure consistent results regardless of batch size.

Key rules:

- Always specify `--seed` explicitly in benchmark scripts
- Use the same seed across all datasets in a comparison
- Document the seed in your benchmark report
- Different seeds produce statistically equivalent but numerically different data

### Metadata Recording

The script automatically stores metadata in Zarr attributes:

```python
z.attrs['dimensions']   # Dimension names
z.attrs['pattern_type'] # Data pattern used
z.attrs['created_by']   # 'synthetic_data.py'
```

For complete reproducibility, also record externally:

- Exact command line used
- Python and library versions (`zarr.__version__`, `numpy.__version__`)
- Date and machine identifier
- Any environment variables affecting storage (AWS region, credentials profile)

### Verifying Reproducibility

```python
import zarr
import numpy as np

z1 = zarr.open("/tmp/run1.zarr", mode="r")
z2 = zarr.open("/tmp/run2.zarr", mode="r")

# Check shapes match
assert z1.shape == z2.shape, f"Shape mismatch: {z1.shape} vs {z2.shape}"

# Check data is bitwise identical
assert np.array_equal(z1[:], z2[:]), "Data differs between runs"

print("Datasets are identical")
```

## Storage Backend Considerations

Where you store synthetic data affects benchmark results. Local disk, S3, and GCS have fundamentally different performance characteristics.

### Local Filesystem

- **Latency:** Sub-millisecond for SSDs, single-digit milliseconds for HDDs
- **Throughput:** 500 MB/s – 3 GB/s for NVMe SSDs
- **Best for:** Pipeline development, quick iteration, compression comparisons
- **Caveat:** Results do not predict cloud performance; OS page cache can mask I/O costs

Always clear caches between benchmark runs on local storage:

```bash
# macOS
sudo purge

# Linux
sync && sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'
```

### Amazon S3

- **Latency:** 50–200 ms per GET request (same region)
- **Throughput:** 5–25 GB/s aggregate with parallel requests
- **Best for:** Production-representative benchmarks
- **Caveat:** Costs for PUT, GET, and storage; regional placement matters

Place synthetic data in the same region as your compute. Cross-region access adds 50–150 ms per request and incurs data transfer charges.

### Google Cloud Storage

- **Latency:** 40–150 ms per GET request (same region)
- **Throughput:** Similar to S3 with parallel requests
- **Best for:** GCP-native workflows
- **Caveat:** Requires `gcsfs` library; authentication via service account or application default credentials

### Choosing a Backend for Benchmarks

| Benchmark Goal | Recommended Backend |
|---------------|-------------------|
| Develop and validate pipeline | Local |
| Compare chunk configurations | Local (faster iteration) |
| Predict production performance | Same backend as production |
| Compare storage backends | Run identical benchmarks on each |

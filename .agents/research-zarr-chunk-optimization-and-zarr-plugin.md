# Research: Zarr Chunk Optimization Plugin & General Zarr Plugin

---
**Date:** 2026-02-26
**Author:** AI Assistant
**Status:** Active
**Related Documents:** None (initial research)

---

## Research Question

What technical foundations, architecture, and domain knowledge are needed to build two Claude Code plugins:
1. **zarr-chunk-optimization** — A plugin specializing in chunk size impact on read performance of Zarr data in cloud-based object stores, benchmarking results, and implementing optimal chunking strategies.
2. **zarr-data-format** — A general-purpose plugin for working with the Zarr array storage format across the full ecosystem.

This research provides sufficient detail for an AI agent to create all plugin components (agents, skills, references, assets) via GitHub issues.

## Executive Summary

Zarr is a cloud-native format for chunked, compressed, N-dimensional arrays that has become the standard for large-scale scientific data in cloud object stores. The Zarr ecosystem in 2025-2026 centers on Zarr-Python 3 (released January 2025) with full v3 specification support, the chunk-sharding extension, and async I/O. Performance on cloud stores depends critically on chunk size selection — research shows up to 63x performance differences based solely on chunk alignment with access patterns, and the optimal range is 1 MB minimum to 100 MB-1 GB for cloud storage.

Two distinct plugins are proposed. The **zarr-chunk-optimization** plugin addresses the specialized problem of benchmarking and optimizing chunk configurations for specific access patterns on cloud object stores (S3, GCS, Azure Blob). It requires agents that understand benchmarking methodology, chunk size heuristics, cloud storage latency characteristics, and the rechunking workflow. The **zarr-data-format** plugin provides comprehensive coverage of the full Zarr ecosystem — array creation, compression codecs, storage backends, metadata management, hierarchical groups, data migration, and integration with xarray/Dask.

The existing plugin architecture in this repository follows a well-defined pattern: `.claude-plugin/plugin.json` for metadata, `agents/` for agent definitions (500-1000+ line markdown files with YAML frontmatter), `skills/` with `SKILL.md` files and `references/` subdirectories (PATTERNS.md, EXAMPLES.md, COMMON_ISSUES.md), and optional `commands/` directories. Both plugins should follow these conventions exactly.

## Scope

**What This Research Covers:**
- Zarr format fundamentals (v2 and v3 specification)
- Chunk size optimization theory, heuristics, and formulas
- Cloud object store performance characteristics (S3, GCS, Azure Blob)
- Benchmarking methodologies and frameworks for Zarr I/O
- The full Zarr Python ecosystem (zarr-python, xarray, Dask, numcodecs, rechunker, fsspec, obstore, Icechunk, VirtualiZarr)
- Compression codecs and filter options
- Storage backend inventory and configuration
- Sharding (Zarr v3 extension)
- Existing plugin architecture patterns in this repository
- Detailed component specifications for both proposed plugins

**What This Research Does NOT Cover:**
- Implementation code for either plugin (that follows in planning/implementation phases)
- Non-Python Zarr implementations (zarrs-Rust, zarr.js) in depth
- Specific cloud provider pricing or service-level comparisons
- Real-time streaming data patterns (focus is on batch read/write)

## Key Findings

### Finding 1: Chunk Size Impact on Read Performance

Research from Nguyen et al. (2023) — "Impact of Chunk Size on Read Performance of Zarr Data in Cloud-based Object Stores" — provides the foundational evidence for the optimization plugin.

**Key Experimental Results:**
- Dataset: GEOS model output, dimensionality `(5136 time, 1152 lon, 721 lat)`
- Time-series access optimal: chunks `(5136, 10, 10)` — fast for temporal queries but 1,405x slower for spatial map extraction
- Spatial access optimal: chunks `(1, 1152, 721)` — fast for maps but 713x slower for time-series extraction
- Memory impact: Time-optimized strategy used 1.497 GB peak (1.294 GB higher than memory-optimized)
- Spatial-optimized strategy used 0.285 GB peak (0.053 GB higher than memory-optimized)
- **Versatile middle-range strategies** exist that perform reasonably well for both access patterns

**Xarray Tutorial Benchmark:**
- Array shape `(200, 200, 200)`, chunks `(1, 200, 200)` vs `(200, 200, 1)`: read time 111 ms vs 1.75 ms = **63x performance difference** based solely on chunk orientation vs access pattern

**Relevant Sources:**
- [ESS Open Archive Paper](https://essopenarchive.org/users/532985/articles/598065-impact-of-chunk-size-on-read-performance-of-zarr-data-in-cloud-based-object-stores)
- [Xarray Zarr Tutorial](https://tutorial.xarray.dev/intermediate/intro-to-zarr.html)

**Key Patterns:**
- Chunk alignment with the primary access dimension is the single most impactful optimization
- Larger chunks along the target dimension always perform best for that dimension
- Trade-off exists between time-series and spatial access — no single optimal strategy
- Middle-ground chunk strategies provide balanced performance across access patterns

### Finding 2: Quantitative Chunk Size Heuristics and Formulas

Multiple sources converge on specific recommendations for chunk sizing:

| Metric | Recommendation | Source |
|--------|---------------|--------|
| Minimum uncompressed chunk size | 1 MB | Zarr official docs |
| Optimal range (Dask context) | 100 MB - 1 GB | Dask best practices |
| S3 byte-range request sweet spot | 8-16 MB | AWS S3 best practices |
| Maximum task graph size | 10,000-100,000 chunks | Dask guidelines |
| Parallelism target | chunk_count >= 2 * num_workers | Dask guidelines |
| Total concurrency formula | `dask_threads * zarr_async_concurrency` | Zarr docs |
| Dask chunk alignment rule | Dask chunks must be integer multiples of Zarr storage chunks | Dask docs |
| Shard file reduction | `shard_volume / chunk_volume` factor | Zarr v3 spec |

**Relevant Sources:**
- [Zarr Performance Guide](https://zarr.readthedocs.io/en/latest/user-guide/performance/)
- [Cloud-Native Geo Zarr Guide](https://guide.cloudnativegeo.org/zarr/zarr-in-practice.html)

**Critical Formula — Total Concurrency:**
```
total_concurrency = dask_threads × zarr_async_concurrency
```
If both are set high, this can overwhelm cloud storage with too many concurrent requests.

**Zarr Async Concurrency Configuration:**
```python
zarr.config.set({'async.concurrency': 128})
# Or via environment variable:
# export ZARR_ASYNC_CONCURRENCY=128
# Default: 10 (conservative)
```

### Finding 3: Cloud Storage Performance Characteristics

Cloud object stores have fundamentally different I/O characteristics than local filesystems:

**Latency Profile:**
- Individual S3/GCS operation: 10-100 ms overhead per request
- Local filesystem: < 1 ms per operation
- Strategy: minimize request count, maximize bytes per request

**Throughput Achievements (2025):**
- Zarr-Python + Icechunk/Obstore on EC2↔S3: fully saturates network bandwidth (physically maximum throughput)
- Zarr + Dask on GCS: up to 5,000 MB/s (5 GB/s) throughput
- These results require proper concurrency tuning and chunk sizing

**Sharding Impact (Zarr v3):**
- Example: 100 GB array with 1 MB chunks = 100,000 objects; with 1 GB shards = 100 objects
- Shards are the minimum unit of writing — writer must fit entire shard in memory
- Sharding decouples chunk granularity from object count, solving the "many small files" problem

**Storage Backend Options:**

| Backend | Library | Cloud Provider |
|---------|---------|---------------|
| Amazon S3 | `s3fs` or `obstore` | AWS |
| Google Cloud Storage | `gcsfs` or `obstore` | GCP |
| Azure Blob Storage | `azure-storage-blob` or `obstore` | Azure |
| HTTP/HTTPS | `fsspec` | Any |
| Icechunk | `icechunk` | Any (wraps object stores) |

**Relevant Sources:**
- [Pangeo Cloud Storage Benchmark](https://gallery.pangeo.io/repos/earthcube2020/ec20_abernathey_etal/cloud_storage.html)
- [Earthmover I/O-Maxing Tensors](https://earthmover.io/blog/i-o-maxing-tensors-in-the-cloud/)

### Finding 4: Benchmarking Methodology and Frameworks

**Airspeed Velocity (ASV):**
- Zarr's official benchmarking tool for performance regression tracking
- Tracks runtime, memory consumption, and custom metrics over time
- Generates interactive web frontend for visualization
- Zarr has an existing ASV configuration tracking convenience, creation, core, and storage modules

**pytest-benchmark:**
- Integration with pytest ecosystem
- Good for one-off benchmark comparisons and CI integration
- Provides statistical analysis (mean, median, stddev, rounds)

**Benchmarking Methodology for Chunk Optimization:**
1. Define access patterns: time-series extraction, spatial map extraction, mixed queries
2. Create test array with known dimensions and data characteristics
3. Write array with multiple chunk configurations
4. Measure read time, memory peak, and throughput for each access pattern × chunk configuration
5. Track metrics: wall time, peak memory, bytes transferred, compression ratio
6. Compare using statistical methods (multiple runs, confidence intervals)

**Dask Dashboard Monitoring Indicators:**
- White space in task stream = inefficient small chunks
- Excessive red (communication) = inadequate computation vs coordination overhead
- Orange bars = approaching memory limits
- Gray bars = disk spillage (chunks too large)

**Key Diagnostic Methods:**
```python
# Zarr array inspection
z.info                    # Summary
z.info_complete()         # Full metadata (slow for large arrays)
z.chunks                  # Chunk shape tuple

# Compression statistics
# data size, storage size, storage ratio, chunks initialized count
```

**Relevant Sources:**
- [Zarr ASV Benchmark Discussion](https://github.com/zarr-developers/zarr-python/discussions/1479)
- [Benchmark Zarr Implementations (GSoC)](https://hackmd.io/@I9Hj1bLETn6QIva97pA3Hw/By7rlRXd5)

### Finding 5: Compression Codecs and Filters

The codec choice interacts with chunk size for overall I/O performance:

**Default Compressor:** Zstandard (Zstd) in Zarr v3 / Blosc in Zarr v2

**Compression Codec Inventory:**

| Codec | Library | Characteristics |
|-------|---------|-----------------|
| Blosc (meta-compressor) | `numcodecs.Blosc` | Internal algorithms: blosclz, lz4, lz4hc, snappy, zlib, zstd |
| Zstandard | `numcodecs.Zstd` | Default in v3, good compression ratio |
| Gzip | `numcodecs.GZip` | Universal compatibility, slower |
| LZ4 | `numcodecs.LZ4` | Fastest decompression |
| LZMA | `numcodecs.LZMA` | Best compression ratio, slowest |
| BZ2 | `numcodecs.BZ2` | Good ratio, moderate speed |
| Zlib | `numcodecs.Zlib` | Standard, good compatibility |

**Blosc Configuration:**
```python
from numcodecs import Blosc
compressor = Blosc(cname='zstd', clevel=3, shuffle=Blosc.BITSHUFFLE)
# Shuffle modes: NOSHUFFLE, SHUFFLE (byte), BITSHUFFLE
# Thread control:
from numcodecs import blosc
blosc.set_nthreads(2)
blosc.use_threads = False  # Required for multi-process safety
```

**Pre-compression Filters:**
- `Delta` — stores differences between consecutive values
- `Quantize` — reduces floating-point precision
- `FixedScaleOffset` — linear scaling
- `PackBits` — boolean packing
- `Categorize` — categorical encoding

**Benchmark Example:**
- Blosc+LZ4 achieved 155.5x compression ratio on test data
- Zstd achieved 7.8x on same data
- Gzip achieved 5.3x

**Integrity Checks:** CRC32, Adler32

### Finding 6: Zarr-Python 3 and the 2025 Ecosystem

**Zarr-Python 3 (Released January 9, 2025):**
- Requires Python 3.11+
- Full Zarr v3 specification support
- Chunk-sharding extension (ZEP 0002)
- Fully async I/O using Python's asyncio
- Compute-intensive operations dispatched to managed thread pool
- 100% type hint coverage
- New Store ABC for custom backends
- Entry point system for custom codecs
- Backward-compatible with v2 format (`zarr_format=2`)

**Ecosystem Components:**

| Component | Role | Status (2025) |
|-----------|------|---------------|
| zarr-python 3 | Core format library | Stable |
| xarray | High-level dataset interface | Full zarr-python 3 support |
| Dask | Parallel/lazy computation | Full zarr-python 3 support |
| numcodecs | Compression codecs | Adapted for v3 codec system |
| rechunker | Efficient rechunking | Stable |
| fsspec | Universal filesystem abstraction | Mature |
| obstore | Rust-based I/O layer (fast) | Active development |
| Icechunk | Versioned storage engine (Rust) | 1.0 released July 2025 |
| VirtualiZarr | Virtual Zarr stores from archival formats | Active development |
| zarrs-python | Rust Zarr implementation for Python | Active development |

**Relevant Sources:**
- [Zarr-Python 3 Release Blog](https://zarr.dev/blog/zarr-python-3-release/)
- [Zarr Everywhere (Development Seed)](https://developmentseed.org/blog/2025-10-13-zarr/)

### Finding 7: Storage Backends and Cloud Access Patterns

**Complete Storage Backend Inventory:**

| Backend | Class / Method | Use Case |
|---------|---------------|----------|
| Local filesystem | `LocalStore` (v3) / `DirectoryStore` (v2) | Default, development |
| ZIP archives | `ZipStore` | Archive-based storage |
| Memory | `MemoryStore` | Testing, temporary data |
| Amazon S3 | `FsspecStore` + `s3fs` or `ObjectStore` + `obstore` | AWS cloud |
| Google Cloud Storage | `FsspecStore` + `gcsfs` or `ObjectStore` + `obstore` | GCP cloud |
| Azure Blob Storage | `FsspecStore` + `adlfs` or `ObjectStore` + `obstore` | Azure cloud |
| HTTP/HTTPS | `FsspecStore` + `aiohttp` | Read-only remote |
| Icechunk | `icechunk.IcechunkStore` | Versioned, ACID transactions |
| Redis | `RedisStore` (v2) | In-memory distributed |
| MongoDB | `MongoDBStore` (v2) | Document database |
| SQLite | `SQLiteStore` (v2) | Embedded database |
| LMDB | `LMDBStore` (v2) | Lightning Memory-Mapped DB |

**Cloud Access Code Patterns:**

```python
# Pattern 1: fsspec URL shorthand (simplest)
ds = xr.open_zarr("s3://bucket/path/to/data.zarr")
ds = xr.open_zarr("gs://bucket/path/to/data.zarr")

# Pattern 2: Explicit fsspec store
import zarr
store = zarr.storage.FsspecStore("s3", path="bucket/path/data.zarr",
                                  storage_options={"anon": True})

# Pattern 3: obstore (Rust-based, fastest for cloud)
import obstore
s3store = obstore.store.S3Store("bucket", prefix="path/data.zarr")
zstore = zarr.store.ObjectStore(s3store)

# Pattern 4: Icechunk (versioned)
from icechunk import IcechunkStore, StorageConfig
store = IcechunkStore.open_or_create(
    storage=StorageConfig.s3_from_env("bucket", "prefix"),
)

# Pattern 5: With caching layer
g = zarr.open_group("simplecache::s3://bucket/data.zarr",
                    storage_options={"s3": {"anon": True}})
```

**Metadata Consolidation (Critical for Cloud):**
```python
zarr.consolidate_metadata(store)
# Opens with single metadata read instead of per-array/group reads
root = zarr.open_consolidated(store)  # v2
# v3: consolidated metadata not yet in spec but functionally useful
```

### Finding 8: Rechunking Workflows

The `rechunker` library solves the problem of transforming existing Zarr data to optimal chunk configurations:

```python
from rechunker import rechunk

result = rechunk(
    source,                     # Source array/dataset
    target_chunks=(4, 1),       # Desired chunk sizes
    target_store="output.zarr", # Output location
    max_mem=256_000,            # Memory budget (bytes)
    temp_store="temp.zarr"      # Intermediate staging
)
result.execute()  # Triggers the computation
```

**Architecture:** source → intermediate staging → target (two-pass with memory constraints)

**When Rechunking is Needed:**
- Data was written with chunks optimized for a different access pattern
- Moving data from HDF5/NetCDF (often poorly chunked) to cloud-optimized Zarr
- Changing from column-oriented to row-oriented access
- Migrating data between storage backends with different optimal sizes

### Finding 9: Domain-Specific Chunking Strategies

Research from real-world datasets shows chunking must be tailored to use case:

**Climate Data (shape: `3650 time, 721 lat, 1440 lon`):**
- Temporal chunking `[T, 1, 1]` — efficient for time-series at fixed locations
- Spatial chunking `[1, Y, X]` — efficient for regional analysis and maps
- Spatio-temporal `[10, 90, 180]` — balanced for mixed access

**Pluvial Flooding (shape: `4, 1, 6, 3, 6000, 6000`):**
- Recommended: `[1, 1, 2, 3, 1, 1]` — users pin location, query scenarios
- Small spatial chunks minimize read I/O

**Hail Projection (shape: `3, 2, 161, 281, 3`):**
- Recommended: `(2, 2, 81, 281, 1)` — single-location queries with ensemble comparisons

**Decision Heuristic:**
| Access Pattern | Chunk Strategy |
|---|---|
| Single lat/lon time-series | Chunk spatial dims at size 1, maximize time dim |
| Spatial maps at single time | Chunk time dim at size 1, maximize spatial dims |
| Mixed access | Moderate chunks across all dims |
| Scenario/ensemble comparison | Include scenario dims in fast chunk dimensions |

### Finding 10: Existing Plugin Architecture Conventions

Based on thorough exploration of 5 existing plugins in this repository:

**Directory Structure:**
```
plugin-name/
├── .claude-plugin/
│   └── plugin.json                 # {"name", "description", "version", "author"}
├── agents/
│   └── agent-name.md               # YAML frontmatter + 500-1000+ lines of content
├── skills/
│   └── skill-name/
│       ├── SKILL.md                 # Main entry point (300+ lines)
│       ├── assets/                  # Templates, configs, example files
│       ├── scripts/                 # Runnable example scripts
│       └── references/
│           ├── PATTERNS.md          # Reusable patterns and advanced usage
│           ├── EXAMPLES.md          # Complete working examples
│           └── COMMON_ISSUES.md     # Troubleshooting guide
├── commands/                        # Optional: custom commands
├── README.md
└── LICENSE
```

**Agent Frontmatter:**
```yaml
---
name: agent-name
description: |
  Multi-line description with use cases and trigger phrases.
  <example>
  Context: ...
  user: "..."
  assistant: "..."
  <commentary>...</commentary>
  </example>
model: inherit
color: cyan
skills:
  - skill-name-1
  - skill-name-2
---
```

**Skill Frontmatter:**
```yaml
---
name: skill-name
description: When user asks to "do X", "work with Y", or needs Z.
---
```

**Marketplace Registration:**
```json
{
  "name": "plugin-name",
  "source": "./plugins/plugin-name",
  "description": "...",
  "category": "data-science",
  "keywords": ["zarr", "chunking", ...],
  "license": "BSD-3-Clause",
  "strict": false
}
```

## Architecture Overview

### Plugin 1: zarr-chunk-optimization

```
zarr-chunk-optimization/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── chunk-optimization-expert.md       # Primary agent: chunk analysis + recommendation
│   └── zarr-benchmark-engineer.md         # Benchmarking specialist agent
├── skills/
│   ├── chunk-strategy/
│   │   ├── SKILL.md                       # Chunk sizing heuristics, formulas, decision trees
│   │   ├── assets/
│   │   │   ├── chunk-calculator.py        # Chunk size calculator utility
│   │   │   └── chunk-decision-tree.md     # Visual decision tree for strategy selection
│   │   └── references/
│   │       ├── PATTERNS.md                # Access pattern analysis patterns
│   │       ├── EXAMPLES.md                # Real-world optimization case studies
│   │       └── COMMON_ISSUES.md           # Common chunking mistakes
│   ├── cloud-storage-benchmarking/
│   │   ├── SKILL.md                       # Benchmark methodology, metrics, tools
│   │   ├── assets/
│   │   │   ├── benchmark-template.py      # Reusable benchmarking script template
│   │   │   ├── benchmark-config.yaml      # Benchmark configuration template
│   │   │   └── results-analysis.py        # Results analysis and visualization
│   │   └── references/
│   │       ├── PATTERNS.md                # Benchmarking patterns (ASV, pytest-benchmark)
│   │       ├── EXAMPLES.md                # S3/GCS/Azure benchmark examples
│   │       └── COMMON_ISSUES.md           # Benchmark pitfalls and solutions
│   └── rechunking-workflows/
│       ├── SKILL.md                       # Using rechunker, migration workflows
│       ├── assets/
│       │   └── rechunk-template.py        # Rechunking script template
│       └── references/
│           ├── PATTERNS.md                # Rechunking patterns and memory management
│           ├── EXAMPLES.md                # HDF5→Zarr, NetCDF→Zarr migration examples
│           └── COMMON_ISSUES.md           # Rechunking failures and solutions
├── README.md
└── LICENSE
```

### Plugin 2: zarr-data-format

```
zarr-data-format/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── zarr-expert.md                     # Primary Zarr expert agent
│   └── zarr-cloud-architect.md            # Cloud storage + Zarr integration specialist
├── skills/
│   ├── zarr-fundamentals/
│   │   ├── SKILL.md                       # Core Zarr operations, creation, I/O, metadata
│   │   ├── assets/
│   │   │   └── zarr-quickstart.py         # Quick start template
│   │   └── references/
│   │       ├── PATTERNS.md                # Array creation, group management, indexing patterns
│   │       ├── EXAMPLES.md                # Complete working examples
│   │       └── COMMON_ISSUES.md           # Common Zarr mistakes
│   ├── compression-codecs/
│   │   ├── SKILL.md                       # Codec selection, configuration, benchmarking
│   │   ├── assets/
│   │   │   └── codec-comparison.py        # Codec benchmark script
│   │   └── references/
│   │       ├── PATTERNS.md                # Codec configuration patterns
│   │       ├── EXAMPLES.md                # Codec benchmarking examples
│   │       └── COMMON_ISSUES.md           # Codec troubleshooting
│   ├── cloud-storage-backends/
│   │   ├── SKILL.md                       # All storage backends, configuration, access patterns
│   │   ├── assets/
│   │   │   ├── s3-config-template.py      # S3 access template
│   │   │   ├── gcs-config-template.py     # GCS access template
│   │   │   └── azure-config-template.py   # Azure access template
│   │   └── references/
│   │       ├── PATTERNS.md                # Cloud access patterns, caching, auth
│   │       ├── EXAMPLES.md                # Multi-cloud access examples
│   │       └── COMMON_ISSUES.md           # Cloud connectivity troubleshooting
│   ├── zarr-xarray-integration/
│   │   ├── SKILL.md                       # xarray + Zarr workflows, Dask integration
│   │   └── references/
│   │       ├── PATTERNS.md                # xarray I/O patterns, encoding, region writes
│   │       ├── EXAMPLES.md                # Dataset read/write/append examples
│   │       └── COMMON_ISSUES.md           # xarray-zarr integration issues
│   └── data-migration/
│       ├── SKILL.md                       # HDF5/NetCDF → Zarr migration, VirtualiZarr
│       ├── assets/
│       │   └── migration-template.py      # Migration script template
│       └── references/
│           ├── PATTERNS.md                # Migration patterns, copy_store, VirtualiZarr
│           ├── EXAMPLES.md                # Complete migration workflows
│           └── COMMON_ISSUES.md           # Migration pitfalls
├── README.md
└── LICENSE
```

## Component Interactions

### Plugin 1 Flow: Chunk Optimization Workflow

```
User provides: dataset shape, access patterns, target cloud store
                          │
                          ▼
        ┌─────────────────────────────────┐
        │   chunk-optimization-expert     │
        │   (Primary agent)               │
        │   - Analyzes dataset dimensions │
        │   - Determines access patterns  │
        │   - Applies chunk heuristics    │
        │   - Recommends strategy         │
        └──────────────┬──────────────────┘
                       │
          ┌────────────┼────────────────┐
          ▼            ▼                ▼
    chunk-strategy   cloud-storage    rechunking-
    skill            benchmarking     workflows
    (Formulas,       skill            skill
     decision tree,  (ASV/pytest,     (rechunker,
     case studies)   metrics,         migration)
                     templates)
          │            │                │
          ▼            ▼                ▼
    Recommendation  Benchmark       Rechunking
    + rationale     results         execution plan
                          │
                          ▼
        ┌─────────────────────────────────┐
        │   zarr-benchmark-engineer       │
        │   (Benchmark specialist)        │
        │   - Designs benchmark suite     │
        │   - Runs performance tests      │
        │   - Analyzes results            │
        │   - Validates recommendations   │
        └─────────────────────────────────┘
```

### Plugin 2 Flow: General Zarr Operations

```
User provides: Zarr task description (create, read, write, migrate, etc.)
                          │
                          ▼
        ┌─────────────────────────────────┐
        │   zarr-expert                   │
        │   (Primary agent)               │
        │   - Routes to appropriate skill │
        │   - Provides Zarr guidance      │
        │   - Handles format conversion   │
        └──────────────┬──────────────────┘
                       │
    ┌──────┬───────────┼──────────┬──────────────┐
    ▼      ▼           ▼          ▼              ▼
  zarr-  compression  cloud-    zarr-xarray    data-
  fund.  codecs       storage   integration    migration
  skill  skill        backends  skill          skill
                      skill
    │      │           │          │              │
    ▼      ▼           ▼          ▼              ▼
  Array  Codec       Cloud      Dataset       HDF5/NetCDF
  ops    config      access     workflows     → Zarr
                          │
                          ▼
        ┌─────────────────────────────────┐
        │   zarr-cloud-architect          │
        │   (Cloud specialist)            │
        │   - Cloud-specific guidance     │
        │   - Storage backend selection   │
        │   - Performance tuning          │
        │   - Metadata consolidation      │
        └─────────────────────────────────┘
```

## Technical Decisions

### Decision 1: Two Separate Plugins

- **Rationale:** Chunk optimization is a specialized performance engineering concern distinct from general Zarr usage. Separating them allows users to install only what they need. The optimization plugin can be used by users who already know Zarr but need performance tuning. The general plugin serves users learning Zarr or working with it daily.
- **Trade-offs:** Some overlap in cloud storage content. The optimization plugin references concepts the general plugin covers in depth. Cross-references between plugins should be documented.

### Decision 2: Two Agents Per Plugin

- **Rationale:** Each plugin has a primary generalist agent and a specialist agent. This follows the pattern established by `scientific-python-development` (which has `scientific-python-expert` and `scientific-docs-architect`).
- **Trade-offs:** More agents means more maintenance but provides focused expertise for distinct workflows.

### Decision 3: ASV + pytest-benchmark for Benchmarking Skill

- **Rationale:** ASV is Zarr's own benchmarking framework and provides time-series regression tracking. pytest-benchmark integrates with standard test suites. Both are needed for different scenarios — ASV for ongoing performance tracking, pytest-benchmark for one-off comparisons.
- **Trade-offs:** Users need to learn two tools, but each serves a distinct purpose.

### Decision 4: Both Zarr v2 and v3 Coverage

- **Rationale:** Zarr v2 data is ubiquitous in existing datasets. v3 is the future with sharding support. Both must be covered for practical utility.
- **Trade-offs:** More content to maintain, but essential for real-world use.

## Dependencies and Integrations

### Plugin 1: zarr-chunk-optimization Dependencies

| Dependency | Purpose | Required |
|-----------|---------|----------|
| `zarr >= 3.0` | Core Zarr operations | Yes |
| `xarray` | Dataset interface for benchmarking | Yes |
| `dask` | Parallel I/O and chunked computation | Yes |
| `numpy` | Array operations | Yes |
| `numcodecs` | Compression codecs | Yes |
| `rechunker` | Efficient rechunking | Yes |
| `pytest-benchmark` | Benchmark framework | Yes |
| `asv` | Airspeed Velocity benchmarking | Recommended |
| `s3fs` / `gcsfs` / `adlfs` | Cloud filesystem access | At least one |
| `obstore` | High-performance cloud I/O | Recommended |
| `matplotlib` / `hvplot` | Results visualization | Recommended |

### Plugin 2: zarr-data-format Dependencies

| Dependency | Purpose | Required |
|-----------|---------|----------|
| `zarr >= 3.0` | Core Zarr operations | Yes |
| `xarray` | High-level dataset interface | Yes |
| `dask` | Parallel computation | Recommended |
| `numpy` | Array operations | Yes |
| `numcodecs` | Compression codecs | Yes |
| `fsspec` | Universal filesystem abstraction | Recommended |
| `s3fs` / `gcsfs` / `adlfs` | Cloud provider access | Per cloud |
| `obstore` | Rust-based cloud I/O | Recommended |
| `icechunk` | Versioned storage | Optional |
| `h5py` | HDF5 compatibility | Optional |
| `rechunker` | Data migration | Optional |

### Integration with Existing Plugins

- **scientific-domain-applications**: The `xarray-for-multidimensional-data` skill already covers xarray basics. The zarr-data-format plugin extends this with Zarr-specific depth. Cross-references should link to the existing skill.
- **scientific-python-development**: Follows the same development best practices (pixi, testing, packaging). Benchmark scripts should follow `python-testing` skill patterns.

## Edge Cases and Constraints

- **Zarr v3 consolidated metadata**: Not yet part of the v3 specification but functionally useful. The plugins should document this gap and recommend workarounds.
- **Blosc thread safety in multi-process**: `blosc.use_threads = False` is required for multi-process safety. This is a common source of silent corruption.
- **Shard memory requirements**: Writers must fit the entire shard (all compressed chunks) in memory. With large shards, this can exceed available RAM.
- **Rechunker temp storage**: Requires temporary intermediate storage approximately equal to the dataset size. Users on constrained systems may not have sufficient space.
- **Empty chunk optimization**: `write_empty_chunks=False` (default) can cause issues if readers don't handle missing chunks correctly. Nearly 2x write performance difference with sparse data.
- **Dask + Zarr concurrency**: Total concurrency = dask_threads x zarr_async_concurrency can overwhelm cloud storage if both are set high.
- **Obstore vs fsspec**: Obstore is faster (Rust-based) but has a smaller ecosystem. fsspec is mature and widely supported. Both should be documented.

## Open Questions

1. **Should the zarr-chunk-optimization plugin include a command (e.g., `/benchmark-chunks`) that generates a benchmark script?** — Commands are optional and only some plugins use them (ai-research-workflows, project-management). Given that benchmarking is a workflow-like activity, commands may add value.

2. **Should the zarr-data-format plugin include an MCP configuration (like holoviz-visualization)?** — If there are Zarr-specific MCP servers or tools, an `.mcp.json` could be useful. Currently no known Zarr MCP servers exist.

3. **How much overlap should exist between the two plugins' cloud storage content?** — The chunk-optimization plugin needs cloud store configuration for benchmarking. The general plugin covers it comprehensively. Option: keep cloud config in the general plugin and cross-reference from the optimization plugin.

4. **Should VirtualiZarr be covered in the general Zarr plugin or as a separate concern?** — VirtualiZarr enables zero-copy ingestion of archival formats. It fits naturally in the data-migration skill of the general plugin.

5. **Zarr v2 → v3 migration guidance**: Should a dedicated skill cover format migration, or should it be part of zarr-fundamentals? Given the ecosystem is transitioning, a section in zarr-fundamentals covering v2/v3 differences and migration is likely sufficient.

---

## Detailed GitHub Issue Specifications

The following issue specifications contain sufficient detail for an AI agent to implement each component.

---

### PLUGIN 1: zarr-chunk-optimization

---

#### Issue 1: Create plugin scaffold for zarr-chunk-optimization

**Title:** feat: Create zarr-chunk-optimization plugin scaffold

**Description:**
Create the initial plugin directory structure and metadata for the zarr-chunk-optimization plugin.

**Acceptance Criteria:**
- [ ] Create `plugins/zarr-chunk-optimization/.claude-plugin/plugin.json` with:
  ```json
  {
    "name": "zarr-chunk-optimization",
    "description": "Specialized agents and skills for Zarr chunk size optimization, cloud storage benchmarking, and rechunking workflows",
    "version": "0.1.0",
    "author": {
      "name": "SSEC Research Team",
      "url": "https://github.com/uw-ssec"
    }
  }
  ```
- [ ] Create empty directories: `agents/`, `skills/chunk-strategy/`, `skills/cloud-storage-benchmarking/`, `skills/rechunking-workflows/`
- [ ] Create `LICENSE` (BSD-3-Clause, symlink to root)
- [ ] Add plugin entry to `.claude-plugin/marketplace.json`:
  ```json
  {
    "name": "zarr-chunk-optimization",
    "source": "./plugins/zarr-chunk-optimization",
    "description": "Specialized agents and skills for Zarr chunk size optimization, cloud storage benchmarking, and rechunking workflows",
    "homepage": "https://github.com/uw-ssec/rse-plugins",
    "repository": "https://github.com/uw-ssec/rse-plugins",
    "license": "BSD-3-Clause",
    "keywords": ["zarr", "chunking", "benchmarking", "cloud-storage", "performance", "optimization", "s3", "gcs", "azure", "scientific-computing"],
    "category": "data-science",
    "strict": false
  }
  ```
- [ ] Create `README.md` documenting the plugin structure, purpose, and available agents/skills (follow pattern from `plugins/scientific-domain-applications/README.md`)

**Labels:** `enhancement`, `plugin`

---

#### Issue 2: Create chunk-optimization-expert agent

**Title:** feat: Create chunk-optimization-expert agent for zarr-chunk-optimization plugin

**Description:**
Create the primary agent for the zarr-chunk-optimization plugin. This agent analyzes dataset characteristics, determines optimal chunk configurations based on access patterns, applies heuristics and formulas, and recommends chunking strategies with rationale.

**File:** `plugins/zarr-chunk-optimization/agents/chunk-optimization-expert.md`

**Agent Specification:**

**Frontmatter:**
```yaml
name: chunk-optimization-expert
description: |
  Expert in Zarr chunk size optimization for cloud-based object stores. Analyzes dataset dimensions, access patterns, and storage characteristics to recommend optimal chunking strategies. Deep knowledge of chunk size heuristics, cloud storage I/O characteristics (S3, GCS, Azure Blob), sharding, compression interaction, and the performance trade-offs between different chunking approaches.

  Use this agent when the user asks to "optimize zarr chunks", "benchmark chunk sizes", "improve zarr read performance", "choose chunk dimensions", "optimize cloud data access", "reduce zarr latency", "tune zarr performance", or needs guidance on chunk strategy for cloud-stored scientific data.

  <example>
  Context: User has a climate dataset and needs chunk optimization
  user: "I have a climate dataset with shape (8760, 721, 1440) stored on S3 and I primarily access time-series at specific locations. How should I chunk it?"
  assistant: "I'll use the chunk-optimization-expert to analyze your dataset dimensions and access patterns to recommend optimal chunk sizes."
  <commentary>
  Chunk optimization requires understanding dataset shape, access patterns, and cloud storage characteristics. This agent applies quantitative heuristics.
  </commentary>
  </example>

  <example>
  Context: User has slow Zarr reads from cloud storage
  user: "My Zarr reads from GCS are really slow. The dataset is chunked at (1, 1000, 1000) but I mostly read time-series."
  assistant: "I'll invoke the chunk-optimization-expert to diagnose the chunk-access pattern mismatch and recommend a better chunking strategy."
  <commentary>
  Chunk orientation misaligned with access pattern is the most common Zarr performance issue. This agent diagnoses and recommends.
  </commentary>
  </example>

  <example>
  Context: User needs to rechunk existing data
  user: "I need to rechunk my dataset from spatial-optimized to time-optimized chunks on S3"
  assistant: "I'll use the chunk-optimization-expert to plan the rechunking workflow with memory and storage constraints."
  <commentary>
  Rechunking involves the rechunker library with memory budgets and intermediate storage. This agent plans the workflow.
  </commentary>
  </example>
model: inherit
color: cyan
skills:
  - chunk-strategy
  - cloud-storage-benchmarking
  - rechunking-workflows
```

**Agent Body Content Must Include (500-1000+ lines):**

1. **Purpose section** — Expert in analyzing Zarr chunk configurations for cloud-optimized read performance. Specializes in the relationship between chunk dimensions, access patterns, and cloud object store I/O characteristics.

2. **Core Knowledge Base:**
   - Chunk size heuristics (1 MB minimum, 100 MB-1 GB optimal for cloud, S3 sweet spot 8-16 MB)
   - Access pattern taxonomy: temporal, spatial, spatio-temporal, ensemble/scenario
   - The 63x performance difference evidence (chunk orientation vs access pattern)
   - Total concurrency formula: `dask_threads * zarr_async_concurrency`
   - Dask chunk alignment rule: must be integer multiples of Zarr storage chunks
   - Sharding considerations (v3): file count reduction, memory implications
   - Compression interaction with chunk size (smaller chunks = less compressible)

3. **Workflow Patterns:**
   - **Analysis workflow:** Receive dataset shape + access patterns → apply heuristics → calculate candidate chunk configs → recommend with rationale
   - **Benchmarking workflow:** Design benchmark suite → configure test matrix → execute benchmarks → analyze results → refine recommendation
   - **Rechunking workflow:** Assess current chunks → determine target → plan rechunking with memory constraints → execute → validate

4. **Decision-Making Framework** using `<thinking>` blocks:
   - Step 1: Identify dataset dimensions and sizes
   - Step 2: Determine primary access patterns (what reads are most common?)
   - Step 3: Check target cloud store (S3/GCS/Azure) and its I/O characteristics
   - Step 4: Apply chunk size heuristics and calculate candidate configurations
   - Step 5: Evaluate trade-offs between access patterns
   - Step 6: Recommend strategy with clear rationale

5. **Constraints:**
   - Always show quantitative reasoning (chunk sizes in bytes, expected request counts)
   - Never recommend chunks smaller than 1 MB uncompressed for cloud storage
   - Always consider the dask_threads * zarr_async_concurrency interaction
   - Always mention sharding as an option for Zarr v3 when many small chunks are needed
   - Always recommend metadata consolidation for cloud stores

6. **Error Handling Framework** for common scenarios:
   - Dataset too small for chunking to matter
   - Conflicting access patterns with no good compromise
   - Memory-constrained environments limiting chunk size options
   - Legacy v2 data that needs migration to v3 for sharding

**Acceptance Criteria:**
- [ ] Agent file is 500-1000+ lines
- [ ] YAML frontmatter includes name, description with 3+ examples, model, color, skills
- [ ] Body includes all 6 sections listed above
- [ ] Includes concrete formulas and heuristic values throughout
- [ ] References specific chunk size numbers from research (not vague)

**Labels:** `enhancement`, `agent`

---

#### Issue 3: Create zarr-benchmark-engineer agent

**Title:** feat: Create zarr-benchmark-engineer agent for zarr-chunk-optimization plugin

**Description:**
Create the benchmarking specialist agent that designs, executes, and analyzes chunk size performance benchmarks.

**File:** `plugins/zarr-chunk-optimization/agents/zarr-benchmark-engineer.md`

**Agent Specification:**

**Frontmatter:**
```yaml
name: zarr-benchmark-engineer
description: |
  Specialist in designing and executing Zarr I/O performance benchmarks on cloud object stores. Expert in Airspeed Velocity (ASV) and pytest-benchmark frameworks, statistical analysis of benchmark results, and translating results into actionable chunking recommendations.

  Use this agent when the user asks to "benchmark zarr performance", "profile chunk sizes", "compare chunking strategies", "measure read throughput", "set up ASV benchmarks", or needs help designing performance tests for Zarr data access patterns.

  <example>
  Context: User wants to compare chunk configurations
  user: "I want to benchmark three different chunk configurations for my dataset on S3"
  assistant: "I'll use the zarr-benchmark-engineer to design a rigorous benchmark suite comparing your chunk configurations."
  <commentary>
  Benchmarking Zarr I/O requires controlled methodology, statistical rigor, and understanding of cloud storage variability.
  </commentary>
  </example>

  <example>
  Context: User has benchmark results to analyze
  user: "I ran chunk size benchmarks and have the results. Help me interpret them."
  assistant: "I'll invoke the zarr-benchmark-engineer to analyze your benchmark data and extract actionable recommendations."
  <commentary>
  Benchmark analysis requires understanding of statistical significance, outlier handling, and translating metrics to recommendations.
  </commentary>
  </example>
model: inherit
color: green
skills:
  - cloud-storage-benchmarking
  - chunk-strategy
```

**Agent Body Content Must Include (500-800+ lines):**

1. **Purpose** — Expert in I/O performance benchmarking for Zarr arrays, specializing in cloud object stores.

2. **Benchmarking Methodology:**
   - Define test matrix: chunk configurations × access patterns × storage backends
   - Statistical approach: minimum 5 runs per configuration, report mean/median/stddev/min/max
   - Warm-up runs to account for cloud storage caching
   - Metrics: wall time, peak memory, bytes transferred, compression ratio, throughput (MB/s)
   - Control variables: same data, same compute instance, same network conditions

3. **Tool Expertise:**
   - ASV configuration and benchmark class writing
   - pytest-benchmark fixtures and parameterization
   - Dask dashboard interpretation (white space, red bars, orange bars, gray bars)
   - `z.info_complete()` for compression statistics

4. **Results Analysis Patterns:**
   - Time-series plots of throughput vs chunk size
   - Heatmaps of access pattern × chunk config
   - Memory profile analysis
   - Identification of optimal operating points

5. **Template Generation:**
   - Can generate benchmark scripts from templates
   - Produces analysis notebooks for visualization

**Acceptance Criteria:**
- [ ] Agent file is 500-800+ lines
- [ ] Covers both ASV and pytest-benchmark frameworks
- [ ] Includes benchmark methodology section with statistical requirements
- [ ] Includes results analysis patterns
- [ ] References Dask dashboard monitoring indicators

**Labels:** `enhancement`, `agent`

---

#### Issue 4: Create chunk-strategy skill

**Title:** feat: Create chunk-strategy skill for zarr-chunk-optimization plugin

**Description:**
Create the skill covering chunk size heuristics, formulas, decision trees, and real-world optimization case studies.

**Directory:** `plugins/zarr-chunk-optimization/skills/chunk-strategy/`

**Files to Create:**

**SKILL.md (300+ lines):**
- Frontmatter: `name: chunk-strategy`, description with trigger phrases
- Quick Reference Card with chunk size formula table
- Decision tree for chunk strategy selection
- Core Concepts: chunk alignment, access patterns, size heuristics
- The quantitative rules:
  - Minimum: 1 MB uncompressed
  - Optimal: 100 MB - 1 GB (cloud)
  - S3 sweet spot: 8-16 MB per request
  - Max task graph: 10K-100K chunks
  - Parallelism: chunks >= 2 * workers
  - Dask alignment: Dask chunks must be integer multiples of Zarr chunks
  - Total concurrency: `dask_threads * zarr_async_concurrency`
- Sharding section (Zarr v3): when to use, sizing, memory implications
- Access pattern taxonomy with recommendations table
- Empty chunk optimization (`write_empty_chunks` flag)
- Memory layout (`order: 'C'` vs `order: 'F'`)
- Links to references/PATTERNS.md, EXAMPLES.md, COMMON_ISSUES.md

**assets/chunk-calculator.py:**
- Python script that calculates recommended chunk sizes given:
  - Array shape (tuple)
  - Data type (dtype)
  - Primary access pattern (temporal/spatial/mixed)
  - Target chunk size range (min/max bytes)
  - Number of workers (for parallelism target)
- Outputs: recommended chunk shape, estimated chunk size in MB, estimated number of chunks, estimated task graph size

**assets/chunk-decision-tree.md:**
- ASCII/markdown decision tree:
  - Is this for cloud or local storage? → Cloud: minimum 1 MB, target 100 MB+; Local: more flexible
  - Primary access pattern? → Temporal: maximize time dim; Spatial: maximize spatial dims; Mixed: balanced
  - Using Dask? → Yes: align with Dask chunks, check total concurrency; No: focus on Zarr-level
  - Zarr v3 available? → Yes: consider sharding; No: optimize chunk count directly
  - Data sparse? → Yes: set `write_empty_chunks=False`; No: default behavior

**references/PATTERNS.md:**
- Pattern: Temporal-First Chunking (climate/weather time-series)
- Pattern: Spatial-First Chunking (map generation, regional analysis)
- Pattern: Balanced Spatio-Temporal (mixed workloads)
- Pattern: Ensemble/Scenario Chunking (multi-scenario datasets)
- Pattern: Sharded Chunks (Zarr v3, many small logical chunks)
- Pattern: Dask-Aligned Chunking (ensuring Dask chunks are multiples of Zarr chunks)
- Each pattern: description, when to use, chunk formula, code example, trade-offs

**references/EXAMPLES.md:**
- Example 1: Climate Dataset Optimization — shape (3650, 721, 1440), temporal vs spatial access, benchmarked results showing 63x difference
- Example 2: Satellite Imagery — high-resolution spatial data, tile-aligned chunks
- Example 3: Ensemble Weather Forecasts — scenario dimension chunking
- Example 4: Pluvial Flooding Dataset — shape (4, 1, 6, 3, 6000, 6000), pinned-location queries
- Each example: dataset description, shape, access patterns, chunking strategy chosen, rationale, code snippet

**references/COMMON_ISSUES.md:**
- Issue: Chunks too small for cloud storage (< 1 MB) → excessive HTTP requests
- Issue: Chunks too large → excessive memory usage and unnecessary data transfer
- Issue: Chunk orientation mismatched with access pattern → orders of magnitude slower
- Issue: Dask chunks not aligned with Zarr chunks → redundant decompression
- Issue: Total concurrency overflow → cloud storage throttling
- Issue: Sparse data with `write_empty_chunks=True` → 2x slower writes
- Each issue: symptoms, cause, solution with code, prevention

**Acceptance Criteria:**
- [ ] SKILL.md is 300+ lines with complete chunk sizing knowledge
- [ ] chunk-calculator.py is a working Python script
- [ ] chunk-decision-tree.md provides clear visual decision guidance
- [ ] PATTERNS.md covers 6+ distinct chunking patterns with code
- [ ] EXAMPLES.md has 4+ real-world case studies
- [ ] COMMON_ISSUES.md covers 6+ common mistakes

**Labels:** `enhancement`, `skill`

---

#### Issue 5: Create cloud-storage-benchmarking skill

**Title:** feat: Create cloud-storage-benchmarking skill for zarr-chunk-optimization plugin

**Description:**
Create the skill covering benchmark methodology, frameworks (ASV, pytest-benchmark), cloud-specific benchmarking, and results analysis.

**Directory:** `plugins/zarr-chunk-optimization/skills/cloud-storage-benchmarking/`

**Files to Create:**

**SKILL.md (300+ lines):**
- Frontmatter: `name: cloud-storage-benchmarking`, description with trigger phrases
- Quick Reference: benchmark setup checklist
- Core Concepts: benchmark design, metrics taxonomy, statistical requirements
- Benchmark metrics:
  - Wall time (seconds)
  - Peak memory (GB)
  - Throughput (MB/s)
  - Bytes transferred
  - Compression ratio
  - Requests count (for cloud stores)
- Framework coverage:
  - ASV setup and configuration (`asv.conf.json` structure)
  - ASV benchmark class patterns (time_*, mem_*, track_*)
  - pytest-benchmark fixtures and parameterization
  - pytest-benchmark comparison mode
- Cloud-specific considerations:
  - Network variability and warm-up runs
  - Cloud storage caching layers
  - Concurrency tuning (`zarr.config.set({'async.concurrency': N})`)
  - Instance-to-storage colocation for consistent results
- Dask Dashboard monitoring:
  - White space = inefficient chunks
  - Red bars = too much communication
  - Orange bars = memory pressure
  - Gray bars = disk spillage
- Results interpretation guidance
- Links to references

**assets/benchmark-template.py:**
- Complete, runnable benchmark script template that:
  - Creates a test Zarr array on a configurable storage backend
  - Tests multiple chunk configurations (parameterized)
  - Tests multiple access patterns (time-series, spatial map, mixed)
  - Measures wall time, peak memory, throughput
  - Uses `timeit` or `pytest-benchmark` for statistical rigor
  - Outputs results as CSV/JSON for analysis
  - Includes cloud backend configuration (S3/GCS/Azure with environment variables)

**assets/benchmark-config.yaml:**
- Template YAML configuration for benchmark parameters:
  ```yaml
  dataset:
    shape: [3650, 721, 1440]
    dtype: float32
    fill_value: NaN
  chunk_configs:
    temporal: [3650, 10, 10]
    spatial: [1, 721, 1440]
    balanced: [30, 90, 180]
  access_patterns:
    - type: timeseries
      selection: {lat: 0, lon: 0}
    - type: spatial_map
      selection: {time: 0}
  storage:
    backend: s3  # s3, gcs, azure, local
    bucket: my-benchmark-bucket
    prefix: benchmark-data/
  benchmark:
    runs: 10
    warmup: 3
    concurrency: [10, 32, 64, 128]
  ```

**assets/results-analysis.py:**
- Python script for analyzing benchmark results:
  - Reads benchmark CSV/JSON output
  - Generates comparison plots (matplotlib/hvplot)
  - Calculates speedup ratios between configurations
  - Identifies optimal configuration per access pattern
  - Generates summary report

**references/PATTERNS.md:**
- Pattern: ASV Benchmark Class for Zarr (complete class with setup/teardown)
- Pattern: pytest-benchmark Parameterized Chunk Comparison
- Pattern: Cloud Storage Warm-up Protocol
- Pattern: Concurrency Sweep Benchmark
- Pattern: Memory Profiling with tracemalloc
- Pattern: Results Visualization with hvplot/matplotlib

**references/EXAMPLES.md:**
- Example 1: Benchmarking 3 chunk configs on S3 with ASV
- Example 2: pytest-benchmark comparing compression codecs × chunk sizes
- Example 3: Concurrency tuning sweep on GCS
- Example 4: Full optimization workflow: benchmark → analyze → rechunk → validate

**references/COMMON_ISSUES.md:**
- Issue: Inconsistent results due to cloud caching → use warm-up runs
- Issue: Network variability masking real differences → increase run count, use median
- Issue: OOM during benchmarks → reduce chunk sizes or use Dask
- Issue: Benchmarks too slow → reduce dataset size proportionally
- Issue: Dask scheduler overhead dominating results → benchmark with and without Dask
- Issue: Comparing results across different cloud instances → normalize to throughput

**Acceptance Criteria:**
- [ ] SKILL.md is 300+ lines with complete benchmarking methodology
- [ ] benchmark-template.py is a runnable script with cloud backend support
- [ ] benchmark-config.yaml is a complete configuration template
- [ ] results-analysis.py generates comparison plots
- [ ] PATTERNS.md covers 6+ benchmarking patterns
- [ ] EXAMPLES.md has 4+ complete benchmark examples
- [ ] COMMON_ISSUES.md covers 6+ benchmarking pitfalls

**Labels:** `enhancement`, `skill`

---

#### Issue 6: Create rechunking-workflows skill

**Title:** feat: Create rechunking-workflows skill for zarr-chunk-optimization plugin

**Description:**
Create the skill covering the rechunker library, data migration rechunking, and validation workflows.

**Directory:** `plugins/zarr-chunk-optimization/skills/rechunking-workflows/`

**Files to Create:**

**SKILL.md (300+ lines):**
- Frontmatter: `name: rechunking-workflows`, description with trigger phrases
- Quick Reference: rechunker API summary
- Core rechunker API:
  ```python
  from rechunker import rechunk
  result = rechunk(source, target_chunks, target_store, max_mem, temp_store)
  result.execute()
  ```
- Architecture: source → intermediate staging → target (two-pass)
- Memory budget planning: how to set `max_mem` based on available RAM
- Temporary storage requirements: approximately equal to dataset size
- When to rechunk vs. when to create new (threshold: is rechunking cheaper than re-generating?)
- Zarr copy operations as alternative:
  - `zarr.copy()` — individual array copy
  - `zarr.copy_all()` — group-level copy
  - `zarr.copy_store()` — store-level (no decompression/recompression)
- HDF5/NetCDF → Zarr migration with rechunking
- Validation: comparing source and target data integrity
- Links to references

**assets/rechunk-template.py:**
- Complete rechunking script template:
  - Opens source Zarr store (local or cloud)
  - Configures target chunks based on optimization analysis
  - Sets memory budget
  - Creates target store (local or cloud)
  - Executes rechunking
  - Validates data integrity (random sample comparison)
  - Cleans up temporary storage

**references/PATTERNS.md:**
- Pattern: Simple Rechunking (single array, local storage)
- Pattern: Cloud-to-Cloud Rechunking (S3 source → S3 target)
- Pattern: HDF5 → Cloud-Optimized Zarr
- Pattern: NetCDF → Cloud-Optimized Zarr with xarray
- Pattern: Incremental Rechunking (processing in batches)
- Pattern: Validation After Rechunking

**references/EXAMPLES.md:**
- Example 1: Rechunking climate data from spatial to temporal chunks
- Example 2: Migrating HDF5 data to Zarr on S3 with optimal chunks
- Example 3: Rechunking with Dask for very large datasets
- Example 4: Complete workflow: benchmark → decide → rechunk → validate → benchmark again

**references/COMMON_ISSUES.md:**
- Issue: Insufficient temporary storage → calculate required space first
- Issue: OOM during rechunking → reduce `max_mem`, use smaller intermediate chunks
- Issue: Data corruption after rechunking → always validate with sample comparison
- Issue: Rechunking from very different chunk shapes (pathological) → use intermediate NumPy
- Issue: Cloud permissions for temp storage → ensure write access to both temp and target
- Issue: Rechunker hanging on large datasets → check Dask scheduler status

**Acceptance Criteria:**
- [ ] SKILL.md is 300+ lines covering rechunker API and workflows
- [ ] rechunk-template.py is a working rechunking script
- [ ] PATTERNS.md covers 6+ rechunking patterns
- [ ] EXAMPLES.md has 4+ complete examples
- [ ] COMMON_ISSUES.md covers 6+ issues

**Labels:** `enhancement`, `skill`

---

### PLUGIN 2: zarr-data-format

---

#### Issue 7: Create plugin scaffold for zarr-data-format

**Title:** feat: Create zarr-data-format plugin scaffold

**Description:**
Create the initial plugin directory structure and metadata for the zarr-data-format plugin.

**Acceptance Criteria:**
- [ ] Create `plugins/zarr-data-format/.claude-plugin/plugin.json` with:
  ```json
  {
    "name": "zarr-data-format",
    "description": "Comprehensive agents and skills for working with the Zarr array storage format",
    "version": "0.1.0",
    "author": {
      "name": "SSEC Research Team",
      "url": "https://github.com/uw-ssec"
    }
  }
  ```
- [ ] Create empty directories: `agents/`, `skills/zarr-fundamentals/`, `skills/compression-codecs/`, `skills/cloud-storage-backends/`, `skills/zarr-xarray-integration/`, `skills/data-migration/`
- [ ] Create `LICENSE` (BSD-3-Clause, symlink to root)
- [ ] Add plugin entry to `.claude-plugin/marketplace.json`:
  ```json
  {
    "name": "zarr-data-format",
    "source": "./plugins/zarr-data-format",
    "description": "Comprehensive agents and skills for working with the Zarr array storage format",
    "homepage": "https://github.com/uw-ssec/rse-plugins",
    "repository": "https://github.com/uw-ssec/rse-plugins",
    "license": "BSD-3-Clause",
    "keywords": ["zarr", "array-storage", "cloud-native", "compression", "xarray", "dask", "hdf5", "netcdf", "scientific-computing", "data-format"],
    "category": "data-science",
    "strict": false
  }
  ```
- [ ] Create `README.md` documenting the plugin

**Labels:** `enhancement`, `plugin`

---

#### Issue 8: Create zarr-expert agent

**Title:** feat: Create zarr-expert agent for zarr-data-format plugin

**Description:**
Create the primary Zarr expert agent that provides comprehensive guidance on all Zarr operations.

**File:** `plugins/zarr-data-format/agents/zarr-expert.md`

**Agent Specification:**

**Frontmatter:**
```yaml
name: zarr-expert
description: |
  Comprehensive Zarr format expert for creating, reading, writing, and managing chunked, compressed, N-dimensional arrays. Deep knowledge of Zarr v2 and v3 specifications, compression codecs, storage backends, metadata management, hierarchical groups, advanced indexing, and integration with xarray, Dask, and the broader scientific Python ecosystem.

  Use this agent when the user asks to "create a zarr array", "read zarr data", "write to zarr store", "configure zarr compression", "set up zarr groups", "work with zarr metadata", "convert data to zarr", "use zarr with xarray", "understand zarr format", or needs general Zarr guidance.

  <example>
  Context: User needs to create a Zarr store
  user: "I need to create a Zarr v3 store with hierarchical groups for my climate model output"
  assistant: "I'll use the zarr-expert agent to help you design the group hierarchy and create the store with appropriate settings."
  <commentary>
  Zarr group creation, hierarchy design, and metadata management are core Zarr operations handled by this agent.
  </commentary>
  </example>

  <example>
  Context: User needs compression guidance
  user: "What compression codec should I use for my float64 temperature data in Zarr?"
  assistant: "I'll invoke the zarr-expert agent to recommend a codec based on your data characteristics and access requirements."
  <commentary>
  Codec selection depends on data type, compression ratio requirements, and speed trade-offs.
  </commentary>
  </example>

  <example>
  Context: User needs format migration
  user: "I have 500 NetCDF files I need to convert to a single Zarr store"
  assistant: "I'll use the zarr-expert agent to plan the migration workflow using xarray and appropriate chunking."
  <commentary>
  Multi-file NetCDF to Zarr migration requires careful handling of concatenation, chunking, and metadata.
  </commentary>
  </example>

  <example>
  Context: User working with Zarr and xarray
  user: "How do I append new timesteps to an existing Zarr store using xarray?"
  assistant: "I'll use the zarr-expert to guide you through xarray's append_dim and region write capabilities for Zarr stores."
  <commentary>
  Zarr append operations via xarray require specific mode and dimension settings.
  </commentary>
  </example>
model: inherit
color: cyan
skills:
  - zarr-fundamentals
  - compression-codecs
  - cloud-storage-backends
  - zarr-xarray-integration
  - data-migration
```

**Agent Body Content Must Include (800-1000+ lines):**

1. **Purpose** — Comprehensive Zarr format expert covering the full lifecycle of array data storage.

2. **Core Knowledge Base:**
   - Zarr v2 vs v3 specification differences
   - Array creation, configuration, and management
   - Group hierarchies and metadata
   - All indexing modes (basic, coordinate, mask, orthogonal, block)
   - Compression codec selection and configuration
   - Storage backend options (local, cloud, database)
   - Thread/process safety and synchronization
   - Data types (numeric, string, object, datetime, ragged arrays)
   - Sharding (v3 extension)
   - Metadata consolidation

3. **Workflow Patterns:**
   - Array Creation: choose dtype → select chunks → configure compression → set metadata
   - Data I/O: open store → select data → read with appropriate indexing → process
   - Cloud Access: configure backend → set credentials → open remote store → read/write
   - Migration: assess source format → plan chunk layout → migrate → validate → consolidate metadata

4. **Decision-Making Framework** using `<thinking>` blocks

5. **Capabilities** organized by category:
   - Array Operations (create, read, write, resize, append)
   - Group Management (create, navigate, tree)
   - Compression (codec selection, filter configuration)
   - Storage (backend selection, cloud configuration)
   - Integration (xarray, Dask, pandas)
   - Migration (HDF5, NetCDF, VirtualiZarr)

6. **Error Handling** for common Zarr scenarios

**Acceptance Criteria:**
- [ ] Agent file is 800-1000+ lines
- [ ] Covers Zarr v2 and v3
- [ ] Includes all indexing modes
- [ ] Covers all storage backends
- [ ] Includes migration workflows
- [ ] References all 5 skills

**Labels:** `enhancement`, `agent`

---

#### Issue 9: Create zarr-cloud-architect agent

**Title:** feat: Create zarr-cloud-architect agent for zarr-data-format plugin

**Description:**
Create the cloud storage specialist agent for Zarr integration with S3, GCS, and Azure Blob.

**File:** `plugins/zarr-data-format/agents/zarr-cloud-architect.md`

**Agent Specification:**

**Frontmatter:**
```yaml
name: zarr-cloud-architect
description: |
  Specialist in integrating Zarr with cloud object stores (AWS S3, Google Cloud Storage, Azure Blob Storage). Expert in storage backend selection (fsspec, obstore, Icechunk), authentication configuration, metadata consolidation for cloud performance, and cloud-specific Zarr optimization.

  Use this agent when the user asks to "store zarr on S3", "read zarr from GCS", "configure azure blob for zarr", "set up cloud zarr store", "optimize zarr for cloud", "use obstore with zarr", "configure icechunk", or needs cloud-specific Zarr guidance.

  <example>
  Context: User needs to set up S3 access
  user: "I need to read a public Zarr dataset from S3 and write processed results to my own S3 bucket"
  assistant: "I'll use the zarr-cloud-architect to set up both anonymous read access and authenticated write access to S3."
  <commentary>
  Cloud Zarr access requires proper backend configuration, credentials, and potentially different stores for read vs write.
  </commentary>
  </example>

  <example>
  Context: User choosing between storage backends
  user: "Should I use fsspec or obstore to access my Zarr data on GCS?"
  assistant: "I'll invoke the zarr-cloud-architect to compare the backends based on your performance and compatibility requirements."
  <commentary>
  Backend selection involves trade-offs between performance (obstore/Rust), ecosystem maturity (fsspec), and feature needs.
  </commentary>
  </example>
model: inherit
color: green
skills:
  - cloud-storage-backends
  - zarr-fundamentals
```

**Agent Body Content Must Include (500-800+ lines):**

1. **Purpose** — Cloud storage integration specialist for Zarr

2. **Storage Backend Expertise:**
   - fsspec ecosystem: s3fs, gcsfs, adlfs, aiohttp
   - obstore: Rust-based, high-throughput, S3/GCS/Azure via `object_store` crate
   - Icechunk: versioned, ACID transactions, Rust-based
   - When to use each backend (performance vs compatibility matrix)

3. **Cloud Provider Configuration:**
   - AWS S3: credentials, regions, endpoint URLs, anonymous access
   - GCS: project IDs, service accounts, anonymous access
   - Azure Blob: connection strings, SAS tokens, managed identity

4. **Performance Optimization:**
   - Metadata consolidation
   - Concurrency tuning per cloud provider
   - Caching layers (simplecache::, filecache::)
   - Sharding for reducing object count

5. **Security and Access Patterns:**
   - IAM roles and policies
   - Pre-signed URLs
   - Cross-region access considerations

**Acceptance Criteria:**
- [ ] Agent file is 500-800+ lines
- [ ] Covers S3, GCS, and Azure Blob in depth
- [ ] Compares fsspec vs obstore vs Icechunk
- [ ] Includes authentication patterns for all providers
- [ ] Covers metadata consolidation for cloud

**Labels:** `enhancement`, `agent`

---

#### Issue 10: Create zarr-fundamentals skill

**Title:** feat: Create zarr-fundamentals skill for zarr-data-format plugin

**Description:**
Create the core Zarr operations skill covering array creation, I/O, metadata, groups, and indexing.

**Directory:** `plugins/zarr-data-format/skills/zarr-fundamentals/`

**Files to Create:**

**SKILL.md (400+ lines):**
- Quick Reference: essential zarr imports and operations
- Installation (pixi, pip, conda-forge)
- Zarr v2 vs v3 differences and when to use each
- Array creation: `zarr.create_array()`, `zarr.zeros()`, `zarr.ones()`, `zarr.open_array()`
- Group management: `zarr.create_group()`, `zarr.open_group()`, `.tree()`
- Metadata: `.attrs`, `.info`, `.info_complete()`, CF conventions
- Indexing modes: basic slicing, coordinate, mask, orthogonal, block
- Data types: numeric, string (fixed/variable), object, datetime, ragged
- Thread/process safety: `ThreadSynchronizer`, `ProcessSynchronizer`
- Sharding (v3): `shards` parameter, implications
- v2 → v3 migration notes

**assets/zarr-quickstart.py:**
- Complete quickstart script: create array, write data, read data, inspect, add metadata

**references/PATTERNS.md:**
- Pattern: Creating a hierarchical Zarr store with metadata
- Pattern: Opening and reading remote Zarr data
- Pattern: Appending data to existing array
- Pattern: Advanced indexing (orthogonal, block, coordinate)
- Pattern: Using shards in Zarr v3
- Pattern: Synchronization for concurrent access

**references/EXAMPLES.md:**
- Example 1: Creating a scientific dataset from scratch
- Example 2: Reading and querying a remote Zarr store
- Example 3: Building a hierarchical store with groups and metadata
- Example 4: Working with structured/ragged arrays

**references/COMMON_ISSUES.md:**
- Issue: Zarr v2 vs v3 API confusion
- Issue: Metadata not persisting (need explicit `.attrs` write)
- Issue: Memory errors with large arrays (chunking not configured)
- Issue: Concurrent write corruption (missing synchronizer)
- Issue: `.info_complete()` slow on large arrays

**Acceptance Criteria:**
- [ ] SKILL.md is 400+ lines
- [ ] Covers both v2 and v3 APIs
- [ ] All 6 indexing modes documented with examples
- [ ] Quick start script works end-to-end

**Labels:** `enhancement`, `skill`

---

#### Issue 11: Create compression-codecs skill

**Title:** feat: Create compression-codecs skill for zarr-data-format plugin

**Description:**
Create the skill covering all compression codecs, filters, and codec configuration for Zarr.

**Directory:** `plugins/zarr-data-format/skills/compression-codecs/`

**Files:**

**SKILL.md (300+ lines):**
- All codecs: Blosc (blosclz, lz4, lz4hc, snappy, zlib, zstd), Zstd, Gzip, LZ4, LZMA, BZ2, Zlib
- Codec selection decision tree (speed vs ratio vs compatibility)
- Blosc configuration: cname, clevel, shuffle modes (NOSHUFFLE, SHUFFLE, BITSHUFFLE)
- Pre-compression filters: Delta, Quantize, FixedScaleOffset, PackBits, Categorize
- Integrity checks: CRC32, Adler32
- Blosc thread safety: `blosc.use_threads`, `blosc.set_nthreads()`
- Default codec override: `zarr.storage.default_compressor`
- Zarr v3 codec pipeline configuration
- numcodecs registry

**assets/codec-comparison.py:**
- Script benchmarking different codecs on sample data, reporting compression ratio and speed

**references/ (PATTERNS.md, EXAMPLES.md, COMMON_ISSUES.md)**

**Acceptance Criteria:**
- [ ] All codec families documented
- [ ] Filter system documented
- [ ] Blosc thread safety covered
- [ ] codec-comparison.py produces meaningful results

**Labels:** `enhancement`, `skill`

---

#### Issue 12: Create cloud-storage-backends skill

**Title:** feat: Create cloud-storage-backends skill for zarr-data-format plugin

**Description:**
Create the skill covering all Zarr storage backends with focus on cloud providers.

**Directory:** `plugins/zarr-data-format/skills/cloud-storage-backends/`

**Files:**

**SKILL.md (300+ lines):**
- Complete storage backend inventory table (15+ backends)
- fsspec-based access (s3fs, gcsfs, adlfs)
- obstore access (Rust-based, high-performance)
- Icechunk (versioned, ACID)
- URL shorthand patterns (`s3://`, `gs://`, `az://`)
- Authentication per cloud provider
- Caching layers (simplecache::, filecache::)
- Metadata consolidation for cloud performance
- Cloud data catalogs (Planetary Computer, AWS Open Data, Pangeo-Forge)

**assets/ (s3-config-template.py, gcs-config-template.py, azure-config-template.py)**

**references/ (PATTERNS.md, EXAMPLES.md, COMMON_ISSUES.md)**

**Acceptance Criteria:**
- [ ] All 15+ storage backends documented
- [ ] All 3 major cloud providers have config templates
- [ ] fsspec vs obstore vs Icechunk comparison included
- [ ] Metadata consolidation documented

**Labels:** `enhancement`, `skill`

---

#### Issue 13: Create zarr-xarray-integration skill

**Title:** feat: Create zarr-xarray-integration skill for zarr-data-format plugin

**Description:**
Create the skill covering xarray + Zarr workflows including read, write, append, region writes, and Dask integration.

**Directory:** `plugins/zarr-data-format/skills/zarr-xarray-integration/`

**Files:**

**SKILL.md (300+ lines):**
- `xr.open_zarr()` and `xr.open_dataset(engine='zarr')` — differences and when to use each
- `ds.to_zarr()` — all write modes:
  - `mode='w'` — overwrite
  - `mode='a'` — append/add variables
  - `append_dim="time"` — resize and append along dimension
  - `region="auto"` — auto-aligned region write
  - `region={"x": slice(10, 20)}` — explicit region write
  - `compute=False` — metadata-only write (for distributed fills)
- Encoding control: compression, chunks, dtype
  - Precedence: manual encoding > Dask chunks > Zarr defaults
- `chunks="auto"` vs `chunks={}` — when to use each
- Distributed write pattern (metadata-only then parallel region fills)
- Cloud access via backend_kwargs and storage_options
- Consolidated metadata with xarray
- Dask integration: lazy loading, compute triggers, memory management

**references/ (PATTERNS.md, EXAMPLES.md, COMMON_ISSUES.md)**

**Acceptance Criteria:**
- [ ] All xarray write modes documented with examples
- [ ] Encoding control fully covered
- [ ] Distributed write pattern documented
- [ ] Cloud access patterns for all providers
- [ ] Dask interaction patterns

**Labels:** `enhancement`, `skill`

---

#### Issue 14: Create data-migration skill

**Title:** feat: Create data-migration skill for zarr-data-format plugin

**Description:**
Create the skill covering data migration from HDF5/NetCDF to Zarr, and VirtualiZarr for zero-copy access.

**Directory:** `plugins/zarr-data-format/skills/data-migration/`

**Files:**

**SKILL.md (300+ lines):**
- zarr.copy(), zarr.copy_all(), zarr.copy_store() — uses and differences
- copy_store: efficient store-to-store (no decompression/recompression)
- HDF5 → Zarr migration with h5py
- NetCDF → Zarr migration with xarray
- Multi-file NetCDF → single Zarr store
- VirtualiZarr: zero-copy ingestion of archival formats
  - `virtualizarr.open_virtual_dataset()`
  - Persisting virtual datasets to Icechunk
  - Performance advantages over traditional conversion
- Validation: comparing source and target data integrity
- Handling coordinate systems, metadata preservation
- Large-scale migration strategies

**assets/migration-template.py:**
- Script template for HDF5/NetCDF → Zarr migration with validation

**references/ (PATTERNS.md, EXAMPLES.md, COMMON_ISSUES.md)**

**Acceptance Criteria:**
- [ ] All zarr copy operations documented
- [ ] HDF5 and NetCDF migration covered
- [ ] VirtualiZarr documented with examples
- [ ] Migration template script works end-to-end
- [ ] Validation patterns included

**Labels:** `enhancement`, `skill`

---

## References

**Files Analyzed:**
- `.claude-plugin/marketplace.json` — Plugin registry
- `plugins/scientific-domain-applications/.claude-plugin/plugin.json` — Plugin metadata pattern
- `plugins/scientific-python-development/.claude-plugin/plugin.json` — Plugin metadata pattern
- `plugins/scientific-domain-applications/agents/astronomy-astrophysics-expert.md` — Agent definition pattern
- `plugins/scientific-domain-applications/skills/xarray-for-multidimensional-data/SKILL.md` — Skill definition pattern
- Full directory trees of 5 existing plugins explored via sub-agent

**External Sources:**
- [Zarr Performance Guide](https://zarr.readthedocs.io/en/latest/user-guide/performance/) — Official chunk size guidance, sharding, concurrency, empty chunks
- [ESIP Cloud Computing Resources](https://esipfed.github.io/cloud-computing-cluster/resources-for-optimization.html) — Cloud optimization standards
- [Xarray Zarr Tutorial](https://tutorial.xarray.dev/intermediate/intro-to-zarr.html) — 63x benchmark, compression, cloud access
- [HackMD Zarr Data Manipulation](https://hackmd.io/@brivadeneira/rkqm_XYHgg) — Domain-specific chunking strategies, Azure Blob
- [Cloud-Native Geo Zarr Guide](https://guide.cloudnativegeo.org/zarr/zarr-in-practice.html) — Practical chunking, compression ratios
- [Zarr-Python 3 Release](https://zarr.dev/blog/zarr-python-3-release/) — v3 features, sharding, async I/O
- [Pangeo Cloud Storage Benchmark](https://gallery.pangeo.io/repos/earthcube2020/ec20_abernathey_etal/cloud_storage.html) — Cloud throughput profiling
- [Earthmover I/O-Maxing Tensors](https://earthmover.io/blog/i-o-maxing-tensors-in-the-cloud/) — Obstore/Icechunk throughput
- [Benchmark Zarr Implementations (GSoC)](https://hackmd.io/@I9Hj1bLETn6QIva97pA3Hw/By7rlRXd5) — ASV benchmark suite
- [Zarr Sharding ZEP 0002](https://zarr.dev/zeps/accepted/ZEP0002.html) — Sharding specification
- [Zarr Everywhere (Development Seed)](https://developmentseed.org/blog/2025-10-13-zarr/) — Ecosystem overview 2025
- [Rechunker Documentation](https://rechunker.readthedocs.io/en/latest/tutorial.html) — Rechunking API
- [Impact of Chunk Size on Read Performance (Nguyen et al. 2023)](https://essopenarchive.org/users/532985/articles/598065-impact-of-chunk-size-on-read-performance-of-zarr-data-in-cloud-based-object-stores) — Key research paper
- [Zarr v3 Spec](https://zarr-specs.readthedocs.io/en/latest/v3/core/v3.0.html) — Format specification

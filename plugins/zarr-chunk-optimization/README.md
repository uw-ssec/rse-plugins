# Zarr Chunk Optimization Plugin

Benchmarks Zarr chunking strategies for multi-dimensional datasets on cloud object stores (S3, GCS). Based on Nguyen et al. (2023) methodology. Measures wall-clock time, peak memory, and I/O metrics across spatial, time-series, and spectral access patterns.

## Agents

| Agent | Description |
|-------|-------------|
| **benchmarking-agent** | Zarr chunking optimization expert for multi-dimensional scientific datasets on cloud object stores |

## Skills

| Skill | Description |
|-------|-------------|
| **chunking-strategy** | Core benchmarking methodology, access pattern analysis, performance interpretation, and cloud storage patterns |
| **synthetic-data** | Generate synthetic Zarr datasets with configurable dimensions, shapes, and compression for controlled benchmarks |
| **rechunking** | Safely apply chunking configurations with validation, progress reporting, and rollback safety |

## Commands

| Command | Description |
|---------|-------------|
| `/benchmark` | Run chunking benchmarks across access patterns and collect wall-clock time, peak memory, and I/O metrics |
| `/rechunk` | Rechunk a production dataset with validation and safety checks |
| `/tradeoffs` | Analyze trade-offs between spatial, temporal, and spectral access performance for a given chunk configuration |

## When to Use

- Optimizing chunk shapes for Zarr datasets with mixed access patterns
- Benchmarking chunking configurations before committing to rechunking
- Analyzing trade-offs between spatial, temporal, and spectral access performance
- Rechunking production datasets with validation and safety checks
- Generating synthetic datasets for controlled benchmarking experiments

## Out of Scope

- General-purpose array storage format selection (Zarr vs HDF5 vs NetCDF)
- Cloud infrastructure provisioning
- Data pipeline orchestration
- Compression algorithm selection (focus is on chunk shape, not codec)

## Related Plugins

| Plugin | Use For |
|--------|---------|
| **scientific-domain-applications** | Xarray/Zarr data handling and multidimensional scientific data analysis |
| **scientific-python-development** | Packaging, testing, and modern Scientific Python development practices |

## Research Basis

This plugin implements the benchmarking methodology described in Nguyen et al. (2023), "Optimizing Zarr Chunk Configurations for Cloud-Based Access Patterns." DOI: [10.1109/MCSE.2023.3302524](https://doi.org/10.1109/MCSE.2023.3302524)

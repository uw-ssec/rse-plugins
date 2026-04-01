# Zarr Data Format Plugin

Comprehensive agents and skills for working with the Zarr array storage format — covering array creation, compression codecs, cloud storage backends, xarray/Dask integration, and data migration from HDF5/NetCDF.

## Agents

| Agent | Description |
|-------|-------------|
| **zarr-expert** | Primary Zarr format expert — array creation, I/O, metadata, groups, indexing, compression, and integration with xarray/Dask |
| **zarr-cloud-architect** | Cloud storage integration specialist — S3, GCS, Azure Blob, fsspec, obstore, Icechunk backends |

## Skills

| Skill | Description |
|-------|-------------|
| **zarr-fundamentals** | Core Zarr operations — array creation, groups, metadata, indexing modes, data types, thread/process safety, v2 vs v3 |
| **compression-codecs** | Compression codec selection and configuration — Blosc, Zstd, LZ4, filters, codec pipelines, benchmarking |
| **cloud-storage-backends** | Cloud object store integration — S3, GCS, Azure, fsspec, obstore, Icechunk, authentication, caching |
| **zarr-xarray-integration** | Zarr + xarray workflows — reading, writing, appending, multi-file datasets, Dask chunking alignment |
| **data-migration** | Format migration — HDF5/NetCDF to Zarr, VirtualiZarr, zarr.copy operations, validation |

## When to Use

- Creating, reading, or writing Zarr arrays and groups
- Choosing and configuring compression codecs for scientific data
- Setting up Zarr stores on cloud object storage (S3, GCS, Azure)
- Integrating Zarr with xarray and Dask for large-scale analysis
- Migrating data from HDF5, NetCDF, or other formats to Zarr
- Understanding Zarr v2 vs v3 differences and migration paths

## Out of Scope

- Chunk size optimization and benchmarking (use **zarr-chunk-optimization** plugin)
- General xarray operations not specific to Zarr (use **scientific-domain-applications** plugin)
- Cloud infrastructure provisioning and management
- Data pipeline orchestration beyond format conversion

## Related Plugins

| Plugin | Use For |
|--------|---------|
| **zarr-chunk-optimization** | Benchmarking and optimizing chunk configurations for specific access patterns |
| **scientific-domain-applications** | General xarray operations, AstroPy, and domain-specific scientific computing |
| **scientific-python-development** | Packaging, testing, and modern Scientific Python development practices |

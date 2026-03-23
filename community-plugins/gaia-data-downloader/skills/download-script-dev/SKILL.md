---
name: download-script-dev
description: >
  This skill should be used when the user asks to "develop a download script",
  "debug data download", "fix download error", "create data pipeline template",
  "download template", "GAIA data pipeline", "download from S3", "access Zarr store",
  "cloud data access", or mentions specific data source names like "CONUS404", "HRRR",
  "WRF", "PRISM", "Stage IV", "USGS", "ORNL", "DEM", "Synoptic", or "IRIS" in the
  context of downloading or processing data. Provides templates, configuration
  validation, and debugging guidance for hydroclimatological data download scripts
  used in the GAIA project.
version: 2026-03-20
compatibility: >
  Requires Python 3.9+, xarray, geopandas, rioxarray.
  Source-specific: herbie-data (HRRR), pyPRISMClimate (PRISM), obspy (IRIS),
  boto3 (WRF/S3), elevation (DEM), s3fs (CONUS404).
---

# Download Script Development Skill

## Overview

Assist in developing, refining, and debugging data download scripts for GAIA hydroclimatological data sources. This skill provides templates, configuration schemas, and troubleshooting guidance for building reproducible data pipelines across 10+ environmental data sources.

## When to Use

- Developing a new download script for a GAIA data source
- Debugging an existing download script (timeouts, auth errors, CRS mismatches)
- Adapting a notebook pattern to a new use case or study area
- Validating download configuration parameters
- Understanding which access pattern or library to use for a data source

## Script Structure Pattern

All download scripts follow a CONFIG-at-top pattern separating parameters from logic:

```python
import xarray as xr
import geopandas as gpd
from concurrent.futures import ThreadPoolExecutor

# ============================================================
# Configuration — modify these parameters before running
# ============================================================
CONFIG = {
    "source": "SOURCE_NAME",
    "date_range": ("2024-01-01", "2024-01-31"),
    "variables": ["var1", "var2"],
    "aoi_path": "../data/GIS/boundary.json",
    "output_path": "../data/output.zarr",
    "output_format": "zarr",
    "max_workers": 8,
}
# ============================================================
# Download logic — generally no need to modify below this line
# ============================================================

def main():
    # 1. Load AOI
    aoi = gpd.read_file(CONFIG["aoi_path"])

    # 2. Download data (parallel)
    # 3. Combine datasets
    # 4. Spatial subset
    # 5. Derive variables (if needed)
    # 6. Save to output format
    # 7. Print QC summary
    pass

if __name__ == "__main__":
    main()
```

## Four Data Access Patterns

### 1. Direct HTTP Download (PRISM, Stage IV, DEM)

Simple URL-based fetching with `requests`. Use `ThreadPoolExecutor` for parallel downloads. Handle retries for network failures.

### 2. REST API Query (USGS, Synoptic)

Parameterized endpoints returning JSON or RDB format. Build URL query strings from CONFIG parameters. Parse response formats appropriately (RDB requires custom parsing).

### 3. Cloud Object Storage / S3 (CONUS404, HRRR, WRF-CMIP6)

Access via `s3fs`, `boto3`, or library wrappers. Supports partial reads and lazy loading with `xarray.open_zarr()`. Use anonymous/unsigned credentials for public buckets.

### 4. Specialized Libraries (Herbie for HRRR, pyPRISMClimate, obspy for IRIS)

Domain-specific wrappers that handle authentication, URL construction, and data parsing internally. Consult library documentation for parameter conventions.

## Spatial Subsetting Methods

Choose based on grid type:

| Grid Type | Method | When to Use |
|-----------|--------|-------------|
| Regular (lat/lon) | `ds.rio.clip(aoi.geometry)` | PRISM, Stage IV, DEM |
| Curvilinear (model) | `regionmask` | CONUS404, WRF-CMIP6 |
| Irregular (points) | `shapely.contains()` | USGS station data |

Ensure the AOI CRS matches the data CRS before subsetting. Model grids often use Lambert Conformal Conic — reproject the AOI with `aoi.to_crs(ds.rio.crs)`.

## Parallel Download Pattern

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def download_item(item):
    """Download a single item. Return path or dataset."""
    # ... download logic
    return result

with ThreadPoolExecutor(max_workers=CONFIG["max_workers"]) as executor:
    futures = {executor.submit(download_item, item): item for item in items}
    for i, future in enumerate(as_completed(futures), 1):
        result = future.result()
        print(f"Downloaded {i}/{len(items)}")
```

Worker count guidance: 4-8 for HTTP downloads, 8-16 for S3 reads, 2-4 for API endpoints with rate limits.

## Output Formats

| Format | When to Use | Trade-offs |
|--------|-------------|------------|
| **Zarr** (preferred) | Large gridded datasets, cloud workflows | Fast parallel I/O, chunked, no single-file limit |
| **NetCDF** | Sharing with traditional tools, small datasets | Widely supported, single-file, 2 GB limit (classic) |
| **CSV** | Tabular station data (USGS) | Human-readable, no spatial metadata |

## Common Issues and Debugging

### wgrib2 Not Found (HRRR)

`wgrib2` is a C binary, not pip-installable. Install via conda-forge: `conda install -c conda-forge wgrib2` or `pixi add wgrib2`. Verify with `shutil.which("wgrib2")`.

### S3 Authentication Errors (CONUS404, WRF)

Public buckets require anonymous access. For CONUS404: set `anon=True` in `s3fs.S3FileSystem()`. For WRF: use `botocore.UNSIGNED` config in boto3.

### CRS Mismatch During Spatial Subsetting

If `rio.clip()` raises a CRS error, reproject the AOI: `aoi = aoi.to_crs(ds.rio.crs)`. For datasets without CRS metadata, set it explicitly: `ds.rio.write_crs("EPSG:4326", inplace=True)`.

### Memory Issues with Large Datasets

Use chunked loading: `xr.open_dataset(path, chunks={"time": 100})`. Process in temporal batches rather than loading the full dataset. Monitor with `ds.nbytes / 1e9` to check size in GB.

### Network Timeouts and Retries

Wrap downloads in retry logic with exponential backoff. Use `requests.Session()` with `urllib3.util.retry.Retry` for HTTP sources. For S3, boto3 has built-in retry configuration.

### USGS RDB Format Parsing

USGS returns tab-separated RDB format with comment headers (`#`). Skip comment lines, parse the header row, and handle the data type row (second header line) before reading data.

## Additional Resources

### Reference Files

For detailed data source documentation, code templates, and configuration schemas, consult:

- **`references/sources/`** — Per-source documentation files (e.g., `sources/hrrr.md`, `sources/conus404.md`): endpoints, response formats, authentication setup, and example API calls. Load only the source relevant to the current task.
- **`references/DOWNLOAD_PATTERNS.md`** — Complete code templates for each access pattern with full pipeline examples for HRRR, CONUS404, and USGS
- **`references/CONFIGURATION.md`** — Per-source parameter tables with types, defaults, and validation rules; size estimation formulas

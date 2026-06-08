---
name: download-script-dev
description: Use this skill when users ask to "develop a download script", "debug data download", "fix download error", "create data pipeline template", "download template", "GAIA data pipeline", "download from S3", "access Zarr store", "cloud data access", or mention sources like CONUS404, HRRR, WRF, PRISM, Stage IV, USGS, ORNL, DEM, Synoptic, or IRIS. Generates CONFIG-at-top Python download scripts, validates source-specific configuration (auth, endpoint/path, date range, variables, AOI/CRS, and output format), and diagnoses common failures (403/auth, timeout/retry, CRS mismatch, missing binaries, and partial downloads).
version: 2026-05-31
metadata:
  references:
    - references/DOWNLOAD_PATTERNS.md
    - references/CONFIGURATION.md
    - references/DATA_SOURCES.md
---

# Download Script Development Skill

## Requirements

- **Python 3.9+** with `xarray`, `geopandas`, `rioxarray`
- **Source-specific libraries:** `herbie-data` (HRRR), `pyPRISMClimate` (PRISM), `obspy` (IRIS), `boto3` (WRF/S3), `elevation` (DEM), `s3fs` (CONUS404)
- **System dependencies:** `wgrib2` for HRRR (`conda install -c conda-forge wgrib2`, not pip)

## Script Structure Pattern

All download scripts follow CONFIG-at-top separating parameters from logic. Complete templates for each source are in [`references/DOWNLOAD_PATTERNS.md`](references/DOWNLOAD_PATTERNS.md).

```python
import xarray as xr
import geopandas as gpd
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# ============================================================
# Configuration — modify these parameters before running
# ============================================================
CONFIG = {
    "source": "SOURCE_NAME",
    "date_range": ("2024-01-01", "2024-01-31"),
    "variables": ["var1", "var2"],
    "aoi_path": "../data/GIS/boundary.json",
    "output_path": "../data/output.zarr",
    "output_format": "zarr",   # "zarr" | "netcdf" | "csv"
    "max_workers": 8,
}
# ============================================================
# Download logic — generally no need to modify below this line
# ============================================================

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)


def validate_config(cfg):
    required = ["source", "date_range", "variables", "output_path", "output_format"]
    missing = [k for k in required if not cfg.get(k)]
    if missing:
        raise ValueError(f"Missing config keys: {missing}")


def validate_aoi(aoi):
    if aoi.empty:
        raise ValueError("AOI GeoDataFrame is empty — check aoi_path")
    if aoi.crs is None:
        raise ValueError("AOI CRS is None — set CRS before subsetting")


def download_with_retry(item, download_fn, retries=3, backoff=2):
    """Run download_fn(item) with exponential backoff on failure."""
    import time
    for attempt in range(retries):
        try:
            return download_fn(item)
        except Exception as e:
            if attempt == retries - 1:
                raise
            wait = backoff ** attempt
            log.warning(f"Attempt {attempt+1} failed for {item}: {e}. Retrying in {wait}s")
            time.sleep(wait)


def main():
    # Step 0: Validate configuration
    validate_config(CONFIG)
    log.info(f"Starting {CONFIG['source']} download: {CONFIG['date_range']}")

    # Step 1: Load and validate AOI
    aoi = gpd.read_file(CONFIG["aoi_path"])
    validate_aoi(aoi)
    log.info(f"AOI loaded: {len(aoi)} feature(s), CRS={aoi.crs}")

    # Step 2: Build item list and download with retry + failure capture
    items = []  # populate with dates, URLs, or identifiers for this source
    failed = []
    results = []
    with ThreadPoolExecutor(max_workers=CONFIG["max_workers"]) as executor:
        futures = {executor.submit(download_with_retry, item, _download_item): item
                   for item in items}
        for i, future in enumerate(as_completed(futures), 1):
            item = futures[future]
            try:
                results.append(future.result())
                log.info(f"[{i}/{len(items)}] Downloaded {item}")
            except Exception as e:
                log.error(f"FAILED {item}: {e}")
                failed.append((item, str(e)))

    # Step 3: Validate completeness — fail hard if any items are missing
    if failed:
        log.error(f"{len(failed)} items failed after retries: {[f[0] for f in failed]}")
        raise RuntimeError(
            f"Download incomplete: {len(failed)}/{len(items)} failed. "
            "Fix CONFIG or network issues, then re-run."
        )
    expected = len(items)
    assert len(results) == expected, f"Expected {expected} results, got {len(results)}"

    # Step 4: Combine results and validate dimensions
    ds = xr.open_mfdataset(results, combine="by_coords") if results else None
    assert ds is not None and ds.dims.get("time", 0) > 0, "Combined dataset has no time steps"

    # Step 5: Reproject AOI if needed, spatial subset, validate bounds
    if aoi.crs != ds.rio.crs:
        aoi = aoi.to_crs(ds.rio.crs)
    ds_sub = ds.rio.clip(aoi.geometry)
    assert not ds_sub.isnull().all().values.any(), "Spatial subset is entirely NaN — check AOI alignment"

    # Step 6: Derive variables and validate units/ranges
    # (source-specific; see references/DOWNLOAD_PATTERNS.md)

    # Step 7: Save output and verify artifact
    out = Path(CONFIG["output_path"])
    if CONFIG["output_format"] == "zarr":
        ds_sub.to_zarr(out, mode="w")
        xr.open_zarr(out)   # verify reopens cleanly
    elif CONFIG["output_format"] == "netcdf":
        ds_sub.to_netcdf(out)
        xr.open_dataset(out).close()
    log.info(f"Saved to {out}")

    # Step 8: QC summary
    log.info(f"QC | time={ds_sub.dims.get('time')} | "
             f"bounds={ds_sub.rio.bounds()} | failed={len(failed)}")


def _download_item(item):
    """Source-specific download — replace with actual implementation."""
    raise NotImplementedError("Replace with source-specific download logic")


if __name__ == "__main__":
    main()
```

**Error recovery:** If Step 3 validation fails, check the error log for failed items, fix `CONFIG` (wrong date range, missing credentials, bad URL), and re-run `main()`. The `results` list is rebuilt fresh each run — no partial-state issues.

## Four Data Access Patterns

### 1. Direct HTTP Download (PRISM, Stage IV, DEM)

```python
import requests
from pathlib import Path

def download_file(url: str, dest_dir: str, retries=3) -> Path:
    dest = Path(dest_dir) / Path(url).name
    if dest.exists():
        return dest  # resume support
    session = requests.Session()
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    session.mount("https://", HTTPAdapter(max_retries=Retry(total=retries, backoff_factor=2)))
    r = session.get(url, timeout=60)
    r.raise_for_status()
    dest.write_bytes(r.content)
    return dest
```

### 2. REST API Query (USGS, Synoptic)

```python
import requests, os

def query_synoptic(station_ids: list[str], start: str, end: str) -> dict:
    token = os.environ["SYNOPTIC_API_TOKEN"]
    params = {
        "stid": ",".join(station_ids),
        "start": start.replace("-", "") + "0000",
        "end":   end.replace("-", "") + "2359",
        "token": token,
        "output": "json",
    }
    r = requests.get("https://api.synopticdata.com/v2/stations/timeseries",
                     params=params, timeout=60)
    r.raise_for_status()
    return r.json()
```

### 3. Cloud Object Storage / S3 (CONUS404, HRRR, WRF-CMIP6)

```python
import s3fs, xarray as xr

# CONUS404 — anonymous public bucket
fs = s3fs.S3FileSystem(anon=True, client_kwargs={"endpoint_url": "https://usgs.osn.mghpcc.org"})
store = s3fs.S3Map("s3://mdmf/gdp/CONUS404/hourly.zarr", s3=fs)
ds = xr.open_zarr(store, consolidated=True)

# WRF-CMIP6 — boto3 with unsigned config
import boto3
from botocore import UNSIGNED
from botocore.config import Config
s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
```

### 4. Specialized Libraries (Herbie/HRRR, pyPRISMClimate, obspy/IRIS)

```python
# HRRR via Herbie
from herbie import Herbie
H = Herbie("2024-01-15 12:00", model="hrrr", product="sfc", fxx=0)
ds = H.xarray("TMP:2 m")  # 2-metre temperature

# IRIS via obspy
from obspy.clients.fdsn import Client
client = Client("IRIS")
inv = client.get_stations(network="UW", station="*", channel="BHZ",
                          starttime="2024-01-01", endtime="2024-02-01")
```

See [`references/DOWNLOAD_PATTERNS.md`](references/DOWNLOAD_PATTERNS.md) for complete pipeline implementations of each pattern.

## Spatial Subsetting

| Grid Type | Method | Sources |
|-----------|--------|---------|
| Regular (lat/lon) | `ds.rio.clip(aoi.geometry)` | PRISM, Stage IV, DEM |
| Curvilinear (model) | `regionmask` | CONUS404, WRF-CMIP6 |
| Irregular (points) | `shapely.contains()` | USGS station data |

Always match CRS before subsetting: `aoi = aoi.to_crs(ds.rio.crs)`.

## Output Formats

| Format | Use When |
|--------|----------|
| **Zarr** (preferred) | Large gridded datasets, cloud workflows |
| **NetCDF** | Sharing with traditional tools, small datasets |
| **CSV** | Tabular station data (USGS) |

## Common Issues and Debugging

### wgrib2 Not Found (HRRR)
```python
import shutil
assert shutil.which("wgrib2"), "Install: conda install -c conda-forge wgrib2"
```

### S3 Auth Errors (CONUS404, WRF)
```python
# CONUS404
fs = s3fs.S3FileSystem(anon=True, client_kwargs={"endpoint_url": "https://usgs.osn.mghpcc.org"})
# WRF
s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
```

### CRS Mismatch
```python
aoi = aoi.to_crs(ds.rio.crs)
ds_clipped = ds.rio.clip(aoi.geometry)
# If ds has no CRS: ds.rio.write_crs("EPSG:4326", inplace=True)
```

### Network Timeouts
```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
session = requests.Session()
session.mount("https://", HTTPAdapter(max_retries=Retry(total=3, backoff_factor=2)))
```

### USGS RDB Parsing
```python
lines = [l for l in response.text.splitlines() if not l.startswith("#")]
df = pd.read_csv(io.StringIO("\n".join([lines[0]] + lines[2:])), sep="\t")
# Note: USGS returns local time — convert to UTC using station timezone metadata
```

### Memory Issues
```python
ds = xr.open_dataset(path, chunks={"time": 100})  # lazy
print(f"Dataset size: {ds.nbytes / 1e9:.1f} GB")   # check before .compute()
```

## Reference Files

- **`references/sources/`** — Per-source files (`hrrr.md`, `conus404.md`, etc.): endpoints, auth, response formats. Load only the relevant source.
- **`references/DOWNLOAD_PATTERNS.md`** — Complete pipeline code for HTTP, S3, REST API, and library patterns.
- **`references/CONFIGURATION.md`** — Per-source parameter tables with types, defaults, and validation rules.

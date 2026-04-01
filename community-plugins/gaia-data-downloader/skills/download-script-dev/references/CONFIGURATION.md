# Configuration Reference

Per-source parameter tables, validation rules, and size estimation formulas.

---

## Common Parameters (All Sources)

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `source` | str | Yes | — | Data source identifier |
| `date_range` | tuple(str, str) | Yes | — | Start and end dates (ISO 8601) |
| `output_path` | str | Yes | — | Path for output file |
| `output_format` | str | No | `"zarr"` | Output format: `zarr`, `netcdf`, `csv` |
| `aoi_path` | str | No | — | Path to AOI boundary (GeoJSON/Shapefile) |
| `max_workers` | int | No | `8` | Parallel download threads |

---

## CONUS404 Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `dataset_kind` | str | Yes | — | `"daily"` or `"hourly"` |
| `variables` | list[str] | Yes | — | Variable names (e.g., `["T2", "Q2", "RAINC"]`) |
| `aoi_path` | str | No | — | Boundary file for spatial subsetting |

**Available Variables:** T2, Q2, U10, V10, PSFC, RAINC, RAINNC, SNOW, SNOWH, SWDOWN, GLW, TSK, HFX, LH

**Validation Rules:**
- `dataset_kind` must be `"daily"` or `"hourly"`
- Variables must be valid CONUS404 variable names
- AOI must use Lambert Conformal Conic or will be reprojected

---

## HRRR Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `model` | str | No | `"hrrr"` | Model name |
| `product` | str | No | `"sfc"` | Product type: `sfc`, `prs`, `nat` |
| `frequency` | str | No | `"1d"` | Temporal frequency for date range |
| `forecast_hour` | int | No | `0` | Forecast hour (0 = analysis) |
| `parameters` | dict[str, str] | Yes | — | GRIB2 parameter:level → output name mapping |

**Common Parameter Mappings:**
```python
{
    "TMP:2 m": "temperature_2m",
    "UGRD:10 m": "u_wind_10m",
    "VGRD:10 m": "v_wind_10m",
    "APCP:surface": "precipitation",
    "DSWRF:surface": "shortwave_radiation",
    "RH:2 m": "relative_humidity_2m",
    "PRES:surface": "surface_pressure",
}
```

**Validation Rules:**
- `product` must be one of `sfc`, `prs`, `nat`
- `forecast_hour` must be 0-48
- `parameters` keys must be valid GRIB2 search strings
- `wgrib2` must be in PATH

---

## WRF-CMIP6 Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `bucket_name` | str | No | `"wrf-cmip6-noversioning"` | S3 bucket |
| `model` | str | Yes | — | GCM name (e.g., `"CESM2"`, `"MPI-ESM1-2-HR"`) |
| `data_tier` | str | Yes | — | Data tier (e.g., `"raw"`, `"regridded"`) |
| `domain` | str | Yes | — | WRF domain (e.g., `"d01"`, `"d02"`) |
| `scenario` | str | Yes | — | `"historical"`, `"ssp245"`, `"ssp585"` |
| `bias_correction` | str | No | `"none"` | Bias correction method |

**Validation Rules:**
- `scenario` must be valid CMIP6 scenario identifier
- Time strings use `YYYY-MM-DD_HH:MM:SS` format (underscore separator)

---

## PRISM Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `variables` | list[str] | Yes | — | PRISM variables |
| `dest_path` | str | Yes | — | Download destination directory |

**Available Variables:** `ppt`, `tmin`, `tmax`, `tmean`, `tdmean`, `vpdmin`, `vpdmax`

**Validation Rules:**
- Variables must be from the available list above
- Date range must be within PRISM coverage (1981-present for daily)

---

## Stage IV Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `analysis_type` | str | No | `"1day"` | `"1day"`, `"6hr"`, `"1hr"` |

**URL Pattern:**
```
https://water.noaa.gov/resources/downloads/precip/stageIV/{YYYY}/{MM}/{DD}/nws_precip_{analysis_type}_{YYYYMMDD}_conus.nc
```

**Validation Rules:**
- `analysis_type` must be `"1day"`, `"6hr"`, or `"1hr"`
- Date range should be within Stage IV availability (~2002-present)

---

## USGS Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `sites` | list[str] | Yes | — | USGS site numbers |
| `parameters` | dict[str, str] | Yes | — | Parameter code → name mapping |
| `batch_size` | int | No | `5` | Sites per API request |
| `request_delay` | float | No | `1.0` | Delay between batches (seconds) |

**Common Parameter Codes:**
| Code | Description |
|------|-------------|
| `00060` | Discharge (cubic feet per second) |
| `00065` | Gage height (feet) |
| `00010` | Water temperature (Celsius) |
| `00045` | Precipitation (inches) |
| `00400` | pH |

**Validation Rules:**
- Site numbers must be valid USGS site identifiers (typically 8-15 digits)
- Parameter codes must be valid USGS parameter codes
- `batch_size` should be <= 100 (API limit)

---

## ORNL DAYMET Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `variables` | list[str] | Yes | — | DAYMET variables |
| `region` | str | No | `"na"` | `"na"` (North America) |

**Available Variables:** `tmin`, `tmax`, `prcp`, `srad`, `vp`, `swe`, `dayl`

**Validation Rules:**
- Requires `~/.netrc` with NASA Earthdata credentials
- Variables must be from the available list

---

## DEM / SRTM Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `bounds` | tuple(float, float, float, float) | Yes | — | (west, south, east, north) in EPSG:4326 |
| `product` | str | No | `"SRTM1"` | `"SRTM1"` (30m) or `"SRTM3"` (90m) |

**Validation Rules:**
- Bounds must be in WGS84 (EPSG:4326)
- Latitude must be between -60 and 60 (SRTM coverage)

---

## Synoptic Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `state` | str | No | — | US state abbreviation |
| `network` | str | No | — | Network IDs (comma-separated) |
| `radius` | str | No | — | Search radius: `"lat,lon,miles"` |
| `bbox` | str | No | — | Bounding box: `"west,south,east,north"` |
| `output` | str | No | `"geojson"` | `"json"` or `"geojson"` |

**Validation Rules:**
- `SYNOPTIC_API_TOKEN` environment variable must be set
- At least one spatial filter (state, radius, bbox) should be provided

---

## IRIS Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `network` | str | Yes | — | Seismic network code (e.g., `"UW"`) |
| `station` | str | Yes | — | Station code (e.g., `"RCM"`) |
| `channel` | str | No | `"HHZ"` | Channel code |
| `location` | str | No | `"--"` | Location code |

**Validation Rules:**
- Network and station must be valid FDSN identifiers
- Channel codes follow SEED convention (3 characters)

---

## Size Estimation Formulas

Use these to estimate data volume before downloading:

| Source | Formula | Example |
|--------|---------|---------|
| CONUS404 | ~1 GB × n_variables × n_years (daily) | 3 vars × 2 years ≈ 6 GB |
| HRRR | ~80 MB × n_timesteps (full CONUS) | 31 days ≈ 2.5 GB (before clipping) |
| PRISM | ~50 MB × n_variables × n_years (daily) | 2 vars × 1 year ≈ 100 MB |
| Stage IV | ~5 MB × n_days | 365 days ≈ 1.8 GB |
| USGS | ~1 MB × n_sites × n_years | 10 sites × 3 years ≈ 30 MB |
| WRF-CMIP6 | Highly variable by domain and tier | Check S3 listing first |
| DEM | ~25 MB per 1° × 1° tile (SRTM1) | 2° × 1° region ≈ 50 MB |

**Estimation function:**
```python
def estimate_size_gb(source, n_variables=1, n_timesteps=365, n_sites=1):
    """Rough size estimate in GB."""
    rates = {
        "CONUS404": 1.0 * n_variables * (n_timesteps / 365),
        "HRRR": 0.08 * n_timesteps,
        "PRISM": 0.05 * n_variables * (n_timesteps / 365),
        "Stage IV": 0.005 * n_timesteps,
        "USGS": 0.001 * n_sites * (n_timesteps / 365),
    }
    return rates.get(source, None)
```

# GAIA Data Downloader Plugin

Generate and develop hydroclimatological data download scripts for the GAIA project.

## Overview

This Claude Code plugin encapsulates knowledge from the [gaia-data-downloaders](https://github.com/gaia-hazlab/gaia-data-downloaders) repository — 18 Jupyter notebooks implementing reproducible data download pipelines for 10+ environmental data sources. It provides:

- **Data Downloader Agent** — Generates complete download scripts from natural language prompts
- **Download Script Dev Skill** — Assists in developing and debugging download scripts

## Supported Data Sources

| Source | Type | Description |
|--------|------|-------------|
| CONUS404 | Weather reanalysis | 4 km daily/hourly historical weather (USGS) |
| HRRR | Weather model | 3 km hourly rapid refresh forecasts (NOAA) |
| WRF-CMIP6 | Climate projections | Dynamically downscaled CMIP6 scenarios |
| PRISM | Climate normals | 4 km daily/monthly climate data |
| Stage IV | Precipitation | Multi-sensor precipitation analysis |
| USGS | Streamflow | Real-time and historical stream gage data |
| ORNL DAYMET | Surface weather | 1 km daily weather for North America |
| DEM/SRTM | Elevation | 30-90 m global elevation data |
| Synoptic | Weather stations | Real-time weather station observations |
| IRIS | Seismic | Seismic waveform data (FDSN) |

## Installation

### Claude Code (via rse-plugins marketplace)

```bash
# Add the marketplace (if not already added)
/plugin marketplace add uw-ssec/rse-plugins

# The gaia-data-downloader plugin is now available
```

For local development:
```bash
claude --plugin-dir ./community-plugins/gaia-data-downloader
```

### GitHub Copilot CLI

```bash
# Add marketplace
copilot plugin marketplace add uw-ssec/rse-plugins

# Install plugin
copilot plugin install gaia-data-downloader@rse-plugins
```

Or install directly:
```bash
copilot plugin install uw-ssec/rse-plugins:community-plugins/gaia-data-downloader
```

## Usage

### Agent: Generate a Download Script

The agent uses a three-phase interaction to ensure scientists have full control over parameters:

**1. Describe what you need:**
```
Download HRRR temperature and wind data for the Skagit watershed, January 2024
```

**2. Review the proposed configuration:**
```
Source: HRRR
Model: hrrr
Product: sfc
Date Range: 2024-01-01 to 2024-01-31
Parameters:
  TMP:2 m → temperature_2m
  UGRD:10 m → u_wind_10m
  VGRD:10 m → v_wind_10m
AOI: ../data/GIS/SkagitBoundary.json
Output: ../data/weather_data/hrrr_skagit_202401.zarr
Max Workers: 8
Estimated size: ~2.5 GB

Would you like to adjust any parameters?
```

**3. Adjust and generate:**
```
Add precipitation. Change frequency to 6h. Reduce workers to 4.
```

The agent generates a Python script with all parameters in a CONFIG dict at the top.

### Skill: Develop a Script

Invoke the skill when developing or debugging download scripts:

```
/gaia-data-downloader:download-script-dev
```

The skill provides templates, configuration validation, and debugging guidance for all supported data sources.

## Prerequisites

- **Python 3.9+** with xarray, geopandas, rioxarray
- **Source-specific:** herbie-data (HRRR), pyPRISMClimate (PRISM), obspy (IRIS), boto3 (WRF/S3), s3fs (CONUS404)
- **System:** wgrib2 for HRRR (install via conda-forge)
- **Credentials:** NASA Earthdata `.netrc` for ORNL, `SYNOPTIC_API_TOKEN` env var for Synoptic

## License

BSD-3-Clause

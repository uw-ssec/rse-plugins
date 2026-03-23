# Data Sources Reference

Detailed documentation for each GAIA hydroclimatological data source.

---

## CONUS404

**Description:** High-resolution (4 km) historical weather dataset covering the contiguous US from 1979-present. Produced by USGS using WRF forced by ERA5.

**Access Pattern:** S3 Zarr store via `xarray` and `s3fs`

**Endpoint:**
- Daily: `s3://hytest/conus404/conus404_daily.zarr`
- Hourly: `s3://hytest/conus404/conus404_hourly.zarr`
- S3 endpoint URL: `https://usgs.osn.mghpcc.org`

**Authentication:** Anonymous (`anon=True` in s3fs)

**Key Libraries:** `xarray`, `s3fs`, `rioxarray`, `geopandas`

**Available Variables:** T2 (temperature), Q2 (humidity), U10/V10 (wind), PSFC (pressure), RAINC/RAINNC (precipitation), SNOW, SNOWH, and many more.

**Access Example:**
```python
import xarray as xr
import s3fs

fs = s3fs.S3FileSystem(anon=True, client_kwargs={"endpoint_url": "https://usgs.osn.mghpcc.org"})
ds = xr.open_zarr(fs.get_mapper("s3://hytest/conus404/conus404_daily.zarr"), consolidated=True)
```

**Notes:**
- Uses Lambert Conformal Conic projection — reproject AOI before clipping
- `DATASET_KIND` controls daily vs. hourly resolution
- Large dataset: ~1 GB per variable per year at daily resolution

---

## HRRR (High-Resolution Rapid Refresh)

**Description:** NOAA's ~3 km operational weather model covering CONUS with hourly forecasts. Ideal for high-resolution meteorological data.

**Access Pattern:** AWS S3 via the `herbie-data` library

**Endpoint:** Managed by Herbie (AWS S3 buckets: `noaa-hrrr-bdp-pds`, `noaa-hrrr-pds`)

**Authentication:** Anonymous

**Key Libraries:** `herbie-data`, `xarray`, `wgrib2` (system binary)

**Available Parameters:**
| GRIB2 Parameter | Description | Level |
|-----------------|-------------|-------|
| `TMP:2 m` | 2-meter temperature | surface |
| `UGRD:10 m` | 10-meter U-wind | surface |
| `VGRD:10 m` | 10-meter V-wind | surface |
| `APCP:surface` | Accumulated precipitation | surface |
| `DSWRF:surface` | Downward shortwave radiation | surface |
| `RH:2 m` | 2-meter relative humidity | surface |
| `PRES:surface` | Surface pressure | surface |

**Access Example:**
```python
from herbie import Herbie
import pandas as pd

date = pd.Timestamp("2024-01-15")
H = Herbie(date, model="hrrr", product="sfc", fxx=0)
ds = H.xarray(":TMP:2 m")
```

**Critical Dependency:** Requires `wgrib2` binary in PATH. Install via `conda install -c conda-forge wgrib2` or `pixi add wgrib2`. Not pip-installable.

**Notes:**
- `product`: `sfc` (surface), `prs` (pressure levels), `nat` (native levels)
- `fxx`: Forecast hour (0 = analysis, 1-48 = forecast hours)
- ~80 MB per timestep for full CONUS; much less after AOI clipping
- Uses Lambert Conformal Conic projection

---

## WRF-CMIP6

**Description:** Dynamically downscaled CMIP6 climate projections using WRF. Provides high-resolution regional climate scenarios.

**Access Pattern:** AWS S3 via `boto3` with unsigned requests

**Endpoint:** `s3://wrf-cmip6-noversioning/downscaled_products/gcm/`

**Authentication:** Anonymous (unsigned requests)

**Key Libraries:** `boto3`, `xarray`, `concurrent.futures`

**S3 Path Structure:**
```
s3://wrf-cmip6-noversioning/downscaled_products/gcm/
  {model}/{data_tier}/{domain}/{historical|ssp*}/{bias_correction}/
    {variable}_{frequency}_{model}_{scenario}_{variant}_{grid}_{start}-{end}.nc
```

**Access Example:**
```python
import boto3
from botocore import UNSIGNED
from botocore.config import Config

s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
s3.download_file("wrf-cmip6-noversioning", key, local_path)
```

**Notes:**
- Non-standard time format: `YYYY-MM-DD_HH:MM:SS` (underscore, not space)
- Parse with: `pd.to_datetime(time_str.replace("_", " "))`
- Use `ThreadPoolExecutor` for parallel file downloads (4-24 workers)
- Multiple GCMs, scenarios (historical, SSP2-4.5, SSP5-8.5), and domains available

---

## PRISM

**Description:** Parameter-elevation Relationships on Independent Slopes Model. High-resolution (~4 km) daily/monthly climate data for the US.

**Access Pattern:** HTTP download via `pyPRISMClimate`

**Authentication:** None

**Key Libraries:** `pyPRISMClimate`, `xarray`, `rioxarray`

**Available Variables:** `ppt` (precipitation), `tmin`, `tmax`, `tmean` (temperature), `tdmean` (dew point), `vpdmin`, `vpdmax` (vapor pressure deficit)

**Access Example:**
```python
from pyPRISMClimate import get_prism_dailys
import pandas as pd

dates = pd.date_range("2024-01-01", "2024-01-31")
get_prism_dailys(variables=["ppt", "tmax"], dates=dates, dest_path="./prism_data/")
```

**Notes:**
- ~50 MB per variable per year at daily resolution
- Regular lat/lon grid — use `rio.clip()` for spatial subsetting
- Monthly normals also available for 1991-2020

---

## Stage IV Precipitation

**Description:** NOAA multi-sensor precipitation analysis. Hourly and daily precipitation estimates for CONUS at ~4 km resolution.

**Access Pattern:** HTTP download via `requests`

**Endpoint:** `https://water.noaa.gov/resources/downloads/precip/stageIV/{YYYY}/{MM}/{DD}/nws_precip_1day_{YYYYMMDD}_conus.nc`

**Authentication:** None

**Key Libraries:** `requests`, `xarray`, `rioxarray`

**Access Example:**
```python
import requests
from datetime import datetime

date = datetime(2024, 1, 15)
url = f"https://water.noaa.gov/resources/downloads/precip/stageIV/{date:%Y}/{date:%m}/{date:%d}/nws_precip_1day_{date:%Y%m%d}_conus.nc"
response = requests.get(url)
with open(f"stageIV_{date:%Y%m%d}.nc", "wb") as f:
    f.write(response.content)
```

**Notes:**
- ~5 MB per daily file
- HRAP (Hydrologic Rainfall Analysis Project) grid — may need reprojection
- Regular grid — use `rio.clip()` for spatial subsetting

---

## USGS Streamflow

**Description:** Real-time and historical streamflow, stage, and water temperature data from USGS stream gages across the US.

**Access Pattern:** REST API returning RDB (tab-separated) format

**Endpoint:** `https://nwis.waterservices.usgs.gov/nwis/iv/`

**Authentication:** None

**Key Libraries:** `requests`, `pandas`

**API Parameters:**
| Parameter | Description | Example |
|-----------|-------------|---------|
| `sites` | Comma-separated site numbers | `12200500,12201500` |
| `startDT` | Start date (ISO 8601) | `2024-01-01` |
| `endDT` | End date (ISO 8601) | `2024-01-31` |
| `parameterCd` | Parameter codes | `00060` (discharge), `00065` (stage), `00010` (temperature) |
| `format` | Response format | `rdb` |

**Access Example:**
```python
import requests
import pandas as pd
import io

params = {
    "sites": "12200500",
    "startDT": "2024-01-01",
    "endDT": "2024-01-31",
    "parameterCd": "00060,00065",
    "format": "rdb",
}
response = requests.get("https://nwis.waterservices.usgs.gov/nwis/iv/", params=params)
# Skip comment lines and data type row
lines = [l for l in response.text.splitlines() if not l.startswith("#")]
df = pd.read_csv(io.StringIO("\n".join(lines)), sep="\t", skiprows=[1])
```

**Notes:**
- Returns data in **local time zones** — convert to UTC using station timezone metadata
- RDB format has comment headers (`#`) and a data-type row below the column headers
- Small data volumes (KB-MB per station)
- Rate limiting may apply for bulk requests — use delays between API calls

---

## ORNL DAYMET

**Description:** Daily surface weather data for North America at 1 km resolution from Oak Ridge National Laboratory.

**Access Pattern:** ORNL DAAC API

**Endpoint:** ORNL DAAC data access portal

**Authentication:** NASA Earthdata credentials via `~/.netrc`

**Key Libraries:** `requests`, `xarray`

**Setup Required:**
```
# ~/.netrc file must contain:
machine urs.earthdata.nasa.gov
  login YOUR_USERNAME
  password YOUR_PASSWORD
```

**Notes:**
- Register at https://urs.earthdata.nasa.gov/ for credentials
- Variables: tmin, tmax, prcp, srad, vp, swe, dayl
- 1 km resolution across North America

---

## DEM / SRTM

**Description:** Digital Elevation Model from the Shuttle Radar Topography Mission. ~30 m or ~90 m resolution global elevation data.

**Access Pattern:** HTTP download via `elevation` library

**Authentication:** None

**Key Libraries:** `elevation`, `rioxarray`, `rasterio`

**Access Example:**
```python
import elevation
import rioxarray

# Download DEM for a bounding box
elevation.clip(bounds=(-122.5, 48.0, -121.0, 49.0), output="dem.tif")
dem = rioxarray.open_rasterio("dem.tif")
```

**Notes:**
- Regular lat/lon grid — use `rio.clip()` for spatial subsetting
- Output is GeoTIFF format
- ~30 m (1 arc-second) resolution globally

---

## Synoptic

**Description:** Real-time and historical weather station data from the Synoptic Data network (MesoWest).

**Access Pattern:** REST API returning JSON/GeoJSON

**Endpoint:** `https://api.synopticdata.com/v2/stations/metadata`

**Authentication:** API token via `SYNOPTIC_API_TOKEN` environment variable

**Key Libraries:** `requests`

**Access Example:**
```python
import os
import requests

token = os.environ["SYNOPTIC_API_TOKEN"]
params = {
    "token": token,
    "state": "WA",
    "network": "1,2",  # NWS + RAWS
    "output": "geojson",
}
response = requests.get("https://api.synopticdata.com/v2/stations/metadata", params=params)
stations = response.json()
```

**Notes:**
- Requires free API token from https://synopticdata.com/
- Token must be set as `SYNOPTIC_API_TOKEN` environment variable
- Returns GeoJSON for station metadata, JSON for time series data

---

## IRIS Seismic

**Description:** Seismic waveform and station data from the International Federation of Digital Seismograph Networks (FDSN).

**Access Pattern:** FDSN web services via `obspy`

**Authentication:** None

**Key Libraries:** `obspy`

**Access Example:**
```python
from obspy.clients.fdsn import Client
from obspy import UTCDateTime

client = Client("IRIS")
st = client.get_waveforms(
    network="UW", station="RCM", location="--", channel="HHZ",
    starttime=UTCDateTime("2024-01-15"), endtime=UTCDateTime("2024-01-16"),
)
```

**Notes:**
- Seismic data, not hydroclimatological — included for cross-domain GAIA studies
- `obspy` handles all FDSN protocol details
- Station inventory available via `client.get_stations()`

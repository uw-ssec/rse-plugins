# Stage IV Precipitation

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

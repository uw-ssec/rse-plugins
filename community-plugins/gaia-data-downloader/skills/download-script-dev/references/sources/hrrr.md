# HRRR (High-Resolution Rapid Refresh)

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

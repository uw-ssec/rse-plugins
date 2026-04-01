# PRISM

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

# ORNL DAYMET

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

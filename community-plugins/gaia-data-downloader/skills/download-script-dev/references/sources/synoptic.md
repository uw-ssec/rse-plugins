# Synoptic

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

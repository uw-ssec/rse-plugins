# USGS Streamflow

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

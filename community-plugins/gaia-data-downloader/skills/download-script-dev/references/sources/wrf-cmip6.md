# WRF-CMIP6

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

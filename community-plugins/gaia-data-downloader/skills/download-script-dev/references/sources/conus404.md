# CONUS404

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

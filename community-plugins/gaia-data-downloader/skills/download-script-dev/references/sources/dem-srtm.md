# DEM / SRTM

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

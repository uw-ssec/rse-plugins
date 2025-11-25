---
name: geospatial-data-processing
description: GIS and raster processing with GDAL, Rasterio, and GeoPandas for scientific geospatial workflows
---

# Geospatial Data Processing

Master geospatial data processing with GDAL, Rasterio, and GeoPandas for scientific workflows. Learn how to work with raster and vector data, handle coordinate reference systems, perform spatial operations, and create cloud-optimized geospatial datasets.

**Key Tools:**
- **GDAL**: Foundational library for geospatial data I/O and processing
- **Rasterio**: Pythonic interface to GDAL for raster data
- **GeoPandas**: Spatial operations on vector data with pandas-like API
- **Shapely**: Geometric operations and spatial predicates
- **Fiona**: Vector data I/O

**Official Documentation:**
- GDAL: https://gdal.org/
- Rasterio: https://rasterio.readthedocs.io/
- GeoPandas: https://geopandas.org/

## Quick Reference Card

### Installation & Setup
```bash
# Using pixi (STRONGLY recommended for geospatial)
pixi add gdal rasterio geopandas shapely fiona pyproj

# Add visualization tools
pixi add matplotlib cartopy

# Development tools
pixi add --feature dev pytest ruff mypy

# Using pip (not recommended - GDAL installation is complex)
pip install rasterio geopandas
```

### Essential Rasterio Commands
```python
import rasterio

# Read raster
with rasterio.open('image.tif') as src:
    data = src.read(1)  # Read band 1
    profile = src.profile
    crs = src.crs
    bounds = src.bounds

# Write raster
with rasterio.open('output.tif', 'w', **profile) as dst:
    dst.write(data, 1)

# Reproject
from rasterio.warp import reproject, Resampling
reproject(source, destination, 
          src_crs='EPSG:4326',
          dst_crs='EPSG:3857',
          resampling=Resampling.bilinear)
```

### Essential GeoPandas Commands
```python
import geopandas as gpd

# Read vector data
gdf = gpd.read_file('data.geojson')

# Reproject
gdf = gdf.to_crs('EPSG:4326')

# Spatial operations
buffered = gdf.buffer(100)
clipped = gpd.clip(gdf, boundary)
joined = gpd.sjoin(gdf1, gdf2, predicate='intersects')

# Write vector data
gdf.to_file('output.geojson', driver='GeoJSON')
```

### Quick Decision Tree

```
Need to process raster data (satellite imagery, DEMs)?
├─ YES → Use Rasterio
└─ NO → Working with vector data (points, lines, polygons)?
    ├─ YES → Use GeoPandas
    └─ NO → Need both raster and vector?
        └─ YES → Use both, see raster-vector operations

Need to handle coordinate systems?
├─ Check CRS with .crs
├─ Reproject with .to_crs() (GeoPandas) or rasterio.warp (Rasterio)
└─ Always verify CRS before spatial operations

Working with large datasets?
├─ Use Cloud-Optimized GeoTIFF (COG) for rasters
├─ Use spatial indexing for vectors
└─ Consider chunked processing
```

## When to Use This Skill

- **Processing satellite imagery** (Landsat, Sentinel, MODIS) for Earth observation and remote sensing
- **Analyzing vector geospatial data** (shapefiles, GeoJSON, GeoPackage) for GIS workflows
- **Working with raster data** (DEMs, climate grids, land cover maps) for spatial analysis
- **Coordinate reference system transformations** and reprojections between different CRS
- **Spatial operations** (clipping, masking, buffering, spatial joins) on geographic data
- **Creating cloud-optimized GeoTIFFs** for efficient cloud-based data access
- **Building geospatial data pipelines** for research and operational workflows
- **Integrating geospatial data** with scientific Python stack (NumPy, Pandas)

## Core Concepts

### 1. Raster vs Vector Data

**Raster Data:**
- Grid of pixels/cells with values
- Examples: Satellite imagery, DEMs, climate grids
- Formats: GeoTIFF, NetCDF, HDF5
- Tools: GDAL, Rasterio

**Vector Data:**
- Geometric features (points, lines, polygons)
- Examples: City boundaries, roads, sampling locations
- Formats: Shapefile, GeoJSON, GeoPackage
- Tools: GeoPandas, Shapely, Fiona

### 2. Coordinate Reference Systems (CRS)

A CRS defines how coordinates map to locations on Earth.

**Common CRS:**
- **EPSG:4326** (WGS84) - Latitude/longitude, used by GPS
- **EPSG:3857** (Web Mercator) - Used by web maps (Google, OSM)
- **UTM zones** - Metric coordinates for specific regions

**Why CRS matters:**
- Spatial operations require matching CRS
- Distance/area calculations depend on CRS
- Visualization requires appropriate projection

### 3. GDAL and Rasterio

**GDAL** is the foundational C++ library for geospatial data. **Rasterio** provides a Pythonic interface to GDAL.

**Key advantages of Rasterio:**
- Context manager support (`with` statements)
- NumPy integration
- Clean, readable API
- Proper resource management

### 4. GeoPandas and Shapely

**GeoPandas** extends Pandas with spatial operations. **Shapely** provides geometric operations.

**Key features:**
- Familiar pandas-like API
- Spatial predicates (intersects, contains, within)
- Geometric operations (buffer, union, difference)
- Easy CRS transformations

### 5. Cloud-Optimized GeoTIFF (COG)

COG is a GeoTIFF with internal tiling and overviews, enabling efficient cloud-based access.

**Benefits:**
- Read only needed portions (HTTP range requests)
- Multiple resolution levels (overviews)
- Efficient for cloud storage (S3, Azure Blob)
- Standard GeoTIFF format (compatible with all tools)

## Patterns

### Pattern 1: Reading and Writing Raster Data

**Scenario**: Load a GeoTIFF, process it, and save the result

**Solution**:

```python
import rasterio
import numpy as np

# Read raster data
with rasterio.open('input.tif') as src:
    # Read first band
    data = src.read(1)
    
    # Get metadata
    profile = src.profile
    transform = src.transform
    crs = src.crs
    
    print(f"Shape: {data.shape}")
    print(f"CRS: {crs}")
    print(f"Bounds: {src.bounds}")

# Process data (example: normalize)
data_normalized = (data - data.min()) / (data.max() - data.min())

# Write result
with rasterio.open('output.tif', 'w', **profile) as dst:
    dst.write(data_normalized, 1)
```

**Best Practices:**
- Always use context managers (`with` statements)
- Preserve metadata with `profile`
- Check data type and nodata values
- Handle edge cases (empty arrays, NaN values)

### Pattern 2: Working with Vector Data

**Scenario**: Load vector data, perform spatial operations, and save results

**Solution**:

```python
import geopandas as gpd

# Read vector data
gdf = gpd.read_file('cities.geojson')

# Check CRS
print(f"CRS: {gdf.crs}")

# Reproject if needed
if gdf.crs != 'EPSG:4326':
    gdf = gdf.to_crs('EPSG:4326')

# Spatial operations
gdf['area_km2'] = gdf.geometry.area / 1e6  # Convert to km²
gdf_buffered = gdf.copy()
gdf_buffered['geometry'] = gdf.geometry.buffer(0.1)  # 0.1 degree buffer

# Filter by attribute
large_cities = gdf[gdf['population'] > 1000000]

# Save result
large_cities.to_file('large_cities.geojson', driver='GeoJSON')
```

**Best Practices:**
- Always check and verify CRS
- Use `.copy()` when modifying geometry
- Choose appropriate file formats (GeoJSON for web, GeoPackage for complex data)

### Pattern 3: Coordinate Reference System Transformations

**Scenario**: Reproject data between different coordinate systems

**Solution**:

```python
import geopandas as gpd
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

# Vector reprojection (GeoPandas)
gdf = gpd.read_file('data.geojson')
gdf_utm = gdf.to_crs('EPSG:32633')  # UTM Zone 33N

# Raster reprojection (Rasterio)
with rasterio.open('input.tif') as src:
    # Calculate transform for new CRS
    dst_crs = 'EPSG:3857'
    transform, width, height = calculate_default_transform(
        src.crs, dst_crs, src.width, src.height, *src.bounds
    )
    
    # Update profile
    profile = src.profile.copy()
    profile.update({
        'crs': dst_crs,
        'transform': transform,
        'width': width,
        'height': height
    })
    
    # Reproject
    with rasterio.open('output_reprojected.tif', 'w', **profile) as dst:
        for i in range(1, src.count + 1):
            reproject(
                source=rasterio.band(src, i),
                destination=rasterio.band(dst, i),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=dst_crs,
                resampling=Resampling.bilinear
            )
```

**Best Practices:**
- Use appropriate resampling method (bilinear for continuous, nearest for categorical)
- Verify output bounds and resolution
- Test with known coordinates

### Pattern 4: Creating Cloud-Optimized GeoTIFF (COG)

**Scenario**: Convert a regular GeoTIFF to Cloud-Optimized GeoTIFF

**Solution**:

```python
import rasterio
from rasterio.shutil import copy

# Read source raster
with rasterio.open('input.tif') as src:
    profile = src.profile.copy()
    
    # Update profile for COG
    profile.update({
        'driver': 'COG',
        'compress': 'deflate',
        'tiled': True,
        'blockxsize': 512,
        'blockysize': 512
    })
    
    # Write as COG
    with rasterio.open('output_cog.tif', 'w', **profile) as dst:
        dst.write(src.read())
        
        # Add overviews
        dst.build_overviews([2, 4, 8, 16], Resampling.average)
```

**Best Practices:**
- Use appropriate compression (deflate, lzw, or jpeg)
- Add overviews for multi-resolution access
- Use 512x512 or 256x256 tile sizes
- Validate COG with `rio cogeo validate`

### Pattern 5: Spatial Joins

**Scenario**: Join two vector datasets based on spatial relationship

**Solution**:

```python
import geopandas as gpd

# Load datasets
points = gpd.read_file('sampling_points.geojson')
polygons = gpd.read_file('regions.geojson')

# Ensure matching CRS
if points.crs != polygons.crs:
    points = points.to_crs(polygons.crs)

# Spatial join - find which region each point is in
points_with_region = gpd.sjoin(points, polygons, how='left', predicate='within')

# Spatial join - find all points within each polygon
polygons_with_points = gpd.sjoin(polygons, points, how='left', predicate='contains')

# Count points per polygon
point_counts = polygons_with_points.groupby(polygons_with_points.index).size()
polygons['point_count'] = point_counts

print(f"Points with region info: {len(points_with_region)}")
print(f"Polygons with point counts: {len(polygons)}")
```

**Best Practices:**
- Always verify CRS match before spatial joins
- Choose appropriate predicate (within, contains, intersects, etc.)
- Handle cases where no match is found (use `how='left'`)

### Pattern 6: Clipping Rasters with Vector Boundaries

**Scenario**: Extract raster data within a specific boundary

**Solution**:

```python
import rasterio
import rasterio.mask
import geopandas as gpd

# Load boundary
boundary = gpd.read_file('study_area.geojson')

# Clip raster
with rasterio.open('large_raster.tif') as src:
    # Ensure CRS match
    if boundary.crs != src.crs:
        boundary = boundary.to_crs(src.crs)
    
    # Clip
    clipped_data, clipped_transform = rasterio.mask.mask(
        src, 
        boundary.geometry, 
        crop=True,
        filled=True
    )
    
    # Update metadata
    profile = src.profile.copy()
    profile.update({
        'height': clipped_data.shape[1],
        'width': clipped_data.shape[2],
        'transform': clipped_transform
    })
    
    # Save clipped raster
    with rasterio.open('clipped_raster.tif', 'w', **profile) as dst:
        dst.write(clipped_data)
```

**Best Practices:**
- Verify CRS match between raster and vector
- Use `crop=True` to reduce output size
- Handle nodata values appropriately

### Pattern 7: Zonal Statistics

**Scenario**: Calculate statistics for raster values within vector zones

**Solution**:

```python
from rasterstats import zonal_stats
import geopandas as gpd

# Load zones
zones = gpd.read_file('zones.geojson')

# Calculate zonal statistics
stats = zonal_stats(
    zones, 
    'raster.tif',
    stats=['mean', 'max', 'min', 'std', 'count'],
    geojson_out=True
)

# Convert to GeoDataFrame
zones_with_stats = gpd.GeoDataFrame.from_features(stats)

# Display results
print(zones_with_stats[['name', 'mean', 'max', 'min']])

# Save results
zones_with_stats.to_file('zones_with_stats.geojson', driver='GeoJSON')
```

**Best Practices:**
- Ensure CRS match between zones and raster
- Choose appropriate statistics for your analysis
- Handle nodata values in raster
- Consider memory usage for large datasets

### Pattern 8: Rasterizing Vector Data

**Scenario**: Convert vector features to raster format

**Solution**:

```python
import rasterio
from rasterio import features
import geopandas as gpd
import numpy as np

# Load vector data
gdf = gpd.read_file('polygons.geojson')

# Define raster properties
width, height = 1000, 1000
transform = rasterio.transform.from_bounds(*gdf.total_bounds, width, height)

# Rasterize
shapes = ((geom, value) for geom, value in zip(gdf.geometry, gdf['value']))
rasterized = features.rasterize(
    shapes,
    out_shape=(height, width),
    transform=transform,
    fill=0,
    dtype='float32'
)

# Save raster
profile = {
    'driver': 'GTiff',
    'height': height,
    'width': width,
    'count': 1,
    'dtype': 'float32',
    'crs': gdf.crs,
    'transform': transform
}

with rasterio.open('rasterized.tif', 'w', **profile) as dst:
    dst.write(rasterized, 1)
```

**Best Practices:**
- Choose appropriate resolution for your use case
- Use meaningful fill values for background
- Consider memory usage for high-resolution outputs

### Pattern 9: Vectorizing Raster Data

**Scenario**: Convert raster pixels to vector polygons

**Solution**:

```python
import rasterio
from rasterio import features
import geopandas as gpd
from shapely.geometry import shape

# Read raster
with rasterio.open('classified.tif') as src:
    image = src.read(1)
    
    # Vectorize
    results = (
        {'properties': {'value': v}, 'geometry': s}
        for i, (s, v) in enumerate(
            features.shapes(image, transform=src.transform)
        )
    )
    
    # Convert to GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(list(results))
    gdf.crs = src.crs

# Filter out background (value 0)
gdf = gdf[gdf['value'] != 0]

# Simplify geometries
gdf['geometry'] = gdf.geometry.simplify(tolerance=0.001)

# Save
gdf.to_file('vectorized.geojson', driver='GeoJSON')
```

**Best Practices:**
- Filter out background/nodata values
- Simplify geometries to reduce file size
- Consider using `mask` parameter to exclude certain values

### Pattern 10: Working with Multi-band Rasters

**Scenario**: Process multi-band satellite imagery (e.g., calculate NDVI)

**Solution**:

```python
import rasterio
import numpy as np

# Read multi-band raster
with rasterio.open('landsat.tif') as src:
    # Read specific bands
    red = src.read(4).astype('float32')    # Band 4
    nir = src.read(5).astype('float32')    # Band 5
    
    # Calculate NDVI
    ndvi = (nir - red) / (nir + red)
    
    # Handle division by zero
    ndvi = np.where((nir + red) == 0, 0, ndvi)
    
    # Update profile for single band output
    profile = src.profile.copy()
    profile.update({
        'count': 1,
        'dtype': 'float32'
    })
    
    # Save NDVI
    with rasterio.open('ndvi.tif', 'w', **profile) as dst:
        dst.write(ndvi, 1)
```

**Best Practices:**
- Convert to float for calculations
- Handle division by zero and invalid values
- Document which bands correspond to which wavelengths
- Consider using rioxarray for complex multi-band operations

### Pattern 11: Spatial Indexing for Performance

**Scenario**: Speed up spatial queries on large vector datasets

**Solution**:

```python
import geopandas as gpd

# Load large dataset
gdf = gpd.read_file('large_dataset.geojson')

# Create spatial index (automatic in GeoPandas)
# The spatial index is created automatically when needed

# Query using spatial index
point = gpd.GeoSeries([Point(-122.4, 37.8)], crs='EPSG:4326')

# Find features that intersect with point (uses spatial index)
nearby = gdf[gdf.intersects(point.iloc[0])]

# For repeated queries, use sindex directly
possible_matches_index = list(gdf.sindex.intersection(point.iloc[0].bounds))
possible_matches = gdf.iloc[possible_matches_index]
precise_matches = possible_matches[possible_matches.intersects(point.iloc[0])]

print(f"Found {len(precise_matches)} matches")
```

**Best Practices:**
- Spatial index is created automatically by GeoPandas
- Use `.sindex` for repeated queries
- Combine bounding box filter with precise geometric test
- Consider saving as GeoPackage to persist spatial index

### Pattern 12: Handling Large Rasters with Windowed Reading

**Scenario**: Process large rasters that don't fit in memory

**Solution**:

```python
import rasterio
from rasterio.windows import Window
import numpy as np

# Process large raster in chunks
with rasterio.open('large_raster.tif') as src:
    # Get profile for output
    profile = src.profile.copy()
    
    # Create output file
    with rasterio.open('processed_raster.tif', 'w', **profile) as dst:
        # Define window size
        window_size = 1024
        
        # Iterate over windows
        for i in range(0, src.height, window_size):
            for j in range(0, src.width, window_size):
                # Define window
                window = Window(j, i, 
                              min(window_size, src.width - j),
                              min(window_size, src.height - i))
                
                # Read window
                data = src.read(1, window=window)
                
                # Process data
                processed = data * 2  # Example processing
                
                # Write window
                dst.write(processed, 1, window=window)
                
                print(f"Processed window at ({i}, {j})")
```

**Best Practices:**
- Choose window size based on available memory
- Handle edge windows that may be smaller
- Process and write windows sequentially to minimize memory usage
- Consider using Dask for parallel processing of windows

## Best Practices Checklist

### Data Handling
- [ ] Always check CRS before spatial operations
- [ ] Use context managers (`with` statements) for file I/O
- [ ] Verify data types and nodata values
- [ ] Handle edge cases (empty geometries, NaN values)
- [ ] Preserve metadata when processing rasters

### Performance
- [ ] Use spatial indexing for large vector datasets
- [ ] Use windowed reading for large rasters
- [ ] Create overviews for multi-resolution access
- [ ] Use Cloud-Optimized GeoTIFF (COG) for cloud storage
- [ ] Consider chunked processing for memory efficiency

### Coordinate Systems
- [ ] Always verify CRS matches before operations
- [ ] Use appropriate CRS for analysis (metric for distances)
- [ ] Document CRS in metadata and file names
- [ ] Test reprojections with known coordinates

### File Formats
- [ ] Use GeoTIFF for rasters (COG for cloud)
- [ ] Use GeoPackage for complex vector data
- [ ] Use GeoJSON for web applications
- [ ] Avoid Shapefiles for new projects (use GeoPackage)

### Code Quality
- [ ] Add type hints for function signatures
- [ ] Write tests for spatial operations
- [ ] Document assumptions about CRS and units
- [ ] Handle invalid geometries gracefully

## Common Issues and Solutions

### Issue: GDAL Installation Fails

**Problem**: `pip install gdal` fails with compilation errors

**Solution**:
```bash
# Use pixi/conda instead of pip for GDAL
pixi add gdal rasterio

# If you must use pip, install system GDAL first:
# Ubuntu/Debian:
sudo apt-get install gdal-bin libgdal-dev

# macOS:
brew install gdal

# Then install Python bindings matching GDAL version
pip install gdal==$(gdal-config --version)
```

### Issue: CRS Mismatch Errors

**Problem**: Spatial operations fail with CRS mismatch

**Solution**:
```python
# Always check CRS before operations
print(f"GDF1 CRS: {gdf1.crs}")
print(f"GDF2 CRS: {gdf2.crs}")

# Reproject to match
if gdf1.crs != gdf2.crs:
    gdf2 = gdf2.to_crs(gdf1.crs)

# Now perform operation
result = gpd.overlay(gdf1, gdf2, how='intersection')
```

### Issue: Memory Error with Large Rasters

**Problem**: Loading large raster causes memory error

**Solution**:
```python
# Use windowed reading (see Pattern 12)
import rasterio
from rasterio.windows import Window

with rasterio.open('large_raster.tif') as src:
    # Process in chunks
    for i in range(0, src.height, 1024):
        for j in range(0, src.width, 1024):
            window = Window(j, i, 1024, 1024)
            data = src.read(1, window=window)
            # Process chunk
```

### Issue: Invalid Geometries

**Problem**: Spatial operations fail due to invalid geometries

**Solution**:
```python
import geopandas as gpd

# Check for invalid geometries
gdf = gpd.read_file('data.geojson')
invalid = ~gdf.is_valid

print(f"Found {invalid.sum()} invalid geometries")

# Fix invalid geometries
gdf.loc[invalid, 'geometry'] = gdf.loc[invalid, 'geometry'].buffer(0)

# Verify fix
print(f"Remaining invalid: {(~gdf.is_valid).sum()}")
```

### Issue: Nodata Values Not Handled

**Problem**: Calculations include nodata values, producing incorrect results

**Solution**:
```python
import rasterio
import numpy as np

with rasterio.open('raster.tif') as src:
    data = src.read(1)
    nodata = src.nodata
    
    # Mask nodata values
    masked_data = np.ma.masked_equal(data, nodata)
    
    # Perform calculations on masked array
    mean = masked_data.mean()
    
    print(f"Mean (excluding nodata): {mean}")
```

## Resources

### Official Documentation
- **GDAL**: https://gdal.org/
- **Rasterio**: https://rasterio.readthedocs.io/
- **GeoPandas**: https://geopandas.org/
- **Shapely**: https://shapely.readthedocs.io/
- **Fiona**: https://fiona.readthedocs.io/
- **PyProj**: https://pyproj4.github.io/pyproj/

### Tutorials and Guides
- **Rasterio Documentation**: https://rasterio.readthedocs.io/en/latest/
- **GeoPandas User Guide**: https://geopandas.org/en/stable/docs/user_guide.html
- **GDAL Tutorials**: https://gdal.org/tutorials/
- **Automating GIS Processes**: https://autogis-site.readthedocs.io/

### Data Sources
- **Landsat**: https://earthexplorer.usgs.gov/
- **Sentinel**: https://scihub.copernicus.eu/
- **Natural Earth**: https://www.naturalearthdata.com/
- **OpenStreetMap**: https://www.openstreetmap.org/

### Complementary Skills
- **xarray-for-multidimensional-data**: Working with multi-dimensional raster arrays
- **holoviz-visualizations**: Interactive geospatial visualization and dashboards
- **python-testing**: Testing geospatial functions and workflows
- **pixi-package-manager**: Managing complex geospatial dependencies
- **code-quality-tools**: Linting and type checking geospatial code

### Community and Support
- **GIS Stack Exchange**: https://gis.stackexchange.com/
- **Rasterio GitHub**: https://github.com/rasterio/rasterio
- **GeoPandas GitHub**: https://github.com/geopandas/geopandas

## Integration with Scientific Python

### Working with NumPy Arrays

Rasterio integrates seamlessly with NumPy for array operations:

```python
import rasterio
import numpy as np

with rasterio.open('dem.tif') as src:
    elevation = src.read(1)
    
    # NumPy operations
    slope = np.gradient(elevation)
    mean_elevation = np.mean(elevation)
    std_elevation = np.std(elevation)
    
    # Masking
    high_elevation = np.where(elevation > 1000, elevation, np.nan)
    
    # Statistical analysis
    percentiles = np.percentile(elevation, [25, 50, 75])
    
    print(f"Mean elevation: {mean_elevation:.2f}m")
    print(f"Std deviation: {std_elevation:.2f}m")
    print(f"Percentiles (25, 50, 75): {percentiles}")
```

### Integration with Pandas

GeoPandas extends Pandas, so all Pandas operations work:

```python
import geopandas as gpd
import pandas as pd

# Read geospatial data
gdf = gpd.read_file('cities.geojson')

# Pandas operations
gdf['population_millions'] = gdf['population'] / 1e6
gdf_sorted = gdf.sort_values('population', ascending=False)
top_10 = gdf.nlargest(10, 'population')

# Groupby operations
by_country = gdf.groupby('country').agg({
    'population': 'sum',
    'geometry': 'count'
})

# Merge with non-spatial data
economic_data = pd.read_csv('economic_data.csv')
gdf_merged = gdf.merge(economic_data, on='city_id')
```

### Visualization with Matplotlib

```python
import matplotlib.pyplot as plt
import rasterio
from rasterio.plot import show
import geopandas as gpd

# Plot raster
fig, ax = plt.subplots(figsize=(10, 10))
with rasterio.open('satellite.tif') as src:
    show(src, ax=ax, cmap='terrain')
    ax.set_title('Satellite Imagery')

# Plot vector
gdf = gpd.read_file('boundaries.geojson')
gdf.plot(ax=ax, facecolor='none', edgecolor='red', linewidth=2)

plt.savefig('map.png', dpi=300, bbox_inches='tight')
```

### Using Cartopy for Map Projections

```python
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import geopandas as gpd

# Create map with projection
fig, ax = plt.subplots(
    figsize=(12, 8),
    subplot_kw={'projection': ccrs.PlateCarree()}
)

# Add features
ax.coastlines()
ax.gridlines(draw_labels=True)

# Plot geospatial data
gdf = gpd.read_file('data.geojson')
gdf.plot(ax=ax, transform=ccrs.PlateCarree(), 
         column='value', cmap='viridis', legend=True)

ax.set_title('Geospatial Data with Cartopy')
plt.savefig('cartopy_map.png', dpi=300, bbox_inches='tight')
```

## Advanced Patterns

### Pattern 13: Mosaicking Multiple Rasters

**Scenario**: Combine multiple raster tiles into a single mosaic

**Solution**:

```python
import rasterio
from rasterio.merge import merge
from pathlib import Path

# List of raster files to mosaic
raster_files = list(Path('tiles/').glob('*.tif'))
src_files_to_mosaic = []

# Open all files
for fp in raster_files:
    src = rasterio.open(fp)
    src_files_to_mosaic.append(src)

# Merge
mosaic, out_trans = merge(src_files_to_mosaic)

# Update metadata
out_meta = src_files_to_mosaic[0].meta.copy()
out_meta.update({
    "driver": "GTiff",
    "height": mosaic.shape[1],
    "width": mosaic.shape[2],
    "transform": out_trans,
    "compress": "lzw"
})

# Write mosaic
with rasterio.open('mosaic.tif', 'w', **out_meta) as dest:
    dest.write(mosaic)

# Close all files
for src in src_files_to_mosaic:
    src.close()

print(f"Mosaicked {len(raster_files)} tiles")
```

**Best Practices:**
- Ensure all tiles have the same CRS
- Handle overlapping areas appropriately
- Consider memory usage for large mosaics
- Use compression to reduce output size

### Pattern 14: Calculating Terrain Attributes

**Scenario**: Derive slope, aspect, and hillshade from a DEM

**Solution**:

```python
import rasterio
import numpy as np
from rasterio.transform import Affine

def calculate_slope(dem, transform):
    """Calculate slope in degrees from DEM."""
    # Get cell size
    cell_size_x = transform.a
    cell_size_y = -transform.e
    
    # Calculate gradients
    dzdx = np.gradient(dem, cell_size_x, axis=1)
    dzdy = np.gradient(dem, cell_size_y, axis=0)
    
    # Calculate slope
    slope = np.arctan(np.sqrt(dzdx**2 + dzdy**2))
    slope_degrees = np.degrees(slope)
    
    return slope_degrees

def calculate_aspect(dem, transform):
    """Calculate aspect in degrees from DEM."""
    cell_size_x = transform.a
    cell_size_y = -transform.e
    
    dzdx = np.gradient(dem, cell_size_x, axis=1)
    dzdy = np.gradient(dem, cell_size_y, axis=0)
    
    aspect = np.arctan2(dzdy, -dzdx)
    aspect_degrees = np.degrees(aspect)
    
    # Convert to compass direction (0-360)
    aspect_degrees = np.where(aspect_degrees < 0, 
                              90 - aspect_degrees, 
                              90 - aspect_degrees)
    aspect_degrees = np.where(aspect_degrees < 0,
                              aspect_degrees + 360,
                              aspect_degrees)
    
    return aspect_degrees

# Read DEM
with rasterio.open('dem.tif') as src:
    dem = src.read(1).astype('float32')
    profile = src.profile.copy()
    transform = src.transform
    
    # Calculate terrain attributes
    slope = calculate_slope(dem, transform)
    aspect = calculate_aspect(dem, transform)
    
    # Save slope
    with rasterio.open('slope.tif', 'w', **profile) as dst:
        dst.write(slope, 1)
    
    # Save aspect
    with rasterio.open('aspect.tif', 'w', **profile) as dst:
        dst.write(aspect, 1)

print("Terrain attributes calculated")
```

**Best Practices:**
- Handle edge effects in gradient calculations
- Use appropriate cell size for gradient calculation
- Consider smoothing DEM before calculating derivatives
- Validate results with known terrain features

### Pattern 15: Buffering and Proximity Analysis

**Scenario**: Create buffers around features and analyze proximity

**Solution**:

```python
import geopandas as gpd
from shapely.geometry import Point

# Load features
roads = gpd.read_file('roads.geojson')
buildings = gpd.read_file('buildings.geojson')

# Ensure projected CRS for accurate distance calculations
if roads.crs.is_geographic:
    roads = roads.to_crs('EPSG:32633')  # UTM Zone 33N
    buildings = buildings.to_crs('EPSG:32633')

# Create buffer around roads (100 meters)
road_buffer = roads.copy()
road_buffer['geometry'] = roads.geometry.buffer(100)

# Find buildings within buffer
buildings_near_roads = gpd.sjoin(
    buildings, 
    road_buffer, 
    how='inner', 
    predicate='within'
)

print(f"Buildings within 100m of roads: {len(buildings_near_roads)}")

# Calculate distance to nearest road for each building
buildings['distance_to_road'] = buildings.geometry.apply(
    lambda x: roads.distance(x).min()
)

# Classify by distance
buildings['proximity_class'] = pd.cut(
    buildings['distance_to_road'],
    bins=[0, 50, 100, 200, float('inf')],
    labels=['Very Close', 'Close', 'Moderate', 'Far']
)

# Save results
buildings.to_file('buildings_with_proximity.geojson', driver='GeoJSON')
```

**Best Practices:**
- Use projected CRS for distance calculations
- Consider computational cost for large datasets
- Use spatial indexing for performance
- Validate buffer distances with known features

## Testing Geospatial Code

### Testing Raster Operations

```python
import pytest
import rasterio
import numpy as np
from pathlib import Path

def test_raster_processing():
    """Test raster processing function."""
    # Create test raster
    test_data = np.random.rand(100, 100).astype('float32')
    profile = {
        'driver': 'GTiff',
        'height': 100,
        'width': 100,
        'count': 1,
        'dtype': 'float32',
        'crs': 'EPSG:4326',
        'transform': rasterio.transform.from_bounds(0, 0, 1, 1, 100, 100)
    }
    
    # Write test file
    with rasterio.open('test.tif', 'w', **profile) as dst:
        dst.write(test_data, 1)
    
    # Test processing
    with rasterio.open('test.tif') as src:
        data = src.read(1)
        assert data.shape == (100, 100)
        assert data.dtype == np.float32
        assert src.crs == 'EPSG:4326'
    
    # Cleanup
    Path('test.tif').unlink()

def test_crs_transformation():
    """Test CRS transformation."""
    import geopandas as gpd
    from shapely.geometry import Point
    
    # Create test data
    gdf = gpd.GeoDataFrame(
        {'name': ['point1']},
        geometry=[Point(0, 0)],
        crs='EPSG:4326'
    )
    
    # Transform
    gdf_utm = gdf.to_crs('EPSG:32633')
    
    # Verify
    assert gdf_utm.crs == 'EPSG:32633'
    assert len(gdf_utm) == 1
```

### Testing Spatial Operations

```python
import pytest
import geopandas as gpd
from shapely.geometry import Point, Polygon

def test_spatial_join():
    """Test spatial join operation."""
    # Create test data
    points = gpd.GeoDataFrame(
        {'id': [1, 2, 3]},
        geometry=[Point(0, 0), Point(1, 1), Point(5, 5)],
        crs='EPSG:4326'
    )
    
    polygons = gpd.GeoDataFrame(
        {'name': ['poly1']},
        geometry=[Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])],
        crs='EPSG:4326'
    )
    
    # Spatial join
    result = gpd.sjoin(points, polygons, predicate='within')
    
    # Verify
    assert len(result) == 2  # Two points within polygon
    assert all(result['name'] == 'poly1')

def test_buffer_operation():
    """Test buffer operation."""
    gdf = gpd.GeoDataFrame(
        {'id': [1]},
        geometry=[Point(0, 0)],
        crs='EPSG:32633'  # Projected CRS
    )
    
    # Buffer
    buffered = gdf.copy()
    buffered['geometry'] = gdf.geometry.buffer(100)
    
    # Verify
    assert buffered.geometry.iloc[0].area > 0
    assert buffered.geometry.iloc[0].geom_type == 'Polygon'
```

## Summary

Geospatial data processing with GDAL, Rasterio, and GeoPandas provides powerful tools for working with raster and vector data in scientific workflows. By mastering coordinate reference systems, spatial operations, and cloud-optimized formats, you can build efficient and reproducible geospatial data pipelines.

**Key takeaways:**

Master the fundamentals of raster (Rasterio) and vector (GeoPandas) data processing. Always verify and handle coordinate reference systems correctly. Use Cloud-Optimized GeoTIFF for efficient cloud-based data access. Apply spatial indexing and windowed reading for large datasets. Integrate geospatial tools with the scientific Python stack. Follow best practices for reproducibility and performance.

**Next steps:**

Start with basic raster and vector operations to understand the APIs. Practice CRS transformations with real-world data. Implement spatial operations for your research workflows. Create cloud-optimized datasets for efficient access. Build reproducible geospatial data pipelines. Write tests to validate spatial operations and ensure correctness.

Geospatial data processing is essential for Earth observation, environmental science, and spatial analysis. With these tools and patterns, you can handle complex geospatial workflows efficiently and reproducibly.

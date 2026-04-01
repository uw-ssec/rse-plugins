---
description: Create interactive maps and geographic visualizations with GeoViews, GeoPandas, and tile providers
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Geospatial Visualization

Create geographic and mapping visualizations with GeoViews.

## Arguments

$ARGUMENTS — describe the map (e.g., "choropleth of population by state", "plot weather stations on a map", "heatmap of earthquake locations")

## Workflow

1. **Understand the geographic data:**
   - Data type: points, lines, polygons, rasters
   - Coordinate reference system (CRS/EPSG)
   - Data format (GeoJSON, Shapefile, GeoParquet, CSV with lat/lon)

2. **Prepare the data:**
   - Create or validate GeoDataFrame
   - Check and transform CRS if needed
   - Handle missing values and invalid geometries

3. **Build the map:**
   - Select base tile provider (OpenStreetMap, CartoDB, Stamen)
   - Create GeoViews elements (Points, Polygons, Path)
   - Encode data with color, size, hover tooltips
   - Compose layers with `*` operator

4. **Add interactivity:**
   - Hover tools for feature inspection
   - Selection and filtering
   - Dynamic updates with Panel widgets

5. **Report** the code and rendering instructions.

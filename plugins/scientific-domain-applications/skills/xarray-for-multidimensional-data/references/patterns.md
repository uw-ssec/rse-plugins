# Xarray Patterns

## Pattern 1: Creating DataArrays and Datasets

**From NumPy arrays:**
```python
import xarray as xr
import numpy as np
import pandas as pd

# Create sample data
data = np.random.randn(365, 10, 20)  # time, lat, lon

# Create DataArray with coordinates
temperature = xr.DataArray(
    data=data,
    dims=["time", "lat", "lon"],
    coords={
        "time": pd.date_range("2024-01-01", periods=365),
        "lat": np.linspace(-90, 90, 10),
        "lon": np.linspace(-180, 180, 20)
    },
    attrs={
        "units": "Celsius",
        "long_name": "Air Temperature"
    }
)

# Create Dataset with multiple variables
ds = xr.Dataset({
    "temperature": temperature,
    "precipitation": (["time", "lat", "lon"], 
                     np.random.rand(365, 10, 20) * 100)
})
```

**From Pandas DataFrame:**
```python
import pandas as pd

# Tabular data
df = pd.DataFrame({
    "time": pd.date_range("2024-01-01", periods=100),
    "station": ["A"] * 50 + ["B"] * 50,
    "temperature": np.random.randn(100),
    "humidity": np.random.rand(100) * 100
})

# Convert to Xarray
ds = df.set_index(["time", "station"]).to_xarray()
```

## Pattern 2: Reading and Writing Data

**NetCDF files:**
```python
# Write to NetCDF
ds.to_netcdf("climate_data.nc")

# Read from NetCDF
ds = xr.open_dataset("climate_data.nc")

# Read multiple files as single dataset
ds = xr.open_mfdataset("data_*.nc", combine="by_coords")

# Lazy loading (doesn't load data into memory)
ds = xr.open_dataset("large_file.nc", chunks={"time": 100})
```

**Zarr format (cloud-optimized):**
```python
# Write to Zarr
ds.to_zarr("climate_data.zarr")

# Read from Zarr
ds = xr.open_zarr("climate_data.zarr")

# Write to cloud storage (S3, GCS)
ds.to_zarr("s3://bucket/climate_data.zarr")
```

**Other formats:**
```python
# From CSV (via Pandas)
df = pd.read_csv("data.csv")
ds = df.to_xarray()

# To CSV (flatten first)
ds.to_dataframe().to_csv("output.csv")
```

## Pattern 3: Selection and Indexing

**Label-based selection:**
```python
# Select single time point
ds.sel(time="2024-01-15")

# Select multiple coordinates
ds.sel(time="2024-01-15", lat=40.7, lon=-74.0)

# Nearest neighbor (useful for inexact matches)
ds.sel(lat=40.5, lon=-74.2, method="nearest")

# Range selection
ds.sel(time=slice("2024-01-01", "2024-01-31"))
ds.sel(lat=slice(30, 50))

# Select multiple discrete values
ds.sel(time=["2024-01-01", "2024-01-15", "2024-01-31"])
```

**Position-based selection:**
```python
# Select by integer index
ds.isel(time=0)
ds.isel(lat=slice(0, 5), lon=slice(0, 10))

# Select every nth element
ds.isel(time=slice(None, None, 7))  # Every 7th time point
```

**Conditional selection:**
```python
# Keep only values meeting condition
warm_days = ds.where(ds["temperature"] > 20, drop=True)

# Replace values not meeting condition
ds_filled = ds.where(ds["temperature"] > 0, 0)

# Boolean mask
mask = (ds["temperature"] > 15) & (ds["temperature"] < 25)
comfortable_temps = ds.where(mask)
```

## Pattern 4: Computation and Aggregation

**Basic operations:**
```python
# Arithmetic operations
ds["temp_kelvin"] = ds["temperature"] + 273.15
ds["temp_fahrenheit"] = ds["temperature"] * 9/5 + 32

# Statistical operations
mean_temp = ds["temperature"].mean()
std_temp = ds["temperature"].std()
max_temp = ds["temperature"].max()

# Aggregation along dimensions
daily_mean = ds.mean(dim="time")
spatial_mean = ds.mean(dim=["lat", "lon"])
```

**GroupBy operations:**
```python
# Group by time components
monthly_mean = ds.groupby("time.month").mean()
seasonal_mean = ds.groupby("time.season").mean()
hourly_mean = ds.groupby("time.hour").mean()

# Custom grouping
ds["region"] = (["lat", "lon"], region_mask)
regional_mean = ds.groupby("region").mean()
```

**Rolling window operations:**
```python
# 7-day rolling mean
rolling_mean = ds.rolling(time=7, center=True).mean()

# 30-day rolling sum
rolling_sum = ds.rolling(time=30).sum()
```

**Resampling (time series):**
```python
# Resample to monthly
monthly = ds.resample(time="1M").mean()

# Resample to weekly
weekly = ds.resample(time="1W").sum()

# Upsample and interpolate
daily = ds.resample(time="1D").interpolate("linear")
```

## Pattern 5: Combining Datasets

**Concatenation:**
```python
# Concatenate along existing dimension
combined = xr.concat([ds1, ds2, ds3], dim="time")

# Concatenate along new dimension
ensemble = xr.concat([run1, run2, run3], 
                     dim=pd.Index([1, 2, 3], name="run"))
```

**Merging:**
```python
# Merge datasets with different variables
merged = xr.merge([temp_ds, precip_ds, pressure_ds])

# Merge with alignment
merged = xr.merge([ds1, ds2], join="inner")  # or "outer", "left", "right"
```

**Alignment:**
```python
# Automatic alignment in operations
result = ds1 + ds2  # Automatically aligns coordinates

# Manual alignment
ds1_aligned, ds2_aligned = xr.align(ds1, ds2, join="inner")
```

## Pattern 6: Dask Integration for Large Data

**Chunked operations:**
```python
import dask

# Open with chunks (lazy loading)
ds = xr.open_dataset("large_file.nc", chunks={"time": 100, "lat": 50})

# Operations remain lazy
result = ds["temperature"].mean(dim="time")

# Trigger computation
computed_result = result.compute()

# Parallel computation
with dask.config.set(scheduler="threads", num_workers=4):
    result = ds.mean(dim="time").compute()
```

**Chunking strategies:**
```python
# Chunk by time (good for time series operations)
ds = ds.chunk({"time": 365})

# Chunk by space (good for spatial operations)
ds = ds.chunk({"lat": 50, "lon": 50})

# Auto-chunking
ds = ds.chunk("auto")

# Rechunk for different operations
ds_rechunked = ds.chunk({"time": -1, "lat": 10, "lon": 10})
```

## Pattern 7: Interpolation and Regridding

**Interpolation:**
```python
# Interpolate to new coordinates
new_lats = np.linspace(-90, 90, 180)
new_lons = np.linspace(-180, 180, 360)

ds_interp = ds.interp(lat=new_lats, lon=new_lons, method="linear")

# Interpolate missing values
ds_filled = ds.interpolate_na(dim="time", method="linear")
```

**Reindexing:**
```python
# Reindex to new coordinates
new_time = pd.date_range("2024-01-01", "2024-12-31", freq="1D")
ds_reindexed = ds.reindex(time=new_time, method="nearest")

# Fill missing values during reindex
ds_reindexed = ds.reindex(time=new_time, fill_value=0)
```

## Pattern 8: Custom Functions with apply_ufunc

**Apply NumPy functions:**
```python
# Apply custom function element-wise
def custom_transform(x):
    return np.log(x + 1)

result = xr.apply_ufunc(
    custom_transform,
    ds["temperature"],
    dask="parallelized",
    output_dtypes=[float]
)
```

**Vectorized operations:**
```python
from scipy import stats

def detrend(data, axis):
    return stats.detrend(data, axis=axis)

# Apply along specific dimension
detrended = xr.apply_ufunc(
    detrend,
    ds["temperature"],
    input_core_dims=[["time"]],
    output_core_dims=[["time"]],
    kwargs={"axis": -1},
    dask="parallelized",
    output_dtypes=[float]
)
```

## Pattern 9: Working with DataTree

**Create hierarchical data structures:**
```python
import xarray as xr
import numpy as np

# Method 1: From dictionary of datasets
dt = xr.DataTree.from_dict({
    "/": xr.Dataset({"project": "Climate Study 2024"}),
    "/observations": xr.Dataset({
        "temp": (["time"], np.random.randn(100)),
        "humidity": (["time"], np.random.rand(100) * 100)
    }),
    "/observations/station_a": xr.Dataset({
        "location": "New York",
        "elevation": 10
    }),
    "/observations/station_b": xr.Dataset({
        "location": "Los Angeles",
        "elevation": 71
    }),
    "/model_outputs": xr.Dataset({
        "predicted_temp": (["time"], np.random.randn(100))
    }),
    "/model_outputs/ensemble_1": xr.Dataset({"model_id": "CESM"}),
    "/model_outputs/ensemble_2": xr.Dataset({"model_id": "GFDL"})
})

# Method 2: Build incrementally
root = xr.DataTree(name="root")
observations = xr.DataTree(name="observations", parent=root)
station_a = xr.DataTree(
    name="station_a",
    parent=observations,
    data=xr.Dataset({"temp": (["time"], [15, 16, 17])})
)
```

**Navigate the tree:**
```python
# Access nodes using paths
node = dt["/observations/station_a"]
node = dt["observations"]["station_a"]  # Equivalent

# Navigate relationships
node.parent  # Get parent node
node.children  # Dict of child nodes
node.root  # Get root node
node.path  # Get path from root ("/observations/station_a")

# Iterate over tree
for node in dt.subtree:
    print(node.path, node.ds)

# Get all leaf nodes
for leaf in dt.leaves:
    print(leaf.path)

# Find common ancestor
dt["/observations/station_a"].find_common_ancestor(
    dt["/observations/station_b"]
)  # Returns "/observations"
```

**Filter and match nodes:**
```python
# Pattern matching (glob-style)
stations = dt.match("*/station_*")  # All station nodes
observations = dt.match("/observations/*")  # Direct children of observations

# Filter by content
nodes_with_temp = dt.filter(lambda node: "temp" in node.ds.data_vars)

# Filter by depth
shallow_nodes = dt.filter(lambda node: node.depth <= 2)
```

**Apply operations across tree:**
```python
# Apply method to all datasets
mean_tree = dt.mean(dim="time")

# Map custom function to all datasets
def add_metadata(ds):
    ds.attrs["processed"] = True
    return ds

dt_processed = dt.map_over_datasets(add_metadata)

# Apply function with access to node information
def label_by_path(ds, node):
    ds.attrs["path"] = node.path
    return ds

dt_labeled = dt.map_over_datasets(label_by_path)
```

**Coordinate inheritance:**
```python
# Define coordinates at parent level
root_ds = xr.Dataset({
    "time": pd.date_range("2024-01-01", periods=100)
})
dt = xr.DataTree(data=root_ds)

# Child nodes inherit parent coordinates
child = xr.DataTree(
    parent=dt,
    data=xr.Dataset({"temp": (["time"], np.random.randn(100))})
)
# child can use "time" coordinate without redefining it

# Important: Child dimensions must align with inherited coordinates
# This will raise an error if lengths don't match:
# bad_child = xr.DataTree(
#     parent=dt,
#     data=xr.Dataset({"temp": (["time"], np.random.randn(50))})  # Wrong length!
# )
```

**Combine DataTrees:**
```python
# Arithmetic operations on isomorphic trees
dt1 = xr.DataTree.from_dict({
    "/a": xr.Dataset({"x": 1}),
    "/b": xr.Dataset({"x": 2})
})
dt2 = xr.DataTree.from_dict({
    "/a": xr.Dataset({"x": 10}),
    "/b": xr.Dataset({"x": 20})
})

# Element-wise operations
dt_sum = dt1 + dt2  # {"/a": {"x": 11}, "/b": {"x": 22}}
dt_diff = dt2 - dt1

# Check if trees have same structure
dt1.isomorphic(dt2)  # True if same node names and hierarchy

# Iterate over multiple trees together
for node1, node2 in xr.group_subtrees(dt1, dt2):
    print(f"Comparing {node1.path}: {node1.ds} vs {node2.ds}")
```

**Save and load DataTree:**
```python
# Save to Zarr (recommended for hierarchical data)
dt.to_zarr("climate_tree.zarr")

# Load from Zarr
dt_loaded = xr.open_datatree("climate_tree.zarr", engine="zarr")

# Save to NetCDF (flattened structure)
dt.to_netcdf("climate_tree.nc")
```

## Pattern 10: Geospatial Operations with rioxarray

**Open and inspect geospatial rasters:**
```python
import rioxarray
import xarray as xr

# Open GeoTIFF with CRS awareness
ds = rioxarray.open_rasterio("satellite_image.tif")

# Check CRS (Coordinate Reference System)
print(ds.rio.crs)  # EPSG:32610

# Check spatial extent
print(ds.rio.bounds())  # (minx, miny, maxx, maxy)

# Check resolution
print(ds.rio.resolution())  # (x_resolution, y_resolution)

# Access spatial attributes
print(ds.rio.width)
print(ds.rio.height)
print(ds.rio.transform())  # Affine transform
```

**Reproject to different CRS:**
```python
# Reproject to WGS84 (lat/lon)
ds_wgs84 = ds.rio.reproject("EPSG:4326")

# Reproject with specific resolution
ds_resampled = ds.rio.reproject(
    "EPSG:4326",
    resolution=0.001  # degrees
)

# Reproject with custom parameters
ds_custom = ds.rio.reproject(
    "EPSG:3857",  # Web Mercator
    resampling=rasterio.enums.Resampling.bilinear,
    nodata=-9999
)
```

**Clip and subset:**
```python
# Clip to bounding box (in CRS units)
ds_clipped = ds.rio.clip_box(
    minx=-120.5,
    miny=35.0,
    maxx=-119.5,
    maxy=36.0,
    crs="EPSG:4326"  # Specify if different from data CRS
)

# Clip to geometry (GeoDataFrame)
import geopandas as gpd

# Load shapefile or GeoJSON
gdf = gpd.read_file("study_area.geojson")

# Clip to geometry bounds
ds_masked = ds.rio.clip(gdf.geometry, gdf.crs, drop=True)

# Clip with mask (keep values inside, NaN outside)
ds_masked = ds.rio.clip(gdf.geometry, gdf.crs, drop=False)
```

**Set and update CRS:**
```python
# Set CRS if missing
ds = ds.rio.write_crs("EPSG:4326")

# Update CRS without reprojection (if CRS was wrong)
ds = ds.rio.write_crs("EPSG:32610", inplace=True)

# Set nodata value
ds = ds.rio.write_nodata(-9999)

# Update coordinate names to standard
ds = ds.rio.set_spatial_dims(x_dim="lon", y_dim="lat")
```

**Raster calculations:**
```python
# NDVI calculation with geospatial metadata
red = rioxarray.open_rasterio("red_band.tif")
nir = rioxarray.open_rasterio("nir_band.tif")

ndvi = (nir - red) / (nir + red)
ndvi = ndvi.rio.write_crs(red.rio.crs)  # Preserve CRS

# Zonal statistics
zones = rioxarray.open_rasterio("zones.tif")
stats = ndvi.groupby(zones).mean()
```

**Save with geospatial metadata:**
```python
# Save to GeoTIFF
ds.rio.to_raster("output.tif", compress="lzw")

# Save with specific options
ds.rio.to_raster(
    "output.tif",
    driver="GTiff",
    dtype="float32",
    compress="deflate",
    nodata=-9999,
    tiled=True,
    blockxsize=512,
    blockysize=512
)

# Save to Cloud Optimized GeoTIFF (COG)
ds.rio.to_raster("output_cog.tif", driver="COG")
```

**Integration with other geospatial tools:**
```python
# Convert to/from GeoPandas (for vector operations)
import geopandas as gpd
from geocube.api.core import make_geocube

# Vector to raster
gdf = gpd.read_file("points.geojson")
cube = make_geocube(
    vector_data=gdf,
    measurements=["temperature"],
    resolution=(-0.01, 0.01)
)

# Regrid with xESMF
import xesmf as xe

# Create regridder
regridder = xe.Regridder(
    ds_source,
    ds_target,
    method="bilinear",
    periodic=False
)

# Apply regridding
ds_regridded = regridder(ds_source)
```

**Multi-temporal geospatial analysis:**
```python
# Open time series of rasters
files = ["image_2020.tif", "image_2021.tif", "image_2022.tif"]
das = [rioxarray.open_rasterio(f, masked=True) for f in files]

# Combine with time dimension
ds = xr.concat(das, dim="time")
ds["time"] = pd.date_range("2020-01-01", periods=3, freq="1Y")
ds = ds.rio.write_crs(das[0].rio.crs)

# Calculate change over time
change = ds.isel(time=-1) - ds.isel(time=0)
change = change.rio.write_crs(ds.rio.crs)

# Trend analysis
from scipy import stats
def calculate_trend(x):
    if np.isnan(x).all():
        return np.nan
    slope, _, _, _, _ = stats.linregress(range(len(x)), x)
    return slope

trend = ds.reduce(calculate_trend, dim="time")
trend = trend.rio.write_crs(ds.rio.crs)
```


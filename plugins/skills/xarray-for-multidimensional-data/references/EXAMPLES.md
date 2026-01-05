# Real-World Examples

## Example 1: Climate Data Analysis

**Load and analyze global temperature data:**
```python
import xarray as xr
import matplotlib.pyplot as plt

# Load climate data
ds = xr.open_dataset("global_temperature.nc", chunks={"time": 365})

# Calculate annual mean temperature
annual_mean = ds["temperature"].resample(time="1Y").mean()

# Calculate global mean (area-weighted)
weights = np.cos(np.deg2rad(ds.lat))
weights.name = "weights"
global_mean = (ds["temperature"] * weights).sum(dim=["lat", "lon"]) / weights.sum()

# Plot time series
global_mean.plot()
plt.title("Global Mean Temperature")
plt.ylabel("Temperature (°C)")
plt.show()

# Calculate temperature anomaly
climatology = ds["temperature"].groupby("time.month").mean(dim="time")
anomaly = ds["temperature"].groupby("time.month") - climatology

# Save results
anomaly.to_netcdf("temperature_anomaly.nc")
```

## Example 2: Satellite Data Processing

**Process multi-temporal satellite imagery:**
```python
# Load satellite data
ds = xr.open_mfdataset("satellite_*.nc", combine="by_coords")

# Calculate NDVI (Normalized Difference Vegetation Index)
ndvi = (ds["nir"] - ds["red"]) / (ds["nir"] + ds["red"])
ds["ndvi"] = ndvi

# Calculate temporal statistics
ndvi_mean = ds["ndvi"].mean(dim="time")
ndvi_std = ds["ndvi"].std(dim="time")
ndvi_trend = ds["ndvi"].polyfit(dim="time", deg=1)

# Identify areas with significant vegetation change
change_mask = np.abs(ndvi_trend.polyfit_coefficients.sel(degree=1)) > 0.01

# Export results
result = xr.Dataset({
    "ndvi_mean": ndvi_mean,
    "ndvi_std": ndvi_std,
    "change_mask": change_mask
})
result.to_netcdf("ndvi_analysis.nc")
```

## Example 3: Oceanographic Data Analysis

**Analyze ocean temperature and salinity profiles:**
```python
# Load ocean data with depth dimension
ds = xr.open_dataset("ocean_profiles.nc")

# Calculate mixed layer depth (where temp drops by 0.5°C from surface)
surface_temp = ds["temperature"].isel(depth=0)
temp_diff = surface_temp - ds["temperature"]
mld = ds["depth"].where(temp_diff > 0.5).min(dim="depth")

# Calculate heat content
heat_capacity = 4186  # J/(kg·K)
density = 1025  # kg/m³
heat_content = (ds["temperature"] * heat_capacity * density).integrate("depth")

# Seasonal analysis
seasonal_temp = ds["temperature"].groupby("time.season").mean()

# Plot vertical profile
ds["temperature"].sel(lat=0, lon=180, method="nearest").plot(y="depth")
plt.gca().invert_yaxis()  # Depth increases downward
plt.title("Temperature Profile at Equator")
```

## Example 4: Multi-Model Ensemble Analysis

**Compare and analyze multiple climate model outputs:**
```python
import xarray as xr
import glob

# Load multiple model outputs
model_files = glob.glob("models/model_*.nc")
models = [xr.open_dataset(f, chunks={"time": 365}) for f in model_files]

# Add model dimension
for i, ds in enumerate(models):
    ds["model"] = i

# Concatenate into single dataset
ensemble = xr.concat(models, dim="model")

# Calculate ensemble mean and spread
ensemble_mean = ensemble.mean(dim="model")
ensemble_std = ensemble.std(dim="model")

# Calculate model agreement (fraction of models agreeing on sign of change)
future_change = ensemble.sel(time=slice("2080", "2100")).mean(dim="time")
historical = ensemble.sel(time=slice("1980", "2000")).mean(dim="time")
change = future_change - historical

# Agreement: fraction of models with same sign as ensemble mean
agreement = (np.sign(change) == np.sign(change.mean(dim="model"))).sum(dim="model") / len(models)

# Identify robust changes (high agreement and large magnitude)
robust_change = change.mean(dim="model").where(
    (agreement > 0.8) & (np.abs(change.mean(dim="model")) > ensemble_std.mean(dim="model"))
)

# Save results
result = xr.Dataset({
    "ensemble_mean": ensemble_mean,
    "ensemble_std": ensemble_std,
    "agreement": agreement,
    "robust_change": robust_change
})
result.to_netcdf("ensemble_analysis.nc")
```

## Example 5: Time Series Decomposition

**Decompose time series into trend, seasonal, and residual components:**
```python
import xarray as xr
from scipy import signal

# Load time series data
ds = xr.open_dataset("timeseries.nc")

# Calculate long-term trend (annual rolling mean)
trend = ds["temperature"].rolling(time=365, center=True).mean()

# Remove trend to get anomaly
anomaly = ds["temperature"] - trend

# Calculate seasonal cycle (monthly climatology)
seasonal = anomaly.groupby("time.month").mean(dim="time")

# Remove seasonal cycle to get residual
residual = anomaly.groupby("time.month") - seasonal

# Combine into single dataset
decomposition = xr.Dataset({
    "original": ds["temperature"],
    "trend": trend,
    "seasonal": seasonal.rename({"month": "time"}),
    "residual": residual
})

# Calculate variance explained by each component
total_var = ds["temperature"].var()
trend_var = trend.var()
seasonal_var = seasonal.var()
residual_var = residual.var()

print(f"Trend explains {100*trend_var/total_var:.1f}% of variance")
print(f"Seasonal explains {100*seasonal_var/total_var:.1f}% of variance")
print(f"Residual explains {100*residual_var/total_var:.1f}% of variance")

# Plot decomposition
import matplotlib.pyplot as plt

fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
decomposition["original"].plot(ax=axes[0])
axes[0].set_title("Original")
decomposition["trend"].plot(ax=axes[1])
axes[1].set_title("Trend")
decomposition["seasonal"].plot(ax=axes[2])
axes[2].set_title("Seasonal")
decomposition["residual"].plot(ax=axes[3])
axes[3].set_title("Residual")
plt.tight_layout()
```

## Example 6: Hierarchical Climate Model Data with DataTree

**Organize multi-model ensemble data with varying resolutions:**
```python
import xarray as xr
import numpy as np
import pandas as pd

# Simulate multi-model climate ensemble with hierarchical structure
# Each model has different resolutions and multiple variables

# Create time coordinate (shared across all models)
time = pd.date_range("2020-01-01", "2050-12-31", freq="1M")

# Model 1: High resolution (2° x 2°)
lat_high = np.linspace(-90, 90, 90)
lon_high = np.linspace(-180, 180, 180)
temp_high = 15 + 10 * np.random.randn(len(time), len(lat_high), len(lon_high))
precip_high = np.abs(50 + 20 * np.random.randn(len(time), len(lat_high), len(lon_high)))

model1_ds = xr.Dataset({
    "temperature": (["time", "lat", "lon"], temp_high),
    "precipitation": (["time", "lat", "lon"], precip_high)
}, coords={
    "time": time,
    "lat": lat_high,
    "lon": lon_high
})

# Model 2: Medium resolution (4° x 4°)
lat_med = np.linspace(-90, 90, 45)
lon_med = np.linspace(-180, 180, 90)
temp_med = 15 + 10 * np.random.randn(len(time), len(lat_med), len(lon_med))
precip_med = np.abs(50 + 20 * np.random.randn(len(time), len(lat_med), len(lon_med)))

model2_ds = xr.Dataset({
    "temperature": (["time", "lat", "lon"], temp_med),
    "precipitation": (["time", "lat", "lon"], precip_med)
}, coords={
    "time": time,
    "lat": lat_med,
    "lon": lon_med
})

# Model 3: Low resolution (8° x 8°)
lat_low = np.linspace(-90, 90, 23)
lon_low = np.linspace(-180, 180, 45)
temp_low = 15 + 10 * np.random.randn(len(time), len(lat_low), len(lon_low))
precip_low = np.abs(50 + 20 * np.random.randn(len(time), len(lat_low), len(lon_low)))

model3_ds = xr.Dataset({
    "temperature": (["time", "lat", "lon"], temp_low),
    "precipitation": (["time", "lat", "lon"], precip_low)
}, coords={
    "time": time,
    "lat": lat_low,
    "lon": lon_low
})

# Create hierarchical DataTree structure
ensemble_tree = xr.DataTree.from_dict({
    "/": xr.Dataset(attrs={
        "project": "CMIP6",
        "experiment": "SSP2-4.5",
        "institution": "Climate Research Center"
    }),
    "/models/CESM": model1_ds.assign_attrs({"resolution": "2deg", "institution": "NCAR"}),
    "/models/GFDL": model2_ds.assign_attrs({"resolution": "4deg", "institution": "NOAA"}),
    "/models/HadGEM": model3_ds.assign_attrs({"resolution": "8deg", "institution": "Met Office"}),
    "/observations": xr.Dataset({
        "description": "Observational data for validation"
    })
})

# Analyze the ensemble
print("Ensemble structure:")
for node in ensemble_tree.subtree:
    if node.ds is not None and len(node.ds.data_vars) > 0:
        print(f"{node.path}: {list(node.ds.data_vars)}, shape: {node.ds.dims}")

# Calculate ensemble statistics across models
# Note: Models have different resolutions, so we work with each separately
model_nodes = list(ensemble_tree["models"].children.values())

# Calculate temporal mean for each model
temporal_means = {}
for model_name, node in ensemble_tree["models"].children.items():
    temporal_means[model_name] = node.ds["temperature"].mean(dim="time")
    print(f"{model_name} mean temperature: {temporal_means[model_name].mean().values:.2f}°C")

# Apply same operation to all models using map_over_datasets
def calculate_climatology(ds):
    """Calculate monthly climatology"""
    if "temperature" in ds.data_vars:
        climatology = ds.groupby("time.month").mean(dim="time")
        return climatology
    return ds

climatology_tree = ensemble_tree["models"].map_over_datasets(calculate_climatology)

# Compare model agreement on warming trend
def calculate_trend(ds):
    """Calculate linear trend in temperature"""
    if "temperature" in ds.data_vars and "time" in ds.dims:
        # Global mean temperature
        weights = np.cos(np.deg2rad(ds.lat))
        global_mean = (ds["temperature"] * weights).sum(dim=["lat", "lon"]) / weights.sum()

        # Calculate trend (°C per year)
        years = (ds.time - ds.time[0]) / np.timedelta64(365, 'D')
        trend = global_mean.polyfit(dim="time", deg=1).polyfit_coefficients.sel(degree=1)

        return xr.Dataset({"warming_trend": trend})
    return ds

trend_tree = ensemble_tree["models"].map_over_datasets(calculate_trend)

print("\nWarming trends (°C/year):")
for model_name, node in trend_tree.children.items():
    if "warming_trend" in node.ds:
        print(f"{model_name}: {node.ds['warming_trend'].values:.4f}")

# Save hierarchical structure to Zarr
ensemble_tree.to_zarr("climate_ensemble.zarr", mode="w")
print("\nSaved ensemble to climate_ensemble.zarr")

# Load and verify
loaded_tree = xr.open_datatree("climate_ensemble.zarr", engine="zarr")
print(f"Loaded tree with {len(list(loaded_tree.subtree))} nodes")

# Filter models by resolution
high_res_models = ensemble_tree["models"].filter(
    lambda node: node.ds.attrs.get("resolution") == "2deg"
)
print(f"\nHigh resolution models: {[n.name for n in high_res_models]}")
```

## Example 7: Geospatial Satellite Data Processing with rioxarray

**Process Landsat imagery with proper CRS handling and geospatial operations:**
```python
import xarray as xr
import rioxarray
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Simulate Landsat-like multispectral imagery
# In practice, you would load real GeoTIFF files

def create_synthetic_landsat_scene(filename, crs="EPSG:32610", nodata=-9999):
    """Create synthetic Landsat scene for demonstration"""
    # UTM Zone 10N coordinates (Northern California)
    x = np.linspace(500000, 600000, 1000)  # 100km extent
    y = np.linspace(4200000, 4300000, 1000)  # 100km extent

    # Create synthetic bands
    np.random.seed(42)
    blue = np.random.randint(8000, 12000, (len(y), len(x)))
    green = np.random.randint(9000, 14000, (len(y), len(x)))
    red = np.random.randint(8000, 13000, (len(y), len(x)))
    nir = np.random.randint(15000, 25000, (len(y), len(x)))

    # Add some vegetation patterns (higher NIR, lower red)
    vegetation_mask = (np.random.rand(len(y), len(x)) > 0.6)
    nir[vegetation_mask] = np.random.randint(20000, 30000, vegetation_mask.sum())
    red[vegetation_mask] = np.random.randint(6000, 10000, vegetation_mask.sum())

    # Create DataArray with spatial reference
    bands_data = np.stack([blue, green, red, nir], axis=0)

    da = xr.DataArray(
        bands_data,
        dims=["band", "y", "x"],
        coords={
            "band": [1, 2, 3, 4],  # Blue, Green, Red, NIR
            "y": y,
            "x": x
        },
        attrs={
            "long_name": "Landsat Surface Reflectance",
            "scale_factor": 0.0001
        }
    )

    # Add CRS and spatial reference
    da = da.rio.write_crs(crs)
    da = da.rio.write_nodata(nodata)

    return da

# Create synthetic scenes for different dates
print("Creating synthetic Landsat scenes...")
scene_2020 = create_synthetic_landsat_scene("landsat_2020.tif")
scene_2021 = create_synthetic_landsat_scene("landsat_2021.tif")
scene_2022 = create_synthetic_landsat_scene("landsat_2022.tif")

# Check CRS and spatial metadata
print(f"CRS: {scene_2020.rio.crs}")
print(f"Bounds: {scene_2020.rio.bounds()}")
print(f"Resolution: {scene_2020.rio.resolution()}")
print(f"Shape: {scene_2020.shape}")

# Calculate NDVI (Normalized Difference Vegetation Index)
def calculate_ndvi(scene):
    """Calculate NDVI from red and NIR bands"""
    red = scene.sel(band=3).astype(float)
    nir = scene.sel(band=4).astype(float)

    ndvi = (nir - red) / (nir + red)

    # Preserve CRS
    ndvi = ndvi.rio.write_crs(scene.rio.crs)
    ndvi = ndvi.rio.write_nodata(-9999)

    return ndvi

ndvi_2020 = calculate_ndvi(scene_2020)
ndvi_2021 = calculate_ndvi(scene_2021)
ndvi_2022 = calculate_ndvi(scene_2022)

print(f"\nNDVI 2020 range: {ndvi_2020.min().values:.3f} to {ndvi_2020.max().values:.3f}")

# Create time series
ndvi_timeseries = xr.concat([ndvi_2020, ndvi_2021, ndvi_2022], dim="time")
ndvi_timeseries["time"] = pd.date_range("2020-07-01", periods=3, freq="1Y")
ndvi_timeseries = ndvi_timeseries.rio.write_crs(scene_2020.rio.crs)

# Reproject to WGS84 (lat/lon) for visualization
print("\nReprojecting to WGS84...")
ndvi_wgs84 = ndvi_2020.rio.reproject("EPSG:4326")
print(f"WGS84 bounds: {ndvi_wgs84.rio.bounds()}")

# Clip to area of interest (bounding box in lat/lon)
aoi_bounds = {
    "minx": -122.5,
    "miny": 37.5,
    "maxx": -121.5,
    "maxy": 38.5
}

ndvi_clipped = ndvi_wgs84.rio.clip_box(**aoi_bounds)
print(f"Clipped shape: {ndvi_clipped.shape}")

# Calculate vegetation change over time
ndvi_change = ndvi_2022 - ndvi_2020
ndvi_change = ndvi_change.rio.write_crs(scene_2020.rio.crs)

# Identify areas with significant vegetation gain/loss
vegetation_gain = ndvi_change > 0.1
vegetation_loss = ndvi_change < -0.1

print(f"\nVegetation gain: {vegetation_gain.sum().values} pixels")
print(f"Vegetation loss: {vegetation_loss.sum().values} pixels")

# Calculate zonal statistics (by latitude zones)
# Create latitude zones
lat_zones = ndvi_wgs84.y // 0.5  # 0.5 degree zones
zonal_mean = ndvi_wgs84.groupby(lat_zones).mean()

print("\nMean NDVI by latitude zone:")
for zone, mean_val in zonal_mean.groupby("y"):
    print(f"  Zone {zone}: {mean_val.values:.3f}")

# Regrid to coarser resolution for faster processing
from rasterio.enums import Resampling

ndvi_coarse = scene_2020.rio.reproject(
    scene_2020.rio.crs,
    resolution=(500, 500),  # 500m resolution
    resampling=Resampling.average
)
print(f"\nCoarse resolution shape: {ndvi_coarse.shape}")

# Save results with proper geospatial metadata
# Note: In real usage, you would uncomment these lines
# ndvi_2020.rio.to_raster("ndvi_2020.tif", compress="lzw")
# ndvi_change.rio.to_raster("ndvi_change_2020_2022.tif", driver="COG")  # Cloud Optimized GeoTIFF

# Multi-temporal analysis: Calculate NDVI trend
def calculate_spatial_trend(timeseries):
    """Calculate pixel-wise trend over time"""
    from scipy import stats

    def trend_func(x):
        if np.isnan(x).all():
            return np.nan
        valid = ~np.isnan(x)
        if valid.sum() < 2:
            return np.nan
        slope, _, _, _, _ = stats.linregress(np.arange(len(x))[valid], x[valid])
        return slope

    # Apply trend calculation across time dimension
    trend = xr.apply_ufunc(
        trend_func,
        timeseries,
        input_core_dims=[["time"]],
        vectorize=True
    )

    return trend

ndvi_trend = calculate_spatial_trend(ndvi_timeseries)
ndvi_trend = ndvi_trend.rio.write_crs(ndvi_timeseries.rio.crs)

print(f"\nNDVI trend range: {np.nanmin(ndvi_trend.values):.4f} to {np.nanmax(ndvi_trend.values):.4f} per year")

# Integration with vector data (example with synthetic polygon)
# In practice, use geopandas to load shapefiles
print("\nExample: Clipping to vector geometry")
print("(In practice, use geopandas.read_file() to load actual shapefiles)")

# Create time-averaged NDVI composite
ndvi_composite = ndvi_timeseries.mean(dim="time")
ndvi_composite = ndvi_composite.rio.write_crs(ndvi_timeseries.rio.crs)

print("\nAnalysis complete!")
print("Results:")
print(f"  - NDVI time series: {ndvi_timeseries.shape}")
print(f"  - NDVI change (2020-2022): {ndvi_change.shape}")
print(f"  - NDVI trend: {ndvi_trend.shape}")
print(f"  - Mean NDVI (2020-2022): {ndvi_composite.mean().values:.3f}")
```


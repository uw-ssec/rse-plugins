---
description: Work with labeled multidimensional data using Xarray for NetCDF, Zarr, climate, and satellite data analysis
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Xarray for Multidimensional Data

Work with labeled multidimensional arrays using Xarray.

## Arguments

$ARGUMENTS — describe the task (e.g., "read this NetCDF file", "analyze climate data", "set up Dask chunking for large dataset")

## Workflow

1. **Understand the task** from the arguments:
   - NetCDF/HDF5/Zarr I/O
   - DataArray and Dataset operations
   - Dask integration for large datasets
   - Climate/satellite/oceanographic analysis
   - Geospatial raster operations (rioxarray)
   - DataTree for hierarchical data

2. **Explore existing data and code:**
   - Check for data files (*.nc, *.zarr, *.hdf5)
   - Identify dimensions, coordinates, and variables
   - Assess data size for chunking strategy

3. **Implement** using Xarray best practices:
   - Named dimensions and coordinates
   - Proper chunking for out-of-core computation
   - Lazy evaluation with Dask where appropriate
   - CF conventions for metadata

4. **Verify** results and performance.

5. **Report** results including data structure and any performance considerations.

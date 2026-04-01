#!/usr/bin/env python3
"""
Zarr Quickstart Script
======================

A complete, runnable introduction to Zarr v3 fundamentals.
Demonstrates array creation, data I/O, group hierarchy, metadata,
inspection, indexing, and compression configuration.

Requirements:
    pip install zarr numpy
    # or: pixi add zarr numpy

Usage:
    python zarr-quickstart.py
"""

import shutil
import tempfile
from pathlib import Path

import numpy as np
import zarr


def main():
    # Use a temporary directory so the script is self-contained and clean
    work_dir = Path(tempfile.mkdtemp(prefix="zarr_quickstart_"))
    print(f"Working directory: {work_dir}\n")

    # ──────────────────────────────────────────────
    # 1. Creating a Zarr v3 Array
    # ──────────────────────────────────────────────
    print("=" * 60)
    print("1. Creating a Zarr v3 Array")
    print("=" * 60)

    store_path = str(work_dir / "temperature.zarr")

    z = zarr.create_array(
        store=store_path,
        shape=(365, 180, 360),       # time x lat x lon
        chunks=(30, 90, 180),        # ~30 days, half-globe chunks
        dtype="float32",
        fill_value=np.nan,
        overwrite=True,
    )

    print(f"Created array: shape={z.shape}, chunks={z.chunks}, dtype={z.dtype}")
    print(f"Format: Zarr v{z.metadata.zarr_format}")
    print()

    # ──────────────────────────────────────────────
    # 2. Writing and Reading Data
    # ──────────────────────────────────────────────
    print("=" * 60)
    print("2. Writing and Reading Data")
    print("=" * 60)

    # Generate synthetic temperature data (roughly 0-30 C with latitude gradient)
    np.random.seed(42)
    lat_values = np.linspace(-90, 90, 180)
    lat_gradient = 15 + 15 * np.cos(np.deg2rad(lat_values))  # warmer near equator
    data = (
        lat_gradient[np.newaxis, :, np.newaxis]
        + np.random.randn(365, 180, 360).astype("float32") * 3
    )
    z[:] = data.astype("float32")
    print(f"Wrote {data.nbytes / 1e6:.1f} MB of data")

    # Read a subset: first 10 days, first 10 lat points, first 10 lon points
    subset = z[0:10, 0:10, 0:10]
    print(f"Read subset shape: {subset.shape}")
    print(f"Subset mean: {subset.mean():.2f}")
    print()

    # ──────────────────────────────────────────────
    # 3. Creating a Group Hierarchy
    # ──────────────────────────────────────────────
    print("=" * 60)
    print("3. Creating a Group Hierarchy")
    print("=" * 60)

    root_path = str(work_dir / "climate_study.zarr")
    root = zarr.open_group(root_path, mode="w")

    # Create subgroups for different data categories
    observations = root.create_group("observations")
    model_output = root.create_group("model_output")
    analysis = root.create_group("analysis")

    # Create arrays within the observations group
    temp_obs = observations.create_array(
        "temperature",
        shape=(365, 180, 360),
        chunks=(30, 90, 180),
        dtype="float32",
        fill_value=np.nan,
    )

    precip_obs = observations.create_array(
        "precipitation",
        shape=(365, 180, 360),
        chunks=(30, 90, 180),
        dtype="float32",
        fill_value=0.0,
    )

    # Create a model output array
    temp_model = model_output.create_array(
        "temperature_forecast",
        shape=(30, 180, 360),
        chunks=(10, 90, 180),
        dtype="float32",
    )

    print(f"Created hierarchy at: {root_path}")
    print(f"Groups: {list(root.group_keys())}")
    print(f"Observations arrays: {list(observations.array_keys())}")
    print()

    # ──────────────────────────────────────────────
    # 4. Setting Metadata and Attributes
    # ──────────────────────────────────────────────
    print("=" * 60)
    print("4. Setting Metadata and Attributes")
    print("=" * 60)

    # Group-level metadata (dataset-wide)
    root.attrs["Conventions"] = "CF-1.8"
    root.attrs["title"] = "Quickstart Climate Dataset"
    root.attrs["institution"] = "Zarr Quickstart Demo"
    root.attrs["source"] = "Synthetic data for demonstration"
    root.attrs["history"] = "Created by zarr-quickstart.py"

    # Array-level metadata (variable-specific)
    temp_obs.attrs["units"] = "Celsius"
    temp_obs.attrs["long_name"] = "Near-Surface Air Temperature"
    temp_obs.attrs["standard_name"] = "air_temperature"
    temp_obs.attrs["valid_range"] = [-80.0, 60.0]

    precip_obs.attrs["units"] = "mm/day"
    precip_obs.attrs["long_name"] = "Daily Precipitation Rate"
    precip_obs.attrs["standard_name"] = "precipitation_flux"

    print("Root attributes:")
    for key, value in root.attrs.items():
        print(f"  {key}: {value}")

    print("\nTemperature attributes:")
    for key, value in temp_obs.attrs.items():
        print(f"  {key}: {value}")
    print()

    # ──────────────────────────────────────────────
    # 5. Inspecting with .info and .tree()
    # ──────────────────────────────────────────────
    print("=" * 60)
    print("5. Inspecting with .info and .tree()")
    print("=" * 60)

    # Re-open to verify persistence
    root = zarr.open_group(root_path, mode="r")

    print("--- Hierarchy (.tree()) ---")
    print(root.tree())

    # Array info (quick summary)
    temp_arr = root["observations/temperature"]
    print("\n--- Array Info (.info) ---")
    print(temp_arr.info)
    print()

    # ──────────────────────────────────────────────
    # 6. Basic and Advanced Indexing
    # ──────────────────────────────────────────────
    print("=" * 60)
    print("6. Basic and Advanced Indexing")
    print("=" * 60)

    # Re-open the standalone temperature array for indexing demos
    z = zarr.open_array(store_path, mode="r")

    # Basic slicing
    time_slice = z[0, :, :]  # Single time step, all spatial
    print(f"Basic slice (1 time step):    shape={time_slice.shape}")

    point_series = z[:, 90, 180]  # Full time series at one point
    print(f"Time series at one point:     shape={point_series.shape}")

    region = z[0:30, 80:100, 170:190]  # Subregion
    print(f"Subregion (30d, 20lat, 20lon): shape={region.shape}")

    # Orthogonal indexing (Cartesian product of indices)
    selected_times = [0, 30, 60, 90]
    selected_lats = [45, 90, 135]
    ortho = z.oindex[selected_times, selected_lats, :]
    print(f"Orthogonal selection:         shape={ortho.shape}")

    # Block indexing (by chunk index)
    first_chunk = z.blocks[0, 0, 0]
    print(f"First chunk block:            shape={first_chunk.shape}")

    # Coordinate selection (scattered points)
    rows = [0, 100, 200, 300]
    cols = [10, 50, 90, 130]
    depths = [0, 100, 200, 300]
    coord_sel = z.get_coordinate_selection((rows, cols, depths))
    print(f"Coordinate selection (4 pts): shape={coord_sel.shape}")
    print()

    # ──────────────────────────────────────────────
    # 7. Compression Configuration
    # ──────────────────────────────────────────────
    print("=" * 60)
    print("7. Compression Configuration")
    print("=" * 60)

    # Default compression (Zstd in v3)
    default_path = str(work_dir / "default_compression.zarr")
    z_default = zarr.create_array(
        store=default_path,
        shape=(1000, 1000),
        chunks=(100, 100),
        dtype="float32",
        overwrite=True,
    )
    z_default[:] = np.random.randn(1000, 1000).astype("float32")
    print(f"Default compression: {z_default.metadata.codecs}")

    # Custom compression with explicit Zstd level
    zstd_path = str(work_dir / "zstd_compression.zarr")
    z_zstd = zarr.create_array(
        store=zstd_path,
        shape=(1000, 1000),
        chunks=(100, 100),
        dtype="float32",
        compressors=zarr.codecs.ZstdCodec(level=5),
        overwrite=True,
    )
    z_zstd[:] = np.random.randn(1000, 1000).astype("float32")
    print(f"Zstd level 5:        {z_zstd.metadata.codecs}")

    # No compression (for already-compressed or incompressible data)
    raw_path = str(work_dir / "no_compression.zarr")
    z_raw = zarr.create_array(
        store=raw_path,
        shape=(1000, 1000),
        chunks=(100, 100),
        dtype="float32",
        compressors=None,
        overwrite=True,
    )
    z_raw[:] = np.random.randn(1000, 1000).astype("float32")
    print(f"No compression:      {z_raw.metadata.codecs}")

    print()

    # ──────────────────────────────────────────────
    # Summary
    # ──────────────────────────────────────────────
    print("=" * 60)
    print("Quickstart Complete!")
    print("=" * 60)
    print(f"\nAll output written to: {work_dir}")
    print("\nKey concepts demonstrated:")
    print("  - Array creation with zarr.create_array()")
    print("  - Data writing (z[:] = ...) and reading (z[0:10, ...])")
    print("  - Group hierarchy with create_group()")
    print("  - Metadata with .attrs")
    print("  - Inspection with .info and .tree()")
    print("  - Six indexing modes: basic, orthogonal, block, coordinate, mask, field")
    print("  - Compression configuration (Zstd, none)")
    print()
    print("Next steps:")
    print("  - Try zarr.open_array('s3://...') for cloud storage")
    print("  - Explore sharding with the shards= parameter")
    print("  - Integrate with xarray: xr.open_zarr('path.zarr')")

    # Clean up temporary directory
    shutil.rmtree(work_dir)
    print(f"\nCleaned up temporary directory: {work_dir}")


if __name__ == "__main__":
    main()

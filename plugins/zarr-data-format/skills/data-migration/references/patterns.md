# Data Migration Patterns

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| Pattern 1: Single HDF5 File to Zarr via xarray | 14–75 | Convert one HDF5 file with rechunking and encoding |
| Pattern 2: Directory of NetCDF Files to Single Zarr Store | 76–155 | Combine many NetCDFs into a consolidated Zarr store |
| Pattern 3: VirtualiZarr References for Cloud-Hosted HDF5 | 156–235 | Create virtual Zarr references without copying data |
| Pattern 4: Direct Copy for Group-Level Migration | 236–320 | Copy HDF5 group hierarchies preserving structure |
| Pattern 5: Incremental Migration with Checkpointing | 321–410 | Batch-process large archives with restart capability |
| Pattern 6: Post-Migration Validation Pipeline | 411–490 | Verify source and target match after migration |

---

## Pattern 1: Single HDF5 File to Zarr via xarray

**Description:** Convert a single HDF5 file to Zarr using xarray as the intermediary. This handles CF metadata, coordinate variables, and allows rechunking during conversion.

**When to use:**
- HDF5 files produced by scientific models or instruments
- Need to change chunk layout for cloud-optimized access
- File has standard dimensions that xarray can interpret

**Code example:**

```python
import xarray as xr

# ── Open the HDF5 file ──
ds = xr.open_dataset(
    "simulation_output.h5",
    engine="h5netcdf",
    chunks={"time": 30, "x": 100, "y": 100},  # lazy loading
)
print(f"Source: {dict(ds.dims)}")
print(f"Variables: {list(ds.data_vars)}")

# ── Define encoding for Zarr ──
encoding = {}
for var in ds.data_vars:
    encoding[var] = {
        "chunks": {"time": 30, "x": 100, "y": 100},
        "dtype": "float32" if ds[var].dtype == "float64" else str(ds[var].dtype),
    }

# ── Write to Zarr ──
ds.to_zarr("simulation_output.zarr", mode="w", encoding=encoding, consolidated=True)

# ── Verify ──
ds_zarr = xr.open_zarr("simulation_output.zarr")
print(f"Target: {dict(ds_zarr.dims)}")
xr.testing.assert_allclose(
    ds.astype("float32"),
    ds_zarr.compute(),
    rtol=1e-5,
)
print("Validation passed")
```

---

## Pattern 2: Directory of NetCDF Files to Single Zarr Store

**Description:** Combine an archive of NetCDF files (typically one file per time step or month) into a single Zarr store. This eliminates the many-small-files problem and enables efficient cloud storage.

**When to use:**
- Climate model output split into monthly or daily files
- Observational archives with one file per satellite pass or station
- Any collection of NetCDF files that should be a single dataset

**Code example:**

```python
import xarray as xr
from pathlib import Path

# ── Discover source files ──
source_dir = Path("netcdf_archive/")
files = sorted(source_dir.glob("*.nc"))
print(f"Found {len(files)} NetCDF files")

# ── Preview one file to understand structure ──
ds_sample = xr.open_dataset(files[0])
print(f"Sample dims: {dict(ds_sample.dims)}")
print(f"Sample vars: {list(ds_sample.data_vars)}")
ds_sample.close()

# ── Open all files lazily ──
ds = xr.open_mfdataset(
    files,
    combine="nested",
    concat_dim="time",
    chunks={"time": 31, "lat": 90, "lon": 180},
    parallel=True,  # use Dask for parallel file opening
)
print(f"Combined: {dict(ds.dims)}")

# ── Define encoding ──
encoding = {
    var: {
        "chunks": {"time": 30, "lat": 90, "lon": 180},
        "dtype": "float32",
    }
    for var in ds.data_vars
    if set(ds[var].dims) == {"time", "lat", "lon"}
}

# ── Write to Zarr ──
ds.to_zarr(
    "combined_archive.zarr",
    mode="w",
    encoding=encoding,
    consolidated=True,
)
print("Migration complete")

# ── Verify total time steps ──
ds_zarr = xr.open_zarr("combined_archive.zarr")
print(f"Total time steps: {len(ds_zarr.time)}")
```

---

## Pattern 3: VirtualiZarr References for Cloud-Hosted HDF5

**Description:** Create a virtual Zarr store that references data in existing HDF5/NetCDF files without copying any array data. Reads are served directly from the source files via byte-range requests.

**When to use:**
- Large archives where full copying is impractical or too expensive
- Source files are already on cloud storage (S3, GCS)
- Need a unified Zarr interface over heterogeneous source files
- Want to test a migration approach before committing to a full copy

**Code example:**

```python
from virtualizarr import open_virtual_dataset
import xarray as xr
from pathlib import Path

# ── Create virtual references for each source file ──
source_files = sorted(Path("archive/").glob("*.nc"))
vds_list = []

for path in source_files:
    vds = open_virtual_dataset(str(path))
    vds_list.append(vds)
    print(f"  Scanned: {path.name}")

# ── Combine along time dimension ──
combined = xr.concat(vds_list, dim="time")
print(f"Combined virtual dataset: {dict(combined.dims)}")

# ── Write the virtual Zarr store (only metadata + byte offsets) ──
combined.virtualize.to_zarr("virtual_archive.zarr")
print("Wrote virtual Zarr store (no data copied)")

# ── Read through the virtual store ──
ds = xr.open_zarr("virtual_archive.zarr")
print(f"Readable dataset: {dict(ds.dims)}")

# Data reads go to the original source files
subset = ds["temperature"].sel(time="2024-01").compute()
print(f"Subset shape: {subset.shape}")

# ── For cloud-hosted sources ──
# vds = open_virtual_dataset(
#     "s3://archive/data_2024.nc",
#     reader_options={"storage_options": {"anon": True}},
# )
```

---

## Pattern 4: Direct Copy for Group-Level Migration

**Description:** Copy HDF5 group hierarchies directly to Zarr, preserving the full tree structure, attributes, and datasets. Use this when xarray cannot represent the HDF5 structure (e.g., deeply nested groups, non-array datasets).

**When to use:**
- HDF5 files with complex group hierarchies that xarray flattens
- Need to preserve exact group/dataset structure
- Files with non-standard HDF5 features

**Code example:**

```python
import h5py
import zarr
import numpy as np

def migrate_hdf5_to_zarr(h5_path, zarr_path):
    """Recursively copy an HDF5 file to a Zarr store."""
    with h5py.File(h5_path, "r") as h5f:
        root = zarr.open_group(zarr_path, mode="w")

        def copy_node(h5_node, zarr_node):
            # Copy attributes
            for attr_name, attr_val in h5_node.attrs.items():
                try:
                    zarr_node.attrs[attr_name] = attr_val
                except TypeError:
                    zarr_node.attrs[attr_name] = str(attr_val)

            for key in h5_node:
                item = h5_node[key]
                if isinstance(item, h5py.Group):
                    zg = zarr_node.create_group(key)
                    copy_node(item, zg)
                elif isinstance(item, h5py.Dataset):
                    # Determine chunks
                    if item.chunks:
                        chunks = item.chunks
                    elif item.ndim > 0:
                        chunks = tuple(min(s, 1000) for s in item.shape)
                    else:
                        chunks = None

                    if item.ndim == 0:
                        # Scalar dataset
                        zarr_node.attrs[key] = item[()]
                    else:
                        arr = zarr_node.create_array(
                            key,
                            data=item[:],
                            chunks=chunks,
                            dtype=item.dtype,
                        )
                        # Copy dataset attributes
                        for attr_name, attr_val in item.attrs.items():
                            try:
                                arr.attrs[attr_name] = attr_val
                            except TypeError:
                                arr.attrs[attr_name] = str(attr_val)

        copy_node(h5f, root)

    print(f"Migrated {h5_path} → {zarr_path}")
    return zarr.open_group(zarr_path, mode="r")

# ── Usage ──
root = migrate_hdf5_to_zarr("instrument_data.h5", "instrument_data.zarr")
print(root.tree())
```

---

## Pattern 5: Incremental Migration with Checkpointing

**Description:** Migrate a large archive of files with checkpoint tracking, so the migration can be resumed if interrupted. Each successfully migrated file is recorded, and previously completed files are skipped on restart.

**When to use:**
- Archives with thousands of files where migration takes hours or days
- Unreliable environments (spot instances, preemptible VMs)
- Need to track progress and handle individual file failures

**Code example:**

```python
import xarray as xr
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def incremental_migrate(
    source_dir: str,
    zarr_path: str,
    checkpoint_file: str = "migration_checkpoint.json",
    pattern: str = "*.nc",
):
    """Migrate files with checkpoint-based resume capability."""
    source_files = sorted(Path(source_dir).glob(pattern))

    # Load checkpoint
    checkpoint_path = Path(checkpoint_file)
    if checkpoint_path.exists():
        completed = set(json.loads(checkpoint_path.read_text()))
        logger.info(f"Resuming: {len(completed)}/{len(source_files)} already done")
    else:
        completed = set()

    # Filter to remaining files
    remaining = [f for f in source_files if str(f) not in completed]
    logger.info(f"Files remaining: {len(remaining)}")

    for i, filepath in enumerate(remaining):
        try:
            ds = xr.open_dataset(filepath)

            if not completed:
                # First file: create the store
                ds.to_zarr(zarr_path, mode="w")
            else:
                # Subsequent files: append
                ds.to_zarr(zarr_path, append_dim="time")

            ds.close()

            # Update checkpoint
            completed.add(str(filepath))
            checkpoint_path.write_text(json.dumps(list(completed)))
            logger.info(f"[{i+1}/{len(remaining)}] Migrated {filepath.name}")

        except Exception as e:
            logger.error(f"Failed on {filepath.name}: {e}")
            continue  # skip and continue with next file

    logger.info(f"Migration complete: {len(completed)}/{len(source_files)} files")

# ── Usage ──
# incremental_migrate("netcdf_archive/", "migrated.zarr")
```

---

## Pattern 6: Post-Migration Validation Pipeline

**Description:** Systematically validate that a migrated Zarr store matches the original source data in dimensions, variables, values, attributes, and data types.

**When to use:**
- After any format migration (HDF5/NetCDF → Zarr)
- Before decommissioning source files
- As part of an automated CI/CD migration pipeline

**Code example:**

```python
import xarray as xr
import numpy as np


def validate_migration(source_path, zarr_path, rtol=1e-5, engine="netcdf4"):
    """Comprehensive validation of source vs migrated Zarr store."""
    ds_src = xr.open_dataset(source_path, engine=engine)
    ds_dst = xr.open_zarr(zarr_path)

    report = {"passed": [], "failed": []}

    # ── 1. Dimension check ──
    if dict(ds_src.dims) == dict(ds_dst.dims):
        report["passed"].append("Dimensions match")
    else:
        report["failed"].append(f"Dims: src={dict(ds_src.dims)}, dst={dict(ds_dst.dims)}")

    # ── 2. Variable check ──
    src_vars = set(ds_src.data_vars)
    dst_vars = set(ds_dst.data_vars)
    missing = src_vars - dst_vars
    extra = dst_vars - src_vars
    if not missing and not extra:
        report["passed"].append("Variables match")
    else:
        if missing:
            report["failed"].append(f"Missing variables: {missing}")
        if extra:
            report["failed"].append(f"Extra variables: {extra}")

    # ── 3. Value check ──
    for var in src_vars & dst_vars:
        src_vals = ds_src[var].values
        dst_vals = ds_dst[var].values

        # Handle dtype differences (e.g., float64 → float32)
        if src_vals.dtype != dst_vals.dtype:
            src_vals = src_vals.astype(dst_vals.dtype)

        if np.allclose(src_vals, dst_vals, equal_nan=True, rtol=rtol):
            report["passed"].append(f"{var}: values match (rtol={rtol})")
        else:
            max_diff = float(np.nanmax(np.abs(src_vals - dst_vals)))
            report["failed"].append(f"{var}: max diff = {max_diff}")

    # ── 4. Attribute check ──
    for var in src_vars & dst_vars:
        missing_attrs = set(ds_src[var].attrs) - set(ds_dst[var].attrs)
        if missing_attrs:
            report["failed"].append(f"{var}: missing attrs {missing_attrs}")
        else:
            report["passed"].append(f"{var}: attributes preserved")

    # ── Print report ──
    print("\n=== Migration Validation Report ===")
    for item in report["passed"]:
        print(f"  PASS: {item}")
    for item in report["failed"]:
        print(f"  FAIL: {item}")
    print(f"\nResult: {len(report['passed'])} passed, {len(report['failed'])} failed")

    ds_src.close()
    ds_dst.close()
    return len(report["failed"]) == 0
```

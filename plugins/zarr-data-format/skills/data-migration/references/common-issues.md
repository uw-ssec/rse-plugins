# Common Issues and Solutions

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| Issue 1: HDF5 Features Not Supported in Zarr | 18–75 | Soft links, object references, and custom filters |
| Issue 2: Metadata Loss During Conversion | 76–135 | Encoding attributes stripped by xarray |
| Issue 3: Memory Errors on Large File Conversion | 136–200 | Loading entire file into memory during migration |
| Issue 4: VirtualiZarr References Become Invalid | 201–255 | Source files moved or renamed after creating references |
| Issue 5: Chunk Size Not Optimal After Migration | 256–315 | Inheriting HDF5 chunk layout for cloud storage |
| Issue 6: Fill Value Mismatch Between HDF5 and Zarr | 316–370 | Different fill value conventions causing data issues |
| Issue 7: Encoding/Dtype Differences Between Source and Target | 371–430 | Unexpected type changes during migration |

---

## Issue 1: HDF5 Features Not Supported in Zarr

**Symptoms:**
- `TypeError` or `ValueError` during migration
- Soft links or external links in HDF5 not appearing in Zarr output
- Object references (`h5py.Reference`) causing errors
- Custom HDF5 filters (e.g., MAFISC, bitshuffle) not recognized

**Cause:** Zarr does not support HDF5-specific features like soft links, hard links, object references, named data types, or custom HDF5 filters. These features have no equivalent in the Zarr specification.

**Solution:**

```python
import h5py
import zarr

# ── Diagnose: Identify unsupported features ──
with h5py.File("complex.h5", "r") as f:
    def check_features(group, path=""):
        for key in group:
            item = group[key]
            full_path = f"{path}/{key}"

            # Check for soft links
            link = group.get(key, getlink=True)
            if isinstance(link, h5py.SoftLink):
                print(f"  SOFT LINK: {full_path} → {link.path}")
            elif isinstance(link, h5py.ExternalLink):
                print(f"  EXTERNAL LINK: {full_path} → {link.filename}:{link.path}")

            if isinstance(item, h5py.Dataset):
                # Check for object references
                if item.dtype.kind == 'O':
                    print(f"  OBJECT REF: {full_path}")
                # Check for custom filters
                if item.id.get_create_plist().get_nfilters() > 0:
                    for i in range(item.id.get_create_plist().get_nfilters()):
                        filt = item.id.get_create_plist().get_filter(i)
                        print(f"  FILTER: {full_path} uses filter {filt}")

            elif isinstance(item, h5py.Group):
                check_features(item, full_path)

    check_features(f)

# ── Fix: Resolve links and convert references before migration ──
with h5py.File("complex.h5", "r") as f:
    root = zarr.open_group("resolved.zarr", mode="w")

    # Resolve soft links by following them
    for key in f:
        target = f[key]  # h5py resolves links automatically on access
        if isinstance(target, h5py.Dataset):
            root.create_array(key, data=target[:], dtype=target.dtype)
```

---

## Issue 2: Metadata Loss During Conversion

**Symptoms:**
- Attributes like `_FillValue`, `scale_factor`, `add_offset` missing after roundtrip
- CF encoding attributes moved from `attrs` to `encoding` or vice versa
- Custom attributes disappearing from variables

**Cause:** xarray treats certain attributes specially during CF decoding/encoding. Attributes like `_FillValue`, `scale_factor`, `add_offset`, `dtype`, and `missing_value` are consumed during decoding and stored in the variable's `encoding` dict, not in `attrs`.

**Solution:**

```python
import xarray as xr

# ── Diagnose: Compare attributes before and after ──
ds_src = xr.open_dataset("source.nc", decode_cf=False)  # raw attributes
ds_decoded = xr.open_dataset("source.nc")  # CF-decoded

for var in ds_src.data_vars:
    raw_attrs = set(ds_src[var].attrs.keys())
    decoded_attrs = set(ds_decoded[var].attrs.keys())
    moved = raw_attrs - decoded_attrs
    if moved:
        print(f"{var}: attrs moved to encoding: {moved}")

# ── Fix 1: Preserve attributes by disabling CF decoding ──
ds = xr.open_dataset("source.nc", decode_cf=False)
ds.to_zarr("output.zarr")  # all original attributes preserved

# ── Fix 2: Explicitly set encoding to preserve CF attributes ──
ds = xr.open_dataset("source.nc")
encoding = {}
for var in ds.data_vars:
    encoding[var] = {
        k: v for k, v in ds[var].encoding.items()
        if k in ("_FillValue", "scale_factor", "add_offset", "dtype", "calendar")
    }
ds.to_zarr("output.zarr", encoding=encoding)

# ── Fix 3: Copy all original attrs back before writing ──
ds_raw = xr.open_dataset("source.nc", decode_cf=False)
for var in ds.data_vars:
    ds[var].attrs.update(ds_raw[var].attrs)
ds.to_zarr("output.zarr")
```

---

## Issue 3: Memory Errors on Large File Conversion

**Symptoms:**
- `MemoryError` when opening a large HDF5/NetCDF file
- System OOM kill during `ds.to_zarr()`
- Swap space fills up during conversion

**Cause:** By default, `xr.open_dataset()` loads data eagerly into memory. For large files (>RAM), the entire dataset is materialized before writing begins.

**Solution:**

```python
import xarray as xr

# ── Fix 1: Open with Dask chunks (lazy loading) ──
ds = xr.open_dataset(
    "huge_file.nc",
    chunks={"time": 30, "lat": 90, "lon": 180},  # lazy
)
ds.to_zarr("output.zarr")  # Dask writes chunk-by-chunk

# ── Fix 2: Process variables one at a time ──
import zarr

ds_info = xr.open_dataset("huge_file.nc", chunks={})
for var in ds_info.data_vars:
    ds_var = xr.open_dataset("huge_file.nc", chunks={"time": 30})[var]
    ds_var.to_dataset().to_zarr(
        "output.zarr",
        mode="a" if var != list(ds_info.data_vars)[0] else "w",
    )
    print(f"Wrote {var}")

# ── Fix 3: For h5py, copy in slices ──
import h5py
import numpy as np

with h5py.File("huge_file.h5", "r") as f:
    src = f["data"]
    root = zarr.open_group("output.zarr", mode="w")
    dst = root.create_array(
        "data",
        shape=src.shape,
        chunks=(1000, 1000),
        dtype=src.dtype,
    )

    # Copy in chunks
    chunk_size = 1000
    for start in range(0, src.shape[0], chunk_size):
        end = min(start + chunk_size, src.shape[0])
        dst[start:end] = src[start:end]
        print(f"Copied rows {start}-{end}")
```

---

## Issue 4: VirtualiZarr References Become Invalid

**Symptoms:**
- `FileNotFoundError` when reading through the virtual Zarr store
- Data was accessible but now returns errors
- Virtual store metadata loads but data reads fail

**Cause:** VirtualiZarr stores byte offsets pointing to specific positions in source files. If source files are moved, renamed, deleted, or modified, the references become stale.

**Solution:**

```python
# ── Prevention: Use immutable storage for sources ──
# - S3 object versioning
# - Glacier or archive tiers (immutable by design)
# - Read-only permissions on source directories

# ── Fix 1: Regenerate references after source changes ──
from virtualizarr import open_virtual_dataset
import xarray as xr

# Re-scan the updated file locations
updated_files = sorted(Path("new_location/").glob("*.nc"))
vds_list = [open_virtual_dataset(str(f)) for f in updated_files]
combined = xr.concat(vds_list, dim="time")
combined.virtualize.to_zarr("virtual_store.zarr")  # overwrite references

# ── Fix 2: Use Icechunk for versioned virtual references ──
from icechunk import IcechunkStore, StorageConfig

storage = StorageConfig.s3_from_env(bucket="bucket", prefix="virtual.zarr")
store = IcechunkStore.open_or_create(storage=storage, mode="w")
combined.virtualize.to_zarr(store)
store.commit("Updated file references after source migration")
# Old snapshots still point to old locations (useful for auditing)
```

---

## Issue 5: Chunk Size Not Optimal After Migration

**Symptoms:**
- Cloud reads are slow despite successful migration
- Thousands of tiny objects in the Zarr store
- Each chunk is only a few KB instead of MB

**Cause:** The migration inherited the HDF5 chunk layout, which was optimized for local disk access (small chunks for fine-grained updates) rather than cloud storage (large chunks to minimize request count).

**Solution:**

```python
import xarray as xr

# ── Diagnose: Check chunk sizes ──
ds = xr.open_zarr("migrated.zarr")
for var in ds.data_vars:
    chunks = ds[var].encoding.get("chunks")
    if chunks:
        size_bytes = ds[var].dtype.itemsize
        for c in chunks:
            size_bytes *= c
        print(f"{var}: chunks={chunks}, size={size_bytes/1e6:.2f} MB")

# ── Fix: Rechunk during migration ──
ds_src = xr.open_dataset("source.h5", engine="h5netcdf", chunks={"time": 30})

# Target: 1-10 MB per chunk for cloud storage
encoding = {
    var: {"chunks": {"time": 30, "lat": 90, "lon": 180}}
    for var in ds_src.data_vars
    if set(ds_src[var].dims) == {"time", "lat", "lon"}
}
ds_src.to_zarr("rechunked_output.zarr", encoding=encoding)

# ── For already-migrated stores, use rechunker ──
# pip install rechunker
from rechunker import rechunk

target_chunks = {"temperature": {"time": 30, "lat": 90, "lon": 180}}
rechunked = rechunk(
    source=xr.open_zarr("poorly_chunked.zarr"),
    target_chunks=target_chunks,
    target_store="rechunked.zarr",
    temp_store="temp_rechunk.zarr",
    max_mem="2GB",
)
rechunked.execute()
```

---

## Issue 6: Fill Value Mismatch Between HDF5 and Zarr

**Symptoms:**
- NaN values in source appear as specific numbers in Zarr (e.g., -9999, 9.96921e+36)
- Valid data values appear as NaN in the Zarr store
- Statistical computations give different results after migration

**Cause:** HDF5 and Zarr handle fill values differently. HDF5 uses `_FillValue` attributes that xarray decodes during read (replacing with NaN). If encoding is not set correctly during write, the fill values may not roundtrip properly.

**Solution:**

```python
import xarray as xr
import numpy as np

# ── Diagnose: Check fill values in source ──
ds_raw = xr.open_dataset("source.nc", decode_cf=False)
for var in ds_raw.data_vars:
    fv = ds_raw[var].attrs.get("_FillValue", "not set")
    mv = ds_raw[var].attrs.get("missing_value", "not set")
    print(f"{var}: _FillValue={fv}, missing_value={mv}")

# ── Fix 1: Preserve fill values in encoding ──
ds = xr.open_dataset("source.nc")
encoding = {}
for var in ds.data_vars:
    fv = ds[var].encoding.get("_FillValue")
    encoding[var] = {"_FillValue": fv}  # preserve original fill value

ds.to_zarr("output.zarr", encoding=encoding)

# ── Fix 2: Use NaN as fill value (simplest for float data) ──
encoding = {var: {"_FillValue": np.nan} for var in ds.data_vars}
ds.to_zarr("output.zarr", encoding=encoding)

# ── Fix 3: Explicitly handle missing data before writing ──
for var in ds.data_vars:
    # Replace any remaining sentinel values with NaN
    ds[var] = ds[var].where(ds[var] != -9999.0)
ds.to_zarr("output.zarr")
```

---

## Issue 7: Encoding/Dtype Differences Between Source and Target

**Symptoms:**
- Values differ slightly between source and migrated store
- Integer data becomes float after migration
- Time coordinates decoded differently
- Large precision differences in specific value ranges

**Cause:** xarray's CF decoding applies `scale_factor` and `add_offset` transformations, converting packed integer data to float. If the Zarr write doesn't re-encode with the same packing parameters, the on-disk representation changes.

**Solution:**

```python
import xarray as xr
import numpy as np

# ── Diagnose: Compare dtypes ──
ds_raw = xr.open_dataset("source.nc", decode_cf=False)
ds_decoded = xr.open_dataset("source.nc")
ds_zarr = xr.open_zarr("output.zarr")

for var in ds_raw.data_vars:
    print(f"{var}:")
    print(f"  Source (raw):     dtype={ds_raw[var].dtype}")
    print(f"  Source (decoded): dtype={ds_decoded[var].dtype}")
    print(f"  Zarr:             dtype={ds_zarr[var].dtype}")

# ── Fix 1: Preserve original packing ──
ds = xr.open_dataset("source.nc")
encoding = {}
for var in ds.data_vars:
    enc = ds[var].encoding
    encoding[var] = {
        k: v for k, v in enc.items()
        if k in ("dtype", "scale_factor", "add_offset", "_FillValue")
    }
ds.to_zarr("output.zarr", encoding=encoding)

# ── Fix 2: Skip CF decoding entirely ──
ds = xr.open_dataset("source.nc", decode_cf=False)
ds.to_zarr("output.zarr")  # exact byte-level copy

# ── Fix 3: Accept the type change and set target dtype explicitly ──
encoding = {
    "temperature": {"dtype": "float32"},  # accept decoded float
    "precipitation": {"dtype": "float32"},
}
ds.to_zarr("output.zarr", encoding=encoding)
```

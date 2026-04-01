#!/usr/bin/env python3
"""
Cloud Storage Backend Demo for Zarr
====================================

Demonstrates how to configure Zarr with different storage backends.
Creates a local Zarr store and shows how the same code pattern applies
to cloud backends by swapping the store object.

This script runs fully locally — cloud examples are shown as commented
patterns that you can enable by installing the appropriate library and
providing credentials.

Requirements:
    pip install zarr numpy
    # For cloud backends: pip install zarr[remote]
    # For obstore: pip install obstore
    # For Icechunk: pip install icechunk

Usage:
    python cloud-storage-demo.py
"""

import shutil
import tempfile
from pathlib import Path

import numpy as np
import zarr


def main():
    work_dir = Path(tempfile.mkdtemp(prefix="zarr_cloud_demo_"))
    print(f"Working directory: {work_dir}\n")

    # ── 1. Local store (baseline) ──
    print("=" * 60)
    print("1. Local Store (baseline)")
    print("=" * 60)
    local_path = work_dir / "local_data.zarr"
    root = zarr.open_group(str(local_path), mode="w")
    root.attrs["title"] = "Cloud Storage Demo Dataset"

    arr = root.create_array(
        "temperature",
        shape=(365, 180, 360),
        chunks=(30, 90, 180),
        dtype="float32",
        fill_value=np.nan,
    )
    arr[:] = np.random.default_rng(42).standard_normal((365, 180, 360)).astype("float32")
    arr.attrs["units"] = "Celsius"
    arr.attrs["long_name"] = "Daily Mean Air Temperature"

    print(f"  Store path: {local_path}")
    print(f"  Array shape: {arr.shape}")
    print(f"  Chunks: {arr.chunks}")
    print(f"  Size on disk: {sum(f.stat().st_size for f in local_path.rglob('*') if f.is_file()) / 1e6:.1f} MB")
    print()

    # ── 2. Demonstrate the backend-swap pattern ──
    print("=" * 60)
    print("2. Backend-Swap Pattern")
    print("=" * 60)
    print("  The same zarr.open_group() call works with any store:")
    print()
    print("  # Local")
    print('  root = zarr.open_group("local_data.zarr", mode="r")')
    print()
    print("  # S3 via fsspec")
    print("  from zarr.storage import FsspecStore")
    print('  store = FsspecStore.from_url("s3://bucket/data.zarr")')
    print("  root = zarr.open_group(store=store, mode='r')")
    print()
    print("  # S3 via obstore")
    print("  from obstore.store import S3Store")
    print('  obs = S3Store.from_url("s3://bucket/data.zarr")')
    print("  store = zarr.storage.ObjectStore(obs)")
    print("  root = zarr.open_group(store=store, mode='r')")
    print()

    # ── 3. Read back and verify ──
    print("=" * 60)
    print("3. Read Back and Verify")
    print("=" * 60)
    root_r = zarr.open_group(str(local_path), mode="r")
    temp = root_r["temperature"]
    subset = temp[0:30, 0:10, 0:10]
    print(f"  Title: {root_r.attrs['title']}")
    print(f"  Array info: shape={temp.shape}, dtype={temp.dtype}")
    print(f"  First month mean (10x10 region): {np.nanmean(subset):.4f}")
    print()

    # ── 4. Caching pattern ──
    print("=" * 60)
    print("4. Caching Pattern (for cloud stores)")
    print("=" * 60)
    print("  Wrap the URL with a cache protocol:")
    print()
    print("  store = FsspecStore.from_url(")
    print('      "simplecache::s3://bucket/data.zarr",')
    print("      storage_options={")
    print('          "s3": {"anon": True},')
    print('          "simplecache": {"cache_storage": "/tmp/zarr-cache"},')
    print("      },")
    print("  )")
    print()

    # ── Cleanup ──
    shutil.rmtree(work_dir)
    print(f"Cleaned up {work_dir}")
    print("Done.")


if __name__ == "__main__":
    main()

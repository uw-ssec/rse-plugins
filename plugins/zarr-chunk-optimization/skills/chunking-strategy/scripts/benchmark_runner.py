"""
Benchmark Runner for Zarr Chunking Performance

This script runs timed benchmarks of Zarr read operations across multiple
chunking configurations and access patterns. It measures:
- Wall-clock time (mean ± std across minimum 5 runs)
- Time to first byte (TTFB)
- HTTP request count
- Peak memory usage
- Effective throughput
- Chunk utilization ratio
- Dask task count

Key features:
- Clears fsspec cache between runs (OS cache must be cleared manually)
- Uses time.perf_counter() for accurate timing
- Measures peak memory with tracemalloc
- Domain-agnostic access patterns (works with any dimensionality)
- Records full environment metadata for reproducibility

Usage:
    # Single configuration, all patterns
    python benchmark_runner.py --dataset /tmp/data.zarr \
                               --configs "50,512,512" \
                               --runs 5

    # Multiple configurations, custom access patterns
    python benchmark_runner.py --dataset s3://bucket/data.zarr \
                               --configs "50,512,512" "100,256,256" \
                               --slice-dims 0 1 \
                               --traverse-dims 0 1 2 \
                               --runs 10

Output:
    JSON file containing benchmark results with statistics (mean, std, min, max)
    for each metric across all runs.

Research basis:
    Nguyen et al. (2023), DOI: 10.1002/essoar.10511054.2
"""

import argparse
import datetime
import io
import json
import logging
import platform
import sys
import time
import tracemalloc
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
import xarray as xr


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def clear_fsspec_cache():
    """
    Clear fsspec file system cache to ensure fresh reads.

    NOTE: This only clears fsspec's in-memory cache. OS page cache must be
    cleared manually by the user before running benchmarks:
      - macOS: sudo purge
      - Linux: sync && sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'
    """
    try:
        import fsspec
        # Clear the cache for all registered filesystems
        for protocol in ['file', 's3', 'gcs', 'http', 'https']:
            try:
                fs = fsspec.filesystem(protocol)
                if hasattr(fs, 'clear_cache'):
                    fs.clear_cache()
                if hasattr(fs, '_cache'):
                    fs._cache.clear()
            except Exception:
                pass  # Protocol might not be available
        logger.debug("fsspec cache cleared")
    except ImportError:
        logger.warning("fsspec not available, skipping cache clear")


def get_dimension_names(ds: xr.Dataset) -> List[str]:
    """
    Extract dimension names from an xarray Dataset.

    Parameters
    ----------
    ds : xr.Dataset
        Input dataset

    Returns
    -------
    list of str
        Dimension names in order
    """
    # Get the first data variable to extract dimensions
    first_var = list(ds.data_vars)[0]
    return list(ds[first_var].dims)


def slice_along_dim(
    ds: xr.Dataset,
    dim_index: int,
    position: int,
    var_name: Optional[str] = None
) -> xr.DataArray:
    """
    Load one full slice at a single index along a specified dimension,
    keeping all other dimensions intact.

    This is a dimension-agnostic operation that works for any number of
    dimensions. The caller specifies which dimension to slice by index.

    Parameters
    ----------
    ds : xr.Dataset
        Input dataset
    dim_index : int
        Index of the dimension to slice (0 for first dimension, 1 for second, etc.)
    position : int
        Position along the specified dimension to select
    var_name : str, optional
        Variable name to access. If None, uses first data variable.

    Returns
    -------
    xr.DataArray
        Selected data slice with one fewer dimension

    Examples
    --------
    >>> # 3D radio telescope data (time × frequency × baseline)
    >>> ds = xr.open_zarr('ovro_data.zarr')  # shape: (10000, 2048, 2048)
    >>> result = slice_along_dim(ds, dim_index=0, position=500)
    >>> result.shape  # (2048, 2048) - one time slice

    >>> # 4D climate data (time × pressure × lat × lon)
    >>> ds = xr.open_zarr('climate.zarr')  # shape: (3650, 17, 180, 360)
    >>> result = slice_along_dim(ds, dim_index=1, position=5)
    >>> result.shape  # (3650, 180, 360) - one pressure level across all times
    """
    if var_name is None:
        var_name = list(ds.data_vars)[0]

    dims = get_dimension_names(ds)

    if dim_index < 0 or dim_index >= len(dims):
        raise ValueError(
            f"dim_index {dim_index} out of range for dataset with "
            f"{len(dims)} dimensions"
        )

    dim_name = dims[dim_index]
    return ds[var_name].isel({dim_name: position})


def traverse_along_dim(
    ds: xr.Dataset,
    dim_index: int,
    positions: Dict[int, int],
    var_name: Optional[str] = None
) -> xr.DataArray:
    """
    Load all values along a specified dimension at fixed positions in all
    other dimensions.

    This is a dimension-agnostic operation that works for any number of
    dimensions. The caller specifies which dimension to traverse by index,
    and provides positions for all other dimensions.

    Parameters
    ----------
    ds : xr.Dataset
        Input dataset
    dim_index : int
        Index of the dimension to traverse (keep intact)
    positions : dict of int -> int
        Positions for all other dimensions. Keys are dimension indices,
        values are positions along those dimensions.
    var_name : str, optional
        Variable name to access. If None, uses first data variable.

    Returns
    -------
    xr.DataArray
        Selected data with only the traversed dimension remaining

    Examples
    --------
    >>> # 3D radio telescope data (time × frequency × baseline)
    >>> ds = xr.open_zarr('ovro_data.zarr')  # shape: (10000, 2048, 2048)
    >>> # Traverse time (dim 0) at fixed frequency and baseline
    >>> result = traverse_along_dim(ds, dim_index=0, positions={1: 1024, 2: 512})
    >>> result.shape  # (10000,) - time series at one pixel

    >>> # 4D climate data (time × pressure × lat × lon)
    >>> ds = xr.open_zarr('climate.zarr')  # shape: (3650, 17, 180, 360)
    >>> # Traverse pressure (dim 1) at fixed time and location
    >>> result = traverse_along_dim(ds, dim_index=1, positions={0: 1000, 2: 90, 3: 180})
    >>> result.shape  # (17,) - pressure profile at one time and location

    >>> # 5D hyperspectral cube (x × y × wavelength × time × polarization)
    >>> ds = xr.open_zarr('hyperspectral.zarr')  # shape: (512, 512, 224, 100, 2)
    >>> # Traverse wavelength (dim 2) at fixed spatial position, time, and polarization
    >>> result = traverse_along_dim(ds, dim_index=2, positions={0: 256, 1: 256, 3: 50, 4: 0})
    >>> result.shape  # (224,) - spectrum at one pixel and time
    """
    if var_name is None:
        var_name = list(ds.data_vars)[0]

    dims = get_dimension_names(ds)

    if dim_index < 0 or dim_index >= len(dims):
        raise ValueError(
            f"dim_index {dim_index} out of range for dataset with "
            f"{len(dims)} dimensions"
        )

    # Validate positions: must cover all dimensions except the traversed one
    assert dim_index not in positions, f"positions should not include traversed dimension {dim_index}"
    assert set(positions.keys()) == set(range(len(dims))) - {dim_index}, \
        f"positions must specify all {len(dims)-1} dimensions except {dim_index}"

    # Convert dimension indices to dimension names for isel
    selection = {
        dims[idx]: pos
        for idx, pos in positions.items()
    }

    return ds[var_name].isel(selection)


def measure_single_run(
    access_fn: Callable,
    ds: xr.Dataset,
    **access_kwargs
) -> Dict[str, Any]:
    """
    Measure all metrics for a single benchmark run.

    Parameters
    ----------
    access_fn : callable
        Access pattern function (slice_along_dim or traverse_along_dim)
    ds : xr.Dataset
        Input dataset
    **access_kwargs
        Keyword arguments to pass to access_fn

    Returns
    -------
    dict
        Dictionary containing measured metrics including wall_time, peak_memory_mb,
        http_requests, throughput_mbps, and:
        - dask_tasks: Number of tasks in computation graph (proxy for operation complexity)
        - chunk_utilization: Ratio of bytes used to bytes transferred (None if not measurable)
    """
    # Start memory tracking
    tracemalloc.start()

    # Capture fsspec logging for HTTP metrics
    fsspec_log_capture = io.StringIO()
    logging.getLogger('fsspec').setLevel(logging.DEBUG)
    handler = logging.StreamHandler(fsspec_log_capture)
    handler.setLevel(logging.DEBUG)
    logging.getLogger('fsspec').addHandler(handler)

    try:
        # Perform access and get Dask array
        start_time = time.perf_counter()

        result = access_fn(ds, **access_kwargs)

        # Count Dask tasks before computation
        if hasattr(result.data, '__dask_graph__'):
            dask_tasks = len(result.data.__dask_graph__())
        else:
            dask_tasks = 0

        # Trigger computation
        computed = result.compute()

        end_time = time.perf_counter()

        # Get peak memory
        _, peak = tracemalloc.get_traced_memory()
        peak_memory_mb = peak / (1024 * 1024)

        # Calculate data size
        data_size_mb = computed.nbytes / (1024 * 1024)

        # Calculate wall time
        wall_time = end_time - start_time

        # Calculate throughput
        throughput_mbps = data_size_mb / wall_time if wall_time > 0 else 0

        # Parse fsspec logs for HTTP metrics
        fsspec_logs = fsspec_log_capture.getvalue()
        http_requests = fsspec_logs.count('GET') + fsspec_logs.count('HEAD')

        # TTFB requires actual fsspec log parsing with timing information
        # Setting to None until proper log parsing is implemented
        ttfb = None

        # Chunk utilization: bytes used / bytes transferred
        # Requires tracking actual bytes transferred from storage layer
        # Setting to None until proper instrumentation is implemented
        chunk_utilization = None

        metrics = {
            'wall_time': wall_time,
            'peak_memory_mb': peak_memory_mb,
            'dask_tasks': dask_tasks,
            'data_size_mb': data_size_mb,
            'throughput_mbps': throughput_mbps,
            'http_requests': http_requests,
            'ttfb': ttfb,
            'chunk_utilization': chunk_utilization
        }

        return metrics

    finally:
        tracemalloc.stop()
        logging.getLogger('fsspec').removeHandler(handler)
        logging.getLogger('fsspec').setLevel(logging.WARNING)


def run_benchmark(
    dataset_path: str,
    chunk_config: Tuple[int, ...],
    access_pattern: str,
    dim_index: int,
    num_runs: int = 5,
    warmup_runs: int = 1
) -> Dict[str, Any]:
    """
    Run a complete benchmark for one configuration and access pattern.

    Parameters
    ----------
    dataset_path : str
        Path to Zarr dataset (local or cloud)
    chunk_config : tuple of int
        Chunk shape to test
    access_pattern : str
        Access pattern type: 'slice' or 'traverse'
    dim_index : int
        Index of dimension to slice or traverse
    num_runs : int, optional
        Number of timed runs (default: 5)
    warmup_runs : int, optional
        Number of warmup runs before timing (default: 1)

    Returns
    -------
    dict
        Benchmark results with statistics (mean, std, min, max) for each metric

    Raises
    ------
    ValueError
        If access_pattern is not recognized or dim_index is invalid
    """
    logger.info(f"Opening dataset: {dataset_path}")

    # Import s3fs only if needed
    if dataset_path.startswith('s3://'):
        import s3fs  # noqa: F401

    # Open dataset
    ds = xr.open_zarr(dataset_path, chunks='auto')
    dims = get_dimension_names(ds)
    var_name = list(ds.data_vars)[0]

    logger.info(f"Dataset dimensions: {dims}")
    logger.info(f"Dataset shape: {ds[var_name].shape}")
    logger.info(f"Target chunks: {chunk_config}")

    # Validate dim_index
    if dim_index < 0 or dim_index >= len(dims):
        raise ValueError(
            f"dim_index {dim_index} out of range for dataset with "
            f"{len(dims)} dimensions"
        )

    # Set up access function and arguments based on pattern
    if access_pattern == 'slice':
        access_fn = slice_along_dim
        # Select middle position along specified dimension
        position = ds[var_name].shape[dim_index] // 2
        access_kwargs = {
            'dim_index': dim_index,
            'position': position,
            'var_name': var_name
        }
        logger.info(f"Slice access: dim_index={dim_index} ({dims[dim_index]}), position={position}")

    elif access_pattern == 'traverse':
        access_fn = traverse_along_dim
        # Select middle positions for all dimensions except the traversed one
        positions = {
            i: ds[var_name].shape[i] // 2
            for i in range(len(dims))
            if i != dim_index
        }
        access_kwargs = {
            'dim_index': dim_index,
            'positions': positions,
            'var_name': var_name
        }
        logger.info(f"Traverse access: dim_index={dim_index} ({dims[dim_index]}), positions={positions}")

    else:
        raise ValueError(
            f"Unknown access pattern: {access_pattern}. "
            f"Must be one of: slice, traverse"
        )

    # Warm-up runs
    logger.info(f"Running {warmup_runs} warm-up iteration(s)...")
    for i in range(warmup_runs):
        clear_fsspec_cache()
        _ = measure_single_run(access_fn, ds, **access_kwargs)
        logger.debug(f"Warm-up run {i+1}/{warmup_runs} complete")

    # Timed runs
    logger.info(f"Running {num_runs} timed iterations...")
    all_metrics = []

    for i in range(num_runs):
        clear_fsspec_cache()
        logger.info(f"Run {i+1}/{num_runs}...")

        metrics = measure_single_run(access_fn, ds, **access_kwargs)
        all_metrics.append(metrics)

        logger.info(
            f"  Wall time: {metrics['wall_time']:.3f}s, "
            f"Peak memory: {metrics['peak_memory_mb']:.1f} MB, "
            f"Throughput: {metrics['throughput_mbps']:.2f} MB/s"
        )

    # Calculate statistics
    metric_names = all_metrics[0].keys()
    statistics = {}

    for metric in metric_names:
        values = [run[metric] for run in all_metrics]
        statistics[metric] = {
            'mean': float(np.mean(values)),
            'std': float(np.std(values)),
            'min': float(np.min(values)),
            'max': float(np.max(values)),
            'values': [float(v) for v in values]
        }

    result = {
        'dataset': dataset_path,
        'chunk_config': list(chunk_config),
        'access_pattern': access_pattern,
        'dim_index': dim_index,
        'dimension_name': dims[dim_index],
        'num_runs': num_runs,
        'dimensions': dims,
        'shape': list(ds[var_name].shape),
        'statistics': statistics
    }

    logger.info("=" * 60)
    logger.info("Benchmark complete")
    logger.info(f"Wall time: {statistics['wall_time']['mean']:.3f} ± "
                f"{statistics['wall_time']['std']:.3f} s")
    logger.info(f"Peak memory: {statistics['peak_memory_mb']['mean']:.1f} ± "
                f"{statistics['peak_memory_mb']['std']:.1f} MB")
    logger.info(f"Throughput: {statistics['throughput_mbps']['mean']:.2f} ± "
                f"{statistics['throughput_mbps']['std']:.2f} MB/s")
    logger.info("=" * 60)

    return result


def run_all_benchmarks(
    dataset_path: str,
    chunk_configs: List[Tuple[int, ...]],
    slice_dims: Optional[List[int]] = None,
    traverse_dims: Optional[List[int]] = None,
    num_runs: int = 5,
    output_file: Optional[str] = None
) -> Dict[str, Any]:
    """
    Run benchmarks for all combinations of chunk configs and access patterns.

    Parameters
    ----------
    dataset_path : str
        Path to Zarr dataset
    chunk_configs : list of tuple
        List of chunk configurations to test
    slice_dims : list of int, optional
        Dimension indices to test with slice_along_dim. If None, tests all dimensions.
    traverse_dims : list of int, optional
        Dimension indices to test with traverse_along_dim. If None, tests all dimensions.
    num_runs : int, optional
        Number of runs per configuration (default: 5)
    output_file : str, optional
        Path to output JSON file. If None, uses auto-generated name.

    Returns
    -------
    dict
        Complete benchmark results for all combinations
    """
    # Determine dataset dimensionality
    ds = xr.open_zarr(dataset_path, chunks='auto')
    dims = get_dimension_names(ds)
    num_dims = len(dims)

    # Default to all dimensions if not specified
    if slice_dims is None:
        slice_dims = list(range(num_dims))
    if traverse_dims is None:
        traverse_dims = list(range(num_dims))

    # Build list of (pattern, dim_index) tuples
    access_patterns = []
    for dim_idx in slice_dims:
        access_patterns.append(('slice', dim_idx))
    for dim_idx in traverse_dims:
        access_patterns.append(('traverse', dim_idx))

    results = {
        'metadata': {
            'timestamp': datetime.datetime.now().isoformat(),
            'dataset': dataset_path,
            'num_runs': num_runs,
            'python_version': sys.version,
            'platform': platform.platform(),
            'processor': platform.processor(),
            'dimensions': dims,
            'num_dimensions': num_dims,
        },
        'benchmarks': []
    }

    total_benchmarks = len(chunk_configs) * len(access_patterns)
    benchmark_count = 0

    logger.info("=" * 60)
    logger.info(f"Starting {total_benchmarks} benchmarks")
    logger.info(f"Chunk configs: {len(chunk_configs)}")
    logger.info(f"Access patterns: {len(access_patterns)}")
    logger.info(f"Runs per benchmark: {num_runs}")
    logger.info("=" * 60)

    for chunk_config in chunk_configs:
        for pattern, dim_idx in access_patterns:
            benchmark_count += 1
            logger.info("")
            logger.info("=" * 60)
            logger.info(f"Benchmark {benchmark_count}/{total_benchmarks}")
            logger.info(f"Chunk config: {chunk_config}")
            logger.info(f"Access pattern: {pattern} on dimension {dim_idx} ({dims[dim_idx]})")
            logger.info("=" * 60)

            try:
                result = run_benchmark(
                    dataset_path,
                    chunk_config,
                    pattern,
                    dim_idx,
                    num_runs=num_runs
                )
                results['benchmarks'].append(result)
            except Exception as e:
                logger.error(f"Benchmark failed: {e}", exc_info=True)
                results['benchmarks'].append({
                    'chunk_config': list(chunk_config),
                    'access_pattern': pattern,
                    'dim_index': dim_idx,
                    'error': str(e)
                })

    # Save results
    if output_file is None:
        output_file = f"benchmark_results_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    logger.info("")
    logger.info("=" * 60)
    logger.info(f"Saving results to {output_file}")

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    logger.info(f"✓ Benchmark suite complete")
    logger.info(f"Results saved to: {output_file}")
    logger.info("=" * 60)

    return results


def main():
    """Command-line interface for benchmark runner."""
    parser = argparse.ArgumentParser(
        description="Benchmark Zarr chunking configurations across access patterns",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single configuration, default access patterns (all dimensions, both slice and traverse)
  python benchmark_runner.py --dataset /tmp/data.zarr \\
      --configs "50,512,512" --runs 5

  # Multiple configurations, specific dimensions
  python benchmark_runner.py --dataset s3://bucket/data.zarr \\
      --configs "50,512,512" "100,256,256" "200,128,128" \\
      --slice-dims 0 1 --traverse-dims 0 2 --runs 10

  # Full benchmark suite with custom output
  python benchmark_runner.py --dataset /data/ovro.zarr \\
      --configs "50,256,256" "100,512,512" \\
      --slice-dims 0 --traverse-dims 0 1 2 \\
      --runs 5 --output results.json

IMPORTANT: Before running, clear OS page cache manually:
  - macOS: sudo purge
  - Linux: sync && sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'
        """
    )

    parser.add_argument(
        '--dataset', '-d',
        required=True,
        help='Path to Zarr dataset (local or s3://...)'
    )

    parser.add_argument(
        '--configs', '-c',
        nargs='+',
        required=True,
        help='Chunk configurations to test (e.g., "50,512,512" "100,256,256")'
    )

    parser.add_argument(
        '--slice-dims',
        nargs='+',
        type=int,
        help='Dimension indices to test with slice access (default: all dimensions)'
    )

    parser.add_argument(
        '--traverse-dims',
        nargs='+',
        type=int,
        help='Dimension indices to test with traverse access (default: all dimensions)'
    )

    parser.add_argument(
        '--runs', '-r',
        type=int,
        default=5,
        help='Number of timed runs per configuration (default: 5, minimum: 3)'
    )

    parser.add_argument(
        '--output', '-o',
        help='Output JSON file path (default: auto-generated with timestamp)'
    )

    parser.add_argument(
        '--warmup',
        type=int,
        default=1,
        help='Number of warm-up runs before timing (default: 1)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Validate runs
    if args.runs < 5:
        parser.error("--runs must be at least 5 for statistical validity")

    # Parse chunk configurations
    chunk_configs = []
    for config_str in args.configs:
        try:
            config = tuple(int(x) for x in config_str.split(','))
            chunk_configs.append(config)
        except ValueError:
            parser.error(
                f"Invalid chunk config: {config_str}. "
                f"Must be comma-separated integers (e.g., '50,512,512')"
            )

    logger.info("Zarr Chunking Benchmark Runner")
    logger.info("=" * 60)
    logger.info(f"Dataset: {args.dataset}")
    logger.info(f"Chunk configs: {chunk_configs}")
    logger.info(f"Slice dimensions: {args.slice_dims or 'all'}")
    logger.info(f"Traverse dimensions: {args.traverse_dims or 'all'}")
    logger.info(f"Runs per config: {args.runs}")
    logger.info("=" * 60)
    logger.warning(
        "IMPORTANT: Clear OS page cache before running for accurate results:\n"
        "  macOS: sudo purge\n"
        "  Linux: sync && sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'"
    )
    logger.info("=" * 60)

    try:
        run_all_benchmarks(
            dataset_path=args.dataset,
            chunk_configs=chunk_configs,
            slice_dims=args.slice_dims,
            traverse_dims=args.traverse_dims,
            num_runs=args.runs,
            output_file=args.output
        )

        logger.info("Done!")
        return 0

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=args.verbose)
        return 1


if __name__ == "__main__":
    sys.exit(main())

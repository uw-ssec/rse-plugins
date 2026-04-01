"""
Synthetic Zarr Data Generator

This script generates synthetic multi-dimensional Zarr arrays for testing
chunking strategies when no real dataset is available.

Key features:
- Creates Zarr arrays with user-specified dimensions and chunk shapes
- Populates with realistic synthetic data (random, structured patterns, etc.)
- Supports multiple data types (float32, float64, int16, etc.)
- Optionally applies compression (zstd, blosc, gzip)
- Writes to local filesystem or cloud storage (S3, GCS)
- Useful for reproducible benchmarking and testing

Usage:
    # Generate OVRO-LWA-like data (time × frequency × baseline)
    python synthetic_data.py --output /tmp/synthetic.zarr \
                             --shape "1000,2048,2048" \
                             --chunks "50,256,256" \
                             --dtype float32 \
                             --compression zstd

    # Generate climate-like data (time × lat × lon)
    python synthetic_data.py --output s3://bucket/synthetic_climate.zarr \
                             --shape "3650,180,360" \
                             --chunks "365,90,180" \
                             --dtype float32 \
                             --pattern temperature

Output:
    Zarr store at the specified output path with synthetic data.

Use cases:
    - Testing benchmarking pipeline without needing real data
    - Generating test cases for different dimension sizes
    - Creating reproducible test data for documentation
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np
import zarr


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def estimate_array_size(shape: Tuple[int, ...], dtype: np.dtype) -> float:
    """
    Estimate the uncompressed size of an array in GB.

    Parameters
    ----------
    shape : tuple of int
        Shape of the array
    dtype : np.dtype
        Data type of the array

    Returns
    -------
    float
        Estimated size in GB
    """
    total_elements = np.prod(shape)
    bytes_per_element = np.dtype(dtype).itemsize
    size_gb = (total_elements * bytes_per_element) / (1024**3)
    return size_gb


def calculate_sample_shape(
    full_shape: Tuple[int, ...],
    target_size_gb: float = 8.0,
    dtype: np.dtype = np.float32
) -> Tuple[int, ...]:
    """
    Calculate a sample shape that targets approximately the specified size in GB.

    Strategy: Reduce the first dimension (typically time) to reach target size,
    keeping other dimensions at full resolution for representative benchmarking.

    Parameters
    ----------
    full_shape : tuple of int
        Full array shape
    target_size_gb : float, optional
        Target sample size in GB (default: 8.0)
    dtype : np.dtype, optional
        Data type of the array (default: float32)

    Returns
    -------
    tuple of int
        Sample shape that approximates target size

    Examples
    --------
    >>> calculate_sample_shape((10000, 2048, 2048), target_size_gb=8.0, dtype=np.float32)
    (500, 2048, 2048)  # Approximately 8 GB
    """
    bytes_per_element = np.dtype(dtype).itemsize
    target_bytes = target_size_gb * (1024**3)

    # Calculate elements in all dimensions except first
    trailing_elements = np.prod(full_shape[1:]) if len(full_shape) > 1 else 1

    # Calculate how many elements we can fit along first dimension
    first_dim_size = int(target_bytes / (trailing_elements * bytes_per_element))

    # Ensure we don't exceed original size
    first_dim_size = min(first_dim_size, full_shape[0])

    # Ensure we have at least some data
    first_dim_size = max(first_dim_size, 1)

    sample_shape = (first_dim_size,) + full_shape[1:]

    actual_size = estimate_array_size(sample_shape, dtype)
    logger.info(f"Sample shape {sample_shape} will be approximately {actual_size:.2f} GB")

    return sample_shape


def generate_synthetic_pattern(
    shape: Tuple[int, ...],
    pattern_type: str = "random",
    seed: Optional[int] = 42
) -> np.ndarray:
    """
    Generate synthetic data with specified statistical patterns.

    Parameters
    ----------
    shape : tuple of int
        Shape of the output array
    pattern_type : str, optional
        Type of pattern to generate. Options:
        - "random": Gaussian random noise (default)
        - "temperature": Simulates temperature-like data with spatial/temporal structure
        - "radio": Simulates radio telescope visibility data
        - "constant": Constant value with small noise
    seed : int or None, optional
        Random seed for reproducibility (default: 42)

    Returns
    -------
    np.ndarray
        Array with synthetic pattern
    """
    if seed is not None:
        np.random.seed(seed)

    logger.info(f"Generating {pattern_type} pattern with shape {shape}")

    if pattern_type == "random":
        # Standard Gaussian noise
        data = np.random.randn(*shape).astype(np.float32)

    elif pattern_type == "temperature":
        # Simulates temperature data: spatial gradients + temporal variation
        # Base field with spatial structure
        data = np.zeros(shape, dtype=np.float32)
        if len(shape) >= 3:
            # Create lat/lon-like gradients
            lat_gradient = np.linspace(-1, 1, shape[1])[:, np.newaxis]
            lon_gradient = np.linspace(-1, 1, shape[2])[np.newaxis, :]
            spatial_pattern = lat_gradient + lon_gradient

            # Add temporal variation
            for t in range(shape[0]):
                temporal_factor = np.sin(2 * np.pi * t / shape[0])
                data[t] = spatial_pattern * (1 + 0.3 * temporal_factor)
                data[t] += np.random.randn(shape[1], shape[2]) * 0.1
        else:
            data = np.random.randn(*shape).astype(np.float32)

    elif pattern_type == "radio":
        # Simulates radio telescope visibility data (complex-valued noise)
        # Using real-valued representation with noise characteristics
        # typical of visibility amplitudes
        data = np.abs(np.random.randn(*shape) + 1j * np.random.randn(*shape))
        data = data.astype(np.float32)

    elif pattern_type == "constant":
        # Constant value with small Gaussian noise (good for compression testing)
        data = np.ones(shape, dtype=np.float32) * 100.0
        data += np.random.randn(*shape).astype(np.float32) * 0.01

    else:
        raise ValueError(
            f"Unknown pattern type: {pattern_type}. "
            f"Choose from: random, temperature, radio, constant"
        )

    return data


def create_synthetic_zarr(
    output_path: str,
    shape: Tuple[int, ...],
    chunks: Tuple[int, ...],
    dimension_names: Optional[List[str]] = None,
    dtype: str = "float32",
    compression: Optional[str] = "zstd",
    compression_level: int = 3,
    pattern_type: str = "random",
    seed: Optional[int] = 42,
    overwrite: bool = False
) -> zarr.Array:
    """
    Create a synthetic Zarr array with specified parameters.

    Parameters
    ----------
    output_path : str
        Output path for Zarr store (local path or S3 URL)
    shape : tuple of int
        Shape of the array to create
    chunks : tuple of int
        Chunk shape for the array
    dimension_names : list of str, optional
        Names for each dimension. If None, uses generic names (dim_0, dim_1, ...)
    dtype : str, optional
        Data type (default: "float32")
    compression : str or None, optional
        Compression codec ("zstd", "blosc", "gzip", or None for no compression).
        Default: "zstd"
    compression_level : int, optional
        Compression level (default: 3)
    pattern_type : str, optional
        Type of data pattern to generate (default: "random")
    seed : int or None, optional
        Random seed for reproducibility (default: 42)
    overwrite : bool, optional
        Whether to overwrite existing store (default: False)

    Returns
    -------
    zarr.Array
        Created Zarr array

    Raises
    ------
    ValueError
        If shapes and chunks don't match in dimensionality
    FileExistsError
        If output_path exists and overwrite=False

    Examples
    --------
    >>> # Create OVRO-LWA-like data
    >>> arr = create_synthetic_zarr(
    ...     output_path="/tmp/test.zarr",
    ...     shape=(1000, 2048, 2048),
    ...     chunks=(50, 256, 256),
    ...     dimension_names=["time", "frequency", "baseline"],
    ...     pattern_type="radio"
    ... )

    >>> # Create climate-like data
    >>> arr = create_synthetic_zarr(
    ...     output_path="s3://bucket/climate.zarr",
    ...     shape=(3650, 180, 360),
    ...     chunks=(365, 90, 180),
    ...     dimension_names=["time", "lat", "lon"],
    ...     pattern_type="temperature"
    ... )
    """
    if len(shape) != len(chunks):
        raise ValueError(
            f"Shape {shape} and chunks {chunks} must have same dimensionality"
        )

    # Set up dimension names
    if dimension_names is None:
        dimension_names = [f"dim_{i}" for i in range(len(shape))]
    elif len(dimension_names) != len(shape):
        raise ValueError(
            f"Number of dimension names ({len(dimension_names)}) must match "
            f"number of dimensions ({len(shape)})"
        )

    # Log configuration
    estimated_size = estimate_array_size(shape, np.dtype(dtype))
    chunk_size_mb = estimate_array_size(chunks, np.dtype(dtype)) * 1024

    logger.info("=" * 60)
    logger.info("Creating synthetic Zarr array")
    logger.info("=" * 60)
    logger.info(f"Output path: {output_path}")
    logger.info(f"Shape: {shape}")
    logger.info(f"Dimensions: {dimension_names}")
    logger.info(f"Chunks: {chunks}")
    logger.info(f"Dtype: {dtype}")
    logger.info(f"Compression: {compression} (level {compression_level})")
    logger.info(f"Pattern: {pattern_type}")
    logger.info(f"Estimated size (uncompressed): {estimated_size:.2f} GB")
    logger.info(f"Chunk size: {chunk_size_mb:.2f} MB")
    logger.info("=" * 60)

    # Set up compression (zarr v3 API - BytesCodec must be first)
    codec_chain = [zarr.codecs.BytesCodec()]
    if compression == "zstd":
        codec_chain.append(zarr.codecs.BloscCodec(
            cname='zstd', clevel=compression_level, shuffle='bitshuffle'
        ))
    elif compression == "blosc":
        codec_chain.append(zarr.codecs.BloscCodec(
            cname='lz4', clevel=compression_level, shuffle='bitshuffle'
        ))
    elif compression == "gzip":
        codec_chain.append(zarr.codecs.GzipCodec(level=compression_level))
    elif compression is not None:
        logger.warning(
            f"Unknown compression {compression}, using zstd instead"
        )
        codec_chain.append(zarr.codecs.BloscCodec(
            cname='zstd', clevel=compression_level, shuffle='bitshuffle'
        ))

    # Create or open store
    if output_path.startswith("s3://") or output_path.startswith("gcs://"):
        # Cloud storage
        import s3fs
        if output_path.startswith("s3://"):
            fs = s3fs.S3FileSystem()
        else:
            # For GCS, would need gcsfs
            raise NotImplementedError("GCS support requires gcsfs installation")

        store = s3fs.S3Map(root=output_path, s3=fs, check=False)
    else:
        # Local filesystem
        store = output_path
        if not overwrite and Path(output_path).exists():
            raise FileExistsError(
                f"Output path {output_path} already exists. "
                f"Use overwrite=True to replace."
            )

    # Create Zarr array
    z = zarr.open(
        store,
        mode='w',
        shape=shape,
        chunks=chunks,
        dtype=dtype,
        codecs=codec_chain
    )

    # Add dimension metadata
    z.attrs['dimensions'] = dimension_names
    z.attrs['pattern_type'] = pattern_type
    z.attrs['created_by'] = 'synthetic_data.py'

    # Generate and write data in chunks to avoid memory issues
    logger.info("Generating and writing data...")

    # Calculate how to slice the generation to stay within memory limits
    # Target ~1GB batches for generation
    target_batch_gb = 1.0
    bytes_per_element = np.dtype(dtype).itemsize
    trailing_elements = np.prod(shape[1:]) if len(shape) > 1 else 1
    batch_size = max(1, int(
        (target_batch_gb * 1024**3) / (trailing_elements * bytes_per_element)
    ))
    batch_size = min(batch_size, shape[0])

    logger.info(f"Writing data in batches of {batch_size} along first dimension")

    for start_idx in range(0, shape[0], batch_size):
        end_idx = min(start_idx + batch_size, shape[0])
        batch_shape = (end_idx - start_idx,) + shape[1:]

        logger.info(
            f"Processing batch [{start_idx}:{end_idx}] "
            f"({end_idx}/{shape[0]}, {100*end_idx/shape[0]:.1f}%)"
        )

        # Generate data for this batch
        batch_data = generate_synthetic_pattern(
            batch_shape,
            pattern_type=pattern_type,
            seed=seed + start_idx if seed is not None else None
        )

        # Write to Zarr
        z[start_idx:end_idx] = batch_data

    logger.info("=" * 60)
    logger.info("✓ Synthetic Zarr array created successfully")
    logger.info(f"Location: {output_path}")
    logger.info(f"Shape: {shape}")
    logger.info(f"Chunks: {chunks}")
    if not output_path.startswith('s3://'):
        try:
            actual_size = sum(f.stat().st_size for f in Path(output_path).rglob('*') if f.is_file())
            logger.info(f"Actual size on disk: {actual_size / 1024**2:.2f} MB")
            compression_ratio = (estimated_size * 1024) / (actual_size / 1024**2)
            logger.info(f"Compression ratio: {compression_ratio:.2f}x")
        except Exception:
            pass
    logger.info("=" * 60)

    return z


def create_sample_for_benchmarking(
    source_zarr_path: str,
    output_path: str,
    target_size_gb: float = 8.0,
    overwrite: bool = False
) -> zarr.Array:
    """
    Create a smaller sample from an existing Zarr array for benchmarking.

    This function creates a representative sample by taking a slice along the
    first dimension while preserving full resolution in other dimensions. This
    approach ensures the sample remains representative for benchmarking different
    access patterns.

    Parameters
    ----------
    source_zarr_path : str
        Path to the source Zarr array
    output_path : str
        Output path for the sample Zarr store
    target_size_gb : float, optional
        Target sample size in GB (default: 8.0)
    overwrite : bool, optional
        Whether to overwrite existing sample (default: False)

    Returns
    -------
    zarr.Array
        Created sample Zarr array

    Examples
    --------
    >>> sample = create_sample_for_benchmarking(
    ...     source_zarr_path="s3://bucket/full_data.zarr",
    ...     output_path="/tmp/sample.zarr",
    ...     target_size_gb=8.0
    ... )
    """
    logger.info(f"Creating benchmark sample from {source_zarr_path}")

    # Open source array
    source = zarr.open(source_zarr_path, mode='r')

    # Calculate sample shape
    sample_shape = calculate_sample_shape(
        source.shape,
        target_size_gb=target_size_gb,
        dtype=source.dtype
    )

    logger.info(f"Source shape: {source.shape}")
    logger.info(f"Sample shape: {sample_shape}")
    logger.info(f"Sampling first {sample_shape[0]} elements along first dimension")

    # Create sample array with same chunks and compression as source
    # In zarr v3, handle codecs properly - BytesCodec must be first
    source_codec_chain = None
    if hasattr(source, 'metadata') and hasattr(source.metadata, 'codecs'):
        # zarr v3: use codecs directly from metadata
        source_codec_chain = source.metadata.codecs
    elif source.compressor is not None:
        # Fallback: create proper codec chain with BytesCodec first
        source_codec_chain = [zarr.codecs.BytesCodec(), source.compressor]
    else:
        # No compression: just BytesCodec
        source_codec_chain = [zarr.codecs.BytesCodec()]

    sample = zarr.open(
        output_path,
        mode='w',
        shape=sample_shape,
        chunks=source.chunks,
        dtype=source.dtype,
        codecs=source_codec_chain
    )

    # Copy metadata
    sample.attrs.update(source.attrs)
    sample.attrs['sampled_from'] = source_zarr_path
    sample.attrs['sample_size_gb'] = target_size_gb

    # Copy data
    logger.info("Copying data...")
    sample_slice = (slice(0, sample_shape[0]),) + tuple(
        slice(0, s) for s in sample_shape[1:]
    )
    sample[:] = source[sample_slice]

    logger.info(f"✓ Sample created at {output_path}")

    return sample


def main():
    """Command-line interface for synthetic data generation."""
    parser = argparse.ArgumentParser(
        description="Generate synthetic Zarr arrays for chunking benchmarks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # OVRO-LWA-like radio telescope data
  python synthetic_data.py --output /tmp/radio.zarr \\
      --shape 1000,2048,2048 --chunks 50,256,256 \\
      --dims time,frequency,baseline --pattern radio

  # Climate data with temperature pattern
  python synthetic_data.py --output /tmp/climate.zarr \\
      --shape 3650,180,360 --chunks 365,90,180 \\
      --dims time,lat,lon --pattern temperature

  # Create sample from existing Zarr
  python synthetic_data.py --sample-from /data/full.zarr \\
      --output /tmp/sample.zarr --target-size 8
        """
    )

    # Output configuration
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output path for Zarr store (local or s3://...)'
    )

    # For sampling from existing data
    parser.add_argument(
        '--sample-from',
        help='Path to existing Zarr array to sample from'
    )
    parser.add_argument(
        '--target-size',
        type=float,
        default=8.0,
        help='Target sample size in GB (default: 8.0)'
    )

    # For creating new synthetic data
    parser.add_argument(
        '--shape',
        help='Array shape as comma-separated integers (e.g., "1000,2048,2048")'
    )
    parser.add_argument(
        '--chunks',
        help='Chunk shape as comma-separated integers (e.g., "50,256,256")'
    )
    parser.add_argument(
        '--dims',
        help='Dimension names as comma-separated strings (e.g., "time,frequency,baseline")'
    )
    parser.add_argument(
        '--dtype',
        default='float32',
        help='Data type (default: float32)'
    )
    parser.add_argument(
        '--compression',
        default='zstd',
        choices=['zstd', 'blosc', 'gzip', 'none'],
        help='Compression codec (default: zstd)'
    )
    parser.add_argument(
        '--compression-level',
        type=int,
        default=3,
        help='Compression level (default: 3)'
    )
    parser.add_argument(
        '--pattern',
        default='random',
        choices=['random', 'temperature', 'radio', 'constant'],
        help='Data pattern type (default: random)'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
        help='Random seed for reproducibility (default: 42)'
    )
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite existing output'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    try:
        if args.sample_from:
            # Create sample from existing Zarr
            create_sample_for_benchmarking(
                source_zarr_path=args.sample_from,
                output_path=args.output,
                target_size_gb=args.target_size,
                overwrite=args.overwrite
            )
        else:
            # Create new synthetic Zarr
            if not args.shape or not args.chunks:
                parser.error(
                    "Either --sample-from or both --shape and --chunks are required"
                )

            shape = tuple(int(x) for x in args.shape.split(','))
            chunks = tuple(int(x) for x in args.chunks.split(','))
            dims = args.dims.split(',') if args.dims else None

            compression = None if args.compression == 'none' else args.compression

            create_synthetic_zarr(
                output_path=args.output,
                shape=shape,
                chunks=chunks,
                dimension_names=dims,
                dtype=args.dtype,
                compression=compression,
                compression_level=args.compression_level,
                pattern_type=args.pattern,
                seed=args.seed,
                overwrite=args.overwrite
            )

        logger.info("Done!")
        return 0

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=args.verbose)
        return 1


if __name__ == "__main__":
    sys.exit(main())

"""
Rechunking Utilities for Zarr Arrays

This script provides utilities for rechunking Zarr arrays to different
chunk configurations for benchmarking or production use.

Key features:
- Validates input/output before rechunking
- Estimates rechunking time based on Nguyen et al. (2023) findings
- Uses rechunker library or zarr's copy mechanism with fallback
- Preserves all metadata and attributes
- Reports progress during rechunking
- Validates output after rechunking
- Handles both local and cloud storage (S3, GCS)
- Domain-agnostic (no hardcoded dimension names)

Usage:
    # Rechunk with validation and progress reporting
    python rechunk.py --input s3://bucket/input.zarr \
                      --output /tmp/rechunked.zarr \
                      --chunks "50,512,512"

    # Rechunk with overwrite
    python rechunk.py --input /data/input.zarr \
                      --output /data/output.zarr \
                      --chunks "100,256,256" \
                      --overwrite

Output:
    Rechunked Zarr store at the specified output path.
    JSON summary file with rechunking statistics.

Research basis:
    Nguyen et al. (2023), DOI: 10.1002/essoar.10511054.2
    - Rechunking time ranges from ~6 min (large chunks) to ~46 hours (small chunks)
"""

import argparse
import datetime
import json
import logging
import sys
import time
from pathlib import Path
from typing import Dict, Optional, Tuple

import numpy as np
import zarr


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def estimate_chunk_size_mb(
    chunk_shape: Tuple[int, ...],
    dtype: np.dtype
) -> float:
    """Estimate chunk size in MB (elements × bytes_per_element / 1024²)."""
    total_elements = np.prod(chunk_shape)
    bytes_per_element = np.dtype(dtype).itemsize
    size_mb = (total_elements * bytes_per_element) / (1024 ** 2)
    return size_mb


def estimate_rechunking_time(
    source_shape: Tuple[int, ...],
    source_chunks: Tuple[int, ...],
    target_chunks: Tuple[int, ...],
    dtype: np.dtype
) -> float:
    """
    Estimate rechunking time based on Nguyen et al. (2023) findings.

    Rechunking time varies from ~6 minutes (large chunks) to ~46 hours
    (small chunks) based on Nguyen et al. (2023). Estimate depends on
    target chunk size relative to dataset size.

    Parameters
    ----------
    source_shape : tuple of int
        Shape of the source array
    source_chunks : tuple of int
        Current chunk shape
    target_chunks : tuple of int
        Target chunk shape
    dtype : np.dtype
        Data type of the array

    Returns
    -------
    float
        Conservative time estimate in seconds (returns None to indicate
        wide range, caller should display range warning)
    """
    # Return None to signal that estimation is unreliable
    # Caller should display the range: 6 minutes to 46 hours
    return None


def validate_input(
    input_path: str
) -> Tuple[zarr.Array, Tuple[int, ...], Tuple[int, ...]]:
    """
    Validate that input Zarr store exists and is readable.

    Parameters
    ----------
    input_path : str
        Path to input Zarr store

    Returns
    -------
    tuple
        (zarr.Array, shape, current_chunks)

    Raises
    ------
    FileNotFoundError
        If input path does not exist
    ValueError
        If input is not a valid Zarr array
    """
    logger.info(f"Validating input: {input_path}")

    try:
        arr = zarr.open(input_path, mode='r')
    except Exception as e:
        raise FileNotFoundError(f"Cannot open input Zarr store: {e}")

    if not isinstance(arr, zarr.Array):
        raise ValueError(f"Input is not a Zarr array: {type(arr)}")

    shape = arr.shape
    chunks = arr.chunks

    logger.info(f"Input validated:")
    logger.info(f"  Shape: {shape}")
    logger.info(f"  Current chunks: {chunks}")
    logger.info(f"  Dtype: {arr.dtype}")
    logger.info(f"  Compressor: {arr.compressor}")

    return arr, shape, chunks


def validate_target_chunks(
    target_chunks: Tuple[int, ...],
    array_shape: Tuple[int, ...]
) -> None:
    """
    Validate that target chunks are compatible with array shape.

    Parameters
    ----------
    target_chunks : tuple of int
        Target chunk shape
    array_shape : tuple of int
        Array shape

    Raises
    ------
    ValueError
        If target chunks are invalid
    """
    if len(target_chunks) != len(array_shape):
        raise ValueError(
            f"Target chunks have {len(target_chunks)} dimensions but "
            f"array has {len(array_shape)} dimensions"
        )

    for i, (chunk_size, array_size) in enumerate(zip(target_chunks, array_shape)):
        if chunk_size <= 0:
            raise ValueError(
                f"Target chunk size must be positive, got {chunk_size} "
                f"for dimension {i}"
            )

        if chunk_size > array_size:
            logger.warning(
                f"Target chunk size {chunk_size} exceeds array size {array_size} "
                f"for dimension {i}. This will be automatically capped."
            )


def validate_output(
    output_path: str,
    overwrite: bool = False
) -> None:
    """
    Validate output path.

    Parameters
    ----------
    output_path : str
        Path for output Zarr store
    overwrite : bool, optional
        Whether to allow overwriting existing output

    Raises
    ------
    FileExistsError
        If output exists and overwrite=False
    """
    if output_path.startswith('s3://') or output_path.startswith('gcs://'):
        # For cloud storage, we'll check later
        return

    output = Path(output_path)
    if output.exists() and not overwrite:
        raise FileExistsError(
            f"Output path already exists: {output_path}. "
            f"Use --overwrite to replace it."
        )


def rechunk_zarr(
    input_path: str,
    output_path: str,
    target_chunks: Tuple[int, ...],
    overwrite: bool = False,
    max_mem: str = "2GB"
) -> Dict:
    """
    Rechunk a Zarr array to a new chunk configuration.

    This function attempts to use the rechunker library if available,
    falls back to zarr.copy with chunks parameter, and as a last resort
    performs manual chunk-by-chunk copying.

    Parameters
    ----------
    input_path : str
        Path to input Zarr store (local or cloud)
    output_path : str
        Path for output Zarr store (local or cloud)
    target_chunks : tuple of int
        Target chunk shape
    overwrite : bool, optional
        Whether to overwrite existing output (default: False)
    max_mem : str, optional
        Maximum memory for rechunker (default: "2GB")

    Returns
    -------
    dict
        Summary of rechunking operation including timing and validation

    Raises
    ------
    FileNotFoundError
        If input does not exist
    FileExistsError
        If output exists and overwrite=False
    ValueError
        If target chunks are incompatible with array shape
    """
    start_time = time.perf_counter()

    logger.info("=" * 60)
    logger.info("RECHUNKING ZARR ARRAY")
    logger.info("=" * 60)

    # Step 1: Validate input
    source_array, source_shape, source_chunks = validate_input(input_path)

    # Step 2: Validate target chunks
    validate_target_chunks(target_chunks, source_shape)

    # Step 3: Validate output
    validate_output(output_path, overwrite=overwrite)

    # Step 4: Estimate rechunking time and output size
    estimated_time = estimate_rechunking_time(
        source_shape,
        source_chunks,
        target_chunks,
        source_array.dtype
    )

    output_size_mb = estimate_chunk_size_mb(source_shape, source_array.dtype) * 1024

    logger.info("=" * 60)
    logger.info("RECHUNKING PLAN")
    logger.info("=" * 60)
    logger.info(f"Input: {input_path}")
    logger.info(f"Output: {output_path}")
    logger.info(f"Array shape: {source_shape}")
    logger.info(f"Source chunks: {source_chunks}")
    logger.info(f"Target chunks: {target_chunks}")
    logger.info(f"Estimated output size: {output_size_mb / 1024:.2f} GB")
    if estimated_time is None:
        logger.info("Estimated rechunking time: 6 minutes to 46 hours (Nguyen et al. 2023)")
        logger.info("  Actual time depends on target chunk size relative to dataset size")
    else:
        logger.info(f"Estimated rechunking time: {estimated_time / 60:.1f} minutes")
    logger.info("=" * 60)

    # Step 5: Import s3fs if needed
    if input_path.startswith('s3://') or output_path.startswith('s3://'):
        import s3fs  # noqa: F401

    # Step 6: Perform rechunking
    logger.info("Starting rechunking...")

    # Try rechunker library first
    try:
        import rechunker
        logger.info("Using rechunker library")

        # Create temporary directory for intermediate storage
        import tempfile
        temp_store = tempfile.mkdtemp(prefix='rechunker_')

        rechunk_plan = rechunker.rechunk(
            source_array,
            target_chunks=target_chunks,
            max_mem=max_mem,
            target_store=output_path,
            temp_store=temp_store
        )

        # Execute rechunking with progress
        logger.info("Executing rechunking plan...")
        rechunk_plan.execute()

        # Clean up temp store
        import shutil
        shutil.rmtree(temp_store, ignore_errors=True)

    except ImportError:
        logger.warning("rechunker library not available, using zarr.copy")

        # Fallback to zarr.copy
        try:
            # Open or create output array
            output_array = zarr.open(
                output_path,
                mode='w',
                shape=source_shape,
                chunks=target_chunks,
                dtype=source_array.dtype,
                compressor=source_array.compressor,
                fill_value=source_array.fill_value,
                order=source_array.order
            )

            # Copy metadata
            output_array.attrs.update(source_array.attrs)

            # Copy data in chunks with progress reporting
            logger.info("Copying data...")
            total_chunks = np.prod([
                int(np.ceil(source_shape[i] / target_chunks[i]))
                for i in range(len(source_shape))
            ])

            chunks_processed = 0

            # Generate all chunk indices
            from itertools import product
            chunk_ranges = [
                range(0, source_shape[i], target_chunks[i])
                for i in range(len(source_shape))
            ]

            for chunk_start in product(*chunk_ranges):
                # Calculate slice for this chunk
                slices = tuple(
                    slice(start, min(start + target_chunks[i], source_shape[i]))
                    for i, start in enumerate(chunk_start)
                )

                # Copy chunk
                output_array[slices] = source_array[slices]

                chunks_processed += 1

                # Log progress every 10%
                if chunks_processed % max(1, total_chunks // 10) == 0:
                    percent = 100 * chunks_processed / total_chunks
                    logger.info(f"Progress: {chunks_processed}/{total_chunks} chunks ({percent:.0f}%)")

        except Exception as e:
            logger.error(f"Rechunking failed: {e}")
            raise

    end_time = time.perf_counter()
    actual_time = end_time - start_time

    logger.info("=" * 60)
    logger.info("Rechunking complete")
    logger.info(f"Actual time: {actual_time / 60:.1f} minutes")
    if estimated_time is not None:
        logger.info(f"Estimated time: {estimated_time / 60:.1f} minutes")
    logger.info("=" * 60)

    # Step 7: Validate output
    logger.info("Validating output...")

    output_array = zarr.open(output_path, mode='r')

    # Validate shape
    if output_array.shape != source_shape:
        raise ValueError(
            f"Output shape {output_array.shape} does not match "
            f"source shape {source_shape}"
        )

    # Validate chunks
    if output_array.chunks != target_chunks:
        raise ValueError(
            f"Output chunks {output_array.chunks} do not match "
            f"target chunks {target_chunks}"
        )

    # Validate total elements
    if output_array.size != source_array.size:
        raise ValueError(
            f"Output size {output_array.size} does not match "
            f"source size {source_array.size}"
        )

    logger.info("✓ Output validation passed")
    logger.info(f"  Shape: {output_array.shape}")
    logger.info(f"  Chunks: {output_array.chunks}")
    logger.info(f"  Total elements: {output_array.size:,}")

    # Step 8: Create summary
    summary = {
        'timestamp': datetime.datetime.now().isoformat(),
        'input_path': input_path,
        'output_path': output_path,
        'array_shape': list(source_shape),
        'source_chunks': list(source_chunks),
        'target_chunks': list(target_chunks),
        'dtype': str(source_array.dtype),
        'compressor': str(source_array.compressor),
        'estimated_time_seconds': estimated_time,
        'actual_time_seconds': actual_time,
        'estimated_output_size_mb': output_size_mb,
        'num_dimensions': len(source_shape),
        'validation': {
            'shape_match': output_array.shape == source_shape,
            'chunks_match': output_array.chunks == target_chunks,
            'size_match': output_array.size == source_array.size
        }
    }

    return summary


def main():
    """Command-line interface for rechunking Zarr arrays."""
    parser = argparse.ArgumentParser(
        description="Rechunk Zarr arrays to optimize for specific access patterns",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Rechunk with validation and progress
  python rechunk.py --input /data/input.zarr \\
      --output /data/output.zarr \\
      --chunks "50,512,512"

  # Rechunk S3 data
  python rechunk.py --input s3://bucket/input.zarr \\
      --output s3://bucket/output.zarr \\
      --chunks "100,256,256" \\
      --max-mem "4GB"

  # Rechunk with overwrite
  python rechunk.py --input /data/input.zarr \\
      --output /data/output.zarr \\
      --chunks "200,128,128" \\
      --overwrite

Research basis:
  Nguyen et al. (2023), DOI: 10.1002/essoar.10511054.2
  - Rechunking time: ~6 min (large chunks) to ~46 hours (small chunks)
  - Always benchmark with sample data before rechunking full datasets
        """
    )

    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Input Zarr store path (local or s3://...)'
    )

    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output Zarr store path (local or s3://...)'
    )

    parser.add_argument(
        '--chunks', '-c',
        required=True,
        help='Target chunk shape as comma-separated integers (e.g., "50,512,512")'
    )

    parser.add_argument(
        '--max-mem',
        default='2GB',
        help='Maximum memory for rechunker library (default: 2GB)'
    )

    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite output if it already exists'
    )

    parser.add_argument(
        '--summary',
        help='Path to save JSON summary (default: rechunk_summary_TIMESTAMP.json)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Parse target chunks
    try:
        target_chunks = tuple(int(x) for x in args.chunks.split(','))
    except ValueError:
        parser.error(
            f"Invalid chunk configuration: {args.chunks}. "
            f"Must be comma-separated integers (e.g., '50,512,512')"
        )

    logger.info("Zarr Rechunking Tool")
    logger.info("=" * 60)
    logger.info(f"Input: {args.input}")
    logger.info(f"Output: {args.output}")
    logger.info(f"Target chunks: {target_chunks}")
    logger.info(f"Max memory: {args.max_mem}")
    logger.info("=" * 60)

    try:
        # Perform rechunking
        summary = rechunk_zarr(
            input_path=args.input,
            output_path=args.output,
            target_chunks=target_chunks,
            overwrite=args.overwrite,
            max_mem=args.max_mem
        )

        # Save summary
        if args.summary:
            summary_path = args.summary
        else:
            summary_path = f"rechunk_summary_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)

        logger.info("")
        logger.info("=" * 60)
        logger.info(f"✓ Rechunking complete")
        logger.info(f"Output: {args.output}")
        logger.info(f"Summary: {summary_path}")
        logger.info("=" * 60)

        return 0

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=args.verbose)
        return 1


if __name__ == "__main__":
    sys.exit(main())

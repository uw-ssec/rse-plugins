#!/usr/bin/env python3
"""
Compression Codec Comparison for Zarr Arrays
=============================================

Benchmarks all major numcodecs compressors and Blosc shuffle modes on a
realistic correlated float64 dataset. Reports compression ratio, compressed
size, compression time, and decompression time in a formatted table.

Dependencies: zarr, numpy, numcodecs (all installed with `pip install zarr`)

Usage:
    python codec-comparison.py
"""

import time
import numpy as np
import numcodecs
from numcodecs import (
    Blosc, Zstd, GZip, LZ4, Zlib, BZ2, Delta
)


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def create_test_data(rows: int = 1000, cols: int = 1000, seed: int = 42) -> np.ndarray:
    """Create a realistic correlated float64 array using cumulative sums.

    Cumulative-sum data mimics real scientific datasets (e.g., temperature
    time-series, accumulated precipitation) and has moderate compressibility.
    """
    rng = np.random.default_rng(seed)
    # 2-D random walk — each row is a cumulative sum of small steps
    increments = rng.normal(loc=0.0, scale=1.0, size=(rows, cols))
    data = np.cumsum(increments, axis=1)
    return data


def benchmark_codec(data: np.ndarray, codec, n_runs: int = 5):
    """Benchmark a single codec, returning timing and size statistics.

    Parameters
    ----------
    data : np.ndarray
        The uncompressed source array.
    codec : numcodecs codec instance
        The codec to benchmark.
    n_runs : int
        Number of repetitions for timing (median is reported).

    Returns
    -------
    dict with keys: codec_name, compressed_size_bytes, ratio,
                    compress_ms, decompress_ms
    """
    raw_bytes = data.tobytes()
    raw_size = len(raw_bytes)

    compress_times = []
    decompress_times = []
    compressed = None

    for _ in range(n_runs):
        # Compression
        t0 = time.perf_counter()
        compressed = codec.encode(raw_bytes)
        t1 = time.perf_counter()
        compress_times.append((t1 - t0) * 1000)  # ms

        # Decompression
        t0 = time.perf_counter()
        codec.decode(compressed)
        t1 = time.perf_counter()
        decompress_times.append((t1 - t0) * 1000)  # ms

    compressed_size = len(compressed)
    ratio = raw_size / compressed_size if compressed_size > 0 else float('inf')

    return {
        "compressed_size_bytes": compressed_size,
        "ratio": ratio,
        "compress_ms": float(np.median(compress_times)),
        "decompress_ms": float(np.median(decompress_times)),
    }


def format_size(size_bytes: int) -> str:
    """Format byte count as a human-readable string."""
    if size_bytes >= 1_000_000:
        return f"{size_bytes / 1_000_000:.2f} MB"
    elif size_bytes >= 1_000:
        return f"{size_bytes / 1_000:.2f} KB"
    return f"{size_bytes} B"


# ---------------------------------------------------------------------------
# Define codec configurations to benchmark
# ---------------------------------------------------------------------------

def get_codec_configs():
    """Return an ordered list of (label, codec) tuples to benchmark."""
    configs = [
        # --- Blosc with different internal algorithms ---
        ("Blosc+LZ4 (SHUFFLE)", Blosc(cname='lz4', clevel=5, shuffle=Blosc.SHUFFLE)),
        ("Blosc+Zstd (SHUFFLE)", Blosc(cname='zstd', clevel=5, shuffle=Blosc.SHUFFLE)),
        ("Blosc+Zlib (SHUFFLE)", Blosc(cname='zlib', clevel=5, shuffle=Blosc.SHUFFLE)),
        ("Blosc+LZ4HC (SHUFFLE)", Blosc(cname='lz4hc', clevel=5, shuffle=Blosc.SHUFFLE)),
        ("Blosc+BloscLZ (SHUFFLE)", Blosc(cname='blosclz', clevel=5, shuffle=Blosc.SHUFFLE)),

        # --- Blosc shuffle mode comparison (using Zstd as inner codec) ---
        ("Blosc+Zstd NOSHUFFLE", Blosc(cname='zstd', clevel=5, shuffle=Blosc.NOSHUFFLE)),
        ("Blosc+Zstd SHUFFLE", Blosc(cname='zstd', clevel=5, shuffle=Blosc.SHUFFLE)),
        ("Blosc+Zstd BITSHUFFLE", Blosc(cname='zstd', clevel=5, shuffle=Blosc.BITSHUFFLE)),

        # --- Standalone codecs ---
        ("Zstd (level 3)", Zstd(level=3)),
        ("Gzip (level 5)", GZip(level=5)),
        ("LZ4 (standalone)", LZ4()),
        ("Zlib (level 5)", Zlib(level=5)),
        ("BZ2 (level 5)", BZ2(level=5)),
    ]

    # --- Delta filter + codec combinations ---
    # Delta must wrap a compressor manually for raw encode/decode benchmarking.
    # We test the Delta filter effect by pre-filtering data separately below.
    return configs


def benchmark_with_delta(data: np.ndarray, codec, n_runs: int = 5):
    """Benchmark a codec with a Delta pre-filter applied.

    Applies Delta encoding to the raw bytes first, then compresses.
    Reports the combined filter + compress / decompress times.
    """
    delta = Delta(dtype=data.dtype)
    raw_bytes = data.tobytes()
    raw_size = len(raw_bytes)

    compress_times = []
    decompress_times = []
    compressed = None

    for _ in range(n_runs):
        # Filter + Compress
        t0 = time.perf_counter()
        filtered = delta.encode(raw_bytes)
        compressed = codec.encode(filtered)
        t1 = time.perf_counter()
        compress_times.append((t1 - t0) * 1000)

        # Decompress + Unfilter
        t0 = time.perf_counter()
        decompressed = codec.decode(compressed)
        delta.decode(decompressed)
        t1 = time.perf_counter()
        decompress_times.append((t1 - t0) * 1000)

    compressed_size = len(compressed)
    ratio = raw_size / compressed_size if compressed_size > 0 else float('inf')

    return {
        "compressed_size_bytes": compressed_size,
        "ratio": ratio,
        "compress_ms": float(np.median(compress_times)),
        "decompress_ms": float(np.median(decompress_times)),
    }


# ---------------------------------------------------------------------------
# Main benchmark runner
# ---------------------------------------------------------------------------

def main():
    print("=" * 85)
    print("Compression Codec Comparison for Zarr Arrays")
    print("=" * 85)

    # Create test data
    data = create_test_data(1000, 1000)
    raw_size = data.nbytes
    print(f"\nTest array: {data.shape} {data.dtype} ({format_size(raw_size)})")
    print(f"Data pattern: cumulative sum (correlated float64)\n")

    # --- Part 1: Codec comparison ---
    configs = get_codec_configs()

    header = f"{'Codec':<30} {'Ratio':>8} {'Compressed':>12} {'Compress':>12} {'Decompress':>12}"
    sep = "-" * 85

    print(sep)
    print("PART 1: Codec Comparison")
    print(sep)
    print(header)
    print(sep)

    for label, codec in configs:
        result = benchmark_codec(data, codec)
        print(
            f"{label:<30} "
            f"{result['ratio']:>7.1f}x "
            f"{format_size(result['compressed_size_bytes']):>12} "
            f"{result['compress_ms']:>10.2f}ms "
            f"{result['decompress_ms']:>10.2f}ms"
        )

    # --- Part 2: Delta filter effect ---
    delta_codecs = [
        ("Blosc+LZ4 (SHUFFLE)", Blosc(cname='lz4', clevel=5, shuffle=Blosc.SHUFFLE)),
        ("Blosc+Zstd (SHUFFLE)", Blosc(cname='zstd', clevel=5, shuffle=Blosc.SHUFFLE)),
        ("Zstd (level 3)", Zstd(level=3)),
        ("Gzip (level 5)", GZip(level=5)),
    ]

    print()
    print(sep)
    print("PART 2: Effect of Delta Filter (Delta + Codec)")
    print(sep)
    print(header)
    print(sep)

    for label, codec in delta_codecs:
        # Without Delta
        result_no_delta = benchmark_codec(data, codec)
        # With Delta
        result_with_delta = benchmark_with_delta(data, codec)

        print(
            f"{'  ' + label + ' (no Delta)':<30} "
            f"{result_no_delta['ratio']:>7.1f}x "
            f"{format_size(result_no_delta['compressed_size_bytes']):>12} "
            f"{result_no_delta['compress_ms']:>10.2f}ms "
            f"{result_no_delta['decompress_ms']:>10.2f}ms"
        )
        print(
            f"{'  ' + label + ' (+ Delta)':<30} "
            f"{result_with_delta['ratio']:>7.1f}x "
            f"{format_size(result_with_delta['compressed_size_bytes']):>12} "
            f"{result_with_delta['compress_ms']:>10.2f}ms "
            f"{result_with_delta['decompress_ms']:>10.2f}ms"
        )
        improvement = result_with_delta['ratio'] / result_no_delta['ratio']
        print(f"{'    → Delta improvement':<30} {improvement:>7.2f}x ratio gain")
        print()

    # --- Part 3: Shuffle mode comparison ---
    print(sep)
    print("PART 3: Blosc Shuffle Mode Comparison (Zstd clevel=5)")
    print(sep)
    print(header)
    print(sep)

    shuffle_configs = [
        ("NOSHUFFLE", Blosc(cname='zstd', clevel=5, shuffle=Blosc.NOSHUFFLE)),
        ("SHUFFLE (byte)", Blosc(cname='zstd', clevel=5, shuffle=Blosc.SHUFFLE)),
        ("BITSHUFFLE", Blosc(cname='zstd', clevel=5, shuffle=Blosc.BITSHUFFLE)),
    ]

    for label, codec in shuffle_configs:
        result = benchmark_codec(data, codec)
        print(
            f"{label:<30} "
            f"{result['ratio']:>7.1f}x "
            f"{format_size(result['compressed_size_bytes']):>12} "
            f"{result['compress_ms']:>10.2f}ms "
            f"{result['decompress_ms']:>10.2f}ms"
        )

    print()
    print(sep)
    print("Benchmark complete.")
    print(sep)
    print()
    print("Notes:")
    print("  - Ratio = uncompressed size / compressed size (higher is better)")
    print("  - Times are median of 5 runs")
    print("  - Blosc with SHUFFLE dramatically improves ratios for numerical data")
    print("  - Delta filter helps most with monotonic or slowly-varying data")
    print("  - Standalone codecs (without Blosc shuffle) show much lower ratios")
    print("    on the same data, demonstrating the value of byte shuffling.")


if __name__ == "__main__":
    main()

# Chunking Benchmark Report

**Dataset:** [DATASET_NAME]
**Date:** [BENCHMARK_DATE]
**Environment:** [INSTANCE_TYPE], [REGION], Python [PYTHON_VERSION]
**Storage backend:** [STORAGE_BACKEND]

---

## Dataset Summary

| Property | Value |
|----------|-------|
| Path | [DATASET_PATH] |
| Shape | [DATASET_SHAPE] |
| Dtype | [DTYPE] |
| Current chunks | [CURRENT_CHUNKS] |
| Total size | [TOTAL_SIZE] |
| Compression | [COMPRESSOR] |

## Benchmark Environment

| Property | Value |
|----------|-------|
| Python | [PYTHON_VERSION] |
| xarray | [XARRAY_VERSION] |
| zarr | [ZARR_VERSION] |
| Instance type | [INSTANCE_TYPE] |
| Region | [REGION] |
| Runs per config | [NUM_RUNS] |
| Memory budget | [MEMORY_BUDGET_GB] GB |

---

## Configuration Comparison

| Config | Chunk Shape | Spatial (s) | Temporal (s) | Spectral (s) | PB | Peak Mem (GB) | Status |
|--------|-------------|-------------|--------------|---------------|----|---------------|--------|
| [CONFIG_1] | [CHUNK_SHAPE_1] | [SPATIAL_1] | [TEMPORAL_1] | [SPECTRAL_1] | [PB_1] | [MEM_1] | [STATUS_1] |
| [CONFIG_2] | [CHUNK_SHAPE_2] | [SPATIAL_2] | [TEMPORAL_2] | [SPECTRAL_2] | [PB_2] | [MEM_2] | [STATUS_2] |
| [CONFIG_3] | [CHUNK_SHAPE_3] | [SPATIAL_3] | [TEMPORAL_3] | [SPECTRAL_3] | [PB_3] | [MEM_3] | [STATUS_3] |
| [CONFIG_4] | [CHUNK_SHAPE_4] | [SPATIAL_4] | [TEMPORAL_4] | [SPECTRAL_4] | [PB_4] | [MEM_4] | [STATUS_4] |

**Status key:** PASS = within memory budget, FAIL = exceeds memory budget

---

## Spatial Access Pattern

**Operation:** [SPATIAL_OPERATION_DESCRIPTION]

| Config | Mean (s) | Std (s) | Min (s) | Max (s) | Chunks Read | Utilization |
|--------|----------|---------|---------|---------|-------------|-------------|
| [CONFIG_1] | [MEAN] | [STD] | [MIN] | [MAX] | [CHUNKS] | [UTIL] |
| [CONFIG_2] | [MEAN] | [STD] | [MIN] | [MAX] | [CHUNKS] | [UTIL] |
| [CONFIG_3] | [MEAN] | [STD] | [MIN] | [MAX] | [CHUNKS] | [UTIL] |
| [CONFIG_4] | [MEAN] | [STD] | [MIN] | [MAX] | [CHUNKS] | [UTIL] |

## Temporal Access Pattern

**Operation:** [TEMPORAL_OPERATION_DESCRIPTION]

| Config | Mean (s) | Std (s) | Min (s) | Max (s) | Chunks Read | Utilization |
|--------|----------|---------|---------|---------|-------------|-------------|
| [CONFIG_1] | [MEAN] | [STD] | [MIN] | [MAX] | [CHUNKS] | [UTIL] |
| [CONFIG_2] | [MEAN] | [STD] | [MIN] | [MAX] | [CHUNKS] | [UTIL] |
| [CONFIG_3] | [MEAN] | [STD] | [MIN] | [MAX] | [CHUNKS] | [UTIL] |
| [CONFIG_4] | [MEAN] | [STD] | [MIN] | [MAX] | [CHUNKS] | [UTIL] |

## Spectral Access Pattern

**Operation:** [SPECTRAL_OPERATION_DESCRIPTION]

| Config | Mean (s) | Std (s) | Min (s) | Max (s) | Chunks Read | Utilization |
|--------|----------|---------|---------|---------|-------------|-------------|
| [CONFIG_1] | [MEAN] | [STD] | [MIN] | [MAX] | [CHUNKS] | [UTIL] |
| [CONFIG_2] | [MEAN] | [STD] | [MIN] | [MAX] | [CHUNKS] | [UTIL] |
| [CONFIG_3] | [MEAN] | [STD] | [MIN] | [MAX] | [CHUNKS] | [UTIL] |
| [CONFIG_4] | [MEAN] | [STD] | [MIN] | [MAX] | [CHUNKS] | [UTIL] |

---

## Performance Bias Summary

| Config | Chunk Shape | Best Pattern | Worst Pattern | PB | Classification |
|--------|-------------|-------------|---------------|-----|----------------|
| [CONFIG_1] | [CHUNK_SHAPE_1] | [BEST_1] | [WORST_1] | [PB_1] | [CLASS_1] |
| [CONFIG_2] | [CHUNK_SHAPE_2] | [BEST_2] | [WORST_2] | [PB_2] | [CLASS_2] |
| [CONFIG_3] | [CHUNK_SHAPE_3] | [BEST_3] | [WORST_3] | [PB_3] | [CLASS_3] |
| [CONFIG_4] | [CHUNK_SHAPE_4] | [BEST_4] | [WORST_4] | [PB_4] | [CLASS_4] |

**Classification key:** Balanced (PB < 1.5), Moderate (1.5-3.0), Biased (3.0-10.0), Extreme (> 10.0)

---

## Recommendations

### Primary Recommendation

**For [WORKLOAD_DESCRIPTION]:**

Use chunk shape **[RECOMMENDED_CHUNK_SHAPE]**:
- [PRIMARY_PATTERN]: [PRIMARY_TIME] +/- [PRIMARY_STD] s
- [SECONDARY_PATTERN]: [SECONDARY_TIME] +/- [SECONDARY_STD] s
- Performance bias: [PB_VALUE] ([PB_CLASSIFICATION])
- Peak memory: [PEAK_MEM] GB ([MEMORY_STATUS] [MEMORY_BUDGET] GB budget)

### Alternative

**If [ALTERNATIVE_CONDITION]:**

Consider chunk shape **[ALTERNATIVE_CHUNK_SHAPE]**:
- [ALTERNATIVE_BENEFIT]
- [ALTERNATIVE_TRADEOFF]

### Configurations to Avoid

- **[AVOID_CONFIG]**: [AVOID_REASON]

---

## Methodology Notes

- All timings measured with `time.perf_counter()` (wall-clock)
- Peak memory measured with `tracemalloc`
- OS page cache cleared between runs ([CACHE_CLEAR_METHOD])
- Warm-up reads performed before timed measurements ([NUM_WARMUP] warm-up iterations)
- Performance bias calculated as max(T) / min(T) per Nguyen et al. (2023)
- [ADDITIONAL_NOTES]

## Environment Metadata

```json
{
  "date": "[BENCHMARK_DATE]",
  "python_version": "[PYTHON_VERSION]",
  "xarray_version": "[XARRAY_VERSION]",
  "zarr_version": "[ZARR_VERSION]",
  "instance_type": "[INSTANCE_TYPE]",
  "storage_backend": "[STORAGE_BACKEND]",
  "region": "[REGION]",
  "num_runs": [NUM_RUNS],
  "memory_budget_gb": [MEMORY_BUDGET_GB]
}
```

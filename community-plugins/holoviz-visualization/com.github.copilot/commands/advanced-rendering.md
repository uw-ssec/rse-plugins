---
description: Render massive datasets (100M+ points) efficiently with Datashader rasterization and aggregation
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Advanced Rendering

Handle large-scale data visualization with Datashader.

## Arguments

$ARGUMENTS — describe the data and goal (e.g., "visualize 500M GPS points", "optimize slow scatter plot", "aggregate time series data")

## Workflow

1. **Assess the data:**
   - Data size (rows, columns, memory footprint)
   - Data types and coordinate ranges
   - Available RAM and performance constraints

2. **Choose the rendering strategy:**
   - Datashader rasterization for point/line data
   - Aggregation functions (count, mean, sum, min, max)
   - Canvas resolution for target display
   - Transfer functions for color mapping

3. **Implement** using Datashader:
   - Configure Canvas with appropriate dimensions
   - Apply aggregation and transfer functions
   - Integrate with HoloViews via `rasterize()` or `datashade()`
   - Add dynamic re-rendering on zoom

4. **Optimize** if needed:
   - Data type downcasting (float64 to float32)
   - Chunked processing for files larger than RAM
   - Caching strategies

5. **Report** the code, performance characteristics, and rendering instructions.

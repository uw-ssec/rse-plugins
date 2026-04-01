---
description: Create quick interactive plots with hvPlot from pandas DataFrames, NumPy arrays, or Xarray datasets
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Plotting Fundamentals

Create quick interactive visualizations with hvPlot.

## Arguments

$ARGUMENTS — describe what to plot (e.g., "line chart of temperature over time", "scatter plot from this CSV", "histogram of values")

## Workflow

1. **Understand the data and desired visualization:**
   - Identify data source (DataFrame, CSV, array, Xarray)
   - Determine plot type (line, scatter, bar, histogram, box, area, heatmap)
   - Identify x/y columns, grouping, and color encoding

2. **Read the data** if a file is specified.

3. **Create the visualization** using hvPlot:
   - Use `.hvplot()` accessor for pandas/Xarray
   - Add interactivity (hover tools, selection)
   - Compose layouts with `+` (side-by-side) and `*` (overlay)
   - Apply appropriate styling and labels

4. **Report** the code and how to display it (Jupyter or Panel serve).

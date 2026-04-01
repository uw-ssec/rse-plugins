---
description: Create advanced declarative visualizations with HoloViews for multi-dimensional data, interactive streams, and complex compositions
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Data Visualization

Create advanced declarative visualizations with HoloViews.

## Arguments

$ARGUMENTS — describe the visualization (e.g., "linked scatter and histogram", "faceted heatmap by category", "interactive network graph")

## Workflow

1. **Understand the requirements:**
   - Data dimensions and relationships
   - Desired interaction patterns (linked brushing, streams, selection)
   - Composition needs (overlays, layouts, facets)
   - Backend preference (Bokeh for interactivity, Matplotlib for publication)

2. **Design the visualization approach:**
   - Choose HoloViews element types (Curve, Scatter, HeatMap, etc.)
   - Plan overlay and layout composition
   - Design interaction with Streams or Selection

3. **Implement** using HoloViews declarative API:
   - Build element objects with proper dimensions (kdims, vdims)
   - Compose with `*` (overlay) and `+` (layout)
   - Add DynamicMap for interactive exploration
   - Apply options for styling

4. **Report** the code and rendering instructions.

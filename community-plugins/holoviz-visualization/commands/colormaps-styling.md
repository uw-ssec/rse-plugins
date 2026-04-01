---
description: Select and apply perceptually uniform colormaps and accessible visual styling with Colorcet
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Colormaps and Styling

Select appropriate colormaps and apply accessible visual styling.

## Arguments

$ARGUMENTS — describe the need (e.g., "colorblind-safe palette for heatmap", "diverging colormap for anomalies", "consistent theme for dashboard")

## Workflow

1. **Understand the visualization context:**
   - Data type (sequential, diverging, categorical, cyclical)
   - Accessibility requirements (colorblind-safe)
   - Output medium (screen, print, projection)

2. **Recommend colormaps** from Colorcet:
   - Sequential: `fire`, `kbc`, `bmw` for ordered data
   - Diverging: `coolwarm`, `bwr` for data with a meaningful center
   - Categorical: distinct hues for nominal data
   - Perceptually uniform for accurate data representation

3. **Apply styling** to the visualization:
   - Colormap selection and configuration
   - Theme application (dark, light, minimal)
   - Consistent styling across multi-plot compositions

4. **Verify accessibility:**
   - Test with colorblind simulation
   - Ensure sufficient contrast
   - Add redundant encoding (shape, pattern) where needed

5. **Report** the recommended approach with code examples.

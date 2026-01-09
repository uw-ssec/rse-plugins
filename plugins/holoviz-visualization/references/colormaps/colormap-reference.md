# Colormap Reference

## Overview

Complete catalog of Colorcet colormaps organized by category. Each colormap is perceptually uniform and designed for specific data types.

**When to use this reference**:
- Selecting colormaps for specific data types
- Understanding colormap properties
- Finding colorblind-safe alternatives
- Choosing between similar colormaps

## Table of Contents

1. [Sequential Colormaps](#sequential-colormaps)
2. [Diverging Colormaps](#diverging-colormaps)
3. [Categorical Colormaps](#categorical-colormaps)
4. [Cyclic Colormaps](#cyclic-colormaps)
5. [Rainbow/Full Spectrum](#rainbow-full-spectrum)
6. [Colorblind-Safe Colormaps](#colorblind-safe-colormaps)
7. [Selection Guide](#selection-guide)

## Sequential Colormaps

**Use for**: Single-channel data with one direction (e.g., temperature, density, probability)

### Blue Sequential

| Name | Description | Best For |
|------|-------------|----------|
| `cet_blues` | Light to dark blue | Water depth, temperature (cold) |
| `cet_kbc` | Black-blue-cyan | High contrast data |
| `cet_kbgyw` | Black-blue-gray-yellow-white | Full range with neutral midpoint |

**Example**:
```python
import colorcet as cc
data.hvplot.scatter('x', 'y', c='value', cmap=cc.cm['cet_blues'])
```

### Green Sequential

| Name | Description | Best For |
|------|-------------|----------|
| `cet_greens` | Light to dark green | Vegetation, health metrics |
| `cet_kgy` | Black-green-yellow | Natural data |

### Red/Fire Sequential

| Name | Description | Best For |
|------|-------------|----------|
| `cet_fire` | Black-red-yellow-white | Heat, intensity, fire data |
| `cet_reds` | Light to dark red | Alerts, warnings |

### Gray Sequential

| Name | Description | Best For |
|------|-------------|----------|
| `cet_gray` | Black to white | Print-safe, grayscale displays |
| `cet_gray_r` | White to black (reversed) | Light backgrounds |

## Diverging Colormaps

**Use for**: Data with meaningful center point (e.g., correlation, anomalies, change)

### Recommended Diverging

| Name | Description | Center | Best For |
|------|-------------|--------|----------|
| `cet_coolwarm` | Blue-white-red | White | Correlation, temperature anomalies |
| `cet_bwy` | Blue-white-yellow | White | Balanced emphasis |
| `cet_bjy` | Blue-gray-yellow | Gray | Neutral center |
| `cet_gwv` | Green-white-violet | White | pH, chemical data |

**Example**:
```python
# Correlation matrix with diverging colormap
correlation.hvplot.heatmap(
    cmap=cc.cm['cet_coolwarm'],
    clim=(-1, 1),  # Symmetric around 0
    colorbar=True
)
```

### Colorblind-Safe Diverging

| Name | Description | Safe For |
|------|-------------|----------|
| `cet_d4` | Blue-white-orange | Deuteranopia, protanopia |
| `cet_bwy` | Blue-white-yellow | Most types |

## Categorical Colormaps

**Use for**: Qualitative data with distinct categories

### Recommended Categorical

| Name | Colors | Max Categories | Best For |
|------|--------|----------------|----------|
| `tab10` | 10 distinct colors | 10 | General categories |
| `tab20` | 20 distinct colors | 20 | Many categories |
| `tab20b` | 20 colors (paired) | 20 | Grouped categories |
| `tab20c` | 20 colors (paired) | 20 | Grouped categories |

**Example**:
```python
from colorcet import palette

categories = df['category'].unique()
colors = palette['tab10'][:len(categories)]
color_map = dict(zip(categories, colors))

df.hvplot.scatter('x', 'y', c='category', cmap=color_map)
```

### Glasbey Categorical

| Name | Description | Best For |
|------|-------------|----------|
| `cet_glasbey` | Maximum perceptual difference | Scientific categories |
| `cet_glasbey_bw` | Excluding black/white | Light/dark backgrounds |
| `cet_glasbey_hv` | High visibility | Presentations |

## Cyclic Colormaps

**Use for**: Periodic/angular data where endpoints meet (e.g., angles, directions, phase)

### Recommended Cyclic

| Name | Description | Best For |
|------|-------------|----------|
| `cet_cyclic_c1` | Blue-yellow cycle | Wind direction |
| `cet_cyclic_c2` | Green-purple cycle | Phase data |
| `cet_cyclic_c3` | Red-blue cycle | Periodic signals |

**Example**:
```python
# Wind direction (0-360 degrees)
wind_data.hvplot.scatter(
    'x', 'y',
    c='direction',
    cmap=cc.cm['cet_cyclic_c1'],
    clim=(0, 360)
)
```

## Rainbow/Full Spectrum

**Use for**: General purpose, full data range

### Recommended Rainbow

| Name | Description | Notes |
|------|-------------|-------|
| `cet_goertzel` | Perceptually uniform rainbow | Best general rainbow |
| `cet_rainbow` | Full spectrum | Scientific data |
| `cet_isolum` | Isoluminant rainbow | Even brightness |

**Example**:
```python
# General purpose visualization
data.hvplot.image(
    cmap=cc.cm['cet_goertzel'],
    colorbar=True
)
```

**Warning**: Avoid matplotlib's `jet` and `rainbow` - they are NOT perceptually uniform.

## Colorblind-Safe Colormaps

**Critical for accessibility**: ~8% of men and ~0.5% of women have color vision deficiency

### By Deficiency Type

**Deuteranopia/Protanopia (Red-Green)**:
- `cet_d4` - Blue-white-orange diverging
- `cet_p3` - Blue-gray-orange
- `cet_blues` - Blue sequential (safe)

**Tritanopia (Blue-Yellow)**:
- `cet_t10` - Red-white-blue
- `cet_reds` - Red sequential (safe)

**Universal (All Types)**:
- `cet_gray` - Grayscale (always safe)
- `cet_blues` - Blue sequential
- `cet_reds` - Red sequential

**Example**:
```python
# Ensure colorblind accessibility
plot = data.hvplot(
    c='value',
    cmap=cc.cm['cet_d4'],  # Safe for red-green colorblindness
    title='Accessible Visualization'
)
```

## Selection Guide

### By Data Type

| Data Type | Recommended Colormap | Alternative |
|-----------|---------------------|-------------|
| Temperature | `cet_fire` or `cet_coolwarm` | `cet_blues` (cold only) |
| Elevation | `cet_kbgyw` | `cet_terrain` |
| Correlation | `cet_coolwarm` | `cet_bwy` |
| Categories | `tab10` | `cet_glasbey` |
| Wind direction | `cet_cyclic_c1` | `cet_cyclic_c2` |
| Density | `cet_blues` | `cet_fire` |
| Probability | `cet_blues` | `cet_greens` |
| Divergence | `cet_coolwarm` | `cet_bjy` |
| General | `cet_goertzel` | `cet_rainbow` |

### By Context

**Publication (Print)**:
- Use `cet_gray` for black & white printing
- Test colormap in grayscale
- Avoid colormaps that lose information in grayscale

**Presentation**:
- `cet_fire` - High visibility
- `cet_coolwarm` - Clear divergence
- Avoid subtle colormaps like `cet_isolum`

**Web Dashboard**:
- `cet_goertzel` - General purpose
- `tab10` - Categories
- Consider dark mode: use `_r` (reversed) variants

**Scientific**:
- `cet_blues`, `cet_fire` - Traditional
- `cet_coolwarm` - Diverging
- Avoid rainbow unless data is truly cyclic

### Accessibility Priority

**High Accessibility Need**:
1. `cet_d4` (colorblind-safe diverging)
2. `cet_gray` (grayscale-safe)
3. `cet_blues` (universally safe)

**Medium Accessibility Need**:
1. `cet_coolwarm` (good contrast)
2. `cet_bwy` (reasonable for most)
3. `tab10` (distinct categories)

## Usage Patterns

### Basic Usage

```python
import colorcet as cc
from colorcet import cm, palette

# Option 1: Use cm dict
cmap = cm['cet_goertzel']

# Option 2: Use colorcet.cc
cmap = cc.cm['cet_coolwarm']

# For categorical
colors = palette['tab10']
```

### With HoloViews

```python
import holoviews as hv
from colorcet import cm

scatter = hv.Scatter(data, 'x', 'y', vdims=['value']).opts(
    color='value',
    cmap=cm['cet_goertzel'],
    colorbar=True
)
```

### With Panel

```python
import panel as pn
from colorcet import cm

plot = data.hvplot.scatter(
    'x', 'y',
    c='value',
    cmap=cm['cet_fire']
).opts(colorbar=True)

pn.panel(plot).servable()
```

### Testing Colorblindness

```python
# Simulate deuteranopia
from colorspacious import cspace_convert

def simulate_colorblind(image):
    # Convert to CVD simulation
    return cspace_convert(image, "sRGB1", "sRGB1+CVD", cvd_type="deuteranomaly")
```

## Avoiding Bad Colormaps

### Never Use

| Colormap | Problem | Use Instead |
|----------|---------|-------------|
| `jet` | Not perceptually uniform, misleading | `cet_goertzel` |
| `rainbow` (matplotlib) | False gradients | `cet_rainbow` |
| `hsv` | Discontinuous | `cet_cyclic_c1` |

### Why These Are Bad

**jet colormap problems**:
- Creates false features in data
- Not perceptually uniform (yellow appears brighter)
- Poor for colorblind viewers
- Unprofessional in scientific publications

**Example - Don't do this**:
```python
# ❌ Bad: Using jet
plot = data.hvplot(cmap='jet')

# ✅ Good: Using perceptually uniform colormap
plot = data.hvplot(cmap=cc.cm['cet_goertzel'])
```

## Colormap Properties

### Perceptual Uniformity

**Definition**: Equal steps in data = equal perceptual steps in color

**Test**:
```python
import numpy as np
import colorcet as cc

# Generate gradient
values = np.linspace(0, 1, 256)
gradient = cc.cm['cet_goertzel'](values)

# Check luminance uniformity
luminance = 0.2126*gradient[:, 0] + 0.7152*gradient[:, 1] + 0.0722*gradient[:, 2]
# Should be monotonic for sequential
```

### Colormap Reversal

```python
# Reverse any colormap
cmap_reversed = cm['cet_fire_r']

# Or manually
from matplotlib.colors import ListedColormap
cmap_reversed = ListedColormap(cm['cet_fire'].colors[::-1])
```

## Summary

**Key principles**:
1. Match colormap type to data type (sequential, diverging, categorical, cyclic)
2. Use perceptually uniform colormaps (Colorcet, not jet)
3. Consider colorblind accessibility (~8% of population)
4. Test in grayscale for print
5. Use categorical for qualitative data

**Most versatile colormaps**:
- Sequential: `cet_blues`, `cet_fire`, `cet_gray`
- Diverging: `cet_coolwarm`, `cet_d4` (colorblind-safe)
- Categorical: `tab10`, `cet_glasbey`
- Cyclic: `cet_cyclic_c1`
- General: `cet_goertzel`

**Always avoid**: `jet`, matplotlib's `rainbow`, `hsv`

## References

- [Colorcet Documentation](https://colorcet.holoviz.org/)
- [Colorcet Gallery](https://colorcet.holoviz.org/user_guide/index.html)
- [Color Universal Design](https://jfly.uni-koeln.de/color/)
- [Why Rainbow Colormaps Are Bad](https://www.kennethmoreland.com/color-advice/)

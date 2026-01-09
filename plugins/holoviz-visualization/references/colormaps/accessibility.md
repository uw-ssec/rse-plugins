# Colormap Accessibility Guide

## Overview

Comprehensive guide to creating accessible visualizations with consideration for color vision deficiency, WCAG compliance, and universal design principles.

**When to use this guide**:
- Designing public-facing visualizations
- Ensuring WCAG compliance
- Supporting colorblind users (~8% of male population)
- Creating print-safe graphics

## Table of Contents

1. [Color Vision Deficiency Types](#color-vision-deficiency-types)
2. [Colorblind-Safe Colormaps](#colorblind-safe-colormaps)
3. [WCAG Compliance](#wcag-compliance)
4. [Testing for Accessibility](#testing-for-accessibility)
5. [Alternative Encoding Strategies](#alternative-encoding-strategies)
6. [Best Practices](#best-practices)

## Color Vision Deficiency Types

### Prevalence

| Type | Affected Colors | Male | Female |
|------|----------------|------|--------|
| Deuteranopia | Red-Green (no green) | 1.0% | 0.01% |
| Protanopia | Red-Green (no red) | 1.0% | 0.01% |
| Tritanopia | Blue-Yellow | 0.003% | 0.003% |
| Anomalous Trichromacy | Reduced sensitivity | 6.0% | 0.4% |
| Total CVD | Any type | ~8.0% | ~0.5% |

**Key insight**: Red-green colorblindness is most common, affecting ~8% of men.

### How Colors Appear

**Normal vision**:
- Full RGB spectrum
- Clear red-green-blue distinction

**Deuteranopia (no green receptors)**:
- Reds appear as browns/yellows
- Greens appear as beiges/grays
- Red-green confusion

**Protanopia (no red receptors)**:
- Reds appear dark/gray
- Greens appear as beiges
- Red-green confusion

**Tritanopia (no blue receptors)**:
- Blues appear green
- Yellows appear pink/gray
- Blue-yellow confusion

## Colorblind-Safe Colormaps

### Universal Safe Colormaps

**Safe for all CVD types**:

```python
from colorcet import cm

# Sequential - Always safe
safe_sequential = [
    'cet_gray',      # Grayscale
    'cet_blues',     # Blue only
    'cet_reds',      # Red only
]

# Usage
data.hvplot.scatter('x', 'y', c='value', cmap=cm['cet_blues'])
```

### Deuteranopia/Protanopia Safe

**Red-green colorblind safe** (~8% of men):

```python
# Diverging colormaps
safe_diverging = {
    'cet_d4': 'Blue-white-orange (best)',
    'cet_bwy': 'Blue-white-yellow',
    'cet_coolwarm': 'Blue-white-red (good contrast)',
}

# Usage
correlation.hvplot.heatmap(
    cmap=cm['cet_d4'],
    title='Colorblind-Safe Correlation'
)
```

### Tritanopia Safe

**Blue-yellow colorblind safe**:

```python
safe_tritanopia = {
    'cet_t10': 'Red-white-blue',
    'cet_reds': 'Red sequential',
    'cet_gray': 'Grayscale',
}
```

### Categorical Safe

**For categories with CVD**:

```python
from colorcet import palette

# Use high-contrast distinct colors
safe_categories = palette['tab10']

# Manually select CVD-safe colors
cvd_safe = [
    '#0173b2',  # Blue
    '#de8f05',  # Orange
    '#029e73',  # Green (avoid with red)
    '#cc78bc',  # Pink
    '#ece133',  # Yellow
    '#56b4e9',  # Light blue
]

color_map = dict(zip(categories, cvd_safe))
```

## WCAG Compliance

### Contrast Requirements

**WCAG 2.1 Standards**:

| Level | Contrast Ratio | Use Case |
|-------|---------------|----------|
| AA (minimum) | 4.5:1 | Normal text |
| AA (large text) | 3:1 | 18pt+ or bold 14pt+ |
| AAA (enhanced) | 7:1 | Maximum accessibility |

### Checking Contrast

```python
def check_contrast(color1, color2):
    """
    Calculate WCAG contrast ratio between two colors.

    Parameters
    ----------
    color1, color2 : str or tuple
        Colors as hex strings or RGB tuples

    Returns
    -------
    float
        Contrast ratio (1-21)
    """
    from matplotlib.colors import to_rgb

    def luminance(color):
        r, g, b = to_rgb(color)
        r = r/12.92 if r <= 0.03928 else ((r+0.055)/1.055)**2.4
        g = g/12.92 if g <= 0.03928 else ((g+0.055)/1.055)**2.4
        b = b/12.92 if b <= 0.03928 else ((b+0.055)/1.055)**2.4
        return 0.2126*r + 0.7152*g + 0.0722*b

    l1 = luminance(color1)
    l2 = luminance(color2)
    lighter = max(l1, l2)
    darker = min(l1, l2)

    return (lighter + 0.05) / (darker + 0.05)

# Example
contrast = check_contrast('#0173b2', '#ffffff')
print(f"Contrast: {contrast:.2f}:1")  # Should be > 4.5
```

### Colorbar Text

```python
import holoviews as hv
from colorcet import cm

# Ensure colorbar labels are readable
plot = data.hvplot.scatter('x', 'y', c='value', cmap=cm['cet_fire']).opts(
    colorbar=True,
    colorbar_opts={
        'title': 'Value',
        'title_text_color': 'black',  # High contrast
        'major_label_text_color': 'black',
        'background_fill_color': 'white',
    }
)
```

## Testing for Accessibility

### Visual Simulation Tools

**Online simulators**:
- [Coblis Color Blindness Simulator](https://www.color-blindness.com/coblis-color-blindness-simulator/)
- [Adobe Color Accessibility Tools](https://color.adobe.com/create/color-accessibility)

**Browser extensions**:
- [Colorblindly](https://chrome.google.com/webstore/detail/colorblindly) (Chrome)
- [Let's Get Color Blind](https://addons.mozilla.org/en-US/firefox/addon/let-s-get-color-blind/) (Firefox)

### Python Simulation

```python
def simulate_cvd(image, cvd_type='deuteranomaly'):
    """
    Simulate color vision deficiency.

    Parameters
    ----------
    image : array
        RGB image array
    cvd_type : str
        'deuteranomaly', 'protanomaly', or 'tritanomaly'

    Returns
    -------
    array
        Simulated image
    """
    from colorspacious import cspace_convert

    return cspace_convert(
        image,
        "sRGB1",
        "sRGB1+CVD",
        cvd_type=cvd_type
    )

# Usage
import matplotlib.pyplot as plt
from PIL import Image

# Load your visualization
img = Image.open('plot.png')
img_array = np.array(img)

# Simulate deuteranopia
simulated = simulate_cvd(img_array, 'deuteranomaly')

# Display
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
ax1.imshow(img_array)
ax1.set_title('Original')
ax2.imshow(simulated)
ax2.set_title('Deuteranopia Simulation')
```

### Grayscale Test

```python
# Test if visualization works in grayscale
grayscale_plot = data.hvplot.scatter(
    'x', 'y',
    c='value',
    cmap='gray'  # Force grayscale
)

# Compare
import panel as pn
pn.Row(
    data.hvplot.scatter('x', 'y', c='value', cmap=cm['cet_fire']).opts(title='Color'),
    grayscale_plot.opts(title='Grayscale Test')
)
```

## Alternative Encoding Strategies

### Pattern/Texture Encoding

**Use patterns in addition to color**:

```python
import holoviews as hv

# Add hatch patterns for categories
overlay = hv.Overlay([
    hv.Area(data[data.category == cat], 'x', 'y').opts(
        color=color,
        hatch_pattern='/' if i % 2 else '\\'  # Alternate patterns
    )
    for i, (cat, color) in enumerate(color_map.items())
])
```

### Shape Encoding

```python
# Use different marker shapes
import panel as pn

plots = []
for category in categories:
    subset = data[data.category == category]
    plots.append(
        subset.hvplot.scatter(
            'x', 'y',
            marker=marker_map[category],  # Different shapes
            color=color_map[category],
            label=category
        )
    )

hv.Overlay(plots).opts(legend_position='right')
```

### Text Labels

```python
# Add text labels for critical information
from holoviews import opts

scatter = hv.Scatter(data, 'x', 'y', vdims=['value', 'label'])

labels = hv.Labels(data, ['x', 'y'], 'label')

(scatter * labels).opts(
    opts.Scatter(color='value', cmap=cm['cet_d4']),
    opts.Labels(text_font_size='8pt', text_color='black')
)
```

### Redundant Encoding

**Encode same information multiple ways**:

```python
# Encode value with both color AND size
scatter = data.hvplot.scatter(
    'x', 'y',
    c='value',
    s='value',  # Redundant size encoding
    cmap=cm['cet_d4'],
    size=50,
    alpha=0.6
)
```

## Best Practices

### 1. Choose Appropriate Colormaps

```python
# ✅ Good: Colorblind-safe diverging
plot = data.hvplot(c='correlation', cmap=cm['cet_d4'])

# ✅ Good: Universal safe sequential
plot = data.hvplot(c='value', cmap=cm['cet_blues'])

# ❌ Bad: Red-green for diverging (8% can't see)
plot = data.hvplot(c='correlation', cmap='RdYlGn')

# ❌ Bad: Rainbow colormap
plot = data.hvplot(c='value', cmap='jet')
```

### 2. Test in Multiple Modes

```python
def test_accessibility(plot, title):
    """Create comparison showing different CVD simulations."""
    import panel as pn

    return pn.Column(
        f"## {title}",
        pn.Row(
            plot.opts(title='Original'),
            # In production, add CVD simulations
        )
    )
```

### 3. Provide Multiple Encodings

```python
# ✅ Good: Color + shape + size
scatter = data.hvplot.scatter(
    'x', 'y',
    by='category',
    c='value',
    s='value',
    cmap=cm['cet_d4'],
    legend='top_right'
)

# Add text annotations for key points
```

### 4. High Contrast

```python
# ✅ Good: High contrast colormap
plot = data.hvplot(
    c='value',
    cmap=cm['cet_fire'],  # Black to white (high contrast)
    colorbar=True
)

# ✅ Good: Clear background contrast
plot.opts(
    bgcolor='white',
    fontsize={'title': 14, 'labels': 12}
)
```

### 5. Descriptive Legends

```python
# ✅ Good: Clear legend with accessible colors
plot = data.hvplot.scatter(
    'x', 'y',
    by='category',
    cmap=['#0173b2', '#de8f05', '#029e73'],  # CVD-safe
    legend='right',
    title='Clear Categorical Encoding'
)
```

### 6. Documentation

```python
def create_accessible_plot(data, **kwargs):
    """
    Create accessible visualization.

    Accessibility features:
    - Colorblind-safe colormap (cet_d4)
    - High contrast (WCAG AA)
    - Redundant size encoding
    - Clear labels and legend
    """
    return data.hvplot.scatter(
        'x', 'y',
        c='value',
        s='value',
        cmap=cm['cet_d4'],
        **kwargs
    )
```

## Accessibility Checklist

### Before Publishing

- [ ] Colormap is colorblind-safe (tested with simulator)
- [ ] Text contrast meets WCAG AA (4.5:1 minimum)
- [ ] Visualization works in grayscale
- [ ] Legend is clear and readable
- [ ] Important information encoded multiple ways
- [ ] Tested with actual users if possible
- [ ] Alternative descriptions provided (alt text)

### For Different Contexts

**Web dashboards**:
- [ ] Support dark/light mode
- [ ] Keyboard navigation
- [ ] Screen reader compatible
- [ ] Configurable color schemes

**Print/PDF**:
- [ ] Test in grayscale
- [ ] High contrast
- [ ] Clear labels
- [ ] Pattern encoding where possible

**Presentations**:
- [ ] High contrast
- [ ] Large text
- [ ] Simple colormaps
- [ ] Clear from distance

## Common Mistakes

### ❌ Red-Green Encoding

```python
# Bad: Red for negative, green for positive
bad_colors = {'negative': 'red', 'positive': 'green'}

# Good: Blue-orange instead
good_colors = {'negative': '#0173b2', 'positive': '#de8f05'}
```

### ❌ Low Contrast

```python
# Bad: Light colors on white
bad_plot = data.hvplot(color='#ffcccc')

# Good: High contrast
good_plot = data.hvplot(color='#cc0000')
```

### ❌ Color-Only Encoding

```python
# Bad: Only color distinguishes categories
bad_plot = data.hvplot.scatter('x', 'y', by='category')

# Good: Color + shape
good_plot = data.hvplot.scatter(
    'x', 'y',
    by='category',
    marker='category',  # Different shapes
    cmap=['#0173b2', '#de8f05', '#029e73']
)
```

## Resources

### Tools

- **Coblis**: Online CVD simulator
- **Colorspacious**: Python CVD simulation
- **WebAIM Contrast Checker**: WCAG compliance
- **Color Oracle**: Desktop CVD simulator

### Guidelines

- [WCAG 2.1 Color Guidelines](https://www.w3.org/WAI/WCAG21/Understanding/use-of-color.html)
- [Color Universal Design](https://jfly.uni-koeln.de/color/)
- [Colorbrewer](https://colorbrewer2.org/) - Colorblind-safe palettes

### Research

- [How Colormaps Can Lie](https://doi.org/10.1109/MCG.2018.2877473)
- [Color Oracle Paper](http://www.colororacle.org/)

## Summary

**Key principles**:
1. ~8% of men have red-green colorblindness
2. Use colorblind-safe colormaps (`cet_d4`, `cet_blues`)
3. Test with CVD simulators
4. Meet WCAG contrast requirements (4.5:1)
5. Provide redundant encodings (color + shape/size)
6. Avoid red-green for binary/diverging data

**Universal safe choices**:
- Sequential: `cet_gray`, `cet_blues`, `cet_fire`
- Diverging: `cet_d4`, `cet_bwy`
- Categorical: Blue-orange-green palette

**Testing workflow**:
1. Create visualization with colorblind-safe colormap
2. Test with CVD simulator
3. Check WCAG contrast
4. Verify in grayscale
5. Add redundant encodings if needed

By following these guidelines, your visualizations will be accessible to the widest possible audience.

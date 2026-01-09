# HoloViews Styling Guide

## Overview

Advanced customization patterns for HoloViews visualizations including styling options, themes, backends, and publication-quality output.

**When to use this guide**:
- Customizing plot appearance
- Creating consistent styling across plots
- Publication-quality figures
- Custom themes and branding

## Table of Contents

1. [Styling Basics](#styling-basics)
2. [Color Customization](#color-customization)
3. [Plot Options](#plot-options)
4. [Themes and Styles](#themes-and-styles)
5. [Backend-Specific Options](#backend-specific-options)
6. [Publication Quality](#publication-quality)

## Styling Basics

### The `.opts()` Method

```python
import holoviews as hv
from colorcet import cm

hv.extension('bokeh')

# Basic scatter plot
scatter = hv.Scatter(data, 'x', 'y')

# Apply styling
scatter.opts(
    color='red',
    size=5,
    alpha=0.7,
    width=600,
    height=400,
    title='My Plot'
)
```

### Global Options

```python
# Set global defaults
hv.opts.defaults(
    hv.opts.Scatter(
        size=5,
        alpha=0.7,
        tools=['hover'],
        width=600,
        height=400
    ),
    hv.opts.Curve(
        line_width=2,
        color='blue'
    )
)

# Now all Scatter and Curve elements use these defaults
```

### Style vs Options

```python
# Options: Bokeh-specific styling
scatter.opts(
    size=10,           # Marker size
    color='red',       # Marker color
    alpha=0.5,         # Transparency
    width=600,         # Plot width
    height=400         # Plot height
)

# Style: Element-level styling (deprecated in favor of opts)
# Use opts() instead
```

## Color Customization

### Single Color

```python
# Static color
scatter = hv.Scatter(data, 'x', 'y').opts(color='#0173b2')

# RGB tuple
scatter.opts(color=(0.0, 0.45, 0.70))
```

### Color by Dimension

```python
# Color by data dimension
scatter = hv.Scatter(data, 'x', 'y', vdims=['value']).opts(
    color='value',
    cmap=cm['cet_fire'],
    colorbar=True
)

# Normalized colormapping
scatter.opts(
    color=hv.dim('value').norm(),  # Normalize to [0, 1]
    cmap=cm['cet_fire']
)
```

### Custom Color Mapping

```python
# Categorical color mapping
categories = ['A', 'B', 'C']
colors = ['#0173b2', '#de8f05', '#029e73']
color_map = dict(zip(categories, colors))

scatter = hv.Scatter(data, 'x', 'y', vdims=['category']).opts(
    color='category',
    cmap=color_map
)

# Continuous with custom levels
scatter.opts(
    color='value',
    cmap=cm['cet_fire'],
    color_levels=10,  # Discrete levels
    clim=(0, 100)     # Color limits
)
```

### Colormaps

```python
from colorcet import cm

# Sequential
scatter.opts(color='value', cmap=cm['cet_fire'])

# Diverging
heatmap.opts(cmap=cm['cet_coolwarm'], symmetric=True)

# Reversed
scatter.opts(cmap=cm['cet_fire_r'])

# Custom colormap
from matplotlib.colors import ListedColormap
custom_cmap = ListedColormap(['#440154', '#31688e', '#35b779', '#fde724'])
scatter.opts(cmap=custom_cmap)
```

## Plot Options

### Size and Dimensions

```python
plot = hv.Curve(data, 'x', 'y').opts(
    width=800,           # Plot width in pixels
    height=400,          # Plot height in pixels
    aspect=2,            # Width/height ratio (alternative to height)
    responsive=True,     # Fill container
    frame_width=600,     # Data frame width
    frame_height=300     # Data frame height
)
```

### Axes

```python
plot.opts(
    # Axis labels
    xlabel='Time (seconds)',
    ylabel='Temperature (°C)',

    # Axis ranges
    xlim=(0, 100),
    ylim=(0, 50),

    # Axis scale
    logx=True,
    logy=True,

    # Invert axes
    invert_axes=True,
    invert_xaxis=True,
    invert_yaxis=True,

    # Axis visibility
    xaxis='top',         # 'top', 'bottom', None
    yaxis='right',       # 'left', 'right', None
)
```

### Titles and Labels

```python
plot.opts(
    title='My Visualization',
    xlabel='X Axis',
    ylabel='Y Axis',

    # Font sizes
    fontsize={
        'title': 16,
        'labels': 12,
        'xticks': 10,
        'yticks': 10
    },

    # Font scale (multiplier)
    fontscale=1.5
)
```

### Markers and Lines

```python
# Scatter markers
scatter.opts(
    marker='circle',     # 'circle', 'square', 'triangle', 'diamond', etc.
    size=10,            # Marker size
    fill_color='red',
    line_color='black',
    fill_alpha=0.7,
    line_alpha=1.0,
    line_width=1
)

# Curve/Line styling
curve.opts(
    line_width=3,
    line_color='blue',
    line_dash='dashed',  # 'solid', 'dashed', 'dotted', 'dotdash', 'dashdot'
    line_alpha=0.8
)
```

### Colorbars

```python
plot.opts(
    colorbar=True,
    colorbar_position='right',  # 'right', 'left', 'top', 'bottom'
    colorbar_opts={
        'title': 'Value',
        'width': 15,
        'height': 300,
        'title_text_font_size': '12pt',
        'major_label_text_font_size': '10pt',
        'ticker': {'desired_num_ticks': 10}
    },
    clabel='Value (units)',  # Colorbar label
    symmetric=True           # Symmetric around 0
)
```

### Legends

```python
# Show legend
overlay = scatter1 * scatter2 * scatter3
overlay.opts(
    legend_position='top_right',  # Position
    legend_offset=(10, 10),       # Pixel offset
    legend_cols=3,                # Number of columns
    show_legend=True
)

# Custom legend labels
scatter.opts(label='Dataset A')

# Legend styling
overlay.opts(
    legend_opts={
        'background_fill_alpha': 0.8,
        'border_line_color': 'black',
        'label_text_font_size': '10pt'
    }
)
```

### Tools and Interaction

```python
plot.opts(
    tools=['hover', 'box_zoom', 'wheel_zoom', 'pan', 'reset', 'save'],
    active_tools=['wheel_zoom'],  # Active by default

    # Hover tool customization
    hover_tooltips=[
        ('X', '@x{0.00}'),
        ('Y', '@y{0.00}'),
        ('Value', '@value{0.00}')
    ],

    # Disable specific tools
    tools=[]  # No tools
)
```

## Themes and Styles

### Built-in Themes

```python
# Dark theme
hv.renderer('bokeh').theme = 'dark_minimal'

# Caliber theme
hv.renderer('bokeh').theme = 'caliber'

# Light minimal (default)
hv.renderer('bokeh').theme = 'light_minimal'
```

### Custom Theme

```python
from bokeh.themes import Theme

custom_theme = Theme(json={
    'attrs': {
        'Figure': {
            'background_fill_color': '#f8f9fa',
            'border_fill_color': '#ffffff',
            'outline_line_color': '#e9ecef',
        },
        'Grid': {
            'grid_line_color': '#dee2e6',
            'grid_line_alpha': 0.5,
        },
        'Title': {
            'text_color': '#212529',
            'text_font': 'helvetica',
            'text_font_size': '14pt',
        },
        'Axis': {
            'axis_line_color': '#495057',
            'major_tick_line_color': '#495057',
            'minor_tick_line_color': '#adb5bd',
            'major_label_text_color': '#495057',
            'axis_label_text_color': '#212529',
        },
    }
})

hv.renderer('bokeh').theme = custom_theme
```

### Consistent Styling Pattern

```python
# Define style constants
COLORS = {
    'primary': '#0173b2',
    'secondary': '#de8f05',
    'accent': '#029e73',
}

SIZES = {
    'small': 400,
    'medium': 600,
    'large': 800,
}

FONTS = {
    'title': 16,
    'labels': 12,
    'ticks': 10,
}

# Apply consistently
def styled_scatter(data, **kwargs):
    return hv.Scatter(data, 'x', 'y').opts(
        color=COLORS['primary'],
        width=SIZES['medium'],
        height=SIZES['medium'] // 2,
        fontsize=FONTS,
        **kwargs
    )
```

## Backend-Specific Options

### Bokeh Options

```python
import holoviews as hv
hv.extension('bokeh')

plot = hv.Scatter(data, 'x', 'y').opts(
    # Bokeh-specific
    backend='bokeh',
    tools=['hover', 'box_zoom'],
    active_tools=['wheel_zoom'],
    toolbar='above',  # 'above', 'below', 'left', 'right', None

    # Grid styling
    show_grid=True,
    gridstyle={
        'grid_line_color': 'gray',
        'grid_line_alpha': 0.3,
        'grid_line_width': 1
    },

    # Background
    bgcolor='white',
    border=10,  # Border padding
)
```

### Matplotlib Options

```python
import holoviews as hv
hv.extension('matplotlib')

plot = hv.Scatter(data, 'x', 'y').opts(
    # Matplotlib-specific
    backend='matplotlib',
    fig_size=200,  # Figure size (DPI * inches)
    aspect=2,      # Aspect ratio

    # Matplotlib styling
    style={
        'edgecolors': 'black',
        'linewidth': 0.5
    },

    # Tight layout
    fig_inches=(8, 4),
    tight=True
)
```

### Plotly Options

```python
import holoviews as hv
hv.extension('plotly')

plot = hv.Scatter(data, 'x', 'y').opts(
    # Plotly-specific
    backend='plotly',

    # Layout options
    width=800,
    height=400,
)
```

## Publication Quality

### High DPI Export

```python
# Save at high DPI
hv.save(plot, 'figure.png', dpi=300)

# SVG for vector graphics
hv.save(plot, 'figure.svg')

# PDF
hv.save(plot, 'figure.pdf')
```

### Publication Style

```python
# Publication-ready styling
pub_style = {
    'fontsize': {
        'title': 14,
        'labels': 12,
        'xticks': 10,
        'yticks': 10,
    },
    'width': 600,
    'height': 400,
    'bgcolor': 'white',
    'show_grid': True,
    'gridstyle': {
        'grid_line_color': '#cccccc',
        'grid_line_alpha': 0.5
    },
    'tools': [],  # No interactive tools
}

plot = hv.Scatter(data, 'x', 'y').opts(**pub_style)
```

### LaTeX Labels

```python
# Use LaTeX in labels (requires matplotlib backend)
hv.extension('matplotlib')

plot = hv.Curve(data, 'x', 'y').opts(
    xlabel=r'$\alpha$ (radians)',
    ylabel=r'$\beta^2$',
    title=r'Plot of $\beta^2$ vs $\alpha$'
)
```

### Multiple Subplots

```python
# Create publication-quality figure with subplots
from holoviews import opts

plot1 = hv.Scatter(data1, 'x', 'y').opts(title='A')
plot2 = hv.Curve(data2, 'x', 'y').opts(title='B')
plot3 = hv.Histogram(data3, 'value').opts(title='C')
plot4 = hv.BoxWhisker(data4, 'category', 'value').opts(title='D')

# 2x2 layout
layout = (plot1 + plot2 + plot3 + plot4).opts(
    opts.Scatter(width=300, height=300, tools=[]),
    opts.Curve(width=300, height=300, tools=[]),
    opts.Histogram(width=300, height=300, tools=[]),
    opts.BoxWhisker(width=300, height=300, tools=[])
).cols(2)

# Save
hv.save(layout, 'figure_panel.png', dpi=300)
```

## Advanced Patterns

### Conditional Styling

```python
# Style based on data
def color_by_value(value):
    return 'red' if value < 0 else 'blue'

scatter = hv.Scatter(data, 'x', 'y', vdims=['value']).opts(
    color=hv.dim('value').apply(color_by_value)
)
```

### Size by Dimension

```python
# Variable marker size
scatter = hv.Scatter(data, 'x', 'y', vdims=['size', 'value']).opts(
    size=hv.dim('size').norm() * 20,  # Scale to reasonable size
    color='value',
    cmap=cm['cet_fire']
)
```

### Custom Tooltips

```python
scatter = hv.Scatter(data, 'x', 'y', vdims=['name', 'value']).opts(
    tools=['hover'],
    hover_tooltips=[
        ('Name', '@name'),
        ('X', '@x{0.00}'),
        ('Y', '@y{0.00}'),
        ('Value', '@value{0,0.00}'),  # Format with commas
    ]
)
```

### Responsive Plots

```python
# Full width/height
plot.opts(
    responsive=True,
    min_width=400,
    max_width=1200
)

# Aspect-based sizing
plot.opts(
    aspect=2,  # Width = 2 * height
    frame_width=600  # Data area width
)
```

## Common Styling Recipes

### Clean Minimal Style

```python
minimal_style = dict(
    bgcolor='white',
    show_grid=False,
    toolbar=None,
    fontsize={'title': 14, 'labels': 11, 'xticks': 9, 'yticks': 9}
)

plot.opts(**minimal_style)
```

### Scientific Publication

```python
sci_style = dict(
    width=600,
    height=400,
    bgcolor='white',
    show_grid=True,
    gridstyle={'grid_line_color': '#e0e0e0', 'grid_line_alpha': 0.8},
    fontsize={'title': 12, 'labels': 11, 'xticks': 10, 'yticks': 10},
    tools=[],
    line_width=2,
    color='black'
)

plot.opts(**sci_style)
```

### Dashboard Style

```python
dash_style = dict(
    width=400,
    height=300,
    bgcolor='#f8f9fa',
    toolbar='above',
    tools=['hover', 'box_zoom', 'reset'],
    fontsize={'title': 13, 'labels': 11},
    cmap=cm['cet_fire']
)

plot.opts(**dash_style)
```

## Troubleshooting

### Options Not Applying

```python
# Ensure correct backend
hv.extension('bokeh')

# Check if option is valid for element type
help(hv.Scatter)

# Use backend-specific opts
plot.opts(backend='bokeh', width=600)
```

### Colormap Not Showing

```python
# Ensure dimension specified
scatter = hv.Scatter(data, 'x', 'y', vdims=['value']).opts(
    color='value',  # Must match vdim name
    cmap=cm['cet_fire'],
    colorbar=True
)
```

### Legend Issues

```python
# Ensure labels are set
overlay = (
    hv.Scatter(data1, 'x', 'y').opts(label='Dataset 1') *
    hv.Scatter(data2, 'x', 'y').opts(label='Dataset 2')
)
overlay.opts(legend_position='top_right', show_legend=True)
```

## Summary

**Key concepts**:
- Use `.opts()` for all styling
- Set global defaults with `hv.opts.defaults()`
- Choose appropriate colormaps from Colorcet
- Consider backend-specific options
- Test styling for publication/dashboard contexts

**Most common options**:
- `width`, `height`: Plot dimensions
- `color`, `cmap`: Color styling
- `xlabel`, `ylabel`, `title`: Labels
- `tools`, `hover_tooltips`: Interactivity
- `colorbar`: Show colorbar
- `legend_position`: Legend placement

**Best practices**:
- Define style constants
- Create reusable styling functions
- Test in target context (web, print, presentation)
- Use colorblind-safe colormaps
- Consider responsive sizing

## References

- [HoloViews Styling Guide](https://holoviews.org/user_guide/Styling_Plots.html)
- [Bokeh Styling](https://docs.bokeh.org/en/latest/docs/user_guide/styling.html)
- [Colorcet Documentation](https://colorcet.holoviz.org/)

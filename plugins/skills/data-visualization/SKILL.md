---
name: data-visualization
description: Master advanced declarative visualization with HoloViews. Use this skill when creating complex multi-dimensional visualizations, composing overlays and layouts, implementing interactive streams and selection, building network or hierarchical visualizations, or exploring data with dynamic maps and faceted displays.
compatibility: Requires holoviews >= 1.18.0, pandas >= 1.0.0, numpy >= 1.15.0, bokeh >= 3.0.0, networkx >= 2.0.0 (for network visualizations)
---

# Data Visualization Skill

## Overview

Master advanced declarative visualization with HoloViews and composition patterns. This skill covers sophisticated visualization techniques for complex data exploration and presentation.

## Dependencies

- holoviews >= 1.18.0
- pandas >= 1.0.0
- numpy >= 1.15.0
- bokeh >= 3.0.0
- networkx >= 2.0.0 (for network visualizations)

## Core Capabilities

### 1. Advanced Element Composition

HoloViews allows sophisticated composition of visualization elements:

```python
import holoviews as hv
from holoviews import opts
import pandas as pd
import numpy as np

# Create overlaid elements
curve = hv.Curve(df, 'x', 'y', label='Measured')
scatter = hv.Scatter(df_with_noise, 'x', 'y', label='Noisy')
overlay = curve * scatter  # Multiplication overlays

# Create layouts
col_layout = hv.Column(plot1, plot2, plot3)
row_layout = hv.Row(plot1, plot2, plot3)
grid_layout = hv.GridMatrix(data_dict)

# Faceted displays
faceted = hv.Curve(df, 'date', 'value').facet('category')

# Nested layouts
complex_layout = hv.Column(
    hv.Row(plot1, plot2),
    hv.Row(plot3, plot4),
    hv.Row(plot5, plot6)
)
```

### 2. Interactive Streams and Selection

Create responsive visualizations with interactive selection:

```python
from holoviews import streams

# Selection stream
range_stream = streams.RangeXY()
scatter = hv.Scatter(df, 'x', 'y').opts(tools=['box_select'])

@hv.transform
def selected_data(data):
    if range_stream.selection:
        x0, x1 = range_stream.selection[0], range_stream.selection[1]
        y0, y1 = range_stream.selection[2], range_stream.selection[3]
        mask = (data['x'] >= x0) & (data['x'] <= x1) & \
               (data['y'] >= y0) & (data['y'] <= y1)
        return data[mask]
    return data

histogram = selected_data.to(hv.Histogram)
scatter_with_hist = scatter + histogram
```

### 3. Dynamic Maps for Responsive Visualization

```python
# Dynamic updating based on parameters
from holoviews import DynamicMap, streams

def plot_by_category(category):
    data = df[df['category'] == category]
    return hv.Scatter(data, 'x', 'y', title=f'Category: {category}')

category_stream = streams.Stream.define('category', category='A')
dmap = DynamicMap(plot_by_category, streams=[category_stream])

# Parameterized dynamic map
def plot_with_params(threshold=0.5):
    filtered = df[df['value'] > threshold]
    return hv.Scatter(filtered, 'x', 'y')

dmap_param = DynamicMap(
    plot_with_params,
    streams=[streams.Stream.define('threshold', threshold=0.5)]
)
```

### 4. Network and Hierarchical Visualizations

```python
import networkx as nx

# Network graph
G = nx.karate_club_graph()
pos = nx.spring_layout(G)
edges = [(u, v) for u, v in G.edges()]
nodes = list(G.nodes())

# Create nodes and edges visualization
edge_plot = hv.Segments(edges, kdims=['source', 'target'])
node_plot = hv.Scatter(
    [(pos[n][0], pos[n][1], n) for n in nodes],
    kdims=['x', 'y', 'node']
)
network = (edge_plot * node_plot).opts(
    opts.Scatter(size=100, color='red'),
    opts.Segments(color='gray')
)

# Treemap for hierarchical data
treemap = hv.TreeMap(
    hierarchical_data,
    label='Organization'
).opts(tools=['hover'])
```

### 5. Statistical and Aggregate Visualizations

```python
# Aggregate with Rasterize
from holoviews.operation import datashader as dshade

# Box plot for comparison
box_plot = hv.BoxWhisker(df, kdims=['category'], vdims=['value'])

# Violin plot
violin = hv.Violin(df, kdims=['category'], vdims=['value'])

# Distribution comparison
dist_layout = hv.Column(*[
    df[df['category'] == cat]['value'].hvplot.hist()
    for cat in df['category'].unique()
])
```

### 6. Multi-Dimensional Data Exploration

```python
# HoloMap for multi-dimensional data
def plot_by_params(category, metric):
    data = df[(df['category'] == category) & (df['metric'] == metric)]
    return hv.Scatter(data, 'x', 'y', title=f'{category} - {metric}')

hmap = hv.HoloMap(
    {(cat, met): plot_by_params(cat, met)
     for cat in categories for met in metrics},
    kdims=['Category', 'Metric']
)

# NdLayout for structured multi-dimensional display
ndlayout = hv.NdLayout({
    (cat, met): plot_by_params(cat, met)
    for cat in categories for met in metrics
}, kdims=['Category', 'Metric'])
```

## Advanced Styling and Theming

### 1. Global Options

```python
# Set global defaults
opts.defaults(
    opts.Curve(width=700, height=400, responsive=True),
    opts.Scatter(size=100, alpha=0.5),
    opts.Image(cmap='viridis')
)

# Apply to multiple elements
styled_plots = [
    plot.opts(
        title='Styled Plot',
        xlabel='X Axis',
        ylabel='Y Axis',
        toolbar='right',
        active_tools=['pan', 'wheel_zoom']
    )
    for plot in plots
]
```

### 2. Custom Styling

```python
# Element-specific styling
plot = hv.Scatter(df, 'x', 'y').opts(
    color=hv.dim('category').categorize({
        'A': '#FF6B6B',
        'B': '#4ECDC4',
        'C': '#45B7D1'
    }),
    size=hv.dim('value').norm(min=10, max=100),
    selection_color='red',
    nonselection_alpha=0.1
)

# Conditional formatting
plot.opts(
    color=hv.dim('status').categorize({
        'good': 'green',
        'warning': 'orange',
        'error': 'red'
    })
)
```

### 3. Interactive Legends and Annotations

```python
# Annotations
annotated_plot = hv.Curve(df, 'x', 'y')
annotations = [
    hv.Text(x, y, text, fontsize=10)
    for x, y, text in annotations_data
]
plot_with_annotations = annotated_plot * hv.Overlay(annotations)

# Custom legend
plot = hv.Overlay([
    hv.Curve(df1, label='Series 1'),
    hv.Curve(df2, label='Series 2'),
    hv.Curve(df3, label='Series 3')
]).opts(
    legend_position='top_left',
    legend_muted_alpha=0.2
)
```

## Best Practices

### 1. Performance with Large Datasets
```python
# Use rasterize for dense plots
from holoviews.operation import rasterize

large_scatter = hv.Scatter(large_df, 'x', 'y')
rasterized = rasterize(large_scatter, pixel_ratio=2)

# Use aggregation
aggregated = df.groupby('category')['value'].mean().hvplot.bar()

# Use datashader for massive datasets (>100M points)
from holoviews.operation.datashader import datashade
dshaded = datashade(large_scatter)
```

### 2. Responsive and Accessible Plots
```python
# Responsive sizing
plot = hv.Scatter(df, 'x', 'y').opts(
    responsive=True,
    sizing_mode='stretch_width'
)

# Accessible color palettes
plot = hv.Scatter(df, 'x', 'y').opts(
    color=hv.dim('value').norm(),
    cmap='cet_gray_r'  # Perceptually uniform
)

# Clear labels
plot.opts(
    title='Clear Title',
    xlabel='Independent Variable (units)',
    ylabel='Dependent Variable (units)',
    fontsize=14
)
```

### 3. Composition Patterns

```python
# Avoid deep nesting
# Bad: ((a + (b + (c + d)))
# Good: a + b + c + d

# Create helper functions
def create_comparison_layout(data_dict):
    plots = [hv.Scatter(v, label=k) for k, v in data_dict.items()]
    return hv.Column(*plots)

# Modular composition
sidebar = hv.Column(title_text, filter_widget)
main = hv.Row(plot1, plot2)
app = hv.Column(sidebar, main)
```

## Common Patterns

### Pattern 1: Linked Brushing
```python
def create_linked_views(df):
    scatter = hv.Scatter(df, 'x', 'y').opts(tools=['box_select'])

    def get_histogram(selection):
        if selection:
            selected_df = df.iloc[selection.event.inds]
        else:
            selected_df = df
        return hv.Histogram(selected_df['x'], bins=20)

    return scatter + DynamicMap(get_histogram, streams=[streams.Selection1D()])
```

### Pattern 2: Multi-Scale Exploration
```python
def create_zoomable_view(df):
    scatter = hv.Scatter(df, 'x', 'y')
    zoomed = scatter.opts(
        xlim=(0, 10),
        ylim=(0, 10)
    )
    return hv.Column(scatter, zoomed)
```

### Pattern 3: Faceted Analysis
```python
def create_faceted_analysis(df, facet_col):
    return df.hvplot.scatter(
        x='x',
        y='y',
        by=facet_col,
        subplots=True,
        layout='vertical'
    )
```

## Integration with Other HoloViz Tools

- **Panel**: Embed interactive HoloViews in dashboards
- **hvPlot**: Quick plotting that produces HoloViews objects
- **Datashader**: Efficient rendering for large data
- **Param**: Parameter-driven dynamic visualizations
- **GeoViews**: Geographic data visualization building on HoloViews

## Common Use Cases

1. **Exploratory Data Analysis**: Multi-dimensional data exploration
2. **Dashboard Metrics**: KPI and metric visualization
3. **Scientific Visualization**: Complex data relationships
4. **Financial Analysis**: Time series and correlation analysis
5. **Report Generation**: Publication-quality visualizations
6. **Real-time Monitoring**: Streaming data visualization

## Troubleshooting

### Issue: Plot Elements Overlapping
- Use layouts instead of overlays for clarity
- Adjust alpha transparency
- Use complementary colors

### Issue: Slow Interactive Performance
- Use rasterize for dense plots
- Reduce data size with aggregation
- Use datashader for massive datasets
- Cache plot computations

### Issue: Unclear Data Relationships
- Use multiple linked views
- Apply faceting for categorical comparison
- Use color and size encoding
- Add annotations and reference lines

## Resources

- [HoloViews Reference](https://holoviews.org/reference/index.html)
- [HoloViews User Guide](https://holoviews.org/user_guide/index.html)
- [Bokeh for Customization](https://docs.bokeh.org)
- [Datashader for Performance](https://datashader.org)

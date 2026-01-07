# Lumen Views Reference

## Overview

Complete reference for visualization types in Lumen dashboards. Covers plots, tables, indicators, and custom views.

**When to use this reference**:
- Choosing visualization types
- Configuring view options
- Creating KPI indicators
- Building custom views

## Table of Contents

1. [View Types](#view-types)
2. [hvPlot Views](#hvplot-views)
3. [Tables](#tables)
4. [Indicators](#indicators)
5. [Other View Types](#other-view-types)
6. [View Configuration](#view-configuration)

## View Types

### Available Views

| View Type | Purpose | Best For |
|-----------|---------|----------|
| `hvplot` | Interactive plots | Most visualizations |
| `table` | Data tables | Detailed data display |
| `indicator` | KPI metrics | Single values, progress |
| `altair` | Altair charts | Grammar of graphics |
| `plotly` | Plotly charts | Interactive 3D plots |
| `vega` | Vega-Lite specs | Declarative charts |
| `markdown` | Formatted text | Documentation, labels |
| `string` | Plain text | Simple text display |

## hvPlot Views

### Basic hvPlot

```yaml
views:
  - type: hvplot
    pipeline: main
    kind: scatter  # Plot type
    x: price
    y: quantity
    title: Price vs Quantity
```

### Plot Types (kind)

**Common plot types**:

```yaml
views:
  # Scatter plot
  - type: hvplot
    pipeline: main
    kind: scatter
    x: x_col
    y: y_col

  # Line plot
  - type: hvplot
    kind: line
    x: date
    y: value

  # Bar chart
  - type: hvplot
    kind: bar
    x: category
    y: value

  # Histogram
  - type: hvplot
    kind: hist
    y: value
    bins: 20

  # Box plot
  - type: hvplot
    kind: box
    y: value
    by: category

  # Heatmap
  - type: hvplot
    kind: heatmap
    x: x_cat
    y: y_cat
    C: value

  # Area plot
  - type: hvplot
    kind: area
    x: date
    y: value
    stacked: true
```

### hvPlot Options

```yaml
views:
  - type: hvplot
    pipeline: main
    kind: scatter

    # Data mapping
    x: column_x
    y: column_y
    by: category  # Color by category

    # Styling
    color: blue
    size: 10
    alpha: 0.7
    cmap: fire  # Colormap

    # Dimensions
    width: 600
    height: 400
    responsive: true

    # Labels
    title: My Plot
    xlabel: X Axis
    ylabel: Y Axis

    # Interactivity
    tools: ['hover', 'box_zoom']
    hover_cols: ['name', 'value']

    # Colorbar
    colorbar: true
    clim: [0, 100]  # Color limits

    # Legend
    legend: top_right
    show_legend: true
```

### Advanced hvPlot

```yaml
views:
  # Time series with options
  - type: hvplot
    pipeline: time_series
    kind: line
    x: date
    y: value
    by: category

    # Styling
    line_width: 2
    line_dash: 'dashed'

    # Interactive
    tools: ['hover']
    hover_tooltips: [
      ['Date', '@date{%F}'],
      ['Value', '@value{0.00}']
    ]

  # Grouped bar chart
  - type: hvplot
    pipeline: grouped_data
    kind: bar
    x: month
    y: revenue
    by: region
    stacked: false  # Side-by-side bars

  # Scatter with color and size
  - type: hvplot
    pipeline: scatter_data
    kind: scatter
    x: price
    y: sales
    c: profit  # Color by profit
    s: quantity  # Size by quantity
    cmap: coolwarm
    colorbar: true
```

## Tables

### Basic Table

```yaml
views:
  - type: table
    pipeline: main
    page_size: 20  # Rows per page
    pagination: remote  # or 'local'
```

### Table Configuration

```yaml
views:
  - type: table
    pipeline: main

    # Pagination
    page_size: 50
    pagination: remote  # Faster for large data

    # Selection
    selectable: true  # Enable row selection
    selection_mode: multiple  # or 'single'

    # Formatting
    formatters:
      revenue: '${value:,.2f}'
      quantity: '{value:,d}'
      date: '{value:%Y-%m-%d}'

    # Column configuration
    widths:
      name: 200
      revenue: 100
      date: 120

    # Frozen columns
    frozen_columns: ['name']  # Keep visible when scrolling

    # Row styling
    row_height: 30

    # Filtering
    filterable: true
```

### Table with Custom Columns

```yaml
views:
  - type: table
    pipeline: main

    # Show specific columns
    columns: ['date', 'region', 'revenue', 'quantity']

    # Column titles
    titles:
      region: Region Name
      revenue: Total Revenue

    # Formatters
    formatters:
      revenue: '${value:,.0f}'
      date: '{value:%b %d, %Y}'

    # Editors (make editable)
    editors:
      quantity: int
      notes: str
```

## Indicators

### Number Indicator

```yaml
views:
  # Simple number
  - type: indicator
    pipeline: kpi
    field: total_revenue
    title: Total Revenue
    format: '${value:,.0f}'

  # With color coding
  - type: indicator
    pipeline: kpi
    field: growth_rate
    title: Growth Rate
    format: '{value:.1f}%'
    colors: [
      [0, 'red'],      # < 0%: red
      [2, 'orange'],   # 0-2%: orange
      [5, 'green']     # > 5%: green
    ]
```

### Gauge Indicator

```yaml
views:
  - type: indicator
    pipeline: kpi
    field: completion
    title: Project Completion
    format: '{value:.0f}%'

    # Gauge styling
    bounds: [0, 100]
    colors: [
      [30, 'red'],
      [70, 'orange'],
      [100, 'green']
    ]

    # Gauge appearance
    annulus_width: 10
```

### Progress Indicator

```yaml
views:
  - type: indicator
    pipeline: progress
    field: percent_complete
    title: Progress
    format: '{value:.0f}%'

    # Progress bar styling
    bar_color: green
    max: 100
```

### Multiple Indicators

```yaml
views:
  # Row of KPI cards
  - type: indicator
    pipeline: metrics
    field: total_revenue
    title: Revenue
    format: '${value:,.0f}'

  - type: indicator
    pipeline: metrics
    field: order_count
    title: Orders
    format: '{value:,d}'

  - type: indicator
    pipeline: metrics
    field: avg_order_value
    title: Avg Order
    format: '${value:.2f}'
```

## Other View Types

### Markdown View

```yaml
views:
  - type: markdown
    pipeline: main
    object: |
      ## Analysis Summary

      This dashboard shows **sales performance** across regions.

      Key findings:
      - North region leads in revenue
      - Q4 shows strongest growth
      - Customer retention improved 15%
```

### String View

```yaml
views:
  - type: string
    pipeline: status
    field: message
    title: Status
```

### Altair View

```yaml
views:
  - type: altair
    pipeline: main

    spec:
      mark: point
      encoding:
        x: {field: price, type: quantitative}
        y: {field: quantity, type: quantitative}
        color: {field: category, type: nominal}
```

### Plotly View

```yaml
views:
  - type: plotly
    pipeline: main

    # Plotly figure configuration
    kind: scatter3d
    x: x_col
    y: y_col
    z: z_col
    color: category
```

### Vega-Lite View

```yaml
views:
  - type: vega
    pipeline: main

    spec:
      $schema: https://vega.github.io/schema/vega-lite/v5.json
      mark: bar
      encoding:
        x: {field: category, type: nominal}
        y: {field: value, type: quantitative}
```

## View Configuration

### Layout Sizing

```yaml
views:
  - type: hvplot
    pipeline: main
    kind: scatter

    # Fixed size
    width: 600
    height: 400

    # Responsive
    responsive: true
    min_width: 400
    max_width: 1200

    # Aspect ratio
    aspect: 2  # width / height
```

### Styling

```yaml
views:
  - type: hvplot
    pipeline: main
    kind: line

    # Colors
    color: '#0173b2'
    cmap: fire  # For color dimension

    # Line styling
    line_width: 3
    line_dash: 'dashed'

    # Marker styling
    marker: 'circle'
    size: 10
    alpha: 0.7

    # Axes
    logx: false
    logy: false
    xlim: [0, 100]
    ylim: [0, 1000]

    # Grid
    grid: true
    gridstyle: {
      'grid_line_color': 'gray',
      'grid_line_alpha': 0.3
    }
```

### Interactivity

```yaml
views:
  - type: hvplot
    pipeline: main
    kind: scatter

    # Tools
    tools: ['hover', 'box_zoom', 'wheel_zoom', 'pan', 'reset']
    active_tools: ['wheel_zoom']

    # Hover tooltips
    hover_cols: ['name', 'category', 'value']
    hover_tooltips: [
      ['Name', '@name'],
      ['Value', '@value{0.00}']
    ]

    # Selection
    selection_group: 'my_group'  # For cross-filtering
```

### Cross-Filtering

```yaml
views:
  # Bar chart that filters other views
  - type: hvplot
    pipeline: main
    kind: bar
    x: category
    y: revenue
    selection_group: category_filter

  # Scatter that responds to selection
  - type: hvplot
    pipeline: main
    kind: scatter
    x: price
    y: quantity
    selection_group: category_filter  # Same group
```

## View Patterns

### Pattern 1: KPI Dashboard

```yaml
layouts:
  - title: KPIs
    layout: [[0, 1, 2]]  # Row of 3 indicators
    views:
      - type: indicator
        pipeline: metrics
        field: revenue
        title: Total Revenue
        format: '${value:,.0f}'

      - type: indicator
        pipeline: metrics
        field: orders
        title: Total Orders
        format: '{value:,d}'

      - type: indicator
        pipeline: metrics
        field: avg_value
        title: Avg Order Value
        format: '${value:.2f}'
```

### Pattern 2: Chart and Table

```yaml
layouts:
  - title: Analysis
    views:
      # Main chart
      - type: hvplot
        pipeline: main
        kind: line
        x: date
        y: revenue
        by: region
        title: Revenue Over Time

      # Supporting table
      - type: table
        pipeline: main
        page_size: 20
        columns: ['date', 'region', 'revenue', 'orders']
```

### Pattern 3: Multi-Chart Dashboard

```yaml
layouts:
  - title: Overview
    layout: [[0, 1], [2, 3]]  # 2x2 grid
    views:
      # Top left
      - type: hvplot
        pipeline: summary
        kind: bar
        x: region
        y: revenue
        title: Revenue by Region

      # Top right
      - type: hvplot
        pipeline: summary
        kind: line
        x: date
        y: orders
        title: Orders Over Time

      # Bottom left
      - type: hvplot
        pipeline: summary
        kind: scatter
        x: price
        y: quantity
        title: Price vs Quantity

      # Bottom right
      - type: table
        pipeline: summary
        page_size: 10
```

## Best Practices

### 1. Choose Appropriate View Types

```yaml
# ✅ Good: Right view for data type
views:
  # Time series → line
  - type: hvplot
    kind: line
    x: date
    y: value

  # Categories → bar
  - type: hvplot
    kind: bar
    x: category
    y: count

  # Distribution → histogram
  - type: hvplot
    kind: hist
    y: values
    bins: 20

  # KPIs → indicators
  - type: indicator
    field: metric
    format: '{value:,.0f}'
```

### 2. Responsive Sizing

```yaml
# ✅ Good: Responsive views
views:
  - type: hvplot
    pipeline: main
    kind: scatter
    responsive: true
    min_width: 400
    max_width: 1200

# ❌ Bad: Fixed small size
views:
  - type: hvplot
    pipeline: main
    kind: scatter
    width: 400  # Too small on large screens
```

### 3. Clear Labels

```yaml
# ✅ Good: Descriptive labels
views:
  - type: hvplot
    pipeline: main
    kind: line
    x: date
    y: revenue
    title: Monthly Revenue Trend
    xlabel: Date
    ylabel: Revenue ($)

# ❌ Bad: No labels
views:
  - type: hvplot
    pipeline: main
    kind: line
    x: date
    y: revenue
```

### 4. Format Numbers

```yaml
# ✅ Good: Formatted indicators
views:
  - type: indicator
    field: revenue
    title: Revenue
    format: '${value:,.2f}'  # $1,234.56

# ❌ Bad: Raw numbers
views:
  - type: indicator
    field: revenue
    title: Revenue
    # Shows: 1234.56789
```

## Troubleshooting

### View Not Showing

```yaml
# Problem: View doesn't display
# Solution: Check pipeline and field names

views:
  - type: hvplot
    pipeline: main  # Must match pipeline name
    kind: scatter
    x: col_x  # Must exist in data
    y: col_y  # Must exist in data
```

### Performance Issues

```yaml
# Problem: Large table is slow
# Solution: Use remote pagination

views:
  - type: table
    pipeline: large_data
    page_size: 50
    pagination: remote  # Faster for large data

# Or limit data in transform
transforms:
  - type: head
    n: 10000  # Limit rows
```

### Indicator Shows No Data

```yaml
# Problem: Indicator is empty
# Solution: Verify aggregation

pipelines:
  metrics:
    source: data
    table: sales

    transforms:
      - type: aggregate
        aggregate:
          total: {revenue: sum}  # Creates 'total' field

views:
  - type: indicator
    pipeline: metrics
    field: total  # Must match aggregated field name
```

## Summary

**Key concepts**:
- Multiple view types for different data
- hvPlot for most visualizations
- Tables for detailed data
- Indicators for KPIs
- Configure sizing and styling

**Most common views**:
- `hvplot`: Interactive plots (scatter, line, bar, etc.)
- `table`: Data tables
- `indicator`: KPI metrics

**Best practices**:
- Choose appropriate plot types
- Use responsive sizing
- Format numbers clearly
- Add descriptive labels
- Enable appropriate interactivity

## References

- [Lumen Views Documentation](https://lumen.holoviz.org/user_guide/Views.html)
- [hvPlot Reference](https://hvplot.holoviz.org/reference/index.html)
- [Panel Indicators](https://panel.holoviz.org/reference/index.html#indicators)
- [Altair Documentation](https://altair-viz.github.io/)
- [Plotly Python](https://plotly.com/python/)

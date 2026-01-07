# Lumen Layouts Reference

## Overview

Guide to organizing views in Lumen dashboard layouts including grid layouts, tabs, and responsive design.

**When to use this reference**:
- Organizing dashboard views
- Creating multi-page dashboards
- Designing responsive layouts

## Table of Contents

1. [Layout Basics](#layout-basics)
2. [Grid Layouts](#grid-layouts)
3. [Tabs](#tabs)
4. [Responsive Design](#responsive-design)
5. [Layout Patterns](#layout-patterns)

## Layout Basics

### Simple Layout

```yaml
layouts:
  - title: Dashboard
    views:
      - type: indicator
        pipeline: metrics
        field: revenue

      - type: hvplot
        pipeline: main
        kind: line
        x: date
        y: value
```

### Layout with Explicit Grid

```yaml
layouts:
  - title: Dashboard
    layout: [[0], [1]]  # View 0 in row 1, view 1 in row 2
    views:
      - type: indicator
        pipeline: metrics
        field: revenue

      - type: hvplot
        pipeline: main
        kind: line
```

## Grid Layouts

### Grid Positioning

```yaml
layouts:
  - title: Grid Layout
    # Format: [[row1_views], [row2_views], ...]
    layout: [[0, 1, 2], [3, 4]]  # 3 views in row 1, 2 in row 2

    views:
      # Row 1
      - type: indicator  # Position 0
      - type: indicator  # Position 1
      - type: indicator  # Position 2

      # Row 2
      - type: hvplot     # Position 3
      - type: table      # Position 4
```

### 2x2 Grid

```yaml
layouts:
  - title: 2x2 Dashboard
    layout: [[0, 1], [2, 3]]

    views:
      - type: hvplot
        title: Top Left

      - type: hvplot
        title: Top Right

      - type: table
        title: Bottom Left

      - type: table
        title: Bottom Right
```

### Unequal Column Widths

```yaml
layouts:
  - title: Custom Widths
    # Wider chart, narrower sidebar
    layout: [[0, 1]]

    views:
      - type: hvplot
        pipeline: main
        width: 800  # Wider

      - type: markdown
        width: 200  # Narrower sidebar
```

## Tabs

### Multi-Tab Dashboard

```yaml
layouts:
  # Tab 1: Overview
  - title: Overview
    views:
      - type: indicator
      - type: hvplot

  # Tab 2: Details
  - title: Details
    views:
      - type: table

  # Tab 3: Analysis
  - title: Analysis
    views:
      - type: hvplot
      - type: hvplot
```

### Tabs with Grid Layouts

```yaml
layouts:
  # Tab 1: KPIs
  - title: KPIs
    layout: [[0, 1, 2], [3]]
    views:
      - type: indicator
      - type: indicator
      - type: indicator
      - type: hvplot

  # Tab 2: Data Table
  - title: Data
    views:
      - type: table
        page_size: 50
```

## Responsive Design

### Responsive Views

```yaml
layouts:
  - title: Responsive Dashboard
    views:
      - type: hvplot
        pipeline: main
        kind: line
        responsive: true  # Fills container width
        min_width: 400
        max_width: 1200

      - type: table
        pipeline: main
        responsive: true
```

### Sizing Modes

```yaml
views:
  - type: hvplot
    pipeline: main
    kind: scatter
    sizing_mode: stretch_width  # Options:
    # - fixed: Use width/height
    # - stretch_width: Fill width, fixed height
    # - stretch_both: Fill width and height
    # - scale_width: Scale to width, maintain aspect
    # - scale_both: Scale to both, maintain aspect
```

## Layout Patterns

### Pattern 1: KPI Dashboard

```yaml
layouts:
  - title: KPIs
    layout: [[0, 1, 2], [3, 4]]
    views:
      # Top row: 3 KPI cards
      - type: indicator
        field: revenue
        title: Revenue

      - type: indicator
        field: orders
        title: Orders

      - type: indicator
        field: avg_value
        title: Avg Order

      # Bottom row: Charts
      - type: hvplot
        kind: line
        title: Trend

      - type: hvplot
        kind: bar
        title: By Category
```

### Pattern 2: Filters + Content

```yaml
config:
  layout: column  # Vertical layout

layouts:
  - title: Dashboard
    layout: [[0], [1, 2]]
    views:
      # Filters at top
      - type: markdown
        object: "## Filters"

      # Content below
      - type: hvplot
        title: Chart

      - type: table
        title: Data
```

### Pattern 3: Master-Detail

```yaml
layouts:
  - title: Master-Detail
    layout: [[0], [1]]
    views:
      # Summary chart
      - type: hvplot
        pipeline: summary
        kind: bar
        title: Summary
        selection_group: detail

      # Detail table (filtered by selection)
      - type: table
        pipeline: detail
        selection_group: detail
```

### Pattern 4: Multi-Tab Analysis

```yaml
layouts:
  # Tab 1: Executive Summary
  - title: Summary
    layout: [[0, 1, 2], [3]]
    views:
      - type: indicator
      - type: indicator
      - type: indicator
      - type: hvplot

  # Tab 2: Regional Analysis
  - title: By Region
    views:
      - type: hvplot
        by: region

  # Tab 3: Time Series
  - title: Trends
    views:
      - type: hvplot
        kind: line
        x: date

  # Tab 4: Raw Data
  - title: Data
    views:
      - type: table
        page_size: 100
```

## Best Practices

### 1. Logical Organization

```yaml
# ✅ Good: Related views together
layouts:
  - title: Sales Dashboard
    layout: [[0, 1], [2]]
    views:
      - type: indicator     # KPI
      - type: indicator     # Related KPI
      - type: hvplot        # Supporting chart

# ❌ Bad: Random organization
layouts:
  - title: Dashboard
    views:
      - type: table         # Detail table first?
      - type: indicator     # KPI buried
```

### 2. Progressive Disclosure

```yaml
# ✅ Good: Overview → Details via tabs
layouts:
  - title: Overview      # High-level summary
    views: [...]

  - title: Details       # Detailed analysis
    views: [...]

  - title: Raw Data      # Full data table
    views: [...]
```

### 3. Responsive Design

```yaml
# ✅ Good: Responsive views
views:
  - type: hvplot
    responsive: true
    min_width: 400

# ❌ Bad: Fixed tiny width
views:
  - type: hvplot
    width: 300  # Too small on large screens
```

### 4. Balanced Layouts

```yaml
# ✅ Good: Balanced 2x2
layout: [[0, 1], [2, 3]]

# ❌ Bad: Unbalanced
layout: [[0, 1, 2, 3]]  # 4 cramped columns
```

## Troubleshooting

### Views Not Aligning

```yaml
# Problem: Views don't align in grid
# Solution: Ensure consistent sizing

views:
  - type: hvplot
    height: 400  # Same height

  - type: hvplot
    height: 400  # Same height
```

### Layout Not Responsive

```yaml
# Problem: Layout doesn't resize
# Solution: Use responsive sizing

config:
  sizing_mode: stretch_width

views:
  - type: hvplot
    responsive: true
```

## Summary

**Key concepts**:
- Organize views with explicit grid layouts
- Use tabs for multi-page dashboards
- Enable responsive sizing
- Follow logical organization patterns

**Layout patterns**:
- KPI dashboard: Row of indicators + charts
- Filters + content: Vertical layout
- Master-detail: Summary + details
- Multi-tab: Separate concerns into tabs

**Best practices**:
- Group related views
- Use progressive disclosure (tabs)
- Enable responsive design
- Balance layout proportions

## References

- [Lumen Layouts Documentation](https://lumen.holoviz.org/user_guide/Layouts.html)
- [Panel Layout Guide](https://panel.holoviz.org/user_guide/Components.html)

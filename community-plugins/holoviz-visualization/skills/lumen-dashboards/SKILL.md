---
name: lumen-dashboards
description: Master declarative, no-code data dashboards with Lumen YAML specifications. Use this skill when building standard data exploration dashboards, connecting multiple data sources (files, databases, APIs), creating interactive filters and cross-filtering, designing responsive layouts with indicators and charts, or enabling rapid dashboard prototyping without writing code.
version: 2025-01-07
compatibility: Requires lumen >= 0.10.0, panel >= 1.3.0, holoviews >= 1.18.0, param >= 2.0.0. Supports PostgreSQL, DuckDB, SQLite, CSV, Parquet, Excel, and REST API data sources.
---

# Lumen Dashboards Skill

## Overview

Lumen is a declarative framework for creating data dashboards through YAML specifications. Build interactive data exploration dashboards without writing code.

### Key Features

- **No-code dashboards**: Define everything in YAML
- **Data pipelines**: Sources → Transforms → Views
- **Interactive exploration**: Built-in filters and cross-filtering
- **Component library**: Reusable sources, transforms, views
- **Live updates**: Auto-reload and real-time data

### When to Use Lumen

| Feature | Lumen Dashboards | Panel | Lumen AI |
|---------|------------------|-------|----------|
| **Approach** | Declarative YAML | Imperative Python | Conversational |
| **Code Required** | No | Yes | No |
| **Use Case** | Fixed dashboards | Custom apps | Ad-hoc exploration |

**Use Lumen when**: Building standard dashboards, working with non-programmers, rapid prototyping.

**Use Panel when**: Need fine-grained control, custom logic, novel interactions.

## Quick Start

### Installation

```bash
pip install lumen
```

### Your First Dashboard

**File: `dashboard.yaml`**

```yaml
sources:
  data:
    type: file
    tables:
      penguins: https://datasets.holoviz.org/penguins/v1/penguins.csv

pipelines:
  main:
    source: data
    table: penguins
    filters:
      - type: widget
        field: species

layouts:
  - title: Penguin Explorer
    views:
      - type: hvplot
        pipeline: main
        kind: scatter
        x: bill_length_mm
        y: bill_depth_mm
        by: species
```

**Launch:**
```bash
lumen serve dashboard.yaml --show
```

## Core Concepts

### 1. Sources

Data sources provide tables for your dashboard.

**Supported sources**: File (CSV, Parquet, Excel, JSON), Database (PostgreSQL, DuckDB, SQLite), REST API, Intake catalogs.

```yaml
sources:
  mydata:
    type: file
    tables:
      sales: ./data/sales.csv
```

**See**: [Data Sources Reference](../../references/lumen-dashboards/sources.md)

### 2. Pipelines

Pipelines define data flows: Source → Filters → Transforms → Views

```yaml
pipelines:
  sales_pipeline:
    source: mydata
    table: sales
    filters:
      - type: widget
        field: region
    transforms:
      - type: aggregate
        by: ['category']
        aggregate:
          total_sales: {revenue: sum}
```

### 3. Filters

Add interactive controls:

```yaml
filters:
  - type: widget
    field: category          # Dropdown select

  - type: widget
    field: region
    multiple: true           # Multi-select

  - type: widget
    field: date
    widget: date_range_slider  # Date range
```

### 4. Transforms

Process data in pipelines:

```yaml
transforms:
  - type: columns
    columns: ['date', 'region', 'revenue']

  - type: query
    query: "revenue > 1000"

  - type: aggregate
    by: ['region']
    aggregate:
      total: {revenue: sum}
```

**See**: [Data Transforms Reference](../../references/lumen-dashboards/transforms.md)

### 5. Views

Visualize data with various chart types:

```yaml
views:
  - type: hvplot
    pipeline: main
    kind: line
    x: date
    y: revenue
    by: category

  - type: indicator
    pipeline: main
    field: total_revenue
    format: '${value:,.0f}'

  - type: table
    pipeline: main
    page_size: 20
```

**See**: [Views Reference](../../references/lumen-dashboards/views.md)

### 6. Layouts

Arrange views on the page:

```yaml
layouts:
  - title: Overview
    layout: [[0, 1, 2], [3], [4, 5]]  # Grid positions
    views:
      - type: indicator
        # View configs...
```

**See**: [Layouts Reference](../../references/lumen-dashboards/layouts.md)

## Common Patterns

### Pattern 1: KPI Dashboard

```yaml
pipelines:
  kpis:
    source: metrics
    table: data
    transforms:
      - type: aggregate
        aggregate:
          total_revenue: {revenue: sum}
          total_orders: {orders: sum}

layouts:
  - title: KPIs
    layout: [[0, 1, 2]]
    views:
      - type: indicator
        pipeline: kpis
        field: total_revenue
        format: '${value:,.0f}'
      - type: indicator
        pipeline: kpis
        field: total_orders
        format: '{value:,.0f}'
```

### Pattern 2: Filtered Exploration

```yaml
pipelines:
  explorer:
    source: mydata
    table: sales
    filters:
      - type: widget
        field: region
      - type: widget
        field: category
        multiple: true
    views:
      - type: hvplot
        kind: scatter
        x: price
        y: quantity
      - type: table
        page_size: 20
```

### Pattern 3: Cross-Filtering

```yaml
layouts:
  - title: Analysis
    views:
      - type: hvplot
        pipeline: main
        kind: bar
        x: category
        y: revenue
        selection_group: category_filter

      - type: hvplot
        pipeline: main
        kind: scatter
        x: price
        y: quantity
        selection_group: category_filter
```

### Pattern 4: SQL Transform

```yaml
transforms:
  - type: sql
    query: |
      SELECT region, category,
        SUM(revenue) as total_revenue,
        COUNT(*) as order_count
      FROM table
      WHERE date >= '2024-01-01'
      GROUP BY region, category
      ORDER BY total_revenue DESC
```

**See**: [Examples](../../references/lumen-dashboards/examples.md) for complete dashboard examples.

## Python API

While Lumen is designed for YAML, you can also use Python:

```python
from lumen.sources import FileSource
from lumen.pipeline import Pipeline
from lumen.views import hvPlotView
from lumen.dashboard import Dashboard

source = FileSource(tables={'sales': './data/sales.csv'})
pipeline = Pipeline(source=source, table='sales')
view = hvPlotView(pipeline=pipeline, kind='scatter', x='price', y='quantity')
dashboard = Dashboard(pipelines={'main': pipeline}, layouts=[view])
dashboard.servable()
```

**See**: [Python API Reference](../../references/lumen-dashboards/python-api.md)

## Configuration

### Global Config

```yaml
config:
  title: My Dashboard
  theme: dark  # or 'default', 'material'
  sizing_mode: stretch_width
  logo: ./logo.png
```

### Themes

```yaml
config:
  theme: material
  theme_json:
    palette:
      primary: '#00aa41'
```

### Authentication

```bash
lumen serve dashboard.yaml \
  --oauth-provider=generic \
  --oauth-key=${OAUTH_KEY} \
  --oauth-secret=${OAUTH_SECRET}
```

## Deployment

### Development

```bash
lumen serve dashboard.yaml --autoreload --show
```

### Production

```bash
panel serve dashboard.yaml \
  --port 80 \
  --num-procs 4 \
  --allow-websocket-origin=analytics.company.com
```

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY dashboard.yaml data/ ./
CMD ["lumen", "serve", "dashboard.yaml", "--port", "5006", "--address", "0.0.0.0"]
```

**See**: [Deployment Guide](../../references/lumen-dashboards/deployment.md)

## Best Practices

### 1. Source Organization

```yaml
# Use descriptive names
sources:
  sales_database:
    type: postgres
    tables: [orders, customers]

  inventory_files:
    type: file
    tables:
      stock: ./inventory.csv
```

### 2. Pipeline Reusability

```yaml
pipelines:
  base_sales:
    source: data
    table: sales
    filters:
      - type: widget
        field: region

  summary_sales:
    pipeline: base_sales  # Extends base_sales
    transforms:
      - type: aggregate
        by: ['category']
```

### 3. Performance

```yaml
# Limit data size for large tables
sources:
  bigdata:
    type: postgres
    tables:
      events: "SELECT * FROM events WHERE date >= '2024-01-01' LIMIT 100000"
```

### 4. User Experience

```yaml
# Provide clear labels
filters:
  - type: widget
    field: region
    label: "Sales Region"

views:
  - type: indicator
    field: revenue
    title: "Total Revenue"
    format: '${value:,.0f}'
```

## Troubleshooting

### Dashboard Won't Load

```bash
# Check YAML syntax
python -c "import yaml; yaml.safe_load(open('dashboard.yaml'))"

# Run with debug logging
lumen serve dashboard.yaml --log-level=debug
```

### Data Not Showing

- Verify data source path/connection
- Check table names match YAML config
- Ensure columns referenced exist in data

**See**: [Troubleshooting Guide](../../references/lumen-dashboards/troubleshooting.md)

## Resources

### Reference Documentation

- **[Data Sources Reference](../../references/lumen-dashboards/sources.md)** - All source types
- **[Data Transforms Reference](../../references/lumen-dashboards/transforms.md)** - Complete transform reference
- **[Views Reference](../../references/lumen-dashboards/views.md)** - All visualization types
- **[Layouts Reference](../../references/lumen-dashboards/layouts.md)** - Layout patterns
- **[Python API Reference](../../references/lumen-dashboards/python-api.md)** - Programmatic creation
- **[Examples](../../references/lumen-dashboards/examples.md)** - Complete dashboard examples
- **[Deployment Guide](../../references/lumen-dashboards/deployment.md)** - Production deployment
- **[Troubleshooting Guide](../../references/lumen-dashboards/troubleshooting.md)** - Common issues

### External Links

- [Lumen Documentation](https://lumen.holoviz.org/)
- [Lumen Gallery](https://lumen.holoviz.org/gallery/)
- [GitHub Repository](https://github.com/holoviz/lumen)
- [Community Discourse](https://discourse.holoviz.org)

## Summary

Lumen enables rapid dashboard development through declarative YAML specifications.

**Strengths**: No Python code required, fast development cycle, reproducible specifications, built-in interactivity.

**Ideal for**: Fixed dashboard layouts, standard data patterns, non-programmer dashboard creators, rapid prototyping.

**Consider alternatives when**:
- Need custom application logic → [Panel Dashboards](../panel-dashboards/SKILL.md)
- Need ad-hoc exploration → [Lumen AI](../lumen-ai/SKILL.md)
- Building novel interactions → [Panel Dashboards](../panel-dashboards/SKILL.md)

## Related Skills

- **[Lumen AI](../lumen-ai/SKILL.md)** - Conversational data exploration
- **[Panel Dashboards](../panel-dashboards/SKILL.md)** - Custom Python dashboards
- **[Plotting Fundamentals](../plotting-fundamentals/SKILL.md)** - Quick plotting with hvPlot

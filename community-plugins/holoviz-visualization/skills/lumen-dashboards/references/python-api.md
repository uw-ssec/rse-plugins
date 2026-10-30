# Lumen Python API Reference

## Overview

Guide to building Lumen dashboards programmatically with Python instead of YAML.

**When to use this reference**:
- Building dashboards with Python code
- Dynamic dashboard generation
- Integrating Lumen with existing Python applications
- Custom sources/transforms/views

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Sources](#sources)
3. [Pipelines](#pipelines)
4. [Views](#views)
5. [Layouts](#layouts)
6. [Custom Components](#custom-components)

## Basic Usage

### Simple Dashboard

```python
from lumen.sources import FileSource
from lumen.pipeline import Pipeline
from lumen.views import hvPlotView
from lumen.dashboard import Dashboard
import panel as pn

pn.extension()

# Create source
source = FileSource(tables={'sales': './data/sales.csv'})

# Create pipeline
pipeline = Pipeline(source=source, table='sales')

# Create view
view = hvPlotView(
    pipeline=pipeline,
    kind='scatter',
    x='price',
    y='quantity'
)

# Create dashboard
dashboard = Dashboard(
    title='Sales Dashboard',
    pipelines={'main': pipeline},
    layouts=[view]
)

# Serve
dashboard.servable()
```

### From YAML Config

```python
from lumen.dashboard import Dashboard

# Load from YAML
dashboard = Dashboard.from_spec('./dashboard.yaml')

# Serve
dashboard.servable()
```

## Sources

### File Source

```python
from lumen.sources import FileSource

source = FileSource(
    tables={
        'sales': './data/sales.csv',
        'customers': './data/customers.csv'
    },
    kwargs={
        'parse_dates': ['date'],
        'dtype': {'customer_id': str}
    }
)

# Get table
df = source.get('sales')
```

### Database Source

```python
from lumen.sources import PostgresSource

source = PostgresSource(
    connection_string='postgresql://user:password@localhost:5432/db',
    tables=['sales', 'customers'],
    cache=True,
    cache_dir='./cache'
)

# Get table
df = source.get('sales')

# Execute custom query
df = source.get('sales', sql="SELECT * FROM sales WHERE date >= '2024-01-01'")
```

### DuckDB Source

```python
from lumen.sources import DuckDBSource

source = DuckDBSource(
    uri=':memory:',
    tables={
        'sales': "SELECT * FROM read_csv_auto('./data/sales.csv')",
        'summary': """
            SELECT
                region,
                SUM(revenue) as total_revenue
            FROM read_csv_auto('./data/sales.csv')
            GROUP BY region
        """
    }
)
```

## Pipelines

### Basic Pipeline

```python
from lumen.pipeline import Pipeline
from lumen.filters import WidgetFilter
from lumen.transforms import QueryTransform, AggregateTransform

# Create pipeline with filters
pipeline = Pipeline(
    source=source,
    table='sales',
    filters=[
        WidgetFilter(field='region'),
        WidgetFilter(field='category', multiple=True)
    ],
    transforms=[
        QueryTransform(query='revenue > 1000'),
        AggregateTransform(
            by=['region'],
            aggregate={'total_revenue': {'revenue': 'sum'}}
        )
    ]
)

# Get filtered data
df = pipeline.data
```

### Pipeline Chaining

```python
# Base pipeline
base_pipeline = Pipeline(
    source=source,
    table='sales',
    filters=[WidgetFilter(field='region')]
)

# Derived pipeline
summary_pipeline = Pipeline(
    source=base_pipeline,  # Use pipeline as source
    transforms=[
        AggregateTransform(
            by=['category'],
            aggregate={'total': {'revenue': 'sum'}}
        )
    ]
)
```

## Views

### hvPlot View

```python
from lumen.views import hvPlotView

view = hvPlotView(
    pipeline=pipeline,
    kind='scatter',
    x='price',
    y='quantity',
    by='category',
    width=600,
    height=400,
    title='Price vs Quantity',
    responsive=True
)

# Render view
pn.panel(view)
```

### Table View

```python
from lumen.views import TableView

view = TableView(
    pipeline=pipeline,
    page_size=50,
    pagination='remote',
    selectable=True,
    formatters={
        'revenue': '${value:,.2f}',
        'date': '{value:%Y-%m-%d}'
    }
)
```

### Indicator View

```python
from lumen.views import IndicatorView

view = IndicatorView(
    pipeline=pipeline,
    field='total_revenue',
    title='Total Revenue',
    format='${value:,.0f}',
    colors=[(0, 'red'), (50000, 'orange'), (100000, 'green')]
)
```

## Layouts

### Simple Layout

```python
from lumen.dashboard import Dashboard
import panel as pn

dashboard = Dashboard(
    title='My Dashboard',
    pipelines={'main': pipeline},
    layouts=[
        pn.Column(
            view1,
            view2,
            view3
        )
    ]
)

dashboard.servable()
```

### Grid Layout

```python
dashboard = Dashboard(
    title='Grid Dashboard',
    pipelines={'main': pipeline},
    layouts=[
        pn.GridSpec(
            indicator1, indicator2, indicator3,  # Row 1
            plot1, plot2,                        # Row 2
            ncols=3
        )
    ]
)
```

### Tabbed Layout

```python
dashboard = Dashboard(
    title='Tabbed Dashboard',
    pipelines={'main': pipeline},
    layouts=[
        pn.Tabs(
            ('Overview', pn.Column(view1, view2)),
            ('Details', pn.Column(view3, view4)),
            ('Data', table_view)
        )
    ]
)
```

### Template Layout

```python
from panel.template import FastListTemplate

template = FastListTemplate(
    title='Dashboard',
    sidebar=[
        pn.pane.Markdown('## Filters'),
        pipeline.filters[0],
        pipeline.filters[1],
    ],
    main=[
        view1,
        view2,
        view3,
    ],
    accent='#0173b2'
)

template.servable()
```

## Custom Components

### Custom Source

```python
from lumen.sources import Source
import param
import pandas as pd

class CustomSource(Source):
    """Custom data source."""

    source_type = 'custom'

    api_key = param.String(doc='API key for data source')

    def get(self, table, **query):
        """Fetch data from custom source."""
        # Your custom logic here
        if table == 'data':
            return pd.DataFrame({
                'x': [1, 2, 3],
                'y': [4, 5, 6]
            })
        raise ValueError(f'Unknown table: {table}')

    def get_tables(self):
        """Return available tables."""
        return ['data']

# Use custom source
source = CustomSource(api_key='secret')
pipeline = Pipeline(source=source, table='data')
```

### Custom Transform

```python
from lumen.transforms import Transform
import param

class CustomTransform(Transform):
    """Custom data transformation."""

    transform_type = 'custom'

    multiplier = param.Number(default=2, doc='Multiplication factor')

    def apply(self, table):
        """Apply transformation."""
        table = table.copy()
        table['doubled'] = table['value'] * self.multiplier
        return table

# Use custom transform
pipeline = Pipeline(
    source=source,
    table='data',
    transforms=[
        CustomTransform(multiplier=3)
    ]
)
```

### Custom View

```python
from lumen.views import View
import panel as pn
import param

class CustomView(View):
    """Custom visualization."""

    view_type = 'custom'

    title = param.String(default='Custom View')

    def __panel__(self):
        """Render view."""
        data = self.get_data()

        # Custom visualization logic
        text = f"Total rows: {len(data)}"

        return pn.Column(
            f"## {self.title}",
            pn.pane.Markdown(text),
            data.hvplot.table()
        )

# Use custom view
view = CustomView(pipeline=pipeline, title='My Custom View')
```

## Dynamic Dashboard Generation

### Programmatic Dashboard

```python
def create_dashboard(config):
    """Create dashboard from configuration."""

    # Create sources
    sources = {}
    for name, source_config in config['sources'].items():
        if source_config['type'] == 'file':
            sources[name] = FileSource(**source_config)
        elif source_config['type'] == 'postgres':
            sources[name] = PostgresSource(**source_config)

    # Create pipelines
    pipelines = {}
    for name, pipeline_config in config['pipelines'].items():
        pipelines[name] = Pipeline(
            source=sources[pipeline_config['source']],
            **pipeline_config
        )

    # Create views
    views = []
    for view_config in config['views']:
        view_type = view_config.pop('type')
        pipeline_name = view_config.pop('pipeline')

        if view_type == 'hvplot':
            views.append(hvPlotView(
                pipeline=pipelines[pipeline_name],
                **view_config
            ))
        elif view_type == 'table':
            views.append(TableView(
                pipeline=pipelines[pipeline_name],
                **view_config
            ))

    # Create dashboard
    return Dashboard(
        title=config.get('title', 'Dashboard'),
        pipelines=pipelines,
        layouts=[pn.Column(*views)]
    )

# Usage
config = {
    'title': 'Sales Dashboard',
    'sources': {
        'data': {
            'type': 'file',
            'tables': {'sales': './data/sales.csv'}
        }
    },
    'pipelines': {
        'main': {
            'source': 'data',
            'table': 'sales'
        }
    },
    'views': [
        {'type': 'hvplot', 'pipeline': 'main', 'kind': 'scatter', 'x': 'price', 'y': 'quantity'},
        {'type': 'table', 'pipeline': 'main'}
    ]
}

dashboard = create_dashboard(config)
dashboard.servable()
```

## Integration Patterns

### With FastAPI

```python
from fastapi import FastAPI
from lumen.dashboard import Dashboard
import panel as pn

app = FastAPI()
pn.extension()

dashboard = Dashboard.from_spec('./dashboard.yaml')

# Mount Panel app
pn.serve(dashboard.layout, port=5006, allow_websocket_origin=['localhost:5006'])

@app.get("/")
async def root():
    return {"message": "Dashboard running on port 5006"}
```

### With Existing Panel App

```python
import panel as pn
from lumen.dashboard import Dashboard

pn.extension()

# Existing Panel components
header = pn.pane.Markdown('# My Application')
sidebar = pn.Column(...)

# Lumen dashboard
lumen_dashboard = Dashboard.from_spec('./dashboard.yaml')

# Combine
app = pn.template.FastListTemplate(
    title='My App',
    sidebar=[sidebar],
    main=[
        header,
        lumen_dashboard.layout
    ]
)

app.servable()
```

## Best Practices

### 1. Reusable Components

```python
# ✅ Good: Create reusable components
def create_kpi_view(pipeline, field, title):
    return IndicatorView(
        pipeline=pipeline,
        field=field,
        title=title,
        format='${value:,.0f}'
    )

# Use multiple times
kpi1 = create_kpi_view(pipeline, 'revenue', 'Revenue')
kpi2 = create_kpi_view(pipeline, 'orders', 'Orders')
```

### 2. Configuration-Driven

```python
# ✅ Good: Use configuration
def build_from_config(config_file):
    return Dashboard.from_spec(config_file)

dashboard = build_from_config('./dashboard.yaml')
```

### 3. Error Handling

```python
# ✅ Good: Handle errors gracefully
try:
    source = PostgresSource(connection_string=db_url)
    pipeline = Pipeline(source=source, table='sales')
except Exception as e:
    # Fallback to sample data
    source = FileSource(tables={'sales': './sample.csv'})
    pipeline = Pipeline(source=source, table='sales')
```

## Summary

**Key concepts**:
- Build dashboards programmatically with Python
- Create custom sources, transforms, and views
- Combine with existing Panel applications
- Generate dashboards dynamically

**Python API classes**:
- `Source`: Data sources
- `Pipeline`: Data pipelines with filters/transforms
- `View`: Visualizations
- `Dashboard`: Complete dashboard

**Best practices**:
- Use YAML for static dashboards
- Use Python for dynamic generation
- Create reusable components
- Handle errors gracefully
- Combine with Panel for maximum flexibility

## References

- [Lumen Python API Documentation](https://lumen.holoviz.org/reference/index.html)
- [Panel Documentation](https://panel.holoviz.org/)
- [Param Documentation](https://param.holoviz.org/)

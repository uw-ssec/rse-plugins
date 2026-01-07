# HoloViz Code Patterns & Snippets

## Overview

Production-ready code patterns for common HoloViz tasks. Organized by domain for progressive discovery.

**When to use code patterns**:
- Starting a new project or feature
- Looking for best practices examples
- Need a template for common tasks
- Want to avoid common pitfalls

## Pattern Categories

### 1. Panel Application Patterns

**Reactive dashboards, web apps, and component systems**

Common patterns:
- Param-based reactive dashboards
- Multi-page applications
- Real-time data streaming
- File upload handling
- OAuth authentication
- WebSocket communication

**See**: [Panel Patterns](./panel-patterns.md)

**When to load**: Building Panel applications, dashboards, or interactive components

### 2. HoloViews Composition Patterns

**Declarative visualization composition and layouts**

Common patterns:
- Overlay and Layout compositions
- DynamicMaps with streams
- Custom operations
- Dimension value formatting
- Interactive selection

**See**: [HoloViews Patterns](./holoviews-patterns.md)

**When to load**: Creating complex visualizations with HoloViews

### 3. Datashader Patterns

**Large-scale data rendering and aggregation**

Common patterns:
- Million-point scatter plots
- Time series rasterization
- Geographic data aggregation
- Custom aggregation functions
- Dynamic colormapping

**See**: [Datashader Patterns](./datashader-patterns.md)

**When to load**: Working with datasets > 100K points

### 4. GeoViews Patterns

**Geographic visualization and spatial analysis**

Common patterns:
- Tile providers and basemaps
- Point/polygon/line overlays
- Coordinate reference systems
- Spatial joins and buffers
- Choropleth maps

**See**: [GeoViews Patterns](./geoviews-patterns.md)

**When to load**: Creating maps or spatial visualizations

### 5. Param Configuration Patterns

**Type-safe parameter systems and reactive dependencies**

Common patterns:
- Parameter validation
- Reactive dependencies
- Watchers and side effects
- Dynamic parameter updates
- Parameter inheritance

**See**: [Param Patterns](./param-patterns.md)

**When to load**: Building parameterized classes or configs

### 6. Integration Patterns

**Combining multiple HoloViz tools**

Common patterns:
- Panel + HoloViews dashboards
- Datashader + HoloViews pipelines
- GeoViews + Datashader maps
- Lumen + custom components
- FastAPI + Panel apps

**See**: [Integration Patterns](./integration-patterns.md)

**When to load**: Using multiple HoloViz libraries together

### 7. Performance Optimization Patterns

**Memory management, caching, and scalability**

Common patterns:
- Data caching strategies
- Lazy loading
- Streaming large datasets
- Web worker offloading
- Async/await patterns

**See**: [Performance Patterns](./performance-patterns.md)

**When to load**: Optimizing slow applications or handling large data

## Quick Reference

### Most Common Patterns

**Reactive Dashboard (Panel + Param)**:
```python
import panel as pn
import param

class Dashboard(param.Parameterized):
    date_range = param.DateRange()

    @param.depends('date_range')
    def view(self):
        # Filter data by date_range
        return plot

pn.Row(Dashboard.param, Dashboard().view).servable()
```
→ See [Panel Patterns](./panel-patterns.md#pattern-1-param-based-dashboard) for full example

**Large Data Visualization (Datashader + HoloViews)**:
```python
import holoviews as hv
from holoviews.operation.datashader import datashade

df = pd.read_parquet('large_data.parquet')  # 10M+ rows
points = hv.Points(df, ['x', 'y'])
datashade(points)  # Renders instantly
```
→ See [Datashader Patterns](./datashader-patterns.md#pattern-1-basic-datashading) for full example

**Interactive Map (GeoViews)**:
```python
import geoviews as gv
import geoviews.tile_sources as gts

points = gv.Points(data, ['lon', 'lat'])
gts.OSM() * points
```
→ See [GeoViews Patterns](./geoviews-patterns.md#pattern-1-basic-map) for full example

## Pattern Selection Guide

### By Use Case

| Use Case | Recommended Pattern | File |
|----------|---------------------|------|
| Interactive dashboard | Param-based Dashboard | [Panel Patterns](./panel-patterns.md) |
| Multi-page app | Multi-page Application | [Panel Patterns](./panel-patterns.md) |
| 1M+ point scatter | Datashader Scatter | [Datashader Patterns](./datashader-patterns.md) |
| Geographic map | Basic Map with Tiles | [GeoViews Patterns](./geoviews-patterns.md) |
| Overlaid plots | HoloViews Overlay | [HoloViews Patterns](./holoviews-patterns.md) |
| Real-time streaming | WebSocket Streaming | [Panel Patterns](./panel-patterns.md) |
| API integration | FastAPI + Panel | [Integration Patterns](./integration-patterns.md) |
| Performance issues | Caching & Lazy Loading | [Performance Patterns](./performance-patterns.md) |

### By Data Size

| Data Size | Recommended Approach | Pattern |
|-----------|---------------------|---------|
| < 10K rows | Standard hvPlot | [HoloViews Patterns](./holoviews-patterns.md) |
| 10K - 100K rows | HoloViews + optimization | [Performance Patterns](./performance-patterns.md) |
| 100K - 10M rows | Datashader | [Datashader Patterns](./datashader-patterns.md) |
| 10M+ rows | Datashader + streaming | [Datashader Patterns](./datashader-patterns.md) |

### By Interactivity Needs

| Interactivity | Pattern | File |
|---------------|---------|------|
| Static plot | Basic hvPlot | [HoloViews Patterns](./holoviews-patterns.md) |
| Hover tools | HoloViews with tooltips | [HoloViews Patterns](./holoviews-patterns.md) |
| Selection/Linking | Streams | [HoloViews Patterns](./holoviews-patterns.md) |
| Full dashboard | Panel application | [Panel Patterns](./panel-patterns.md) |
| Real-time updates | Streaming | [Panel Patterns](./panel-patterns.md) |

## Best Practices

### Code Organization

```
project/
├── app.py              # Main application
├── components/         # Reusable components
│   ├── plots.py
│   ├── tables.py
│   └── filters.py
├── data/               # Data loading
│   └── sources.py
└── utils/              # Helper functions
    └── processing.py
```

### Testing Patterns

```python
import pytest
import panel as pn

def test_dashboard_loads():
    """Test dashboard initializes without errors."""
    dashboard = MyDashboard()
    assert dashboard.view() is not None

def test_reactive_update():
    """Test parameter changes trigger updates."""
    dashboard = MyDashboard()
    dashboard.date_range = (date(2024, 1, 1), date(2024, 12, 31))
    view = dashboard.view()
    assert view is not None
```

### Documentation Patterns

```python
class DataDashboard(param.Parameterized):
    """
    Interactive data exploration dashboard.

    Parameters
    ----------
    data_source : str
        Name of data source to load
    date_range : tuple of datetime
        Start and end dates for filtering

    Examples
    --------
    >>> dashboard = DataDashboard(data_source='sales')
    >>> dashboard.servable()
    """

    def __init__(self, **params):
        """Initialize dashboard with data source."""
        super().__init__(**params)
```

## Pattern Development Workflow

1. **Identify need**: What problem are you solving?
2. **Find similar pattern**: Check pattern files for similar use cases
3. **Adapt pattern**: Modify for your specific requirements
4. **Test thoroughly**: Verify edge cases and performance
5. **Document**: Add comments explaining customizations

## Contributing Patterns

When adding new patterns to these resources:

1. **Clear use case**: Explain when to use the pattern
2. **Complete example**: Include all imports and setup
3. **Best practices**: Follow established conventions
4. **Performance notes**: Mention scalability considerations
5. **Related patterns**: Link to similar or complementary patterns

## References

- [Panel Documentation](https://panel.holoviz.org/)
- [HoloViews Documentation](https://holoviews.org/)
- [Datashader Documentation](https://datashader.org/)
- [GeoViews Documentation](https://geoviews.org/)
- [Param Documentation](https://param.holoviz.org/)

---

## Pattern File Table of Contents

### Detailed Pattern Files

1. **[Panel Patterns](./panel-patterns.md)** (Loaded when: Building Panel apps)
   - Param-based dashboards
   - Multi-page applications
   - Real-time streaming
   - File uploads
   - Authentication

2. **[HoloViews Patterns](./holoviews-patterns.md)** (Loaded when: Composing visualizations)
   - Overlays and layouts
   - DynamicMaps
   - Custom operations
   - Interactive streams

3. **[Datashader Patterns](./datashader-patterns.md)** (Loaded when: Visualizing > 100K points)
   - Scatter plots
   - Time series
   - Custom aggregations
   - Dynamic colormapping

4. **[GeoViews Patterns](./geoviews-patterns.md)** (Loaded when: Creating maps)
   - Basemaps
   - Geographic overlays
   - CRS handling
   - Spatial analysis

5. **[Param Patterns](./param-patterns.md)** (Loaded when: Building parameter systems)
   - Validation
   - Dependencies
   - Watchers
   - Dynamic updates

6. **[Integration Patterns](./integration-patterns.md)** (Loaded when: Using multiple tools)
   - Panel + HoloViews
   - Datashader + HoloViews
   - FastAPI + Panel
   - Lumen extensions

7. **[Performance Patterns](./performance-patterns.md)** (Loaded when: Optimizing performance)
   - Caching
   - Lazy loading
   - Streaming
   - Async patterns

---

**Note**: Each pattern file includes complete, runnable examples with explanations. Load only the files relevant to your current task to minimize context usage.

# HoloViz Best Practices

## Overview

Proven practices for building production-quality HoloViz applications. Organized by domain for focused learning.

**Use this guide when**:
- Starting a new project
- Reviewing code quality
- Preparing for production
- Teaching or mentoring

## General Principles

### 1. Start Simple, Add Complexity

```python
# ✅ Good: Start with basics
plot = df.hvplot.scatter('x', 'y')

# Then add features as needed
plot = df.hvplot.scatter(
    'x', 'y',
    by='category',
    size='value',
    hover_cols=['name', 'date']
)

# ❌ Bad: Everything at once
plot = df.hvplot.scatter(...50 parameters...)
```

### 2. Use Declarative Patterns

```python
# ✅ Good: Param-based reactivity
class Dashboard(param.Parameterized):
    date = param.Date()

    @param.depends('date')
    def view(self):
        return self.plot_for_date(self.date)

# ❌ Bad: Manual callbacks
date_widget = pn.widgets.DatePicker()

def update_plot(event):
    # Manual update logic
    ...

date_widget.param.watch(update_plot, 'value')
```

### 3. Separate Concerns

```python
# ✅ Good: Separate data, logic, presentation
class DataLoader:
    def load(self): ...

class Analyzer:
    def analyze(self, data): ...

class Dashboard:
    def __init__(self):
        self.loader = DataLoader()
        self.analyzer = Analyzer()
```

### 4. Test Early and Often

```python
import pytest

def test_data_loading():
    loader = DataLoader()
    data = loader.load()
    assert not data.empty

def test_visualization():
    plot = create_plot(test_data)
    assert plot is not None
```

## Domain-Specific Best Practices

### Performance Optimization

**Key practices**: Caching, lazy loading, data reduction, Datashader for large data

**See**: [Performance Best Practices](./performance.md)

**Load when**: Optimizing slow applications or handling large datasets

### Panel Applications

**Key practices**: Reactive patterns, layout design, state management, deployment

**See**: [Panel Best Practices](./panel.md)

**Load when**: Building Panel dashboards or web applications

### HoloViews Visualizations

**Key practices**: Composition patterns, customization, styling, backends

**See**: [HoloViews Best Practices](./holoviews.md)

**Load when**: Creating complex visualizations with HoloViews

### Param Configuration

**Key practices**: Validation, dependencies, documentation, inheritance

**See**: [Param Best Practices](./param.md)

**Load when**: Designing parameter systems

### GeoViews Maps

**Key practices**: CRS handling, tile providers, performance, accuracy

**See**: [GeoViews Best Practices](./geoviews.md)

**Load when**: Creating geographic visualizations

### Code Organization

**Key practices**: Project structure, modularity, naming conventions

**See**: [Code Organization Best Practices](./code-organization.md)

**Load when**: Structuring a new project or refactoring

### Testing

**Key practices**: Unit tests, integration tests, visual regression

**See**: [Testing Best Practices](./testing.md)

**Load when**: Writing tests for HoloViz applications

### Documentation

**Key practices**: Docstrings, examples, API docs, user guides

**See**: [Documentation Best Practices](./documentation.md)

**Load when**: Documenting code or creating user guides

### Deployment

**Key practices**: Environment setup, security, monitoring, scaling

**See**: [Deployment Best Practices](./deployment.md)

**Load when**: Preparing applications for production

### Accessibility

**Key practices**: Color contrast, keyboard navigation, screen readers, WCAG compliance

**See**: [Accessibility Best Practices](./accessibility.md)

**Load when**: Ensuring applications are accessible to all users

## Quick Reference

### Most Important Practices

**1. Use Progressive Disclosure**
- Start with simple patterns
- Add complexity only when needed
- Reference detailed docs as you learn

**2. Follow the Data Flow**
```
Data Source → Transform → Visualize → Interact → Update
```

**3. Leverage Reactivity**
```python
# Automatic updates with @param.depends
@param.depends('filter_value')
def filtered_view(self):
    return self.data[self.data.value > self.filter_value]
```

**4. Cache Expensive Operations**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_computation(param):
    # Heavy processing
    return result
```

**5. Use Datashader for Large Data**
```python
# Automatically use Datashader for 100K+ points
if len(df) > 100_000:
    from holoviews.operation.datashader import datashade
    plot = datashade(hv.Points(df, ['x', 'y']))
```

## Anti-Patterns to Avoid

### ❌ Tight Coupling

```python
# Bad: Everything in one class
class MegaDashboard:
    def __init__(self):
        self.load_data()
        self.process_data()
        self.create_plots()
        self.setup_widgets()
        self.define_callbacks()
        # 1000 more lines...
```

**Better**: Split into focused components

### ❌ No Caching

```python
# Bad: Recompute on every update
@param.depends('date')
def expensive_view(self):
    data = self.load_data()  # Slow!
    processed = self.process(data)  # Slow!
    return self.visualize(processed)
```

**Better**: Cache intermediate results

### ❌ Ignoring Data Size

```python
# Bad: No optimization for size
df = pd.read_csv('huge_file.csv')  # 10M rows
df.hvplot.scatter('x', 'y')  # Browser crashes!
```

**Better**: Use Datashader or sample data

### ❌ Magic Numbers

```python
# Bad: Unexplained constants
if value > 0.73 and metric < 142:
    # Why these numbers?
```

**Better**: Named constants with explanations
```python
THRESHOLD_CONFIDENCE = 0.73  # Based on statistical analysis
MAX_LATENCY_MS = 142  # SLA requirement
```

### ❌ No Error Handling

```python
# Bad: Assumes everything works
def load_data(url):
    return pd.read_csv(url)
```

**Better**: Handle failures gracefully
```python
def load_data(url):
    try:
        return pd.read_csv(url)
    except Exception as e:
        logger.error(f"Failed to load {url}: {e}")
        return pd.DataFrame()  # Return empty DF as fallback
```

## Practice Selection Guide

### By Project Phase

| Phase | Focus On | Best Practices |
|-------|----------|----------------|
| Planning | Architecture | [Code Organization](./code-organization.md) |
| Development | Patterns | [Panel](./panel.md), [HoloViews](./holoviews.md) |
| Optimization | Speed | [Performance](./performance.md) |
| Testing | Quality | [Testing](./testing.md) |
| Documentation | Clarity | [Documentation](./documentation.md) |
| Deployment | Reliability | [Deployment](./deployment.md) |

### By Application Type

| App Type | Key Practices | Documents |
|----------|---------------|-----------|
| Dashboard | Reactivity, Layout | [Panel](./panel.md) |
| Visualization | Composition, Style | [HoloViews](./holoviews.md) |
| Big Data | Datashader, Caching | [Performance](./performance.md) |
| Geographic | CRS, Tiles | [GeoViews](./geoviews.md) |
| Public-facing | Accessibility | [Accessibility](./accessibility.md) |

### By Problem

| Problem | Solution | Best Practice |
|---------|----------|---------------|
| Slow performance | Optimize data flow | [Performance](./performance.md) |
| Hard to maintain | Improve structure | [Code Organization](./code-organization.md) |
| Bugs in production | Add tests | [Testing](./testing.md) |
| Users confused | Better docs | [Documentation](./documentation.md) |
| Deployment issues | Follow deploy guide | [Deployment](./deployment.md) |

## Summary Checklist

### Before Starting

- [ ] Read relevant best practices docs
- [ ] Plan project structure
- [ ] Set up testing framework
- [ ] Configure development environment

### During Development

- [ ] Follow naming conventions
- [ ] Use reactive patterns
- [ ] Cache expensive operations
- [ ] Write tests as you code
- [ ] Document as you go

### Before Deployment

- [ ] Run full test suite
- [ ] Check performance with production data
- [ ] Review security practices
- [ ] Test accessibility
- [ ] Update documentation

### In Production

- [ ] Monitor performance
- [ ] Track errors
- [ ] Collect user feedback
- [ ] Plan improvements

## Progressive Learning Path

### Level 1: Fundamentals
**Focus**: Core patterns and anti-patterns

**Read**:
- General Principles (this doc)
- [Code Organization](./code-organization.md)

### Level 2: Library-Specific
**Focus**: Best practices for your primary library

**Read**:
- [Panel Best Practices](./panel.md) OR
- [HoloViews Best Practices](./holoviews.md) OR
- [GeoViews Best Practices](./geoviews.md)

### Level 3: Optimization
**Focus**: Performance and quality

**Read**:
- [Performance Best Practices](./performance.md)
- [Testing Best Practices](./testing.md)

### Level 4: Production
**Focus**: Deployment and maintenance

**Read**:
- [Deployment Best Practices](./deployment.md)
- [Accessibility Best Practices](./accessibility.md)

## References

### Best Practice Documents

- **[Performance Best Practices](./performance.md)** - Optimization strategies
- **[Panel Best Practices](./panel.md)** - Dashboard development
- **[HoloViews Best Practices](./holoviews.md)** - Visualization patterns
- **[Param Best Practices](./param.md)** - Parameter systems
- **[GeoViews Best Practices](./geoviews.md)** - Geographic visualization
- **[Code Organization Best Practices](./code-organization.md)** - Project structure
- **[Testing Best Practices](./testing.md)** - Testing strategies
- **[Documentation Best Practices](./documentation.md)** - Writing docs
- **[Deployment Best Practices](./deployment.md)** - Production deployment
- **[Accessibility Best Practices](./accessibility.md)** - Inclusive design

### External Resources

- [Panel User Guide](https://panel.holoviz.org/user_guide/)
- [HoloViews User Guide](https://holoviews.org/user_guide/)
- [Python Best Practices](https://docs.python-guide.org/)
- [Web Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

---

**Note**: Each best practices file contains detailed guidelines, examples, and anti-patterns for that specific domain. Load only the files relevant to your current focus area to minimize context usage.

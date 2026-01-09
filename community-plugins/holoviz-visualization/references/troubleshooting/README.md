# HoloViz Troubleshooting Guide

## Overview

Solutions for common issues across the HoloViz ecosystem. Organized by library for quick problem resolution.

**How to use this guide**:
1. Identify which library is causing the issue
2. Check the appropriate troubleshooting file
3. Try common debugging strategies if issue persists
4. Consult community resources

## Library-Specific Troubleshooting

### Panel Issues

**Common problems**: Server won't start, widgets not updating, deployment issues, authentication problems

**See**: [Panel Troubleshooting](./panel-troubleshooting.md)

**Load when**: Panel server issues, widget problems, or deployment errors

### HoloViews Issues

**Common problems**: Plots not rendering, composition errors, dimension mismatches, backend issues

**See**: [HoloViews Troubleshooting](./holoviews-troubleshooting.md)

**Load when**: Visualization rendering problems or HoloViews-specific errors

### Datashader Issues

**Common problems**: Performance degradation, memory errors, aggregation failures, colormapping issues

**See**: [Datashader Troubleshooting](./datashader-troubleshooting.md)

**Load when**: Large dataset rendering problems or Datashader errors

### GeoViews Issues

**Common problems**: CRS errors, tile provider failures, projection mismatches, geographic data loading

**See**: [GeoViews Troubleshooting](./geoviews-troubleshooting.md)

**Load when**: Map rendering issues or geographic data problems

### Param Issues

**Common problems**: Validation errors, dependency loops, watcher not firing, parameter inheritance

**See**: [Param Troubleshooting](./param-troubleshooting.md)

**Load when**: Parameter system errors or reactive update issues

### hvPlot Issues

**Common problems**: Import errors, plot not showing, groupby failures, kind not recognized

**See**: [hvPlot Troubleshooting](./hvplot-troubleshooting.md)

**Load when**: hvPlot API issues or quick plotting problems

## Common Error Messages

### "No module named 'X'"

**Problem**: Missing dependency

**Solution**:
```bash
# Install missing library
pip install X

# Or install with specific extra
pip install panel[recommended]
pip install lumen[ai]
```

### "Javascript Error: <model> could not be instantiated"

**Problem**: Extension not loaded

**Solution**:
```python
import panel as pn
pn.extension('tabulator', 'plotly')  # Load required extensions
```

### "BokehDeprecationWarning"

**Problem**: Using deprecated API

**Solution**:
- Check documentation for updated API
- Update code to use new methods
- Or suppress warnings (not recommended):
```python
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
```

### "Object of type X is not JSON serializable"

**Problem**: Trying to serialize non-JSON-compatible object

**Solution**:
```python
# Convert to JSON-compatible types
import json
import numpy as np

# Use tolist() for numpy arrays
data = {
    'values': np_array.tolist(),
    'timestamp': datetime_obj.isoformat()
}
```

### "RuntimeError: There is no current event loop"

**Problem**: Async code running without event loop

**Solution**:
```python
# Use async context
import asyncio

async def main():
    # Your async code here
    pass

asyncio.run(main())

# Or for Panel
pn.serve(app, port=5006)
```

## Quick Debugging Checklist

### Visualization Not Showing

- [ ] Extensions loaded? (`pn.extension()`, `hv.extension()`)
- [ ] Data not empty? (check `df.head()`)
- [ ] Correct dimensions specified? (check column names)
- [ ] In Jupyter: cell executed and output visible?
- [ ] In script: `.servable()` or `.show()` called?

### Widget Not Updating

- [ ] `@param.depends` decorator present?
- [ ] Correct parameter names in decorator?
- [ ] Method returns a displayable object?
- [ ] Parameter actually changing? (add print statement)
- [ ] No circular dependencies?

### Performance Issues

- [ ] Data size reasonable? (< 100K rows for most operations)
- [ ] Using Datashader for large data?
- [ ] Caching enabled where appropriate?
- [ ] Unnecessary recomputation happening?
- [ ] Memory leaks from unclosed resources?

### Import Errors

- [ ] All dependencies installed?
- [ ] Correct package versions?
- [ ] Virtual environment activated?
- [ ] No conflicting package versions?
- [ ] Python version compatible? (3.9+)

## Debugging Strategies

### 1. Enable Debug Logging

```python
import logging

# Set logging level
logging.basicConfig(level=logging.DEBUG)

# Panel-specific logging
import panel as pn
pn.config.console_output = 'accumulate'
```

### 2. Isolate the Problem

```python
# Test with minimal example
import panel as pn
pn.extension()

# Simplest possible test
pn.panel("Hello").show()  # Does this work?
```

### 3. Check Versions

```python
import panel as pn
import holoviews as hv
import datashader as ds

print(f"Panel: {pn.__version__}")
print(f"HoloViews: {hv.__version__}")
print(f"Datashader: {ds.__version__}")
```

### 4. Inspect Objects

```python
# Check data
print(df.head())
print(df.dtypes)
print(df.shape)

# Check HoloViews elements
print(element.dimensions())
print(element.data)

# Check Panel components
print(component.param)
print(component.param.values())
```

### 5. Use Browser DevTools

For Panel applications:
1. Open browser DevTools (F12)
2. Check Console for JavaScript errors
3. Check Network tab for failed requests
4. Check WebSocket connection status

### 6. Test in Different Environments

```bash
# Test in Python shell
python -c "import panel; panel.__version__"

# Test in Jupyter
jupyter lab  # or jupyter notebook

# Test standalone
panel serve app.py --show
```

## Performance Profiling

### Memory Profiling

```python
from memory_profiler import profile

@profile
def create_dashboard():
    # Your code here
    pass

create_dashboard()
```

### Time Profiling

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Your code here

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)
```

### Panel Performance Debugging

```python
import panel as pn

# Enable performance logging
pn.config.profiler = 'pyinstrument'  # or 'snakeviz'

# Run your app
app.servable()
```

## Getting Help

### Before Asking for Help

1. **Search existing issues**: Check GitHub issues and Discourse
2. **Create minimal example**: Reduce to simplest reproducible case
3. **Check documentation**: Review relevant docs and examples
4. **Include versions**: List all package versions
5. **Show error messages**: Include full error traceback

### Where to Get Help

**Community Forum** (Best for questions):
- [HoloViz Discourse](https://discourse.holoviz.org)
- Searchable history
- Community support

**GitHub Issues** (For bugs):
- [Panel Issues](https://github.com/holoviz/panel/issues)
- [HoloViews Issues](https://github.com/holoviz/holoviews/issues)
- [Datashader Issues](https://github.com/holoviz/datashader/issues)
- [GeoViews Issues](https://github.com/holoviz/geoviews/issues)

**Stack Overflow** (For coding questions):
- Tag: `holoviews`, `panel`, `datashader`
- Good for general coding questions

### Minimal Reproducible Example Template

```python
"""
Issue: [Brief description]

Environment:
- Python: 3.11
- Panel: 1.3.0
- HoloViews: 1.18.0
- OS: macOS / Linux / Windows
"""

import panel as pn
import holoviews as hv

pn.extension()
hv.extension('bokeh')

# Minimal code that reproduces the issue
def create_issue():
    # Your minimal example here
    pass

# Expected: [What should happen]
# Actual: [What actually happens]
# Error: [Full error message if any]
```

## Environment Troubleshooting

### Virtual Environment Issues

```bash
# Verify environment is activated
which python  # Should show venv path

# Recreate environment if needed
python -m venv fresh_env
source fresh_env/bin/activate  # or fresh_env\Scripts\activate on Windows
pip install panel holoviews
```

### Package Conflicts

```bash
# Check for conflicts
pip check

# Create requirements file
pip freeze > requirements.txt

# Fresh install
pip uninstall -y panel holoviews datashader
pip install panel holoviews datashader
```

### Jupyter Extension Issues

```bash
# Reinstall Jupyter extensions
jupyter labextension install @pyviz/jupyterlab_pyviz

# Or for JupyterLab 3+
pip install jupyterlab_pyviz
```

## Quick Reference: Error → Solution

| Error | Solution | Doc Link |
|-------|----------|----------|
| Plot not showing | Load extensions | [Panel](./panel-troubleshooting.md) |
| Widget not updating | Check `@param.depends` | [Param](./param-troubleshooting.md) |
| Memory error with large data | Use Datashader | [Datashader](./datashader-troubleshooting.md) |
| CRS/projection error | Check coordinate systems | [GeoViews](./geoviews-troubleshooting.md) |
| Server won't start | Check port availability | [Panel](./panel-troubleshooting.md) |
| Import error | Install dependencies | All docs |
| JavaScript error | Load extensions | [Panel](./panel-troubleshooting.md) |

## Common Solutions by Symptom

### Nothing Displays

1. Check extensions loaded
2. Verify data not empty
3. Ensure cell executed (Jupyter)
4. Check `.servable()` or `.show()` called

**See**: [Panel Troubleshooting](./panel-troubleshooting.md#displays)

### Slow Performance

1. Check data size
2. Use Datashader for large data
3. Enable caching
4. Profile code

**See**: [Performance Patterns](../patterns/performance-patterns.md)

### Unexpected Behavior

1. Check parameter values
2. Verify data types
3. Test with simple example
4. Enable debug logging

**See**: Library-specific troubleshooting guides

## Summary

Most issues fall into these categories:
1. **Missing dependencies** → Install required packages
2. **Extensions not loaded** → Add `pn.extension()` / `hv.extension()`
3. **Data issues** → Check data shape, types, and contents
4. **Configuration** → Verify parameters and settings
5. **Environment** → Check package versions and conflicts

**Next steps**:
1. Identify the specific library causing issues
2. Check the relevant troubleshooting guide
3. Try debugging strategies
4. Ask community if still stuck

## Library Troubleshooting References

- **[Panel Troubleshooting](./panel-troubleshooting.md)** - Server, widgets, deployment
- **[HoloViews Troubleshooting](./holoviews-troubleshooting.md)** - Plots, composition, backends
- **[Datashader Troubleshooting](./datashader-troubleshooting.md)** - Performance, memory, aggregation
- **[GeoViews Troubleshooting](./geoviews-troubleshooting.md)** - Maps, CRS, projections
- **[Param Troubleshooting](./param-troubleshooting.md)** - Parameters, validation, dependencies
- **[hvPlot Troubleshooting](./hvplot-troubleshooting.md)** - Quick plotting issues

---

**Note**: Each troubleshooting file contains specific error messages, solutions, and workarounds for that library. Load only the file relevant to your issue.

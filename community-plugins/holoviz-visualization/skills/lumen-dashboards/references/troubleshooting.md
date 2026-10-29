# Lumen Troubleshooting Guide

## Overview

Solutions for common Lumen dashboard issues including configuration errors, data problems, and deployment issues.

**When to use this guide**:
- Dashboard won't load
- Data not showing
- Performance problems
- Deployment issues

## Table of Contents

1. [Dashboard Won't Load](#dashboard-wont-load)
2. [Data Issues](#data-issues)
3. [View Problems](#view-problems)
4. [Performance Issues](#performance-issues)
5. [Deployment Problems](#deployment-problems)

## Dashboard Won't Load

### YAML Syntax Error

**Problem**: Dashboard fails to load with YAML error

**Solution**:
```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('dashboard.yaml'))"

# Common issues:
# - Incorrect indentation (use spaces, not tabs)
# - Missing colons
# - Unquoted strings with special characters
```

**Fix**:
```yaml
# ❌ Bad: Inconsistent indentation
views:
  - type: hvplot
  kind: scatter  # Wrong indentation

# ✅ Good: Consistent indentation
views:
  - type: hvplot
    kind: scatter  # Correct indentation
```

### Import Error

**Problem**: `ModuleNotFoundError: No module named 'lumen'`

**Solution**:
```bash
# Install Lumen
pip install lumen

# Verify installation
python -c "import lumen; print(lumen.__version__)"
```

### Configuration Not Found

**Problem**: Dashboard YAML file not found

**Solution**:
```bash
# Check file path
ls dashboard.yaml

# Use absolute path
lumen serve /full/path/to/dashboard.yaml

# Or ensure correct working directory
cd /path/to/dashboard
lumen serve dashboard.yaml
```

## Data Issues

### Source Connection Failed

**Problem**: Cannot connect to data source

**Database connection**:
```yaml
# Check connection string format
sources:
  db:
    type: postgres
    # Correct format
    connection_string: postgresql://user:password@host:5432/database

# Test connection
import psycopg2
conn = psycopg2.connect("postgresql://user:password@host:5432/database")
```

**File not found**:
```yaml
# Check file path
sources:
  data:
    type: file
    tables:
      # Use relative or absolute path
      sales: ./data/sales.csv  # Relative to YAML file
      # or
      sales: /full/path/to/sales.csv
```

### No Data Showing

**Problem**: Views are empty

**Check pipeline**:
```yaml
pipelines:
  main:
    source: data  # Must match source name
    table: sales  # Must match table name

    # Debug: Remove transforms to see raw data
    # transforms: []
```

**Check transforms**:
```yaml
# Problem: Filter removes all data
transforms:
  - type: query
    query: "revenue > 1000000"  # Too restrictive?

# Solution: Relax filter or check data range
transforms:
  - type: query
    query: "revenue > 0"
```

### Wrong Data Type

**Problem**: Data types causing errors

**Solution**:
```yaml
transforms:
  # Convert data types explicitly
  - type: astype
    dtypes:
      date: datetime64
      customer_id: str
      revenue: float
      quantity: int
```

## View Problems

### Plot Not Showing

**Problem**: hvPlot view is blank

**Check columns**:
```yaml
views:
  - type: hvplot
    pipeline: main
    kind: scatter
    x: price  # Column must exist in data
    y: quantity  # Column must exist in data

# Verify columns in data
transforms:
  - type: columns
    columns: ['price', 'quantity', 'other_cols']
```

**Check data range**:
```yaml
# Problem: Empty data range
views:
  - type: hvplot
    kind: scatter
    xlim: [0, 10]  # If data is outside this range, won't show
```

### Table Not Paginating

**Problem**: Table shows all rows instead of paginating

**Solution**:
```yaml
views:
  - type: table
    pipeline: main
    page_size: 50
    pagination: remote  # Use 'remote' for large data

# For very large data, limit in pipeline
transforms:
  - type: head
    n: 10000
```

### Indicator Shows NaN

**Problem**: Indicator shows NaN or empty

**Check aggregation**:
```yaml
# Ensure pipeline produces aggregated value
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

## Performance Issues

### Slow Loading

**Problem**: Dashboard takes too long to load

**Solution 1: Limit data**:
```yaml
sources:
  db:
    type: postgres
    connection_string: ${DATABASE_URL}
    tables:
      # Limit at source
      recent: |
        SELECT * FROM sales
        WHERE date >= CURRENT_DATE - INTERVAL '30 days'
        LIMIT 100000
```

**Solution 2: Enable caching**:
```yaml
sources:
  db:
    type: postgres
    connection_string: ${DATABASE_URL}
    cache: true
    cache_dir: ./cache
    cache_timeout: 3600  # 1 hour
```

**Solution 3: Use Parquet**:
```yaml
# Convert CSV to Parquet for faster loading
sources:
  data:
    type: file
    tables:
      sales: ./data/sales.parquet  # Much faster than CSV
```

### Table Performance

**Problem**: Table with large dataset is slow

**Solution**:
```yaml
views:
  - type: table
    pipeline: main
    page_size: 50
    pagination: remote  # Server-side pagination (faster)

# Or limit rows
transforms:
  - type: head
    n: 10000
```

### Memory Issues

**Problem**: Dashboard crashes with out-of-memory

**Solution**:
```yaml
# Limit data size
transforms:
  - type: query
    query: "date >= '2024-01-01'"  # Filter early

  - type: columns
    columns: ['date', 'revenue']  # Select only needed columns

  - type: head
    n: 100000  # Limit rows
```

## Deployment Problems

### Port Already in Use

**Problem**: `Address already in use`

**Solution**:
```bash
# Find process using port
lsof -i :5006

# Kill process
kill -9 <PID>

# Or use different port
lumen serve dashboard.yaml --port 5007
```

### WebSocket Connection Failed

**Problem**: WebSocket connection issues in production

**Solution**:
```bash
# Allow WebSocket origins
panel serve dashboard.yaml \
  --allow-websocket-origin=dashboard.company.com \
  --allow-websocket-origin=www.dashboard.company.com
```

**Nginx configuration**:
```nginx
location / {
    proxy_pass http://localhost:5006;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
}
```

### Environment Variables Not Working

**Problem**: Environment variables not being read

**Solution**:
```bash
# Verify environment variable is set
echo $DATABASE_URL

# Set before running
export DATABASE_URL="postgresql://..."
lumen serve dashboard.yaml

# Or pass inline
DATABASE_URL="postgresql://..." lumen serve dashboard.yaml
```

**Docker**:
```yaml
# docker-compose.yml
services:
  dashboard:
    environment:
      - DATABASE_URL=${DATABASE_URL}  # From host environment
```

## Common Error Messages

### "Pipeline 'main' not found"

**Problem**: View references non-existent pipeline

**Solution**:
```yaml
pipelines:
  main:  # Define pipeline
    source: data
    table: sales

views:
  - type: hvplot
    pipeline: main  # Must match pipeline name
```

### "Table 'sales' not found"

**Problem**: Pipeline references non-existent table

**Solution**:
```yaml
sources:
  data:
    type: file
    tables:
      sales: ./data/sales.csv  # Define table

pipelines:
  main:
    source: data
    table: sales  # Must match table name
```

### "Field 'revenue' not found"

**Problem**: View references non-existent column

**Solution**:
```yaml
# Check column names in data
# Ensure transforms don't remove the column

views:
  - type: hvplot
    pipeline: main
    x: price      # Column must exist
    y: revenue    # Column must exist
```

### "Query syntax error"

**Problem**: Invalid query in transform

**Solution**:
```yaml
# Use pandas query syntax
transforms:
  # ✅ Good: Correct syntax
  - type: query
    query: "revenue > 1000 and category == 'A'"

  # ❌ Bad: Wrong operators
  - type: query
    query: "revenue > 1000 AND category = 'A'"  # Use 'and' and '=='
```

## Debugging Tips

### Enable Debug Logging

```bash
# Run with debug output
lumen serve dashboard.yaml --log-level=debug
```

### Test Components Separately

```yaml
# Test source
sources:
  data:
    type: file
    tables:
      test: ./data/test.csv

# Test pipeline
pipelines:
  test:
    source: data
    table: test
    # Comment out transforms to test raw data
    # transforms: []

# Test view
views:
  - type: table  # Table shows all data
    pipeline: test
```

### Simplify Configuration

```yaml
# Start minimal and add complexity
sources:
  data:
    type: file
    tables:
      sales: ./data/sales.csv

pipelines:
  main:
    source: data
    table: sales

layouts:
  - title: Test
    views:
      - type: table
        pipeline: main
```

## Best Practices

### 1. Validate Configuration

```bash
# Check YAML syntax before deploying
python -c "import yaml; yaml.safe_load(open('dashboard.yaml'))"

# Test locally first
lumen serve dashboard.yaml --autoreload
```

### 2. Use Error Handling

```yaml
# Provide fallback data
sources:
  primary:
    type: postgres
    connection_string: ${DATABASE_URL}

  fallback:
    type: file
    tables:
      sample: ./sample_data.csv
```

### 3. Monitor Logs

```bash
# Save logs to file
lumen serve dashboard.yaml 2>&1 | tee dashboard.log
```

### 4. Test with Small Data

```yaml
# Test with subset first
sources:
  data:
    type: postgres
    tables:
      test: SELECT * FROM sales LIMIT 1000  # Small sample
```

## Getting Help

### Check Documentation

- [Lumen Documentation](https://lumen.holoviz.org/)
- [Panel Documentation](https://panel.holoviz.org/)
- [HoloViews Documentation](https://holoviews.org/)

### Community Support

- [HoloViz Discourse](https://discourse.holoviz.org/)
- [GitHub Issues](https://github.com/holoviz/lumen/issues)

### Minimal Reproducible Example

When asking for help, provide:

```yaml
# Minimal example that shows the problem
sources:
  data:
    type: file
    tables:
      test: https://datasets.holoviz.org/penguins/v1/penguins.csv

pipelines:
  main:
    source: data
    table: test

layouts:
  - title: Problem
    views:
      - type: hvplot
        pipeline: main
        kind: scatter
        x: bill_length_mm
        y: bill_depth_mm
```

Include:
- Full error message
- Python/Lumen versions
- Operating system
- What you expected vs. what happened

## Summary

**Most common issues**:
- YAML syntax errors
- Source connection problems
- Column name mismatches
- Performance with large data

**Quick fixes**:
- Validate YAML syntax
- Check connection strings
- Verify column names
- Enable caching
- Limit data size

**Debugging workflow**:
1. Check logs for errors
2. Test components separately
3. Simplify configuration
4. Verify data at each step
5. Ask for help with minimal example

## References

- [Lumen Troubleshooting](https://lumen.holoviz.org/user_guide/Troubleshooting.html)
- [Panel Debugging](https://panel.holoviz.org/user_guide/Performance.html)
- [HoloViz Discourse](https://discourse.holoviz.org/)

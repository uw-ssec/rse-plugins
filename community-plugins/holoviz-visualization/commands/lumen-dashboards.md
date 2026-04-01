---
description: Build declarative no-code data dashboards with Lumen YAML specifications
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Lumen Dashboards

Build data dashboards declaratively with Lumen YAML specifications.

## Arguments

$ARGUMENTS — describe the dashboard (e.g., "dashboard from this CSV with filters", "multi-source dashboard with SQL and API", "cross-filtered explorer")

## Workflow

1. **Understand the data and requirements:**
   - Data sources (CSV, Parquet, SQL database, REST API)
   - Desired views (tables, charts, indicators)
   - Filtering and cross-filtering needs
   - Layout structure

2. **Design the YAML specification:**
   - Define data sources with connection details
   - Configure transforms (filters, aggregations, joins)
   - Create views with appropriate chart types
   - Design layout with tabs, rows, columns

3. **Write the Lumen YAML file:**
   - Sources section with data connections
   - Pipelines section with transforms
   - Layouts section with views and widgets
   - Config section for theme and settings

4. **Verify** the dashboard runs:
   ```bash
   lumen serve dashboard.yaml --show
   ```

5. **Report** the YAML specification and how to run it.

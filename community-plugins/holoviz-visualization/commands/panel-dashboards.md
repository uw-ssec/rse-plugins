---
description: Build interactive dashboards and web applications with Panel and Param
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Panel Dashboards

Build interactive dashboards and applications with Panel.

## Arguments

$ARGUMENTS — describe the dashboard (e.g., "monitoring dashboard with live metrics", "data explorer with file upload", "multi-page app with sidebar")

## Workflow

1. **Understand the requirements:**
   - Data sources and update frequency
   - User interactions needed (widgets, forms, uploads)
   - Layout structure (single page, multi-page, sidebar)
   - Deployment target (Jupyter, standalone server)

2. **Design the architecture:**
   - Choose template (Material, Bootstrap, Vanilla)
   - Plan component hierarchy
   - Design state management with Param
   - Plan callbacks and reactive dependencies

3. **Implement** using Panel:
   - Create Parameterized classes for state
   - Build widget panels for user input
   - Create visualization panels for output
   - Wire up callbacks with `@param.depends` or watchers
   - Apply responsive layout with `FlexBox`, `GridSpec`, or `Column`/`Row`

4. **Verify** the dashboard works:
   ```bash
   panel serve dashboard.py --show
   ```

5. **Report** the code and how to run it.

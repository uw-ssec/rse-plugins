---
description: Set up or improve Python package structure with pyproject.toml, src layout, and Hatchling following Scientific Python standards
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Python Packaging

Set up or improve a Python package following Scientific Python community standards.

## Arguments

$ARGUMENTS — optional description of what to package (e.g., "my spectral analysis library", "add CLI entry point")

## Workflow

1. **Explore the project** to understand current state:
   - Check for existing `pyproject.toml`, `setup.py`, `setup.cfg`
   - Identify source layout (src/ vs flat)
   - List existing Python modules and packages

2. **Determine the task** based on arguments:
   - **New package**: scaffold full structure (src layout, pyproject.toml, Hatchling backend)
   - **Migrate**: convert setup.py/setup.cfg to pyproject.toml
   - **Improve**: add missing metadata, optional dependencies, CLI entry points, or build config

3. **Apply Scientific Python packaging standards:**
   - Use `src/` layout
   - Hatchling as build backend
   - No upper version caps on Python (SPEC 0)
   - Proper metadata: name, version, description, license, classifiers, URLs
   - Optional dependency groups for dev, test, docs

4. **Verify** the package builds cleanly:
   ```bash
   python -m build --no-isolation 2>&1 | head -20
   ```

5. **Report** what was created or changed.

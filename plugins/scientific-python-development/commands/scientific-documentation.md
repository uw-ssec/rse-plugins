---
description: Set up or improve documentation for a scientific Python package using Sphinx, MkDocs, and Diataxis framework
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Scientific Documentation

Set up or improve documentation for a scientific Python project.

## Arguments

$ARGUMENTS — optional focus (e.g., "set up Sphinx docs", "add API reference", "organize with Diataxis", "fix build errors")

## Workflow

1. **Assess current state:**
   - Check for `docs/` directory, `conf.py`, `mkdocs.yml`
   - Scan for existing docstrings and their style
   - Identify documentation gaps

2. **Determine the task** based on arguments:
   - **Set up**: create docs structure with Sphinx or MkDocs
   - **API reference**: configure autodoc/napoleon for NumPy-style docstrings
   - **Organize**: restructure docs using Diataxis (tutorials, how-to, reference, explanation)
   - **Fix**: diagnose and fix documentation build errors

3. **Apply Scientific Python documentation standards:**
   - NumPy-style docstrings for all public functions
   - Diataxis framework for content organization
   - Intersphinx for cross-referencing NumPy, SciPy, etc.
   - pydata-sphinx-theme or furo for theming
   - Executable code examples in documentation

4. **Verify** the docs build cleanly:
   ```bash
   sphinx-build -W docs/ docs/_build/html
   ```

5. **Report** what was created or improved.

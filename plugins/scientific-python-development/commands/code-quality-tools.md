---
description: Set up or fix ruff, mypy, and pre-commit for scientific Python code quality
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Code Quality Tools

Configure or fix code quality tooling (ruff, mypy, pre-commit) for a scientific Python project.

## Arguments

$ARGUMENTS — optional focus (e.g., "set up ruff", "fix mypy errors", "add pre-commit hooks", "configure linting rules")

## Workflow

1. **Assess current state:**
   - Check `pyproject.toml` for existing ruff/mypy configuration
   - Look for `.pre-commit-config.yaml`
   - Identify any existing linting or formatting setup

2. **Determine the task** based on arguments:
   - **Set up**: add ruff + mypy config to pyproject.toml, create pre-commit config
   - **Fix errors**: run the tool, read output, fix issues
   - **Configure rules**: adjust ruff rule selection, mypy strictness

3. **Apply Scientific Python standards:**
   - Ruff for linting and formatting (replaces flake8, isort, black)
   - mypy for type checking with appropriate strictness
   - Pre-commit hooks for automated checks
   - Line length 88 (black-compatible)
   - NumPy-style docstring enforcement

4. **Verify** the configuration works:
   ```bash
   ruff check . && ruff format --check .
   ```

5. **Report** what was configured or fixed.

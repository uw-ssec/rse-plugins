---
description: Set up or manage pixi environments for reproducible scientific Python workflows
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Bash
---

# Pixi Package Manager

Set up or manage pixi for reproducible environment management in a scientific Python project.

## Arguments

$ARGUMENTS — optional task (e.g., "initialize pixi", "add numpy pandas", "migrate from conda", "add test task")

## Workflow

1. **Assess current state:**
   - Check for existing `pixi.toml`, `pixi.lock`
   - Look for `environment.yml`, `conda-lock.yml`, or `requirements.txt` (migration candidates)
   - Identify current dependency management approach

2. **Determine the task** based on arguments:
   - **Initialize**: `pixi init` with appropriate channels and platforms
   - **Add dependencies**: `pixi add` with version constraints from conda-forge + PyPI
   - **Migrate**: convert conda/pip environment to pixi.toml
   - **Tasks**: add pixi tasks for common operations (test, lint, docs, build)
   - **Multi-environment**: set up separate environments for dev, test, docs

3. **Apply best practices:**
   - conda-forge as primary channel
   - Lock files committed to version control
   - Task automation for common workflows
   - Platform-specific dependencies where needed

4. **Verify** the environment resolves:
   ```bash
   pixi install
   ```

5. **Report** what was configured and how to use it.

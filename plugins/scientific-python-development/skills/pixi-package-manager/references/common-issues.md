# Common Issues and Solutions

## Issue: Package Not Found in Conda-forge

**Problem**: Running `pixi add my-package` fails with "package not found"

**Solution**:
```bash
# Search conda-forge
pixi search my-package

# If not in conda-forge, use PyPI
pixi add --pypi my-package

# Check if package has different name in conda
# Example: scikit-learn (PyPI) vs sklearn (conda)
pixi add scikit-learn  # correct conda name
```

## Issue: Conflicting Dependencies

**Problem**: Dependency solver fails with "conflict" error

**Solution**:
```bash
# Check dependency tree
pixi tree numpy

# Use solve groups to isolate conflicts
[tool.pixi.environments]
env1 = { features = ["feat1"], solve-group = "group1" }
env2 = { features = ["feat2"], solve-group = "group2" }  # separate solver

# Relax version constraints
# Instead of: numpy==1.26.0
# Use: numpy>=1.24,<2.0

# Force specific channel priority
pixi add numpy -c conda-forge --force-reinstall
```

## Issue: Slow Environment Creation

**Problem**: `pixi install` takes very long

**Solution**:
```bash
# Use solve groups to avoid re-solving everything
[tool.pixi.environments]
default = { solve-group = "default" }
test = { features = ["test"], solve-group = "default" }  # reuses default solve

# Clean cache if corrupted
pixi clean cache

# Check for large dependency trees
pixi tree --depth 2

# Update pixi to latest version
pixi self-update
```

## Issue: Platform-Specific Failures

**Problem**: Works on Linux but fails on macOS/Windows

**Solution**:
```toml
# Use platform-specific dependencies
[tool.pixi.target.osx-arm64.dependencies]
# macOS ARM specific packages
tensorflow-macos = "*"

[tool.pixi.target.linux-64.dependencies]
# Linux-specific
tensorflow = "*"

# Exclude unsupported platforms
[tool.pixi.platforms]
linux-64 = true
osx-arm64 = true
# win-64 intentionally excluded if unsupported
```

## Issue: PyPI Package Installation Fails

**Problem**: `pixi add --pypi package` fails with build errors

**Solution**:
```bash
# Install build dependencies from conda first
pixi add python-build setuptools wheel

# Then retry PyPI package
pixi add --pypi package

# For packages needing system libraries
pixi add libgdal  # system library
pixi add --pypi gdal  # Python bindings

# Check if conda-forge version exists
pixi search gdal  # might have compiled version
```

## Issue: Lockfile Merge Conflicts

**Problem**: Git merge conflicts in `pixi.lock`

**Solution**:
```bash
# Accept one version
git checkout --theirs pixi.lock  # or --ours

# Regenerate lockfile
pixi install

# Commit regenerated lockfile
git add pixi.lock
git commit -m "Regenerate lockfile after merge"

# Prevention: coordinate updates with team
# One person updates dependencies at a time
```

## Issue: Editable Install of Local Package

**Problem**: Want to develop local package in pixi environment

**Solution**:
```toml
[tool.pixi.pypi-dependencies]
mypackage = { path = ".", editable = true }

# Or for relative paths
sibling-package = { path = "../sibling", editable = true }
```

```bash
# Install in development mode
pixi install

# Changes to source immediately reflected
pixi run python -c "import mypackage; print(mypackage.__file__)"
```


---
name: scientific-python-packaging
description: Create distributable scientific Python packages following Scientific Python community best practices with pyproject.toml, src layout, and Hatchling build backend
---

# Scientific Python Packaging

A comprehensive guide to creating, structuring, and distributing Python packages for scientific computing, following the [Scientific Python Community guidelines](https://learn.scientific-python.org/development/guides/packaging-simple/). This skill focuses on modern packaging standards using `pyproject.toml`, PEP 621 metadata, and the Hatchling build backend.

## Quick Decision Tree

**Package Structure Selection:**
```
START
  ├─ Pure Python scientific package (most common) → Pattern 1 (src/ layout)
  ├─ Need data files with package → Pattern 2 (data/ subdirectory)
  ├─ CLI tool → Pattern 5 (add [project.scripts])
  └─ Complex multi-feature package → Pattern 3 (full-featured)
```

**Build Backend Choice:**
```
START → Use Hatchling (recommended for scientific Python)
  ├─ Need VCS versioning? → Add hatch-vcs plugin
  ├─ Simple manual versioning? → version = "X.Y.Z" in pyproject.toml
  └─ Dynamic from __init__.py? → [tool.hatch.version] path
```

**Dependency Management:**
```
START
  ├─ Runtime dependencies → [project] dependencies
  ├─ Optional features → [project.optional-dependencies]
  ├─ Development tools → [dependency-groups] (PEP 735)
  └─ Version constraints → Use >= for minimum, avoid upper caps
```

**Publishing Workflow:**
```
1. Build: python -m build
2. Check: twine check dist/*
3. Test: twine upload --repository testpypi dist/*
4. Verify: pip install --index-url https://test.pypi.org/simple/ pkg
5. Publish: twine upload dist/*
```

**Common Task Quick Reference:**
```bash
# Setup new package
mkdir -p my-pkg/src/my_pkg && cd my-pkg
# Create pyproject.toml with [build-system] and [project] sections

# Development install
pip install -e . --group dev

# Build distributions
python -m build

# Test installation
pip install dist/*.whl

# Publish
twine upload dist/*
```

## When to Use This Skill

- Creating scientific Python libraries for distribution
- Building research software packages with proper structure
- Publishing scientific packages to PyPI
- Setting up reproducible scientific Python projects
- Creating installable packages with scientific dependencies
- Implementing command-line tools for scientific workflows
- Following community standards for scientific Python development
- Preparing packages for peer review and publication

## Core Concepts

### 1. Modern Build Systems

Python packages now use standardized build systems instead of classic `setup.py`:

- **PEP 621**: Standardized project metadata in `pyproject.toml`
- **PEP 517/518**: Build system independence
- **Build backend**: Hatchling
- **No classic files**: No `setup.py`, `setup.cfg`, or `MANIFEST.in`

### 2. Build Backend: Hatchling

- **Hatchling**: Excellent balance of speed, configurability, and extendability
- Modern, standards-compliant build backend
- Automatic package discovery in `src/` layout
- VCS-aware file inclusion for SDists
- Extensible through plugins

### 3. Package Structure

- **src/ layout**: Required for proper isolation (prevents importing uninstalled code)
- **Automatic discovery**: Hatchling auto-detects packages in `src/`
- **Standard structure**: Consistent organization for testing and documentation

### 4. Scientific Python Standards

- **Dependency management**: Careful version constraints
- **Python version support**: Minimum version without upper caps
- **Development dependencies**: Use dependency-groups (PEP 735)
- **Documentation**: Include README, LICENSE, and docs folder
- **Testing**: Dedicated tests folder

## Quick Start

### Minimal Scientific Package Structure

```
my-sci-package/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── my_sci_package/
│       ├── __init__.py
│       ├── analysis.py
│       └── utils.py
├── tests/
│   ├── test_analysis.py
│   └── test_utils.py
└── docs/
    └── index.md
```

### Minimal pyproject.toml with Hatchling

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-sci-package"
version = "0.1.0"
description = "A scientific Python package for data analysis"
readme = "README.md"
license = "BSD-3-Clause"
license-files = ["LICENSE"]
requires-python = ">=3.9"
authors = [
    {name = "Your Name", email = "you@example.com"},
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Scientific/Engineering",
]

dependencies = [
    "numpy>=1.20",
    "scipy>=1.7",
]

[project.urls]
Homepage = "https://github.com/username/my-sci-package"
Documentation = "https://my-sci-package.readthedocs.io"
"Bug Tracker" = "https://github.com/username/my-sci-package/issues"
Discussions = "https://github.com/username/my-sci-package/discussions"
Changelog = "https://my-sci-package.readthedocs.io/en/latest/changelog.html"

[dependency-groups]
test = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
]
dev = [
    {include-group = "test"},
    "ruff>=0.1",
    "mypy>=1.0",
]
```

## Package Structure Patterns

### Pattern 1: Pure Python Scientific Package (Recommended)

```
my-sci-package/
├── pyproject.toml
├── README.md
├── LICENSE
├── .gitignore
├── src/
│   └── my_sci_package/
│       ├── __init__.py
│       ├── analysis.py
│       ├── preprocessing.py
│       ├── visualization.py
│       ├── utils.py
│       └── py.typed          # For type hints
├── tests/
│   ├── __init__.py
│   ├── test_analysis.py
│   ├── test_preprocessing.py
│   └── test_visualization.py
└── docs/
    ├── conf.py
    ├── index.md
    └── api.md
```

**Key advantages:**
- Prevents accidental imports from source
- Forces proper installation for testing
- Professional structure for scientific libraries
- Clear separation of concerns

### Pattern 2: Scientific Package with Data Files

```
my-sci-package/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── my_sci_package/
│       ├── __init__.py
│       ├── analysis.py
│       └── data/
│           ├── reference.csv
│           ├── constants.json
│           └── coefficients.dat
├── tests/
│   └── test_analysis.py
└── docs/
    └── index.md
```

**Include data files in pyproject.toml (if needed):**

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/my_sci_package"]

# Only if you need to explicitly include data
[tool.hatch.build.targets.wheel.force-include]
"src/my_sci_package/data" = "my_sci_package/data"
```

**Access data files in code:**

```python
from importlib.resources import files
import json

def load_constants():
    """Load constants from package data."""
    data_file = files("my_sci_package").joinpath("data/constants.json")
    with data_file.open() as f:
        return json.load(f)
```

## Complete pyproject.toml Examples

### Pattern 3: Full-Featured Scientific Package

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "advanced-sci-package"
version = "1.0.0"
description = "Advanced scientific computing package"
readme = "README.md"
license = "BSD-3-Clause"
license-files = ["LICENSE"]
requires-python = ">=3.9"
authors = [
    {name = "Research Team", email = "team@university.edu"},
]
maintainers = [
    {name = "Lead Maintainer", email = "maintainer@university.edu"},
]
keywords = ["scientific-computing", "data-analysis", "research"]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Physics",
    "Topic :: Scientific/Engineering :: Mathematics",
]

dependencies = [
    "numpy>=1.20",
    "scipy>=1.7",
    "pandas>=1.3",
    "matplotlib>=3.4",
]

[project.optional-dependencies]
ml = [
    "scikit-learn>=1.0",
    "tensorflow>=2.8",
]
viz = [
    "plotly>=5.0",
    "seaborn>=0.11",
]
all = [
    "advanced-sci-package[ml,viz]",
]

[project.urls]
Homepage = "https://github.com/org/advanced-sci-package"
Documentation = "https://advanced-sci-package.readthedocs.io"
Repository = "https://github.com/org/advanced-sci-package"
"Bug Tracker" = "https://github.com/org/advanced-sci-package/issues"
Discussions = "https://github.com/org/advanced-sci-package/discussions"
Changelog = "https://advanced-sci-package.readthedocs.io/en/latest/changelog.html"

[project.scripts]
sci-analyze = "advanced_sci_package.cli:main"

[dependency-groups]
test = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "pytest-xdist>=3.0",
]
docs = [
    "sphinx>=5.0",
    "sphinx-rtd-theme>=1.0",
    "numpydoc>=1.5",
]
dev = [
    {include-group = "test"},
    {include-group = "docs"},
    "ruff>=0.1",
    "mypy>=1.0",
    "pre-commit>=3.0",
]

# Hatchling configuration
[tool.hatch.build.targets.wheel]
packages = ["src/advanced_sci_package"]

# Ruff configuration (linting and formatting)
[tool.ruff]
line-length = 88
target-version = "py39"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "NPY", "RUF"]
ignore = ["E501"]  # Line too long (handled by formatter)

# Pytest configuration
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-v --cov=advanced_sci_package --cov-report=term-missing"

# MyPy configuration
[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

# Coverage configuration
[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
```

## Project Metadata

### License (Modern SPDX Format)

Use SPDX identifiers (supported by hatchling>=1.26):

```toml
[project]
license = "BSD-3-Clause"
license-files = ["LICENSE"]
```

Common scientific licenses:
- `MIT` - Permissive, simple
- `BSD-3-Clause` - Permissive, commonly used in science
- `Apache-2.0` - Permissive, explicit patent grant
- `GPL-3.0-or-later` - Copyleft

**Do not include License classifiers if using the `license` field.**

### Python Version Requirements

**Best practice**: Specify minimum version only, no upper cap:

```toml
requires-python = ">=3.9"
```

This allows pip to back-solve for old package versions when needed.

### Dependencies

**Use appropriate version constraints:**

```toml
dependencies = [
    "numpy>=1.20",              # Minimum version
    "scipy>=1.7,<2.0",          # Compatible range (use sparingly)
    "pandas>=1.3",              # Open-ended (preferred)
    "matplotlib>=3.4",          # Minimum version
]
```

**Avoid pinning exact versions unless absolutely necessary.**

### Classifiers

Important classifiers for scientific packages:

```toml
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Physics",
    "Typing :: Typed",
]
```

[Browse all classifiers](https://pypi.org/classifiers/)

## Optional Dependencies (Extras)

Use extras for optional scientific features:

```toml
[project.optional-dependencies]
plotting = [
    "matplotlib>=3.4",
    "seaborn>=0.11",
]
ml = [
    "scikit-learn>=1.0",
    "xgboost>=1.5",
]
parallel = [
    "dask[array]>=2021.0",
    "joblib>=1.0",
]
all = [
    "my-sci-package[plotting,ml,parallel]",
]
```

**Install with extras:**
```bash
pip install my-sci-package[plotting]
pip install my-sci-package[plotting,ml]
pip install my-sci-package[all]
```

## Development Dependencies (Dependency Groups)

Use `dependency-groups` (PEP 735) instead of extras for development tools:

```toml
[dependency-groups]
test = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "hypothesis>=6.0",
]
docs = [
    "sphinx>=5.0",
    "numpydoc>=1.5",
    "sphinx-gallery>=0.11",
]
dev = [
    {include-group = "test"},
    {include-group = "docs"},
    "ruff>=0.1",
    "mypy>=1.0",
]
```

**Install dependency groups:**
```bash
# Using uv (recommended)
uv pip install --group dev

# Using pip 25.1+
pip install --group dev

# Traditional approach with editable install
pip install -e ".[dev]"  # if using extras
```

**Advantages over extras:**
- Formally standardized
- More composable
- Not available on PyPI (development-only)
- Installed by default with `uv`

## Command-Line Interface

### Pattern 5: Scientific CLI Tool

```python
# src/my_sci_package/cli.py
import click
import numpy as np
from pathlib import Path

@click.group()
@click.version_option()
def cli():
    """Scientific analysis CLI tool."""
    pass

@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="Output file path")
@click.option("--threshold", "-t", type=float, default=0.5, help="Analysis threshold")
def analyze(input_file: str, output: str, threshold: float):
    """Analyze scientific data from input file."""
    # Load and analyze data
    data = np.loadtxt(input_file)
    result = np.mean(data[data > threshold])
    
    click.echo(f"Analysis complete: mean = {result:.4f}")
    
    if output:
        np.savetxt(output, [result])
        click.echo(f"Results saved to {output}")

@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--format", type=click.Choice(["png", "pdf", "svg"]), default="png")
def plot(input_file: str, format: str):
    """Generate plots from data."""
    import matplotlib.pyplot as plt
    
    data = np.loadtxt(input_file)
    plt.plot(data)
    output_file = f"plot.{format}"
    plt.savefig(output_file)
    click.echo(f"Plot saved to {output_file}")

def main():
    """Entry point for CLI."""
    cli()

if __name__ == "__main__":
    main()
```

**Register in pyproject.toml:**

```toml
[project.scripts]
sci-analyze = "my_sci_package.cli:main"
```

**Usage:**
```bash
pip install -e .
sci-analyze analyze data.txt --threshold 0.7
sci-analyze plot data.txt --format pdf
```

## Versioning

### Pattern 6: Manual Versioning

```toml
[project]
version = "1.2.3"
```

```python
# src/my_sci_package/__init__.py
__version__ = "1.2.3"
```

### Pattern 7: Dynamic Versioning with Hatchling

```toml
[project]
dynamic = ["version"]

[tool.hatch.version]
path = "src/my_sci_package/__init__.py"
```

```python
# src/my_sci_package/__init__.py
__version__ = "1.2.3"
```

### Pattern 8: Git-Based Versioning with Hatchling

```toml
[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"

[project]
dynamic = ["version"]

[tool.hatch.version]
source = "vcs"

[tool.hatch.build.hooks.vcs]
version-file = "src/my_sci_package/_version.py"
```

**Semantic versioning for scientific software:**
- `MAJOR`: Breaking API changes
- `MINOR`: New features, backward compatible
- `PATCH`: Bug fixes

## Building and Publishing

### Pattern 9: Build Package Locally

```bash
# Install build tools
pip install build

# Build distribution
python -m build

# Creates:
# dist/my-sci-package-1.0.0.tar.gz (source distribution)
# dist/my_sci_package-1.0.0-py3-none-any.whl (wheel)

# Verify the distribution
pip install twine
twine check dist/*

# Inspect contents
tar -tvf dist/*.tar.gz
unzip -l dist/*.whl
```

**Critical**: Test the SDist contents to ensure all necessary files are included.

### Pattern 10: Publishing to PyPI

```bash
# Install publishing tools
pip install twine

# Test on TestPyPI first (always!)
twine upload --repository testpypi dist/*

# Install and test from TestPyPI
pip install --index-url https://test.pypi.org/simple/ my-sci-package

# If everything works, publish to PyPI
twine upload dist/*
```

**Using API tokens (recommended):**

Create `~/.pypirc`:
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-...your-token...

[testpypi]
username = __token__
password = pypi-...your-test-token...
```

### Pattern 11: Automated Publishing with GitHub Actions

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    environment: release
    permissions:
      id-token: write  # For trusted publishing

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install build tools
        run: pip install build

      - name: Build package
        run: python -m build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
```

**Use PyPI trusted publishing instead of API tokens for GitHub Actions.**

## Testing Installation

### Pattern 12: Editable Install for Development

```bash
# Install in development mode
pip install -e .

# With dependency groups
pip install -e . --group dev

# Using uv (recommended for scientific workflows)
uv pip install -e . --group dev

# Now changes to source code are immediately reflected
```

### Pattern 13: Testing in Isolated Environment

```bash
# Create and activate virtual environment
python -m venv test-env
source test-env/bin/activate  # Linux/Mac

# Install from wheel
pip install dist/my_sci_package-1.0.0-py3-none-any.whl

# Test import and version
python -c "import my_sci_package; print(my_sci_package.__version__)"

# Test CLI
sci-analyze --help

# Cleanup
deactivate
rm -rf test-env
```

## Documentation

### Pattern 14: Scientific Package README.md

```markdown
# My Scientific Package

[![PyPI version](https://badge.fury.io/py/my-sci-package.svg)](https://pypi.org/project/my-sci-package/)
[![Python versions](https://img.shields.io/pypi/pyversions/my-sci-package.svg)](https://pypi.org/project/my-sci-package/)
[![Tests](https://github.com/username/my-sci-package/workflows/Tests/badge.svg)](https://github.com/username/my-sci-package/actions)
[![Documentation](https://readthedocs.org/projects/my-sci-package/badge/?version=latest)](https://my-sci-package.readthedocs.io/)

A Python package for [brief description of scientific purpose].

## Features

- Feature 1: Description
- Feature 2: Description
- Feature 3: Description

## Installation

```bash
pip install my-sci-package
```

For plotting capabilities:
```bash
pip install my-sci-package[plotting]
```

## Quick Start

```python
import my_sci_package as msp
import numpy as np

# Example usage
data = np.random.randn(100)
result = msp.analyze(data, threshold=0.5)
print(f"Result: {result}")
```

## Documentation

Full documentation: https://my-sci-package.readthedocs.io

## Citation

If you use this package in your research, please cite:

```bibtex
@software{my_sci_package,
  author = {Your Name},
  title = {My Scientific Package},
  year = {2025},
  url = {https://github.com/username/my-sci-package}
}
```

## Development

```bash
git clone https://github.com/username/my-sci-package.git
cd my-sci-package
pip install -e . --group dev
pytest
```

## License

BSD-3-Clause License - see LICENSE file for details.
```

## File Templates

### .gitignore for Scientific Python Packages

```gitignore
# Build artifacts
build/
dist/
*.egg-info/
*.egg
.eggs/
src/**/_version.py

# Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp

# Testing
.pytest_cache/
.coverage
htmlcov/
.hypothesis/

# Documentation
docs/_build/
docs/_generated/

# Scientific data (adjust as needed)
*.hdf5
*.nc
*.mat
data/processed/

# Jupyter
.ipynb_checkpoints/
*.ipynb

# Distribution
*.whl
*.tar.gz
```

### Pattern 15: Sphinx Documentation Setup

```python
# docs/conf.py
import sys
from pathlib import Path

# Add package to path
sys.path.insert(0, str(Path("..").resolve() / "src"))

# Project information
project = "My Scientific Package"
copyright = "2025, Your Name"
author = "Your Name"

# Extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",  # NumPy/Google style docstrings
    "sphinx.ext.viewcode",
    "sphinx.ext.mathjax",   # Math rendering
    "sphinx.ext.intersphinx",
    "numpydoc",             # NumPy documentation style
]

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
}

# Theme
html_theme = "sphinx_rtd_theme"
```

## Checklist for Publishing Scientific Packages

- [ ] Code is tested with pytest (>90% coverage recommended)
- [ ] Documentation is complete (README, docstrings, Sphinx docs)
- [ ] Version number follows semantic versioning
- [ ] CHANGELOG.md or NEWS.md updated
- [ ] LICENSE file included with appropriate license
- [ ] pyproject.toml has complete metadata
- [ ] Package uses src/ layout
- [ ] Package builds without errors (`python -m build`)
- [ ] SDist contents verified (`tar -tvf dist/*.tar.gz`)
- [ ] Installation tested in clean environment
- [ ] CLI tools work if applicable
- [ ] All classifiers are appropriate
- [ ] Python version constraint is correct (no upper bound)
- [ ] Dependencies have appropriate version constraints
- [ ] Repository is linked in project.urls
- [ ] Tested on TestPyPI first
- [ ] GitHub release created (if using)
- [ ] Documentation published (ReadTheDocs, GitHub Pages)
- [ ] Citation information included (CITATION.cff or README)

## Best Practices for Scientific Python Packages

1. **Use src/ layout** - Prevents importing uninstalled code, ensures proper testing
2. **Use pyproject.toml** - Modern standard, tool-independent configuration
3. **Use Hatchling** - Modern, fast, and configurable build backend
4. **No classic files** - Avoid setup.py, setup.cfg, MANIFEST.in
5. **Version constraints** - Minimum versions for dependencies, no upper cap for Python
6. **Test SDist contents** - Always verify what files are included/excluded
7. **Use TestPyPI** - Always test publishing before going to production
8. **Document thoroughly** - README, docstrings, Sphinx documentation
9. **Include LICENSE** - Use SPDX identifiers, choose appropriate scientific license
10. **Use dependency-groups** - For development dependencies (PEP 735)
11. **Semantic versioning** - Clear versioning strategy
12. **Automate CI/CD** - GitHub Actions for testing and publishing
13. **Type hints** - Include py.typed marker for typed packages
14. **Citation information** - Make it easy for users to cite your work
15. **Community standards** - Follow Scientific Python guidelines

## Scientific Python Specific Considerations

### NumPy-style Docstrings

```python
def analyze_data(data, threshold=0.5, method="mean"):
    """
    Analyze scientific data above a threshold.

    Parameters
    ----------
    data : array_like
        Input data array to analyze.
    threshold : float, optional
        Minimum value for inclusion in analysis, by default 0.5.
    method : {"mean", "median", "std"}, optional
        Statistical method to apply, by default "mean".

    Returns
    -------
    result : float
        Computed statistical result.

    Raises
    ------
    ValueError
        If method is not recognized.

    Examples
    --------
    >>> import numpy as np
    >>> data = np.array([0.1, 0.6, 0.8, 0.3, 0.9])
    >>> analyze_data(data, threshold=0.5)
    0.7666666666666667

    Notes
    -----
    This function uses NumPy for efficient computation.

    References
    ----------
    .. [1] Harris et al., "Array programming with NumPy", Nature 585, 2020.
    """
    pass
```

### Scientific Dependencies

Common scientific Python dependencies:

```toml
dependencies = [
    "numpy>=1.20",          # Arrays and numerical computing
    "scipy>=1.7",           # Scientific computing algorithms
    "pandas>=1.3",          # Data structures and analysis
    "matplotlib>=3.4",      # Plotting
    "xarray>=0.19",         # Labeled multi-dimensional arrays
    "scikit-learn>=1.0",    # Machine learning
    "astropy>=5.0",         # Astronomy (if applicable)
]
```

### Reproducibility

Include information for reproducibility:

```toml
[project.urls]
"Source Code" = "https://github.com/org/package"
"Documentation" = "https://package.readthedocs.io"
"Bug Reports" = "https://github.com/org/package/issues"
"Changelog" = "https://github.com/org/package/blob/main/CHANGELOG.md"
"Citation" = "https://doi.org/10.xxxx/xxxxx"  # DOI if available
```

## Resources

- **Scientific Python Development Guide**: https://learn.scientific-python.org/development/
- **Simple Packaging Guide**: https://learn.scientific-python.org/development/guides/packaging-simple/
- **Python Packaging Guide**: https://packaging.python.org/
- **PyPI**: https://pypi.org/
- **TestPyPI**: https://test.pypi.org/
- **Hatchling documentation**: https://hatch.pypa.io/latest/
- **build**: https://pypa-build.readthedocs.io/
- **twine**: https://twine.readthedocs.io/
- **Scientific Python Cookie**: https://github.com/scientific-python/cookie
- **NumPy documentation style**: https://numpydoc.readthedocs.io/

## Common Issues and Solutions

### Issue: Import errors in tests

**Problem**: Tests import the source code instead of installed package.

**Solution**: Use src/ layout and install package with `pip install -e .`

### Issue: Missing files in distribution

**Problem**: Data files or documentation not included in SDist/wheel.

**Solution**: 
- For Hatchling: VCS ignore file controls SDist contents
- Check with: `tar -tvf dist/*.tar.gz`
- Explicitly configure if needed in `[tool.hatch.build]`

### Issue: Dependency conflicts

**Problem**: Users cannot install due to incompatible dependency versions.

**Solution**: Use minimal version constraints, avoid upper bounds on dependencies.

### Issue: Python version incompatibility

**Problem**: Package doesn't work on newer Python versions.

**Solution**: Don't cap `requires-python`, test on multiple Python versions with CI.

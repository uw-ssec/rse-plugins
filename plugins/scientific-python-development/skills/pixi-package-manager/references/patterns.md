# Pixi Patterns

## Pattern 1: Converting Existing Projects to Pixi

**Scenario**: You have an existing project with `requirements.txt` or `environment.yml`

**Solution**:

```bash
# From requirements.txt
cd existing-project
pixi init --format pyproject

# Import from requirements.txt
while IFS= read -r package; do
    # Skip comments and empty lines
    [[ "$package" =~ ^#.*$ ]] || [[ -z "$package" ]] && continue

    # Try conda first, fallback to PyPI
    pixi add "$package" 2>/dev/null || pixi add --pypi "$package"
done < requirements.txt

# From environment.yml
pixi init --format pyproject --import-environment environment.yml

# Verify installation
pixi install
pixi run python -c "import numpy, pandas, scipy; print('Success!')"
```

**Best Practice**: Review generated `pyproject.toml` and organize dependencies:
- Core runtime dependencies → `[project.dependencies]`
- PyPI-only packages → `[tool.pixi.pypi-dependencies]`
- Development tools → `[tool.pixi.feature.dev.dependencies]`

## Pattern 2: Multi-Environment Scientific Workflow

See [assets/pyproject-multi-env.toml](assets/pyproject-multi-env.toml) for a complete example of multi-environment configuration.

**Key concepts:**
- Use features to organize dependencies by purpose (dev, test, gpu, etc.)
- Combine features in environments
- Use solve groups to isolate independent environments
- Define tasks for common workflows

## Pattern 3: Scientific Library Development

**Structure**:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mylib"
version = "0.1.0"
description = "Scientific computing library"
dependencies = [
    "numpy>=1.24",
    "scipy>=1.11",
]

[project.optional-dependencies]
viz = ["matplotlib>=3.7", "seaborn>=0.12"]

# Development dependencies
[tool.pixi.feature.dev.dependencies]
ipython = "*"
ruff = "*"
mypy = "*"

# Testing dependencies
[tool.pixi.feature.test.dependencies]
pytest = ">=7.4"
pytest-cov = ">=4.1"
pytest-benchmark = ">=4.0"
hypothesis = ">=6.82"

# Documentation dependencies
[tool.pixi.feature.docs.dependencies]
sphinx = ">=7.0"
sphinx-rtd-theme = ">=1.3"
numpydoc = ">=1.5"
sphinx-gallery = ">=0.14"

[tool.pixi.feature.docs.pypi-dependencies]
myst-parser = ">=2.0"

# Build dependencies
[tool.pixi.feature.build.dependencies]
build = "*"
twine = "*"

[tool.pixi.environments]
default = { features = [], solve-group = "default" }
dev = { features = ["dev", "test", "docs"], solve-group = "default" }
test = { features = ["test"], solve-group = "default" }
docs = { features = ["docs"], solve-group = "default" }

# Tasks for development workflow
[tool.pixi.tasks]
# Development
install-dev = "pip install -e ."
format = "ruff format src/ tests/"
lint = "ruff check src/ tests/"
typecheck = "mypy src/"

# Testing
test = "pytest tests/ -v"
test-cov = "pytest tests/ --cov=src --cov-report=html --cov-report=term"
test-fast = "pytest tests/ -x -v"
benchmark = "pytest tests/benchmarks/ --benchmark-only"

# Documentation
docs-build = "sphinx-build docs/ docs/_build/html"
docs-serve = { cmd = "python -m http.server 8000 -d docs/_build/html", depends-on = ["docs-build"] }
docs-clean = "rm -rf docs/_build docs/generated"

# Build and release
build = "python -m build"
publish-test = { cmd = "twine upload --repository testpypi dist/*", depends-on = ["build"] }
publish = { cmd = "twine upload dist/*", depends-on = ["build"] }

# Combined workflows
ci = { depends-on = ["format", "lint", "typecheck", "test-cov"] }
pre-commit = { depends-on = ["format", "lint", "test-fast"] }
```

## Pattern 4: Conda + PyPI Dependency Strategy

**Strategy**:

```toml
[project]
dependencies = [
    # Core scientific stack: prefer conda-forge (optimized builds)
    "numpy>=1.24",           # MKL or OpenBLAS optimized
    "scipy>=1.11",           # optimized BLAS/LAPACK
    "pandas>=2.0",           # optimized pandas
    "matplotlib>=3.7",       # compiled components
    "scikit-learn>=1.3",     # optimized algorithms

    # Geospatial/climate: conda-forge essential (C/Fortran deps)
    "xarray>=2023.1",
    "netcdf4>=1.6",
    "h5py>=3.9",
    "rasterio>=1.3",         # GDAL dependency

    # Data processing: conda-forge preferred
    "dask>=2023.1",
    "numba>=0.57",           # LLVM dependency
]

[tool.pixi.pypi-dependencies]
# Pure Python packages or PyPI-only packages
my-custom-tool = ">=1.0"
experimental-lib = { git = "https://github.com/user/repo.git" }
internal-pkg = { path = "../internal-pkg", editable = true }
```

**Decision Rules**:

1. **Use conda-forge (pixi add) for**:
   - NumPy, SciPy, Pandas (optimized builds)
   - Packages with C/C++/Fortran extensions (GDAL, netCDF4, h5py)
   - Packages with complex system dependencies (Qt, OpenCV)
   - R, Julia, or other language packages

2. **Use PyPI (pixi add --pypi) for**:
   - Pure Python packages not in conda-forge
   - Bleeding-edge versions before conda-forge packaging
   - Internal/private packages
   - Editable local packages during development

## Pattern 5: Reproducible Research Environment

**Implementation**:

```toml
[project]
name = "nature-paper-2024"
version = "1.0.0"
description = "Analysis for Nature Paper 2024"
requires-python = ">=3.11,<3.12"  # pin Python version range

dependencies = [
    "python=3.11.6",      # exact Python version
    "numpy=1.26.2",       # exact versions for reproducibility
    "pandas=2.1.4",
    "scipy=1.11.4",
    "matplotlib=3.8.2",
    "scikit-learn=1.3.2",
]

[tool.pixi.pypi-dependencies]
# Pin with exact hashes for ultimate reproducibility
seaborn = "==0.13.0"

# Analysis environments
[tool.pixi.feature.analysis.dependencies]
jupyter = "1.0.0"
jupyterlab = "4.0.9"

[tool.pixi.feature.analysis.pypi-dependencies]
jupyterlab-vim = "0.16.0"

# Environments
[tool.pixi.environments]
default = { solve-group = "default" }
analysis = { features = ["analysis"], solve-group = "default" }

# Reproducible tasks
[tool.pixi.tasks]
# Data processing pipeline
download-data = "python scripts/01_download.py"
preprocess = { cmd = "python scripts/02_preprocess.py", depends-on = ["download-data"] }
analyze = { cmd = "python scripts/03_analyze.py", depends-on = ["preprocess"] }
visualize = { cmd = "python scripts/04_visualize.py", depends-on = ["analyze"] }
full-pipeline = { depends-on = ["download-data", "preprocess", "analyze", "visualize"] }

# Notebook execution
run-notebooks = "jupyter nbconvert --execute --to notebook --inplace notebooks/*.ipynb"
```

**Best Practices**:

```bash
# Generate lockfile
pixi install

# Commit lockfile to repository
git add pixi.lock pyproject.toml
git commit -m "Lock environment for reproducibility"

# Anyone can recreate exact environment
git clone https://github.com/user/nature-paper-2024.git
cd nature-paper-2024
pixi install  # installs exact versions from pixi.lock

# Run complete pipeline
pixi run full-pipeline

# Archive for long-term preservation
pixi list --export environment.yml  # backup as conda format
```

## Pattern 6: Task Dependencies and Workflows

**Scenario**: Complex scientific workflows with data dependencies

**Implementation**:

```toml
[tool.pixi.tasks]
# Data acquisition
download-raw = "python scripts/download.py --source=api"
validate-raw = { cmd = "python scripts/validate.py data/raw/", depends-on = ["download-raw"] }

# Data processing pipeline
clean-data = { cmd = "python scripts/clean.py", depends-on = ["validate-raw"] }
transform = { cmd = "python scripts/transform.py", depends-on = ["clean-data"] }
feature-engineering = { cmd = "python scripts/features.py", depends-on = ["transform"] }

# Analysis
train-model = { cmd = "python scripts/train.py", depends-on = ["feature-engineering"] }
evaluate = { cmd = "python scripts/evaluate.py", depends-on = ["train-model"] }
visualize = { cmd = "python scripts/visualize.py", depends-on = ["evaluate"] }

# Testing at each stage
test-cleaning = "pytest tests/test_clean.py"
test-transform = "pytest tests/test_transform.py"
test-features = "pytest tests/test_features.py"
test-model = "pytest tests/test_model.py"

# Combined workflows
all-tests = { depends-on = ["test-cleaning", "test-transform", "test-features", "test-model"] }
full-pipeline = { depends-on = ["download-raw", "validate-raw", "clean-data", "transform", "feature-engineering", "train-model", "evaluate", "visualize"] }
pipeline-with-tests = { depends-on = ["all-tests", "full-pipeline"] }
```

**Running Workflows**:

```bash
# Run entire pipeline
pixi run full-pipeline

# Run with testing
pixi run pipeline-with-tests

# Check what will run
pixi task list --summary

# Visualize task dependencies
pixi task info full-pipeline
```


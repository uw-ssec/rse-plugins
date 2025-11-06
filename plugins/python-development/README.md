# Python Development Plugin

Comprehensive agents and skills for modern Scientific Python development following community best practices.

## Overview

This plugin provides expert guidance for scientific Python development, emphasizing reproducibility, modern tooling, and community standards from the [Scientific Python Development Guide](https://learn.scientific-python.org/development/).

**Version:** 0.1.0

**Contents:**
- 1 Agent (Scientific Python Expert)
- 3 Skills (pixi, packaging, testing)

## Available Agents

### Scientific Python Expert

**File:** [agents/scientific-python-expert.md](agents/scientific-python-expert.md)

**Description:** Comprehensive agent for building reproducible scientific software using the modern Python ecosystem (NumPy, Pandas, SciPy, Matplotlib, Xarray). Expert in environment management with pixi, modern packaging, testing strategies, and performance optimization.

**Capabilities:**
- Scientific Python stack (NumPy, Pandas, SciPy, Matplotlib, Xarray, scikit-learn)
- Modern environment management with pixi
- Python packaging with pyproject.toml and src layout
- Testing with pytest and Hypothesis
- Code quality with ruff and mypy
- Documentation with Sphinx and NumPy-style docstrings
- Performance optimization with vectorization and Numba
- Data I/O (HDF5, NetCDF, Parquet, Zarr)

**When to use:**
- Building scientific computing applications
- Developing research software and data analysis pipelines
- Creating distributable Python packages for science
- Implementing reproducible computational workflows
- Setting up modern Python projects from scratch

**Key features:**
- Follows Scientific Python Process principles (Collaborate, Refactor, Wide over Deep)
- Structured decision-making framework for technical choices
- Self-review checklist for correctness, quality, reproducibility
- Comprehensive error handling and validation

## Available Skills

### Pixi Package Manager

**File:** [skills/pixi-package-manager/SKILL.md](skills/pixi-package-manager/SKILL.md)

**Description:** Master the pixi package manager for fast, reproducible scientific Python environments that unify conda and PyPI ecosystems.

**Key topics:**
- Installation and project initialization
- Unified conda + PyPI dependency management
- Multi-platform lockfiles for reproducibility
- Feature-based environments (dev, test, prod, GPU)
- Task automation and workflow management
- Cross-platform development
- CI/CD integration
- Migrating from conda/requirements.txt

**When to use:**
- Setting up projects with complex compiled dependencies (NumPy, SciPy, GDAL, netCDF4)
- Managing multi-environment workflows (development, testing, production)
- Ensuring reproducibility across platforms and time
- Combining conda-forge and PyPI packages
- Replacing conda/mamba with faster tooling

**Includes:** Quick reference card, decision trees, 13 detailed patterns, best practices checklist, troubleshooting guide

### Python Packaging

**File:** [skills/python-packaging/SKILL.md](skills/python-packaging/SKILL.md)

**Description:** Create distributable scientific Python packages following modern standards with pyproject.toml, src layout, and Hatchling build backend.

**Key topics:**
- Modern build systems (PEP 621, Hatchling)
- src/ layout for proper isolation
- Project metadata and dependencies
- Optional dependencies (extras) and dependency groups
- Command-line interface creation
- Versioning strategies
- Building and publishing to PyPI
- Testing installation
- Sphinx documentation setup

**When to use:**
- Creating scientific Python libraries for distribution
- Publishing packages to PyPI
- Setting up proper package structure
- Managing dependencies and optional features
- Building command-line tools for science

**Includes:** Quick reference, decision trees, 15 patterns, complete examples, publishing workflows, checklists

### Python Testing

**File:** [skills/python-testing/SKILL.md](skills/python-testing/SKILL.md)

**Description:** Write robust, maintainable tests for scientific Python packages using pytest, following Scientific Python community guidelines.

**Key topics:**
- pytest fundamentals and configuration
- Testing principles (outside-in approach, test suites)
- Approximate comparisons for numerical code
- Fixtures and parametrization
- Test organization with markers and directories
- Mocking and monkeypatching
- NumPy array testing
- Testing random/stochastic code
- Property-based testing with Hypothesis
- Coverage reporting

**When to use:**
- Writing tests for scientific computations
- Testing numerical algorithms and data pipelines
- Setting up test infrastructure for research code
- Implementing CI/CD for scientific software
- Validating scientific simulations

**Includes:** Quick reference card, decision trees, 13 patterns, testing checklist, CI/CD examples

## Architecture and Design

### Scientific Python Principles

This plugin follows the [Scientific Python Process recommendations](https://learn.scientific-python.org/development/principles/process/):

1. **Collaborate** - Use conventions and tooling from the broader scientific Python community for easier collaboration
2. **Don't Be Afraid to Refactor** - Leverage tests and tooling to iterate confidently
3. **Prefer Wide Over Deep** - Build reusable, extensible solutions for unforeseen applications

### Testing Approach

Follows the [outside-in testing strategy](https://learn.scientific-python.org/development/principles/testing/):

1. **Public Interface Tests** - Test from user perspective
2. **Integration Tests** - Test component interactions
3. **Unit Tests** - Test isolated components for speed

### Code Quality Standards

- Type hints throughout
- NumPy-style docstrings
- Ruff for linting and formatting
- MyPy for static type checking
- Pre-commit hooks for automation
- Comprehensive test coverage (>90% recommended)

## When to Use This Plugin

Use the Python Development plugin when working on:

- **Scientific computing projects** requiring NumPy, SciPy, Pandas, or similar libraries
- **Research software** that needs to be reproducible and maintainable
- **Data analysis pipelines** with complex dependencies
- **Package development** for distribution on PyPI
- **Numerical simulations** requiring validated code
- **Collaborative projects** following community standards
- **Publications** requiring reproducible computational methods

## Technologies Covered

### Core Scientific Stack
- NumPy - Numerical computing with N-dimensional arrays
- Pandas - Data manipulation and analysis
- Matplotlib, Seaborn - Visualization
- SciPy - Scientific algorithms
- Xarray - Labeled multidimensional data
- scikit-learn - Machine learning

### Development Tools
- pixi - Environment and package management
- pytest - Testing framework
- ruff - Fast linting and formatting
- mypy - Static type checking
- Sphinx - Documentation generation
- pre-commit - Git hooks for quality checks

### Build and Packaging
- pyproject.toml - Modern project configuration
- Hatchling - Build backend
- build - Package building tool
- twine - PyPI publishing

### Performance
- Numba - JIT compilation
- Dask - Parallel computing
- joblib - Lightweight pipelining

## Integration with Other Plugins

- **Scientific Computing Plugin** - For HPC, parallel computing, and numerical methods (coming soon)
- **Data Science Plugin** - For machine learning and statistical analysis (planned)

## Examples and Use Cases

### Example 1: Setting Up a New Research Project

```bash
# Initialize project with pixi
pixi init --format pyproject my-research

# Add scientific dependencies
cd my-research
pixi add python=3.11 numpy pandas matplotlib scipy xarray

# Add development tools
pixi add --feature dev pytest ruff mypy ipython jupyter

# Create proper package structure
mkdir -p src/my_research tests docs

# Start development
pixi run jupyter lab
```

### Example 2: Creating a Distributable Package

Create a package following modern standards:
- Use src/ layout
- Configure pyproject.toml with Hatchling
- Write comprehensive tests with pytest
- Add NumPy-style docstrings
- Build and publish to PyPI

(See python-packaging skill for complete workflow)

### Example 3: Reproducible Data Analysis

Set up a reproducible analysis pipeline:
- Lock dependencies with pixi.lock
- Organize code with separation of concerns (I/O, processing, analysis)
- Write tests for numerical correctness
- Document with Jupyter notebooks
- Version control with Git

## Resources

### Scientific Python Community
- [Scientific Python Development Guide](https://learn.scientific-python.org/development/)
- [Scientific Python Lectures](https://lectures.scientific-python.org/)
- [NumPy Documentation](https://numpy.org/doc/stable/)
- [SciPy Documentation](https://docs.scipy.org/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

### Tools and Frameworks
- [pixi Documentation](https://pixi.sh)
- [pytest Documentation](https://docs.pytest.org/)
- [Hatchling](https://hatch.pypa.io/latest/)
- [Ruff](https://docs.astral.sh/ruff/)
- [Sphinx](https://www.sphinx-doc.org/)

### Package Development
- [Python Packaging Guide](https://packaging.python.org/)
- [Scientific Python Cookie](https://github.com/scientific-python/cookie) - Project template
- [PyPI](https://pypi.org/) - Python Package Index

## Contributing

We welcome contributions to this plugin! You can:

- **Add new skills** - Create focused guides on specific topics
- **Enhance existing skills** - Add patterns, examples, or clarifications
- **Improve the agent** - Suggest enhancements to the Scientific Python Expert
- **Report issues** - Let us know if something is unclear or incorrect

See the main [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

### Potential Additions

Ideas for new skills or improvements:

- Performance profiling patterns
- GPU acceleration with CuPy/JAX
- Async Python for I/O-bound tasks
- Debugging techniques for numerical code
- Data validation patterns
- Continuous integration best practices

## Questions or Feedback?

Please open an issue on [GitHub](https://github.com/uw-ssec/rse-agents/issues) with the label `python-development`.

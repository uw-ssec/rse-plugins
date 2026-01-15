# Scientific Python Development Plugin

Comprehensive agents and skills for modern Scientific Python development following community best practices.

## Overview

This plugin provides expert guidance for scientific Python development, emphasizing reproducibility, modern tooling, and community standards from the [Scientific Python Development Guide](https://learn.scientific-python.org/development/).

**Version:** 0.2.0

**Contents:**
- 2 Agents: Scientific Python Expert, Scientific Docs Architect
- 5 Skills: Code Quality Tools, Pixi Package Manager, Python Packaging, Python Testing, Scientific Documentation

## Installation

This plugin is part of the RSE Plugins collection. To use it with Claude Code:

1. Clone the repository:
   ```bash
   git clone https://github.com/uw-ssec/rse-plugins.git
   ```

2. The plugin will be automatically available in the repository's marketplace at:
   ```
   plugins/scientific-python-development/
   ```

3. Load the Scientific Python Expert agent or individual skills through Claude Code's plugin interface.

## Plugin Structure

```
scientific-python-development/
├── .claude-plugin/
│   └── plugin.json                    # Plugin metadata and configuration
├── agents/
│   ├── scientific-python-expert.md    # Main scientific Python development agent
│   └── scientific-docs-architect.md   # Scientific documentation architect agent
├── skills/
│   ├── code-quality-tools/            # Ruff, mypy, pre-commit skill
│   │   ├── SKILL.md
│   │   ├── assets/
│   │   │   ├── pre-commit-config.yaml
│   │   │   └── pyproject-ruff-mypy.toml
│   │   └── references/
│   │       ├── COMMON_ISSUES.md
│   │       ├── CONFIGURATION_PATTERNS.md
│   │       └── TYPE_HINTS.md
│   ├── pixi-package-manager/          # Pixi environment management skill
│   │   ├── SKILL.md
│   │   ├── assets/
│   │   │   ├── github-actions-pixi.yml
│   │   │   ├── pyproject-multi-env.toml
│   │   │   └── pyproject-pixi-example.toml
│   │   └── references/
│   │       ├── COMMON_ISSUES.md
│   │       └── PATTERNS.md
│   ├── python-packaging/              # Package creation and distribution skill
│   │   ├── SKILL.md
│   │   ├── assets/
│   │   │   ├── .gitignore
│   │   │   ├── github-actions-publish.yml
│   │   │   ├── pyproject-full-featured.toml
│   │   │   ├── pyproject-minimal.toml
│   │   │   ├── README-template.md
│   │   │   └── sphinx-conf.py
│   │   ├── scripts/
│   │   │   └── cli-example.py
│   │   └── references/
│   │       ├── COMMON_ISSUES.md
│   │       ├── DOCSTRINGS.md
│   │       ├── METADATA.md
│   │       └── PATTERNS.md
│   ├── python-testing/                # pytest testing skill
│   │   ├── SKILL.md
│   │   ├── assets/
│   │   │   ├── conftest-example.py
│   │   │   ├── github-actions-tests.yml
│   │   │   └── pyproject-pytest.toml
│   │   └── references/
│   │       ├── COMMON_PITFALLS.md
│   │       ├── SCIENTIFIC_PATTERNS.md
│   │       └── TEST_PATTERNS.md
│   └── scientific-documentation/      # Scientific documentation skill
│       ├── SKILL.md
│       ├── assets/
│       │   ├── sphinx-conf-scientific.py
│       │   ├── readthedocs.yaml
│       │   ├── mkdocs-scientific.yml
│       │   ├── noxfile-docs.py
│       │   └── index-template.md
│       ├── references/
│       │   ├── DIATAXIS_FRAMEWORK.md
│       │   ├── SPHINX_EXTENSIONS.md
│       │   ├── DOCSTRING_EXAMPLES.md
│       │   ├── NOTEBOOK_INTEGRATION.md
│       │   └── COMMON_ISSUES.md
│       └── scripts/
│           └── generate-api-docs.py
├── LICENSE -> ../../LICENSE            # Symlink to main repository license
└── README.md                          # This file
```

## Available Agents

### Scientific Python Expert

**File:** [agents/scientific-python-expert.md](agents/scientific-python-expert.md)

**Agent Version:** 2026-01-07

**Description:** Expert scientific Python developer for research computing, data analysis, and scientific software. Specializes in NumPy, Pandas, Matplotlib, SciPy, and modern reproducible workflows with pixi. Follows Scientific Python community best practices from the [Scientific Python Development Guide](https://learn.scientific-python.org/development/).

**Integrated Skills:**
- python-packaging
- python-testing
- code-quality-tools
- pixi-package-manager

**Capabilities:**
- Scientific Python stack (NumPy, Pandas, SciPy, Matplotlib, Xarray, scikit-learn)
- Modern environment management with pixi (preferred) or venv/uv
- Python packaging with pyproject.toml and src layout
- Outside-in testing with pytest and Hypothesis for property-based testing
- Code quality with ruff (linting/formatting) and mypy (type checking)
- Documentation with Sphinx and NumPy-style docstrings
- Performance optimization with vectorization and Numba
- Data I/O (HDF5, NetCDF, Parquet, Zarr)
- Separation of I/O and scientific logic
- Duck typing and Protocol-based interfaces
- Proper handling of NaN, inf, and empty arrays
- Reproducible random number generation

**When to use:**
- Building scientific computing applications
- Developing research software and data analysis pipelines
- Creating distributable Python packages for science
- Implementing reproducible computational workflows
- Setting up modern Python projects from scratch
- Scientific domain work in astronomy, biology, physics, geosciences, etc.

**Decision-Making Framework:**

The agent follows a structured approach for every task:

1. **Understand Context** - Scientific domain, research question, data characteristics
2. **Assess Requirements** - Computational, reproducibility, and performance needs
3. **Identify Constraints** - Data size, platform, dependency limitations
4. **Choose Tools** - Select appropriate Scientific Python libraries
5. **Design Approach** - Structure code for reusability and collaboration
6. **Plan Validation** - Define testing strategy with known results

**Scientific Python Process Principles:**

1. **Collaborate** - Use conventions and tooling from the broader community for easier collaboration
2. **Don't Be Afraid to Refactor** - Leverage tests and tooling to iterate confidently
3. **Prefer Wide Over Deep** - Build reusable, extensible solutions for unforeseen applications

**Quality Assurance:**

Every response includes a self-review checklist covering:
- **Correctness** - Handles NaN/inf/empty arrays, numerical stability, reproducible randomness
- **Quality** - Type hints, NumPy-style docstrings, I/O separation, functional style
- **Reproducibility** - Environment management, version constraints, fixed seeds
- **Performance** - Vectorization, memory efficiency, profiling suggestions

### Scientific Docs Architect

**File:** [agents/scientific-docs-architect.md](agents/scientific-docs-architect.md)

**Agent Version:** 2026-01-15

**Description:** Expert scientific Python documentation architect specializing in research software documentation following the Diátaxis framework. Creates comprehensive documentation including API references, tutorials, how-to guides, and explanations for scientific codebases. Follows Scientific Python community best practices from the [Scientific Python Development Guide](https://learn.scientific-python.org/development/guides/docs/).

**Integrated Skills:**
- scientific-documentation

**Tools:**
- Read, Write, Edit, Glob, Grep, Bash

**Capabilities:**
- Diátaxis framework mastery (tutorials, how-to guides, reference, explanation)
- Sphinx and MkDocs configuration for scientific Python
- NumPy-style docstring writing and validation
- API reference generation with autodoc/autosummary
- Read the Docs integration
- Jupyter notebook integration (nbsphinx, mkdocs-jupyter)
- Mathematical notation with MathJax/KaTeX
- Intersphinx linking to scientific Python ecosystem
- Citation and reproducibility documentation
- Documentation build automation with Nox
- Version awareness (package, Python, and dependency versions)
- Structured output formats (plans, files, summaries)

**When to use:**
- Creating comprehensive documentation for scientific Python packages
- Setting up documentation infrastructure (Sphinx, MkDocs, Read the Docs)
- Writing NumPy-style docstrings for API documentation
- Organizing documentation following the Diátaxis framework
- Generating API reference pages
- Integrating Jupyter notebooks into documentation
- Creating tutorials and how-to guides for scientific software
- Documenting scientific methods and algorithms

**Documentation Process:**

The agent follows a structured four-phase approach:

1. **Discovery** - Examine codebase, identify domain, catalog existing docs, understand audience
2. **Planning** - Apply Diátaxis framework, establish hierarchy, select tooling, plan structure
3. **Structuring** - Create directory structure, set up tooling, organize navigation
4. **Writing** - Generate comprehensive content with examples, diagrams, and cross-references

**Quality Standards:**

Every documentation deliverable demonstrates:
- **Clarity** - Understandable by target audience
- **Completeness** - All public interfaces documented
- **Correctness** - Examples work, links resolve, facts accurate
- **Consistency** - Uniform style and structure
- **Accessibility** - Multiple entry points and learning paths
- **Reproducibility** - Environment and version information included
- **Scientific Rigor** - Methods properly documented and cited

**Constraints:**

The agent follows these guardrails:
- Does not document private APIs unless explicitly requested
- Always checks for existing documentation framework before assuming one
- Verifies code examples execute correctly before including them
- Never removes existing documentation without user confirmation
- Avoids placeholder content like "TODO" or "Add description here"

## Available Skills

### Code Quality Tools

**File:** [skills/code-quality-tools/SKILL.md](skills/code-quality-tools/SKILL.md)

**Description:** Master automated code quality tools for scientific Python including ruff (fast linting and formatting), mypy (static type checking), and pre-commit hooks for automated quality gates.

**Key topics:**
- Ruff for ultra-fast linting and formatting (replaces flake8, black, isort)
- MyPy for static type checking and catching bugs before runtime
- Pre-commit hooks for automated quality enforcement
- NumPy-specific linting rules
- Type hints for scientific code
- CI/CD integration
- Migration from legacy tools

**When to use:**
- Setting up code quality standards for new projects
- Enforcing consistent style across team contributions
- Catching bugs early through static type checking
- Automating code reviews
- Preparing code for publication or distribution
- Migrating from black/flake8/isort to modern tooling

**Skill contents:**
- SKILL.md: Main skill guide with quick reference, configuration examples, and workflows
- assets/pre-commit-config.yaml: Pre-commit hook configuration template
- assets/pyproject-ruff-mypy.toml: Ruff and MyPy configuration for pyproject.toml
- references/COMMON_ISSUES.md: Troubleshooting guide for common problems
- references/CONFIGURATION_PATTERNS.md: Detailed configuration patterns and examples
- references/TYPE_HINTS.md: Type hints guide for scientific Python code

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

**Skill contents:**
- SKILL.md: Main skill guide with quick reference, essential commands, and patterns
- assets/github-actions-pixi.yml: GitHub Actions workflow template using pixi
- assets/pyproject-multi-env.toml: Multi-environment pyproject.toml configuration example
- assets/pyproject-pixi-example.toml: Complete pyproject.toml example with pixi configuration
- references/COMMON_ISSUES.md: Troubleshooting guide for pixi-related problems
- references/PATTERNS.md: Detailed patterns for pixi workflows and best practices

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

**Skill contents:**
- SKILL.md: Main skill guide with quick decision trees, patterns, and workflows
- assets/.gitignore: Standard .gitignore template for Python packages
- assets/github-actions-publish.yml: GitHub Actions workflow for automated PyPI publishing
- assets/pyproject-full-featured.toml: Full-featured pyproject.toml with all options
- assets/pyproject-minimal.toml: Minimal pyproject.toml template for simple packages
- assets/README-template.md: Package README template following best practices
- assets/sphinx-conf.py: Sphinx documentation configuration template
- scripts/cli-example.py: Example CLI application using argparse
- references/COMMON_ISSUES.md: Troubleshooting guide for packaging problems
- references/DOCSTRINGS.md: NumPy-style docstring guide and examples
- references/METADATA.md: Comprehensive guide to pyproject.toml metadata fields
- references/PATTERNS.md: Detailed packaging patterns and best practices

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

**Skill contents:**
- SKILL.md: Main skill guide with quick reference, decision trees, and testing patterns
- assets/conftest-example.py: Example pytest conftest.py with common fixtures
- assets/github-actions-tests.yml: GitHub Actions workflow template for running tests
- assets/pyproject-pytest.toml: pytest configuration for pyproject.toml
- references/COMMON_PITFALLS.md: Guide to common testing mistakes and how to avoid them
- references/SCIENTIFIC_PATTERNS.md: Testing patterns specific to scientific computing
- references/TEST_PATTERNS.md: General pytest patterns and best practices

### Scientific Documentation

**File:** [skills/scientific-documentation/SKILL.md](skills/scientific-documentation/SKILL.md)

**Description:** Create comprehensive documentation for scientific Python packages following the Diátaxis framework and Scientific Python community guidelines. Master Sphinx/MkDocs tooling, NumPy-style docstrings, and documentation hosting on Read the Docs.

**Key topics:**
- Diátaxis framework (tutorials, how-to guides, reference, explanation)
- Documentation framework selection (Sphinx, MkDocs, Jupyter Book)
- Theme selection and configuration (PyData, Material, Furo)
- Sphinx extensions for scientific Python (autodoc, napoleon, mathjax, intersphinx)
- NumPy-style docstrings (functions, classes, modules)
- Read the Docs integration and configuration
- MkDocs Material configuration for scientific packages
- Jupyter notebook integration (nbsphinx, mkdocs-jupyter)
- Documentation build automation with Nox
- API documentation generation

**When to use:**
- Setting up documentation infrastructure for scientific Python packages
- Writing comprehensive API reference documentation
- Creating tutorials and how-to guides following Diátaxis
- Configuring Sphinx or MkDocs for scientific projects
- Integrating Jupyter notebooks into documentation
- Publishing documentation to Read the Docs
- Generating API documentation from docstrings
- Troubleshooting documentation build issues

**Skill contents:**
- SKILL.md: Main skill guide with decision trees, quick reference, and comprehensive examples
- assets/sphinx-conf-scientific.py: Complete Sphinx configuration for scientific Python
- assets/readthedocs.yaml: Read the Docs configuration template
- assets/mkdocs-scientific.yml: MkDocs Material configuration for scientific packages
- assets/noxfile-docs.py: Nox sessions for documentation building and testing
- assets/index-template.md: Documentation index page template
- references/DIATAXIS_FRAMEWORK.md: Comprehensive guide to the Diátaxis framework
- references/SPHINX_EXTENSIONS.md: Guide to Sphinx extensions for scientific Python
- references/DOCSTRING_EXAMPLES.md: Extensive NumPy-style docstring examples
- references/NOTEBOOK_INTEGRATION.md: Guide to integrating Jupyter notebooks
- references/COMMON_ISSUES.md: Troubleshooting guide for documentation problems
- scripts/generate-api-docs.py: Script for automated API documentation generation

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

## How to Use This Plugin

### Using the Scientific Python Expert Agent

The agent is designed to be used **proactively** for scientific computing, data analysis, or research software development tasks. It automatically loads all four skills and provides comprehensive guidance.

Load the agent through Claude Code's interface and use it for:
- End-to-end project setup and development
- Complex workflows requiring multiple tools
- Architectural decisions and design review
- Learning Scientific Python best practices

### Using Individual Skills

Skills can be loaded independently when you need focused expertise:

- **Load code-quality-tools** when configuring ruff, mypy, or pre-commit
- **Load pixi-package-manager** when setting up environments or dependencies
- **Load python-packaging** when creating or publishing packages
- **Load python-testing** when writing or organizing tests

Skills provide:
- Quick reference cards for common tasks
- Decision trees for choosing approaches
- Configuration templates and examples
- Troubleshooting guides
- Best practices and patterns

### Skill Usage Pattern

```bash
# Example: Loading a skill for a specific task
# In Claude Code, reference the skill:
# "Load the python-packaging skill"

# Or directly invoke skill guidance:
# "Using python-packaging skill, help me set up a new package with CLI"
```

## When to Use This Plugin

Use the Scientific Python Development plugin when working on:

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

This plugin is part of the RSE Plugins ecosystem. Other available plugins:

- **holoviz-visualization** - Development kit for working with HoloViz ecosystem (Panel, hvPlot, HoloViews, Datashader, GeoViews, Lumen)

Future plugins under consideration:
- Scientific Computing Plugin - For HPC, parallel computing, and numerical methods
- Data Science Plugin - For machine learning and statistical analysis

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

- **Add new skills** - Create focused guides on specific topics (e.g., NumPy patterns, data visualization)
- **Enhance existing skills** - Add patterns, examples, troubleshooting tips, or clarifications
- **Improve the agent** - Suggest enhancements to the Scientific Python Expert agent
- **Report issues** - Let us know if something is unclear, incorrect, or outdated
- **Share examples** - Contribute real-world usage examples and case studies

See the main repository [CONTRIBUTING.md](../../CONTRIBUTING.md) for detailed guidelines.

### Skill Structure Guidelines

When contributing a new skill, follow this structure:

```
skills/your-skill-name/
├── SKILL.md                    # Main skill guide (required)
├── assets/                     # Configuration files, templates, examples
│   └── example-config.yml
├── scripts/                    # Runnable example scripts (optional)
│   └── example.py
└── references/                 # Deep-dive documentation (optional)
    ├── PATTERNS.md
    └── COMMON_ISSUES.md
```

### Ideas for New Skills

Potential additions that would enhance this plugin:

- **numpy-advanced-patterns** - Advanced NumPy techniques (broadcasting, indexing, ufuncs)
- **performance-profiling** - Profiling scientific Python code (cProfile, line_profiler, memory_profiler)
- **gpu-acceleration** - GPU computing with CuPy/JAX
- **data-validation** - Input validation patterns for scientific code (Pydantic, pandera)
- **scientific-visualization** - Matplotlib, Seaborn, Plotly best practices
- **parallel-computing** - Dask, joblib, multiprocessing patterns
- **async-python** - Async patterns for I/O-bound scientific workflows
- **debugging-scientific-code** - Debugging numerical issues, NaN tracking, assertions

## Questions or Feedback?

- **Issues**: Open an issue on [GitHub](https://github.com/uw-ssec/rse-plugins/issues) with the label `scientific-python-development`
- **Discussions**: Start a discussion on [GitHub Discussions](https://github.com/uw-ssec/rse-plugins/discussions)
- **Pull Requests**: Submit improvements via [pull requests](https://github.com/uw-ssec/rse-plugins/pulls)

## License

This plugin is part of the RSE Plugins project and is licensed under the BSD-3-Clause License. See [LICENSE](../../LICENSE) for details.

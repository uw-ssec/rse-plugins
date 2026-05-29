---
name: pixi-package-manager
description: "Manage scientific Python dependencies and environments with the pixi package manager: create environments, add conda-forge and PyPI packages, define and run tasks, and generate reproducible multi-platform lockfiles. Use when the user mentions pixi, pixi.toml, pixi.lock, pixi init/add/run, conda-forge, or needs reproducible scientific Python environments combining conda and PyPI packages."
metadata:
  pixi-version: "0.69.0"
  last-verified: "2026-05-29"
  assets:
    - assets/github-actions-pixi.yml
    - assets/pyproject-multi-env.toml
    - assets/pyproject-pixi-example.toml
  references:
    - references/common-issues.md
    - references/patterns.md
---

# Pixi Package Manager for Scientific Python

**pixi** is a package manager that unifies the conda and PyPI ecosystems for reproducible scientific Python development. Use it to manage scientific dependencies, create isolated environments, and build reproducible workflows via `pyproject.toml` integration.

**Official Documentation**: https://pixi.sh
**GitHub**: https://github.com/prefix-dev/pixi

## Quick Reference Card

### Installation & Setup
```bash
# Install pixi (macOS/Linux)
curl -fsSL https://pixi.sh/install.sh | bash

# Install pixi (Windows)
iwr -useb https://pixi.sh/install.ps1 | iex

# Initialize new project with pyproject.toml
pixi init --format pyproject

# Import from an existing environment.yml
pixi init --format pyproject --import environment.yml
```

### Essential Commands
```bash
# Add dependencies
pixi add numpy scipy pandas              # conda packages
pixi add --pypi pytest-cov               # PyPI-only packages
pixi add --feature dev pytest ruff       # dev environment

# Install all dependencies
pixi install

# Run commands in environment
pixi run python script.py
pixi run pytest

# Shell with environment activated
pixi shell

# Add tasks
pixi task add test "pytest tests/"
pixi task add docs "sphinx-build docs/ docs/_build"

# Run tasks
pixi run test
pixi run docs

# Update dependencies
pixi update numpy                         # update specific
pixi update                              # update all

# List packages
pixi list
pixi tree numpy                          # show dependency tree

# Global tools (replaces pipx / condax for CLI utilities)
pixi global install ruff                  # install a CLI tool globally
pixi global list                          # list globally installed tools

# Run a tool in a temporary throwaway environment (no project needed)
pixi exec ruff check .                    # run ruff without installing it
pixi exec --spec python=3.12 python -V    # one-off env with a pinned spec

# Print activation for use in scripts / CI without a subshell
pixi shell-hook                           # emit activation commands
```

### Quick Decision Tree: Pixi vs UV vs Both

```
Need compiled scientific libraries (NumPy, SciPy, GDAL)?
├─ YES → Use pixi (conda-forge has pre-built binaries)
└─ NO → Consider uv for pure Python projects

Need multi-language support (Python + R, Julia, C++)?
├─ YES → Use pixi (supports conda ecosystem)
└─ NO → uv sufficient for Python-only

Need multiple environments (dev, test, prod, GPU, CPU)?
├─ YES → Use pixi features for environment management
└─ NO → Single environment projects work with either

Need reproducible environments across platforms?
├─ CRITICAL → Use pixi (lockfiles include all platforms)
└─ LESS CRITICAL → uv also provides lockfiles

Want to use both conda-forge AND PyPI packages?
├─ YES → Use pixi (integrates both in one graph)
└─ ONLY PYPI → uv is simpler and faster

Legacy conda environment files (environment.yml)?
├─ YES → pixi can import and modernize
└─ NO → Start fresh with pixi or uv
```

## When to Use This Skill

- **Compiled scientific dependencies** (NumPy, SciPy, GDAL, netCDF4) that need conda-forge pre-built binaries
- **Reproducible multi-platform environments** that work identically across Linux, macOS, and Windows
- **Mixed conda-forge + PyPI** dependency graphs in a single project
- **Multiple environment configurations** (dev, test, GPU/CPU) defined via features

## Core Concepts

### 1. Unified Package Management (conda + PyPI)

Pixi resolves dependencies from **both conda-forge and PyPI** in a single unified graph, ensuring compatibility:

```toml
[project]
name = "my-science-project"
dependencies = [
    "numpy>=1.24",      # from conda-forge (optimized builds)
    "pandas>=2.0",      # from conda-forge
]

[tool.pixi.pypi-dependencies]
my-custom-pkg = ">=1.0"        # PyPI-only package
```

A single lockfile guarantees conda-forge (MKL/OpenBLAS-optimized) and PyPI-only packages stay compatible.

### 2. Multi-Platform Lockfiles

Pixi generates `pixi.lock` with dependency specifications for **all platforms** (Linux, macOS, Windows, different architectures):

```toml
# pixi.lock includes:
# - linux-64
# - osx-64, osx-arm64
# - win-64
```

Commit the lockfile to git so collaborators and CI get identical versions across any OS.

### 3. Feature-Based Environments

Create multiple environments using **features** without duplicating dependencies:

```toml
[tool.pixi.feature.test.dependencies]
pytest = ">=7.0"
pytest-cov = ">=4.0"

[tool.pixi.feature.gpu.dependencies]
pytorch-cuda = "11.8.*"

[tool.pixi.environments]
test = ["test"]
gpu = ["gpu"]
gpu-test = ["gpu", "test"]  # combines features
```

### 4. Task Automation

Define reusable commands as tasks:

```toml
[tool.pixi.tasks]
test = "pytest tests/ -v"
format = "ruff format src/ tests/"
lint = "ruff check src/ tests/"
docs = "sphinx-build docs/ docs/_build"
analyse = { cmd = "python scripts/analyze.py", depends-on = ["test"] }
```

### 5. Dependency Resolution

Pixi uses **rattler** (a Rust-based conda resolver) with parallel downloads and caching for fast resolution.

### 6. pyproject.toml Integration

Pixi reads standard Python project metadata from `pyproject.toml`, enabling:
- Single source of truth for project configuration
- Compatibility with pip, uv, and other tools
- Standard Python packaging workflows

> **Terminology note:** pixi renamed the project-level table to
> `[tool.pixi.workspace]` (standalone manifests use `[workspace]`). The older
> `[tool.pixi.project]` / `[project]`-style pixi table still works as a
> deprecated alias, so existing manifests keep functioning — but new projects
> should use `workspace`.

### 7. Manifest Format: `pixi.toml` vs `pyproject.toml`

Pixi supports two manifest formats. This skill leads with `pyproject.toml`
because scientific Python work usually involves a distributable package, and
`pyproject.toml` is the standard single source of truth.

| Use `pyproject.toml` (this skill's default) | Use standalone `pixi.toml` |
|---------------------------------------------|----------------------------|
| You are building an installable Python package | The project is a workflow, analysis, or app, not a package |
| You want pip/build/uv compatibility | You want the leanest possible manifest |
| `pixi init --format pyproject` | `pixi init` (the default) |

Everything in this skill maps to both formats. The only difference is table
prefixes: `pyproject.toml` uses `[tool.pixi.*]` (e.g. `[tool.pixi.workspace]`,
`[tool.pixi.dependencies]`); a standalone `pixi.toml` drops the prefix
(`[workspace]`, `[dependencies]`).

### 8. Global Tools and One-Off Execution

Not every tool belongs in a project environment:

- **`pixi global install <tool>`** installs a CLI tool into an isolated global
  environment on your `PATH` — the pixi-native replacement for `pipx`/`condax`
  (e.g. `ruff`, `pre-commit`, `jupyterlab`).
- **`pixi exec <cmd>`** runs a command in a temporary environment that is
  discarded afterward — ideal for trying a tool without adding a dependency, or
  for CI one-offs (`pixi exec --spec python=3.12 python -V`).
- **`pixi shell-hook`** prints the activation script for an environment without
  spawning a subshell, which is what you want in CI steps and wrapper scripts.

## Quick Start

### Minimal Example: Data Analysis Project

```bash
# Create new project
mkdir climate-analysis && cd climate-analysis
pixi init --format pyproject

# Add scientific stack
pixi add python=3.11 numpy pandas matplotlib xarray

# Add development tools
pixi add --feature dev pytest ipython ruff

# Create analysis script
cat > analyze.py << 'EOF'
import pandas as pd
import matplotlib.pyplot as plt

# Your analysis code
data = pd.read_csv("data.csv")
data.plot()
plt.savefig("output.png")
EOF

# Run in pixi environment
pixi run python analyze.py

# Verify the environment and lockfile
pixi list                 # confirm packages installed
ls pixi.lock              # confirm lockfile was generated

# Or activate shell
pixi shell
python analyze.py
```

## Patterns

See [references/patterns.md](references/patterns.md) for detailed patterns including:
- Converting existing projects to Pixi
- Multi-environment scientific workflows
- Scientific library development
- Conda + PyPI dependency strategy
- Reproducible research environments
- Task dependencies and workflows

## File Templates

Ready-to-use templates are available in the `assets/` directory:

- **[assets/pyproject-pixi-example.toml](assets/pyproject-pixi-example.toml)** - Basic pixi project configuration
- **[assets/pyproject-multi-env.toml](assets/pyproject-multi-env.toml)** - Multi-environment configuration example
- **[assets/github-actions-pixi.yml](assets/github-actions-pixi.yml)** - GitHub Actions workflow for pixi

## Common Issues and Solutions

See [references/common-issues.md](references/common-issues.md) for solutions to:
- Package not found in conda-forge
- Conflicting dependencies
- Slow environment creation
- Platform-specific failures
- PyPI package installation fails
- Lockfile merge conflicts
- Editable install of local package

## Best Practices Checklist

### Project Setup
- [ ] Use `pixi init --format pyproject` for new projects
- [ ] Set explicit Python version constraint (`python>=3.11,<3.13`)
- [ ] Organize dependencies by source (conda vs PyPI)
- [ ] Create separate features for dev, test, docs environments
- [ ] Define useful tasks for common workflows
- [ ] Set up `.gitignore` to exclude `.pixi/` directory

### Dependency Management
- [ ] Prefer conda-forge for compiled scientific packages (NumPy, SciPy, GDAL)
- [ ] Use PyPI only for pure Python or conda-unavailable packages
- [ ] Pin exact versions for reproducible research
- [ ] Use version ranges for libraries (allow updates)
- [ ] Specify solve groups for independent environment solving
- [ ] Use `pixi update` regularly to get security patches

### Reproducibility
- [ ] Commit `pixi.lock` to version control
- [ ] Include all platforms in lockfile for cross-platform teams
- [ ] Document environment recreation steps in README
- [ ] Use exact version pins for published research
- [ ] Test environment from scratch periodically
- [ ] Archive environments for long-term preservation

### Performance
- [ ] Use pixi's parallel downloads (automatic)
- [ ] Leverage caching in CI/CD (`prefix-dev/setup-pixi` action)
- [ ] Keep environments minimal (only necessary dependencies)
- [ ] Use solve groups to isolate independent environments
- [ ] Clean old packages with `pixi clean cache`
- [ ] Pin GitHub Actions to commit SHAs (not mutable tags) in CI — see `assets/github-actions-pixi.yml`; a tag like `@v5` can be repointed to malicious code, a SHA cannot

### Development Workflow
- [ ] Define tasks for common operations (test, lint, format)
- [ ] Use task dependencies for complex workflows
- [ ] Create environment-specific tasks when needed
- [ ] Use `pixi shell` for interactive development
- [ ] Use `pixi run` for automated scripts and CI
- [ ] Test in clean environment before releasing

## Resources

### Official Documentation
- **Pixi Website**: https://pixi.sh
- **Documentation**: https://pixi.sh/latest/
- **GitHub Repository**: https://github.com/prefix-dev/pixi
- **Configuration Reference**: https://pixi.sh/latest/reference/project_configuration/
- **Building packages (`pixi build`)**: https://pixi.sh/latest/build/getting_started/
- **Migration guides (conda, poetry, uv)**: https://pixi.sh/latest/switching_from/conda/

### Community & Support
- **Discord**: https://discord.gg/kKV8ZxyzY4
- **GitHub Discussions**: https://github.com/prefix-dev/pixi/discussions
- **Issue Tracker**: https://github.com/prefix-dev/pixi/issues

### Related Technologies
- **Conda-forge**: https://conda-forge.org/
- **Rattler**: https://github.com/mamba-org/rattler (underlying solver)
- **PyPI**: https://pypi.org/
- **UV Package Manager**: https://github.com/astral-sh/uv

### Complementary Skills
- **scientific-python-packaging**: Modern Python packaging patterns
- **scientific-python-testing**: Testing strategies with pytest
- **uv-package-manager**: Fast pure-Python package management

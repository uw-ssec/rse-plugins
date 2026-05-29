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
    - references/best-practices.md
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

### Pixi vs uv

Choose **pixi** for compiled/conda-forge packages (NumPy, SciPy, GDAL), multi-language stacks, mixed conda + PyPI graphs, or multi-platform lockfiles. Choose **uv** for pure-Python, PyPI-only projects where it is simpler and faster.

## Core Concepts

### 1. Unified Package Management (conda + PyPI)

Conda-forge and PyPI packages resolve in one graph:

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

`pixi.lock` captures resolved versions for every platform:

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

### 5. pyproject.toml Integration

Pixi reads standard Python project metadata from `pyproject.toml`, enabling:
- Single source of truth for project configuration
- Compatibility with pip, uv, and other tools
- Standard Python packaging workflows

> **Terminology note:** pixi renamed the project-level table to
> `[tool.pixi.workspace]` (standalone manifests use `[workspace]`). The older
> `[tool.pixi.project]` / `[project]`-style pixi table still works as a
> deprecated alias, so existing manifests keep functioning — but new projects
> should use `workspace`.

### 6. Manifest Format: `pixi.toml` vs `pyproject.toml`

This skill leads with `pyproject.toml` (the standard single source of truth for
distributable packages); standalone `pixi.toml` is the leaner alternative.

| Use `pyproject.toml` (this skill's default) | Use standalone `pixi.toml` |
|---------------------------------------------|----------------------------|
| You are building an installable Python package | The project is a workflow, analysis, or app, not a package |
| You want pip/build/uv compatibility | You want the leanest possible manifest |
| `pixi init --format pyproject` | `pixi init` (the default) |

Everything in this skill maps to both formats. The only difference is table
prefixes: `pyproject.toml` uses `[tool.pixi.*]` (e.g. `[tool.pixi.workspace]`,
`[tool.pixi.dependencies]`); a standalone `pixi.toml` drops the prefix
(`[workspace]`, `[dependencies]`).

### 7. Global Tools and One-Off Execution

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

## Troubleshooting

Quick fixes for the most common failures (full guide in
[references/common-issues.md](references/common-issues.md)):

- **`pixi add` fails with "package not found"** → it may be PyPI-only; retry with
  `pixi add --pypi <pkg>`, or check the conda name with `pixi search <pkg>`.
- **Solver reports a conflict** → relax pins (`numpy>=1.24,<2` instead of `==`),
  or isolate the environment with its own `solve-group`; inspect with
  `pixi tree <pkg>`.
- **Lockfile didn't generate / is stale** → run `pixi install` to regenerate
  `pixi.lock`; after a git merge conflict, take one side then re-run `pixi install`.
- **Works on one OS, fails on another** → guard OS-specific deps under
  `[tool.pixi.target.<platform>.dependencies]` and confirm the platform is in
  `[tool.pixi.workspace].platforms`.

See the reference for editable local installs, slow environment creation, and
PyPI build failures.

## Best Practices

See [references/best-practices.md](references/best-practices.md) for checklists
covering project setup, dependency management, reproducibility, performance, and
development workflow — including pinning GitHub Actions to commit SHAs (not
mutable tags) in CI; a tag like `@v5` can be repointed to malicious code, a SHA
cannot (see [assets/github-actions-pixi.yml](assets/github-actions-pixi.yml)).

## Resources

- **Documentation**: https://pixi.sh/latest/ · **GitHub**: https://github.com/prefix-dev/pixi
- **Configuration reference**: https://pixi.sh/latest/reference/project_configuration/
- **Building packages (`pixi build`)**: https://pixi.sh/latest/build/getting_started/
- **Migration guides (conda, poetry, uv)**: https://pixi.sh/latest/switching_from/conda/

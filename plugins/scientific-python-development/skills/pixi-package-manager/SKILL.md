---
name: pixi-package-manager
description: "Use when the user works with pixi (pixi.toml, pixi.lock, pixi add/run/task/global/exec) or wants a reproducible scientific Python environment that mixes conda-forge and PyPI packages: creating environments, adding dependencies, defining tasks, multi-platform lockfiles, or migrating from conda environment.yml / requirements.txt. Not for pure uv/pip projects or for building and publishing packages to PyPI (use python-packaging)."
metadata:
  pixi-version: "0.83.0"
  last-verified: "2026-10-27"
  assets:
    - assets/github-actions-pixi.yml
    - assets/pyproject-multi-env.toml
    - assets/pyproject-pixi-example.toml
  references:
    - references/best-practices.md
    - references/common-issues.md
    - references/manifest-and-tooling.md
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
irm -useb https://pixi.sh/install.ps1 | iex

# Initialize new project with pyproject.toml
pixi init --format pyproject

# Import from an existing environment.yml (writes pixi.toml; --import and --format can't be combined)
pixi init --import environment.yml
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

## Core Concepts

Pixi uses the `[tool.pixi.workspace]` table (formerly `project`; still a
deprecated alias). For `pixi.toml` vs `pyproject.toml`, pyproject integration,
and pixi-vs-uv guidance, see
[references/manifest-and-tooling.md](references/manifest-and-tooling.md).

### 1. Unified Package Management (conda + PyPI)

Conda-forge and PyPI packages resolve in one graph. In a `pyproject.toml`
manifest, `[project].dependencies` are **PyPI** requirements; conda-forge
packages go in `[tool.pixi.dependencies]`. If a package appears in both, pixi
installs the conda version.

```toml
[project]
name = "my-science-project"
requires-python = ">=3.11"
dependencies = [
    "my-custom-pkg>=1.0",   # PyPI (also what `pip install .` sees)
]

[tool.pixi.dependencies]
numpy = ">=1.24"            # conda-forge (optimized builds)
pandas = ">=2.0"            # conda-forge
```

`pixi add numpy` writes to `[tool.pixi.dependencies]`; `pixi add --pypi pkg`
writes to `[project].dependencies`.

### 2. Multi-Platform Lockfiles

Commit `pixi.lock` so collaborators and CI resolve identical versions. The
lockfile only covers the platforms listed in the workspace, which default to
the current machine's platform, so list every platform you support:

```toml
[tool.pixi.workspace]
channels = ["conda-forge"]
platforms = ["linux-64", "osx-arm64", "osx-64", "win-64"]
```

Regenerate the lockfile without installing with `pixi lock`.

### 3. Feature-Based Environments

Compose environments from features without duplicating dependencies:

```toml
[tool.pixi.feature.test.dependencies]
pytest = ">=7.0"
pytest-cov = ">=4.0"

[tool.pixi.feature.gpu.system-requirements]
cuda = "12"                 # lets the solver pick CUDA builds

[tool.pixi.feature.gpu.dependencies]
pytorch-gpu = "*"           # conda-forge CUDA build of pytorch

[tool.pixi.environments]
test = ["test"]
gpu = ["gpu"]
gpu-test = ["gpu", "test"]  # combines features
```

`pixi add --feature dev ...` only records dependencies on the feature. Nothing
can use them until an environment lists the feature, for example
`dev = ["dev"]` under `[tool.pixi.environments]`; then run `pixi run -e dev ...`.

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

### 5. Global Tools and One-Off Execution

Not every tool belongs in a project environment — install persistent CLI tools,
run throwaway one-offs, or emit a subshell-free activation script for CI using
the `global` / `exec` / `shell-hook` commands in the Quick Reference Card above.

## Quick Start

### Minimal Example: Data Analysis Project

```bash
# Create new project
mkdir climate-analysis && cd climate-analysis
pixi init --format pyproject

# Add scientific stack
pixi add python=3.11 numpy pandas matplotlib xarray

# Add development tools and expose them as a `dev` environment
pixi add --feature dev pytest ipython ruff
pixi workspace environment add dev --feature dev

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

## Deeper References

- **[references/manifest-and-tooling.md](references/manifest-and-tooling.md)** — `pixi.toml` vs `pyproject.toml`, the `workspace` terminology, pyproject integration, and pixi-vs-uv selection.
- **[references/patterns.md](references/patterns.md)** — migrating existing projects, multi-environment workflows, library development, conda + PyPI strategy, reproducible research, task pipelines.
- **`assets/`** — ready-to-use templates: `pyproject-pixi-example.toml`, `pyproject-multi-env.toml`, and a SHA-pinned `github-actions-pixi.yml` CI workflow.

## Troubleshooting

Quick fixes for the most common failures (full guide in
[references/common-issues.md](references/common-issues.md)):

- **`pixi add` fails with "package not found"** → it may be PyPI-only; retry with
  `pixi add --pypi <pkg>` (or check the conda name with `pixi search <pkg>`), then
  run `pixi list` to confirm it installed.
- **Solver reports a conflict** → inspect with `pixi tree <pkg>`, relax pins
  (`numpy>=1.24,<2` instead of `==`) or isolate the environment with its own
  `solve-group`, then re-run `pixi install` and confirm it resolves cleanly.
- **Lockfile didn't generate / is stale** → run `pixi lock` (or `pixi install`)
  to regenerate `pixi.lock`, then verify with `ls pixi.lock`; after a git merge
  conflict, take one side and re-run `pixi lock`.
- **Works on one OS, fails on another** → guard OS-specific deps under
  `[tool.pixi.target.<platform>.dependencies]`, confirm the platform is listed in
  `[tool.pixi.workspace].platforms`, then re-run `pixi install` on that platform.

See the reference for editable local installs, slow environment creation, and
PyPI build failures.

See [references/best-practices.md](references/best-practices.md) for setup, dependency management, reproducibility, and CI checklists — including the CI SHA-pinning requirement shown in `assets/github-actions-pixi.yml`.

---
name: pixi-package-manager
description: "Use when the user mentions pixi, pixi.toml, pixi.lock, pixi add/run/task, conda-forge environments, or needs reproducible scientific Python environments combining conda and PyPI packages. Manage scientific Python dependencies with pixi: create environments, add conda-forge and PyPI packages, define and run tasks, generate multi-platform lockfiles, and migrate from conda/requirements.txt. Trigger phrases: 'pixi', 'pixi.toml', 'pixi.lock', 'pixi add', 'pixi run', 'scientific computing environment', 'conda-forge', 'dependency lockfile'."
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

## Core Concepts

Pixi uses the `[tool.pixi.workspace]` table (formerly `project`; still a
deprecated alias). For `pixi.toml` vs `pyproject.toml`, pyproject integration,
and pixi-vs-uv guidance, see
[references/manifest-and-tooling.md](references/manifest-and-tooling.md).

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

### 2. Multi-Platform Lockfiles

Commit `pixi.lock` (covers linux-64, osx-64/arm64, win-64) so collaborators and CI resolve identical versions.

### 3. Feature-Based Environments

Compose environments from features without duplicating dependencies:

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

### 5. Global Tools and One-Off Execution

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
- **Lockfile didn't generate / is stale** → run `pixi install` to regenerate
  `pixi.lock`, then verify with `ls pixi.lock`; after a git merge conflict, take
  one side and re-run `pixi install`.
- **Works on one OS, fails on another** → guard OS-specific deps under
  `[tool.pixi.target.<platform>.dependencies]`, confirm the platform is listed in
  `[tool.pixi.workspace].platforms`, then re-run `pixi install` on that platform.

See the reference for editable local installs, slow environment creation, and
PyPI build failures.

See [references/best-practices.md](references/best-practices.md) for setup, dependency management, reproducibility, and CI checklists — including the CI SHA-pinning requirement shown in `assets/github-actions-pixi.yml`.

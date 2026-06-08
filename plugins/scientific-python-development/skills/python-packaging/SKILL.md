---
name: python-packaging
description: Create and publish distributable scientific Python packages following Scientific Python community best practices. Covers pyproject.toml, src layout, Hatchling, metadata, CLI entry points, and PyPI publishing. Use when the user wants to create a new Python package, set up pyproject.toml, configure Hatchling, publish to PyPI, or follow Scientific Python packaging standards.
metadata:
  assets:
    - assets/pyproject-minimal.toml
    - assets/pyproject-full-featured.toml
    - assets/readme-template.md
    - assets/github-actions-publish.yml
    - assets/sphinx-conf.py
    - assets/.gitignore
  references:
    - references/common-issues.md
    - references/docstrings.md
    - references/metadata.md
    - references/patterns.md
  scripts:
    - scripts/cli-example.py
---

# Scientific Python Packaging

## Package Structure

```
my-sci-package/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── my_sci_package/
│       ├── __init__.py
│       └── analysis.py
└── tests/
    └── test_analysis.py
```

Use `src/` layout — prevents accidental import of uninstalled code, required for Hatchling auto-discovery.

## Minimal pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-sci-package"
version = "0.1.0"
description = "A scientific Python package"
readme = "README.md"
license = "BSD-3-Clause"
requires-python = ">=3.9"
authors = [
    {name = "Your Name", email = "you@example.com"},
]
dependencies = [
    "numpy>=1.20",
    "scipy>=1.7",
]

[project.urls]
Homepage = "https://github.com/username/my-sci-package"

[dependency-groups]
dev = ["pytest>=7.0", "ruff>=0.1", "mypy>=1.0"]
```

Full template with classifiers, optional deps, and CI config: [assets/pyproject-minimal.toml](assets/pyproject-minimal.toml) and [assets/pyproject-full-featured.toml](assets/pyproject-full-featured.toml).

## CLI Entry Point

```toml
[project.scripts]
sci-analyze = "my_sci_package.cli:main"
```

See [scripts/cli-example.py](scripts/cli-example.py) for a Click-based CLI implementation.

## Publishing Workflow

```bash
# 1. Build
python -m build

# 2. Check metadata and distribution
twine check dist/*
# If check fails: fix metadata in [project] section of pyproject.toml and rebuild

# 3. Test on TestPyPI
twine upload --repository testpypi dist/*
pip install --index-url https://test.pypi.org/simple/ my-sci-package
# If install fails: check package name availability, verify dist/ contents with tar -tvf dist/*.tar.gz

# 4. Publish to PyPI
twine upload dist/*
```

For automated publishing on GitHub release: [assets/github-actions-publish.yml](assets/github-actions-publish.yml) (uses OIDC Trusted Publishers — no stored tokens needed).

## Key Rules

- Use `src/` layout — no `setup.py`, `setup.cfg`, or `MANIFEST.in`
- Use Hatchling as build backend (Scientific Python recommendation)
- Set `requires-python` with minimum only — no upper cap
- Use `>=` for dependency lower bounds — avoid upper caps unless absolutely necessary
- Test on TestPyPI before production publish
- Verify SDist contents: `tar -tvf dist/*.tar.gz`

## Pre-Publish Checklist

- [ ] `python -m build` succeeds
- [ ] `twine check dist/*` passes
- [ ] Installed from wheel in clean virtualenv and imports correctly
- [ ] `requires-python` and dependency versions are correct
- [ ] `LICENSE` file present; `license` field uses SPDX identifier
- [ ] `project.urls` includes repository link

## References

- Dependency version constraints, classifiers, optional extras: [references/metadata.md](references/metadata.md)
- Package structure patterns, versioning strategies: [references/patterns.md](references/patterns.md)
- NumPy-style docstrings: [references/docstrings.md](references/docstrings.md)
- Import errors, missing files, dependency conflicts: [references/common-issues.md](references/common-issues.md)
- Scientific Python guidelines: https://learn.scientific-python.org/development/guides/packaging-simple/

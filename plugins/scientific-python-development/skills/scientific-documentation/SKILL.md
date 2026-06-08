---
name: scientific-documentation
description: Use when the user asks about setting up docs for a Python package, configuring Sphinx or MkDocs, writing NumPy-style docstrings, or deploying to Read the Docs. Set up and maintain documentation for scientific Python packages. Covers Sphinx, MkDocs, NumPy-style docstrings, Diataxis framework, accessibility standards, and documentation hosting with Read the Docs.
metadata:
  assets:
    - assets/sphinx-conf-scientific.py
    - assets/mkdocs-scientific.yml
    - assets/noxfile-docs.py
    - assets/readthedocs.yaml
    - assets/index-template.md
  references:
    - references/accessible-documentation.md
    - references/common-issues.md
    - references/diataxis-framework.md
    - references/docstring-examples.md
    - references/notebook-integration.md
    - references/sphinx-extensions.md
  scripts:
    - scripts/generate-api-docs.py
---

# Scientific Python Documentation

## Setup Workflow

End-to-end sequence for a new project. Run each step and verify before proceeding.

```
1. Choose framework      Sphinx (math-heavy / API-first / PDF needed)
                         MkDocs + Material (Markdown-native / simpler setup)
                         Jupyter Book (notebook-centric tutorials)

2. Initialize docs/      sphinx-quickstart docs/   OR   mkdocs new .

3. Configure             Copy asset template, fill in package name and extensions
                         assets/sphinx-conf-scientific.py  (Sphinx)
                         assets/mkdocs-scientific.yml      (MkDocs)

4. Build locally         nox -s docs                (warns-as-errors on)
   └─ Checkpoint: zero warnings, all pages render

5. Check links           nox -s docs_linkcheck
   └─ Checkpoint: no broken internal or external links

6. Deploy                .readthedocs.yaml → import repo on readthedocs.org
                         assets/readthedocs.yaml for the config file
   └─ Checkpoint: RTD build passes; versioned URL resolves
```

---

## Resources in This Skill

| File | Contents |
|------|----------|
| `assets/sphinx-conf-scientific.py` | Complete annotated `conf.py` for scientific Python (all extensions pre-configured) |
| `assets/mkdocs-scientific.yml` | Complete `mkdocs.yml` with Material theme, math, mkdocstrings, mkdocs-jupyter |
| `assets/noxfile-docs.py` | Nox sessions: `docs`, `docs_live`, `docs_linkcheck`, `docs_spelling`, `docs_doctest` |
| `assets/readthedocs.yaml` | `.readthedocs.yaml` v2 with `pip install .[docs]`, `fail_on_warning: true` |
| `assets/index-template.md` | Landing page template (badges, one-liner, install snippet, Diataxis nav) |
| `references/diataxis-framework.md` | Full Diataxis guide: templates and examples for tutorials, how-to, reference, explanation |
| `references/sphinx-extensions.md` | Extension-by-extension config: autodoc, autosummary, napoleon, intersphinx, myst_parser, mathjax |
| `references/docstring-examples.md` | NumPy-style docstrings for functions, classes, generators, modules |
| `references/notebook-integration.md` | nbsphinx and mkdocs-jupyter: execution options, cell tags, CI considerations |
| `references/accessible-documentation.md` | Accessibility: alt text, color contrast, heading hierarchy, video captions |
| `references/common-issues.md` | Build failures, autodoc import errors, intersphinx 404s, RTD environment issues |
| `scripts/generate-api-docs.py` | Script to generate autosummary stubs from package modules |

---

## Framework Quick-Start Snippets

### Sphinx — minimal `conf.py` additions

```python
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",      # NumPy/Google docstrings
    "sphinx.ext.mathjax",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "numpydoc",
    "myst_parser",
]
html_theme = "pydata_sphinx_theme"
napoleon_numpy_docstring = True
autosummary_generate = True
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
}
```

See `assets/sphinx-conf-scientific.py` for the full annotated file including theme options, myst extensions, nbsphinx, and version switcher config.

### MkDocs — minimal `mkdocs.yml` additions

```yaml
theme:
  name: material
plugins:
  - mkdocstrings:
      handlers:
        python:
          options:
            docstring_style: numpy
  - mkdocs-jupyter:
      execute: false
markdown_extensions:
  - pymdownx.arithmatex:
      generic: true
```

See `assets/mkdocs-scientific.yml` for the full file including navigation structure, MathJax setup, dark/light mode, and search configuration.

### Build commands

```bash
# Sphinx (via nox — see assets/noxfile-docs.py)
nox -s docs            # build with warnings-as-errors
nox -s docs_live       # live reload in browser
nox -s docs_linkcheck  # check all links

# Sphinx (direct)
sphinx-build -W -b html docs docs/_build/html
sphinx-autobuild docs docs/_build/html

# MkDocs
mkdocs build --strict
mkdocs serve
```

---

## NumPy-Style Docstrings

Standard for scientific Python packages. Minimal complete example:

```python
def compute_statistic(data, method="mean", axis=0):
    """
    Compute a statistical measure along the specified axis.

    Parameters
    ----------
    data : array_like
        Input data. Any shape.
    method : {'mean', 'median', 'std'}, optional
        Statistical method. Default is ``'mean'``.
    axis : int or None, optional
        Axis along which to compute. Default is 0.

    Returns
    -------
    ndarray
        Computed statistic with the same shape as `data` minus `axis`.

    Raises
    ------
    ValueError
        If `method` is not one of the supported options.

    Examples
    --------
    >>> import numpy as np
    >>> compute_statistic(np.array([1, 2, 3, 4, 5]))
    3.0
    """
```

Key conventions:
- Section headers underlined with dashes (`----------`)
- Types on the same line as the parameter name, separated by ` : `
- Literal values in double backticks: `` ``'mean'`` ``
- Inline references to other parameters: single backtick `` `data` ``

See `references/docstring-examples.md` for classes, generators, `Attributes`, `See Also`, and `Notes` with math.

---

## Dependencies (`pyproject.toml`)

```toml
[project.optional-dependencies]
docs = [
    "sphinx>=7.0",
    "pydata-sphinx-theme>=0.15",
    "numpydoc>=1.6",
    "myst-parser>=2.0",
    "sphinx-autodoc-typehints>=2.0",
    "nbsphinx>=0.9",          # or mkdocs-jupyter for MkDocs
]
```

---

## Non-Obvious Gotchas

- **`autodoc` can't import your package at build time**: install the package (`pip install -e .`) in the RTD build environment with `pip install .[docs]`, not just the docs extras.
- **`autosummary_generate = True`** creates stub `.rst` files in `docs/generated/` — add that directory to `.gitignore` and tell Sphinx to write there with `:toctree: generated/`.
- **`napoleon` vs `numpydoc`**: don't enable both simultaneously; use `numpydoc` alone for the richest NumPy-style output (cross-references, parameter tables).
- **`myst_parser` dollar-math**: requires `dollarmath` in `myst_enable_extensions` AND `sphinx.ext.mathjax` in `extensions` to actually render in HTML.
- **RTD `fail_on_warning: true`**: set this from day one; it prevents silent docstring formatting errors from accumulating.
- **Intersphinx 404s on CI**: cache the inventory files or use `intersphinx_timeout = 30` to avoid flaky builds on slow networks.

See `references/common-issues.md` for build failures, autodoc import errors, and RTD environment problems.

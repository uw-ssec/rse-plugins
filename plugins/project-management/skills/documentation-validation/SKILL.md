---
name: documentation-validation
description: Documentation quality assurance tools and strategies for research software projects. Covers prose linting (Vale), link checking (HTMLProofer), Markdown validation (markdownlint), code example testing, container-based instruction validation, and CI integration.
metadata:
  references:
    - references/VALE_CONFIGURATION.md
    - references/DOCUMENTATION_STANDARDS.md
    - references/VALIDATION_TOOLS.md
  assets:
    - assets/vale-config.ini
    - assets/validation-checklist.md
---

# Documentation Validation

A comprehensive guide to treating documentation as a first-class deliverable that can be automatically tested, linted, and validated. This skill covers prose linting, link checking, code example testing, container-based instruction validation, and CI integration for documentation quality assurance. These practices are essential for research software projects where incorrect setup instructions or broken links can cost researchers hours of wasted effort.

## Resources in This Skill

This skill includes supporting materials for documentation validation tasks:

**References** (detailed guides — consult the table of contents in each file and read specific sections as needed):
- `references/VALE_CONFIGURATION.md` - Complete Vale setup: .vale.ini options, style packages (proselint, write-good, Google, alex), custom rules (substitution, existence, consistency), vocabulary files, editor/CI integration, and configuration recipes
- `references/DOCUMENTATION_STANDARDS.md` - Documentation quality frameworks: Diataxis (tutorials, how-to, reference, explanation), completeness criteria at 4 maturity levels, README standards, API doc coverage, readability metrics, documentation debt, and accessibility
- `references/VALIDATION_TOOLS.md` - All validation tools: markdownlint rules and config, HTMLProofer for link checking, doc8 for RST, language-specific doc testing (Python/Rust/R/Go/Julia), notebook validation (nbval), CI pipeline assembly, and pre-commit integration

**Assets** (ready-to-use configurations and checklists):
- `assets/validation-checklist.md` - Comprehensive documentation completeness checklist for project handoff
- `assets/vale-config.ini` - Vale prose linting configuration template for scientific documentation

## Quick Reference Card

### Validation Tool Decision Tree

```
What do you need to validate?
|
+-- Prose quality (grammar, style, jargon)?
|   => Vale (configurable prose linter)
|
+-- Markdown syntax and formatting?
|   => markdownlint / markdownlint-cli2
|
+-- reStructuredText syntax?
|   => doc8
|
+-- Links (internal + external)?
|   => HTMLProofer (for generated HTML)
|   => markdown-link-check (for raw Markdown)
|   => sphinx -b linkcheck (for Sphinx projects)
|
+-- Code examples actually work?
|   => pytest --doctest-glob (for Markdown/RST)
|   => doctest module (for docstrings)
|   => nbval / pytest-notebook (for Jupyter notebooks)
|
+-- Setup instructions actually work?
|   => Docker-based instruction testing
|   => GitHub Actions clean environment
|
+-- Overall documentation completeness?
|   => Handoff checklist (see assets/validation-checklist.md)
```

### Essential Commands at a Glance

```bash
# Prose linting with Vale
vale docs/

# Markdown linting
markdownlint-cli2 "docs/**/*.md"

# reStructuredText linting
doc8 docs/

# Link checking (Sphinx)
sphinx-build -b linkcheck docs docs/_build/linkcheck

# Link checking (HTML output)
htmlproofer docs/_build/html --check-links

# Test code examples in documentation
pytest --doctest-glob="*.md" docs/
pytest --doctest-glob="*.rst" docs/

# Notebook validation
pytest --nbval docs/notebooks/

# Container-based instruction testing
docker build -f Dockerfile.test-docs -t docs-test .
```

## When to Use This Skill

Use this skill when you need to:

- Ensure documentation prose is clear, consistent, and free of common writing issues
- Validate that all links in documentation (internal and external) resolve correctly
- Test that code examples embedded in documentation actually execute and produce expected output
- Verify that setup and installation instructions work in a clean environment
- Set up continuous integration pipelines that automatically check documentation quality
- Prepare a project for handoff by verifying documentation completeness
- Establish documentation quality standards for a team or organization
- Audit existing documentation for staleness, broken links, or incomplete coverage
- Lint reStructuredText or Markdown files for syntax errors and style consistency
- Test Jupyter notebooks included in documentation to ensure they still execute

## Validation Tools

### Vale: Prose Linting

**What it does:** Vale is a syntax-aware prose linter that enforces writing style rules. It checks for grammar issues, jargon, passive voice, weasel words, and adherence to style guides. Unlike generic spell checkers, Vale understands markup syntax (Markdown, RST, HTML) and only checks prose content.

**Why it matters for scientific documentation:** Scientific writing often suffers from unnecessarily complex language, inconsistent terminology, and jargon that alienates newcomers. Vale enforces readable, inclusive documentation while allowing domain-specific vocabulary.

**Installation:**

```bash
# macOS
brew install vale

# Linux (snap)
snap install vale

# Linux (manual)
wget https://github.com/errata-ai/vale/releases/latest/download/vale_Linux_64-bit.tar.gz
tar -xvzf vale_Linux_64-bit.tar.gz -C /usr/local/bin

# Using pipx (cross-platform, runs the vale-cli wrapper)
pipx install vale
```

**Configuration:**

Create a `.vale.ini` in your repository root. See `assets/vale-config.ini` for a complete template. The minimal configuration is:

```ini
StylesPath = .vale/styles
MinAlertLevel = warning

Packages = proselint, write-good, Google

[*.md]
BasedOnStyles = Vale, proselint, write-good
```

After creating the config, sync the packages:

```bash
vale sync
```

**Running Vale:**

```bash
# Lint all documentation
vale docs/

# Lint a specific file
vale docs/getting-started/installation.md

# Output as JSON (useful for CI)
vale --output=JSON docs/

# Only show errors (not warnings or suggestions)
vale --minAlertLevel=error docs/
```

**Scientific Writing Rules:**

Vale supports custom rules for domain-specific needs. Create vocabulary files to allow scientific terms that would otherwise be flagged:

```
# .vale/styles/Vocab/Scientific/accept.txt
NumPy
SciPy
DataFrame
docstring
boolean
namespace
reproducibility
citable
metadata
```

```
# .vale/styles/Vocab/Scientific/reject.txt
obviously
trivially
simply
easy
straightforward
```

Rejecting words like "obviously" and "simply" helps produce documentation that does not make assumptions about the reader's background, which is particularly important in scientific contexts where audiences vary widely in expertise.

**Custom Vale Rule Example:**

Create project-specific rules in `.vale/styles/Custom/`:

```yaml
# .vale/styles/Custom/ScientificAbbreviations.yml
extends: existence
message: "Expand '%s' on first use. Scientific abbreviations should be defined."
level: warning
tokens:
  - '\b[A-Z]{2,}\b'
exceptions:
  - API
  - CI
  - CD
  - URL
  - HTML
  - CSS
  - JSON
  - YAML
  - RST
  - PDF
```

### HTMLProofer: Link Checking for Generated Documentation

**What it does:** HTMLProofer validates generated HTML documentation by checking that all links resolve, images have alt attributes, and HTML is well-formed. It is the standard tool for validating the output of Sphinx, MkDocs, and Jupyter Book builds.

**Installation:**

```bash
# Requires Ruby
gem install html-proofer

# Or via Docker
docker run --rm -v $(pwd)/docs/_build/html:/site 18fgsa/html-proofer /site
```

**Basic Usage:**

```bash
# First, build your documentation
sphinx-build -b html docs docs/_build/html

# Then validate the output
htmlproofer docs/_build/html \
  --check-links \
  --check-images \
  --allow-missing-href \
  --ignore-status-codes "403,429"
```

**Advanced Configuration:**

```bash
htmlproofer docs/_build/html \
  --check-links \
  --check-images \
  --check-scripts \
  --enforce-https \
  --ignore-urls "/localhost/,/127.0.0.1/,/example.com/" \
  --ignore-status-codes "403,429,503" \
  --swap-urls "https://docs.myproject.org:docs/_build/html" \
  --typhoeus-config '{"timeout":30,"connecttimeout":10}' \
  --cache '{"timeframe":{"external":"1d"}}'
```

**Alternative: Sphinx Built-in Link Checker:**

For Sphinx-based projects, use the built-in linkcheck builder:

```bash
sphinx-build -b linkcheck docs docs/_build/linkcheck
```

This generates a report at `docs/_build/linkcheck/output.txt` showing the status of every external link.

**Alternative for Raw Markdown: markdown-link-check:**

```bash
# Install
npm install -g markdown-link-check

# Check a file
markdown-link-check docs/README.md

# Check all markdown files
find docs -name "*.md" -exec markdown-link-check {} \;

# Using a config file
markdown-link-check -c .markdown-link-check.json docs/README.md
```

Configuration file `.markdown-link-check.json`:

```json
{
  "ignorePatterns": [
    { "pattern": "^https://localhost" },
    { "pattern": "^https://example\\.com" }
  ],
  "replacementPatterns": [
    { "pattern": "^/docs", "replacement": "https://mysite.org/docs" }
  ],
  "httpHeaders": [
    {
      "urls": ["https://github.com"],
      "headers": { "Accept": "text/html" }
    }
  ],
  "timeout": "20s",
  "retryOn429": true,
  "retryCount": 3,
  "aliveStatusCodes": [200, 206]
}
```

### markdownlint: Markdown Syntax and Style Consistency

**What it does:** markdownlint enforces consistent Markdown formatting and catches common syntax errors. It validates heading structure, list formatting, line length, code block syntax, and dozens of other Markdown conventions.

**Installation:**

```bash
# CLI version (recommended)
npm install -g markdownlint-cli2

# Or via Docker
docker run --rm -v $(pwd):/workdir davidanson/markdownlint-cli2 "docs/**/*.md"
```

**Configuration:**

Create `.markdownlint-cli2.yaml` in your repository root:

```yaml
config:
  # MD013 - Line length
  MD013:
    line_length: 120
    code_blocks: false
    tables: false
    headings: false

  # MD024 - Allow duplicate headings in different sections
  MD024:
    siblings_only: true

  # MD033 - Allow specific inline HTML
  MD033:
    allowed_elements:
      - details
      - summary
      - br
      - sup
      - sub

  # MD041 - First line should be a heading (disable for includes)
  MD041: false

  # MD046 - Code block style
  MD046:
    style: fenced

  # MD048 - Code fence style
  MD048:
    style: backtick

globs:
  - "docs/**/*.md"
  - "*.md"
  - "!node_modules"
  - "!.vale"

ignores:
  - "CHANGELOG.md"
  - "**/generated/**"
```

**Running markdownlint:**

```bash
# Lint all documentation
markdownlint-cli2 "docs/**/*.md"

# Fix auto-fixable issues
markdownlint-cli2 --fix "docs/**/*.md"

# Lint specific file
markdownlint-cli2 docs/getting-started/installation.md
```

### doc8: reStructuredText Linting

**What it does:** doc8 is an opinionated linter for reStructuredText files. It checks line length, trailing whitespace, invalid RST syntax, and other formatting issues. It is particularly useful for projects that use Sphinx with reStructuredText.

**Installation:**

```bash
pip install doc8
```

**Configuration in `pyproject.toml`:**

```toml
[tool.doc8]
max-line-length = 120
ignore-path = [
    "docs/_build",
    "docs/generated",
]
ignore-path-errors = [
    "docs/changelog.rst;D001",
]
```

**Running doc8:**

```bash
# Lint all RST files in docs/
doc8 docs/

# With custom max line length
doc8 --max-line-length 120 docs/

# Ignore specific rules
doc8 --ignore D001 docs/
```

**Common doc8 rules:**

| Rule | Description |
|------|-------------|
| D000 | Invalid RST syntax |
| D001 | Line too long |
| D002 | Trailing whitespace |
| D003 | Tabulation used for indentation |
| D004 | Found literal block with no indentation |
| D005 | No newline at end of file |

## Documentation-as-Code Testing Strategies

### Treating Documentation Like Code

Documentation-as-code means applying the same practices to documentation that you apply to source code:

| Practice | Code | Documentation |
|----------|------|---------------|
| Version control | git | git (docs live alongside code) |
| Code review | Pull requests | Pull requests for doc changes |
| Automated testing | pytest, CI | Vale, linkcheck, doctest, CI |
| Linting | ruff, mypy | Vale, markdownlint, doc8 |
| Formatting | ruff format | Prettier, markdownlint --fix |
| Deployment | PyPI, Docker | Read the Docs, GitHub Pages |
| Issue tracking | GitHub Issues | GitHub Issues (label: documentation) |

**Key principle:** Every documentation change goes through the same review and CI pipeline as code changes. Documentation pull requests should be tested automatically before merge.

### Testing Code Examples in Documentation

Code examples that do not actually work are worse than no examples at all. They erode trust and waste the reader's time. Always validate that code examples execute correctly.

**Using pytest with doctest-glob:**

```bash
# Test code examples in Markdown files
pytest --doctest-glob="*.md" docs/

# Test code examples in reStructuredText files
pytest --doctest-glob="*.rst" docs/

# Combine with regular tests
pytest tests/ --doctest-glob="*.md" docs/
```

**Writing testable examples in Markdown:**

````markdown
Here is how to compute the mean of an array:

```python
>>> import numpy as np
>>> data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
>>> np.mean(data)
3.0
```
````

The `>>>` prefix makes these examples discoverable by doctest. The expected output on the next line is used for assertion.

**Using doctest in Python docstrings:**

```bash
# Run doctests in all module docstrings
pytest --doctest-modules src/

# Or with the standard library
python -m doctest -v docs/tutorial.md
```

**pytest configuration for doctest:**

```toml
# pyproject.toml
[tool.pytest.ini_options]
addopts = [
    "--doctest-glob=*.md",
    "--doctest-glob=*.rst",
]
doctest_optionflags = [
    "NORMALIZE_WHITESPACE",
    "ELLIPSIS",
    "NUMBER",
]
```

The `NORMALIZE_WHITESPACE` flag prevents failures from trivial whitespace differences. `ELLIPSIS` allows `...` to match any text, and `NUMBER` handles floating-point comparison tolerance.

### Notebook Testing

**Note:** The following section covers Python/Jupyter notebook testing. For non-Python projects, validate documentation examples using language-appropriate test frameworks (cargo test --doc for Rust, go test for Go, testthat for R, npm test for Node.js).

Jupyter notebooks in documentation must be validated to ensure they still execute correctly as dependencies and APIs evolve.

**nbval: Validate notebook output:**

```bash
# Install
pip install nbval

# Validate that notebooks execute and produce the same output
pytest --nbval docs/notebooks/

# Validate that notebooks execute (ignore output differences)
pytest --nbval-lax docs/notebooks/

# Skip cells tagged with 'skip' in metadata
pytest --nbval --nbval-current-env docs/notebooks/
```

**pytest-notebook: More control over notebook testing:**

```bash
# Install
pip install pytest-notebook

# Run notebook tests
pytest --nb-test-files docs/notebooks/
```

**Configuration for nbval in `pyproject.toml`:**

```toml
[tool.pytest.ini_options]
nb_test_files = "docs/notebooks/"
nb_diff_ignore = [
    "/metadata",
    "/cells/*/outputs/*/execution_count",
]
```

**Tagging cells to skip during testing:**

In notebook cell metadata, add:

```json
{
  "tags": ["skip-execution"]
}
```

Then configure nbval to respect the tag:

```bash
pytest --nbval --nbval-cell-timeout=120 docs/notebooks/
```

## Container-Based Instruction Testing

### Why Test Instructions in a Clean Environment

The most common documentation failure is "works on my machine" syndrome. Setup instructions that rely on undocumented system dependencies, cached packages, or pre-existing configuration will fail for new users. Testing instructions in a clean container catches these issues.

### Following Setup Instructions in Docker

Create a `Dockerfile.test-docs` that simulates a new user following your README:

```dockerfile
# Dockerfile.test-docs
# Tests that setup instructions from README actually work

# Replace with your language's base image (python:3.12-slim, rust:1.75, node:20-slim, etc.)
FROM ubuntu:22.04

# Start from a minimal environment
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Copy the repository
COPY . .

# Replace with your project's install command
# Examples:
#   Python:  pip install -e ".[dev,docs]"
#   Rust:    cargo build
#   Node.js: npm install
#   R:       Rscript -e "devtools::install('.')"
#   Go:     go build ./...
RUN echo "Add your install command here"

# Verify the installation works
# Examples:
#   Python:  python -c "import my_package; print(my_package.__version__)"
#   Rust:    cargo test --no-run
#   Node.js: node -e "require('./index')"
RUN echo "Add your verification command here"

# Run the quickstart example from the documentation
RUN echo "Add your quickstart test command here"

# Build the documentation to verify it compiles
RUN echo "Add your documentation build command here"
```

**Build and run the test:**

```bash
# Build the image (this runs all the instructions)
docker build -f Dockerfile.test-docs -t docs-test .

# If the build succeeds, the instructions work
echo "Documentation instructions validated successfully"
```

### Automated README Validation Script

Create a script that extracts and tests code blocks from your README:

```bash
#!/usr/bin/env bash
# scripts/test-readme.sh
# Extract and run code blocks from README.md in a clean environment

set -euo pipefail

echo "=== Testing README instructions in clean Docker container ==="

docker run --rm -v "$(pwd)":/workspace -w /workspace python:3.12-slim bash -c '
    set -euo pipefail

    echo "--- Installing from README instructions ---"
    pip install -e ".[dev]" 2>&1 | tail -5

    echo "--- Running import check ---"
    python -c "import my_package; print(f\"Version: {my_package.__version__}\")"

    echo "--- Running quickstart example ---"
    python -c "
from my_package import analyze
result = analyze([1, 2, 3, 4, 5])
print(f\"Result: {result}\")
"
    echo "--- All README instructions passed ---"
'
```

### Multi-Environment Testing

Test instructions across multiple Python versions and operating systems:

```yaml
# .github/workflows/test-docs-instructions.yml
name: Test Documentation Instructions

on:
  push:
    paths:
      - "docs/**"
      - "README.md"
      - "INSTALL.md"
  pull_request:
    paths:
      - "docs/**"
      - "README.md"
      - "INSTALL.md"

jobs:
  test-instructions:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ["3.10", "3.11", "3.12"]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Follow installation instructions
        run: |
          pip install -e ".[dev,docs]"

      - name: Verify import works
        run: |
          python -c "import my_package; print(my_package.__version__)"

      - name: Run quickstart example
        run: |
          python docs/getting-started/quickstart_test.py
```

## GitHub Actions Integration for Automated Doc Validation

### Comprehensive Documentation CI Workflow

**Note:** The following CI workflow examples use Python tooling (pip, Sphinx, pytest). Adapt these patterns for your project's language and documentation build system.

```yaml
# .github/workflows/docs-validation.yml
name: Documentation Validation

on:
  push:
    branches: [main]
    paths:
      - "docs/**"
      - "*.md"
      - ".vale.ini"
      - ".markdownlint-cli2.yaml"
  pull_request:
    paths:
      - "docs/**"
      - "*.md"
      - ".vale.ini"
      - ".markdownlint-cli2.yaml"

jobs:
  prose-lint:
    name: Prose Linting (Vale)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: errata-ai/vale-action@reviewdog
        with:
          files: docs/
          reporter: github-pr-review
          fail_on_error: true

  markdown-lint:
    name: Markdown Linting
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: DavidAnson/markdownlint-cli2-action@v19
        with:
          globs: |
            docs/**/*.md
            *.md

  link-check:
    name: Link Validation
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: pip install -e ".[docs]"
      - name: Build documentation
        run: sphinx-build -b html docs docs/_build/html
      - name: Check links
        run: sphinx-build -b linkcheck docs docs/_build/linkcheck

  doctest:
    name: Documentation Code Examples
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: pip install -e ".[dev,docs]"
      - name: Run doctests in documentation
        run: pytest --doctest-glob="*.md" --doctest-glob="*.rst" docs/
      - name: Run doctests in source
        run: pytest --doctest-modules src/

  notebook-validation:
    name: Notebook Validation
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: pip install -e ".[dev,docs]" nbval
      - name: Validate notebooks
        run: pytest --nbval-lax docs/notebooks/

  docs-build:
    name: Documentation Build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: pip install -e ".[docs]"
      - name: Build docs (treat warnings as errors)
        run: sphinx-build -W --keep-going -b html docs docs/_build/html
      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: documentation
          path: docs/_build/html/
```

### Standalone Vale GitHub Action

For projects that want Vale as a pull request reviewer:

```yaml
# .github/workflows/vale.yml
name: Vale Prose Lint

on:
  pull_request:
    paths:
      - "docs/**"
      - "*.md"

jobs:
  vale:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: errata-ai/vale-action@reviewdog
        with:
          files: docs/
          vale_flags: "--minAlertLevel=warning"
          reporter: github-pr-review
          fail_on_error: true
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Scheduled Link Checking

External links break over time. Schedule periodic link checks:

```yaml
# .github/workflows/link-check-scheduled.yml
name: Scheduled Link Check

on:
  schedule:
    # Run weekly on Monday at 9:00 UTC
    - cron: "0 9 * * 1"
  workflow_dispatch:

jobs:
  link-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: pip install -e ".[docs]"
      - name: Build documentation
        run: sphinx-build -b html docs docs/_build/html
      - name: Check links
        run: sphinx-build -b linkcheck docs docs/_build/linkcheck
      - name: Report broken links
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: linkcheck-report
          path: docs/_build/linkcheck/output.txt
```

## Quality Metrics and Standards

### Readability Scores

Readability metrics help ensure documentation is accessible to your target audience:

| Metric | Target | Interpretation |
|--------|--------|----------------|
| Flesch Reading Ease | 40-60 (technical), 60-70 (tutorials) | Higher = easier to read |
| Flesch-Kincaid Grade | 10-14 (technical), 8-10 (tutorials) | Grade level required to understand |
| Gunning Fog Index | 10-14 (technical), 8-10 (tutorials) | Years of education needed |

Vale can enforce readability with the `readability` package:

```ini
# .vale.ini addition
Packages = readability

[docs/tutorials/*.md]
BasedOnStyles = Vale, readability
readability.FleschKincaid = warning
```

### Link Health Metrics

Track link health over time:

| Metric | Target | Action if Below |
|--------|--------|-----------------|
| Internal links resolving | 100% | Fix immediately (blocks merge) |
| External links resolving | >95% | Investigate; ignore transient 429/503 |
| Links with redirects | <10% | Update to final URLs |
| Links over 3 years old | <20% | Verify content still relevant |

### Documentation Completeness Metrics

| Category | Weight | Minimum Standard |
|----------|--------|-----------------|
| README with install + quickstart | Critical | Must exist |
| API reference for public functions | Critical | 100% coverage |
| At least one tutorial | High | Must exist |
| Contributing guide | High | Must exist |
| Architecture overview | Medium | Should exist for complex projects |
| Changelog | High | Must exist and be current |
| License file | Critical | Must exist |

### Definition of "Documentation Complete"

A project's documentation is considered complete when it meets all of the following criteria:

1. **Buildable**: Documentation builds without warnings (`sphinx-build -W`)
2. **Linkable**: All internal and external links resolve
3. **Testable**: All code examples execute successfully
4. **Linted**: Prose passes Vale checks with no errors
5. **Structured**: Follows Diataxis framework (tutorials, how-to, reference, explanation)
6. **Accessible**: Meets basic accessibility standards (alt text, heading hierarchy, contrast)
7. **Complete**: Passes the handoff checklist (see `assets/validation-checklist.md`)
8. **Reviewable**: At least one person other than the author has reviewed the docs
9. **Findable**: Search works and navigation is logical
10. **Current**: No documentation references deprecated APIs or removed features

## Project Handoff Documentation Completeness Checklist

Use this checklist when preparing a project for handoff to new maintainers, a new team, or the broader community. A detailed, standalone version with additional context is available at `assets/validation-checklist.md`.

### Summary Checklist

**Essential Files:**
- [ ] README.md with project description, installation, and quickstart
- [ ] LICENSE file with appropriate open-source license
- [ ] CONTRIBUTING.md with contribution guidelines
- [ ] CHANGELOG.md with version history
- [ ] CITATION.cff for scientific projects

**User Documentation:**
- [ ] Installation guide covering all supported methods
- [ ] Quickstart tutorial (5-minute path to first result)
- [ ] At least one in-depth tutorial
- [ ] API reference for all public interfaces
- [ ] Configuration reference

**Developer Documentation:**
- [ ] Architecture overview with diagrams
- [ ] Development environment setup guide
- [ ] Testing guide (how to run tests, write tests, CI behavior)
- [ ] Release process documentation
- [ ] Dependency management explanation

**Project Health:**
- [ ] CI/CD pipeline documented and working
- [ ] Code quality tools configured and documented
- [ ] All tests passing
- [ ] Documentation builds without warnings
- [ ] No critical security vulnerabilities

**Onboarding:**
- [ ] "Getting started as a developer" guide
- [ ] Key contacts and communication channels
- [ ] Glossary of project-specific terms
- [ ] Known issues and technical debt documented
- [ ] Decision log for major architectural choices

## Best Practices

### Integrate Early, Validate Often

Do not wait until the end of a project to validate documentation. Set up CI-based documentation validation from the start:

1. Add Vale and markdownlint to pre-commit hooks for immediate feedback
2. Run doctests as part of your regular test suite
3. Check links on every pull request
4. Build documentation with warnings-as-errors in CI
5. Schedule weekly link checks for external URL decay

### Pre-commit Integration

Add documentation validation to your pre-commit configuration:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/errata-ai/vale
    rev: v3.9.0
    hooks:
      - id: vale
        args: [--minAlertLevel, warning]
        types_or: [markdown, rst]

  - repo: https://github.com/DavidAnson/markdownlint-cli2
    rev: v0.17.0
    hooks:
      - id: markdownlint-cli2
        args: ["docs/**/*.md", "*.md"]

  - repo: https://github.com/PyCQA/doc8
    rev: v1.1.2
    hooks:
      - id: doc8
        args: [--max-line-length, "120"]
```

### Nox Sessions for Documentation Validation

**Python Example:** The following Nox sessions demonstrate documentation validation for Python projects. Adapt the patterns to your project's task runner.

```python
# noxfile.py additions for documentation validation
import nox

@nox.session(python="3.12")
def docs_lint(session):
    """Lint documentation prose with Vale."""
    session.run("vale", "docs/", external=True)

@nox.session(python="3.12")
def docs_linkcheck(session):
    """Check documentation links."""
    session.install(".[docs]")
    session.run(
        "sphinx-build", "-b", "linkcheck",
        "docs", "docs/_build/linkcheck",
    )

@nox.session(python="3.12")
def docs_doctest(session):
    """Test code examples in documentation."""
    session.install(".[dev,docs]")
    session.run(
        "pytest",
        "--doctest-glob=*.md",
        "--doctest-glob=*.rst",
        "docs/",
    )

@nox.session(python="3.12")
def docs_notebooks(session):
    """Validate Jupyter notebooks in documentation."""
    session.install(".[dev,docs]", "nbval")
    session.run(
        "pytest", "--nbval-lax",
        "docs/notebooks/",
    )

@nox.session(python="3.12")
def docs_build(session):
    """Build documentation with warnings as errors."""
    session.install(".[docs]")
    session.run(
        "sphinx-build", "-W", "--keep-going",
        "-b", "html",
        "docs", "docs/_build/html",
    )
```

### Documentation Review Checklist for Pull Requests

When reviewing documentation changes in pull requests, verify:

- [ ] Prose is clear, concise, and free of jargon (or jargon is defined)
- [ ] Code examples are complete and runnable
- [ ] Links point to stable URLs (not branch-specific or ephemeral)
- [ ] Headings follow a logical hierarchy
- [ ] New features have corresponding documentation
- [ ] Removed features have documentation updated or removed
- [ ] Screenshots or diagrams are current
- [ ] Alt text is provided for all images

## Resources

### Official Documentation for Validation Tools
- **Vale**: https://vale.sh/docs/
- **HTMLProofer**: https://github.com/gjtorikian/html-proofer
- **markdownlint**: https://github.com/DavidAnson/markdownlint
- **markdownlint-cli2**: https://github.com/DavidAnson/markdownlint-cli2
- **doc8**: https://github.com/PyCQA/doc8
- **nbval**: https://github.com/computationalmodelling/nbval
- **pytest-notebook**: https://github.com/chrisjsewell/pytest-notebook

### Style Guides and Packages for Vale
- **proselint**: https://github.com/errata-ai/proselint
- **write-good**: https://github.com/errata-ai/write-good
- **Google Developer Style**: https://github.com/errata-ai/Google
- **Microsoft Style**: https://github.com/errata-ai/Microsoft

### Language-Specific Documentation Resources
- **Scientific Python Development Guide - Docs**: https://learn.scientific-python.org/development/guides/docs/
- **Diataxis Framework**: https://diataxis.fr/
- **NumPy Documentation Style**: https://numpydoc.readthedocs.io/en/latest/format.html
- **Rust Documentation**: https://doc.rust-lang.org/rustdoc/
- **R pkgdown**: https://pkgdown.r-lib.org/
- **Go Documentation**: https://go.dev/doc/
- **Julia Documenter.jl**: https://documenter.juliadocs.org/

### GitHub Actions for Documentation
- **Vale Action**: https://github.com/errata-ai/vale-action
- **markdownlint-cli2-action**: https://github.com/DavidAnson/markdownlint-cli2-action
- **markdown-link-check Action**: https://github.com/gaurav-nelson/github-action-markdown-link-check

## Summary

Documentation validation transforms documentation from an afterthought into a tested, reliable deliverable. By applying the same rigor to documentation that we apply to code -- version control, automated testing, linting, and CI -- we ensure that users and contributors can trust the documentation they read.

**Key takeaways:**

Use Vale for prose quality and style consistency across your documentation. Use HTMLProofer or Sphinx linkcheck to catch broken links before users encounter them. Test code examples with pytest doctest-glob and validate notebooks with nbval. Test setup instructions in clean Docker containers to catch "works on my machine" problems. Integrate all validation into GitHub Actions so every pull request is automatically checked. Use the handoff checklist to verify documentation completeness before project milestones.

**Start here:** Install Vale and add it to your pre-commit hooks. This single step catches the most common documentation issues -- unclear prose, passive voice, jargon, and inconsistency -- before they ever reach a reviewer.

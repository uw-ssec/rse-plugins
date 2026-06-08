---
name: documentation-validation
description: "Use when the user wants to validate documentation quality, check for broken links, lint prose or Markdown, test code examples, verify setup instructions, or set up CI for documentation testing. Covers prose linting with Vale, Markdown/RST syntax checking (markdownlint, doc8), link validation (HTMLProofer, lychee, markdown-link-check), code example testing (pytest doctest, cargo test --doc), notebook validation (nbval), container-based instruction testing, and GitHub Actions CI integration for research software projects. Trigger phrases: check my docs, broken links, doc quality, documentation errors, spelling/grammar in docs, test documentation, validate README, link check, prose linting, doc CI."
metadata:
  references:
    - references/vale-configuration.md
    - references/documentation-standards.md
    - references/validation-tools.md
  assets:
    - assets/vale-config.ini
    - assets/validation-checklist.md
---

# Documentation Validation

Treat documentation as a tested, linted, CI-checked deliverable — not an afterthought.

## Resources in This Skill

**References** (detailed guides — use the table of contents in each file):

| File | Contents |
|------|----------|
| `references/vale-configuration.md` | Vale `.vale.ini` options, style packages (proselint, write-good, Google, alex), custom rules, vocabulary files, editor/CI integration, configuration recipes |
| `references/validation-tools.md` | markdownlint, HTMLProofer, doc8, link checkers (lychee, markdown-link-check), language-specific doc testing (Python/Rust/R/Go/Julia), notebook validation, CI pipeline assembly, pre-commit hooks, container-based instruction testing |
| `references/documentation-standards.md` | Diataxis framework, completeness criteria (4 maturity levels), README standards, API doc coverage, readability metrics, documentation debt, definition of "documentation complete" |

**Assets** (ready-to-use):

| File | Contents |
|------|----------|
| `assets/vale-config.ini` | Annotated Vale config template for scientific documentation |
| `assets/validation-checklist.md` | Completeness checklist for project handoff (Essential Files, User Docs, Developer Docs, Project Health, Scientific-specific, Onboarding) |

---

## Quick Reference Card

### Tool Decision Tree

```
What do you need to validate?
│
├── Prose quality (grammar, style, passive voice, jargon)?
│   └── Vale  →  see references/vale-configuration.md
│
├── Markdown syntax and formatting?
│   └── markdownlint-cli2  →  see references/validation-tools.md#markdownlint
│
├── reStructuredText syntax?
│   └── doc8  →  see references/validation-tools.md#doc8
│
├── Broken links?
│   ├── In Markdown files  →  markdown-link-check or lychee
│   ├── In HTML docs       →  HTMLProofer
│   └── In Sphinx projects →  sphinx-build -b linkcheck
│
├── Code examples actually work?
│   ├── Python (>>> blocks)   →  pytest --doctest-glob
│   ├── Rust (/// comments)   →  cargo test --doc
│   ├── Go (// Output: blocks) →  go test -run Example
│   └── Julia (jldoctest)     →  julia Documenter.jl doctests
│
├── Jupyter notebooks execute correctly?
│   └── nbval / pytest-notebook  →  see references/validation-tools.md#notebook-validation
│
├── Setup instructions work in a clean environment?
│   └── Container-based testing  →  see references/validation-tools.md#container-based-instruction-testing
│
└── Overall documentation completeness?
    └── assets/validation-checklist.md
```

### Essential Commands

```bash
# Prose linting
vale docs/                                          # lint all docs
vale --minAlertLevel=error docs/                    # errors only

# Markdown linting
markdownlint-cli2 "docs/**/*.md"                   # lint
markdownlint-cli2 --fix "docs/**/*.md"             # auto-fix

# RST linting
doc8 docs/

# Link checking
lychee "**/*.md"                                    # Markdown files
sphinx-build -b linkcheck docs docs/_build/linkcheck  # Sphinx
htmlproofer docs/_build/html --ignore-status-codes "403,429"  # HTML output

# Code examples
pytest --doctest-glob="*.md" --doctest-glob="*.rst" docs/
cargo test --doc
go test -run Example ./...

# Notebook validation
pytest --nbval-lax docs/notebooks/

# Container-based instruction testing
docker build -f Dockerfile.test-docs -t docs-test .
```

---

## Setup Workflow for a New Project

Follow these steps in order, verifying each checkpoint before proceeding.

### 1. Prose linting (Vale)

```bash
# Install Vale (macOS/Linux)
brew install vale          # macOS
snap install vale          # Linux

# Copy the template config and sync packages
cp path/to/assets/vale-config.ini .vale.ini
vale sync

# Checkpoint: Vale runs locally without errors
vale docs/
```

For full configuration options (style packages, custom rules, vocabulary), see `references/vale-configuration.md`.

### 2. Markdown / RST linting

```bash
npm install -g markdownlint-cli2
pip install doc8

# Checkpoint: linters run cleanly
markdownlint-cli2 "docs/**/*.md"
doc8 docs/
```

For `.markdownlint-cli2.yaml` and `.doc8.ini` config examples, see `references/validation-tools.md`.

### 3. Link checking

```bash
brew install lychee   # or: cargo install lychee

# Checkpoint: no broken internal links
lychee --exclude "example\.com" "**/*.md"
```

Set up a scheduled CI job for external links (external links are slow and flaky — avoid blocking PRs on them). See `references/validation-tools.md#ci-pipeline-assembly` for a ready-to-use GitHub Actions workflow.

### 4. Code example testing

```bash
# Python
pytest --doctest-glob="*.md" docs/

# Checkpoint: all >>> blocks pass
```

Other languages: see `references/validation-tools.md#language-specific-doc-testing`.

### 5. Pre-commit hooks

Add Vale and markdownlint to `.pre-commit-config.yaml` so every commit is checked locally. See `references/validation-tools.md#pre-commit-integration` for the full hook config.

### 6. CI integration

Add a GitHub Actions workflow that runs all validation on every PR touching docs. See `references/validation-tools.md#ci-pipeline-assembly` for a complete multi-job workflow.

**Checkpoint:** Before marking documentation ready, verify against the completeness criteria in `references/documentation-standards.md#completeness-criteria` and the "definition of documentation complete" checklist.

---

## Common Tasks

### Set up Vale for a project

1. Copy `assets/vale-config.ini` to `.vale.ini` in the repo root
2. Run `vale sync` to download style packages
3. Add scientific terms to `.vale/styles/Vocab/Scientific/accept.txt`
4. Run `vale docs/` to see initial findings
5. See `references/vale-configuration.md` for style package selection and custom rule examples

### Audit documentation for a project handoff

1. Run all linters locally: `vale docs/`, `markdownlint-cli2 "**/*.md"`, `lychee "**/*.md"`
2. Run code example tests: `pytest --doctest-glob="*.md" docs/`
3. Work through `assets/validation-checklist.md` item by item
4. Check completeness level against `references/documentation-standards.md#completeness-criteria`

### Test that setup instructions actually work

Create a `Dockerfile.test-docs` that installs the project from scratch and runs the quickstart example. See `references/validation-tools.md#container-based-instruction-testing` for a language-agnostic template and multi-OS GitHub Actions matrix.

### Add documentation CI to an existing project

See `references/validation-tools.md#ci-pipeline-assembly` for a complete GitHub Actions workflow covering prose linting, Markdown linting, link checking, code example testing, and documentation build.

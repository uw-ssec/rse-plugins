# Documentation Completeness Checklist

A comprehensive checklist for validating that project documentation is complete, accurate, and ready for handoff. Use this checklist when preparing a project for release, transferring ownership to new maintainers, onboarding new team members, or auditing documentation health.

**How to use this checklist:**
- Copy this file into your project repository or issue tracker
- Check off items as they are completed
- Items marked **(Critical)** must be completed before any release or handoff
- Items marked **(Recommended)** should be completed for mature projects
- Items marked **(Scientific)** are specific to scientific/research software
- Not every project needs every item -- skip categories that do not apply

---

## Essential Repository Files

These files should exist at the root of the repository and are expected by the open-source community.

- [ ] **(Critical)** `README.md` exists and contains:
  - [ ] Project name and one-sentence description
  - [ ] Badges for CI status, coverage, PyPI version, and license
  - [ ] Installation instructions (at least one method)
  - [ ] Minimal usage example (copy-paste-runnable)
  - [ ] Link to full documentation
  - [ ] Link to contributing guide
  - [ ] License information
- [ ] **(Critical)** `LICENSE` or `LICENSE.txt` exists with an appropriate open-source license
  - [ ] License is OSI-approved (MIT, BSD-3-Clause, Apache-2.0, etc.)
  - [ ] License year and copyright holder are correct
- [ ] **(Critical)** `CONTRIBUTING.md` exists and contains:
  - [ ] How to report bugs
  - [ ] How to request features
  - [ ] How to submit pull requests
  - [ ] Development environment setup instructions
  - [ ] Code style and quality expectations
  - [ ] Code of conduct reference
- [ ] **(Critical)** `CHANGELOG.md` or `CHANGES.rst` exists and contains:
  - [ ] Entries for all released versions
  - [ ] Categorized changes (Added, Changed, Deprecated, Removed, Fixed, Security)
  - [ ] Date for each release
  - [ ] Links to relevant pull requests or issues
- [ ] **(Recommended)** `CODE_OF_CONDUCT.md` exists (Contributor Covenant or equivalent)
- [ ] **(Recommended)** `SECURITY.md` exists with vulnerability reporting instructions
- [ ] **(Recommended)** `.github/ISSUE_TEMPLATE/` directory with bug report and feature request templates
- [ ] **(Recommended)** `.github/PULL_REQUEST_TEMPLATE.md` exists

---

## User Documentation

Documentation that end users need to install, configure, and use the software.

### Installation

- [ ] **(Critical)** Installation instructions cover the primary method (the project's package manager)
- [ ] **(Recommended)** Installation instructions cover alternative methods
- [ ] **(Recommended)** System prerequisites are listed (Language/runtime version, OS, system libraries)
- [ ] **(Recommended)** Instructions tested in a clean environment (Docker or fresh venv)
- [ ] **(Recommended)** Troubleshooting section for common installation issues
- [ ] **(Scientific)** Instructions for installing optional heavy dependencies (GPU, MPI, etc.)

### Quickstart / Getting Started

- [ ] **(Critical)** Quickstart guide exists (path to first meaningful result in under 5 minutes)
- [ ] **(Critical)** Quickstart code examples are copy-paste-runnable
- [ ] **(Recommended)** Quickstart uses realistic but minimal data
- [ ] **(Recommended)** Expected output is shown alongside code examples
- [ ] **(Recommended)** Quickstart links to deeper tutorials for next steps

### Tutorials

- [ ] **(Critical)** At least one tutorial exists for the primary use case
- [ ] **(Recommended)** Tutorials progress from simple to complex
- [ ] **(Recommended)** Tutorials use the Diataxis "learning-oriented" style
- [ ] **(Recommended)** Tutorials include complete, working code (not fragments)
- [ ] **(Recommended)** Tutorials explain the "why" alongside the "how"
- [ ] **(Scientific)** Tutorials use realistic scientific data or scenarios
- [ ] **(Scientific)** Tutorials include visualization of results where applicable

### How-to Guides

- [ ] **(Recommended)** Common tasks have dedicated how-to guides
- [ ] **(Recommended)** How-to guides are goal-oriented and practical
- [ ] **(Recommended)** How-to guides assume the reader has basic familiarity
- [ ] **(Recommended)** How-to guides link to relevant API reference

### API Reference

- [ ] **(Critical)** All public modules, classes, and functions are documented
- [ ] **(Critical)** Docstrings follow a consistent style (the project's standard docstring/comment style)
- [ ] **(Critical)** Parameters, return values, and types are documented
- [ ] **(Recommended)** Docstrings include at least one usage example
- [ ] **(Recommended)** Deprecated functions are marked with deprecation warnings
- [ ] **(Recommended)** Cross-references link to related functions and classes
- [ ] **(Recommended)** API documentation is auto-generated from source (autodoc/mkdocstrings)

### Configuration Reference

- [ ] **(Recommended)** All configuration options are documented
- [ ] **(Recommended)** Default values are listed
- [ ] **(Recommended)** Environment variables are documented
- [ ] **(Recommended)** Example configuration files are provided

### CLI Reference (if applicable)

- [ ] **(Critical)** All commands and subcommands are documented
- [ ] **(Critical)** All flags and options have descriptions
- [ ] **(Recommended)** Usage examples for common workflows
- [ ] **(Recommended)** Auto-generated from CLI help text where possible

---

## Developer Documentation

Documentation that contributors need to understand, build, test, and extend the software.

### Architecture Overview

- [ ] **(Recommended)** High-level architecture diagram exists
- [ ] **(Recommended)** Major components and their responsibilities are described
- [ ] **(Recommended)** Data flow between components is documented
- [ ] **(Recommended)** Key design decisions and their rationale are recorded
- [ ] **(Recommended)** External dependencies and their purposes are listed

### Development Environment Setup

- [ ] **(Critical)** Step-by-step development setup instructions exist
- [ ] **(Critical)** Instructions cover cloning, installing dependencies, and running tests
- [ ] **(Recommended)** Instructions cover IDE/editor setup (VS Code, PyCharm)
- [ ] **(Recommended)** Instructions for pre-commit hook installation
- [ ] **(Recommended)** Instructions verified in a clean environment

### Testing Guide

- [ ] **(Critical)** How to run the full test suite
- [ ] **(Critical)** How to run a subset of tests
- [ ] **(Recommended)** How to write new tests (conventions, fixtures, patterns)
- [ ] **(Recommended)** Test organization and naming conventions
- [ ] **(Recommended)** How CI runs tests (matrix, environments)
- [ ] **(Recommended)** Coverage expectations and how to check coverage

### Release Process

- [ ] **(Critical)** Step-by-step release process is documented
- [ ] **(Critical)** Version numbering scheme is documented (semver, calver, etc.)
- [ ] **(Recommended)** Changelog update process is documented
- [ ] **(Recommended)** Release automation (CI/CD) is documented
- [ ] **(Recommended)** Post-release verification steps are listed
- [ ] **(Recommended)** Who has release permissions is documented

### Dependency Management

- [ ] **(Recommended)** How to add, update, and remove dependencies
- [ ] **(Recommended)** Pinning strategy is documented (exact pins, ranges, lock files)
- [ ] **(Recommended)** How to handle security updates
- [ ] **(Recommended)** Optional vs. required dependencies are explained

---

## Project Health

Indicators that the project infrastructure is working and documented.

### CI/CD Pipeline

- [ ] **(Critical)** CI runs on pull requests and passes
- [ ] **(Critical)** CI configuration files exist and are readable
- [ ] **(Recommended)** CI matrix covers supported Python versions and OS
- [ ] **(Recommended)** CI includes linting, type checking, and documentation builds
- [ ] **(Recommended)** CI failure modes are documented (what a red check means)
- [ ] **(Recommended)** Deployment/release pipeline is documented

### Code Quality

- [ ] **(Recommended)** Linter is configured and documented (the project's linter)
- [ ] **(Recommended)** Formatter is configured and documented (the project's formatter)
- [ ] **(Recommended)** Type checker is configured and documented (the project's type checker, if applicable)
- [ ] **(Recommended)** Pre-commit hooks are configured
- [ ] **(Recommended)** Code quality expectations are in CONTRIBUTING.md

### Documentation Build

- [ ] **(Critical)** Documentation builds without errors or warnings
- [ ] **(Critical)** Documentation is deployed and accessible at a public URL
- [ ] **(Recommended)** Documentation builds are part of CI
- [ ] **(Recommended)** Documentation versioning is configured (if multiple versions exist)
- [ ] **(Recommended)** Documentation uses a responsive, accessible theme

---

## Scientific Software Specific

Additional requirements for software used in research contexts.

### Citation

- [ ] **(Scientific)** `CITATION.cff` exists in the repository root
- [ ] **(Scientific)** CITATION.cff is valid (check with `cffconvert --validate`)
- [ ] **(Scientific)** BibTeX citation is provided in documentation
- [ ] **(Scientific)** DOI is registered (Zenodo, etc.)
- [ ] **(Scientific)** ORCID identifiers are included for authors
- [ ] **(Scientific)** Citation instructions are in README and documentation

### Data Access and Formats

- [ ] **(Scientific)** Sample/test data is documented and accessible
- [ ] **(Scientific)** Input data formats are documented with examples
- [ ] **(Scientific)** Output data formats are documented with examples
- [ ] **(Scientific)** Data download instructions are provided (if external data required)
- [ ] **(Scientific)** Data size and storage requirements are documented
- [ ] **(Scientific)** Data licenses are documented

### Reproducibility

- [ ] **(Scientific)** Environment specification is provided (the project's dependency specification files, e.g., requirements.txt, environment.yml, Cargo.lock, package-lock.json)
- [ ] **(Scientific)** Pinned/locked dependency versions are available
- [ ] **(Scientific)** Random seeds are documented for stochastic processes
- [ ] **(Scientific)** Hardware requirements are documented (RAM, GPU, disk)
- [ ] **(Scientific)** Expected runtime for common tasks is documented
- [ ] **(Scientific)** Instructions to reproduce published results are provided

### Methodology

- [ ] **(Scientific)** Algorithms and methods are described or referenced
- [ ] **(Scientific)** Mathematical notation is rendered correctly
- [ ] **(Scientific)** Assumptions and limitations are documented
- [ ] **(Scientific)** Validation against known results is documented
- [ ] **(Scientific)** Units and coordinate systems are documented

---

## Onboarding Documentation

Documentation specifically for new team members or contributors joining the project.

### Getting Started as a Developer

- [ ] **(Recommended)** "Day one" guide for new contributors exists
- [ ] **(Recommended)** Guide covers: clone, install, run tests, make a change, submit PR
- [ ] **(Recommended)** Guide links to deeper documentation for each step
- [ ] **(Recommended)** Common "first issues" or "good first issue" labels are used
- [ ] **(Recommended)** Mentorship or review process for new contributors is described

### Key Contacts and Communication

- [ ] **(Recommended)** Primary maintainers are listed with contact information
- [ ] **(Recommended)** Communication channels are documented (Slack, Discourse, mailing list)
- [ ] **(Recommended)** Meeting schedule and notes location (if applicable)
- [ ] **(Recommended)** Decision-making process is documented
- [ ] **(Recommended)** Governance model is documented (for larger projects)

### Glossary and Context

- [ ] **(Recommended)** Glossary of project-specific terms and abbreviations
- [ ] **(Scientific)** Glossary of domain-specific terminology
- [ ] **(Recommended)** List of acronyms used in the codebase
- [ ] **(Recommended)** Links to background reading or prerequisite knowledge
- [ ] **(Recommended)** Project history and motivation summary

### Known Issues and Technical Debt

- [ ] **(Recommended)** Known issues are documented (or linked to issue tracker)
- [ ] **(Recommended)** Technical debt is catalogued with severity and impact
- [ ] **(Recommended)** Planned deprecations are documented with timelines
- [ ] **(Recommended)** Workarounds for known issues are documented
- [ ] **(Recommended)** Areas of the codebase that need refactoring are identified

### Decision Log

- [ ] **(Recommended)** Major architectural decisions are recorded (ADRs or similar)
- [ ] **(Recommended)** Each decision includes context, decision, and consequences
- [ ] **(Recommended)** Alternatives considered are documented
- [ ] **(Recommended)** Decisions are dated and attributed

---

## Validation Automation

Checks that can be automated in CI to continuously verify documentation quality.

- [ ] Documentation builds without warnings (`sphinx-build -W`)
- [ ] All internal links resolve
- [ ] External links checked on schedule (weekly)
- [ ] Prose passes Vale linting
- [ ] Markdown passes markdownlint checks
- [ ] Code examples in documentation execute successfully (doctest)
- [ ] Jupyter notebooks execute successfully (nbval)
- [ ] API reference coverage matches public API surface
- [ ] No references to deprecated functions or removed features
- [ ] CITATION.cff is valid

---

## Scoring Guide

Use this scoring guide to assess overall documentation readiness:

| Level | Criteria | Suitable For |
|-------|----------|-------------|
| **Minimal** | All **(Critical)** items checked | Internal/prototype projects |
| **Good** | All **(Critical)** + 50% of **(Recommended)** | Open-source release |
| **Excellent** | All **(Critical)** + 80% of **(Recommended)** | Community project handoff |
| **Exemplary** | All items checked including **(Scientific)** | Published research software |

**Tip:** Track your score over time. Aim to move up one level with each release cycle.

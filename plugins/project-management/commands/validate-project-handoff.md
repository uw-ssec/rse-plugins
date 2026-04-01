---
description: Validate project handoff by testing that setup instructions, documentation, and workflows actually work
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# Validate Project Handoff Command

When this command is invoked, actively test that the project's documentation and setup instructions actually work by following them step-by-step. This is the complementary command to `/project-handoff` — while that command checks for the *presence* of documentation, this command tests that the documentation is *correct and functional*.

## Input Handling

**If argument provided** (e.g., `/validate-project-handoff` or `/validate-project-handoff path/to/project`):
- If a path is provided, validate the project at that path
- If no path, validate the current working directory

**If no context:**
- Validate the current working directory
- Detect the repository from git configuration

## Validation Process

### Step 1: Read All Documentation

Read the following files completely:

1. `README.md` — Primary setup and usage instructions
2. `CONTRIBUTING.md` — Development setup instructions
3. `docs/` directory — Any additional documentation
4. Project configuration file (pyproject.toml, Cargo.toml, package.json, etc.) — Dependency specification

Identify all instruction blocks that contain commands a user would run.

### Step 2: Validate Installation Instructions

Trace through the installation instructions documented in README.md:

**For each installation method documented (e.g., pip, conda, pixi, from source):**

1. Read the exact commands listed in the documentation
2. Check if prerequisites are mentioned (Python version, system packages)
3. Verify the package name is correct for the documented install command
4. If "from source" instructions exist, verify they reference the correct repository URL
5. Check that the documented Python version requirement matches `pyproject.toml`

**Record for each method:**
- Commands documented
- Whether commands are syntactically correct
- Whether prerequisites are listed
- Any ambiguities or missing steps

### Step 3: Validate Development Setup Instructions

Trace through the development setup in CONTRIBUTING.md:

1. Read fork/clone instructions
2. Check that the documented environment setup commands reference correct files
3. Verify that dependency installation commands match the project's package manager
4. Check that pre-commit installation is documented (if `.pre-commit-config.yaml` exists)
5. Verify test running commands match the configured test framework

**Check for common issues:**
- References to files that don't exist (e.g., `requirements-dev.txt` when only `pyproject.toml` exists)
- Outdated package manager references (e.g., documents `pip` but project uses `pixi`)
- Missing steps between "clone repo" and "run tests"
- Undocumented system dependencies

### Step 4: Validate Code Examples

If the README or docs contain code examples:

1. Read each code example
2. Check if code examples reference modules, functions, or types that exist in the codebase
3. Verify that example function calls reference functions that exist in the codebase
4. Check that example output (if shown) is plausible

Use `grep` and file reading to verify that referenced modules, classes, and functions exist.

### Step 5: Validate CI Configuration

Check that CI configuration matches the documented development workflow:

1. Read `.github/workflows/*.yml`
2. Verify CI language/runtime versions match the documented requirements
3. Check that CI test commands match the documented test commands
4. Verify that CI uses the same build tools and package managers documented for contributors

### Step 6: Check for Broken Links

Scan documentation files for URLs and verify them:

1. Extract all URLs from README.md, CONTRIBUTING.md, and docs/
2. Categorize: internal links (relative paths), external links (http/https)
3. For internal links, verify the target file exists
4. For external links, note them for manual verification (don't fetch automatically)

### Step 7: Validate CITATION.cff

If `CITATION.cff` exists:

1. Check that it has required fields (cff-version, message, title, authors, type)
2. Verify the version matches the project version
3. Check that the repository-code URL is correct
4. Validate date format (YYYY-MM-DD)

### Step 8: Generate Validation Report

Present the validation results:

```
## Project Handoff Validation Report

**Project:** <project-name>
**Date:** <today>
**Validated by:** AI Assistant

### Overall Status: VALID / ISSUES FOUND / CRITICAL ISSUES

---

### Installation Instructions
| Method | Status | Issues |
|--------|--------|--------|
| pip install | ✅ VALID | Commands are correct |
| From source | ⚠️ ISSUE | Missing step: `pip install -e .` after clone |
| conda | ❌ BROKEN | References `conda-forge` channel but package not published there |

**Details:**
- README line 42: `pip install my-package` — Package name verified on PyPI ✅
- README line 55: Clone instructions reference correct repository URL ✅
- README line 58: Missing `cd my-package` between clone and install ❌

### Development Setup
| Step | Status | Issues |
|------|--------|--------|
| Fork & Clone | ✅ VALID | Clear instructions |
| Create environment | ⚠️ ISSUE | Documents `conda` but project uses `pixi` |
| Install dependencies | ❌ BROKEN | References `requirements-dev.txt` which doesn't exist |
| Run tests | ✅ VALID | `pytest` command matches pyproject.toml config |
| Pre-commit | ⚠️ ISSUE | .pre-commit-config.yaml exists but setup not documented |

**Details:**
- CONTRIBUTING.md line 23: References `requirements-dev.txt` — file not found ❌
- CONTRIBUTING.md line 31: `pytest tests/` — command is correct ✅
- CONTRIBUTING.md line 35: No mention of `pre-commit install` ⚠️

### Code Examples
| Example | Location | Status | Issue |
|---------|----------|--------|-------|
| Basic usage | README:72-85 | ✅ VALID | Imports match package structure |
| Advanced | README:90-110 | ❌ BROKEN | `from mypackage.utils import deprecated_func` — function removed in v0.4 |

### CI Configuration
| Check | Status | Issue |
|-------|--------|-------|
| Python versions match | ⚠️ MISMATCH | CI tests 3.10-3.12, pyproject says >=3.10, docs say 3.11+ |
| Test command matches | ✅ VALID | Both use `pytest` |
| Package manager matches | ❌ MISMATCH | CI uses pixi, CONTRIBUTING documents conda |

### Internal Links
| Link | File | Status |
|------|------|--------|
| `docs/api.md` | README:120 | ❌ BROKEN | File does not exist |
| `CONTRIBUTING.md` | README:130 | ✅ VALID | File exists |
| `LICENSE` | README:135 | ✅ VALID | File exists |

### CITATION.cff
| Field | Status | Issue |
|-------|--------|-------|
| Required fields | ✅ VALID | All present |
| Version match | ⚠️ MISMATCH | CITATION says 0.3.0, pyproject says 0.4.1 |
| Repository URL | ✅ VALID | Matches git remote |

---

### Summary
- **Critical Issues:** <count> — Documentation actively misleads users
- **Issues:** <count> — Documentation is incomplete or inconsistent
- **Valid:** <count> — Documentation is correct and functional

### Priority Fixes
1. [CRITICAL] CONTRIBUTING.md:23 — Replace `requirements-dev.txt` reference with `pip install -e ".[dev]"`
2. [CRITICAL] README:90-110 — Update code example: `deprecated_func` was removed in v0.4
3. [IMPORTANT] CONTRIBUTING.md — Add `pre-commit install` step after environment setup
4. [IMPORTANT] README:55 — Add `cd my-package` step after clone command
5. [IMPORTANT] Sync Python version requirements across README, pyproject.toml, and CI config
6. [IMPORTANT] Update CITATION.cff version to match current release
7. [RECOMMENDED] Remove broken link to `docs/api.md` or create the file
```

## Important Notes

- **Read-only validation**: This command reads and analyzes but does NOT modify any files
- **Be specific**: Every issue must reference the exact file and line number
- **Trace instructions literally**: Follow documentation as a new user would — don't fill in gaps with assumptions
- **Distinguish severity**: "Actively misleading" (CRITICAL) vs "missing information" (IMPORTANT) vs "could be better" (RECOMMENDED)
- **Complement `/project-handoff`**: That command checks presence; this command checks correctness
- **Use the `documentation-validation` skill** for recommendations on automated validation tooling
- **Suggest fixes**: For each issue found, suggest the specific correction

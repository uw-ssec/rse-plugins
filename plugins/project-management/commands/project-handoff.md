---
description: Assess project readiness for handoff to new maintainers with a comprehensive health check
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# Project Handoff Command

When this command is invoked, perform a comprehensive project health assessment to determine if the project is ready for handoff to new maintainers. Generate a detailed readiness report with pass/fail/warning for each criterion.

## Input Handling

**If argument provided** (e.g., `/project-handoff` or `/project-handoff path/to/project`):
- If a path is provided, assess the project at that path
- If no path, assess the current working directory

**If run without context:**
- Assess the current working directory as the project root
- Detect the repository from git configuration

## Handoff Assessment Process

### Step 1: Community Health Files Check

Check for the presence and completeness of standard community health files:

| File | Status | Criteria |
|------|--------|----------|
| README.md | Required | Must exist, >50 lines, has installation and usage sections |
| LICENSE | Required | Must exist, recognized license text |
| CONTRIBUTING.md | Required | Must exist, has development setup instructions |
| CODE_OF_CONDUCT.md | Recommended | Should exist for community projects |
| SECURITY.md | Recommended | Should exist with reporting instructions |
| CHANGELOG.md | Recommended | Should exist, has recent entries |
| CITATION.cff | Recommended | Should exist for academic/research projects |

For each file:
- **PASS**: File exists and meets criteria
- **WARN**: File exists but is incomplete or minimal
- **FAIL**: File is missing

### Step 2: Documentation Quality Check

Assess documentation completeness:

- **Installation instructions**: Do they exist in README or dedicated docs?
- **Quickstart / Usage**: Is there a getting-started guide?
- **API Reference**: Is there auto-generated or hand-written API documentation?
- **Development setup**: Can a new developer set up their environment from docs?
- **Testing guide**: Are testing instructions documented?
- **Architecture overview**: Is there a high-level description of the codebase?

Read the README and CONTRIBUTING files to verify these sections exist.

### Step 3: CI/CD Status Check

Use `gh` to check CI/CD health:

```bash
# Check for workflow files
ls .github/workflows/*.yml 2>/dev/null

# Check recent CI runs on default branch
gh run list --branch main --limit 5 --json conclusion,name,createdAt

# Check if branch protection is configured
gh api repos/{owner}/{repo}/branches/main/protection 2>/dev/null
```

Assess:
- **CI workflows exist**: Are there GitHub Actions workflow files?
- **CI is passing**: Did the most recent run on the default branch succeed?
- **Branch protection**: Is the default branch protected?

### Step 4: Test Suite Assessment

Check the test suite:

```bash
# Check for test files (look for common test directory patterns)
ls tests/ test/ spec/ 2>/dev/null

# Check for test framework configuration in project config files
# (e.g., pyproject.toml, package.json, Cargo.toml, Makefile, etc.)

# Check recent test coverage (if available)
```

Assess:
- **Tests exist**: Are there test files?
- **Test framework configured**: Is the project's test framework configured?
- **Coverage reporting**: Is coverage measurement set up?

### Step 5: Dependency and Security Check

```bash
# Check for dependency specification files
# (pyproject.toml, Cargo.toml, package.json, go.mod, DESCRIPTION, etc.)
ls pyproject.toml Cargo.toml package.json go.mod DESCRIPTION pixi.toml environment.yml requirements.txt 2>/dev/null

# Check for Dependabot or Renovate configuration
ls .github/dependabot.yml .renovaterc.json 2>/dev/null

# Check for security alerts (if accessible)
gh api repos/{owner}/{repo}/vulnerability-alerts 2>/dev/null
```

Assess:
- **Dependencies specified**: Are dependencies locked/pinned?
- **Automated updates**: Is Dependabot or Renovate configured?
- **Security alerts**: Are there open security vulnerabilities?

### Step 6: Project Activity and Open Work

```bash
# Check for open issues
gh issue list --state open --json number,title,labels --limit 50

# Check for open PRs
gh pr list --state open --json number,title,labels --limit 20

# Check for stale branches
git branch -r --sort=-committerdate | head -20

# Check last commit date
git log -1 --format=%ci
```

Assess:
- **Open issues triaged**: Are open issues labeled and organized?
- **Open PRs addressed**: Are there stale PRs that need resolution?
- **Stale branches**: Are there experimental branches that should be cleaned up?
- **Recent activity**: When was the last commit?

### Step 7: Generate Handoff Readiness Report

Present the assessment as a structured report:

```
## Project Handoff Readiness Report

**Project:** <project-name>
**Date:** <today>
**Assessed by:** AI Assistant

### Overall Status: READY / NEEDS WORK / NOT READY

---

### Community Health Files
| File | Status | Notes |
|------|--------|-------|
| README.md | ✅ PASS | 120 lines, has installation and usage |
| LICENSE | ✅ PASS | BSD-3-Clause |
| CONTRIBUTING.md | ⚠️ WARN | Exists but missing development setup |
| CODE_OF_CONDUCT.md | ✅ PASS | Contributor Covenant v2.1 |
| SECURITY.md | ❌ FAIL | Missing |
| CHANGELOG.md | ⚠️ WARN | Exists but no entries since v0.3.0 |
| CITATION.cff | ❌ FAIL | Missing (recommended for research software) |

### Documentation
| Area | Status | Notes |
|------|--------|-------|
| Installation | ✅ PASS | Clear pip install instructions in README |
| Usage / Quickstart | ⚠️ WARN | Basic example but no tutorial |
| API Reference | ❌ FAIL | No API documentation found |
| Development Setup | ❌ FAIL | CONTRIBUTING.md lacks setup instructions |
| Testing Guide | ✅ PASS | Documented in CONTRIBUTING.md |
| Architecture Overview | ❌ FAIL | No architecture documentation |

### CI/CD
| Check | Status | Notes |
|-------|--------|-------|
| Workflows exist | ✅ PASS | ci.yml, docs.yml |
| CI passing | ✅ PASS | Last 5 runs all passed |
| Branch protection | ⚠️ WARN | Not configured |

### Test Suite
| Check | Status | Notes |
|-------|--------|-------|
| Tests exist | ✅ PASS | 42 test files found |
| Framework configured | ✅ PASS | pytest in pyproject.toml |
| Coverage reporting | ⚠️ WARN | Not configured |

### Dependencies & Security
| Check | Status | Notes |
|-------|--------|-------|
| Dependencies specified | ✅ PASS | pyproject.toml with pinned deps |
| Automated updates | ❌ FAIL | No Dependabot configuration |
| Security alerts | ⚠️ WARN | 2 moderate alerts |

### Project Activity
| Check | Status | Notes |
|-------|--------|-------|
| Open issues triaged | ⚠️ WARN | 15 open, 8 unlabeled |
| Open PRs addressed | ✅ PASS | 2 open, both recent |
| Stale branches | ⚠️ WARN | 5 branches >6 months old |

---

### Summary
- **Critical Issues (FAIL):** <count> — Must fix before handoff
- **Warnings (WARN):** <count> — Should fix before handoff
- **Passing (PASS):** <count>

### Priority Actions Before Handoff
1. [CRITICAL] Create SECURITY.md with vulnerability reporting instructions
2. [CRITICAL] Add development setup instructions to CONTRIBUTING.md
3. [CRITICAL] Generate API documentation
4. [IMPORTANT] Create CITATION.cff for academic attribution
5. [IMPORTANT] Configure Dependabot for automated dependency updates
6. [IMPORTANT] Triage and label all open issues
7. [RECOMMENDED] Set up branch protection on default branch
8. [RECOMMENDED] Add coverage reporting to CI
9. [RECOMMENDED] Clean up stale branches
10. [RECOMMENDED] Update CHANGELOG.md with recent changes
```

## Important Notes

- **Read-only assessment**: This command only checks and reports — it does not modify any files
- **Use `/validate-project-handoff`** for the complementary step of actually testing that setup instructions work
- **Use `/setup-project`** or the `project-onboarding-specialist` agent to fix identified gaps
- **Be specific**: Every FAIL and WARN should include what's missing and what to do about it
- **Consider the audience**: New maintainers need to understand the project quickly — gaps in documentation are critical
- **Reference the `documentation-validation` skill** for validation tool recommendations

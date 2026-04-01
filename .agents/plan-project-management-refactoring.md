# Implementation Plan: Refocus project-management Plugin on Project Lifecycle (Issue #60)

---
**Date:** 2026-02-26
**Author:** AI Assistant
**Status:** Draft
**Related Documents:**
- [Research: Project Management Plugin](research-project-management-plugin.md)
- [Issue #58 — Containerization Plugin](https://github.com/uw-ssec/rse-plugins/issues/58)
- [Issue #59 — GitHub Plugin](https://github.com/uw-ssec/rse-plugins/issues/59)
- [Issue #60 — Project Management Refactoring](https://github.com/uw-ssec/rse-plugins/issues/60)

---

## Overview

This plan refactors the `project-management` plugin from a monolithic plugin covering GitHub platform mechanics, containerization/DevOps, and project lifecycle into a focused **project lifecycle management** plugin. The refactoring removes content that has already been moved to the new containerization plugin (#58) and GitHub plugin (#59), then generalizes the remaining content from "scientific Python" to language-agnostic "research software" framing.

The plugin currently contains 8 skills, 5 agents, and 7 commands. After refactoring, it retains 2 skills, 2 agents, and 3 commands — all focused on project onboarding, documentation quality, handoff readiness, and community health.

**Goal:** A focused, language-agnostic project-management plugin that handles the human and organizational concerns of running an open-source research software project — scaffolding community health files, validating documentation, and assessing handoff readiness.

**Motivation:** The monolithic plugin mixes three orthogonal concerns. Extracting GitHub and containerization content into dedicated plugins (#58, #59) creates three focused, independently installable plugins. This issue (#60) cleans up what remains.

## Current State Analysis

**Existing Implementation:**
- `plugins/project-management/.claude-plugin/plugin.json:1-9` — Describes plugin as "GitHub-based open-source scientific Python project management, CI/CD, and DevOps"
- `plugins/project-management/README.md:1-67` — Documents all 8 skills, 5 agents, 7 commands
- `plugins/project-management/agents/` — 5 agent files (3 move out, 2 stay)
- `plugins/project-management/skills/` — 8 skill directories (6 move out, 2 stay)
- `plugins/project-management/commands/` — 7 command files (4 move out, 3 stay)
- `.claude-plugin/marketplace.json:91-113` — Marketplace entry with GitHub/CI/CD/DevOps keywords

**Current Behavior:**
The plugin serves three distinct audiences: users needing GitHub CI/CD setup, users needing containerization, and users needing project lifecycle management (onboarding, handoff, docs). All content is scoped to "scientific Python" projects.

**Current Limitations:**
- Mixes three unrelated concerns in one plugin
- Python-specific language in all components excludes R, Julia, Rust, Go, and multi-language projects
- Plugin is too large to install if you only need one concern

## Desired End State

**New Behavior:**
The plugin focuses exclusively on project lifecycle: scaffolding community health files for any language, validating documentation quality, assessing handoff readiness, and testing setup instructions. It recommends (but does not require) the GitHub and containerization plugins for CI/CD and container setup.

**Success Looks Like:**
- Plugin contains exactly 2 agents, 2 skills, 3 commands — no leftover moved content
- No file in the plugin contains "scientific Python" as a scope limitation
- The `setup-project` command scaffolds community health files for any project in any language
- The `project-handoff` and `validate-project-handoff` commands work on any repository
- The plugin functions standalone without requiring the GitHub or containerization plugins
- The README clearly communicates the focused scope and points to related plugins

## What We're NOT Doing

- [ ] Building the containerization plugin (#58) — separate issue, Phase 1
- [ ] Building the GitHub plugin (#59) — separate issue, Phase 2
- [ ] Renaming the plugin from "project-management" — would break marketplace, installations, and documentation
- [ ] Adding new capabilities or features — this is strictly removal + generalization
- [ ] Creating a plugin dependency mechanism in plugin.json — out of scope
- [ ] Generating language-specific project config files (pyproject.toml, Cargo.toml, etc.) in setup-project — delegated to user tooling
- [ ] Modifying other plugins (scientific-python-development, scientific-domain-applications, ai-research-workflows)
- [ ] Changing the plugin validation workflow

**Rationale:** This is a scoping and generalization refactoring, not a feature addition. Content that moves out is handled by their respective issues. New capabilities belong in future issues.

## Implementation Approach

**Technical Strategy:**
Execute in 5 sequential phases: remove moved content, generalize agents, generalize skills, generalize commands, update identity. Each phase is independently verifiable. The ordering ensures we remove content before generalizing, preventing wasted effort on files that will be deleted.

**Key Architectural Decisions:**

1. **Decision:** Keep `community-health-files` in project-management (not duplicated to GitHub plugin)
   - **Rationale:** Community health files are a project lifecycle concern (onboarding, handoff readiness). The template *content* (what goes in README, CONTRIBUTING, etc.) belongs here. The GitHub plugin owns the *platform mechanics* (`.github` repo pattern, org-level defaults, community profile API).
   - **Trade-offs:** Some overlap since community health files are a GitHub feature, but template content is universal.

2. **Decision:** `setup-project` asks the user for project type instead of auto-detecting language
   - **Rationale:** The command's core responsibility is community health file scaffolding, which is language-agnostic. Language-specific project config (pyproject.toml, Cargo.toml, package.json) is out of scope — the command delegates to user tooling or other plugins.
   - **Trade-offs:** Less "magic" than auto-detection, but more reliable and explicitly language-agnostic.

3. **Decision:** `project-handoff` and `validate-project-handoff` still check CI/CD presence
   - **Rationale:** CI/CD existence is a project health indicator. The check is read-only (look for `.github/workflows/`, run `gh run list`) and doesn't require the GitHub plugin to generate anything.
   - **Trade-offs:** Creates a soft conceptual dependency on CI/CD being present, but this is a health check, not a generation task.

4. **Decision:** Replace "scientific Python" with "research software" (not fully generic)
   - **Rationale:** The plugin serves RSE organizations. "Research software" is broader than "scientific Python" while retaining the RSE focus. "Any software project" would dilute the value proposition.
   - **Trade-offs:** Still somewhat niche, but accurately reflects the target audience.

5. **Decision:** Keep plugin name as "project-management"
   - **Rationale:** Renaming has ecosystem-wide implications (marketplace, cached installations, user documentation). The new description communicates the narrowed scope.
   - **Trade-offs:** Name is broader than scope, but less disruptive than renaming.

**Patterns to Follow:**
- Agent frontmatter format — See `plugins/project-management/agents/project-onboarding-specialist.md:1-48`
- Skill SKILL.md format — See `plugins/project-management/skills/community-health-files/SKILL.md:1-8`
- Command frontmatter format — See `plugins/project-management/commands/project-handoff.md:1-3`

## Implementation Phases

### Phase 1: Remove Moved Content

**Objective:** Delete all skills, agents, and commands that have been moved to the containerization (#58) and GitHub (#59) plugins. After this phase, only the retained content remains.

**Prerequisites:** Issues #58 and #59 must be completed first, with their content live in their respective new plugins. This is a hard requirement from the issue ordering (Phase 1: #58, Phase 2: #59, Phase 3: #60).

**Tasks:**

- [x] Delete agent: `plugins/project-management/agents/devops-engineer.md`
  - Moved to containerization plugin (#58)

- [x] Delete agent: `plugins/project-management/agents/github-workflow-specialist.md`
  - Moved to GitHub plugin (#59)

- [x] Delete agent: `plugins/project-management/agents/github-org-manager.md`
  - Moved to GitHub plugin (#59)

- [x] Delete skill directory: `plugins/project-management/skills/containerization/`
  - Contains: `SKILL.md`, `assets/Dockerfile-conda-template`, `assets/Dockerfile-pixi-template`
  - Moved to containerization plugin (#58)

- [x] Delete skill directory: `plugins/project-management/skills/github-actions/`
  - Contains: `SKILL.md`, `assets/ci-docs-workflow.yml`, `assets/ci-publish-workflow.yml`, `assets/ci-test-workflow.yml`
  - Moved to GitHub plugin (#59)

- [x] Delete skill directory: `plugins/project-management/skills/release-management/`
  - Contains: `SKILL.md`, `assets/pyproject-release-config.toml`, `assets/release-checklist.md`
  - Moved to GitHub plugin (#59)

- [x] Delete skill directory: `plugins/project-management/skills/github-org-management/`
  - Contains: `SKILL.md`, `references/health-metrics.md`
  - Moved to GitHub plugin (#59)

- [x] Delete skill directory: `plugins/project-management/skills/issue-triage/`
  - Contains: `SKILL.md`, `assets/bug-report-template.md`, `assets/feature-request-template.md`
  - Moved to GitHub plugin (#59)

- [x] Delete skill directory: `plugins/project-management/skills/pre-commit-workflows/`
  - Contains: `SKILL.md`, `assets/pre-commit-config-template.yaml`
  - Moved to GitHub plugin (#59)

- [x] Delete command: `plugins/project-management/commands/ci-setup.md`
  - Moved to GitHub plugin (#59)

- [x] Delete command: `plugins/project-management/commands/audit-github-org.md`
  - Moved to GitHub plugin (#59)

- [x] Delete command: `plugins/project-management/commands/release-plan.md`
  - Moved to GitHub plugin (#59)

- [x] Delete command: `plugins/project-management/commands/triage.md`
  - Moved to GitHub plugin (#59)

**Verification:**
- [x] Only these files/directories remain in `plugins/project-management/`:
  ```
  .claude-plugin/plugin.json
  README.md
  LICENSE
  agents/project-onboarding-specialist.md
  agents/documentation-validator.md
  skills/community-health-files/ (SKILL.md + 5 asset templates)
  skills/documentation-validation/ (SKILL.md + 2 assets)
  commands/setup-project.md
  commands/project-handoff.md
  commands/validate-project-handoff.md
  ```
- [x] No dangling symlinks or empty directories

### Phase 2: Generalize Remaining Agents

**Objective:** Update the two remaining agents to remove "scientific Python" scoping and make them language-agnostic for any research software project.

**Tasks:**

- [x] Generalize `plugins/project-management/agents/project-onboarding-specialist.md`
  - **Frontmatter description (line 4):** Change "scientific Python project initialization" → "research software project initialization"
  - **Example 1 (line 10):** Change "set up a new Python package for our climate data analysis library" → "set up a new project for our climate data analysis library" (remove Python-specific framing)
  - **Example 4 (line 38):** Change "tailored to your scientific Python project" → "tailored to your research software project"
  - **Body line 50:** Change "scientific Python project initialization" → "research software project initialization"
  - **Body line 54:** Change "from initial scaffolding with community health files and CI/CD" → "from initial scaffolding with community health files" (remove CI/CD — that's the GitHub plugin's job now)
  - **Body line 59:** Change "scientific Python conventions (src layout)" → "project conventions appropriate for the language/framework"
  - **Body line 62:** Remove "Configure initial CI/CD with GitHub Actions" (moved to GitHub plugin)
  - **Body line 63:** Remove "Create .pre-commit-config.yaml with essential hooks" (moved to GitHub plugin)
  - **Body line 64:** Change "Initialize pixi.toml or pyproject.toml with standard configuration" → "Recommend appropriate project configuration tooling for the detected language"
  - **Body line 93:** Change "Always use BSD-3-Clause license for SSEC/UW projects" → "Default to BSD-3-Clause for research software projects" (keep as default but not organization-specific)
  - **Key Preferences section (lines 117-120):** Change "src layout for Python packages (recommended by Scientific Python)" → "Recommended project layout for the detected language/framework"
  - **Key Preferences section (line 133):** Change "reference community standards for scientific Python" → "reference community standards for the relevant ecosystem"
  - **Add delegation note** in Workflow Patterns: After scaffolding community files, suggest the GitHub plugin for CI/CD and the containerization plugin for Dockerfiles
  - **Skills list stays as-is** — `community-health-files` and `documentation-validation` both stay

- [x] Generalize `plugins/project-management/agents/documentation-validator.md`
  - **Frontmatter description (line 4):** Change "for scientific Python projects" → "for research software projects"
  - **Body line 41:** Change "for scientific Python projects" → "for research software projects"
  - **Body line 46:** Change "scientific software projects" → "research software projects"
  - **Validation Tools section (line 114):** Keep nbval/notebook testing but add a note: "nbval is specific to Python/Jupyter; for other ecosystems, validate documentation examples using language-appropriate test frameworks"
  - **Add language-agnostic alternatives** after line 114: Mention `cargo test --doc` for Rust, `testthat` for R, `doctest` for Python, `go test` examples for Go
  - **Skills list stays as-is** — `documentation-validation` and `community-health-files` both stay

**Verification:**
- [x] `grep -r "scientific Python" plugins/project-management/agents/` returns no results
- [x] Both agents still reference only `community-health-files` and `documentation-validation` skills
- [x] Agent descriptions make sense for a user working on an R package, a Rust library, or a multi-language project

### Phase 3: Generalize Remaining Skills and Assets

**Objective:** Update the two remaining skills and their template assets to remove Python-specific scoping and support any language.

**Tasks:**

- [x] Generalize `plugins/project-management/skills/community-health-files/SKILL.md`
  - **Title (line 6):** Change "Community Health Files for Scientific Software Projects" → "Community Health Files for Research Software Projects"
  - **Opening paragraph (line 8):** Change "for open-source scientific Python projects" → "for open-source research software projects"
  - **When to Use section (line 52):** Change "Setting up a new open-source scientific Python project from scratch" → "Setting up a new open-source research software project from scratch"
  - **License section (lines 94-110):** Keep BSD-3-Clause recommendation but remove "Scientific Python ecosystem" framing. Change to "research software ecosystem" and add examples from other language communities (Apache-2.0 used by many Rust/Go projects, MIT common in Node.js)
  - **License section (line 109):** Change "Use SPDX identifiers in `pyproject.toml`" → "Use SPDX identifiers in your project configuration (pyproject.toml, Cargo.toml, package.json, etc.)"
  - **Bug report template (lines 423-428):** Change the placeholder code block from Python-specific to language-neutral:
    ```
    ```
    # Code that triggers the bug
    ```
    ```
  - **Bug report environment section (lines 448-453):** Remove "Python version" and "Installation method: [pip, conda, source]" — replace with language-neutral: "Language/runtime version", "Installation method"
  - **Best practices section (line 549):** Change "Scientific Software Projects" to "Research Software Projects"
  - **Reproducibility section (line 567):** Change "Provide environment files (requirements.txt, environment.yml, pixi.toml)" → "Provide environment specification files appropriate for your language (requirements.txt, environment.yml, Cargo.lock, package-lock.json, etc.)"
  - **File Templates section (lines 590-596):** Change "for scientific Python projects" → "for research software projects"
  - **Add a note** in the .github Organization-Level Defaults section (line 279): "The GitHub plugin provides deeper guidance on organization-level defaults and platform mechanics."

- [x] Generalize `plugins/project-management/skills/community-health-files/assets/README-template.md`
  - **Line 7-9:** Remove PyPI-specific badges. Replace with language-neutral badge placeholders:
    ```
    [![Package version](PACKAGE_BADGE_URL)](PACKAGE_URL)
    ```
  - **Line 19:** Change "is a Python library for" → "is a [language] library/tool for"
  - **Installation section (lines 33-51):** Replace Python-specific methods with language-neutral structure:
    ```
    ### Install (recommended method)
    <!-- Replace with your package manager's install command -->

    ### From source (for development)
    ```
  - **Requirements section (lines 53-58):** Change Python/NumPy/SciPy → generic "Runtime version >= X.Y" and "See [project config file] for full dependency list"
  - **Quick Start section (lines 66-77):** Replace Python import example with a language-neutral placeholder and a comment telling the user to add their own
  - **Citation BibTeX (lines 116-124):** Already mostly language-neutral — keep as-is

- [x] Generalize `plugins/project-management/skills/community-health-files/assets/CONTRIBUTING-template.md`
  - **Prerequisites section (lines 86-88):** Change "Python >= 3.10" → "[Language/Runtime] >= [version]"
  - **Development Setup section (lines 108-137):** Replace Python-specific steps with language-neutral structure:
    - Keep fork/clone/upstream steps (universal)
    - Replace "Create a virtual environment" + "pip install" with generic: "Install dependencies using your project's package manager" and show examples for multiple ecosystems (pip, npm, cargo, etc.) as comments
    - Keep pre-commit install step (universal)
    - Change "pytest" → "Run tests using the project's test framework"
  - **Code Style section (lines 183-255):** Replace Python-specific section (PEP 8, ruff, mypy, NumPy docstrings) with a language-neutral structure:
    - "This project uses automated formatting and linting. See the project configuration for specific tools."
    - Keep the pre-commit guidance (universal)
    - Remove the Python docstring example
  - **Testing section (lines 258-335):** Replace pytest-specific commands and examples with language-neutral structure:
    - "See the project's test configuration for how to run tests"
    - Keep the general testing philosophy (test naming, coverage, fixtures)
    - Remove Python-specific test example
  - **Documentation section (lines 337-359):** Change "pip install -e '.[docs]'" → generic build instruction
  - **Release Process section (lines 399-405):** Change "CI automatically builds and publishes to PyPI" → "CI automatically builds and publishes the release"
  - **Environment section (lines 61-66):** Change "Python version" and "pip list" → language-neutral version and dependency listing

- [x] Review `plugins/project-management/skills/community-health-files/assets/CITATION-template.cff`
  - Already language-agnostic — no changes expected. Verify and confirm.

- [x] Review `plugins/project-management/skills/community-health-files/assets/CODE_OF_CONDUCT-template.md`
  - Already language-agnostic — no changes expected. Verify and confirm.

- [x] Review `plugins/project-management/skills/community-health-files/assets/SECURITY-template.md`
  - Already language-agnostic — no changes expected. Verify and confirm.

- [x] Generalize `plugins/project-management/skills/documentation-validation/SKILL.md`
  - **Opening paragraph (line 8):** Change "scientific software projects where incorrect setup instructions" → "research software projects where incorrect setup instructions"
  - **Notebook Testing section (lines 503-558):** Keep the content but frame it as one option among many. Add a note: "For non-Python projects, validate documentation examples using language-appropriate test frameworks (cargo test --doc for Rust, go test for Go, testthat for R)"
  - **Container-Based Instruction Testing section (lines 571-602):** Change the Dockerfile from Python-specific (`FROM python:3.12-slim`, `pip install`) to a language-neutral template with comments showing how to adapt for any language
  - **GitHub Actions section (lines 696-798):** The CI workflow examples use `pip install`, `sphinx-build`, `pytest` — add a note that these are Python examples and should be adapted for the project's language
  - **Nox Sessions section (lines 1006-1055):** Keep but note these are Python-specific examples. Don't remove — they're useful for Python users — but frame as "Python example"
  - **Scientific Python Resources section (line 1087):** Change heading to "Language-Specific Documentation Resources" and add resources for other ecosystems

- [x] Review `plugins/project-management/skills/documentation-validation/assets/validation-checklist.md`
  - **Line 55:** Change "pip, conda, pixi" → "the project's package manager"
  - **Line 63:** Change "Python version" → "Language/runtime version"
  - **Line 91:** Change "NumPy-style" → "the project's standard docstring/comment style"
  - **Line 175:** Change "ruff, flake8" → "the project's linter"
  - **Line 176:** Change "ruff format, black" → "the project's formatter"
  - **Line 177:** Change "mypy, pyright" → "the project's type checker (if applicable)"
  - **Line 215:** Change "requirements.txt, environment.yml, pixi.toml" → language-neutral list
  - Otherwise the checklist is already well-structured and mostly language-agnostic

- [x] Review `plugins/project-management/skills/documentation-validation/assets/vale-config.ini`
  - Already language-agnostic (Vale lints prose, not code) — no changes expected. Verify and confirm.

**Verification:**
- [x] `grep -r "scientific Python" plugins/project-management/skills/` returns no results
- [x] All templates work conceptually for a Rust, R, Go, or Julia project (read through and verify)
- [x] No Python-specific tools are presented as the only option — always framed with alternatives

### Phase 4: Generalize Remaining Commands

**Objective:** Rewrite `setup-project` for language-agnostic scaffolding with delegation, and make minor updates to the handoff commands.

**Tasks:**

- [x] Rewrite `plugins/project-management/commands/setup-project.md`
  - **Frontmatter description (line 2):** Change "Scaffold a new scientific Python project with community health files, CI/CD, and standard structure" → "Scaffold a new project with community health files and standard structure for any language"
  - **Title (line 5):** Change "scientific Python project" → "project"
  - **No-argument prompt (lines 17-29):** Replace the Python-specific prompt:
    ```
    What is the name of your new project?

    I'll create a project with:
    - Community health files (README, CONTRIBUTING, LICENSE, CODE_OF_CONDUCT, SECURITY, CITATION.cff)
    - Issue and PR templates
    - .gitignore for your language

    Optionally:
    - Set up CI/CD (requires the GitHub plugin)
    - Add a Dockerfile (requires the containerization plugin)

    Please provide a project name (kebab-case recommended, e.g., `climate-analysis-tool`).
    ```
  - **Information Gathering (lines 34-42):** Replace Python-specific questions:
    1. **Brief project description** (one sentence) — keep
    2. **License** — keep (BSD-3-Clause default is good for research software)
    3. ~~**Python version range**~~ → **Primary language** (Python, R, Julia, Rust, Go, Node.js, C/C++, Other)
    4. **Author/organization name** — keep
    5. ~~**Package manager**~~ → Remove (language-specific, not our concern)
  - **Step 1: Create Directory Structure (lines 48-76):** Replace Python src layout with language-neutral structure:
    ```
    <project-name>/
    ├── .github/
    │   ├── ISSUE_TEMPLATE/
    │   │   ├── bug_report.yml
    │   │   └── feature_request.yml
    │   └── PULL_REQUEST_TEMPLATE.md
    ├── README.md
    ├── CONTRIBUTING.md
    ├── LICENSE
    ├── CODE_OF_CONDUCT.md
    ├── SECURITY.md
    ├── CITATION.cff
    └── .gitignore
    ```
    Note: Language-specific directories (src/, tests/, docs/) and config files (pyproject.toml, Cargo.toml, etc.) are the user's responsibility or handled by language-specific tooling.
  - **Step 2: Generate Community Health Files (lines 82-89):** Keep — already references the skill correctly. Remove the "detected package manager" customization note.
  - **Step 3: Generate Issue and PR Templates (lines 92-95):** Keep — already language-agnostic at the structural level. Update the bug report template placeholder code block to be language-neutral.
  - **Step 4: Generate pyproject.toml (lines 98-135):** Remove entirely. This is Python-specific. Replace with a note:
    ```
    ### Step 4: Language-Specific Configuration (User Responsibility)

    The project scaffold includes community health files and GitHub templates. Language-specific
    project configuration should be created using the appropriate tooling:

    - **Python:** `pip install hatch && hatch new` or configure `pyproject.toml` manually
    - **Rust:** `cargo init`
    - **Node.js:** `npm init`
    - **R:** `usethis::create_package()`
    - **Go:** `go mod init`
    - **Julia:** `Pkg.generate()`

    This command focuses on the universal project infrastructure that every project needs
    regardless of language.
    ```
  - **Step 5: Generate CI Workflow (lines 138-144):** Remove. Replace with delegation:
    ```
    ### Step 5: CI/CD Setup (Optional — Requires GitHub Plugin)

    If you have the GitHub plugin installed, run `/ci-setup` to generate
    GitHub Actions CI/CD workflows tailored to your project's language and tooling.
    ```
  - **Step 6: Generate Pre-commit Configuration (lines 147-153):** Remove. Replace with delegation:
    ```
    ### Step 6: Pre-commit Hooks (Optional — Requires GitHub Plugin)

    If you have the GitHub plugin installed, it can configure pre-commit hooks
    appropriate for your project's language.
    ```
  - **Step 7: Generate .gitignore (lines 155-166):** Keep but generalize. Instead of a Python-specific .gitignore, generate one based on the detected language (use gitignore.io patterns or language-standard ignores). Include universal entries (.DS_Store, Thumbs.db, .env, *.log).
  - **Output Summary (lines 169-203):** Update to reflect the new, smaller set of generated files. Remove references to pyproject.toml, .pre-commit-config.yaml, ci.yml, and src/ directory. Add notes about optional next steps (GitHub plugin for CI, containerization plugin for Docker).
  - **Important Notes (lines 206-210):** Keep all. Add: "This command scaffolds universal project infrastructure. Language-specific tooling is the user's responsibility."

- [x] Update `plugins/project-management/commands/project-handoff.md`
  - **Frontmatter (line 2):** Already language-agnostic ("Assess project readiness for handoff to new maintainers") — no change needed
  - **Step 4: Test Suite Assessment (lines 76-91):** Change Python-specific checks:
    - Line 79: Change `find tests/ -name "test_*.py"` → "Check for test files (test directory, language-appropriate test file patterns)"
    - Line 83: Change `grep -l "pytest" pyproject.toml setup.cfg tox.ini noxfile.py` → "Check for test framework configuration in project config files"
  - **Step 5: Dependency and Security Check (lines 94-103):** Change Python-specific file checks:
    - Line 96: Change `ls pyproject.toml pixi.toml environment.yml requirements.txt` → "Check for dependency specification files (pyproject.toml, Cargo.toml, package.json, go.mod, etc.)"
  - Otherwise the command's methodology is already language-agnostic — keep the structure

- [x] Update `plugins/project-management/commands/validate-project-handoff.md`
  - **Frontmatter (line 2):** Already language-agnostic — no change needed
  - **Step 2: Validate Installation Instructions (lines 34-48):** Already framed as "for each installation method documented" — keep. The approach of tracing documented instructions is inherently language-agnostic.
  - **Step 4: Validate Code Examples (lines 68-75):** Change "Check if the imported module names match the actual package structure" → "Check if code examples reference modules/functions/types that exist in the codebase"
  - **Step 5: Validate CI Configuration (lines 79-84):** Change "Verify CI Python versions match the documented `requires-python`" → "Verify CI language/runtime versions match the documented requirements"
  - Otherwise the command is already a language-agnostic methodology — minimal changes

**Verification:**
- [x] `grep -r "scientific Python" plugins/project-management/commands/` returns no results
- [x] `setup-project` command no longer generates any language-specific files (pyproject.toml, .pre-commit-config.yaml, ci.yml)
- [x] `setup-project` command generates only universal files (README, CONTRIBUTING, LICENSE, etc.)
- [x] `project-handoff` and `validate-project-handoff` commands work conceptually on a non-Python repository

### Phase 5: Update Plugin Identity

**Objective:** Update the plugin manifest, README, and marketplace entry to reflect the refocused scope.

**Tasks:**

- [x] Update `plugins/project-management/.claude-plugin/plugin.json`
  - Change `description` from:
    ```
    "Agents, skills, and commands for GitHub-based open-source scientific Python project management, CI/CD, and DevOps"
    ```
    to:
    ```
    "Project lifecycle management — onboarding, documentation quality, handoff readiness, and community health for research software projects"
    ```
  - Keep `name`, `version`, and `author` unchanged

- [x] Rewrite `plugins/project-management/README.md`
  - New content structure:
    ```markdown
    # Project Management Plugin

    Project lifecycle management — onboarding, documentation quality, handoff
    readiness, and community health for research software projects in any language.

    ## Purpose

    This plugin handles the human and organizational concerns of running an
    open-source research software project. It answers: "Is this project
    well-documented? Can a new contributor get started? Is it ready for handoff?
    Does it have the right community files?"

    It does NOT handle GitHub platform mechanics (CI/CD, Actions, releases,
    org management) or containerization — those are separate plugins.

    ## Prerequisites

    - **Git**: For repository operations
    - **GitHub CLI (`gh`)** (optional): Enhanced handoff assessment with CI/CD
      status and issue/PR checks

    ## Agents

    | Agent | Description |
    |-------|-------------|
    | **Project Onboarding Specialist** | Expert in project initialization,
    contributor onboarding, and knowledge transfer for research software |
    | **Documentation Validator** | Expert in documentation quality assurance,
    setup instruction validation, and completeness checking |

    ## Skills

    | Skill | Description |
    |-------|-------------|
    | **community-health-files** | Templates and guidance for README,
    CONTRIBUTING, LICENSE, CODE_OF_CONDUCT, SECURITY, CITATION.cff, and
    issue/PR templates |
    | **documentation-validation** | Validation tools (Vale, markdownlint,
    HTMLProofer) and documentation quality metrics |

    ## Commands

    | Command | Description |
    |---------|-------------|
    | `/setup-project` | Scaffold a new project with community health files |
    | `/project-handoff` | Assess project readiness for handoff to new
    maintainers |
    | `/validate-project-handoff` | Test that setup instructions and
    documentation actually work |

    ## When to Use

    - Starting a new project and need standard community health files
    - Onboarding new contributors and need to verify documentation quality
    - Preparing a project for handoff to new maintainers
    - Validating that setup instructions actually work
    - Auditing documentation completeness

    ## Related Plugins

    This plugin focuses on project lifecycle. For other concerns, use:

    | Need | Plugin |
    |------|--------|
    | GitHub Actions CI/CD, releases, org audit, issue triage | GitHub plugin |
    | Docker, Singularity, Podman, container registries | Containerization plugin |
    | Python-specific development practices | Scientific Python Development |

    ## Integration with Other Plugins

    - **GitHub Plugin** — After scaffolding with `/setup-project`, use
      `/ci-setup` to add CI/CD workflows
    - **Containerization Plugin** — Use to add Dockerfiles after project setup
    - **AI Research Workflows** — Use `/research` and `/plan` for complex
      project management tasks
    ```

- [x] Update `.claude-plugin/marketplace.json` entry for project-management
  - Change `description` to match plugin.json
  - Update `keywords` from:
    ```json
    ["project-management", "github", "ci-cd", "devops", "github-actions", "docker",
     "pre-commit", "release-management", "issue-triage", "onboarding", "scientific-computing"]
    ```
    to:
    ```json
    ["project-management", "onboarding", "documentation", "handoff",
     "community-health", "research-software", "project-lifecycle"]
    ```

**Verification:**
- [x] `plugin.json` description matches the new scope
- [x] README accurately lists only the remaining 2 agents, 2 skills, 3 commands
- [x] README does not mention CI/CD, GitHub Actions, containerization, Docker, or DevOps as capabilities
- [x] README "Related Plugins" section points to GitHub and containerization plugins
- [x] Marketplace entry keywords no longer include "github", "ci-cd", "devops", "docker", "github-actions"

## Success Criteria

### Automated Verification

These checks can be run without human intervention:

- [x] `grep -r "scientific Python" plugins/project-management/` returns no results
- [x] `ls plugins/project-management/agents/` shows exactly 2 files: `project-onboarding-specialist.md`, `documentation-validator.md`
- [x] `ls plugins/project-management/skills/` shows exactly 2 directories: `community-health-files/`, `documentation-validation/`
- [x] `ls plugins/project-management/commands/` shows exactly 3 files: `setup-project.md`, `project-handoff.md`, `validate-project-handoff.md`
- [x] `ls plugins/project-management/skills/community-health-files/assets/` shows 5 template files
- [x] `ls plugins/project-management/skills/documentation-validation/assets/` shows 2 files
- [x] No empty directories exist under `plugins/project-management/`
- [x] `python -c "import json; d=json.load(open('plugins/project-management/.claude-plugin/plugin.json')); assert 'scientific Python' not in d['description']"` passes
- [x] `python -c "import json; d=json.load(open('.claude-plugin/marketplace.json')); pm=[p for p in d['plugins'] if p['name']=='project-management'][0]; assert 'ci-cd' not in pm['keywords']"` passes
- [ ] Plugin validation workflow passes (if running in CI)

### Manual Verification

These require human testing and judgment:

- [ ] Read through `setup-project.md` and verify it makes sense for scaffolding an R package, a Rust crate, or a Node.js project
- [ ] Read through `project-handoff.md` and verify the assessment criteria work for non-Python repositories
- [ ] Read through the CONTRIBUTING-template.md and verify it provides useful guidance for any language
- [ ] Read through the README-template.md and verify badge and installation sections are language-neutral
- [ ] Verify the README.md "Related Plugins" section correctly describes when to use other plugins
- [ ] Verify the agent descriptions would trigger correctly for non-Python project setup requests
- [ ] Spot-check that documentation-validation SKILL.md mentions alternatives to Python-specific tools

## Testing Strategy

**Structural Tests:**
- [ ] Verify file counts match expected (2 agents, 2 skills, 3 commands)
- [ ] Verify no "scientific Python" string remains in any file
- [ ] Verify plugin.json is valid JSON with updated description
- [ ] Verify marketplace.json is valid JSON with updated entry

**Content Tests:**
- [ ] Read each remaining file end-to-end to verify coherence after edits
- [ ] Verify all internal file references (e.g., `assets/README-template.md`) still resolve
- [ ] Verify skill names in agent frontmatter match existing skill directories

**Regression Tests:**
- [ ] Verify the CITATION-template.cff, CODE_OF_CONDUCT-template.md, and SECURITY-template.md are unchanged (they were already language-agnostic)
- [ ] Verify vale-config.ini is unchanged (already language-agnostic)

## Migration Strategy

**Migration Steps:**
1. Document the change in the README under a "Migration" section
2. Point users to the GitHub plugin for moved capabilities: `/ci-setup`, `/triage`, `/release-plan`, `/audit-github-org`
3. Point users to the containerization plugin for Docker/Singularity/Apptainer guidance

**Rollback Plan:**
All changes are file deletions and text edits tracked in git. Rollback is `git revert` of the refactoring commit(s).

**Backward Compatibility:**
This is a breaking change for users who depend on the moved commands and skills. The new plugins (#58, #59) provide the same capabilities in their new locations. The README migration section provides clear guidance.

## Risk Assessment

**Potential Risks:**

1. **Risk:** Users install the refactored plugin expecting CI/CD capabilities
   - **Likelihood:** Medium — existing documentation and tutorials may reference old capabilities
   - **Impact:** Medium — user confusion, not data loss
   - **Mitigation:** Clear README with "Related Plugins" section and migration guide

2. **Risk:** Generalization removes useful Python-specific guidance from templates
   - **Likelihood:** Low — Python users can still use the templates; the guidance is generalized, not removed
   - **Impact:** Low — slightly less prescriptive for Python users
   - **Mitigation:** Templates include language-specific examples as comments/options, not just generic placeholders

3. **Risk:** setup-project becomes too generic to be useful
   - **Likelihood:** Low — community health files (the core output) are inherently language-agnostic
   - **Impact:** Medium — the command's value proposition depends on generating useful files
   - **Mitigation:** Focus on what the command does well (community files) and delegate language-specific scaffolding explicitly

## Edge Cases and Error Handling

**Edge Cases:**

1. **Case:** User runs `/setup-project` without the GitHub or containerization plugins installed
   - **Expected Behavior:** Command completes successfully, scaffolding community health files. Suggests installing the other plugins for CI/CD and containerization as optional next steps.
   - **Implementation:** setup-project generates only universal files. Delegation suggestions are informational, not functional dependencies.

2. **Case:** User runs `/project-handoff` on a non-GitHub repository (e.g., GitLab, Bitbucket)
   - **Expected Behavior:** `gh` commands fail gracefully. Command still checks local files (README, CONTRIBUTING, LICENSE, tests). Reports that GitHub-specific checks were skipped.
   - **Implementation:** The `gh` CLI is documented as optional in prerequisites. Command should handle `gh` failures gracefully.

3. **Case:** CONTRIBUTING-template.md is used for a language with no pre-commit ecosystem
   - **Expected Behavior:** Template includes pre-commit as a recommended tool but does not require it. User can remove the section.
   - **Implementation:** Template presents pre-commit as optional with a note about when it applies.

## Documentation Updates

- [x] Rewrite `plugins/project-management/README.md` (covered in Phase 5)
- [ ] Update `.claude-plugin/marketplace.json` (covered in Phase 5)
- [ ] No external documentation to update (plugin docs are self-contained)

## Open Questions

None. All decisions have been resolved:
- community-health-files stays in project-management (no duplication)
- setup-project asks for language, doesn't auto-detect
- Plugin name stays as "project-management"
- Migration documented in README
- Handoff commands keep CI/CD checks as read-only health indicators

---

## References

**Research Documents:**
- [Research: Project Management Plugin](research-project-management-plugin.md)
- [Research: Plugin Gap Analysis](research-plugin-gap-analysis.md)

**Files Analyzed:**
- `plugins/project-management/.claude-plugin/plugin.json`
- `plugins/project-management/README.md`
- `plugins/project-management/agents/project-onboarding-specialist.md`
- `plugins/project-management/agents/documentation-validator.md`
- `plugins/project-management/skills/community-health-files/SKILL.md`
- `plugins/project-management/skills/community-health-files/assets/README-template.md`
- `plugins/project-management/skills/community-health-files/assets/CONTRIBUTING-template.md`
- `plugins/project-management/skills/community-health-files/assets/CITATION-template.cff`
- `plugins/project-management/skills/community-health-files/assets/CODE_OF_CONDUCT-template.md`
- `plugins/project-management/skills/community-health-files/assets/SECURITY-template.md`
- `plugins/project-management/skills/documentation-validation/SKILL.md`
- `plugins/project-management/skills/documentation-validation/assets/validation-checklist.md`
- `plugins/project-management/skills/documentation-validation/assets/vale-config.ini`
- `plugins/project-management/commands/setup-project.md`
- `plugins/project-management/commands/project-handoff.md`
- `plugins/project-management/commands/validate-project-handoff.md`
- `.claude-plugin/marketplace.json`

**GitHub Issues:**
- [#58 — Containerization Plugin](https://github.com/uw-ssec/rse-plugins/issues/58)
- [#59 — GitHub Plugin](https://github.com/uw-ssec/rse-plugins/issues/59)
- [#60 — Project Management Refactoring](https://github.com/uw-ssec/rse-plugins/issues/60)

---

## Review History

### Version 1.0 — 2026-02-26
- Initial plan created based on research document and issue #60
- All 5 open questions from research resolved
- 5-phase implementation structure defined

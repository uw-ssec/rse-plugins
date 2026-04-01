# Implementation Plan: Project Management Plugin

---
**Date:** 2026-02-19
**Author:** AI Assistant
**Status:** Draft
**Related Documents:**
- [Research: Plugin Gap Analysis](research-plugin-gap-analysis.md)
- [Research: Project Management Plugin](research-project-management-plugin.md)

---

## Overview

This plan creates a comprehensive **project-management** core plugin for the RSE Plugins repository. The plugin addresses the two highest-priority gaps identified in the gap analysis: (1) open-source project management and collaboration tooling, and (2) CI/CD and DevOps for scientific software. It is tailored specifically to GitHub-hosted scientific Python projects and organizations like SSEC at the University of Washington.

The plugin provides 5 agents, 8 skills, and 7 slash commands that cover the full project lifecycle — from initializing a new project with standard templates, through day-to-day issue triage and CI/CD management, to release planning, project handoff validation, and organization-wide repository auditing.

**Goal:** A fully functional core plugin at `plugins/project-management/` registered in the marketplace, with all agents, skills, and commands following the established patterns from existing plugins (especially `ai-research-workflows` and `scientific-python-development`).

**Motivation:** Project management and CI/CD are the two most impactful missing capabilities in the RSE Plugins ecosystem. Every scientific Python project needs issue management, CI pipelines, release workflows, and community health files — yet no plugin exists for any of these. This plugin makes it a one-stop shop.

## Current State Analysis

**Existing Implementation:**
- `.claude-plugin/marketplace.json:1-47` — Marketplace catalog listing 4 current plugins (scientific-python-development, scientific-domain-applications, holoviz-visualization, ai-research-workflows)
- `plugins/ai-research-workflows/` — Exemplar plugin with commands, agents, and skills
- `plugins/ai-research-workflows/.claude-plugin/plugin.json:1-9` — Plugin manifest format to follow
- `plugins/ai-research-workflows/commands/research.md` — Command definition pattern to follow
- `plugins/scientific-python-development/agents/scientific-python-expert.md:1-50` — Agent YAML frontmatter pattern to follow
- `plugins/scientific-python-development/skills/python-testing/SKILL.md:1-5` — Skill YAML frontmatter pattern to follow

**Current Behavior:**
The repository provides zero project management, CI/CD, or DevOps capabilities. Users working on scientific Python projects must manually set up GitHub Actions, write issue templates, configure pre-commit hooks, plan releases, and manage community health files without AI assistance.

**Current Limitations:**
- No agent understands GitHub project management workflows
- No skill provides CI/CD configuration knowledge
- No commands exist for issue triage, release planning, or repo health auditing
- No templates exist for community health files (CONTRIBUTING, CODE_OF_CONDUCT, SECURITY)
- No onboarding/offboarding workflow support
- No organization-level repository management tooling

## Desired End State

**New Behavior:**
Users can invoke specialized agents and slash commands to manage scientific Python projects end-to-end:
- `/setup-project` scaffolds a new project with all community health files, CI/CD, and standard structure
- `/triage ISSUE_URL` analyzes an issue and suggests labels, priority, and next steps
- `/release-plan` generates a release plan from current milestones
- `/ci-setup` generates GitHub Actions workflows tailored to scientific Python
- `/project-handoff` validates a project is ready for handoff to new maintainers
- `/validate-project-handoff` tests that documentation actually works by following it
- `/audit-github-org` audits all repos in a GitHub organization for health metrics

**Success Looks Like:**
- Plugin appears in marketplace and is installable via `/plugin marketplace add`
- All 7 commands are invocable and produce useful output
- All 5 agents are triggerable by relevant user queries
- All 8 skills provide comprehensive reference material
- Plugin follows all established patterns from existing plugins
- README.md documents all components clearly

## What We're NOT Doing

- [ ] Integration with non-GitHub platforms (Jira, GitLab, Bitbucket)
- [ ] Cloud computing / deployment skills (reserved for a future plugin)
- [ ] Database or state management for tracking project status over time
- [ ] MCP server integration (unlike holoviz-visualization)
- [ ] Automated two-way sync with external project management tools
- [ ] GitHub App or OAuth — relies on existing `gh` CLI auth

**Rationale:** Keeping scope to GitHub-only and file-based (no databases, no MCP) ensures the plugin is achievable in a single iteration and follows the simplest patterns from existing plugins. External platform support can be added later as separate plugins or extensions.

## Implementation Approach

**Technical Strategy:**
Follow the established plugin architecture exactly. Each component (agent, skill, command) is a standalone Markdown file with YAML frontmatter. Skills contain reference material in `SKILL.md` with supporting `assets/` and `references/` directories. Commands define behavior instructions that Claude Code executes when the user invokes them. The plugin integrates with GitHub via the `gh` CLI tool, which handles authentication natively.

**Key Architectural Decisions:**

1. **Decision:** Core plugin in `plugins/` (not `community-plugins/`)
   - **Rationale:** Project management is fundamental to the RSE mission, not ecosystem-specific
   - **Trade-offs:** Higher bar for quality since it's an official plugin
   - **Alternatives considered:** Community plugin (rejected — too foundational)

2. **Decision:** Merge CI/CD into this plugin rather than a separate plugin
   - **Rationale:** GitHub Actions, pre-commit, and containerization are tightly coupled with project management (releases trigger CI, PRs require CI, etc.)
   - **Trade-offs:** Larger plugin, but more cohesive user experience
   - **Alternatives considered:** Separate ci-cd plugin (rejected — too fragmented)

3. **Decision:** Use `gh` CLI for all GitHub API interactions
   - **Rationale:** Already available in most dev environments, handles auth automatically, Claude Code can invoke via Bash tool
   - **Trade-offs:** Dependency on gh being installed
   - **Alternatives considered:** Direct REST API calls (rejected — auth complexity)

4. **Decision:** 5 agents with distinct responsibilities rather than 1 mega-agent
   - **Rationale:** Follows the holoviz-visualization pattern (4 specialized agents), enables better triggering and focused expertise
   - **Trade-offs:** More files to maintain
   - **Alternatives considered:** 1-2 general agents (rejected — too broad, poor trigger accuracy)

**Patterns to Follow:**
- Plugin manifest format — See `plugins/ai-research-workflows/.claude-plugin/plugin.json:1-9`
- Agent YAML frontmatter with examples — See `plugins/scientific-python-development/agents/scientific-python-expert.md:1-50`
- Skill YAML frontmatter with triggers — See `plugins/scientific-python-development/skills/python-testing/SKILL.md:1-5`
- Command markdown format — See `plugins/ai-research-workflows/commands/research.md`
- Marketplace registration — See `.claude-plugin/marketplace.json:3-47`

## Implementation Phases

### Phase 1: Plugin Scaffold and Manifest

**Objective:** Create the directory structure and plugin manifest so the plugin is recognized by the marketplace.

**Tasks:**

- [x] Create plugin directory structure
  - Directory: `plugins/project-management/`
  - Create all subdirectories:
    ```
    plugins/project-management/
    ├── .claude-plugin/
    ├── agents/
    ├── commands/
    └── skills/
        ├── community-health-files/
        │   ├── assets/
        │   └── references/
        ├── documentation-validation/
        │   ├── assets/
        │   └── references/
        ├── github-org-management/
        │   └── references/
        ├── release-management/
        │   ├── assets/
        │   └── references/
        ├── issue-triage/
        │   └── references/
        ├── github-actions/
        │   ├── assets/
        │   └── references/
        ├── containerization/
        │   ├── assets/
        │   └── references/
        └── pre-commit-workflows/
            ├── assets/
            └── references/
    ```

- [x] Create plugin manifest
  - File: `plugins/project-management/.claude-plugin/plugin.json`
  - Content:
    ```json
    {
        "name": "project-management",
        "description": "Agents, skills, and commands for GitHub-based open-source scientific Python project management, CI/CD, and DevOps",
        "version": "0.1.0",
        "author": {
            "name": "SSEC Research Team",
            "url": "https://github.com/uw-ssec"
        }
    }
    ```

- [x] Register plugin in marketplace
  - File: `.claude-plugin/marketplace.json`
  - Changes: Add new entry to the `plugins` array:
    ```json
    {
        "name": "project-management",
        "source": "./plugins/project-management",
        "description": "GitHub-based project management, CI/CD, and DevOps for scientific Python projects",
        "homepage": "https://github.com/uw-ssec/rse-plugins",
        "repository": "https://github.com/uw-ssec/rse-plugins",
        "license": "BSD-3-Clause",
        "keywords": ["project-management", "github", "ci-cd", "devops", "github-actions", "docker", "pre-commit", "release-management", "issue-triage", "onboarding", "scientific-computing"],
        "category": "development",
        "strict": false
    }
    ```

**Dependencies:** None

**Verification:**
- [x] `plugins/project-management/.claude-plugin/plugin.json` exists and is valid JSON
- [x] All skill subdirectories exist
- [x] Marketplace entry is valid JSON and contains the new plugin

---

### Phase 2: Skills — Community Health, Documentation Validation, and Org Management

**Objective:** Create the 3 skills from the prior research document that focus on organizational project management fundamentals.

**Tasks:**

- [x] Create `community-health-files` skill
  - File: `plugins/project-management/skills/community-health-files/SKILL.md`
  - Frontmatter: name, description with triggers ("create README template", "add CONTRIBUTING", "set up CODE_OF_CONDUCT", "create SECURITY policy", "community health files", "project templates", "CITATION.cff")
  - Content sections:
    - Quick Reference Card — checklist of all community health files
    - Standard community health files (README, CONTRIBUTING, LICENSE, CODE_OF_CONDUCT, SECURITY, SUPPORT, FUNDING.yml, ISSUE_TEMPLATE/, PULL_REQUEST_TEMPLATE)
    - The .github organization-level defaults pattern
    - CITATION.cff for academic projects
    - Template guidance for each file type
    - Best practices for scientific software projects
  - Assets:
    - `assets/README-template.md` — Scientific Python project README template
    - `assets/CONTRIBUTING-template.md` — Contribution guidelines template
    - `assets/CODE_OF_CONDUCT-template.md` — Contributor Covenant template
    - `assets/SECURITY-template.md` — Security policy template
    - `assets/CITATION-template.cff` — CITATION.cff template for academic projects

- [x] Create `documentation-validation` skill
  - File: `plugins/project-management/skills/documentation-validation/SKILL.md`
  - Frontmatter: name, description with triggers ("validate documentation", "test setup instructions", "check docs quality", "lint prose", "validate links", "documentation testing")
  - Content sections:
    - Quick Reference Card — validation tool decision tree
    - Validation tools: Vale (prose linting), HTMLProofer (link checking), markdownlint
    - Documentation-as-code testing strategies
    - Container-based instruction testing (following docs step-by-step)
    - GitHub Actions integration for automated doc validation
    - Quality metrics and standards
    - Checklist for project handoff documentation completeness
  - Assets:
    - `assets/validation-checklist.md` — Documentation completeness checklist
    - `assets/vale-config.ini` — Vale configuration template for scientific docs

- [x] Create `github-org-management` skill
  - File: `plugins/project-management/skills/github-org-management/SKILL.md`
  - Frontmatter: name, description with triggers ("audit github organization", "manage repositories", "archive repository", "repository health", "organization cleanup", "repo naming conventions", "repository topics")
  - Content sections:
    - Quick Reference Card — org management decision tree
    - Repository organization strategies (naming, topics, templates)
    - Health metrics (last activity, open issues/PRs, community files, CI status, security alerts)
    - Archival criteria and process (12+ months inactive, superseded, completed)
    - The .github and .github-private repository patterns
    - Multi-repository management with `gh` CLI
    - Repository lifecycle states (active, maintenance, archived)
  - References:
    - `references/health-metrics.md` — Detailed metrics definitions and thresholds

**Dependencies:** Phase 1 (directories must exist)

**Verification:**
- [x] All 3 SKILL.md files exist and have valid YAML frontmatter
- [x] All referenced asset files exist
- [x] Frontmatter `name` and `description` fields are present

---

### Phase 3: Skills — Release Management, Issue Triage, CI/CD, Containers, and Pre-commit

**Objective:** Create the 5 skills from the gap analysis that focus on day-to-day development operations.

**Tasks:**

- [x] Create `release-management` skill
  - File: `plugins/project-management/skills/release-management/SKILL.md`
  - Frontmatter: name, description with triggers ("plan release", "semantic versioning", "create changelog", "publish to PyPI", "conda-forge recipe", "towncrier", "release workflow", "version bump")
  - Content sections:
    - Quick Reference Card — release workflow decision tree
    - Semantic versioning (SemVer) for scientific packages
    - Changelog management: towncrier (fragment-based), auto-changelog, keep-a-changelog
    - PyPI publishing workflow (build, twine, trusted publishers)
    - conda-forge recipe creation and maintenance
    - GitHub Releases and tag management
    - Release automation with GitHub Actions
    - Version bumping tools (bump2version, hatch version)
  - Assets:
    - `assets/pyproject-release-config.toml` — Release tooling configuration snippet
    - `assets/release-checklist.md` — Pre-release validation checklist

- [x] Create `issue-triage` skill
  - File: `plugins/project-management/skills/issue-triage/SKILL.md`
  - Frontmatter: name, description with triggers ("triage issue", "label issues", "prioritize bugs", "stale issues", "issue templates", "bug report template", "feature request template")
  - Content sections:
    - Quick Reference Card — triage decision tree
    - Label taxonomy for scientific Python projects (type, priority, status, component)
    - Bug vs. feature classification criteria
    - Priority assignment framework (P0-critical through P3-nice-to-have)
    - Issue template design (bug report, feature request, documentation)
    - Stale issue management (probot/stale, actions/stale)
    - Triage workflow for maintainers
    - Automated labeling with GitHub Actions
  - Assets:
    - `assets/bug-report-template.md` — GitHub issue template for bug reports
    - `assets/feature-request-template.md` — GitHub issue template for feature requests

- [x] Create `github-actions` skill
  - File: `plugins/project-management/skills/github-actions/SKILL.md`
  - Frontmatter: name, description with triggers ("set up github actions", "CI workflow", "matrix testing", "github actions cache", "reusable workflows", "secrets management", "CI/CD pipeline", "automated testing")
  - Content sections:
    - Quick Reference Card — common workflow patterns
    - Workflow YAML syntax and structure
    - Matrix testing strategies (Python versions, OS, dependency sets)
    - Caching strategies (pip, conda, pixi)
    - Reusable workflows and composite actions
    - Secrets management and environment variables
    - Triggering strategies (push, PR, schedule, manual dispatch)
    - Scientific Python-specific patterns (pixi run, tox, nox)
    - Common workflows: test, lint, build docs, publish
    - Security hardening (pinned actions, OIDC, permissions)
  - Assets:
    - `assets/ci-test-workflow.yml` — Template: test with matrix Python versions
    - `assets/ci-publish-workflow.yml` — Template: publish to PyPI with trusted publishers
    - `assets/ci-docs-workflow.yml` — Template: build and deploy docs

- [x] Create `containerization` skill
  - File: `plugins/project-management/skills/containerization/SKILL.md`
  - Frontmatter: name, description with triggers ("create Dockerfile", "Docker for scientific Python", "containerize", "Singularity", "Apptainer", "multi-stage build", "pixi in Docker", "conda in container")
  - Content sections:
    - Quick Reference Card — container strategy decision tree
    - Dockerfile patterns for scientific Python (pip, conda, pixi)
    - Multi-stage builds to reduce image size
    - pixi in containers (pixi-docker patterns)
    - GPU containers (NVIDIA CUDA base images)
    - Singularity/Apptainer for HPC environments
    - Docker Compose for multi-service scientific applications
    - Container registries (GHCR, Docker Hub, Quay)
    - Best practices: non-root users, layer caching, .dockerignore
  - Assets:
    - `assets/Dockerfile-pixi-template` — Dockerfile template using pixi
    - `assets/Dockerfile-conda-template` — Dockerfile template using conda/mamba

- [x] Create `pre-commit-workflows` skill
  - File: `plugins/project-management/skills/pre-commit-workflows/SKILL.md`
  - Frontmatter: name, description with triggers ("set up pre-commit", "pre-commit hooks", "pre-commit.ci", "git hooks", "automated code quality", "pre-commit config")
  - Content sections:
    - Quick Reference Card — essential hooks for scientific Python
    - .pre-commit-config.yaml setup and structure
    - Essential hooks: ruff (lint+format), mypy, check-yaml, check-json, trailing-whitespace, end-of-file-fixer
    - Scientific Python-specific hooks (notebook cleanup, FITS validation)
    - Custom hook creation
    - pre-commit.ci integration (auto-fix PRs)
    - CI integration (run pre-commit in GitHub Actions)
    - Troubleshooting common issues
  - Assets:
    - `assets/pre-commit-config-template.yaml` — Template .pre-commit-config.yaml for scientific Python

**Dependencies:** Phase 1 (directories must exist)

**Verification:**
- [x] All 5 SKILL.md files exist and have valid YAML frontmatter
- [x] All referenced asset files exist
- [x] Frontmatter `name` and `description` fields are present

---

### Phase 4: Agents

**Objective:** Create all 5 agent definitions following the established pattern from `scientific-python-expert.md`.

**Tasks:**

- [x] Create `project-onboarding-specialist` agent
  - File: `plugins/project-management/agents/project-onboarding-specialist.md`
  - Frontmatter:
    - name: project-onboarding-specialist
    - description: with usage examples covering "set up new project", "onboard new contributor", "create project documentation", "project handoff"
    - model: inherit
    - color: blue
    - skills: community-health-files, documentation-validation
  - Body sections:
    - Purpose: Expert in project initialization, contributor onboarding, and knowledge transfer
    - Core Competencies: project scaffolding, community health files, onboarding documentation, handoff preparation
    - Workflow Patterns: project setup, onboarding guide generation, offboarding checklist
    - When to Use: setting up new projects, preparing handoff docs, onboarding team members
    - Key Constraints: DO rely on `gh` CLI; DON'T assume specific org structure
    - Completion Criteria: project has all community health files, setup instructions work, onboarding docs are complete

- [x] Create `github-org-manager` agent
  - File: `plugins/project-management/agents/github-org-manager.md`
  - Frontmatter:
    - name: github-org-manager
    - description: with usage examples covering "audit organization repos", "clean up repositories", "archive stale repos", "repository health check"
    - model: inherit
    - color: purple
    - skills: github-org-management, community-health-files
  - Body sections:
    - Purpose: Expert in GitHub organization management, multi-repo health monitoring, and repository lifecycle
    - Core Competencies: org auditing, repo health metrics, archival workflows, naming/topic conventions
    - Workflow Patterns: org audit, repo cleanup, health reporting
    - When to Use: auditing org health, archiving repos, standardizing repo configuration
    - Key Constraints: requires `gh` CLI with org-level access; DON'T auto-archive without user confirmation
    - Completion Criteria: audit report generated, recommendations provided, no destructive actions without approval

- [x] Create `documentation-validator` agent
  - File: `plugins/project-management/agents/documentation-validator.md`
  - Frontmatter:
    - name: documentation-validator
    - description: with usage examples covering "validate documentation", "test setup instructions", "check project readiness", "documentation quality"
    - model: inherit
    - color: cyan
    - skills: documentation-validation, community-health-files
  - Body sections:
    - Purpose: Expert in documentation quality assurance, setup instruction validation, and completeness checking
    - Core Competencies: doc completeness audit, prose linting, link validation, instruction testing
    - Workflow Patterns: static validation (tools), dynamic validation (following instructions), completeness checklist
    - When to Use: preparing for release, handoff, auditing docs quality
    - Key Constraints: DON'T modify code — validation and reporting only
    - Completion Criteria: validation report generated with pass/fail for each criterion

- [x] Create `github-workflow-specialist` agent
  - File: `plugins/project-management/agents/github-workflow-specialist.md`
  - Frontmatter:
    - name: github-workflow-specialist
    - description: with usage examples covering "set up GitHub Actions", "CI/CD pipeline", "automate releases", "configure branch protection", "reusable workflows"
    - model: inherit
    - color: yellow
    - skills: github-actions, pre-commit-workflows, release-management
  - Body sections:
    - Purpose: Expert in GitHub-native CI/CD, automation, and workflow design for scientific Python
    - Core Competencies: Actions workflow authoring, matrix testing, caching, release automation, pre-commit integration
    - Workflow Patterns: CI setup, release workflow design, PR automation
    - When to Use: setting up CI, automating releases, configuring GitHub workflows
    - Key Constraints: ALWAYS pin action versions; ALWAYS use OIDC for publishing; NEVER store secrets in workflow files
    - Completion Criteria: workflows are syntactically valid, follow security best practices, run in CI

- [x] Create `devops-engineer` agent
  - File: `plugins/project-management/agents/devops-engineer.md`
  - Frontmatter:
    - name: devops-engineer
    - description: with usage examples covering "containerize application", "create Dockerfile", "set up Docker for scientific Python", "Singularity container", "deploy application"
    - model: inherit
    - color: orange
    - skills: containerization, github-actions
  - Body sections:
    - Purpose: Expert in containerization, deployment, and infrastructure for scientific software
    - Core Competencies: Docker/Podman, multi-stage builds, HPC containers (Singularity/Apptainer), GPU, CI/CD integration
    - Workflow Patterns: container build, optimization, registry push, HPC deployment
    - When to Use: containerizing scientific software, deploying to HPC, optimizing Docker images
    - Key Constraints: ALWAYS use non-root users; ALWAYS use multi-stage builds; NEVER include credentials in images
    - Completion Criteria: container builds successfully, runs tests, image size is optimized

**Dependencies:** Phase 2 and Phase 3 (skills must exist so agents can reference them)

**Verification:**
- [x] All 5 agent .md files exist in `plugins/project-management/agents/`
- [x] Each has valid YAML frontmatter with name, description (including examples), model, color, and skills
- [x] Each references only skills that exist in this plugin
- [x] Each follows the section structure from `scientific-python-expert.md`

---

### Phase 5: Commands

**Objective:** Create all 7 slash commands following the pattern from `ai-research-workflows/commands/`.

**Tasks:**

- [x] Create `/setup-project` command
  - File: `plugins/project-management/commands/setup-project.md`
  - Frontmatter: description field
  - Behavior:
    - Accept project name and optional arguments (language, license, org)
    - Create project directory structure with standard layout
    - Generate community health files from templates (README, CONTRIBUTING, LICENSE, CODE_OF_CONDUCT, SECURITY)
    - Set up pyproject.toml with basic configuration
    - Create .pre-commit-config.yaml
    - Generate GitHub Actions CI workflow
    - Create CITATION.cff template
    - Create initial issue templates (bug report, feature request)
    - Output summary of created files

- [x] Create `/triage` command
  - File: `plugins/project-management/commands/triage.md`
  - Frontmatter: description field
  - Behavior:
    - Accept issue URL or issue number (with optional repo context)
    - Use `gh issue view` to fetch issue details
    - Analyze issue content (title, body, comments)
    - Classify: bug, feature, documentation, question, enhancement
    - Suggest labels from standard taxonomy
    - Assign priority (P0-P3)
    - Suggest assignee if team context available
    - Recommend next steps (needs reproduction, needs design, ready to implement)
    - Output structured triage report

- [x] Create `/release-plan` command
  - File: `plugins/project-management/commands/release-plan.md`
  - Frontmatter: description field
  - Behavior:
    - Detect current version from pyproject.toml or equivalent
    - Use `gh` to list merged PRs since last release/tag
    - Categorize changes (features, fixes, breaking, docs, internal)
    - Suggest next version number (based on SemVer analysis of changes)
    - Generate draft changelog entries
    - List remaining open issues in current milestone (if any)
    - Create pre-release checklist
    - Output structured release plan document to `.agents/release-plan-<version>.md`

- [x] Create `/project-handoff` command
  - File: `plugins/project-management/commands/project-handoff.md`
  - Frontmatter: description field
  - Behavior:
    - Scan project for community health files (README, CONTRIBUTING, LICENSE, etc.)
    - Check documentation completeness (installation, usage, development, testing)
    - Verify CI/CD configuration exists and recent runs pass
    - Check for CITATION.cff
    - Verify test suite exists and has recent passing runs
    - Check for open security vulnerabilities (Dependabot alerts)
    - Generate handoff readiness report with pass/fail/warning for each criterion
    - Provide specific recommendations for gaps
    - Output structured report

- [x] Create `/validate-project-handoff` command
  - File: `plugins/project-management/commands/validate-project-handoff.md`
  - Frontmatter: description field
  - Behavior:
    - Read project README and setup instructions
    - Attempt to follow installation instructions step-by-step
    - Attempt to run test suite as documented
    - Attempt to build documentation as documented
    - Record success/failure at each step
    - Identify unclear, missing, or broken instructions
    - Generate validation report with specific issues found
    - Suggest documentation improvements based on failures
    - Output structured validation report

- [x] Create `/audit-github-org` command
  - File: `plugins/project-management/commands/audit-github-org.md`
  - Frontmatter: description field
  - Behavior:
    - Accept organization name (or detect from current repo)
    - Use `gh api` to list all organization repositories
    - For each repo, check:
      - Last commit date (stale threshold: 12 months)
      - Open issues and PRs count
      - Community health file presence (README, LICENSE, CONTRIBUTING)
      - CI/CD workflow presence
      - Dependabot/security alerts
      - Topics and description completeness
    - Categorize repos: active, maintenance, archive-candidate, needs-attention
    - Generate summary statistics
    - Provide prioritized recommendations
    - Output structured audit report to `.agents/audit-<org-name>.md`

- [x] Create `/ci-setup` command
  - File: `plugins/project-management/commands/ci-setup.md`
  - Frontmatter: description field
  - Behavior:
    - Detect project type (pixi, conda, pip, poetry) from config files
    - Accept optional framework argument (pytest, tox, nox)
    - Generate GitHub Actions CI workflow file (`.github/workflows/ci.yml`)
    - Include matrix testing (Python versions, OS)
    - Include caching for detected package manager
    - Include pre-commit check step
    - Include optional steps: docs build, coverage upload
    - Optionally generate `.pre-commit-config.yaml` if missing
    - Output summary of generated files with key configuration decisions

**Dependencies:** Phases 2-3 (commands reference skills for knowledge), Phase 4 (agents must exist for the plugin to be complete)

**Verification:**
- [x] All 7 command .md files exist in `plugins/project-management/commands/`
- [x] Each has valid YAML frontmatter with `description` field
- [x] Each describes clear input/output behavior
- [x] Commands that generate output files use the `.agents/` directory convention

---

### Phase 6: Documentation and Integration

**Objective:** Create the plugin README, update the root README, and ensure the plugin integrates properly with the marketplace.

**Tasks:**

- [x] Create plugin README
  - File: `plugins/project-management/README.md`
  - Content:
    - Plugin description and purpose
    - List of all agents with brief descriptions
    - List of all skills with brief descriptions
    - List of all commands with usage examples
    - Prerequisites (gh CLI)
    - When to use this plugin
    - Integration with other RSE plugins

- [x] Update root README.md
  - File: `README.md`
  - Changes: Add a new section for the project-management plugin between "AI Research Workflows Plugin" and "HoloViz Visualization Plugin" sections, following the same format pattern used by other plugins (Agents, Skills, Commands, When to use)

- [x] Update repository structure diagram
  - File: `README.md:112-188`
  - Changes: Add `project-management/` directory tree to the structure diagram

**Dependencies:** All previous phases complete

**Verification:**
- [x] `plugins/project-management/README.md` exists and is comprehensive
- [x] `README.md` lists the project-management plugin with all components
- [x] Repository structure diagram includes the new plugin directory

---

## Success Criteria

### Automated Verification

- [ ] `plugins/project-management/.claude-plugin/plugin.json` exists and is valid JSON
- [ ] `.claude-plugin/marketplace.json` is valid JSON and contains project-management entry
- [ ] All 5 agent files exist: `ls plugins/project-management/agents/*.md | wc -l` equals 5
- [ ] All 8 skill files exist: `find plugins/project-management/skills -name "SKILL.md" | wc -l` equals 8
- [ ] All 7 command files exist: `ls plugins/project-management/commands/*.md | wc -l` equals 7
- [ ] Plugin README exists: `plugins/project-management/README.md`
- [ ] All YAML frontmatter in agent files has required fields (name, description, model, skills)
- [ ] All YAML frontmatter in skill files has required fields (name, description)
- [ ] All YAML frontmatter in command files has required field (description)
- [ ] No broken internal references (skills referenced by agents must exist)
- [ ] Root `README.md` mentions "project-management" plugin

### Manual Verification

- [ ] Each agent definition follows the section structure pattern from `scientific-python-expert.md` (Purpose, Core Competencies, Workflow Patterns, When to Use, Key Constraints, Completion Criteria)
- [ ] Each skill provides a Quick Reference Card and comprehensive reference material
- [ ] Each command provides clear step-by-step behavior instructions
- [ ] All template/asset files contain useful, non-placeholder content
- [ ] Plugin README accurately describes all components
- [ ] Root README section for the plugin is consistent with other plugin sections
- [ ] Agent descriptions include at least 3 usage examples with `<example>` tags
- [ ] Skill triggers cover the common ways users would invoke the capability

## Testing Strategy

**Structural Tests:**
- [ ] Validate all JSON files parse correctly (`python -m json.tool`)
- [ ] Validate YAML frontmatter in all .md files (grep for `---` delimiters)
- [ ] Verify file counts match expected (5 agents, 8 skills, 7 commands)
- [ ] Verify all skills referenced in agent frontmatter exist as directories

**Content Tests:**
- [ ] Each agent file is > 100 lines (ensures substantive content, matching existing agent depth)
- [ ] Each skill file is > 50 lines (ensures substantive content)
- [ ] Each command file is > 30 lines (ensures clear behavior specification)
- [ ] All asset files are non-empty

**Integration Tests:**
- [ ] Install plugin via marketplace and verify all commands appear
- [ ] Invoke each command to verify it's recognized (doesn't need to succeed, just trigger)
- [ ] Verify agents trigger on relevant user queries

**Manual Testing:**
- [ ] Run `/setup-project test-project` and verify output is useful
- [ ] Run `/ci-setup` in a real scientific Python project and verify generated workflow
- [ ] Run `/triage` on a real GitHub issue and verify analysis quality
- [ ] Run `/audit-github-org uw-ssec` and verify org audit output

## Risk Assessment

**Potential Risks:**

1. **Risk:** Plugin size — 20+ files across agents/skills/commands
   - **Likelihood:** Low
   - **Impact:** Low
   - **Mitigation:** Existing plugins (holoviz-visualization) are similarly large. Follow established patterns exactly.

2. **Risk:** `gh` CLI not installed in user environments
   - **Likelihood:** Medium
   - **Impact:** Medium (commands that use `gh` will fail)
   - **Mitigation:** Skills and agents work without `gh`; commands that require it should check for `gh` availability and provide installation guidance if missing.

3. **Risk:** GitHub API rate limits during org audits
   - **Likelihood:** Medium (for large orgs)
   - **Impact:** Low (audit is incomplete but doesn't break anything)
   - **Mitigation:** `/audit-github-org` command should handle pagination and provide partial results with a warning.

4. **Risk:** Template/asset content becomes outdated
   - **Likelihood:** Medium (over months)
   - **Impact:** Low
   - **Mitigation:** Templates follow stable standards (SemVer, Contributor Covenant, CITATION.cff). Version pin references in skills.

## Edge Cases and Error Handling

**Edge Cases:**

1. **Case:** User runs `/triage` without providing an issue URL
   - **Expected Behavior:** Prompt user for issue URL or number
   - **Implementation:** Command preamble checks for argument

2. **Case:** User runs `/audit-github-org` without org access
   - **Expected Behavior:** Clear error message about permissions; suggest `gh auth login` and required scopes
   - **Implementation:** Command checks `gh auth status` first

3. **Case:** User runs `/setup-project` in a directory that already has a project
   - **Expected Behavior:** Warn about existing files; offer to add missing files only (don't overwrite)
   - **Implementation:** Command checks for existing pyproject.toml/README.md first

4. **Case:** User runs `/validate-project-handoff` on a project with no README
   - **Expected Behavior:** Report as critical failure; cannot validate what doesn't exist
   - **Implementation:** First check is README existence

**Error Scenarios:**

1. **Error:** `gh` CLI not authenticated
   - **Handling:** Detect via `gh auth status`, provide clear instructions for `gh auth login`

2. **Error:** Network issues during GitHub API calls
   - **Handling:** Graceful degradation — report what can be checked locally, skip API-dependent checks

## Documentation Updates

- [ ] Create `plugins/project-management/README.md` — Full plugin documentation
- [ ] Update `README.md` — Add project-management plugin section
- [ ] Update `README.md` — Update repository structure diagram
- [ ] Update `.claude-plugin/marketplace.json` — Register new plugin

## Open Questions

None — all questions resolved during planning.

---

## References

**Research Documents:**
- [Research: Plugin Gap Analysis](research-plugin-gap-analysis.md) — Identified project management and CI/CD as top-2 priority gaps
- [Research: Project Management Plugin](research-project-management-plugin.md) — Detailed requirements for SSEC-focused project management

**Files Analyzed:**
- `.claude-plugin/marketplace.json` — Marketplace registration format
- `plugins/ai-research-workflows/.claude-plugin/plugin.json` — Plugin manifest format
- `plugins/ai-research-workflows/commands/research.md` — Command definition pattern
- `plugins/scientific-python-development/agents/scientific-python-expert.md` — Agent definition pattern
- `plugins/scientific-python-development/skills/python-testing/SKILL.md` — Skill definition pattern
- `README.md` — Root documentation structure
- `CONTRIBUTING.md` — Contribution guidelines

**External Documentation:**
- [GitHub Docs: Creating default community health files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file)
- [GitHub Docs: GitHub Actions](https://docs.github.com/en/actions)
- [Scientific Python Development Guide](https://learn.scientific-python.org/development/)
- [Semantic Versioning](https://semver.org/)
- [Contributor Covenant](https://www.contributor-covenant.org/)
- [CITATION.cff](https://citation-file-format.github.io/)

---

## Review History

### Version 1.0 — 2026-02-19
- Initial plan created
- Merged components from two research documents
- Scoped to GitHub-focused, core plugin with CI/CD included
- 5 agents, 8 skills, 7 commands across 6 implementation phases

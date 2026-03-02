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
| **Project Onboarding Specialist** | Expert in project initialization, contributor onboarding, and knowledge transfer for research software |
| **Documentation Validator** | Expert in documentation quality assurance, setup instruction validation, and completeness checking |

## Skills

| Skill | Description |
|-------|-------------|
| **community-health-files** | Templates and guidance for README, CONTRIBUTING, LICENSE, CODE_OF_CONDUCT, SECURITY, CITATION.cff, and issue/PR templates |
| **documentation-validation** | Validation tools (Vale, markdownlint, HTMLProofer) and documentation quality metrics |

## Commands

| Command | Description |
|---------|-------------|
| `/setup-project` | Scaffold a new project with community health files and standard structure |
| `/project-handoff` | Assess project readiness for handoff to new maintainers |
| `/validate-project-handoff` | Test that setup instructions and documentation actually work |

## When to Use

- Starting a new research software project and need standard community health files
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

- **GitHub Plugin** — After scaffolding with `/setup-project`, use `/ci-setup` to add CI/CD workflows
- **Containerization Plugin** — Use to add Dockerfiles after project setup
- **AI Research Workflows** — Use `/research` and `/plan` for complex project management tasks

## Migration from Previous Version

This plugin was previously a monolithic plugin covering GitHub platform mechanics,
containerization/DevOps, and project lifecycle. It has been refocused to handle
only project lifecycle concerns. If you previously used capabilities that are no
longer in this plugin:

| Previous Capability | New Location |
|-------------------|--------------|
| `/ci-setup`, `/triage`, `/release-plan`, `/audit-github-org` | GitHub plugin |
| GitHub Actions workflows, pre-commit hooks, issue triage | GitHub plugin |
| Docker, Singularity, Apptainer containers | Containerization plugin |

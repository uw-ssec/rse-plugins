# Research: Project Management Plugin — Current State and Refactoring Plan

---
**Date:** 2026-02-26 (updated from 2026-02-17)
**Author:** AI Assistant
**Status:** Active
**Related Documents:**
- [Issue #58 — Containerization Plugin](https://github.com/uw-ssec/rse-plugins/issues/58)
- [Issue #59 — GitHub Plugin](https://github.com/uw-ssec/rse-plugins/issues/59)
- [Issue #60 — Project Management Refactoring](https://github.com/uw-ssec/rse-plugins/issues/60)
- `.agents/research-plugin-gap-analysis.md` — Gap analysis that informed the plugin extraction

---

## Research Question

What is the current state of the `project-management` plugin, how does it overlap with the proposed containerization (#58) and GitHub (#59) plugins, and what specific changes are needed to refocus it on project lifecycle management per issue #60?

## Executive Summary

The `project-management` plugin was built as a monolithic plugin covering three distinct concerns: GitHub platform mechanics, containerization/DevOps, and project lifecycle management. It currently contains **8 skills, 5 agents, and 7 commands** all scoped to "scientific Python" projects.

Issue #60 defines a refactoring plan to extract GitHub-related content into a new language-agnostic GitHub plugin (#59) and containerization content into a new language-agnostic containerization plugin (#58). After extraction, the project-management plugin retains **2 skills, 2 agents, and 3 commands** focused exclusively on project lifecycle — onboarding, documentation quality, handoff readiness, and community health. The remaining content needs generalization from "scientific Python" to language-agnostic "research software" framing.

Cross-plugin analysis reveals **no hardcoded dependencies** between plugins. Integration is conceptual and documented only in the project-management README. This loose coupling means the refactoring can proceed without breaking other plugins, though documentation cross-references need updating.

## Scope

**What This Research Covers:**
- Complete inventory of the current project-management plugin (all agents, skills, commands, assets)
- Classification of every component by refactoring fate (stays, moves to #58, moves to #59)
- Language-specificity analysis for all components
- Cross-plugin dependency mapping
- Detailed generalization requirements for components that stay

**What This Research Does NOT Cover:**
- Implementation details for the new containerization or GitHub plugins
- Content of the new plugins (covered in their respective issues)
- Changes needed to other plugins (scientific-python-development, scientific-domain-applications, ai-research-workflows)

## Key Findings

### Finding 1: Current Plugin Structure and Identity

The plugin is registered in the marketplace and self-describes as:

**Relevant Files:**
- `plugins/project-management/.claude-plugin/plugin.json:1-9` — Plugin manifest
- `plugins/project-management/README.md:1-67` — Plugin documentation

**Current Identity:**
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

**Post-Refactoring Identity (per issue #60):**
```json
{
    "name": "project-management",
    "description": "Project lifecycle management — onboarding, documentation quality, handoff readiness, and community health for research software projects"
}
```

**Current Directory Structure:**
```
plugins/project-management/
├── .claude-plugin/
│   └── plugin.json
├── README.md
├── LICENSE
├── agents/
│   ├── devops-engineer.md                  # → containerization plugin (#58)
│   ├── documentation-validator.md          # STAYS
│   ├── github-org-manager.md               # → GitHub plugin (#59)
│   ├── github-workflow-specialist.md       # → GitHub plugin (#59)
│   └── project-onboarding-specialist.md    # STAYS
├── commands/
│   ├── audit-github-org.md                 # → GitHub plugin (#59)
│   ├── ci-setup.md                         # → GitHub plugin (#59)
│   ├── project-handoff.md                  # STAYS
│   ├── release-plan.md                     # → GitHub plugin (#59)
│   ├── setup-project.md                    # STAYS (needs generalization)
│   ├── triage.md                           # → GitHub plugin (#59)
│   └── validate-project-handoff.md         # STAYS
└── skills/
    ├── community-health-files/             # STAYS
    │   ├── SKILL.md
    │   └── assets/
    │       ├── CITATION-template.cff
    │       ├── CODE_OF_CONDUCT-template.md
    │       ├── CONTRIBUTING-template.md
    │       ├── README-template.md
    │       └── SECURITY-template.md
    ├── containerization/                   # → containerization plugin (#58)
    │   ├── SKILL.md
    │   └── assets/
    │       ├── Dockerfile-conda-template
    │       └── Dockerfile-pixi-template
    ├── documentation-validation/           # STAYS
    │   ├── SKILL.md
    │   └── assets/
    │       ├── vale-config.ini
    │       └── validation-checklist.md
    ├── github-actions/                     # → GitHub plugin (#59)
    │   ├── SKILL.md
    │   └── assets/
    │       ├── ci-docs-workflow.yml
    │       ├── ci-publish-workflow.yml
    │       └── ci-test-workflow.yml
    ├── github-org-management/              # → GitHub plugin (#59)
    │   ├── SKILL.md
    │   └── references/
    │       └── health-metrics.md
    ├── issue-triage/                       # → GitHub plugin (#59)
    │   ├── SKILL.md
    │   └── assets/
    │       ├── bug-report-template.md
    │       └── feature-request-template.md
    ├── pre-commit-workflows/               # → GitHub plugin (#59)
    │   ├── SKILL.md
    │   └── assets/
    │       └── pre-commit-config-template.yaml
    └── release-management/                 # → GitHub plugin (#59)
        ├── SKILL.md
        └── assets/
            ├── pyproject-release-config.toml
            └── release-checklist.md
```

### Finding 2: Complete Agent Inventory and Refactoring Fate

**Relevant Files:**
- `plugins/project-management/agents/devops-engineer.md` — containerization + GitHub Actions agent
- `plugins/project-management/agents/github-workflow-specialist.md` — CI/CD + release agent
- `plugins/project-management/agents/github-org-manager.md` — org management agent
- `plugins/project-management/agents/project-onboarding-specialist.md` — onboarding agent
- `plugins/project-management/agents/documentation-validator.md` — doc validation agent

| Agent | Description (first line) | Skills Referenced | Language-Specific? | Fate |
|-------|-------------------------|-------------------|-------------------|------|
| devops-engineer | "Expert in containerization, deployment infrastructure, and DevOps practices for scientific Python software" | containerization, github-actions | YES — "scientific Python software" | → #58 |
| github-workflow-specialist | "Expert in GitHub Actions CI/CD, workflow automation, and release pipeline design for scientific Python projects" | github-actions, pre-commit-workflows, release-management | YES — "scientific Python projects" | → #59 |
| github-org-manager | "Expert in GitHub organization management, multi-repository health monitoring, and repository lifecycle management for scientific software engineering organizations" | github-org-management, community-health-files | NO — says "scientific software" (not Python) | → #59 |
| project-onboarding-specialist | "Expert in scientific Python project initialization, contributor onboarding, and knowledge transfer for open-source research software" | community-health-files, documentation-validation | YES — "scientific Python project initialization" | STAYS |
| documentation-validator | "Expert in documentation quality assurance, setup instruction validation, and completeness checking for scientific Python projects" | documentation-validation, community-health-files | YES — "scientific Python projects" | STAYS |

**Key Pattern:** All agents use `model: inherit` and define a `color` property. All agents include detailed usage examples in their frontmatter description. The two staying agents both reference the two staying skills — there are no dangling skill references after refactoring.

### Finding 3: Complete Skill Inventory and Refactoring Fate

**Relevant Files:**
- `plugins/project-management/skills/*/SKILL.md` — All 8 skill definition files

| Skill | Description Scope | Assets | References | Language-Specific? | Fate |
|-------|-------------------|--------|------------|-------------------|------|
| community-health-files | Community standards, templates, CITATION.cff | 5 templates | — | Mixed — says "scientific software" with some Python examples | STAYS |
| containerization | Docker, Singularity, Apptainer, GPU, GHCR | 2 Dockerfiles | — | YES — "scientific Python applications" | → #58 |
| documentation-validation | Vale, markdownlint, HTMLProofer, nbval | vale-config.ini, validation-checklist.md | — | Mixed — tools are agnostic, examples are Python | STAYS |
| github-actions | GH Actions CI/CD, matrix, caching, security | 3 workflow YAMLs | — | YES — "scientific Python CI/CD patterns" | → #59 |
| github-org-management | Org audit, health, archival, lifecycle | — | health-metrics.md | NO — fully language-agnostic | → #59 |
| issue-triage | Labels, priority, templates, stale management | 2 issue templates | — | YES — "scientific Python projects" in description | → #59 |
| pre-commit-workflows | Pre-commit hooks, pre-commit.ci, custom hooks | 1 config template | — | YES — "scientific Python projects" | → #59 |
| release-management | SemVer, changelog, PyPI, conda-forge | 2 config files | — | YES — "scientific Python packages" | → #59 |

**Content Size (approximate line counts for SKILL.md files):**
- containerization: ~985 lines
- github-actions: ~1010 lines
- release-management: ~1060 lines
- github-org-management: ~835 lines
- community-health-files: ~600 lines
- documentation-validation: ~500 lines
- issue-triage: ~400 lines
- pre-commit-workflows: ~350 lines

**Key Pattern:** Skills moving to #59 represent ~3,655 lines of content. The containerization skill moving to #58 is ~985 lines. The two staying skills total ~1,100 lines. The plugin is losing roughly 80% of its skill content by volume.

### Finding 4: Complete Command Inventory and Refactoring Fate

**Relevant Files:**
- `plugins/project-management/commands/*.md` — All 7 command definition files

| Command | Frontmatter Description | Language-Specific? | Fate |
|---------|------------------------|-------------------|------|
| audit-github-org | "Audit all repositories in a GitHub organization for health metrics and generate a prioritized report" | NO | → #59 |
| ci-setup | "Generate GitHub Actions CI/CD workflows tailored to a scientific Python project" | YES — "scientific Python project" | → #59 |
| project-handoff | "Assess project readiness for handoff to new maintainers with a comprehensive health check" | NO — methodology is language-agnostic | STAYS |
| release-plan | "Generate a release plan from current milestones, merged PRs, and changelog entries" | YES — detects pyproject.toml, setup.cfg, conda-forge | → #59 |
| setup-project | "Scaffold a new scientific Python project with community health files, CI/CD, and standard structure" | YES — "scientific Python project", creates pyproject.toml, src/ layout | STAYS (needs generalization) |
| triage | "Analyze a GitHub issue and suggest labels, priority, and next steps" | NO — fully language-agnostic | → #59 |
| validate-project-handoff | "Validate project handoff by testing that setup instructions, documentation, and workflows actually work" | NO — methodology is language-agnostic | STAYS |

**Key Pattern:** The three staying commands form a coherent "project lifecycle trio": scaffold (setup-project), assess readiness (project-handoff), and validate (validate-project-handoff). The four moving commands are all GitHub-platform-specific operations.

### Finding 5: Cross-Plugin Dependencies

**Relevant Files:**
- `.claude-plugin/marketplace.json` — Marketplace registration for all plugins
- `plugins/project-management/README.md:60-67` — Integration section

**Key Findings:**

1. **No hardcoded cross-references exist between plugins.** Agent files do not import or reference skills from other plugins. Each plugin is self-contained.

2. **The only explicit cross-plugin documentation** is in the project-management README:
   ```
   ## Integration with Other Plugins

   This plugin works well alongside:
   - **Scientific Python Development** — Use for Python-specific development guidance
   - **AI Research Workflows** — Use /research and /plan for complex tasks
   - **Scientific Domain Applications** — Domain-specific agents reference this plugin's CI/CD and containerization skills
   ```

3. **Implicit overlaps exist** — project-management agents reference `pixi`, `pytest`, and `ruff` which are tools from the scientific-python-development ecosystem, but these are inline references in agent instructions, not formal skill imports.

4. **Plugin.json files contain no dependency declarations.** The plugin manifest format is minimal: name, description, version, author. There is no mechanism for declaring plugin-to-plugin dependencies.

5. **Impact of refactoring on other plugins:** Zero direct impact. No other plugin's agents, skills, or commands reference project-management resources. The README claim that "domain-specific agents reference this plugin's CI/CD and containerization skills" appears to be aspirational rather than implemented.

### Finding 6: Generalization Requirements for Staying Content

Components that stay in project-management need the following changes to become language-agnostic:

#### Agents

**project-onboarding-specialist.md — 6+ locations to generalize:**
- Frontmatter description: "scientific Python project initialization" → "research software project initialization"
- Example: "set up a new Python package for our climate data analysis library" → use language-neutral example
- Body: "scientific Python conventions (src layout)" → "project conventions"
- Body: "Initialize pixi.toml or pyproject.toml" → "Initialize appropriate project configuration"
- Multiple body references to "scientific Python" → "scientific software"

**documentation-validator.md — 3+ locations to generalize:**
- Frontmatter description: "for scientific Python projects" → "for scientific software projects"
- Body references to Python-specific validation (nbval for Jupyter) → keep as one example among others
- Core tools (Vale, HTMLProofer, markdownlint) are already language-agnostic

#### Skills

**community-health-files/SKILL.md:**
- Title: "Community Health Files for Scientific Software Projects" — already close, just remove any Python-specific phrasing
- CONTRIBUTING template: references Python tooling (pip, pytest, ruff) → generalize to language-neutral structure
- README template: may reference Python-specific install instructions → generalize
- CITATION.cff template: already language-agnostic
- CODE_OF_CONDUCT, SECURITY templates: already language-agnostic

**documentation-validation/SKILL.md:**
- Core tools (Vale, markdownlint, HTMLProofer) are language-agnostic — no changes needed
- nbval/notebook testing: note as Python/Jupyter-specific, add alternatives for other ecosystems
- Add mentions of documentation validation in other ecosystems (pkgdown for R, rustdoc for Rust, godoc for Go)
- validation-checklist.md: review for Python-specific items

#### Commands

**setup-project.md — heavy generalization needed:**
- Description: "Scaffold a new scientific Python project" → "Scaffold a new project"
- Currently creates Python-specific structure: pyproject.toml, src/ layout, snake_case conversion
- Should detect project language/type and adapt scaffolding
- Should delegate to GitHub plugin for CI and containerization plugin for Dockerfiles
- Community health file scaffolding (the core responsibility) is already language-agnostic

**project-handoff.md — minimal changes:**
- Assessment methodology is already language-agnostic
- Remove any "scientific Python" phrasing from description

**validate-project-handoff.md — minimal changes:**
- Validation approach (follow README step-by-step) is already language-agnostic
- Remove any "scientific Python" phrasing from description

## Architecture Overview

### Current State (Pre-Refactoring)

```
plugins/project-management/  (current — monolith)
│
├── GITHUB PLATFORM CONCERN          (6 skills, 3 agents, 4 commands)
│   ├── github-actions               ──┐
│   ├── release-management            ──┤
│   ├── github-org-management         ──┤ → GitHub Plugin (#59)
│   ├── issue-triage                  ──┤
│   ├── pre-commit-workflows          ──┤
│   ├── github-workflow-specialist    ──┤
│   ├── github-org-manager            ──┤
│   ├── ci-setup                      ──┤
│   ├── audit-github-org              ──┤
│   ├── release-plan                  ──┤
│   └── triage                        ──┘
│
├── CONTAINERIZATION CONCERN          (1 skill, 1 agent)
│   ├── containerization              ──┐ → Containerization Plugin (#58)
│   └── devops-engineer               ──┘
│
└── PROJECT LIFECYCLE CONCERN         (2 skills, 2 agents, 3 commands)
    ├── community-health-files        ──┐
    ├── documentation-validation      ──┤
    ├── project-onboarding-specialist ──┤ STAYS
    ├── documentation-validator       ──┤
    ├── setup-project                 ──┤
    ├── project-handoff               ──┤
    └── validate-project-handoff      ──┘
```

### Post-Refactoring State

```
plugins/project-management/  (after — focused)
├── .claude-plugin/
│   └── plugin.json                         # Updated description
├── README.md                               # Rewritten
├── LICENSE
├── agents/
│   ├── project-onboarding-specialist.md    # Generalized
│   └── documentation-validator.md          # Generalized
├── skills/
│   ├── community-health-files/             # Minor generalization
│   │   ├── SKILL.md
│   │   └── assets/ (5 templates)
│   └── documentation-validation/           # Minor generalization
│       ├── SKILL.md
│       └── assets/ (2 files)
└── commands/
    ├── setup-project.md                    # Generalized + delegates
    ├── project-handoff.md                  # Minor updates
    └── validate-project-handoff.md         # Minor updates
```

## Component Interactions

### Post-Refactoring Interaction Model

```
                    ┌─────────────────────────────┐
                    │     PROJECT-MANAGEMENT       │
                    │   (Project Lifecycle Focus)   │
                    │                               │
                    │  /setup-project ─────────────────► delegates to GitHub
                    │       │                       │    plugin for CI setup
                    │       └─────────────────────────► delegates to Container
                    │                               │    plugin for Dockerfiles
                    │  /project-handoff             │
                    │       │ checks community files│
                    │       │ checks doc quality    │
                    │       │ checks CI status      │
                    │       └──► handoff report     │
                    │                               │
                    │  /validate-project-handoff    │
                    │       │ follows README steps  │
                    │       │ tests setup works     │
                    │       └──► validation report  │
                    └─────────────────────────────┘
                                │
                    References (not imports):
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌───────────────┐   ┌───────────────────┐   ┌───────────────────┐
│ GitHub Plugin │   │ Containerization  │   │ Sci-Py-Dev Plugin │
│    (#59)      │   │  Plugin (#58)     │   │   (unchanged)     │
│               │   │                   │   │                   │
│ CI/CD setup   │   │ Dockerfile gen    │   │ Python packaging  │
│ Release mgmt  │   │ Singularity/HPC   │   │ Testing patterns  │
│ Org audit     │   │ GPU containers    │   │ Code quality      │
│ Issue triage  │   │ Container security│   │ pixi management   │
└───────────────┘   └───────────────────┘   └───────────────────┘
```

**Key Interaction Changes:**
1. `setup-project` currently scaffolds CI/CD inline → post-refactoring, it delegates to the GitHub plugin's CI setup capability
2. `setup-project` currently creates Dockerfiles inline → post-refactoring, it delegates to the containerization plugin
3. `project-handoff` checks for CI/CD presence but doesn't generate it → no change needed, remains a read-only assessment
4. No other plugin currently references project-management resources → no external breakage

## Technical Decisions

- **Decision:** Extract by concern rather than by language
  - **Rationale:** The three concerns (GitHub platform, containerization, project lifecycle) are orthogonal. A GitHub Actions workflow has nothing to do with documentation validation. Extracting by concern creates focused, cohesive plugins.
  - **Trade-offs:** Creates three plugins where one existed, but each is independently useful and independently installable.

- **Decision:** Keep `community-health-files` in project-management rather than moving to GitHub plugin
  - **Rationale:** Community health files are a project lifecycle concern (onboarding, handoff readiness). The GitHub plugin should own the `.github` repository platform mechanics; project-management owns the template content.
  - **Trade-offs:** Some conceptual overlap since community health files are a GitHub feature, but the template content is universal.

- **Decision:** Generalize to "research software" rather than removing domain focus entirely
  - **Rationale:** The plugin serves RSE organizations. "Research software" is broader than "scientific Python" while retaining the RSE focus. Making it fully generic (e.g., "any software project") would dilute the value proposition.
  - **Trade-offs:** Still somewhat niche, but accurately reflects the target audience.

- **Decision:** `setup-project` delegates to other plugins rather than duplicating their capabilities
  - **Rationale:** Avoids content duplication and keeps each plugin authoritative for its domain. setup-project focuses on what it does best (community files, project structure) and recommends other plugins for CI and containerization.
  - **Trade-offs:** Users need multiple plugins installed for the full setup experience, but each plugin works standalone.

## Dependencies and Integrations

**Internal Dependencies (within project-management):**
- `project-onboarding-specialist` agent → references `community-health-files` and `documentation-validation` skills
- `documentation-validator` agent → references `documentation-validation` and `community-health-files` skills
- All staying components reference only other staying components — no dangling references after extraction

**External Dependencies (tools):**
- **Git:** Repository operations (all commands)
- **GitHub CLI (`gh`):** Used by `project-handoff` to check repo status. May become optional if handoff assessment doesn't require GitHub API calls.
- **Vale:** Documentation linting (documentation-validation skill, optional)
- **markdownlint:** Markdown quality (documentation-validation skill, optional)
- **HTMLProofer:** Link validation (documentation-validation skill, optional)

**Cross-Plugin References (post-refactoring):**
- `setup-project` will recommend (not require) the GitHub plugin for CI setup
- `setup-project` will recommend (not require) the containerization plugin for Dockerfiles
- README will document "Related Plugins" pointing to #58 and #59
- No formal dependency mechanism exists in plugin.json

## Edge Cases and Constraints

- **Plugin.json has no dependency mechanism.** There is no way to declare that project-management "recommends" the GitHub plugin. This is documentation-only.
- **Marketplace.json needs updating** after refactoring to add the two new plugins and update the project-management entry.
- **Skills moving out reference `community-health-files`.** The `github-org-manager` agent references both `github-org-management` and `community-health-files`. When it moves to the GitHub plugin, it loses access to the `community-health-files` skill that stays behind. The GitHub plugin will need its own version of community health guidance focused on platform mechanics.
- **Ordering matters.** Issue #60 specifies: build #58 first, then #59, then refactor project-management. This prevents a period where content exists in neither location.
- **Validation workflow** (`.github/workflows/validate-plugins.yml`) will need to validate the new plugin structures.

## Open Questions

1. **Should `community-health-files` be duplicated or shared?** The `github-org-manager` agent (moving to #59) currently references this skill. Should the GitHub plugin get its own community health skill, or should there be a mechanism for cross-plugin skill sharing?

2. **How should `setup-project` detect project language?** Currently hardcoded to Python (pyproject.toml, src/ layout). After generalization, what heuristics should it use? Presence of package.json, Cargo.toml, go.mod, DESCRIPTION (R), Project.toml (Julia)?

3. **Should the plugin name change?** "project-management" is broad. After refactoring, "project-lifecycle" or "project-onboarding" might be more accurate. However, renaming has ecosystem-wide implications (marketplace, user documentation, cached installations).

4. **What happens to users who installed the monolithic plugin?** Users who depend on `/ci-setup` or `/triage` commands will lose them when the plugin is refactored. Migration guidance is needed.

5. **Should `project-handoff` and `validate-project-handoff` check for the presence of CI/CD (a GitHub plugin concern)?** These commands currently verify that CI passes and configuration exists. Post-refactoring, this creates a soft dependency on the GitHub plugin's domain.

## References

**Files Analyzed:** 27 files
- `plugins/project-management/.claude-plugin/plugin.json`
- `plugins/project-management/README.md`
- `plugins/project-management/agents/devops-engineer.md`
- `plugins/project-management/agents/documentation-validator.md`
- `plugins/project-management/agents/github-org-manager.md`
- `plugins/project-management/agents/github-workflow-specialist.md`
- `plugins/project-management/agents/project-onboarding-specialist.md`
- `plugins/project-management/skills/community-health-files/SKILL.md`
- `plugins/project-management/skills/containerization/SKILL.md`
- `plugins/project-management/skills/documentation-validation/SKILL.md`
- `plugins/project-management/skills/github-actions/SKILL.md`
- `plugins/project-management/skills/github-org-management/SKILL.md`
- `plugins/project-management/skills/issue-triage/SKILL.md`
- `plugins/project-management/skills/pre-commit-workflows/SKILL.md`
- `plugins/project-management/skills/release-management/SKILL.md`
- `plugins/project-management/commands/audit-github-org.md`
- `plugins/project-management/commands/ci-setup.md`
- `plugins/project-management/commands/project-handoff.md`
- `plugins/project-management/commands/release-plan.md`
- `plugins/project-management/commands/setup-project.md`
- `plugins/project-management/commands/triage.md`
- `plugins/project-management/commands/validate-project-handoff.md`
- `.claude-plugin/marketplace.json`
- `plugins/scientific-python-development/.claude-plugin/plugin.json`
- `plugins/scientific-domain-applications/.claude-plugin/plugin.json`
- `plugins/ai-research-workflows/.claude-plugin/plugin.json`
- `.agents/research-plugin-gap-analysis.md`

**GitHub Issues:**
- [#58 — feat: Create language-agnostic Containerization plugin](https://github.com/uw-ssec/rse-plugins/issues/58)
- [#59 — feat: Create language-agnostic GitHub plugin for RSE power users](https://github.com/uw-ssec/rse-plugins/issues/59)
- [#60 — refactor: Refocus project-management plugin on project lifecycle](https://github.com/uw-ssec/rse-plugins/issues/60)

---

## Update History

### Update 2026-02-26 — Refactoring analysis per issue #60

**Context:** Issues #58, #59, and #60 were created to decompose the monolithic project-management plugin into three focused, language-agnostic plugins. This update replaces the original pre-implementation research (2026-02-17) with a current-state analysis and refactoring plan.

**Key changes from original research:**
- The plugin now exists and is fully built (the original research was pre-implementation)
- Three extraction issues have been filed with detailed separation-of-concerns plans
- Every component has been classified by refactoring fate with specific generalization requirements
- Cross-plugin dependencies have been mapped (found to be zero hardcoded references)
- Post-refactoring architecture has been documented

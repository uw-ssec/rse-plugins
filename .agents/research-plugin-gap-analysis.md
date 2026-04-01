# Research: Plugin Gap Analysis — Agents, Skills, and Commands for New Plugins

---
**Date:** 2026-02-19
**Author:** AI Assistant
**Status:** Active
**Related Documents:** None (initial research)

---

## Research Question

What other agents, skills, and commands could and should be included as new plugins in the RSE Plugins repository, given the existing ecosystem and the repository's mission of supporting Research Software Engineering and Scientific Computing?

## Executive Summary

The RSE Plugins repository currently contains **4 plugins** (3 core + 1 community) providing **8 agents** and **17 skills** across scientific Python development, astronomical domain applications, AI-assisted development workflows, and HoloViz data visualization. Coverage is strong in visualization (9 skills, 4 agents) and Python development tooling (5 skills, 2 agents), but significant gaps exist across multiple dimensions of the Research Software Engineering lifecycle.

The most impactful gaps fall into six broad categories: **(1) Scientific Domain Expansion** — the domain-applications plugin only covers astronomy and xarray, leaving major scientific domains (biology, chemistry, Earth science, social sciences) without dedicated agents or skills; **(2) Data Engineering & Management** — no coverage for data pipelines, databases, data formats beyond FITS/NetCDF, or data validation; **(3) DevOps & Infrastructure** — no CI/CD, containerization, cloud computing, or HPC skills despite these being core to modern RSE; **(4) Collaboration & Community** — no coverage for open-source project management, code review, community building, or contribution workflows; **(5) Machine Learning & AI for Science** — no agents for scientific ML, model training, or experiment tracking despite ML being pervasive in research; **(6) Reproducibility & FAIR Data** — no dedicated coverage for reproducibility beyond pixi, research data management, or FAIR principles.

The branch name `cdcore09/feat/project-management` suggests a project management plugin is being developed, which would address gap category #4 and is a high-priority addition given that open-source project management is central to the RSE mission.

## Scope

**What This Research Covers:**
- Complete inventory of existing plugins, agents, skills, and commands
- Analysis of coverage density and thematic gaps
- Identification of missing capabilities relative to the RSE and scientific computing mission
- Prioritized recommendations for new plugins, agents, and skills
- Pattern analysis of how existing plugins are structured

**What This Research Does NOT Cover:**
- Implementation details for proposed new plugins
- Comparison with competing plugin ecosystems
- User demand analysis or survey data
- Cost/effort estimation for building new plugins

## Key Findings

### Finding 1: Current Ecosystem Inventory

The existing ecosystem consists of 4 plugins with the following coverage:

| Plugin | Category | Agents | Skills | Commands | MCP |
|--------|----------|--------|--------|----------|-----|
| scientific-python-development | Core | 2 | 5 | 0 | No |
| scientific-domain-applications | Core | 1 | 2 | 0 | No |
| ai-research-workflows | Core | 1 | 1 | 6 | No |
| holoviz-visualization | Community | 4 | 9 | 0 | Yes |
| **TOTAL** | | **8** | **17** | **6** | **1** |

**Relevant Files:**
- `.claude-plugin/marketplace.json` — Marketplace configuration listing all 4 plugins
- `plugins/scientific-python-development/.claude-plugin/plugin.json` — SciPy dev plugin manifest
- `plugins/scientific-domain-applications/.claude-plugin/plugin.json` — Domain apps manifest
- `plugins/ai-research-workflows/.claude-plugin/plugin.json` — Workflows manifest
- `community-plugins/holoviz-visualization/.claude-plugin/plugin.json` — HoloViz manifest

**Key Patterns:**
- Skills are the primary unit of knowledge, agents orchestrate skills
- The ai-research-workflows plugin is the only one with slash commands
- Only holoviz-visualization uses MCP integration (Docker-based doc server)
- All skills follow a consistent structure: `SKILL.md` + optional `assets/`, `references/`, `scripts/`

### Finding 2: Coverage Density Analysis

Coverage is unevenly distributed across the RSE lifecycle:

```
RSE Lifecycle Stage          | Coverage Level | Plugins/Skills
-----------------------------|----------------|---------------------------
Environment Setup            | Strong         | pixi-package-manager
Development (Python)         | Strong         | python-packaging, code-quality-tools, python-testing
Documentation                | Strong         | scientific-documentation, scientific-docs-architect
Data Visualization           | Very Strong    | 9 HoloViz skills + 4 agents
Domain Science (Astronomy)   | Strong         | astronomy-astrophysics-expert, astropy-fundamentals
Domain Science (Climate)     | Moderate       | xarray-for-multidimensional-data
Development Workflow         | Strong         | ai-research-workflows (6 commands)
CI/CD & DevOps               | NONE           | —
Data Engineering             | NONE           | —
Machine Learning             | NONE           | —
HPC & Cloud                  | NONE           | —
Reproducibility/FAIR         | Weak           | (only pixi lockfiles)
Project Management           | NONE           | —
Community/Collaboration      | NONE           | —
Domain Science (Bio/Chem)    | NONE           | —
Domain Science (Earth/Geo)   | NONE           | (only xarray)
Security & Compliance        | NONE           | —
```

### Finding 3: Existing Plugin Design Patterns

All plugins follow consistent conventions that new plugins should emulate:

**Agent Pattern (from `plugins/scientific-python-development/agents/scientific-python-expert.md`):**
- YAML frontmatter: `name`, `description`, `model: inherit`, `color`, `skills` list
- Sections: Profile, Core Competencies, Specialized Knowledge, Problem-Solving, When to Use, Integration with Other Agents
- Behavioral constraints (DO/DON'T lists)
- Decision framework for handling requests
- Self-review checklist
- Completion criteria

**Skill Pattern (from all 17 SKILL.md files):**
- YAML frontmatter: `name`, `description`, `version`, dependency info
- Triggers/invocation patterns
- Reference material organized by subtopic
- Code examples with specific library versions
- Assets directory for templates and configs

**Command Pattern (from `plugins/ai-research-workflows/commands/`):**
- Markdown files defining command behavior
- Template-driven output (research, plan, experiment, implement templates)
- Output written to `.agents/` directory
- Cross-referencing between workflow stages

## Gap Analysis: Recommended New Plugins

### Priority 1: Project Management Plugin (In Progress)

**Rationale:** The branch name `cdcore09/feat/project-management` suggests this is already being developed. Project management is a critical gap — RSE teams need tools for managing open-source projects, tracking issues, coordinating contributors, and planning releases.

**Suggested Agents:**
| Agent | Purpose |
|-------|---------|
| `project-manager` | Orchestrator for open-source project management — issue triage, milestone planning, release coordination, contributor management |
| `github-workflow-specialist` | Expert in GitHub-specific workflows — Actions CI/CD, issue/PR templates, project boards, release automation, branch protection strategies |

**Suggested Skills:**
| Skill | Purpose |
|-------|---------|
| `github-project-management` | GitHub Projects, milestones, labels, issue templates, PR workflows |
| `release-management` | Semantic versioning, changelogs (towncrier, auto-changelog), release workflows, PyPI/conda-forge publishing |
| `community-building` | CONTRIBUTING.md patterns, CODE_OF_CONDUCT, governance models, onboarding, mentoring new contributors |
| `issue-triage` | Issue labeling strategies, bug vs. feature classification, priority assignment, stale issue management |

**Suggested Commands:**
| Command | Purpose |
|---------|---------|
| `/triage [issue-url]` | Analyze a GitHub issue and suggest labels, priority, and assignment |
| `/release-plan` | Generate a release plan based on current milestones and unreleased changes |
| `/health-check` | Audit repository health — CI status, stale issues, documentation coverage, dependency freshness |

---

### Priority 2: CI/CD & DevOps Plugin

**Rationale:** CI/CD is fundamental to modern RSE yet completely absent from the repository. Every scientific Python project needs CI configuration, and the patterns are complex enough to warrant dedicated skills.

**Suggested Agents:**
| Agent | Purpose |
|-------|---------|
| `devops-engineer` | Expert in CI/CD pipelines, containerization, and deployment for scientific software |

**Suggested Skills:**
| Skill | Purpose |
|-------|---------|
| `github-actions` | Workflow YAML authoring, matrix testing (Python versions, OS), caching, secrets management, reusable workflows |
| `containerization` | Docker/Podman for scientific software, multi-stage builds, conda-pack/pixi in containers, GPU containers, Singularity/Apptainer for HPC |
| `pre-commit-workflows` | Pre-commit hook configuration, custom hooks for scientific code, CI integration with pre-commit.ci |
| `cloud-computing` | AWS/GCP/Azure patterns for scientific workloads, S3/GCS data access, Jupyter on cloud, cost management |

**Suggested Commands:**
| Command | Purpose |
|---------|---------|
| `/ci-setup [framework]` | Generate CI configuration for a scientific Python project |
| `/docker-setup` | Generate Dockerfile optimized for scientific Python dependencies |

---

### Priority 3: Data Engineering & Management Plugin

**Rationale:** Scientific projects increasingly involve complex data pipelines, data validation, and multiple storage formats. The current repository only covers FITS (astronomy) and NetCDF/Zarr (xarray) but lacks general data engineering capabilities.

**Suggested Agents:**
| Agent | Purpose |
|-------|---------|
| `data-pipeline-architect` | Expert in scientific data pipeline design, ETL workflows, data validation, and storage optimization |

**Suggested Skills:**
| Skill | Purpose |
|-------|---------|
| `data-validation` | Pandera, Great Expectations, Pydantic for scientific data validation, schema definition, data quality checks |
| `data-formats` | Parquet, Arrow, HDF5, Zarr, CSV best practices, format conversion, chunking strategies, compression |
| `database-fundamentals` | SQLite, PostgreSQL, DuckDB for scientific data, spatial databases (PostGIS), time-series databases |
| `data-pipelines` | Prefect, Luigi, Snakemake for scientific workflows, DAG-based pipeline design, checkpointing, provenance tracking |

**Suggested Commands:**
| Command | Purpose |
|---------|---------|
| `/validate-data [schema]` | Generate data validation code for a dataset |
| `/convert-data [from] [to]` | Guide for converting between scientific data formats |

---

### Priority 4: Scientific Machine Learning Plugin

**Rationale:** ML is now pervasive in scientific research. No existing plugin covers model training, experiment tracking, or scientific ML frameworks. This is a large and growing need.

**Suggested Agents:**
| Agent | Purpose |
|-------|---------|
| `scientific-ml-engineer` | Expert in applying ML to scientific problems — scikit-learn, PyTorch, JAX, experiment tracking, model evaluation |

**Suggested Skills:**
| Skill | Purpose |
|-------|---------|
| `scikit-learn-workflows` | Classification, regression, clustering for scientific data, cross-validation, feature engineering, pipeline construction |
| `deep-learning-frameworks` | PyTorch, JAX, TensorFlow patterns for scientific applications (physics-informed NNs, graph NNs, generative models) |
| `experiment-tracking` | MLflow, Weights & Biases, DVC for experiment management, model versioning, hyperparameter tracking |
| `model-evaluation` | Scientific model evaluation — cross-validation strategies, uncertainty quantification, calibration, domain-specific metrics |

---

### Priority 5: Expanded Scientific Domain Plugins

**Rationale:** The scientific-domain-applications plugin only covers astronomy (1 agent, 1 skill) and xarray. Many other scientific domains have large Python ecosystems that would benefit from dedicated agents and skills.

**Suggested new skills for the existing scientific-domain-applications plugin:**

| Skill | Domain | Key Libraries |
|-------|--------|---------------|
| `biopython-fundamentals` | Biology/Bioinformatics | BioPython, sequence analysis, BLAST, phylogenetics |
| `rdkit-chemistry` | Chemistry/Cheminformatics | RDKit, molecular visualization, property prediction |
| `scipy-signal-processing` | Signal Processing | SciPy signal, filtering, spectral analysis, time-frequency |
| `geospatial-analysis` | Earth Science | GeoPandas, Rasterio, Fiona, Shapely, GDAL beyond what GeoViews covers |
| `climate-modeling` | Climate Science | CMIP data, climate indices, ESMValTool, cf-conventions |
| `image-analysis` | Microscopy/Medical | scikit-image, napari, cell segmentation, DICOM |

**Suggested new agents:**

| Agent | Domain |
|-------|--------|
| `bioinformatics-expert` | Genomics, sequence analysis, phylogenetics |
| `earth-science-expert` | Geospatial, climate, meteorological analysis |
| `computational-chemistry-expert` | Molecular modeling, cheminformatics |

---

### Priority 6: Reproducibility & FAIR Data Plugin

**Rationale:** Reproducibility is a cornerstone of scientific computing. While pixi handles environment reproducibility, there's no coverage for broader research reproducibility, FAIR data principles, or provenance tracking.

**Suggested Skills:**
| Skill | Purpose |
|-------|---------|
| `reproducible-research` | Reproducibility best practices, seed management, environment capture, provenance tracking |
| `fair-data-principles` | Findable, Accessible, Interoperable, Reusable data — metadata standards, DOIs, data repositories |
| `literate-programming` | Jupyter notebooks best practices, MyST-NB, Jupyter Book, parameterized notebooks (Papermill) |
| `research-data-management` | Data management plans, institutional repositories, Zenodo/Figshare integration, data citation |

---

### Priority 7: HPC & Parallel Computing Plugin

**Rationale:** High-Performance Computing is central to many scientific workflows. The CONTRIBUTING.md even lists "scientific-computing/HPC" as a planned category, but no skills exist for it.

**Suggested Agents:**
| Agent | Purpose |
|-------|---------|
| `hpc-specialist` | Expert in HPC workflows, job schedulers, parallel programming, performance optimization |

**Suggested Skills:**
| Skill | Purpose |
|-------|---------|
| `parallel-computing` | Dask, multiprocessing, concurrent.futures, joblib for scientific parallel workloads |
| `hpc-job-management` | SLURM, PBS, LSF job scripts, resource estimation, array jobs, job dependencies |
| `performance-optimization` | Profiling (cProfile, line_profiler), Numba JIT, Cython, memory optimization for scientific code |
| `gpu-computing` | CuPy, RAPIDS, JAX GPU, PyTorch GPU for scientific computing |

---

### Priority 8: Security & Compliance Plugin

**Rationale:** Security is increasingly important for research software, especially with sensitive data (medical, genomic, personally identifiable). No coverage exists.

**Suggested Skills:**
| Skill | Purpose |
|-------|---------|
| `dependency-security` | Dependabot, safety, pip-audit, vulnerability scanning, supply chain security |
| `secrets-management` | Environment variables, vault systems, credential handling in scientific workflows |
| `data-privacy` | Anonymization, de-identification, HIPAA/FERPA basics for research data |

---

## Architecture Overview

The gap analysis reveals the current ecosystem focuses on a "build and visualize" workflow:

```
Current Coverage:

  [Environment]  ->  [Code]  ->  [Test]  ->  [Document]  ->  [Visualize]
   pixi              packaging    testing    docs              HoloViz (9 skills)
                     quality

  [Domain Science]              [Workflow]
   astronomy                     research/plan/implement/validate
   xarray/climate

Missing Coverage:

  [Project Mgmt]  ->  [CI/CD]  ->  [Deploy]  ->  [Monitor]
   issues/releases    GitHub Actions  containers   metrics
   triage             pre-commit      cloud

  [Data Engineering]  ->  [ML/AI]  ->  [Reproduce]
   pipelines             scikit-learn   FAIR data
   validation            deep learning  provenance
   databases             experiment     literate prog
   formats               tracking

  [HPC/Parallel]      [Security]      [More Domains]
   Dask/SLURM          dep scanning    biology
   GPU computing        secrets         chemistry
   profiling            privacy         earth science
```

## Technical Decisions

- **Decision:** Prioritize project management plugin first (already in development)
  - **Rationale:** Branch name suggests it's actively being built; addresses collaboration gap
  - **Trade-offs:** Enables better community engagement before expanding domain coverage

- **Decision:** CI/CD should be a separate plugin rather than added to scientific-python-development
  - **Rationale:** CI/CD is cross-cutting — used by all scientific domains, not just Python development
  - **Trade-offs:** More plugins to maintain, but cleaner separation of concerns

- **Decision:** Expand scientific-domain-applications rather than creating separate domain plugins
  - **Rationale:** Keeps domain skills consolidated; follows existing pattern of one agent per domain
  - **Trade-offs:** Plugin could grow large, but domains share common patterns (data I/O, units, validation)

- **Decision:** ML/AI warrants its own plugin separate from domain applications
  - **Rationale:** ML is a methodology, not a domain — it's used across all scientific fields
  - **Trade-offs:** Some overlap with domain-specific ML, but cleaner for generalist ML workflows

## Dependencies and Integrations

Each proposed plugin would integrate with the existing ecosystem:

- **All new plugins** should follow the agent/skill/command pattern established by ai-research-workflows
- **Project management plugin** integrates with GitHub CLI (`gh`) for issue/PR automation
- **CI/CD plugin** would reference pixi-package-manager and python-testing skills from the existing ecosystem
- **Data engineering plugin** would complement xarray-for-multidimensional-data
- **ML plugin** would build on scientific-python-expert patterns for reproducible code
- **HPC plugin** would integrate with pixi for environment management on clusters

## Edge Cases and Constraints

- The repository uses BSD-3-Clause license, which limits inclusion of GPL-dependent tool guidance
- Some proposed domains (bioinformatics, chemistry) have very large ecosystems — scoping is important
- MCP integration (as used by holoviz-visualization) could enhance new plugins but adds Docker dependency
- Community plugins vs. core plugins: Domain expansions might work better as community contributions
- The CONTRIBUTING.md mentions categories (`scientific-computing/`, `data-science/`, `research-tools/`, `domain-specific/`) that don't match the actual directory structure — this should be reconciled

## Open Questions

1. **What is the scope of the project-management plugin being developed on `cdcore09/feat/project-management`?** Understanding what's already planned helps avoid duplication in recommendations.
2. **Should domain expansions (bio, chem, earth science) be core plugins or community plugins?** The holoviz-visualization precedent suggests community is appropriate for large ecosystem-specific plugins.
3. **Is MCP integration desired for new plugins?** The holoviz-visualization plugin uses Docker-based MCP — should new plugins follow this pattern for dynamic documentation access?
4. **What is the priority order among these gaps?** The analysis prioritizes by estimated impact to the RSE mission, but actual user needs may differ.
5. **Should the ai-research-workflows command pattern be adopted by other plugins?** Currently only one plugin has slash commands — expanding this pattern could improve discoverability.

## References

- Files analyzed: 25+ files across the repository
  - `.claude-plugin/marketplace.json`
  - `plugins/scientific-python-development/.claude-plugin/plugin.json`
  - `plugins/scientific-python-development/agents/scientific-python-expert.md`
  - `plugins/scientific-python-development/agents/scientific-docs-architect.md`
  - `plugins/scientific-python-development/skills/*/SKILL.md` (5 files)
  - `plugins/scientific-domain-applications/.claude-plugin/plugin.json`
  - `plugins/scientific-domain-applications/agents/astronomy-astrophysics-expert.md`
  - `plugins/scientific-domain-applications/skills/*/SKILL.md` (2 files)
  - `plugins/ai-research-workflows/.claude-plugin/plugin.json`
  - `plugins/ai-research-workflows/agents/research-workflow-orchestrator.md`
  - `plugins/ai-research-workflows/skills/research-workflow-management/SKILL.md`
  - `community-plugins/holoviz-visualization/.claude-plugin/plugin.json`
  - `community-plugins/holoviz-visualization/.mcp.json`
  - `community-plugins/holoviz-visualization/agents/*.md` (4 files)
  - `community-plugins/holoviz-visualization/skills/*/SKILL.md` (9 files)
  - `README.md`
  - `CONTRIBUTING.md`

- Related documentation:
  - [Scientific Python Development Guide](https://learn.scientific-python.org/development/)
  - [Claude Code Plugin Documentation](https://docs.anthropic.com/claude/docs)
  - [Best Practices for Scientific Computing](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1001745)

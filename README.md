# RSE Plugins

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/uw-ssec/rse-plugins?quickstart=1)

Custom AI agents and skills for Research Software Engineering (RSE) and Scientific Computing tasks, designed for use with [Claude Code](https://www.anthropic.com/claude/code) and compatible AI coding assistants.

## GitHub Codespaces

Click the badge above to open a Codespace with all RSE plugins pre-installed. Claude Code and GitHub Copilot CLI are ready to use immediately.

### Using a LiteLLM Gateway (Optional)

To route Copilot through a custom LiteLLM-compatible gateway, you need to set two secrets. Because GitHub Codespaces secrets can only be scoped to repos you own, follow these steps:

1. **Fork this repo** — Click **Fork** on [github.com/uw-ssec/rse-plugins](https://github.com/uw-ssec/rse-plugins).
2. **Add secrets** — Go to your GitHub account settings: **Settings → Codespaces → Secrets**, then add:
   - `LITELLM_BASE_URL` — your gateway base URL
   - `LITELLM_API_KEY` — your gateway API key
   - When adding each secret, under **Repository access**, select your fork.
3. **Open a Codespace from your fork** — Go to your fork on GitHub and click **Code → Codespaces → Create codespace on main**.

The Codespace will automatically detect the secrets and configure Copilot to route through your gateway.

## Purpose

This repository provides specialized agents and skills that understand the unique challenges of scientific software development, including:

- Modern Scientific Python development following community best practices
- Reproducible environment management with pixi
- Python packaging and distribution with pyproject.toml
- Comprehensive testing strategies with pytest
- Scientific computing workflows and numerical methods
- Research software engineering practices
- Domain-specific scientific computing (astronomy, geospatial analysis, climate science)
- Interactive data visualization with the HoloViz ecosystem (Panel, hvPlot, HoloViews, Datashader, GeoViews, Lumen)
- Scientific Python ecosystem (NumPy, Pandas, SciPy, Matplotlib, Xarray, Astropy, etc.)

## Installation

Each plugin follows the [Agent Plugins](https://agent-plugins.org/specification) v1.0.0 format. It has a portable `plugin.json` at the plugin root, plus client-specific files for the clients that need them. Skills work in every client below. Agents, commands and MCP servers are client-specific, and not every client loads them:

| Client | Install from | Skills | Agents | Commands | HoloViz MCP |
| --- | --- | --- | --- | --- | --- |
| Claude Code | marketplace | ✅ | ✅ | ✅ | ✅ |
| GitHub Copilot CLI | marketplace | ✅ | 🚧 [#240](https://github.com/uw-ssec/rse-plugins/issues/240) | 🚧 [#240](https://github.com/uw-ssec/rse-plugins/issues/240) | ✅ |
| VS Code (Copilot) | marketplace setting | 🟡 | 🚧 [#240](https://github.com/uw-ssec/rse-plugins/issues/240) | 🚧 [#240](https://github.com/uw-ssec/rse-plugins/issues/240) | ❔ |
| Codex | marketplace | ✅ | ❌ | ❌ | ✅ |
| Cursor | local folder | 🟡 | ❌ | ❌ | 🟡 |
| OpenCode | copied skills | ✅ | ❌ | ❌ | 🔧 `opencode.json` |

✅ Verified · 🟡 Expected, untested · ❔ Unknown · 🚧 Planned ([#240](https://github.com/uw-ssec/rse-plugins/issues/240)) · ❌ Unsupported · 🔧 Manual setup

🟡 cells follow the client's documentation but haven't been run against this repository. For MCP, ✅ means the client found the server configuration; the server itself wasn't started.

Replace `scientific-python-development` in the examples below with any plugin from [Available Plugins](#available-plugins).

### Claude Code

```bash
claude plugin marketplace add uw-ssec/rse-plugins
claude plugin install scientific-python-development@rse-plugins
```

Inside Claude Code, the same commands are `/plugin marketplace add uw-ssec/rse-plugins` and `/plugin install scientific-python-development@rse-plugins`. Claude Code reads `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`.

### GitHub Copilot CLI

```bash
copilot plugin marketplace add uw-ssec/rse-plugins
copilot plugin install scientific-python-development@rse-plugins
```

Copilot reads the root `plugin.json` and the marketplace in `.claude-plugin/marketplace.json`, and loads each plugin's skills and MCP servers. It doesn't load our agents or commands yet: those are written for Claude Code, and Copilot-format versions for Copilot CLI and VS Code are tracked in [#240](https://github.com/uw-ssec/rse-plugins/issues/240). The [Codespace](#github-codespaces) installs every plugin this way.

### Codex

```bash
codex plugin marketplace add uw-ssec/rse-plugins
codex plugin add scientific-python-development@rse-plugins
```

Codex loads skills and MCP servers. It doesn't load agents or commands.

### Cursor

Cursor's public marketplace is curated, so this repository isn't listed there. To use a plugin, copy it into Cursor's local plugin folder. Cursor skips symlinks that point outside that folder, so copy rather than link:

```bash
git clone https://github.com/uw-ssec/rse-plugins.git
mkdir -p ~/.cursor/plugins/local
cp -R rse-plugins/plugins/scientific-python-development ~/.cursor/plugins/local/
```

Then restart Cursor (or run **Developer: Reload Window**), and check the plugin's skills and MCP servers under **Customize**. Cursor loads each plugin as an Agent Plugin, which means skills and MCP servers only. Our agents and commands use Claude Code's format, so Cursor doesn't load them. Teams and Enterprise plans can also add the repository to a team marketplace (`.cursor-plugin/marketplace.json`) instead of copying. See [Cursor plugins](https://cursor.com/docs/plugins). These steps follow Cursor's documentation; they haven't been tested.

### OpenCode

OpenCode doesn't install plugin packages, but it discovers skills. Copy the skills you want into a skills directory, either globally (`~/.config/opencode/skills/`) or in a project (`.agents/skills/` or `.opencode/skills/`):

```bash
git clone https://github.com/uw-ssec/rse-plugins.git
mkdir -p ~/.config/opencode/skills
cp -R rse-plugins/plugins/scientific-python-development/skills/* ~/.config/opencode/skills/
```

The same copy works for any client that reads a skills directory, such as `~/.agents/skills/`. Agents and commands aren't available in OpenCode. To use the HoloViz MCP server, add it to your `opencode.json` yourself:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "holoviz-mcp": {
      "type": "local",
      "command": ["docker", "run", "-i", "--rm", "-v", "holoviz-mcp:/root/.holoviz-mcp", "ghcr.io/marcskovmadsen/holoviz-mcp:latest"]
    }
  }
}
```

### VS Code

To configure plugin marketplaces in VS Code, use the `chat.plugins.marketplaces` setting.

Here's an example that can be added to the `settings.json` file.

```json
"chat.plugins.marketplaces": [
    "uw-ssec/rse-plugins"
]
```

([Documentation link](https://code.visualstudio.com/docs/agent-customization/agent-plugins#_configure-plugin-marketplaces))

## Available Plugins

The repository provides Claude Code plugins organized by domain. Each plugin contains agents (specialized AI personas) and skills (reusable knowledge modules).

### Scientific Python Development Plugin

Expert agents and comprehensive skills for modern Scientific Python development.

**Agents:**
- **Scientific Python Expert** - Comprehensive agent for scientific Python development following [Scientific Python Development Guide](https://learn.scientific-python.org/development/) best practices
- **Scientific Documentation Architect** - Expert in creating comprehensive, user-friendly documentation for scientific software following Scientific Python community standards

**Skills:**
- **pixi-package-manager** - Fast, reproducible scientific Python environments with unified conda and PyPI management
- **python-packaging** - Modern packaging with pyproject.toml, src layout, and Hatchling build backend
- **python-testing** - Robust testing strategies with pytest following Scientific Python community guidelines
- **code-quality-tools** - Linting, formatting, and type checking tools for Python code quality
- **scientific-documentation** - Documentation best practices for scientific software including Sphinx, API docs, tutorials, and examples

**When to use:** Scientific computing projects, data analysis pipelines, research software development, package creation, reproducible research workflows

### Scientific Domain Applications Plugin

Domain-specific scientific computing agents and skills for astronomy, geospatial analysis, climate science, and interactive visualization.

**Agents:**
- **Astronomy & Astrophysics Expert** - Expert in astronomical data analysis, FITS files, coordinate systems, and photometry/spectroscopy pipelines with Astropy

**Skills:**
- **xarray-for-multidimensional-data** - Work with labeled multidimensional arrays and NetCDF/Zarr datasets for climate and Earth science
- **astropy-fundamentals** - Astronomical data formats, coordinate transformations, physical units, and time handling with Astropy

**When to use:** Astronomy research, telescope data processing, climate data analysis, Earth science workflows, geospatial analysis

### AI Research Workflows Plugin

Skills-first research workflows for Research Software Engineers and researchers — covering the full arc from understanding code and surveying prior art through planning, experimentation, implementation, validation, reproducibility, and handoff.

**Agent:**
- **Research Workflow Orchestrator** - Guides users through structured development workflows from research to validated implementation

**Commands:**
- `/research` - Document how existing code works
- `/plan` - Create a phased implementation plan
- `/iterate-plan` - Revise an existing plan
- `/experiment` - Compare approaches with real prototype code
- `/implement` - Execute an approved plan phase by phase
- `/validate` - Verify implementation against plan criteria
- `/handoff` - Write a context-transfer document
- `/prior-art` - Survey tools, papers, and methods outside the codebase
- `/reproduce` - Capture provenance so a result can be reproduced
- `/harden` - Add correctness and regression tests to research code

**Skills (11):**
- **using-research-workflows** (meta), **researching-codebases**, **planning-implementations**, **iterating-plans**, **running-experiments**, **implementing-plans**, **validating-implementations**, **creating-handoffs**, **researching-prior-art**, **ensuring-reproducibility**, **hardening-research-code**

**When to use:** Complex feature development, architectural changes, exploratory implementation, prior-art surveys, reproducibility capture, research code hardening, context-transfer handoffs

### Project Management Plugin

Project lifecycle management — onboarding, documentation quality, handoff readiness, and community health for research software projects in any language.

**Agents:**
- **Project Onboarding Specialist** - Expert in project initialization, contributor onboarding, and knowledge transfer
- **Documentation Validator** - Expert in documentation quality assurance, setup instruction validation, and completeness checking

**Commands:**
- `/setup-project` - Scaffold a new project with community health files and standard structure
- `/project-handoff` - Assess project readiness for handoff to new maintainers
- `/validate-project-handoff` - Test that setup instructions and documentation actually work

**Skills:**
- **community-health-files** - Templates for README, CONTRIBUTING, LICENSE, CODE_OF_CONDUCT, SECURITY, and CITATION.cff
- **documentation-validation** - Validation tools (Vale, markdownlint, HTMLProofer) and documentation quality metrics

**When to use:** Project initialization, onboarding documentation, project handoff, documentation quality auditing, community health file creation

### HoloViz Visualization Plugin

Expert agents and comprehensive skills for interactive data visualization using the HoloViz ecosystem (Panel, hvPlot, HoloViews, Datashader, GeoViews, Lumen).

**Agents:**
- **Panel Specialist** - Expert in building interactive dashboards, web applications, and component systems with Panel and Param
- **Visualization Designer** - Strategic guide for multi-library visualization design using HoloViz ecosystem tools
- **Data Engineer** - Specialist in large-scale data rendering and performance optimization with Datashader (100M+ points)
- **Geo-Spatial Expert** - Expert in geographic and mapping visualizations with GeoViews and spatial data handling

**Skills:**
- **panel-dashboards** - Interactive dashboard and application development with Panel and Param
- **plotting-fundamentals** - Quick plotting and interactive visualization with hvPlot
- **data-visualization** - Advanced declarative visualization with HoloViews
- **advanced-rendering** - High-performance rendering for large datasets with Datashader
- **geospatial-visualization** - Geographic and mapping visualizations with GeoViews
- **colormaps-styling** - Color management and visual styling with Colorcet
- **parameterization** - Declarative parameter systems with Param for type-safe configuration
- **lumen-dashboards** - Declarative, no-code data dashboards with Lumen YAML specifications
- **lumen-ai** - AI-powered natural language data exploration with Lumen AI

**When to use:** Interactive dashboards, web applications, large-scale data visualization, geographic mapping, real-time data streaming, exploratory data analysis, publication-quality visualizations

### GAIA Data Downloader Plugin

Generate and develop hydroclimatological data download scripts for the GAIA project, covering 10+ environmental data sources.

**Agent:**
- **Data Downloader** - Generates download scripts from natural language prompts using a three-phase interaction (propose config → confirm → generate) for CONUS404, HRRR, WRF, PRISM, Stage IV, USGS, ORNL, DEM, Synoptic, and IRIS data

**Skill:**
- **download-script-dev** - Templates, configuration validation, and debugging guidance for developing data download scripts

**When to use:** Downloading hydroclimatological data for GAIA geoscience research, creating reproducible data pipelines, setting up new data download workflows

### UI/UX Design Team Plugin

Comprehensive UI/UX design team simulation with 10 specialized agents covering the full design lifecycle — user research, information architecture, interaction design, visual design, motion design, design systems engineering, accessibility auditing, UX writing, and design operations.

**Agent:**
- **UX Design Lead** - Coordinator agent that facilitates design thinking, conducts design critiques, and orchestrates 9 specialist agents (research, information architecture, interaction, visual, motion, design systems, accessibility, writing, ops) across the full design lifecycle

**Commands (10):**
- `/design-review`, `/audit-accessibility`, `/create-design-system`, `/create-persona`, `/create-type-scale`, `/design-handoff`, `/evaluate-usability`, `/frontend-design`, `/generate-palette`, `/map-journey`

**Skills (22):**
- **user-research**, **information-architecture**, **wireframing**, **visual-design**, **motion-design**, **design-tokens**, **design-system-creation**, **component-library**, **accessibility-audit**, **ux-writing**, **responsive-design**, **css-architecture**, **frontend-components**, **usability-evaluation**, **design-philosophies**, **design-case-studies**, **user-journey-mapping**, **ab-testing-strategy**, **design-handoff**, **color-systems**, **typography-systems**, **grid-layout-systems**

**When to use:** UI/UX design work, design system creation, accessibility audits, usability evaluation, user research and persona creation, design reviews, frontend component design, design-to-development handoff

Browse the [plugins directory](plugins/) and [community-plugins directory](community-plugins/) to explore all available plugins.

## Repository Structure

```
rse-plugins/
├── .claude-plugin/
│   └── marketplace.json                                # Plugin catalog (Claude Code, Copilot CLI, Codex)
├── .agents/plugins/
│   └── marketplace.json                                # Codex marketplace (generated)
├── .cursor-plugin/
│   └── marketplace.json                                # Cursor marketplace (generated)
├── plugins/                                            # Main plugin collection
│   ├── scientific-python-development/                  # Scientific Python development plugin
│   │   ├── plugin.json                                 # Agent Plugins manifest (edit this one)
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json                             # Claude Code manifest (generated)
│   │   ├── agents/
│   │   │   ├── scientific-python-expert.md
│   │   │   └── scientific-docs-architect.md
│   │   ├── commands/
│   │   └── skills/
│   │       ├── pixi-package-manager/
│   │       ├── python-packaging/
│   │       ├── python-testing/
│   │       ├── code-quality-tools/
│   │       └── scientific-documentation/
│   ├── scientific-domain-applications/                 # Domain-specific scientific computing plugin
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── agents/
│   │   │   └── astronomy-astrophysics-expert.md
│   │   └── skills/
│   │       ├── xarray-for-multidimensional-data/
│   │       └── astropy-fundamentals/
│   ├── ai-research-workflows/                          # Skills-first research workflow plugin
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── agents/
│   │   │   └── research-workflow-orchestrator.md
│   │   ├── commands/                                 # 10 thin wrappers (research, plan, iterate-plan,
│   │   │   └── ...                                   #   experiment, implement, validate, handoff,
│   │   │                                             #   prior-art, reproduce, harden)
│   │   └── skills/                                   # 11 skills
│   │       ├── using-research-workflows/             #   meta-skill
│   │       ├── researching-codebases/
│   │       ├── planning-implementations/
│   │       ├── iterating-plans/
│   │       ├── running-experiments/
│   │       ├── implementing-plans/
│   │       ├── validating-implementations/
│   │       ├── creating-handoffs/
│   │       ├── researching-prior-art/
│   │       ├── ensuring-reproducibility/
│   │       └── hardening-research-code/
│   └── project-management/                              # Project lifecycle management plugin
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── agents/
│       │   ├── project-onboarding-specialist.md
│       │   └── documentation-validator.md
│       ├── commands/
│       │   ├── setup-project.md
│       │   ├── project-handoff.md
│       │   └── validate-project-handoff.md
│       └── skills/
│           ├── community-health-files/
│           └── documentation-validation/
├── community-plugins/                                  # Community-contributed plugins
│   ├── gaia-data-downloader/                           # GAIA data download plugin
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── agents/
│   │   │   └── data-downloader.md
│   │   ├── skills/
│   │   │   └── download-script-dev/
│   │   │       ├── SKILL.md
│   │   │       └── references/
│   │   ├── AGENTS.md
│   │   ├── CLAUDE.md
│   │   └── README.md
│   └── holoviz-visualization/                          # HoloViz ecosystem plugin
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── agents/
│       │   ├── panel-specialist.md
│       │   ├── visualization-designer.md
│       │   ├── data-engineer.md
│       │   └── geo-spatial-expert.md
│       ├── skills/
│       │   ├── panel-dashboards/
│       │   ├── plotting-fundamentals/
│       │   ├── data-visualization/
│       │   ├── advanced-rendering/
│       │   ├── geospatial-visualization/
│       │   ├── colormaps-styling/
│       │   ├── parameterization/
│       │   ├── lumen-dashboards/
│       │   └── lumen-ai/
│       └── references/                                 # HoloViz ecosystem documentation
│           ├── holoviz-ecosystem.md
│           ├── library-matrix.md
│           ├── best-practices/
│           ├── patterns/
│           ├── troubleshooting/
│           ├── lumen-dashboards/
│           ├── lumen-ai/
│           └── colormaps/
├── CONTRIBUTING.md                                     # Contribution guidelines
├── LICENSE                                             # BSD 3-Clause License
└── README.md                                           # This file
```

## Architecture

### Plugin System

This repository uses the Claude Code plugin marketplace architecture:

- **Plugins** - Top-level containers organized by domain (e.g., python-development, scientific-computing)
- **Agents** - Specialized AI personas with comprehensive expertise in specific areas
- **Skills** - Reusable knowledge modules that provide detailed guidance on specific topics

### Design Philosophy

The agents and skills follow the [Scientific Python Development Guide](https://learn.scientific-python.org/development/) principles:

1. **Collaborate** - Adopt conventions and tooling used by the broader scientific Python community
2. **Refactor Fearlessly** - Leverage tests and tools to enable confident iteration
3. **Prefer Wide Over Deep** - Build reusable, extensible solutions for unforeseen applications

### Agent vs Skill

- **Agents** - Comprehensive personas that handle complete workflows, make decisions, and provide end-to-end guidance
- **Skills** - Focused knowledge modules on specific topics (e.g., testing patterns, packaging workflows) that agents can reference

## Contributing

We welcome contributions of new agents, skills, and improvements! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:

- Creating new agents and skills
- Plugin organization and structure
- Naming conventions and best practices
- Testing and validation
- Submitting pull requests

## Documentation

For detailed information about the plugins and their contents:

- [Contributing Guidelines](CONTRIBUTING.md) - How to contribute to this repository
- [HoloViz Ecosystem Overview](community-plugins/holoviz-visualization/references/holoviz-ecosystem.md) - Introduction to the HoloViz ecosystem
- [HoloViz Library Matrix](community-plugins/holoviz-visualization/references/library-matrix.md) - Comparison of HoloViz libraries and when to use each

## Related Resources

### Scientific Python Community
- [Scientific Python Development Guide](https://learn.scientific-python.org/development/) - Community best practices
- [Scientific Python Lectures](https://lectures.scientific-python.org/) - Educational materials
- [NumPy](https://numpy.org/), [SciPy](https://scipy.org/), [Pandas](https://pandas.pydata.org/) - Core libraries

### HoloViz Ecosystem
- [HoloViz.org](https://holoviz.org/) - Main HoloViz ecosystem portal
- [Panel](https://panel.holoviz.org/) - Build interactive dashboards and web applications
- [hvPlot](https://hvplot.holoviz.org/) - High-level plotting API for pandas and xarray
- [HoloViews](https://holoviews.org/) - Declarative data visualization
- [Datashader](https://datashader.org/) - Render large datasets accurately
- [GeoViews](https://geoviews.org/) - Geographic data visualization
- [Lumen](https://lumen.holoviz.org/) - No-code dashboards with AI capabilities
- [Param](https://param.holoviz.org/) - Declarative parameter management
- [Colorcet](https://colorcet.holoviz.org/) - Perceptually uniform colormaps

### Domain-Specific Libraries
- [Astropy](https://www.astropy.org/) - Astronomy and astrophysics in Python
- [Xarray](https://xarray.dev/) - Labeled multidimensional arrays for climate and Earth science

### Research Software Engineering
- [UW Scientific Software Engineering Center](https://escience.washington.edu/software-engineering/)
- [Best Practices for Scientific Computing](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1001745)
- [The Turing Way](https://the-turing-way.netlify.app/) - Guide to reproducible research

### Claude Code
- [Claude Code Documentation](https://docs.anthropic.com/claude/docs)
- [Claude Plugin Marketplace](https://code.claude.com/docs/en/plugins)

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Developed and maintained by the University of Washington Scientific Software Engineering Center (UW-SSEC).

## Questions or Issues?

Please open an issue on [GitHub](https://github.com/uw-ssec/rse-plugins/issues).

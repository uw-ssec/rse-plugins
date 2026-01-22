# RSE Plugins

Custom AI agents and skills for Research Software Engineering (RSE) and Scientific Computing tasks, designed for use with [Claude Code](https://www.anthropic.com/claude/code) and compatible AI coding assistants.

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

To use these agents and skills in Claude Code, add this repository to your plugin marketplace:

```bash
/plugin marketplace add uw-ssec/rse-plugins
```

Once installed, the agents and skills will be available in your Claude Code environment and can be invoked when working on scientific software projects.

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

Browse the [plugins directory](plugins/) and [community-plugins directory](community-plugins/) to explore all available plugins.

## Repository Structure

```
rse-plugins/
├── .claude-plugin/
│   └── marketplace.json                                # Claude plugin marketplace configuration
├── plugins/                                            # Main plugin collection
│   ├── scientific-python-development/                  # Scientific Python development plugin
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── agents/
│   │   │   ├── scientific-python-expert.md
│   │   │   └── scientific-docs-architect.md
│   │   └── skills/
│   │       ├── pixi-package-manager/
│   │       ├── python-packaging/
│   │       ├── python-testing/
│   │       ├── code-quality-tools/
│   │       └── scientific-documentation/
│   └── scientific-domain-applications/                 # Domain-specific scientific computing plugin
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── agents/
│       │   └── astronomy-astrophysics-expert.md
│       └── skills/
│           ├── xarray-for-multidimensional-data/
│           └── astropy-fundamentals/
├── community-plugins/                                  # Community-contributed plugins
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

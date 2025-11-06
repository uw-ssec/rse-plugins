# RSE Agents

Custom AI agents and skills for Research Software Engineering (RSE) and Scientific Computing tasks, designed for use with [Claude Code](https://www.anthropic.com/claude/code) and compatible AI coding assistants.

## Purpose

This repository provides specialized agents and skills that understand the unique challenges of scientific software development, including:

- Modern Scientific Python development following community best practices
- Reproducible environment management with pixi
- Python packaging and distribution with pyproject.toml
- Comprehensive testing strategies with pytest
- Scientific computing workflows and numerical methods
- Research software engineering practices
- High-performance computing (HPC) patterns
- Scientific Python ecosystem (NumPy, Pandas, SciPy, Matplotlib, Xarray, etc.)

## Installation

To use these agents and skills in Claude Code, add this repository to your plugin marketplace:

```bash
/plugin marketplace add uw-ssec/rse-agents
```

Once installed, the agents and skills will be available in your Claude Code environment and can be invoked when working on scientific software projects.

## Available Plugins

The repository provides Claude Code plugins organized by domain. Each plugin contains agents (specialized AI personas) and skills (reusable knowledge modules).

### Python Development Plugin

Expert agents and comprehensive skills for modern Scientific Python development.

**Location:** [plugins/python-development/](plugins/python-development/)

**Agents:**
- **Scientific Python Expert** - Comprehensive agent for scientific Python development following [Scientific Python Development Guide](https://learn.scientific-python.org/development/) best practices

**Skills:**
- **pixi-package-manager** - Fast, reproducible scientific Python environments with unified conda and PyPI management
- **python-packaging** - Modern packaging with pyproject.toml, src layout, and Hatchling build backend
- **python-testing** - Robust testing strategies with pytest following Scientific Python community guidelines

**When to use:** Scientific computing projects, data analysis pipelines, research software development, package creation, reproducible research workflows

### Scientific Computing Plugin

Agents for computational science, numerical methods, and high-performance computing.

**Location:** [plugins/scientific-computing/](plugins/scientific-computing/)

**Status:** Plugin structure in place, agents coming soon

**Planned focus areas:** HPC workflows, parallel computing, numerical algorithms, scientific simulations, performance optimization

Browse the [plugins directory](plugins/) to explore all available plugins.

## Repository Structure

```
rse-agents/
├── .claude-plugin/
│   └── marketplace.json        # Claude plugin marketplace configuration
├── plugins/
│   ├── python-development/     # Scientific Python development plugin
│   │   ├── agents/
│   │   │   └── scientific-python-expert.md
│   │   ├── skills/
│   │   │   ├── pixi-package-manager/
│   │   │   │   └── SKILL.md
│   │   │   ├── python-packaging/
│   │   │   │   └── SKILL.md
│   │   │   └── python-testing/
│   │   │       └── SKILL.md
│   │   └── README.md
│   ├── scientific-computing/   # Scientific computing plugin (planned)
│   │   ├── agents/
│   │   └── README.md
│   └── README.md               # Plugin directory overview
├── CONTRIBUTING.md             # Contribution guidelines
├── LICENSE                     # BSD 3-Clause License
└── README.md                   # This file
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

- [Plugins Overview](plugins/README.md) - Complete overview of all plugins
- [Python Development Plugin](plugins/python-development/README.md) - Scientific Python agents and skills
- [Scientific Computing Plugin](plugins/scientific-computing/README.md) - HPC and computational science
- [Contributing Guidelines](CONTRIBUTING.md) - How to contribute

## Related Resources

### Scientific Python Community
- [Scientific Python Development Guide](https://learn.scientific-python.org/development/) - Community best practices
- [Scientific Python Lectures](https://lectures.scientific-python.org/) - Educational materials
- [NumPy](https://numpy.org/), [SciPy](https://scipy.org/), [Pandas](https://pandas.pydata.org/) - Core libraries

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

Please open an issue on [GitHub](https://github.com/uw-ssec/rse-agents/issues).

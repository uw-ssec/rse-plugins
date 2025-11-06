# RSE Agents 🔬

Custom AI agents for Research Software Engineering (RSE) and Scientific Computing tasks, designed for use with [Claude Code](https://www.anthropic.com/claude/code) and compatible AI coding assistants.

## 🎯 Purpose

This repository provides specialized agents that understand the unique challenges of scientific software development, including:

- Scientific computing workflows and best practices
- Research data analysis and visualization
- High-performance computing (HPC) patterns
- Reproducible research and computational science
- Scientific Python ecosystem (NumPy, Pandas, SciPy, Matplotlib, etc.)
- Domain-specific scientific software development

## 📦 Installation

To use these agents in Claude Code, add this repository to your plugin marketplace:

```bash
/plugin marketplace add uw-ssec/rse-agents
```

Once installed, the agents will be available in your Claude Code environment and can be invoked when working on scientific software projects.

## 🤖 Available Agents

> **Note:** This repository is in active development. Agents will be added progressively to address various RSE and scientific computing needs.

Agents are organized by scientific domain categories in the `plugins/` directory. Each category contains specialized agents designed for specific areas of scientific software engineering.

### Agent Categories

- **[scientific-computing/](plugins/scientific-computing/)** - HPC, numerical computing, and computational science
- **[data-science/](plugins/data-science/)** - Data analysis, statistics, and machine learning
- **[research-tools/](plugins/research-tools/)** - General RSE practices and tools
- **[domain-specific/](plugins/domain-specific/)** - Discipline-specific scientific applications

Browse the [plugins directory](plugins/) to explore all categories and available agents.

## 📁 Repository Structure

```
rse-agents/
├── plugins/                    # Plugin categories
│   ├── scientific-computing/   # HPC & computational science agents
│   │   ├── README.md
│   │   └── agents/
│   │       └── TEMPLATE.md
│   ├── data-science/           # Data analysis & ML agents
│   │   └── agents/
│   ├── research-tools/         # General RSE agents
│   │   └── agents/
│   └── domain-specific/        # Domain-specific agents
│       └── agents/
├── LICENSE                     # BSD 3-Clause License
├── README.md                   # This file
└── CONTRIBUTING.md             # Guidelines for contributing agents
```

## 🤝 Contributing

We welcome contributions of new agents and improvements to existing ones! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:

- Creating new agents
- Agent naming conventions
- Testing and validation
- Submitting pull requests

## 📖 Documentation

For detailed information about developing and using RSE agents, please refer to:

- [Plugin Categories Overview](plugins/README.md) - Overview of all agent categories
- [Contributing Guidelines](CONTRIBUTING.md) - How to contribute to this repository
- Category-specific guides in each plugin directory

## 🔗 Related Resources

- [Claude Code Documentation](https://docs.anthropic.com/claude/docs)
- [UW Scientific Software Engineering Center](https://escience.washington.edu/software-engineering/)
- [Best Practices for Scientific Computing](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1001745)

## 📄 License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Developed and maintained by the University of Washington Scientific Software Engineering Center (UW-SSEC).

---

**Questions or Issues?** Please open an issue on [GitHub](https://github.com/uw-ssec/rse-agents/issues).

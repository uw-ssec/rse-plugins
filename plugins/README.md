# RSE Agents Plugins

This directory contains Claude Code plugins for Research Software Engineering (RSE) and scientific computing tasks. Each plugin provides specialized agents and skills organized by domain.

## Plugin Architecture

Plugins are self-contained units that provide domain-specific agents and skills:

- **Agents** - Comprehensive AI personas with deep expertise in specific areas, capable of guiding complete workflows
- **Skills** - Focused knowledge modules providing detailed guidance on specific topics and techniques
- **README** - Documentation for each plugin describing its contents and use cases

## Directory Structure

```
plugins/
├── python-development/           # Scientific Python development
│   ├── agents/
│   │   └── scientific-python-expert.md
│   ├── skills/
│   │   ├── pixi-package-manager/
│   │   │   └── SKILL.md
│   │   ├── python-packaging/
│   │   │   └── SKILL.md
│   │   └── python-testing/
│   │       └── SKILL.md
│   └── README.md
├── scientific-computing/         # HPC & computational science
│   ├── agents/                   # (planned)
│   └── README.md
└── README.md                     # This file
```

## Available Plugins

### Python Development

**Status:** Active (v0.1.0)

**Location:** [python-development/](python-development/)

**Description:** Comprehensive agents and skills for modern Scientific Python development following the [Scientific Python Development Guide](https://learn.scientific-python.org/development/) community best practices.

**Contents:**
- 1 Agent (Scientific Python Expert)
- 3 Skills (pixi package manager, Python packaging, Python testing)

**Key capabilities:**
- Reproducible environment management with pixi
- Modern packaging with pyproject.toml and src layout
- Comprehensive testing with pytest
- Scientific computing with NumPy, Pandas, SciPy, Matplotlib, Xarray
- Code quality tooling (ruff, mypy, pre-commit)
- Documentation with Sphinx and NumPy-style docstrings

**When to use:**
- Setting up scientific Python projects
- Creating distributable Python packages
- Implementing testing for numerical code
- Managing dependencies for reproducibility
- Data analysis and visualization workflows
- Research software development

### Scientific Computing

**Status:** Planned

**Location:** [scientific-computing/](scientific-computing/)

**Description:** Agents and skills for high-performance computing, numerical methods, and computational science.

**Planned capabilities:**
- HPC workflow optimization
- Parallel computing (MPI, OpenMP, GPU)
- Numerical algorithms and methods
- Scientific simulations
- Performance profiling and optimization
- Cluster computing and job scheduling

**Target technologies:** SLURM, MPI, CUDA, OpenCL, Dask, Numba, JAX

## Plugin Development

### Creating New Plugins

When creating a new plugin:

1. **Choose a clear domain** - Plugins should focus on a cohesive set of related tasks
2. **Create the directory structure** - Include `agents/`, `skills/`, and `README.md`
3. **Write comprehensive documentation** - Explain what the plugin provides and when to use it
4. **Follow naming conventions** - Use kebab-case for directory names
5. **Update marketplace.json** - Register the plugin in `.claude-plugin/marketplace.json`

### Plugin Structure

```
my-plugin/
├── agents/
│   ├── agent-name-1.md
│   └── agent-name-2.md
├── skills/
│   ├── skill-name-1/
│   │   └── SKILL.md
│   └── skill-name-2/
│       └── SKILL.md
└── README.md
```

### Agents vs Skills

**When to create an Agent:**
- Need a comprehensive persona that handles complete workflows
- Requires decision-making across multiple domains
- Involves end-to-end guidance from problem definition to solution
- Example: Scientific Python Expert agent

**When to create a Skill:**
- Focused expertise on a specific topic or technique
- Reusable knowledge that multiple agents might need
- Detailed how-to guidance or reference material
- Example: pytest testing patterns skill

### Naming Conventions

**Agents:**
- Use kebab-case: `scientific-python-expert.md`
- Be descriptive and specific
- Indicate expertise level or domain

**Skills:**
- Use kebab-case for directories: `pixi-package-manager/`
- Include descriptive SKILL.md file
- Focus on specific tools or techniques

## Quality Standards

All plugins should:
- Follow Scientific Python community best practices
- Promote reproducibility and scientific rigor
- Provide accurate, up-to-date information
- Include clear documentation and usage guidelines
- Emphasize testing and validation
- Support open science principles
- Stay within clearly defined scope

## Resources

### Claude Code
- [Claude Code Documentation](https://docs.anthropic.com/claude/docs)
- [Claude Plugin Marketplace](https://code.claude.com/docs/en/plugins)

### Scientific Python
- [Scientific Python Development Guide](https://learn.scientific-python.org/development/)
- [Scientific Python Lectures](https://lectures.scientific-python.org/)
- [NumPy Documentation Style](https://numpydoc.readthedocs.io/)

### Research Software Engineering
- [The Turing Way](https://the-turing-way.netlify.app/)
- [Best Practices for Scientific Computing](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1001745)
- [Software Carpentry](https://software-carpentry.org/)

## Contributing

See the main [CONTRIBUTING.md](../CONTRIBUTING.md) file for detailed contribution guidelines, workflows, and requirements.

Ready to create content? Choose a plugin or create a new one!

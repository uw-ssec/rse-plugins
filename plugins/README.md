# RSE Agents Plugin Directory

This directory contains custom agent configurations for Research Software Engineering (RSE) and scientific computing tasks, organized by scientific domain categories.

## 📂 Directory Structure

Agents are organized into scientific categories, each containing their own `agents/` subdirectory:

```
plugins/
├── scientific-computing/     # Scientific computing & HPC agents
│   └── agents/
├── python-development/       # Scientific Python development agents
│   └── agents/
│       └── scientific-python-expert.md
├── data-science/             # Data analysis & ML agents (coming soon)
│   └── agents/
├── research-tools/           # Research software tools agents (coming soon)
│   └── agents/
└── domain-specific/          # Domain-specific science agents (coming soon)
    └── agents/
```

## 🗂️ Agent Categories

### Scientific Computing (`scientific-computing/`)
Agents for computational science, numerical computing, and high-performance computing:
- High-performance computing (HPC) workflows
- Parallel and distributed computing
- Scientific simulations and modeling
- Numerical algorithms and optimization

### Python Development (`python-development/`)
Agents specialized in scientific Python development and modern Python practices:
- Modern Python packaging and project structure
- Reproducible environment management (pixi, venv)
- Testing and quality assurance for scientific code
- Documentation and publication workflows
- Performance optimization for numerical Python code

### Data Science (`data-science/`)
Agents for data analysis, statistics, and machine learning:
- Data processing and cleaning
- Statistical analysis
- Machine learning for scientific applications
- Data visualization and exploration

### Research Tools (`research-tools/`)
Agents for general research software engineering:
- Version control and collaboration
- Testing and validation of scientific code
- Documentation and reproducibility
- Software architecture for research

### Domain-Specific (`domain-specific/`)
Agents specialized for specific scientific domains:
- Bioinformatics and computational biology
- Climate and earth science computing
- Physics and astronomy software
- Chemistry and materials science
- Social sciences and digital humanities

## 🔨 Creating New Agents

### 1. Choose the Appropriate Category

Determine which category best fits your agent's primary focus:
- **scientific-computing**: For HPC, numerical computing, simulations
- **python-development**: For Python packaging, environments, testing, documentation
- **data-science**: For data analysis, statistics, ML
- **research-tools**: For general RSE practices and tools
- **domain-specific**: For discipline-specific applications

### 2. Follow Naming Conventions

- Use kebab-case: `agent-name.md`
- Be descriptive and specific
- Examples:
  - `scientific-computing/agents/hpc-optimization-expert.md`
  - `data-science/agents/scientific-python-analyst.md`
  - `research-tools/agents/reproducibility-specialist.md`

## 📋 Agent File Structure

Each agent markdown file should include:

1. **Title and Description**: Clear explanation of the agent's purpose
2. **Expertise Section**: List of specific capabilities
3. **When to Use**: Guidelines for appropriate usage
4. **Agent Prompt**: The instruction text for Claude Code
5. **Examples** (optional): Sample use cases
6. **Tags**: Relevant keywords for discovery

## 🎯 Quality Standards

All agents should:
- Promote scientific rigor and reproducibility
- Follow best practices for scientific computing
- Provide accurate, up-to-date technical information
- Stay within clearly defined scope
- Emphasize testing and validation
- Support open science principles

## 🧪 Testing Your Agent

Before submitting:

1. **Functional Test**: Use with Claude Code on real tasks
2. **Scope Test**: Verify it stays within defined expertise
3. **Quality Test**: Ensure recommendations follow best practices
4. **Documentation Test**: Check usage guidelines are clear

## 📚 Resources

- [Claude Code Plugin Documentation](https://code.claude.com/docs/en/plugins)
- [Agent Development Guide](../CONTRIBUTING.md)
- [Scientific Python Best Practices](https://learn.scientific-python.org/development/)
- [The Turing Way](https://the-turing-way.netlify.app/)

## 🤝 Contributing

See the main [CONTRIBUTING.md](../CONTRIBUTING.md) file for detailed contribution guidelines and workflow.

---

**Ready to create an agent?** Choose your category and start building!

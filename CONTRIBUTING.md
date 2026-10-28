# Contributing to RSE Plugins

Thank you for your interest in contributing to RSE Plugins! This document provides guidelines for creating and contributing custom agents for scientific software engineering tasks.

## 🌟 Types of Contributions

We welcome various types of contributions:

- **New Agents**: Create agents for specific RSE or scientific computing tasks
- **Agent Improvements**: Enhance existing agents with better prompts or capabilities
- **Documentation**: Improve guides, examples, and documentation
- **Bug Reports**: Report issues with existing agents
- **Feature Requests**: Suggest new agent capabilities or improvements

## 🤖 Creating a New Agent

### 1. Choose the Right Category

Agents are organized by scientific domain in the `plugins/` directory:

- **scientific-computing/** - HPC, numerical computing, simulations
- **data-science/** - Data analysis, statistics, machine learning
- **research-tools/** - General RSE practices and tools
- **domain-specific/** - Discipline-specific applications

### 2. Agent File Structure

Agents are stored in `plugins/{category}/agents/` as Markdown files. Each agent file should:

1. Have a descriptive, kebab-case filename (e.g., `scientific-python-expert.md`)
2. Include a clear agent prompt that defines its expertise and behavior
3. Follow the template structure provided in each category's `agents/TEMPLATE.md`

### Agent Template

```markdown
# Agent Name

Brief description of what this agent does.

## Expertise

- List key areas of expertise
- Specific technologies or domains
- Types of problems it solves

## When to Use This Agent

Describe scenarios where this agent should be used, such as:
- Working with specific libraries or frameworks
- Solving particular types of problems
- Following specific methodologies

## Agent Prompt

[Your agent prompt goes here - this is the instruction text that will be used by Claude Code]
```

### Agent Naming Conventions

- Use clear, descriptive names that indicate the agent's purpose
- Use kebab-case for filenames: `domain-specific-expert.md`
- Keep names concise but informative
- Examples:
  - `plugins/scientific-computing/agents/hpc-workflow-optimizer.md`
  - `plugins/data-science/agents/scientific-python-analyst.md`
  - `plugins/research-tools/agents/reproducibility-specialist.md`

### Best Practices for Agent Prompts

1. **Be Specific**: Clearly define the agent's domain expertise and limitations
2. **Provide Context**: Include relevant background about scientific software engineering practices
3. **Set Expectations**: Explain what the agent can and cannot do
4. **Include Examples**: When helpful, provide example use cases or code patterns
5. **Reference Standards**: Cite relevant scientific computing best practices or standards
6. **Focus on Quality**: Emphasize code quality, reproducibility, and scientific rigor

### Example Agent Qualities

Good agents for scientific software should:

- Understand reproducibility and version control practices
- Know scientific Python ecosystem conventions
- Recognize performance considerations for computational workloads
- Promote testing and validation of scientific code
- Encourage documentation and metadata practices
- Support open science principles

## 📝 Contribution Workflow

1. **Fork the Repository**: Create your own fork of uw-ssec/rse-plugins

2. **Create a Branch**: Make a branch for your contribution
   ```bash
   git checkout -b add-agent-name
   ```

3. **Add Your Agent**: Create your agent file in the appropriate `plugins/{category}/agents/` directory

4. **Test Your Agent**: Test the agent with Claude Code to ensure it works as expected

5. **Update Documentation**: If adding a new agent, update the category README to list it

6. **Submit a Pull Request**: 
   - Provide a clear description of the agent and its purpose
   - Explain the types of tasks it helps with
   - Include any testing or validation you've done

## ✅ Pull Request Checklist

Before submitting your PR, ensure:

- [ ] Agent file is in the appropriate `plugins/{category}/agents/` directory
- [ ] Filename follows kebab-case convention
- [ ] Agent prompt is clear and well-documented
- [ ] Agent has been tested with Claude Code (or equivalent)
- [ ] README.md is updated if adding a new agent
- [ ] Commit messages are clear and descriptive
- [ ] No sensitive information or credentials are included

## 🧪 Testing Your Agent

To test your agent:

1. Add the agent file to your local `plugins/{category}/agents/` directory
2. Use Claude Code to invoke the agent on relevant tasks
3. Verify that the agent provides appropriate guidance
4. Check that the agent stays within its defined scope
5. Ensure the agent promotes best practices for scientific software

## 📊 Evaluating Skills

On every pull request that changes a skill, **Skill quality check** runs [SkillEvaluator](https://github.com/NVIDIA/SkillEvaluator)'s keyless `quality-check` (pinned to v0.6.0) on each changed skill. It fails if a skill scores below 70, and lists every changed skill's score and grade in the job summary. It scores quality only: SkillEvaluator's full `validate` (schema, PII and security scanners) is not part of this check. To check a skill locally before pushing:

```bash
uv tool install --python 3.13 "skillevaluator @ git+https://github.com/NVIDIA/SkillEvaluator.git@5320d9329c36ecc72bc94c4f58cc813d6b54224b"
skillevaluator quality-check plugins/<plugin>/skills/<skill> --min-score 70
```

Two manually triggered workflows measure skills (**Actions → workflow → Run workflow**). Neither runs on pull requests.

- **Evaluate All Skills** runs each skill's testcases with and without the skill on every model the LiteLLM proxy serves, and writes a baseline-versus-skill comparison to the run summary. Testcases live in the private `uw-ssec/rse-plugins-testcases` repository. A full run takes many hours, so narrow it with the `skills` and `models` inputs (comma-separated) and set `sleep-seconds` to `0` for a quick check. When the `TESSL_TOKEN` secret is set, the run also adds an advisory Tessl review of each selected skill.
- **Generate Testcases for New Skills** drafts five or six testcases for each skill a pull request adds. Run it with the PR number after reviewing the PR. With `dry-run` on (the default), the drafts are uploaded as a run artifact; turn it off to open a pull request in the testcases repository for review.

| Secret or variable | Used by | Purpose |
|---|---|---|
| `LITELLM_API_KEY`, `LITELLM_PROXY_URL` | Both | Model access through the LiteLLM proxy |
| `TEST_REPO_TOKEN` | Both | Fine-grained token for `rse-plugins-testcases`: Contents read for evaluation; Contents and Pull requests read/write for generation |
| `TESSL_TOKEN` (optional secret) | Evaluate All Skills | Turns on the Tessl review |
| `TESSL_WORKSPACE` (optional variable) | Evaluate All Skills | Tessl workspace to use when the token can see more than one |

Run the unit tests for these workflows' scripts with `pixi exec --spec python=3.12 --spec pytest --spec pyyaml pytest .github/scripts/tests -q`.

## 📋 Code of Conduct

This project adheres to professional standards of conduct. Please be respectful and constructive in all interactions.

## 🤔 Questions or Need Help?

- Open an issue for questions about contributing
- Check existing issues and pull requests for similar contributions
- Reach out to the maintainers if you need guidance

## 📚 Additional Resources

- [Claude Code Documentation](https://docs.anthropic.com/claude/docs)
- [Best Practices for Scientific Computing](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1001745)
- [Software Carpentry](https://software-carpentry.org/) - Teaching foundational coding skills
- [Research Software Engineering](https://researchsoftware.org/) - Community resources

## 🙏 Thank You!

Your contributions help improve scientific software development practices and make research computing more accessible and reliable. We appreciate your effort!

# AI Research Workflows Plugin

Structured AI-enabled research workflows for software development: Research, Plan, Experiment, Implement, Validate.

## Overview

This plugin provides a systematic approach to complex development tasks through distinct, well-defined phases. Software development often involves jumping between understanding existing code, planning changes, experimenting with approaches, implementing solutions, and validating results. This plugin formalizes these activities into a structured workflow with dedicated commands and documentation templates.

**Version:** 0.1.0

**Contents:**
- 1 Agent: Research Workflow Orchestrator
- 1 Skill: Research Workflow Management
- 6 Commands: research, plan, iterate-plan, experiment, implement, validate

### Workflow Phases

1. **Research** (`/research`) — Document and understand existing code, patterns, and architecture
2. **Plan** (`/plan`) — Create detailed, testable implementation plans through interactive research
3. **Iterate Plan** (`/iterate-plan`) — Refine existing plans based on feedback or changed requirements
4. **Experiment** (`/experiment`) — Try multiple approaches before committing (optional)
5. **Implement** (`/implement`) — Execute the plan phase by phase with verification
6. **Validate** (`/validate`) — Systematically verify implementation against plan criteria

Each phase produces a structured markdown document saved to `.agents/` in your project root, creating an auditable trail of technical decisions and implementation details.

## Installation

This plugin is part of the RSE Agents collection. To use it with Claude Code:

1. Clone the repository:
   ```bash
   git clone https://github.com/uw-ssec/rse-agents.git
   ```

2. The plugin will be automatically available in the repository's marketplace at:
   ```
   plugins/ai-research-workflows/
   ```

3. Alternatively, symlink the plugin to your local Claude plugins directory:
   ```bash
   ln -s $(pwd)/rse-agents/plugins/ai-research-workflows ~/.claude/plugins/ai-research-workflows
   ```

4. Verify installation by checking available commands:
   ```bash
   /help
   ```

## Plugin Structure

```
ai-research-workflows/
├── .claude-plugin/
│   └── plugin.json                           # Plugin metadata and configuration
├── agents/
│   └── research-workflow-orchestrator.md     # Main workflow orchestrator agent
├── commands/
│   ├── research.md                           # Research command
│   ├── plan.md                               # Planning command
│   ├── iterate-plan.md                       # Plan iteration command
│   ├── experiment.md                         # Experimentation command
│   ├── implement.md                          # Implementation command
│   └── validate.md                           # Validation command
├── skills/
│   └── research-workflow-management/
│       ├── SKILL.md                          # Skill definition
│       └── assets/
│           ├── research-template.md          # Research doc template
│           ├── plan-template.md              # Plan doc template
│           ├── experiment-template.md        # Experiment doc template
│           └── implement-template.md         # Implementation doc template
├── LICENSE
└── README.md                                 # This file
```

## Available Agents

### Research Workflow Orchestrator

**File:** [agents/research-workflow-orchestrator.md](agents/research-workflow-orchestrator.md)

**Description:** Use this agent when the user wants to "research the codebase", "plan implementation", "iterate on the plan", "experiment with solutions", "implement the plan", "validate implementation", mentions "AI workflow", "structured development", "workflow orchestration", or wants guidance on using the structured research workflow (Research → Plan → Iterate Plan → Experiment → Implement → Validate).

**Integrated Skills:**
- research-workflow-management

**Capabilities:**
- Guides users through structured six-phase workflow
- Manages workflow state and transitions between phases
- Tracks workflow artifacts in `.agents/` directory
- Cross-references workflow documents
- Provides context-aware workflow recommendations
- Ensures document completeness and quality
- Adapts workflow to user needs (full workflow vs. skipping phases)

**Workflow Decision Framework:**

The agent uses a comprehensive decision-making framework to recommend the right workflow step:

1. **When to Suggest Research:**
   - User wants to understand existing code
   - User asks "how does X work?"
   - Planning a change and context about current implementation is missing
   - Need to document architecture or patterns

2. **When to Suggest Planning:**
   - User wants to implement a new feature
   - User describes a change requiring multiple files
   - Implementation approach needs thought and structure
   - Checks for existing research first

3. **When to Suggest Plan Iteration:**
   - User wants to adjust an existing plan
   - Requirements have changed
   - Experiment results need to be incorporated

4. **When to Suggest Experimentation:**
   - Genuine uncertainty about the best approach
   - Multiple valid technical solutions exist
   - Performance or integration characteristics are unknown
   - Not for obvious decisions or low-risk choices

5. **When to Suggest Implementation:**
   - A plan exists and is approved
   - User says they're ready to implement
   - Plan has been iterated to satisfaction

6. **When to Suggest Validation:**
   - Implementation is complete
   - Tests are failing and systematic review is needed
   - Before creating a pull request

**Quality Assurance:**

Every workflow phase includes comprehensive quality checks:

- **Research:** Complete documentation with file references, no suggestions or critique
- **Plans:** No open questions, measurable success criteria (Automated + Manual), specific file:line references
- **Experiments:** Actual running code, honest observations including failures
- **Implementation:** Sequential phases, continuous verification, progress tracking
- **Validation:** All automated checks run, manual steps documented, deviations identified

**When to use:**
- Complex multi-file changes requiring planning
- Understanding unfamiliar codebases systematically
- Making evidence-based architectural decisions
- Ensuring systematic verification before commits
- Creating auditable records of technical decisions
- Learning structured development workflows

## Available Skills

### Research Workflow Management

**File:** [skills/research-workflow-management/SKILL.md](skills/research-workflow-management/SKILL.md)

**Description:** This skill should be used when the user asks to "research the codebase", "plan implementation", "iterate on the plan", "experiment with solutions", "implement the plan", "validate implementation", "AI workflow", "structured development", "workflow orchestration", or mentions any phase of the structured research workflow (Research → Plan → Iterate Plan → Experiment → Implement → Validate).

**Key Topics:**
- Six-phase workflow overview (Research, Plan, Iterate Plan, Experiment, Implement, Validate)
- Document naming conventions and cross-referencing
- Template-based document generation
- Best practices for each workflow phase
- Common workflow patterns
- Integration with standard development practices

**When to use:**
- Setting up structured workflows for complex tasks
- Creating auditable development documentation
- Bridging research and implementation phases
- Making evidence-based technical decisions
- Systematic verification and validation
- Building knowledge bases from codebase exploration

**Skill Contents:**
- SKILL.md: Main skill guide with workflow overview, decision trees, and best practices
- assets/research-template.md: Template for research documentation
- assets/plan-template.md: Template for implementation plans
- assets/experiment-template.md: Template for experiment reports
- assets/implement-template.md: Template for implementation summaries

**Quick Reference Card:**

```
Need to understand existing code?
└─> /research <topic>

Ready to design an implementation?
├─> Have research docs?
│   └─> /plan <feature> (references research automatically)
└─> No research docs?
    └─> Run /research first, then /plan

Need to adjust an existing plan?
└─> /iterate-plan <plan-file> <changes>

Uncertain about the best approach?
└─> /experiment <approach-question>

Ready to execute the plan?
└─> /implement <plan-file>

Implementation complete, need verification?
└─> /validate <plan-file>
```

## Available Commands

### `/research <topic>`

Research and document existing code to build context for a task.

**Purpose:** Create comprehensive technical documentation of how the codebase works TODAY. This is pure documentation — no critique, no suggestions, just explaining what exists and how it works.

**Usage:**
```bash
# Research a specific topic
/research how error handling works

# Research specific files
/research authentication in auth.py and session.py

# Interactive mode
/research
```

**Output:** Creates `.agents/research-<slug>.md` with:
- Executive summary of findings
- Detailed component documentation with file references
- Architecture patterns and data flows
- Code examples where illuminating
- References to key files with line numbers

**Best for:**
- Understanding existing code before making changes
- Documenting architectural patterns
- Finding where specific functionality lives
- Building knowledge base for future work
- Answering "how does X work?" questions

### `/plan <feature>`

Create detailed implementation plans through interactive research and iteration.

**Purpose:** Design a complete, actionable implementation plan with specific file references, measurable success criteria, and phased execution strategy.

**Usage:**
```bash
# Plan a new feature
/plan add OAuth authentication

# Plan with research context
/plan add JWT auth @research-auth-system.md

# Interactive mode
/plan
```

**Output:** Creates `.agents/plan-<slug>.md` with:
- Overview and motivation
- Current state analysis with file references
- Desired end state
- "What We're NOT Doing" scope boundaries
- Phased implementation steps
- Automated and manual success criteria
- Testing strategy
- References to research and experiment documents

**Key Features:**
- Interactive planning with user feedback at each stage
- Researches actual code patterns, doesn't guess
- Asks focused questions that can't be answered from code
- NO open questions remain in final plan
- Includes specific file:line references throughout

**Best for:**
- New feature implementations
- Refactoring or architectural changes
- Multi-file modifications
- Getting stakeholder buy-in before coding

### `/iterate-plan <plan-file> <changes>`

Refine existing plans based on feedback or changed requirements.

**Purpose:** Make surgical updates to plans without rewriting from scratch. Maintains plan consistency while adapting to new information.

**Usage:**
```bash
# Adjust plan scope
/iterate-plan .agents/plan-oauth-support.md remove email notification phase

# Add a new phase
/iterate-plan .agents/plan-oauth-support.md add database migration as a separate phase before Phase 3

# Update based on experiment
/iterate-plan .agents/plan-redis-caching.md incorporate experiment results from experiment-redis-vs-memcached.md
```

**Output:** Updates the existing plan file with requested changes

**Best for:**
- Scope adjustments
- Incorporating experiment results
- Responding to changed requirements
- Fixing issues found during plan review

### `/experiment <comparison>`

Try multiple approaches with working code before committing to a design.

**Purpose:** Make evidence-based architectural decisions by prototyping 2-3 distinct approaches and comparing them with real measurements.

**Usage:**
```bash
# Compare technical approaches
/experiment JWT vs session cookies for OAuth

# Test integration patterns
/experiment GraphQL vs REST for new API

# Performance comparison
/experiment Redis vs Memcached for caching
```

**Output:** Creates `.agents/experiment-<slug>.md` with:
- Hypothesis and success criteria
- Implementation details for each approach
- Observations and measurements
- Comparative analysis with trade-offs
- Clear recommendation with reasoning

**Key Features:**
- Actually runs code prototypes (not just theory)
- Records honest observations including failures
- Provides evidence-based recommendations

**Best for:**
- Genuine uncertainty about best approach
- Multiple valid technical solutions
- Unknown performance or integration characteristics
- Architectural decisions with significant trade-offs

**NOT needed for:**
- Obvious decisions
- Approaches already used in codebase
- Low-risk choices

### `/implement <plan-file>`

Execute an approved plan phase by phase with continuous verification.

**Purpose:** Systematically implement the plan, tracking progress and verifying correctness after each phase.

**Usage:**
```bash
# Implement a plan
/implement .agents/plan-oauth-support.md

# Resume interrupted implementation
/implement .agents/plan-oauth-support.md
```

**Output:**
- Updates plan file with checkmarks as phases complete
- Creates `.agents/implement-<slug>.md` with implementation summary
- Runs automated verification after each phase
- Lists manual verification steps for user

**Key Features:**
- Creates task list to track progress
- Implements phases sequentially (not in parallel)
- Pauses for human verification between phases
- Stops and communicates if reality doesn't match plan
- Updates plan checkmarks in real-time

**Best for:**
- Executing approved plans
- Tracking implementation progress
- Ensuring systematic verification
- Creating auditable implementation record

### `/validate <plan-file>`

Systematically verify implementation against plan criteria.

**Purpose:** Comprehensive validation that implementation matches the plan by running all automated checks and documenting manual testing needs.

**Usage:**
```bash
# Validate implementation
/validate .agents/plan-oauth-support.md
```

**Output:** Inline validation report with:
- Pass/fail status for each automated check
- Code review findings summary
- Manual testing steps clearly listed
- Recommendations categorized by priority
- Deviations from plan identified

**Best for:**
- Verifying implementation correctness
- Catching incomplete implementations
- Pre-pull-request validation
- Debugging failing tests systematically

## Architecture and Design

### Workflow Philosophy

This plugin follows a structured approach that provides several key benefits:

1. **Separation of Concerns** — Research, planning, and implementation are distinct activities with different goals
2. **Incremental Progress** — Each phase produces concrete artifacts that can be reviewed independently
3. **Reduced Cognitive Load** — Focus on one type of work at a time rather than trying to do everything simultaneously
4. **Better Collaboration** — Documents provide clear communication artifacts for stakeholders
5. **Auditable Decisions** — Technical choices are documented with their context and reasoning
6. **Reduced Rework** — Issues are caught during planning rather than after implementation

### Core Principles

**Documentation-First Research:**
- Document WHAT EXISTS, not what should exist
- No critique or suggestions during research phase
- Comprehensive file references with line numbers
- Architecture patterns documented clearly

**Interactive Planning:**
- Build plans through dialog, not in isolation
- Verify assumptions with code research
- Ask focused questions that can't be answered from code
- NO open questions remain in final plans

**Evidence-Based Decisions:**
- Run actual code in experiments, don't just theorize
- Measure real performance characteristics
- Record honest observations including failures

**Systematic Implementation:**
- Sequential phase execution with verification
- Continuous automated checking after each phase
- Stop and communicate when reality doesn't match plan

**Comprehensive Validation:**
- All automated checks from plan executed
- Manual testing steps clearly documented
- Deviations from plan identified and explained

### Document Organization

**Naming Convention:**
All workflow documents follow consistent naming in `.agents/`:

- `research-<slug>.md` — Research documentation
- `plan-<slug>.md` — Implementation plans
- `experiment-<slug>.md` — Experiment reports
- `implement-<slug>.md` — Implementation summaries

**Cross-Referencing:**
Documents reference each other using relative links, creating a navigable graph of technical decisions:

```markdown
## References

**Research Documents:**
- [Research: Auth System](research-auth-system.md)

**Experiment Reports:**
- [Experiment: JWT vs Session](experiment-jwt-vs-session.md)
```

## How to Use This Plugin

### Using the Research Workflow Orchestrator Agent

The agent is designed to guide you through structured workflows proactively. It automatically loads the research-workflow-management skill and provides context-aware recommendations.

**Load the agent when:**
- Starting complex multi-file changes
- Understanding unfamiliar codebases
- Making architectural decisions
- Need systematic verification workflows

### Using Individual Commands

Commands can be invoked independently when you know which phase you need:

- **Use `/research`** when you need to understand existing code
- **Use `/plan`** when you're ready to design an implementation
- **Use `/iterate-plan`** when adjusting existing plans
- **Use `/experiment`** when comparing technical approaches
- **Use `/implement`** when executing approved plans
- **Use `/validate`** when verifying implementation correctness

### Workflow Flexibility

The workflow is designed to be flexible — you can:
- Skip optional phases like experimentation
- Iterate on plans as requirements evolve
- Use research without immediate implementation
- Combine multiple research documents for comprehensive context

The key is maintaining clear documentation of what was built and why.

## When to Use This Plugin

Use the AI Research Workflows plugin when:

- **Complex Features** — Implementation requires multiple files and careful planning
- **Architectural Changes** — Refactoring or redesigning system components
- **Unfamiliar Codebases** — Need systematic understanding before making changes
- **Technical Decisions** — Multiple valid approaches require evidence-based selection
- **Verification Critical** — Changes must be thoroughly validated before deployment
- **Collaboration** — Need clear artifacts for stakeholder review and approval
- **Auditing** — Technical decisions must be documented for future reference
- **Learning** — Want to build structured approach to software development

**Don't use for:**
- Single-line fixes or typos
- Obvious implementations with clear requirements
- Experimental prototyping without structure
- Pure research without implementation intent (though `/research` alone is valuable)

## Workflow Patterns

### Pattern 1: Full Workflow (Complex Changes)

For significant features or architectural changes:

```
/research [topic]           → Document current state
↓
/plan [feature]             → Create implementation plan
↓
/experiment [comparison]    → (Optional) Test approaches
↓
/iterate-plan [adjustments] → Refine plan based on findings
↓
/implement [plan]           → Execute implementation
↓
/validate [plan]            → Verify correctness
```

### Pattern 2: Simple Feature (Skip Experiment)

For straightforward additions following known patterns:

```
/research [existing patterns]
↓
/plan [new feature]
↓
/implement [plan]
↓
/validate [plan]
```

### Pattern 3: Rapid Iteration (Known Approach)

When the approach is clear and research already exists:

```
/plan [feature]
↓
/iterate-plan [scope adjustment]
↓
/implement [plan]
```

### Pattern 4: Research Only (Build Context)

For understanding codebases without immediate changes:

```
/research [system A]
↓
/research [system B] (follow-up)
↓
[Use findings for future planning]
```

## Integration with Existing Workflows

This plugin complements standard development practices:

- **Before coding:** Research and plan
- **During coding:** Follow the plan, iterate as needed
- **After coding:** Validate before committing
- **Standard tools still work:** Use `/commit`, `/pr`, git commands normally

The workflow adds structure and documentation, not restrictions.

## Examples and Use Cases

### Example 1: Adding a New API Endpoint

```bash
# Research existing API patterns
/research API endpoint patterns and middleware

# Plan the new endpoint
/plan add user profile endpoint

# Review the generated plan at .agents/plan-add-user-profile-endpoint.md
# Make any needed adjustments
/iterate-plan .agents/plan-add-user-profile-endpoint.md add rate limiting to Phase 2

# Implement the plan
/implement .agents/plan-add-user-profile-endpoint.md

# Validate implementation
/validate .agents/plan-add-user-profile-endpoint.md
```

### Example 2: Refactoring with Experimentation

```bash
# Understand current database layer
/research database layer architecture

# Create refactoring plan
/plan migrate to repository pattern

# Test different approaches
/experiment Active Record vs Repository pattern

# Update plan with experiment insights
/iterate-plan .agents/plan-migrate-to-repository-pattern.md use Repository pattern from experiment

# Execute the refactoring
/implement .agents/plan-migrate-to-repository-pattern.md
```

### Example 3: Investigation Without Implementation

```bash
# Research a complex subsystem
/research payment processing flow

# Follow-up on specific component
/research Stripe integration in payment processor

# Documents in .agents/ now available for future planning
```

### Example 4: Quick Feature with Known Pattern

```bash
# Quick research of existing pattern
/research how we handle form validation

# Plan following established pattern
/plan add contact form with validation

# Implement directly
/implement .agents/plan-add-contact-form-with-validation.md
```

## Best Practices

### Research Phase

✅ **Do:**
- Read referenced files completely
- Use parallel research for comprehensive exploration
- Include specific file paths and line numbers
- Document patterns, not problems
- Focus on WHAT EXISTS, not what should exist

❌ **Don't:**
- Suggest improvements (unless explicitly asked)
- Critique implementation
- Make partial file reads
- Guess about how code works

### Planning Phase

✅ **Do:**
- Reference existing research documents
- Ask focused questions that can't be answered from code
- Include measurable success criteria (Automated + Manual)
- Define "what we're NOT doing"
- Get feedback at each planning stage
- Resolve ALL open questions before finalizing

❌ **Don't:**
- Write full plan in one shot without feedback
- Leave open questions or TODOs
- Guess about code behavior
- Include vague success criteria like "works well"

### Implementation Phase

✅ **Do:**
- Read the plan and all referenced files completely
- Create a task list to track progress
- Implement phases sequentially
- Update plan checkmarks as you complete sections
- Run automated verification after each phase
- Stop and communicate if reality doesn't match plan

❌ **Don't:**
- Implement all phases in parallel
- Skip automated verification
- Proceed when plan assumptions are violated
- Forget to update progress checkmarks

### Validation Phase

✅ **Do:**
- Run ALL automated checks from the plan
- Document pass/fail for each check
- List clear manual testing steps
- Identify deviations from plan
- Provide actionable recommendations

❌ **Don't:**
- Skip checks because "it should work"
- Assume tests pass without running them
- Ignore manual verification steps

## Resources

### Documentation
- [Claude Code Documentation](https://docs.anthropic.com/claude/docs) - Official Claude Code docs
- [Plugin Development Guide](https://github.com/anthropics/claude-code/docs/plugins) - Creating Claude Code plugins

### Related Plugins
- **scientific-python-development** - Scientific Python development with modern tooling
- **holoviz-visualization** - Development kit for HoloViz ecosystem

### Software Engineering Practices
- [The Pragmatic Programmer](https://pragprog.com/titles/tpp20/) - Classic software development guide
- [Clean Code](https://www.oreilly.com/library/view/clean-code-a/9780136083238/) - Code quality principles
- [Working Effectively with Legacy Code](https://www.oreilly.com/library/view/working-effectively-with/0131177052/) - Techniques for understanding existing codebases

## Troubleshooting

### Documents not being created

**Issue:** Commands run but no documents appear in `.agents/`

**Solution:**
- Check that you're running commands from the project root
- Verify `.agents/` directory exists (created automatically on first use)
- Check command output for error messages

### Plans have open questions

**Issue:** Generated plans contain unresolved questions or TODOs

**Solution:** This indicates the planning process was interrupted. Continue the planning conversation and ask Claude to:
1. Research code to find answers
2. Ask you for clarification on product decisions
3. Resolve all questions before finalizing

### Implementation doesn't match plan

**Issue:** During implementation, you discover the plan assumptions were wrong

**Solution:** This is expected! Stop implementation and either:
- Use `/iterate-plan` to update the plan based on discoveries
- Document the mismatch and get user feedback on how to proceed

### Can't find research documents

**Issue:** Planning command doesn't reference existing research

**Solution:** Ensure research documents are:
- Located in `.agents/` directory
- Named with `research-` prefix
- In markdown format (`.md` extension)

## Contributing

We welcome contributions to this plugin! You can:

- **Add new commands** - Extend the workflow with additional phases
- **Enhance existing commands** - Improve command prompts and guidance
- **Improve templates** - Add sections or enhance existing templates
- **Report issues** - Let us know if something is unclear or not working
- **Share examples** - Contribute real-world usage examples and patterns

See the main repository [CONTRIBUTING.md](../../CONTRIBUTING.md) for detailed guidelines.

### Development

To modify or extend the plugin:

1. **Edit command files** in `commands/` to change workflow steps
2. **Update agent** in `agents/` to change orchestration behavior
3. **Modify templates** in `skills/research-workflow-management/assets/` to change document structure
4. **Update skill** in `skills/` to change workflow guidance

### Testing

Test workflows end-to-end:

```bash
# Test research phase
/research test component

# Test planning phase
/plan test feature

# Test full workflow
# (Follow pattern examples above)
```

### Ideas for Enhancements

Potential additions that would enhance this plugin:

- **Code review command** - Automated code review against plan criteria
- **Retrospective command** - Post-implementation analysis and lessons learned
- **Dependency tracking** - Visualize dependencies between workflow documents
- **Metrics collection** - Track workflow effectiveness (time saved, issues caught)
- **Integration templates** - Templates for specific frameworks (React, Django, etc.)
- **Visualization** - Generate diagrams from research documents

## Questions or Feedback?

- **Issues**: Open an issue on [GitHub](https://github.com/uw-ssec/rse-agents/issues) with the label `ai-research-workflows`
- **Discussions**: Start a discussion on [GitHub Discussions](https://github.com/uw-ssec/rse-agents/discussions)
- **Pull Requests**: Submit improvements via [pull requests](https://github.com/uw-ssec/rse-agents/pulls)

## License

This plugin is part of the RSE Agents project. See [LICENSE](LICENSE) file for details.

## Authors

SSEC Research Team - [https://github.com/uw-ssec](https://github.com/uw-ssec)

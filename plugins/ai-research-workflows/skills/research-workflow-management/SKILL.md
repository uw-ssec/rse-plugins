---
name: research-workflow-management
description: Structured AI-enabled research workflows for software development. Covers the six-phase workflow (Research, Plan, Iterate Plan, Experiment, Implement, Validate) with templates for each phase.
user-invocable: false
metadata:
  assets:
    - assets/research-template.md
    - assets/plan-template.md
    - assets/experiment-template.md
    - assets/implement-template.md
    - assets/handoff-template.md
---

# Research Workflow Management

A structured, AI-enabled workflow for software development that guides you from initial research through to validated implementation. This skill provides a systematic approach to complex development tasks through distinct, well-defined phases.

## Workflow Overview

The research workflow consists of six phases:

1. **Research** (`/research`) — Document and understand existing code, patterns, and architecture
2. **Plan** (`/plan`) — Create detailed, testable implementation plans through interactive research
3. **Iterate Plan** (`/iterate-plan`) — Refine existing plans based on feedback or changed requirements
4. **Experiment** (`/experiment`) — Try multiple approaches before committing (optional)
5. **Implement** (`/implement`) — Execute the plan phase by phase with verification
6. **Validate** (`/validate`) — Systematically verify implementation against plan criteria

Each phase produces a structured markdown document saved to `.agents/` in your project root, creating an auditable trail of technical decisions and implementation details.

## Quick Reference Card

Use this decision tree to choose which workflow step to run:

```
Need to understand existing code?
└─> Research <topic>

Ready to design an implementation?
├─> Have research docs?
│   └─> Plan <feature> (references research automatically)
└─> No research docs?
    └─> Run Research first, then Plan

Need to adjust an existing plan?
└─> Iterate Plan <plan-file> <changes>

Uncertain about the best approach?
└─> Experiment <approach-question>

Ready to execute the plan?
└─> Implement <plan-file>

Implementation complete, need verification?
└─> Validate <plan-file>
```

## Document Naming Convention

All workflow documents are saved to `.agents/` with this naming pattern:

- `research-<slug>.md` — Example: `research-auth-system.md`
- `plan-<slug>.md` — Example: `plan-auth-system.md`
- `experiment-<slug>.md` — Example: `experiment-jwt-vs-session.md`
- `implement-<slug>.md` — Example: `implement-auth-system.md`

The slug is automatically derived from the command argument (lowercased and hyphenated).

**Note:** The `/iterate-plan` command edits existing plan documents in place. The `/validate` command produces inline validation reports rather than templated documents.

## Cross-Referencing Between Steps

Workflow phases build on each other through explicit references:

- **Plan documents** include a `## References` section listing research docs consulted
- **Experiment documents** reference both research and plan docs that inform the experiments
- **Implement documents** reference the specific plan being executed
- **Validation reports** reference both the plan and the implementation document

Each document uses relative links to referenced docs:
```markdown
[Research: Auth System](research-auth-system.md)
[Plan: Auth System Implementation](plan-auth-system.md)
```

This creates a navigable graph of technical decisions and their implementation.

## When to Use Each Step

### Research — Use when you need to:
- Understand how existing code works
- Document architecture patterns in the codebase
- Find where specific functionality lives
- Map out component interactions
- Build context before planning changes
- Answer technical questions about the codebase

**Output:** A comprehensive technical document explaining the current state with file references and architecture insights.

**Key principle:** Document what IS, not what SHOULD BE. You are a technical documentarian, not a critic.

### Plan — Use when you need to:
- Design a new feature implementation
- Plan a refactoring or architectural change
- Create a roadmap for complex multi-file changes
- Define success criteria and testing strategy
- Get stakeholder buy-in before implementation

**Output:** A detailed, phased implementation plan with measurable success criteria, specific file references, and testing strategy.

**Key principle:** Interactive and iterative. Ask questions, research patterns, get feedback at each stage before finalizing.

### Iterate Plan — Use when you need to:
- Adjust scope based on new requirements
- Add or remove phases from an existing plan
- Update success criteria after discoveries
- Refine implementation approach
- Fix issues found during planning review

**Output:** Updated plan document with surgical edits maintaining consistency.

**Key principle:** Verify assumptions with code research. Confirm understanding before making changes.

### Experiment — Use when you need to:
- Compare 2-3 distinct technical approaches
- Prototype before committing to a design
- Validate performance characteristics
- Test integration patterns with existing code
- Make evidence-based architectural decisions

**Output:** Comparative analysis with code prototypes, observations, and a clear recommendation.

**Key principle:** Actually run code. Don't theorize — test real implementations and record honest observations.

**Note:** This step is OPTIONAL. Only use when the best approach is genuinely uncertain.

### Implement — Use when you need to:
- Execute an approved plan phase by phase
- Track implementation progress with checkmarks
- Verify work against success criteria
- Pause for manual verification between phases
- Create an auditable implementation record

**Output:** Working implementation with updated plan checkmarks and an implementation summary document.

**Key principle:** Follow the plan's intent while adapting to reality. Communicate mismatches clearly.

### Validate — Use when you need to:
- Verify implementation matches the plan
- Run all automated verification checks
- Identify what needs manual testing
- Catch incomplete or incorrect implementations
- Generate a validation report for review

**Output:** Comprehensive validation report showing pass/fail status for each success criterion.

**Key principle:** Systematic and thorough. Validate what was actually built, not what was intended.

## Best Practices Checklist

### Research Phase
- [ ] Read referenced files completely (full file reads)
- [ ] Use parallel research when possible for comprehensive exploration
- [ ] Include specific file paths and line numbers
- [ ] Document patterns, not problems
- [ ] Save to `.agents/research-<slug>.md`

### Planning Phase
- [ ] Reference existing research documents
- [ ] Read all context files completely before delegating sub-tasks
- [ ] Ask focused questions that can't be answered from code
- [ ] Include measurable success criteria split into Automated and Manual
- [ ] Define "what we're NOT doing"
- [ ] Get feedback before finalizing each section
- [ ] Resolve ALL open questions before completing the plan
- [ ] Save to `.agents/plan-<slug>.md`

### Experimentation Phase (Optional)
- [ ] Define clear hypothesis and success criteria
- [ ] Actually run code prototypes, don't just theorize
- [ ] Record all observations, including failures
- [ ] Create honest comparison with trade-offs
- [ ] Make a clear recommendation with reasoning
- [ ] Save to `.agents/experiment-<slug>.md`

### Implementation Phase
- [ ] Read the plan and all referenced files completely
- [ ] Create a task list to track progress
- [ ] Implement phases sequentially, not in parallel
- [ ] Update plan checkmarks as you complete sections
- [ ] Run automated verification after each phase
- [ ] Pause for human verification between phases
- [ ] Stop and communicate if reality doesn't match the plan
- [ ] Save to `.agents/implement-<slug>.md` on completion

### Validation Phase
- [ ] Read the plan completely
- [ ] Verify each phase's completion status
- [ ] Run all automated verification commands from the plan
- [ ] Document pass/fail status for each check
- [ ] List clear manual testing steps
- [ ] Identify deviations from the plan
- [ ] Provide actionable recommendations

## Template Assets

This skill provides four document templates in `${CLAUDE_PLUGIN_ROOT}/skills/research-workflow-management/assets/`:

- `research-template.md` — Structure for research documentation
- `plan-template.md` — Structure for implementation plans
- `experiment-template.md` — Structure for experiment reports
- `implement-template.md` — Structure for implementation summaries

Commands automatically use these templates when generating workflow documents.

## Workflow Philosophy

This structured approach provides several benefits:

1. **Separation of concerns** — Research, planning, and implementation are distinct activities with different goals
2. **Incremental progress** — Each phase produces concrete artifacts that can be reviewed independently
3. **Reduced cognitive load** — Focus on one type of work at a time rather than trying to do everything simultaneously
4. **Better collaboration** — Documents provide clear communication artifacts for stakeholders
5. **Auditable decisions** — Technical choices are documented with their context and reasoning
6. **Reduced rework** — Issues are caught during planning rather than after implementation

The workflow is designed to be flexible — you can skip optional phases like experimentation or iterate on plans as requirements evolve. The key is maintaining clear documentation of what was built and why.

## Common Workflow Patterns

### Pattern 1: Simple Feature Addition
1. Research existing patterns
2. Plan new feature
3. Implement plan

### Pattern 2: Complex Architectural Change
1. Research current architecture
2. Plan architectural change
3. Experiment with approach comparison
4. Iterate plan to incorporate experiment results
5. Implement plan
6. Validate plan

### Pattern 3: Rapid Iteration
1. Plan initial approach
2. Iterate plan for scope adjustment
3. Iterate plan to add phase
4. Implement plan

### Pattern 4: Investigation + Documentation
1. Research system behavior
2. Research related component (follow-up)
3. Use research docs for future planning

## Integration with Other Workflows

This workflow integrates seamlessly with standard development practices:

- **After implementation**: Create a git commit with your changes
- **After validation passes**: Create a pull request for review
- **During planning**: Reference existing documentation and code patterns
- **During research**: Use available code exploration tools

The structured workflow complements rather than replaces your existing development process.

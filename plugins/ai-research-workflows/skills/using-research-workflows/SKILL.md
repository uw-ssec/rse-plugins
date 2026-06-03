---
name: using-research-workflows
description: >-
  Use when starting or continuing research-software work and you need to decide
  which workflow skill to use next or how interactive to be. Triggers: research
  workflow, which skill should I use, where do I start, guide me through the
  workflow, structured development.
---

# Using Research Workflows

This plugin is a set of skills for research-software development that guides
work from initial exploration through to validated, reproducible implementation.
This meta-skill helps you pick the right skill to invoke and sequence them in
an order that suits the task at hand — from a quick feature addition to a
full architectural change with prior-art research, experimentation, and hardened
code.

## Choosing a skill (decision tree)

```text
Need to understand existing code?            → researching-codebases
Need to research a topic / prior work/tools? → researching-prior-art
Ready to design an implementation?           → planning-implementations
Need to adjust an existing plan?             → iterating-plans
Unsure which technical approach is best?     → running-experiments
Ready to execute an approved plan?           → implementing-plans
Implementation complete, need verification?  → validating-implementations
Need a result to be reproducible?            → ensuring-reproducibility
Research code needs to be made robust?       → hardening-research-code
Transferring work to another session?        → creating-handoffs
```

## Interaction modes

Every workflow skill starts by selecting one of two interaction modes.
**Collaborative** mode asks one question at a time, proposes options with a
recommendation, and gates on approval before producing artifacts — the
brainstorming and planning feel. **Direct** mode acts on stated intent,
narrates progress briefly, and stops only when genuinely blocked or before an
irreversible action — the execution feel. Explicit user phrasing wins
("brainstorm with me" → Collaborative; "just do it" → Direct); absent that,
vague or exploratory requests default to Collaborative, specific directives with
enough context default to Direct. Hard stops (destructive, irreversible, or
outward-facing actions) always require confirmation regardless of mode.

Full protocol: `${CLAUDE_PLUGIN_ROOT}/skills/using-research-workflows/references/interaction-modes.md`.

## Document naming & cross-references

All workflow documents are saved to `.agents/` in the project root. Naming
conventions:

- `research-<slug>.md` — codebase research (e.g. `research-auth-system.md`)
- `prior-art-<slug>.md` — prior-art / topic research (e.g. `prior-art-jwt-libraries.md`)
- `plan-<slug>.md` — implementation plan (e.g. `plan-auth-system.md`)
- `experiment-<slug>.md` — experiment report (e.g. `experiment-jwt-vs-session.md`)
- `implement-<slug>.md` — implementation summary (e.g. `implement-auth-system.md`)
- `handoff-<timestamp>-<slug>.md` — handoff document (e.g. `handoff-20240315-auth-system.md`)

The slug is derived from the topic or feature name (lowercased, hyphenated).
Docs cross-link via relative markdown links:

```markdown
[Research: Auth System](research-auth-system.md)
[Plan: Auth System Implementation](plan-auth-system.md)
```

This creates a navigable graph of technical decisions and their context:

- **Plan documents** list research and prior-art docs consulted.
- **Experiment documents** reference research, prior-art, and plan docs.
- **Implement documents** reference the specific plan being executed.
- **Validation reports** reference both the plan and the implementation document.
- **Handoff documents** reference all prior documents for the feature.

## Common workflow patterns

### Full workflow (complex architectural change)

`researching-codebases` → `planning-implementations` → `running-experiments` →
`iterating-plans` → `implementing-plans` → `validating-implementations`

### Simple feature addition

`researching-codebases` → `planning-implementations` → `implementing-plans`

### Rapid iteration

`planning-implementations` → `iterating-plans` → `iterating-plans` →
`implementing-plans`

### Research-only / investigation

`researching-codebases` → `researching-codebases` (follow-up) — use docs for
future planning sessions.

### Research-first (unknown problem space)

`researching-prior-art` → `planning-implementations`

## Cross-plugin deferral

Some concerns are better handled by specialist plugins. Hand off to them rather
than re-implementing their guidance here.

| Concern | Defer to |
|---|---|
| Environments (pixi) | `scientific-python-development:pixi-package-manager` |
| Environments (uv) | `python-development:uv-package-manager` |
| Tests | `scientific-python-development:python-testing` |
| Packaging | `scientific-python-development:python-packaging` |
| Documentation | `scientific-python-development:scientific-documentation` |
| Community / handoff readiness | `project-management:community-health-files` |
| Project handoff | `project-management:project-handoff` |
| Heavy multi-source research | `deep-research` |

## Common Mistakes

- **Forcing the full workflow when a single skill suffices** — invoking the entire chain for a minor change wastes time. Use the decision tree to pick exactly the skill that matches the current need.
- **Skipping research or prior-art before planning** — jumping straight to `planning-implementations` without first understanding the codebase or existing approaches produces plans that miss critical context.
- **Not picking an interaction mode** — every workflow skill defaults to a mode, but failing to confirm the right mode for the task leads to unnecessary interruptions (Collaborative when Direct is wanted) or unreviewed decisions (Direct when Collaborative is needed).
- **Treating this skill as a substitute for the specialist skills** — this meta-skill routes and orients; the actual work happens in the individual skills. Invoke the right specialist skill rather than asking this one to execute.

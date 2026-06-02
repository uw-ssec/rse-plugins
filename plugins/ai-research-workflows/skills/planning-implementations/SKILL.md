---
name: planning-implementations
description: >-
  Use when a feature, refactor, or multi-file change needs to be designed before
  coding — breaks work into testable phases, identifies component dependencies,
  defines Automated and Manual success criteria, and produces a saved plan in
  .agents/ (plan-SLUG.md). Triggers: plan X, design the implementation, how
  should we build X, create an implementation plan.
---

# Planning Implementations

Produce a comprehensive, phased implementation plan grounded in actual codebase
research, with measurable success criteria and no unresolved decisions.

## Interaction mode

Choose a mode before acting. Full protocol: `${CLAUDE_PLUGIN_ROOT}/skills/using-research-workflows/references/interaction-modes.md`.

1. **Explicit override wins** — "brainstorm / walk me through / help me think" → Collaborative; "just do it / don't ask / go ahead" → Direct.
2. **Else infer** — vague/exploratory phrasing, or required inputs missing → Collaborative; a specific directive with enough context → Direct.
3. **Else default** — this skill leans **Collaborative**.
4. **Hard stops, regardless of mode** — destructive, irreversible, or outward-facing actions always get a confirmation first.

## Starting the skill

If no topic is given, enter Collaborative mode and ask what to plan (and check
`.agents/` for existing research/prior-art). If the topic is given without a
research doc, look for `.agents/research-*.md` matches and suggest running
`researching-codebases` first if none are found — then proceed on user
preference.

## Process

### Step 1: Context Gathering

- Read all mentioned files **completely** before anything else.
- Check `.agents/research-*.md`, `.agents/prior-art-*.md` for relevant context.
- Investigate related files, existing patterns, integration points, and test
  coverage in parallel where possible.
- Only ask questions that code cannot answer (product decisions, ambiguous
  scenarios). Never ask "which database?" — read the code.
- In Collaborative mode, present findings and focused questions before
  proceeding.

### Step 2: Research & Discovery

- Investigate in parallel: existing patterns, integration points, available
  dependencies, current test coverage.
- **Wait for all research to complete** before synthesizing.
- In Collaborative mode, present design options with pros/cons and a
  recommendation; get approval before continuing.

### Step 3: Plan Structure (Collaborative mode)

- Propose a phased breakdown with a one-line objective per phase.
- Get feedback before writing detailed steps.

### Step 4: Plan Writing

Generate filename from the topic slug (`plan-<slug>.md`). Read the template:
`${CLAUDE_PLUGIN_ROOT}/skills/planning-implementations/assets/plan-template.md`.

**Required sections:**

1. Overview — what, why, high-level how
2. Current State Analysis — existing code with `file:line` references
3. Desired End State — observable success outcomes
4. What We're NOT Doing — explicit scope boundaries
5. Implementation Approach — technical strategy and key decisions
6. Implementation Phases — phased tasks with file paths and verification steps
7. Success Criteria — split into Automated and Manual (see below)
8. Testing Strategy — unit, integration, manual
9. References — research docs, files analyzed, external docs

Each phase needs: a clear objective, tasks with `path/to/file.ext:lines`,
dependencies on prior phases, and verification steps.

#### Success Criteria split

**Automated Verification** — commands agents can run without human intervention
(`make test`, `pytest`, file-existence checks, linters).

**Manual Verification** — steps requiring human judgment (UI behavior, UX, edge
cases, performance under real conditions).

#### Blocking rule: NO open questions

If an uncertainty surfaces while writing, **stop**, then either research the
code to resolve it or ask the user. Resume only after it is resolved. A plan
section titled "Open Questions" with unresolved items is **not acceptable**.

### Step 5: Review & Iterate (Collaborative mode)

Present a summary (approach, phase count, criteria counts) and ask for feedback
on phasing, success criteria, technical approach, and edge cases.

For major revisions use the `iterating-plans` skill.

## References and output

- Ground the plan in `.agents/research-*.md` and `.agents/prior-art-*.md`;
  incorporate `.agents/experiment-*.md` when present.
- List all referenced docs in the References section with relative markdown links.
- Create `.agents/` if needed; write to `.agents/plan-<slug>.md`.
- To revise an existing plan use `iterating-plans`; to execute use
  `implementing-plans`.

## Quality checklist

Before completing the plan verify:

- [ ] All referenced files read completely
- [ ] All research completed and incorporated
- [ ] User consulted on approach and structure (Collaborative mode)
- [ ] Official template used
- [ ] Saved to `.agents/plan-<slug>.md`
- [ ] Every phase has `file:line` references
- [ ] Success criteria split into Automated and Manual
- [ ] Criteria are measurable and concrete
- [ ] "What We're NOT Doing" section is filled out
- [ ] NO open questions remain
- [ ] References section links to research and experiment docs

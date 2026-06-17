---
name: planning-implementations
description: >-
  Use when a feature, refactor, or multi-file change needs to be designed before
  coding. Triggers: plan X, design the implementation, how should we build X,
  create an implementation plan.
---

# Planning Implementations

Produce a comprehensive, phased implementation plan grounded in actual codebase
research, with measurable success criteria and no unresolved decisions.

## Interaction mode

This skill leans **Collaborative** by default. For the full Collaborative-vs-Direct protocol and override rules, see the Interaction Modes reference in the `ai-research-workflows:using-research-workflows` skill.

## Starting the skill

If no topic is given, enter Collaborative mode and ask what to plan (and check
`docs/rse/specs/` (then legacy `.agents/`) for existing research/prior-art). If the topic is given without a
research doc, look for `docs/rse/specs/research-*.md` matches and suggest running
`ai-research-workflows:researching` first if none are found — then proceed on user
preference.

## Process

### Step 1: Context Gathering

- Read all mentioned files **completely** before anything else.
- Check `docs/rse/specs/research-*.md` (and legacy `.agents/research-*.md`, `.agents/prior-art-*.md`) for relevant context.
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
`assets/plan-template.md`.

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

#### Bite-sized, test-first tasks

Each phase's tasks must be **executable steps an engineer can follow without
guessing**, sequenced test-first. Write the actual content, not a description:

- Sequence each unit of work as: write the failing test → run it, watch it fail
  → implement the minimal code → run the test, watch it pass → commit.
- Show the actual code or the exact command for any step that changes code or
  runs something — never a paraphrase.
- Reference an exact `path/to/file.ext:line` for every task.

(For numerical/research code, the "failing test" is an assertion against a known
result, analytic case, or invariant — see `ai-research-workflows:hardening-research-code`.)

#### Blocking rule: NO placeholders

A step that says *what* to do without showing *how* is a plan failure. Never
ship any of these — resolve each before saving:

- "TBD", "TODO", "implement later", "fill in details".
- "Add appropriate error handling" / "add validation" / "handle edge cases" —
  name the specific cases and show how each is handled.
- "Write tests for the above" without the actual test code.
- "Similar to Phase N" — repeat the code; phases may be executed out of order.
- Any reference to a type, function, or file not defined in some task.

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

For major revisions use the `ai-research-workflows:iterating-plans` skill.

## References and output

- Ground the plan in `docs/rse/specs/research-*.md` (and legacy `.agents/research-*.md`, `.agents/prior-art-*.md`);
  incorporate `docs/rse/specs/experiment-*.md` (or legacy `.agents/experiment-*.md`) when present.
- List all referenced docs in the References section with relative markdown links.
- Create `docs/rse/specs/` if needed; write to `docs/rse/specs/plan-<slug>.md`.
- To revise an existing plan use `ai-research-workflows:iterating-plans`; to execute use
  `ai-research-workflows:implementing-plans`.

## Common Mistakes

- **Confirming approach too late** — writing a detailed multi-phase plan before the user has approved the overall strategy wastes effort; in Collaborative mode, get approach sign-off after Step 2.
- **Placeholder tasks** — "add appropriate error handling", "write tests for the above", or any step that states intent without the concrete code/command is a plan the executor cannot follow; write the actual content.
- **Tests bolted on at the end** — lumping all tests into a trailing Testing Strategy section produces tests-last code; sequence tasks test-first (the failing test before the implementation) within each phase.
- **Vague success criteria** — "works well" or "passes tests" is not a criterion; every item must be a concrete, runnable command or an observable human-verifiable outcome.
- **Unsplit Automated vs Manual** — lumping all criteria together hides what requires human judgment; always separate the two categories explicitly.
- **Leaving open questions in the "final" plan** — a plan section titled "Open Questions" with unresolved items ships ambiguity to the implementer; resolve or explicitly defer every question before saving the plan.
- **Skipping scope boundaries** — omitting the "What We're NOT Doing" section lets scope creep in silently; fill it out even when the answer seems obvious.

## Quality checklist

Before completing the plan verify:

- [ ] All referenced files read completely
- [ ] All research completed and incorporated
- [ ] User consulted on approach and structure (Collaborative mode)
- [ ] Official template used
- [ ] Saved to `docs/rse/specs/plan-<slug>.md`
- [ ] Every phase has `file:line` references
- [ ] Phase tasks are bite-sized and test-first (failing test before implementation)
- [ ] No placeholder tasks ("add appropriate error handling", "write tests for the above", or intent-without-code)
- [ ] Success criteria split into Automated and Manual
- [ ] Criteria are measurable and concrete
- [ ] "What We're NOT Doing" section is filled out
- [ ] NO open questions remain
- [ ] References section links to research and experiment docs

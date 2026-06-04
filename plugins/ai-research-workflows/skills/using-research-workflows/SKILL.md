---
name: using-research-workflows
description: >-
  Use when starting or continuing ANY research-software task — understanding or
  modifying code, surveying prior art, planning, experimenting, implementing,
  validating, reproducing, or hardening — and before reading code to "just
  check", before editing, or before answering "how does X work". Triggers:
  research workflow, which skill should I use, where do I start, guide me through
  the workflow, structured development.
---

# Using Research Workflows

This plugin is a set of skills for research-software development that guides work
from initial exploration through to validated, reproducible implementation. This
meta-skill makes you *use* the right skill — it does not just list them.

<EXTREMELY-IMPORTANT>
If there is even a 1% chance a research-workflow skill applies to what you are
about to do, you MUST invoke it before acting — before reading code to "just
check", before editing, before answering a "how does X work" question.

IF A SKILL APPLIES, YOU DO NOT HAVE A CHOICE. Invoke it. You cannot rationalize
your way past this because you are in a hurry, because the change "looks small",
or because the user said "don't overthink it".

This compels using the **right** skill, not running the whole chain. Right-sizing
the workflow (see *Common workflow patterns*) means picking the minimal matching
skill — a quick `researching` read, a short plan. Right-sized never means **zero
skills** for code or research work.
</EXTREMELY-IMPORTANT>

## Instruction priority

The user is in control. Priority order:

1. **The user's explicit instructions** — highest.
2. **These workflow skills** — override default behavior where they conflict.
3. **The default system prompt** — lowest.

"Don't plan, just write it" from the user wins. But "add retry logic" or "fix
the loader" states **WHAT** to do — it is not permission to skip the workflow.

## The rule

Invoke the relevant skill BEFORE any response or action. If an invoked skill
turns out not to fit, drop it — but you must check first. A directive ("just add
X", "fix Y") never authorizes skipping straight to code.

## Choosing a skill (decision tree)

```text
Need to understand code or survey prior art? → researching
Ready to design an implementation?           → planning-implementations
Need to adjust an existing plan?             → iterating-plans
Unsure which technical approach is best?     → running-experiments
Ready to execute an approved plan?           → implementing-plans
Implementation complete, need verification?  → validating-implementations
Need a result to be reproducible?            → ensuring-reproducibility
Research code needs to be made robust?       → hardening-research-code
Transferring work to another session?        → creating-handoffs
```

Invoke any skill by its fully-qualified id `ai-research-workflows:<name>` (e.g.
`ai-research-workflows:planning-implementations`). The short names above and in
the workflow chains below refer to these.

## Skill priority & sequencing

Process-shaping skills come before execution: understand before you plan, plan
before you build, verify after.

1. **Understand first** — don't write or modify code until you've engaged
   `researching`; for anything non-trivial, then `planning-implementations`.
2. **Build second** — `implementing-plans` executes an approved plan.
3. **Verify last** — `validating-implementations`, plus `ensuring-reproducibility`
   / `hardening-research-code` whenever a result will be reported or relied on.

## Interaction modes

Every workflow skill starts by selecting one of two interaction modes.
**Collaborative** mode asks one question at a time, proposes options with a
recommendation, and gates on approval before producing artifacts — the
brainstorming and planning feel. **Direct** mode acts on stated intent, narrates
progress briefly, and stops only when genuinely blocked or before an irreversible
action — the execution feel. Explicit user phrasing wins ("brainstorm with me" →
Collaborative; "just do it" → Direct); absent that, vague or exploratory requests
default to Collaborative, specific directives with enough context default to
Direct. Hard stops (destructive, irreversible, or outward-facing actions) always
require confirmation regardless of mode. Note: "just do it" / "don't overthink
it" selects **Direct mode** — it does not switch off the workflow.

Full protocol: `references/interaction-modes.md`.

## Red flags — STOP, you're rationalizing

These thoughts mean you are about to skip a skill you should invoke:

| Thought | Reality |
|---|---|
| "This is just a quick data/code question" | Questions are tasks. Invoke `researching`. |
| "I'll just tweak the code real quick" | Code changes need understanding first → `researching` then `planning-implementations`. |
| "I already know how this codebase works" | Memory drifts; the code is ground truth. Trace it with `researching`. |
| "5 minutes — don't overthink it" | Right-size the skill, don't skip it. A 90-second read still beats a stale-cache bug. |
| "This change is too small for a plan" | Small multi-file / network / state changes break callers. Plan it. |
| "It's just an experiment, no rigor needed" | Experiments drive design decisions → `running-experiments`; record failures too. |
| "The result obviously reproduces" | Unverified provenance is a hypothesis → `ensuring-reproducibility`. |
| "I'll capture provenance / harden it later" | Later never comes. Do it when the result is produced. |

## Common workflow patterns

Right-size the chain to the task — these are the menu, not a mandate to run all.

### Full workflow (complex architectural change)

`researching` → `planning-implementations` → `running-experiments` →
`iterating-plans` → `implementing-plans` → `validating-implementations`

### Simple feature addition

`researching` → `planning-implementations` → `implementing-plans`

### Rapid iteration

`planning-implementations` → `iterating-plans` → `iterating-plans` →
`implementing-plans`

### Research-only / investigation

`researching` → `researching` (follow-up) — use docs for future planning.

### Research-first (unknown problem space)

`researching` → `planning-implementations`

## Document naming & cross-references

All workflow documents are saved to `docs/rse/specs/` in the project root as
`research-<slug>.md`, `plan-<slug>.md`, `experiment-<slug>.md`,
`implement-<slug>.md`, and `handoff-<timestamp>-<slug>.md` (slug = lowercased,
hyphenated topic). These are committed, version-controlled artifacts — the
decision record lives in the repo. **Write** new documents to `docs/rse/specs/`;
when **reading** existing documents, search `docs/rse/specs/` first and fall back
to the legacy `.agents/` location (older layout). Legacy `prior-art-<slug>.md`
docs are still read when present.
Docs cross-link with relative markdown links so plan → research, implement → plan,
validation → plan+implement, and handoff → all of them form a navigable graph.
Each skill states its own naming and cross-reference rules.

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

- **Skipping the workflow because the task "looks small"** — the most common and
  most expensive mistake. Right-size the skill (a quick `researching` read, a
  short plan), but never skip skill-invocation entirely for code or research
  work. See *Red flags* above.
- **Forcing the *full* chain when one skill suffices** — the opposite error:
  running research → plan → experiment → implement → validate for a trivial change
  wastes time. Pick the minimal matching skill from the decision tree. This is
  about right-sizing, never about reaching zero skills.
- **Not picking an interaction mode** — every workflow skill defaults to a mode,
  but failing to confirm the right mode leads to unnecessary interruptions
  (Collaborative when Direct is wanted) or unreviewed decisions (Direct when
  Collaborative is needed).
- **Treating this skill as a substitute for the specialist skills** — this
  meta-skill routes and compels; the actual work happens in the individual
  skills. Invoke the right specialist skill rather than asking this one to execute.

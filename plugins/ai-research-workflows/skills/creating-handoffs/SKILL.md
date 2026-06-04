---
name: creating-handoffs
description: >-
  Use when work context must transfer to another session or person. Triggers:
  create a handoff, hand off this work, summarize context for the next session,
  prepare a handoff.
---

# Creating Handoffs

Produce a handoff document that transfers full working context to the next session with no information loss.

## Interaction mode

This skill leans **Direct** by default. For the full Collaborative-vs-Direct protocol and override rules, see the Interaction Modes reference in the `ai-research-workflows:using-research-workflows` skill.

## Process

### 1. Gather context

Run these in parallel where possible:

**Git state:**
- Current branch name
- Current commit hash (short)
- Summary of uncommitted changes (`git status` and `git diff --stat`)

**Workflow artifacts** — search `docs/rse/specs/` (then legacy `.agents/`) for:
- `research-*.md` — research documents
- `plan-*.md` — plan documents
- `experiment-*.md` — experiment documents
- `implement-*.md` — implementation documents
- `handoff-*.md` — previous handoff documents

**Session context:**
- Review the conversation to understand what tasks were worked on.
- Identify the current workflow phase (Research, Plan, Iterate Plan, Experiment, Implement, Validate).
- Note which workflow artifacts were produced or referenced this session.

**Research state (for research/scientific work):**
- Random seeds, the active environment/lockfile (`pixi.lock` / `uv.lock`), and
  dataset versions/paths/checksums in play.
- Partial or intermediate results, saved checkpoints/outputs, and any
  long-running experiment or job still in flight — with how to check or resume it.

### 2. Determine what's relevant

From the gathered context, identify:

- **Tasks:** What was being worked on and the status of each (completed, in progress, planned).
- **Current phase:** Where in the workflow cycle the work sits.
- **Artifacts:** Which `docs/rse/specs/` documents are relevant.
- **Critical files:** The 2–3 most important files the next session must read first.
- **Recent changes:** What code was modified (use `file:line` references).
- **Learnings:** Important discoveries, patterns, or gotchas.
- **Research state:** seeds, environment/lockfile, data versions, and partial
  results needed to resume (see `ai-research-workflows:ensuring-reproducibility`).
- **Verification status:** what is tested and passing vs. broken or unverified,
  and what is uncommitted or unpushed.
- **Next steps:** What the next session should do, in priority order.

### Report true state — don't paper over broken work

A handoff must reflect reality, not a tidy fiction. Before generating the
document, explicitly surface:

- **Uncommitted / unpushed work** — name it; the next session cannot see your
  working tree.
- **Failing or unrun tests** — state which, with the actual status; never imply
  green when it isn't.
- **Unreproducible or unverified results** — flag any result that has not been
  reproduced or whose provenance is incomplete.

Put these in a "Known-broken / unverified" callout in the handoff. A clean-looking
handoff that hides broken state is worse than none — it sends the next session
down a false trail.

### 3. Generate the handoff document

**Filename format:** `handoff-YYYY-MM-DD-HH-MM-<slug>.md`
- `YYYY-MM-DD-HH-MM` is the current date and time.
- `<slug>` is a brief kebab-case description of the work.
- Example: `handoff-2025-06-15-14-30-auth-system-refactor.md`

**Read the handoff template:**
`assets/handoff-template.md`

**Fill out all sections:**
- Replace all placeholder text with actual content.
- Remove artifact sections that don't apply (e.g., if no experiments were run, remove Experiment Reports).
- Be specific — use `file:line` references, not vague descriptions.
- Name the recommended next skill for the receiving session based on the current phase (e.g., `ai-research-workflows:implementing-plans`, `ai-research-workflows:validating-implementations`).

**Save to** `docs/rse/specs/handoff-YYYY-MM-DD-HH-MM-<slug>.md`.

### 4. Present the handoff

After saving, present a concise summary:

```
## Handoff Created

**File:** `docs/rse/specs/handoff-<filename>.md`
**Current Phase:** [phase]
**Status:** [brief status of work]

### Quick Summary
[2–3 sentence summary of what was done and what's next]

### For the Next Session
Start by running:
> Read the handoff document at `docs/rse/specs/handoff-<filename>.md` and resume the work described within.

Or to continue with the workflow:
> [recommended-skill] [relevant arguments]
```

## Writing guidelines

- **More information, not less.** The template is the minimum; always include more when necessary.
- **Be thorough and precise.** Include both top-level objectives and lower-level details.
- **Avoid excessive code snippets.** Prefer `path/to/file.ext:line` references. Only include code blocks when describing an error being debugged or a critical pattern.
- **Cross-reference workflow artifacts.** Link to research, plan, experiment, and implementation documents by filename so the next session can read them.
- **Name the recommended next skill.** Based on where you are in the workflow, tell the next session which skill to invoke next (e.g., `ai-research-workflows:implementing-plans`, `ai-research-workflows:validating-implementations`).
- **Include learnings.** Capture non-obvious insights about the codebase, patterns that matter, or gotchas encountered.

## Common Mistakes

- **Dumping raw history instead of a focused summary** — pasting the full conversation or every git commit message produces an unreadable wall of text. Distil to what the next session actually needs to act.
- **Omitting the critical files to read first** — the most common cause of a slow hand-off restart is not knowing where to begin. Always name the 2–3 files the next session must read before doing anything else.
- **Not naming the recommended next skill** — leaving "next steps" vague forces the receiving session to re-derive the workflow position. Always state the exact skill to invoke next (e.g., `ai-research-workflows:implementing-plans`).
- **Missing learnings and gotchas** — documenting what was done without capturing why certain decisions were made, or what dead ends were hit, forces the next session to rediscover them.
- **A clean-looking handoff that hides broken state** — omitting failing tests, uncommitted work, or unverified results sends the next session down a false trail; surface them in a "Known-broken / unverified" callout.
- **Omitting research state** — leaving out seeds, environment/lockfile, dataset versions, partial results, or in-flight jobs makes the work impossible to resume or reproduce; capture them for any research/scientific work.

## Cross-references

- Use `ai-research-workflows:implementing-plans` as the recommended next skill when a plan is approved and ready to execute.
- Use `ai-research-workflows:validating-implementations` when implementation is complete and needs verification.
- Use `ai-research-workflows:planning-implementations` or `ai-research-workflows:iterating-plans` when the next session needs to (re-)design the approach.
- All handoff documents are picked up automatically by `ai-research-workflows:using-research-workflows` when it surveys `docs/rse/specs/` (and legacy `.agents/`).

---
name: creating-handoffs
description: >-
  Use when work context must transfer to another session or person — produces a
  concise but thorough handoff document capturing state, artifacts, key files,
  learnings, and next steps. Trigger phrases: create a handoff, hand off this
  work, summarize context for the next session, write a handoff, prepare a
  handoff.
---

# Creating Handoffs

Produce a handoff document that transfers full working context to the next session with no information loss.

## Interaction mode

Choose a mode before acting. Full protocol: `${CLAUDE_PLUGIN_ROOT}/skills/using-research-workflows/references/interaction-modes.md`.

1. **Explicit override wins** — "brainstorm / walk me through / help me think" → Collaborative; "just do it / don't ask / go ahead" → Direct.
2. **Else infer** — vague/exploratory phrasing, or required inputs missing → Collaborative; a specific directive with enough context → Direct.
3. **Else default** — this skill leans **Direct**.
4. **Hard stops, regardless of mode** — destructive, irreversible, or outward-facing actions always get a confirmation first.

## Process

### 1. Gather context

Run these in parallel where possible:

**Git state:**
- Current branch name
- Current commit hash (short)
- Summary of uncommitted changes (`git status` and `git diff --stat`)

**Workflow artifacts** — search `.agents/` for:
- `research-*.md` — research documents
- `plan-*.md` — plan documents
- `experiment-*.md` — experiment documents
- `implement-*.md` — implementation documents
- `handoff-*.md` — previous handoff documents

**Session context:**
- Review the conversation to understand what tasks were worked on.
- Identify the current workflow phase (Research, Plan, Iterate Plan, Experiment, Implement, Validate).
- Note which workflow artifacts were produced or referenced this session.

### 2. Determine what's relevant

From the gathered context, identify:

- **Tasks:** What was being worked on and the status of each (completed, in progress, planned).
- **Current phase:** Where in the workflow cycle the work sits.
- **Artifacts:** Which `.agents/` documents are relevant.
- **Critical files:** The 2–3 most important files the next session must read first.
- **Recent changes:** What code was modified (use `file:line` references).
- **Learnings:** Important discoveries, patterns, or gotchas.
- **Next steps:** What the next session should do, in priority order.

### 3. Generate the handoff document

**Filename format:** `handoff-YYYY-MM-DD-HH-MM-<slug>.md`
- `YYYY-MM-DD-HH-MM` is the current date and time.
- `<slug>` is a brief kebab-case description of the work.
- Example: `handoff-2025-06-15-14-30-auth-system-refactor.md`

**Read the handoff template:**
`${CLAUDE_PLUGIN_ROOT}/skills/creating-handoffs/assets/handoff-template.md`

**Fill out all sections:**
- Replace all placeholder text with actual content.
- Remove artifact sections that don't apply (e.g., if no experiments were run, remove Experiment Reports).
- Be specific — use `file:line` references, not vague descriptions.
- Name the recommended next skill for the receiving session based on the current phase (e.g., `implementing-plans`, `validating-implementations`).

**Save to** `.agents/handoff-YYYY-MM-DD-HH-MM-<slug>.md`.

### 4. Present the handoff

After saving, present a concise summary:

```
## Handoff Created

**File:** `.agents/handoff-<filename>.md`
**Current Phase:** [phase]
**Status:** [brief status of work]

### Quick Summary
[2–3 sentence summary of what was done and what's next]

### For the Next Session
Start by running:
> Read the handoff document at `.agents/handoff-<filename>.md` and resume the work described within.

Or to continue with the workflow:
> [recommended-skill] [relevant arguments]
```

## Writing guidelines

- **More information, not less.** The template is the minimum; always include more when necessary.
- **Be thorough and precise.** Include both top-level objectives and lower-level details.
- **Avoid excessive code snippets.** Prefer `path/to/file.ext:line` references. Only include code blocks when describing an error being debugged or a critical pattern.
- **Cross-reference workflow artifacts.** Link to research, plan, experiment, and implementation documents by filename so the next session can read them.
- **Name the recommended next skill.** Based on where you are in the workflow, tell the next session which skill to invoke next (e.g., `implementing-plans`, `validating-implementations`).
- **Include learnings.** Capture non-obvious insights about the codebase, patterns that matter, or gotchas encountered.

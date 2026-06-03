# Codebase Research Pass

How to investigate the *current* codebase for the `researching` skill.

## Stance

Describe what the code does and how, with `file:line` references. You may note
gaps and light, clearly-labeled observations ("note: no error handling on this
path"), but defer deep critique and redesign to planning/validation. Do not
rewrite or refactor.

## Steps

### 1. Read directly mentioned files first

If the user names specific files, read them **completely** before delegating any
sub-tasks. Partial reads miss critical information and produce worse sub-task
queries.

### 2. Decompose into parallel sub-questions

Break the topic into focused, read-only sub-questions covering:

- WHERE specific files/components live (use `grep`, `find`, or ripgrep)
- HOW a component works (read files, trace call paths)
- WHAT patterns exist (find representative examples)

Frame every query as "find", "explain", "document", "trace", or "map".

**Launch sub-questions concurrently** — 3–5 parallel read-only tasks beat
sequential investigation.

**No subagents?** If your platform has no parallel sub-agent support, investigate
each sub-question sequentially in the main context instead. Gather the same
evidence, just one query at a time.

### 3. Synthesize

Wait until every sub-question reports back, then:

- Compile results into a coherent narrative grouped by component or concern.
- Include `file:line` references throughout.
- Trace data flows and call hierarchies.
- Surface repeating patterns and any gaps you noticed.

The result becomes the **Codebase Findings** section of `.agents/research-<slug>.md`.

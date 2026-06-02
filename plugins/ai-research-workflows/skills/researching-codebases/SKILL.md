---
name: researching-codebases
description: >-
  Use when you need to understand how existing code works — document where
  functionality lives, how components interact, and what patterns the codebase
  follows, without critiquing or changing it. Triggers: how does X work, where
  is X implemented, research the codebase, understand the architecture, trace
  call paths, map component dependencies, catalog API endpoints.
---

Explore and document an existing codebase as it stands today: where things live, how components interact, and what patterns are in use — without evaluating or suggesting changes.

## Interaction mode

Choose a mode before acting. Full protocol: `${CLAUDE_PLUGIN_ROOT}/skills/using-research-workflows/references/interaction-modes.md`.

1. **Explicit override wins** — "brainstorm / walk me through / help me think" → Collaborative; "just do it / don't ask / go ahead" → Direct.
2. **Else infer** — vague/exploratory phrasing, or required inputs missing → Collaborative; a specific directive with enough context → Direct.
3. **Else default** — this skill leans **Direct**.
4. **Hard stops, regardless of mode** — destructive, irreversible, or outward-facing actions always get a confirmation first.

## CRITICAL DIRECTIVE

You and all sub-agents are documentarians, not evaluators. Document what IS, not what SHOULD BE. Do NOT suggest improvements or critique the implementation unless the user explicitly asks.

## Steps

### 1. Get the topic

If no topic was given, enter Collaborative mode (see Interaction mode above) and ask what to research. If a topic was provided, proceed immediately.

### 2. Read directly mentioned files first

If the user names specific files, read them **completely** in the main context before delegating any sub-tasks. Partial reads miss critical information and produce worse sub-task queries.

### 3. Decompose and plan parallel research

Break the topic into focused sub-questions covering:
- WHERE specific files/components live (use `grep`, `find`, or ripgrep)
- HOW a component works (read files, trace call paths)
- WHAT patterns exist (find representative examples)

Assign a task for each sub-question. Each task must be read-only; frame all queries as "find", "explain", "document", "trace", or "map".

**Launch all tasks concurrently** — 3–5 parallel tasks beats sequential investigation.

### 4. Synthesize findings

Wait until every task reports back. Then:
- Compile results into a coherent narrative grouped by component or concern
- Include `file:line` references throughout
- Trace data flows and call hierarchies
- Surface repeating patterns

### 5. Write the research document

```bash
mkdir -p .agents
```

Derive a slug from the topic (lowercase, hyphenated). Read the template:

```
${CLAUDE_PLUGIN_ROOT}/skills/researching-codebases/assets/research-template.md
```

Fill every section with synthesized findings and write to `.agents/research-<slug>.md`.

### 6. Present findings

```
# Research Complete: [Topic]

Documented in `.agents/research-[slug].md`.

## Key Findings
- [finding 1]
- [finding 2]

## Important File References
- `path/to/file.ext:123` — [what's here]

Do you have follow-up questions about [topic]?
```

### 7. Handle follow-ups

Read the existing document, run additional research as needed, and append:

```markdown
## Follow-up Research [timestamp]

**Question:** [question]

**Findings:** [findings with file:line references]
```

## Quality checklist

- [ ] All research tasks completed
- [ ] Specific `file:line` references throughout the document
- [ ] Official template used
- [ ] Document saved to `.agents/research-<slug>.md`
- [ ] Synthesis connects findings across components
- [ ] No suggestions or critiques (unless explicitly requested)
- [ ] Document is self-contained

## Cross-references

- Plans automatically pick up `.agents/research-<slug>.md` files — use consistent naming.
- For broader topic/prior-art research beyond this codebase, use the `researching-prior-art` skill.

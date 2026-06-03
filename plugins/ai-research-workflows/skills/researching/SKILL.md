---
name: researching
description: >-
  Use when you need to understand how an existing codebase works and/or survey
  external prior work (papers, methods, tools) before planning or changing
  something. Traces function call paths, maps module dependencies, searches
  academic papers and documentation, compares library alternatives. Triggers:
  research the codebase, how does X work, where is X implemented, what tools or
  libraries exist for X, prior art on X, has this been done before, survey
  approaches to X.
---

# Researching

Build the context a task needs by investigating the current codebase and/or
external prior art in one pass, then synthesizing a single research document
that feeds planning. Run the internal dimension, the external dimension, or
both.

## Interaction mode

Leans **Collaborative** by default; see `ai-research-workflows:using-research-workflows` for the full protocol.

## Process

Scope → plan → investigate → present → write → review → hand off.

### 1. Explore context

Read the request. Scan `.agents/` for existing research and plan documents
(`research-*.md`, and legacy `prior-art-*.md`). Note recent commits if relevant.

### 2. Scope the question

Establish: the precise question; whether it needs **internal** codebase research,
**external** prior-art research, or **both**; what counts as relevant; and the
desired depth. In Collaborative mode ask one focused question at a time; in
Direct mode infer scope from the request and state it before proceeding.

### 3. Propose the research plan

Before investigating, present the decomposition: the codebase sub-questions you
will trace and/or the prior-art sources and dimensions you will search. Get a
quick OK (Collaborative) or state it and proceed (Direct).

### 4. Investigate

Run the dimension(s) in scope:

- **Codebase pass** — see `references/codebase-research.md`
- **Prior-art pass** — see `references/prior-art-research.md`

Both passes may surface gaps and light, clearly-labeled observations; defer deep
critique and design decisions to planning or validation.

### 5. Present findings

Present synthesized findings in sections (codebase first, then prior art),
confirming understanding as you go. Use `file:line` anchors for code and
citations for external sources.

### 6. Write the research document

Derive a slug (lowercase, hyphenated). Read the template:
`assets/research-template.md`. Fill the sections that apply and write to
`.agents/research-<slug>.md`. Omit sections for any dimension not investigated.

### 7. Self-review

Check for gaps, uncited prior-art claims, contradictions, unanswered
sub-questions, and scope drift. Fix inline.

### 8. Hand off

Point to the next skill — usually `ai-research-workflows:planning-implementations`
(or `ai-research-workflows:running-experiments` when an approach is uncertain).

## Common Mistakes

- **Researching both dimensions when one suffices** — scope first; don't search external prior art for a question that is purely about current code, or vice-versa.
- **Uncited prior-art claims** — every external factual claim needs a primary-source citation; label secondary sources as such.
- **Vague codebase findings** — every code finding cites a specific `file:line`; "it's somewhere in auth" is not a finding.
- **Skipping the disconfirming search** — for prior art, actively search for limitations, critiques, and failures, not just supporting evidence.
- **Turning research into a rewrite plan** — surface gaps and light observations, but defer detailed design and critique to planning/validation.

## Quality checklist

- [ ] Scope (internal / external / both) was established and stated
- [ ] Codebase findings carry `file:line` references (if the internal pass ran)
- [ ] Every prior-art claim is cited and ≥1 disconfirming search ran (if the external pass ran)
- [ ] Synthesis connects findings and names gaps
- [ ] Template used; saved to `.agents/research-<slug>.md`
- [ ] Document is self-contained
- [ ] Next skill suggested

## Cross-references

- Feeds `ai-research-workflows:planning-implementations`.
- For comparing uncertain approaches with real code, use `ai-research-workflows:running-experiments`.
- Surveyed automatically by `ai-research-workflows:using-research-workflows`.

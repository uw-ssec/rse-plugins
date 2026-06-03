---
name: researching-prior-art
description: >-
  Use when you need to research prior work, papers, methods, or existing tools
  outside the current codebase before designing a solution. Triggers: research
  prior art, what tools exist for X, literature on X, has this been done
  before, survey approaches to X.
---

# Researching Prior Art

Research the space *outside* the current codebase — papers, existing tools, methods, and comparable approaches — and produce a cited synthesis that informs design decisions. Use `ai-research-workflows:researching-codebases` instead when you need to understand the *current* code.

## Interaction mode

This skill leans **Collaborative** by default. For the full Collaborative-vs-Direct protocol and override rules, see the Interaction Modes reference in the `ai-research-workflows:using-research-workflows` skill.

## Process

### Step 1: Scope the question (Collaborative mode)

Before searching, align on:
- The domain and exact question being investigated.
- What counts as relevant (papers, OSS tools, benchmarks, docs, blog posts).
- Desired depth (quick survey vs. exhaustive review).
- How the output will be used (design decision, feasibility check, gap analysis).

In Direct mode, infer scope from context and proceed.

### Step 2: Fan-out search

Search across modalities in parallel:
- Web (general search, news, blog posts).
- Official documentation and project sites.
- Package indexes (PyPI, npm, crates.io, etc.).
- Academic sources (arXiv, Semantic Scholar, ACM DL, Google Scholar).

Cast a wide net first; refine based on initial results.

### Step 3: Deep-read top sources

Identify the 3–6 most relevant results and read them fully. Prefer primary sources (original papers, official docs, project READMEs) over secondary summaries.

### Step 4: Adversarial verification

Actively search for evidence that contradicts or qualifies the main findings. Look for known limitations, published critiques, benchmark failures, and deprecations. Note disconfirming evidence explicitly.

### Step 5: Synthesize

Group findings by theme. For each candidate tool or method: note what it does, where it excels, its limitations, and how it compares to alternatives.

## Deferral

For heavy multi-source, fact-checked research, prefer the `deep-research` skill if it is available; otherwise use your available web-search and fetch tools.

## Output

Write `.agents/prior-art-<slug>.md` (create `.agents/` if needed). The document must contain:

1. **Question / Scope** — the research question and what was considered in-scope.
2. **Methodology** — what was searched, which sources were consulted, and why.
3. **Findings** — grouped by theme, with inline citations (links or references).
4. **Candidate tools / methods** — a table or list with trade-offs for each.
5. **Gaps and open questions** — what is unresolved or absent from the literature.
6. **Sources** — full list of links and citations.
7. **How this informs the work** — explicit connection to the design decision or plan.

This document feeds the `ai-research-workflows:planning-implementations` skill; use a slug consistent with the planned `.agents/plan-<slug>.md`.

## Quality checklist

- [ ] Every factual claim cites a source.
- [ ] Primary sources used where available; secondary sources labeled as such.
- [ ] At least one disconfirming search was attempted and the result noted.
- [ ] Document is self-contained — a reader with no prior context can follow it.
- [ ] Sources section contains working links or full citations.

## Common Mistakes

- **Uncited claims** — stating "Tool X is widely used" or "Method Y outperforms Z" without a linked source makes the synthesis untrustworthy. Every factual claim must cite a primary source.
- **Skipping primary sources** — relying on blog posts or secondary summaries instead of the original paper, official docs, or project README risks propagating errors. Label secondary sources as such.
- **No disconfirming search** — only searching for evidence that supports the preferred approach produces a biased synthesis. Always run at least one search for known limitations, critiques, or failures.
- **Confusing this skill with researching-codebases** — this skill covers external tools, methods, and literature; for understanding the current codebase use `ai-research-workflows:researching-codebases` instead.
- **Scope drift** — starting with a narrow question and gradually expanding it until the document is unfocused. Lock scope in Step 1 and document any intentional scope changes.

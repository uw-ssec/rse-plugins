# Prior-Art Research Pass

How to research the space *outside* the current codebase — papers, tools,
methods, comparable approaches — for the `researching` skill. Produces the
**Prior Art** section of `.agents/research-<slug>.md`.

## Steps

### 1. Scope (Collaborative)

Align on: the domain and exact question; what counts as relevant (papers, OSS
tools, benchmarks, docs, blog posts); desired depth; how the output will be used.
In Direct mode, infer scope from context and proceed.

### 2. Fan-out search

Search across modalities in parallel:

- Web (general search, news, blog posts).
- Official documentation and project sites.
- Package indexes (PyPI, npm, crates.io, etc.).
- Academic sources (arXiv, Semantic Scholar, ACM DL, Google Scholar).

Cast a wide net first; refine based on initial results.

### 3. Deep-read top sources

Identify the 3–6 most relevant results and read them fully. Prefer primary
sources (original papers, official docs, project READMEs) over secondary
summaries.

### 4. Adversarial verification

Actively search for evidence that contradicts or qualifies the main findings:
known limitations, published critiques, benchmark failures, deprecations. Note
disconfirming evidence explicitly.

### 5. Synthesize

Group findings by theme. For each candidate tool or method, note what it does,
where it excels, its limitations, and how it compares to alternatives. Keep
inline citations for every factual claim.

## Deferral

For heavy multi-source, fact-checked research, prefer the `deep-research` skill
if it is available; otherwise use your available web-search and fetch tools.

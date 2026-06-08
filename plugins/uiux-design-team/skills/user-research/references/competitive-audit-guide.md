# Competitive Audit Guide

A structured reference for planning, running, and reporting competitive audits in UX research. Covers criteria selection, scoring rubric, the full example table, gap analysis, inter-rater process, and reporting formats.

## Table of Contents

| Section | Description |
|---------|-------------|
| [When to Run a Competitive Audit](#when-to-run-a-competitive-audit) | Triggers and scope decisions |
| [Criteria Selection](#criteria-selection) | How to choose what to evaluate |
| [Scoring Rubric](#scoring-rubric) | 1-5 scale definitions |
| [Full Example Audit Table](#full-example-audit-table) | 12-criterion worked example |
| [Gap Analysis](#gap-analysis) | Finding your wedge from the data |
| [Inter-Rater Process](#inter-rater-process) | Two-reviewer reconciliation workflow |
| [Reporting Format](#reporting-format) | How to present findings to stakeholders |
| [See Also](#see-also) | Related references |

## When to Run a Competitive Audit

Run a competitive audit when:
- Entering a new market or category for the first time
- Planning a redesign and need external benchmarks
- A competitor has shipped a major update
- Leadership asks "how do we compare to X?"
- You need evidence to prioritize a capability gap

**Scope rule:** 3–5 direct competitors maximum per audit. More than 5 diffuses focus. Use a landscape map to decide who counts as direct vs. adjacent.

## Criteria Selection

Choose 8–12 criteria that map to user goals and your strategic questions. Avoid evaluating things that don't affect users.

**Categories to draw from:**

| Category | Example Criteria |
|----------|-----------------|
| First-time experience | Onboarding clarity, time-to-first-value |
| Core task flow | Task completion rate (heuristic), IA findability |
| Visual quality | Design polish, brand consistency |
| Technical | Performance (LCP, CLS), mobile responsiveness |
| Accessibility | axe violations, keyboard navigation, contrast |
| Trust | Pricing transparency, security indicators |
| Support | Docs quality, support channel availability |
| Ecosystem | Integration count, community health |

## Scoring Rubric

Use a consistent 1–5 scale. Define what each score means before starting.

| Score | Label | Definition |
|-------|-------|-----------|
| 1 | Poor | Fails to meet basic user expectations; multiple serious issues |
| 2 | Below average | Present but with significant usability or quality problems |
| 3 | Average | Meets the minimum bar; nothing distinctive |
| 4 | Good | Above average; notable strengths with minor gaps |
| 5 | Excellent | Best-in-class; sets the bar others should follow |

For objective metrics (e.g. LCP in seconds), convert to scores after collection using agreed thresholds (e.g. LCP < 2.5s = 5, 2.5–4s = 3, > 4s = 1).

## Full Example Audit Table

| Criterion | Acme | Globex | Initech | Notes |
|-----------|:----:|:------:|:-------:|-------|
| Onboarding clarity | 4 | 2 | 3 | Acme uses progressive disclosure; Globex shows 12 fields on step 1 |
| Feature parity (core) | 5 | 4 | 3 | All cover must-haves; Initech missing bulk actions |
| Pricing transparency | 2 | 5 | 4 | Acme hides Enterprise tier; others show full table |
| IA / findability | 3 | 4 | 2 | Initech buries reports 4 levels deep |
| Visual design polish | 5 | 3 | 2 | Globex uses stock imagery; Initech outdated UI |
| Accessibility (axe pass) | 1 | 3 | 4 | Acme has 12 violations on hero; Initech best |
| Mobile experience | 4 | 2 | 3 | Globex non-responsive at <768px |
| Performance (LCP) | 1.8s→5 | 4.2s→1 | 2.9s→3 | Acme leads; Globex unacceptable |
| Content / docs | 5 | 3 | 2 | Acme has best DX writing; Initech docs outdated |
| Support channels | 3 | 5 | 2 | Globex offers 24/7 chat; Initech email only |
| Integrations | 5 | 2 | 3 | Acme has 80+; Globex has 12 |
| Community | 4 | 1 | 2 | Acme runs active forum; others dormant |

**Reading the table:**
- Columns are competitors; rows are evaluation criteria.
- Score each criterion independently before looking at others to prevent anchoring.
- Add the Notes column — raw scores without context mislead.

## Gap Analysis

After scoring, run the gap analysis to find strategic opportunities:

**Wedge criteria:** Any criterion where ALL competitors score ≤ 2. This is unmet table stakes — entering with a strong answer here is a differentiator.

**Parity criteria:** Any criterion where all competitors score ≥ 4. These are must-have; falling below them is a liability.

**Your relative gaps:** Criteria where your product scores 2+ points below the category leader. Prioritize closing these before chasing wedge opportunities.

```
Gap analysis summary template:
- Wedge opportunities: [list criteria where all competitors ≤ 2]
- Must-have parity (all ≥ 4): [list criteria]
- Your relative gaps vs. [strongest competitor]: [list criteria]
- Recommended focus areas: [top 3, ranked by user impact]
```

## Inter-Rater Process

Two reviewers score independently to prevent bias. Follow this process:

1. Both reviewers evaluate the same criteria independently, with no discussion.
2. Compare scores. For each criterion, calculate the difference.
3. For any criterion where scores diverge by **> 1 point**: hold a 10-minute reconciliation — each reviewer explains their rationale; arrive at a consensus score.
4. Track agreement rate: target **≥ 80% of criteria within 1 point** before the first pass.
5. If agreement is below 80%, revisit the scoring rubric — definitions are ambiguous.

**Why inter-rater matters:** Individual evaluators have blind spots. Two independent scorers surface criteria where the judgment call is genuinely difficult, preventing the audit from reflecting one person's opinion.

## Reporting Format

Structure the audit report in three parts:

**1. Executive summary (1 page)**
- Scope: which competitors, which criteria, date
- Method: how criteria were chosen, who evaluated
- Top 3 findings with strategic implication

**2. Scored table**
- Full matrix with all criteria and scores
- Color-coded heat map (1=red, 3=yellow, 5=green)
- Notes column explaining non-obvious scores

**3. Recommendations**
- Wedge opportunities ranked by user impact
- Parity gaps to close immediately
- Criteria to monitor over time (re-audit every 6 months or after major competitor release)

## See Also

- [[interview-guide.md]] — Interview techniques for qualitative competitive context (user interviews about competitor products)
- [[synthesis-methods.md]] — Affinity mapping and insight synthesis applied to audit findings
- [[../../usability-evaluation/SKILL.md]] — Heuristic evaluation that can be applied alongside competitive audit

**Back to:** [User Research Skill](../SKILL.md)

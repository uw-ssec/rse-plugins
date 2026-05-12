---
name: user-research
description: Use when planning or running user interviews, building personas or JTBD job stories, designing a competitive audit, synthesizing research data, or framing insights and How-Might-We questions for ideation.
metadata:
   references:
   - references/interview-guide.md
   - references/jtbd-framework.md
   - references/persona-templates.md
   - references/synthesis-methods.md
---

# User Research

## Method picker

| Question | Method | Time | Output |
|----------|--------|------|--------|
| Why do users do X? | Interviews (5-8) | 1-2 wk | Transcripts, themes |
| How does work actually happen? | Contextual inquiry | 1-3 wk | Field notes, workflows |
| How many feel X? | Survey | 1-2 wk | Stats, distributions |
| How do users group content? | Card sort | 3-5 d | Clusters, dendrograms |
| Does the design work? | Usability test (5-8) | 1-2 wk | Task success, issues |
| Behavior over time? | Diary study | 2-4 wk | Longitudinal data |
| Which variant wins? | A/B test | 1-4 wk | Significance data |
| What patterns at scale? | Analytics review | 1-3 d | Funnels, drop-offs |

Pair one qualitative (why) with one quantitative (how many) per question.

## Quick start: persona

Spend ≥ 5-8 interviews before drafting a primary persona.

1. Gather raw data (transcripts, surveys, support tickets, analytics).
2. Cluster by behavior, goals, frustrations (not demographics).
3. Draft using template below.
4. Validate with teammates who joined interviews — "does this feel like someone we talked to?"
5. Socialize: pin to Figma/Confluence; reference in every review.

### Template

```
Name:         [First name + last initial]
Role:         [Job title or life role]
Demographics: [Age range, location, tech comfort]
Goals:        [2-3 primary]
Frustrations: [2-3 recurring]
Behaviors:    [Habits, tools, workflows]
JTBD:         [Job story]
Quote:        [Verbatim from research]
```

### Example output

```
Name:         Maria T.
Role:         PM, mid-stage B2B SaaS
Demographics: 32-38, urban, high tech fluency
Goals:        Ship faster without sacrificing quality; align eng+design;
              prove ROI to leadership
Frustrations: Disconnected tools; mid-sprint requirement churn;
              feedback synthesis at scale
Behaviors:    Lives in Slack/Linear; weekly user calls; async-first
JTBD:         When planning next quarter's roadmap, I want to quantify
              which user problems matter most, so I can defend
              prioritization to the executive team.
Quote:        "Gut feelings don't survive a board meeting."
```

More templates: [persona-templates.md](references/persona-templates.md).

## JTBD job story (one-line format)

> "When [situation], I want to [motivation], so I can [outcome]."

Write functional + emotional + social variants per job. Detail and switch-interview method: [jtbd-framework.md](references/jtbd-framework.md).

### Example HMW set (from insight "new users abandon dashboard in <15s")

- HMW make the first-login dashboard feel manageable in 5 seconds?
- HMW progressively reveal advanced features instead of showing all at once?
- HMW use empty states to teach the product instead of showing zeros?
- HMW celebrate the first completed action to anchor return visits?
- HMW personalize the dashboard based on signup-time intent?

## Competitive audit (output table)

For each competitor, score 1-5 across criteria:

| Criterion | Acme | Globex | Initech | Notes |
|-----------|:----:|:------:|:-------:|-------|
| Onboarding clarity | 4 | 2 | 3 | Acme uses progressive disclosure |
| Feature parity (core) | 5 | 4 | 3 | All cover the must-haves |
| Pricing transparency | 2 | 5 | 4 | Acme hides Enterprise tier |
| IA / findability | 3 | 4 | 2 | Initech buries reports 4 levels deep |
| Visual design polish | 5 | 3 | 2 | Globex uses stock imagery |
| Accessibility (axe pass) | 1 | 3 | 4 | Acme has 12 violations on hero |
| Mobile experience | 4 | 2 | 3 | Globex non-responsive at <768px |
| Performance (LCP) | 1.8s | 4.2s | 2.9s | Acme leads |
| Content/docs | 5 | 3 | 2 | Acme has best DX writing |
| Support channels | 3 | 5 | 2 | Globex offers 24/7 chat |
| Integrations | 5 | 2 | 3 | Acme has 80+ |
| Community | 4 | 1 | 2 | Acme runs active forum |

Gap = criteria where ALL competitors score ≤ 2 → that's your wedge. Process detail: [interview-guide.md](references/interview-guide.md).

### Inter-rater check
Two reviewers score independently. For any criterion where scores diverge by > 1 point, reconcile before publishing. Target: ≥ 80% within-1 agreement.

## Synthesis workflow

1. **Affinity map** — one observation per note; cluster; label theme.
   - **Validation:** every cluster has ≥ 3 supporting observations from ≥ 2 different participants. Singletons go to a "parking lot," not a cluster.
2. **Empathy map** per persona — Says / Thinks / Does / Feels.
3. **Insight statements** (template):
   > "We observed [X]. We were surprised that [Y]. Because of this, we might [Z]."
4. **HMW questions** — 3-5 per insight to seed ideation.

### Example insight set (3-5)

```
1. We observed users abandon the settings page in <15s. We were surprised
   that 8/10 could not find notification preferences. Because of this,
   we might surface notification controls in the context where
   notifications appear.

2. We observed users open Slack alongside our app in 7/10 sessions.
   We were surprised that they use Slack to copy data out manually.
   Because of this, we might add a native Slack export or integration.

3. We observed mobile users tap the export button accidentally on the
   list screen. We were surprised that it had a 22% misfire rate. Because
   of this, we might move primary actions out of the list scroll area.

4. We observed every interviewed admin keep a personal cheat-sheet doc.
   We were surprised these docs all contained the same 6 commands.
   Because of this, we might ship a built-in "common tasks" panel.

5. We observed first-month churners share a single behavior: zero
   teammates invited. We were surprised that 0 of 12 saw the invite CTA.
   Because of this, we might move team invite into onboarding day 1.
```

Methods + repository structure: [synthesis-methods.md](references/synthesis-methods.md).

## Rules

- Never assume — validate every hypothesis with evidence.
- Real users only — no friends/family/coworkers as participants.
- Triangulate — same finding across ≥ 2 methods = high confidence.
- Quote users directly when reporting.

## Next Steps

- **[User Journey Mapping](../user-journey-mapping/SKILL.md)** — map end-to-end experience per persona
- **[Usability Evaluation](../usability-evaluation/SKILL.md)** — evaluate designs against heuristics

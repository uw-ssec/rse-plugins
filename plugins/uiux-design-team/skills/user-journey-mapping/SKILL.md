---
name: user-journey-mapping
description: Use when visualizing a user's end-to-end experience for a specific scenario, identifying pain points and emotion lows, aligning teams on user flow, planning improvements to onboarding/checkout/support, or producing a service blueprint.
metadata:
   references:
   - references/blueprint-guide.md
   - references/journey-template.md
   - references/touchpoint-patterns.md
---

# User Journey Mapping

## Map Type Selection

| Type | Use When |
|------|----------|
| **Journey Map** | Optimizing one persona through one specific scenario |
| **Experience Map** | Entering a new market; understanding category-level behavior outside your product |
| **Service Blueprint** | Coordinating across teams; surfacing backstage/support processes affecting UX |

## Workflow

**Step 1 — Define scope.** One persona, one scenario (e.g., "New user signs up and completes first project"). Narrow scope produces actionable maps; broad scope produces wallpaper.

**Step 2 — Identify 5–7 sequential stages.** Each stage = a distinct phase with its own goal.
Example: Awareness → Sign-Up → First Use → Configuration → First Value → Routine Use → Expansion.

**Step 3 — Fill the stage matrix.** For each stage document: Actions, Thoughts, Emotions (1–5), Touchpoints, Pain Points, Opportunities (template below).

**Step 4 — Validation checkpoint.** Before continuing, verify the map against real data:
- Compare every Action/Thought row against ≥5 user interview transcripts or analytics events.
- Flag any row backed only by team assumption — mark "ASSUMPTION" and schedule research.
- Pass criteria: ≥80% of rows have direct evidence (quote, log event, survey response). If <80%, pause and run targeted research before Step 5.

**Step 5 — Plot the emotion curve.** Graph 1–5 scores across stages. Identify valleys (likely churn points) and peaks (delight moments).

**Step 6 — Prioritize using severity × frequency.** Apply the P0–P3 matrix below. Share with product/engineering to align on what ships first.

## Stage Matrix Template

| Stage          | Awareness        | Sign-Up           | First Use         | Configuration     | First Value       |
|----------------|------------------|-------------------|-------------------|-------------------|-------------------|
| **Actions**    | Reads blog, clicks CTA | Enters email | Opens dashboard | Sets preferences | Completes first task |
| **Thoughts**   | "Does this solve my problem?" | "Worth my time?" | "Where do I start?" | "More setup than expected" | "Oh, this works" |
| **Emotions**   | Curious (3/5) | Hopeful (4/5) | Confused (2/5) | Frustrated (2/5) | Satisfied (4/5) |
| **Touchpoints** | Blog, landing page | Sign-up form, email | Dashboard, tooltip | Settings, invite flow | Core feature |
| **Pain Points** | Value prop unclear | Too many fields | No guidance | Wrong defaults | — |
| **Opportunities** | Clearer headline | Social sign-in | Guided walkthrough | Smart defaults | Celebrate moment |
| **Evidence**   | Interview #2, #4 | Funnel drop 38% | Session replay | Survey Q7 | Activation event |

## Emotion Curve Format

```
  5 |         *                              *
  4 |    *         *                    *
  3 |                   *
  2 |                        *    *
  1 |
    +------------------------------------------
      Aware  Sign-Up  First  Config  Value  Routine
```

Measure emotion: ask interviewees to rate 1–5 at each stage. Also watch verbal cues (sighs, laughter, hesitation). Aggregate across 5+ users.

## Moments of Truth

Flag and design explicitly for:
- **First impression** — Does the product communicate value within 5 seconds?
- **First friction** — How does it handle the user's first mistake?
- **First value** — When does the user achieve what they came for?
- **Recovery** — When something fails, what happens next?

## Pain Point Prioritization

| Priority | Severity | Frequency | Action |
|----------|----------|-----------|--------|
| P0 | High | High | Fix now — users churning |
| P1 | High | Low | Fix soon — catastrophic when hit |
| P2 | Low | High | Improve — constant minor annoyance (quick wins) |
| P3 | Low | Low | Backlog |

## Deliverable Checklist

Before sharing the map:
- [ ] Persona named and linked to a persona doc
- [ ] Scenario stated in one sentence
- [ ] 5–7 stages, each with all six rows filled
- [ ] Evidence column populated for ≥80% of cells
- [ ] Emotion curve drawn
- [ ] Top 3 P0/P1 opportunities highlighted with owner and ETA proposed
- [ ] Reviewed with 1 user-research lead and 1 PM/engineer

## Deep Dive References

- [Journey Template](references/journey-template.md) — Full canvas, components, formats, presentation tips
- [Blueprint Guide](references/blueprint-guide.md) — Frontstage/backstage/support layers, digital adaptations
- [Touchpoint Patterns](references/touchpoint-patterns.md) — Inventory method, owned/earned/paid, matrix, moment-of-truth identification

## Next Steps

- **user-research** — If the validation checkpoint flagged assumption-heavy stages, run targeted research to fill the gaps.
- **information-architecture** — Use the journey to inform navigation that matches the user's mental model.

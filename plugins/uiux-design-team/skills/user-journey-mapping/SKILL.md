---
name: user-journey-mapping
description: Create user journey maps, experience maps, service blueprints, and touchpoint analysis to visualize the complete user experience with stages, actions, emotions, pain points, and opportunities.
metadata:
   references:
   - references/blueprint-guide.md
   - references/journey-template.md
   - references/touchpoint-patterns.md
---

# User Journey Mapping

Journey maps make the invisible visible. They transform abstract user experiences into concrete, shareable artifacts that align teams around a common understanding of what users go through. A good journey map does not just describe steps; it captures the emotional arc, surfaces hidden pain points, and reveals opportunities that no single team member could see on their own.

## Quick Start: Create a Journey Map

Follow this process to build a journey map for any user scenario.

**Step 1 -- Define scope.** Select one persona and one specific scenario (e.g., "New user signs up and completes first project"). A focused scope produces actionable maps; a broad scope produces wallpaper.

**Step 2 -- Identify stages.** Break the scenario into 5-7 sequential stages. Each stage represents a distinct phase of the experience with its own goal. Example stages for a SaaS onboarding: Awareness, Sign-Up, First Use, Configuration, First Value, Routine Use, Expansion.

**Step 3 -- Map each stage.** For every stage, document the following:

| Stage         | Awareness       | Sign-Up          | First Use        | Configuration    | First Value      |
|---------------|-----------------|------------------|------------------|------------------|------------------|
| **Actions**   | Reads blog post, clicks CTA | Enters email, creates password | Opens dashboard, looks around | Sets preferences, adds team | Completes first task |
| **Thoughts**  | "Does this solve my problem?" | "Is this worth my time?" | "Where do I start?" | "This is more setup than I expected" | "Oh, this actually works" |
| **Emotions**  | Curious (3/5)   | Hopeful (4/5)    | Confused (2/5)   | Frustrated (2/5) | Satisfied (4/5)  |
| **Touchpoints** | Blog, landing page | Sign-up form, email confirmation | Dashboard, onboarding tooltip | Settings, invite flow | Core feature, success screen |
| **Pain Points** | Value prop unclear | Too many form fields | No guidance | Defaults are wrong | None identified  |
| **Opportunities** | Clearer headline | Social sign-in | Guided walkthrough | Smart defaults | Celebrate the moment |

**Step 4 -- Draw the emotion curve.** Plot emotional highs and lows across stages to identify the overall arc:

```
  5 |         *                              *
  4 |    *         *                    *
  3 |                   *
  2 |                        *    *
  1 |
    +------------------------------------------
      Aware  Sign-Up  First  Config  Value  Routine
```

**Step 5 -- Prioritize opportunities.** Focus on the deepest emotional valleys. These are the moments where users are most likely to churn or develop negative perceptions.

## Map Types

Different visualization types serve different purposes. Choose the right one for your context.

**Journey Map** -- Follows a single persona through a single scenario from beginning to end. Best for understanding a specific user flow in detail. Use when you need to optimize a particular experience.

**Experience Map** -- Broader than a journey map. Captures the full context of how a user interacts with a category of product or service, not just yours. Includes activities that happen before and after they touch your product. Use when entering a new market or redefining product boundaries.

**Service Blueprint** -- Extends the journey map by adding behind-the-scenes layers:
- **Frontstage interactions** -- What the user sees and interacts with
- **Backstage interactions** -- Internal processes the user cannot see (APIs, manual reviews, queue processing)
- **Support processes** -- Systems, databases, and third-party services that enable the experience

Use service blueprints when you need to coordinate across teams or identify operational bottlenecks that affect user experience.

## Emotion Curves

Emotion curves are the most powerful element of a journey map. They reveal where the experience breaks down and where it delights.

**How to measure emotions:**

- During user interviews, ask participants to rate their feeling at each stage on a 1-5 scale (1 = very frustrated, 5 = very satisfied)
- Look for verbal cues: sighs, laughter, hesitation, excitement
- Aggregate across 5+ users to find patterns

**Moments of truth** are the critical points in the emotion curve where the experience can go very right or very wrong:
- **First impression** -- Does the product immediately communicate value?
- **First friction** -- How does the product handle the user's first mistake or confusion?
- **First value** -- When does the user first achieve what they came to do?
- **Recovery** -- When something goes wrong, how does the product respond?

Identify moments of truth and design for them explicitly. A journey with a strong recovery moment can produce higher satisfaction than a journey where nothing went wrong.

## Pain Point Prioritization

Not all pain points deserve equal attention. Use a severity-frequency matrix to prioritize:

| Priority | Severity | Frequency | Action                          |
|----------|----------|-----------|----------------------------------|
| P0       | High     | High      | Fix immediately; users are leaving |
| P1       | High     | Low       | Fix soon; catastrophic when hit    |
| P2       | Low      | High      | Improve; constant minor annoyance  |
| P3       | Low      | Low       | Backlog; address when convenient   |

**Quick wins** are P2 items that can be resolved with minimal effort. They improve the day-to-day experience and build team momentum.

**Strategic improvements** are P0 and P1 items that require significant investment. They prevent churn and drive retention.

Map every identified pain point onto this matrix and share it with product and engineering stakeholders to drive alignment on priorities.

## Deep Dive References

### [Journey Template](references/journey-template.md)

- Overview
- Template Components
- Emotional Curve Mapping
- Journey Map Formats
- Journey Map Creation Process
- Stakeholder Presentation Tips
- Journey Map Canvas
- Persona: _______________________________________________
- *...and 8 more sections*

### [Blueprint Guide](references/blueprint-guide.md)

- Overview
- Difference from Journey Maps
- Blueprint Components
- Visual Structure
- Creation Process
- Cross-Functional Alignment
- Digital Service Blueprint Adaptations
- Service Blueprint Template
- *...and 8 more sections*

### [Touchpoint Patterns](references/touchpoint-patterns.md)

- Overview
- Touchpoint Inventory Methodology
- Digital vs Physical Touchpoints
- Owned vs Earned vs Paid Touchpoints
- Touchpoint Matrix
- Channel Consistency Analysis
- Moment-of-Truth Identification
- Touchpoint Optimization Prioritization
- *...and 2 more sections*

## Next Steps

After completing your journey map, continue with these related skills:

- **user-research** -- If your journey map reveals stages where you lack data, go back and conduct targeted research to fill those gaps.
- **information-architecture** -- Use journey maps to inform the structure and navigation of your product, ensuring it matches the user's mental model of the process.

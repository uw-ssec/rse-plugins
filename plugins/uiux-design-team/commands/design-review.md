---
name: design-review
description: Run a multi-specialist design review with severity-rated findings from accessibility, visual, interaction, and content experts orchestrated by the UX design lead.
user-invocable: true
allowed-tools: []
---

# Multi-Specialist Design Review

Run a comprehensive design review by routing your artifact through multiple specialist reviewers, orchestrated by @ux-design-lead. Each specialist evaluates the design from their domain expertise, and findings are synthesized into a prioritized action plan.

## When to Use This Command

- Before developer handoff to catch issues early
- During design critiques and team reviews
- When evaluating a redesign or new feature
- As a quality gate before user testing
- When you want a thorough, multi-perspective assessment

## Workflow

### Step 1: Gather the Design Artifact

Provide the design to be reviewed. This can be:

- A URL to a live page or staging environment
- A screenshot or mockup image
- HTML/CSS code for a component or page
- A Figma export or design specification
- A wireframe or prototype description

**Prompt the user:**
> What design artifact should I review? Provide a URL, screenshot, code, or detailed description of the interface.

Establish the review context:
- What is the purpose of this interface?
- Who is the target audience?
- What stage is this design in (wireframe, mockup, production)?
- Are there specific concerns to focus on?

### Step 2: Route to @ux-design-lead for Orchestration

@ux-design-lead coordinates the review by assigning the artifact to each specialist. The lead determines which specialists are most relevant based on the artifact type and context.

The lead assigns reviews to:

1. **@accessibility-specialist** - WCAG compliance, keyboard navigation, screen reader support, color contrast, ARIA patterns
2. **@visual-designer** - Visual hierarchy, typography, color usage, spacing, alignment, brand consistency
3. **@interaction-designer** - User flows, interaction patterns, feedback mechanisms, error handling, state management
4. **@ux-writer** - Content clarity, microcopy quality, error messages, labels, tone consistency, reading level

### Step 3: Accessibility Review

@accessibility-specialist evaluates using the `accessibility-audit` skill:

- **Perceivable**: Color contrast ratios (AA minimum 4.5:1 for text), text alternatives, content structure
- **Operable**: Keyboard navigation, focus management, target sizes (minimum 44x44px), timing
- **Understandable**: Labels, instructions, error identification, consistent navigation
- **Robust**: Semantic HTML, ARIA usage, assistive technology compatibility

Document each finding with:
- The specific element or pattern
- The WCAG criterion violated
- The impact on users with disabilities
- A recommended fix

### Step 4: Visual Design Review

@visual-designer evaluates using the `visual-design` and `color-systems` skills:

- **Hierarchy**: Is the visual hierarchy clear? Can users scan and find key information?
- **Typography**: Is the type scale consistent? Are font sizes readable? Is line height comfortable (1.4-1.6 for body)?
- **Color**: Is the palette cohesive? Are colors used consistently for meaning? Does it work in light and dark contexts?
- **Spacing**: Is the spacing system consistent? Are elements properly grouped using proximity?
- **Alignment**: Are elements aligned to a grid? Are there unintentional misalignments?
- **Brand**: Does the design align with brand guidelines and design system tokens?

### Step 5: Interaction Design Review

@interaction-designer evaluates using the `usability-evaluation` skill:

- **User Flow**: Is the task flow logical and efficient? Are there unnecessary steps?
- **Feedback**: Does the interface respond to user actions? Are loading states, success states, and error states covered?
- **Affordances**: Are interactive elements clearly clickable/tappable? Do they look interactive?
- **Error Handling**: Are errors prevented where possible? Are error messages helpful and actionable?
- **States**: Are all component states accounted for (default, hover, focus, active, disabled, loading, error, empty)?
- **Edge Cases**: What happens with long text, empty data, slow connections, or unexpected input?

### Step 6: Content and UX Writing Review

@ux-writer evaluates using the `ux-writing` skill:

- **Clarity**: Is the language clear and unambiguous? Can users understand without re-reading?
- **Conciseness**: Is microcopy as short as possible while remaining clear?
- **Actionability**: Do CTAs clearly describe what will happen? Are button labels action-oriented?
- **Tone**: Is the tone consistent and appropriate for the context (error vs. success vs. neutral)?
- **Inclusivity**: Is language gender-neutral, culturally sensitive, and free of jargon?
- **Error Messages**: Do they explain what went wrong, why, and how to fix it?

### Step 7: Synthesize Findings

@ux-design-lead collects all findings and categorizes them by severity:

#### Severity Levels

| Level | Label | Definition | Action |
|-------|-------|------------|--------|
| 1 | **Critical** | Blocks users from completing tasks, causes accessibility barriers, or creates legal risk | Must fix before launch |
| 2 | **Major** | Significantly degrades experience, confuses users, or violates established patterns | Fix in current sprint |
| 3 | **Minor** | Noticeable but does not prevent task completion; polish issues | Fix in next sprint |
| 4 | **Enhancement** | Opportunities to improve beyond current requirements; nice-to-haves | Add to backlog |

#### Report Structure

For each finding, document:

```
### [Severity] Finding Title
- **Specialist**: Which reviewer identified this
- **Category**: Accessibility / Visual / Interaction / Content
- **Location**: Where in the design this applies
- **Issue**: Clear description of the problem
- **Impact**: How this affects users
- **Recommendation**: Specific fix with example if possible
```

### Step 8: Prioritize and Recommend Next Steps

@ux-design-lead creates an action plan:

1. **Immediate fixes** (Critical items) - List specific changes with owners
2. **Sprint work** (Major items) - Group related fixes into logical work items
3. **Backlog items** (Minor + Enhancements) - Prioritized list for future sprints
4. **Positive findings** - Highlight what the design does well to reinforce good patterns

Provide a summary score:
- Total findings by severity
- Top 3 issues to address first
- Overall design quality assessment
- Recommendation: Ready for handoff / Needs revision / Needs significant rework

## Related Skills

- `accessibility-audit` - Detailed WCAG 2.2 compliance checking
- `visual-design` - Visual design principles and evaluation
- `usability-evaluation` - Nielsen's heuristics and usability assessment
- `ux-writing` - Microcopy and content design guidance
- `color-systems` - Color palette evaluation and contrast checking

## Related Commands

- `/audit-accessibility` - Deep-dive accessibility audit
- `/evaluate-usability` - Full heuristic evaluation
- `/design-handoff` - Prepare reviewed design for development

## Cross-Plugin Bridge (PROACTIVE)

When the design review is complete:

- PROACTIVELY route critical and major findings to the **frontend-engineering-team** plugin's **@frontend-lead** for implementation prioritization and engineering effort estimation.
- If the review identifies component architecture concerns, PROACTIVELY route to **@react-specialist** for component restructuring guidance.
- If the review identifies performance-related design issues, PROACTIVELY route to **@performance-engineer** for performance impact assessment and optimization planning.
- If the design is ready for handoff (recommendation: "Ready for handoff"), PROACTIVELY initiate the `/design-handoff` process AND route to **@frontend-lead** for parallel engineering implementation planning.

Design review findings should directly feed into engineering action, not sit in a report.

## Tips

- Provide as much context as possible about the target audience and use case
- If the design is in early stages (wireframe), mention that so reviewers calibrate expectations
- Request focus on specific areas if you have known concerns
- Run this review before `/design-handoff` to catch issues before development begins

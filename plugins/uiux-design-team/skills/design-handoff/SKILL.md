---
name: design-handoff
description: Create developer handoff documentation with visual specifications, interaction state annotations, responsive behavior notes, accessibility requirements, animation timing, and design QA checklists for smooth design-to-development transitions.
metadata:
   references:
   - references/annotation-guide.md
   - references/handoff-checklist.md
   - references/qa-process.md
---

# Design Handoff

Handoff is where design quality lives or dies. A pixel-perfect mockup means nothing if the developer implementing it has to guess at spacing values, invent hover states, or ignore accessibility requirements because they were never documented. The gap between design intent and production output is not a development problem -- it is a handoff problem.

Effective handoff documentation transforms a static design into a complete behavioral specification. It answers every question a developer will ask before they ask it: What happens on hover? What does the loading state look like? How does this behave at 320px? What ARIA role does this need? How long is the fade-in animation?

This skill provides the systematic approach to producing handoff documentation that eliminates ambiguity, reduces implementation rounds, and preserves design fidelity through the development process.

## Quick Start: Handoff Checklist

Before handing off any design, verify every item on this checklist. Incomplete handoffs create implementation debt that compounds across every subsequent sprint.

1. **Visual Specifications** -- Every spacing value, color, and typographic property documented using design token names (not raw hex codes or pixel values). Developers should never need to use an eyedropper tool.

2. **Interaction States** -- Every interactive element annotated with all relevant states:
   - Default / Resting
   - Hover
   - Active / Pressed
   - Focus (keyboard navigation)
   - Disabled
   - Loading / Processing
   - Error / Invalid
   - Empty / No Data

3. **Responsive Behavior** -- Breakpoint-by-breakpoint documentation of layout changes. What reflows? What stacks? What hides? What changes size? Document the behavior, not just the endpoints.

4. **Accessibility Notes** -- ARIA roles, labels, and relationships. Keyboard navigation order and behavior. Screen reader announcement expectations. Color contrast verification for all text and interactive elements.

5. **Animation Specifications** -- Duration, easing function, trigger event, and affected properties for every transition and animation. Include delay values for staggered sequences.

6. **Edge Cases** -- Long text truncation behavior, missing data fallbacks, error state recovery paths, maximum and minimum content scenarios, localization expansion room.

7. **Assets** -- All icons, illustrations, and images exported at required resolutions, named according to the project's asset naming convention, and optimized for their target format (SVG for icons, WebP/AVIF for photos).

## Specification Format

The specification format determines whether developers can find and use the information you provide. Consistency and predictability matter more than comprehensiveness.

### Use Token Names, Not Raw Values

Instead of: "padding: 16px, color: #3b82f6, font-size: 14px"

Write: "padding: `--spacing-4`, color: `--color-primary`, font-size: `--font-size-sm`"

Token names connect the implementation to the design system. Raw values disconnect it. When the design system evolves, token-referenced implementations update automatically. Hard-coded implementations require manual archaeology.

### Annotate with Measurements

Every annotation should follow this format:

```
[Element Name]
├── Width: [token or value] | Height: [token or value]
├── Padding: [top] [right] [bottom] [left] (use token names)
├── Margin: [top] [right] [bottom] [left] (use token names)
├── Background: [token name]
├── Border: [width] [style] [token name]
├── Border Radius: [token name]
├── Typography: [font-family token] / [size token] / [weight token] / [line-height token]
└── Color: [token name]
```

### Component State Matrix

For every interactive component, produce a state matrix that maps every state to its visual properties:

| State | Background | Text Color | Border | Shadow | Cursor | Opacity |
|-------|-----------|------------|--------|--------|--------|---------|
| Default | `--color-surface` | `--color-on-surface` | `--border-default` | `--shadow-sm` | pointer | 1 |
| Hover | `--color-surface-hover` | `--color-on-surface` | `--border-hover` | `--shadow-md` | pointer | 1 |
| Active | `--color-surface-active` | `--color-on-surface` | `--border-active` | none | pointer | 1 |
| Focus | `--color-surface` | `--color-on-surface` | `--border-focus` | `--shadow-focus` | pointer | 1 |
| Disabled | `--color-surface-disabled` | `--color-on-surface-disabled` | `--border-disabled` | none | not-allowed | 0.6 |
| Loading | `--color-surface` | `--color-on-surface-muted` | `--border-default` | `--shadow-sm` | wait | 0.8 |
| Error | `--color-error-surface` | `--color-error` | `--border-error` | none | pointer | 1 |

## Design QA Process

Design QA happens after implementation, not after design. It is the verification step that ensures the built product matches the designed product. Skipping design QA means accepting drift between design and code that will compound with every release.

### Visual Fidelity

Pixel-perfect comparison is a relic of fixed-width desktop design. Modern design QA checks proportions, spacing rhythm, and visual weight rather than exact pixel measurements. Verify:

- Spacing rhythm is consistent (elements breathe evenly)
- Typography hierarchy reads correctly (you can identify H1, H2, body at a glance)
- Color application matches semantic intent (errors are red, success is green)
- Visual weight is balanced (no section feels heavier than intended)
- Component proportions match the design (buttons are the right height, icons are the right size)

### Responsive Testing

Test across the defined breakpoint spectrum. At minimum:

- 320px (small mobile -- iPhone SE)
- 375px (standard mobile -- iPhone 14)
- 768px (tablet portrait)
- 1024px (tablet landscape / small desktop)
- 1440px (standard desktop)
- 1920px (large desktop)

At each breakpoint, verify layout changes match the responsive specification. Check for content overflow, text truncation, and touch target sizes on mobile.

### Interaction State Verification

Systematically trigger every state for every interactive element:

- Hover each button, link, and interactive element
- Tab through the entire page to verify focus states
- Submit forms with invalid data to verify error states
- Trigger loading states and verify skeleton/spinner behavior
- Test empty states by removing data

### Accessibility Verification

- Navigate the entire interface using only the keyboard
- Run a screen reader through the critical user flows
- Verify all images have meaningful alt text
- Confirm color contrast ratios meet WCAG 2.2 AA (4.5:1 for normal text, 3:1 for large text)
- Verify focus is never trapped and skip links function correctly

### Performance Verification

- Check Cumulative Layout Shift (CLS) -- content should not jump during load
- Verify Largest Contentful Paint (LCP) is under 2.5 seconds
- Confirm animations run at 60fps with no jank
- Test on a throttled connection (3G) for graceful degradation

## Deep Dive References

### [Handoff Checklist](references/handoff-checklist.md)

- Overview
- Visual Specifications
- Interaction Specifications
- Responsive Behavior
- Content Specifications
- Accessibility Requirements
- Asset Delivery
- Technical Constraints
- *...and 2 more sections*

### [Annotation Guide](references/annotation-guide.md)

- Overview
- What to Annotate
- Annotation Tools and Methods
- Developer-Readable Specifications
- Visual Specifications
- Interaction Specifications
- Responsive Specifications
- Content Specifications
- *...and 7 more sections*

### [QA Process](references/qa-process.md)

- Overview
- Visual QA Checklist
- Interaction QA Checklist
- Responsive QA Checklist
- Accessibility QA Checklist
- Cross-Browser Testing
- Device Testing Matrix
- Bug Reporting Template
- *...and 4 more sections*

## Next Steps

After completing the handoff documentation, continue with implementation support and quality assurance:

- **[Design System Creation](../design-system-creation/SKILL.md)**: Ensure the design system backing the handoff is complete and documented
- **[Accessibility Audit](../accessibility-audit/SKILL.md)**: Perform a thorough accessibility review of the implemented design
- **[Component Library](../component-library/SKILL.md)**: Verify component implementations match handoff specifications
- **[CSS Architecture](../css-architecture/SKILL.md)**: Ensure the CSS implementation follows the specified token architecture

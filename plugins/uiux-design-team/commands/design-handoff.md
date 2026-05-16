---
name: design-handoff
description: Prepares comprehensive design-to-development handoff documentation with component specs, tokens, and annotation guides
user-invocable: true
allowed-tools: []
---

# Design Handoff

A structured command for preparing thorough design-to-development handoff documentation. This command routes through **@ux-design-lead** to **@design-ops** for execution.

## Workflow

### Step 1: Inventory Components

Catalog every unique component present in the design. For each component, record:

- **Component name** (using the project's naming convention)
- **Variant count** (e.g., primary, secondary, ghost for a button)
- **State count** (default, hover, active, focus, disabled, loading, error)
- **Usage context** (where it appears in the layout)

**Prompt the user:**

> Please describe or provide the design to hand off. I will inventory all components found, including:
> - Interactive elements (buttons, inputs, toggles, selectors)
> - Display elements (cards, badges, tags, avatars, tooltips)
> - Layout elements (headers, footers, sidebars, modals, drawers)
> - Navigation elements (nav bars, tabs, breadcrumbs, pagination)
> - Feedback elements (alerts, toasts, progress bars, skeletons)

Generate a component manifest table:

| # | Component | Variants | States | Notes |
|---|-----------|----------|--------|-------|
| 1 | Button | primary, secondary, ghost, danger | default, hover, active, focus, disabled, loading | Icon-left and icon-right sub-variants |
| 2 | Text Input | standard, with-icon, with-addon | default, focus, filled, error, disabled | Includes label and helper text |
| ... | ... | ... | ... | ... |

### Step 2: Document Specifications

For each component in the inventory, produce a specification sheet covering:

#### Spacing Specifications Checklist

- [ ] Internal padding (top, right, bottom, left)
- [ ] Margin/gap relative to adjacent elements
- [ ] Minimum touch target size (44x44px for mobile, 24x24px minimum for desktop)
- [ ] Icon-to-text spacing
- [ ] Spacing between grouped components (e.g., button groups, form fields)
- [ ] Container padding at each breakpoint

#### Typography Specifications Checklist

- [ ] Font family (including fallback stack)
- [ ] Font size (using design system tokens)
- [ ] Font weight
- [ ] Line height
- [ ] Letter spacing (if non-default)
- [ ] Text transform (uppercase, capitalize, none)
- [ ] Text truncation behavior (ellipsis, wrap, clip)
- [ ] Maximum line count (if applicable)

#### Color Token Specifications Checklist

- [ ] Background color (all states)
- [ ] Text/foreground color (all states)
- [ ] Border color (all states)
- [ ] Shadow/elevation values
- [ ] Overlay/backdrop colors
- [ ] Focus ring color and style
- [ ] Semantic color mapping (success, warning, error, info)
- [ ] Dark mode equivalents (if applicable)

#### Responsive Behavior Checklist

- [ ] Behavior at each breakpoint (mobile, tablet, desktop, wide)
- [ ] Stack/reflow rules
- [ ] Visibility changes (show/hide at breakpoints)
- [ ] Size adaptation (full-width on mobile, fixed on desktop)
- [ ] Touch vs. pointer interaction differences
- [ ] Container query behavior (if applicable)

#### Interaction States Checklist

- [ ] Default/resting state
- [ ] Hover state (desktop only)
- [ ] Active/pressed state
- [ ] Focus state (keyboard navigation)
- [ ] Focus-visible state (keyboard-only focus indicator)
- [ ] Disabled state
- [ ] Loading/pending state
- [ ] Error/invalid state
- [ ] Selected/checked state
- [ ] Expanded/collapsed state (if applicable)
- [ ] Dragging state (if applicable)
- [ ] Transition/animation between states

### Step 3: Create Annotation Guide

Produce a visual annotation guide that developers can reference. The guide should cover:

**Measurement Annotations:**
- Use red lines for spacing measurements
- Use blue lines for component dimensions
- Use green highlights for interactive/clickable areas
- Label all measurements in pixels and rem equivalents

**Naming Convention:**
```
[component]--[variant]--[state]
Example: button--primary--hover
```

**Layering and Z-Index Map:**

| Layer | Z-Index Range | Elements |
|-------|---------------|----------|
| Base content | 0 | Page content, cards, sections |
| Sticky elements | 100-199 | Sticky headers, floating action buttons |
| Dropdowns | 200-299 | Select menus, popovers, autocomplete |
| Overlays | 300-399 | Backdrop overlays, scrims |
| Modals | 400-499 | Dialogs, modal sheets |
| Toasts | 500-599 | Notifications, snackbars |
| Tooltips | 600-699 | Tooltips, contextual help |

### Step 4: Prepare Asset List

Compile all assets required for implementation:

**Icons:**
- Icon name, size(s), format (SVG preferred)
- Color: currentColor (inherits from parent) or fixed color
- Accessibility: aria-label or decorative (aria-hidden)

**Images:**
- Source file, export sizes (1x, 2x, 3x)
- Format recommendations (WebP with JPEG fallback)
- Lazy loading candidates
- Alt text for each image

**Fonts:**
- Font files required (WOFF2 preferred)
- Font weights actually used
- Character subsets (Latin, extended Latin, etc.)
- Font-display strategy (swap, optional, fallback)

**Other assets:**
- Favicons and app icons
- Open Graph images
- Lottie/animation files
- Video assets with poster frames

### Step 5: Generate Handoff Document

Compile all of the above into a single, structured handoff document with the following sections:

```markdown
# Design Handoff: [Project/Feature Name]

## Overview
Brief description of what is being handed off, its purpose, and user-facing impact.

## Design System Tokens Used
List of all design tokens referenced (colors, spacing, typography, elevation).

## Component Specifications
Per-component spec sheets from Step 2.

## Layout & Grid
Grid system, breakpoints, container widths, column configuration.

## Annotation Guide
Visual guide from Step 3.

## Asset Manifest
Complete asset list from Step 4.

## Interaction Notes
Any complex interactions, micro-animations, or conditional logic.

## Accessibility Requirements
WCAG compliance targets, ARIA patterns, keyboard navigation flows.

## Open Questions
Any unresolved design decisions flagged for developer input.
```

## Delegation

1. **@ux-design-lead** receives the handoff request, reviews the design for completeness, and identifies gaps.
2. **@design-ops** executes the full handoff documentation process, coordinating token extraction, spec generation, and asset preparation.

## Cross-Plugin Bridge (PROACTIVE)

When preparing the design handoff:

- PROACTIVELY route to the **frontend-engineering-team** plugin's **@frontend-lead** for implementation planning. The handoff document should be accompanied by a technical implementation plan that engineering has validated.
- PROACTIVELY engage **@typescript-architect** to design type-safe component interfaces that match the spec'd component variants and states.
- PROACTIVELY engage **@build-tooling-specialist** to validate that design tokens map correctly to the Tailwind configuration and CSS custom property setup.
- PROACTIVELY engage **@testing-engineer** to plan test coverage for every component and interaction documented in the handoff, including accessibility test requirements.
- PROACTIVELY engage **@react-specialist** to validate component architecture feasibility (Server vs Client boundaries, hooks requirements, rendering strategy).

The handoff is not complete until both design and engineering have validated the specifications.

## Quality Gates

Before delivering the handoff document, verify:

- [ ] Every component has all states documented
- [ ] All spacing uses design system tokens (no magic numbers)
- [ ] Color tokens map to semantic names, not raw hex values
- [ ] Responsive behavior is defined for at least 3 breakpoints
- [ ] All interactive elements have keyboard navigation defined
- [ ] Focus order is documented for complex layouts
- [ ] All images have alt text specified
- [ ] Animations include duration, easing, and reduced-motion alternatives
- [ ] The handoff document is self-contained (a developer can build from it alone)

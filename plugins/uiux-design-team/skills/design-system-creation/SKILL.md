---
name: design-system-creation
description: Build comprehensive design systems with token architecture, component APIs, Atomic Design methodology, theming support, multi-brand capability, documentation strategy, governance models, and versioning for scalable UI consistency.
metadata:
   references:
   - references/atomic-design-guide.md
   - references/component-api-guide.md
   - references/theming-patterns.md
   - references/token-architecture.md
---

# Design System Creation

A design system is the single source of truth for how a product looks, feels, and behaves. It is not a component library, a style guide, or a Figma file -- it encompasses all of these and more. A design system encodes design decisions into reusable, governed, documented artifacts that enable teams to build consistent interfaces at scale without bottlenecking on a central design team.

Building a design system is an investment in velocity. The cost is upfront; the payoff compounds with every screen, every feature, and every new team member who can ship consistent UI without reinventing decisions.

## Quick Start Checklist

When building a design system from scratch, follow this sequence:

1. **Audit existing UI** -- Screenshot every unique component, pattern, and style across the product. Identify inconsistencies, duplicates, and gaps.
2. **Define design tokens** -- Establish the foundational values (colors, spacing, typography, elevation, radii) that everything else builds on. See [Token Architecture](references/token-architecture.md).
3. **Build atoms** -- Create the smallest indivisible components: buttons, inputs, labels, icons, badges, avatars, spinners.
4. **Compose molecules** -- Combine atoms into functional units: search bars (input + button), form fields (label + input + error), nav items (icon + label).
5. **Create organisms** -- Assemble molecules into complex, distinct sections: headers, sidebars, card grids, data tables, forms.
6. **Define templates** -- Page-level layouts that arrange organisms into content areas without real data.
7. **Document everything** -- Every component needs usage guidelines, API documentation, do/don't examples, and accessibility notes.
8. **Establish governance** -- Define who can propose changes, how changes are reviewed, and how versions are released.

## Atomic Design Overview

Brad Frost's Atomic Design methodology provides a mental model for building UI from small to large. It maps directly to how component libraries are structured.

| Level | Description | Examples |
|-------|-------------|---------|
| **Atoms** | Smallest UI elements, cannot be broken down further | Button, Input, Label, Icon, Badge, Avatar, Divider |
| **Molecules** | Groups of atoms functioning as a unit | Search bar, Form field, Stat card, Toast notification |
| **Organisms** | Complex sections composed of molecules and atoms | Header, Sidebar, Card grid, Data table, Hero section |
| **Templates** | Page layouts with placeholder content areas | Dashboard layout, Settings layout, Marketing page layout |
| **Pages** | Templates populated with real content and data | Actual dashboard with live metrics, real settings page |

For a thorough breakdown of each level with component catalogs, see [Atomic Design Guide](references/atomic-design-guide.md).

## Token Architecture Overview

Design tokens are the foundation of every design system. They encode raw values into a three-tier architecture that enables theming, multi-brand support, and consistent styling.

### Three Tiers

1. **Global tokens** -- Raw values with no semantic meaning: `--color-blue-500: #3b82f6`, `--spacing-4: 1rem`
2. **Alias tokens** -- Semantic meaning mapped to global values: `--color-primary: var(--color-blue-500)`, `--spacing-content-gap: var(--spacing-4)`
3. **Component tokens** -- Scoped to specific components: `--button-bg: var(--color-primary)`, `--card-padding: var(--spacing-content-gap)`

This three-tier system is what makes theming possible. Switching from Brand A to Brand B means changing only the alias layer. Switching light to dark mode means remapping alias tokens to different global values. Components never change.

For full implementation details, see [Token Architecture](references/token-architecture.md).

## Component Inventory Methodology

Before building components, you need to know what exists. A component inventory answers: what do we have, how inconsistent is it, and what should we build first?

### Process

1. **Screenshot audit**: Capture every screen in the product. Group by page type.
2. **Component extraction**: Identify every distinct UI element. Catalog variants (is that button the same as this button?).
3. **Inconsistency map**: Document where the same concept is implemented differently (three different modal styles, five button sizes).
4. **Priority matrix**: Score components by frequency of use (high = appears on many screens) and inconsistency (high = many variants). Build high-frequency, high-inconsistency components first.

## Documentation Strategy

A design system without documentation is just a code library. Documentation turns code into a shared language.

### What to Document

- **Usage guidelines**: When to use this component (and when not to)
- **API reference**: Every prop, slot, event, and CSS custom property
- **Do/Don't examples**: Visual examples of correct and incorrect usage
- **Accessibility notes**: ARIA attributes, keyboard behavior, screen reader expectations
- **Code examples**: Copy-paste snippets for common use cases

### Documentation Tooling

- **Storybook**: Interactive component explorer with knobs, docs, and visual testing integration
- **MDX**: Combine Markdown prose with live component demos
- **Figma documentation**: Annotated component pages with usage notes in the design tool

## Governance Model

Design systems are living products. Without governance, they drift, fragment, and die.

### Contribution Model

| Role | Responsibility |
|------|---------------|
| **Core team** | Maintain tokens, core components, documentation, versioning |
| **Contributors** | Propose new components, report bugs, submit enhancements |
| **Consumers** | Use the system, provide feedback, follow guidelines |

### Change Process

1. **Proposal**: Open an issue describing the change, its rationale, and its impact
2. **Design review**: Core team evaluates against system principles and existing patterns
3. **Implementation**: Build the change with tests, documentation, and migration notes
4. **Release**: Semantic versioning (breaking changes = major, new features = minor, fixes = patch)

### Versioning

Follow semantic versioning strictly:
- **Major (X.0.0)**: Breaking changes to component APIs or token names
- **Minor (0.X.0)**: New components, new variants, new tokens (backward-compatible)
- **Patch (0.0.X)**: Bug fixes, documentation updates, accessibility improvements

Publish changelogs with every release. Include migration guides for breaking changes.

## Deep Dive References

### [Token Architecture](references/token-architecture.md)

- Three-Tier Token Hierarchy
- Token Naming Conventions
- Token Types
- Token Formats
- Style Dictionary Configuration
- Token Transformation Pipeline
- Platform-Specific Output
- Versioning Tokens

### [Component API Guide](references/component-api-guide.md)

- Prop Naming Conventions
- Required vs Optional Props
- Prop Types and Validation
- Event / Callback Naming
- Composition vs Configuration
- Accessibility Props
- Size / Variant / Color Conventions
- Forward Refs
- *...and 2 more sections*

### [Theming Patterns](references/theming-patterns.md)

- CSS Custom Properties Theming
- Multi-Brand Theming
- Theme Switching (Light / Dark / Custom)
- Theme Tokens
- Theme Provider Patterns
- Runtime vs Compile-Time Theming
- Theme Inheritance
- White-Labeling

### [Atomic Design Guide](references/atomic-design-guide.md)

- The Five Levels
- Atoms
- Molecules
- Organisms
- Templates
- Pages
- Creation Workflow
- Component Documentation Template
- *...and 7 more sections*

## Next Steps

After establishing the design system foundation, build out the implementation:

- **[Design Tokens](../design-tokens/SKILL.md)**: Deep dive into token implementation, naming conventions, and platform output
- **[Component Library](../component-library/SKILL.md)**: Build the component library with composition patterns and variant systems
- **[Visual Design](../visual-design/SKILL.md)**: Apply visual identity and brand alignment to the system
- **[Design Handoff](../design-handoff/SKILL.md)**: Prepare the system for cross-team adoption and developer consumption

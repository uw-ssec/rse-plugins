---
name: design-tokens
description: Implement design tokens with three-tier architecture (global, alias, component), naming conventions, CSS custom properties, multi-platform output, and token governance for consistent, themeable design across applications.
metadata:
   references:
   - references/naming-conventions.md
   - references/platform-output.md
   - references/token-taxonomy.md
---

# Design Tokens

Design tokens are the atoms of a design system. They are platform-agnostic key-value pairs that store visual design decisions -- colors, spacing, typography, elevation, motion -- in a format that can be consumed by any platform: web, iOS, Android, or documentation tools. Tokens replace hard-coded values with meaningful names, making design systems maintainable, themeable, and scalable.

Without tokens, a design system is a collection of components with magic numbers. With tokens, it is a coherent system where changing `--color-primary` from blue to green updates every component that references it, across every platform, in one commit.

## Three-Tier Architecture

The three-tier token system separates raw values from semantic meaning from component usage. This separation is what enables theming, multi-brand support, and systematic change.

### Tier 1: Global Tokens

Raw values with descriptive names. No semantic meaning. These are your palette, your scale, your raw material.

```css
--color-blue-500: #3b82f6;
--color-blue-600: #2563eb;
--color-gray-100: #f3f4f6;
--color-gray-900: #111827;
--spacing-1: 0.25rem;
--spacing-2: 0.5rem;
--spacing-4: 1rem;
--spacing-8: 2rem;
--font-size-sm: 0.875rem;
--font-size-base: 1rem;
--font-size-lg: 1.125rem;
```

### Tier 2: Alias Tokens

Semantic tokens that map to global values. These encode design intent. Alias tokens are where theming happens -- switch the mapping, switch the theme.

```css
--color-primary: var(--color-blue-500);
--color-primary-hover: var(--color-blue-600);
--color-surface: var(--color-gray-100);
--color-on-surface: var(--color-gray-900);
--spacing-content-gap: var(--spacing-4);
--spacing-section-gap: var(--spacing-8);
--font-size-body: var(--font-size-base);
```

### Tier 3: Component Tokens

Scoped to specific components. They reference alias tokens, isolating components from global changes. Component tokens are optional -- use them when a component needs to deviate from the alias layer or when you want explicit documentation of a component's token dependencies.

```css
--button-bg: var(--color-primary);
--button-bg-hover: var(--color-primary-hover);
--button-padding-x: var(--spacing-4);
--button-padding-y: var(--spacing-2);
--button-font-size: var(--font-size-body);
```

## Token Categories

| Category | What It Stores | Examples |
|----------|---------------|---------|
| **Color** | Palette scales, semantic colors, state colors | `--color-red-500`, `--color-error`, `--color-success` |
| **Spacing** | Whitespace, padding, margins, gaps | `--spacing-0` through `--spacing-24` |
| **Sizing** | Component heights, icon sizes, avatar sizes | `--size-icon-sm`, `--size-avatar-lg` |
| **Typography** | Font families, sizes, weights, line heights | `--font-family-body`, `--font-weight-bold` |
| **Elevation** | Box shadows for depth levels | `--shadow-sm`, `--shadow-lg` |
| **Border radius** | Corner rounding | `--radius-sm`, `--radius-full` |
| **Opacity** | Transparency levels | `--opacity-disabled`, `--opacity-overlay` |
| **Motion** | Durations and easing functions | `--duration-fast`, `--ease-in-out` |
| **Breakpoints** | Responsive width thresholds | `--breakpoint-sm`, `--breakpoint-lg` |
| **Z-index** | Stacking layers | `--z-dropdown`, `--z-modal`, `--z-toast` |

## Naming Convention

Follow a consistent pattern: `--{category}-{property}-{variant}-{state}`

```
--color-primary              (category: color, variant: primary)
--color-primary-hover        (category: color, variant: primary, state: hover)
--spacing-content-gap        (category: spacing, property: content-gap)
--font-size-heading-lg       (category: font, property: size, variant: heading-lg)
--button-color-bg-disabled   (component: button, category: color, property: bg, state: disabled)
```

For comprehensive naming guidance and real-world examples from Shopify Polaris, IBM Carbon, and Atlassian, see [Naming Conventions](references/naming-conventions.md).

## CSS Custom Properties Implementation

CSS custom properties are the primary web implementation for design tokens.

```css
:root {
  /* Global tokens */
  --color-blue-500: #3b82f6;
  --spacing-4: 1rem;

  /* Alias tokens */
  --color-primary: var(--color-blue-500);
  --spacing-gap: var(--spacing-4);
}

/* Dark theme override at the alias layer */
[data-theme="dark"] {
  --color-primary: var(--color-blue-400);
  --color-surface: var(--color-gray-900);
  --color-on-surface: var(--color-gray-100);
}
```

## Token Governance

Tokens are shared infrastructure. Changes to tokens ripple across every component and every screen. Governance ensures stability.

- **Adding tokens**: Any team member can propose via pull request. Core team reviews for naming consistency and necessity.
- **Changing token values**: Requires design review. Alias and component token changes are low-risk. Global token value changes affect everything downstream.
- **Removing tokens**: Treat as a breaking change. Deprecate first, remove in a major version. Provide migration guidance.
- **Auditing tokens**: Periodically review for unused tokens, inconsistent naming, and missing categories.

## Deep Dive References

### [Token Taxonomy](references/token-taxonomy.md)

- Token Tiers Overview
- Global Tokens (Primitive Palette)
- Alias Tokens (Semantic Mappings)
- Component Tokens (Specific Bindings)
- Spacing Tokens (Scale)
- Typography Tokens
- Shadow Tokens
- Border Tokens
- *...and 3 more sections*

### [Naming Conventions](references/naming-conventions.md)

- CTI (Category-Type-Item) Structure
- Semantic Naming vs Absolute Naming
- Platform Prefixes
- Casing Conventions
- Namespace Strategies
- Aliasing Conventions
- Deprecated Token Handling
- Documentation Standards

### [Platform Output](references/platform-output.md)

- CSS Custom Properties Output
- SCSS Variables Output
- iOS / Swift Output
- Android / Kotlin Output
- React Native Output
- JSON Output for Design Tools
- Style Dictionary Transforms and Formats
- CI/CD Integration for Token Publishing

## Next Steps

After implementing design tokens, integrate them into the broader system:

- **[Design System Creation](../design-system-creation/SKILL.md)**: Use tokens as the foundation of the full design system
- **[Component Library](../component-library/SKILL.md)**: Consume tokens in component implementations
- **[Color Systems](../color-systems/SKILL.md)**: Define color token scales, semantic mapping, and contrast requirements
- **[Typography Systems](../typography-systems/SKILL.md)**: Implement type scale tokens and fluid typography

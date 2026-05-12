---
name: css-architecture
description: Choose and implement CSS architecture patterns including BEM, Tailwind CSS, CSS Modules, CSS-in-JS, cascade layers, CSS custom properties, and specificity management for maintainable, scalable styling.
metadata:
   references:
   - references/bem-guide.md
   - references/css-in-js-patterns.md
   - references/css-modules-guide.md
   - references/tailwind-patterns.md
---

# CSS Architecture

CSS architecture prevents styling chaos at scale. Without deliberate architectural decisions, CSS codebases inevitably devolve into specificity wars, unpredictable overrides, duplicated declarations, and the fear-driven practice of only adding styles and never removing them. The right architecture makes styling predictable, maintainable, and scalable.

This skill covers the major CSS architecture approaches, the foundational CSS features that underpin all of them, and how to choose the right approach for your project.

## Decision Matrix

Choosing a CSS architecture is one of the most consequential decisions in a frontend project. The wrong choice creates friction that compounds over time.

| Approach | Best For | Team Size | Learning Curve | Runtime Cost | Type Safety |
|----------|----------|-----------|---------------|-------------|-------------|
| **BEM** | Large teams with shared CSS, CMS themes | Any | Low | None | No |
| **Tailwind CSS** | Rapid prototyping, utility-first teams, design systems | Any | Medium | None (build-time purge) | No |
| **CSS Modules** | Component-scoped apps (React, Vue, Next.js) | Small-Medium | Low | None (build-time) | No |
| **styled-components / Emotion** | Dynamic theming, component co-location | Small-Medium | Medium | Yes (runtime) | Optional |
| **Vanilla Extract** | Type-safe, zero-runtime, large apps | Medium-Large | High | None (build-time) | Yes |
| **Panda CSS** | Utility-first with type safety, modern stacks | Medium-Large | High | None (build-time) | Yes |

### Decision Flow

1. **Do you need type-safe styles?** Yes: Vanilla Extract or Panda CSS. No: Continue.
2. **Is runtime performance critical?** Yes: Avoid styled-components/Emotion at scale. No: Continue.
3. **Do you need dynamic, props-based styling?** Yes: CSS-in-JS (styled-components, Emotion) or Panda CSS. No: Continue.
4. **Do you prefer utility classes?** Yes: Tailwind CSS. No: Continue.
5. **Do you need global, sharable CSS?** Yes: BEM. No: CSS Modules.

## CSS Custom Properties

CSS custom properties (variables) are the foundation that all modern CSS architectures build upon. They enable theming, design token consumption, runtime dynamism, and component-level customization without JavaScript.

### Defining Design Tokens as Custom Properties

```css
:root {
  /* Color tokens */
  --color-primary: #2563eb;
  --color-primary-hover: #1d4ed8;
  --color-surface: #ffffff;
  --color-text: #1a1a2e;

  /* Spacing tokens */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;

  /* Typography tokens */
  --font-body: 'Source Sans 3', sans-serif;
  --font-display: 'Fraunces', serif;
  --text-base: 1rem;
  --text-lg: 1.25rem;
  --leading-normal: 1.5;
}
```

### Scoping with Selectors

Custom properties follow CSS inheritance. Define global tokens on `:root` and override per-context:

```css
/* Global default */
:root {
  --color-surface: #ffffff;
  --color-text: #1a1a2e;
}

/* Dark theme override */
[data-theme="dark"] {
  --color-surface: #1a1a2e;
  --color-text: #e2e8f0;
}

/* Component-scoped override */
.card--featured {
  --color-surface: #f0f9ff;
  --color-text: #0c4a6e;
}
```

### Theming with Property Override

The power of custom properties for theming is that components reference tokens, and themes redefine those tokens:

```css
.button {
  background: var(--color-primary);
  color: var(--color-on-primary, #ffffff);
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-md, 0.375rem);
}

/* No button overrides needed; the theme changes the tokens */
[data-theme="warm"] {
  --color-primary: #dc2626;
  --color-on-primary: #ffffff;
}
```

## Cascade Layers

The `@layer` rule, introduced in CSS Cascade Layers, gives you explicit control over the cascade order. This solves the age-old problem of specificity conflicts between resets, frameworks, component styles, and overrides.

### Layer Ordering

```css
/* Declare layer order first; later layers override earlier ones */
@layer reset, base, components, utilities, overrides;

@layer reset {
  *, *::before, *::after { box-sizing: border-box; margin: 0; }
}

@layer base {
  body { font-family: var(--font-body); color: var(--color-text); }
  a { color: var(--color-primary); }
}

@layer components {
  .card { padding: var(--space-lg); background: var(--color-surface); }
  .button { /* button styles */ }
}

@layer utilities {
  .sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0,0,0,0); }
  .text-center { text-align: center; }
}

@layer overrides {
  /* Emergency overrides, page-specific adjustments */
}
```

### Integrating with Frameworks

When using third-party CSS (e.g., a component library), wrap their styles in a layer to control their cascade priority:

```css
@layer vendor, components, overrides;

@import url('vendor-library.css') layer(vendor);

@layer components {
  /* Your component styles override vendor styles regardless of specificity */
}
```

## Specificity Management

Specificity conflicts are the root cause of most CSS maintenance pain. Every architecture approach includes a specificity management strategy.

### Keep Specificity Flat

The ideal CSS codebase has uniformly low specificity. Every selector should have roughly the same specificity weight, so source order alone determines cascade resolution.

| Selector | Specificity | Recommendation |
|----------|------------|----------------|
| `.card` | 0-1-0 | Ideal: single class |
| `.card .title` | 0-2-0 | Acceptable: limited nesting |
| `.sidebar .card .title a` | 0-3-1 | Avoid: deep nesting |
| `#main .card` | 1-1-0 | Avoid: ID selectors |
| `div.card` | 0-1-1 | Avoid: qualifying with element |

### Why BEM Helps Specificity

BEM methodology produces selectors with exactly 0-1-0 specificity because every selector is a single class:

```css
.card { }           /* 0-1-0 */
.card__title { }    /* 0-1-0 */
.card--featured { } /* 0-1-0 */
```

No nesting. No IDs. No element qualifiers. Every selector has equal weight, and source order becomes the only cascade factor.

### Utility-First Specificity

Tailwind and utility-first approaches generate single-class selectors with 0-1-0 specificity. Cascade layers place utilities after components, so a utility class `.text-center` always overrides a component class `.card__body` by layer order, not specificity.

### Avoiding `!important`

The `!important` flag breaks the cascade. Legitimate uses are rare:

- Utility classes that must always win (e.g., `.sr-only`)
- Overriding inline styles from third-party widgets

If you find yourself using `!important` to fix a styling issue, the real problem is a specificity or cascade ordering issue that should be fixed at the architectural level.

## Deep Dive References

### [BEM Guide](references/bem-guide.md)

- BEM Naming Convention
- File Organization
- Preprocessor Integration
- Component-Scoped BEM
- BEM with Utility Classes
- Migration Patterns
- Naming Edge Cases

### [Tailwind Patterns](references/tailwind-patterns.md)

- Configuration and Theme Extension
- Component Extraction
- Design Token Integration
- CVA for Variant Management
- JIT Compilation
- Performance Optimization
- Tailwind with Design Systems

### [CSS Modules Guide](references/css-modules-guide.md)

- Local Scoping Mechanism
- Framework Integration
- Composes Keyword
- Global Styles Escape Hatch
- Theming with CSS Modules
- Naming Conventions
- Co-Location Patterns

### [CSS-in-JS Patterns](references/css-in-js-patterns.md)

- Runtime vs Build-Time
- styled-components Patterns
- Emotion Patterns
- Vanilla Extract
- Panda CSS
- Performance Comparison
- Choosing the Right Approach

## Next Steps

After establishing CSS architecture, build out the systematic styling foundations:

- **[Design Tokens](../design-tokens/SKILL.md)**: Define the token layer that feeds into any CSS architecture
- **[Frontend Components](../frontend-components/SKILL.md)**: Implement components that consume your styling architecture
- **[Design System Creation](../design-system-creation/SKILL.md)**: Build the comprehensive system that ties architecture to components
- **[Responsive Design](../responsive-design/SKILL.md)**: Apply responsive strategies within your chosen CSS architecture

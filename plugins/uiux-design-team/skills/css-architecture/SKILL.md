---
name: css-architecture
description: Use when starting a new frontend project and choosing a CSS approach, refactoring inconsistent CSS, hitting specificity wars, integrating a component library, adding theming/dark mode, or deciding between BEM, Tailwind, CSS Modules, or CSS-in-JS.
metadata:
   references:
   - references/bem-guide.md
   - references/css-in-js-patterns.md
   - references/css-modules-guide.md
   - references/tailwind-patterns.md
---

# CSS Architecture

## Decision Matrix

| Approach | Best For | Runtime Cost | Type Safety |
|----------|----------|-------------|-------------|
| BEM | Large teams, CMS themes, global CSS | None | No |
| Tailwind CSS | Rapid prototyping, design systems | None (purge) | No |
| CSS Modules | Component-scoped apps (React, Vue, Next.js) | None | No |
| styled-components / Emotion | Dynamic theming, co-location | Runtime | Optional |
| Vanilla Extract | Type-safe, zero-runtime, large apps | None | Yes |
| Panda CSS | Utility-first with type safety | None | Yes |

**Decision flow:**
1. Need type-safe styles? → Vanilla Extract or Panda CSS.
2. Runtime perf critical? → Avoid styled-components/Emotion at scale.
3. Need props-based dynamic styling? → CSS-in-JS or Panda CSS.
4. Prefer utility classes? → Tailwind.
5. Need global, sharable CSS? → BEM. Otherwise → CSS Modules.

## Workflow

1. Pick approach via matrix above.
2. Define tokens as CSS custom properties on `:root` (see snippet below).
3. Declare cascade layers in order: `@layer reset, base, components, utilities, overrides;`.
4. Configure stylelint with the linter snippet below.
5. Run validation commands at the bottom. If any check fails, fix before merging.

## CSS Custom Properties (Tokens)

```css
:root {
  --color-primary: #2563eb;
  --color-surface: #ffffff;
  --color-text: #1a1a2e;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --radius-md: 0.375rem;
}

[data-theme="dark"] {
  --color-surface: #1a1a2e;
  --color-text: #e2e8f0;
}
```

## Cascade Layers

```css
@layer reset, base, components, utilities, overrides;

@import url('vendor-library.css') layer(vendor);

@layer components {
  .card { padding: var(--space-lg); background: var(--color-surface); }
}

@layer utilities {
  .sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0,0,0,0); }
}
```

## Specificity Targets

| Selector | Specificity | Verdict |
|----------|------------|---------|
| `.card` | 0-1-0 | Ideal |
| `.card .title` | 0-2-0 | Acceptable |
| `#main .card` | 1-1-0 | Avoid (ID) |
| `div.card` | 0-1-1 | Avoid (qualifier) |

If you reach for `!important`, fix the layer order or selector instead.

## Stylelint Config (copy-paste)

`.stylelintrc.json`:

```json
{
  "extends": ["stylelint-config-standard"],
  "rules": {
    "selector-max-id": 0,
    "selector-max-specificity": "0,3,0",
    "selector-max-compound-selectors": 3,
    "declaration-no-important": true,
    "custom-property-pattern": "^[a-z][a-z0-9]*(-[a-z0-9]+)*$",
    "no-descending-specificity": true
  }
}
```

## Validation Checklist

Run these before merging. Each must pass.

```bash
# 1. Lint passes with zero errors
npx stylelint "**/*.css"

# 2. Specificity audit: report any selector above 0,3,0
npx specificity-graph src/**/*.css

# 3. Search for !important (should return zero hits outside utilities layer)
grep -rn "!important" src/ --include="*.css" | grep -v "@layer utilities"

# 4. Search for ID selectors in stylesheets
grep -rnE "^#[a-zA-Z]" src/ --include="*.css"

# 5. Production CSS bundle size (target <50KB gzipped for most apps)
gzip -c dist/assets/*.css | wc -c
```

**Browser test pass criteria:**
- Theme toggle (`[data-theme="dark"]`) updates all components without per-component overrides.
- Vendor library styles do not override your component styles (verify in DevTools Computed panel).
- Lighthouse "Unused CSS" report shows <10KB unused.

## Deep Dive References

- [BEM Guide](references/bem-guide.md) — Naming, file organization, preprocessor integration
- [Tailwind Patterns](references/tailwind-patterns.md) — Config, CVA, JIT, design tokens
- [CSS Modules Guide](references/css-modules-guide.md) — Scoping, composes, framework integration
- [CSS-in-JS Patterns](references/css-in-js-patterns.md) — Runtime vs build-time, Vanilla Extract, Panda

## Next Steps

- **[Design Tokens](../design-tokens/SKILL.md)**: Token layer feeding the architecture
- **[Frontend Components](../frontend-components/SKILL.md)**: Components consuming the styling
- **[Design System Creation](../design-system-creation/SKILL.md)**: Tie architecture to components
- **[Responsive Design](../responsive-design/SKILL.md)**: Responsive strategies within the chosen approach

# CSS Modules Guide

Comprehensive reference for CSS Modules as a styling architecture. Covers the local scoping mechanism, framework integration with React, Vue, and Next.js, the composes keyword for composition, global styles, theming strategies, naming conventions, and co-location patterns.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Local Scoping Mechanism](#local-scoping-mechanism) | 14-45 | How CSS Modules generate unique class names and prevent collisions |
| [Framework Integration](#framework-integration) | 47-95 | Using CSS Modules in React, Vue, and Next.js |
| [Composes Keyword](#composes-keyword) | 97-130 | Composing styles from other modules for reuse without duplication |
| [Global Styles Escape Hatch](#global-styles-escape-hatch) | 132-155 | Breaking out of local scope when necessary |
| [Theming with CSS Modules](#theming-with-css-modules) | 157-190 | Theme implementation using CSS custom properties and module composition |
| [Naming Conventions](#naming-conventions) | 192-220 | Class naming strategies within CSS Modules |
| [Co-Location Patterns](#co-location-patterns) | 222-250 | File organization and component-style co-location |
| [See Also](#see-also) | 252-258 | Related references and skills |

## Local Scoping Mechanism

CSS Modules transform class names at build time to guarantee uniqueness. Each `.className` in a CSS Module file becomes a unique string in the compiled output, eliminating the possibility of name collisions across your entire application.

### How It Works

Given a CSS Module file:

```css
/* Button.module.css */
.button {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
}

.primary {
  background: var(--color-primary);
  color: white;
}

.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

The build tool (webpack, Vite, esbuild) transforms the class names:

```css
/* Compiled output */
.Button_button_a1b2c { padding: 0.5rem 1rem; /* ... */ }
.Button_primary_d3e4f { background: var(--color-primary); /* ... */ }
.Button_disabled_g5h6i { opacity: 0.5; /* ... */ }
```

The JavaScript import receives a mapping object:

```js
import styles from './Button.module.css';
// styles = {
//   button: "Button_button_a1b2c",
//   primary: "Button_primary_d3e4f",
//   disabled: "Button_disabled_g5h6i",
// }
```

### Build Tool Configuration

Most modern tools support CSS Modules out of the box when files end in `.module.css`:

- **Vite**: Zero configuration. Any `.module.css` file is treated as a CSS Module.
- **Next.js**: Zero configuration. Built-in CSS Module support.
- **webpack**: Requires `css-loader` with `modules: true` option.

## Framework Integration

### React

```tsx
import styles from './Card.module.css';

function Card({ featured, children }) {
  return (
    <div className={`${styles.card} ${featured ? styles.featured : ''}`}>
      <div className={styles.body}>{children}</div>
    </div>
  );
}
```

For cleaner class name joining, use the `clsx` library:

```tsx
import clsx from 'clsx';
import styles from './Card.module.css';

function Card({ featured, compact, children }) {
  return (
    <div className={clsx(styles.card, {
      [styles.featured]: featured,
      [styles.compact]: compact,
    })}>
      {children}
    </div>
  );
}
```

### Vue

Vue supports CSS Modules natively in Single File Components with the `module` attribute:

```vue
<template>
  <div :class="[$style.card, { [$style.featured]: featured }]">
    <div :class="$style.body">
      <slot />
    </div>
  </div>
</template>

<style module>
.card {
  padding: var(--space-lg);
  background: var(--color-surface);
  border-radius: var(--radius-md);
}

.featured {
  border-left: 4px solid var(--color-primary);
}

.body {
  color: var(--color-on-surface);
}
</style>
```

Vue's `$style` object is automatically available in templates when using `<style module>`.

### Next.js

Next.js treats `.module.css` files as CSS Modules automatically. Combine with Next.js font optimization:

```tsx
import styles from './Layout.module.css';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export default function Layout({ children }) {
  return (
    <div className={`${inter.className} ${styles.layout}`}>
      <header className={styles.header}>...</header>
      <main className={styles.main}>{children}</main>
    </div>
  );
}
```

Next.js also supports global CSS imports in `_app.tsx` or `layout.tsx` for base styles and reset files.

## Composes Keyword

The `composes` keyword allows one CSS Module class to inherit styles from another, either within the same file or from a different module.

### Same-File Composition

```css
/* Button.module.css */
.base {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  border-radius: var(--radius-sm);
  transition: background-color 150ms ease;
}

.primary {
  composes: base;
  background: var(--color-primary);
  color: white;
}

.secondary {
  composes: base;
  background: var(--color-surface);
  color: var(--color-on-surface);
  border: 1px solid var(--color-border);
}
```

When you use `styles.primary`, the element gets both `base` and `primary` class names in the output.

### Cross-File Composition

```css
/* shared/typography.module.css */
.heading { font-weight: 700; line-height: 1.2; }
.body { font-weight: 400; line-height: 1.5; }

/* Card.module.css */
.title {
  composes: heading from './shared/typography.module.css';
  font-size: var(--text-lg);
  margin-bottom: var(--space-sm);
}

.description {
  composes: body from './shared/typography.module.css';
  color: var(--color-text-secondary);
}
```

### Composition vs @apply

| Feature | `composes` (CSS Modules) | `@apply` (Tailwind/PostCSS) |
|---------|--------------------------|----------------------------|
| Output | Multiple class names on element | Inlined properties in single class |
| File size | Shared class, smaller CSS | Duplicated properties, larger CSS |
| Specificity | Multiple 0-1-0 classes | Single 0-1-0 class |
| Cross-file | Yes, with `from` | No |

## Global Styles Escape Hatch

Sometimes you need to target elements outside the local scope: third-party components, slotted content, or body-level styles.

### :global() Selector

```css
/* Card.module.css */
.card {
  padding: var(--space-lg);
}

/* Target a global class within the scoped context */
.card :global(.third-party-badge) {
  position: absolute;
  top: var(--space-sm);
  right: var(--space-sm);
}

/* Entirely global class */
:global(.visually-hidden) {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
}
```

### Global Stylesheet for Base Styles

Keep a non-module CSS file for global concerns:

```
styles/
  globals.css           (reset, base typography, CSS custom properties)
  components/
    Button.module.css
    Card.module.css
```

Import `globals.css` at the application root (e.g., `_app.tsx` in Next.js, `main.ts` in Vite).

## Theming with CSS Modules

CSS Modules pair naturally with CSS custom properties for theming. The module provides component-specific structure; custom properties provide the dynamic values.

### Token-Based Theming

```css
/* Button.module.css */
.button {
  background: var(--color-primary);
  color: var(--color-on-primary);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-sm);
  font-family: var(--font-body);
  font-size: var(--text-base);
}

.button:hover {
  background: var(--color-primary-hover);
}
```

Theme switching happens at the CSS custom property level, not at the module level. When `[data-theme="dark"]` redefines `--color-primary`, every module that references it updates automatically.

### Theme-Specific Overrides

```css
/* Card.module.css */
.card {
  background: var(--color-surface);
  box-shadow: var(--shadow-sm);
}

/* Dark mode specific adjustments */
:global([data-theme="dark"]) .card {
  box-shadow: none;
  border: 1px solid var(--color-border);
}
```

### Multi-Brand Theming

```css
/* tokens.css */
:root {
  --color-primary: #3b82f6;
  --radius-sm: 0.25rem;
}

[data-brand="finance"] {
  --color-primary: #059669;
  --radius-sm: 0;
}

[data-brand="creative"] {
  --color-primary: #8b5cf6;
  --radius-sm: 1rem;
}
```

CSS Module components automatically adopt brand styling because they reference custom properties, not hard-coded values.

## Naming Conventions

### camelCase Class Names

CSS Modules commonly use camelCase for class names because the import object maps directly to JavaScript property access:

```css
/* Card.module.css */
.card { }
.cardHeader { }
.cardBody { }
.cardFooter { }
.isFeatured { }
.isCompact { }
```

```tsx
// Clean property access
<div className={styles.card}>
  <div className={styles.cardHeader}>...</div>
</div>
```

### kebab-case with Bracket Access

If you prefer kebab-case (matching standard CSS conventions), use bracket notation:

```css
.card { }
.card-header { }
.card-body { }
.is-featured { }
```

```tsx
<div className={styles['card-header']}>...</div>
```

### Naming Guidelines

| Convention | Example | When to Use |
|-----------|---------|-------------|
| Component part | `.title`, `.body`, `.footer` | Structural elements of a component |
| State | `.isActive`, `.isDisabled`, `.isLoading` | Boolean states |
| Variant | `.primary`, `.secondary`, `.compact` | Visual variants |
| Size | `.sm`, `.md`, `.lg` | Size variants |

Avoid deeply descriptive names like `.cardHeaderTitleText`. CSS Modules already scope by file, so `.title` inside `Card.module.css` will never collide with `.title` inside `Modal.module.css`.

## Co-Location Patterns

### Component + Module Side by Side

```
components/
  Button/
    Button.tsx
    Button.module.css
    Button.test.tsx
    Button.stories.tsx
  Card/
    Card.tsx
    Card.module.css
    Card.test.tsx
```

### Shared Modules

For styles shared across multiple components (typography, spacing utilities, animation keyframes), create a shared directory:

```
styles/
  shared/
    typography.module.css
    animations.module.css
    layout.module.css
  globals.css
components/
  Card/
    Card.tsx
    Card.module.css    (composes from shared modules)
```

### Index Exports

```tsx
// components/Button/index.ts
export { Button } from './Button';
export type { ButtonProps } from './Button';
```

This keeps imports clean: `import { Button } from '@/components/Button'` rather than `import { Button } from '@/components/Button/Button'`.

### Avoiding Style Leakage

- Never use element selectors in CSS Modules (they apply globally)
- Always use class selectors for component-specific styles
- Use `:global()` sparingly and only for documented exceptions
- Keep module files small -- if a module exceeds 100 lines, the component may need splitting

## See Also

- [[bem-guide.md]] -- BEM naming within CSS Modules for additional structure and readability
- [[tailwind-patterns.md]] -- Utility-first alternative to CSS Modules
- [[css-in-js-patterns.md]] -- Runtime and build-time alternatives with component-level co-location
- [[../../frontend-components/references/react-patterns.md]] -- React component patterns that consume CSS Modules
- [[../../frontend-components/references/vue-patterns.md]] -- Vue SFC integration with CSS Modules
- [[../../design-system-creation/references/theming-patterns.md]] -- Theming strategies that CSS Modules support

**Back to:** [CSS Architecture Skill](../SKILL.md)

# BEM Guide

Complete reference for the Block Element Modifier (BEM) naming convention. Covers the naming system, file organization, preprocessor integration, component-scoped BEM, utility class coexistence, migration patterns, and edge case naming strategies.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [BEM Naming Convention](#bem-naming-convention) | 14-55 | Block, Element, and Modifier definitions with examples |
| [File Organization](#file-organization) | 57-85 | One block per file, directory structure, and import patterns |
| [Preprocessor Integration](#preprocessor-integration) | 87-120 | BEM with Sass nesting, mixins, and the ampersand selector |
| [Component-Scoped BEM](#component-scoped-bem) | 122-150 | BEM inside React, Vue, and Svelte component files |
| [BEM with Utility Classes](#bem-with-utility-classes) | 152-180 | Combining BEM structure with Tailwind or utility helpers |
| [Migration Patterns](#migration-patterns) | 182-215 | Migrating from unstructured CSS to BEM incrementally |
| [Naming Edge Cases](#naming-edge-cases) | 217-250 | Multi-word names, nested elements, modifier stacking, and common mistakes |
| [See Also](#see-also) | 252-258 | Related references and skills |

## BEM Naming Convention

BEM divides CSS classes into three categories: Blocks, Elements, and Modifiers. The naming pattern is `block__element--modifier`. The double underscore separates elements from their block, and the double hyphen separates modifiers from blocks or elements.

### Block

A Block is a standalone, meaningful component. It is the top-level abstraction. Blocks can be nested inside other blocks, but they are semantically independent.

```css
.card { }
.header { }
.search-form { }
.nav { }
```

Block names describe what the component is, not what it looks like. Use `.search-form`, not `.big-blue-box`.

### Element

An Element is a part of a Block that has no standalone meaning. Elements are semantically tied to their block. The naming pattern is `block__element`.

```css
.card__title { }
.card__body { }
.card__footer { }
.search-form__input { }
.search-form__button { }
```

Elements belong to exactly one block. Never write `.card__body__text` -- Svelte's `card__body` is the block-level context for `text`, but in BEM the convention is to flatten: use `.card__text` instead of nesting elements within elements.

### Modifier

A Modifier changes the appearance, behavior, or state of a Block or Element. The naming pattern is `block--modifier` or `block__element--modifier`.

```css
.card--featured { }
.card--compact { }
.card__title--large { }
.button--primary { }
.button--disabled { }
```

Modifiers are always used alongside the base class, never alone:

```html
<!-- Correct: base class + modifier -->
<div class="card card--featured">
  <h2 class="card__title card__title--large">Featured</h2>
</div>

<!-- Wrong: modifier without base class -->
<div class="card--featured">...</div>
```

### Specificity Benefit

Every BEM selector is a single class with specificity 0-1-0. No nesting, no IDs, no element qualifiers. This means the cascade is resolved by source order alone, which is predictable and maintainable.

## File Organization

### One Block Per File

Each BEM block gets its own file. This creates a clean mapping between the filesystem and the component architecture.

```
styles/
  blocks/
    card.scss
    button.scss
    header.scss
    nav.scss
    search-form.scss
    modal.scss
  utilities/
    sr-only.scss
    text-align.scss
  base/
    reset.scss
    typography.scss
  main.scss           (imports all blocks)
```

### Import Order in main.scss

```scss
// 1. Base: reset, typography, custom properties
@use 'base/reset';
@use 'base/typography';

// 2. Blocks: one per file, alphabetical
@use 'blocks/button';
@use 'blocks/card';
@use 'blocks/header';
@use 'blocks/modal';
@use 'blocks/nav';
@use 'blocks/search-form';

// 3. Utilities: last so they override blocks
@use 'utilities/sr-only';
@use 'utilities/text-align';
```

This import order ensures that utilities always win over blocks by source order, without needing specificity hacks or `!important`.

## Preprocessor Integration

Sass nesting with the `&` parent selector keeps BEM-structured code readable while producing flat output.

### Sass Nesting Pattern

```scss
.card {
  padding: var(--space-lg);
  background: var(--color-surface);
  border-radius: var(--radius-md);

  // Elements
  &__title {
    font-size: var(--text-lg);
    font-weight: var(--font-weight-bold);
    margin-bottom: var(--space-sm);
  }

  &__body {
    color: var(--color-text-secondary);
    line-height: var(--leading-relaxed);
  }

  &__footer {
    display: flex;
    justify-content: flex-end;
    gap: var(--space-sm);
    padding-top: var(--space-md);
    border-top: 1px solid var(--color-border);
  }

  // Modifiers
  &--featured {
    border-left: 4px solid var(--color-primary);
    background: var(--color-surface-accent);
  }

  &--compact {
    padding: var(--space-sm);

    .card__title {
      font-size: var(--text-base);
    }
  }
}
```

### Compiled Output

The Sass above compiles to flat, single-class selectors:

```css
.card { padding: var(--space-lg); /* ... */ }
.card__title { font-size: var(--text-lg); /* ... */ }
.card__body { color: var(--color-text-secondary); /* ... */ }
.card__footer { display: flex; /* ... */ }
.card--featured { border-left: 4px solid var(--color-primary); /* ... */ }
.card--compact { padding: var(--space-sm); }
.card--compact .card__title { font-size: var(--text-base); }
```

Note that the `.card--compact .card__title` selector has specificity 0-2-0. This is acceptable because it is a modifier context, but keep these nested modifier overrides to a minimum.

## Component-Scoped BEM

When using BEM inside component-based frameworks, each component file contains the styles for its block.

### React with CSS Modules + BEM

```tsx
import styles from './Card.module.css';

function Card({ featured, children }) {
  const className = [
    styles.card,
    featured && styles['card--featured'],
  ].filter(Boolean).join(' ');

  return <div className={className}>{children}</div>;
}
```

### Vue with Scoped Styles + BEM

```vue
<template>
  <div :class="['card', { 'card--featured': featured }]">
    <h2 class="card__title"><slot name="title" /></h2>
    <div class="card__body"><slot /></div>
  </div>
</template>

<style scoped>
.card { padding: var(--space-lg); }
.card__title { font-size: var(--text-lg); }
.card--featured { border-left: 4px solid var(--color-primary); }
</style>
```

### Svelte with BEM

```svelte
<div class="card" class:card--featured={featured}>
  <h2 class="card__title"><slot name="title" /></h2>
  <div class="card__body"><slot /></div>
</div>

<style>
  .card { padding: var(--space-lg); }
  .card__title { font-size: var(--text-lg); }
  .card--featured { border-left: 4px solid var(--color-primary); }
</style>
```

## BEM with Utility Classes

BEM handles structural styling (layout, spacing, component-specific rules), while utility classes handle one-off adjustments and responsive overrides.

### Separation of Concerns

```html
<div class="card card--featured">
  <h2 class="card__title">Title</h2>
  <p class="card__body text-center">Body content</p>
  <div class="card__footer mt-4">
    <button class="button button--primary">Submit</button>
  </div>
</div>
```

In this approach:
- `card`, `card__title`, `card__body`, `card__footer` handle the component's structural styling
- `text-center`, `mt-4` are utility overrides for specific layout needs

### Cascade Layers for Coexistence

```css
@layer components, utilities;

@layer components {
  .card { /* BEM block styles */ }
  .card__title { /* BEM element styles */ }
}

@layer utilities {
  .text-center { text-align: center; }
  .mt-4 { margin-top: 1rem; }
}
```

Utilities in a later layer always override BEM component styles by layer order, regardless of specificity.

### When to Use BEM vs Utilities

| Scenario | Use BEM | Use Utility |
|----------|---------|-------------|
| Component-specific layout | Yes | No |
| One-off spacing adjustment | No | Yes |
| Interactive states (hover, focus) | Yes | Either |
| Responsive behavior | Yes | Either |
| Quick prototyping | No | Yes |
| Production component library | Yes | Supporting role |

## Migration Patterns

### Incremental Migration Strategy

Migrating from unstructured CSS to BEM is best done incrementally, one component at a time.

**Phase 1: Audit and Map**
- Identify all components in the existing UI
- Map existing class names to BEM block/element/modifier equivalents
- Document the mapping in a migration guide

**Phase 2: Introduce BEM Alongside Existing Styles**
- Add BEM classes to HTML without removing old classes
- Write new BEM styles alongside existing styles
- Both class systems coexist temporarily

```html
<!-- During migration: old and new classes coexist -->
<div class="product-card card">
  <h2 class="product-title card__title">...</h2>
</div>
```

**Phase 3: Remove Legacy Classes**
- Once BEM styles are verified, remove old class names from HTML
- Remove old CSS rules
- Run visual regression tests to confirm no visual changes

**Phase 4: Organize Files**
- Move each block into its own file
- Set up the canonical import order
- Remove the old monolithic CSS file

### Naming Translation Table

| Legacy Pattern | BEM Equivalent |
|---------------|----------------|
| `.product-card .title` | `.product-card__title` |
| `.product-card.featured` | `.product-card--featured` |
| `.product-card .title.small` | `.product-card__title--small` |
| `#sidebar .nav a` | `.sidebar-nav__link` |
| `.btn.btn-primary.btn-lg` | `.button.button--primary.button--lg` |

## Naming Edge Cases

### Multi-Word Block Names

Use a single hyphen to separate words within a block, element, or modifier name:

```css
.search-form { }          /* Multi-word block */
.search-form__submit-button { }  /* Multi-word element */
.search-form--full-width { }     /* Multi-word modifier */
```

### Nested Elements (Flattening)

BEM elements do not nest. Even if the DOM nests elements three levels deep, the BEM class names remain flat:

```html
<!-- DOM structure -->
<div class="card">
  <div class="card__header">
    <h2 class="card__title">Title</h2>  <!-- NOT card__header__title -->
    <span class="card__badge">New</span>
  </div>
</div>
```

The rule: elements are always named relative to the block, never relative to other elements. `.card__header__title` is wrong. `.card__title` is correct.

### Boolean vs Key-Value Modifiers

```css
/* Boolean modifier: the modifier is true or false */
.button--disabled { }
.button--loading { }

/* Key-value modifier: the modifier has a specific value */
.button--size-sm { }
.button--size-lg { }
.button--variant-outline { }
```

### When a Block Contains Another Block

Blocks can be nested in the DOM, but they do not own each other in BEM. Each block styles itself independently:

```html
<div class="card">
  <div class="card__body">
    <!-- This button is its own block, not a card element -->
    <button class="button button--primary">Submit</button>
  </div>
</div>
```

### Common Naming Mistakes

| Mistake | Why It Is Wrong | Correct |
|---------|----------------|---------|
| `.card__header__title` | Elements within elements | `.card__title` |
| `.card_title` | Single underscore | `.card__title` |
| `.card-title` | Hyphen instead of double underscore | `.card__title` |
| `.card--featured__title` | Element of a modifier | `.card__title` (style via `.card--featured .card__title`) |
| `.Card__Title` | Pascal/Title case | `.card__title` (lowercase with hyphens) |

## See Also

- [[tailwind-patterns.md]] -- Utility-first approach that complements or replaces BEM
- [[css-modules-guide.md]] -- Scoped CSS approach that can incorporate BEM naming for readability
- [[css-in-js-patterns.md]] -- Runtime and build-time styling alternatives to BEM
- [[../../design-tokens/references/naming-conventions.md]] -- Token naming conventions that parallel BEM's structured naming
- [[../../component-library/references/composition-patterns.md]] -- Component patterns that BEM styles support

**Back to:** [CSS Architecture Skill](../SKILL.md)

[Back to Responsive Design](../index.md)

# Container Queries Reference

Container queries allow components to adapt their layout based on their container's size, enabling truly responsive component design independent of viewport dimensions.

---

## container-type

The `container-type` property defines how an element establishes a containment context.

```css
/* Respond to inline (width) size only -- most common */
.wrapper {
  container-type: inline-size;
}

/* Respond to both inline and block (width and height) size */
.wrapper {
  container-type: size;
}

/* No size containment -- default value */
.wrapper {
  container-type: normal;
}
```

### inline-size vs size

| Value | Containment | Use When |
|-------|------------|----------|
| `inline-size` | Width only | Most layout changes (column count, stacking direction) |
| `size` | Width and height | Height-dependent layouts (aspect-ratio containers, scroll areas) |

**Recommendation:** Use `inline-size` unless you specifically need height-based queries. `size` establishes stricter containment that can affect layout behavior.

---

## container-name

Name containers so queries can target specific ancestors.

```css
.sidebar {
  container-type: inline-size;
  container-name: sidebar;
}

.main-content {
  container-type: inline-size;
  container-name: main;
}

/* Target the sidebar container specifically */
@container sidebar (min-width: 300px) {
  .nav-link {
    display: flex;
    gap: 8px;
  }
}

/* Target the main content container */
@container main (min-width: 600px) {
  .article {
    columns: 2;
  }
}
```

### Shorthand

```css
/* container shorthand: name / type */
.wrapper {
  container: card / inline-size;
}

/* Equivalent to: */
.wrapper {
  container-name: card;
  container-type: inline-size;
}
```

---

## @container Rule Syntax

```css
@container [name] (condition) {
  /* Styles applied when the container matches the condition */
}
```

### Width-Based Queries

```css
/* Unnamed container -- matches nearest ancestor with container-type */
@container (min-width: 400px) {
  .child { flex-direction: row; }
}

/* Named container */
@container card (min-width: 500px) {
  .card-content { display: grid; grid-template-columns: 1fr 1fr; }
}

/* Range syntax */
@container (width > 400px) {
  .child { flex-direction: row; }
}

/* Combined conditions */
@container (min-width: 300px) and (max-width: 599px) {
  .child { grid-template-columns: repeat(2, 1fr); }
}
```

### Height-Based Queries

Requires `container-type: size` on the container.

```css
.panel {
  container-type: size;
  container-name: panel;
}

@container panel (min-height: 400px) {
  .panel-footer {
    position: sticky;
    bottom: 0;
  }
}
```

---

## Container Query Units

Container query units are relative to the container's dimensions.

| Unit | Description |
|------|-------------|
| `cqw` | 1% of the container's width |
| `cqh` | 1% of the container's height |
| `cqi` | 1% of the container's inline size |
| `cqb` | 1% of the container's block size |
| `cqmin` | Smaller of `cqi` and `cqb` |
| `cqmax` | Larger of `cqi` and `cqb` |

```css
.card-container {
  container-type: inline-size;
}

.card-title {
  /* Font size scales with container width */
  font-size: clamp(1rem, 4cqi, 2rem);
}

.card-image {
  /* Image height proportional to container */
  height: 30cqi;
  object-fit: cover;
}

.card-padding {
  /* Responsive padding based on container */
  padding: 3cqi;
}
```

---

## Nesting Containers

Containers can nest. Child container queries reference their own container, not the outer one.

```css
.page {
  container: page / inline-size;
}

.sidebar {
  container: sidebar / inline-size;
}

/* This query checks the .page container */
@container page (min-width: 1024px) {
  .layout {
    display: grid;
    grid-template-columns: 280px 1fr;
  }
}

/* This query checks the .sidebar container */
@container sidebar (min-width: 250px) {
  .nav-item {
    display: flex;
    align-items: center;
    gap: 8px;
  }
}

@container sidebar (max-width: 249px) {
  .nav-item {
    display: flex;
    justify-content: center;
  }
  .nav-label {
    display: none;
  }
}
```

---

## Combining with Media Queries

Container queries and media queries serve different purposes and work well together.

```css
/* Media query: page-level layout */
@media (min-width: 768px) {
  .page-layout {
    display: grid;
    grid-template-columns: 300px 1fr;
  }
}

/* Container query: component-level adaptation */
.card-wrapper {
  container-type: inline-size;
}

@container (min-width: 350px) {
  .card {
    display: grid;
    grid-template-columns: 120px 1fr;
  }
}

/* Media query for user preferences */
@media (prefers-reduced-motion: reduce) {
  .card {
    transition: none;
  }
}
```

### Guideline

- Use **media queries** for page-level layout, user preferences, and print styles.
- Use **container queries** for component-level layout that depends on available space.

---

## Component-Level Responsive Design

Container queries make components truly portable. The same component works in any layout context.

### Responsive Card

```css
.card-container {
  container-type: inline-size;
  container-name: card;
}

/* Small: vertical stack */
.card {
  display: flex;
  flex-direction: column;
}

.card__image {
  width: 100%;
  aspect-ratio: 16/9;
  object-fit: cover;
}

.card__body {
  padding: 16px;
}

/* Medium: horizontal layout */
@container card (min-width: 400px) {
  .card {
    flex-direction: row;
  }

  .card__image {
    width: 200px;
    aspect-ratio: 1;
  }

  .card__body {
    padding: 20px;
  }
}

/* Large: featured layout with more detail */
@container card (min-width: 600px) {
  .card__image {
    width: 280px;
  }

  .card__body {
    padding: 24px;
  }

  .card__meta {
    display: flex;
    gap: 16px;
  }
}
```

### Responsive Navigation

```css
.nav-container {
  container: nav / inline-size;
}

/* Narrow: icon-only */
.nav-link {
  display: flex;
  justify-content: center;
  padding: 12px;
}

.nav-label {
  display: none;
}

/* Wide enough for labels */
@container nav (min-width: 200px) {
  .nav-link {
    justify-content: flex-start;
    gap: 12px;
    padding: 10px 16px;
  }

  .nav-label {
    display: block;
  }
}
```

### Responsive Sidebar Widget

```css
.widget-container {
  container: widget / inline-size;
}

/* Narrow: compact layout */
.widget {
  padding: 12px;
}

.widget__title {
  font-size: 0.875rem;
}

.widget__list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

/* Wide: expanded layout */
@container widget (min-width: 300px) {
  .widget {
    padding: 20px;
  }

  .widget__title {
    font-size: 1.125rem;
    margin-bottom: 12px;
  }

  .widget__list {
    gap: 8px;
  }
}
```

---

## Browser Support

Container queries have broad support in modern browsers (Chrome 105+, Firefox 110+, Safari 16+). For older browsers:

### Feature Detection

```css
/* Progressive enhancement */
.card {
  /* Base layout for browsers without container query support */
  display: flex;
  flex-direction: column;
}

@supports (container-type: inline-size) {
  .card-wrapper {
    container-type: inline-size;
  }

  @container (min-width: 400px) {
    .card {
      flex-direction: row;
    }
  }
}
```

### JavaScript Feature Detection

```ts
const supportsContainerQueries = CSS.supports('container-type', 'inline-size');

if (!supportsContainerQueries) {
  // Fall back to ResizeObserver-based approach
  const observer = new ResizeObserver((entries) => {
    for (const entry of entries) {
      const width = entry.contentRect.width;
      entry.target.classList.toggle('is-wide', width >= 400);
      entry.target.classList.toggle('is-narrow', width < 400);
    }
  });
  observer.observe(document.querySelector('.card-wrapper'));
}
```

---

## Polyfills

### container-query-polyfill (Google Chrome Labs)

```html
<script src="https://cdn.jsdelivr.net/npm/container-query-polyfill@1/dist/container-query-polyfill.modern.js"></script>
```

This polyfill uses ResizeObserver and MutationObserver to simulate container query behavior in older browsers. It supports `@container` rules written in standard CSS.

### Limitations of Polyfills

- Performance overhead on pages with many containers.
- Container query units (`cqw`, `cqi`) are not polyfilled.
- Some edge cases around nesting may not match native behavior.
- Only use if you must support browsers older than Chrome 105 / Safari 16.

---

## Best Practices

| Practice | Rationale |
|----------|-----------|
| Use `inline-size` over `size` | Less restrictive containment, covers most use cases |
| Name containers for clarity | Makes it obvious which container a query targets |
| Keep query thresholds to 2-3 per component | Too many breakpoints make components hard to reason about |
| Test components in different container widths | Drag the edge of a resizable container, not just the browser window |
| Use container query units sparingly | Prefer fixed values or `clamp()` for predictability |
| Combine with CSS Grid/Flexbox `auto-fit` | Some layouts adapt without any queries at all |

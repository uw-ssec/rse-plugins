---
name: grid-layout-systems
description: Design and implement layout systems using CSS Grid, Flexbox, column grids, modular grids, baseline grids, container queries, and subgrid for responsive, consistent page compositions across devices and content types.
metadata:
   references:
   - references/grid-patterns.md
   - references/responsive-strategies.md
   - references/spacing-systems.md
---

# Grid Layout Systems

Grids are the invisible architecture of every well-designed interface. They create alignment, rhythm, and spatial consistency that users feel even when they cannot articulate it. A page without a grid is a page where every element placement is an ad hoc decision. A page with a grid is a page where every element has a reason for being where it is.

## Grid Types

### Column Grid

The most common grid type for web design. The page is divided into vertical columns with gutters between them.

**Standard configurations:**
- **12-column grid**: Maximum flexibility. Divides evenly into halves (6+6), thirds (4+4+4), quarters (3+3+3+3), and sixths (2+2+2+2+2+2).
- **8-column grid**: Good for simpler layouts. Divides into halves and quarters cleanly.
- **4-column grid**: Mobile layouts. Simple, constrained.

```css
.container {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

/* Content area spanning 8 columns, sidebar spanning 4 */
.content { grid-column: span 8; }
.sidebar { grid-column: span 4; }

/* Full-width section */
.hero { grid-column: 1 / -1; }

/* Centered content block */
.narrow-content { grid-column: 3 / 11; } /* 8 of 12 columns, centered */
```

### Modular Grid

A column grid with horizontal divisions added, creating a matrix of rectangular modules. Each module is the intersection of a column and a row.

**Use cases:**
- Dashboard layouts with cards of varying sizes
- Portfolio and gallery layouts
- Magazine-style editorial layouts

```css
.dashboard {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: repeat(3, 200px);
  gap: 16px;
}

/* A large card spanning 2 columns and 2 rows */
.card-large {
  grid-column: span 2;
  grid-row: span 2;
}

/* Standard single-module card */
.card-standard {
  grid-column: span 1;
  grid-row: span 1;
}
```

### Baseline Grid

An invisible horizontal grid that aligns all text to a consistent vertical rhythm. The baseline grid interval is typically the body text line-height.

```css
:root {
  --baseline: 1.5rem; /* 24px if base is 16px with 1.5 line-height */
}

h1 {
  font-size: 2.5rem;
  line-height: calc(var(--baseline) * 2); /* 48px - double baseline */
  margin-bottom: var(--baseline);
}

h2 {
  font-size: 1.75rem;
  line-height: calc(var(--baseline) * 1.5); /* 36px - 1.5x baseline */
  margin-bottom: var(--baseline);
}

p {
  font-size: 1rem;
  line-height: var(--baseline); /* 24px - single baseline */
  margin-bottom: var(--baseline);
}
```

### Compound Grid

Two or more grids overlaid to create richer alignment possibilities. A 3-column and 4-column grid overlaid produces a 12-column compound grid with unique alignment points.

**When to use compound grids:**
- Complex editorial layouts where a single column count is too limiting
- Designs that need to accommodate both even (halves, quarters) and odd (thirds, fifths) divisions

## CSS Grid Deep Dive

### Named Grid Areas

```css
.page {
  display: grid;
  grid-template-columns: 240px 1fr 300px;
  grid-template-rows: auto 1fr auto;
  grid-template-areas:
    "header  header  header"
    "nav     main    aside"
    "footer  footer  footer";
  min-height: 100vh;
}

.header { grid-area: header; }
.nav    { grid-area: nav; }
.main   { grid-area: main; }
.aside  { grid-area: aside; }
.footer { grid-area: footer; }
```

### Auto-Fill and Auto-Fit

```css
/* Auto-fill: creates as many columns as fit, empty columns remain */
.grid-fill {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 24px;
}

/* Auto-fit: creates as many columns as fit, empty columns collapse */
.grid-fit {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
}
```

**When to use which:**
- `auto-fill` when you want the grid to maintain its column structure even with few items
- `auto-fit` when you want fewer items to expand and fill the available space

### Subgrid

Subgrid allows child grids to inherit the track definitions of their parent grid. This solves the alignment problem where nested components need to align with the outer page grid.

```css
.page {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 24px;
}

.card-group {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: subgrid; /* Inherits parent's 12 columns */
}

.card {
  grid-column: span 4; /* Each card spans 4 of the parent's 12 columns */
}
```

## Flexbox Patterns

Flexbox excels at one-dimensional layouts (row OR column). Use Flexbox for component-level layout and CSS Grid for page-level layout.

### Navigation Bar

```css
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 64px;
}

.navbar-links {
  display: flex;
  gap: 24px;
}
```

### Card Content

```css
.card {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.card-body {
  flex: 1; /* Fills available space, pushing footer to bottom */
}

.card-footer {
  margin-top: auto; /* Alternative: pushes to bottom within flex container */
}
```

### Centering

```css
/* The definitive centering technique */
.center {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Or with grid */
.center-grid {
  display: grid;
  place-items: center;
}
```

## Container Queries

Container queries allow components to respond to their container's size rather than the viewport's size. This is essential for reusable components that may appear in different layout contexts.

```css
/* Define a containment context */
.card-container {
  container-type: inline-size;
  container-name: card;
}

/* Component responds to container width */
@container card (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 120px 1fr;
    gap: 16px;
  }
}

@container card (max-width: 399px) {
  .card {
    display: flex;
    flex-direction: column;
  }

  .card-image {
    aspect-ratio: 16 / 9;
    width: 100%;
  }
}
```

### Container Query Units

```css
/* cqw = 1% of container width */
.card-title {
  font-size: clamp(1rem, 3cqw, 1.5rem);
}
```

## Spacing System

Consistent spacing reinforces the grid's rhythm. Use a base unit and derive all spacing from multiples of it.

### Base-4 System

```css
:root {
  --space-1:  4px;   /* 0.25rem */
  --space-2:  8px;   /* 0.5rem  */
  --space-3:  12px;  /* 0.75rem */
  --space-4:  16px;  /* 1rem    */
  --space-5:  20px;  /* 1.25rem */
  --space-6:  24px;  /* 1.5rem  */
  --space-8:  32px;  /* 2rem    */
  --space-10: 40px;  /* 2.5rem  */
  --space-12: 48px;  /* 3rem    */
  --space-16: 64px;  /* 4rem    */
  --space-20: 80px;  /* 5rem    */
  --space-24: 96px;  /* 6rem    */
}
```

### Spatial Hierarchy

- **Intra-component spacing** (4-12px): Padding within buttons, spacing between icon and label, gaps between form label and input
- **Inter-component spacing** (16-24px): Gap between cards, space between form groups, margin between list items
- **Section spacing** (32-96px): Space between page sections, margin above/below hero areas, separator between content blocks

## Responsive Grid Strategies

### Breakpoint-Based Column Changes

```css
.grid {
  display: grid;
  gap: 16px;
  grid-template-columns: 1fr; /* Mobile: single column */
}

@media (min-width: 640px) {
  .grid {
    grid-template-columns: repeat(2, 1fr); /* Tablet: 2 columns */
    gap: 20px;
  }
}

@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr); /* Desktop: 3 columns */
    gap: 24px;
  }
}

@media (min-width: 1440px) {
  .grid {
    grid-template-columns: repeat(4, 1fr); /* Wide: 4 columns */
  }
}
```

### No-Breakpoint Responsive Grid

```css
/* Components automatically reflow based on available space */
.auto-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr));
  gap: 24px;
}
```

## Deep Dive References

### [Grid Patterns](references/grid-patterns.md)

- Holy Grail Layout
- Dashboard Grid
- Card Grid (Auto-Fit)
- Magazine Layout
- Masonry-Like Grid
- Sidebar Layouts
- Full-Bleed Within Constrained Grid
- Pancake Stack (Sticky Footer)
- *...and 1 more sections*

### [Responsive Strategies](references/responsive-strategies.md)

- Mobile-First vs Desktop-First
- Content-Driven Breakpoints
- Fluid Grids Without Breakpoints
- Container Queries
- Responsive Testing Methodology

### [Spacing Systems](references/spacing-systems.md)

- Base-Unit Systems
- Spatial Hierarchy
- Density Modes
- Spacing Token Naming
- Spacing and Visual Rhythm

## Next Steps

- **[Typography Systems](../typography-systems/SKILL.md)**: Align type to baseline grid
- **[Responsive Design](../responsive-design/SKILL.md)**: Grids within the broader responsive strategy
- **[CSS Architecture](../css-architecture/SKILL.md)**: Organize grid utilities within CSS architecture
- **[Design Tokens](../design-tokens/SKILL.md)**: Encode spacing and breakpoints as tokens

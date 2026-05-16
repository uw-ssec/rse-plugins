[Back to Grid Layout Systems Skill](../SKILL.md)

# CSS Grid Layout Patterns

A collection of production-ready CSS Grid patterns for common layout needs. Each pattern includes complete CSS, HTML structure, and notes on responsive behavior.

---

## Holy Grail Layout

The classic full-page layout: header, footer, main content with two sidebars.

```css
.holy-grail {
  display: grid;
  grid-template-areas:
    "header  header  header"
    "nav     main    aside"
    "footer  footer  footer";
  grid-template-columns: 250px 1fr 300px;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
  gap: 0;
}

.holy-grail > header { grid-area: header; }
.holy-grail > nav    { grid-area: nav; }
.holy-grail > main   { grid-area: main; }
.holy-grail > aside  { grid-area: aside; }
.holy-grail > footer { grid-area: footer; }

/* Responsive: stack everything on mobile */
@media (max-width: 768px) {
  .holy-grail {
    grid-template-areas:
      "header"
      "nav"
      "main"
      "aside"
      "footer";
    grid-template-columns: 1fr;
    grid-template-rows: auto auto 1fr auto auto;
  }
}

/* Tablet: drop the aside sidebar */
@media (min-width: 769px) and (max-width: 1024px) {
  .holy-grail {
    grid-template-areas:
      "header header"
      "nav    main"
      "footer footer";
    grid-template-columns: 220px 1fr;
  }

  .holy-grail > aside {
    display: none;
  }
}
```

```html
<div class="holy-grail">
  <header>Site Header</header>
  <nav>Navigation</nav>
  <main>Main Content</main>
  <aside>Sidebar</aside>
  <footer>Footer</footer>
</div>
```

---

## Dashboard Grid

A dense, multi-widget layout typical of analytics dashboards. Widgets span different numbers of columns and rows.

```css
.dashboard {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  grid-auto-rows: minmax(120px, auto);
  gap: 1rem;
  padding: 1rem;
}

/* Widget sizing classes */
.widget--full   { grid-column: span 12; }
.widget--half   { grid-column: span 6; }
.widget--third  { grid-column: span 4; }
.widget--quarter { grid-column: span 3; }
.widget--two-thirds { grid-column: span 8; }

/* Tall widgets */
.widget--tall   { grid-row: span 2; }
.widget--xtall  { grid-row: span 3; }

/* Widget base styles */
.widget {
  background: var(--bg-secondary);
  border-radius: 8px;
  border: 1px solid var(--border-primary);
  padding: 1.25rem;
  overflow: hidden;
}

/* Responsive: 2-column on tablet, 1-column on mobile */
@media (max-width: 1024px) {
  .dashboard {
    grid-template-columns: repeat(6, 1fr);
  }
  .widget--full   { grid-column: span 6; }
  .widget--half   { grid-column: span 6; }
  .widget--third  { grid-column: span 3; }
  .widget--quarter { grid-column: span 3; }
  .widget--two-thirds { grid-column: span 6; }
}

@media (max-width: 640px) {
  .dashboard {
    grid-template-columns: 1fr;
  }
  .dashboard > * {
    grid-column: span 1 !important;
    grid-row: span 1 !important;
  }
}
```

```html
<div class="dashboard">
  <div class="widget widget--full">Revenue Chart</div>
  <div class="widget widget--two-thirds widget--tall">Activity Feed</div>
  <div class="widget widget--third">Quick Stats</div>
  <div class="widget widget--third">Notifications</div>
  <div class="widget widget--quarter">Users Online</div>
  <div class="widget widget--quarter">Conversion Rate</div>
  <div class="widget widget--quarter">Response Time</div>
  <div class="widget widget--quarter">Error Rate</div>
</div>
```

---

## Card Grid (Auto-Fit)

A responsive card grid that automatically adjusts column count based on available space. No media queries needed.

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr));
  gap: 1.5rem;
  padding: 1.5rem;
}

.card {
  background: var(--bg-secondary);
  border-radius: 12px;
  border: 1px solid var(--border-primary);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.card__image {
  aspect-ratio: 16 / 9;
  object-fit: cover;
  width: 100%;
}

.card__body {
  padding: 1.25rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card__title {
  font-size: var(--text-lg);
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.card__text {
  font-size: var(--text-sm);
  color: var(--fg-secondary);
  flex: 1;
}

.card__footer {
  padding: 1rem 1.25rem;
  border-top: 1px solid var(--border-secondary);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
```

**Variations:**

```css
/* Minimum 250px cards (more columns) */
.card-grid--compact {
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr));
  gap: 1rem;
}

/* Minimum 400px cards (fewer, larger columns) */
.card-grid--wide {
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 400px), 1fr));
  gap: 2rem;
}

/* Fixed 3-column with responsive fallback */
.card-grid--fixed {
  grid-template-columns: repeat(3, 1fr);
}

@media (max-width: 900px) {
  .card-grid--fixed { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 600px) {
  .card-grid--fixed { grid-template-columns: 1fr; }
}
```

---

## Magazine Layout

An editorial layout with a featured article spanning multiple columns and rows, surrounded by smaller articles.

```css
.magazine {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(200px, auto);
  gap: 1.25rem;
  padding: 2rem;
}

/* Featured article: large, spanning top-left */
.magazine__featured {
  grid-column: 1 / 3;
  grid-row: 1 / 3;
}

/* Secondary articles fill the remaining cells */
.magazine__article {
  display: flex;
  flex-direction: column;
}

.magazine__article--wide {
  grid-column: span 2;
}

.magazine__article--tall {
  grid-row: span 2;
}

/* Image treatment */
.magazine__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
}

.magazine__featured .magazine__image {
  aspect-ratio: 3 / 2;
}

/* Responsive */
@media (max-width: 1024px) {
  .magazine {
    grid-template-columns: repeat(2, 1fr);
  }
  .magazine__featured {
    grid-column: 1 / -1;
    grid-row: span 1;
  }
}

@media (max-width: 640px) {
  .magazine {
    grid-template-columns: 1fr;
  }
  .magazine__article--wide,
  .magazine__article--tall {
    grid-column: span 1;
    grid-row: span 1;
  }
}
```

```html
<div class="magazine">
  <article class="magazine__featured">
    <img class="magazine__image" src="featured.webp" alt="Featured story" />
    <h2>Featured Headline</h2>
    <p>Featured article excerpt...</p>
  </article>
  <article class="magazine__article">...</article>
  <article class="magazine__article">...</article>
  <article class="magazine__article magazine__article--wide">...</article>
  <article class="magazine__article">...</article>
  <article class="magazine__article">...</article>
</div>
```

---

## Masonry-Like Grid

CSS Grid doesn't natively support masonry (as of early 2026, `grid-template-rows: masonry` has limited support). Here are practical approaches.

### Approach 1: Multi-Column Fallback

```css
.masonry-columns {
  column-count: 3;
  column-gap: 1.5rem;
  padding: 1.5rem;
}

.masonry-columns > * {
  break-inside: avoid;
  margin-bottom: 1.5rem;
}

@media (max-width: 900px) {
  .masonry-columns { column-count: 2; }
}

@media (max-width: 600px) {
  .masonry-columns { column-count: 1; }
}
```

### Approach 2: Grid with Explicit Row Spans

```css
.masonry-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  grid-auto-rows: 10px; /* Small row unit for fine control */
  gap: 0 1.5rem;
}

/* JavaScript sets grid-row-end based on content height */
.masonry-item {
  /* Base styles */
}
```

```js
function layoutMasonry() {
  const grid = document.querySelector('.masonry-grid');
  const rowHeight = parseInt(
    getComputedStyle(grid).getPropertyValue('grid-auto-rows')
  );
  const gap = parseInt(
    getComputedStyle(grid).getPropertyValue('row-gap') || '0'
  );

  grid.querySelectorAll('.masonry-item').forEach((item) => {
    const contentHeight = item.querySelector('.masonry-item__content').getBoundingClientRect().height;
    const rowSpan = Math.ceil((contentHeight + gap) / (rowHeight + gap));
    item.style.gridRowEnd = `span ${rowSpan}`;
  });
}

// Run on load and resize
window.addEventListener('load', layoutMasonry);
window.addEventListener('resize', layoutMasonry);
```

### Approach 3: Native Masonry (Progressive Enhancement)

```css
@supports (grid-template-rows: masonry) {
  .masonry-native {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    grid-template-rows: masonry;
    gap: 1.5rem;
  }
}
```

---

## Sidebar Layouts

### Fixed Sidebar with Scrollable Content

```css
.sidebar-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  height: 100vh;
}

.sidebar {
  overflow-y: auto;
  border-right: 1px solid var(--border-primary);
  padding: 1.5rem;
}

.content {
  overflow-y: auto;
  padding: 2rem;
}

/* Collapsible sidebar */
.sidebar-layout.sidebar-collapsed {
  grid-template-columns: 64px 1fr;
}

.sidebar-layout.sidebar-collapsed .sidebar__label {
  display: none;
}

/* Mobile: sidebar becomes a drawer */
@media (max-width: 768px) {
  .sidebar-layout {
    grid-template-columns: 1fr;
  }

  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    width: 280px;
    transform: translateX(-100%);
    transition: transform 300ms cubic-bezier(0.16, 1, 0.3, 1);
    z-index: 200;
    background: var(--bg-primary);
  }

  .sidebar.is-open {
    transform: translateX(0);
  }
}
```

### Intrinsic Sidebar (Content-Driven Width)

```css
/* Sidebar takes its natural width; content fills the rest */
.intrinsic-sidebar {
  display: grid;
  grid-template-columns: fit-content(300px) 1fr;
  gap: 2rem;
}

/* Flipped: content then sidebar */
.intrinsic-sidebar--right {
  grid-template-columns: 1fr fit-content(300px);
}

@media (max-width: 768px) {
  .intrinsic-sidebar,
  .intrinsic-sidebar--right {
    grid-template-columns: 1fr;
  }
}
```

### Sidebar with Minimum Content Width

```css
/* Sidebar collapses when content would be too narrow */
.smart-sidebar {
  display: grid;
  grid-template-columns: minmax(200px, 280px) minmax(min(100%, 500px), 1fr);
  gap: 1.5rem;
}

@media (max-width: 768px) {
  .smart-sidebar {
    grid-template-columns: 1fr;
  }
}
```

---

## Full-Bleed Within Constrained Grid

Content that breaks out of a centered, max-width container to span the full viewport width.

```css
.constrained-layout {
  display: grid;
  grid-template-columns:
    1fr
    min(65ch, calc(100% - 4rem))
    1fr;
}

.constrained-layout > * {
  grid-column: 2;
}

/* Full-bleed element breaks out of constraints */
.constrained-layout > .full-bleed {
  grid-column: 1 / -1;
  width: 100%;
}

/* Wide element: wider than content but not full-bleed */
.constrained-layout > .wide {
  grid-column: 1 / -1;
  width: min(90ch, calc(100% - 2rem));
  margin-inline: auto;
}
```

```html
<div class="constrained-layout">
  <h1>Article Title</h1>
  <p>Constrained body text, comfortable reading width...</p>

  <figure class="full-bleed">
    <img src="hero.webp" alt="Full-width image" />
  </figure>

  <p>More constrained body text...</p>

  <figure class="wide">
    <img src="chart.webp" alt="Wider-than-body chart" />
  </figure>

  <p>Returning to normal reading width...</p>
</div>
```

---

## Pancake Stack (Sticky Footer)

The simplest full-page layout: header sticks to top, footer sticks to bottom, content fills the middle.

```css
.pancake {
  display: grid;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}

.pancake > header {
  position: sticky;
  top: 0;
  z-index: 100;
}

.pancake > main {
  padding: 2rem;
}

.pancake > footer {
  /* Always at the bottom, even with short content */
}
```

---

## RAM (Repeat, Auto, Minmax) Pattern

The most versatile one-liner for responsive grids.

```css
/* The pattern */
.ram {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, VAR), 1fr));
  gap: GAP;
}

/* Practical examples */
.ram--cards {
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr));
  gap: 1.5rem;
}

.ram--thumbnails {
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 150px), 1fr));
  gap: 0.5rem;
}

.ram--features {
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr));
  gap: 2rem;
}
```

**auto-fit vs auto-fill:**
- `auto-fit`: empty tracks collapse, content stretches to fill space
- `auto-fill`: empty tracks remain, preserving the column width

Use `auto-fit` when you want items to grow. Use `auto-fill` when you want consistent item sizes regardless of container width.

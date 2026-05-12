[Back to Responsive Design](../index.md)

# Fluid Layout Techniques

Methods for creating layouts that adapt smoothly across all screen sizes without relying solely on breakpoints.

---

## Fluid Typography with clamp()

`clamp()` creates font sizes that scale fluidly between a minimum and maximum value.

```css
/* Syntax: clamp(minimum, preferred, maximum) */
h1 {
  font-size: clamp(1.75rem, 1rem + 3vw, 3.5rem);
  /* At 320px viewport: ~1.75rem (minimum wins) */
  /* At 800px viewport: ~2.5rem (scaling) */
  /* At 1400px viewport: 3.5rem (maximum caps) */
}

h2 {
  font-size: clamp(1.25rem, 0.8rem + 2vw, 2.25rem);
}

p {
  font-size: clamp(1rem, 0.9rem + 0.5vw, 1.25rem);
}
```

### Calculating the Preferred Value

The preferred value determines the scaling rate. Use this formula:

```
preferred = minSize + (maxSize - minSize) * ((100vw - minViewport) / (maxViewport - minViewport))
```

Simplified for common use:

```css
/* Scale from 16px at 320px viewport to 24px at 1280px viewport */
/* Rate: (24 - 16) / (1280 - 320) = 8 / 960 = 0.833vw */
font-size: clamp(1rem, 0.667rem + 0.833vw, 1.5rem);
```

### Fluid Type Scale

```css
:root {
  --text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --text-sm: clamp(0.875rem, 0.8rem + 0.35vw, 1rem);
  --text-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --text-lg: clamp(1.125rem, 0.95rem + 0.85vw, 1.5rem);
  --text-xl: clamp(1.25rem, 0.9rem + 1.5vw, 2rem);
  --text-2xl: clamp(1.5rem, 0.8rem + 2.5vw, 2.75rem);
  --text-3xl: clamp(1.875rem, 0.7rem + 3.5vw, 3.5rem);
  --text-display: clamp(2.25rem, 0.5rem + 5vw, 5rem);
}

h1 { font-size: var(--text-3xl); }
h2 { font-size: var(--text-2xl); }
h3 { font-size: var(--text-xl); }
p  { font-size: var(--text-base); }
```

---

## Fluid Spacing with clamp()

Apply the same technique to margins, padding, and gaps.

```css
:root {
  --space-xs: clamp(0.25rem, 0.2rem + 0.25vw, 0.5rem);
  --space-sm: clamp(0.5rem, 0.4rem + 0.5vw, 0.75rem);
  --space-md: clamp(1rem, 0.75rem + 1vw, 1.5rem);
  --space-lg: clamp(1.5rem, 1rem + 2vw, 3rem);
  --space-xl: clamp(2rem, 1.25rem + 3vw, 4rem);
  --space-2xl: clamp(3rem, 1.5rem + 5vw, 6rem);
}

.section {
  padding-block: var(--space-2xl);
  padding-inline: var(--space-md);
}

.card {
  padding: var(--space-md);
  gap: var(--space-sm);
}

.hero {
  padding-block: var(--space-2xl);
  margin-bottom: var(--space-xl);
}
```

### Fluid Gap in Grid/Flexbox

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: clamp(16px, 2vw, 32px);
}
```

---

## Fluid Grid Columns

Use `auto-fit` and `minmax()` for grids that adapt without breakpoints.

```css
/* Cards that flow to fill available space */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: clamp(16px, 2vw, 24px);
}

/* Tighter minimum for smaller items */
.tag-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 8px;
}

/* auto-fill vs auto-fit */
/* auto-fill: creates empty tracks when there is extra space */
/* auto-fit: collapses empty tracks, stretching items to fill */

/* auto-fill keeps consistent column widths */
.gallery-fill {
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
}

/* auto-fit stretches items to fill the row */
.gallery-fit {
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}
```

### Hybrid: Fixed Sidebar + Fluid Main

```css
.layout {
  display: grid;
  grid-template-columns: minmax(200px, 300px) minmax(0, 1fr);
  gap: clamp(16px, 2vw, 32px);
}

/* On narrow screens, stack */
@media (max-width: 640px) {
  .layout {
    grid-template-columns: 1fr;
  }
}
```

---

## aspect-ratio Property

Maintain proportional dimensions without padding hacks.

```css
.video-container {
  aspect-ratio: 16 / 9;
  width: 100%;
}

.square-avatar {
  aspect-ratio: 1;
  width: 48px;
  border-radius: 50%;
  object-fit: cover;
}

.card-image {
  aspect-ratio: 4 / 3;
  width: 100%;
  object-fit: cover;
}

/* Responsive hero with aspect ratio */
.hero-image {
  aspect-ratio: 21 / 9;
  width: 100%;
  object-fit: cover;
  object-position: center;
}
```

### Fluid Aspect Ratio

```css
/* Aspect ratio that changes with viewport */
.hero {
  aspect-ratio: 16 / 9;
}

@media (max-width: 768px) {
  .hero {
    aspect-ratio: 4 / 3; /* Taller on mobile for better content visibility */
  }
}

@media (max-width: 480px) {
  .hero {
    aspect-ratio: 1; /* Square on small phones */
  }
}
```

---

## Viewport Units

### Traditional Units

| Unit | Description |
|------|-------------|
| `vw` | 1% of viewport width |
| `vh` | 1% of viewport height |
| `vmin` | Smaller of `vw` and `vh` |
| `vmax` | Larger of `vw` and `vh` |

### New Viewport Units (Recommended)

Mobile browsers have dynamic toolbars that change the viewport height. New units handle this:

| Unit | Description |
|------|-------------|
| `dvh` | Dynamic viewport height -- changes as toolbar appears/disappears |
| `svh` | Small viewport height -- smallest possible (toolbar visible) |
| `lvh` | Large viewport height -- largest possible (toolbar hidden) |
| `dvw` | Dynamic viewport width |
| `svw` | Small viewport width |
| `lvw` | Large viewport width |

```css
/* Full-height hero that accounts for mobile toolbar */
.hero {
  min-height: 100vh;           /* Fallback for older browsers */
  min-height: 100dvh;          /* Adjusts when mobile toolbar appears */
}

/* Full-height layout that uses the smallest viewport */
.app-shell {
  height: 100svh;              /* Never overflows, toolbar always accounted for */
}

/* Element that fills the largest available viewport */
.fullscreen-modal {
  height: 100lvh;
}
```

### Using Viewport Units for Fluid Sizing

```css
/* Fluid element sizing */
.sidebar {
  width: clamp(200px, 20vw, 320px);
}

/* Viewport-relative spacing */
.section {
  padding-block: clamp(2rem, 8vh, 6rem);
}
```

---

## min() / max() / clamp() for Responsive Values

These CSS math functions enable responsive values without media queries.

### min()

Returns the smallest of the given values:

```css
/* Container that is either 90% of viewport or 1200px, whichever is smaller */
.container {
  width: min(90%, 1200px);
  margin-inline: auto;
}

/* Image that never exceeds its container or its natural size */
.responsive-image {
  width: min(100%, 800px);
}

/* Padding that caps at a maximum */
.section {
  padding-inline: min(5vw, 64px);
}
```

### max()

Returns the largest of the given values:

```css
/* Minimum width for readability */
.sidebar {
  width: max(250px, 20%);
}

/* Ensure minimum spacing even on small screens */
.gap {
  gap: max(8px, 1vw);
}
```

### clamp()

Combines min and max in a single function:

```css
/* clamp(minimum, preferred, maximum) */

/* Container width: at least 300px, prefers 80%, max 1200px */
.content {
  width: clamp(300px, 80%, 1200px);
}

/* Border radius that scales but stays reasonable */
.card {
  border-radius: clamp(4px, 1vw, 16px);
}

/* Gap that adapts */
.grid {
  gap: clamp(8px, 2vw, 32px);
}
```

### Nesting Math Functions

```css
/* Complex responsive padding */
.section {
  padding: clamp(1rem, max(2vw, 1.5rem), 4rem);
}

/* Width that accounts for sidebar */
.main {
  width: min(100% - 280px, 900px);
}
```

---

## Fluid Images

```css
/* Basic fluid image */
img {
  max-width: 100%;
  height: auto;
}

/* Fluid image within a constrained container */
.article img {
  width: min(100%, 720px);
  height: auto;
  margin-inline: auto;
  display: block;
}

/* Full-bleed image */
.full-bleed {
  width: 100vw;
  margin-left: calc(-50vw + 50%);
}

/* Responsive image with aspect ratio */
.hero-image {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
}

/* Art direction with <picture> */
```

```html
<picture>
  <source media="(min-width: 1024px)" srcset="hero-wide.webp" />
  <source media="(min-width: 640px)" srcset="hero-medium.webp" />
  <img src="hero-narrow.webp" alt="Hero" loading="lazy" decoding="async" />
</picture>
```

---

## Fluid Containers Without max-width Breakpoints

Replace traditional container breakpoints with a single fluid container.

### Traditional (Breakpoint-Based)

```css
/* Traditional: different max-widths at each breakpoint */
.container {
  width: 100%;
  margin-inline: auto;
  padding-inline: 16px;
}
@media (min-width: 640px) { .container { max-width: 640px; } }
@media (min-width: 768px) { .container { max-width: 768px; } }
@media (min-width: 1024px) { .container { max-width: 1024px; } }
@media (min-width: 1280px) { .container { max-width: 1200px; } }
```

### Fluid (No Breakpoints)

```css
/* Fluid: single rule, no breakpoints needed */
.container {
  width: min(100% - 2rem, 1200px);
  margin-inline: auto;
}

/* With fluid padding that grows on wider screens */
.container-fluid {
  width: min(100%, 1400px);
  padding-inline: clamp(1rem, 5vw, 4rem);
  margin-inline: auto;
}
```

### Content Width Containers

```css
/* Narrow container for reading content */
.prose {
  width: min(100% - 2rem, 65ch);
  margin-inline: auto;
}

/* Medium container for forms and cards */
.form-container {
  width: min(100% - 2rem, 640px);
  margin-inline: auto;
}

/* Wide container for dashboards and galleries */
.wide-container {
  width: min(100% - 2rem, 1400px);
  margin-inline: auto;
}
```

### Full-Width with Max Content Width

```css
/* Background spans full width, content is contained */
.section {
  padding-inline: clamp(1rem, 5vw, 4rem);
}

.section-inner {
  max-width: 1200px;
  margin-inline: auto;
}
```

---

## Putting It All Together

A complete fluid layout system using no breakpoints for core sizing:

```css
:root {
  /* Fluid type scale */
  --text-sm: clamp(0.875rem, 0.8rem + 0.35vw, 1rem);
  --text-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --text-lg: clamp(1.25rem, 0.9rem + 1.5vw, 2rem);
  --text-xl: clamp(1.5rem, 0.8rem + 2.5vw, 2.75rem);

  /* Fluid spacing */
  --space-sm: clamp(0.5rem, 0.4rem + 0.5vw, 0.75rem);
  --space-md: clamp(1rem, 0.75rem + 1vw, 1.5rem);
  --space-lg: clamp(2rem, 1.25rem + 3vw, 4rem);
}

/* Fluid container */
.page {
  width: min(100% - 2rem, 1200px);
  margin-inline: auto;
}

/* Fluid grid */
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-md);
}

/* Fluid section spacing */
.section {
  padding-block: var(--space-lg);
}

/* Fluid typography */
.section h2 {
  font-size: var(--text-xl);
  margin-bottom: var(--space-md);
}

.section p {
  font-size: var(--text-base);
  max-width: 65ch;
}
```

This approach eliminates most `@media` queries. Breakpoints are only needed for structural layout changes (showing/hiding navigation, switching from sidebar to stacked layout) -- not for sizing and spacing.

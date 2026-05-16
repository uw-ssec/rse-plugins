# Responsive Strategies

Approaches for building layouts that adapt gracefully to any viewport size. This reference covers mobile-first versus desktop-first methodology, content-driven breakpoints, fluid grids without breakpoints, and a systematic responsive testing methodology.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Mobile-First vs Desktop-First](#mobile-first-vs-desktop-first) | 14-60 | Comparing the two fundamental responsive approaches |
| [Content-Driven Breakpoints](#content-driven-breakpoints) | 62-110 | Setting breakpoints based on content, not devices |
| [Fluid Grids Without Breakpoints](#fluid-grids-without-breakpoints) | 112-155 | Techniques for layouts that adapt without media queries |
| [Container Queries](#container-queries) | 157-195 | Component-level responsive design |
| [Responsive Testing Methodology](#responsive-testing-methodology) | 197-240 | Systematic approach to verifying responsive behavior |
| [See Also](#see-also) | 242-250 | Related references and skills |

## Mobile-First vs Desktop-First

### Mobile-First Approach

Mobile-first means writing CSS for the smallest viewport first, then progressively enhancing with `min-width` media queries for larger screens.

```css
/* Base styles: mobile layout */
.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

/* Enhance for tablet */
@media (min-width: 640px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }
}

/* Enhance for desktop */
@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
  }
}
```

**Advantages:**
- Forces prioritization of core content and actions
- Smaller initial CSS payload (mobile styles are simpler)
- Progressive enhancement aligns with how CSS works (later rules override earlier ones)
- Better performance on mobile devices that download less CSS before first render

**When to use:** Most projects. Mobile-first is the industry standard and the recommended default approach.

### Desktop-First Approach

Desktop-first means writing CSS for the largest viewport first, then using `max-width` media queries to adapt for smaller screens.

```css
/* Base styles: desktop layout */
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

/* Adapt for tablet */
@media (max-width: 1023px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }
}

/* Adapt for mobile */
@media (max-width: 639px) {
  .grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}
```

**Advantages:**
- Easier when converting an existing desktop design to responsive
- Matches the design process when designers deliver desktop mockups first
- Can be simpler for complex desktop layouts that simplify dramatically on mobile

**When to use:** Legacy projects being retrofitted with responsive design, enterprise applications with desktop-primary audiences, or when design deliverables are desktop-first.

## Content-Driven Breakpoints

Device-based breakpoints (320px, 768px, 1024px) target specific devices. Content-driven breakpoints target the points where your specific content begins to look broken. This is the more principled approach.

### The Methodology

1. Start with the smallest viewport width (320px)
2. Slowly widen the browser window
3. When the layout starts to look awkward, broken, or suboptimal -- that is your breakpoint
4. Write the media query at that specific width

**Example process:**

```
At 320px: Single column, stacked cards -- looks fine.
At 480px: Cards have too much horizontal space, text lines too long.
→ Breakpoint at 480px: switch to 2-column card grid.

At 720px: Two cards per row with lots of side padding. Sidebar could fit.
→ Breakpoint at 720px: add sidebar, move to sidebar+content layout.

At 960px: Content column is comfortable, sidebar has room.
→ No breakpoint needed.

At 1200px: Content line length exceeds 75ch, sidebar feels cramped.
→ Breakpoint at 1200px: max-width on content, widen sidebar.
```

### Named Breakpoints for Team Communication

Even with content-driven breakpoints, name them for team communication:

```css
:root {
  /* Content-driven, named for communication */
  --breakpoint-card-grid: 480px;
  --breakpoint-sidebar: 720px;
  --breakpoint-wide: 1200px;
  --breakpoint-ultrawide: 1600px;
}
```

### Typography-Driven Breakpoints

Line length is one of the best indicators for when a layout needs to change:

```css
/* When body text exceeds 75ch, constrain or reflow */
.prose {
  max-width: 65ch;
  margin-inline: auto;
}

/* When there is room for a sidebar without cramping text below 45ch */
@media (min-width: 860px) {
  .article-layout {
    display: grid;
    grid-template-columns: 1fr 280px;
    gap: 48px;
  }
}
```

### Avoiding Breakpoint Overload

Common mistake: too many breakpoints (320, 375, 414, 480, 640, 768, 1024, 1280, 1440, 1920). Each breakpoint adds testing surface area and maintenance cost.

**Target: 3-5 breakpoints for most projects.** If you need more, your components may not be fluid enough between breakpoints. Add fluid techniques (clamp, auto-fill/auto-fit, container queries) to reduce breakpoint dependency.

## Fluid Grids Without Breakpoints

Fluid techniques allow layouts to adapt continuously rather than jumping between discrete breakpoints.

### auto-fill and auto-fit

```css
/* Cards flow from 1 column to many without breakpoints */
.fluid-card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(300px, 100%), 1fr));
  gap: 24px;
}
```

**How it works:**
- `min(300px, 100%)` ensures the minimum is never wider than the container (prevents overflow on small screens)
- `auto-fill` creates as many columns as fit
- As the container grows, columns are added automatically
- As the container shrinks, columns are removed automatically

### Fluid Spacing

```css
.section {
  padding: clamp(16px, 4vw, 64px);
  gap: clamp(16px, 2vw, 32px);
}
```

### Fluid Sidebar

A sidebar that appears when there is room and collapses when there is not, using no media queries:

```css
.sidebar-layout {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
}

.sidebar {
  flex: 1 1 200px;  /* Grows and shrinks, min 200px */
  min-width: 200px;
  max-width: 300px;
}

.content {
  flex: 1 1 60%;    /* Takes remaining space */
  min-width: 300px; /* If less than 300px available, wraps to next line */
}
```

**When this works:** The sidebar wraps below the content when the container is too narrow for both. No breakpoint needed.

### calc() and clamp() for Fluid Values

```css
/* Font size that scales from 14px at 320px viewport to 18px at 1440px */
body {
  font-size: clamp(0.875rem, 0.3vw + 0.8rem, 1.125rem);
}

/* Padding that scales proportionally */
.card {
  padding: clamp(12px, 2cqi, 24px); /* Using container query inline unit */
}
```

## Container Queries

Container queries let components respond to their container's size rather than the viewport. This is essential for reusable components that appear in different layout contexts.

### Basic Container Query

```css
/* Define containment context */
.card-wrapper {
  container-type: inline-size;
  container-name: card;
}

/* Horizontal card when container is wide enough */
@container card (min-width: 500px) {
  .card {
    display: grid;
    grid-template-columns: 200px 1fr;
    gap: 16px;
  }
}

/* Vertical card when container is narrow */
@container card (max-width: 499px) {
  .card {
    display: flex;
    flex-direction: column;
  }
  .card-image {
    aspect-ratio: 16 / 9;
  }
}
```

### Container Query Units

| Unit | Meaning |
|------|---------|
| `cqw` | 1% of container width |
| `cqh` | 1% of container height |
| `cqi` | 1% of container inline size |
| `cqb` | 1% of container block size |
| `cqmin` | Smaller of cqi and cqb |
| `cqmax` | Larger of cqi and cqb |

```css
/* Typography that scales with container, not viewport */
.card-title {
  font-size: clamp(1rem, 4cqi, 1.5rem);
}

.card-body {
  font-size: clamp(0.875rem, 3cqi, 1rem);
}
```

### When Container Queries vs Media Queries

| Scenario | Use |
|----------|-----|
| Page-level layout changes | Media queries |
| Component adapting to its context | Container queries |
| Sidebar width affecting card layout | Container queries |
| Navigation pattern change | Media queries |
| Typography scaling with component size | Container query units |
| Typography scaling with viewport | Viewport units + clamp |

## Responsive Testing Methodology

### The Testing Matrix

Test at these minimum viewport widths (resize continuously between them, do not just check at exact values):

| Width | Represents | What to Check |
|-------|-----------|--------------|
| 320px | iPhone SE, smallest common mobile | Content overflow, touch targets (44x44px min), text legibility |
| 375px | iPhone 14, standard mobile | Typical mobile experience, no horizontal scroll |
| 480px | Large phones, small tablets | Content reflow between mobile and tablet |
| 768px | iPad portrait, small laptops | Sidebar appearance, multi-column transitions |
| 1024px | iPad landscape, small desktops | Full navigation visibility, card grid columns |
| 1280px | Standard desktop | Primary design viewport, all features visible |
| 1440px | Large desktop | No excessive whitespace, content max-width respected |
| 1920px | Full HD monitors | Layout does not break at wide viewports |

### Testing Checklist Per Viewport

For each viewport width, verify:

1. **No horizontal scrollbar** -- Content fits within the viewport width
2. **Text is readable** -- Line length stays within 45-75ch for body text
3. **Touch targets are adequate** -- At least 44x44px on mobile viewports
4. **Images scale correctly** -- No overflow, no excessive cropping
5. **Navigation is accessible** -- Menu is reachable and usable
6. **Interactive states work** -- Hover on desktop, tap on mobile
7. **Forms are usable** -- Input fields are wide enough, labels are visible
8. **Content hierarchy is clear** -- Primary content is prominent at every width

### Continuous Resize Test

Do not only test at specific breakpoints. Slowly resize the browser from 320px to 1920px and watch for:
- Moments where text wraps awkwardly
- Images that jump between sizes
- Gaps that appear or disappear suddenly
- Elements that overlap or clip
- Containers that become too narrow for their content

These "in-between" states reveal the breakpoints you are missing.

## See Also

- [[grid-patterns.md]] -- Layout patterns that demonstrate responsive behavior
- [[spacing-systems.md]] -- Spacing values that adapt across viewport sizes
- [[../../typography-systems/references/type-scale-theory.md]] -- Responsive type scale ratio strategies
- [[../../responsive-design/SKILL.md]] -- Broader responsive design skill covering all aspects
- [[../../design-tokens/SKILL.md]] -- Encoding breakpoints and fluid values as tokens

**Back to:** [Grid Layout Systems Skill](../SKILL.md)

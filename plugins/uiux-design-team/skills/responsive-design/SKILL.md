---
name: responsive-design
description: Use when building or refactoring an interface that must work across phone, tablet, and desktop; setting breakpoints; sizing touch targets; serving responsive images; or testing layout across viewports.
metadata:
   references:
   - references/breakpoint-strategy.md
   - references/container-queries.md
   - references/fluid-layouts.md
---

# Responsive Design

## Workflow

1. **Implement mobile-first.** Write base styles for 320–375px. Add `@media (min-width: ...)` only to enhance.
2. **Set breakpoint tokens.** Use the standard scale below or content-driven values when layouts break.
3. **Apply fluid sizing.** Use `clamp()` for type/spacing and `auto-fit minmax()` for grids before reaching for breakpoints.
4. **Add container queries** for components reused in multiple layout contexts.
5. **Serve responsive images** with `srcset`/`sizes` or `<picture>`.
6. **Verify touch targets** ≥ 44×44 CSS px with ≥ 8px gaps.
7. **Run validation checklist** (bottom). If any check fails, fix and re-test.

## Breakpoint Tokens

```css
:root {
  --bp-sm: 640px;   /* large phones landscape */
  --bp-md: 768px;   /* tablets portrait */
  --bp-lg: 1024px;  /* tablets landscape, small laptops */
  --bp-xl: 1280px;  /* laptops, desktops */
  --bp-2xl: 1536px; /* large desktops */
}
```

```css
/* Mobile-first pattern */
.card { padding: 1rem; }
@media (min-width: 768px) { .card { padding: 1.5rem; display: grid; grid-template-columns: 1fr 1fr; } }
@media (min-width: 1280px) { .card { padding: 2rem; grid-template-columns: 1fr 1fr 1fr; } }
```

## Fluid Sizing with clamp()

```css
:root {
  --fs-base: clamp(1rem, 0.5rem + 1vw, 1.125rem);
  --fs-h1:   clamp(2rem, 1rem + 3vw, 3.5rem);
  --fs-h2:   clamp(1.5rem, 0.75rem + 2vw, 2.5rem);
}

.section { padding: clamp(1rem, 3vw, 3rem); }
```

## Auto-Reflowing Grid

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}
```

## Container Queries

```css
.card-container { container-type: inline-size; }

@container (min-width: 400px) { .card { display: grid; grid-template-columns: 200px 1fr; } }
@container (min-width: 600px) { .card { grid-template-columns: 250px 1fr 150px; } }
```

## Responsive Images

```html
<img
  src="hero-800.jpg"
  srcset="hero-400.jpg 400w, hero-800.jpg 800w, hero-1200.jpg 1200w"
  sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
  alt="..."
/>

<picture>
  <source media="(min-width: 1024px)" srcset="hero-wide.avif" type="image/avif" />
  <source media="(min-width: 1024px)" srcset="hero-wide.webp" type="image/webp" />
  <source srcset="hero-narrow.avif" type="image/avif" />
  <img src="hero-narrow.jpg" alt="..." />
</picture>
```

Prefer AVIF, then WebP, then JPEG.

## Touch Targets

- Minimum 44×44 CSS px (WCAG 2.5.8).
- ≥ 8px gap between adjacent targets.
- Icon-only buttons: expand tap area with padding.
- Inline links: increase line-height for vertical hit area.

## Validation Workflow

Execute in order. If a step fails, fix before proceeding.

**1. Breakpoint sweep.** Resize browser through 320, 375, 414, 640, 768, 1024, 1280, 1536, 1920 px. Pass: no horizontal scroll, no overflow, no overlapping content.

**2. Touch target audit.**
```bash
# Lighthouse mobile audit
npx lighthouse https://localhost:3000 --preset=mobile --only-categories=accessibility
```
Pass: "Tap targets are sized appropriately" score = 100.

**3. Image loading verification.** Open DevTools Network panel, filter to Img. At 375px viewport, the 400w variant loads (not 1200w). At 1280px viewport, the 1200w variant loads.

**4. Container query check.** Place the same component in a wide container and a narrow container on one page. Confirm both render appropriately.

**5. Real-device test matrix.** Pass on each of: iPhone SE (375), iPhone 14 (390), iPad (768), iPad landscape (1024), 13-inch laptop (1366), desktop (1920).

**6. Network throttling.** Chrome DevTools → Slow 3G. Verify skeleton states or loading indicators appear; no layout shift on image load (CLS < 0.1).

**7. Body text minimum.** Inspect computed font-size on body text at smallest breakpoint. Pass: ≥ 16px.

## Deep Dive References

- [Breakpoint Strategy](references/breakpoint-strategy.md) — Common values, content-first, naming, CSS custom properties, container query integration
- [Fluid Layouts](references/fluid-layouts.md) — clamp(), fluid type, aspect-ratio, viewport units, min/max
- [Container Queries](references/container-queries.md) — container-type, nesting, units, browser support

## Next Steps

- **[Grid Layout Systems](../grid-layout-systems/SKILL.md)**: Grid/Flexbox patterns for responsive structures
- **[CSS Architecture](../css-architecture/SKILL.md)**: Organize responsive styles
- **[Wireframing](../wireframing/SKILL.md)**: Design responsive wireframes
- **[Design Tokens](../design-tokens/SKILL.md)**: Store breakpoints and fluid values as tokens

---
name: grid-layout-systems
description: Use when laying out a page or component, choosing between CSS Grid and Flexbox, setting up a column grid, aligning nested components to a parent grid, or building responsive card/dashboard layouts.
metadata:
   references:
   - references/grid-patterns.md
   - references/responsive-strategies.md
   - references/spacing-systems.md
---

# Grid Layout Systems

## Choose the Right Tool

| Need | Use |
|------|-----|
| 2D page layout (rows + columns) | CSS Grid |
| 1D component layout (row OR column) | Flexbox |
| Nested element aligned to parent grid | `grid-template-columns: subgrid` |
| Auto-reflowing card grid (no breakpoints) | Grid + `auto-fit minmax()` |
| Component responsive to container, not viewport | Container queries |

## Workflow

1. Decide page-level vs component-level. Page → Grid. Component → Flexbox.
2. Pick a column count: 12 (flexible), 8 (simpler), 4 (mobile).
3. Set tokens for `--gap`, `--max-width`, spacing scale (see Spacing).
4. Build layout with named areas OR `repeat(N, 1fr)`.
5. Add responsive behavior: prefer `auto-fit minmax()` over breakpoints; fall back to `@media (min-width: ...)` for structural changes.
6. Validate against the checklist at the bottom.

## 12-Column Grid (copy-paste)

```css
.container {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.content { grid-column: span 8; }
.sidebar { grid-column: span 4; }
.hero    { grid-column: 1 / -1; }
.narrow  { grid-column: 3 / 11; }
```

## Named Grid Areas (Holy Grail)

```css
.page {
  display: grid;
  grid-template-columns: 240px 1fr 300px;
  grid-template-rows: auto 1fr auto;
  grid-template-areas:
    "header header header"
    "nav    main   aside"
    "footer footer footer";
  min-height: 100vh;
}
.header { grid-area: header; }
.nav    { grid-area: nav; }
.main   { grid-area: main; }
.aside  { grid-area: aside; }
.footer { grid-area: footer; }
```

## Auto-Reflow Card Grid

```css
/* auto-fit: empty tracks collapse; auto-fill: empty tracks preserved */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(280px, 100%), 1fr));
  gap: 24px;
}
```

## Subgrid (align nested to parent)

```css
.page { display: grid; grid-template-columns: repeat(12, 1fr); gap: 24px; }
.card-group {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: subgrid;
}
.card { grid-column: span 4; }
```

## Flexbox Patterns

```css
/* Navbar */
.navbar { display: flex; align-items: center; justify-content: space-between; }

/* Card with footer pinned to bottom */
.card { display: flex; flex-direction: column; height: 100%; }
.card-body { flex: 1; }
.card-footer { margin-top: auto; }

/* Centering */
.center { display: grid; place-items: center; }
```

## Container Queries

```css
.card-container { container-type: inline-size; container-name: card; }

@container card (min-width: 400px) {
  .card { display: grid; grid-template-columns: 120px 1fr; gap: 16px; }
}
@container card (max-width: 399px) {
  .card { display: flex; flex-direction: column; }
}
```

## Spacing Tokens (Base-4)

```css
:root {
  --space-1: 4px;  --space-2: 8px;   --space-3: 12px;  --space-4: 16px;
  --space-6: 24px; --space-8: 32px;  --space-12: 48px; --space-16: 64px;
}
```

- Intra-component: 4–12px. Inter-component: 16–24px. Section: 32–96px.

## Validation Checklist

- [ ] DevTools grid overlay shows all major elements aligned to the same column tracks.
- [ ] No element uses absolute positioning to escape the grid.
- [ ] Resize from 320px → 1920px: no horizontal scroll, no overlaps, no orphaned items.
- [ ] Cards in an `auto-fit` grid reflow without breakpoints.
- [ ] Sub-components in nested grids align to the parent (use subgrid or matching tracks).
- [ ] Gap values come from spacing tokens, not magic numbers.

## Deep Dive References

- [Grid Patterns](references/grid-patterns.md) — Holy Grail, dashboard, magazine, masonry, sidebar, sticky footer
- [Responsive Strategies](references/responsive-strategies.md) — Mobile-first, content-driven breakpoints, fluid grids
- [Spacing Systems](references/spacing-systems.md) — Base units, hierarchy, density modes, token naming

## Next Steps

- **[Typography Systems](../typography-systems/SKILL.md)**: Align type to baseline grid
- **[Responsive Design](../responsive-design/SKILL.md)**: Broader responsive strategy
- **[CSS Architecture](../css-architecture/SKILL.md)**: Organize grid utilities
- **[Design Tokens](../design-tokens/SKILL.md)**: Encode spacing and breakpoints as tokens

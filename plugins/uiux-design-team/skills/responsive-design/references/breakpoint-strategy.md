[Back to Responsive Design](../index.md)

# Breakpoint Strategy Reference

A practical guide to defining, naming, and implementing breakpoints for responsive layouts.

---

## Common Breakpoint Values

The following breakpoints cover the spectrum of modern devices:

| Name | Width | Typical Devices |
|------|-------|----------------|
| `xs` | 320px | Small phones (iPhone SE) |
| `sm` | 640px | Large phones, small tablets |
| `md` | 768px | Tablets (iPad portrait) |
| `lg` | 1024px | Tablets (landscape), laptops |
| `xl` | 1280px | Desktops, laptops |
| `2xl` | 1440px | Large desktops |
| `3xl` | 1920px | Full HD monitors |

### Choosing Your Breakpoints

Not every project needs all breakpoints. Start with three:

```css
/* Minimum viable breakpoint set */
--breakpoint-sm: 640px;   /* Mobile to tablet transition */
--breakpoint-lg: 1024px;  /* Tablet to desktop transition */
--breakpoint-xl: 1280px;  /* Desktop to wide desktop */
```

Add more only when your content requires them. Five breakpoints is typically the maximum before complexity outweighs benefit.

---

## Mobile-First vs Desktop-First

### Mobile-First (Recommended)

Write base styles for mobile, then layer on styles for larger screens using `min-width`.

```css
/* Base: mobile */
.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

/* Tablet and up */
@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 32px;
  }
}
```

**Why mobile-first:**
- Forces you to prioritize content for the smallest screen.
- Progressive enhancement: you add complexity, never remove it.
- Smaller CSS payloads for mobile devices (no overriding).
- Matches how modern CSS frameworks (Tailwind, Bootstrap) work.

### Desktop-First

Write base styles for desktop, then override for smaller screens using `max-width`.

```css
/* Base: desktop */
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
}

/* Tablet and below */
@media (max-width: 1023px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
  }
}

/* Mobile */
@media (max-width: 767px) {
  .grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}
```

**When to use desktop-first:**
- Legacy projects originally designed for desktop.
- Admin dashboards and internal tools where desktop is the primary context.

---

## Content-First Breakpoints

Instead of device-based breakpoints, set breakpoints where the content breaks.

### Process

1. Start with no breakpoints and a fluid layout.
2. Resize the browser from narrow to wide.
3. When the content looks awkward (text lines too long, elements too cramped or too spaced), add a breakpoint at that width.
4. The resulting breakpoints are specific to your design, not to devices.

```css
/* Content-first breakpoints */
.article {
  max-width: 65ch;   /* Optimal reading width */
  padding: 16px;
}

/* When sidebar can comfortably fit */
@media (min-width: 52rem) {
  .layout {
    display: grid;
    grid-template-columns: 240px 1fr;
  }
}

/* When three-column layout works */
@media (min-width: 80rem) {
  .layout {
    grid-template-columns: 240px 1fr 300px;
  }
}
```

---

## Device-Agnostic Approach

Target capabilities, not specific devices.

```css
/* Bad: targeting specific devices */
@media (min-width: 768px) and (max-width: 1024px) { /* iPad only */ }

/* Good: targeting layout needs */
@media (min-width: 768px) { /* any screen wide enough for two columns */ }

/* Capability-based queries */
@media (hover: hover) { /* devices with hover capability (mouse/trackpad) */ }
@media (pointer: fine) { /* devices with precise pointer (mouse, not finger) */ }
@media (prefers-reduced-motion: reduce) { /* respect user motion preferences */ }
```

---

## Breakpoint Naming Conventions

### T-Shirt Sizes (Most Common)

```
xs, sm, md, lg, xl, 2xl
```

### Descriptive Names

```
mobile, tablet, desktop, wide
```

### Number-Based

```
bp-480, bp-768, bp-1024, bp-1280
```

### Recommendation

Use t-shirt sizes. They are framework-standard, concise, and do not reference specific devices.

---

## Breakpoints in CSS Custom Properties

CSS custom properties cannot be used in `@media` queries directly. Use these workarounds:

### Sass Variables (Pre-compile)

```scss
$breakpoints: (
  sm: 640px,
  md: 768px,
  lg: 1024px,
  xl: 1280px,
);

@mixin respond-to($bp) {
  @media (min-width: map-get($breakpoints, $bp)) {
    @content;
  }
}

// Usage
.sidebar {
  display: none;

  @include respond-to(lg) {
    display: block;
    width: 260px;
  }
}
```

### JavaScript Access

```ts
const breakpoints = {
  sm: 640,
  md: 768,
  lg: 1024,
  xl: 1280,
} as const;

function useBreakpoint(bp: keyof typeof breakpoints) {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const mql = window.matchMedia(`(min-width: ${breakpoints[bp]}px)`);
    setMatches(mql.matches);
    const handler = (e: MediaQueryListEvent) => setMatches(e.matches);
    mql.addEventListener('change', handler);
    return () => mql.removeEventListener('change', handler);
  }, [bp]);

  return matches;
}

// Usage
const isDesktop = useBreakpoint('lg');
```

### PostCSS Custom Media (Spec Proposal)

```css
@custom-media --sm (min-width: 640px);
@custom-media --md (min-width: 768px);
@custom-media --lg (min-width: 1024px);

@media (--lg) {
  .sidebar { display: block; }
}
```

Requires the `postcss-custom-media` plugin.

---

## Breakpoints with Container Queries

Container queries let components respond to their container's size rather than the viewport. This replaces many breakpoint use cases.

```css
.card-container {
  container-type: inline-size;
  container-name: card;
}

/* Container query replaces viewport breakpoint for component-level layout */
@container card (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 200px 1fr;
  }
}

@container card (min-width: 600px) {
  .card {
    grid-template-columns: 250px 1fr auto;
  }
}
```

### When to Use Which

| Scenario | Use Viewport Breakpoints | Use Container Queries |
|----------|------------------------|----------------------|
| Page-level layout changes | Yes | No |
| Component adapts to its container | No | Yes |
| Navigation showing/hiding | Yes | No |
| Card layout changes in a grid | No | Yes |
| Font size scaling across page | Yes | No |
| Sidebar widget adapting | No | Yes |

---

## Testing Across Breakpoints

### Browser DevTools

1. Open DevTools and toggle device toolbar (Ctrl/Cmd + Shift + M).
2. Test at each breakpoint value, not just preset device sizes.
3. Test in-between sizes -- bugs often appear 10-20px around breakpoints.

### Automated Visual Testing

```ts
// Playwright viewport testing
const viewports = [
  { width: 375, height: 812 },   // Mobile
  { width: 768, height: 1024 },  // Tablet
  { width: 1280, height: 800 },  // Desktop
  { width: 1920, height: 1080 }, // Wide
];

for (const viewport of viewports) {
  test(`renders correctly at ${viewport.width}x${viewport.height}`, async ({ page }) => {
    await page.setViewportSize(viewport);
    await page.goto('/');
    await expect(page).toHaveScreenshot(`home-${viewport.width}.png`);
  });
}
```

### Testing Checklist

- [ ] Content is readable at every breakpoint (no text overflow, no truncation hiding critical info)
- [ ] Touch targets are at least 44x44px on mobile
- [ ] Navigation is accessible on all screen sizes
- [ ] Images scale appropriately and do not overflow containers
- [ ] No horizontal scrollbar appears at any width
- [ ] Layout transitions between breakpoints are smooth (no abrupt jumps)
- [ ] Test at 320px width (smallest supported phone)
- [ ] Test at widths just below and above each breakpoint

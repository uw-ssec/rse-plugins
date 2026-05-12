---
name: responsive-design
description: Implement responsive design with mobile-first methodology, breakpoint strategy, fluid layouts using clamp and minmax, container queries, responsive images, touch targets, and device testing to ensure interfaces work across all screen sizes.
metadata:
   references:
   - references/breakpoint-strategy.md
   - references/container-queries.md
   - references/fluid-layouts.md
---

# Responsive Design

Responsive design is a mindset, not a bolt-on. It is not "make the desktop layout work on mobile." It is designing a single interface that adapts intelligently to the constraints and opportunities of every screen size, input method, and context. The best responsive interfaces feel native to every device, not like a compromise.

The core principle: design for the smallest screen first, then enhance for larger ones. This forces you to prioritize ruthlessly -- mobile has no room for "nice to have" content. What survives the mobile cut is what truly matters.

## Mobile-First Methodology

Start with the mobile layout and progressively enhance for larger screens. This approach has practical benefits:

- **Forces content prioritization**: Limited space means only essential content survives
- **Performance by default**: Mobile-first CSS loads the lightest styles first; larger screen styles load conditionally
- **Simpler CSS**: Adding styles for larger screens (min-width) is more intuitive than overriding desktop styles for smaller screens (max-width)
- **Realistic constraints**: Most users are on mobile. Starting there ensures the majority experience is designed first, not retrofitted

```css
/* Mobile-first: base styles are for mobile */
.card { padding: 1rem; }

/* Enhance for tablet */
@media (min-width: 768px) {
  .card { padding: 1.5rem; display: grid; grid-template-columns: 1fr 1fr; }
}

/* Enhance for desktop */
@media (min-width: 1280px) {
  .card { padding: 2rem; grid-template-columns: 1fr 1fr 1fr; }
}
```

## Breakpoint Strategy

Breakpoints should be driven by content, not devices. When the layout breaks -- when content becomes cramped, lines become too long, or elements lose their relationship -- that is where a breakpoint belongs.

That said, common breakpoints align with device categories for practical reasons:

| Token | Width | Typical Devices |
|-------|-------|----------------|
| `sm` | 640px | Large phones in landscape |
| `md` | 768px | Tablets in portrait |
| `lg` | 1024px | Tablets in landscape, small laptops |
| `xl` | 1280px | Laptops, desktops |
| `2xl` | 1536px | Large desktops, external monitors |

Store breakpoints as design tokens. Use consistent names across CSS, JavaScript, and design tools. See [Breakpoint Strategy](references/breakpoint-strategy.md) for detailed guidance.

## Fluid Layouts

Rather than jumping between fixed layouts at breakpoints, use fluid techniques that scale smoothly.

### clamp()

The most powerful tool for fluid sizing. Sets a minimum, preferred, and maximum value.

```css
/* Font size: minimum 1rem, scales with viewport, maximum 1.5rem */
font-size: clamp(1rem, 0.5rem + 1.5vw, 1.5rem);

/* Padding: minimum 1rem, scales fluidly, maximum 3rem */
padding: clamp(1rem, 3vw, 3rem);
```

### minmax() in CSS Grid

```css
/* Cards that are at least 280px, fill available space, wrap automatically */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}
```

For comprehensive fluid layout recipes, see [Fluid Layouts](references/fluid-layouts.md).

## Container Queries

Container queries enable component-level responsiveness. Instead of reacting to the viewport width, a component reacts to the width of its container. This means the same component can adapt whether it is in a full-width main content area or a narrow sidebar.

```css
.card-container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card { display: grid; grid-template-columns: 200px 1fr; }
}

@container (min-width: 600px) {
  .card { grid-template-columns: 250px 1fr 150px; }
}
```

Container queries represent a fundamental shift from page-level to component-level responsive design. See [Container Queries](references/container-queries.md) for implementation patterns.

## Responsive Images

Images are often the heaviest assets on a page. Responsive image techniques ensure the right image loads for the right context.

### srcset and sizes

```html
<img
  src="hero-800.jpg"
  srcset="hero-400.jpg 400w, hero-800.jpg 800w, hero-1200.jpg 1200w"
  sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
  alt="Hero image"
/>
```

### picture Element

```html
<picture>
  <source media="(min-width: 1024px)" srcset="hero-wide.avif" type="image/avif" />
  <source media="(min-width: 1024px)" srcset="hero-wide.webp" type="image/webp" />
  <source srcset="hero-narrow.avif" type="image/avif" />
  <source srcset="hero-narrow.webp" type="image/webp" />
  <img src="hero-narrow.jpg" alt="Hero image" />
</picture>
```

Prefer AVIF (best compression) with WebP fallback and JPEG as the final fallback.

## Touch Targets

Mobile interfaces are operated by imprecise fingers, not precise cursors. WCAG 2.5.8 requires a minimum target size of 44x44 CSS pixels. Apple's HIG recommends 44pt and Material Design recommends 48dp.

- **Buttons, links, and interactive elements**: Minimum 44x44px
- **Spacing between targets**: At least 8px gap to prevent accidental taps
- **Inline links in text**: Increase line height to create sufficient vertical target space
- **Icon buttons without visible boundaries**: Use padding to expand the tap area beyond the visible icon

## Responsive Typography

Typography should scale fluidly between breakpoints, not jump between fixed sizes.

```css
:root {
  --font-size-base: clamp(1rem, 0.5rem + 1vw, 1.125rem);
  --font-size-h1: clamp(2rem, 1rem + 3vw, 3.5rem);
  --font-size-h2: clamp(1.5rem, 0.75rem + 2vw, 2.5rem);
  --line-height-body: clamp(1.5, 1.4 + 0.2vw, 1.75);
}
```

Maintain a minimum of 16px for body text on all devices to ensure readability without zooming.

## Device Testing Strategy

Responsive design requires testing on real devices, not just browser resize.

| Test Level | Method | What It Catches |
|------------|--------|----------------|
| **Browser resize** | Drag browser window | Layout breaks, overflow, squished content |
| **Device emulation** | Chrome DevTools, Safari Responsive Mode | Touch target sizes, viewport units, safe areas |
| **Real devices** | Physical phones and tablets | Touch behavior, scroll performance, font rendering |
| **Network conditions** | Throttled connections | Image loading order, lazy load behavior, skeleton states |

Test at least: iPhone SE (375px), iPhone 14 (390px), iPad (768px), iPad landscape (1024px), laptop (1366px), desktop (1920px).

## Deep Dive References

### [Breakpoint Strategy](references/breakpoint-strategy.md)

- Common Breakpoint Values
- Mobile-First vs Desktop-First
- Content-First Breakpoints
- Device-Agnostic Approach
- Breakpoint Naming Conventions
- Breakpoints in CSS Custom Properties
- Breakpoints with Container Queries
- Testing Across Breakpoints

### [Fluid Layouts](references/fluid-layouts.md)

- Fluid Typography with clamp()
- Fluid Spacing with clamp()
- Fluid Grid Columns
- aspect-ratio Property
- Viewport Units
- min() / max() / clamp() for Responsive Values
- Fluid Images
- Fluid Containers Without max-width Breakpoints
- *...and 1 more sections*

### [Container Queries](references/container-queries.md)

- container-type
- container-name
- @container Rule Syntax
- Container Query Units
- Nesting Containers
- Combining with Media Queries
- Component-Level Responsive Design
- Browser Support
- *...and 2 more sections*

## Next Steps

After implementing responsive design, build out the supporting systems:

- **[Grid Layout Systems](../grid-layout-systems/SKILL.md)**: CSS Grid and Flexbox layout patterns for responsive structures
- **[CSS Architecture](../css-architecture/SKILL.md)**: Organize responsive styles with scalable CSS methodology
- **[Wireframing](../wireframing/SKILL.md)**: Design responsive wireframes showing layout transformations
- **[Design Tokens](../design-tokens/SKILL.md)**: Store breakpoints and fluid values as design tokens

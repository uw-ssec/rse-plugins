---
name: typography-systems
description: Use when building a new type scale, converting fixed sizes to fluid clamp() values, choosing or pairing fonts, fixing readability issues (line height, measure, tracking), or encoding typography as design tokens / CSS custom properties.
metadata:
   references:
   - references/font-pairing-guide.md
   - references/reading-optimization.md
   - references/type-scale-theory.md
---

# Typography Systems

## Build Workflow

### Step 1 — Choose a ratio

Pick by use case (full table in [type-scale-theory.md](references/type-scale-theory.md)):

| Context | Ratio |
|---------|-------|
| Dense data UI / dashboard | 1.125 (Major Second) |
| Most web apps | 1.200 (Minor Third) |
| Content / blog | 1.250 (Major Third) |
| Marketing / editorial | 1.333 (Perfect Fourth) |
| Landing / hero | 1.500 (Perfect Fifth) |

**Checkpoint:** Hold the ratio against your densest screen. If h1 dwarfs everything, drop one step.

### Step 2 — Generate the scale

Base 16px (or 1rem). Multiply up, divide down. Tools: `npx type-scale-generator`, or by hand. Worked example in [type-scale-theory.md](references/type-scale-theory.md).

```css
:root {
  --font-size-xs:      0.64rem;
  --font-size-sm:      0.80rem;
  --font-size-base:    1rem;
  --font-size-lg:      1.25rem;
  --font-size-xl:      1.5625rem;
  --font-size-2xl:     1.953rem;
  --font-size-3xl:     2.441rem;
  --font-size-4xl:     3.052rem;
  --font-size-display: 3.815rem;
}
```

### Step 3 — Implement fluid values

Convert each token to `clamp(min, slope*vw + intercept, max)`. Formula and walkthrough in [type-scale-theory.md](references/type-scale-theory.md).

```css
:root {
  --font-size-xs:      clamp(0.64rem,  0.2vw + 0.56rem,  0.72rem);
  --font-size-sm:      clamp(0.80rem,  0.2vw + 0.72rem,  0.90rem);
  --font-size-base:    clamp(1rem,     0.2vw + 0.93rem,  1.125rem);
  --font-size-lg:      clamp(1.25rem,  0.4vw + 1.1rem,   1.5rem);
  --font-size-xl:      clamp(1.5rem,   0.6vw + 1.3rem,   1.875rem);
  --font-size-2xl:     clamp(1.875rem, 0.8vw + 1.6rem,   2.375rem);
  --font-size-3xl:     clamp(2.25rem,  1.2vw + 1.8rem,   3.052rem);
  --font-size-4xl:     clamp(2.75rem,  1.4vw + 2.2rem,   3.815rem);
  --font-size-display: clamp(3.25rem,  2vw + 2.5rem,     5rem);
}
```

### Step 4 — Test at breakpoints

```bash
# Visual diff at standard widths
npx playwright test --grep "typography snapshots"
```

Or manually in Chrome DevTools `Cmd+Shift+M` at 320, 375, 768, 1024, 1440, 1920px.

**Pass/fail:**
- No h1 wraps to more than 3 lines on mobile.
- No body text below 14px effective at any width.
- Line length stays in 45–75ch on prose containers.

### Step 5 — Validate accessibility

```bash
# Lighthouse will flag font-size < 12px and tap-target conflicts
npx lighthouse https://example.com --only-categories=accessibility --output=json

# axe will flag insufficient text contrast (interacts with type weight)
npx @axe-core/cli https://example.com --tags wcag2aa
```

**Pass criteria:**
- Body ≥ 16px effective at default zoom.
- Text reflows at 200% browser zoom without horizontal scroll.
- Line height ≥ 1.5× font size for body copy (WCAG 1.4.12).
- Letter spacing supports +0.12× font size without breaking layout.

## Font Pairing (Quick Reference)

| Pattern | Combo |
|---------|-------|
| Versatile | Lora (heading) + Inter (body) |
| Editorial | Montserrat (heading) + Lora (body) |
| Strong personality | Space Grotesk (heading) + Inter (body) |
| Developer | JetBrains Mono (accent) + Inter (body) |

Rules: contrast not conflict; max 3 fonts; match x-height. Full guidance, extended combos, and `@font-face` loading strategy in [font-pairing-guide.md](references/font-pairing-guide.md).

## Reading Metrics (Quick Reference)

- **Measure:** `max-width: 65ch` on prose.
- **Leading:** body 1.5–1.6, subheads 1.4–1.5, headings 1.2–1.3, display 1.1–1.2.
- **Tracking:** all-caps +0.08em; display −0.02em; body 0.
- **Paragraph rhythm:** `p + p { margin-top: 1.5em }`.

Full tables, tokens, and dyslexia/dark-mode guidance in [reading-optimization.md](references/reading-optimization.md).

## Deep Dive References

- [references/type-scale-theory.md](references/type-scale-theory.md) — full ratio table, scale math, clamp() walkthrough
- [references/font-pairing-guide.md](references/font-pairing-guide.md) — classification, principles, extended combos, font loading
- [references/reading-optimization.md](references/reading-optimization.md) — measure/leading/tracking detail, accessibility, dark mode, dyslexia

## Next Steps

- **[Visual Design](../visual-design/SKILL.md)**: typography within visual design
- **[Design Tokens](../design-tokens/SKILL.md)**: encode typography as tokens
- **[Grid Layout Systems](../grid-layout-systems/SKILL.md)**: align typography to grid
- **[Responsive Design](../responsive-design/SKILL.md)**: typography in responsive layout

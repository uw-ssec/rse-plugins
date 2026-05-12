---
name: visual-design
description: Use when designing or coding a new interface that needs a distinctive aesthetic direction, when reviewing visuals for hierarchy/brand alignment, or when an existing UI feels generic ("AI slop") and needs production-grade visual polish.
metadata:
   references:
   - references/aesthetic-principles.md
   - references/brand-alignment.md
   - references/visual-hierarchy.md
---

# Visual Design

## Workflow

1. **Commit to one aesthetic direction** (see table below). Pick one — do not blend three.
2. **Document brand inputs**: values, voice, existing tokens, audience, competitors.
3. **Define hierarchy plan**: primary CTA, secondary content, tertiary, decoration — ranked.
4. **Choose type pair**: distinctive display + refined body. Avoid Inter/Roboto/Arial/Space Grotesk defaults.
5. **Build tokens**: colors (dominant + sharp accent), spacing scale, radii, shadows, motion timings.
6. **Implement**: real code (HTML/CSS or framework), not mockups.
7. **Quality gate** (before shipping):
   - Run `npx pa11y <url>` — zero contrast failures (WCAG AA: 4.5:1 body, 3:1 large text).
   - Visual consistency: same spacing scale across all pages, same radius vocabulary, no orphan one-off colors.
   - First-impression check: screenshot the hero, ask "would this be memorable in a Dribbble feed?"
   - Reduced-motion: confirm `prefers-reduced-motion` disables non-essential animation.

## Aesthetic direction picker (one)

| Tone | Use for | Signal moves |
|------|---------|--------------|
| Brutally minimal | Dev tools, SaaS | Mono type, hairline borders, no shadows |
| Luxury/refined | Premium retail | Serif display, restrained palette, generous whitespace |
| Editorial | Content, blogs | Dramatic type contrast, asymmetric grid, large imagery |
| Playful | Consumer, kids | Rounded shapes, bouncy easing, oversized elements |
| Retro-futurist | Creative agency | Neon accents, dark base, geometric shapes, scanlines |
| Organic | Wellness, food | Earth tones, hand-drawn marks, textured backgrounds |
| Brutalist/raw | Art, counter-culture | Exposed structure, system fonts used ironically |
| Industrial | Dashboards | Dense info, mono type, muted colors, grid-heavy |
| Maximalist | Fashion, entertainment | Mixed media, clashing palettes, controlled chaos |
| Glassmorphism | Modern SaaS | Frosted blur over vibrant backgrounds |
| Swiss | Corporate, institutional | Grid precision, Akzidenz-style type, clean geometry |

Full library + when-not-to-use guidance: [aesthetic-principles.md](references/aesthetic-principles.md).

## Concrete example — editorial hero (HTML/CSS)

```html
<section class="hero">
  <p class="kicker">Issue 14 — Winter</p>
  <h1 class="title">The <em>Quiet</em> Architecture<br/>of Better Tools</h1>
  <p class="dek">A field report on craft software, written by the people who use it daily.</p>
  <a class="cta" href="/read">Read the issue →</a>
</section>

<style>
:root {
  --ink: #111; --paper: #f5f1ea; --accent: #c2410c; --rule: #111;
  --serif: "Tiempos Headline", "Cormorant Garamond", Georgia, serif;
  --mono: "JetBrains Mono", ui-monospace, monospace;
}
.hero { background: var(--paper); color: var(--ink); padding: clamp(3rem, 8vw, 8rem) clamp(1.5rem, 6vw, 6rem); border-bottom: 2px solid var(--rule); }
.kicker { font: 500 .8rem/1 var(--mono); letter-spacing: .12em; text-transform: uppercase; margin-bottom: 2rem; }
.title { font: 600 clamp(2.5rem, 7vw, 6rem)/0.95 var(--serif); letter-spacing: -0.02em; max-width: 14ch; margin: 0 0 1.5rem; }
.title em { color: var(--accent); font-style: italic; }
.dek { font: 400 1.125rem/1.5 var(--serif); max-width: 48ch; margin-bottom: 2.5rem; }
.cta { font: 500 .9rem/1 var(--mono); border-bottom: 1px solid currentColor; padding-bottom: 2px; text-decoration: none; color: var(--ink); }
.cta:hover { color: var(--accent); }
@media (prefers-reduced-motion: no-preference) {
  .title { animation: rise .8s cubic-bezier(.2,.7,.2,1) both; }
  @keyframes rise { from { opacity: 0; transform: translateY(1rem); } }
}
</style>
```

## Concrete example — React + Motion staggered reveal

```tsx
import { motion } from "motion/react";

export function FeatureRow({ items }: { items: { title: string; body: string }[] }) {
  return (
    <ul className="grid gap-12 md:grid-cols-3">
      {items.map((it, i) => (
        <motion.li key={it.title}
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-10%" }}
          transition={{ delay: i * 0.08, duration: 0.5, ease: [0.2, 0.7, 0.2, 1] }}>
          <h3 className="font-serif text-2xl">{it.title}</h3>
          <p className="text-neutral-600">{it.body}</p>
        </motion.li>
      ))}
    </ul>
  );
}
```

## Hard rules

- Pick a CLEAR direction (bold minimal OR maximalist) — never timid middle ground.
- One distinctive display font, one refined body font — no more.
- Dominant base color + one sharp accent. Avoid purple-gradient-on-white default.
- Match implementation effort to the tone: maximalist needs many details; minimal needs ruthless restraint.
- Vary across generations — never converge on Space Grotesk + purple + Inter.

## Deeper context

- [Visual Hierarchy](references/visual-hierarchy.md) — hierarchy tools, scanning patterns, golden ratio
- [Brand Alignment](references/brand-alignment.md) — brand audit, mood board, extending vs evolving
- [Aesthetic Principles](references/aesthetic-principles.md) — anti-patterns, tone library, Norman's three levels

## Next Steps

- **[Color Systems](../color-systems/SKILL.md)**: palettes, contrast, semantic tokens, dark mode
- **[Typography Systems](../typography-systems/SKILL.md)**: scales, pairing, fluid type
- **[Motion Design](../motion-design/SKILL.md)**: choreography, performance
- **[Grid Layout Systems](../grid-layout-systems/SKILL.md)**: column grids, spacing scales

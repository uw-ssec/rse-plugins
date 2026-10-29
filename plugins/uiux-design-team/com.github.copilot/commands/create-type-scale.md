---
name: create-type-scale
description: Guided command to create a fluid typographic scale with CSS custom properties using modular scale ratios and clamp() values
user-invocable: true
allowed-tools: []
---

# Create Type Scale

A guided workflow for creating a mathematically grounded, fluid typographic scale. This command routes through **@ux-design-lead** to **@visual-designer** for execution.

## Workflow

### Step 1: Choose Base Size

Ask the user for their base font size. This is the fundamental unit from which all other sizes are derived.

**Prompt the user:**

> What base font size should we use? Common choices:
>
> - **14px** -- Compact interfaces, data-dense dashboards
> - **16px** -- Browser default, most web applications (recommended)
> - **18px** -- Content-heavy sites, editorial, blogs
> - **20px** -- Large-format reading experiences, accessibility-first

Default to **16px** if the user does not specify.

Record as `$BASE_SIZE`.

### Step 2: Select a Modular Scale Ratio

Ask the user to pick a ratio that determines the mathematical relationship between each step in the scale.

**Prompt the user:**

> Choose a typographic scale ratio:
>
> | Ratio | Value | Character | Best For |
> |-------|-------|-----------|----------|
> | Minor Second | 1.067 | Subtle, tight | Dense UI, dashboards |
> | Major Second | 1.125 | Gentle progression | Body-heavy content, documentation |
> | Minor Third | 1.200 | Balanced, versatile | General-purpose web apps |
> | Major Third | 1.250 | Clear hierarchy | Marketing sites, landing pages |
> | Perfect Fourth | 1.333 | Strong contrast | Editorial, news sites |
> | Augmented Fourth | 1.414 | Bold separation | Magazine layouts, portfolios |
> | Perfect Fifth | 1.500 | Dramatic jumps | Hero-driven pages, presentations |
> | Minor Sixth | 1.600 | Very dramatic | Poster-style layouts |
> | Major Sixth | 1.667 | Extreme contrast | Art direction, experimental |
> | Minor Seventh | 1.778 | Very wide range | Display typography |
> | Major Seventh | 1.875 | Near-double jumps | Headline-dominant layouts |
> | Octave | 2.000 | Doubling | Minimal scale, max contrast |
> | Golden Ratio | 1.618 | Harmonious, natural | Design-forward, aesthetic-first |

Default to **Minor Third (1.200)** if the user does not specify.

Record as `$RATIO`.

### Step 3: Define Scale Steps

Determine how many steps above and below the base size are needed.

**Standard scale steps (recommended):**

| Token | Step | Purpose |
|-------|------|---------|
| `--text-xs` | -2 | Fine print, captions, labels |
| `--text-sm` | -1 | Secondary text, metadata |
| `--text-base` | 0 | Body copy, default reading size |
| `--text-md` | +1 | Lead paragraphs, emphasized body |
| `--text-lg` | +2 | H4, card titles |
| `--text-xl` | +3 | H3, section headings |
| `--text-2xl` | +4 | H2, page section titles |
| `--text-3xl` | +5 | H1, page titles |
| `--text-4xl` | +6 | Display, hero headlines |
| `--text-5xl` | +7 | Jumbo display text |

Ask the user if they want the standard 10-step scale or a custom range.

### Step 4: Generate Fluid Scale with clamp()

For each step, compute three values:

1. **Minimum size** -- the size at the smallest viewport (e.g., 320px)
2. **Preferred size** -- a fluid value using `vw` units
3. **Maximum size** -- the size at the largest viewport (e.g., 1440px)

**Formula for each step:**

```
size = $BASE_SIZE * ($RATIO ^ step)
```

**Fluid interpolation formula:**

```
preferred = calc(min_size_rem + (max_size - min_size) * ((100vw - min_viewport) / (max_viewport - min_viewport)))
```

Simplified to a `clamp()` expression:

```css
/* For step N: */
--text-{token}: clamp({min}rem, {preferred}vw + {offset}rem, {max}rem);
```

**Viewport range defaults:**
- Minimum viewport: `320px` (20rem)
- Maximum viewport: `1440px` (90rem)
- Fluid scaling factor: scale down to 85% of computed size at minimum viewport

### Step 5: Output CSS Custom Properties

Generate the final output as a `:root` block of CSS custom properties.

**Example output (base: 16px, ratio: Minor Third 1.200):**

```css
:root {
  /* Type Scale: Minor Third (1.200) | Base: 16px */
  /* Viewport range: 320px to 1440px */

  --text-xs:   clamp(0.6944rem, 0.6604rem + 0.1702vw, 0.8rem);
  --text-sm:   clamp(0.8333rem, 0.7917rem + 0.2083vw, 0.96rem);
  --text-base: clamp(1rem, 0.9286rem + 0.3571vw, 1.25rem);
  --text-md:   clamp(1.2rem, 1.1rem + 0.5vw, 1.5rem);
  --text-lg:   clamp(1.44rem, 1.2971rem + 0.7146vw, 1.9438rem);
  --text-xl:   clamp(1.728rem, 1.5171rem + 1.0546vw, 2.3325rem);
  --text-2xl:  clamp(2.0736rem, 1.7657rem + 1.5396vw, 2.799rem);
  --text-3xl:  clamp(2.4883rem, 2.0481rem + 2.2011vw, 3.3588rem);
  --text-4xl:  clamp(2.986rem, 2.3691rem + 3.0846vw, 4.0306rem);
  --text-5xl:  clamp(3.5832rem, 2.7334rem + 4.2488vw, 4.8366rem);

  /* Line height scale (tighter at larger sizes) */
  --leading-xs:   1.5;
  --leading-sm:   1.5;
  --leading-base: 1.6;
  --leading-md:   1.5;
  --leading-lg:   1.4;
  --leading-xl:   1.3;
  --leading-2xl:  1.25;
  --leading-3xl:  1.2;
  --leading-4xl:  1.1;
  --leading-5xl:  1.1;
}
```

### Step 6: Generate Utility Classes (Optional)

If the user requests utility classes, also output:

```css
/* Typographic Scale Utilities */
.text-xs   { font-size: var(--text-xs);   line-height: var(--leading-xs); }
.text-sm   { font-size: var(--text-sm);   line-height: var(--leading-sm); }
.text-base { font-size: var(--text-base); line-height: var(--leading-base); }
.text-md   { font-size: var(--text-md);   line-height: var(--leading-md); }
.text-lg   { font-size: var(--text-lg);   line-height: var(--leading-lg); }
.text-xl   { font-size: var(--text-xl);   line-height: var(--leading-xl); }
.text-2xl  { font-size: var(--text-2xl);  line-height: var(--leading-2xl); }
.text-3xl  { font-size: var(--text-3xl);  line-height: var(--leading-3xl); }
.text-4xl  { font-size: var(--text-4xl);  line-height: var(--leading-4xl); }
.text-5xl  { font-size: var(--text-5xl);  line-height: var(--leading-5xl); }
```

## Delegation

1. **@ux-design-lead** receives the request and validates the typographic requirements against the project's design system.
2. **@visual-designer** executes the scale generation, ensuring harmony with existing font choices, weight distributions, and layout constraints.

## Validation Checklist

Before delivering the type scale, confirm:

- [ ] All sizes pass WCAG minimum text size recommendations
- [ ] Line heights are appropriate for each size tier
- [ ] The scale has sufficient contrast between heading levels
- [ ] Fluid values don't produce sizes below readable thresholds on small screens
- [ ] The scale is harmonious with the project's spacing system (if one exists)
- [ ] CSS custom properties follow project naming conventions

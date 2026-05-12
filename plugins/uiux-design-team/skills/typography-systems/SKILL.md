---
name: typography-systems
description: Build responsive typography systems with modular type scales, fluid typography using clamp(), font pairing strategies, reading metrics optimization, and CSS custom properties for systematic type management across devices and contexts.
metadata:
   references:
   - references/font-pairing-guide.md
   - references/reading-optimization.md
   - references/type-scale-theory.md
---

# Typography Systems

Typography is the foundation of interface design. It carries 95% of the information in most interfaces, and its quality determines whether content is readable, scannable, and emotionally resonant. A well-built typography system eliminates ad hoc font sizing decisions and creates visual rhythm across every screen.

## Type Scale Fundamentals

A type scale is a predetermined set of font sizes based on a mathematical ratio. Using a scale ensures harmonious proportions and eliminates arbitrary sizing decisions.

### Common Ratios

| Ratio | Value | Character | Best For |
|-------|-------|-----------|----------|
| Minor Second | 1.067 | Very tight, subtle | Dense data UIs, dashboards |
| Major Second | 1.125 | Tight, professional | Enterprise SaaS, data-heavy apps |
| Minor Third | 1.200 | Balanced, versatile | Most web applications |
| Major Third | 1.250 | Clear, readable | Content-rich sites, blogs |
| Perfect Fourth | 1.333 | Strong hierarchy | Marketing sites, editorial |
| Augmented Fourth | 1.414 | Dramatic | Landing pages, portfolios |
| Perfect Fifth | 1.500 | Very dramatic | Hero sections, display typography |
| Golden Ratio | 1.618 | Classical proportion | Art, luxury, editorial |

### Generating a Scale

Start with a base size (typically 16px for body text) and multiply by the ratio for each step up, divide for each step down:

```
Base: 16px, Ratio: 1.250 (Major Third)

Step -2: 16 / 1.250 / 1.250 = 10.24px → 0.64rem  (caption, fine print)
Step -1: 16 / 1.250            = 12.80px → 0.80rem  (small text, labels)
Step  0: 16                     = 16.00px → 1.00rem  (body text)
Step  1: 16 × 1.250            = 20.00px → 1.25rem  (large body, lead text)
Step  2: 16 × 1.250²           = 25.00px → 1.5625rem (h4, subheading)
Step  3: 16 × 1.250³           = 31.25px → 1.953rem  (h3)
Step  4: 16 × 1.250⁴           = 39.06px → 2.441rem  (h2)
Step  5: 16 × 1.250⁵           = 48.83px → 3.052rem  (h1)
Step  6: 16 × 1.250⁶           = 61.04px → 3.815rem  (display)
```

### CSS Custom Properties

```css
:root {
  --font-size-xs:      0.64rem;   /* 10.24px */
  --font-size-sm:      0.80rem;   /* 12.80px */
  --font-size-base:    1rem;      /* 16.00px */
  --font-size-lg:      1.25rem;   /* 20.00px */
  --font-size-xl:      1.5625rem; /* 25.00px */
  --font-size-2xl:     1.953rem;  /* 31.25px */
  --font-size-3xl:     2.441rem;  /* 39.06px */
  --font-size-4xl:     3.052rem;  /* 48.83px */
  --font-size-display: 3.815rem;  /* 61.04px */
}
```

## Fluid Typography

Fluid typography scales smoothly between a minimum and maximum size based on the viewport width, eliminating the need for breakpoint-specific font size overrides.

### The clamp() Approach

```css
/* clamp(minimum, preferred, maximum) */
h1 {
  font-size: clamp(2rem, 5vw + 1rem, 3.815rem);
}

body {
  font-size: clamp(1rem, 0.5vw + 0.875rem, 1.125rem);
}
```

**How it works:**
- Below the minimum viewport, the minimum size applies
- Above the maximum viewport, the maximum size applies
- Between them, the preferred value creates a smooth interpolation

### Calculating Preferred Values

To calculate the preferred value for a smooth transition between two sizes:

```
Given:
  min-size: 2rem at min-viewport: 320px
  max-size: 3.815rem at max-viewport: 1440px

Slope = (max-size - min-size) / (max-viewport - min-viewport)
      = (3.815 - 2) / (1440 - 320)
      = 1.815 / 1120
      = 0.00162rem per px
      = 0.162rem per 100px ≈ 1.62vw

Intercept = min-size - slope × min-viewport
          = 2 - (0.00162 × 320)
          = 2 - 0.518
          = 1.482rem

Result: clamp(2rem, 1.62vw + 1.482rem, 3.815rem)
```

### Full Fluid Type Scale

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

## Font Pairing

Font pairing is the art of selecting two or three typefaces that work together harmoniously. Poor pairing creates visual discord; great pairing creates a cohesive voice.

### Pairing Principles

1. **Contrast, not conflict.** Pair fonts that are clearly different but share structural DNA. A geometric sans with a humanist serif creates contrast. Two similar sans-serifs create confusion.

2. **Limit to 2-3 fonts.** One display/heading font, one body font, and optionally one monospace or accent font. More than three creates visual noise.

3. **Match x-height.** When fonts have similar x-heights (the height of lowercase letters), they feel natural together even at different sizes.

4. **Share an era or designer.** Fonts from the same designer or era often pair well because they share underlying design principles.

### Reliable Pairing Strategies

**Serif heading + Sans-serif body** (most versatile):
- Playfair Display + Source Sans Pro
- Lora + Inter
- Merriweather + Open Sans
- Fraunces + Work Sans

**Sans-serif heading + Serif body** (editorial feel):
- Montserrat + Lora
- Poppins + Merriweather
- DM Sans + Charter

**Display heading + Clean body** (strong personality):
- Space Grotesk + Inter
- Cabinet Grotesk + Söhne
- Clash Display + Satoshi

**Monospace accent + Sans-serif body** (technical/developer):
- JetBrains Mono + Inter
- Fira Code + Source Sans Pro
- IBM Plex Mono + IBM Plex Sans

### Font Loading Strategy

```css
/* Preload critical fonts */
<link rel="preload" href="/fonts/heading.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/body.woff2" as="font" type="font/woff2" crossorigin>

/* Font-face declarations with swap strategy */
@font-face {
  font-family: 'Heading';
  src: url('/fonts/heading.woff2') format('woff2');
  font-weight: 700;
  font-display: swap;
}

@font-face {
  font-family: 'Body';
  src: url('/fonts/body.woff2') format('woff2');
  font-weight: 400;
  font-display: swap;
}
```

## Reading Metrics

Optimized reading metrics reduce eye strain, increase comprehension, and keep users engaged with content.

### Line Length (Measure)

The optimal line length for body text is **45-75 characters** per line, with 65 characters as the ideal.

```css
/* Constrain reading width */
.prose {
  max-width: 65ch; /* ch unit = width of the '0' character */
}
```

Lines that are too long cause the eye to lose its place when returning to the start of the next line. Lines that are too short create excessive line breaks and a choppy reading rhythm.

### Line Height (Leading)

Line height depends on font size, line length, and typeface design:

| Font Size | Recommended Line Height | Ratio |
|-----------|------------------------|-------|
| 12-14px | 1.6-1.7 | Tighter for small text |
| 16-18px | 1.5-1.6 | Standard body text |
| 20-24px | 1.4-1.5 | Subheadings |
| 28-36px | 1.2-1.3 | Headings |
| 40px+ | 1.1-1.2 | Display text |

**The rule:** As font size increases, line height ratio decreases. Large text needs less leading because the letterforms are already clearly distinguished.

```css
:root {
  --leading-tight:   1.2;
  --leading-snug:    1.375;
  --leading-normal:  1.5;
  --leading-relaxed: 1.625;
  --leading-loose:   1.75;
}
```

### Letter Spacing (Tracking)

- **All-caps text:** Add 0.05-0.1em tracking. Uppercase letters are designed to follow lowercase letters, so they look cramped when set alone.
- **Large display text:** Tighten tracking slightly (-0.02em to -0.01em). Large type reveals gaps between letters that look natural at body sizes.
- **Body text:** Leave at default (0). The font designer has optimized letter spacing for the intended reading size.
- **Small text:** Slightly increase tracking (+0.01em to +0.02em) for legibility at small sizes.

```css
.uppercase-label {
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: var(--font-size-xs);
}

.display-heading {
  letter-spacing: -0.02em;
  font-size: var(--font-size-display);
}
```

### Paragraph Spacing

Use margin between paragraphs rather than first-line indent for screen reading:

```css
.prose p + p {
  margin-top: 1.5em; /* One line height of space between paragraphs */
}
```

## Responsive Typography Strategies

### Strategy 1: Fluid Only (Recommended)

Use `clamp()` for all sizes. No breakpoints needed for typography.

```css
body { font-size: clamp(1rem, 0.2vw + 0.93rem, 1.125rem); }
h1   { font-size: clamp(2.25rem, 2vw + 1.5rem, 3.815rem); }
h2   { font-size: clamp(1.875rem, 1.2vw + 1.4rem, 2.441rem); }
```

### Strategy 2: Scale Shift at Breakpoints

Use a different ratio for different screen sizes:

```css
:root {
  /* Mobile: Minor Third (1.200) */
  --font-size-base: 1rem;
  --font-size-lg: 1.2rem;
  --font-size-xl: 1.44rem;
  --font-size-2xl: 1.728rem;
  --font-size-3xl: 2.074rem;
}

@media (min-width: 768px) {
  :root {
    /* Desktop: Major Third (1.250) */
    --font-size-lg: 1.25rem;
    --font-size-xl: 1.5625rem;
    --font-size-2xl: 1.953rem;
    --font-size-3xl: 2.441rem;
  }
}
```

### Strategy 3: Base Size Shift

Change only the base size and let `rem` units handle the cascade:

```css
html {
  font-size: 14px;
}

@media (min-width: 768px) {
  html {
    font-size: 16px;
  }
}

@media (min-width: 1440px) {
  html {
    font-size: 18px;
  }
}
```

This approach is simple but creates less dramatic heading changes than a ratio shift.

## Deep Dive References

### [Type Scale Theory](references/type-scale-theory.md)

- Mathematical Foundations
- Ratio Comparison Table
- Historical Context
- Multi-Base Scales
- Practical Ratio Selection
- Implementation Patterns

### [Font Pairing Guide](references/font-pairing-guide.md)

- Typeface Classification System
- Pairing Principles
- Extended Pairing Examples
- Google Fonts Recommendations
- Testing Methodology

### [Reading Optimization](references/reading-optimization.md)

- Research-Backed Reading Metrics
- Accessibility Considerations
- Dark Mode Typography
- Dyslexia-Friendly Type
- Performance and Reading

## Next Steps

- **[Visual Design](../visual-design/SKILL.md)**: Apply typography within the broader visual design context
- **[Design Tokens](../design-tokens/SKILL.md)**: Encode typography decisions as design tokens
- **[Grid Layout Systems](../grid-layout-systems/SKILL.md)**: Align typography to grid structure
- **[Responsive Design](../responsive-design/SKILL.md)**: Typography within responsive layout strategy

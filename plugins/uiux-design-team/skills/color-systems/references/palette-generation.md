# Palette Generation

Comprehensive reference for algorithmically generating, scaling, and validating color palettes for production design systems.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Algorithmic Palette Generation](#algorithmic-palette-generation) | 14-50 | Systematic methods for deriving palettes from base colors |
| [Brand Color Extraction](#brand-color-extraction) | 52-80 | Deriving a full palette from a single brand color |
| [Scaling to 50-950 Range](#scaling-to-50-950-range) | 82-120 | Building a complete shade scale with perceptual uniformity |
| [Accessible Palette Construction](#accessible-palette-construction) | 122-150 | Ensuring every palette combination meets WCAG standards |
| [Tool Recommendations](#tool-recommendations) | 152-170 | Software and utilities for palette generation |
| [CSS Custom Properties Output](#css-custom-properties-output) | 172-195 | Production-ready CSS variable format |

## Algorithmic Palette Generation

### Hue Rotation Method

Start with a base hue and generate complementary colors through mathematical rotation:

**Complementary**: Rotate 180 degrees
```
Base hue: 220 (blue)
Complement: 220 + 180 = 40 (orange)
```

**Triadic**: Rotate 120 degrees
```
Base hue: 220 (blue)
Second: 220 + 120 = 340 (pink-red)
Third: 220 + 240 = 100 (yellow-green)
```

**Split-Complementary**: Rotate 150 and 210 degrees
```
Base hue: 220 (blue)
Split 1: 220 + 150 = 10 (red-orange)
Split 2: 220 + 210 = 70 (yellow)
```

**Analogous**: Rotate 30 degrees in each direction
```
Base hue: 220 (blue)
Neighbor 1: 220 - 30 = 190 (cyan)
Neighbor 2: 220 + 30 = 250 (purple-blue)
```

### Saturation-Based Generation

Generate neutral and accent variants by modifying saturation while keeping hue constant:

- **Full saturation** (80-100%): Brand colors, primary actions, status indicators
- **Medium saturation** (40-60%): Secondary elements, hover states, highlights
- **Low saturation** (10-25%): Backgrounds, borders, subtle tints
- **Zero saturation** (0%): Pure neutrals derived from the brand hue's lightness

### Lightness-Based Generation

Generate a complete tonal range by systematically adjusting lightness:

```
95% lightness → near-white tint (backgrounds)
85% lightness → light tint (hover backgrounds, highlights)
70% lightness → medium-light (secondary text, borders)
50% lightness → mid-tone (base brand color)
35% lightness → medium-dark (dark variant, hover states)
20% lightness → dark (headings, high-emphasis text)
10% lightness → near-black (maximum contrast)
```

## Brand Color Extraction

### From a Single Brand Color

Most brand guidelines provide a single primary color. Deriving a full system requires systematic expansion.

**Step 1: Decompose the brand color into HSL**
```
Brand blue: #2563eb
HSL: hsl(221, 83%, 53%)
```

**Step 2: Generate the primary scale** (adjust lightness, slight saturation curve)
- 50: hsl(221, 83%, 97%) — lightest tint
- 100: hsl(221, 80%, 93%)
- 200: hsl(221, 78%, 85%)
- 300: hsl(221, 75%, 73%)
- 400: hsl(221, 80%, 63%)
- 500: hsl(221, 83%, 53%) — brand color
- 600: hsl(221, 80%, 45%)
- 700: hsl(221, 75%, 37%)
- 800: hsl(221, 70%, 28%)
- 900: hsl(221, 65%, 20%)
- 950: hsl(221, 60%, 12%) — darkest shade

**Step 3: Generate neutral scale** using the brand hue at very low saturation
```
Neutral with brand undertone:
50:  hsl(221, 8%, 97%)
100: hsl(221, 7%, 93%)
200: hsl(221, 6%, 85%)
...
900: hsl(221, 4%, 12%)
```

This creates warm or cool neutrals that harmonize with the brand color rather than using pure grays.

**Step 4: Generate semantic colors**

Derive success, warning, error, and info colors that harmonize with the brand:
- **Success**: Rotate hue toward green (120), maintain similar saturation
- **Warning**: Rotate hue toward yellow (45), reduce saturation slightly
- **Error**: Rotate hue toward red (0), maintain or increase saturation
- **Info**: Use the brand primary, or a lighter tint

### From Multiple Brand Colors

When brand guidelines specify multiple colors:
1. Designate one as primary (used for main actions and brand identification)
2. Designate others as secondary or accent
3. Generate scales for each independently
4. Verify that scales do not produce confusingly similar shades at any level (e.g., primary-300 should not look like secondary-400)

## Scaling to 50-950 Range

### The Standard Scale

The 50-950 naming convention (popularized by Tailwind CSS) provides 11 steps from near-white to near-black:

| Step | Lightness (OKLCH L) | Usage |
|------|---------------------|-------|
| 50 | 0.95-0.97 | Lightest background tint |
| 100 | 0.90-0.93 | Light background, hover state of 50 |
| 200 | 0.83-0.87 | Borders on light backgrounds, tags |
| 300 | 0.73-0.78 | Disabled text on light backgrounds |
| 400 | 0.63-0.68 | Placeholder text, secondary icons |
| 500 | 0.53-0.58 | Base brand color, primary icons |
| 600 | 0.45-0.48 | Hover state of 500, text on light backgrounds |
| 700 | 0.37-0.40 | Active/pressed state, heading text |
| 800 | 0.28-0.32 | High-emphasis text |
| 900 | 0.20-0.24 | Maximum contrast text |
| 950 | 0.12-0.18 | Near-black, dark mode backgrounds |

### Lightness Steps

Ensure perceptual uniformity by using OKLCH or LAB lightness. In OKLCH, distribute lightness values with roughly equal perceived intervals:

```
Step differences (OKLCH L):
50→100:  ~0.04
100→200: ~0.06
200→300: ~0.09
300→400: ~0.10
400→500: ~0.10
500→600: ~0.10
600→700: ~0.08
700→800: ~0.08
800→900: ~0.08
900→950: ~0.06
```

The steps are slightly larger in the middle range (where the eye is most sensitive to differences) and slightly smaller at the extremes.

### Chroma Curve

Chroma (saturation) should not remain constant across the scale. It should peak at the base color and taper toward both extremes:

```
50:  low chroma (nearly white — minimal color)
100: low chroma
200: medium-low chroma
300: medium chroma (color becoming noticeable)
400: medium-high chroma
500: peak chroma (full brand color)
600: medium-high chroma (slightly less than 500)
700: medium chroma
800: medium-low chroma (color still present but darker)
900: low chroma (nearly achromatic dark)
950: very low chroma (near-black with hint of hue)
```

This natural chroma curve prevents near-white tints from looking gaudy and near-black shades from looking artificially saturated.

## Accessible Palette Construction

### Contrast Pair Matrix

For every palette, document which combinations meet WCAG AA and AAA:

```
Background  | Text Color | Contrast Ratio | AA Normal | AA Large | AAA Normal
------------|-----------|----------------|-----------|----------|----------
50          | 900       | 15.2:1         | PASS      | PASS     | PASS
50          | 700       | 8.1:1          | PASS      | PASS     | PASS
50          | 500       | 4.6:1          | PASS      | PASS     | FAIL
100         | 900       | 13.8:1         | PASS      | PASS     | PASS
200         | 900       | 11.2:1         | PASS      | PASS     | PASS
900         | 50        | 15.2:1         | PASS      | PASS     | PASS
900         | 200       | 11.2:1         | PASS      | PASS     | PASS
900         | 400       | 5.8:1          | PASS      | PASS     | FAIL
```

### Accessible Combinations for Common Patterns

**Light mode (white/near-white background)**:
- Body text: use 800 or 900 (high contrast)
- Secondary text: use 600 or 700 (must still meet 4.5:1)
- Disabled text: use 400 (note: disabled elements are exempt from WCAG but should still be legible)
- Borders: use 200 or 300 (non-text 3:1 requirement)

**Dark mode (900/950 background)**:
- Body text: use 100 or 200 (high contrast)
- Secondary text: use 300 or 400 (must still meet 4.5:1)
- Borders: use 700 or 800 (non-text 3:1 requirement)

### Cross-Palette Accessibility

When combining colors from different palettes (e.g., white text on a success-green button):
- Verify contrast for each semantic color at the shades used for interactive elements
- Common issue: green and orange at 500 often fail with white text (insufficient contrast). Use 600 or 700 instead.
- Store accessible text-on-color pairings as tokens: `--color-on-success: #ffffff` (only if success-600+ is the background)

## Tool Recommendations

### Design Tools
- **Figma Plugins**: "Contrast" for real-time checking, "Color Palette" for generation
- **Adobe Color**: Web-based color wheel with harmony rules and accessibility checker
- **Coolors**: Quick palette generator with contrast checking and export options
- **Huemint**: AI-powered palette generator that shows colors in context

### Developer Tools
- **OKLCH Color Picker** (oklch.com): OKLCH-based color picker designed for shade scale generation
- **Contrast Checker** (webaim.org/resources/contrastchecker): Simple, reliable WCAG contrast checker
- **Who Can Use** (whocanuse.com): Shows how color combinations appear to people with different vision types
- **Color Review** (color.review): Interactive tool showing contrast ratios as you adjust colors

### Programmatic Tools
- **chroma.js**: JavaScript library for color manipulation, scale generation, and color space conversion
- **culori**: Modern JavaScript color library with OKLCH support
- **polished**: CSS-in-JS utility with color functions (lighten, darken, saturate)

## CSS Custom Properties Output

### Production Format

```css
:root {
  /* Primary palette */
  --color-primary-50:  oklch(0.97 0.02 250);
  --color-primary-100: oklch(0.93 0.04 250);
  --color-primary-200: oklch(0.87 0.08 250);
  --color-primary-300: oklch(0.78 0.12 250);
  --color-primary-400: oklch(0.68 0.16 250);
  --color-primary-500: oklch(0.58 0.19 250);
  --color-primary-600: oklch(0.48 0.18 250);
  --color-primary-700: oklch(0.40 0.15 250);
  --color-primary-800: oklch(0.32 0.12 250);
  --color-primary-900: oklch(0.24 0.08 250);
  --color-primary-950: oklch(0.18 0.05 250);

  /* Semantic aliases */
  --color-primary: var(--color-primary-500);
  --color-primary-hover: var(--color-primary-600);
  --color-primary-active: var(--color-primary-700);
  --color-primary-bg: var(--color-primary-50);
  --color-primary-border: var(--color-primary-200);
  --color-on-primary: #ffffff;
}
```

### Fallback Pattern for OKLCH

```css
:root {
  /* Fallback for browsers without OKLCH support */
  --color-primary-500: #3b82f6;
  --color-primary-600: #2563eb;
}

@supports (color: oklch(0.5 0.1 250)) {
  :root {
    --color-primary-500: oklch(0.58 0.19 250);
    --color-primary-600: oklch(0.48 0.18 250);
  }
}
```

## See Also

- [[color-theory.md]] - Color science foundations for understanding palette relationships
- [[contrast-requirements.md]] - WCAG standards that validate palette accessibility
- [[../../visual-design/references/brand-alignment.md]] - Brand-driven palette requirements
- [[../../visual-design/references/aesthetic-principles.md]] - Aesthetic tone influences palette character

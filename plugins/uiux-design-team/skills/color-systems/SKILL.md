---
name: color-systems
description: Design accessible color palettes using color theory fundamentals, systematic palette generation methods, WCAG contrast compliance, semantic token architecture, and robust dark mode strategies with CSS custom properties.
metadata:
   references:
   - references/color-theory.md
   - references/contrast-requirements.md
   - references/palette-generation.md
---

# Color Systems

Color is the most immediately impactful visual design tool. A well-constructed color system ensures consistency, accessibility, and emotional resonance across every screen and component.

## Color Theory Fundamentals

### The Color Wheel

The color wheel organizes hues in a circle based on their relationships:
- **Primary colors**: Red, blue, yellow (traditional) or red, green, blue (light/additive)
- **Secondary colors**: Created by mixing two primaries (orange, green, purple)
- **Tertiary colors**: Created by mixing a primary and adjacent secondary (red-orange, blue-green, etc.)

### HSL Model

HSL (Hue, Saturation, Lightness) is the most intuitive model for designing color systems:
- **Hue** (0-360): Position on the color wheel. 0=red, 120=green, 240=blue.
- **Saturation** (0-100%): Color intensity. 0%=gray, 100%=full color. Reduce saturation for neutral, professional palettes; increase for vibrant, energetic ones.
- **Lightness** (0-100%): How light or dark. 0%=black, 50%=pure color, 100%=white. This axis is the primary tool for generating shade/tint scales.

### Warm vs. Cool Colors

- **Warm colors** (red, orange, yellow): Advance toward the viewer, create energy, urgency, and intimacy. Use for CTAs, alerts, and attention-grabbing elements.
- **Cool colors** (blue, green, purple): Recede from the viewer, create calm, trust, and space. Use for backgrounds, information-dense areas, and institutional contexts.
- **Neutral colors** (gray, beige, slate): Provide visual rest and let accent colors stand out. The backbone of any color system.

## Palette Generation Methods

### Complementary

Two colors directly opposite on the color wheel (e.g., blue and orange). Creates maximum contrast and visual tension. Best for: high-energy interfaces, CTAs that need to pop against backgrounds.

### Analogous

Three colors adjacent on the color wheel (e.g., blue, blue-green, green). Creates harmony and visual comfort. Best for: cohesive, calming interfaces, nature and wellness brands.

### Triadic

Three colors equally spaced on the color wheel (e.g., red, blue, yellow). Creates vibrant, balanced diversity. Best for: playful interfaces, children's products, creative platforms. Use one dominant, two as accents.

### Split-Complementary

One base color plus the two colors adjacent to its complement (e.g., blue + yellow-orange + red-orange). Creates contrast with less tension than pure complementary. Best for: balanced interfaces that need variety without clashing.

### Tetradic (Double Complementary)

Four colors forming a rectangle on the color wheel. Creates rich, diverse palettes. Best for: complex dashboards, data visualization where multiple distinct categories need differentiation. Hardest to balance; designate one dominant.

## WCAG Contrast Requirements

Accessibility is non-negotiable. Every text element must meet minimum contrast ratios.

### WCAG 2.2 Standards

| Level | Normal Text (< 18pt) | Large Text (>= 18pt or >= 14pt bold) |
|-------|----------------------|---------------------------------------|
| **AA** | 4.5:1 minimum | 3:1 minimum |
| **AAA** | 7:1 minimum | 4.5:1 minimum |

### Non-Text Contrast

UI components and graphical objects require **3:1 minimum** contrast against adjacent colors:
- Form field borders against their background
- Button backgrounds against the page background
- Icon fills against their container background
- Focus indicators against the focused element

### Common Failures and Fixes

- **Light gray text on white**: #999 on #fff = 2.85:1 (FAIL). Fix: darken to at least #767676 for 4.54:1.
- **Colored text on colored background**: Blue (#3b82f6) on dark blue (#1e3a5f) may look distinct but fail mathematically. Always verify with a contrast checker.
- **Placeholder text**: Often styled at very low contrast. Ensure placeholder text meets at least 4.5:1 or provide visible labels.
- **Transparent overlays**: Text over images with a semi-transparent overlay can fail in regions where the image is light. Use a solid-enough overlay or a text-shadow fallback.

## Semantic Color Tokens

Abstract colors from specific values to semantic meanings. This enables theming, dark mode, and consistent color usage.

### Token Architecture

```css
/* Primitive tokens — raw color values */
--color-blue-500: #3b82f6;
--color-blue-600: #2563eb;
--color-red-500: #ef4444;
--color-green-500: #22c55e;
--color-yellow-500: #eab308;
--color-gray-50: #f9fafb;
--color-gray-900: #111827;

/* Semantic tokens — meaning-based aliases */
--color-primary: var(--color-blue-600);
--color-primary-hover: var(--color-blue-500);
--color-secondary: var(--color-gray-900);
--color-success: var(--color-green-500);
--color-warning: var(--color-yellow-500);
--color-error: var(--color-red-500);
--color-info: var(--color-blue-500);

/* Surface tokens — background and text */
--color-surface: var(--color-gray-50);
--color-surface-elevated: #ffffff;
--color-on-surface: var(--color-gray-900);
--color-on-surface-muted: #6b7280;
--color-on-primary: #ffffff;

/* Border tokens */
--color-border: #e5e7eb;
--color-border-focus: var(--color-primary);
```

### Naming Convention

Follow a three-tier naming hierarchy:
1. **Primitive**: `--color-{hue}-{shade}` (color-blue-500)
2. **Semantic**: `--color-{role}` (color-primary, color-error)
3. **Component**: `--button-bg`, `--card-border` (component-specific, references semantic tokens)

## Dark Mode Strategy

Dark mode is not "invert all the colors." It requires a deliberate, separate design pass.

### Key Principles

- **Reduce contrast, do not invert it**: Pure white (#fff) on pure black (#000) is harsher than dark-on-light. Use off-white (#e5e7eb) on dark gray (#1f2937).
- **Elevate with lightness, not shadow**: In light mode, depth is shown with shadows. In dark mode, elevated surfaces are slightly lighter than the base surface.
- **Desaturate colors slightly**: Fully saturated colors on dark backgrounds create visual vibration. Reduce saturation by 10-20% for dark mode variants.
- **Maintain semantic meaning**: Error is still red, success still green. Adjust lightness and saturation, not hue.

### CSS Custom Properties Pattern

```css
:root {
  --color-surface: #ffffff;
  --color-surface-elevated: #ffffff;
  --color-on-surface: #111827;
  --color-on-surface-muted: #6b7280;
  --color-border: #e5e7eb;
  --color-primary: #2563eb;
  --shadow-elevation-1: 0 1px 3px rgba(0,0,0,0.12);
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-surface: #111827;
    --color-surface-elevated: #1f2937;
    --color-on-surface: #e5e7eb;
    --color-on-surface-muted: #9ca3af;
    --color-border: #374151;
    --color-primary: #60a5fa;
    --shadow-elevation-1: 0 1px 3px rgba(0,0,0,0.4);
  }
}
```

### Dark Mode Testing Checklist

- [ ] All text meets WCAG AA contrast ratios against dark surfaces
- [ ] Semantic colors (success, error, warning) remain distinguishable
- [ ] Images and illustrations do not clash with dark backgrounds
- [ ] Borders remain visible but not harsh
- [ ] Elevated surfaces are perceptibly lighter than the base surface
- [ ] Focus indicators remain visible
- [ ] Shadows are intensified to remain visible on dark backgrounds

## Deep Dive References

### [Color Theory](references/color-theory.md)

- Color Models
- Perceptual Color Spaces
- Color Psychology
- Cultural Color Considerations
- Color Temperature

### [Palette Generation](references/palette-generation.md)

- Algorithmic Palette Generation
- Brand Color Extraction
- Scaling to 50-950 Range
- Accessible Palette Construction
- Tool Recommendations
- CSS Custom Properties Output

### [Contrast Requirements](references/contrast-requirements.md)

- WCAG 2.2 Contrast Ratios
- Testing Methodologies
- Common Failures
- Non-Text Contrast
- Large Text Definition

## Next Steps

- **[Visual Design](../visual-design/SKILL.md)**: Apply color systems within a broader aesthetic framework
- **[Typography Systems](../typography-systems/SKILL.md)**: Ensure text colors work with the typographic system
- **[Motion Design](../motion-design/SKILL.md)**: Color transitions and animated color states
- **[Grid Layout Systems](../grid-layout-systems/SKILL.md)**: Surface colors that define layout zones

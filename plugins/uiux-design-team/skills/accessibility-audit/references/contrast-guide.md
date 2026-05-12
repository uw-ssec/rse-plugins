# Contrast Guide

Comprehensive reference for color contrast accessibility. Covers WCAG contrast ratio requirements, testing tools, common contrast failures, non-text contrast for UI components, and practical patterns for fixing low-contrast designs.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Contrast Ratio Requirements](#contrast-ratio-requirements) | 14-50 | AA and AAA ratios for text, large text, and UI components |
| [Testing Tools](#testing-tools) | 52-85 | Browser extensions, DevTools, design tools, and CI integration |
| [Common Contrast Failures](#common-contrast-failures) | 87-130 | The most frequent violations and their visual impact |
| [Non-Text Contrast](#non-text-contrast) | 132-165 | 3:1 requirement for UI components and graphical objects |
| [Fixing Low-Contrast Patterns](#fixing-low-contrast-patterns) | 167-210 | Practical solutions for common design situations |
| [Contrast in Theming](#contrast-in-theming) | 212-245 | Maintaining contrast across light, dark, and high-contrast themes |
| [See Also](#see-also) | 247-253 | Related references and skills |

## Contrast Ratio Requirements

### WCAG Levels

| Content Type | AA Minimum | AAA Enhanced |
|-------------|-----------|--------------|
| Normal text (< 18pt regular, < 14pt bold) | 4.5:1 | 7:1 |
| Large text (>= 18pt regular or >= 14pt bold) | 3:1 | 4.5:1 |
| UI components and graphical objects | 3:1 | Not defined |
| Inactive components | No requirement | No requirement |
| Decorative elements | No requirement | No requirement |
| Logotypes | No requirement | No requirement |

### What Counts as Large Text

Large text is defined as 18pt (24px) at regular weight, or 14pt (approximately 18.66px) at bold weight. This threshold exists because larger text is inherently easier to read at lower contrast.

### Understanding the Ratio

The contrast ratio is calculated as `(L1 + 0.05) / (L2 + 0.05)` where L1 is the relative luminance of the lighter color and L2 is the relative luminance of the darker color.

- **1:1** -- No contrast (same color)
- **3:1** -- Minimum for large text and UI components
- **4.5:1** -- Minimum for normal text (AA)
- **7:1** -- Enhanced contrast for normal text (AAA)
- **21:1** -- Maximum contrast (black on white)

### Practical Contrast Values

| Foreground | Background | Ratio | Meets |
|-----------|-----------|-------|-------|
| `#000000` (black) | `#ffffff` (white) | 21:1 | AAA |
| `#333333` (dark gray) | `#ffffff` (white) | 12.6:1 | AAA |
| `#595959` (medium gray) | `#ffffff` (white) | 7:1 | AAA |
| `#767676` (gray) | `#ffffff` (white) | 4.5:1 | AA |
| `#949494` (light gray) | `#ffffff` (white) | 2.8:1 | Fails AA |
| `#ffffff` (white) | `#3b82f6` (blue-500) | 4.6:1 | AA |
| `#ffffff` (white) | `#2563eb` (blue-600) | 5.7:1 | AA |

## Testing Tools

### Browser Extensions

**axe DevTools** -- Comprehensive accessibility scanner that flags contrast violations with exact ratios and suggested fixes. Available for Chrome, Firefox, and Edge.

**WAVE** -- Visual overlay that highlights contrast issues directly on the page. Shows the exact contrast ratio for each text element.

**Lighthouse** -- Built into Chrome DevTools (Audits tab). Includes contrast checking as part of the accessibility score.

### Browser DevTools

Chrome DevTools color picker shows the contrast ratio against the background color for any selected text element. Look for the contrast section when inspecting a color value.

Firefox Accessibility Inspector includes a contrast checker that flags all elements below the required ratio.

### Design Tool Integration

**Figma**: Use the Stark plugin or the built-in contrast checker in the color picker. Check contrast during design, not after handoff.

**Sketch**: Stark plugin provides contrast checking within the design tool.

### Command-Line and CI Tools

**pa11y** -- Runs accessibility tests including contrast from the command line. Integrates into CI pipelines.

```bash
pa11y https://your-site.com --standard WCAG2AA
```

**axe-core** -- Programmatic accessibility testing library. Use in unit tests, integration tests, or as a CI step.

```js
const { AxePuppeteer } = require('@axe-core/puppeteer');
const results = await new AxePuppeteer(page).analyze();
const contrastViolations = results.violations.filter(v => v.id === 'color-contrast');
```

### Manual Checking

**WebAIM Contrast Checker** (webaim.org/resources/contrastchecker) -- Enter foreground and background hex values, get the ratio and pass/fail status.

**Colour Contrast Analyser (CCA)** -- Desktop application (free) that includes an eyedropper tool for checking any on-screen colors.

## Common Contrast Failures

### 1. Placeholder Text

Placeholder text in form fields is almost always below 4.5:1 contrast. Default browser placeholder color (`#a0a0a0` on white) fails.

**Fix**: Do not rely on placeholder text for essential information. If used, increase placeholder contrast or use a visible label that meets contrast requirements.

### 2. Disabled State Text

Disabled elements are exempt from contrast requirements, but text should still be legible enough for users to understand what the disabled option is.

**Recommendation**: Target at least 3:1 for disabled text, even though it is not required.

### 3. Text on Images

Text overlaid on photographs or gradients has variable contrast depending on the underlying image content. A white heading on a sunset image may pass in some areas and fail in others.

**Fix**: Add a semi-transparent overlay or text shadow behind the text. Alternatively, place text in a solid-background container over the image.

```css
.hero-text {
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  /* Or use a scrim: */
  background: linear-gradient(rgba(0,0,0,0), rgba(0,0,0,0.6));
}
```

### 4. Brand Colors on White

Brand accent colors (especially yellows, light greens, and light blues) often fail contrast when used as text color on white backgrounds.

**Fix**: Reserve low-contrast brand colors for large decorative elements. Use darker shades for text. For example, use `brand-700` instead of `brand-500` for text on white.

### 5. Links Within Text

Links that are the same color as surrounding text but distinguished only by underline still need 3:1 contrast against the surrounding text color (not just against the background).

**Fix**: Ensure links have either an underline or 3:1 contrast difference from surrounding text.

### 6. Focus Indicators

Focus rings that do not contrast against both the element and the surrounding background fail the non-text contrast requirement.

**Fix**: Use a focus ring color that contrasts 3:1 against adjacent background colors. Test on all background variations.

## Non-Text Contrast

WCAG 1.4.11 requires a 3:1 contrast ratio for UI components and graphical objects that are necessary for understanding content.

### What It Applies To

- Form control borders (input, select, checkbox outlines)
- Icon-only buttons (the icon must contrast against its background)
- Custom focus indicators
- Charts, graphs, and data visualizations
- State indicators (toggle switches, radio buttons)
- Interactive component boundaries

### What It Does Not Apply To

- Inactive/disabled components
- Components whose appearance is determined by the browser (native checkboxes, radio buttons)
- Purely decorative graphics

### Common Non-Text Failures

| Element | Failure | Fix |
|---------|---------|-----|
| Input borders | Light gray (`#d1d5db`) on white | Use `#6b7280` or darker for 3:1 |
| Checkbox borders | `#9ca3af` on white (2.7:1) | Darken to `#6b7280` (4.6:1) |
| Icon buttons | `#9ca3af` icon on white | Use `#4b5563` or darker |
| Chart segments | Light colors adjacent to each other | Ensure each segment borders contrast with adjacent segments |
| Toggle switches | Gray track on white | Add border or darken the track |

### Testing Non-Text Contrast

Use a color contrast checker to test the colors at the boundary of each UI component against its adjacent background. For example, measure the input border color against the page background, not the input background.

## Fixing Low-Contrast Patterns

### Strategy 1: Darken the Foreground

The simplest fix. Shift the text or element color to a darker shade in the same hue family.

| Original | Fixed | Ratio Change |
|----------|-------|-------------|
| `#9ca3af` on white (2.9:1) | `#6b7280` on white (4.6:1) | +1.7 |
| `#3b82f6` on white (3.1:1) | `#2563eb` on white (4.6:1) | +1.5 |
| `#10b981` on white (2.8:1) | `#047857` on white (5.9:1) | +3.1 |

### Strategy 2: Add a Background

When you cannot change the foreground color (brand requirements), add a background that provides contrast:

```css
.tag-success {
  /* Green text on white fails at 2.8:1 */
  /* Solution: green text on light green background */
  color: #047857;        /* green-700 */
  background: #d1fae5;   /* green-100 */
  /* Ratio: 4.9:1 -- passes AA */
}
```

### Strategy 3: Increase Font Size or Weight

If the text is large (18pt+ regular or 14pt+ bold), the required ratio drops to 3:1. Making text larger or bolder is a legitimate contrast solution for near-miss ratios.

### Strategy 4: Add Non-Color Indicators

When color alone carries meaning (error states, status indicators), add text labels, icons, or patterns so the information is conveyed even without the color:

```html
<!-- Color + icon + text: robust against contrast issues -->
<span class="status status--error">
  <svg class="status-icon" aria-hidden="true"><!-- X icon --></svg>
  Error: Payment declined
</span>
```

## Contrast in Theming

### Light Mode Considerations

- Text colors should be `gray-900` to `gray-700` for maximum readability
- Secondary text can go as light as `gray-600` on white (4.5:1)
- Link colors need 4.5:1 on white AND 3:1 against surrounding body text
- Background surfaces (`gray-50`, `gray-100`) reduce available contrast for text

### Dark Mode Considerations

- Text colors should be `gray-100` to `gray-300` for readability
- Pure white text on pure black (`#ffffff` on `#000000`) creates halation (blurring) for some users; use slightly off-white (`#e2e8f0`) on dark gray (`#1a1a2e`)
- Surface colors (`gray-800`, `gray-900`) have less luminance range than light mode, making contrast harder to achieve
- Links and interactive elements may need different colors in dark mode to maintain contrast

### High-Contrast Mode

Provide a high-contrast theme using the `forced-colors` media query for users who enable Windows High Contrast or similar OS settings:

```css
@media (forced-colors: active) {
  .button {
    border: 2px solid ButtonText;
  }
  .focus-ring {
    outline: 2px solid Highlight;
  }
}
```

### Automated Contrast Testing Across Themes

Test contrast in every theme variation. A color that passes in light mode may fail in dark mode. Include contrast checks in your CI pipeline for all supported themes.

## See Also

- [[wcag-checklist.md]] -- WCAG 1.4.3 and 1.4.11 criteria in the full compliance checklist
- [[inclusive-design.md]] -- Designing for low vision and color vision deficiency beyond contrast ratios
- [[keyboard-nav-guide.md]] -- Focus indicator contrast requirements
- [[../../color-systems/references/contrast-requirements.md]] -- Building color systems with contrast baked in
- [[../../design-tokens/references/token-taxonomy.md]] -- Color tokens organized for contrast compliance
- [[../../design-system-creation/references/theming-patterns.md]] -- Theme switching with contrast preservation

**Back to:** [Accessibility Audit Skill](../SKILL.md)

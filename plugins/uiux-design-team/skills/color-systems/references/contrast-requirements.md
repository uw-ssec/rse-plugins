# Contrast Requirements

Detailed reference on WCAG 2.2 contrast standards, testing methodologies, common accessibility failures, and remediation strategies for color contrast in web interfaces.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [WCAG 2.2 Contrast Ratios](#wcag-22-contrast-ratios) | 14-45 | Complete standard with examples and calculations |
| [Testing Methodologies](#testing-methodologies) | 47-80 | Tools, automated checks, and manual verification processes |
| [Common Failures](#common-failures) | 82-130 | Frequent contrast problems with before/after fixes |
| [Non-Text Contrast](#non-text-contrast) | 132-155 | UI component and graphical object requirements |
| [Large Text Definition](#large-text-definition) | 157-170 | What qualifies as large text and why it matters |

## WCAG 2.2 Contrast Ratios

### The Standard

WCAG (Web Content Accessibility Guidelines) defines minimum contrast ratios between foreground and background colors. Contrast ratio is calculated as (L1 + 0.05) / (L2 + 0.05) where L1 is the relative luminance of the lighter color and L2 is the relative luminance of the darker.

The ratio ranges from 1:1 (no contrast, identical colors) to 21:1 (maximum contrast, black on white).

### Level AA Requirements

Level AA is the minimum standard for legal compliance in most jurisdictions and the baseline for any professional web project.

| Element Type | Minimum Ratio | Example Pass | Example Fail |
|-------------|--------------|--------------|--------------|
| Normal text (< 18pt / < 14pt bold) | **4.5:1** | #595959 on #ffffff (7.0:1) | #999999 on #ffffff (2.85:1) |
| Large text (>= 18pt / >= 14pt bold) | **3:1** | #767676 on #ffffff (4.54:1) | #aaaaaa on #ffffff (2.32:1) |
| UI components and graphical objects | **3:1** | #767676 border on #ffffff (4.54:1) | #cccccc border on #ffffff (1.6:1) |

### Level AAA Requirements

Level AAA represents enhanced accessibility. While not legally required in most contexts, AAA compliance benefits users with low vision, aging eyes, or poor display conditions (bright sunlight, cheap monitors).

| Element Type | Minimum Ratio | Example Pass | Example Fail |
|-------------|--------------|--------------|--------------|
| Normal text | **7:1** | #333333 on #ffffff (12.63:1) | #666666 on #ffffff (5.74:1) |
| Large text | **4.5:1** | #595959 on #ffffff (7.0:1) | #808080 on #ffffff (3.95:1) |

### Calculating Contrast Ratios

Relative luminance for each color is calculated from linear RGB values:

```
1. Convert sRGB to linear RGB:
   For each channel (R, G, B as 0-1):
   If value <= 0.03928: linear = value / 12.92
   Else: linear = ((value + 0.055) / 1.055) ^ 2.4

2. Calculate relative luminance:
   L = 0.2126 * R_linear + 0.7152 * G_linear + 0.0722 * B_linear

3. Calculate contrast ratio:
   Ratio = (L_lighter + 0.05) / (L_darker + 0.05)
```

In practice, always use a tool for this calculation rather than computing manually. The formula is important to understand but error-prone to implement ad hoc.

## Testing Methodologies

### Automated Tools

**Browser Extensions**:
- **axe DevTools**: Comprehensive accessibility scanner that flags contrast failures with specific elements and fix suggestions
- **WAVE**: Visual overlay showing contrast errors directly on the page
- **Lighthouse**: Google's built-in audit tool includes contrast checking in its accessibility score

**CLI and CI/CD Integration**:
- **axe-core**: Programmatic accessibility testing library; integrable into test suites
- **pa11y**: CLI tool for automated accessibility testing; supports CI/CD pipelines
- **jest-axe**: Jest matcher for accessibility assertions in component tests

```javascript
// Example: jest-axe integration
import { axe, toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);

test('component has no accessibility violations', async () => {
  const { container } = render(<MyComponent />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### Manual Verification

Automated tools catch approximately 30-50% of accessibility issues. Manual checking is essential for:

**Dynamic contrast**: Elements whose color changes on hover, focus, or based on state. Automated scans test only the initial render state. Manually verify:
- Hover states maintain contrast
- Focus indicators are visible against both light and dark backgrounds
- Active/pressed states remain readable
- Disabled states, while exempt from WCAG, are still legible

**Overlaid text**: Text positioned over images, gradients, or video. Automated tools often cannot evaluate these accurately. Test by:
- Checking the worst-case scenario (lightest possible image behind dark text, or darkest image behind light text)
- Ensuring text overlays have sufficient background treatment (solid overlay, gradient overlay, text-shadow, or background-color on the text element)

**Transparent and semi-transparent elements**: Glassmorphism effects, transparent cards, and backdrop-filter elements create contrast that depends on what is behind them. Test across all possible background variations.

### Design-Time Checking

Integrate contrast checking into the design process, not just the QA process:

- **Figma plugins**: "Stark" and "A11y - Color Contrast Checker" provide real-time contrast checking in design files
- **Design tokens**: Define accessible-by-default text/background pairings in the token system
- **Palette documentation**: For every palette, pre-compute which combinations pass AA and AAA (see palette-generation.md for the contrast pair matrix)

## Common Failures

### Failure 1: Light Gray Text on White

**The problem**: Using light gray (#999, #aaa, #bbb) for "secondary" or "muted" text on white backgrounds.

```
#999999 on #ffffff = 2.85:1 (FAIL AA)
#aaaaaa on #ffffff = 2.32:1 (FAIL AA)
#bbbbbb on #ffffff = 1.87:1 (FAIL AA)
```

**The fix**: The lightest gray that passes AA normal text on white is **#767676** (4.54:1). For a more comfortable reading experience, use **#595959** (7.0:1, passes AAA).

```css
/* Before (fails) */
.muted-text { color: #999999; }

/* After (passes AA) */
.muted-text { color: #767676; }

/* After (passes AAA) */
.muted-text { color: #595959; }
```

### Failure 2: Colored Text on Colored Backgrounds

**The problem**: Using brand colors for both text and background without verifying contrast. Blue text on a light blue background, green text on a green-tinted surface, etc.

```
#3b82f6 (blue) on #dbeafe (light blue) = 3.12:1 (FAIL AA normal)
#22c55e (green) on #dcfce7 (light green) = 2.41:1 (FAIL AA)
```

**The fix**: Use darker shades of the text color or lighter shades of the background. Check the specific combination.

```css
/* Before (fails) */
.info-text { color: #3b82f6; background: #dbeafe; }

/* After (passes) — darker text */
.info-text { color: #1d4ed8; background: #dbeafe; } /* 5.96:1 */
```

### Failure 3: Placeholder Text

**The problem**: Placeholder text in input fields styled at very low contrast, following the browser's default light gray.

**The fix**: Style placeholder text to meet at least 4.5:1 contrast. If the visual hierarchy concern is that placeholder text should look "lighter" than user input, use a slightly lighter shade that still passes:

```css
::placeholder {
  color: #6b7280; /* meets 4.5:1 on white */
  opacity: 1; /* override browser default opacity */
}
```

### Failure 4: Text Over Images

**The problem**: White text overlaid on photographs without a background treatment. The text may be readable over dark image regions but illegible over light regions.

**The fix options**:
1. **Solid overlay**: `background: rgba(0, 0, 0, 0.55)` over the image, text on top
2. **Gradient overlay**: Linear gradient from transparent to `rgba(0,0,0,0.7)` at the text position
3. **Text background**: `background-color: rgba(0, 0, 0, 0.6); padding: 4px 8px;` on the text element itself
4. **Text shadow**: `text-shadow: 0 1px 3px rgba(0, 0, 0, 0.8);` (less reliable but useful as a supplement)

### Failure 5: Focus Indicators

**The problem**: Custom focus styles that are too subtle or that conflict with the element's background color.

```css
/* Fails when button is on a blue background */
:focus { outline: 2px solid #3b82f6; }
```

**The fix**: Use a focus indicator that works on both light and dark backgrounds. Double-ring outlines (one dark, one light) ensure visibility everywhere:

```css
:focus-visible {
  outline: 2px solid #1d4ed8;
  outline-offset: 2px;
  box-shadow: 0 0 0 4px #ffffff, 0 0 0 6px #1d4ed8;
}
```

### Failure 6: Status Colors Without Text

**The problem**: Using only color to convey status (green dot for online, red dot for error) without any text label or icon differentiation. This fails for colorblind users.

**The fix**: Always pair color with a secondary indicator:
- Color + icon (green checkmark, red X, yellow triangle)
- Color + text label ("Active", "Error", "Warning")
- Color + pattern/shape (filled circle for active, empty circle for inactive)

## Non-Text Contrast

### Requirement

WCAG 2.2 Success Criterion 1.4.11 requires **3:1 minimum contrast** for:

**UI Components**: Visual information needed to identify interactive elements:
- Input field borders (against the page background)
- Button boundaries (fill or border against the page background)
- Checkbox and radio button outlines
- Toggle switch tracks and thumbs
- Slider tracks and handles
- Tab indicators

**Graphical Objects**: Parts of graphics required to understand the content:
- Chart lines, bars, and data points
- Icon fills when the icon conveys meaning (not purely decorative)
- Infographic elements
- Status indicators (dots, badges)

### Common Non-Text Failures

```
#e5e7eb border on #ffffff = 1.3:1 (FAIL — border invisible)
#d1d5db border on #ffffff = 1.5:1 (FAIL — still too light)
#9ca3af border on #ffffff = 2.6:1 (FAIL — close but not enough)
#6b7280 border on #ffffff = 4.6:1 (PASS)
```

For input fields, the minimum visible border color on a white background is approximately **#949494** (3.03:1). However, many modern designs use background color change or shadow instead of borders. These alternative visual treatments must also meet 3:1 contrast against the page background.

## Large Text Definition

### What Qualifies as Large Text

WCAG defines large text as:
- **18pt (24px) or larger** at normal weight
- **14pt (18.66px, round to 19px) or larger** at bold weight (700+)

Large text benefits from relaxed contrast requirements (3:1 AA instead of 4.5:1) because larger characters are inherently more legible.

### Points vs. Pixels

The WCAG standard uses points (pt), but web development uses pixels (px). The conversion depends on resolution, but the standard assumes 96 DPI:
- 1pt = 1.333px
- 14pt = 18.66px (round up to 19px for implementation)
- 18pt = 24px

### Practical Application

For design systems, define thresholds in the type scale:
```css
/* These sizes qualify as "large text" at normal weight */
--font-size-lg: 1.5rem;    /* 24px — large text threshold */
--font-size-xl: 1.875rem;  /* 30px */
--font-size-2xl: 2.25rem;  /* 36px */

/* These sizes qualify as "large text" at bold weight */
--font-size-md-bold: 1.1875rem; /* 19px bold — large text threshold */
```

Headings typically qualify as large text. Body text, labels, and UI element text typically do not. Design the contrast system to meet normal-text requirements (4.5:1) by default, with the large-text relaxation available only for verified large elements.

## See Also

- [[color-theory.md]] - Color science underlying contrast perception
- [[palette-generation.md]] - Building palettes that meet contrast requirements by design
- [[../../visual-design/references/visual-hierarchy.md]] - How contrast drives visual hierarchy
- [[../../visual-design/references/aesthetic-principles.md]] - Balancing aesthetics with accessibility requirements

## Dark Mode Testing Checklist (Moved from SKILL.md)

- [ ] All text meets WCAG AA against dark surfaces
- [ ] Semantic colors (success/error/warning) remain distinguishable
- [ ] Images/illustrations don't clash with dark backgrounds
- [ ] Borders visible but not harsh
- [ ] Elevated surfaces perceptibly lighter than base
- [ ] Focus indicators visible
- [ ] Shadows intensified for dark backgrounds

## Common Failures (Moved from SKILL.md)

- Light gray on white: #999/#fff = 2.85:1 → darken to #767676 (4.54:1)
- Colored on colored: always verify mathematically, not visually
- Placeholders: must meet 4.5:1 or pair with visible labels
- Transparent overlays over images: use solid-enough overlay or text-shadow fallback

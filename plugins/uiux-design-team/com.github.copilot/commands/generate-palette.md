---
name: generate-palette
description: Accessible color palette generation with brand-tinted scales, semantic colors, WCAG AA contrast verification, and CSS custom property output.
user-invocable: true
allowed-tools: []
---

# Accessible Color Palette Generation

Generate a complete, WCAG-compliant color palette from one or more brand colors, led by @visual-designer and @accessibility-specialist. This command produces primary, neutral, and semantic color scales with verified contrast ratios and ready-to-use CSS custom properties.

## When to Use This Command

- Starting a new brand or product and need a color system
- Existing colors fail contrast checks and need to be fixed
- Building a dark mode palette alongside a light mode palette
- Creating a design system that requires verified accessible colors
- Consolidating an inconsistent set of colors into a systematic palette

## Workflow

### Step 1: Define Brand Color(s)

@visual-designer gathers the starting point for palette generation.

**Gather from the user:**
- What is your primary brand color? (hex, RGB, or HSL)
- Do you have secondary brand colors?
- Are there any colors that must be preserved exactly (logo colors, brand guidelines)?
- What is the visual tone? (Corporate, playful, minimal, bold, warm, cool)
- Do you need both light and dark mode palettes?

**If no brand color exists:**
- Ask about the product domain and emotional associations
- Suggest 2-3 starting hues with rationale
- Let the user choose before proceeding

### Step 2: Generate Primary Color Scale (50-950)

@visual-designer creates a full primary scale using the `color-systems` skill.

**Scale structure:**

| Step | Lightness | Typical Use |
|------|-----------|-------------|
| 50 | Very light | Subtle backgrounds, hover states on light surfaces |
| 100 | Light | Background tints, selected row backgrounds |
| 200 | Light-mid | Borders on colored elements, light decorative use |
| 300 | Mid-light | Decorative elements, secondary borders |
| 400 | Mid | Secondary interactive elements, icons |
| 500 | Mid (base) | Primary buttons, links, active states |
| 600 | Mid-dark | Primary button hover, dark mode text on colored bg |
| 700 | Dark | Pressed states, dark mode primary elements |
| 800 | Dark | High-contrast text on light backgrounds |
| 900 | Very dark | Headings on light backgrounds, dark surfaces |
| 950 | Darkest | Near-black with brand tint, dark mode backgrounds |

**Generation method:**
1. Start with the brand color as the 500 or 600 step
2. Increase lightness progressively toward 50 (maintaining hue and adjusting saturation)
3. Decrease lightness progressively toward 950 (maintaining hue, adjusting saturation to avoid muddiness)
4. Ensure perceptual uniformity: each step should feel like an equal visual jump

**Output format:**
```css
--color-primary-50:  #[hex];
--color-primary-100: #[hex];
--color-primary-200: #[hex];
--color-primary-300: #[hex];
--color-primary-400: #[hex];
--color-primary-500: #[hex];
--color-primary-600: #[hex];
--color-primary-700: #[hex];
--color-primary-800: #[hex];
--color-primary-900: #[hex];
--color-primary-950: #[hex];
```

### Step 3: Generate Neutral Scale with Brand Undertone

@visual-designer creates a neutral gray scale that harmonizes with the primary color.

**Method:**
1. Take the hue of the primary color
2. Reduce saturation to 3-8% (enough to be felt, not enough to be obvious)
3. Generate the full 50-950 scale

**Purpose of brand-tinted neutrals:**
- Pure gray (#808080) feels cold and disconnected from brand colors
- A warm or cool tint creates visual harmony between colored and neutral elements
- The tint should be invisible unless placed next to pure gray

**Output format:**
```css
--color-neutral-50:  #[hex];  /* Page background */
--color-neutral-100: #[hex];  /* Card background, alternate rows */
--color-neutral-200: #[hex];  /* Borders, dividers */
--color-neutral-300: #[hex];  /* Disabled text, placeholder */
--color-neutral-400: #[hex];  /* Muted text, icons */
--color-neutral-500: #[hex];  /* Secondary text */
--color-neutral-600: #[hex];  /* Body text (light mode) */
--color-neutral-700: #[hex];  /* Strong text */
--color-neutral-800: #[hex];  /* Headings */
--color-neutral-900: #[hex];  /* Primary text */
--color-neutral-950: #[hex];  /* Maximum contrast text */
```

### Step 4: Generate Semantic Color Scales

@visual-designer creates four semantic color scales, each with a purpose-driven subset of steps.

**Success (Green)**
- Communicates: Positive outcomes, confirmations, valid states, completed actions
- Hue range: 120-160
- Generate: 50, 100, 200, 500, 600, 700, 900

**Warning (Amber)**
- Communicates: Caution, attention needed, non-blocking issues, pending states
- Hue range: 35-50
- Generate: 50, 100, 200, 500, 600, 700, 900

**Error (Red)**
- Communicates: Errors, destructive actions, validation failures, critical alerts
- Hue range: 0-10 or 350-360
- Generate: 50, 100, 200, 500, 600, 700, 900

**Info (Blue)**
- Communicates: Informational messages, neutral alerts, help text, tips
- Hue range: 200-230 (differentiate from primary if primary is blue)
- Generate: 50, 100, 200, 500, 600, 700, 900

**Output format for each:**
```css
--color-success-50:  #[hex];
--color-success-100: #[hex];
--color-success-200: #[hex];
--color-success-500: #[hex];
--color-success-600: #[hex];
--color-success-700: #[hex];
--color-success-900: #[hex];
```

### Step 5: Verify WCAG AA Contrast for All Combinations

@accessibility-specialist checks every color combination that will be used together.

**Required contrast checks:**

| Combination | Minimum Ratio | Standard |
|-------------|---------------|----------|
| Neutral-900 on Neutral-50 (body text) | 4.5:1 | AA Normal |
| Neutral-600 on Neutral-50 (secondary text) | 4.5:1 | AA Normal |
| Primary-600 on White (links, buttons) | 4.5:1 | AA Normal |
| White on Primary-600 (button text) | 4.5:1 | AA Normal |
| Error-700 on Error-50 (error text on error bg) | 4.5:1 | AA Normal |
| Success-700 on Success-50 (success text on bg) | 4.5:1 | AA Normal |
| Warning-700 on Warning-50 (warning text on bg) | 4.5:1 | AA Normal |
| Neutral-300 on Neutral-50 (disabled state) | 3:1 | AA UI Component |
| Primary-500 on White (icon color) | 3:1 | AA UI Component |

**Contrast report format:**
```
Foreground          Background          Ratio    Pass/Fail
--color-neutral-900 --color-neutral-50  [X.X]:1  [PASS/FAIL] AA
--color-primary-600 #ffffff             [X.X]:1  [PASS/FAIL] AA
[... all combinations ...]
```

**If any combination fails:**
1. Adjust the failing color step darker (for foreground) or lighter (for background)
2. Re-verify that the adjustment does not break other combinations
3. Note the adjustment in the output

### Step 6: Output as CSS Custom Properties

@visual-designer compiles the complete palette.

**Complete output structure:**

```css
:root {
  /* ========================
     Primary Scale
     ======================== */
  --color-primary-50:  #[hex];
  --color-primary-100: #[hex];
  --color-primary-200: #[hex];
  --color-primary-300: #[hex];
  --color-primary-400: #[hex];
  --color-primary-500: #[hex];
  --color-primary-600: #[hex];
  --color-primary-700: #[hex];
  --color-primary-800: #[hex];
  --color-primary-900: #[hex];
  --color-primary-950: #[hex];

  /* ========================
     Neutral Scale
     ======================== */
  --color-neutral-50:  #[hex];
  --color-neutral-100: #[hex];
  --color-neutral-200: #[hex];
  --color-neutral-300: #[hex];
  --color-neutral-400: #[hex];
  --color-neutral-500: #[hex];
  --color-neutral-600: #[hex];
  --color-neutral-700: #[hex];
  --color-neutral-800: #[hex];
  --color-neutral-900: #[hex];
  --color-neutral-950: #[hex];

  /* ========================
     Semantic: Success
     ======================== */
  --color-success-50:  #[hex];
  --color-success-100: #[hex];
  --color-success-200: #[hex];
  --color-success-500: #[hex];
  --color-success-600: #[hex];
  --color-success-700: #[hex];
  --color-success-900: #[hex];

  /* ========================
     Semantic: Warning
     ======================== */
  --color-warning-50:  #[hex];
  --color-warning-100: #[hex];
  --color-warning-200: #[hex];
  --color-warning-500: #[hex];
  --color-warning-600: #[hex];
  --color-warning-700: #[hex];
  --color-warning-900: #[hex];

  /* ========================
     Semantic: Error
     ======================== */
  --color-error-50:  #[hex];
  --color-error-100: #[hex];
  --color-error-200: #[hex];
  --color-error-500: #[hex];
  --color-error-600: #[hex];
  --color-error-700: #[hex];
  --color-error-900: #[hex];

  /* ========================
     Semantic: Info
     ======================== */
  --color-info-50:  #[hex];
  --color-info-100: #[hex];
  --color-info-200: #[hex];
  --color-info-500: #[hex];
  --color-info-600: #[hex];
  --color-info-700: #[hex];
  --color-info-900: #[hex];
}
```

**Also provide alias tokens:**
```css
:root {
  /* Semantic aliases */
  --color-bg-page:       var(--color-neutral-50);
  --color-bg-surface:    #ffffff;
  --color-bg-muted:      var(--color-neutral-100);
  --color-text-primary:  var(--color-neutral-900);
  --color-text-secondary: var(--color-neutral-600);
  --color-text-muted:    var(--color-neutral-400);
  --color-border:        var(--color-neutral-200);
  --color-border-strong: var(--color-neutral-300);
  --color-interactive:   var(--color-primary-600);
  --color-interactive-hover: var(--color-primary-700);
  --color-focus-ring:    var(--color-primary-500);
}
```

## Related Skills

- `color-systems` - Color theory, palette generation, and harmony rules
- `accessibility-audit` - WCAG contrast requirements and testing
- `design-tokens` - Token architecture and naming conventions
- `visual-design` - Color usage in visual hierarchy and composition

## Related Commands

- `/create-design-system` - Use this palette as the color foundation
- `/audit-accessibility` - Verify the palette in a live interface
- `/create-type-scale` - Pair typography with the color system
- `/frontend-design` - Apply the palette in a production design

## Tips

- Test your palette in both light and dark mode early; retrofitting dark mode is expensive
- Brand-tinted neutrals make a bigger visual impact than most people expect
- When in doubt, go darker on text colors; readability trumps aesthetics
- Keep semantic colors distinct from brand colors to avoid confusion (red error vs. red brand)
- Print the final contrast report and keep it in your design system documentation

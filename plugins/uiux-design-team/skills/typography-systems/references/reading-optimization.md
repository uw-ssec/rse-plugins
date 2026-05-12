# Reading Optimization

Research-backed guidelines for optimizing on-screen reading. This reference covers the empirical foundations of line length, line height, and contrast; accessibility considerations for typographic choices; dark mode typography adjustments; and dyslexia-friendly type settings.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Research-Backed Reading Metrics](#research-backed-reading-metrics) | 14-65 | Empirical guidelines for line length, line height, and contrast |
| [Accessibility Considerations](#accessibility-considerations) | 67-115 | WCAG requirements and inclusive typography practices |
| [Dark Mode Typography](#dark-mode-typography) | 117-160 | Adjustments for readable typography on dark backgrounds |
| [Dyslexia-Friendly Type](#dyslexia-friendly-type) | 162-210 | Research-informed settings for readers with dyslexia |
| [Performance and Reading](#performance-and-reading) | 212-235 | Font loading strategies that protect the reading experience |
| [See Also](#see-also) | 237-245 | Related references and skills |

## Research-Backed Reading Metrics

### Line Length (Measure)

Research from the Baymard Institute and Nielsen Norman Group consistently identifies optimal line length as **45-75 characters per line**, with 65 characters as the sweet spot for sustained reading.

**Why 65 characters?** At this length, the eye can comfortably return to the start of the next line without losing its position. Shorter lines (under 40 characters) create excessive line breaks that fragment sentences and disrupt reading rhythm. Longer lines (over 80 characters) cause the eye to lose track during the return sweep, leading to rereading and fatigue.

**Implementation:**

```css
.prose {
  max-width: 65ch; /* The `ch` unit equals the width of the '0' character */
}
```

**Context-dependent adjustments:**
- **Mobile (320-480px):** Lines naturally constrain to 35-50 characters. This is acceptable because users hold phones closer, reducing the return-sweep distance.
- **Multi-column layouts:** Each column should maintain 40-60 characters. Narrower columns compensate with easier scanning.
- **Captions and annotations:** Shorter line lengths (30-45ch) are acceptable for small text, which is typically read in brief bursts rather than sustained reading.
- **Data tables:** No character limit applies. Table cells contain fragments, not prose.

### Line Height (Leading)

Line height controls the vertical space between baselines. Optimal line height depends on font size, line length, and typeface design.

**General guidelines from research:**

| Font Size | Line Length | Recommended Line Height |
|-----------|-----------|------------------------|
| 14px | 45-55ch | 1.6-1.7 |
| 16px | 55-65ch | 1.5-1.6 |
| 18px | 55-65ch | 1.45-1.55 |
| 20-24px | 40-55ch | 1.3-1.45 |
| 28-40px | 20-40ch | 1.2-1.3 |
| 48px+ | 10-30ch | 1.05-1.2 |

**The inverse relationship:** As font size increases, line height ratio decreases. Large text has enough vertical presence that tight leading still leaves clear separation between lines. Small text needs proportionally more space to prevent lines from visually merging.

**The typeface factor:** Fonts with tall x-heights (Inter, Roboto) need more line height than fonts with smaller x-heights (Garamond, Caslon). The x-height determines how much of the line-height space is filled by letterforms versus whitespace.

### Contrast and Readability

**WCAG contrast requirements:**
- **Normal text (under 18px or under 14px bold):** Minimum 4.5:1 contrast ratio (AA), 7:1 for AAA
- **Large text (18px+ or 14px+ bold):** Minimum 3:1 contrast ratio (AA), 4.5:1 for AAA

**Beyond minimum contrast:** Maximum contrast (pure black on pure white, #000 on #FFF, ratio 21:1) is not always optimal. Research suggests slightly reduced contrast (e.g., #1a1a1a on #ffffff, ratio ~18:1) reduces glare on backlit screens without sacrificing legibility. However, never reduce contrast below WCAG AA requirements.

**Text rendering considerations:**
- Light text on dark backgrounds appears heavier than dark text on light backgrounds at the same weight. Compensate by using a lighter font weight or slightly increasing letter spacing.
- Anti-aliased text at small sizes loses contrast. Ensure body text contrast exceeds the minimum by a comfortable margin.

## Accessibility Considerations

### WCAG Typography Requirements

WCAG 2.2 Success Criteria relevant to typography:

**1.4.3 Contrast (Minimum, Level AA):** Text must have a contrast ratio of at least 4.5:1 (3:1 for large text). This is non-negotiable for any public-facing interface.

**1.4.4 Resize Text (Level AA):** Text must be resizable up to 200% without loss of content or functionality. This means:
- Use relative units (`rem`, `em`) not fixed pixels for font sizes
- Ensure layouts do not break when the browser font size is doubled
- Test with browser zoom at 200%

**1.4.6 Contrast (Enhanced, Level AAA):** Text must have a contrast ratio of at least 7:1 (4.5:1 for large text). Target this for critical content like error messages, instructions, and primary body text.

**1.4.8 Visual Presentation (Level AAA):** For blocks of text:
- The user can select foreground and background colors
- Width is no more than 80 characters
- Text is not justified (right edge is ragged)
- Line spacing is at least 1.5 within paragraphs
- Paragraph spacing is at least 1.5 times the line spacing

**1.4.12 Text Spacing (Level AA):** Content must remain functional when users override:
- Line height to at least 1.5 times the font size
- Paragraph spacing to at least 2 times the font size
- Letter spacing to at least 0.12 times the font size
- Word spacing to at least 0.16 times the font size

### Implementation for Spacing Override Compliance

```css
/* Design with these as minimums, not maximums */
body {
  line-height: 1.5;       /* Allows user override without breaking layout */
  letter-spacing: normal;  /* Does not constrain user adjustments */
  word-spacing: normal;    /* Does not constrain user adjustments */
}

/* Avoid fixed heights on text containers */
.text-container {
  min-height: auto;        /* Expands with text spacing changes */
  overflow: visible;       /* Never clip text that has been respaced */
}
```

### Font Selection for Accessibility

Choose body fonts with these characteristics:
- **Open counters:** The enclosed spaces in letters like 'a', 'e', 'c' should be generous, aiding letter recognition
- **Distinct letterforms:** 'I' (capital i), 'l' (lowercase L), and '1' (one) should be visually distinct. Same for '0' (zero) and 'O' (capital o)
- **Generous x-height:** Larger x-heights improve readability at small sizes
- **Even stroke width:** Fonts with extreme thick-thin contrast lose their thin strokes at small sizes and on low-resolution screens

## Dark Mode Typography

### The Core Challenge

Dark mode reverses the figure-ground relationship of text. On light backgrounds, dark text absorbs light and appears defined. On dark backgrounds, light text emits light and appears to glow, making it seem heavier and less crisp.

### Weight Adjustment

Light text on dark backgrounds appears optically bolder than the same weight on a light background. Compensate:

```css
@media (prefers-color-scheme: dark) {
  body {
    font-weight: 350; /* Slightly lighter than 400 regular */
    /* Or if variable font is not available: */
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
}
```

The `-webkit-font-smoothing: antialiased` property reduces subpixel rendering that makes light-on-dark text appear bolder on macOS. Use it specifically for dark mode, not globally.

### Contrast Calibration

Do not use pure white (#ffffff) text on pure black (#000000) backgrounds. The extreme contrast causes "halation" -- the white text appears to bleed into the dark background, reducing legibility.

**Recommended dark mode text colors:**
- Primary text: #e4e4e7 (zinc-200) or #d4d4d8 (zinc-300) on #18181b (zinc-900)
- Secondary text: #a1a1aa (zinc-400) on #18181b
- Background: #09090b (zinc-950) or #18181b (zinc-900), never pure #000000

**Contrast ratios to verify:**
- Primary text on background: target 12:1 to 15:1 (not maximum 21:1)
- Secondary text on background: maintain at least 4.5:1

### Line Height in Dark Mode

Some typographers recommend increasing line height by 0.05-0.1 in dark mode because the perceived boldness of light text reduces the visual separation between lines. This is a subtle adjustment:

```css
@media (prefers-color-scheme: dark) {
  .prose {
    line-height: 1.6; /* Up from 1.5 in light mode */
  }
}
```

### Color Temperature

Warm-tinted text (#f5f5f0, slightly warm white) on dark backgrounds reduces eye strain compared to cool-tinted text (#f0f0ff, slightly blue white). Screens emit blue light that is more fatiguing in dark environments, and warm text tones partially compensate.

## Dyslexia-Friendly Type

### What Research Shows

Dyslexia affects approximately 15-20% of the population to some degree. While no single font "fixes" dyslexia, research identifies specific typographic properties that reduce reading difficulty for dyslexic readers.

### Font Characteristics That Help

**Distinct letterforms:** Dyslexic readers most commonly confuse mirrored or rotated letters: b/d, p/q, n/u, m/w. Fonts where these letters have distinct shapes (not just rotations of each other) reduce confusion. OpenDyslexic, Lexie Readable, and humanist sans-serifs like Verdana and Tahoma address this.

**Weighted bottoms:** Some dyslexia-specific fonts weight the bottom of letters to provide a visual "anchor" that prevents the reader from mentally rotating letters. OpenDyslexic uses this technique.

**Generous spacing:** Tight letter spacing increases "crowding effects" that are particularly disabling for dyslexic readers. Wider spacing reduces errors.

**Simple, unambiguous forms:** Decorative fonts, thin fonts, and fonts with unusual letterforms increase cognitive load. Simple, regular forms reduce it.

### Recommended Settings

```css
.dyslexia-friendly {
  font-family: 'Lexend', 'Verdana', 'Tahoma', sans-serif;
  font-size: 1.125rem;      /* Slightly larger than default */
  line-height: 1.8;         /* More generous than standard */
  letter-spacing: 0.05em;   /* Wider than default */
  word-spacing: 0.1em;      /* Wider than default */
  max-width: 60ch;          /* Slightly shorter lines */
}
```

### Recommended Fonts

| Font | Type | Key Feature | Availability |
|------|------|-------------|-------------|
| Lexend | Sans-serif | Designed for reading fluency research | Google Fonts (free) |
| Atkinson Hyperlegible | Sans-serif | Maximized letterform distinction | Google Fonts (free) |
| OpenDyslexic | Sans-serif | Weighted bottoms, dyslexia-specific | Open source (free) |
| Verdana | Sans-serif | Wide letterforms, distinct shapes | System font |
| Comic Sans | Sans-serif | Irregular shapes prevent rotation | System font (stigmatized but genuinely helpful) |

### Offering Reader Controls

The most accessible approach is to give readers control over their own typography:

```css
/* User-controlled reading preferences */
.reader-settings {
  --reader-font-size: 1rem;
  --reader-line-height: 1.5;
  --reader-letter-spacing: normal;
  --reader-font-family: inherit;
}

.prose {
  font-size: var(--reader-font-size);
  line-height: var(--reader-line-height);
  letter-spacing: var(--reader-letter-spacing);
  font-family: var(--reader-font-family);
}
```

Allow users to adjust font size, line height, letter spacing, and font family through a reading preferences panel. This accommodates the full spectrum of reading needs without requiring the designer to predict every individual's optimal settings.

## Performance and Reading

### Font Loading and Reading Experience

Font loading directly affects reading. If fonts load slowly, users experience either invisible text (FOIT -- Flash of Invisible Text) or text that shifts appearance (FOUT -- Flash of Unstyled Text).

**Recommended strategy:**

```html
<!-- Preload the body font (most critical for reading) -->
<link rel="preload" href="/fonts/body-regular.woff2" as="font" type="font/woff2" crossorigin>

<!-- Font-face with swap to prevent invisible text -->
<style>
  @font-face {
    font-family: 'Body';
    src: url('/fonts/body-regular.woff2') format('woff2');
    font-weight: 400;
    font-display: swap;
  }
</style>
```

**Fallback font matching.** When using `font-display: swap`, the fallback font briefly appears before the custom font loads. Minimize the visual shift by choosing a fallback with similar metrics:

```css
body {
  font-family: 'Body', 'Segoe UI', system-ui, -apple-system, sans-serif;
  /* System fonts with similar metrics reduce layout shift */
}
```

### Content Layout Stability

Font loading can cause Cumulative Layout Shift (CLS) when the custom font has different metrics than the fallback. Use the `size-adjust`, `ascent-override`, and `descent-override` descriptors to match metrics:

```css
@font-face {
  font-family: 'Body Fallback';
  src: local('Arial');
  size-adjust: 105%;
  ascent-override: 90%;
  descent-override: 22%;
  line-gap-override: 0%;
}
```

## See Also

- [[type-scale-theory.md]] -- Ensure scale sizes remain legible at the smallest steps
- [[font-pairing-guide.md]] -- Select fonts with the accessibility characteristics described here
- [[../../color-systems/references/contrast-requirements.md]] -- Detailed WCAG contrast ratio calculations and testing tools
- [[../../accessibility-audit/SKILL.md]] -- Full accessibility evaluation methodology including typography checks
- [[../../design-tokens/SKILL.md]] -- Encode reading-optimized values as tokens for consistent application

**Back to:** [Typography Systems Skill](../SKILL.md)

## Reading Metrics (Reference)

### Line Length

Optimal body line length: **45–75 characters**, ideal 65.

```css
.prose { max-width: 65ch; }
```

### Line Height Ratios

| Font Size | Recommended Line Height |
|-----------|-------------------------|
| 12–14px | 1.6–1.7 |
| 16–18px | 1.5–1.6 |
| 20–24px | 1.4–1.5 |
| 28–36px | 1.2–1.3 |
| 40px+   | 1.1–1.2 |

Rule: larger size → smaller ratio.

```css
:root {
  --leading-tight:   1.2;
  --leading-snug:    1.375;
  --leading-normal:  1.5;
  --leading-relaxed: 1.625;
  --leading-loose:   1.75;
}
```

### Letter Spacing

- All-caps: +0.05 to +0.1em
- Large display: −0.02 to −0.01em
- Body: 0 (font designer optimized)
- Small text: +0.01 to +0.02em

```css
.uppercase-label { text-transform: uppercase; letter-spacing: 0.08em; }
.display-heading { letter-spacing: -0.02em; }
```

### Paragraph Spacing

Use margin between paragraphs, not first-line indent, for screen reading:

```css
.prose p + p { margin-top: 1.5em; }
```

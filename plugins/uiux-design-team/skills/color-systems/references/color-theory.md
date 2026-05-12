# Color Theory

Deep reference on color science, perceptual models, color psychology, and cultural considerations for building design-grade color systems.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Color Models](#color-models) | 14-55 | RGB, HSL, LAB, and OKLCH compared for design use |
| [Perceptual Color Spaces](#perceptual-color-spaces) | 57-90 | Why perceptual uniformity matters and how OKLCH solves it |
| [Color Psychology](#color-psychology) | 92-130 | Emotional associations of colors in Western and global contexts |
| [Cultural Color Considerations](#cultural-color-considerations) | 132-155 | How color meaning varies across cultures |
| [Color Temperature](#color-temperature) | 157-180 | Warm vs. cool color theory and practical applications |

## Color Models

### RGB (Red, Green, Blue)

RGB is the additive color model used by screens. Values range from 0-255 for each channel, or 0-100% in CSS.

- **Strengths**: Direct representation of how screens produce color. Useful for programmatic color manipulation.
- **Weaknesses**: Unintuitive for design. Predicting what rgb(180, 45, 120) looks like requires experience. Adjusting one channel affects perceived hue, saturation, and lightness simultaneously.
- **Use when**: Writing color manipulation code, working with canvas/WebGL, or interfacing with APIs that expect RGB.

### HSL (Hue, Saturation, Lightness)

HSL maps color to human-understandable dimensions.

- **Hue** (0-360 degrees): The color itself. 0/360=red, 60=yellow, 120=green, 180=cyan, 240=blue, 300=magenta.
- **Saturation** (0-100%): Color purity. 0%=gray, 100%=vivid. Controls how "colorful" the color appears.
- **Lightness** (0-100%): Brightness. 0%=black, 100%=white, 50%=pure color.

- **Strengths**: Intuitive to manipulate. "Make it darker" = reduce lightness. "Make it more muted" = reduce saturation. "Shift the hue" = rotate the hue value.
- **Weaknesses**: Not perceptually uniform. hsl(60, 100%, 50%) (yellow) appears much lighter than hsl(240, 100%, 50%) (blue) despite identical lightness values. This makes generating consistent scales difficult.
- **Use when**: Quickly exploring color options, explaining color relationships to non-designers, or building simple palettes.

### LAB (CIELAB)

LAB separates lightness from color information and is designed to be perceptually uniform.

- **L** (0-100): Lightness. Perceptually calibrated; L=50 looks like medium gray.
- **a** (-128 to 127): Green-to-red axis.
- **b** (-128 to 127): Blue-to-yellow axis.

- **Strengths**: Perceptually uniform — equal numerical changes produce equal perceived changes. Excellent for generating even color gradients and accessible palettes.
- **Weaknesses**: The a/b axes are not intuitive. Difficult to think in terms of green-red and blue-yellow axes.
- **Use when**: Precise color science work, checking perceptual contrast, generating even gradients.

### OKLCH

OKLCH is the modern perceptually uniform color space designed specifically for CSS and digital design. Available in CSS via `oklch()`.

- **L** (0-1): Lightness, perceptually calibrated.
- **C** (0-0.4+): Chroma (colorfulness). Similar to saturation but perceptually accurate.
- **H** (0-360): Hue angle, like HSL but perceptually uniform.

- **Strengths**: Combines the intuitiveness of HSL (hue angle + lightness) with the perceptual accuracy of LAB. Equal lightness values actually look equally light. Supported in modern CSS.
- **Weaknesses**: Newer; less tooling support. Some older browsers lack support (use fallbacks).
- **Use when**: Building production color systems, generating perceptually even shade scales, creating accessible palettes.

## Perceptual Color Spaces

### The Problem with HSL

HSL's lightness channel does not correspond to human perception. Consider these colors, all at HSL lightness 50%:

- `hsl(60, 100%, 50%)` — Yellow: appears very bright
- `hsl(240, 100%, 50%)` — Blue: appears very dark
- `hsl(120, 100%, 50%)` — Green: appears medium-bright
- `hsl(0, 100%, 50%)` — Red: appears medium

This means an HSL-based shade scale (lightness from 10% to 90%) will have uneven perceptual steps. Some steps will look barely different; others will jump dramatically.

### How OKLCH Solves This

In OKLCH, lightness is perceptually calibrated. Setting L=0.5 for any hue produces colors that genuinely appear equally bright. This means:

- **Shade scales are even**: A 10-step lightness scale from L=0.15 to L=0.95 produces perceptually even steps for any hue.
- **Cross-hue comparisons work**: Primary-500 (blue) and Success-500 (green) at the same OKLCH lightness actually look equally prominent in the interface.
- **Contrast ratios are predictable**: If two OKLCH colors have a large lightness difference, they will have high contrast. In HSL, this is not guaranteed.

### Generating a Shade Scale with OKLCH

For a given brand hue, generate a 50-950 scale:

```css
--color-brand-50:  oklch(0.97 0.02 250);   /* near-white tint */
--color-brand-100: oklch(0.93 0.04 250);
--color-brand-200: oklch(0.87 0.08 250);
--color-brand-300: oklch(0.78 0.12 250);
--color-brand-400: oklch(0.68 0.16 250);
--color-brand-500: oklch(0.58 0.19 250);   /* base color */
--color-brand-600: oklch(0.48 0.18 250);
--color-brand-700: oklch(0.40 0.15 250);
--color-brand-800: oklch(0.32 0.12 250);
--color-brand-900: oklch(0.24 0.08 250);
--color-brand-950: oklch(0.18 0.05 250);   /* near-black shade */
```

Lightness decreases linearly. Chroma peaks at the base color and tapers toward both extremes (very light and very dark colors are naturally less chromatic).

## Color Psychology

Color associations are real but not universal. These are general patterns observed in Western contexts; see Cultural Considerations for important caveats.

### Primary Associations

| Color | Positive Associations | Negative Associations | Common UI Usage |
|-------|----------------------|----------------------|-----------------|
| **Red** | Energy, passion, urgency, love | Danger, aggression, error | Error states, destructive actions, sale pricing, urgency indicators |
| **Orange** | Warmth, enthusiasm, creativity, appetite | Caution, cheapness | CTAs (high visibility), warnings, creative tool accents |
| **Yellow** | Optimism, clarity, warmth, attention | Anxiety, caution, cowardice | Warning states, highlights, attention indicators |
| **Green** | Growth, success, nature, safety, health | Envy, inexperience | Success states, confirmation, health/wellness, financial gain |
| **Blue** | Trust, stability, professionalism, calm | Coldness, sadness, detachment | Primary brand color (most popular), links, informational states |
| **Purple** | Luxury, creativity, mystery, wisdom | Artificiality, excess | Premium features, creative tools, spiritual/wellness contexts |
| **Pink** | Playfulness, compassion, romance, youth | Immaturity, frivolity | Consumer apps, lifestyle brands, gender-specific contexts (use carefully) |
| **Black** | Sophistication, power, elegance, authority | Darkness, heaviness, mourning | Luxury brands, text, borders, premium UI |
| **White** | Purity, simplicity, cleanliness, space | Emptiness, sterility | Backgrounds, negative space, minimalist design |
| **Gray** | Neutrality, balance, sophistication | Dullness, ambiguity, indecision | Disabled states, borders, secondary text, backgrounds |

### Applying Psychology to Interface Design

Do not apply color psychology as a formula ("my app needs to feel trustworthy, so everything must be blue"). Instead:
- Use psychology to validate choices ("our blue palette aligns with our trust-focused brand")
- Use psychological contrast deliberately ("the red delete button creates urgency against the calm blue interface")
- Consider that most users do not consciously register color psychology; they experience it as a vague emotional impression

## Cultural Color Considerations

Color meaning varies significantly across cultures. For international products, these considerations are critical.

### Key Cultural Variations

| Color | Western | East Asian | Middle Eastern | South Asian |
|-------|---------|------------|---------------|-------------|
| **White** | Purity, weddings | Mourning, death, funerals | Purity, peace | Peace, sometimes mourning |
| **Red** | Danger, passion, stop | Luck, prosperity, celebration | Danger, caution | Purity, fertility, love |
| **Yellow** | Happiness, caution | Royalty (China), courage (Japan) | Happiness, prosperity | Sacred, auspicious |
| **Green** | Nature, growth, go | Youth, eternity | Islam, paradise, fertility | Harvest, happiness |
| **Blue** | Trust, sadness | Immortality, healing | Protection, spirituality | Strength, life |
| **Black** | Death, elegance | Power, wealth | Mourning, evil | Evil, negativity |
| **Purple** | Royalty, luxury | Privilege, wealth | Wealth, spirituality | Sorrow, comforting |

### Design Implications

- **Error states**: Red means "error" in most Western UI conventions, but in East Asian contexts, red is positive. For international products, pair color with icons and text (a red X icon with "Error" text) rather than relying on color alone.
- **Success states**: Green means "success/go" in most contexts but has religious significance in Islamic cultures. This usually reinforces the positive meaning but be aware of the association.
- **White space**: Western design values white space as sophistication. Some East Asian design traditions favor density and richness. Research your specific audience.

## Color Temperature

Color temperature describes the warm-cool spectrum and has practical applications in interface design.

### The Warm-Cool Spectrum

Colors are classified by their position on the color wheel:
- **Warm**: Red through yellow (0-60 on the hue wheel). These colors advance toward the viewer and create visual energy.
- **Cool**: Green through blue-violet (120-280 on the hue wheel). These colors recede from the viewer and create visual calm.
- **Neutral-warm**: Orange-adjacent colors, beige, cream, warm grays. Feel inviting and approachable.
- **Neutral-cool**: Blue-adjacent grays, slate, cool whites. Feel professional and distant.

### Temperature in Interface Design

**Background temperature** sets the emotional baseline:
- Warm backgrounds (#faf5ef warm cream) create intimacy and approachability
- Cool backgrounds (#f0f4f8 cool gray) create professionalism and objectivity
- True neutral backgrounds (#f5f5f5 pure gray) create no temperature bias

**Accent temperature** creates emphasis:
- Warm accents on cool backgrounds create strong focal points (a warm CTA button on a cool interface)
- Cool accents on warm backgrounds are more subtle and sophisticated
- Same-temperature accents create harmony at the cost of reduced contrast

**Temperature consistency**: Within a single interface, maintain consistent temperature. Mixing warm and cool neutrals (warm gray sidebar + cool gray content area) creates subtle visual tension. This can be intentional (distinguishing areas) or accidental (inconsistency).

## See Also

- [[palette-generation.md]] - Algorithmic methods for generating palettes from color theory
- [[contrast-requirements.md]] - WCAG contrast standards that constrain color choices
- [[../../visual-design/references/aesthetic-principles.md]] - How color choices support aesthetic direction
- [[../../visual-design/references/brand-alignment.md]] - Color within brand identity systems

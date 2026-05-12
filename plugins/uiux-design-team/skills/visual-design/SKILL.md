---
name: visual-design
description: Create distinctive, production-grade frontend interfaces with bold aesthetic choices, systematic visual hierarchy, brand alignment, and emotional design methodology. Incorporates Claude's frontend-design guidance with expanded context for visual hierarchy, brand alignment, and design philosophy.
metadata:
   references:
   - references/aesthetic-principles.md
   - references/brand-alignment.md
   - references/visual-hierarchy.md
---

# Visual Design

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.

## Visual Hierarchy Principles

Visual hierarchy is the arrangement of design elements in order of importance. It controls the sequence in which the human eye perceives what it sees, guiding users through content in a deliberate, meaningful order.

### Gestalt-Informed Hierarchy

Apply Gestalt principles to establish clear visual relationships:

- **Proximity**: Elements placed close together are perceived as related. Group navigation items, form fields with labels, and card content to create logical clusters. The space between groups should be noticeably larger than space within groups.
- **Similarity**: Elements sharing visual properties (color, size, shape, texture) are perceived as belonging together. Use consistent styling for same-level headings, repeated card layouts, and action buttons of equal importance.
- **Figure-Ground**: The relationship between foreground elements and their background creates depth. Elevated cards over subtle backgrounds, modal overlays with dimmed backdrops, and highlighted rows in tables all leverage figure-ground separation.
- **Continuity**: The eye follows smooth lines and curves. Align elements along invisible axes to create visual flow. Left-aligned text columns, grid lines, and progress indicators all exploit continuity.
- **Closure**: The mind completes incomplete shapes. Icon design, logo marks, and decorative elements can use implied shapes to create visual interest with minimal ink.

### The Hierarchy Tools

Each tool controls attention differently. Combine them deliberately:

| Tool | Effect | Application |
|------|--------|-------------|
| **Size** | Largest = most important | Hero headlines, primary CTAs, featured images |
| **Color/Contrast** | High contrast = attention | Error states, active navigation, primary buttons |
| **Spacing** | More space = more importance | Section padding, card margins, breathing room around key content |
| **Position** | Top-left in LTR = first seen | Logo placement, primary navigation, page titles |
| **Weight** | Bold = emphasis | Headings, key metrics, labels vs. values |
| **Motion** | Movement = attention | Loading indicators, notification badges, onboarding highlights |

### Scanning Patterns

- **F-Pattern**: Text-heavy pages (articles, search results, documentation). Users scan horizontally across the top, then down the left side with occasional horizontal scans. Place critical information in the first two lines and along the left edge.
- **Z-Pattern**: Minimal pages (landing pages, hero sections, sign-up forms). The eye moves from top-left to top-right, diagonally to bottom-left, then across to bottom-right. Place logo top-left, CTA top-right or bottom-right.

### Golden Ratio Applications

The golden ratio (1:1.618) produces naturally pleasing proportions:
- Content area to sidebar: 61.8% to 38.2%
- Image dimensions and crop ratios
- Spacing scale progression (each step ~1.618x the previous)
- Typography scale ratios for harmonious size relationships

### Visual Weight and Balance

- **Symmetrical balance**: Formal, stable, trustworthy. Best for institutional sites, legal, finance. Equal visual weight on both sides of a central axis.
- **Asymmetrical balance**: Dynamic, interesting, modern. Best for creative portfolios, startups, editorial. Unequal elements balanced through contrast (a large light element balanced by a small dark one).

## Brand Alignment

Every interface exists within a brand context. Visual design decisions must reinforce, not contradict, the brand's identity.

### Brand Audit Checklist

Before designing, document these brand attributes:
- **Values**: What does the brand stand for? (innovation, trust, playfulness, authority)
- **Voice**: How does the brand communicate? (formal, casual, technical, warm)
- **Existing visual language**: Current colors, typography, imagery style, iconography
- **Target audience**: Demographics, psychographics, technical sophistication
- **Competitive landscape**: What do competitors look like? How can this brand differentiate?

### Mood Board Methodology

1. Collect 10-15 reference images spanning typography, color, layout, photography, and texture
2. Identify emerging patterns: recurring colors, spatial relationships, emotional qualities
3. Extract the design language: distill patterns into concrete tokens (colors, type choices, spacing)
4. Validate against brand values: does the mood board feel like the brand?
5. Share and iterate before committing to implementation

### Extending vs. Evolving Brand Identity

- **Extending**: Working within established guidelines. Respect existing tokens, introduce new elements only where the system has gaps. Match existing component patterns.
- **Evolving**: Pushing the brand forward. Propose new directions that honor brand essence while modernizing expression. Always provide rationale tied to brand values and business goals.

### Consistency Tokens

Design tokens encode brand decisions into reusable, platform-agnostic values:
- Color tokens (primary, secondary, neutral, semantic)
- Typography tokens (font families, sizes, weights, line heights)
- Spacing tokens (consistent scale applied globally)
- Shadow and elevation tokens (depth system)
- Border radius tokens (sharp = serious, rounded = friendly)

## Emotional Design Layers

Design operates on three psychological levels simultaneously. Exceptional interfaces address all three.

### Norman's Three Levels

1. **Visceral (first 50ms)**: The immediate sensory reaction. Before conscious thought, users form an impression. This is pure aesthetics: color, imagery, composition, visual polish. A beautiful interface triggers positive emotion that colors the entire subsequent experience.

2. **Behavioral (usability)**: Does it work? Is the interaction smooth, predictable, responsive? This is the functional layer: navigation clarity, form usability, error recovery, loading states. Users forgive aesthetic imperfections if the interface works flawlessly, but visual beauty cannot compensate for broken interactions.

3. **Reflective (meaning)**: What does using this interface say about me? This is the layer of identity, memory, and storytelling. Premium aesthetics signal premium quality. Playful design signals approachability. A thoughtfully designed 404 page creates a moment of delight that users share and remember.

### Designing for All Three

- **Visceral**: Invest in first-impression moments. Page load animations, hero sections, onboarding screens. The first screen a user sees sets the emotional baseline.
- **Behavioral**: Ensure every interaction provides immediate, clear feedback. Button state changes, form validation, loading indicators, transition animations between states.
- **Reflective**: Craft moments of delight and meaning. Micro-copy with personality, celebratory animations on task completion, empty states that feel warm rather than cold, error messages that empathize.

## Expanded Aesthetic Direction Library

Choose a tone that matches the project's context. Each direction demands different implementation approaches.

| Tone | Best For | Key Characteristics |
|------|----------|-------------------|
| Brutally Minimal | SaaS tools, developer tools | Monospace type, stark contrast, zero decoration, functional beauty |
| Luxury/Refined | Fashion, premium products | Serif type, restrained palette, generous whitespace, subtle animations |
| Editorial/Magazine | Content platforms, blogs | Strong typography hierarchy, dramatic imagery, asymmetric layouts |
| Playful/Toy-like | Consumer apps, kids products | Rounded shapes, vibrant colors, bouncy animations, oversized elements |
| Retro-Futuristic | Creative agencies, tech products | Neon accents, dark backgrounds, geometric shapes, CRT/scanline effects |
| Organic/Natural | Wellness, sustainability | Earth tones, organic shapes, textured backgrounds, hand-drawn elements |
| Brutalist/Raw | Art, counter-culture | Raw HTML aesthetic, exposed structure, intentional ugliness, system fonts used ironically |
| Industrial/Utilitarian | Data-heavy apps, dashboards | Dense information, monospace type, muted colors, grid-heavy layouts |
| Art Deco/Geometric | Luxury, events, hospitality | Gold accents, symmetry, geometric patterns, decorative borders |
| Soft/Pastel | Health, children, lifestyle | Muted colors, soft shadows, rounded corners, gentle gradients |
| Cyberpunk/Neon | Gaming, nightlife, music | Glitch effects, neon gradients, dark UI, high-energy motion |
| Neomorphic | Modern fintech, IoT dashboards | Soft extruded elements, monochromatic, subtle inner/outer shadows |
| Glassmorphism | Modern SaaS, creative tools | Frosted glass effects, transparency, vibrant backgrounds behind blur |
| Swiss/International | Corporate, institutional | Grid precision, Akzidenz-style type, clean geometry, objective clarity |
| Maximalist/Eclectic | Fashion, art, entertainment | Mixed media, clashing colors, layered textures, controlled chaos |

## Deep Dive References

### [Aesthetic Principles](references/aesthetic-principles.md)

- Aesthetic Philosophy
- Anti-Pattern Library
- Tone Selection Framework
- Applied Aesthetic Examples

### [Brand Alignment](references/brand-alignment.md)

- Brand Audit Template
- Mood Board Creation Process
- Design Language Documentation
- Brand Extension Methodology
- Case Studies

### [Visual Hierarchy](references/visual-hierarchy.md)

- Gestalt Principles Applied
- Scanning Patterns
- Visual Weight Formulas
- Golden Ratio in Web Layout
- Eye-Tracking Research Insights
- Practical Hierarchy Exercises

## Next Steps

After establishing the visual design direction, build out the systematic foundations:

- **[Color Systems](../color-systems/SKILL.md)**: Define palettes, contrast requirements, semantic tokens, dark mode
- **[Typography Systems](../typography-systems/SKILL.md)**: Type scales, font pairing, fluid typography, reading metrics
- **[Motion Design](../motion-design/SKILL.md)**: Animation principles, transitions, performance, choreography
- **[Grid Layout Systems](../grid-layout-systems/SKILL.md)**: Column grids, spacing scales, responsive strategies, CSS implementation

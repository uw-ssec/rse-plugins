# Spacing Systems

A complete reference for building consistent spacing systems in user interfaces. Covers base-unit systems, spatial hierarchy levels, density modes for different contexts, and spacing token naming conventions for design systems.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Base-Unit Systems](#base-unit-systems) | 14-55 | 4px and 8px base-unit approaches with trade-offs |
| [Spatial Hierarchy](#spatial-hierarchy) | 57-110 | Intra-component, inter-component, and section-level spacing |
| [Density Modes](#density-modes) | 112-160 | Compact, default, and comfortable spacing configurations |
| [Spacing Token Naming](#spacing-token-naming) | 162-210 | Naming conventions for spacing tokens in design systems |
| [Spacing and Visual Rhythm](#spacing-and-visual-rhythm) | 212-240 | How spacing creates rhythm, grouping, and hierarchy |
| [See Also](#see-also) | 242-250 | Related references and skills |

## Base-Unit Systems

A base-unit spacing system constrains all spacing values to multiples of a single base unit. This eliminates arbitrary pixel values and creates visual rhythm throughout the interface.

### 4px Base System

All spacing values are multiples of 4px. This produces a granular scale suitable for interfaces that need fine control.

```css
:root {
  --space-0:   0px;
  --space-0.5: 2px;    /* Half-step for borders and fine adjustments */
  --space-1:   4px;
  --space-1.5: 6px;
  --space-2:   8px;
  --space-3:   12px;
  --space-4:   16px;
  --space-5:   20px;
  --space-6:   24px;
  --space-7:   28px;
  --space-8:   32px;
  --space-10:  40px;
  --space-12:  48px;
  --space-14:  56px;
  --space-16:  64px;
  --space-20:  80px;
  --space-24:  96px;
  --space-32:  128px;
}
```

**Advantages:** Fine granularity. The 4px steps allow subtle distinctions (12px vs 16px vs 20px) that a coarser system cannot express. Works well for dense UIs with many spacing levels.

**Disadvantages:** Many options create decision fatigue. Designers may debate 12px vs 16px when either would work. Requires discipline to avoid using arbitrary values.

### 8px Base System

All spacing values are multiples of 8px. This produces a simpler scale with fewer choices, which can accelerate decisions.

```css
:root {
  --space-1:   8px;
  --space-2:   16px;
  --space-3:   24px;
  --space-4:   32px;
  --space-5:   40px;
  --space-6:   48px;
  --space-8:   64px;
  --space-10:  80px;
  --space-12:  96px;
  --space-16:  128px;
}
```

**Advantages:** Fewer decisions. Every spacing choice is clearly distinct from its neighbors (8px jumps). Aligns naturally with baseline grids (common line-heights are multiples of 8px).

**Disadvantages:** Less granular. The jump from 8px to 16px is significant, and sometimes 12px would be more appropriate. Hybrid approaches (4px for small spacing, 8px for large) can mitigate this.

### Hybrid Approach (Recommended)

Use 4px steps for small values (0-24px) where fine control matters, and 8px steps for larger values (32px+) where the difference between steps is less critical.

```css
:root {
  /* Fine control range (4px steps) */
  --space-1:   4px;
  --space-2:   8px;
  --space-3:   12px;
  --space-4:   16px;
  --space-5:   20px;
  --space-6:   24px;

  /* Coarse range (8px steps) */
  --space-8:   32px;
  --space-10:  40px;
  --space-12:  48px;
  --space-16:  64px;
  --space-20:  80px;
  --space-24:  96px;
}
```

## Spatial Hierarchy

Spacing communicates relationship. Elements that are closer together are perceived as related (Gestalt principle of proximity). A consistent spatial hierarchy uses three tiers of spacing to express three levels of relationship.

### Tier 1: Intra-Component Spacing (4-12px)

Spacing within a single component. These are the tightest values, expressing that elements belong to the same unit.

**Examples:**
- Gap between an icon and its label: 4-8px
- Padding inside a button: 8px vertical, 16px horizontal
- Space between a form label and its input: 4-6px
- Space between an avatar and a username: 8px
- Padding within a chip or tag: 4px vertical, 8px horizontal

```css
.button {
  padding: var(--space-2) var(--space-4); /* 8px 16px */
  gap: var(--space-2);                    /* 8px between icon and text */
}

.form-field label {
  margin-bottom: var(--space-1);           /* 4px between label and input */
}
```

### Tier 2: Inter-Component Spacing (16-32px)

Spacing between sibling components. These values express that elements are related but distinct.

**Examples:**
- Gap between cards in a grid: 16-24px
- Space between form groups (name group, address group): 24-32px
- Margin between a heading and its body text: 16px
- Gap between navigation items: 16-24px
- Space between a section title and the first content block: 16-24px

```css
.card-grid {
  gap: var(--space-6);          /* 24px between cards */
}

.form-section + .form-section {
  margin-top: var(--space-8);   /* 32px between form sections */
}
```

### Tier 3: Section Spacing (48-128px)

Spacing between major page sections. These large values create clear separation between distinct areas of content.

**Examples:**
- Margin between hero section and feature grid: 64-96px
- Padding of a page section: 48-80px vertical
- Space between the header/nav and page content: 32-48px
- Footer margin from final content section: 64-96px

```css
.page-section {
  padding-block: var(--space-16); /* 64px top and bottom */
}

.hero + .features {
  margin-top: var(--space-24);    /* 96px between hero and features */
}
```

### The Proximity Test

To verify your spatial hierarchy, apply the squint test: blur your vision and look at the layout. You should be able to identify:
- Which elements belong to the same component (tight spacing)
- Which components are siblings (medium spacing)
- Where one section ends and another begins (wide spacing)

If two different relationship levels use similar spacing, the hierarchy is ambiguous and needs adjustment.

## Density Modes

Different contexts require different spacing density. A data-heavy analytics dashboard needs tighter spacing than a marketing landing page. Density modes let you adjust the entire spatial system for a given context.

### Compact Mode

Reduces all spacing by approximately 25-33%. Used for data-dense interfaces where screen real estate is at a premium.

```css
[data-density="compact"] {
  --space-1:   2px;
  --space-2:   4px;
  --space-3:   8px;
  --space-4:   12px;
  --space-5:   16px;
  --space-6:   20px;
  --space-8:   24px;
  --space-10:  32px;
  --space-12:  40px;
  --space-16:  56px;
}
```

**Use cases:**
- Data tables with many rows
- Admin dashboards with dense widget layouts
- IDE-like interfaces with toolbars, panels, and editors
- Enterprise applications where users prioritize information density

### Default Mode

The standard spacing scale. Suitable for most interfaces.

```css
[data-density="default"] {
  --space-1:   4px;
  --space-2:   8px;
  --space-3:   12px;
  --space-4:   16px;
  --space-5:   20px;
  --space-6:   24px;
  --space-8:   32px;
  --space-10:  40px;
  --space-12:  48px;
  --space-16:  64px;
}
```

### Comfortable Mode

Increases all spacing by approximately 25-50%. Used for reading-focused and marketing interfaces where generous whitespace creates a premium feel.

```css
[data-density="comfortable"] {
  --space-1:   6px;
  --space-2:   12px;
  --space-3:   16px;
  --space-4:   24px;
  --space-5:   28px;
  --space-6:   32px;
  --space-8:   48px;
  --space-10:  56px;
  --space-12:  64px;
  --space-16:  96px;
}
```

**Use cases:**
- Marketing and landing pages
- Editorial and blog layouts
- Luxury brand interfaces
- Accessibility-focused interfaces where users benefit from more breathing room

### Implementing Density Modes

```html
<!-- Applied at the page or section level -->
<main data-density="default">
  <section data-density="compact" class="data-table-section">
    <!-- Dense data table -->
  </section>
  <section class="content-section">
    <!-- Standard spacing -->
  </section>
</main>
```

Components that reference spacing tokens automatically adapt to the density mode of their containing context.

## Spacing Token Naming

### Semantic vs Scale-Based Naming

**Scale-based naming** uses numerical indices: `--space-1`, `--space-2`, `--space-4`. This is straightforward and maps directly to the spacing scale. Developers know that `--space-4` is 16px (4 * 4px base). However, it communicates nothing about purpose.

**Semantic naming** uses descriptive names: `--space-inset-sm`, `--space-stack-md`, `--space-inline-lg`. This communicates intent but adds a layer of abstraction that teams must learn.

**Recommended approach:** Use both. Scale tokens define the raw values. Semantic tokens alias scale tokens for specific contexts.

```css
:root {
  /* Scale tokens (raw values) */
  --space-1:   4px;
  --space-2:   8px;
  --space-3:   12px;
  --space-4:   16px;
  --space-6:   24px;
  --space-8:   32px;

  /* Semantic tokens (aliased) */
  --space-inset-xs:     var(--space-1) var(--space-2);   /* Tight padding */
  --space-inset-sm:     var(--space-2) var(--space-3);   /* Small padding */
  --space-inset-md:     var(--space-3) var(--space-4);   /* Medium padding */
  --space-inset-lg:     var(--space-4) var(--space-6);   /* Large padding */

  --space-stack-xs:     var(--space-1);   /* Vertical gap: very tight */
  --space-stack-sm:     var(--space-2);   /* Vertical gap: tight */
  --space-stack-md:     var(--space-4);   /* Vertical gap: standard */
  --space-stack-lg:     var(--space-6);   /* Vertical gap: loose */
  --space-stack-xl:     var(--space-8);   /* Vertical gap: wide */

  --space-inline-xs:    var(--space-1);   /* Horizontal gap: very tight */
  --space-inline-sm:    var(--space-2);   /* Horizontal gap: tight */
  --space-inline-md:    var(--space-4);   /* Horizontal gap: standard */
  --space-inline-lg:    var(--space-6);   /* Horizontal gap: loose */
}
```

### Naming Convention Patterns

| Convention | Example | Used By |
|-----------|---------|---------|
| Numeric scale | `--space-4`, `--space-8` | Tailwind CSS |
| T-shirt sizes | `--space-sm`, `--space-md`, `--space-lg` | Many design systems |
| Semantic + size | `--space-inset-md`, `--space-stack-lg` | Salesforce Lightning |
| Multiplier | `--space-2x`, `--space-4x` | Material Design |

### Categories of Spacing Tokens

| Category | Purpose | Example |
|----------|---------|---------|
| **Inset** | Internal padding (all sides) | Button padding, card padding |
| **Stack** | Vertical spacing between elements | Space between paragraphs, form fields |
| **Inline** | Horizontal spacing between elements | Space between icon and label, nav items |
| **Gap** | Grid and flex gap values | Card grid gaps, layout gutters |
| **Section** | Large vertical spacing between sections | Page section margins |

## Spacing and Visual Rhythm

### Vertical Rhythm

Vertical rhythm means spacing between elements follows a consistent pattern, like beats in music. When every vertical space is a multiple of the same base unit, the eye perceives order and harmony.

**Implementation with baseline grid alignment:**

```css
:root {
  --baseline: 24px; /* Derived from body line-height: 16px * 1.5 */
}

h2 {
  font-size: 1.5rem;
  line-height: calc(var(--baseline) * 1.5);  /* 36px */
  margin-top: calc(var(--baseline) * 2);      /* 48px */
  margin-bottom: var(--baseline);              /* 24px */
}

p {
  margin-bottom: var(--baseline);              /* 24px */
}
```

### Horizontal Rhythm

Horizontal spacing follows the same base unit as vertical spacing, creating a unified grid.

```css
.card {
  padding: var(--space-4);         /* 16px all sides */
  gap: var(--space-3);             /* 12px between child elements */
}

.card-grid {
  gap: var(--space-6);             /* 24px between cards */
  padding-inline: var(--space-6);  /* 24px page margins */
}
```

### Spacing as Hierarchy Signal

Larger spacing draws more attention to separation. Use this to reinforce content hierarchy:
- **Tight spacing** between a heading and its paragraph says "these belong together"
- **Medium spacing** between paragraphs says "these are related but distinct thoughts"
- **Large spacing** between sections says "this is a new topic"

The relative difference matters more than the absolute values. If inter-paragraph spacing is 24px, inter-section spacing should be at least 48px (2x) to feel clearly different.

## See Also

- [[grid-patterns.md]] -- Layout patterns that use spacing tokens for gap and padding
- [[responsive-strategies.md]] -- How spacing adapts across viewport sizes
- [[../../typography-systems/references/type-scale-theory.md]] -- Aligning type scale with baseline spacing
- [[../../design-tokens/SKILL.md]] -- Encoding spacing values as cross-platform design tokens
- [[../../visual-design/references/visual-hierarchy.md]] -- Using spacing to create and reinforce visual hierarchy

**Back to:** [Grid Layout Systems Skill](../SKILL.md)

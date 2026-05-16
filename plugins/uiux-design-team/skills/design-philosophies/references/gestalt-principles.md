# Gestalt Principles

A comprehensive reference on all seven Gestalt principles of visual perception as applied to user interface design, with concrete UI examples, common violations and their fixes, and CSS implementation tips for each principle.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Overview](#overview) | 14-25 | Why Gestalt psychology matters for interface design |
| [Proximity](#proximity) | 27-58 | Spatial grouping to communicate relationships |
| [Similarity](#similarity) | 60-90 | Shared visual properties to indicate relatedness |
| [Closure](#closure) | 92-118 | Completing incomplete shapes and patterns |
| [Continuation](#continuation) | 120-146 | Guiding the eye along smooth paths |
| [Figure-Ground](#figure-ground) | 148-175 | Separating foreground elements from background |
| [Common Region](#common-region) | 177-203 | Boundary-based grouping of related elements |
| [Symmetry and Order](#symmetry-and-order) | 205-230 | Perceiving balanced, organized compositions |

## Overview

Gestalt psychology explains how the human visual system organizes individual elements into meaningful wholes. The word "Gestalt" means "form" or "shape" in German. The central insight is that perception is not a bottom-up process of assembling parts into a whole -- the brain perceives the whole first, then the parts.

For interface designers, Gestalt principles are not optional theory. They are the perceptual rules governing how every user sees your layout. When a user glances at a page and instantly understands which elements belong together, which are interactive, and what the hierarchy is -- that is Gestalt at work. When a user feels confused by a layout without knowing why -- that is usually a Gestalt violation.

Understanding these principles transforms layout decisions from guesswork into science.

## Proximity

**Principle:** Elements placed close together are perceived as belonging to the same group. Distance implies separation; closeness implies relationship.

**Why it matters in UI:** Proximity is the single most powerful grouping principle. It requires no borders, no backgrounds, no shared styling -- just space. Users will perceive items near each other as related and items far apart as unrelated, regardless of other visual properties.

### UI Applications

**Form design:** Place labels directly above or immediately beside their input fields (4-8px gap). The label-to-field distance should be significantly smaller than the field-to-field distance. When labels float too far from their fields, users associate labels with the wrong inputs.

**Card content:** Within a card, group the title and subtitle tightly (2-4px gap). Separate the content block from the action bar with a larger gap (16-24px). This creates two perceptual groups without needing a divider line.

**Navigation clusters:** Group related navigation items with minimal spacing (4-8px). Separate navigation categories with larger gaps (16-24px) or explicit dividers.

### Common Violations

| Violation | Description | Fix |
|-----------|-------------|-----|
| Equal spacing everywhere | Same gap between all elements destroys grouping signals | Vary spacing: tight within groups, generous between groups |
| Label far from field | Form labels float equidistant between two fields | Reduce label-to-field gap to 4px; increase field-to-field gap to 24px+ |
| Card with uniform padding | All internal spacing identical makes content feel like a flat list | Group related items tightly; separate sections with 2-3x the internal spacing |
| Unrelated items touching | Placing unrelated actions adjacent to each other | Add intentional space between unrelated elements |

### CSS Implementation

```css
/* Form field grouping: label close to field, fields spaced apart */
.form-field { margin-bottom: 1.5rem; }  /* between field groups */
.form-field label { margin-bottom: 0.25rem; display: block; }  /* label tight to input */

/* Card content grouping */
.card-header { margin-bottom: 0.25rem; }  /* title/subtitle tight */
.card-body { margin-top: 1rem; }          /* content separated from header */
.card-actions { margin-top: 1.5rem; }     /* actions separated from content */
```

## Similarity

**Principle:** Elements sharing visual properties -- color, size, shape, weight, or texture -- are perceived as related or belonging to the same category.

**Why it matters in UI:** Similarity establishes visual categories. When all primary buttons share the same color and shape, users learn that "blue rounded rectangle means primary action" and can find actions quickly. When similar items look different, users waste cognitive effort classifying them.

### UI Applications

**Button hierarchy:** Primary buttons share one style (filled, brand color). Secondary buttons share another (outlined). Tertiary share another (text only). This similarity within each tier and difference between tiers creates an instant visual hierarchy.

**Status indicators:** Use consistent color coding across the interface. Green always means success, red always means error, yellow always means warning. Users build a color vocabulary that accelerates comprehension.

**Data table rows:** Alternate row backgrounds (zebra striping) use similarity to group cell values within a row. Same-styled column headers use similarity to distinguish headers from data.

**Icon families:** Icons sharing the same stroke width, corner radius, and visual weight feel like a coherent set. Mixing filled and outlined icons, or icons from different families, breaks similarity and creates visual dissonance.

### Common Violations

| Violation | Description | Fix |
|-----------|-------------|-----|
| Inconsistent button styles | Primary actions styled differently across pages | Define a single button component with consistent variants |
| Mixed icon styles | Outlined icons next to filled icons in the same context | Choose one icon style and apply it consistently |
| Color overload | Too many colors used for status, making categorization impossible | Limit semantic colors to 4-5 and use them consistently |
| Typography inconsistency | Body text at different sizes on different pages | Enforce a type scale with defined sizes for each hierarchy level |

### CSS Implementation

```css
/* Consistent button hierarchy through similarity */
.btn-primary { background: var(--color-primary); color: white; border-radius: 0.375rem; }
.btn-secondary { background: transparent; color: var(--color-primary); border: 1px solid var(--color-primary); border-radius: 0.375rem; }
.btn-tertiary { background: transparent; color: var(--color-primary); border: none; border-radius: 0.375rem; }

/* Consistent status indicators */
.status-success { color: var(--color-success); }
.status-error { color: var(--color-error); }
.status-warning { color: var(--color-warning); }
.status-info { color: var(--color-info); }
```

## Closure

**Principle:** The mind fills in missing information to perceive complete shapes, even when parts are missing. We see whole forms from incomplete visual data.

**Why it matters in UI:** Closure enables designers to communicate more with less. A progress ring does not need to be fully drawn for users to understand completion percentage. A skeleton screen with gray rectangles is perceived as "content loading" because users close the pattern from context.

### UI Applications

**Progress indicators:** A circular progress indicator at 75% is perceived as a complete circle that is partially filled. Users understand the whole (complete task) from the part (filled arc).

**Skeleton screens:** Gray rectangles approximating the shape and position of content leverage closure. Users perceive "a card with a title, image, and description is loading" from abstract shapes.

**Icon design:** Many effective icons use negative space and implied shapes. The play button (triangle) is perceived as complete even without a bounding circle. The hamburger menu (three lines) is perceived as a stacked menu.

**Cropped images:** An image cropped at the edge of a viewport implies continuation beyond the visible area. This can be used deliberately to suggest more content is available by scrolling.

**Tabs and segmented controls:** Active tab connected to content area below creates closure -- the tab and content are perceived as one unit. An inactive tab separated by a border line is perceived as distinct.

### Common Violations

| Violation | Description | Fix |
|-----------|-------------|-----|
| Broken progress indicators | Progress bar without clear start/end points | Always show the full track (empty state) behind the fill |
| Ambiguous cropping | Image cropped in a way that hides important content | Crop intentionally to suggest continuation, not accidentally to obscure meaning |
| Skeleton mismatch | Skeleton shapes that do not match actual content layout | Match skeleton placeholders exactly to final content dimensions |

### CSS Implementation

```css
/* Progress ring using closure */
.progress-ring { stroke-dasharray: 251.2; /* circumference */ stroke-dashoffset: 62.8; /* 75% complete */ }

/* Skeleton screen leveraging closure */
.skeleton { background: linear-gradient(90deg, #e0e0e0 25%, #f0f0f0 50%, #e0e0e0 75%); background-size: 200% 100%; animation: shimmer 1.5s infinite; border-radius: 0.25rem; }
```

## Continuation

**Principle:** The eye follows smooth lines, curves, and paths. Elements arranged along a line or curve are perceived as related and moving in a direction.

**Why it matters in UI:** Continuation guides the user's eye through the interface in a deliberate sequence. It creates visual flow -- the sense that elements connect to each other and lead somewhere.

### UI Applications

**Stepper components:** A horizontal line connecting numbered circles creates a visual path from step 1 to step N. The eye naturally follows the line from completed steps toward the current and future steps.

**Timeline designs:** Vertical or horizontal timelines use a continuous line to connect events chronologically. The line implies sequence, causation, and progression.

**Breadcrumb navigation:** Chevron separators (>) between breadcrumb items create a left-to-right reading path that mirrors the hierarchical depth of navigation.

**Aligned content columns:** When left edges of content blocks align vertically, the eye follows the alignment edge downward, creating a reading rail that organizes the entire page. Break this alignment and the eye stutters.

**Flow diagrams:** Arrows and connecting lines between nodes leverage continuation to communicate process flow, decision trees, and system architecture.

### Common Violations

| Violation | Description | Fix |
|-----------|-------------|-----|
| Broken alignment | Content blocks with inconsistent left margins | Snap all content to a grid; maintain consistent left edges |
| Disconnected steppers | Step indicators without a connecting line | Always include the track line between steps |
| Jagged reading paths | Mixed alignments (centered, left, right) on the same page | Choose a primary alignment and maintain it |
| Timeline gaps | Events on a timeline without visual connection | Use a continuous line, even across large time gaps |

### CSS Implementation

```css
/* Stepper with continuation line */
.stepper { display: flex; align-items: center; }
.stepper-step { position: relative; }
.stepper-step + .stepper-step::before {
  content: ''; position: absolute; top: 50%; right: 100%; width: 2rem;
  height: 2px; background: var(--color-border);
}

/* Consistent left alignment rail */
.content-column { max-width: 65ch; margin-left: var(--spacing-8); }
```

## Figure-Ground

**Principle:** The visual system separates elements into foreground (figure) and background (ground). Figures are perceived as having shape and being "in front of" the ground.

**Why it matters in UI:** Figure-ground relationships create depth and hierarchy. Modals float above the page. Tooltips hover near their trigger. Selected items rise above their list. Without clear figure-ground separation, interfaces feel flat and elements compete for attention.

### UI Applications

**Modal overlays:** A modal with a dimmed backdrop (scrim) creates strong figure-ground separation. The modal is the figure; the dimmed page is the ground. The scrim communicates "this content is temporarily inaccessible" while keeping context visible.

**Card elevation:** Cards with subtle box-shadow float above the page surface. The shadow creates depth, making the card a figure against the page ground. Increased shadow on hover signals interactivity by suggesting the card is rising further from the surface.

**Dropdown menus:** Dropdown menus cast shadows and overlap page content, establishing themselves as foreground elements. The shadow edge communicates where the menu ends and the background begins.

**Selected states:** In a list, the selected item often has a distinct background color, visually pulling it forward as a figure while unselected items recede into the ground.

**Fixed headers:** A fixed header with a bottom shadow floats above scrolling content, establishing a persistent figure layer that maintains navigation context.

### Common Violations

| Violation | Description | Fix |
|-----------|-------------|-----|
| Flat modals | Modals without backdrop dim or shadow | Add a semi-transparent scrim and elevation shadow |
| Shadow soup | Every element has a heavy shadow, making nothing stand out | Reserve shadows for true figure elements; most content sits on the ground plane |
| Ambiguous layers | Overlapping elements without clear depth order | Use consistent elevation scale: page < card < dropdown < modal < toast |
| Missing focus backdrop | Focused element does not visually separate from surroundings | Use a focus ring, background shift, or subtle elevation change |

### CSS Implementation

```css
/* Elevation scale for consistent figure-ground hierarchy */
:root {
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.07);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
  --shadow-xl: 0 20px 25px rgba(0,0,0,0.15);
}
.card { box-shadow: var(--shadow-sm); }
.dropdown { box-shadow: var(--shadow-lg); }
.modal { box-shadow: var(--shadow-xl); }
.modal-scrim { background: rgba(0,0,0,0.5); }
```

## Common Region

**Principle:** Elements enclosed within a shared boundary -- a border, background color, or container -- are perceived as a group, even if they are otherwise dissimilar.

**Why it matters in UI:** Common region is a stronger grouping signal than proximity alone. A bordered card groups its contents more definitively than spacing alone. This makes common region the go-to principle for creating distinct content sections in complex interfaces.

### UI Applications

**Cards:** The most ubiquitous application of common region. A card's border or background creates a visual container that groups title, description, metadata, and actions into a single perceived unit.

**Form fieldsets:** Related form fields enclosed in a fieldset with a legend create a visual group. "Billing Address" fields inside a bordered region are instantly understood as related.

**Sections with distinct backgrounds:** Alternating section backgrounds (white, light gray, white) create regions that group content within each section without explicit borders.

**Chips and badges:** A colored pill shape around a text label creates a distinct region, making the label a discrete object that can be selected, removed, or interacted with.

**Sidebar and main content areas:** The sidebar's distinct background color creates a region that separates navigation from content, even without an explicit border.

### Common Violations

| Violation | Description | Fix |
|-----------|-------------|-----|
| Border overload | Every element has a visible border, making regions indistinguishable | Use borders sparingly; prefer background color for large regions, borders for smaller containers |
| Nested containers | Cards inside cards inside sections create confusing nesting | Limit container nesting to 2 levels maximum |
| No region differentiation | Sidebar and content area share the same background with no visual separator | Differentiate regions with background color, border, or shadow |
| Inconsistent container styles | Some cards have borders, others have shadows, others have backgrounds | Choose one container style and apply it consistently |

### CSS Implementation

```css
/* Card as common region */
.card { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: 0.5rem; padding: 1.5rem; }

/* Section alternating backgrounds */
.section:nth-child(even) { background: var(--color-surface-secondary); }
.section:nth-child(odd) { background: var(--color-surface); }

/* Form fieldset grouping */
fieldset { border: 1px solid var(--color-border-light); border-radius: 0.375rem; padding: 1rem 1.5rem; }
legend { font-weight: 600; padding: 0 0.5rem; }
```

## Symmetry and Order

**Principle:** The mind perceives objects as symmetrical forms organized around a center point. Symmetrical compositions feel stable, ordered, and balanced. Asymmetry creates tension and dynamism.

**Why it matters in UI:** Symmetry communicates stability, trust, and professionalism. It is appropriate for dashboards, enterprise tools, and content that demands credibility. Deliberate asymmetry communicates creativity, dynamism, and editorial sophistication. The key is intentionality -- accidental asymmetry reads as sloppiness.

### UI Applications

**Centered hero sections:** A centered headline, centered subtitle, and centered CTA button create a symmetrical composition that feels authoritative and focused. This is the default pattern for landing page hero sections.

**Dashboard grid layouts:** Symmetrical grid layouts with equally sized metric cards create an ordered, stable composition appropriate for data-heavy interfaces. The symmetry communicates that all metrics are equally important.

**Login and authentication pages:** Centered, symmetric forms on authentication pages communicate trust and formality. The visual stability reduces anxiety at a moment when users are sharing credentials.

**Intentional asymmetry:** Magazine-style layouts deliberately break symmetry with offset headlines, images bleeding past margins, and unequal column widths. This creates visual tension that makes the layout feel dynamic and editorial.

### Common Violations

| Violation | Description | Fix |
|-----------|-------------|-----|
| Accidental asymmetry | Elements slightly off-center or unequally spaced | Snap to grid; if centering, center precisely |
| Forced symmetry | Asymmetric content forced into symmetric containers, creating awkward spacing | If content is naturally asymmetric, embrace intentional asymmetry |
| Monotonous symmetry | Every section centered, every element balanced, creating visual boredom | Break symmetry intentionally in 1-2 sections per page for visual interest |

### CSS Implementation

```css
/* Centered symmetric hero */
.hero { text-align: center; max-width: 48rem; margin-inline: auto; }

/* Intentional asymmetric layout */
.asymmetric-hero { display: grid; grid-template-columns: 1.5fr 1fr; gap: 3rem; align-items: center; }

/* Symmetric dashboard grid */
.metrics-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem; }
```

## See Also

- [[design-thinking.md]] -- Gestalt principles inform prototyping and layout decisions during the ideation and testing phases
- [[emotional-design.md]] -- Gestalt organization contributes to the visceral response layer of emotional design
- [[dieter-rams-principles.md]] -- "Good design makes a product understandable" relies heavily on Gestalt-based visual clarity
- [[../../wireframing/references/content-hierarchy.md]] -- Content hierarchy leverages Gestalt proximity and similarity for scanning optimization
- [[../../visual-design/references/visual-hierarchy.md]] -- Visual hierarchy builds directly on Gestalt principles for weight and emphasis
- [[../../wireframing/references/layout-systems.md]] -- Layout systems apply Gestalt continuation and symmetry to structural patterns

**Back to:** [Design Philosophies Skill](../SKILL.md)

## Gestalt Principles (Moved from SKILL.md)

1. Proximity — closeness = grouping
2. Similarity — shared visual properties = related
3. Closure — mind completes incomplete shapes
4. Continuation — eye follows smooth lines
5. Figure-ground — foreground vs background
6. Common region — shared boundary = group
7. Symmetry and order — balance perceived as cohesion

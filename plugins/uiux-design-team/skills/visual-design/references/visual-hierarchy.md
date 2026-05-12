# Visual Hierarchy

Comprehensive reference for establishing clear visual hierarchy in frontend interfaces. Covers Gestalt principles, scanning patterns, visual weight, golden ratio applications, and practical exercises.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Gestalt Principles Applied](#gestalt-principles-applied) | 14-65 | Core perceptual principles with interface examples |
| [Scanning Patterns](#scanning-patterns) | 67-105 | F-pattern, Z-pattern, and research-backed eye-tracking insights |
| [Visual Weight Formulas](#visual-weight-formulas) | 107-140 | Calculating relative visual weight of interface elements |
| [Golden Ratio in Web Layout](#golden-ratio-in-web-layout) | 142-170 | Applying 1:1.618 proportions to layouts, spacing, and typography |
| [Eye-Tracking Research Insights](#eye-tracking-research-insights) | 172-195 | Key findings from usability eye-tracking studies |
| [Practical Hierarchy Exercises](#practical-hierarchy-exercises) | 197-230 | Hands-on exercises for developing hierarchy intuition |

## Gestalt Principles Applied

Gestalt psychology explains how humans perceive visual organization. These principles are not design opinions; they are descriptions of how the human visual system processes information. Leveraging them creates interfaces that feel intuitive because they align with cognitive expectations.

### Proximity

**Principle**: Elements positioned close together are perceived as belonging to a group.

**Interface applications**:
- Form fields and their labels must be closer to each other than to adjacent form groups. A label 4px from its input and 24px from the next group creates instant association.
- Card content (title, description, metadata) should have tighter internal spacing than the gap between cards. If cards have 16px internal padding, card-to-card gap should be 24px or more.
- Navigation items within a category cluster together; different categories separate with visible gaps or dividers.
- Dashboard widgets: related metrics group into a single card; unrelated metrics occupy separate cards with clear spatial separation.

**Common failure**: Equal spacing everywhere. When the gap between a label and its field equals the gap between field groups, users cannot quickly parse the form structure.

### Similarity

**Principle**: Elements sharing visual characteristics (color, size, shape, texture) are perceived as related.

**Interface applications**:
- All clickable elements share a visual trait: primary buttons share a fill color, secondary actions share an outlined style, and text links share an underline or color.
- Section headings at the same level share identical styling (font size, weight, color). A user scanning the page can instantly identify all h2-level entry points.
- Status indicators use consistent color coding across the entire application. If green means "active" in the sidebar, green means "active" everywhere.
- Data table rows: alternating background colors group every-other-row, but more importantly, the same column shares the same alignment and formatting.

**Common failure**: Styling similar elements differently because of local context. A "Save" button on page A should look identical to a "Save" button on page B.

### Figure-Ground

**Principle**: The visual system separates elements into foreground (figure) and background (ground). Foreground elements receive attention.

**Interface applications**:
- Modal overlays: the modal is figure, the dimmed page behind is ground. The dimming (typically 40-60% black overlay) establishes depth separation.
- Dropdown menus: elevated with shadow to float above the page content. Without shadow or background difference, dropdowns merge with the page and lose clarity.
- Toast notifications: appear above content with shadow and contrasting background to register as foreground events.
- Active vs. inactive tabs: the active tab should visually connect to the content below (shared background color, no bottom border) while inactive tabs recede.

**Common failure**: Flat design taken to extremes where every element sits on the same visual plane. Without depth cues, users struggle to distinguish interactive foreground elements from static backgrounds.

### Continuity

**Principle**: The eye follows the smoothest path. Elements arranged along a line or curve are perceived as related.

**Interface applications**:
- Left-aligned text creates a strong vertical line that the eye follows downward, making left-aligned layouts scannable.
- Timeline components use a vertical or horizontal line to connect events in sequence.
- Step indicators (1 > 2 > 3) use a connecting line to imply progression and relationship.
- Grid alignment: when elements share a common left edge, top edge, or baseline, they read as organized even if their sizes differ.

**Common failure**: Breaking alignment without purpose. When one element is 2px off the grid, it looks like a bug, not a design choice. Intentional grid-breaking should be dramatic enough to read as purposeful.

### Closure

**Principle**: The mind completes incomplete shapes, seeing whole forms from partial information.

**Interface applications**:
- Carousel indicators: partially visible cards at the edges imply more content beyond the viewport, inviting horizontal scroll.
- Loading skeletons: rectangular shapes with animated gradients suggest content structure before data arrives.
- Icon design: simple icons work because the mind completes the implied shape. A magnifying glass icon does not need every detail; the circle and handle are sufficient.
- Cropped images at container edges suggest continuation and create visual interest without requiring the full image.

### Common Interface Failure

**Failure**: No hierarchy at all. Every heading the same size, every button the same prominence, every section the same spacing. This forces users to read everything linearly instead of scanning. The fix is always the same: create contrast. Make one thing bigger. Make one thing bolder. Make one thing a different color. Hierarchy is created through difference.

## Scanning Patterns

Research into how users actually look at web pages reveals predictable patterns. Designing for these patterns means placing critical information where eyes naturally land.

### F-Pattern Scanning

**Context**: Text-heavy pages (articles, documentation, search results, email lists).

**Pattern**: Users read the first horizontal line across the top of the page. Then they move down and read a second horizontal line, typically shorter than the first. Finally, they scan the left side of the page in a vertical movement.

**Design implications**:
- Place the most important content in the first two lines (headline and subheadline)
- Front-load sentences with key words (users scan the first 2-3 words of each line)
- Use bold text, bullet points, and subheadings to create scannable entry points along the left edge
- Do not rely on right-side content for critical information on text-heavy pages
- Navigation placed at the top benefits from the first horizontal scan

### Z-Pattern Scanning

**Context**: Minimal pages with sparse content (landing pages, login screens, hero sections).

**Pattern**: The eye moves from top-left to top-right, then diagonally to bottom-left, then across to bottom-right, forming a Z shape.

**Design implications**:
- Top-left: logo/brand mark (first thing seen)
- Top-right: navigation or secondary CTA
- Center/diagonal: main content, hero image, or key message
- Bottom-right: primary CTA (last stop, highest conversion position)
- This pattern explains why hero sections with a left-aligned headline and a right-aligned CTA button convert well

### Layer-Cake Pattern

**Context**: Content-rich pages with clear section headers (blogs, documentation, FAQ pages).

**Pattern**: Users scan headings (horizontal lines) and skip body text (the "cake" between layers), choosing which sections to read based on heading relevance.

**Design implications**:
- Headings must be descriptively useful, not clever or vague
- Visual contrast between headings and body text must be significant (size, weight, color all contributing)
- Consistent heading hierarchy allows users to understand content depth at a glance
- Collapsible sections (accordions) work because they formalize this natural scanning behavior

## Visual Weight Formulas

Visual weight determines how much attention an element commands. Understanding what makes elements "heavier" or "lighter" allows precise control of hierarchy.

### Weight Factors

Each factor contributes to an element's visual weight:

**Size**: Larger elements are heavier. A 48px heading commands more attention than a 14px body line. The relationship is roughly proportional: doubling size approximately doubles visual weight.

**Color value**: Darker elements are heavier than lighter ones. A dark navy button (#1a365d) carries more weight than a light blue button (#bee3f8) of the same size. Saturated colors are heavier than desaturated ones.

**Contrast**: The difference between an element and its background determines weight. White text on dark backgrounds and dark text on light backgrounds both create high weight. Low-contrast elements recede.

**Density**: Elements with more visual information (icons with detail, text-heavy cards, complex illustrations) are heavier than simple elements (a thin line, a single word, an outlined icon).

**Isolation**: An element surrounded by whitespace appears heavier than the same element crowded by neighbors. This is why luxury brands use generous whitespace: it makes every element feel more important.

**Position**: Elements higher on the page carry more weight due to natural top-down reading. Elements centered horizontally carry more weight than edge-aligned elements.

### Balancing Weight Across a Layout

**Symmetrical balance**: Equal weight on both sides of a vertical axis. Both sides contain elements of similar size, color, and density. Creates stability and formality. Appropriate for institutional, conservative, or trust-focused designs.

**Asymmetrical balance**: Unequal elements balanced through compensation. A large, light image on the left balanced by small, dark text on the right. A heavy navigation bar at the top balanced by a footer with dense content. Creates dynamism and visual interest. Appropriate for creative, modern, and editorial designs.

**Radial balance**: Elements arranged around a central point. Less common in web design but useful for dashboard layouts, circular navigation patterns, or hero sections with a central focal point.

### Weight Hierarchy Rule

The primary element on any screen should have at least 2x the visual weight of secondary elements. Secondary elements should have at least 1.5x the weight of tertiary elements. This creates clear, unambiguous scanning order.

## Golden Ratio in Web Layout

The golden ratio (1:1.618, approximately 61.8% to 38.2%) produces proportions that appear naturally balanced and aesthetically pleasing.

### Two-Column Layouts

For a content area alongside a sidebar on a 1200px container:
- Content column: 1200 * 0.618 = 741px
- Sidebar column: 1200 * 0.382 = 459px
- This ratio produces a main column that feels substantial without overwhelming the sidebar

### Spacing Progressions

A golden-ratio-based spacing scale where each step is ~1.618x the previous:
- 4px, 6px, 10px, 16px, 26px, 42px, 68px, 110px
- This creates a progression that feels harmonious: the jumps between values are proportionally consistent rather than arbitrary

### Typography Scale

Using the golden ratio as the type scale multiplier:
- Base: 16px
- Level 1: 16 * 1.618 = 25.9px (round to 26px)
- Level 2: 26 * 1.618 = 42px
- Level 3: 42 * 1.618 = 68px
- This produces dramatic size contrast suited to editorial and marketing layouts

### Image Proportions

Golden ratio crop: images at 1:1.618 aspect ratio (e.g., 800 x 494px) feel naturally balanced. Useful for hero images, card thumbnails, and featured media.

### When Not to Use the Golden Ratio

The golden ratio is one tool, not a universal law. Dense data interfaces need tighter ratios. Playful designs may benefit from unexpected proportions. The golden ratio is best suited for content-focused layouts where reading comfort and visual harmony are priorities.

## Eye-Tracking Research Insights

Key findings from eye-tracking studies that inform hierarchy decisions.

### Findings from Nielsen Norman Group and Others

1. **Users spend 80% of viewing time above the fold**. Critical actions and key messages must appear without scrolling. Content below the fold is seen by fewer than half of users.

2. **The first 2-3 words of headings matter most**. When scanning, users read just the beginning of each heading before deciding to continue or skip. Front-load headings with meaningful keywords.

3. **Users fixate on images with faces**. Human faces attract attention more than any other visual element. Use faces strategically: a face near a CTA draws attention to the CTA. A face opposite the CTA draws attention away from it.

4. **Large text attracts fixation regardless of content**. Users look at large headings even when the content is not relevant to them. This is both an opportunity (guaranteed attention) and a responsibility (do not waste it with vague headlines).

5. **Bullet points increase reading engagement**. Bulleted content receives more visual attention than paragraphs. Users scan bullet lists more thoroughly than continuous prose.

6. **Whitespace increases comprehension**. Studies show that appropriate whitespace around and between paragraphs increases reading comprehension by 20%. Cramped layouts degrade both speed and understanding.

7. **Users ignore banner-like elements**. Anything that looks like an advertisement is skipped, even if it contains relevant content. Avoid designing important information in horizontal banner shapes or with stock photography treatments.

8. **Gutenberg Diagram for balanced pages**: On pages with uniform content distribution, attention follows a Z-like path with a "strong fallow area" (top-right) and "weak fallow area" (bottom-left). Place primary actions in the "terminal area" (bottom-right).

## Practical Hierarchy Exercises

These exercises develop the ability to see and create hierarchy intentionally.

### Exercise 1: The Squint Test

Blur your vision (or apply a Gaussian blur to a screenshot) and evaluate:
- Can you still identify the primary heading?
- Can you still find the main CTA?
- Do logical groups still appear grouped?
- Is there a clear top-to-bottom reading order?

If any answer is no, the hierarchy relies too heavily on text content and not enough on visual structure.

### Exercise 2: Grayscale Test

Convert the interface to grayscale and evaluate:
- Does the hierarchy still work without color?
- Can you distinguish interactive from non-interactive elements?
- Are primary and secondary actions still distinguishable?

If hierarchy collapses in grayscale, it depends too heavily on color. Hierarchy should work through size, weight, and position first, with color as reinforcement.

### Exercise 3: Five-Second Test

Show the interface to someone for five seconds, then ask:
- What is this page about?
- What is the main action you can take?
- What stood out most?

If they cannot answer these questions, the hierarchy has failed to communicate the page's purpose.

### Exercise 4: Content Priority Matrix

List every element on a page and assign a priority (1-5). Then audit:
- Does the highest-priority element have the greatest visual weight?
- Are there elements with high visual weight but low priority (visual noise)?
- Are there elements with high priority but low visual weight (buried content)?

Map priority to visual weight: 1 = hero-level prominence, 5 = fine print.

### Exercise 5: Hierarchy by Removal

Progressively remove visual hierarchy tools (color, then size differences, then weight differences, then spatial differences) and observe how the hierarchy degrades. This reveals which tools are carrying the hierarchy and which are redundant. A robust hierarchy degrades gracefully; a fragile one collapses immediately when one tool is removed.

## See Also

- [[aesthetic-principles.md]] - How aesthetic choices create and reinforce hierarchy
- [[brand-alignment.md]] - Ensuring hierarchy decisions align with brand priorities
- [[../../../typography-systems/references/type-scale-guide.md]] - Typographic hierarchy through modular scales
- [[../../../grid-layout-systems/references/grid-types.md]] - Structural hierarchy through grid systems
- [[../../../color-systems/references/contrast-requirements.md]] - Contrast ratios that ensure readable hierarchy

## Hierarchy Tools (moved from SKILL.md)

| Tool | Effect | Application |
|------|--------|-------------|
| Size | Largest = most important | Hero headlines, primary CTAs |
| Color/Contrast | High contrast = attention | Error states, active nav, primary buttons |
| Spacing | More space = more importance | Section padding, breathing room |
| Position | Top-left in LTR = first seen | Logo, primary nav, page titles |
| Weight | Bold = emphasis | Headings, key metrics |
| Motion | Movement = attention | Loading, badges, onboarding highlights |

## Gestalt-Informed Hierarchy

Proximity (group related), Similarity (consistent same-level styling), Figure-Ground (elevation/depth), Continuity (alignment axes), Closure (implied shapes for icon/logo work).

## Scanning Patterns

- F-Pattern: text-heavy pages — prioritize top + left edge.
- Z-Pattern: minimal pages — logo top-left, CTA top-right or bottom-right.

## Golden Ratio Applications

1:1.618 for content/sidebar split (61.8/38.2), spacing scale progression, type scale ratio.

## Visual Weight & Balance

- Symmetrical: formal, institutional, finance.
- Asymmetrical: dynamic, editorial; balance a large light element with a small dark one.

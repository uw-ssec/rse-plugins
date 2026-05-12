---
name: wireframing
description: Create wireframes from low-fidelity content blocks through high-fidelity layouts with proper content hierarchy, annotation conventions, responsive considerations, and common page layout patterns.
metadata:
   references:
   - references/content-hierarchy.md
   - references/layout-systems.md
   - references/wireframe-patterns.md
---

# Wireframing

Wireframes are thinking tools. They strip away color, imagery, and visual polish to focus on what matters most: content structure, layout logic, and interaction flow. A wireframe forces you to answer hard questions early -- what content goes where, what's most important, and how do users move through the interface -- before the cost of change becomes high.

Wireframes are not art. They are arguments about structure, made visible.

## Fidelity Levels

Choose your fidelity based on the decision you need to make.

### Low-Fidelity (Sketch)

Boxes, lines, and labels. No real content, no precise sizing. Created in minutes on paper or a whiteboard. Use low-fi wireframes for:
- Exploring multiple layout concepts quickly
- Facilitating team discussions about structure
- Early stakeholder alignment on page intent
- Deciding what content belongs on a page at all

Low-fi wireframes should be intentionally rough. Polish signals "this is decided" and discourages feedback on the structure itself.

### Mid-Fidelity

Real content dimensions, approximate sizing, placeholder text that represents actual content length. Created in design tools or code. Use mid-fi wireframes for:
- Testing content hierarchy with realistic proportions
- Validating navigation flows between screens
- Getting developer input on layout feasibility
- Usability testing focused on findability and flow

### High-Fidelity

Near-final layout with real or realistic content, precise spacing, actual typography sizing (though typically grayscale). Use high-fi wireframes for:
- Final layout approval before visual design
- Responsive behavior specification
- Detailed interaction annotation
- Handoff documentation for complex layouts

## Content-First Wireframing

Start every wireframe with a content priority list, not a layout. Ask:

1. What is the single most important thing on this page?
2. What must every user see without scrolling?
3. What content supports the primary action?
4. What is secondary or supplemental?
5. What can be hidden behind progressive disclosure?

Rank every content element by importance, then design the layout to serve that ranking. The layout should emerge from the content hierarchy, not the other way around.

## Common Page Layouts

### Landing Page
Hero section with value proposition and primary CTA at the top. Feature highlights (3-4 benefits with icons) in the middle. Social proof (testimonials, logos, stats) to build trust. Secondary CTA and footer. The entire page is a persuasion sequence.

### Dashboard
Metrics summary row at the top (3-5 key numbers). Primary data visualization (chart or graph) in the dominant content area. Activity feed or recent items below. Quick actions accessible without scrolling. Navigation to detailed views.

### Settings Page
Category sidebar on the left. Form-based content on the right. Group related settings under clear headings. Show current values. Provide save/cancel or auto-save with confirmation. Never require users to navigate away to save.

### List/Detail (Master-Detail)
Master list on the left or top, showing items with enough metadata to identify them. Detail panel on the right or bottom, showing full content of the selected item. Common in email clients, file managers, and admin panels.

### Form Page
Single-column layout for most forms. Group related fields with section headings. Show validation inline. Place primary action button at the bottom. For multi-step forms, show progress and allow backward navigation.

### Search Results
Search input prominent at the top. Filter panel (left sidebar or collapsible top bar). Results in a list or grid with key metadata. Pagination or infinite scroll. "No results" state with suggestions.

For detailed ASCII wireframe examples and layout rationale, see [Wireframe Patterns](references/wireframe-patterns.md).

## Annotation Conventions

Wireframes communicate through annotations. Establish consistent annotation practices.

| Annotation Type | Purpose | Format |
|----------------|---------|--------|
| **Content notes** | Explain what content goes in a region | Callout with description |
| **Interaction notes** | Describe what happens on click/tap/hover | Numbered callouts with behavior description |
| **Conditions** | Show conditional content or states | "If [condition], show [element]" |
| **Responsive notes** | Describe layout changes at breakpoints | "At mobile: stack vertically" |
| **Data notes** | Specify dynamic content sources | "Populated from user profile API" |
| **Constraints** | Character limits, image ratios, min/max | "Max 120 characters", "16:9 ratio" |

Number annotations sequentially and reference them in a separate notes panel when the wireframe gets dense.

## Responsive Wireframing

Design wireframes at three key widths to cover the responsive spectrum:

- **Mobile** (375px): Single column, stacked layout, touch targets, simplified navigation
- **Tablet** (768px): Two-column opportunities, side-by-side comparisons, expanded navigation
- **Desktop** (1280px): Full layout with sidebars, multi-column grids, hover interactions

For each breakpoint, document:
- Which elements reflow or stack
- Which elements hide or collapse (and how to access them)
- How navigation transforms (tabs to hamburger, sidebar to bottom bar)
- Touch target adjustments

See [Layout Systems](references/layout-systems.md) for common responsive layout structures.

## Deep Dive References

### [Wireframe Patterns](references/wireframe-patterns.md)

- Header & Navigation Patterns
- Hero Section Patterns
- Card Patterns
- Form Patterns
- List Patterns
- Modal & Dialog Patterns
- Sidebar Patterns
- Footer Patterns
- *...and 3 more sections*

### [Layout Systems](references/layout-systems.md)

- Common Page Layouts
- Responsive Layout Transformations
- Content Area Proportions
- Layout by Page Type
- Grid Overlays for Wireframes
- Layout Sketching Techniques

### [Content Hierarchy](references/content-hierarchy.md)

- The Hierarchy Pyramid
- Inverted Pyramid Structure
- Progressive Disclosure
- F-Pattern Content Placement
- Z-Pattern Content Placement
- Above the Fold
- Content Prioritization Matrix
- Heading Hierarchy
- *...and 3 more sections*

## Next Steps

After wireframing, refine the design and build out the system:

- **[Information Architecture](../information-architecture/SKILL.md)**: Validate that wireframe structure aligns with IA decisions
- **[Visual Design](../visual-design/SKILL.md)**: Apply visual styling, color, typography, and brand identity to wireframes
- **[Responsive Design](../responsive-design/SKILL.md)**: Implement fluid layouts and breakpoint behavior in code
- **[Design Handoff](../design-handoff/SKILL.md)**: Prepare annotated wireframes for developer implementation

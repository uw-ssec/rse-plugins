[Back to Information Architecture](../information-architecture.md)

# Navigation Design Patterns

## Overview

Navigation is the primary mechanism by which users orient themselves, find content, and accomplish goals within a digital product. Effective navigation reduces cognitive load, supports wayfinding, and scales with content growth. This reference covers global and local navigation patterns, mobile considerations, and accessibility requirements.

---

## Global Navigation Patterns

Global navigation persists across all or most pages, providing consistent access to top-level sections.

### Top Bar (Horizontal Navigation)

The most common pattern for desktop websites and web applications.

**Structure:**
```
[Logo] [Home] [Products] [Pricing] [About] [Blog]    [Search] [Login]
```

**When to use:**
- Sites with 3-8 top-level sections
- Content-focused websites (marketing, editorial, documentation)
- When primary navigation items are roughly equal in importance

**Best practices:**
- Keep items to 7 or fewer (Miller's Law)
- Place the most important items on the left (for LTR languages)
- Include utility navigation (search, login, cart) in a separate right-aligned section
- Use clear, concise labels (nouns or noun phrases, not verbs)
- Highlight the current section with a visual indicator (underline, background color, bold text)

### Sidebar (Vertical Navigation)

A persistent left-side panel containing navigation links, common in SaaS applications and admin panels.

**Structure:**
```
[Logo]
------------------
[Dashboard]
[Projects]
  > Active
  > Archived
[Team]
[Settings]
------------------
[Help]
[User Avatar]
```

**When to use:**
- Applications with 8-20+ navigation items
- Hierarchical content requiring nested sections
- Tools where users spend extended time and need constant access to navigation
- When navigation items have varying depths

**Best practices:**
- Allow collapsing to icons only for more screen space
- Group related items with visual separators or section headers
- Show active state clearly with background highlight
- Support keyboard navigation for all items
- Consider a "pinned" or "favorites" section for power users

### Hamburger Menu

A hidden navigation accessed via a three-line icon, typically in the top-left or top-right corner.

**When to use:**
- Mobile interfaces where screen space is limited
- Secondary navigation that does not need constant visibility
- When the primary task does not require frequent navigation

**Controversy and research findings:**
- Reduces discoverability by 21% compared to visible navigation (Nielsen Norman Group)
- Users under 35 recognize the icon readily; older demographics may struggle
- Works best when combined with a visible label ("Menu")
- Consider using it for secondary items while keeping primary items visible

### Tab Bar (Bottom Navigation)

A fixed bar at the bottom of the screen with 3-5 icon-and-label navigation items. Standard on mobile apps.

**Structure:**
```
[Home icon] [Search icon] [+ Create] [Messages icon] [Profile icon]
      Home      Search      Create      Messages       Profile
```

**When to use:**
- Native mobile applications
- 3-5 top-level destinations that users switch between frequently
- When all primary destinations are equally important

**Best practices:**
- Always include labels below icons (icons alone are ambiguous)
- Limit to 5 items maximum
- Highlight the active tab with color and/or fill changes
- Use a badge for unread counts or notifications
- Central item can be elevated for a primary action (floating action button pattern)

---

## Local Navigation

Local navigation helps users move within a section or page, supplementing global navigation.

### Breadcrumbs

A trail showing the user's position in the site hierarchy.

```
Home > Products > Cameras > DSLR > Canon EOS R5
```

**When to use:**
- Sites with 3+ levels of hierarchy
- E-commerce product catalogs
- Documentation and knowledge bases
- Any context where users may arrive deep in the hierarchy via search

**Best practices:**
- Use the `>` or `/` separator between levels
- Make all levels clickable except the current page
- Current page should be displayed as plain text, not a link
- Place breadcrumbs above the page title, below the global navigation
- Use `aria-label="Breadcrumb"` and `<nav>` element for accessibility
- Implement structured data (JSON-LD) for SEO

```html
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li><a href="/products/cameras">Cameras</a></li>
    <li aria-current="page">Canon EOS R5</li>
  </ol>
</nav>
```

### In-Page Navigation (Table of Contents)

A sidebar or sticky element linking to sections within a long page.

**When to use:**
- Long-form content (documentation, articles, legal pages)
- Pages with 4+ distinct sections
- When users need to jump to specific content quickly

**Best practices:**
- Use smooth scrolling with appropriate offset for fixed headers
- Highlight the active section as the user scrolls (scroll spy)
- Make it sticky so it remains visible during scrolling
- Collapse on mobile into a dropdown or expandable menu

### Pagination

Sequential navigation through a set of results or content pages.

**Patterns:**
- **Numbered pagination:** `< 1 2 3 ... 10 >` (best for known, bounded result sets)
- **Load more button:** Appends content without page change (good for browsing)
- **Infinite scroll:** Loads content automatically as user scrolls (use with caution)

**Best practices for numbered pagination:**
- Show first page, last page, current page, and 1-2 adjacent pages
- Use ellipsis for large gaps
- Clearly indicate the current page
- Include "Previous" and "Next" links with keyboard shortcuts
- Show total result count when possible

**Infinite scroll warnings:**
- Prevents access to footer content
- Makes it impossible to bookmark a position
- Can cause performance issues with very large lists
- Breaks the back button expectation
- Use a hybrid approach: load more button with optional auto-load

---

## Navigation Depth vs Breadth Tradeoffs

### Broad Navigation (Shallow Hierarchy)

Many items at the top level with few sub-levels.

```
Level 1: 12 items
Level 2: 3-5 items each
Total depth: 2 levels
```

**Advantages:**
- Fewer clicks to reach any destination
- More items visible at once
- Lower interaction cost

**Disadvantages:**
- Can overwhelm users with too many choices (Hick's Law)
- Requires more screen space
- Harder to scale as content grows

### Deep Navigation (Narrow Hierarchy)

Few items at each level with many sub-levels.

```
Level 1: 4 items
Level 2: 4 items each
Level 3: 4 items each
Level 4: 4 items each
Total depth: 4 levels
```

**Advantages:**
- Each choice is simpler (fewer options at each level)
- Uses less screen space
- Easier to add new content without restructuring

**Disadvantages:**
- More clicks to reach content
- Users lose context of where they are
- Higher abandonment rates at each level

### Research-Based Guidance

Studies consistently show that **broader, shallower hierarchies** outperform deeper ones:
- Users navigate faster with broader menus (Larson & Czerwinski, 1998)
- Optimal range: 5-9 items per level, 2-3 levels deep
- Beyond 3 levels, provide alternative access paths (search, shortcuts, cross-links)

---

## Mega Menus

Large, multi-column dropdown panels that display many navigation options at once.

### When to Use

- Sites with extensive content (100+ pages across 6+ categories)
- E-commerce with many product categories and subcategories
- When users benefit from seeing the full breadth of options at once

### Structure

```
+------------------------------------------------------------------+
| [Category 1]     | [Category 2]     | [Category 3]    | [Promo] |
|  - Subcategory A |  - Subcategory D |  - Subcategory G | [Image] |
|  - Subcategory B |  - Subcategory E |  - Subcategory H |         |
|  - Subcategory C |  - Subcategory F |  - Subcategory I |         |
+------------------------------------------------------------------+
```

### Best Practices

- Organize content in clear columns with group headers
- Limit to a single level of subcategories within the mega menu
- Include visual hierarchy (bold group headers, indented sub-items)
- Add a featured/promotional area for key content or offers
- Ensure the mega menu stays open long enough for mouse traversal
- Use a delay (300-500ms) before closing to prevent accidental dismissal
- Implement proper keyboard navigation (arrow keys, Tab, Escape to close)

---

## Faceted Navigation for Complex Sites

Faceted navigation allows users to filter content by multiple attributes simultaneously. Essential for e-commerce, job boards, real estate, and any domain with multi-dimensional content.

### Structure

```
Filters:
  Category: [Electronics] [Clothing] [Home]
  Price: [$0-50] [$50-100] [$100-500] [$500+]
  Brand: [Apple] [Samsung] [Sony] [LG]
  Rating: [4+ stars] [3+ stars]
  Availability: [In stock] [Pre-order]

Applied filters: Electronics x | $50-100 x | In stock x    [Clear all]
```

### Design Principles

- Show the number of results for each filter value before selection
- Allow multiple selections within and across facets
- Display applied filters prominently with easy removal (X button)
- Update results immediately (or with a clear "Apply" action for complex filtering)
- Preserve filter state in the URL for sharing and bookmarking
- Sort facet values by relevance or count, not just alphabetically
- Collapse less-used facets; expand the most commonly used ones by default

---

## Mobile Navigation Patterns

### Priority+ Pattern

Show as many navigation items as space allows; overflow items go into a "More" menu.

```
[Home] [Products] [Pricing] [More ...]
                                |-> About
                                |-> Blog
                                |-> Contact
```

**Best for:** Responsive sites transitioning from desktop to mobile without a complete redesign.

### Swipe/Scrollable Tabs

A horizontal row of tabs that can be swiped left/right to reveal more options.

**Best for:** Content categories (news, shopping), when all items are peers.

### Drill-Down Navigation

Full-screen menus that reveal sub-levels one at a time with a back button.

```
Screen 1: [Products] [Services] [About]
  -> tap Products
Screen 2: <- Back | [Software] [Hardware] [Accessories]
  -> tap Software
Screen 3: <- Back | [Design Tools] [Dev Tools] [Analytics]
```

**Best for:** Deep hierarchies on mobile; e-commerce category browsing.

### Gesture-Based Navigation

Swipe gestures for forward/back, pull-to-refresh, long-press for options.

**Caution:** Always provide visible alternatives to gesture-based navigation. Gestures are not discoverable and may conflict with OS-level gestures.

---

## Accessibility Requirements

### ARIA Landmarks

Use semantic HTML and ARIA landmarks so screen readers can identify and jump to navigation regions.

```html
<header role="banner">
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/products" aria-current="page">Products</a></li>
      <li><a href="/about">About</a></li>
    </ul>
  </nav>
</header>

<nav aria-label="Breadcrumb">
  <!-- breadcrumb content -->
</nav>

<aside>
  <nav aria-label="Section navigation">
    <!-- sidebar/local nav -->
  </nav>
</aside>
```

**Key rules:**
- Use `<nav>` elements for navigation regions
- Add unique `aria-label` when multiple `<nav>` elements exist on the same page
- Use `aria-current="page"` to indicate the current page
- Use `role="menubar"` and `role="menu"` only for true application menus, not website navigation

### Skip Links

Provide a mechanism to bypass repetitive navigation and jump to main content.

```html
<body>
  <a href="#main-content" class="skip-link">Skip to main content</a>
  <nav><!-- navigation --></nav>
  <main id="main-content">
    <!-- page content -->
  </main>
</body>
```

```css
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  padding: 8px 16px;
  background: #000;
  color: #fff;
  z-index: 100;
}
.skip-link:focus {
  top: 0;
}
```

### Keyboard Navigation

All navigation must be fully operable with a keyboard.

**Requirements:**
- All interactive elements reachable via Tab key
- Logical tab order matching visual order
- Enter or Space activates links and buttons
- Arrow keys navigate within menus and tab bars
- Escape closes dropdown menus and overlays
- Visible focus indicator on all focusable elements (minimum 2px outline, 3:1 contrast ratio per WCAG 2.2)

### Focus Management for Dynamic Navigation

When navigation changes the page content without a full page load:
- Move focus to the new content area or a heading within it
- Announce page changes to screen readers via `aria-live` regions
- Ensure the back button works as expected (update browser history)

### Color and Contrast

- Active/current navigation indicators must not rely solely on color
- Text in navigation must meet WCAG AA contrast ratio (4.5:1 for normal text, 3:1 for large text)
- Focus indicators must have 3:1 contrast against adjacent colors
- Hover states should be distinguishable from active/focus states

---

## Navigation Audit Checklist

- [ ] Primary navigation is accessible within one interaction from any page
- [ ] Current location is clearly indicated in the navigation
- [ ] Labels are concise, user-tested, and free of jargon
- [ ] Navigation structure reflects user mental models (validated via card sorting)
- [ ] Mobile navigation is functional and tested on real devices
- [ ] All navigation is keyboard accessible
- [ ] ARIA landmarks and labels are correctly implemented
- [ ] Skip links are present and functional
- [ ] Search is available as an alternative to browsing navigation
- [ ] Navigation scales gracefully as content grows

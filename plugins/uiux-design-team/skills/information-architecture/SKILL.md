---
name: information-architecture
description: Design information architecture including sitemaps, navigation patterns, taxonomy, card sorting, content hierarchy, labeling systems, and wayfinding to structure how users find and understand content.
metadata:
   references:
   - references/card-sorting-methods.md
   - references/navigation-guide.md
   - references/sitemap-patterns.md
---

# Information Architecture

Information architecture (IA) is the structural design of shared information environments. It determines how content is organized, labeled, and connected so that users can find what they need and understand where they are. Poor IA is the silent killer of usability: users don't complain about "bad information architecture" -- they say "I can't find anything" or "this doesn't make sense."

Good IA makes content findable, understandable, and navigable. It bridges the gap between user mental models and system organization, turning chaotic content into coherent experiences.

## Quick Start: Creating a Sitemap

When starting a new project or restructuring an existing one, follow this sequence:

1. **Inventory content** -- List every page, feature, and content type that exists or will exist
2. **Identify user goals** -- What are users trying to accomplish? What do they search for?
3. **Run a card sort** -- Have users group and label content (see [Card Sorting Methods](references/card-sorting-methods.md))
4. **Draft the sitemap** -- Organize content into a hierarchy based on sort results and business priorities
5. **Validate with tree testing** -- Give users tasks and see if they can navigate the hierarchy without a UI
6. **Define labeling** -- Choose clear, unambiguous labels for every category and page
7. **Design navigation** -- Translate the sitemap into navigation patterns (see [Navigation Guide](references/navigation-guide.md))

## Navigation Patterns

The navigation model you choose depends on content volume, user tasks, and device context. Each pattern has distinct strengths.

### Hierarchical (Tree)

Content organized in parent-child relationships with multiple depth levels. Best for large content sites, documentation portals, and enterprise applications with many feature areas. Keep depth to 3-4 levels maximum; users lose orientation beyond that.

### Flat

All primary destinations at the same level with no nesting. Best for applications with 4-7 core sections of equal importance. Common in mobile apps where a bottom tab bar provides direct access to every major area.

### Hub-and-Spoke

A central hub (home screen or dashboard) from which users navigate to discrete task areas and return. Best for mobile apps with independent task flows (banking: accounts, transfers, payments, settings) where cross-section navigation is rare.

### Sequential (Linear)

Users progress through content in a defined order. Best for onboarding flows, checkout processes, wizards, and educational content where steps build on each other. Always show progress and allow backward navigation.

### Faceted

Multiple simultaneous classification schemes let users filter and combine attributes. Best for e-commerce, search-heavy applications, and content libraries with many items sharing multiple attributes (size, color, price, rating).

For comprehensive navigation implementation guidance, see [Navigation Guide](references/navigation-guide.md).

## Content Hierarchy Principles

### Progressive Disclosure

Show only what users need at each level of engagement. Start with a summary or overview, then let users drill into details on demand. This reduces cognitive load and keeps interfaces clean while still providing depth for users who need it.

- **Level 1**: Title, thumbnail, key metadata (list view)
- **Level 2**: Summary, primary actions, important details (expanded/detail view)
- **Level 3**: Full content, secondary actions, related items (deep dive)

### Information Scent

Users follow "information scent" -- cues that signal whether a path will lead to their goal. Strong scent means clear labels, descriptive link text, and preview content that helps users predict what they'll find. Weak scent causes pogo-sticking (clicking back and forth) and abandonment.

Strengthen scent by:
- Using descriptive labels instead of clever or branded terms
- Adding contextual descriptions to navigation items
- Showing content previews (snippets, thumbnails, metadata)
- Making search results rich with context

## Labeling Systems

Labels are the words you use to represent categories, navigation items, and content groups. They are the most visible expression of your IA.

### Labeling Principles

| Principle | Description | Example |
|-----------|-------------|---------|
| **Clarity** | Labels must be unambiguous | "Pricing" not "Plans & Solutions" |
| **Consistency** | Same concept = same label everywhere | Don't mix "Settings" and "Preferences" |
| **User language** | Match how users think and speak | "Help" not "Knowledge Base" (unless your audience expects it) |
| **Mutual exclusivity** | Categories shouldn't overlap | "Shoes" and "Footwear" in the same nav is confusing |
| **Scannability** | Front-load meaningful words | "Account Settings" not "Settings for Your Account" |

### Label Testing

Before committing to labels, test them:
- **First-click testing**: Show users a task and see which label they click first
- **Highlight testing**: Ask users to highlight the label they'd click for a given task
- **Card sorting**: Have users label groups they've created (reveals their vocabulary)

## Sitemap Patterns

Different content structures demand different sitemap shapes. Understanding these patterns helps you choose the right foundation. See [Sitemap Patterns](references/sitemap-patterns.md) for detailed diagrams and examples.

## Card Sorting

Card sorting is the foundational IA research method. It reveals how users naturally group and think about content, preventing you from imposing an internal organizational structure that makes sense to the business but confuses users. See [Card Sorting Methods](references/card-sorting-methods.md) for methodology details.

## Deep Dive References

### [Sitemap Patterns](references/sitemap-patterns.md)

- Overview
- Hierarchical Sitemaps
- Flat Sitemaps
- Hub-and-Spoke
- Sequential / Linear
- Matrix / Faceted
- Content Inventory Template
- Page Naming Conventions
- *...and 3 more sections*

### [Navigation Guide](references/navigation-guide.md)

- Overview
- Global Navigation Patterns
- Local Navigation
- Navigation Depth vs Breadth Tradeoffs
- Mega Menus
- Faceted Navigation for Complex Sites
- Mobile Navigation Patterns
- Accessibility Requirements
- *...and 1 more sections*

### [Card Sorting Methods](references/card-sorting-methods.md)

- Overview
- Open Card Sorting
- Closed Card Sorting
- Hybrid Card Sorting
- Tools and Facilitation
- Participant Recruitment
- Analysis Methods
- Online vs In-Person
- *...and 9 more sections*

## Next Steps

After defining the information architecture, move into detailed structural design:

- **[Wireframing](../wireframing/SKILL.md)**: Translate IA into page layouts with content hierarchy and annotation
- **[User Research](../user-research/SKILL.md)**: Validate IA decisions with real users through testing and observation
- **[UX Writing](../ux-writing/SKILL.md)**: Craft clear labels, microcopy, and content that reinforces the IA

[Back to Design Handoff](../../design-handoff.md)

# Design Annotation Guide

## Overview

Design annotations bridge the gap between visual design and development implementation. Well-annotated designs reduce guesswork, prevent misinterpretation, and accelerate development. This guide covers what to annotate, how to annotate it, and tools for creating developer-readable specifications.

---

## What to Annotate

### Spacing and Layout

Every spacing value that is not immediately obvious from the design should be annotated.

**Required annotations:**
- Margins between major sections
- Padding within containers (cards, buttons, inputs)
- Gap between grid items
- Spacing between text elements (heading to body, label to input)
- Alignment references (center-aligned, left-aligned, baseline)

```
Annotation format:
┌─────────────────────────────────┐
│  ← 24px →  Card Title          │
│             ↕ 8px               │
│  ← 24px →  Card description    │
│             ↕ 16px              │
│  ← 24px →  [Button]   → 24px  │
│             ↕ 24px              │
└─────────────────────────────────┘
     ↕ 32px (gap between cards)
```

### Colors

Annotate colors using design token names, not raw hex values. This ensures developers reference the token system rather than hardcoding values.

**Format:**
```
Background: surface-primary (#ffffff)
Text: text-primary (#1a1a2e)
Border: border-default (#e2e8f0)
Button background: interactive-primary (#0056b3)
Button text: text-on-primary (#ffffff)
```

### Typography

**Required annotations per text element:**
- Font family (or token name)
- Font weight
- Font size (px and/or rem)
- Line height
- Letter spacing (if non-default)
- Text color token

**Example:**
```
Heading:
  Font: Inter SemiBold
  Size: 24px / 1.5rem
  Line height: 32px / 1.33
  Color: text-primary
  Token: heading-lg

Body:
  Font: Inter Regular
  Size: 16px / 1rem
  Line height: 24px / 1.5
  Color: text-secondary
  Token: body-md
```

### Interactions

**Annotate all interactive states:**

| State | What to Specify |
|-------|----------------|
| Default | Base appearance (often implicit from the design) |
| Hover | Color changes, shadows, transforms, cursor type |
| Focus | Focus ring style, outline width, offset, color |
| Active/Pressed | Scale, color shift, shadow reduction |
| Disabled | Opacity, color changes, cursor type |
| Loading | Spinner placement, skeleton state, disabled interactions |
| Error | Border color, error message position, icon |
| Selected | Background, border, checkmark, or other indicator |

**Interaction annotation example:**
```
Button States:
  Default:  bg: interactive-primary, text: text-on-primary, border-radius: 8px
  Hover:    bg: interactive-primary-hover, shadow: shadow-md
  Focus:    outline: 3px solid focus-ring, offset: 2px
  Active:   bg: interactive-primary-pressed, shadow: none
  Disabled: bg: surface-disabled, text: text-disabled, opacity: 1
  Loading:  spinner replaces label text, button width maintained
```

### Responsive Behavior

**Annotate breakpoint-specific changes:**

```
Breakpoints:
  Mobile (< 768px):
    - Cards stack vertically, full width
    - Navigation collapses to hamburger menu
    - Sidebar hidden, accessible via drawer
    - Font size: heading-lg reduces to heading-md

  Tablet (768px - 1024px):
    - Cards: 2-column grid, 16px gap
    - Sidebar visible as collapsed icons
    - Navigation remains visible

  Desktop (> 1024px):
    - Cards: 3-column grid, 24px gap
    - Sidebar fully expanded
    - Navigation fully visible with dropdowns
```

**Annotate responsive rules:**
- Which elements reflow, stack, or hide at each breakpoint
- How navigation transforms (full to hamburger)
- Image aspect ratio changes
- Typography scale adjustments
- Spacing changes (tighter on mobile, wider on desktop)

---

## Annotation Tools and Methods

### Design Tool Annotations

**Figma:**
- Use the built-in measurement tool (hover between elements with Option/Alt held)
- Create annotation components with consistent styling
- Use auto-layout frames to show spacing values
- Leverage Figma's Dev Mode for automatic spec generation
- Name layers semantically (developers see layer names in inspect mode)

**Annotation component library:**
```
Create reusable annotation components:
├── Spacing indicator (red lines with pixel values)
├── Color swatch (token name + hex value)
├── Typography spec (font, size, weight, line-height)
├── Interaction note (state descriptions)
├── Responsive note (breakpoint behavior)
├── Accessibility note (ARIA roles, keyboard behavior)
└── Developer note (implementation guidance)
```

### Third-Party Annotation Tools

| Tool | Platform | Features |
|------|----------|----------|
| **Figma Dev Mode** | Figma | Auto-generated specs, code snippets, design tokens |
| **Zeplin** | Standalone | Design spec generation, style guide, asset export |
| **Storybook** | Code-based | Living documentation alongside component code |
| **Supernova** | Standalone | Design system documentation from Figma |

---

## Developer-Readable Specifications

### Specification Document Structure

```
Component: [Component Name]
Version: [Design version]
Last updated: [Date]
Designer: [Name]
Status: Ready for development

## Visual Specifications
- Layout diagram with spacing values
- Color specifications (tokens)
- Typography specifications (tokens)
- Border radius, shadows, other decorative properties

## Interaction Specifications
- State diagram (default → hover → active → focus)
- Animation specifications (duration, easing, properties)
- Keyboard behavior
- Screen reader announcements

## Responsive Specifications
- Breakpoint behaviors
- Layout transformations
- Element visibility changes

## Content Specifications
- Maximum character counts
- Truncation behavior
- Empty state content
- Error state content

## Accessibility Specifications
- ARIA roles and properties
- Keyboard navigation pattern
- Focus management
- Screen reader behavior

## Edge Cases
- Long content handling
- Missing data handling
- Error states
- Loading states
```

---

## Interactive Prototype Annotations

### What to Document in Prototypes

Prototypes show flow and interaction, but they need annotations to communicate timing, easing, and behavior details that are not self-evident.

**Transition annotations:**
```
Page transition:
  Type: Slide from right
  Duration: 300ms
  Easing: ease-out (cubic-bezier(0, 0, 0.2, 1))
  Trigger: Navigation link click

Modal open:
  Type: Fade in + scale from 0.95
  Duration: 200ms
  Easing: ease-out
  Backdrop: Fade to rgba(0,0,0,0.5) over 200ms
  Trigger: Button click

Modal close:
  Type: Fade out + scale to 0.95
  Duration: 150ms
  Easing: ease-in
  Focus: Returns to trigger button
  Trigger: Close button, Escape key, backdrop click
```

---

## Accessibility Annotations

### What to Annotate for Accessibility

| Element | Annotation Needed |
|---------|------------------|
| Images | Alt text (or mark as decorative) |
| Icons | Whether meaningful (needs label) or decorative (aria-hidden) |
| Headings | Heading level (h1, h2, h3) |
| Landmarks | Role assignments (nav, main, aside, footer) |
| Forms | Label associations, error messages, required indicators |
| Custom widgets | ARIA role, keyboard pattern reference |
| Dynamic content | Live region type (polite, assertive) |
| Focus order | Tab sequence, especially for complex layouts |
| Skip links | Target and label |
| Color meaning | Non-color alternatives specified |

**Annotation example:**
```
Search Component:
  - Input: role="combobox", aria-label="Search products"
  - Suggestions: role="listbox", aria-live="polite"
  - Each suggestion: role="option"
  - Keyboard: Arrow Up/Down to navigate, Enter to select, Escape to close
  - Focus: Returns to input after selection
  - Screen reader: "X suggestions available" announced on filter
```

---

## Motion Specifications

### How to Document Motion

```
Motion Specification:
  Property:    transform: translateY
  From:        translateY(16px), opacity: 0
  To:          translateY(0), opacity: 1
  Duration:    200ms
  Easing:      cubic-bezier(0.0, 0.0, 0.2, 1)  (ease-out)
  Delay:       0ms (or stagger: 50ms between items)
  Trigger:     Element enters viewport
  Reduced motion: No animation, instant display
```

**Easing quick reference:**
| Name | Value | Use |
|------|-------|-----|
| Ease out | cubic-bezier(0, 0, 0.2, 1) | Elements entering |
| Ease in | cubic-bezier(0.4, 0, 1, 1) | Elements exiting |
| Ease in-out | cubic-bezier(0.4, 0, 0.2, 1) | Elements moving |
| Spring | Custom per framework | Bouncy, playful interactions |

---

## Edge Case Documentation

### What Edge Cases to Document

1. **Long content:** What happens when text exceeds expected length? (Truncate with ellipsis, wrap, scroll)
2. **Empty states:** What appears when there is no data?
3. **Error states:** What does each error look like? Where does the error message appear?
4. **Loading states:** Skeleton screens, spinners, or progressive loading?
5. **Missing images:** Fallback placeholder or icon
6. **Permissions:** What appears when a user lacks permission?
7. **First-time use:** Onboarding state vs. populated state
8. **Maximum items:** What happens with 1 item, 10 items, 100 items, 1000 items?
9. **Offline state:** What is available without connectivity?
10. **Internationalization:** RTL layout, text expansion, date/number formatting

---

## Version Control for Annotations

### Maintaining Annotation Currency

- **Version number:** Include in every annotation spec document
- **Change log:** Track what changed between versions
- **Status labels:** Draft, In Review, Ready for Dev, Implemented, QA Approved
- **Figma branching:** Use Figma branches for design iterations; merge when approved
- **Link to tickets:** Every annotation should reference the related development ticket
- **Archive old versions:** Keep previous versions accessible for reference

### Handoff Workflow

```
1. Designer completes visual design
2. Designer adds annotations (spacing, colors, typography, interactions)
3. Designer adds accessibility annotations
4. Designer adds responsive specifications
5. Design review with another designer (annotations reviewed)
6. Developer review (developers ask questions, annotations updated)
7. Annotations marked "Ready for Development"
8. Development begins (questions resolved via annotation comments)
9. Design QA against annotations
10. Annotations marked "Implemented"
```

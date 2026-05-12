---
name: component-library
description: Build component libraries with composition patterns, variant systems using CVA, state management for UI components, accessibility requirements per component, Storybook documentation, and visual regression testing.
metadata:
   references:
   - references/composition-patterns.md
   - references/state-management.md
   - references/variant-systems.md
---

# Component Library

A component library is the implementation of a design system. While the design system defines the rules -- tokens, principles, patterns -- the component library is the code that enforces them. Every component encapsulates structure, style, behavior, and accessibility into a reusable unit that teams consume to build interfaces.

A well-built component library eliminates the most expensive form of technical debt: inconsistency. When every button, modal, and form field comes from a shared library, changes propagate everywhere, accessibility is baked in, and new features ship faster because developers compose from existing parts rather than building from scratch.

## Component Inventory Methodology

Before building, understand what you have and what you need.

### Audit Process

1. **Screenshot every screen** in the current product. Group screenshots by page type (dashboard, settings, forms, lists).
2. **Extract unique components**: Identify every distinct UI element. A "distinct" element is one that differs in structure, behavior, or purpose -- not just color or size.
3. **Catalog variants**: For each component, document all observed variations. Three different button styles means three variants of one Button component, not three components.
4. **Score by priority**: Use a 2x2 matrix of **frequency** (how many screens use it) and **inconsistency** (how many unintentional variants exist). High-frequency, high-inconsistency components get built first.

### Recommended Build Order

Start with the components everything else depends on:

1. **Design tokens** (consumed by all components)
2. **Layout primitives** (Box, Stack, Flex, Grid)
3. **Typography** (Heading, Text, Label)
4. **Button** (most used interactive element)
5. **Input, Select, Checkbox, Radio** (form foundation)
6. **Card, Modal, Drawer** (container components)
7. **Table, List** (data display)
8. **Navigation components** (Nav, Tabs, Breadcrumbs)

## Composition Patterns

How components are structured internally determines how flexible and maintainable they are. See [Composition Patterns](references/composition-patterns.md) for detailed guidance.

### Compound Components

A parent component manages shared state while child components handle rendering. Like `<Select>` containing `<Option>` elements. The parent provides context; children consume it.

### Headless Components

Logic-only components that provide behavior without any rendered UI. Consumers supply all markup and styling. Libraries like Radix UI and Headless UI follow this pattern. Maximum flexibility at the cost of more consumer effort.

### Slots and Children

Named insertion points where consumers inject custom content. Vue and Svelte have native slot syntax. In React, use children for the default slot and named props (e.g., `header`, `footer`) for additional slots.

## Variant Systems with CVA

Class Variance Authority (CVA) provides a structured way to define component variants when using utility-first CSS like Tailwind.

```typescript
import { cva } from "class-variance-authority";

const button = cva("inline-flex items-center justify-center font-medium", {
  variants: {
    variant: {
      solid: "bg-primary text-white",
      outline: "border-2 border-primary text-primary",
      ghost: "text-primary hover:bg-primary/10",
    },
    size: {
      sm: "h-8 px-3 text-sm",
      md: "h-10 px-4 text-base",
      lg: "h-12 px-6 text-lg",
    },
  },
  defaultVariants: {
    variant: "solid",
    size: "md",
  },
});
```

For detailed CVA patterns and alternatives, see [Variant Systems](references/variant-systems.md).

## Component States

Every interactive component must handle multiple states. Designing for the "happy path" alone creates fragile interfaces.

| State | Description | Design Requirement |
|-------|-------------|-------------------|
| **Empty** | No data to display | Helpful message, illustration, action to add data |
| **Loading** | Data is being fetched | Skeleton, spinner, or progress indicator |
| **Partial** | Some data loaded, more available | Render available data, indicate more exists |
| **Error** | Something went wrong | Clear error message, recovery action, retry option |
| **Ideal** | Everything works as expected | Full content displayed as designed |
| **Disabled** | Interaction is not available | Reduced opacity, no pointer events, tooltip explaining why |
| **Hover** | Pointer is over the element | Visual feedback (color shift, elevation change) |
| **Focus** | Keyboard focus is on the element | Visible focus ring (required for accessibility) |
| **Active/Pressed** | Element is being clicked or tapped | Compressed or darkened appearance |

For comprehensive state management patterns, see [State Management](references/state-management.md).

## Accessibility Per Component Type

Accessibility is not an add-on. Every component must meet these requirements at the library level.

| Component | Key Requirements |
|-----------|-----------------|
| **Button** | Proper role, disabled state announced, loading state announced, keyboard activation (Enter/Space) |
| **Input** | Associated label (for/id or aria-labelledby), error state linked (aria-describedby), required announced |
| **Modal** | Focus trap, Escape to close, focus returns to trigger, aria-modal, announced on open |
| **Tabs** | role=tablist/tab/tabpanel, arrow key navigation, active tab state announced |
| **Dropdown** | role=listbox or menu, arrow key navigation, typeahead, Escape to close |
| **Toast** | role=alert or aria-live=polite, auto-dismiss with sufficient time, dismiss action |
| **Table** | Proper th/td semantics, scope attributes, sortable column announcement |

## Documentation with Storybook

Every component in the library needs a Storybook story that serves as both documentation and a testing surface.

### Story Requirements

- **Default story**: Component with default props
- **All variants**: One story per variant combination (or use Controls addon)
- **States**: Stories for loading, error, disabled, empty states
- **Responsive**: Stories showing component at different widths
- **Accessibility**: Include a11y addon panel showing automated audit results
- **Usage docs**: MDX page with guidelines, do/don't examples, code snippets

## Visual Regression Testing

Prevent unintended visual changes with automated screenshot comparison.

- **Chromatic** or **Percy**: Cloud-based visual testing that captures screenshots of every Storybook story
- **Playwright screenshot tests**: Local visual regression with pixel comparison
- Run visual tests on every pull request. Require approval for any visual diff.

## Deep Dive References

### [Composition Patterns](references/composition-patterns.md)

- Compound Components
- Render Props and Slots
- Headless Components
- Provider Pattern
- Controlled vs Uncontrolled
- Forwarding Refs
- Polymorphic Components

### [Variant Systems](references/variant-systems.md)

- CVA Detailed Usage
- Compound Variants
- Tailwind Integration
- Alternative Approaches
- Type-Safe Variant APIs
- Variant Documentation Patterns

### [State Management](references/state-management.md)

- The Five UI States
- State Machines
- Controlled vs Uncontrolled Components
- Optimistic Updates
- Form State Management
- Loading State Patterns

## Next Steps

After building the component library, integrate and expand:

- **[Design System Creation](../design-system-creation/SKILL.md)**: Ensure the library aligns with the broader design system governance
- **[Design Tokens](../design-tokens/SKILL.md)**: Consume tokens correctly and contribute component tokens back to the system
- **[Frontend Components](../frontend-components/SKILL.md)**: Implementation-specific guidance for React, Vue, and Svelte components
- **[Accessibility Audit](../accessibility-audit/SKILL.md)**: Validate component accessibility with automated and manual testing

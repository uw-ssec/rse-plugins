---
name: create-design-system
description: Design system initialization workflow covering pattern audit, design principles, token architecture, color palette, type scale, spacing scale, and foundational component creation.
user-invocable: true
allowed-tools: []
---

# Design System Initialization

Create a design system from the ground up, led by @design-systems-engineer. This command walks through auditing existing patterns, defining principles, creating a token architecture, and building foundational components with documentation.

## When to Use This Command

- Starting a new product and need a consistent design foundation
- Consolidating inconsistent styles across an existing product
- Migrating from ad-hoc CSS to a systematic approach
- Building a shared design language across multiple products
- Establishing design-to-code standards for a team

## Workflow

### Step 1: Audit Existing Patterns

@design-systems-engineer catalogs what currently exists using the `design-system-creation` skill.

**If there is an existing product:**

1. **Visual audit**: Screenshot every unique page/view and catalog:
   - How many unique font sizes are in use?
   - How many unique colors are in use?
   - How many unique spacing values are in use?
   - How many button variants exist?
   - How many form input styles exist?

2. **Code audit**: Scan stylesheets for:
   - Unique color values (hex, rgb, hsl, named)
   - Unique font-size declarations
   - Unique spacing values (margin, padding, gap)
   - Unique border-radius values
   - Unique shadow definitions
   - Unique z-index values

3. **Inconsistency report**:
   ```
   Colors:     [X] unique values found → Target: [Y] tokens
   Font sizes: [X] unique values found → Target: [Y] scale steps
   Spacing:    [X] unique values found → Target: [Y] scale steps
   Components: [X] unique variants found → Target: [Y] standardized
   ```

**If starting fresh:**
- Define the product type (marketing site, SaaS app, mobile app, design tool)
- Identify the visual tone (minimal, expressive, corporate, playful)
- List reference products or design systems for inspiration

### Step 2: Define Design Principles

@design-systems-engineer establishes 3-5 principles that guide every design decision.

**Principle format:**
```
[Principle Name]: [One-sentence definition]
This means: [Concrete implication for design decisions]
This does NOT mean: [Common misinterpretation to avoid]
```

**Example principles:**
```
Clarity First: Every element must communicate its purpose without explanation.
This means: Labels are explicit, icons have text companions, states are visually distinct.
This does NOT mean: The interface is boring or stripped of personality.

Progressive Disclosure: Show only what is needed, when it is needed.
This means: Advanced options are accessible but not overwhelming.
This does NOT mean: Features are hidden or hard to find.

Accessible by Default: Accessibility is a baseline requirement, not an enhancement.
This means: Every component meets WCAG 2.2 AA before it is considered complete.
This does NOT mean: Visual design is compromised.
```

### Step 3: Create Token Architecture

@design-systems-engineer builds a three-tier token system using the `design-tokens` skill.

**Tier 1: Global Tokens (Raw Values)**
The complete palette of available values. These are never used directly in components.

```css
/* Global color tokens */
--color-blue-50: #eff6ff;
--color-blue-100: #dbeafe;
--color-blue-200: #bfdbfe;
--color-blue-500: #3b82f6;
--color-blue-600: #2563eb;
--color-blue-700: #1d4ed8;
--color-blue-900: #1e3a5f;
--color-blue-950: #172554;

/* Global spacing tokens */
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
```

**Tier 2: Alias Tokens (Semantic Meaning)**
Map global tokens to purpose. These are what components reference.

```css
/* Alias color tokens */
--color-primary: var(--color-blue-600);
--color-primary-hover: var(--color-blue-700);
--color-surface: var(--color-neutral-50);
--color-text-primary: var(--color-neutral-900);
--color-text-secondary: var(--color-neutral-600);
--color-border: var(--color-neutral-200);
--color-error: var(--color-red-600);
--color-success: var(--color-green-600);

/* Alias spacing tokens */
--space-inline-sm: var(--space-2);
--space-inline-md: var(--space-4);
--space-stack-sm: var(--space-2);
--space-stack-md: var(--space-4);
--space-stack-lg: var(--space-8);
```

**Tier 3: Component Tokens (Scoped to Components)**
Override alias tokens for specific component needs.

```css
/* Button component tokens */
--button-padding-x: var(--space-inline-md);
--button-padding-y: var(--space-2);
--button-radius: var(--radius-md);
--button-font-size: var(--text-sm);
--button-font-weight: var(--font-semibold);
```

### Step 4: Define Color Palette

@design-systems-engineer builds the color system using the `color-systems` skill.

**Required color scales:**

1. **Primary**: Brand color with full 50-950 scale
2. **Neutral**: Gray scale with brand undertone for backgrounds, text, borders
3. **Semantic colors**:
   - Success (green) - Confirmations, positive states
   - Warning (amber/yellow) - Caution states, attention needed
   - Error (red) - Errors, destructive actions, validation failures
   - Info (blue) - Informational messages, neutral alerts

**For each color, verify:**
- Text on background passes 4.5:1 contrast (AA)
- Large text on background passes 3:1 contrast (AA)
- Adjacent UI components have 3:1 contrast

See `/generate-palette` for detailed palette generation.

### Step 5: Define Typography Scale

@design-systems-engineer creates the type system using the `typography-systems` skill.

**Type scale definition:**

```css
--text-xs:   clamp(0.75rem, 0.7rem + 0.25vw, 0.8125rem);    /* 12-13px */
--text-sm:   clamp(0.875rem, 0.825rem + 0.25vw, 0.9375rem);  /* 14-15px */
--text-base: clamp(1rem, 0.95rem + 0.25vw, 1.0625rem);       /* 16-17px */
--text-lg:   clamp(1.125rem, 1.05rem + 0.375vw, 1.25rem);    /* 18-20px */
--text-xl:   clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem);        /* 20-24px */
--text-2xl:  clamp(1.5rem, 1.3rem + 1vw, 2rem);              /* 24-32px */
--text-3xl:  clamp(1.875rem, 1.6rem + 1.375vw, 2.5rem);      /* 30-40px */
--text-4xl:  clamp(2.25rem, 1.85rem + 2vw, 3rem);            /* 36-48px */
```

**Line height pairings:**
- Body text: 1.5-1.6
- Headings: 1.1-1.3
- UI elements: 1.25

**Font weight scale:**
```css
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

See `/create-type-scale` for detailed typography generation.

### Step 6: Define Spacing Scale

@design-systems-engineer defines consistent spacing.

**Base unit**: 4px (0.25rem)

**Scale:**
| Token | Value | Use Case |
|-------|-------|----------|
| `--space-0.5` | 2px | Tight inline spacing |
| `--space-1` | 4px | Icon-to-text gap, tight padding |
| `--space-2` | 8px | Default inline padding, related elements |
| `--space-3` | 12px | Comfortable inline padding |
| `--space-4` | 16px | Default block spacing, card padding |
| `--space-6` | 24px | Section padding, group separation |
| `--space-8` | 32px | Major section separation |
| `--space-12` | 48px | Page section breaks |
| `--space-16` | 64px | Hero/feature section padding |

**Related scales:**
- Border radius: `--radius-sm` (4px), `--radius-md` (8px), `--radius-lg` (12px), `--radius-full` (9999px)
- Shadows: `--shadow-sm`, `--shadow-md`, `--shadow-lg` (elevation levels)
- Z-index: `--z-dropdown` (10), `--z-sticky` (20), `--z-modal` (30), `--z-toast` (40)

### Step 7: Build Foundational Components

@design-systems-engineer creates the base components using the `component-library` skill.

**Priority components (build these first):**

1. **Button** - Primary, secondary, ghost, destructive variants; sm/md/lg sizes; with icon support; all states (hover, focus, active, disabled, loading)

2. **Input** - Text, email, password, number, textarea; with label, helper text, error message; required/optional indicators; all states

3. **Card** - Container with optional header, body, footer; padding variants; border and shadow options

**For each component, document:**
- Visual specification (spacing, colors, typography)
- All variants and their use cases
- All states (default, hover, focus, active, disabled, loading, error)
- Accessibility requirements (roles, labels, keyboard behavior)
- Code implementation (semantic HTML + CSS using design tokens)
- Usage guidelines (when to use, when not to use)

### Step 8: Document Usage

@design-systems-engineer creates documentation for the system.

**Documentation structure:**
1. **Getting started**: How to install and use the tokens and components
2. **Principles**: The design principles that guide the system
3. **Tokens**: Complete token reference with examples
4. **Components**: Component API, variants, examples, and guidelines
5. **Patterns**: Common layout and interaction patterns
6. **Contributing**: How to propose changes or new components

## Cross-Plugin Bridge (PROACTIVE)

A design system must be buildable by engineering from day one. PROACTIVELY engage the **frontend-engineering-team** throughout the creation process:

- **During token architecture (Step 3):** Route to **@build-tooling-specialist** to validate token architecture maps to Tailwind configuration and build tooling. Tokens that engineering cannot consume are theoretical.
- **During color and typography (Steps 4-5):** Route to **@performance-engineer** for font loading performance assessment and **@build-tooling-specialist** for Tailwind theme configuration.
- **During component building (Step 7):** Route to **@react-specialist** for component architecture patterns (Server vs Client boundaries, hooks, composition), **@typescript-architect** for type-safe component prop APIs with generics, and **@testing-engineer** for component test strategy (Testing Library, visual regression, accessibility testing).
- **During documentation (Step 8):** Route to **@frontend-lead** to ensure engineering documentation (usage in code, TypeScript interfaces, test examples) accompanies design documentation.

## Related Skills

- `design-system-creation` - Design system methodology and governance
- `design-tokens` - Token architecture and management
- `color-systems` - Color palette generation and management
- `typography-systems` - Type scale creation and font pairing
- `component-library` - Component design and documentation
- `css-architecture` - CSS organization and methodology

## Related Commands

- `/generate-palette` - Create an accessible color palette
- `/create-type-scale` - Generate a typography system
- `/design-handoff` - Document components for developer implementation

## Tips

- Start small and expand. Three solid components are worth more than thirty incomplete ones.
- Tokens are the foundation. Get the token architecture right before building components.
- Every component must meet WCAG 2.2 AA before it is considered complete.
- Document decisions, not just outcomes. Future contributors need to understand the "why."
- Version your design system. Breaking changes need migration guides.

# Material Design

A comprehensive reference on Material Design 3, covering the Dynamic Color system, type system, component library, motion system, elevation system, customization with Material Theme Builder, and guidance on when to follow versus deviate from the system.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Material Design Philosophy](#material-design-philosophy) | 14-30 | The physical material metaphor and its evolution to MD3 |
| [Dynamic Color System](#dynamic-color-system) | 32-75 | Color roles, tonal palettes, and personalized theming |
| [Type System](#type-system) | 77-110 | Type scale, roles, and implementation |
| [Component Library](#component-library) | 112-150 | Key components, states, and customization guidance |
| [Motion System](#motion-system) | 152-180 | Transition patterns, easing, and duration tokens |
| [Elevation System](#elevation-system) | 182-205 | Surface tonal elevation and shadow model |
| [Material Theme Builder](#material-theme-builder) | 207-225 | Customizing Material for brand identity |
| [When to Follow vs. Deviate](#when-to-follow-vs-deviate) | 227-250 | Decision framework for Material adoption |

## Material Design Philosophy

Material Design began in 2014 as Google's design language, built on a physical material metaphor -- surfaces that cast shadows, respond to touch, and occupy layered space. Material 2 refined the system with a comprehensive component library and theming capabilities. Material 3 (Material You), launched in 2021 and refined through 2025, represents the most significant evolution: personalization through Dynamic Color, expressive typography, and a more flexible component system.

The core metaphor remains: interfaces are made of material surfaces that exist in 3D space. These surfaces have physical properties -- they cast shadows, stack on top of each other, and respond to interaction with visual feedback. Motion communicates spatial relationships and causality. Color communicates hierarchy, state, and brand.

Material's greatest strength is systematic completeness. Every component, every state, every platform consideration is documented. This makes Material an excellent starting point for any product, even if the final design deviates significantly from Material's visual language.

Material's greatest weakness is recognizability. Strict adherence produces interfaces that feel generically "Googley." The challenge is using Material's system while creating a distinctive identity.

## Dynamic Color System

Material 3's Dynamic Color system generates an entire color scheme from a single source color. This enables personalized theming (generating palettes from the user's wallpaper on Android) and ensures consistent, accessible color relationships.

### Color Roles

Material 3 defines specific color roles rather than generic color names. Each role has a defined function:

| Role | Usage | Relationship |
|------|-------|--------------|
| `primary` | Key components, active states, FAB | Brand's main color |
| `on-primary` | Text/icons on primary surfaces | Accessible contrast against primary |
| `primary-container` | Filled tonal buttons, active indicators | Lighter tint of primary |
| `on-primary-container` | Text on primary-container | Accessible contrast against primary-container |
| `secondary` | Less prominent components, filters | Complementary to primary |
| `secondary-container` | Tonal fills for secondary elements | Lighter tint of secondary |
| `tertiary` | Accent and contrast elements | Triadic relationship to primary |
| `error` | Error states, destructive actions | Typically red, independent of primary |
| `surface` | Page and card backgrounds | Neutral, low-chroma |
| `on-surface` | Text on surface backgrounds | High contrast against surface |
| `surface-variant` | Dividers, outlines, disabled states | Slightly different from surface |
| `outline` | Borders, dividers | Visible against surface and surface-variant |

### Tonal Palettes

Each source color generates a 13-tone palette from 0 (black) to 100 (white). The tones are: 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99, 100. Color roles map to specific tones:

- Light theme: `primary` = tone 40, `on-primary` = tone 100, `primary-container` = tone 90, `on-primary-container` = tone 10
- Dark theme: `primary` = tone 80, `on-primary` = tone 20, `primary-container` = tone 30, `on-primary-container` = tone 90

This mapping guarantees accessible contrast ratios between each color and its "on" counterpart regardless of the source color.

### Custom Color Implementation

```css
:root {
  /* Generated from Material Theme Builder */
  --md-sys-color-primary: #6750a4;
  --md-sys-color-on-primary: #ffffff;
  --md-sys-color-primary-container: #eaddff;
  --md-sys-color-on-primary-container: #21005d;
  --md-sys-color-secondary: #625b71;
  --md-sys-color-surface: #fffbfe;
  --md-sys-color-on-surface: #1c1b1f;
  --md-sys-color-surface-variant: #e7e0ec;
  --md-sys-color-outline: #79747e;
  --md-sys-color-error: #b3261e;
}

/* Dark theme overrides */
@media (prefers-color-scheme: dark) {
  :root {
    --md-sys-color-primary: #d0bcff;
    --md-sys-color-on-primary: #381e72;
    --md-sys-color-primary-container: #4f378b;
    --md-sys-color-on-primary-container: #eaddff;
    --md-sys-color-surface: #1c1b1f;
    --md-sys-color-on-surface: #e6e1e5;
  }
}
```

## Type System

Material 3 defines a type scale with 5 categories and 3 sizes each (large, medium, small), producing 15 type styles:

| Category | Usage | Typical Font |
|----------|-------|-------------|
| Display | Hero text, large numbers, prominent headings | Display or serif font |
| Headline | Section headings, page titles | Display or sans-serif |
| Title | Card titles, dialog headers, sub-sections | Sans-serif, medium weight |
| Body | Paragraph text, descriptions, form labels | Sans-serif, regular weight |
| Label | Buttons, chips, tabs, navigation items | Sans-serif, medium weight |

### Type Scale Values

| Style | Size | Weight | Line Height | Tracking |
|-------|------|--------|-------------|----------|
| Display Large | 57px | 400 | 64px | -0.25px |
| Display Medium | 45px | 400 | 52px | 0 |
| Display Small | 36px | 400 | 44px | 0 |
| Headline Large | 32px | 400 | 40px | 0 |
| Headline Medium | 28px | 400 | 36px | 0 |
| Headline Small | 24px | 400 | 32px | 0 |
| Title Large | 22px | 400 | 28px | 0 |
| Title Medium | 16px | 500 | 24px | 0.15px |
| Title Small | 14px | 500 | 20px | 0.1px |
| Body Large | 16px | 400 | 24px | 0.5px |
| Body Medium | 14px | 400 | 20px | 0.25px |
| Body Small | 12px | 400 | 16px | 0.4px |
| Label Large | 14px | 500 | 20px | 0.1px |
| Label Medium | 12px | 500 | 16px | 0.5px |
| Label Small | 11px | 500 | 16px | 0.5px |

Material 3 encourages using a distinctive display font paired with a readable body font to create brand differentiation within the system.

## Component Library

Material 3 provides a comprehensive set of components. Each component has defined states, anatomy, and guidelines.

### Key Component Categories

**Actions:** FAB (floating action button), extended FAB, filled button, tonal button, outlined button, text button, icon button, segmented button.

**Communication:** Badges, progress indicators (linear and circular), snackbar, tooltip.

**Containment:** Bottom sheet, card (elevated, filled, outlined), dialog, side sheet, carousel.

**Navigation:** Bottom app bar, navigation bar, navigation drawer, navigation rail, tabs, top app bar.

**Selection:** Checkbox, chip (assist, filter, input, suggestion), date picker, menu, radio button, slider, switch, time picker.

**Text Input:** Filled text field, outlined text field, search bar.

### Component State System

Every Material component supports a consistent set of states:

| State | Visual Change | Applies To |
|-------|--------------|-----------|
| Enabled | Default appearance | All interactive components |
| Disabled | Reduced opacity (38%), no interaction | All interactive components |
| Hovered | State layer at 8% opacity over surface | All interactive components |
| Focused | State layer at 10% opacity, focus indicator | All interactive components |
| Pressed | State layer at 10% opacity, ripple effect | All interactive components |
| Dragged | State layer at 16% opacity, elevated | Draggable components |
| Selected | Filled or tonal variant, check indicator | Selection components |
| Error | Error color applied to container and text | Input components |

### Customization Guidance

Material components are designed to be customized. The recommended approach:

1. **Use the component structure** (anatomy, states, interaction patterns) as-is
2. **Customize visual properties** (color, shape, typography) through the theme
3. **Extend with custom components** when Material's library does not cover a need
4. **Do not fight the system** -- if a Material component's behavior does not match your need, build a custom component rather than hacking a Material one

## Motion System

Material 3's motion system uses transitions to reinforce spatial relationships, provide feedback, and guide attention. Motion should feel natural, not decorative.

### Transition Patterns

| Pattern | Duration | Easing | Use When |
|---------|----------|--------|----------|
| Enter | 250ms | Emphasized decelerate | Element appears (dialog, sheet, menu) |
| Exit | 200ms | Emphasized accelerate | Element disappears |
| Shared axis (forward) | 300ms | Standard easing | Moving forward in a sequence (onboarding) |
| Shared axis (backward) | 300ms | Standard easing | Moving backward in a sequence |
| Container transform | 300ms | Standard easing | Element expands into a new context (card to detail) |
| Fade through | 300ms | Standard easing | Unrelated content replacing other content (tab switch) |

### Easing Curves

Material 3 defines named easing functions:

| Name | CSS Curve | Usage |
|------|----------|-------|
| Standard | `cubic-bezier(0.2, 0, 0, 1)` | Most transitions |
| Standard decelerate | `cubic-bezier(0, 0, 0, 1)` | Elements entering from off-screen |
| Standard accelerate | `cubic-bezier(0.3, 0, 1, 1)` | Elements leaving to off-screen |
| Emphasized | `cubic-bezier(0.2, 0, 0, 1)` | Important, attention-grabbing transitions |
| Emphasized decelerate | `cubic-bezier(0.05, 0.7, 0.1, 1)` | Emphasized entry |
| Emphasized accelerate | `cubic-bezier(0.3, 0, 0.8, 0.15)` | Emphasized exit |

### Duration Tokens

| Token | Duration | Usage |
|-------|----------|-------|
| Short 1 | 50ms | Micro-interactions (state layers) |
| Short 2 | 100ms | Small component transitions |
| Short 3 | 150ms | Medium component transitions |
| Short 4 | 200ms | Exit transitions |
| Medium 1 | 250ms | Standard transitions |
| Medium 2 | 300ms | Complex transitions |
| Medium 3 | 350ms | Page-level transitions |
| Medium 4 | 400ms | Large container transforms |
| Long 1-4 | 450-700ms | Full-screen transitions |

## Elevation System

Material 3 uses tonal elevation rather than shadow-only elevation. Instead of relying solely on drop shadows to communicate depth, elevated surfaces receive a tonal color overlay that becomes more visible at higher elevation levels.

### Elevation Levels

| Level | Shadow | Tonal Overlay | Usage |
|-------|--------|--------------|-------|
| Level 0 | None | None | Page background |
| Level 1 | 1dp | Surface + 5% primary | Cards, navigation rail |
| Level 2 | 3dp | Surface + 8% primary | Elevated cards, top app bar (scrolled) |
| Level 3 | 6dp | Surface + 11% primary | FAB, navigation bar |
| Level 4 | 8dp | Surface + 12% primary | (Reserved) |
| Level 5 | 12dp | Surface + 14% primary | Navigation drawer, side sheet |

In dark themes, tonal elevation is particularly important because shadows are less visible against dark backgrounds. The tonal overlay ensures elevated surfaces remain distinguishable.

```css
/* Tonal elevation in CSS */
.surface-level-0 { background: var(--md-sys-color-surface); }
.surface-level-1 { background: color-mix(in srgb, var(--md-sys-color-primary) 5%, var(--md-sys-color-surface)); box-shadow: 0 1px 2px rgba(0,0,0,0.3); }
.surface-level-2 { background: color-mix(in srgb, var(--md-sys-color-primary) 8%, var(--md-sys-color-surface)); box-shadow: 0 1px 3px rgba(0,0,0,0.3); }
.surface-level-3 { background: color-mix(in srgb, var(--md-sys-color-primary) 11%, var(--md-sys-color-surface)); box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
```

## Material Theme Builder

Material Theme Builder is Google's tool for generating custom Material 3 themes from a source color. It produces color tokens for both light and dark themes with guaranteed accessibility.

### Customization Process

1. **Choose a source color**: Enter your brand's primary color. The builder generates the complete tonal palette.
2. **Review generated roles**: Examine primary, secondary, tertiary, and neutral palettes. Adjust if the generated secondary or tertiary colors conflict with your brand.
3. **Add custom colors**: For semantic colors beyond the default set (e.g., a specific "warning" orange), add custom color slots.
4. **Export tokens**: Export as CSS custom properties, Android XML, Compose theme, or design tool tokens.
5. **Test in context**: Apply the generated theme to actual screens and verify that the color roles work in your specific UI context.

### What to Customize

| Element | Customization Level | Guidance |
|---------|-------------------|----------|
| Source color | Always | Use your brand's primary color |
| Typography | Always | Swap default fonts for brand fonts |
| Shape (corner radius) | Usually | Adjust from Material's rounded default if needed |
| Component structure | Rarely | Changing component anatomy breaks user expectations |
| State behavior | Never | Hover, focus, disabled states should follow Material conventions |
| Color role mapping | Rarely | The role-to-tone mapping is designed for accessibility |

## When to Follow vs. Deviate

### Follow Material When

- Building for **Android**: Material is the expected design language. Users notice non-Material apps.
- Building **cross-platform** products: Material provides the most comprehensive, platform-agnostic system.
- Working with **limited design resources**: Material's completeness reduces design decisions. Use the system as-is and customize with theme builder.
- Building **enterprise/productivity** tools: Material's systematic approach handles complex UIs well.
- **Prototyping rapidly**: Material's component library enables fast, consistent prototyping.

### Deviate From Material When

- Building for **iOS only**: Apple HIG is expected. Material on iOS feels foreign to Apple users.
- Building a **brand-forward consumer product**: Material's recognizability can overshadow brand identity. Use Material's structural patterns but create custom visual language.
- Creating a **reading-focused product**: Material's component density and surface model can compete with content. Simplify the chrome.
- Building **marketing pages**: Material is designed for applications, not marketing. Landing pages need more visual expression than Material's system provides.
- When Material's opinionated choices **conflict with user research**: If testing shows Material's pattern does not work for your users, user evidence trumps system guidelines.

### The Hybrid Approach

The most practical approach for many teams: use Material's **system architecture** (color roles, type scale, elevation model, state system) while creating **custom visual execution** (brand colors, brand typography, custom component styling). This gives you the rigor of a complete design system with the distinctiveness of custom design.

## See Also

- [[apple-hig.md]] -- Compare Material's approach to Apple's Human Interface Guidelines for platform-specific decisions
- [[dieter-rams-principles.md]] -- Material Design operationalizes many of Rams' principles at component level
- [[gestalt-principles.md]] -- Material's spatial model relies on Gestalt figure-ground and common region
- [[../../design-case-studies/references/mobile-apps.md]] -- Case studies of Material Design implemented in production apps
- [[../../design-case-studies/references/design-systems-in-practice.md]] -- Compare Material to other production design systems
- [[../../responsive-design/references/breakpoint-strategy.md]] -- Material's responsive layout grid and breakpoint system

**Back to:** [Design Philosophies Skill](../SKILL.md)

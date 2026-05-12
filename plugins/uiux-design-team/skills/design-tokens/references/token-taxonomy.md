[Back to Design Tokens](../index.md)

# Design Token Taxonomy

A complete classification of all token types used in design systems, organized by tier and category.

---

## Token Tiers Overview

```
Global Tokens (Primitives)
    |
    v
Alias Tokens (Semantic Mappings)
    |
    v
Component Tokens (Specific Bindings)
```

---

## Global Tokens (Primitive Palette)

Global tokens define the raw design values. They have no semantic meaning and are named by their visual characteristics.

### Color Palette

```json
{
  "color": {
    "blue": {
      "50": { "value": "#eff6ff" },
      "100": { "value": "#dbeafe" },
      "200": { "value": "#bfdbfe" },
      "300": { "value": "#93c5fd" },
      "400": { "value": "#60a5fa" },
      "500": { "value": "#3b82f6" },
      "600": { "value": "#2563eb" },
      "700": { "value": "#1d4ed8" },
      "800": { "value": "#1e40af" },
      "900": { "value": "#1e3a8a" },
      "950": { "value": "#172554" }
    },
    "gray": {
      "50": { "value": "#f9fafb" },
      "100": { "value": "#f3f4f6" },
      "200": { "value": "#e5e7eb" },
      "300": { "value": "#d1d5db" },
      "400": { "value": "#9ca3af" },
      "500": { "value": "#6b7280" },
      "600": { "value": "#4b5563" },
      "700": { "value": "#374151" },
      "800": { "value": "#1f2937" },
      "900": { "value": "#111827" },
      "950": { "value": "#030712" }
    },
    "red": { "500": { "value": "#ef4444" }, "600": { "value": "#dc2626" }, "700": { "value": "#b91c1c" } },
    "green": { "500": { "value": "#22c55e" }, "600": { "value": "#16a34a" }, "700": { "value": "#15803d" } },
    "yellow": { "500": { "value": "#eab308" }, "600": { "value": "#ca8a04" } },
    "white": { "value": "#ffffff" },
    "black": { "value": "#000000" }
  }
}
```

---

## Alias Tokens (Semantic Mappings)

Alias tokens map primitives to functional names. They answer "what is this token for?" rather than "what does this token look like?"

### Color Semantics

```json
{
  "color": {
    "text": {
      "primary": { "value": "{color.gray.900}", "description": "Default body text" },
      "secondary": { "value": "{color.gray.500}", "description": "Supporting text, captions" },
      "tertiary": { "value": "{color.gray.400}", "description": "Placeholder text, hints" },
      "inverse": { "value": "{color.white}", "description": "Text on dark backgrounds" },
      "brand": { "value": "{color.blue.600}", "description": "Branded text, links" },
      "error": { "value": "{color.red.600}", "description": "Error messages" },
      "success": { "value": "{color.green.600}", "description": "Success messages" },
      "warning": { "value": "{color.yellow.600}", "description": "Warning messages" }
    },
    "background": {
      "default": { "value": "{color.white}", "description": "Page background" },
      "subtle": { "value": "{color.gray.50}", "description": "Slightly tinted background" },
      "muted": { "value": "{color.gray.100}", "description": "Distinct background sections" },
      "inverse": { "value": "{color.gray.900}", "description": "Dark background sections" },
      "brand": { "value": "{color.blue.600}", "description": "Branded background areas" },
      "error": { "value": "{color.red.50}", "description": "Error state background" },
      "success": { "value": "{color.green.50}", "description": "Success state background" },
      "warning": { "value": "{color.yellow.50}", "description": "Warning state background" }
    },
    "border": {
      "default": { "value": "{color.gray.200}" },
      "strong": { "value": "{color.gray.400}" },
      "brand": { "value": "{color.blue.600}" },
      "error": { "value": "{color.red.500}" }
    },
    "interactive": {
      "default": { "value": "{color.blue.600}" },
      "hover": { "value": "{color.blue.700}" },
      "active": { "value": "{color.blue.800}" },
      "disabled": { "value": "{color.gray.300}" }
    }
  }
}
```

---

## Component Tokens (Specific Bindings)

Component tokens bind semantic tokens to specific component properties.

```json
{
  "button": {
    "primary": {
      "bg": { "value": "{color.interactive.default}" },
      "bg-hover": { "value": "{color.interactive.hover}" },
      "bg-active": { "value": "{color.interactive.active}" },
      "text": { "value": "{color.text.inverse}" },
      "border": { "value": "transparent" }
    },
    "ghost": {
      "bg": { "value": "transparent" },
      "bg-hover": { "value": "{color.background.subtle}" },
      "text": { "value": "{color.text.primary}" }
    },
    "border-radius": { "value": "{border.radius.md}" },
    "font-weight": { "value": "{font.weight.medium}" },
    "padding-x-sm": { "value": "{spacing.3}" },
    "padding-x-md": { "value": "{spacing.4}" },
    "padding-x-lg": { "value": "{spacing.6}" }
  },
  "input": {
    "bg": { "value": "{color.background.default}" },
    "border": { "value": "{color.border.default}" },
    "border-focus": { "value": "{color.interactive.default}" },
    "border-error": { "value": "{color.border.error}" },
    "text": { "value": "{color.text.primary}" },
    "placeholder": { "value": "{color.text.tertiary}" },
    "border-radius": { "value": "{border.radius.md}" }
  }
}
```

---

## Spacing Tokens (Scale)

A consistent spacing scale ensures uniform rhythm across the entire UI.

```json
{
  "spacing": {
    "0": { "value": "0px", "description": "No spacing" },
    "px": { "value": "1px", "description": "Hairline spacing" },
    "0.5": { "value": "2px" },
    "1": { "value": "4px", "description": "Tightest spacing" },
    "1.5": { "value": "6px" },
    "2": { "value": "8px", "description": "Compact internal spacing" },
    "3": { "value": "12px" },
    "4": { "value": "16px", "description": "Standard internal spacing" },
    "5": { "value": "20px" },
    "6": { "value": "24px", "description": "Comfortable spacing" },
    "8": { "value": "32px", "description": "Section spacing" },
    "10": { "value": "40px" },
    "12": { "value": "48px" },
    "16": { "value": "64px", "description": "Large section spacing" },
    "20": { "value": "80px" },
    "24": { "value": "96px", "description": "Page-level spacing" }
  }
}
```

### Spacing Scale Rationale

Most spacing scales follow a 4px base unit. Each step is a multiple of 4:

```
4  8  12  16  20  24  32  40  48  64  80  96
```

This creates visual consistency and makes alignment predictable.

---

## Typography Tokens

### Font Family

```json
{
  "font": {
    "family": {
      "sans": { "value": "'Inter', system-ui, -apple-system, sans-serif" },
      "serif": { "value": "'Merriweather', Georgia, serif" },
      "mono": { "value": "'JetBrains Mono', 'Fira Code', monospace" }
    }
  }
}
```

### Font Size

```json
{
  "font": {
    "size": {
      "xs": { "value": "0.75rem", "description": "12px -- fine print" },
      "sm": { "value": "0.875rem", "description": "14px -- secondary text" },
      "base": { "value": "1rem", "description": "16px -- body text" },
      "lg": { "value": "1.125rem", "description": "18px -- large body" },
      "xl": { "value": "1.25rem", "description": "20px -- subheadings" },
      "2xl": { "value": "1.5rem", "description": "24px -- section headings" },
      "3xl": { "value": "1.875rem", "description": "30px -- page headings" },
      "4xl": { "value": "2.25rem", "description": "36px -- hero headings" },
      "5xl": { "value": "3rem", "description": "48px -- display headings" }
    }
  }
}
```

### Font Weight, Line Height, Letter Spacing

```json
{
  "font": {
    "weight": {
      "light": { "value": "300" },
      "normal": { "value": "400" },
      "medium": { "value": "500" },
      "semibold": { "value": "600" },
      "bold": { "value": "700" }
    },
    "line-height": {
      "none": { "value": "1" },
      "tight": { "value": "1.25" },
      "snug": { "value": "1.375" },
      "normal": { "value": "1.5" },
      "relaxed": { "value": "1.625" },
      "loose": { "value": "2" }
    },
    "letter-spacing": {
      "tighter": { "value": "-0.05em" },
      "tight": { "value": "-0.025em" },
      "normal": { "value": "0em" },
      "wide": { "value": "0.025em" },
      "wider": { "value": "0.05em" },
      "widest": { "value": "0.1em" }
    }
  }
}
```

---

## Shadow Tokens

```json
{
  "shadow": {
    "none": { "value": "none" },
    "xs": { "value": "0 1px 2px 0 rgba(0, 0, 0, 0.05)" },
    "sm": { "value": "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1)" },
    "md": { "value": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)" },
    "lg": { "value": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1)" },
    "xl": { "value": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)" },
    "inner": { "value": "inset 0 2px 4px 0 rgba(0, 0, 0, 0.05)" }
  }
}
```

---

## Border Tokens

### Width

```json
{
  "border": {
    "width": {
      "none": { "value": "0" },
      "thin": { "value": "1px" },
      "medium": { "value": "2px" },
      "thick": { "value": "4px" }
    }
  }
}
```

### Radius

```json
{
  "border": {
    "radius": {
      "none": { "value": "0" },
      "sm": { "value": "0.25rem" },
      "md": { "value": "0.5rem" },
      "lg": { "value": "0.75rem" },
      "xl": { "value": "1rem" },
      "2xl": { "value": "1.5rem" },
      "full": { "value": "9999px" }
    }
  }
}
```

### Style

```json
{
  "border": {
    "style": {
      "solid": { "value": "solid" },
      "dashed": { "value": "dashed" },
      "dotted": { "value": "dotted" }
    }
  }
}
```

---

## Motion Tokens

### Duration

```json
{
  "motion": {
    "duration": {
      "instant": { "value": "0ms", "description": "No animation" },
      "fast": { "value": "100ms", "description": "Micro-interactions (hover, toggle)" },
      "normal": { "value": "200ms", "description": "Standard transitions" },
      "slow": { "value": "400ms", "description": "Complex transitions (modals, panels)" },
      "slower": { "value": "600ms", "description": "Large element transitions" }
    }
  }
}
```

### Easing

```json
{
  "motion": {
    "easing": {
      "default": { "value": "cubic-bezier(0.4, 0, 0.2, 1)", "description": "Standard ease in-out" },
      "in": { "value": "cubic-bezier(0.4, 0, 1, 1)", "description": "Accelerating (entering)" },
      "out": { "value": "cubic-bezier(0, 0, 0.2, 1)", "description": "Decelerating (exiting)" },
      "linear": { "value": "linear", "description": "Constant speed" },
      "spring": { "value": "cubic-bezier(0.34, 1.56, 0.64, 1)", "description": "Bouncy, playful feel" }
    }
  }
}
```

---

## Breakpoint Tokens

```json
{
  "breakpoint": {
    "xs": { "value": "475px", "description": "Large phones" },
    "sm": { "value": "640px", "description": "Small tablets" },
    "md": { "value": "768px", "description": "Tablets" },
    "lg": { "value": "1024px", "description": "Laptops" },
    "xl": { "value": "1280px", "description": "Desktops" },
    "2xl": { "value": "1536px", "description": "Large desktops" }
  }
}
```

Note: Breakpoints are typically not output as CSS custom properties (since `@media` queries cannot use custom properties). They are used in Sass variables, JS constants, or Tailwind config.

---

## Z-Index Tokens

A controlled z-index scale prevents z-index wars.

```json
{
  "z-index": {
    "hide": { "value": "-1", "description": "Hidden behind content" },
    "base": { "value": "0", "description": "Default stacking" },
    "raised": { "value": "1", "description": "Slightly above siblings" },
    "dropdown": { "value": "1000", "description": "Dropdown menus" },
    "sticky": { "value": "1100", "description": "Sticky headers" },
    "overlay": { "value": "1200", "description": "Overlay backgrounds" },
    "modal": { "value": "1300", "description": "Modal dialogs" },
    "popover": { "value": "1400", "description": "Popovers, tooltips" },
    "toast": { "value": "1500", "description": "Toast notifications" },
    "max": { "value": "9999", "description": "Always on top" }
  }
}
```

### Usage

```css
.dropdown { z-index: var(--z-index-dropdown); }
.modal-backdrop { z-index: var(--z-index-overlay); }
.modal { z-index: var(--z-index-modal); }
.toast { z-index: var(--z-index-toast); }
```

This scale ensures that modals always appear above dropdowns, and toasts always appear above modals, without guessing or hard-coding arbitrary numbers.

## Token Categories (Moved from SKILL.md)

| Category | What It Stores | Examples |
|----------|---------------|---------|
| Color | Palette scales, semantic, state | `--color-red-500`, `--color-error` |
| Spacing | Whitespace, padding, gaps | `--spacing-0` through `--spacing-24` |
| Sizing | Component/icon/avatar sizes | `--size-icon-sm`, `--size-avatar-lg` |
| Typography | Families, sizes, weights, line heights | `--font-family-body`, `--font-weight-bold` |
| Elevation | Box shadows for depth | `--shadow-sm`, `--shadow-lg` |
| Border radius | Corner rounding | `--radius-sm`, `--radius-full` |
| Opacity | Transparency levels | `--opacity-disabled` |
| Motion | Durations and easings | `--duration-fast`, `--ease-in-out` |
| Breakpoints | Responsive width thresholds | `--breakpoint-sm`, `--breakpoint-lg` |
| Z-index | Stacking layers | `--z-dropdown`, `--z-modal`, `--z-toast` |

## Tier Detail (Moved from SKILL.md)

**Tier 1 — Global:** raw values, no semantics. Palette + scales.
**Tier 2 — Alias:** semantic role mapped to global. Theming happens here.
**Tier 3 — Component:** component-scoped, references alias. Optional — use when component deviates or for explicit dependency documentation.

## Governance (Moved from SKILL.md)

- Adding tokens: any contributor via PR; core team reviews naming + necessity.
- Changing values: design review required. Global changes ripple — high risk.
- Removing: treated as breaking change. Deprecate first, remove in major version.
- Auditing: periodic review for unused, inconsistent names, missing categories.

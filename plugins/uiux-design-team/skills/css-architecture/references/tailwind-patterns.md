# Tailwind Patterns

Comprehensive reference for Tailwind CSS architecture in design systems. Covers configuration and theme extension, component extraction strategies, design token integration, CVA for variant management, JIT compilation, performance optimization, and Tailwind as a design system foundation.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Configuration and Theme Extension](#configuration-and-theme-extension) | 14-55 | tailwind.config.js customization, extending vs overriding, custom values |
| [Component Extraction](#component-extraction) | 57-95 | @apply, component files, and when to extract |
| [Design Token Integration](#design-token-integration) | 97-130 | Mapping design tokens to Tailwind's theme system |
| [CVA for Variant Management](#cva-for-variant-management) | 132-172 | class-variance-authority patterns for component variants |
| [JIT Compilation](#jit-compilation) | 174-195 | Just-in-Time engine, arbitrary values, and content configuration |
| [Performance Optimization](#performance-optimization) | 197-225 | Purging, bundle size, and production build strategies |
| [Tailwind with Design Systems](#tailwind-with-design-systems) | 227-258 | Building a design system on top of Tailwind |
| [See Also](#see-also) | 260-266 | Related references and skills |

## Configuration and Theme Extension

### Extending the Theme

The `tailwind.config.js` file maps your design tokens to Tailwind's utility class system. Use `extend` to add values without replacing Tailwind's defaults:

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx,vue,svelte}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: 'oklch(0.97 0.02 250)',
          100: 'oklch(0.93 0.04 250)',
          500: 'oklch(0.58 0.19 250)',
          900: 'oklch(0.24 0.08 250)',
        },
        surface: 'var(--color-surface)',
        'on-surface': 'var(--color-on-surface)',
        primary: 'var(--color-primary)',
      },
      spacing: {
        '4.5': '1.125rem',
        '18': '4.5rem',
      },
      borderRadius: {
        'card': 'var(--radius-md)',
        'button': 'var(--radius-sm)',
      },
      fontFamily: {
        body: ['var(--font-body)', 'sans-serif'],
        display: ['var(--font-display)', 'serif'],
      },
      boxShadow: {
        'elevation-1': 'var(--shadow-sm)',
        'elevation-2': 'var(--shadow-md)',
        'elevation-3': 'var(--shadow-lg)',
      },
    },
  },
  plugins: [],
};
```

### Overriding vs Extending

| Action | Syntax | Effect |
|--------|--------|--------|
| **Extend** | `theme.extend.colors.brand` | Adds `brand` colors alongside default colors |
| **Override** | `theme.colors` (no `extend`) | Replaces all default colors with your values |

Override when your design system defines the complete set (e.g., your own color palette replaces Tailwind's). Extend when you want to add to Tailwind's defaults.

### Custom Screen Breakpoints

```js
theme: {
  screens: {
    'sm': '640px',
    'md': '768px',
    'lg': '1024px',
    'xl': '1280px',
    '2xl': '1536px',
  },
},
```

## Component Extraction

### Using @apply

`@apply` extracts utility combinations into a CSS class. Use it sparingly for repeated patterns that appear in many places.

```css
/* components/button.css */
.btn {
  @apply inline-flex items-center justify-center font-medium
    rounded-button transition-colors duration-150
    focus-visible:outline-2 focus-visible:outline-offset-2
    focus-visible:outline-primary;
}

.btn-primary {
  @apply btn bg-primary text-white hover:bg-primary/90
    active:bg-primary/80;
}

.btn-outline {
  @apply btn border-2 border-primary text-primary
    hover:bg-primary/10 active:bg-primary/20;
}
```

### When to Extract vs When to Use Utilities Inline

| Situation | Recommendation |
|-----------|---------------|
| Repeated across 3+ places | Extract into a component or @apply class |
| Complex multi-state styling | Extract into a component with CVA |
| One-off layout adjustment | Use inline utilities |
| Prototype or experiment | Use inline utilities |
| Design system component | Extract into a dedicated component file |

### Framework Component Extraction

The preferred approach in component frameworks is to extract utilities into component files rather than CSS classes:

```tsx
// Button.tsx -- utilities live in the component, not in a CSS file
function Button({ variant = "solid", size = "md", children, ...props }) {
  const baseClasses = "inline-flex items-center justify-center font-medium rounded-button transition-colors";
  const variantClasses = {
    solid: "bg-primary text-white hover:bg-primary/90",
    outline: "border-2 border-primary text-primary hover:bg-primary/10",
    ghost: "text-primary hover:bg-primary/10",
  };
  const sizeClasses = {
    sm: "h-8 px-3 text-sm",
    md: "h-10 px-4 text-base",
    lg: "h-12 px-6 text-lg",
  };

  return (
    <button className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]}`} {...props}>
      {children}
    </button>
  );
}
```

## Design Token Integration

### CSS Custom Properties as Token Layer

The most maintainable approach uses CSS custom properties as the bridge between design tokens and Tailwind:

```css
/* tokens.css -- generated from your token source */
:root {
  --color-primary: #3b82f6;
  --color-primary-hover: #2563eb;
  --color-surface: #ffffff;
  --color-on-surface: #1a1a2e;
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
}

[data-theme="dark"] {
  --color-primary: #60a5fa;
  --color-surface: #1a1a2e;
  --color-on-surface: #e2e8f0;
}
```

```js
// tailwind.config.js -- references CSS custom properties
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: 'var(--color-primary)',
        'primary-hover': 'var(--color-primary-hover)',
        surface: 'var(--color-surface)',
        'on-surface': 'var(--color-on-surface)',
      },
    },
  },
};
```

This approach means `bg-primary` automatically respects dark mode, brand switching, and any theme change -- all through CSS custom property overrides without Tailwind recompilation.

### Token-to-Utility Mapping

| Token | Tailwind Utility | Usage |
|-------|-----------------|-------|
| `--color-primary` | `bg-primary`, `text-primary`, `border-primary` | Primary brand color |
| `--color-surface` | `bg-surface` | Page and card backgrounds |
| `--radius-md` | `rounded-card` | Card corner rounding |
| `--shadow-sm` | `shadow-elevation-1` | Subtle elevation |
| `--font-body` | `font-body` | Body text font family |

## CVA for Variant Management

Class Variance Authority (CVA) provides a structured, type-safe way to define component variants with Tailwind classes.

### Basic CVA Usage

```ts
import { cva, type VariantProps } from "class-variance-authority";

const button = cva(
  // Base classes (always applied)
  "inline-flex items-center justify-center font-medium rounded-button transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary disabled:opacity-50 disabled:pointer-events-none",
  {
    variants: {
      variant: {
        solid: "bg-primary text-white hover:bg-primary-hover",
        outline: "border-2 border-primary text-primary hover:bg-primary/10",
        ghost: "text-primary hover:bg-primary/10",
        destructive: "bg-red-600 text-white hover:bg-red-700",
      },
      size: {
        sm: "h-8 px-3 text-sm gap-1.5",
        md: "h-10 px-4 text-base gap-2",
        lg: "h-12 px-6 text-lg gap-2.5",
      },
    },
    defaultVariants: {
      variant: "solid",
      size: "md",
    },
  }
);

type ButtonProps = VariantProps<typeof button>;
```

### Compound Variants

Compound variants apply styles when multiple variant conditions are met simultaneously:

```ts
const badge = cva("inline-flex items-center rounded-full font-medium", {
  variants: {
    variant: { solid: "", outline: "border" },
    color: { success: "", warning: "", error: "" },
    size: { sm: "px-2 py-0.5 text-xs", md: "px-3 py-1 text-sm" },
  },
  compoundVariants: [
    { variant: "solid", color: "success", className: "bg-green-100 text-green-800" },
    { variant: "solid", color: "warning", className: "bg-yellow-100 text-yellow-800" },
    { variant: "solid", color: "error", className: "bg-red-100 text-red-800" },
    { variant: "outline", color: "success", className: "border-green-600 text-green-700" },
    { variant: "outline", color: "warning", className: "border-yellow-600 text-yellow-700" },
    { variant: "outline", color: "error", className: "border-red-600 text-red-700" },
  ],
  defaultVariants: { variant: "solid", color: "success", size: "md" },
});
```

### Merging with tailwind-merge

Use `tailwind-merge` alongside CVA to safely merge conflicting classes when consumers pass additional class names:

```ts
import { twMerge } from "tailwind-merge";

function Button({ variant, size, className, ...props }) {
  return (
    <button
      className={twMerge(button({ variant, size }), className)}
      {...props}
    />
  );
}
```

## JIT Compilation

Tailwind's Just-In-Time engine generates styles on demand rather than purging unused styles. It scans your content files and generates only the utilities you actually use.

### Content Configuration

The `content` array tells Tailwind where to look for class names:

```js
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,vue,svelte}',
    './node_modules/@myds/components/**/*.{js,ts}',
    './content/**/*.mdx',
  ],
};
```

Include all files that contain Tailwind class names, including packages from node_modules.

### Arbitrary Values

JIT enables arbitrary values in brackets for one-off values not in your theme:

```html
<div class="w-[347px] mt-[13px] bg-[#1a365d] grid-cols-[1fr_2fr_1fr]">
```

Use sparingly. If you use the same arbitrary value more than twice, add it to the theme configuration instead.

### Dynamic Class Names

Tailwind scans files as static text. Dynamic class construction does not work:

```js
// WRONG: Tailwind cannot detect these classes
const color = 'red';
const className = `bg-${color}-500`;

// CORRECT: Use complete class names
const colorClasses = {
  red: 'bg-red-500',
  blue: 'bg-blue-500',
  green: 'bg-green-500',
};
```

## Performance Optimization

### Production Build Size

A well-configured Tailwind build is typically 10-30kb gzipped. If your bundle is larger, check:

1. **Content paths are correct** -- overly broad globs include files that reference unused classes
2. **No safelist abuse** -- safelisting classes defeats the purpose of tree-shaking
3. **Minimize arbitrary values** -- each arbitrary value generates a unique class

### CSS Layers

Use `@layer` to organize Tailwind's output and prevent specificity issues:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer components {
  /* Your component styles here */
  .card { @apply rounded-card bg-surface shadow-elevation-1 p-6; }
}
```

### Reducing Class Count in HTML

For components with many utilities, extract into CVA variants or @apply classes. Long class strings (10+ utilities) are a signal that extraction would improve maintainability.

### Preload Critical CSS

For server-rendered pages, inline the critical CSS (above-the-fold utilities) in the `<head>` and load the rest asynchronously:

```html
<head>
  <style>/* Inlined critical Tailwind utilities */</style>
  <link rel="preload" href="/styles.css" as="style" onload="this.rel='stylesheet'">
</head>
```

## Tailwind with Design Systems

### Tailwind as a Design System Layer

Tailwind's configuration file becomes the enforcement layer for design system tokens. By defining only your system's values in the theme and disabling defaults, you ensure developers can only use sanctioned values.

```js
module.exports = {
  theme: {
    // Override (not extend) to restrict to system values only
    colors: {
      primary: 'var(--color-primary)',
      secondary: 'var(--color-secondary)',
      surface: 'var(--color-surface)',
      'on-surface': 'var(--color-on-surface)',
      error: 'var(--color-error)',
      success: 'var(--color-success)',
      warning: 'var(--color-warning)',
      transparent: 'transparent',
      current: 'currentColor',
    },
    spacing: {
      0: '0',
      1: 'var(--space-1)',
      2: 'var(--space-2)',
      3: 'var(--space-3)',
      4: 'var(--space-4)',
      6: 'var(--space-6)',
      8: 'var(--space-8)',
      12: 'var(--space-12)',
      16: 'var(--space-16)',
    },
  },
};
```

### Preset Sharing

Share Tailwind configuration across projects using presets:

```js
// @myds/tailwind-preset/index.js
module.exports = {
  theme: { /* design system theme */ },
  plugins: [ /* design system plugins */ ],
};

// Consumer's tailwind.config.js
module.exports = {
  presets: [require('@myds/tailwind-preset')],
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
};
```

### Plugins for Custom Utilities

Create Tailwind plugins for design-system-specific utilities:

```js
const plugin = require('tailwindcss/plugin');

module.exports = plugin(function({ addUtilities, theme }) {
  addUtilities({
    '.text-balance': { 'text-wrap': 'balance' },
    '.scrollbar-hidden': {
      'scrollbar-width': 'none',
      '&::-webkit-scrollbar': { display: 'none' },
    },
  });
});
```

## See Also

- [[bem-guide.md]] -- BEM naming convention that can complement Tailwind for structural styling
- [[css-modules-guide.md]] -- Scoped CSS alternative to Tailwind's utility approach
- [[css-in-js-patterns.md]] -- Runtime and build-time styling approaches compared to Tailwind
- [[../../component-library/references/variant-systems.md]] -- CVA and variant patterns in depth
- [[../../design-tokens/references/naming-conventions.md]] -- Token naming that maps to Tailwind theme keys
- [[../../design-system-creation/references/token-architecture.md]] -- Three-tier token system that feeds Tailwind configuration

**Back to:** [CSS Architecture Skill](../SKILL.md)

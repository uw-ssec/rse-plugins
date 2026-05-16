# Variant Systems

Comprehensive reference for implementing component variant systems in design libraries. Covers CVA (class-variance-authority) in depth, compound variants, Tailwind integration, alternative approaches with Stitches and Vanilla Extract recipes, type-safe variant APIs, and variant documentation patterns.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [CVA Detailed Usage](#cva-detailed-usage) | 14-65 | Core CVA API, defining variants, defaults, and composing |
| [Compound Variants](#compound-variants) | 67-105 | Applying styles when multiple variant conditions are true |
| [Tailwind Integration](#tailwind-integration) | 107-140 | CVA with Tailwind CSS, tailwind-merge, and class conflicts |
| [Alternative Approaches](#alternative-approaches) | 142-185 | Stitches variants, Vanilla Extract recipes, and CSS-only variants |
| [Type-Safe Variant APIs](#type-safe-variant-apis) | 187-220 | TypeScript patterns for variant props and exhaustive checking |
| [Variant Documentation Patterns](#variant-documentation-patterns) | 222-255 | Storybook stories, visual regression, and variant catalogs |
| [See Also](#see-also) | 257-263 | Related references and skills |

## CVA Detailed Usage

Class Variance Authority (CVA) provides a structured way to define and apply component variants. It maps variant names and values to CSS class strings, producing a function that returns the correct classes for any variant combination.

### Core API

```ts
import { cva, type VariantProps } from 'class-variance-authority';

const component = cva(
  'base-class another-base-class',
  {
    variants: {
      variantName: {
        value1: 'classes-for-value1',
        value2: 'classes-for-value2',
      },
    },
    compoundVariants: [],
    defaultVariants: {
      variantName: 'value1',
    },
  }
);
```

### Complete Button Example

```ts
const button = cva(
  [
    'inline-flex items-center justify-center',
    'font-medium rounded-md',
    'transition-colors duration-150',
    'focus-visible:outline-2 focus-visible:outline-offset-2',
    'disabled:opacity-50 disabled:pointer-events-none',
  ],
  {
    variants: {
      intent: {
        primary: 'bg-primary text-white hover:bg-primary/90 focus-visible:outline-primary',
        secondary: 'bg-surface text-on-surface border border-border hover:bg-surface-hover',
        danger: 'bg-red-600 text-white hover:bg-red-700 focus-visible:outline-red-600',
        ghost: 'text-on-surface hover:bg-surface-hover',
      },
      size: {
        sm: 'h-8 px-3 text-sm gap-1.5',
        md: 'h-10 px-4 text-base gap-2',
        lg: 'h-12 px-6 text-lg gap-2.5',
        icon: 'h-10 w-10 p-0',
      },
      fullWidth: {
        true: 'w-full',
        false: '',
      },
    },
    defaultVariants: {
      intent: 'primary',
      size: 'md',
      fullWidth: false,
    },
  }
);

type ButtonVariants = VariantProps<typeof button>;
```

## Compound Variants

Compound variants apply additional classes when multiple variant conditions are met simultaneously. They handle cases where the combination of two variants requires styling that neither variant alone provides.

### When You Need Compound Variants

An outlined danger button should have red border and red text. Neither `intent: danger` nor `outlined: true` alone produces this combination.

```ts
const button = cva('inline-flex items-center justify-center font-medium', {
  variants: {
    intent: {
      primary: 'bg-primary text-white',
      danger: 'bg-red-600 text-white',
      ghost: 'bg-transparent text-on-surface',
    },
    outlined: {
      true: 'bg-transparent border-2',
      false: '',
    },
  },
  compoundVariants: [
    {
      intent: 'danger',
      outlined: true,
      className: 'border-red-600 text-red-600 hover:bg-red-50',
    },
    {
      intent: 'primary',
      outlined: true,
      className: 'border-primary text-primary hover:bg-primary/10',
    },
  ],
  defaultVariants: { intent: 'primary', outlined: false },
});
```

### Compound Variant for Badge Colors

```ts
const badge = cva('inline-flex items-center rounded-full font-medium', {
  variants: {
    variant: { solid: '', subtle: '', outline: 'border bg-transparent' },
    color: { success: '', warning: '', error: '', info: '' },
    size: { sm: 'px-2 py-0.5 text-xs', md: 'px-2.5 py-0.5 text-sm' },
  },
  compoundVariants: [
    { variant: 'solid', color: 'success', className: 'bg-green-600 text-white' },
    { variant: 'solid', color: 'warning', className: 'bg-yellow-500 text-black' },
    { variant: 'solid', color: 'error', className: 'bg-red-600 text-white' },
    { variant: 'subtle', color: 'success', className: 'bg-green-100 text-green-800' },
    { variant: 'subtle', color: 'warning', className: 'bg-yellow-100 text-yellow-800' },
    { variant: 'subtle', color: 'error', className: 'bg-red-100 text-red-800' },
    { variant: 'outline', color: 'success', className: 'border-green-600 text-green-700' },
    { variant: 'outline', color: 'error', className: 'border-red-600 text-red-700' },
  ],
  defaultVariants: { variant: 'subtle', color: 'success', size: 'md' },
});
```

## Tailwind Integration

### CVA with tailwind-merge

When consumers pass additional class names, conflicts can occur. Use `tailwind-merge` to resolve them:

```ts
import { twMerge } from 'tailwind-merge';
import { clsx, type ClassValue } from 'clsx';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

function Button({ intent, size, fullWidth, className, ...props }: ButtonProps) {
  return (
    <button className={cn(button({ intent, size, fullWidth }), className)} {...props} />
  );
}
```

### Tailwind IntelliSense Configuration

For IDE autocompletion inside CVA definitions, add to `.vscode/settings.json`:

```json
{
  "tailwindCSS.experimental.classRegex": [
    ["cva\\(([^)]*)\\)", "[\"'`]([^\"'`]*).*?[\"'`]"],
    ["cx\\(([^)]*)\\)", "(?:'|\"|`)([^']*)(?:'|\"|`)"]
  ]
}
```

### Dynamic Class Names Warning

Tailwind scans files as static text. Dynamic class construction does not work:

```ts
// WRONG: Tailwind cannot detect these
const bg = `bg-${color}-500`;

// CORRECT: Use complete class names in variant definitions
const colorMap = {
  red: 'bg-red-500 text-red-800',
  blue: 'bg-blue-500 text-blue-800',
};
```

## Alternative Approaches

### Vanilla Extract Recipes

Zero-runtime, type-safe variant API that generates static CSS:

```ts
import { recipe } from '@vanilla-extract/recipes';
import { vars } from '../theme.css';

export const button = recipe({
  base: {
    display: 'inline-flex',
    alignItems: 'center',
    fontWeight: 500,
    borderRadius: vars.radius.sm,
  },
  variants: {
    intent: {
      primary: { background: vars.color.primary, color: 'white' },
      secondary: { background: vars.color.surface, border: `1px solid ${vars.color.border}` },
    },
    size: {
      sm: { height: '2rem', padding: '0 0.75rem' },
      md: { height: '2.5rem', padding: '0 1rem' },
    },
  },
  defaultVariants: { intent: 'primary', size: 'md' },
});
```

### CSS-Only Variants with Data Attributes

For simple cases, no JavaScript variant library is needed:

```css
.button {
  display: inline-flex;
  padding: var(--button-padding, 0.5rem 1rem);
  background: var(--button-bg, var(--color-primary));
  color: var(--button-color, white);
}

.button[data-variant="outline"] {
  --button-bg: transparent;
  --button-color: var(--color-primary);
  border: 2px solid var(--color-primary);
}

.button[data-size="sm"] {
  --button-padding: 0.25rem 0.75rem;
  font-size: 0.875rem;
}
```

### Comparison Table

| Feature | CVA | Vanilla Extract Recipes | CSS Data Attributes |
|---------|-----|------------------------|-------------------|
| Runtime cost | None (string concat) | None (static CSS) | None (CSS only) |
| Type safety | Via VariantProps | Native TypeScript | No |
| Framework | Any | Any (build plugin required) | Any |
| Bundle impact | ~1kb | 0kb (static CSS) | 0kb |
| IDE support | With config | Native | Native (CSS) |

## Type-Safe Variant APIs

### Extracting Variant Types

```ts
const alertVariants = cva('...', {
  variants: {
    severity: { info: '...', warning: '...', error: '...', success: '...' },
    dismissible: { true: '...', false: '...' },
  },
});

type AlertVariants = VariantProps<typeof alertVariants>;

type AlertProps = AlertVariants & {
  title: string;
  children: React.ReactNode;
  onDismiss?: () => void;
};
```

### Exhaustive Variant Handling

```ts
function getIcon(severity: NonNullable<AlertVariants['severity']>): React.ReactNode {
  const icons: Record<NonNullable<AlertVariants['severity']>, React.ReactNode> = {
    info: <InfoIcon />,
    warning: <WarningIcon />,
    error: <ErrorIcon />,
    success: <CheckIcon />,
  };
  return icons[severity];
}
```

### Restricting Invalid Combinations

```ts
type ButtonProps =
  | { intent: 'primary' | 'secondary'; loading?: boolean }
  | { intent: 'link'; loading?: never };
```

## Variant Documentation Patterns

### Storybook Variant Matrix

```tsx
export const VariantMatrix: Story = {
  render: () => (
    <div className="grid gap-4">
      {(['primary', 'secondary', 'danger', 'ghost'] as const).map((intent) => (
        <div key={intent} className="flex gap-2 items-center">
          <span className="w-24 text-sm font-mono">{intent}</span>
          {(['sm', 'md', 'lg'] as const).map((size) => (
            <Button key={size} intent={intent} size={size}>{size}</Button>
          ))}
        </div>
      ))}
    </div>
  ),
};
```

### Variant Catalog Documentation

| Variant | Value | Description | When to Use |
|---------|-------|-------------|-------------|
| intent | `primary` | Highest emphasis | Primary page action, CTAs |
| intent | `secondary` | Medium emphasis | Secondary actions, cancel buttons |
| intent | `danger` | Destructive | Delete, remove, irreversible actions |
| intent | `ghost` | Lowest emphasis | Tertiary actions, toolbar items |
| size | `sm` | 32px height | Tables, dense UIs, toolbars |
| size | `md` | 40px height | Default, most contexts |
| size | `lg` | 48px height | Hero sections, prominent CTAs |

### Visual Regression Testing

```ts
const intents = ['primary', 'secondary', 'danger', 'ghost'];
const sizes = ['sm', 'md', 'lg'];

for (const intent of intents) {
  for (const size of sizes) {
    test(`Button ${intent} ${size}`, async ({ page }) => {
      await page.goto(`/iframe.html?id=button--${intent}-${size}`);
      await expect(page).toHaveScreenshot(`button-${intent}-${size}.png`);
    });
  }
}
```

## See Also

- [[composition-patterns.md]] -- Structural patterns that variant systems style
- [[state-management.md]] -- UI states that extend variant definitions
- [[../../css-architecture/references/tailwind-patterns.md]] -- Tailwind configuration feeding CVA variant classes
- [[../../css-architecture/references/css-in-js-patterns.md]] -- Vanilla Extract recipes and runtime variants
- [[../../design-tokens/references/naming-conventions.md]] -- Token naming aligned with variant naming
- [[../../design-system-creation/references/component-api-guide.md]] -- API design for variant props

**Back to:** [Component Library Skill](../SKILL.md)

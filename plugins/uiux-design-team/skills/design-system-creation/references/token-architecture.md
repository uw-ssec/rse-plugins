[Back to Design System Creation](../index.md)

# Design Token Architecture

A comprehensive guide to structuring, naming, transforming, and distributing design tokens across platforms.

---

## Three-Tier Token Hierarchy

Design tokens are organized into three tiers that create a clear abstraction path from raw values to component-specific bindings.

### Tier 1: Global Tokens (Primitives)

Raw values with no semantic meaning. They describe what the value is, not how it is used.

```json
{
  "color": {
    "blue": {
      "50": { "value": "#eff6ff" },
      "100": { "value": "#dbeafe" },
      "500": { "value": "#3b82f6" },
      "600": { "value": "#2563eb" },
      "700": { "value": "#1d4ed8" },
      "900": { "value": "#1e3a8a" }
    },
    "gray": {
      "50": { "value": "#f9fafb" },
      "100": { "value": "#f3f4f6" },
      "500": { "value": "#6b7280" },
      "800": { "value": "#1f2937" },
      "900": { "value": "#111827" }
    }
  },
  "spacing": {
    "1": { "value": "4px" },
    "2": { "value": "8px" },
    "3": { "value": "12px" },
    "4": { "value": "16px" },
    "6": { "value": "24px" },
    "8": { "value": "32px" }
  }
}
```

### Tier 2: Alias Tokens (Semantic)

Map primitives to meaningful names that describe how they are used.

```json
{
  "color": {
    "text": {
      "primary": { "value": "{color.gray.900}" },
      "secondary": { "value": "{color.gray.500}" },
      "inverse": { "value": "{color.gray.50}" },
      "brand": { "value": "{color.blue.600}" }
    },
    "background": {
      "default": { "value": "#ffffff" },
      "subtle": { "value": "{color.gray.50}" },
      "brand": { "value": "{color.blue.600}" }
    },
    "border": {
      "default": { "value": "{color.gray.200}" },
      "strong": { "value": "{color.gray.400}" }
    },
    "interactive": {
      "default": { "value": "{color.blue.600}" },
      "hover": { "value": "{color.blue.700}" },
      "active": { "value": "{color.blue.800}" }
    }
  }
}
```

### Tier 3: Component Tokens (Specific)

Bind semantic tokens to specific component properties.

```json
{
  "button": {
    "primary": {
      "background": { "value": "{color.interactive.default}" },
      "background-hover": { "value": "{color.interactive.hover}" },
      "text": { "value": "{color.text.inverse}" },
      "border-radius": { "value": "{radius.md}" },
      "padding-x": { "value": "{spacing.4}" },
      "padding-y": { "value": "{spacing.2}" }
    },
    "secondary": {
      "background": { "value": "{color.background.subtle}" },
      "text": { "value": "{color.text.primary}" }
    }
  },
  "card": {
    "background": { "value": "{color.background.default}" },
    "border": { "value": "{color.border.default}" },
    "border-radius": { "value": "{radius.lg}" },
    "padding": { "value": "{spacing.6}" },
    "shadow": { "value": "{shadow.md}" }
  }
}
```

---

## Token Naming Conventions

Follow the CTI (Category-Type-Item) structure:

```
[category]-[type]-[item]-[sub-item]-[state]

color-text-primary
color-background-brand
spacing-inline-md
font-size-lg
border-radius-sm
shadow-elevation-2
```

| Segment | Purpose | Examples |
|---------|---------|---------|
| Category | What kind of token | `color`, `spacing`, `font`, `border`, `shadow`, `motion` |
| Type | Sub-category | `text`, `background`, `border`, `size`, `weight`, `radius` |
| Item | Specific usage | `primary`, `secondary`, `brand`, `sm`, `md`, `lg` |
| State | Interactive state | `hover`, `active`, `disabled`, `focus` |

---

## Token Types

### Color

```json
{
  "color": {
    "value": "#2563eb",
    "type": "color",
    "description": "Primary brand color"
  }
}
```

### Typography

```json
{
  "font": {
    "family": { "sans": { "value": "Inter, system-ui, sans-serif" } },
    "size": {
      "sm": { "value": "0.875rem" },
      "base": { "value": "1rem" },
      "lg": { "value": "1.125rem" }
    },
    "weight": {
      "normal": { "value": "400" },
      "medium": { "value": "500" },
      "bold": { "value": "700" }
    },
    "line-height": {
      "tight": { "value": "1.25" },
      "normal": { "value": "1.5" },
      "relaxed": { "value": "1.75" }
    },
    "letter-spacing": {
      "tight": { "value": "-0.02em" },
      "normal": { "value": "0" },
      "wide": { "value": "0.025em" }
    }
  }
}
```

### Spacing

```json
{
  "spacing": {
    "0": { "value": "0" },
    "1": { "value": "4px" },
    "2": { "value": "8px" },
    "4": { "value": "16px" },
    "8": { "value": "32px" },
    "16": { "value": "64px" }
  }
}
```

### Shadow

```json
{
  "shadow": {
    "sm": { "value": "0 1px 2px 0 rgba(0, 0, 0, 0.05)" },
    "md": { "value": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)" },
    "lg": { "value": "0 10px 15px -3px rgba(0, 0, 0, 0.1)" }
  }
}
```

### Motion

```json
{
  "motion": {
    "duration": {
      "fast": { "value": "100ms" },
      "normal": { "value": "200ms" },
      "slow": { "value": "400ms" }
    },
    "easing": {
      "default": { "value": "cubic-bezier(0.4, 0, 0.2, 1)" },
      "in": { "value": "cubic-bezier(0.4, 0, 1, 1)" },
      "out": { "value": "cubic-bezier(0, 0, 0.2, 1)" },
      "spring": { "value": "cubic-bezier(0.34, 1.56, 0.64, 1)" }
    }
  }
}
```

### Border

```json
{
  "border": {
    "width": {
      "thin": { "value": "1px" },
      "medium": { "value": "2px" },
      "thick": { "value": "4px" }
    },
    "radius": {
      "none": { "value": "0" },
      "sm": { "value": "4px" },
      "md": { "value": "8px" },
      "lg": { "value": "12px" },
      "full": { "value": "9999px" }
    }
  }
}
```

---

## Token Formats

### JSON (Recommended Default)

```json
{
  "color": {
    "primary": {
      "value": "#2563eb",
      "type": "color",
      "description": "Primary brand color for interactive elements"
    }
  }
}
```

### YAML

```yaml
color:
  primary:
    value: "#2563eb"
    type: color
    description: Primary brand color for interactive elements
```

### DTCG (Design Tokens Community Group) Format

```json
{
  "color": {
    "primary": {
      "$value": "#2563eb",
      "$type": "color",
      "$description": "Primary brand color"
    }
  }
}
```

---

## Style Dictionary Configuration

Style Dictionary transforms and distributes tokens across platforms.

```js
// config.js
module.exports = {
  source: ['tokens/**/*.json'],
  platforms: {
    css: {
      transformGroup: 'css',
      buildPath: 'dist/css/',
      files: [
        {
          destination: 'tokens.css',
          format: 'css/variables',
          options: { outputReferences: true },
        },
      ],
    },
    scss: {
      transformGroup: 'scss',
      buildPath: 'dist/scss/',
      files: [
        { destination: '_tokens.scss', format: 'scss/variables' },
      ],
    },
    ios: {
      transformGroup: 'ios-swift',
      buildPath: 'dist/ios/',
      files: [
        { destination: 'Tokens.swift', format: 'ios-swift/class.swift', className: 'DesignTokens' },
      ],
    },
    android: {
      transformGroup: 'android',
      buildPath: 'dist/android/',
      files: [
        { destination: 'tokens.xml', format: 'android/resources' },
      ],
    },
  },
};
```

---

## Token Transformation Pipeline

```
Source files (JSON/YAML)
  |
  v
Parse tokens into a flat dictionary
  |
  v
Apply transforms (name, value, attribute)
  |
  v
Resolve references ({color.blue.600} -> #2563eb)
  |
  v
Apply formatters (CSS variables, Swift constants, etc.)
  |
  v
Write output files
```

### Custom Transform Example

```js
const StyleDictionary = require('style-dictionary');

StyleDictionary.registerTransform({
  name: 'size/pxToRem',
  type: 'value',
  matcher: (token) => token.attributes.category === 'font' && token.attributes.type === 'size',
  transformer: (token) => {
    const px = parseFloat(token.original.value);
    return `${px / 16}rem`;
  },
});
```

---

## Platform-Specific Output

### CSS Custom Properties

```css
:root {
  --color-primary: #2563eb;
  --color-text-primary: #111827;
  --spacing-4: 16px;
  --font-size-base: 1rem;
  --radius-md: 8px;
}
```

### iOS / Swift

```swift
public class DesignTokens {
  public static let colorPrimary = UIColor(red: 0.145, green: 0.388, blue: 0.922, alpha: 1.0)
  public static let spacing4: CGFloat = 16.0
  public static let fontSizeBase: CGFloat = 16.0
}
```

### Android / Kotlin

```xml
<resources>
  <color name="color_primary">#2563eb</color>
  <dimen name="spacing_4">16dp</dimen>
  <dimen name="font_size_base">16sp</dimen>
</resources>
```

---

## Versioning Tokens

Treat design tokens as a versioned package. Follow semantic versioning:

| Change Type | Version Bump | Example |
|-------------|-------------|---------|
| New token added | Minor | Added `color-text-tertiary` |
| Token value changed | Patch | Changed `color-primary` from `#2563eb` to `#2558e0` |
| Token renamed or removed | Major | Renamed `color-brand` to `color-primary` |
| Token type changed | Major | Changed spacing from `px` to `rem` |

### Publishing Tokens

```json
{
  "name": "@org/design-tokens",
  "version": "2.4.1",
  "files": ["dist/"],
  "scripts": {
    "build": "style-dictionary build",
    "prepublishOnly": "npm run build"
  }
}
```

Publish to npm or an internal registry. Consuming apps install the package and import the platform-specific output.

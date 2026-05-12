[Back to Design Tokens](../index.md)

# Design Token Platform Output Reference

How to transform and distribute design tokens to CSS, SCSS, iOS, Android, React Native, and other platforms.

---

## CSS Custom Properties Output

The most common web output format. All tokens become CSS custom properties on `:root`.

```css
/* Generated: tokens.css */
:root {
  /* Colors - Primitive */
  --color-blue-50: #eff6ff;
  --color-blue-500: #3b82f6;
  --color-blue-600: #2563eb;
  --color-blue-700: #1d4ed8;

  /* Colors - Semantic */
  --color-text-primary: var(--color-gray-900);
  --color-text-secondary: var(--color-gray-500);
  --color-background-default: #ffffff;
  --color-interactive-default: var(--color-blue-600);
  --color-interactive-hover: var(--color-blue-700);
  --color-border-default: var(--color-gray-200);

  /* Spacing */
  --spacing-1: 0.25rem;
  --spacing-2: 0.5rem;
  --spacing-4: 1rem;
  --spacing-6: 1.5rem;
  --spacing-8: 2rem;

  /* Typography */
  --font-family-sans: 'Inter', system-ui, sans-serif;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-bold: 700;
  --line-height-normal: 1.5;

  /* Borders */
  --border-radius-sm: 0.25rem;
  --border-radius-md: 0.5rem;
  --border-radius-lg: 0.75rem;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);

  /* Motion */
  --duration-fast: 100ms;
  --duration-normal: 200ms;
  --easing-default: cubic-bezier(0.4, 0, 0.2, 1);
}
```

### With Output References

When `outputReferences: true` is enabled in Style Dictionary, semantic tokens preserve their reference chain:

```css
--color-interactive-default: var(--color-blue-600);
/* Instead of: --color-interactive-default: #2563eb; */
```

This lets consumers see the relationship and enables runtime theme switching.

---

## SCSS Variables Output

```scss
// Generated: _tokens.scss
$color-blue-600: #2563eb;
$color-text-primary: #111827;
$color-interactive-default: $color-blue-600;
$spacing-4: 1rem;
$font-size-base: 1rem;
$border-radius-md: 0.5rem;
$shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
```

### SCSS Map Output

Style Dictionary can generate Sass maps for iteration:

```scss
// Generated: _token-maps.scss
$colors: (
  'text-primary': #111827,
  'text-secondary': #6b7280,
  'interactive-default': #2563eb,
  'interactive-hover': #1d4ed8,
  'background-default': #ffffff,
  'border-default': #e5e7eb,
);

// Usage
@each $name, $value in $colors {
  .text-#{$name} { color: $value; }
}
```

---

## iOS / Swift Output

### UIColor Extensions

```swift
// Generated: DesignTokens+Color.swift
import UIKit

extension UIColor {
    static let textPrimary = UIColor(red: 0.067, green: 0.094, blue: 0.153, alpha: 1.0)
    static let textSecondary = UIColor(red: 0.420, green: 0.447, blue: 0.502, alpha: 1.0)
    static let interactiveDefault = UIColor(red: 0.145, green: 0.388, blue: 0.922, alpha: 1.0)
    static let interactiveHover = UIColor(red: 0.114, green: 0.306, blue: 0.847, alpha: 1.0)
    static let backgroundDefault = UIColor.white
    static let borderDefault = UIColor(red: 0.898, green: 0.906, blue: 0.922, alpha: 1.0)
}
```

### SwiftUI Color Extensions

```swift
// Generated: DesignTokens+SwiftUI.swift
import SwiftUI

extension Color {
    static let textPrimary = Color(red: 0.067, green: 0.094, blue: 0.153)
    static let interactiveDefault = Color(red: 0.145, green: 0.388, blue: 0.922)
}
```

### Spacing and Sizing

```swift
// Generated: DesignTokens+Spacing.swift
import CoreGraphics

struct Spacing {
    static let xs: CGFloat = 4
    static let sm: CGFloat = 8
    static let md: CGFloat = 16
    static let lg: CGFloat = 24
    static let xl: CGFloat = 32
}

struct FontSize {
    static let sm: CGFloat = 14
    static let base: CGFloat = 16
    static let lg: CGFloat = 18
    static let xl: CGFloat = 20
}
```

---

## Android / Kotlin Output

### Color Resources

```xml
<!-- Generated: colors.xml -->
<resources>
    <color name="color_text_primary">#111827</color>
    <color name="color_text_secondary">#6b7280</color>
    <color name="color_interactive_default">#2563eb</color>
    <color name="color_interactive_hover">#1d4ed8</color>
    <color name="color_background_default">#ffffff</color>
    <color name="color_border_default">#e5e7eb</color>
</resources>
```

### Dimension Resources

```xml
<!-- Generated: dimens.xml -->
<resources>
    <dimen name="spacing_xs">4dp</dimen>
    <dimen name="spacing_sm">8dp</dimen>
    <dimen name="spacing_md">16dp</dimen>
    <dimen name="spacing_lg">24dp</dimen>

    <dimen name="font_size_sm">14sp</dimen>
    <dimen name="font_size_base">16sp</dimen>
    <dimen name="font_size_lg">18sp</dimen>

    <dimen name="border_radius_sm">4dp</dimen>
    <dimen name="border_radius_md">8dp</dimen>
    <dimen name="border_radius_lg">12dp</dimen>
</resources>
```

### Jetpack Compose Output

```kotlin
// Generated: DesignTokens.kt
object DesignTokens {
    val colorTextPrimary = Color(0xFF111827)
    val colorInteractiveDefault = Color(0xFF2563EB)
    val spacingMd = 16.dp
    val fontSizeBase = 16.sp
    val borderRadiusMd = 8.dp
}
```

---

## React Native Output

```ts
// Generated: tokens.ts
export const colors = {
  textPrimary: '#111827',
  textSecondary: '#6b7280',
  interactiveDefault: '#2563eb',
  interactiveHover: '#1d4ed8',
  backgroundDefault: '#ffffff',
  borderDefault: '#e5e7eb',
} as const;

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
} as const;

export const fontSize = {
  sm: 14,
  base: 16,
  lg: 18,
  xl: 20,
} as const;

export const borderRadius = {
  sm: 4,
  md: 8,
  lg: 12,
  full: 9999,
} as const;
```

---

## JSON Output for Design Tools

```json
{
  "color": {
    "text-primary": { "value": "#111827", "type": "color" },
    "interactive-default": { "value": "#2563eb", "type": "color" }
  },
  "spacing": {
    "md": { "value": "16px", "type": "dimension" }
  },
  "font": {
    "size-base": { "value": "16px", "type": "dimension" }
  }
}
```

This format can be consumed by Figma plugins, Sketch libraries, or custom design tool integrations.

---

## Style Dictionary Transforms and Formats

### Built-in Transform Groups

| Transform Group | Platforms | What It Does |
|----------------|-----------|-------------|
| `css` | Web (CSS) | kebab-case names, px values |
| `scss` | Web (SCSS) | kebab-case with $ prefix, px values |
| `less` | Web (Less) | kebab-case with @ prefix |
| `ios-swift` | iOS | camelCase, UIColor/CGFloat values |
| `android` | Android | snake_case, dp/sp units |
| `compose` | Android | camelCase, Compose types |
| `react-native` | React Native | camelCase, number values |

### Custom Formatters

```js
const StyleDictionary = require('style-dictionary');

StyleDictionary.registerFormat({
  name: 'typescript/module',
  formatter: ({ dictionary }) => {
    const lines = dictionary.allProperties.map((token) => {
      const name = token.name
        .split('-')
        .map((s, i) => (i === 0 ? s : s[0].toUpperCase() + s.slice(1)))
        .join('');
      return `export const ${name} = '${token.value}';`;
    });
    return lines.join('\n');
  },
});

StyleDictionary.registerFormat({
  name: 'css/theme-variables',
  formatter: ({ dictionary, options }) => {
    const selector = options.selector || ':root';
    const vars = dictionary.allProperties
      .map((token) => `  --${token.name}: ${token.value};`)
      .join('\n');
    return `${selector} {\n${vars}\n}`;
  },
});
```

---

## CI/CD Integration for Token Publishing

### Pipeline Stages

```yaml
# .github/workflows/tokens.yml
name: Build and Publish Design Tokens

on:
  push:
    paths: ['tokens/**']
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm ci
      - run: npm run build          # style-dictionary build
      - run: npm test               # validate output

  publish:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          registry-url: 'https://registry.npmjs.org'
      - run: npm ci && npm run build
      - run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### Token Validation

```js
// validate-tokens.js
const tokens = require('./dist/tokens.json');

function validate(tokens) {
  const errors = [];

  for (const [name, token] of Object.entries(tokens)) {
    if (!token.value) errors.push(`${name}: missing value`);
    if (token.type === 'color' && !/^#[0-9a-f]{6}$/i.test(token.value)) {
      errors.push(`${name}: invalid color format "${token.value}"`);
    }
  }

  if (errors.length > 0) {
    console.error('Token validation failed:');
    errors.forEach((e) => console.error(`  - ${e}`));
    process.exit(1);
  }

  console.log('All tokens valid.');
}

validate(tokens);
```

### Multi-Platform Distribution

```
npm package: @org/tokens           -> CSS, SCSS, JS/TS consumers
CocoaPod:    OrgDesignTokens       -> iOS consumers
Maven:       org.company:tokens    -> Android consumers
Figma plugin: sync from JSON       -> Design tool consumers
```

Each platform consumes the format it needs, all generated from the same source tokens.

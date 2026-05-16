[Back to Design Tokens](../index.md)

# Design Token Naming Conventions

A comprehensive guide to naming design tokens consistently, semantically, and across platforms.

---

## CTI (Category-Type-Item) Structure

The Category-Type-Item naming model is the standard for design token names. Each segment narrows the scope.

```
category-type-item[-sub-item][-state]
```

| Segment | Description | Examples |
|---------|-------------|---------|
| Category | The broad domain | `color`, `spacing`, `font`, `border`, `shadow`, `motion`, `opacity`, `z-index` |
| Type | Sub-category within the domain | `text`, `background`, `border`, `size`, `weight`, `radius`, `duration` |
| Item | Specific usage or variant | `primary`, `secondary`, `brand`, `sm`, `md`, `lg`, `error` |
| Sub-item | Further refinement | `light`, `dark`, `muted` |
| State | Interactive or conditional state | `hover`, `active`, `disabled`, `focus`, `pressed` |

### Examples

```
color-text-primary
color-text-primary-hover
color-background-brand
color-border-error
spacing-inline-md
font-size-lg
font-weight-bold
font-line-height-tight
border-radius-sm
border-width-thin
shadow-elevation-1
motion-duration-fast
motion-easing-in-out
opacity-disabled
z-index-modal
```

---

## Semantic Naming vs Absolute Naming

### Absolute (Avoid for Component Consumption)

```
color-blue-600
color-gray-100
spacing-16
font-size-14
```

Absolute tokens describe the value itself. They belong in the **global/primitive** tier only.

### Semantic (Use for Component Consumption)

```
color-text-primary          (not color-gray-900)
color-interactive-default   (not color-blue-600)
color-surface-elevated      (not color-white)
spacing-component-gap       (not spacing-16)
```

Semantic tokens describe the **purpose**. Components should only reference semantic tokens, never primitives directly.

### Why Semantic Naming Matters

```css
/* Bad: if blue changes to purple, this name is misleading */
--color-blue-600: #7c3aed;

/* Good: semantic name is always accurate regardless of value */
--color-interactive-default: #7c3aed;
```

---

## Platform Prefixes

Each platform uses its own convention for token names.

### CSS Custom Properties

```css
--color-text-primary: #111827;
--spacing-md: 16px;
--font-size-base: 1rem;
```

Prefix with `--`. Use kebab-case.

### iOS / Swift

```swift
static let colorTextPrimary = UIColor(...)
static let spacingMd: CGFloat = 16.0
static let fontSizeBase: CGFloat = 16.0
```

Use camelCase. No prefix needed (namespace via class/struct).

### Android

```xml
<color name="color_text_primary">#111827</color>
<dimen name="spacing_md">16dp</dimen>
<dimen name="font_size_base">16sp</dimen>
```

Use snake_case. Resource type serves as implicit prefix.

### JavaScript / TypeScript

```ts
export const colorTextPrimary = '#111827';
export const spacingMd = '16px';
export const fontSizeBase = '1rem';
```

Use camelCase. Export from a module.

---

## Casing Conventions

| Platform | Convention | Example |
|----------|-----------|---------|
| CSS | kebab-case | `--color-text-primary` |
| JavaScript | camelCase | `colorTextPrimary` |
| Swift | camelCase | `colorTextPrimary` |
| Kotlin | camelCase | `colorTextPrimary` |
| Android XML | snake_case | `color_text_primary` |
| Sass | kebab-case | `$color-text-primary` |
| JSON source | kebab-case or nested objects | `color.text.primary` |

### Automatic Casing Transforms

Style Dictionary can transform names automatically:

```js
// Built-in transforms
'name/cti/kebab'    // color-text-primary
'name/cti/camel'    // colorTextPrimary
'name/cti/pascal'   // ColorTextPrimary
'name/cti/snake'    // color_text_primary
'name/cti/constant' // COLOR_TEXT_PRIMARY
```

---

## Namespace Strategies

### Organization Namespace

For published token packages, prefix with an org or system name:

```
--ds-color-text-primary      (design system)
--acme-color-text-primary    (organization)
```

This prevents collisions when multiple design systems coexist on the same page.

### Component Namespace

Component-level tokens include the component name:

```
--button-color-background
--button-color-text
--button-border-radius
--button-padding-x
--button-padding-y

--card-color-background
--card-border-radius
--card-shadow
```

### Platform Namespace

When tokens from multiple themes share a scope:

```css
[data-theme='light'] {
  --color-background: #ffffff;
}
[data-theme='dark'] {
  --color-background: #0f172a;
}
```

---

## Aliasing Conventions

Aliases reference other tokens using a curly-brace syntax in the source format.

```json
{
  "color": {
    "interactive": {
      "default": { "value": "{color.blue.600}" },
      "hover": { "value": "{color.blue.700}" },
      "active": { "value": "{color.blue.800}" }
    }
  }
}
```

### Rules for Aliasing

1. **Primitives never reference other tokens.** They are the raw source values.
2. **Semantic tokens always reference primitives** (or other semantics in rare cases).
3. **Component tokens reference semantic tokens**, never primitives.
4. **Avoid circular references.** Token A referencing Token B that references Token A.
5. **Keep alias chains short.** Ideally one hop: primitive -> semantic. At most two hops: primitive -> semantic -> component.

### Multi-Theme Aliasing

```json
{
  "color": {
    "text": {
      "primary": {
        "value": "{color.gray.900}",
        "dark": { "value": "{color.gray.50}" }
      }
    }
  }
}
```

---

## Deprecated Token Handling

When a token is being phased out, mark it clearly and provide a migration path.

### In Source Files

```json
{
  "color": {
    "brand": {
      "value": "{color.blue.600}",
      "deprecated": true,
      "deprecated-comment": "Use color.interactive.default instead. Will be removed in v4.0."
    }
  }
}
```

### In CSS Output

```css
/* DEPRECATED: Use --color-interactive-default instead. Removal in v4.0. */
--color-brand: var(--color-interactive-default);
```

### In TypeScript Output

```ts
/**
 * @deprecated Use `colorInteractiveDefault` instead. Removal in v4.0.
 */
export const colorBrand = colorInteractiveDefault;
```

### Deprecation Workflow

1. Add `deprecated: true` and `deprecated-comment` to the token source.
2. Generate output with deprecation warnings (JSDoc `@deprecated`, CSS comments).
3. Announce in release notes with migration instructions.
4. Run a deprecation lint rule that warns consumers.
5. Remove the token in the next major version.

---

## Documentation Standards

### Token Documentation Template

Every token should include:

```json
{
  "color-text-primary": {
    "value": "#111827",
    "type": "color",
    "description": "Primary text color for body content and headings",
    "tier": "semantic",
    "references": "color.gray.900",
    "usage": "Default text color for paragraphs, headings, and labels",
    "a11y": "Meets WCAG AA contrast ratio (7:1) against color-background-default"
  }
}
```

### Token Catalog Format

| Token | Value | Tier | Description |
|-------|-------|------|-------------|
| `color-text-primary` | `#111827` | Semantic | Primary body text color |
| `color-text-secondary` | `#6b7280` | Semantic | Supporting text, captions |
| `color-text-inverse` | `#f9fafb` | Semantic | Text on dark backgrounds |
| `color-interactive-default` | `#2563eb` | Semantic | Links, buttons, interactive elements |
| `spacing-sm` | `8px` | Global | Tight spacing between related elements |
| `spacing-md` | `16px` | Global | Standard component internal spacing |

### Naming Checklist

Before finalizing a token name, verify:

- [ ] Follows CTI structure (category-type-item)
- [ ] Describes purpose, not appearance (semantic, not absolute)
- [ ] Uses consistent vocabulary with existing tokens
- [ ] Does not duplicate an existing token's meaning
- [ ] Works across all supported themes
- [ ] Has a clear, non-ambiguous name
- [ ] Includes deprecation annotations if replacing another token

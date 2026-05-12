---
name: design-tokens
description: Use when implementing or refactoring design tokens, setting up Style Dictionary, defining a three-tier token architecture, wiring multi-platform output (web/iOS/Android), or auditing existing tokens for naming and reference integrity.
metadata:
   references:
   - references/naming-conventions.md
   - references/platform-output.md
   - references/token-taxonomy.md
---

# Design Tokens

## Workflow

1. **Define globals** (`tokens/global.json`) — raw values, no semantics.
2. **Create alias mappings** (`tokens/alias.json`) — semantic role → global ref.
3. **Bind component tokens** (`tokens/components/*.json`) — component → alias ref.
4. **Validate** — lint names, check unused, verify no broken refs.
5. **Generate platform outputs** via Style Dictionary (CSS, iOS, Android, JS).

Validate after each step before proceeding.

## Source Token File (`tokens/global.json`)

```json
{
  "color": {
    "blue":  { "500": { "value": "#3b82f6", "type": "color" },
               "600": { "value": "#2563eb", "type": "color" } },
    "gray":  { "100": { "value": "#f3f4f6", "type": "color" },
               "900": { "value": "#111827", "type": "color" } }
  },
  "spacing": {
    "1": { "value": "0.25rem", "type": "dimension" },
    "2": { "value": "0.5rem",  "type": "dimension" },
    "4": { "value": "1rem",    "type": "dimension" }
  }
}
```

`tokens/alias.json`:

```json
{
  "color": {
    "primary":       { "value": "{color.blue.500}" },
    "primary-hover": { "value": "{color.blue.600}" },
    "surface":       { "value": "{color.gray.100}" },
    "on-surface":    { "value": "{color.gray.900}" }
  }
}
```

## Style Dictionary Config (`style-dictionary.config.js`)

```js
module.exports = {
  source: ["tokens/**/*.json"],
  platforms: {
    css: {
      transformGroup: "css",
      buildPath: "build/css/",
      files: [{ destination: "tokens.css", format: "css/variables",
                options: { outputReferences: true } }]
    },
    ios: {
      transformGroup: "ios-swift",
      buildPath: "build/ios/",
      files: [{ destination: "Tokens.swift", format: "ios-swift/class.swift",
                className: "Tokens" }]
    },
    android: {
      transformGroup: "android",
      buildPath: "build/android/",
      files: [
        { destination: "colors.xml",  format: "android/colors" },
        { destination: "dimens.xml",  format: "android/dimens" }
      ]
    },
    js: {
      transformGroup: "js",
      buildPath: "build/js/",
      files: [{ destination: "tokens.js", format: "javascript/es6" }]
    }
  }
};
```

Run: `npx style-dictionary build`

## Validation Checkpoints

Run each between steps. Fail closed.

```bash
# 1. Lint token names match convention: --category-property-variant-state
rg -o '"[a-z]+(\.[a-z0-9-]+)+"' tokens/ | \
  rg -v '^"(color|spacing|size|font|shadow|radius|opacity|duration|z)\.' && \
  echo "FAIL: tokens violate naming convention"

# 2. Verify no broken alias references
node -e "
const sd = require('style-dictionary').extend('./style-dictionary.config.js');
try { sd.buildAllPlatforms(); } catch(e) { process.exit(1); }
"

# 3. Detect unused tokens (build CSS, then grep components for usage)
diff <(rg -o -- '--[a-z0-9-]+' build/css/tokens.css | sort -u) \
     <(rg -o -- '--[a-z0-9-]+' src/ | sort -u) | rg '^<' && \
  echo "WARN: unused tokens above"

# 4. No raw hex values in components (tokens-only enforcement)
rg '#[0-9a-fA-F]{3,8}\b' src/components/ && echo "FAIL: raw hex in components"
```

Pass criteria: lint exits clean, build succeeds, no raw hex in `src/components/`.

## Three-Tier Naming Pattern

`--{category}-{property}-{variant}-{state}` — e.g. `--color-primary-hover`, `--button-bg-disabled`.

Theme overrides happen only at the alias tier:

```css
[data-theme="dark"] {
  --color-primary: var(--color-blue-400);
  --color-surface: var(--color-gray-900);
}
```

## References

- [Token Taxonomy](references/token-taxonomy.md) — categories, tiers, full examples
- [Naming Conventions](references/naming-conventions.md) — CTI, Polaris/Carbon/Atlassian patterns
- [Platform Output](references/platform-output.md) — Style Dictionary transforms, CI publishing

## Next Steps

- **[Design System Creation](../design-system-creation/SKILL.md)**: Use tokens as the foundation of the full design system
- **[Component Library](../component-library/SKILL.md)**: Consume tokens in component implementations
- **[Color Systems](../color-systems/SKILL.md)**: Define color token scales, semantic mapping, and contrast requirements
- **[Typography Systems](../typography-systems/SKILL.md)**: Implement type scale tokens and fluid typography

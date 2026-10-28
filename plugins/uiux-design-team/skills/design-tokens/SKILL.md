---
name: design-tokens
description: Guides design token architecture and Style Dictionary configuration, generates token files for web CSS variables, iOS, and Android, and audits token naming and reference integrity. Use when implementing or refactoring design tokens, setting up Style Dictionary, defining a three-tier token architecture, wiring multi-platform output (web/iOS/Android), or auditing existing tokens for naming and reference integrity.
metadata:
   style-dictionary-version: "4.x / 5.x"
   last-verified: "2026-10-27"
   assets:
   - assets/validate-tokens.mjs
   - assets/validate-tokens.test.mjs
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
    "primary":       { "value": "{color.blue.500}", "type": "color" },
    "primary-hover": { "value": "{color.blue.600}", "type": "color" },
    "surface":       { "value": "{color.gray.100}", "type": "color" },
    "on-surface":    { "value": "{color.gray.900}", "type": "color" }
  },
  "spacing": {
    "inset-x":       { "value": "{spacing.4}", "type": "dimension" },
    "inset-y":       { "value": "{spacing.2}", "type": "dimension" }
  }
}
```

Give every alias an explicit `type`. A reference does not inherit the type of
the token it points to, and type-filtered formats such as `android/colors`
silently drop untyped tokens.

`tokens/components/button.json` (step 3 — component tokens referencing alias tier):

```json
{
  "button": {
    "bg":             { "value": "{color.primary}",        "type": "color" },
    "bg-hover":       { "value": "{color.primary-hover}",  "type": "color" },
    "bg-disabled":    { "value": "{color.surface}",        "type": "color" },
    "text":           { "value": "{color.on-surface}",     "type": "color" },
    "padding-x":      { "value": "{spacing.inset-x}",      "type": "dimension" },
    "padding-y":      { "value": "{spacing.inset-y}",      "type": "dimension" }
  }
}
```

Component tokens always reference alias names, never global names directly.
This applies to every category (spacing, radius, weight), not just color. The
only literals allowed are keywords such as `transparent` or `none`.

## Style Dictionary Config (`style-dictionary.config.mjs`)

Targets Style Dictionary v4 (Node 18+) or v5 (Node 22+), both ESM with an async API. v3 used a different API
(`require(...).extend()`, synchronous builds); pin `style-dictionary@^5` or
`@^4` in `package.json`.

```js
export default {
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
                options: { className: "Tokens" } }]
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

Run: `npx style-dictionary build --config style-dictionary.config.mjs`

A build that exits 0 can still emit unusable output. Check that
`build/ios/Tokens.swift` declares `public class Tokens` and that
`build/android/colors.xml` contains the alias colors (`color_primary`, ...).

## Validation Checkpoints

Run after each workflow step. Fail closed: any failure exits nonzero.

```bash
npm install --save-dev @babel/parser@^7   # parses JS/JSX/TS for the raw-hex check (Node 18+)
cp <skill>/assets/validate-tokens.mjs scripts/validate-tokens.mjs
node scripts/validate-tokens.mjs
```

[`assets/validate-tokens.mjs`](assets/validate-tokens.mjs) loads the config through the Style
Dictionary v4+/v5 API and checks:

1. **Names.** Every token path segment is lowercase kebab-case.
2. **References and tiers.** All references resolve. Globals hold raw values,
   aliases reference globals, and components reference aliases.
3. **No raw hex** under `src/components/`. CSS declaration values are checked
   (wrapped lines included). JS/JSX/TS is parsed with `@babel/parser`: every
   string and template piece counts, and `css`/`styled` templates are read as
   CSS with their `${...}` interpolations checked as JS. `style="..."` and `:style`
   in HTML, Vue and Svelte are checked too. ID selectors, `href="#abc"`,
   `querySelector("#abc")`, import paths and `url(#abc)` pass. A file that
   doesn't parse, or a missing directory, is an error, not a pass.
4. **Unused tokens** (warning only). These are component tokens that no
   `var(--…)` in `src/components/` uses, plus aliases and globals that nothing
   references.

Pass criteria: the script exits 0 and the build succeeds. The scanner's
regression cases live in [`assets/validate-tokens.test.mjs`](assets/validate-tokens.test.mjs)
(`node --test`); add a case there when you change what counts as a raw colour. Test the checks
themselves by injecting a bad name, a broken reference, a literal value in
an alias and a raw hex value; each must make the script exit 1.

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

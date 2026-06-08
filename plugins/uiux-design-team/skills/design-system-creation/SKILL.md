---
name: design-system-creation
description: Scaffolds design system infrastructure, generates Style Dictionary token configs, produces component templates and Storybook setups, and creates UI audit reports. Use when bootstrapping a new design system from scratch, auditing an existing UI for systemization, setting up Storybook + Style Dictionary scaffolding, or defining governance and versioning for a shared component system.
metadata:
   references:
   - references/atomic-design-guide.md
   - references/component-api-guide.md
   - references/component-template.md
   - references/theming-patterns.md
   - references/token-architecture.md
---

# Design System Creation

## Quick Start

1. **Audit existing UI** — screenshot each unique screen; tag duplicate/inconsistent patterns.
2. **Define tokens** — see sample `tokens.json` below; build via Style Dictionary.
3. **Build atoms** → **molecules** → **organisms** → **templates**. See [atomic-design-guide.md](references/atomic-design-guide.md).
4. **Wire Storybook** — see config below.
5. **Validate** at each tier (commands below).
6. **Document + version** — see [theming-patterns.md](references/theming-patterns.md) and [component-api-guide.md](references/component-api-guide.md).

## Sample `tokens/core.json`

```json
{
  "color": {
    "brand": { "500": { "value": "#5B5BD6", "type": "color" } },
    "neutral": { "0": { "value": "#FFFFFF", "type": "color" },
                  "900": { "value": "#0B0D12", "type": "color" } }
  },
  "spacing": { "1": { "value": "4px" }, "2": { "value": "8px" }, "4": { "value": "16px" } },
  "radius":  { "sm": { "value": "4px" }, "md": { "value": "8px" } },
  "font":    { "size": { "body": { "value": "16px" }, "h1": { "value": "32px" } } }
}
```

## Style Dictionary Config (`sd.config.js`)

```js
module.exports = {
  source: ["tokens/**/*.json"],
  platforms: {
    css: { transformGroup: "css", buildPath: "dist/",
           files: [{ destination: "tokens.css", format: "css/variables" }] },
    js:  { transformGroup: "js",  buildPath: "dist/",
           files: [{ destination: "tokens.js", format: "javascript/es6" }] }
  }
};
```

## Component Template & Storybook Config

See [component-template.md](references/component-template.md) for the full React + CVA Button template, Storybook `main.ts` config, and a matching `Button.stories.tsx` example.

## Validation Checkpoints

```bash
# 1. After tokens build: ensure no raw hex in components
rg "#[0-9a-fA-F]{6}" src/components/ && echo "FAIL: replace with tokens"

# 2. After atoms built: a11y audit via Storybook test runner
npx test-storybook --url http://127.0.0.1:6006

# 3. After each tier: type-check + visual regression
tsc --noEmit && npx chromatic --exit-zero-on-changes

# 4. Before release: verify semver — breaking API changes require major bump
npx changeset status --since=origin/main
```

Pass criteria per checkpoint: (1) exits clean, (2) zero a11y violations on built stories, (3) tsc clean + visual diffs reviewed, (4) changeset matches change scope.

## References

- [token-architecture.md](references/token-architecture.md), [component-api-guide.md](references/component-api-guide.md), [theming-patterns.md](references/theming-patterns.md), [atomic-design-guide.md](references/atomic-design-guide.md), [component-template.md](references/component-template.md)

## Next Steps

[design-tokens](../design-tokens/SKILL.md) · [component-library](../component-library/SKILL.md) · [visual-design](../visual-design/SKILL.md) · [design-handoff](../design-handoff/SKILL.md)

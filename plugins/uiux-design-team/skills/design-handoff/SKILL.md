---
name: design-handoff
description: Use when packaging a design for developer implementation, writing component specifications, running design QA against a built UI, exporting assets from Figma, or resolving design-vs-code drift before a release.
metadata:
   references:
   - references/annotation-guide.md
   - references/handoff-checklist.md
   - references/qa-process.md
---

# Design Handoff

## Pre-Handoff Checklist

Tick every item before transferring to engineering. Missing items become implementation debt.

- [ ] **Tokens, not raw values** — every spec uses `--spacing-4` / `--color-primary`, never `16px` / `#3b82f6`.
- [ ] **All interaction states** — default, hover, active, focus, disabled, loading, error, empty.
- [ ] **Responsive behavior** — what reflows / stacks / hides / resizes at each breakpoint.
- [ ] **Accessibility notes** — ARIA roles, labels, keyboard order, contrast verified.
- [ ] **Motion specs** — duration, easing, trigger, properties for every transition.
- [ ] **Edge cases** — long text, missing data, error recovery, localization expansion.
- [ ] **Assets exported** — SVG icons, WebP/AVIF images, named per convention.

## Asset Export

```bash
# Figma assets via figma-export CLI
npx figma-export use-config

# Or via REST:
curl -H "X-Figma-Token: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/images/$FILE_KEY?ids=$NODE_IDS&format=svg&scale=2" \
  | jq -r '.images[]' | xargs -I{} curl -o "./assets/{}.svg" "{}"

# Optimize SVGs
npx svgo --multipass --folder ./assets

# Convert raster to WebP/AVIF
npx @squoosh/cli --webp '{"quality":85}' --avif '{"cqLevel":30}' ./images/*.png
```

## Component Spec Format

For every interactive component, ship this state matrix:

| State | Background | Text | Border | Shadow | Cursor | Opacity |
|-------|-----------|------|--------|--------|--------|---------|
| Default | `--color-surface` | `--color-on-surface` | `--border-default` | `--shadow-sm` | pointer | 1 |
| Hover | `--color-surface-hover` | `--color-on-surface` | `--border-hover` | `--shadow-md` | pointer | 1 |
| Active | `--color-surface-active` | `--color-on-surface` | `--border-active` | none | pointer | 1 |
| Focus | `--color-surface` | `--color-on-surface` | `--border-focus` | `--shadow-focus` | pointer | 1 |
| Disabled | `--color-surface-disabled` | `--color-on-surface-disabled` | `--border-disabled` | none | not-allowed | 0.6 |
| Loading | `--color-surface` | `--color-on-surface-muted` | `--border-default` | `--shadow-sm` | wait | 0.8 |
| Error | `--color-error-surface` | `--color-error` | `--border-error` | none | pointer | 1 |

Box-model annotation block (paste into Figma comment or spec doc):

```
[Button / Primary]
├── Width: auto (min 96px) | Height: --size-10
├── Padding: --spacing-2 --spacing-4
├── Background: --color-primary
├── Border: 1px solid transparent | Radius: --radius-md
├── Typography: --font-sans / --text-sm / 600 / --leading-tight
└── Color: --color-on-primary
```

## Design QA Workflow

Run after the engineer says "done", before sign-off. Each gate has a documented failure path.

### Gate 1 — Visual fidelity

Compare implemented page against the Figma frame side-by-side. Verify spacing rhythm, typography hierarchy, color application, component proportions.

**Fail path:** open a ticket with [screenshot from Figma | screenshot from build | element selector | token expected vs token used]. Re-run Gate 1 after fix.

### Gate 2 — Responsive

Test at 320, 375, 768, 1024, 1440, 1920px (Chrome DevTools `Cmd+Shift+M`). Verify layout matches the responsive spec; check overflow, truncation, and touch targets.

**Fail path:** record the breakpoint and behavior. If a layout shift wasn't specified, escalate to design — do not let the engineer invent it.

### Gate 3 — Interaction states

Hover, tab through, submit invalid, trigger loading, empty the data. Each state must match the matrix above.

**Fail path:** flag missing states. Loop back to design if any state was never specified.

### Gate 4 — Accessibility

```bash
npx @axe-core/cli https://staging.example.com/page --tags wcag2aa
npx pa11y https://staging.example.com/page --standard WCAG2AA
```

Plus manual: keyboard-only flow, screen reader on critical paths, contrast for focus ring against every background it lands on.

**Pass criteria:** 0 critical / serious axe violations, 0 pa11y errors, all interactive elements reachable.

### Gate 5 — Performance

```bash
npx lighthouse https://staging.example.com/page \
  --only-categories=performance \
  --output=json --output-path=lh.json \
  --chrome-flags="--headless" \
  --throttling-method=devtools
```

**Pass criteria:** LCP < 2.5s, CLS < 0.1, INP < 200ms, Performance score ≥ 90. Verify animations hold 60fps in DevTools Performance panel.

**Fail path:** Performance regressions get a dedicated ticket (not bundled with visual bugs). Re-verify only the failing metric after the fix.

### Sign-off

All five gates green → mark the Figma frame "Implemented" and close the handoff ticket. Any gate red → block release.

## Deep Dive References

- [references/handoff-checklist.md](references/handoff-checklist.md) — full pre-handoff checklist with examples
- [references/annotation-guide.md](references/annotation-guide.md) — what to annotate, tools, full spec formats
- [references/qa-process.md](references/qa-process.md) — full QA checklists, cross-browser, device matrix, bug template

## Next Steps

- **[Design System Creation](../design-system-creation/SKILL.md)**: ensure tokens behind the handoff are complete
- **[Accessibility Audit](../accessibility-audit/SKILL.md)**: full a11y review
- **[Component Library](../component-library/SKILL.md)**: verify component code matches spec
- **[CSS Architecture](../css-architecture/SKILL.md)**: enforce token architecture in CSS

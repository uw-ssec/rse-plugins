---
name: accessibility-audit
description: Use when auditing a web interface for WCAG 2.2 AA/AAA compliance, fixing reported accessibility violations, verifying ARIA usage, checking keyboard navigation or color contrast, or preparing accessibility documentation for a release.
metadata:
   references:
   - references/aria-patterns.md
   - references/contrast-guide.md
   - references/inclusive-design.md
   - references/keyboard-nav-guide.md
   - references/wcag-checklist.md
---

# Accessibility Audit

## Audit Workflow

### Step 1 — Automated scan (axe + pa11y + Lighthouse)

Run all three. Each catches different issues.

```bash
# axe-core CLI (most accurate rule coverage)
npx @axe-core/cli https://example.com --tags wcag2a,wcag2aa,wcag22aa --save axe-report.json

# pa11y (CI-friendly, exits non-zero on failures)
npx pa11y --standard WCAG2AA --reporter json https://example.com > pa11y-report.json

# Lighthouse (accessibility category)
npx lighthouse https://example.com --only-categories=accessibility --output=json --output-path=lh-report.json --chrome-flags="--headless"
```

Expected axe output shape:
```json
{"violations":[{"id":"color-contrast","impact":"serious","nodes":[{"target":["#cta-btn"],"failureSummary":"..."}]}]}
```

**Checkpoint:** If axe reports any `impact: "critical"` or `impact: "serious"` violations, fix before proceeding to Step 2. Lighthouse accessibility score must be ≥ 95.

### Step 2 — Keyboard pass

Tab through the entire flow. For each interactive element verify: receives focus, has visible focus ring, responds to Enter/Space, no traps, Escape closes overlays, focus restores on close.

**Pass/fail:** Every interactive element reachable and operable with keyboard only. Skip link present and works on first Tab.

### Step 3 — Screen reader pass

Test critical flows with VoiceOver (macOS: `Cmd+F5`) or NVDA (Windows). Verify each control announces role + name + state. Verify form errors are announced via `aria-live` or `role="alert"`. Verify dynamic updates reach the user.

**Pass/fail:** No control announces as "button" with no name. No silent state changes on submit/error.

### Step 4 — Contrast & zoom

- Run axe color-contrast (already in Step 1). Cross-check focus rings against all backgrounds (axe misses these).
- Zoom to 200% and 400% — no horizontal scroll, no clipped content, no overlap.
- Test light, dark, and forced-colors / high-contrast modes.

**Pass/fail:** Text ≥ 4.5:1, large text ≥ 3:1, UI components ≥ 3:1, focus indicators ≥ 3:1 against adjacent colors.

### Step 5 — Content review

Link text descriptive (no "click here"), `<html lang>` set, error messages identify the field and suggest a fix, captions on video, `alt` on images (`alt=""` if decorative).

### Step 6 — Document findings

Use this table format for the report:

```markdown
| # | WCAG SC | Severity | Location | Issue | Fix | Status |
|---|---------|----------|----------|-------|-----|--------|
| 1 | 1.4.3 Contrast (Min) | Critical | /pricing #cta-btn | 3.2:1 white on #6FA8DC | Use #1A5490 (8.1:1) | Open |
| 2 | 2.4.7 Focus Visible | Serious | global `button:focus { outline: none }` | No focus indicator | Add `:focus-visible { outline: 2px solid var(--focus) }` | Fixed |
| 3 | 4.1.2 Name/Role/Value | Critical | header search icon button | No accessible name | Add `aria-label="Search"` | Open |
```

## Top 10 Common Failures (Fix Order)

| # | Failure | Quick Fix |
|---|---------|-----------|
| 1 | Missing alt text | Add descriptive `alt`; `alt=""` for decorative |
| 2 | Low contrast text | Raise to ≥ 4.5:1 (normal) / 3:1 (large) |
| 3 | Missing form labels | `<label for="id">` matching input `id` |
| 4 | No keyboard access | Native `<button>`/`<a>`, or `tabindex="0"` + key handlers |
| 5 | No focus indicator | Never strip `outline` without `:focus-visible` replacement |
| 6 | ARIA misuse | Prefer semantic HTML; ARIA only when no native equivalent |
| 7 | Auto-playing media | Provide pause; respect `prefers-reduced-motion` |
| 8 | Skipped heading levels | H1 → H2 → H3, never skip |
| 9 | Color-only signaling | Add icon, text, or pattern alongside color |
| 10 | Inaccessible custom controls | Follow WAI-ARIA Authoring Practices |

## Automated vs Manual Coverage

Automation catches ~30% of WCAG issues. The rest needs human judgment.

| Automation catches | Manual required |
|--------------------|-----------------|
| Missing alt, invalid ARIA, duplicate IDs, contrast ratios, missing labels | Alt-text quality, focus order, screen-reader narration, cognitive clarity, dynamic announcement, touch-target adequacy |

## Deep Dive References

- [references/wcag-checklist.md](references/wcag-checklist.md) — full WCAG 2.2 success criteria tables (POUR)
- [references/aria-patterns.md](references/aria-patterns.md) — dialog, tabs, combobox, menu, tree, live regions
- [references/keyboard-nav-guide.md](references/keyboard-nav-guide.md) — focus management, roving tabindex, skip links
- [references/contrast-guide.md](references/contrast-guide.md) — ratio requirements, theming, fixes
- [references/inclusive-design.md](references/inclusive-design.md) — disability spectrum, cognitive accessibility

## Next Steps

- **[Inclusive Design](references/inclusive-design.md)**: Move beyond compliance to broad-spectrum inclusion
- **[UX Writing](../ux-writing/SKILL.md)**: Error messages and microcopy
- **[Color Systems](../color-systems/SKILL.md)**: Bake contrast into the palette
- **[Frontend Components](../frontend-components/SKILL.md)**: Accessible component implementations

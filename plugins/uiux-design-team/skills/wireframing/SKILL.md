---
name: wireframing
description: Use when sketching a new screen before visual design, when restructuring an existing page's content priority, when validating layout feasibility with engineering, or when communicating responsive behavior across breakpoints.
metadata:
   references:
   - references/content-hierarchy.md
   - references/layout-systems.md
   - references/wireframe-patterns.md
---

# Wireframing

## Workflow (input → output)

Given a user request for a wireframe:

1. **Identify page type** — landing, dashboard, list/detail, settings, form, search results.
2. **List content blocks in priority order** — number each block 1..N (1 = highest).
3. **Pick a layout pattern** from the catalog below that matches the page type.
4. **Produce annotated ASCII wireframe** at desktop (1280px) — label every block, attach numbered notes for interaction/conditional/responsive behavior.
5. **Add responsive notes** — describe mobile (375px) and tablet (768px) reflow rules.

Output format: ASCII block + numbered notes table + responsive notes section.

**Fidelity selector:**
- Low-fi (boxes + labels): exploration, structure debates
- Mid-fi (real content lengths): hierarchy validation, usability testing
- Hi-fi (precise spacing, near-final): final approval, dev handoff

## Worked example

**Input:** "Create a wireframe for a SaaS pricing page."

**Output:**

```
+----------------------------------------------------------------+
| [Logo]   Product  Pricing  Docs  Blog        [Sign in] [Try]  | (1)
+----------------------------------------------------------------+
|                                                                |
|         Simple pricing. No surprises.                          | (2)
|         Pick a plan, change anytime.                           |
|                                                                |
|         [ Monthly | Annual -20% ]                              | (3)
|                                                                |
+----------------------------------------------------------------+
|  +------------+   +------------+   +------------+              |
|  | Starter    |   | Pro ★      |   | Enterprise |              | (4)
|  | $0/mo      |   | $29/mo     |   | Contact us |              |
|  |  - 3 seats |   |  - 25 seats|   |  - Unltd   |              |
|  |  - Basic   |   |  - SSO     |   |  - SLA     |              |
|  | [Get free] |   | [Start trl]|   | [Talk]     |              |
|  +------------+   +------------+   +------------+              |
+----------------------------------------------------------------+
|  Compare plans (collapsible feature matrix)                    | (5)
+----------------------------------------------------------------+
|  Logos: Acme, Globex, Initech, Umbrella                        | (6)
+----------------------------------------------------------------+
|  FAQ accordion (5 items)                                       | (7)
+----------------------------------------------------------------+
|  Footer                                                        |
+----------------------------------------------------------------+
```

| # | Block | Notes |
|---|-------|-------|
| 1 | Header | Sticky on scroll. Trial CTA always visible. |
| 2 | Headline | Plain language. No jargon. |
| 3 | Toggle | Default = Annual (highest LTV). Persist choice in URL. |
| 4 | Plan cards | Highlight Pro with badge + scale 1.05. CTAs route to signup with plan preselected. |
| 5 | Comparison | Collapsed by default; expand updates URL hash. |
| 6 | Social proof | Grayscale logos, color on hover. |
| 7 | FAQ | One open at a time; structured data for SEO. |

**Responsive:**
- Mobile (375px): cards stack vertically; Pro card first. Header collapses to hamburger; trial CTA persists in header.
- Tablet (768px): cards 2-up + 1; nav stays inline.

## Page-type catalog (with ASCII)

### Dashboard (1280px)

```
+--------+----------------------------------------------------+
| Logo   |  Page title              [Search]  [Avatar]       |
+--------+----------------------------------------------------+
| Nav    |  KPI 1 | KPI 2 | KPI 3 | KPI 4                    |
|  Home  |--------+-------+-------+--------                   |
|  Users |                                                    |
|  Data  |  +-------------------- Chart -------------------+  |
|  Bills |  |                                              |  |
|  ...   |  +----------------------------------------------+  |
|        |                                                    |
|        |  Recent activity (table, 10 rows, paginated)      |
+--------+----------------------------------------------------+
```

### List/Detail (master-detail, 1280px)

```
+----------------+-------------------------------------------+
| [Search]       |  Subject: Re: Q3 budget review            |
| [Filter ▾]     |  From: alex@acme.co · 2h ago              |
|----------------|-------------------------------------------|
| ● Item 1   2h  |                                           |
|   Preview…     |  Body of the selected item renders here. |
|----------------|  Toolbar: Reply | Forward | Archive       |
|   Item 2   5h  |                                           |
|   Preview…     |  Attachments (2)                          |
|----------------|                                           |
|   Item 3   1d  |                                           |
+----------------+-------------------------------------------+
```

More patterns (settings, form, search results, landing mobile): [wireframe-patterns.md](references/wireframe-patterns.md), [layout-systems.md](references/layout-systems.md).

## Annotation conventions

| Type | Format |
|------|--------|
| Content | Callout with description |
| Interaction | Numbered note: "On click → opens modal X" |
| Conditional | "If logged in, show Y; else show Z" |
| Responsive | "At <768px: stack vertically" |
| Data source | "Populated from /api/v2/plans" |
| Constraint | "Max 120 chars", "16:9 ratio" |

## Responsive checkpoints

Document at 375 / 768 / 1280px:
- What reflows or stacks?
- What hides or collapses (and how is it accessed)?
- How does navigation transform (tabs → hamburger, sidebar → bottom bar)?
- Are touch targets ≥ 44×44 px on mobile?

## Next Steps

- **[Information Architecture](../information-architecture/SKILL.md)**: align wireframe structure with IA
- **[Visual Design](../visual-design/SKILL.md)**: apply style/color/type to wireframes
- **[Responsive Design](../responsive-design/SKILL.md)**: implement fluid layouts in code
- **[Design Handoff](../design-handoff/SKILL.md)**: annotate for engineering

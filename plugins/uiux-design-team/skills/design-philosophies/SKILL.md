---
name: design-philosophies
description: Use when running a heuristic evaluation, structuring a design critique, selecting which design framework to apply for a given project context, or auditing a UI against Gestalt/Nielsen/Rams principles.
metadata:
   references:
   - references/apple-hig.md
   - references/design-thinking.md
   - references/dieter-rams-principles.md
   - references/emotional-design.md
   - references/gestalt-principles.md
   - references/material-design.md
   - references/nielsen-heuristics.md
---

# Design Philosophies

## Philosophy Selection Framework

| Context | Primary | Supporting |
|---------|---------|-----------|
| New product, unclear users | Design Thinking | JTBD, HCD |
| Complex information display | Gestalt | Nielsen |
| Premium/luxury | Emotional Design + Rams | Apple HIG |
| Enterprise SaaS | Nielsen | Material, Inclusive |
| Consumer mobile | Apple HIG / Material | Gestalt, Emotional |
| Accessibility-first | Inclusive | WCAG 2.2, Nielsen |
| Developer tool | Rams ("less but better") | Nielsen, Gestalt |
| Content platform | Gestalt + Emotional | Apple HIG |
| E-commerce | Nielsen | Emotional, Gestalt |
| Design system | Rams + Gestalt | Material, Inclusive |

Decision rule: pick **one** primary as backbone; use supporting frameworks only to fill gaps the primary leaves unaddressed.

## Heuristic Evaluation Template (Nielsen)

```markdown
# Heuristic Evaluation: <product/flow>
Evaluator: <name>  Date: <YYYY-MM-DD>  Scope: <screens or task>

## Findings
| # | Heuristic | Severity (0-4) | Location | Issue | Recommendation |
|---|-----------|----------------|----------|-------|----------------|
| 1 | H1 Visibility of system status | 3 | Checkout step 2 | No spinner during 4s payment call | Show inline progress + disable submit |
| 2 | H5 Error prevention            | 4 | Account delete | One-click, irreversible | Add typed-confirmation modal |
...

## Severity scale
0=not a problem · 1=cosmetic · 2=minor · 3=major · 4=catastrophic

## Summary
- Total findings: N
- Severity ≥3: M  (must fix before ship)
- Top 3 systemic patterns: ...
```

Rule: every finding cites a specific heuristic number; recommendations reference the same principle.

## Design Critique Output Format

```markdown
# Critique: <artifact>
Philosophy applied: <primary>  Supporting: <list>

## Strengths (3-5)
- [Principle name] What works and why, tied to principle

## Issues (ranked by severity)
1. [Principle name] Specific issue → concrete fix
2. ...

## Open questions
- ...

## Validation
- [ ] Every recommendation cites which principle it derives from
- [ ] No recommendation contradicts the chosen primary philosophy
- [ ] Severity rated; top item is a must-fix
```

## Gestalt Layout Checklist

Run against any composed screen:

- [ ] **Proximity**: related elements grouped via spacing (no orphan labels)
- [ ] **Similarity**: like things look alike (consistent button family, icon stroke)
- [ ] **Common region**: cards/fieldsets bound related content
- [ ] **Continuation**: alignment creates reading lines (left edge, baseline grid)
- [ ] **Figure-ground**: foreground vs background clear (modal dim, card elevation)
- [ ] **Closure**: incomplete shapes work (skeleton/progress) — none accidental
- [ ] **Symmetry/order**: intentional balance, not arbitrary

## Worked Example (input → output)

Input UI (ASCII):

```
[Logo]  Home  Products  About                       [Sign in] [Sign up]
─────────────────────────────────────────────────────────────────────
                Welcome!
   [search...........................]            <- centered, isolated
   New arrivals                                    <- left
   [img] $19   [img] $24   [img] $29
   [img] $39   [img] $44   [img] $49
   Save 20% on first order!                        <- floating banner top-right red
```

Philosophy Selection: e-commerce → **Primary: Nielsen** · **Supporting: Emotional Design, Gestalt**.

Critique:

| # | Principle | Sev | Issue → Recommendation |
|---|-----------|-----|------------------------|
| 1 | Nielsen H1 | 3 | "Save 20%" floats untethered → anchor to grid, add countdown (Emotional/visceral) |
| 2 | Gestalt Proximity | 3 | Centered search, left-aligned products imply unrelated → left-align OR add label |
| 3 | Nielsen H4 | 2 | Sign in/Sign up both gray → promote Sign up to primary intent |
| 4 | Gestalt Similarity | 2 | Inconsistent price formatting → enforce `$XX.00` |
| 5 | Rams #4 | 1 | "Welcome!" carries no info → value-prop subtitle |

Each row cites principle; severity drives ship/no-ship.

## Decision Rules & Pitfalls

- Don't mix Material + Apple HIG in one product — pick one metaphor.
- Rams "less, but better" ≠ minimalism-as-style; it is reduction to essentials.
- Design Thinking is for ambiguous problems; if well-defined, skip to Prototype.
- Emotional/visceral cannot compensate for a broken behavioral layer.
- Inclusive Design ≠ WCAG (floor); inclusive treats diversity as resource.

## Validation Step

Before sign-off:
1. Every recommendation cites a principle from the chosen primary or a named supporting framework.
2. No recommendation violates a Rams principle (especially #6 honest, #2 useful).
3. Heuristic severities ≥3 are tracked as blockers.
4. If a recommendation derives from a supporting philosophy that contradicts the primary, flag for explicit decision.

## References

- [Nielsen Heuristics](references/nielsen-heuristics.md)
- [Gestalt Principles](references/gestalt-principles.md)
- [Emotional Design](references/emotional-design.md) — Norman's three levels in depth
- [Dieter Rams Principles](references/dieter-rams-principles.md)
- [Design Thinking](references/design-thinking.md) — Stanford 5-phase, Double Diamond, facilitation
- [Material Design](references/material-design.md) · [Apple HIG](references/apple-hig.md)

## Next Steps

- **[Design Case Studies](../design-case-studies/SKILL.md)**: Study how real products apply these philosophies
- **[Usability Evaluation](../usability-evaluation/SKILL.md)**: Use Nielsen's heuristics as the foundation for systematic usability review
- **[Visual Design](../visual-design/SKILL.md)**: Apply emotional design and Gestalt principles to create distinctive interfaces
- **[Accessibility Audit](../accessibility-audit/SKILL.md)**: Implement inclusive design through thorough accessibility evaluation

---
name: information-architecture
description: Use when structuring a new site/app's content, when users report "I can't find anything," when running a card sort or tree test, or when auditing navigation labels and taxonomy for an existing product.
metadata:
   references:
   - references/card-sorting-methods.md
   - references/navigation-guide.md
   - references/sitemap-patterns.md
---

# Information Architecture

## Workflow

1. **Inventory content** — list every page/feature/content-type in a spreadsheet (cols: URL, title, type, owner, last-updated, traffic).
2. **Identify user goals** — top 10 tasks users come to do.
3. **Run open card sort** (15-20 participants via Optimal Workshop / Maze).
4. **Draft sitemap** — depth ≤ 4 levels, ≤ 7 siblings per node.
5. **Tree test** — 10+ tasks, 30+ participants.
   - **Pass:** ≥ 70% direct success (target found within 3 clicks, no backtrack) per task.
   - **Fail:** restructure the failing branch and re-test before shipping.
6. **Lock labels** — first-click test the top 10 labels (≥ 80% clicking expected option).
7. **Wire to navigation patterns** — see [navigation-guide.md](references/navigation-guide.md).

## Deliverables (formats in references)

- **Sitemap** — indented tree, depth ≤ 4, siblings ≤ 7. Example: [sitemap-patterns.md](references/sitemap-patterns.md).
- **Card sort analysis** — clusters with agreement %, disputed cards with action, participant vocabulary. Template: [card-sorting-methods.md](references/card-sorting-methods.md).
- **Navigation spec** — pattern + primary/secondary/wayfinding + rationale. Format: [navigation-guide.md](references/navigation-guide.md).

## Labeling audit checklist

For each navigation label, verify:
- [ ] Unambiguous: a stranger can predict what's behind it
- [ ] Consistent: same concept = same word across product
- [ ] User language: matches card-sort vocabulary, not internal jargon
- [ ] Mutually exclusive: no overlap with sibling labels ("Shoes" vs "Footwear")
- [ ] Scannable: meaningful word first ("Account Settings" not "Settings for Your Account")
- [ ] First-click test success ≥ 80%

## Navigation pattern picker

| Pattern | When |
|---------|------|
| Hierarchical tree | Large content sites, docs, enterprise — depth ≤ 4 |
| Flat | 4-7 equal-weight sections; mobile bottom-tab |
| Hub-and-spoke | Independent task flows; rare cross-section nav |
| Sequential | Onboarding, checkout, wizard — always show progress + back |
| Faceted | E-commerce, search-heavy libraries with multi-attribute items |

Details: [navigation-guide.md](references/navigation-guide.md).

## Validation checkpoints

- After card sort: clusters with < 60% agreement → re-run with refined card set.
- After tree test: any task < 70% success → restructure failing branch, re-test.
- After labeling audit: any label with < 80% first-click success → rename.
- After launch: monitor search queries — high volume of "where is X" = IA failure.

## Next Steps

[wireframing](../wireframing/SKILL.md) · [user-research](../user-research/SKILL.md) · [ux-writing](../ux-writing/SKILL.md)

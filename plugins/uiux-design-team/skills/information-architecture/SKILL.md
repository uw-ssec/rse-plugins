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

## Deliverable templates

### Sitemap (indented tree)

```
Root
├── Products
│   ├── Plans & Pricing
│   ├── Features
│   │   ├── Collaboration
│   │   ├── Analytics
│   │   └── Integrations
│   └── Changelog
├── Solutions
│   ├── By Industry
│   │   ├── Healthcare
│   │   └── Finance
│   └── By Team Size
├── Resources
│   ├── Docs
│   ├── Blog
│   ├── Case Studies
│   └── Help Center
├── Company
│   ├── About
│   ├── Careers
│   └── Contact
└── Auth
    ├── Sign in
    └── Sign up
```

Constraints: depth ≤ 4, siblings ≤ 7. Note breadcrumb path for any node ≥ 3 deep.

### Card sort analysis template

```
Study: <name> · Method: open · n=18 · Tool: Optimal Workshop

Top emergent clusters (by agreement %):
1. "Account & Billing"  — 89% agreement — 7 cards
2. "Reports"            — 78% agreement — 6 cards
3. "Team Management"    — 72% agreement — 5 cards
4. "Integrations"       — 67% agreement — 4 cards

Disputed cards (assigned to >2 clusters by >25% of participants):
- "API keys"      → split: Account (45%) vs Integrations (40%)
- "Audit log"     → split: Reports (35%) vs Settings (35%)
  Action: test both placements in tree test.

Vocabulary used by participants (frequency):
- "Settings" 14 · "Preferences" 4 · "Configuration" 2 → use "Settings"
- "Reports" 11 · "Analytics" 7 · "Insights" 3 → use "Reports" (audience match)

Recommendation:
- Top-level IA: Home, Reports, Team, Integrations, Settings, Help
- Move "Audit log" under Settings (matches participant mental model + admin task flow)
```

### Labeling audit checklist

For each navigation label, verify:
- [ ] Unambiguous: a stranger can predict what's behind it
- [ ] Consistent: same concept = same word across product
- [ ] User language: matches card-sort vocabulary, not internal jargon
- [ ] Mutually exclusive: no overlap with sibling labels ("Shoes" vs "Footwear")
- [ ] Scannable: meaningful word first ("Account Settings" not "Settings for Your Account")
- [ ] Tested: first-click success ≥ 80%

### Navigation recommendations (output format)

```
Pattern:    Hub-and-Spoke
Primary:    Bottom tab bar (5 items: Home, Search, Create, Inbox, Profile)
Secondary:  In-screen tabs within each section
Wayfinding: Sticky section title + breadcrumb when depth ≥ 2
Rationale:  Tasks are independent (low cross-section navigation).
            User research showed 92% return to home between tasks.
```

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

## Deep references

- [Sitemap Patterns](references/sitemap-patterns.md) — diagrams + content inventory template
- [Navigation Guide](references/navigation-guide.md) — global/local/mega-menu/mobile patterns
- [Card Sorting Methods](references/card-sorting-methods.md) — open/closed/hybrid, analysis

## Next Steps

- **[Wireframing](../wireframing/SKILL.md)**: translate IA into page layouts
- **[User Research](../user-research/SKILL.md)**: validate IA with real users
- **[UX Writing](../ux-writing/SKILL.md)**: craft labels and microcopy

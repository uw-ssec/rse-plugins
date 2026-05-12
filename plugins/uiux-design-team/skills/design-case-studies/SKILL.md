---
name: design-case-studies
description: Use when analyzing a product's UI/UX to extract transferable patterns, benchmarking your own design against a category leader, looking up how a specific product (Stripe, Linear, Notion, Apple, Spotify, Netflix, Tinder, Airbnb, etc.) solves a design problem, or building a competitive teardown.
metadata:
   references:
   - references/brand-experiences.md
   - references/content-platforms.md
   - references/design-systems-in-practice.md
   - references/developer-tools.md
   - references/e-commerce.md
   - references/mobile-apps.md
   - references/saas-dashboards.md
   - references/emotional-design-growth.md
   - references/psychological-design-engines.md
   - references/saas-conversion-psychology.md
   - references/onboarding-psychology.md
   - references/tinder-dopamine-design.md
   - references/outcome-first-ai-design.md
   - references/peak-end-rule-design.md
   - references/apple-design-principles.md
   - references/spotify-design-moat.md
   - references/netflix-behavioral-design.md
   - references/product-led-growth-funnel.md
---

# Design Case Studies

## Five-Layer Analysis Framework

Apply in order. Each layer feeds the next.

1. **Visceral (3-second reaction)** — name the emotion in one word before analyzing anything.
2. **Aesthetic** — fonts/sizes/hierarchy; palette structure and semantic color use; spacing rhythm; motion duration/trigger.
3. **Usability** — walk the primary flow, mark friction; check Nielsen heuristics; enumerate states (default/hover/focus/loading/empty/error); stress-test edge cases (long text, no data, slow net).
4. **System** — visible token system (spacing, type scale, palette); component DNA; could you add a new screen without inventing patterns?
5. **Philosophy** — map decisions to Gestalt, Rams, Norman's three levels, platform conventions (Material/HIG/custom).

## Analysis Template

```markdown
**Product:** [Name]
**Category:** [SaaS / E-commerce / Content / Mobile / Design System]
**Visceral:** [one word + one sentence]

**Why it works**
| Principle | Concrete application |
|-----------|----------------------|
| ... | ... |

**Key takeaway:** [one sentence]
**Study this closely:** [specific screen, flow, or interaction]
```

## Worked Example — Linear

```markdown
**Product:** Linear
**Category:** SaaS / Project Management
**Visceral:** Fast. The keyboard-driven feel registers before any visual detail does.

**Why it works**
| Principle | Concrete application |
|-----------|----------------------|
| Rams: As little design as possible | Single-column issue view; no decorative chrome; commands surfaced via Cmd+K, not nav menus |
| Norman: Behavioral level | Every action has a keyboard shortcut shown next to its label; muscle memory compounds with use |
| Nielsen: Recognition over recall | Cmd+K palette shows recent commands + fuzzy search; users never memorize paths |
| Fitts's Law | Frequently used controls (status, assignee, priority) live in a fixed sidebar — large targets, predictable position |
| Hick's Law | Issue creation form shows only title field by default; metadata expands progressively, not all at once |

**Key takeaway:** Speed is a design feature, not a performance one — it's produced by removing decisions, not by removing milliseconds.
**Study this closely:** The Cmd+K palette transitions and the inline issue-creation flow (press C anywhere).
```

## Categories at a Glance

| Category | Reference | Exemplars |
|----------|-----------|-----------|
| SaaS Dashboards | [saas-dashboards.md](references/saas-dashboards.md) | Stripe, Linear, Notion, Figma |
| E-commerce | [e-commerce.md](references/e-commerce.md) | Shopify, Apple Store, Glossier, Aesop |
| Content Platforms | [content-platforms.md](references/content-platforms.md) | Medium, Substack, NYT, Readwise |
| Mobile Apps | [mobile-apps.md](references/mobile-apps.md) | Apple native, Material apps, gesture UIs |
| Design Systems | [design-systems-in-practice.md](references/design-systems-in-practice.md) | Polaris, Carbon, Atlassian, Radix |
| Brand Experiences | [brand-experiences.md](references/brand-experiences.md) | Apple.com, Porsche, Aesop, Muji |
| Developer Tools | [developer-tools.md](references/developer-tools.md) | Raycast |
| Emotional Design as Growth | [emotional-design-growth.md](references/emotional-design-growth.md) | Duolingo, Phantom, Revolut |
| Psychological Design Engines | [psychological-design-engines.md](references/psychological-design-engines.md) | Perplexity, Apple Fitness, Waze, Headspace, Discord, Stompers |
| SaaS Conversion Psychology | [saas-conversion-psychology.md](references/saas-conversion-psychology.md) | Blinkist, Headspace, Moonly, Slopes, Mobbin, Busuu, Uber |
| Onboarding Psychology | [onboarding-psychology.md](references/onboarding-psychology.md) | Breathwork, Stompers, Sudoku, Speechify, Marathon |
| Tinder Dopamine Framework | [tinder-dopamine-design.md](references/tinder-dopamine-design.md) | Tinder ($0 → $2B) |
| Outcome-First AI Design | [outcome-first-ai-design.md](references/outcome-first-ai-design.md) | Dia, Intercom Finn |
| Peak-End Rule | [peak-end-rule-design.md](references/peak-end-rule-design.md) | Airbnb, Ahead, Uber |
| Apple's Four Principles | [apple-design-principles.md](references/apple-design-principles.md) | iOS / macOS |
| Spotify's Design Moat | [spotify-design-moat.md](references/spotify-design-moat.md) | Spotify |
| Netflix Behavioral Weapons | [netflix-behavioral-design.md](references/netflix-behavioral-design.md) | Netflix |
| Product-Led Growth Funnel | [product-led-growth-funnel.md](references/product-led-growth-funnel.md) | PLG patterns |

## Next Steps

- **[Design Philosophies](../design-philosophies/SKILL.md)**: theoretical foundations
- **[Visual Design](../visual-design/SKILL.md)**: apply aesthetic lessons
- **[Component Library](../component-library/SKILL.md)**: build components from observed patterns
- **[Design System Creation](../design-system-creation/SKILL.md)**: your own system using Polaris/Carbon/Radix lessons

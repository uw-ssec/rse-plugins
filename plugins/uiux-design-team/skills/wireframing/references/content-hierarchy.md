# Content Hierarchy

> Back to [Wireframing](../SKILL.md)

Content hierarchy determines the order in which users perceive and process information on a page. A clear hierarchy guides the eye from the most important element to the least, ensuring that users find what they need without conscious effort.

## The Hierarchy Pyramid

Every page has a single primary objective. Content hierarchy ensures that objective dominates visual attention.

```
┌─────────────────────┐
│   Primary Action     │  ← One thing you want users to do
├─────────────────────┤
│  Supporting Content  │  ← Context that enables the action
├─────────────────────┤
│  Secondary Info      │  ← Helpful but not essential
├─────────────────────┤
│  Tertiary Details    │  ← Available on demand
└─────────────────────┘
```

### Priority Levels

| Level | Purpose | Visual Treatment | Examples |
|-------|---------|-----------------|----------|
| **P1** | Primary action/message | Largest, highest contrast, most prominent position | Hero headline, primary CTA |
| **P2** | Supporting context | Medium size, strong but secondary contrast | Subheadline, key benefits |
| **P3** | Secondary information | Standard size, moderate contrast | Feature details, testimonials |
| **P4** | Tertiary details | Smaller size, lower contrast | Legal text, metadata, footnotes |

## Inverted Pyramid Structure

Borrowed from journalism, the inverted pyramid front-loads the most important information.

```
┌─────────────────────────────────────────┐
│         Most Important (Lead)            │
│   Who, What, When, Where, Why, How       │
├───────────────────────────────────┤
│      Important Details             │
│   Supporting facts, context        │
├─────────────────────────┤
│    Background Info       │
│   Nice to have           │
└─────────────────────┘
```

**Application to wireframes:**
- Hero section: answer the user's core question immediately
- Body content: provide supporting evidence and detail
- Footer area: supplementary information and navigation

## Progressive Disclosure

Reveal information progressively rather than presenting everything at once.

### Disclosure Patterns

**Accordion/Expand:**
```
[+] Shipping Information
    Standard: 5-7 business days ($4.99)
    Express: 2-3 business days ($12.99)
    Overnight: Next business day ($24.99)

[+] Return Policy
[+] Size Guide
```

**Tabs:**
```
[Overview] [Specifications] [Reviews] [FAQ]
─────────────────────────────────────────
Currently showing: Overview content
```

**Show More:**
```
Feature description paragraph one...
Feature description paragraph two...

[Show More ▼]  ← Reveals paragraphs 3-5
```

### When to Use Progressive Disclosure

- **Use when:** Information serves different user segments, content is long, or secondary details would overwhelm the primary message
- **Avoid when:** All information is equally critical, hiding content creates confusion, or users need to compare across sections

## F-Pattern Content Placement

For text-heavy pages, place content according to the F-pattern scanning behavior.

```
████████████████████████████████  ← First horizontal scan (headline)
████████████████████████████████

████████████████████           ← Second horizontal scan (subheading)
████████████████████

██████                          ← Vertical scan down left edge
██████
██████                          ← Periodic horizontal scans
██████████████
██████
██████
```

**Placement rules:**
1. Most important content in the first two lines
2. Start each new section with a strong keyword or heading
3. Use bullet points and bold text along the left edge
4. Front-load paragraphs with key information

## Z-Pattern Content Placement

For minimal pages with few elements (landing pages, sign-up forms).

```
[Logo]─────────────────[Navigation/CTA]
       ╲
        ╲
         ╲
          ╲
[Supporting Image]────[Primary CTA Button]
```

**Placement rules:**
1. Brand/logo top-left (start of Z)
2. Secondary CTA or navigation top-right
3. Supporting content in the diagonal center
4. Primary CTA bottom-right (end of Z, natural conclusion)

## Above the Fold

The visible area before scrolling. While users do scroll, above-the-fold content sets expectations and determines whether they continue.

### What Goes Above the Fold

- **Always:** Primary headline, primary CTA, core value proposition
- **Usually:** Supporting subheadline, hero image/illustration
- **Sometimes:** Social proof snippet, navigation
- **Never:** Terms and conditions, lengthy descriptions, secondary features

### Fold Considerations by Device

| Device | Approximate fold height | Priority content |
|--------|------------------------|------------------|
| Mobile (portrait) | ~600px | Headline + CTA only |
| Tablet (portrait) | ~900px | Headline + CTA + brief support |
| Desktop (1080p) | ~700px | Full hero with image and CTA |
| Desktop (1440p) | ~900px | Full hero with expanded content |

## Content Prioritization Matrix

Use this matrix to decide what to include and where to place it.

| | High User Need | Low User Need |
|---|---|---|
| **High Business Value** | P1 — Prominent, above fold | P2 — Visible, supporting |
| **Low Business Value** | P2 — Accessible, clear path | P3/P4 — Available on demand |

### Prioritization Process

1. **List all content elements** the page needs to communicate
2. **Score each element** on user need (1-5) and business value (1-5)
3. **Plot on the matrix** to determine priority level
4. **Assign visual treatment** based on priority level
5. **Test with users** to validate the hierarchy matches their mental model

## Heading Hierarchy

Headings create a scannable outline of the page's content structure.

```
H1: Page Title (one per page)
  H2: Major Section
    H3: Subsection
      H4: Detail group
    H3: Subsection
  H2: Major Section
    H3: Subsection
```

**Rules:**
- Never skip heading levels (no H1 → H3)
- Only one H1 per page
- Headings should make sense when read in sequence without body text
- Use headings for structure, not for visual styling

## Content Grouping Strategies

### Card Groups

Related items presented as scannable cards:

```
┌──────────┐  ┌──────────┐  ┌──────────┐
│ [Icon]   │  │ [Icon]   │  │ [Icon]   │
│ Title    │  │ Title    │  │ Title    │
│ Brief    │  │ Brief    │  │ Brief    │
│ desc...  │  │ desc...  │  │ desc...  │
│ [Action] │  │ [Action] │  │ [Action] │
└──────────┘  └──────────┘  └──────────┘
```

### Comparison Tables

When users need to evaluate options side by side:

```
             │ Basic  │ Pro    │ Enterprise
─────────────┼────────┼────────┼──────────
Feature A    │   ✓    │   ✓    │    ✓
Feature B    │   ─    │   ✓    │    ✓
Feature C    │   ─    │   ─    │    ✓
─────────────┼────────┼────────┼──────────
Price        │ $9/mo  │ $29/mo │  Custom
```

### Timeline/Process

Sequential content that tells a story:

```
Step 1          Step 2          Step 3
  ●───────────────●───────────────●
Sign Up       Configure       Launch
```

## Call-to-Action Placement

### Primary CTA

- **Position:** Within the first visible viewport and repeated at the logical decision point
- **Visual treatment:** Highest contrast, largest interactive element
- **Copy:** Action-oriented verb (Start, Get, Try, Create)

### Secondary CTA

- **Position:** Near the primary CTA or in the navigation
- **Visual treatment:** Visible but clearly subordinate (outline button, text link)
- **Copy:** Lower-commitment alternative (Learn More, See Demo, Compare Plans)

### CTA Repetition

On long pages, repeat the primary CTA:
1. Above the fold (initial exposure)
2. After key benefit sections (decision reinforcement)
3. At the page bottom (final opportunity)

## Wireframe Hierarchy Checklist

- [ ] Single clear P1 element on every page/screen
- [ ] Content follows appropriate scanning pattern (F or Z)
- [ ] Above-the-fold content answers "What is this? Why should I care?"
- [ ] Headings create a meaningful outline when read alone
- [ ] Progressive disclosure hides secondary content appropriately
- [ ] CTAs are placed at natural decision points
- [ ] Content grouping reflects logical relationships
- [ ] Visual weight decreases from P1 → P4 consistently

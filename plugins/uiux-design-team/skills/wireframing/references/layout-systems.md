# Layout Systems

> Back to [Wireframing](../SKILL.md)

Layout systems provide the structural foundation for wireframes. Choosing the right layout for a page type ensures content is organized predictably and users can navigate without friction.

## Common Page Layouts

### Single Column

The simplest layout. Content flows vertically in a single constrained column.

```
┌──────────────────────────────┐
│          Navigation           │
├──────────────────────────────┤
│                               │
│       Content Area            │
│       (max-width: 65ch)       │
│                               │
│       Paragraph text          │
│       flows within a          │
│       single centered         │
│       column                  │
│                               │
├──────────────────────────────┤
│          Footer               │
└──────────────────────────────┘
```

**Best for:** Blog posts, articles, long-form reading, terms/privacy pages, email templates, mobile layouts.

**Key dimensions:**
- Content width: 600-800px (45-75 characters per line)
- Side padding: 16-24px on mobile, auto margins on desktop

### Two Column: Content + Sidebar

```
┌──────────────────────────────────────┐
│             Navigation                │
├──────────────────────┬───────────────┤
│                      │               │
│   Main Content       │   Sidebar     │
│   (8 columns)        │   (4 columns) │
│                      │               │
│   Primary reading    │   Navigation  │
│   area with full     │   Filters     │
│   articles, forms,   │   Related     │
│   or data            │   content     │
│                      │               │
├──────────────────────┴───────────────┤
│             Footer                    │
└──────────────────────────────────────┘
```

**Best for:** Documentation, settings pages, email clients, dashboards with navigation, e-commerce category pages.

**Ratio options:**
- 8:4 (67%:33%) — Standard sidebar
- 9:3 (75%:25%) — Narrow sidebar
- 7:5 (58%:42%) — Wide sidebar for complex filters

### Two Column: Equal Split

```
┌──────────────────────────────────────┐
│             Navigation                │
├──────────────┬───────────────────────┤
│              │                       │
│   Left       │   Right               │
│   Panel      │   Panel               │
│   (6 col)    │   (6 col)             │
│              │                       │
│   List or    │   Detail or           │
│   navigation │   content             │
│              │                       │
├──────────────┴───────────────────────┤
│             Footer                    │
└──────────────────────────────────────┘
```

**Best for:** Comparison pages, sign-up/sign-in (form + marketing), master-detail views, split-screen tools.

### Three Column

```
┌────────────────────────────────────────────┐
│                Navigation                   │
├────────┬──────────────────────┬─────────────┤
│        │                      │             │
│  Nav   │   Main Content       │  Contextual │
│  (3)   │   (6 columns)        │  Info (3)   │
│        │                      │             │
│  Links │   Primary content    │  Related    │
│  Menu  │   area               │  Quick      │
│  Tree  │                      │  actions    │
│        │                      │             │
├────────┴──────────────────────┴─────────────┤
│                Footer                        │
└────────────────────────────────────────────┘
```

**Best for:** Complex web applications, email clients (folders/list/preview), enterprise dashboards, documentation with table of contents.

### Dashboard Grid

```
┌──────────────────────────────────────────┐
│  Navigation Bar                           │
├──────┬───────────────────────────────────┤
│      │  ┌──────┐  ┌──────┐  ┌──────┐    │
│ Side │  │ KPI  │  │ KPI  │  │ KPI  │    │
│ Nav  │  │ Card │  │ Card │  │ Card │    │
│      │  └──────┘  └──────┘  └──────┘    │
│      │  ┌──────────────┐  ┌──────────┐  │
│      │  │              │  │          │  │
│      │  │  Chart Area  │  │  Table   │  │
│      │  │  (8 columns) │  │  (4 col) │  │
│      │  │              │  │          │  │
│      │  └──────────────┘  └──────────┘  │
│      │  ┌──────────────────────────────┐│
│      │  │  Full-width data table       ││
│      │  └──────────────────────────────┘│
├──────┴───────────────────────────────────┤
└──────────────────────────────────────────┘
```

**Best for:** Analytics dashboards, admin panels, monitoring tools, project management interfaces.

### Card Grid

```
┌──────────────────────────────────────┐
│          Navigation                   │
├──────────────────────────────────────┤
│  [Filters]  [Sort]  [View Toggle]    │
├──────────────────────────────────────┤
│  ┌────────┐  ┌────────┐  ┌────────┐ │
│  │ Card 1 │  │ Card 2 │  │ Card 3 │ │
│  │        │  │        │  │        │ │
│  └────────┘  └────────┘  └────────┘ │
│  ┌────────┐  ┌────────┐  ┌────────┐ │
│  │ Card 4 │  │ Card 5 │  │ Card 6 │ │
│  │        │  │        │  │        │ │
│  └────────┘  └────────┘  └────────┘ │
│          [Load More]                  │
├──────────────────────────────────────┤
│          Footer                       │
└──────────────────────────────────────┘
```

**Best for:** Product listings, portfolios, galleries, team directories, blog archives, app stores.

## Responsive Layout Transformations

### Sidebar Collapse

```
Desktop (>1024px)          Tablet (768-1024px)       Mobile (<768px)
┌──────┬─────────┐        ┌──┬──────────────┐       ┌──────────────┐
│ Side │ Content │        │☰ │ Content      │       │ ☰  Content   │
│ bar  │         │   →    │  │              │   →   │              │
│      │         │        │  │              │       │              │
└──────┴─────────┘        └──┴──────────────┘       └──────────────┘
 Visible sidebar           Collapsed sidebar         Hamburger menu
```

### Grid Reflow

```
Desktop (4 col)        Tablet (2 col)        Mobile (1 col)
┌──┐ ┌──┐ ┌──┐ ┌──┐   ┌──────┐ ┌──────┐   ┌────────────┐
│  │ │  │ │  │ │  │   │      │ │      │   │            │
└──┘ └──┘ └──┘ └──┘   └──────┘ └──────┘   └────────────┘
                       ┌──────┐ ┌──────┐   ┌────────────┐
                 →     │      │ │      │ → │            │
                       └──────┘ └──────┘   └────────────┘
                                           ┌────────────┐
                                           │            │
                                           └────────────┘
```

### Stack Reorder

Content priority may change on mobile. Use CSS `order` or restructure for mobile-first hierarchy.

```
Desktop                      Mobile
┌──────────┬────────────┐    ┌──────────────┐
│ Sidebar  │ Hero Image │    │ Hero Image   │  ← Image first on mobile
│ Nav      │            │    ├──────────────┤
│          ├────────────┤    │ Key Content  │  ← Content second
│          │ Content    │    ├──────────────┤
│          │            │    │ Sidebar Nav  │  ← Nav last
└──────────┴────────────┘    └──────────────┘
```

## Content Area Proportions

### Golden Ratio (1:1.618)

```
┌──────────────────────┬─────────────────────────────────────┐
│   Sidebar (38.2%)    │        Main Content (61.8%)          │
│                      │                                      │
└──────────────────────┴─────────────────────────────────────┘
```

### Rule of Thirds

Divide the page into thirds for natural balance:

```
┌────────────┬────────────┬────────────┐
│   1/3      │    1/3     │    1/3     │
│            │            │            │
│   Place    │   Place    │   Place    │
│   key      │   primary  │   secondary│
│   nav      │   content  │   info     │
└────────────┴────────────┴────────────┘
```

## Layout by Page Type

| Page Type | Recommended Layout | Key Considerations |
|-----------|-------------------|-------------------|
| Landing page | Single column, Z-pattern | Focus on single CTA, minimal distraction |
| Article/Blog | Single column with optional sidebar | 65ch max reading width |
| Product page | Two column (image + details) | Sticky add-to-cart on mobile |
| Category/List | Card grid with filters | Responsive column count |
| Dashboard | Sidebar + modular grid | Collapsible nav, dense information |
| Settings | Two column (nav + forms) | Grouped sections, save indicators |
| Search results | Single or two column | Filters sidebar or top bar |
| Checkout | Single column, progressive | Minimize distraction, clear progress |
| Documentation | Three column (nav + content + TOC) | Sticky navigation elements |
| Auth (login/signup) | Centered single column or split | Focus on form, minimal navigation |

## Grid Overlays for Wireframes

### 12-Column Grid Overlay

Apply a 12-column grid to wireframes for consistent alignment:

```
│ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │10 │11 │12 │
├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
│   Sidebar (3)  │        Content (9)              │
├───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┤
```

### Common Column Spans

| Element | Columns | Percentage |
|---------|---------|------------|
| Full width | 12/12 | 100% |
| Wide content | 10/12 | 83.3% |
| Standard content | 8/12 | 66.7% |
| Half width | 6/12 | 50% |
| Third width | 4/12 | 33.3% |
| Quarter width | 3/12 | 25% |
| Narrow sidebar | 3/12 | 25% |
| Standard sidebar | 4/12 | 33.3% |

## Layout Sketching Techniques

### Thumbnail Sketches

Quick, small sketches to explore layout options rapidly:

1. Draw 6-8 small rectangles (business card size)
2. Sketch a different layout approach in each
3. Spend no more than 30 seconds per sketch
4. Circle the 2-3 most promising options
5. Develop those into full wireframes

### Block Diagrams

Before detailing content, establish the spatial structure with labeled blocks:

```
┌─────────────────────────────────┐
│           [HEADER]               │
├─────────────────────────────────┤
│           [HERO]                 │
│                                  │
├────────────┬────────────────────┤
│ [FEATURES] │ [FEATURES]         │
├────────────┴────────────────────┤
│        [TESTIMONIALS]            │
├─────────────────────────────────┤
│           [CTA]                  │
├─────────────────────────────────┤
│          [FOOTER]                │
└─────────────────────────────────┘
```

### Annotation Conventions

- **Solid lines:** Fixed boundaries
- **Dashed lines:** Flexible/responsive boundaries
- **Arrows:** Scroll direction or content flow
- **Numbers in circles:** Interactive sequence order
- **Shaded areas:** Image/media placeholders
- **Wavy lines:** Text placeholders

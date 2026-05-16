# Wireframe Patterns

> Back to [Wireframing](../SKILL.md)

Wireframe patterns are reusable structural solutions for common UI components and page sections. Using established patterns accelerates the wireframing process and ensures consistency across screens.

## Header & Navigation Patterns

### Top Navigation Bar

```
┌─────────────────────────────────────────────────────┐
│ [Logo]   Home  Products  About  Blog    [Search] [☰]│
└─────────────────────────────────────────────────────┘
```

**Variants:**
- **Sticky header:** Remains visible on scroll, often reduced in height
- **Transparent header:** Overlays hero content, transitions to solid on scroll
- **Centered logo:** Logo centered with nav links split on either side

### Mega Menu

```
┌─────────────────────────────────────────────────────┐
│ [Logo]  [Products ▼]  Solutions  Pricing  Resources │
├─────────────────────────────────────────────────────┤
│ Products                                             │
│ ┌───────────┐ ┌───────────┐ ┌───────────┐          │
│ │ Category 1│ │ Category 2│ │ Category 3│          │
│ │ • Item A  │ │ • Item D  │ │ • Item G  │          │
│ │ • Item B  │ │ • Item E  │ │ • Item H  │          │
│ │ • Item C  │ │ • Item F  │ │ • Item I  │          │
│ └───────────┘ └───────────┘ └───────────┘          │
│                          [View All Products →]       │
└─────────────────────────────────────────────────────┘
```

### Sidebar Navigation

```
┌──────────────┐
│ [Logo]       │
├──────────────┤
│ ● Dashboard  │
│ ○ Projects   │
│ ○ Team       │
│ ○ Messages   │
│ ○ Settings   │
├──────────────┤
│ WORKSPACE    │
│ ○ Project A  │
│ ○ Project B  │
├──────────────┤
│              │
│ [User Avatar]│
│ [Logout]     │
└──────────────┘
```

### Tab Navigation

```
┌─────────┬─────────┬─────────┬─────────┐
│ General │ Profile │ Billing │ Security│
├─────────┘         └─────────┴─────────┤
│                                        │
│  Profile settings content area         │
│                                        │
└────────────────────────────────────────┘
```

## Hero Section Patterns

### Centered Hero

```
┌──────────────────────────────────────────┐
│                                          │
│           [Overline Text]                │
│                                          │
│      Large Compelling Headline           │
│      That Captures Attention             │
│                                          │
│      Supporting paragraph that            │
│      explains the value proposition       │
│                                          │
│      [Primary CTA]  [Secondary CTA]     │
│                                          │
└──────────────────────────────────────────┘
```

### Split Hero (Text + Image)

```
┌──────────────────────────────────────────┐
│                                          │
│  Headline That          ┌─────────────┐  │
│  Grabs Attention        │             │  │
│                         │   Hero      │  │
│  Supporting text        │   Image     │  │
│  with context           │             │  │
│                         │             │  │
│  [Primary CTA]          └─────────────┘  │
│                                          │
└──────────────────────────────────────────┘
```

### Video/Background Hero

```
┌──────────────────────────────────────────┐
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│ ░░░░░░░░░░░ Background ░░░░░░░░░░░░░░░░ │
│ ░░░░░░░░░ Video / Image ░░░░░░░░░░░░░░░ │
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│ ░░░░░░  [Overlay: Headline]  ░░░░░░░░░░ │
│ ░░░░░░░░░ [Primary CTA] ░░░░░░░░░░░░░░ │
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
└──────────────────────────────────────────┘
```

## Card Patterns

### Standard Card

```
┌────────────────────┐
│ ┌────────────────┐ │
│ │    Image        │ │
│ │                 │ │
│ └────────────────┘ │
│ Category           │
│ Card Title         │
│ Description text   │
│ that wraps to      │
│ multiple lines...  │
│                    │
│ [Action]  [Action] │
└────────────────────┘
```

### Horizontal Card

```
┌──────────────────────────────────┐
│ ┌──────────┐  Title              │
│ │  Image   │  Description text   │
│ │          │  that provides      │
│ │          │  context...         │
│ └──────────┘  [Action]           │
└──────────────────────────────────┘
```

### Stats Card

```
┌────────────────────┐
│ ↑ 12.5%            │
│                    │
│ 24,531             │
│ Active Users       │
│                    │
│ ▁▂▃▄▅▆▇█▇▆▅▄▃▂▁  │
└────────────────────┘
```

### Profile Card

```
┌────────────────────┐
│      [Avatar]       │
│    Jane Doe         │
│    Product Designer │
│    San Francisco    │
│                     │
│  [Message] [Follow] │
└────────────────────┘
```

## Form Patterns

### Stacked Form

```
┌────────────────────────────┐
│ Create Account              │
│                             │
│ Full Name                   │
│ ┌─────────────────────────┐ │
│ │                         │ │
│ └─────────────────────────┘ │
│                             │
│ Email Address               │
│ ┌─────────────────────────┐ │
│ │                         │ │
│ └─────────────────────────┘ │
│                             │
│ Password                    │
│ ┌─────────────────────────┐ │
│ │                     [👁]│ │
│ └─────────────────────────┘ │
│ Must be at least 8 chars    │
│                             │
│ [Create Account]            │
│                             │
│ Already have an account?    │
│ [Sign in]                   │
└────────────────────────────┘
```

### Inline Form

```
┌──────────────────────────────────────────┐
│ Subscribe to our newsletter               │
│                                           │
│ ┌──────────────────────────┐ ┌──────────┐│
│ │ Enter your email         │ │Subscribe ││
│ └──────────────────────────┘ └──────────┘│
└──────────────────────────────────────────┘
```

### Multi-Step Form

```
  Step 1         Step 2         Step 3
  ●──────────────○──────────────○
  Personal       Payment        Confirm

┌────────────────────────────────────┐
│ Personal Information                │
│                                     │
│ First Name        Last Name         │
│ ┌──────────────┐ ┌──────────────┐  │
│ │              │ │              │  │
│ └──────────────┘ └──────────────┘  │
│                                     │
│ Email Address                       │
│ ┌────────────────────────────────┐ │
│ │                                │ │
│ └────────────────────────────────┘ │
│                                     │
│              [Back]  [Continue →]   │
└────────────────────────────────────┘
```

## List Patterns

### Simple List

```
┌──────────────────────────────────┐
│ ┌──┐ Item Title                  │
│ │  │ Secondary text              │
│ └──┘                         [>] │
├──────────────────────────────────┤
│ ┌──┐ Item Title                  │
│ │  │ Secondary text              │
│ └──┘                         [>] │
├──────────────────────────────────┤
│ ┌──┐ Item Title                  │
│ │  │ Secondary text              │
│ └──┘                         [>] │
└──────────────────────────────────┘
```

### Data Table

```
┌──────────────────────────────────────────────┐
│ □  Name ▼        Role         Status   Actions│
├──────────────────────────────────────────────┤
│ □  Jane Doe      Designer     Active    ⋯    │
│ □  John Smith    Developer    Active    ⋯    │
│ □  Alex Chen     PM           Away      ⋯    │
├──────────────────────────────────────────────┤
│ Showing 1-3 of 24            [<] 1 2 3 [>]  │
└──────────────────────────────────────────────┘
```

## Modal & Dialog Patterns

### Confirmation Dialog

```
        ┌────────────────────────────┐
        │ Delete Project?             │
        │                             │
        │ Are you sure you want to    │
        │ delete "Project Alpha"?     │
        │ This action cannot be       │
        │ undone.                      │
        │                             │
        │       [Cancel] [Delete]     │
        └────────────────────────────┘
```

### Full Modal

```
    ┌──────────────────────────────────────┐
    │ Create New Project                [×]│
    ├──────────────────────────────────────┤
    │                                      │
    │ Project Name                         │
    │ ┌──────────────────────────────────┐ │
    │ │                                  │ │
    │ └──────────────────────────────────┘ │
    │                                      │
    │ Description                          │
    │ ┌──────────────────────────────────┐ │
    │ │                                  │ │
    │ │                                  │ │
    │ └──────────────────────────────────┘ │
    │                                      │
    │ Team Members                         │
    │ [+ Add Members]                      │
    │                                      │
    ├──────────────────────────────────────┤
    │               [Cancel]  [Create]     │
    └──────────────────────────────────────┘
```

## Sidebar Patterns

### Filters Sidebar

```
┌──────────────────┐
│ Filters     [Clear]│
├──────────────────┤
│ Category         │
│ □ Electronics    │
│ □ Clothing       │
│ ■ Books          │
│ □ Home           │
├──────────────────┤
│ Price Range      │
│ $[10] — $[500]   │
│ ○────●───────○   │
├──────────────────┤
│ Rating           │
│ ★★★★★ & up (12) │
│ ★★★★☆ & up (34) │
│ ★★★☆☆ & up (67) │
├──────────────────┤
│ [Apply Filters]  │
└──────────────────┘
```

## Footer Patterns

### Multi-Column Footer

```
┌─────────────────────────────────────────────────┐
│                                                  │
│  [Logo]          Product     Company    Support  │
│  Brief           Features   About      Help     │
│  description     Pricing    Blog       Contact  │
│  of the          Docs       Careers    Status   │
│  product         Updates    Press      API      │
│                                                  │
├─────────────────────────────────────────────────┤
│  © 2024 Company   [Twitter] [GitHub] [LinkedIn] │
│  Privacy · Terms                                 │
└─────────────────────────────────────────────────┘
```

## Mobile Wireframe Patterns

### Bottom Navigation

```
┌──────────────┐
│              │
│   Content    │
│   Area       │
│              │
│              │
│              │
├──────────────┤
│ 🏠  🔍  ➕  💬  👤│
│Home Search Add Chat Me│
└──────────────┘
```

### Pull-to-Refresh

```
┌──────────────┐
│    ↓ Pull     │
│   to refresh  │
├──────────────┤
│ List Item 1  │
│ List Item 2  │
│ List Item 3  │
│ List Item 4  │
│ List Item 5  │
│              │
└──────────────┘
```

### Bottom Sheet

```
┌──────────────┐
│  (dimmed      │
│   background  │
│   content)    │
├──────────────┤
│ ═══ (handle)  │
│               │
│ Sheet Title   │
│               │
│ Option 1      │
│ Option 2      │
│ Option 3      │
│               │
│ [Cancel]      │
└──────────────┘
```

## Annotation Conventions

When annotating wireframes for handoff, use consistent markers:

| Symbol | Meaning | Example |
|--------|---------|---------|
| `→` | Links to / navigates to | `→ /product/detail` |
| `[H]` | Hover state exists | `[H] Shows tooltip` |
| `[C]` | Click/tap interaction | `[C] Opens modal` |
| `[S]` | Scroll behavior | `[S] Sticky on scroll` |
| `*` | Required field | `* Email Address` |
| `#` | Dynamic content | `# User name from API` |
| `~` | Placeholder text | `~ Lorem ipsum` |
| `(i)` | Information note | `(i) Max 3 items shown` |

### State Annotations

Document all relevant states for each interactive element:

```
Button States:
  [Default]  →  [Hover]  →  [Active/Pressed]
  [Disabled]
  [Loading...]

Input States:
  [Empty]  →  [Focused]  →  [Filled]
  [Error: "Invalid email"]
  [Success ✓]
  [Disabled]
```

## Wireframe Fidelity Levels

| Level | Detail | Tools | Use When |
|-------|--------|-------|----------|
| **Sketch** | Hand-drawn, rough boxes | Pen + paper, whiteboard | Ideation, brainstorming |
| **Lo-fi** | Clean boxes, labels, no style | Balsamiq, Excalidraw | Early concepts, stakeholder alignment |
| **Mid-fi** | Real content, basic hierarchy | Figma, Sketch wireframe kit | User testing, developer preview |
| **Hi-fi** | Visual design applied | Figma, production CSS | Final approval, development handoff |

### Lo-fi Wireframe Checklist

- [ ] All page sections identified with labeled blocks
- [ ] Content hierarchy established (P1 through P4)
- [ ] Navigation structure defined
- [ ] Interactive elements identified (buttons, links, forms)
- [ ] Responsive behavior annotated
- [ ] Key states documented (empty, loading, error, populated)
- [ ] Scroll behavior noted
- [ ] Linked to user flow or sitemap

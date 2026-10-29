---
name: frontend-design
description: Creates a complete frontend design from a description with bold aesthetic direction, design tokens, and production-grade code
user-invocable: true
allowed-tools: []
---

# Frontend Design

The flagship design command. Takes a description and produces a complete frontend design with bold aesthetic choices, design tokens, and production-grade code. No generic output. No safe defaults. Every design decision is intentional. This command routes through **@ux-design-lead** who orchestrates the full team.

## Philosophy

Every interface has a personality. This command rejects the bland, homogeneous "AI-designed" aesthetic. Instead, it makes deliberate, opinionated choices that serve the content, the audience, and the brand. The output should look like a human designer with taste made it -- because the system is guided by real design principles, not template interpolation.

## Workflow

### Step 1: Gather Requirements

Interview the user to understand what needs to be built.

**Prompt the user:**

> Describe what you want to build. I need to understand:
>
> 1. **What is it?** (landing page, dashboard, form, portfolio, app screen, etc.)
> 2. **Who is it for?** (target audience, their technical comfort, their expectations)
> 3. **What should it accomplish?** (primary goal: convert, inform, entertain, manage)
> 4. **What's the brand personality?** (serious, playful, premium, grassroots, technical)
> 5. **Any existing constraints?** (brand colors, existing design system, framework preference)
> 6. **Reference or inspiration?** (sites, apps, or styles you admire)

If the user provides a brief description without answering all questions, infer reasonable answers but call out assumptions explicitly.

### Step 2: Establish Aesthetic Direction

This is the defining step. Choose an aesthetic direction that serves the requirements -- not a safe middle ground.

**Aesthetic Direction Library:**

Select one primary direction and optionally one accent direction. Reference the visual-design skill's full aesthetic direction library for deeper guidance on each.

| Direction | Character | Typical Signals | Best For |
|-----------|-----------|-----------------|----------|
| **Swiss Precision** | Clean, grid-rigid, typographic mastery | Monospace accents, strict alignment, generous whitespace | SaaS dashboards, dev tools, documentation |
| **Editorial Luxury** | Magazine-quality, dramatic type, curated feel | Serif headlines, high contrast, asymmetric layouts | Content platforms, portfolios, brand sites |
| **Brutalist Honesty** | Raw, intentionally unpolished, bold | System fonts, harsh borders, visible structure | Creative agencies, experimental, counter-culture |
| **Soft Modernism** | Warm, approachable, rounded | Rounded corners, pastel-adjacent palette, generous padding | Consumer apps, wellness, education |
| **Dark Sophisticate** | Premium, moody, immersive | Dark backgrounds, accent lighting, subtle gradients | Media, entertainment, luxury products |
| **Neo-Geometric** | Mathematical, pattern-driven, precise | Geometric shapes, modular grids, systematic color | Fintech, analytics, data products |
| **Organic Flow** | Natural, dynamic, breathing | Fluid shapes, natural color palette, flowing layouts | Environmental, food, lifestyle brands |
| **Retro Terminal** | Nostalgic, hacker aesthetic, glowing | Monospace everything, green/amber on dark, scanlines | Developer tools, CLI wrappers, tech-forward |
| **Maximalist Pop** | Loud, layered, unapologetic | Clashing colors done right, mixed media, gradient overload | Youth brands, creative tools, entertainment |
| **Minimal Japandi** | Restrained, intentional, meditative | Asymmetric balance, muted earth tones, vast whitespace | Premium minimalism, ceramics, architecture |
| **Industrial Utility** | Functional, no-nonsense, tool-like | Monochrome, dense information, utilitarian typography | Admin panels, internal tools, B2B platforms |
| **Glassmorphism Plus** | Layered depth, translucent, modern | Blurred backgrounds, glass panels, subtle shadows | Modern landing pages, iOS-style interfaces |
| **Neubrutalism** | Bold blocks, thick borders, playful rebellion | High contrast, offset shadows, chunky elements | Startup sites, personal brands, indie products |
| **Data Ink** | Information-dense, Tufte-inspired | Small multiples, sparklines, minimal chrome | Analytics dashboards, reporting, research tools |
| **Kinetic Narrative** | Motion-driven, story-telling, immersive | Scroll-driven animation, parallax, cinematic | Product launches, case studies, interactive stories |

**Present the recommendation:**

> Based on your requirements, I recommend **[Direction]** because [specific reasoning tied to their audience, goal, and content]. This will give the interface [specific quality] which serves your users' need to [specific user need].
>
> As an accent, I'll weave in elements of **[Secondary Direction]** to [specific purpose].

### Step 3: Define Color Palette

Build a purposeful color palette. No generic blue-and-gray.

**Palette structure:**

```css
:root {
  /* Semantic Background */
  --bg-primary:   /* Main surface */;
  --bg-secondary: /* Card/elevated surface */;
  --bg-tertiary:  /* Subtle/recessed surface */;
  --bg-inverse:   /* Flipped contrast surface */;

  /* Semantic Foreground */
  --fg-primary:   /* Main text */;
  --fg-secondary: /* Supporting text */;
  --fg-tertiary:  /* Muted/placeholder text */;
  --fg-inverse:   /* Text on inverse background */;

  /* Accent Colors */
  --accent-primary:    /* Primary brand action */;
  --accent-secondary:  /* Secondary brand color */;
  --accent-highlight:  /* Attention/emphasis */;

  /* Semantic Feedback */
  --feedback-success: ;
  --feedback-warning: ;
  --feedback-error:   ;
  --feedback-info:    ;

  /* Surface & Border */
  --border-primary:   ;
  --border-secondary: ;
  --shadow-sm: ;
  --shadow-md: ;
  --shadow-lg: ;
}
```

**Color selection rules:**
- Primary accent must have minimum 4.5:1 contrast ratio against its expected background
- Every color must earn its place -- if it doesn't serve a function, remove it
- Palette should have one "surprise" color -- the unexpected choice that gives the design character
- Test the palette in context, not in isolation

### Step 4: Set Typography

Select typefaces and build a scale that reinforces the aesthetic direction.

**Font selection guidance by direction:**

| Direction | Heading Recommendation | Body Recommendation |
|-----------|----------------------|---------------------|
| Swiss Precision | Tight grotesque (Helvetica Neue, Inter, Suisse) | Same family, lighter weight |
| Editorial Luxury | High-contrast serif (Playfair, Cormorant, Freight) | Readable serif or clean sans |
| Brutalist Honesty | System font stack or monospace | System font stack |
| Soft Modernism | Rounded sans (Nunito, Varela Round, Poppins) | Same family, regular weight |
| Dark Sophisticate | Thin/light sans or didone serif | Light-weight humanist sans |
| Neo-Geometric | Geometric sans (Geist, DM Sans, Outfit) | Same family or complementary geometric |
| Organic Flow | Humanist sans (Source Sans, Lato) or soft serif | Same family at regular weight |
| Retro Terminal | Monospace (JetBrains Mono, Berkeley Mono, Fira Code) | Same monospace at lighter weight |
| Maximalist Pop | Display/decorative (Clash Display, Cabinet Grotesk) | Contrasting clean sans |
| Minimal Japandi | Thin geometric (Satoshi, General Sans) | Same family at regular weight |
| Industrial Utility | Condensed sans (Barlow Condensed, Oswald) | Standard-width sans for body |
| Glassmorphism Plus | Light-weight sans (SF Pro, Inter) | Same family |
| Neubrutalism | Bold sans or slab serif (Space Grotesk, Archivo Black) | Clean sans for body |
| Data Ink | Tabular-friendly sans (IBM Plex Sans, Source Sans) | Same family |
| Kinetic Narrative | Variable-weight display font | Clean readable sans |

Generate a full type scale using the `create-type-scale` command or produce inline:

```css
:root {
  --font-heading: 'Font Name', [fallback stack];
  --font-body:    'Font Name', [fallback stack];
  --font-mono:    'Font Name', ui-monospace, monospace;

  /* Apply type scale tokens here */
}
```

### Step 5: Design Layout

Design the layout structure using CSS Grid and/or Flexbox.

**Layout deliverables:**
- Grid system definition (columns, gutters, margins per breakpoint)
- Component placement on the grid
- Responsive reflow behavior (what stacks, what hides, what resizes)
- Spacing rhythm using the project's spacing tokens

**Layout must include:**
- Mobile layout (320-767px)
- Tablet layout (768-1023px)
- Desktop layout (1024px+)
- Optional: wide layout (1440px+)

### Step 6: Implement with Production-Grade Code

Write real, shippable code. Not a prototype. Not a wireframe in HTML.

**Code quality requirements:**
- Semantic HTML5 (proper heading hierarchy, landmark regions, form labels)
- CSS custom properties for all design tokens
- Responsive without media query soup (prefer fluid techniques: clamp(), auto-fit, min())
- Accessible by default (ARIA where needed, focus management, skip links)
- Performance-conscious (no layout thrashing, will-change used sparingly, efficient selectors)

**Output format:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Project Title]</title>
  <style>
    /* === Design Tokens === */
    :root { ... }

    /* === Reset & Base === */
    *, *::before, *::after { box-sizing: border-box; }
    ...

    /* === Typography === */
    ...

    /* === Layout === */
    ...

    /* === Components === */
    ...

    /* === Utilities === */
    ...

    /* === Responsive === */
    @media (min-width: 768px) { ... }
    @media (min-width: 1024px) { ... }
  </style>
</head>
<body>
  <!-- Semantic, well-structured markup -->
</body>
</html>
```

If the user specifies a framework (Svelte, React, Vue), output in that framework's idiom instead.

## Delegation

1. **@ux-design-lead** receives the design brief, conducts the requirements interview, selects the aesthetic direction, and orchestrates the team.
2. The lead delegates to design specialists as needed:
   - **@visual-designer** for color, typography, and visual treatment
   - **@interaction-designer** for layout, component behavior, and responsive strategy
   - **@accessibility-specialist** for WCAG compliance and inclusive design
3. The lead PROACTIVELY engages the **frontend-engineering-team** for implementation:
   - **@frontend-lead** for overall implementation coordination and feasibility
   - **@react-specialist** for component architecture and rendering strategy
   - **@build-tooling-specialist** for Tailwind configuration and design token consumption
   - **@performance-engineer** for performance validation of the design (bundle impact, CWV compliance)
   - **@typescript-architect** for type-safe component interfaces
   - **@testing-engineer** for accessibility and visual regression test planning

## Design Principles for This Command

1. **No safe defaults.** Every color, font, and spacing value is a deliberate choice.
2. **Aesthetic coherence over feature completeness.** A beautiful half-page beats an ugly full page.
3. **The design should have a point of view.** If it could belong to any brand, it belongs to no brand.
4. **Code is the final design deliverable.** Not a mockup, not a description -- working code.
5. **Accessibility is non-negotiable.** Bold design and inclusive design are not in tension.

## Cross-Plugin Bridge (PROACTIVE)

This command produces production-grade code. PROACTIVELY engage the **frontend-engineering-team** throughout:

- **During token definition (Step 3-4):** Route to **@build-tooling-specialist** to validate that CSS custom properties and token architecture align with the engineering stack.
- **During layout design (Step 5):** Route to **@react-specialist** for component architecture feasibility and **@performance-engineer** for responsive rendering performance validation.
- **During code implementation (Step 6):** Route to **@react-specialist** for React/Next.js idiom compliance, **@typescript-architect** for type-safe implementations if framework output is requested, and **@testing-engineer** for test strategy.
- **After delivery:** Route to the frontend-engineering-team's `/code-review` for engineering quality assessment of the produced code.

## Quality Gates

Before delivering the design, verify:

- [ ] The aesthetic direction is identifiable and intentional (not "generic modern")
- [ ] Color palette has sufficient contrast ratios (WCAG AA minimum)
- [ ] Typography has clear hierarchy (squint test: can you tell H1 from H2 from body?)
- [ ] Layout works at 320px, 768px, and 1024px+
- [ ] All interactive elements are keyboard accessible
- [ ] Code is valid HTML and CSS (no syntax errors)
- [ ] Design tokens are extracted into custom properties (no hardcoded values in component styles)
- [ ] The design serves the stated user goal, not just looks good
- [ ] There is at least one bold design choice that differentiates this from a template

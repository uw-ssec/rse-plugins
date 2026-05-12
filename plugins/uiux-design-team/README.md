# UI/UX Design Team Plugin

A full design organization inside Claude Code. Ten specialist agents, 22 skills, 10 guided commands, and 91 reference documents that cover the entire design lifecycle -- from user research interviews through production-grade frontend code. Every agent has a defined role, every skill has progressive-disclosure reference material, and the lead agent routes work to the right specialist based on the problem at hand.

This is not a collection of prompts. It is a structured knowledge system that gives Claude deep, specific expertise in UI/UX design by encoding the frameworks, principles, and case studies that professional designers spend years learning.

## Why This Exists

Claude's built-in `frontend-design` capability is a single 42-line skill focused on visual aesthetics. It produces good-looking interfaces but has no depth behind the choices it makes -- no research methodology, no accessibility framework, no design system architecture, no understanding of why Stripe's dashboard works or why Netflix's Skip Intro button generates 136 million daily presses.

This plugin fills that gap across three dimensions:

**Process over output.** Professional design is not "make it look good." It is a lifecycle: research users, define the problem, architect the information, design the interactions, establish the visual language, build the system, test for accessibility, hand off to development, and evaluate what shipped. This plugin covers every phase with dedicated specialist agents and structured workflows.

**Team over individual.** A single designer cannot be expert in user research, information architecture, visual design, motion design, accessibility compliance, UX writing, design systems engineering, and frontend implementation simultaneously. This plugin models a professional design team where each role has deep, specialized knowledge. The UX Design Lead coordinates the team, routes questions to the right specialist, and synthesizes multi-perspective reviews.

**Knowledge over instinct.** The plugin encodes 91 reference documents covering established frameworks (Nielsen's 10 heuristics, Don Norman's emotional design, Gestalt principles, WCAG 2.2, Atomic Design, Jobs-to-Be-Done) alongside 18 behavioral psychology case studies analyzing real products (Netflix, Spotify, Apple, Tinder, Airbnb, Duolingo, Stripe, Linear, Notion). When Claude recommends a design decision, it can ground that recommendation in specific principles and real-world precedent.

Claude's proven aesthetic guidance is incorporated verbatim into the `visual-design` skill and augmented with systematic methodology for visual hierarchy, brand alignment, and emotional design.

## What Is In This Plugin

### 10 Specialist Agents

The plugin models a professional design team. Each agent has a defined personality, specific expertise areas, use-case triggers, and access to relevant skills and references.

| Agent | Role | What They Do |
|-------|------|-------------|
| **ux-design-lead** | Coordinator | Understands the design challenge, asks clarifying questions, routes to the right specialist or combination of specialists. Facilitates design thinking (Stanford d.school), conducts structured critiques, and orchestrates multi-specialist design reviews. The 797-line agent definition includes routing logic for every specialist, 20 example interaction scripts, design thinking phase facilitation, and review orchestration protocols. |
| **ux-researcher** | User Research | Conducts user interviews, builds personas with the Jobs-to-Be-Done framework, runs competitive audits, designs surveys, performs affinity mapping, and synthesizes research into actionable design insights. |
| **information-architect** | Information Architecture | Designs sitemaps, navigation patterns, taxonomy systems, card sorting exercises, content hierarchy, labeling systems, and wayfinding strategies. |
| **interaction-designer** | Interaction Design | Creates user flows, wireframes, prototypes, and defines interaction states (loading, empty, error, success, partial). Designs micro-interactions, form behavior, multi-step processes, and responsive interaction patterns. |
| **visual-designer** | Visual / UI Design | Establishes aesthetic direction from 15 defined styles (Swiss Precision, Editorial Luxury, Brutalist Honesty, Soft Modernism, Dark Sophisticate, etc.). Designs typography systems, color palettes, visual hierarchy, brand-aligned interfaces, and iconography. Incorporates Claude's `frontend-design` aesthetic guidance. |
| **motion-designer** | Motion Design | Applies Disney's 12 principles adapted for UI. Designs transitions, scroll-based effects, micro-interactions, loading animations, and page transition choreography. Ensures animations respect `prefers-reduced-motion` and stay within performance budgets. |
| **design-systems-engineer** | Design Systems | Architects token systems (global, alias, component tiers), component APIs, Atomic Design methodology, theming strategies, multi-brand support, dark mode implementation, governance models, and versioning. |
| **accessibility-specialist** | Accessibility | Audits for WCAG 2.2 AA/AAA compliance across all four principles (perceivable, operable, understandable, robust). Deep knowledge of ARIA patterns, keyboard navigation, screen reader testing (VoiceOver, NVDA, JAWS), cognitive accessibility, and Microsoft's inclusive design framework. |
| **ux-writer** | UX Writing | Writes microcopy, error messages, CTAs, onboarding flows, empty state messaging, and voice/tone documentation. Ensures interface copy is clear, concise, actionable, inclusive, and localization-ready. |
| **design-ops** | Design Operations | Optimizes design team workflows, builds handoff processes, establishes design QA checklists, manages asset pipelines, and structures design review cadences. |

### 22 Skills

Skills are the knowledge layer. Each skill is a structured markdown document that provides frameworks, patterns, and guidance for a specific design discipline. Every skill has a `metadata.references` block in its YAML frontmatter that declares its associated reference documents for progressive disclosure.

**Research and Strategy (4 skills, 14 references)**
- `user-research` -- Persona creation, interview scripts, JTBD analysis, competitive audits, empathy mapping, research synthesis
- `user-journey-mapping` -- Journey maps, service blueprints, touchpoint analysis, emotion curves, pain point identification
- `usability-evaluation` -- Nielsen's 10 heuristics, cognitive walkthroughs, System Usability Scale scoring, severity ratings
- `ab-testing-strategy` -- Hypothesis formation, test design, sample size calculation, statistical significance, results analysis

**Structure and Architecture (2 skills, 6 references)**
- `information-architecture` -- Sitemaps, navigation patterns, taxonomy, card sorting, tree testing, content grouping
- `wireframing` -- Low-fidelity to high-fidelity wireframes, layout patterns, content hierarchy, annotation standards

**Design Systems (3 skills, 10 references)**
- `design-system-creation` -- Token architecture, component APIs, Atomic Design methodology, theming, multi-brand, governance
- `design-tokens` -- Three-tier token hierarchy (global/alias/component), naming conventions, platform-specific output
- `component-library` -- Composition patterns, variant systems (CVA), state management, prop APIs, compound components

**Visual Design (4 skills, 12 references)**
- `visual-design` -- Claude's aesthetic guidance integrated with visual hierarchy, brand alignment, emotional design methodology
- `color-systems` -- Color theory, palette generation, WCAG contrast compliance, semantic tokens, dark mode palettes
- `typography-systems` -- Type scales, fluid typography with `clamp()`, font pairing, reading metrics, vertical rhythm
- `grid-layout-systems` -- Column grids, modular grids, CSS Grid, Flexbox, container queries, responsive layout strategy

**Motion (1 skill, 3 references)**
- `motion-design` -- Disney's 12 principles adapted for UI, transition choreography, scroll effects, performance budgets

**Accessibility (1 skill, 5 references)**
- `accessibility-audit` -- WCAG 2.2 checklist, ARIA patterns, keyboard navigation, screen reader compatibility, inclusive design

**Content (1 skill, 3 references)**
- `ux-writing` -- Microcopy patterns, error message frameworks, voice/tone guides, onboarding copy, empty state messaging

**Responsive and Adaptive (1 skill, 3 references)**
- `responsive-design` -- Mobile-first methodology, breakpoint strategy, fluid layouts, container queries, touch targets

**Frontend Implementation (2 skills, 8 references)**
- `css-architecture` -- BEM, Tailwind CSS, CSS Modules, CSS-in-JS, cascade layers, custom property systems
- `frontend-components` -- React, Vue, Svelte, and Web Components patterns, server components, hydration strategies

**Process (1 skill, 3 references)**
- `design-handoff` -- Specification documentation, annotation standards, redline practices, design QA checklists

**Design Knowledge (2 skills, 25 references)**
- `design-philosophies` -- Design Thinking, Gestalt principles, Don Norman, Dieter Rams, Material Design 3, Apple HIG, Nielsen's heuristics
- `design-case-studies` -- 18 in-depth case studies covering product analysis, behavioral psychology, and growth strategy (see below)

### 10 Commands

Commands are guided workflows that walk users through structured design processes.

| Command | What It Does |
|---------|-------------|
| `/design-review` | Multi-specialist design review. Routes a design artifact through accessibility, visual, interaction, and content specialists. Findings are severity-rated (Critical/Major/Minor/Enhancement) and synthesized into a prioritized action plan. |
| `/frontend-design` | The flagship command. Takes a description and produces a complete frontend design with a bold aesthetic direction chosen from 15 defined styles, design tokens, responsive layout, and production-grade HTML/CSS. Rejects generic "AI-designed" aesthetics. |
| `/create-persona` | Guided persona creation using the Jobs-to-Be-Done framework. Starts with research evidence, not assumptions. |
| `/map-journey` | User journey mapping with stages, touchpoints, emotion curves, pain points, and opportunity identification. |
| `/audit-accessibility` | Structured WCAG 2.2 compliance audit with prioritized remediation plan. |
| `/create-design-system` | Initializes a token-based design system with Atomic Design methodology, component architecture, and governance model. |
| `/generate-palette` | Accessible color palette generation with WCAG contrast verification, semantic token mapping, and dark mode support. |
| `/create-type-scale` | Responsive typography system using modular ratios, fluid sizing with `clamp()`, and vertical rhythm. |
| `/evaluate-usability` | Nielsen's heuristic evaluation with severity scoring across all 10 heuristics. |
| `/design-handoff` | Developer handoff documentation with visual specs, interaction annotations, responsive behavior notes, and QA checklist. |

### 91 Reference Documents

Every skill has associated reference documents that provide deep, specific guidance. References use progressive disclosure -- the SKILL.md provides the framework and overview, and references contain the detailed tables, code examples, checklists, and principle mappings.

**73 skill references** covering technical topics like ARIA patterns, BEM methodology, React component patterns, color theory, type scale theory, WCAG checklists, token architecture, and more.

**18 design case study references** organized into three categories:

#### Product and Platform Analysis (7 references)

| Reference | Products Analyzed |
|-----------|------------------|
| SaaS Dashboards | Stripe (data visualization mastery), Linear (keyboard-first), Notion (flexible workspace), Figma (collaborative design) |
| E-commerce | Shopify (merchant empowerment), Apple Store (product-as-hero), Glossier (community-driven), Aesop (luxury minimalism) |
| Content Platforms | Medium (reading optimization), Substack (newsletter-native), NYT (information hierarchy), Readwise (annotation-first) |
| Mobile Apps | Apple native apps (HIG in practice), Material Design apps, gesture-heavy UIs (Tinder, Maps, Snapchat) |
| Design Systems in Practice | Polaris (Shopify), Carbon (IBM), Atlassian Design System, Radix (headless primitives) |
| Brand Experiences | Apple.com (product reveal mastery), Porsche (heritage meets tech), Aesop (sensory web), Muji (radical simplicity) |
| Developer Tools | Raycast (growth-by-design thesis, keyboard-first adoption patterns) |

#### Behavioral Psychology and Growth (8 references)

Each case study maps specific design decisions to the psychological principles behind them, includes measured business outcomes, and provides a transferable playbook with strategy selection tables and common mistake analysis.

| Reference | Products Analyzed | Key Principles |
|-----------|------------------|----------------|
| Emotional Design as Growth Engine | Duolingo, Phantom, Revolut | Animation and character design as deliberate business strategy |
| Psychological Design Engines | Perplexity, Apple Fitness, Waze, Headspace, Discord, Stompers | Feedback loops, Hick's Law, Fitts's Law, emotional anchoring, social proof, Zeigarnik effect |
| SaaS Conversion Psychology | Blinkist, Headspace, Moonly, Slopes, Mobbin, Busuu, Uber | Framing effect, decoy effect, loss aversion, anchoring bias, certainty effect. Includes measured A/B test results (e.g., Moonly +39% conversion via decoy pricing). |
| Onboarding Psychology | Breathwork, Stompers, Sudoku, Speechify, Marathon | Eureka effect, Zeigarnik effect, trial-and-error learning, familiarity principle, goal gradient |
| Dopamine Design Framework | Tinder | Five integrated principles: variable reward loops (1.6B swipes/day), onboarding to aha moment, rejection-proof design (26M matches/day), victory visualization, value-first monetization ($2B revenue) |
| Netflix Behavioral Design | Netflix | Microfriction Eraser (Skip Intro: 136M daily presses, 195 years of user time saved), Algorithmic Intimacy (1,300+ micro-genres, 80% of viewing from recommendations), Viral UX (features that become cultural memes) |
| Spotify Design Moat | Spotify | Trojan Horse (invisible AI in familiar interfaces), Vanity Mirror (Wrapped: tens of millions of shares), Comfort Trap (consistency as switching cost, $8B to $25B valuation) |
| Product-Led Growth Funnel | Cross-product framework | 3-second trust test (50ms impression, 20-30% user loss), friction sweet spots, win mapping with peak-end rule, emotional design as retention layer |

#### Design Principles and Rules (3 references)

| Reference | Focus | Key Principles |
|-----------|-------|----------------|
| Apple Design Principles | Apple ecosystem | Four-layer system: physics-based interaction (rubber band, gesture momentum), mathematical precision (squircles, haptic illusions), strategic reduction (three-tap rule, iOS 77% vs Android 13% adoption), ecosystem consistency |
| Peak-End Rule | Airbnb, Ahead, Uber | Kahneman's peak-end rule applied to product design: peaks that drive bookings, peaks that create stickiness, endings that reduce churn. Five-step implementation checklist. |
| Outcome-First AI Design | Dia (Browser Company), Intercom Finn | The paradigm shift from optimizing interfaces to collapsing them. AI Disruption Matrix (2x2: utility vs experience, repetitive vs nuanced). Edge cases where interfaces must stay. |

## How the Pieces Fit Together

The plugin is designed so that agents, skills, references, and commands work as an integrated system:

1. **The UX Design Lead routes to specialists.** When you ask a design question, the lead agent determines which specialist (or combination of specialists) should handle it. A question about "our app feels generic" routes to `@visual-designer` with skills `visual-design`, `typography-systems`, and `color-systems`. A question about "users are dropping off during onboarding" routes to `@interaction-designer` and `@ux-writer` with skills `wireframing`, `user-journey-mapping`, and `ux-writing`.

2. **Skills provide frameworks and methodology.** When a specialist is working, they draw on their associated skills for structured guidance. The `visual-design` skill includes Claude's aesthetic direction library with 15 defined styles. The `accessibility-audit` skill includes the complete WCAG 2.2 checklist organized by the four principles.

3. **References provide depth.** Each skill's `metadata.references` declares its reference documents. When deeper knowledge is needed -- specific ARIA patterns, BEM naming conventions, color theory formulas, or case study precedent -- the references provide it without cluttering the primary skill document.

4. **Commands orchestrate multi-step workflows.** `/design-review` coordinates four specialists through a structured review process. `/frontend-design` walks through requirements gathering, aesthetic direction selection, color palette, typography, layout, and production code generation. Each command is a guided workflow that would otherwise require knowing which agents and skills to invoke in which order.

5. **Case studies ground decisions in precedent.** When the system recommends a design approach, it can point to how Netflix solved the same problem (microfriction erasure), how Apple applied the same principle (mathematical precision in squircle corners), or how Tinder weaponized the same psychology (variable ratio reinforcement in swipe mechanics).

## Design Philosophies Represented

The plugin encodes knowledge from these established design frameworks:

- Design Thinking (Stanford d.school five-phase process)
- Human-Centered Design
- Jobs-to-Be-Done (Ulwick/Christensen)
- Atomic Design (Brad Frost)
- Gestalt Principles (proximity, similarity, closure, continuity, figure-ground)
- Emotional Design (Don Norman's three levels: visceral, behavioral, reflective)
- Dieter Rams' 10 Principles of Good Design
- Nielsen's 10 Usability Heuristics
- Material Design 3 (Google)
- Apple Human Interface Guidelines
- Microsoft Inclusive Design
- WCAG 2.2 (W3C)

## Behavioral Psychology Principles Covered

The case study references analyze how these psychological principles are applied across real products with measured business outcomes:

- Peak-End Rule (Kahneman)
- Hick's Law, Fitts's Law
- Zeigarnik Effect
- Variable Ratio Reinforcement
- Cialdini's Principles (Social Proof, Reciprocity, Scarcity)
- Fogg Behavior Model
- Loss Aversion, Framing Effect, Anchoring Bias, Decoy Effect, Certainty Effect
- Cognitive Load Theory
- IKEA Effect, Endowment Effect
- Aesthetic-Usability Effect
- Mere Exposure Effect
- Jakob's Law
- Goal Gradient Effect
- Eureka Effect, Familiarity Principle

## Getting Started

Once installed, you can interact with the plugin in several ways:

1. **Ask the design lead anything.** The `ux-design-lead` agent understands the full design lifecycle and routes to the right specialist. "How do I make our checkout flow less confusing?" "We need to support dark mode." "Our CSS is a mess." The lead asks clarifying questions and brings in the right expertise.

2. **Use commands for guided workflows.** Run `/frontend-design` to produce a complete interface with aesthetic direction and production code. Run `/design-review` for a multi-specialist critique. Run `/audit-accessibility` for a WCAG 2.2 compliance check.

3. **Access skills directly.** Skills auto-trigger when Claude detects relevant design queries. A question about type scales activates `typography-systems`. A question about ARIA patterns activates `accessibility-audit`.

4. **Dive deep with references.** Each skill includes progressive-disclosure reference documents. The `design-case-studies` skill alone contains 18 in-depth references analyzing products from Netflix to Tinder to Apple, mapping every design decision to the psychological principle behind it.

## License

Proprietary - BitBarrel LLC

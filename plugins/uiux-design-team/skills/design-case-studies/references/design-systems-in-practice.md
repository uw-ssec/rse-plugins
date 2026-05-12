# Design Systems in Practice

In-depth case studies of four production design systems: Polaris (Shopify), Carbon (IBM), Atlassian Design System, and Radix (headless primitives). Each analysis covers system architecture, token strategy, documentation approach, and governance model.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Polaris (Shopify)](#polaris-shopify) | 14-65 | Merchant-focused design system with strong opinions |
| [Carbon (IBM)](#carbon-ibm) | 67-120 | Enterprise-scale system for complex products |
| [Atlassian Design System](#atlassian-design-system) | 122-175 | Collaboration-focused system spanning multiple products |
| [Radix](#radix) | 177-225 | Headless primitives and the unstyled component approach |
| [Cross-System Analysis](#cross-system-analysis) | 227-250 | Comparative patterns across all four systems |

## Polaris (Shopify)

Polaris is Shopify's design system, built specifically for the Shopify admin and merchant-facing tools. It is one of the most comprehensive open-source design systems, with deep documentation that explains not just what to use but why.

### System Architecture

Polaris is structured in layers that build on each other:

1. **Design tokens** -- Color, typography, spacing, shadow, border, and motion values stored as platform-agnostic tokens.
2. **CSS foundations** -- Utility classes and global styles derived from tokens.
3. **React components** -- A complete component library implemented in React with TypeScript.
4. **Patterns** -- Multi-component compositions for common commerce workflows (resource lists, data tables, forms).
5. **Guidelines** -- Design and content guidelines that explain when and how to use each component.

### Token Strategy

Polaris uses a three-tier token architecture:

| Tier | Example | Purpose |
|------|---------|---------|
| Global tokens | `--p-color-bg` | Platform-level primitives |
| Alias tokens | `--p-color-bg-surface` | Semantic meaning applied to global tokens |
| Component tokens | `--p-button-bg-primary` | Component-specific overrides |

Token names follow a structured naming convention: `--p-{category}-{property}-{variant}-{state}`. This predictable naming enables developers to guess token names without consulting documentation.

### Documentation Approach

Polaris documentation is exceptionally thorough:

- **Component pages** include: description, usage guidelines, best practices, anatomy diagram, props table, accessibility notes, and live examples.
- **Pattern pages** combine multiple components into workflow solutions with complete code examples.
- **Content guidelines** provide microcopy guidance for every component: what to write in buttons, how to phrase error messages, tone recommendations per context.
- **"Do/Don't" examples** appear throughout, showing correct and incorrect usage with explanations.

### Governance Model

Shopify's design system team operates with a hub-and-spoke model:

- **Core team** maintains the component library, token system, and documentation.
- **Product teams** contribute new components and patterns through a proposal process.
- **RFC (Request for Comments)** process for significant changes. Any team member can submit an RFC for new components, token changes, or breaking modifications.
- **Versioning** follows semantic versioning. Breaking changes require a major version bump with migration guides.
- **Deprecation policy**: Components are deprecated with warnings for two minor versions before removal.

### Transferable Lessons

1. **Content guidelines within the design system reduce UX writing inconsistency across teams.**
2. **Three-tier token architecture balances flexibility (global) with specificity (component).**
3. **"Do/Don't" documentation is more effective than written guidelines alone.**
4. **The RFC process democratizes system evolution while maintaining quality.**

## Carbon (IBM)

Carbon is IBM's open-source design system, built for enterprise-scale applications. It handles the unique challenges of enterprise design: dense data, complex workflows, accessibility compliance at scale, and multi-product consistency.

### System Architecture

Carbon is organized into packages:

1. **Carbon Styles** -- Sass-based styles with design tokens, grid, and typography.
2. **Carbon Components** -- Framework-specific implementations (React, Angular, Vue, Svelte, Web Components).
3. **Carbon Charts** -- A dedicated data visualization library aligned with the Carbon design language.
4. **Carbon for IBM.com** -- Extended patterns for IBM's marketing and documentation sites.
5. **Carbon for AI** -- Components and patterns specific to AI-powered interfaces (prompt inputs, response displays, confidence indicators).

### Token Strategy

Carbon uses a two-tier token system with a strong emphasis on theme-ability:

| Tier | Example | Purpose |
|------|---------|---------|
| Theme tokens | `$background`, `$text-primary` | Semantic tokens that change with theme |
| Layout tokens | `$spacing-05`, `$container-02` | Fixed spacing and sizing values |

Carbon provides four built-in themes: White, Gray 10, Gray 90, and Gray 100. Each theme maps semantic tokens to different values, enabling instant theme switching without component changes.

**Grid system:** Carbon uses a responsive grid with 16 columns (not the more common 12). This provides finer layout control for data-dense enterprise interfaces where precise column alignment matters.

### Documentation Approach

Carbon's documentation is technically rigorous:

- **Component specification** with detailed props, variants, and interaction states.
- **Accessibility guidelines** per component, including ARIA roles, keyboard interaction, and screen reader expectations.
- **Code examples** in every supported framework (React, Angular, Vue, Svelte, Web Components).
- **Usage guidelines** focused on enterprise-specific contexts: data tables with pagination, complex forms with validation, and multi-step workflows.
- **Migration guides** between major versions with detailed before/after code examples.

### Governance Model

IBM's governance reflects its scale:

- **Dedicated design system team** of 30+ contributors across design, engineering, and documentation.
- **Cross-product design council** meets regularly to align on system direction and resolve conflicts.
- **Contribution guidelines** with specific requirements for accessibility compliance, documentation completeness, and cross-framework implementation.
- **PAT (Pattern and Asset Team)** reviews all contributions for quality, consistency, and alignment with system principles.
- **IBM Design Language** serves as the overarching philosophical foundation that Carbon implements.

### Transferable Lessons

1. **Enterprise systems need more grid columns for data-dense layouts.**
2. **Theme-ability is essential for enterprise products that serve different contexts and brands.**
3. **Multi-framework support requires careful architecture to avoid implementation drift.**
4. **Dedicated AI component patterns are becoming necessary as AI features proliferate.**

## Atlassian Design System

Atlassian Design System (ADS) serves Jira, Confluence, Trello, Bitbucket, and other Atlassian products. The design challenge: maintaining consistency across products with very different purposes (project management, documentation, kanban boards, code hosting) while allowing each product to serve its specific users effectively.

### System Architecture

ADS is organized around a unified token foundation with product-specific extensions:

1. **Design tokens** -- Shared across all Atlassian products via the `@atlaskit/tokens` package. Tokens are the single source of truth for color, spacing, typography, and elevation.
2. **Atlaskit components** -- A React component library shared across products. Components reference tokens, ensuring theme consistency.
3. **Product-specific patterns** -- Each product (Jira, Confluence, Trello) has product-specific patterns built from shared components. Jira's board view is built from Atlaskit primitives but with Jira-specific behavior.
4. **Pragmatic patterns** -- Cross-product patterns for common workflows: user pickers, permission selectors, project selectors.

### Token Strategy

Atlassian uses a semantic token approach with a strong emphasis on accessibility:

| Category | Example | Purpose |
|----------|---------|---------|
| Color | `color.text`, `color.text.subtle`, `color.text.disabled` | Semantic text colors that adapt to theme |
| Spacing | `space.100`, `space.200` | Incremental spacing scale (100 = 8px) |
| Elevation | `elevation.surface`, `elevation.surface.raised` | Surface hierarchy tokens |
| Typography | `font.heading.large`, `font.body` | Composite typography tokens |

**Token-first migration:** Atlassian undertook a massive migration from hardcoded values to tokens across all products. The migration tooling automatically detected hardcoded hex values and suggested token replacements, enabling automated pull requests across thousands of files.

### Documentation Approach

ADS documentation focuses on cross-product consistency:

- **Token browser** -- Interactive tool to explore all tokens with visual previews and usage guidance.
- **Component pages** -- Standard props documentation with a focus on composition (how components work together).
- **Pattern pages** -- Cross-product patterns with product-specific variations documented.
- **Migration guides** -- Detailed guides for each major version, including automated codemods.
- **Decision records** -- Public ADRs (Architecture Decision Records) explaining why specific design system choices were made.

### Governance Model

Atlassian's governance balances central control with product autonomy:

- **Platform Design team** owns the shared token system and core Atlaskit components.
- **Product Design teams** own product-specific patterns and can propose additions to the shared system.
- **Contribution model**: Products build with shared components. When a product-specific pattern becomes useful across products, it is promoted to the shared system through a review process.
- **Token governance**: Any token change that affects multiple products requires cross-product sign-off.
- **Design reviews**: Major product features include a "system consistency check" where the platform team reviews alignment with ADS.

### Transferable Lessons

1. **Multi-product systems need a shared token layer with product-specific pattern extensions.**
2. **Automated migration tooling is essential for large-scale token adoption.**
3. **Architecture Decision Records (ADRs) build institutional knowledge about why decisions were made.**
4. **Token-first design (designing with tokens from the start) is easier than token-migration (converting existing designs to tokens).**

## Radix

Radix takes a fundamentally different approach: headless (unstyled) UI primitives that provide accessible interaction behavior without visual opinions. Developers bring their own styles.

### System Architecture

Radix is organized into three products:

1. **Radix Primitives** -- Unstyled, accessible components (Dialog, Dropdown, Tabs, Tooltip, Accordion, etc.). No CSS included. Components provide ARIA attributes, keyboard navigation, focus management, and state logic.
2. **Radix Themes** -- An optional visual layer built on Primitives. Provides a complete, styled component library with a token-based theming system.
3. **Radix Colors** -- A scientifically designed color scale system with 12 steps per hue, optimized for dark mode and accessibility.

### Philosophy: Separation of Behavior and Style

Radix Primitives intentionally ship zero CSS. The component handles:
- Accessible markup (correct ARIA roles and attributes)
- Keyboard navigation (arrow keys, Enter, Escape, Tab)
- Focus management (focus trapping in modals, focus restoration)
- State management (open/closed, selected/unselected)

The developer handles:
- All visual styling (colors, spacing, typography, borders, shadows)
- Animation (entry/exit transitions)
- Layout and positioning

This separation means Radix components work with any styling approach: CSS modules, Tailwind, styled-components, vanilla CSS, or any other method.

### Token Strategy (Radix Themes)

Radix Themes uses a CSS custom property system with a consistent naming convention:

```css
/* Radix Themes token structure */
--accent-1 through --accent-12    /* 12-step color scale */
--gray-1 through --gray-12        /* 12-step neutral scale */
--radius-1 through --radius-6     /* Border radius scale */
--space-1 through --space-9       /* Spacing scale */
```

The 12-step color scale provides specific assignments:
- Steps 1-2: Backgrounds
- Steps 3-5: Component backgrounds (hover, active)
- Steps 6-8: Borders
- Steps 9-10: Solid fills
- Steps 11-12: Text

This structured scale ensures accessible contrast regardless of which hue is chosen.

### Documentation Approach

Radix documentation is developer-centric:

- **API reference** -- Complete props documentation for every component.
- **Accessibility** -- Detailed description of ARIA attributes, keyboard interactions, and screen reader behavior for each component.
- **Styling examples** -- CSS examples showing how to style each component with different approaches (CSS modules, Tailwind, styled-components).
- **Composition patterns** -- How to combine primitives into complex components (combobox from popover + input + list).
- **No design guidelines** -- Unlike Polaris and Carbon, Radix deliberately provides no visual design guidance. The developer makes all visual decisions.

### Governance Model

Radix is an open-source project maintained by WorkOS:

- **Core team** designs the API and implements the primitives.
- **Community contributions** focus on bug fixes, documentation, and edge case handling.
- **RFC process** for new primitives and API changes.
- **Strict API stability** -- breaking changes are rare and announced well in advance.
- **Unstyled by design** means fewer visual opinions to govern. The governance focuses on interaction behavior and accessibility compliance.

### Transferable Lessons

1. **Separating behavior from style enables maximum flexibility for diverse teams.**
2. **12-step color scales provide a systematic approach to accessible color usage.**
3. **Headless components are ideal when teams have strong design opinions but need accessible interaction behavior.**
4. **Not providing design guidelines is itself a design decision that serves teams with existing design systems.**

## Cross-System Analysis

| Dimension | Polaris | Carbon | Atlassian | Radix |
|-----------|---------|--------|-----------|-------|
| Primary audience | Shopify merchants + internal | IBM products + enterprise | Atlassian products | Any web developer |
| Styling approach | Opinionated (styled) | Opinionated (themed) | Opinionated (tokenized) | Headless (unstyled) |
| Token tiers | 3 (global, alias, component) | 2 (theme, layout) | Semantic categories | 12-step scales |
| Framework support | React | React, Angular, Vue, Svelte, Web Components | React | React |
| Grid system | 12-column | 16-column | Flexible | None (developer's choice) |
| Documentation depth | Exceptional (content guidelines included) | Strong (enterprise focus) | Strong (multi-product focus) | API-focused (no design guidelines) |
| Governance | RFC process, hub-and-spoke | Design council, PAT review | Platform team + product teams | Core team, community contributions |

**Pattern:** Opinionated systems (Polaris, Carbon, Atlassian) trade flexibility for consistency. Headless systems (Radix) trade consistency for flexibility. Choose based on whether your challenge is "we need consistency across teams" (opinionated) or "we need accessibility without visual constraints" (headless).

## See Also

- [[saas-dashboards.md]] -- Products built with these design systems (Stripe, Linear, Notion)
- [[brand-experiences.md]] -- How design systems support brand consistency across touchpoints
- [[../../design-philosophies/references/dieter-rams-principles.md]] -- Design systems operationalize Rams' principles at scale
- [[../../design-philosophies/references/material-design.md]] -- Material Design as the most widely adopted design system
- [[../../responsive-design/references/breakpoint-strategy.md]] -- How design systems define and manage breakpoints

**Back to:** [Design Case Studies Skill](../SKILL.md)

---
name: frontend-components
description: Implement frontend components with framework-specific patterns for React, Vue, Svelte, and Web Components including server components, hydration strategies, performance optimization, image handling, and font loading.
metadata:
   references:
   - references/react-patterns.md
   - references/svelte-patterns.md
   - references/vue-patterns.md
   - references/web-components.md
---

# Frontend Components

Components bridge design and code. A design system lives or dies by the quality of its component implementations. Well-built components enforce consistency, encapsulate complexity, provide accessible defaults, and make the right thing the easy thing for every developer who uses them.

This skill covers framework-specific implementation patterns, architectural principles that apply across all frameworks, and performance optimization techniques that keep component-driven interfaces fast.

## Framework Comparison

Each framework brings different trade-offs to component implementation. Choose based on team expertise, ecosystem requirements, and performance constraints.

| Feature | React | Vue | Svelte | Web Components |
|---------|-------|-----|--------|----------------|
| **State management** | useState/useReducer, external stores (Zustand, Jotai) | ref/reactive, Pinia | Reactive declarations, stores | Properties, attributes, internal state |
| **Styling approach** | CSS Modules, CSS-in-JS, Tailwind | Scoped styles (SFC), CSS Modules | Scoped styles (automatic), :global() | Shadow DOM encapsulation, ::part |
| **Composition** | Children, render props, hooks | Slots, composables, provide/inject | Slots, context, actions | Slots, Shadow DOM |
| **SSR** | Next.js, Remix, React Server Components | Nuxt, SSR mode | SvelteKit | Limited (Declarative Shadow DOM) |
| **Ecosystem** | Largest: libraries for everything | Growing: strong official tooling | Smaller: focused, high-quality | Native: framework-agnostic |
| **Learning curve** | Medium (hooks mental model) | Low (familiar HTML/CSS/JS model) | Low (least boilerplate) | Medium (platform APIs) |
| **Bundle size** | ~40kb (React + ReactDOM) | ~33kb (Vue 3) | ~2kb (Svelte runtime) | 0kb (native platform) |

## Component Architecture Principles

These principles apply regardless of which framework you use.

### Single Responsibility

Each component should do one thing well. A `Button` component renders a button with appropriate styles and states. It does not fetch data, manage routes, or validate forms. When a component starts accumulating unrelated responsibilities, split it.

Indicators a component needs splitting:
- It accepts more than 8-10 props
- It contains multiple conditional rendering branches for unrelated features
- Its file exceeds 200-300 lines
- Changes to one part frequently break another

### Prop Drilling vs. Context

**Prop drilling** (passing data through intermediate components) is acceptable for 2-3 levels. Beyond that, it creates fragile coupling and noisy component signatures.

**Context/Provide-Inject/Stores** solve this by making data available to any descendant without threading it through every intermediate component. Use context for:
- Theme values (colors, spacing, mode)
- Locale and internationalization
- Authentication state
- Feature flags

Do not use context for frequently-changing values (like cursor position or scroll offset) because context changes trigger re-renders in all consumers.

### Controlled vs. Uncontrolled Components

**Controlled components** receive their state as props and notify parents of changes via callbacks. The parent owns the state. This is the correct pattern for form components in design systems because it gives consumers full control.

**Uncontrolled components** manage their own internal state. Useful for components where the parent does not need to know the intermediate state (e.g., an accordion's open/close state, a tooltip's visibility).

**Hybrid approach**: Accept an optional value prop. If provided, the component is controlled. If not, it manages its own state internally. This pattern maximizes flexibility.

### Error Boundaries

Components fail. Network requests fail. Data arrives in unexpected shapes. Error boundaries catch rendering failures and display fallback UI instead of crashing the entire application.

- In React: `ErrorBoundary` class component or libraries like `react-error-boundary`
- In Vue: `onErrorCaptured` lifecycle hook or `<Suspense>` with error slot
- In Svelte: `{#await}` block with catch clause, or SvelteKit `+error.svelte`
- In Web Components: try/catch in lifecycle callbacks, custom error rendering

### Loading States

Every component that depends on asynchronous data needs three states:
1. **Loading**: Skeleton, spinner, or placeholder indicating work in progress
2. **Success**: The rendered content
3. **Error**: A meaningful error message with recovery options

Never show a blank screen while loading. Skeleton screens are preferred over spinners because they set expectations about the shape of incoming content and reduce perceived loading time.

## Performance Patterns

Frontend performance is a design feature. A beautiful component that takes 3 seconds to render provides a worse user experience than a plain one that renders instantly.

### Lazy Loading and Code Splitting

Load components only when they are needed. Below-the-fold content, modal dialogs, and admin-only features should not be included in the initial bundle.

- **React**: `React.lazy()` with `<Suspense>` fallback
- **Vue**: `defineAsyncComponent()` with loading/error components
- **Svelte**: Dynamic `import()` with `{#await}`
- **Route-based splitting**: Next.js, Nuxt, and SvelteKit split by route automatically

### Virtualization for Long Lists

Rendering thousands of DOM nodes is expensive. Virtual scrolling renders only the visible items plus a small buffer.

- **React**: `react-window` or `@tanstack/react-virtual`
- **Vue**: `vue-virtual-scroller`
- **Svelte**: `svelte-virtual-list`
- **Principle**: Render only what is in the viewport; recycle DOM nodes as the user scrolls

### Image Optimization

Images are typically the largest assets on any page. Optimizing them produces the biggest performance wins.

- **Format**: Use WebP or AVIF with JPEG/PNG fallbacks. AVIF is ~50% smaller than JPEG at equivalent quality.
- **Responsive images**: Use `srcset` and `sizes` attributes to serve appropriately-sized images for each viewport.
- **Lazy loading**: Apply `loading="lazy"` to below-the-fold images. Framework image components (Next.js `<Image>`, Nuxt `<NuxtImg>`) handle this automatically.
- **Aspect ratio**: Set `width` and `height` attributes or use `aspect-ratio` CSS to prevent layout shift (CLS).
- **Priority hints**: Mark above-the-fold hero images with `fetchpriority="high"` and `loading="eager"`.

### Font Loading

Web fonts cause layout shift if not handled correctly. The wrong loading strategy creates a flash of invisible text (FOIT) or flash of unstyled text (FOUT).

- **`font-display: swap`**: Shows fallback font immediately, swaps when web font loads. Best for body text.
- **`font-display: optional`**: Uses web font only if it loads very quickly; otherwise uses fallback permanently. Best for reducing CLS.
- **Preloading**: Add `<link rel="preload" href="font.woff2" as="font" type="font/woff2" crossorigin>` for critical fonts.
- **Subsetting**: Remove unused glyphs to reduce font file size. A Latin-only subset of a full Unicode font can be 80% smaller.
- **Variable fonts**: One variable font file replaces multiple weight/style files, reducing total download size.

### Cumulative Layout Shift (CLS) Prevention

CLS occurs when visible elements shift position after the initial render. It is one of the Core Web Vitals and directly affects user experience.

- Reserve space for images with explicit dimensions or `aspect-ratio`
- Reserve space for ads and embeds with `min-height`
- Avoid inserting content above existing content (e.g., late-loading banners)
- Use `font-display: optional` or `size-adjust` for font fallbacks
- Animate with `transform` and `opacity` only (never animate `width`, `height`, `top`, `left`)

## Deep Dive References

### [React Patterns](references/react-patterns.md)

- Core Hooks
- Custom Hooks
- Compound Components
- Server Components vs Client Components
- Suspense Boundaries
- forwardRef and Polymorphic Components
- Performance Optimization
- Accessibility with React

### [Vue Patterns](references/vue-patterns.md)

- Reactive Refs and Computed
- Composables
- Provide/Inject
- Scoped Slots
- Pinia State Management
- Teleport
- Transitions and Animations
- Nuxt Integration
- *...and 1 more sections*

### [Svelte Patterns](references/svelte-patterns.md)

- Reactive Declarations
- Stores
- Transitions and Animations
- SvelteKit Routing and Loading
- Actions
- Built-in Accessibility Warnings
- Component Composition
- CSS Scoping

### [Web Components](references/web-components.md)

- Custom Elements API
- Shadow DOM Encapsulation
- Lit Framework Patterns
- Declarative Shadow DOM
- Framework Interoperability
- Cross-Framework Design Systems
- Form-Associated Custom Elements

## Next Steps

After mastering component implementation, expand into system-level concerns:

- **[Component Library](../component-library/SKILL.md)**: Build a reusable component library with documentation, testing, and versioning
- **[CSS Architecture](../css-architecture/SKILL.md)**: Choose and implement the styling strategy that components consume
- **[Design System Creation](../design-system-creation/SKILL.md)**: Connect components with tokens, documentation, and governance
- **[Accessibility Audit](../accessibility-audit/SKILL.md)**: Ensure every component meets WCAG 2.2 AA compliance
- **[Motion Design](../motion-design/SKILL.md)**: Add purposeful animation and transitions to component interactions

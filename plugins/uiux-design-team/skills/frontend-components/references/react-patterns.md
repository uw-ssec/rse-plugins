# React Patterns

Comprehensive reference for React component patterns used in design system implementation. Covers hooks, composition patterns, Server Components, Suspense boundaries, performance optimization, and accessibility integration for building robust, reusable UI components.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Core Hooks](#core-hooks) | 14-68 | useState, useEffect, useRef, useMemo, useCallback with design system examples |
| [Custom Hooks](#custom-hooks) | 70-105 | Building reusable hooks for design system concerns |
| [Compound Components](#compound-components) | 107-140 | Context-based compound component pattern for complex widgets |
| [Server Components vs Client Components](#server-components-vs-client-components) | 142-172 | When to use each, serialization boundaries, and composition rules |
| [Suspense Boundaries](#suspense-boundaries) | 174-200 | Streaming, lazy loading, and loading state architecture |
| [forwardRef and Polymorphic Components](#forwardref-and-polymorphic-components) | 202-230 | Ref forwarding and the "as" prop pattern for flexible components |
| [Performance Optimization](#performance-optimization) | 232-262 | React.memo, useDeferredValue, useTransition, and profiling |
| [Accessibility with React](#accessibility-with-react) | 264-295 | ARIA attributes, focus management, and live regions in React |
| [See Also](#see-also) | 297-303 | Related references and skills |

## Core Hooks

### useState

Use `useState` for component-local state that triggers re-renders when it changes. In design system components, this typically manages visibility, selection, and internal interaction state.

```tsx
function Accordion({ defaultOpen = false, children }) {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <div className="accordion">
      <button
        aria-expanded={isOpen}
        onClick={() => setIsOpen(prev => !prev)}
      >
        Toggle
      </button>
      {isOpen && <div role="region">{children}</div>}
    </div>
  );
}
```

When a component needs to support both controlled and uncontrolled modes, use a pattern that checks whether the value prop is provided:

```tsx
function Toggle({ value, defaultValue = false, onChange }) {
  const [internalValue, setInternalValue] = useState(defaultValue);
  const isControlled = value !== undefined;
  const currentValue = isControlled ? value : internalValue;

  const handleChange = (next) => {
    if (!isControlled) setInternalValue(next);
    onChange?.(next);
  };

  return (
    <button role="switch" aria-checked={currentValue} onClick={() => handleChange(!currentValue)}>
      {currentValue ? "On" : "Off"}
    </button>
  );
}
```

### useEffect

Use `useEffect` for synchronizing with external systems: DOM measurements, event listeners, focus management, and data fetching. Avoid using it for derived state -- use `useMemo` instead.

```tsx
function Tooltip({ anchorRef, content, isVisible }) {
  const tooltipRef = useRef(null);

  useEffect(() => {
    if (!isVisible || !anchorRef.current || !tooltipRef.current) return;

    // Position tooltip relative to anchor
    const anchorRect = anchorRef.current.getBoundingClientRect();
    tooltipRef.current.style.top = `${anchorRect.bottom + 8}px`;
    tooltipRef.current.style.left = `${anchorRect.left}px`;
  }, [isVisible, anchorRef]);

  if (!isVisible) return null;
  return <div ref={tooltipRef} role="tooltip">{content}</div>;
}
```

### useRef

Use `useRef` for persisting values across renders without triggering re-renders. Common uses in design systems: DOM element references, previous value tracking, and storing interval/timeout IDs.

```tsx
function FocusTrap({ children }) {
  const containerRef = useRef(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const focusableElements = container.querySelectorAll(
      'a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const first = focusableElements[0];
    const last = focusableElements[focusableElements.length - 1];

    const handleKeyDown = (e) => {
      if (e.key !== "Tab") return;
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    };

    container.addEventListener("keydown", handleKeyDown);
    first?.focus();
    return () => container.removeEventListener("keydown", handleKeyDown);
  }, []);

  return <div ref={containerRef}>{children}</div>;
}
```

### useMemo and useCallback

Use `useMemo` to cache expensive computations. Use `useCallback` to stabilize function references passed to memoized children. Both are optimization tools, not correctness tools -- code should work without them; they only prevent unnecessary work.

```tsx
function DataTable({ rows, sortColumn, sortDirection }) {
  const sortedRows = useMemo(() => {
    return [...rows].sort((a, b) => {
      const val = a[sortColumn] > b[sortColumn] ? 1 : -1;
      return sortDirection === "asc" ? val : -val;
    });
  }, [rows, sortColumn, sortDirection]);

  return <table>{/* render sortedRows */}</table>;
}
```

## Custom Hooks

Custom hooks extract reusable stateful logic from components. In design systems, they encapsulate common concerns like media queries, keyboard interactions, and outside-click detection.

### useMediaQuery

```tsx
function useMediaQuery(query) {
  const [matches, setMatches] = useState(() =>
    typeof window !== "undefined" ? window.matchMedia(query).matches : false
  );

  useEffect(() => {
    const mql = window.matchMedia(query);
    const handler = (e) => setMatches(e.matches);
    mql.addEventListener("change", handler);
    return () => mql.removeEventListener("change", handler);
  }, [query]);

  return matches;
}

// Usage: const isMobile = useMediaQuery("(max-width: 768px)");
```

### useClickOutside

```tsx
function useClickOutside(ref, handler) {
  useEffect(() => {
    const listener = (event) => {
      if (!ref.current || ref.current.contains(event.target)) return;
      handler(event);
    };
    document.addEventListener("mousedown", listener);
    document.addEventListener("touchstart", listener);
    return () => {
      document.removeEventListener("mousedown", listener);
      document.removeEventListener("touchstart", listener);
    };
  }, [ref, handler]);
}

// Usage in a dropdown:
// const dropdownRef = useRef(null);
// useClickOutside(dropdownRef, () => setIsOpen(false));
```

### useId for Accessible Labels

React 18's `useId` generates stable, unique IDs for associating labels with form controls:

```tsx
function FormField({ label, children, error }) {
  const id = useId();
  const errorId = `${id}-error`;

  return (
    <div>
      <label htmlFor={id}>{label}</label>
      {React.cloneElement(children, {
        id,
        "aria-describedby": error ? errorId : undefined,
        "aria-invalid": !!error,
      })}
      {error && <p id={errorId} role="alert">{error}</p>}
    </div>
  );
}
```

## Compound Components

The compound component pattern uses React Context to share state between a parent and its children without prop drilling. This is the standard pattern for design system widgets like Tabs, Accordion, and Select.

```tsx
const TabsContext = createContext(null);

function Tabs({ defaultValue, children }) {
  const [activeTab, setActiveTab] = useState(defaultValue);

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div role="tablist">{children}</div>
    </TabsContext.Provider>
  );
}

function Tab({ value, children }) {
  const { activeTab, setActiveTab } = useContext(TabsContext);
  const isActive = activeTab === value;

  return (
    <button
      role="tab"
      aria-selected={isActive}
      tabIndex={isActive ? 0 : -1}
      onClick={() => setActiveTab(value)}
    >
      {children}
    </button>
  );
}

function TabPanel({ value, children }) {
  const { activeTab } = useContext(TabsContext);
  if (activeTab !== value) return null;

  return <div role="tabpanel">{children}</div>;
}

// Usage:
// <Tabs defaultValue="tab1">
//   <Tab value="tab1">First</Tab>
//   <Tab value="tab2">Second</Tab>
//   <TabPanel value="tab1">Content 1</TabPanel>
//   <TabPanel value="tab2">Content 2</TabPanel>
// </Tabs>
```

The compound pattern is preferable to a monolithic props-based API because it gives consumers control over rendering order, wrapper elements, and conditional rendering while the parent still controls shared state.

## Server Components vs Client Components

React Server Components (RSC) render on the server and send HTML to the client. They cannot use state, effects, or browser APIs. Client Components render on the client and support full interactivity.

### When to Use Server Components

- Static content display (headings, text, images)
- Data fetching (directly await database/API calls)
- Accessing server-only resources (file system, environment variables)
- Rendering markdown, syntax highlighting, or other heavy transformations
- Layout components that wrap interactive children

### When to Use Client Components

- Any component using `useState`, `useEffect`, `useRef`, or other hooks
- Event handlers (onClick, onChange, onSubmit)
- Browser APIs (window, document, localStorage, IntersectionObserver)
- Third-party libraries that use client-side features

### Composition Rules

```tsx
// Server Component (default in Next.js App Router)
async function ProductPage({ id }) {
  const product = await db.getProduct(id); // Server-only data access

  return (
    <article>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      {/* Client Component nested inside Server Component -- valid */}
      <AddToCartButton productId={id} />
    </article>
  );
}

// Client Component
"use client";
function AddToCartButton({ productId }) {
  const [loading, setLoading] = useState(false);
  // Interactive logic here
}
```

Server Components cannot import Client Components as children via `import` inside the server file and then pass them JSX that uses client hooks. Instead, pass Client Components as `children` or props from a parent Server Component. This is the "donut pattern": server shell, client hole, server filling.

## Suspense Boundaries

Suspense lets components declare loading states declaratively. When a component inside a Suspense boundary is not ready (lazy-loaded, fetching data with a Suspense-compatible library), the boundary renders its fallback.

```tsx
import { Suspense, lazy } from "react";

const HeavyChart = lazy(() => import("./HeavyChart"));

function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<ChartSkeleton />}>
        <HeavyChart />
      </Suspense>
      <Suspense fallback={<TableSkeleton />}>
        <DataTable />
      </Suspense>
    </div>
  );
}
```

### Nesting Strategy

Place Suspense boundaries around independently loading sections. Do not wrap the entire page in a single boundary -- this shows one giant loading state instead of progressive content. Each boundary should correspond to a meaningful UI section that can load independently.

### Streaming with Server Components

In Next.js App Router, Suspense boundaries define streaming chunks. The server sends HTML for resolved components immediately and streams the rest as it completes:

```tsx
async function Page() {
  return (
    <main>
      <Header /> {/* Sent immediately */}
      <Suspense fallback={<FeedSkeleton />}>
        <Feed /> {/* Streamed when data resolves */}
      </Suspense>
      <Suspense fallback={<SidebarSkeleton />}>
        <Sidebar /> {/* Streamed independently */}
      </Suspense>
    </main>
  );
}
```

## forwardRef and Polymorphic Components

### forwardRef

Design system components must forward refs so consumers can access the underlying DOM element for focus management, measurements, and animation libraries.

```tsx
const Button = forwardRef(function Button({ variant = "solid", size = "md", children, ...props }, ref) {
  return (
    <button ref={ref} className={buttonStyles({ variant, size })} {...props}>
      {children}
    </button>
  );
});
```

### Polymorphic "as" Prop

The polymorphic pattern lets consumers change the rendered element while keeping component styles and behavior. A `Button` might render as an `<a>` for navigation or a `<div>` for custom contexts.

```tsx
function Box({ as: Component = "div", className, ...props }) {
  return <Component className={className} {...props} />;
}

// Usage:
// <Box as="section" className="card">...</Box>
// <Box as="a" href="/about" className="card">...</Box>
```

For type-safe polymorphic components in TypeScript:

```tsx
type BoxProps<C extends React.ElementType> = {
  as?: C;
  children?: React.ReactNode;
} & Omit<React.ComponentPropsWithoutRef<C>, "as" | "children">;

function Box<C extends React.ElementType = "div">({ as, ...props }: BoxProps<C>) {
  const Component = as || "div";
  return <Component {...props} />;
}
```

## Performance Optimization

### React.memo

Wrap components in `React.memo` when they receive the same props across parent re-renders. This is most valuable for list items, table cells, and other components rendered many times.

```tsx
const ListItem = React.memo(function ListItem({ id, label, onSelect }) {
  return (
    <li>
      <button onClick={() => onSelect(id)}>{label}</button>
    </li>
  );
});
```

Memoization only works if props are referentially stable. Stabilize objects and functions with `useMemo` and `useCallback` in the parent.

### useDeferredValue

`useDeferredValue` creates a deferred version of a value that lags behind during urgent updates. Use it for expensive renders that should not block user input.

```tsx
function SearchResults({ query }) {
  const deferredQuery = useDeferredValue(query);
  const isStale = query !== deferredQuery;

  const results = useMemo(() => filterLargeDataset(deferredQuery), [deferredQuery]);

  return (
    <ul style={{ opacity: isStale ? 0.7 : 1 }}>
      {results.map(item => <li key={item.id}>{item.name}</li>)}
    </ul>
  );
}
```

### useTransition

`useTransition` marks state updates as non-urgent, allowing React to keep the UI responsive during heavy re-renders.

```tsx
function TabContainer() {
  const [tab, setTab] = useState("home");
  const [isPending, startTransition] = useTransition();

  function selectTab(nextTab) {
    startTransition(() => setTab(nextTab));
  }

  return (
    <div>
      <TabBar activeTab={tab} onSelect={selectTab} />
      <div style={{ opacity: isPending ? 0.6 : 1 }}>
        {tab === "home" && <HomePanel />}
        {tab === "settings" && <SettingsPanel />}
      </div>
    </div>
  );
}
```

## Accessibility with React

### ARIA Attributes in JSX

React uses camelCase for ARIA attributes: `aria-label` becomes `aria-label` (exception: ARIA attributes keep their hyphens in JSX). Always prefer semantic HTML over ARIA.

```tsx
// Prefer semantic HTML
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/">Home</a></li>
  </ul>
</nav>

// ARIA only when no semantic element exists
<div role="alert" aria-live="assertive">
  {errorMessage}
</div>
```

### Focus Management

When opening modals, drawers, or dropdowns, move focus to the new content. When closing, return focus to the trigger element.

```tsx
function Dialog({ isOpen, onClose, triggerRef, children }) {
  const dialogRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      dialogRef.current?.focus();
    } else {
      triggerRef.current?.focus();
    }
  }, [isOpen, triggerRef]);

  if (!isOpen) return null;

  return (
    <div
      ref={dialogRef}
      role="dialog"
      aria-modal="true"
      tabIndex={-1}
      onKeyDown={(e) => e.key === "Escape" && onClose()}
    >
      {children}
    </div>
  );
}
```

### Live Regions

Use `aria-live` to announce dynamic content changes to screen readers. Use `"polite"` for non-urgent updates and `"assertive"` for errors or critical alerts.

```tsx
function SearchStatus({ count, isLoading }) {
  return (
    <div aria-live="polite" aria-atomic="true" className="sr-only">
      {isLoading ? "Searching..." : `${count} results found`}
    </div>
  );
}
```

## See Also

- [[vue-patterns.md]] -- Vue 3 Composition API patterns for comparison and cross-framework understanding
- [[svelte-patterns.md]] -- Svelte reactive patterns and how they differ from React's hooks model
- [[web-components.md]] -- Using React with Web Components and building framework-agnostic components
- [[../../component-library/references/composition-patterns.md]] -- Framework-agnostic compound component and headless patterns
- [[../../accessibility-audit/references/aria-patterns.md]] -- Complete ARIA widget implementations for common components
- [[../../css-architecture/references/css-in-js-patterns.md]] -- Styling approaches commonly used with React components

**Back to:** [Frontend Components Skill](../SKILL.md)

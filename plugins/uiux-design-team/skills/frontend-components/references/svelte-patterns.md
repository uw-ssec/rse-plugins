# Svelte Patterns

Comprehensive reference for Svelte component patterns used in design system implementation. Covers reactive declarations, stores, transitions, SvelteKit routing, actions, built-in accessibility warnings, component composition, and CSS scoping mechanisms.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Reactive Declarations](#reactive-declarations) | 14-50 | The $: syntax, reactive assignments, and derived values |
| [Stores](#stores) | 52-100 | Writable, readable, and derived stores for shared state |
| [Transitions and Animations](#transitions-and-animations) | 102-140 | Built-in transition directives, custom transitions, and motion |
| [SvelteKit Routing and Loading](#sveltekit-routing-and-loading) | 142-178 | File-based routing, load functions, and SSR patterns |
| [Actions](#actions) | 180-210 | Reusable DOM-level behaviors via the use: directive |
| [Built-in Accessibility Warnings](#built-in-accessibility-warnings) | 212-240 | Compiler-enforced a11y checks and how to address them |
| [Component Composition](#component-composition) | 242-275 | Slots, context, component events, and forwarding patterns |
| [CSS Scoping](#css-scoping) | 277-305 | Automatic scoping, :global(), and CSS custom properties |
| [See Also](#see-also) | 307-313 | Related references and skills |

## Reactive Declarations

Svelte's reactivity is compile-time, not runtime. The compiler detects assignments to variables and generates code that updates the DOM when those variables change. No virtual DOM, no hooks rules, no dependency arrays.

### Basic Reactivity

```svelte
<script>
  let count = 0;
  let name = 'world';

  function increment() {
    count += 1; // Assignment triggers reactivity
  }
</script>

<button on:click={increment}>
  Clicked {count} times
</button>
<p>Hello {name}!</p>
```

### Reactive Declarations with $:

The `$:` label marks statements that re-run whenever their dependencies change. Use them for derived values and side effects.

```svelte
<script>
  let width = 10;
  let height = 20;

  // Derived value -- recalculates when width or height changes
  $: area = width * height;
  $: perimeter = 2 * (width + height);

  // Reactive statement -- runs as a side effect
  $: if (area > 500) {
    console.warn('Area exceeds maximum');
  }

  // Reactive block
  $: {
    document.title = `Area: ${area}`;
    console.log(`Dimensions: ${width}x${height}`);
  }
</script>

<input type="number" bind:value={width} />
<input type="number" bind:value={height} />
<p>Area: {area}, Perimeter: {perimeter}</p>
```

### Array and Object Reactivity

Svelte's reactivity triggers on assignment, not mutation. Array methods like `push` and `splice` do not trigger updates unless you reassign the variable afterward.

```svelte
<script>
  let items = [];

  function addItem(item) {
    items = [...items, item]; // Spread creates new array -- triggers update
    // items.push(item); items = items; // Also works but less idiomatic
  }

  function removeItem(id) {
    items = items.filter(i => i.id !== id);
  }
</script>
```

## Stores

Stores provide shared reactive state that any component can subscribe to. Svelte includes three built-in store types and supports custom stores that implement the store contract (a `subscribe` method).

### Writable Store

```js
// stores/theme.js
import { writable } from 'svelte/store';

export const theme = writable('light');

// Custom methods via a function that returns a store
export function createThemeStore() {
  const { subscribe, set, update } = writable('light');

  return {
    subscribe,
    toggle: () => update(current => current === 'light' ? 'dark' : 'light'),
    setLight: () => set('light'),
    setDark: () => set('dark'),
  };
}

export const themeStore = createThemeStore();
```

### Readable Store

Readable stores are set from outside and cannot be modified by consumers. Use them for values derived from external sources.

```js
import { readable } from 'svelte/store';

export const viewport = readable({ width: 0, height: 0 }, (set) => {
  function update() {
    set({ width: window.innerWidth, height: window.innerHeight });
  }

  update();
  window.addEventListener('resize', update);
  return () => window.removeEventListener('resize', update);
});
```

### Derived Store

Derived stores compute values from one or more other stores.

```js
import { derived } from 'svelte/store';
import { viewport } from './viewport';

export const breakpoint = derived(viewport, ($viewport) => {
  if ($viewport.width < 640) return 'sm';
  if ($viewport.width < 1024) return 'md';
  return 'lg';
});
```

### Auto-Subscription with $

In Svelte components, prefix a store with `$` to auto-subscribe and auto-unsubscribe:

```svelte
<script>
  import { themeStore } from './stores/theme';
</script>

<button on:click={themeStore.toggle}>
  Current: {$themeStore}
</button>
```

## Transitions and Animations

Svelte includes built-in transition directives that handle enter/leave animations declaratively.

### Built-in Transitions

```svelte
<script>
  import { fade, fly, slide, scale, blur } from 'svelte/transition';
  let visible = true;
</script>

<button on:click={() => visible = !visible}>Toggle</button>

{#if visible}
  <div transition:fade={{ duration: 200 }}>Fade in/out</div>
  <div in:fly={{ y: 20, duration: 300 }} out:fade>Fly in, fade out</div>
  <div transition:slide={{ duration: 250 }}>Slide open/close</div>
{/if}
```

### Custom Transitions

```js
function typewriter(node, { speed = 1 }) {
  const text = node.textContent;
  const duration = text.length / (speed * 0.01);

  return {
    duration,
    tick: (t) => {
      const i = Math.trunc(text.length * t);
      node.textContent = text.slice(0, i);
    },
  };
}
```

### Respecting Reduced Motion

```svelte
<script>
  import { fade } from 'svelte/transition';
  import { prefersReducedMotion } from './stores/a11y';

  $: transitionParams = $prefersReducedMotion
    ? { duration: 0 }
    : { duration: 200 };
</script>

{#if visible}
  <div transition:fade={transitionParams}>Content</div>
{/if}
```

### Animate Directive for Lists

```svelte
<script>
  import { flip } from 'svelte/animate';
  import { fade } from 'svelte/transition';
</script>

{#each items as item (item.id)}
  <div animate:flip={{ duration: 300 }} transition:fade>
    {item.name}
  </div>
{/each}
```

## SvelteKit Routing and Loading

SvelteKit is the official framework for building full-stack Svelte applications with file-based routing, server-side rendering, and data loading.

### File-Based Routes

```
src/routes/
  +page.svelte           → /
  +layout.svelte          → layout wrapping all child routes
  about/+page.svelte      → /about
  users/
    +page.svelte          → /users
    [id]/+page.svelte     → /users/:id (dynamic param)
    [id]/+page.server.js  → server-only load function
```

### Load Functions

```js
// src/routes/users/[id]/+page.js
export async function load({ params, fetch }) {
  const res = await fetch(`/api/users/${params.id}`);
  if (!res.ok) throw error(404, 'User not found');

  return {
    user: await res.json(),
  };
}
```

```svelte
<!-- src/routes/users/[id]/+page.svelte -->
<script>
  export let data; // Populated by the load function
</script>

<h1>{data.user.name}</h1>
```

### Layout Data and Shared State

```svelte
<!-- src/routes/+layout.svelte -->
<script>
  import Header from '$lib/components/Header.svelte';
  import Footer from '$lib/components/Footer.svelte';
</script>

<Header />
<main>
  <slot /> <!-- Child routes render here -->
</main>
<Footer />
```

### Error Pages

```svelte
<!-- src/routes/+error.svelte -->
<script>
  import { page } from '$app/stores';
</script>

<h1>{$page.status}</h1>
<p>{$page.error.message}</p>
```

## Actions

Actions are reusable DOM-level behaviors applied via the `use:` directive. They receive the DOM node and optional parameters, and can return an `update` function and a `destroy` cleanup function.

### Click Outside Action

```js
export function clickOutside(node, callback) {
  function handler(event) {
    if (!node.contains(event.target)) callback();
  }

  document.addEventListener('mousedown', handler);

  return {
    destroy() {
      document.removeEventListener('mousedown', handler);
    },
  };
}
```

```svelte
<script>
  import { clickOutside } from './actions/clickOutside';
  let isOpen = false;
</script>

{#if isOpen}
  <div use:clickOutside={() => isOpen = false}>
    Dropdown content
  </div>
{/if}
```

### Focus Trap Action

```js
export function focusTrap(node) {
  const focusable = node.querySelectorAll(
    'a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const first = focusable[0];
  const last = focusable[focusable.length - 1];

  function handleKeydown(e) {
    if (e.key !== 'Tab') return;
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  }

  node.addEventListener('keydown', handleKeydown);
  first?.focus();

  return {
    destroy() {
      node.removeEventListener('keydown', handleKeydown);
    },
  };
}
```

### Tooltip Action

```js
export function tooltip(node, text) {
  let tip;

  function show() {
    tip = document.createElement('div');
    tip.textContent = text;
    tip.className = 'tooltip';
    tip.setAttribute('role', 'tooltip');
    document.body.appendChild(tip);
    const rect = node.getBoundingClientRect();
    tip.style.top = `${rect.bottom + 8}px`;
    tip.style.left = `${rect.left}px`;
  }

  function hide() {
    tip?.remove();
  }

  node.addEventListener('mouseenter', show);
  node.addEventListener('mouseleave', hide);
  node.addEventListener('focus', show);
  node.addEventListener('blur', hide);

  return {
    update(newText) { text = newText; },
    destroy() {
      node.removeEventListener('mouseenter', show);
      node.removeEventListener('mouseleave', hide);
      node.removeEventListener('focus', show);
      node.removeEventListener('blur', hide);
      tip?.remove();
    },
  };
}
```

## Built-in Accessibility Warnings

Svelte's compiler includes accessibility checks that produce warnings at build time. These are not optional suggestions -- they catch real barriers.

### Warnings Svelte Catches

| Warning | What It Catches | Fix |
|---------|----------------|-----|
| `a11y-missing-attribute` | `<img>` without `alt`, `<a>` without `href` | Add the missing attribute |
| `a11y-missing-content` | `<a>` or `<button>` with no text content | Add text or `aria-label` |
| `a11y-click-events-have-key-events` | `on:click` without `on:keydown` on non-interactive elements | Add keyboard handler or use a `<button>` |
| `a11y-no-static-element-interactions` | Event handlers on `<div>`, `<span>` without a role | Add `role` or use a semantic element |
| `a11y-label-has-associated-control` | `<label>` not associated with an input | Use `for` attribute or nest the input |
| `a11y-autofocus` | Use of `autofocus` attribute | Remove or provide justification |
| `a11y-positive-tabindex` | `tabindex` value greater than 0 | Use `tabindex="0"` or `tabindex="-1"` |
| `a11y-no-noninteractive-tabindex` | `tabindex` on a non-interactive element | Remove tabindex or add a role |
| `a11y-media-has-caption` | `<video>` without `<track>` captions | Add a caption track |

### Addressing Warnings

Never suppress accessibility warnings without understanding them. If a warning is a false positive, add a comment explaining why:

```svelte
<!-- svelte-ignore a11y-autofocus -->
<input autofocus />
<!-- Justified: this is a search modal that opens on keyboard shortcut -->
```

## Component Composition

### Slots

```svelte
<!-- Card.svelte -->
<div class="card">
  {#if $$slots.header}
    <div class="card__header">
      <slot name="header" />
    </div>
  {/if}

  <div class="card__body">
    <slot />
  </div>

  {#if $$slots.footer}
    <div class="card__footer">
      <slot name="footer" />
    </div>
  {/if}
</div>
```

### Component Events

```svelte
<!-- Select.svelte -->
<script>
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  export let options = [];
  export let value = null;

  function handleSelect(option) {
    value = option;
    dispatch('change', { value: option });
  }
</script>
```

### Context API

```svelte
<!-- Parent.svelte -->
<script>
  import { setContext } from 'svelte';
  import { writable } from 'svelte/store';

  const activeItem = writable(null);
  setContext('accordion', { activeItem });
</script>

<!-- Child.svelte -->
<script>
  import { getContext } from 'svelte';
  const { activeItem } = getContext('accordion');
</script>
```

## CSS Scoping

Svelte automatically scopes component styles to the component. Styles in a `<style>` block only affect elements in that component's template.

### How Scoping Works

Svelte adds a unique class (e.g., `svelte-1a2b3c`) to both the CSS selectors and the HTML elements at compile time:

```svelte
<style>
  /* Compiled to: p.svelte-1a2b3c { color: red; } */
  p { color: red; }
</style>

<!-- Compiled to: <p class="svelte-1a2b3c">Hello</p> -->
<p>Hello</p>
```

### :global() Escape Hatch

Use `:global()` to target elements outside the component scope. Common for styling slotted content or third-party elements.

```svelte
<style>
  /* Scoped: only affects this component's divs */
  div { padding: 1rem; }

  /* Global: affects all .tooltip elements in the document */
  :global(.tooltip) { z-index: 1000; }

  /* Scoped parent, global child */
  .card :global(a) { color: var(--color-primary); }
</style>
```

### CSS Custom Properties for Component APIs

Expose styling hooks via CSS custom properties, allowing consumers to customize without breaking encapsulation:

```svelte
<style>
  .button {
    background: var(--button-bg, var(--color-primary));
    color: var(--button-color, white);
    padding: var(--button-padding, 0.5rem 1rem);
    border-radius: var(--button-radius, 0.375rem);
  }
</style>

<!-- Consumer can override: -->
<!-- <Button --button-bg="red" --button-radius="0" /> -->
```

## See Also

- [[react-patterns.md]] -- React patterns for cross-framework comparison
- [[vue-patterns.md]] -- Vue Composition API patterns and how they compare to Svelte's reactivity
- [[web-components.md]] -- Integrating Web Components with Svelte applications
- [[../../component-library/references/composition-patterns.md]] -- Framework-agnostic composition patterns
- [[../../accessibility-audit/references/keyboard-nav-guide.md]] -- Keyboard navigation patterns that Svelte actions implement
- [[../../css-architecture/references/css-modules-guide.md]] -- CSS scoping approaches compared to Svelte's built-in scoping

**Back to:** [Frontend Components Skill](../SKILL.md)

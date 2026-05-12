---
name: frontend-components
description: Use when implementing or scaffolding a reusable UI component in React, Vue, Svelte, or Web Components/Lit; when porting a design across frameworks; or when a component needs hooks, composables, reactive state, slots, or shadow-DOM encapsulation.
metadata:
   references:
   - references/react-patterns.md
   - references/svelte-patterns.md
   - references/vue-patterns.md
   - references/web-components.md
---

# Frontend Components

## Framework selection (one-line picker)

| Need | Pick |
|------|------|
| Largest ecosystem, RSC/Next.js | React |
| Low-boilerplate SFCs, Nuxt | Vue |
| Smallest bundle, compiler-driven | Svelte |
| Framework-agnostic / design-system primitive | Web Components (Lit) |

Deep comparison: [react-patterns.md](references/react-patterns.md), [vue-patterns.md](references/vue-patterns.md), [svelte-patterns.md](references/svelte-patterns.md), [web-components.md](references/web-components.md).

## Workflow: build a new component

1. **Define props API** — name, types, required vs optional, default values, controlled-vs-uncontrolled pattern (accept optional `value` + `onChange`).
2. **Render markup** — semantic HTML first, then styling.
3. **Wire state/effects** — local state for ephemeral UI; lift to parent for shared.
4. **Add a11y** — role, aria-*, keyboard handlers, focus management. Verify with axe DevTools.
5. **Write tests** — render, interaction, a11y snapshot.
6. **Document** — Storybook story per variant + states (default, loading, error, disabled).

**Checkpoint after step 4:** run `npx @axe-core/cli http://localhost:6006/iframe?id=<story>` — fail build if any violation.
**Checkpoint after step 5:** branch coverage on the component file must be >= 80% (`vitest run --coverage`).

## Copy-paste templates

### React (controlled input + custom hook + Suspense)

```tsx
import { Suspense, use, useState, useId } from "react";

function useDebounced<T>(value: T, ms = 300): T {
  const [v, setV] = useState(value);
  useEffect(() => { const t = setTimeout(() => setV(value), ms); return () => clearTimeout(t); }, [value, ms]);
  return v;
}

export function SearchBox({ value, onChange, resultsPromise }: {
  value: string; onChange: (s: string) => void; resultsPromise: Promise<string[]>;
}) {
  const id = useId();
  const debounced = useDebounced(value);
  return (
    <div role="search">
      <label htmlFor={id}>Search</label>
      <input id={id} value={value} onChange={(e) => onChange(e.target.value)} aria-describedby={`${id}-hint`} />
      <Suspense fallback={<p>Loading…</p>}>
        <Results promise={resultsPromise} query={debounced} />
      </Suspense>
    </div>
  );
}
function Results({ promise }: { promise: Promise<string[]>; query: string }) {
  const items = use(promise);
  return <ul>{items.map((i) => <li key={i}>{i}</li>)}</ul>;
}
```

### Vue 3 SFC (composable + reactive)

```vue
<script setup lang="ts">
import { ref, computed, watchEffect } from 'vue'
const props = defineProps<{ modelValue: string }>()
const emit = defineEmits<{ 'update:modelValue': [v: string] }>()
const local = ref(props.modelValue)
const length = computed(() => local.value.length)
watchEffect(() => emit('update:modelValue', local.value))
</script>

<template>
  <label class="field">
    <span>Search</span>
    <input v-model="local" :aria-describedby="`hint`" />
    <small id="hint">{{ length }} characters</small>
  </label>
</template>

<style scoped>
.field { display: grid; gap: .25rem; }
</style>
```

### Svelte 5 (runes)

```svelte
<script lang="ts">
  let { value = $bindable(''), onSearch }: { value?: string; onSearch: (q: string) => void } = $props();
  let debounced = $state(value);
  $effect(() => { const t = setTimeout(() => { debounced = value; onSearch(debounced); }, 250); return () => clearTimeout(t); });
</script>

<label>
  Search
  <input bind:value aria-describedby="hint" />
  <small id="hint">{value.length} chars</small>
</label>
```

### Lit Web Component

```ts
import { LitElement, html, css } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';

@customElement('search-box')
export class SearchBox extends LitElement {
  static styles = css`:host{display:block} input{width:100%}`;
  @property() value = '';
  @state() private _count = 0;
  private _onInput(e: Event) {
    this.value = (e.target as HTMLInputElement).value;
    this._count = this.value.length;
    this.dispatchEvent(new CustomEvent('search', { detail: this.value, bubbles: true, composed: true }));
  }
  render() {
    return html`<label>Search<input .value=${this.value} @input=${this._onInput} aria-describedby="h" /><small id="h">${this._count}</small></label>`;
  }
}
```

## Performance gates (run before merge)

- Bundle delta: `npx size-limit` — fail if component adds >5kb gzipped without justification.
- Long lists (>100 rows): use `react-window` / `vue-virtual-scroller` / `svelte-virtual-list`.
- Images: set explicit `width`/`height` or `aspect-ratio`; use `loading="lazy"` below the fold; preload hero with `<link rel="preload" as="image" fetchpriority="high">`.
- Fonts: `font-display: swap` + preload critical WOFF2. Subset to needed glyphs.
- Code-split modal/admin features: `React.lazy`, `defineAsyncComponent`, dynamic `import()`.

## Next Steps

- **[Component Library](../component-library/SKILL.md)**: docs, testing, versioning
- **[CSS Architecture](../css-architecture/SKILL.md)**: styling strategy
- **[Design System Creation](../design-system-creation/SKILL.md)**: tokens + governance
- **[Accessibility Audit](../accessibility-audit/SKILL.md)**: WCAG 2.2 AA
- **[Motion Design](../motion-design/SKILL.md)**: purposeful animation

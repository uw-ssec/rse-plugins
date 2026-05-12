# Vue Patterns

Comprehensive reference for Vue 3 Composition API patterns used in design system implementation. Covers reactive state, composables, provide/inject, scoped slots, Pinia state management, Teleport, transitions, Nuxt integration, and accessibility practices.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Reactive Refs and Computed](#reactive-refs-and-computed) | 14-58 | ref, reactive, computed, and watchEffect for component state |
| [Composables](#composables) | 60-105 | Reusable stateful logic extracted into composable functions |
| [Provide/Inject](#provideinject) | 107-140 | Dependency injection for component trees and design system context |
| [Scoped Slots](#scoped-slots) | 142-170 | Renderless components and slot-based composition |
| [Pinia State Management](#pinia-state-management) | 172-205 | Store patterns for shared UI state |
| [Teleport](#teleport) | 207-225 | Rendering modals, tooltips, and overlays outside the component tree |
| [Transitions and Animations](#transitions-and-animations) | 227-255 | Built-in transition components and transition-group for lists |
| [Nuxt Integration](#nuxt-integration) | 257-280 | Server-side rendering, auto-imports, and Nuxt-specific patterns |
| [Accessibility in Vue](#accessibility-in-vue) | 282-305 | ARIA bindings, focus management, and accessible component patterns |
| [See Also](#see-also) | 307-313 | Related references and skills |

## Reactive Refs and Computed

### ref

`ref` wraps a value in a reactive container. Access the value with `.value` in script; templates unwrap automatically. Use `ref` for primitives and simple values.

```vue
<script setup>
import { ref } from 'vue'

const isOpen = ref(false)
const count = ref(0)

function toggle() {
  isOpen.value = !isOpen.value
}
</script>

<template>
  <button @click="toggle" :aria-expanded="isOpen">
    {{ isOpen ? 'Close' : 'Open' }}
  </button>
  <div v-if="isOpen" role="region">Panel content</div>
</template>
```

### reactive

`reactive` makes an entire object deeply reactive. Use it for complex state objects. Unlike `ref`, you do not need `.value` but you cannot reassign the entire object.

```vue
<script setup>
import { reactive } from 'vue'

const form = reactive({
  name: '',
  email: '',
  errors: {}
})

function validate() {
  form.errors = {}
  if (!form.name) form.errors.name = 'Name is required'
  if (!form.email) form.errors.email = 'Email is required'
}
</script>
```

### computed

`computed` creates derived reactive values. They re-evaluate only when their dependencies change. Use computed for any value derived from reactive state.

```vue
<script setup>
import { ref, computed } from 'vue'

const items = ref([])
const filter = ref('all')

const filteredItems = computed(() => {
  if (filter.value === 'all') return items.value
  return items.value.filter(item => item.status === filter.value)
})

const isEmpty = computed(() => filteredItems.value.length === 0)
</script>
```

### watchEffect and watch

`watchEffect` runs immediately and re-runs when any reactive dependency changes. `watch` watches specific sources and provides old/new values.

```vue
<script setup>
import { ref, watch, watchEffect } from 'vue'

const query = ref('')
const results = ref([])

// watchEffect: runs when query changes, no need to specify dependency
watchEffect(() => {
  document.title = query.value ? `Search: ${query.value}` : 'Search'
})

// watch: explicit source, access to old and new values, supports debounce
watch(query, async (newQuery, oldQuery) => {
  if (newQuery.length < 2) return
  results.value = await fetchResults(newQuery)
}, { debounce: 300 })
</script>
```

## Composables

Composables are the Vue equivalent of React custom hooks. They encapsulate reusable reactive logic in a function that starts with `use`.

### useMediaQuery

```js
import { ref, onMounted, onUnmounted } from 'vue'

export function useMediaQuery(query) {
  const matches = ref(false)
  let mql

  function update(e) {
    matches.value = e.matches
  }

  onMounted(() => {
    mql = window.matchMedia(query)
    matches.value = mql.matches
    mql.addEventListener('change', update)
  })

  onUnmounted(() => {
    mql?.removeEventListener('change', update)
  })

  return matches
}

// Usage: const isMobile = useMediaQuery('(max-width: 768px)')
```

### useClickOutside

```js
import { onMounted, onUnmounted } from 'vue'

export function useClickOutside(elementRef, callback) {
  function handler(event) {
    if (!elementRef.value || elementRef.value.contains(event.target)) return
    callback(event)
  }

  onMounted(() => {
    document.addEventListener('mousedown', handler)
    document.addEventListener('touchstart', handler)
  })

  onUnmounted(() => {
    document.removeEventListener('mousedown', handler)
    document.removeEventListener('touchstart', handler)
  })
}
```

### useLocalStorage

```js
import { ref, watch } from 'vue'

export function useLocalStorage(key, defaultValue) {
  const stored = localStorage.getItem(key)
  const data = ref(stored ? JSON.parse(stored) : defaultValue)

  watch(data, (newValue) => {
    localStorage.setItem(key, JSON.stringify(newValue))
  }, { deep: true })

  return data
}

// Usage: const theme = useLocalStorage('theme', 'light')
```

## Provide/Inject

`provide` and `inject` enable dependency injection across the component tree without prop drilling. This is the foundation for theme providers, design system context, and compound components in Vue.

### Theme Provider

```vue
<!-- ThemeProvider.vue -->
<script setup>
import { provide, ref } from 'vue'

const theme = ref('light')

function toggleTheme() {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
}

provide('theme', { theme, toggleTheme })
</script>

<template>
  <div :data-theme="theme">
    <slot />
  </div>
</template>
```

```vue
<!-- Any descendant component -->
<script setup>
import { inject } from 'vue'

const { theme, toggleTheme } = inject('theme')
</script>
```

### Compound Components with Provide/Inject

```vue
<!-- Tabs.vue -->
<script setup>
import { provide, ref } from 'vue'

const activeTab = ref(props.defaultValue)
provide('tabs', { activeTab, setActiveTab: (val) => activeTab.value = val })
</script>

<template>
  <div role="tablist"><slot /></div>
</template>
```

```vue
<!-- Tab.vue -->
<script setup>
import { inject, computed } from 'vue'

const props = defineProps(['value'])
const { activeTab, setActiveTab } = inject('tabs')
const isActive = computed(() => activeTab.value === props.value)
</script>

<template>
  <button role="tab" :aria-selected="isActive" @click="setActiveTab(value)">
    <slot />
  </button>
</template>
```

## Scoped Slots

Scoped slots pass data from a child component back to the parent's slot content. This enables the renderless component pattern where the child provides logic and the parent provides rendering.

### Renderless Data Fetcher

```vue
<!-- FetchData.vue -->
<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps(['url'])
const data = ref(null)
const error = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await fetch(props.url)
    data.value = await res.json()
  } catch (e) {
    error.value = e
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <slot :data="data" :error="error" :loading="loading" />
</template>
```

```vue
<!-- Usage -->
<FetchData url="/api/users" v-slot="{ data, loading, error }">
  <div v-if="loading">Loading...</div>
  <div v-else-if="error">Error: {{ error.message }}</div>
  <UserList v-else :users="data" />
</FetchData>
```

### Named Slots for Complex Layouts

```vue
<!-- Card.vue -->
<template>
  <div class="card">
    <div class="card__header" v-if="$slots.header">
      <slot name="header" />
    </div>
    <div class="card__body">
      <slot />
    </div>
    <div class="card__footer" v-if="$slots.footer">
      <slot name="footer" />
    </div>
  </div>
</template>
```

## Pinia State Management

Pinia is the official state management library for Vue. Use it for state shared across components that is not suited for provide/inject (global UI state, user preferences, feature flags).

### Defining a Store

```js
import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    mode: 'light',
    accentColor: 'blue',
    fontSize: 'medium',
  }),

  getters: {
    isDark: (state) => state.mode === 'dark',
    cssClass: (state) => `theme-${state.mode} accent-${state.accentColor}`,
  },

  actions: {
    toggleMode() {
      this.mode = this.mode === 'light' ? 'dark' : 'light'
      document.documentElement.setAttribute('data-theme', this.mode)
    },
    setAccentColor(color) {
      this.accentColor = color
    },
  },
})
```

### Composition API Style (Setup Stores)

```js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useNotificationStore = defineStore('notifications', () => {
  const notifications = ref([])

  const unreadCount = computed(() =>
    notifications.value.filter(n => !n.read).length
  )

  function add(notification) {
    notifications.value.push({ ...notification, id: Date.now(), read: false })
  }

  function dismiss(id) {
    notifications.value = notifications.value.filter(n => n.id !== id)
  }

  return { notifications, unreadCount, add, dismiss }
})
```

## Teleport

`<Teleport>` renders component content at a different DOM location. Essential for modals, tooltips, dropdown menus, and toast notifications that need to escape parent overflow/stacking contexts.

```vue
<script setup>
import { ref } from 'vue'

const isOpen = ref(false)
</script>

<template>
  <button @click="isOpen = true">Open Modal</button>

  <Teleport to="body">
    <div v-if="isOpen" class="modal-overlay" @click.self="isOpen = false">
      <div
        class="modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
      >
        <h2 id="modal-title">Modal Title</h2>
        <p>Modal content goes here.</p>
        <button @click="isOpen = false">Close</button>
      </div>
    </div>
  </Teleport>
</template>
```

The `to` prop accepts any CSS selector. Use `to="#modals"` to teleport to a dedicated modal container, keeping all overlays in a predictable DOM location.

## Transitions and Animations

### Single Element Transitions

Vue's `<Transition>` component applies enter/leave classes automatically during element insertion and removal.

```vue
<template>
  <button @click="show = !show">Toggle</button>

  <Transition name="fade">
    <div v-if="show" class="panel">Content</div>
  </Transition>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 200ms ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
```

### TransitionGroup for Lists

```vue
<template>
  <TransitionGroup name="list" tag="ul">
    <li v-for="item in items" :key="item.id">
      {{ item.name }}
    </li>
  </TransitionGroup>
</template>

<style>
.list-enter-active,
.list-leave-active {
  transition: all 300ms ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
.list-move {
  transition: transform 300ms ease;
}
</style>
```

Respect user preferences by wrapping transitions with a reduced-motion check:

```css
@media (prefers-reduced-motion: reduce) {
  .fade-enter-active,
  .fade-leave-active,
  .list-enter-active,
  .list-leave-active {
    transition: none;
  }
}
```

## Nuxt Integration

Nuxt is the standard SSR/SSG framework for Vue. Design system components should work seamlessly in both client-only and Nuxt environments.

### Auto-Imports

Nuxt auto-imports Vue APIs (`ref`, `computed`, `watch`) and composables from the `composables/` directory. Design system packages can register their composables for auto-import via Nuxt modules.

### Server-Side Rendering Considerations

- Components that access `window` or `document` must guard those references or use `<ClientOnly>`:
  ```vue
  <ClientOnly>
    <TooltipProvider />
  </ClientOnly>
  ```
- Use `onMounted` for browser-only setup (DOM measurements, event listeners, localStorage)
- Teleport targets must exist in the SSR HTML; use `<Teleport to="body">` which is always available

### Nuxt Layouts and Pages

```
layouts/
  default.vue     <!-- wraps all pages with header, footer, sidebar -->
pages/
  index.vue       <!-- / route -->
  about.vue       <!-- /about route -->
  users/
    [id].vue      <!-- /users/:id dynamic route -->
```

Design system layout components (Shell, Sidebar, TopBar) map directly to Nuxt layout files, creating a clean separation between structural layout and page content.

## Accessibility in Vue

### Dynamic ARIA Bindings

Vue's attribute binding makes ARIA attributes reactive:

```vue
<template>
  <button
    :aria-expanded="isOpen"
    :aria-controls="panelId"
    @click="toggle"
  >
    {{ label }}
  </button>
  <div
    :id="panelId"
    v-show="isOpen"
    role="region"
    :aria-labelledby="buttonId"
  >
    <slot />
  </div>
</template>
```

### Focus Management

```vue
<script setup>
import { ref, nextTick } from 'vue'

const dialogRef = ref(null)
const isOpen = ref(false)

async function open() {
  isOpen.value = true
  await nextTick()
  dialogRef.value?.focus()
}
</script>
```

`nextTick` is critical for focus management -- the DOM must update before you can focus a newly rendered element.

### Vue-Specific Accessibility Tooling

- **vue-axe**: Development-time accessibility auditing that logs ARIA violations in the console
- **eslint-plugin-vuejs-accessibility**: Linting rules that catch common accessibility mistakes in templates
- **@vue-a11y/announcer**: Composable for managing screen reader announcements in SPAs

## See Also

- [[react-patterns.md]] -- React hooks and patterns for cross-framework comparison
- [[svelte-patterns.md]] -- Svelte reactive patterns and how they compare to Vue's Composition API
- [[web-components.md]] -- Using Web Components in Vue applications
- [[../../component-library/references/composition-patterns.md]] -- Framework-agnostic composition patterns
- [[../../accessibility-audit/references/aria-patterns.md]] -- Complete ARIA widget implementations
- [[../../css-architecture/references/css-modules-guide.md]] -- CSS Modules integration with Vue SFCs

**Back to:** [Frontend Components Skill](../SKILL.md)

## SearchBox SFC (composable + reactive)

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

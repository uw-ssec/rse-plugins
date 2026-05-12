# Composition Patterns

Comprehensive reference for component composition patterns used in design system component libraries. Covers compound components, render props and slots, headless components, the provider pattern, controlled vs uncontrolled components, ref forwarding, and polymorphic components.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Compound Components](#compound-components) | 14-60 | Context-based parent-child component patterns for complex widgets |
| [Render Props and Slots](#render-props-and-slots) | 62-100 | Passing rendering control to consumers via functions or slot templates |
| [Headless Components](#headless-components) | 102-145 | Logic-only components that separate behavior from presentation |
| [Provider Pattern](#provider-pattern) | 147-180 | Context-based state sharing across component trees |
| [Controlled vs Uncontrolled](#controlled-vs-uncontrolled) | 182-215 | State ownership patterns and the hybrid approach |
| [Forwarding Refs](#forwarding-refs) | 217-240 | Passing DOM references through component abstractions |
| [Polymorphic Components](#polymorphic-components) | 242-275 | The "as" prop for rendering different element types |
| [See Also](#see-also) | 277-283 | Related references and skills |

## Compound Components

Compound components are a set of components that work together to form a cohesive unit. The parent manages shared state via context, and children consume that context to coordinate behavior. This pattern is the standard for design system widgets like Tabs, Accordion, Select, and Menu.

### Why Compound Components

The alternative -- a single component with many props -- becomes unwieldy as complexity grows:

```tsx
// Monolithic: hard to extend, hard to customize rendering
<Tabs items={[{ label: "Tab 1", content: <div>Content 1</div> }]} />

// Compound: flexible, composable, consumer controls rendering
<Tabs defaultValue="tab1">
  <TabList>
    <Tab value="tab1">Tab 1</Tab>
    <Tab value="tab2">Tab 2</Tab>
  </TabList>
  <TabPanel value="tab1">Content 1</TabPanel>
  <TabPanel value="tab2">Content 2</TabPanel>
</Tabs>
```

### Implementation Pattern (React)

```tsx
const AccordionContext = createContext(null);

function Accordion({ type = "single", defaultValue, children }) {
  const [openItems, setOpenItems] = useState(
    defaultValue ? [defaultValue] : []
  );

  const toggle = useCallback((value) => {
    setOpenItems((prev) => {
      if (type === "single") return prev.includes(value) ? [] : [value];
      return prev.includes(value)
        ? prev.filter((v) => v !== value)
        : [...prev, value];
    });
  }, [type]);

  return (
    <AccordionContext.Provider value={{ openItems, toggle }}>
      <div role="region">{children}</div>
    </AccordionContext.Provider>
  );
}

function AccordionItem({ value, children }) {
  const { openItems, toggle } = useContext(AccordionContext);
  const isOpen = openItems.includes(value);

  return (
    <div>
      <button
        role="button"
        aria-expanded={isOpen}
        onClick={() => toggle(value)}
      >
        {children}
      </button>
      {isOpen && <div role="region">{children}</div>}
    </div>
  );
}
```

### Implementation Pattern (Vue)

```vue
<!-- Accordion.vue -->
<script setup>
import { provide, ref } from 'vue';

const props = defineProps({ type: { default: 'single' } });
const openItems = ref([]);

function toggle(value) {
  if (props.type === 'single') {
    openItems.value = openItems.value.includes(value) ? [] : [value];
  } else {
    const idx = openItems.value.indexOf(value);
    idx >= 0 ? openItems.value.splice(idx, 1) : openItems.value.push(value);
  }
}

provide('accordion', { openItems, toggle });
</script>

<template><div role="region"><slot /></div></template>
```

## Render Props and Slots

Render props (React) and scoped slots (Vue/Svelte) let parent components expose data to children, giving consumers full control over how that data is rendered.

### React Render Props

```tsx
function Toggle({ defaultOn = false, children }) {
  const [on, setOn] = useState(defaultOn);
  const toggle = () => setOn((prev) => !prev);

  return children({ on, toggle });
}

// Usage
<Toggle>
  {({ on, toggle }) => (
    <button onClick={toggle} aria-pressed={on}>
      {on ? "ON" : "OFF"}
    </button>
  )}
</Toggle>
```

### Vue Scoped Slots

```vue
<!-- Toggle.vue -->
<script setup>
import { ref } from 'vue';
const on = ref(false);
const toggle = () => on.value = !on.value;
</script>

<template>
  <slot :on="on" :toggle="toggle" />
</template>
```

```vue
<!-- Usage -->
<Toggle v-slot="{ on, toggle }">
  <button @click="toggle" :aria-pressed="on">
    {{ on ? 'ON' : 'OFF' }}
  </button>
</Toggle>
```

### When to Use Render Props vs Compound Components

| Scenario | Best Pattern |
|----------|-------------|
| Widget with fixed structure (Tabs, Accordion) | Compound components |
| Logic reuse with flexible rendering | Render props / scoped slots |
| Data fetching abstraction | Render props / scoped slots |
| Form field wrapper | Compound components |

## Headless Components

Headless components provide behavior and state management without any rendered UI. They are the ultimate separation of concerns: the library provides logic and accessibility, the consumer provides all markup and styling.

### Headless Libraries

- **Radix UI** (React): Unstyled, accessible primitives
- **Headless UI** (React, Vue): Tailwind Labs' headless components
- **Ark UI** (React, Vue, Svelte): Framework-agnostic headless components
- **Melt UI** (Svelte): Headless builder API for Svelte

### Headless Component Pattern

```tsx
function useSelect({ items, defaultValue, onChange }) {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedValue, setSelectedValue] = useState(defaultValue);
  const [highlightedIndex, setHighlightedIndex] = useState(0);

  const getToggleProps = () => ({
    role: 'combobox',
    'aria-expanded': isOpen,
    'aria-haspopup': 'listbox',
    onClick: () => setIsOpen(!isOpen),
  });

  const getListProps = () => ({
    role: 'listbox',
    'aria-activedescendant': `option-${highlightedIndex}`,
  });

  const getOptionProps = (index) => ({
    role: 'option',
    id: `option-${index}`,
    'aria-selected': items[index] === selectedValue,
    onClick: () => { setSelectedValue(items[index]); onChange?.(items[index]); setIsOpen(false); },
  });

  return {
    isOpen, selectedValue, highlightedIndex,
    getToggleProps, getListProps, getOptionProps,
  };
}

// Consumer provides all rendering
function CustomSelect({ items }) {
  const { isOpen, selectedValue, getToggleProps, getListProps, getOptionProps } =
    useSelect({ items });

  return (
    <div>
      <button {...getToggleProps()}>{selectedValue || 'Select...'}</button>
      {isOpen && (
        <ul {...getListProps()}>
          {items.map((item, i) => (
            <li key={item} {...getOptionProps(i)}>{item}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

### Benefits and Tradeoffs

| Benefit | Tradeoff |
|---------|----------|
| Complete styling freedom | More consumer code required |
| No style dependencies | Consumer must implement layout |
| Accessibility built in | Learning curve for prop-getter pattern |
| Works with any CSS approach | No visual defaults to start from |

## Provider Pattern

The provider pattern uses framework context to share configuration, state, or services across an entire component tree without prop drilling.

### Design System Provider

```tsx
const DSContext = createContext({
  theme: 'light',
  locale: 'en',
  colorMode: 'light',
});

function DSProvider({ theme = 'light', locale = 'en', children }) {
  const [colorMode, setColorMode] = useState(theme);

  const value = useMemo(() => ({
    theme: colorMode,
    locale,
    colorMode,
    setColorMode,
  }), [colorMode, locale]);

  return (
    <DSContext.Provider value={value}>
      <div data-theme={colorMode} lang={locale}>
        {children}
      </div>
    </DSContext.Provider>
  );
}

function useDS() {
  const context = useContext(DSContext);
  if (!context) throw new Error('useDS must be used within DSProvider');
  return context;
}
```

### Nested Providers

Providers can nest to override values for subtrees:

```tsx
<DSProvider theme="light">
  <Header /> {/* Uses light theme */}
  <DSProvider theme="dark">
    <Sidebar /> {/* Uses dark theme */}
  </DSProvider>
  <Main /> {/* Uses light theme */}
</DSProvider>
```

### Common Provider Uses

| Provider | What It Shares | Consumers |
|----------|---------------|-----------|
| ThemeProvider | Color mode, tokens | All styled components |
| LocaleProvider | Language, direction | Text, date, number formatters |
| ToastProvider | Toast state, dispatch | Toast trigger buttons, toast container |
| ModalProvider | Open/close state, stack | Modal triggers, modal containers |

## Controlled vs Uncontrolled

### Controlled Pattern

The parent owns the state and passes it down. The component is a pure function of its props.

```tsx
function Slider({ value, onChange, min = 0, max = 100 }) {
  return (
    <input
      type="range"
      value={value}
      min={min}
      max={max}
      onChange={(e) => onChange(Number(e.target.value))}
      aria-valuenow={value}
      aria-valuemin={min}
      aria-valuemax={max}
    />
  );
}
```

### Hybrid Pattern (Design System Standard)

```tsx
function useControllableState({ value: controlledValue, defaultValue, onChange }) {
  const [uncontrolledValue, setUncontrolledValue] = useState(defaultValue);
  const isControlled = controlledValue !== undefined;
  const value = isControlled ? controlledValue : uncontrolledValue;

  const setValue = useCallback((next) => {
    const nextValue = typeof next === 'function' ? next(value) : next;
    if (!isControlled) setUncontrolledValue(nextValue);
    onChange?.(nextValue);
  }, [isControlled, value, onChange]);

  return [value, setValue];
}
```

This hook is reusable across every design system component that needs to support both controlled and uncontrolled usage.

## Forwarding Refs

Design system components must forward refs so consumers can access the underlying DOM element for focus management, measurements, and animation libraries.

### React forwardRef

```tsx
const Input = forwardRef(function Input({ label, error, ...props }, ref) {
  const id = useId();
  return (
    <div>
      <label htmlFor={id}>{label}</label>
      <input ref={ref} id={id} aria-invalid={!!error} {...props} />
      {error && <p role="alert">{error}</p>}
    </div>
  );
});
```

### Vue Template Refs

```vue
<script setup>
import { ref } from 'vue';
const inputEl = ref(null);
defineExpose({ focus: () => inputEl.value?.focus() });
</script>

<template>
  <input ref="inputEl" v-bind="$attrs" />
</template>
```

### Svelte bind:this

```svelte
<script>
  let inputEl;
  export function focus() { inputEl?.focus(); }
</script>

<input bind:this={inputEl} {...$$restProps} />
```

## Polymorphic Components

Polymorphic components accept an `as` prop that changes the rendered HTML element while preserving the component's styles and behavior.

### Use Cases

- A `Button` that renders as an `<a>` for navigation links
- A `Box` that renders as any semantic element (`section`, `article`, `nav`)
- A `Text` component that renders as `p`, `span`, `label`, or any text element

### Type-Safe Polymorphic (TypeScript)

```tsx
type PolymorphicProps<C extends React.ElementType, Props = {}> = Props & {
  as?: C;
} & Omit<React.ComponentPropsWithoutRef<C>, keyof Props | 'as'>;

function Box<C extends React.ElementType = 'div'>({
  as,
  className,
  ...props
}: PolymorphicProps<C>) {
  const Component = as || 'div';
  return <Component className={className} {...props} />;
}

// TypeScript validates props based on the "as" element
<Box as="a" href="/about">Link</Box>       // href valid for <a>
<Box as="button" type="submit">Submit</Box> // type valid for <button>
```

### Accessibility Consideration

When using polymorphic components, ensure the rendered element is semantically appropriate. A `Button` rendered as a `<div>` loses keyboard activation and ARIA semantics. If consumers must use non-interactive elements, the component should add `role`, `tabIndex`, and keyboard handlers automatically.

## See Also

- [[variant-systems.md]] -- CVA and variant patterns that compose with these structural patterns
- [[state-management.md]] -- State management for the five UI states that compound components must handle
- [[../../frontend-components/references/react-patterns.md]] -- React-specific implementation of these patterns
- [[../../frontend-components/references/vue-patterns.md]] -- Vue-specific implementation with provide/inject and scoped slots
- [[../../frontend-components/references/svelte-patterns.md]] -- Svelte-specific implementation with context and actions
- [[../../accessibility-audit/references/aria-patterns.md]] -- ARIA patterns that compound components must implement

**Back to:** [Component Library Skill](../SKILL.md)

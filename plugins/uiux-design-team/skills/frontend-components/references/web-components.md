# Web Components

Comprehensive reference for building framework-agnostic components using web standards. Covers Custom Elements API, Shadow DOM encapsulation, Lit framework patterns, declarative Shadow DOM, framework interoperability, cross-framework design systems, and form-associated custom elements.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Custom Elements API](#custom-elements-api) | 14-55 | Defining, registering, and lifecycle of custom elements |
| [Shadow DOM Encapsulation](#shadow-dom-encapsulation) | 57-95 | Style isolation, slots, and the ::part pseudo-element |
| [Lit Framework Patterns](#lit-framework-patterns) | 97-140 | Reactive properties, templates, and decorators in Lit |
| [Declarative Shadow DOM](#declarative-shadow-dom) | 142-165 | Server-rendered Shadow DOM for SSR compatibility |
| [Framework Interoperability](#framework-interoperability) | 167-205 | Using Web Components in React, Vue, and Svelte |
| [Cross-Framework Design Systems](#cross-framework-design-systems) | 207-240 | Architecture for design systems that span multiple frameworks |
| [Form-Associated Custom Elements](#form-associated-custom-elements) | 242-275 | Participating in native form submission and validation |
| [See Also](#see-also) | 277-283 | Related references and skills |

## Custom Elements API

Custom Elements let you define new HTML tags with encapsulated behavior. The browser treats them as first-class elements with lifecycle callbacks, attributes, and properties.

### Defining a Custom Element

```js
class MyButton extends HTMLElement {
  static observedAttributes = ['variant', 'disabled'];

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
    this.shadowRoot.querySelector('button')
      .addEventListener('click', this._handleClick.bind(this));
  }

  disconnectedCallback() {
    // Cleanup: remove event listeners, disconnect observers
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (oldValue !== newValue) this.render();
  }

  _handleClick(event) {
    this.dispatchEvent(new CustomEvent('my-click', {
      bubbles: true,
      composed: true, // Crosses Shadow DOM boundary
      detail: { variant: this.getAttribute('variant') },
    }));
  }

  render() {
    const variant = this.getAttribute('variant') || 'solid';
    const disabled = this.hasAttribute('disabled');
    this.shadowRoot.innerHTML = `
      <style>
        button { /* styles per variant */ }
      </style>
      <button class="${variant}" ${disabled ? 'disabled' : ''}>
        <slot></slot>
      </button>
    `;
  }
}

customElements.define('my-button', MyButton);
```

### Lifecycle Callbacks

| Callback | When It Runs | Common Use |
|----------|-------------|------------|
| `constructor()` | Element created | Attach Shadow DOM, set initial state |
| `connectedCallback()` | Added to the document | Render, add event listeners, fetch data |
| `disconnectedCallback()` | Removed from the document | Cleanup listeners, cancel timers |
| `attributeChangedCallback()` | Observed attribute changes | Re-render, update internal state |
| `adoptedCallback()` | Moved to a new document | Rare; update document-specific references |

Only attributes listed in the static `observedAttributes` array trigger `attributeChangedCallback`.

## Shadow DOM Encapsulation

Shadow DOM creates an isolated DOM subtree with its own scope for styles. Styles defined inside the Shadow DOM do not leak out, and external styles do not leak in (with controlled exceptions).

### Creating Shadow DOM

```js
constructor() {
  super();
  const shadow = this.attachShadow({ mode: 'open' });
  // mode: 'open' allows external access via element.shadowRoot
  // mode: 'closed' prevents external access (rarely needed)
}
```

### Slots for Content Projection

Slots allow consumers to inject content into predefined locations within the Shadow DOM:

```html
<!-- Component template (inside Shadow DOM) -->
<div class="card">
  <div class="card-header">
    <slot name="header">Default Header</slot>
  </div>
  <div class="card-body">
    <slot></slot> <!-- Default slot -->
  </div>
</div>

<!-- Consumer usage -->
<my-card>
  <span slot="header">Custom Title</span>
  <p>Body content goes in the default slot.</p>
</my-card>
```

### Styling the Host Element

```css
/* Inside Shadow DOM styles */
:host {
  display: block;
  font-family: var(--font-body, sans-serif);
}

:host([variant="outlined"]) {
  border: 2px solid var(--color-primary);
}

:host(:hover) {
  background: var(--color-surface-hover);
}
```

### The ::part Pseudo-Element

`::part` allows external CSS to style specifically exposed internal elements:

```js
// Inside the Shadow DOM template
`<button part="button trigger"><slot></slot></button>`
```

```css
/* External CSS */
my-dropdown::part(trigger) {
  background: var(--color-primary);
  color: white;
}
```

### CSS Custom Properties Cross Boundaries

CSS custom properties (unlike regular CSS) inherit through Shadow DOM boundaries. This is the primary theming mechanism for Web Components:

```css
/* External theme */
:root {
  --color-primary: #3b82f6;
  --font-body: 'Inter', sans-serif;
}

/* Inside Shadow DOM -- inherits from :root */
button {
  background: var(--color-primary);
  font-family: var(--font-body);
}
```

## Lit Framework Patterns

Lit is a lightweight library (5kb) that adds reactive properties, declarative templates, and lifecycle management on top of Web Components. It produces standard custom elements with less boilerplate.

### Basic Lit Component

```js
import { LitElement, html, css } from 'lit';

class LitButton extends LitElement {
  static properties = {
    variant: { type: String, reflect: true },
    disabled: { type: Boolean, reflect: true },
    loading: { type: Boolean },
  };

  static styles = css`
    :host { display: inline-flex; }
    button {
      padding: var(--button-padding, 0.5rem 1rem);
      border-radius: var(--button-radius, 0.375rem);
      font-family: inherit;
      cursor: pointer;
    }
    button[disabled] { opacity: 0.5; cursor: not-allowed; }
    :host([variant="solid"]) button {
      background: var(--color-primary);
      color: white;
      border: none;
    }
    :host([variant="outline"]) button {
      background: transparent;
      color: var(--color-primary);
      border: 2px solid var(--color-primary);
    }
  `;

  constructor() {
    super();
    this.variant = 'solid';
    this.disabled = false;
    this.loading = false;
  }

  render() {
    return html`
      <button ?disabled=${this.disabled || this.loading} part="button">
        ${this.loading ? html`<span class="spinner"></span>` : ''}
        <slot></slot>
      </button>
    `;
  }
}

customElements.define('lit-button', LitButton);
```

### Reactive Properties

Lit properties automatically trigger re-renders when their values change. The `reflect: true` option syncs the property to an HTML attribute, making it styleable with CSS attribute selectors.

### Lit Directives

```js
import { classMap } from 'lit/directives/class-map.js';
import { styleMap } from 'lit/directives/style-map.js';
import { ifDefined } from 'lit/directives/if-defined.js';

render() {
  const classes = { active: this.isActive, disabled: this.disabled };
  const styles = { width: this.width ? `${this.width}px` : undefined };

  return html`
    <div class=${classMap(classes)} style=${styleMap(styles)}>
      <a href=${ifDefined(this.href)}><slot></slot></a>
    </div>
  `;
}
```

## Declarative Shadow DOM

Declarative Shadow DOM allows Shadow DOM to be expressed in HTML, enabling server-side rendering of Web Components without JavaScript hydration for the initial paint.

```html
<my-card>
  <template shadowrootmode="open">
    <style>
      .card { padding: var(--space-md); border-radius: var(--radius-md); }
    </style>
    <div class="card">
      <slot name="header"></slot>
      <slot></slot>
    </div>
  </template>
  <h2 slot="header">Server-Rendered Title</h2>
  <p>This content is visible before JavaScript loads.</p>
</my-card>
```

### Benefits for SSR

- Content is visible on first paint without waiting for JavaScript
- Search engines can index Shadow DOM content
- Progressive enhancement: interactivity loads after initial render
- Works with streaming SSR frameworks

### Hydration

When the component's JavaScript loads, it detects the existing declarative Shadow DOM and adopts it rather than creating a new shadow root. Lit handles this automatically with its SSR package `@lit-labs/ssr`.

## Framework Interoperability

Web Components work in any framework, but each framework has quirks around property vs attribute binding, event handling, and typing.

### Web Components in React

React has historically had poor Web Component support, but React 19+ improves it significantly. For older React versions, use a wrapper.

```tsx
// React 19+ -- properties and events work natively
function App() {
  return (
    <my-button
      variant="solid"
      onMyClick={(e) => console.log(e.detail)}
    >
      Click me
    </my-button>
  );
}

// React 18 and earlier -- use a ref for properties and events
function App() {
  const buttonRef = useRef(null);

  useEffect(() => {
    const el = buttonRef.current;
    const handler = (e) => console.log(e.detail);
    el.addEventListener('my-click', handler);
    return () => el.removeEventListener('my-click', handler);
  }, []);

  return <my-button ref={buttonRef} variant="solid">Click me</my-button>;
}
```

### Web Components in Vue

Vue handles Web Components well out of the box. Configure the compiler to recognize custom elements:

```js
// vite.config.js
export default {
  plugins: [
    vue({
      template: {
        compilerOptions: {
          isCustomElement: (tag) => tag.startsWith('my-'),
        },
      },
    }),
  ],
};
```

```vue
<template>
  <my-button
    :variant="variant"
    @my-click="handleClick"
  >
    Click me
  </my-button>
</template>
```

### Web Components in Svelte

Svelte treats Web Components as native HTML elements. Properties bind with standard syntax:

```svelte
<my-button
  variant="solid"
  on:my-click={handleClick}
>
  Click me
</my-button>
```

## Cross-Framework Design Systems

Web Components enable design systems that work across multiple frameworks. This is valuable for organizations with React, Vue, and Svelte teams sharing a common component library.

### Architecture

```
design-tokens/          (framework-agnostic, CSS custom properties)
  tokens.css
  tokens.json

web-components/         (Lit-based core components)
  src/
    button.ts
    input.ts
    modal.ts
  dist/
    index.js            (ES module bundle)
    index.css           (shared styles)

react-wrappers/         (thin React wrappers for type safety and DX)
  src/
    Button.tsx
    Input.tsx

vue-wrappers/           (thin Vue wrappers)
  src/
    Button.vue
    Input.vue
```

### Wrapper Pattern

Framework wrappers provide native DX (TypeScript types, framework-specific events, IDE autocompletion) while delegating rendering to the Web Component:

```tsx
// react-wrappers/Button.tsx
import { createComponent } from '@lit/react';
import { LitButton } from '@myds/web-components';

export const Button = createComponent({
  tagName: 'lit-button',
  elementClass: LitButton,
  react: React,
  events: {
    onClick: 'my-click',
  },
});
```

### Token Sharing

Design tokens defined as CSS custom properties are consumed identically by Web Components and any framework, creating a single source of truth for visual consistency.

## Form-Associated Custom Elements

Form-associated custom elements participate in native HTML forms: they submit values, support validation, and work with the constraint validation API.

### Implementing Form Association

```js
class MyInput extends HTMLElement {
  static formAssociated = true;

  constructor() {
    super();
    this._internals = this.attachInternals();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.shadowRoot.innerHTML = `
      <input type="text" part="input" />
    `;
    const input = this.shadowRoot.querySelector('input');
    input.addEventListener('input', (e) => {
      this._internals.setFormValue(e.target.value);
      this.validate(e.target.value);
    });
  }

  validate(value) {
    if (this.hasAttribute('required') && !value) {
      this._internals.setValidity(
        { valueMissing: true },
        'This field is required',
        this.shadowRoot.querySelector('input')
      );
    } else {
      this._internals.setValidity({});
    }
  }

  // Form lifecycle callbacks
  formResetCallback() {
    this.shadowRoot.querySelector('input').value = '';
    this._internals.setFormValue('');
  }

  formStateRestoreCallback(state) {
    this.shadowRoot.querySelector('input').value = state;
    this._internals.setFormValue(state);
  }
}

customElements.define('my-input', MyInput);
```

### Usage in a Form

```html
<form id="my-form">
  <label for="username">Username</label>
  <my-input name="username" id="username" required></my-input>

  <button type="submit">Submit</button>
</form>

<script>
  document.getElementById('my-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const data = new FormData(e.target);
    console.log(data.get('username')); // Value from the custom element
  });
</script>
```

The `ElementInternals` API provides access to form state, validation, and accessibility features that were previously exclusive to built-in form elements.

## See Also

- [[react-patterns.md]] -- React-specific patterns and using Web Components in React applications
- [[vue-patterns.md]] -- Vue integration with Web Components
- [[svelte-patterns.md]] -- Svelte integration with Web Components
- [[../../design-system-creation/references/token-architecture.md]] -- Token architecture that Web Components consume via CSS custom properties
- [[../../css-architecture/references/css-in-js-patterns.md]] -- Comparing Shadow DOM encapsulation with CSS-in-JS approaches
- [[../../accessibility-audit/references/aria-patterns.md]] -- ARIA patterns for building accessible custom elements

**Back to:** [Frontend Components Skill](../SKILL.md)

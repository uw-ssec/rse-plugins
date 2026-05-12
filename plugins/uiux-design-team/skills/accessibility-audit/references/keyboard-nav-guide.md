# Keyboard Navigation Guide

Comprehensive reference for keyboard navigation implementation. Covers focus management fundamentals, tab order optimization, roving tabindex pattern, focus trapping for modals, skip navigation links, keyboard interaction patterns by component type, and focus-visible styling.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Focus Management Fundamentals](#focus-management-fundamentals) | 14-45 | What receives focus, tabindex values, and programmatic focus |
| [Tab Order Optimization](#tab-order-optimization) | 47-75 | Logical focus order, DOM order, and common pitfalls |
| [Roving Tabindex](#roving-tabindex) | 77-115 | Arrow-key navigation within composite widgets |
| [Focus Trapping](#focus-trapping) | 117-150 | Containing focus within modals, drawers, and dialogs |
| [Skip Navigation Links](#skip-navigation-links) | 152-175 | Bypassing repeated content for keyboard users |
| [Keyboard Interaction Patterns](#keyboard-interaction-patterns) | 177-225 | Expected key bindings for each component type |
| [Focus-Visible Styling](#focus-visible-styling) | 227-260 | Visible focus indicators that do not affect mouse users |
| [See Also](#see-also) | 262-268 | Related references and skills |

## Focus Management Fundamentals

### What Receives Focus

Only interactive elements receive keyboard focus by default: `<a href>`, `<button>`, `<input>`, `<select>`, `<textarea>`, and elements with `tabindex`. Non-interactive elements (`<div>`, `<span>`, `<p>`) do not receive focus unless given `tabindex`.

### tabindex Values

| Value | Behavior | When to Use |
|-------|----------|-------------|
| `tabindex="0"` | Adds element to natural tab order | Custom interactive elements (div-as-button, custom widgets) |
| `tabindex="-1"` | Focusable via JavaScript but not in tab order | Programmatic focus targets (dialogs, skip-link destinations) |
| `tabindex="1+"` | Forced priority in tab order | **Never use** -- creates unpredictable navigation |

### Programmatic Focus

Move focus programmatically when context changes: opening modals, navigating between views, or displaying dynamic content.

```js
// Move focus to an element
element.focus();

// Move focus with scroll prevention
element.focus({ preventScroll: true });

// Ensure the element can receive focus
element.setAttribute('tabindex', '-1');
element.focus();
```

### Focus vs Activation

Focus (where the keyboard cursor is) and activation (performing an action) are separate concepts:

- **Tab/Shift+Tab**: Move focus between elements
- **Enter**: Activate links and buttons
- **Space**: Activate buttons, toggle checkboxes, scroll page
- **Arrow keys**: Navigate within composite widgets (tabs, menus, listboxes)

## Tab Order Optimization

### Logical Focus Order

Tab order should match the visual reading order. Users expect focus to move left-to-right, top-to-bottom (in LTR languages), following the visual layout.

**Correct**: Focus moves through header navigation, then main content, then sidebar, then footer.

**Incorrect**: Focus jumps from header to footer, then back to sidebar, then to main content.

### DOM Order Is Tab Order

The simplest way to ensure correct tab order is to make the DOM order match the visual order. CSS can rearrange visual presentation without changing DOM order, but this creates a mismatch between what users see and what keyboards navigate.

**Dangerous CSS properties** that create tab order mismatches:
- `order` (flexbox/grid)
- `position: absolute/fixed` with visual reordering
- `float` changing visual flow
- CSS Grid explicit row/column placement

### Audit Technique

Tab through the entire page with the keyboard. If focus ever jumps to an unexpected location, the DOM order does not match the visual order. Fix the DOM order rather than using `tabindex` values to compensate.

### Grouping Related Controls

Related controls should be adjacent in tab order. Use `<fieldset>` and `<legend>` for form groups. Use `role="group"` with `aria-labelledby` for non-form groups.

```html
<fieldset>
  <legend>Notification preferences</legend>
  <label><input type="checkbox" /> Email</label>
  <label><input type="checkbox" /> SMS</label>
  <label><input type="checkbox" /> Push</label>
</fieldset>
```

## Roving Tabindex

Roving tabindex is the standard pattern for keyboard navigation within composite widgets: tablists, toolbars, menubars, and listboxes. Only one item in the group has `tabindex="0"` (the active item); all others have `tabindex="-1"`. Arrow keys move the active item.

### How It Works

1. The composite widget has one item with `tabindex="0"` (the current/active item)
2. All other items have `tabindex="-1"` (focusable via JS but not in tab order)
3. **Tab** moves focus into the widget (to the `tabindex="0"` item) and out of it
4. **Arrow keys** move focus between items within the widget, updating `tabindex` values

### Implementation

```js
function rovingTabindex(container, selector, direction = 'horizontal') {
  const items = Array.from(container.querySelectorAll(selector));
  let currentIndex = items.findIndex(item => item.tabIndex === 0);
  if (currentIndex === -1) currentIndex = 0;

  // Initialize: only the current item is in tab order
  items.forEach((item, i) => {
    item.tabIndex = i === currentIndex ? 0 : -1;
  });

  container.addEventListener('keydown', (e) => {
    const prev = direction === 'horizontal' ? 'ArrowLeft' : 'ArrowUp';
    const next = direction === 'horizontal' ? 'ArrowRight' : 'ArrowDown';

    let newIndex = currentIndex;

    if (e.key === next) {
      newIndex = (currentIndex + 1) % items.length;
    } else if (e.key === prev) {
      newIndex = (currentIndex - 1 + items.length) % items.length;
    } else if (e.key === 'Home') {
      newIndex = 0;
    } else if (e.key === 'End') {
      newIndex = items.length - 1;
    } else {
      return; // Not a navigation key
    }

    e.preventDefault();
    items[currentIndex].tabIndex = -1;
    items[newIndex].tabIndex = 0;
    items[newIndex].focus();
    currentIndex = newIndex;
  });
}
```

### Which Components Use Roving Tabindex

| Component | Direction | Keys |
|-----------|-----------|------|
| Tabs (horizontal) | Horizontal | Arrow Left/Right |
| Tabs (vertical) | Vertical | Arrow Up/Down |
| Toolbar | Horizontal | Arrow Left/Right |
| Menubar | Horizontal | Arrow Left/Right |
| Radio group | Either | Arrow keys |
| Tree view | Vertical | Arrow Up/Down, Left/Right for expand |
| Listbox | Vertical | Arrow Up/Down |

## Focus Trapping

Focus trapping confines Tab navigation within a specific container, preventing focus from leaving. This is required for modal dialogs, drawers, and any overlay that obscures the main content.

### Implementation

```js
function trapFocus(container) {
  const focusable = container.querySelectorAll(
    'a[href], button:not([disabled]), input:not([disabled]), ' +
    'select:not([disabled]), textarea:not([disabled]), ' +
    '[tabindex]:not([tabindex="-1"])'
  );
  const first = focusable[0];
  const last = focusable[focusable.length - 1];

  function handleKeydown(e) {
    if (e.key !== 'Tab') return;

    if (e.shiftKey) {
      if (document.activeElement === first) {
        e.preventDefault();
        last.focus();
      }
    } else {
      if (document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }
  }

  container.addEventListener('keydown', handleKeydown);
  first?.focus();

  return () => container.removeEventListener('keydown', handleKeydown);
}
```

### Focus Trap Rules

1. **On open**: Move focus into the trapped container (first focusable element or the container itself)
2. **During**: Tab cycles within the container; Shift+Tab cycles in reverse
3. **On Escape**: Close the overlay and release the trap
4. **On close**: Return focus to the element that triggered the overlay

### The inert Attribute

The `inert` attribute provides a declarative way to make background content non-interactive while a modal is open:

```html
<div id="app" inert>
  <!-- All content behind the modal is non-interactive -->
</div>
<div role="dialog" aria-modal="true">
  <!-- Modal content: the only interactive area -->
</div>
```

`inert` removes elements from the tab order, makes them invisible to screen readers, and prevents click interactions -- all in one attribute.

## Skip Navigation Links

Skip links allow keyboard users to bypass repeated navigation blocks and jump directly to the main content. They are required by WCAG 2.4.1.

### Implementation

```html
<body>
  <a href="#main-content" class="skip-link">Skip to main content</a>
  <nav><!-- 20+ navigation items --></nav>
  <main id="main-content" tabindex="-1">
    <!-- Main page content -->
  </main>
</body>
```

```css
.skip-link {
  position: absolute;
  left: -9999px;
  top: auto;
  width: 1px;
  height: 1px;
  overflow: hidden;
}

.skip-link:focus {
  position: fixed;
  top: 0;
  left: 0;
  width: auto;
  height: auto;
  padding: 0.75rem 1.5rem;
  background: var(--color-primary);
  color: white;
  z-index: 10000;
  font-size: var(--text-base);
}
```

### Multiple Skip Links

For complex layouts, offer multiple skip targets:

```html
<a href="#main-content" class="skip-link">Skip to main content</a>
<a href="#search" class="skip-link">Skip to search</a>
<a href="#footer-nav" class="skip-link">Skip to footer</a>
```

## Keyboard Interaction Patterns

### Button

| Key | Action |
|-----|--------|
| Enter | Activate the button |
| Space | Activate the button |

### Link

| Key | Action |
|-----|--------|
| Enter | Follow the link |

### Checkbox

| Key | Action |
|-----|--------|
| Space | Toggle checked state |

### Radio Button Group

| Key | Action |
|-----|--------|
| Arrow Down/Right | Select next radio button |
| Arrow Up/Left | Select previous radio button |
| Space | Select the focused radio button |

### Select / Dropdown

| Key | Action |
|-----|--------|
| Enter/Space | Open dropdown |
| Arrow Down | Move to next option |
| Arrow Up | Move to previous option |
| Home | Move to first option |
| End | Move to last option |
| Escape | Close dropdown |
| Type character | Jump to option starting with that character |

### Modal Dialog

| Key | Action |
|-----|--------|
| Tab | Cycle forward through focusable elements (trapped) |
| Shift+Tab | Cycle backward (trapped) |
| Escape | Close dialog, return focus to trigger |

### Slider

| Key | Action |
|-----|--------|
| Arrow Right/Up | Increase value by one step |
| Arrow Left/Down | Decrease value by one step |
| Page Up | Increase by larger step |
| Page Down | Decrease by larger step |
| Home | Set to minimum value |
| End | Set to maximum value |

## Focus-Visible Styling

### The :focus-visible Pseudo-Class

`:focus-visible` applies focus styles only when the browser determines the user is navigating via keyboard (not mouse). This provides visible focus rings for keyboard users without affecting mouse users.

```css
/* Remove default outline */
:focus {
  outline: none;
}

/* Add custom focus ring for keyboard navigation only */
:focus-visible {
  outline: 2px solid var(--color-focus, #2563eb);
  outline-offset: 2px;
  border-radius: inherit;
}
```

### Focus Ring Design Guidelines

- **Width**: Minimum 2px (3px recommended for better visibility)
- **Color**: High contrast against all backgrounds; use a consistent focus color
- **Offset**: 2px offset prevents the ring from overlapping the element border
- **Shape**: Follow the element's border-radius

### Per-Component Focus Styles

```css
/* Buttons: outline ring */
button:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

/* Inputs: ring replaces or enhances border */
input:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: -1px;
  border-color: var(--color-focus);
}

/* Cards and containers: ring around the full element */
.card:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

/* Dark backgrounds: ensure contrast */
.dark-section :focus-visible {
  outline-color: var(--color-focus-on-dark, #93c5fd);
}
```

### Testing Focus Visibility

Use Tab to navigate through the interface. Every interactive element must show a clearly visible focus indicator. Check on both light and dark backgrounds. The focus ring must meet 3:1 contrast ratio against adjacent colors (WCAG 2.4.11).

## See Also

- [[wcag-checklist.md]] -- WCAG criteria for keyboard accessibility (2.1.1, 2.1.2, 2.4.3, 2.4.7)
- [[aria-patterns.md]] -- ARIA widget patterns with their expected keyboard interactions
- [[contrast-guide.md]] -- Contrast requirements for focus indicators
- [[../../frontend-components/references/react-patterns.md]] -- React focus management with useRef and useEffect
- [[../../frontend-components/references/svelte-patterns.md]] -- Svelte actions for focus trapping and keyboard handling
- [[../../component-library/references/composition-patterns.md]] -- Component patterns that implement keyboard navigation

**Back to:** [Accessibility Audit Skill](../SKILL.md)

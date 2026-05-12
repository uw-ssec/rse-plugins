# ARIA Patterns

Correct ARIA implementation for common interactive widgets. Each pattern includes the required roles, properties, states, keyboard interactions, and complete HTML code examples following WAI-ARIA Authoring Practices.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Dialog / Modal](#dialog--modal) | 14-50 | Modal dialog with focus trap and screen reader announcements |
| [Tabs](#tabs) | 52-90 | Tablist, tab, and tabpanel with keyboard navigation |
| [Accordion](#accordion) | 92-125 | Collapsible sections with proper state management |
| [Combobox / Autocomplete](#combobox--autocomplete) | 127-165 | Text input with filtered suggestions listbox |
| [Menu / Menubar](#menu--menubar) | 167-200 | Application menus with keyboard navigation |
| [Tooltip](#tooltip) | 202-225 | Supplementary information on hover and focus |
| [Tree View](#tree-view) | 227-255 | Hierarchical list with expand/collapse |
| [Alert and Live Regions](#alert-and-live-regions) | 257-285 | Dynamic content announcements without focus change |
| [See Also](#see-also) | 287-293 | Related references and skills |

## Dialog / Modal

### Required ARIA

| Attribute | Element | Purpose |
|-----------|---------|---------|
| `role="dialog"` | Container | Identifies the dialog |
| `aria-modal="true"` | Container | Indicates background is inert |
| `aria-labelledby` | Container | Points to the dialog title |
| `aria-describedby` | Container | Points to dialog description (optional) |

### Keyboard Behavior

- **Tab**: Cycles through focusable elements within the dialog (focus trap)
- **Shift+Tab**: Reverse cycles through focusable elements
- **Escape**: Closes the dialog and returns focus to the trigger element

### Code Example

```html
<button id="open-dialog" aria-haspopup="dialog">Open Settings</button>

<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  aria-describedby="dialog-desc"
  tabindex="-1"
>
  <h2 id="dialog-title">Settings</h2>
  <p id="dialog-desc">Configure your notification preferences.</p>

  <form>
    <label for="email-notifications">Email notifications</label>
    <input type="checkbox" id="email-notifications" />

    <div class="dialog-actions">
      <button type="button" id="close-dialog">Cancel</button>
      <button type="submit">Save</button>
    </div>
  </form>
</div>
```

### Implementation Notes

- Set `tabindex="-1"` on the dialog container so it can receive programmatic focus
- On open: move focus to the first focusable element or the dialog itself
- On close: return focus to the element that triggered the dialog
- Trap focus by intercepting Tab on the last element and Shift+Tab on the first

## Tabs

### Required ARIA

| Attribute | Element | Purpose |
|-----------|---------|---------|
| `role="tablist"` | Container | Groups the tabs |
| `role="tab"` | Each tab | Identifies a tab |
| `role="tabpanel"` | Content area | Identifies the tab's content |
| `aria-selected="true/false"` | Each tab | Indicates the active tab |
| `aria-controls` | Each tab | Points to its tabpanel ID |
| `aria-labelledby` | Each tabpanel | Points to its tab ID |

### Keyboard Behavior

- **Arrow Right/Left**: Moves focus between tabs (horizontal tabs)
- **Arrow Down/Up**: Moves focus between tabs (vertical tabs)
- **Home**: Moves focus to the first tab
- **End**: Moves focus to the last tab
- **Enter/Space**: Activates the focused tab (if using manual activation)

### Code Example

```html
<div role="tablist" aria-label="Account settings">
  <button role="tab" id="tab-1" aria-selected="true" aria-controls="panel-1" tabindex="0">
    Profile
  </button>
  <button role="tab" id="tab-2" aria-selected="false" aria-controls="panel-2" tabindex="-1">
    Security
  </button>
  <button role="tab" id="tab-3" aria-selected="false" aria-controls="panel-3" tabindex="-1">
    Notifications
  </button>
</div>

<div role="tabpanel" id="panel-1" aria-labelledby="tab-1" tabindex="0">
  <h3>Profile Settings</h3>
  <!-- Panel content -->
</div>

<div role="tabpanel" id="panel-2" aria-labelledby="tab-2" tabindex="0" hidden>
  <h3>Security Settings</h3>
  <!-- Panel content -->
</div>
```

### Implementation Notes

- Use roving tabindex: active tab has `tabindex="0"`, inactive tabs have `tabindex="-1"`
- Arrow keys move between tabs; Tab moves focus out of the tablist and into the active panel
- Automatic activation (focus = select) provides faster navigation than manual activation

## Accordion

### Required ARIA

| Attribute | Element | Purpose |
|-----------|---------|---------|
| `aria-expanded="true/false"` | Trigger button | Indicates open/closed state |
| `aria-controls` | Trigger button | Points to the collapsible content ID |
| `role="region"` | Content area | Identifies the expandable content |
| `aria-labelledby` | Content area | Points to the trigger button ID |

### Code Example

```html
<div class="accordion">
  <h3>
    <button
      id="acc-trigger-1"
      aria-expanded="true"
      aria-controls="acc-panel-1"
    >
      Shipping Information
    </button>
  </h3>
  <div
    id="acc-panel-1"
    role="region"
    aria-labelledby="acc-trigger-1"
  >
    <p>We ship to all 50 states. Standard shipping takes 5-7 business days.</p>
  </div>

  <h3>
    <button
      id="acc-trigger-2"
      aria-expanded="false"
      aria-controls="acc-panel-2"
    >
      Return Policy
    </button>
  </h3>
  <div
    id="acc-panel-2"
    role="region"
    aria-labelledby="acc-trigger-2"
    hidden
  >
    <p>Returns accepted within 30 days of purchase.</p>
  </div>
</div>
```

### Keyboard Behavior

- **Enter/Space**: Toggle the focused accordion section
- **Arrow Down**: Move focus to the next accordion header
- **Arrow Up**: Move focus to the previous accordion header
- **Home**: Move focus to the first accordion header
- **End**: Move focus to the last accordion header

## Combobox / Autocomplete

### Required ARIA

| Attribute | Element | Purpose |
|-----------|---------|---------|
| `role="combobox"` | Input | Identifies the combobox pattern |
| `aria-expanded="true/false"` | Input | Indicates whether the listbox is visible |
| `aria-controls` | Input | Points to the listbox ID |
| `aria-activedescendant` | Input | Points to the currently highlighted option |
| `role="listbox"` | Suggestion list | Identifies the list of options |
| `role="option"` | Each suggestion | Identifies an option |
| `aria-selected` | Each option | Indicates the selected option |

### Code Example

```html
<label for="city-input">City</label>
<div class="combobox-wrapper">
  <input
    type="text"
    id="city-input"
    role="combobox"
    aria-expanded="true"
    aria-controls="city-listbox"
    aria-activedescendant="city-option-2"
    aria-autocomplete="list"
    autocomplete="off"
  />
  <ul id="city-listbox" role="listbox" aria-label="Cities">
    <li id="city-option-1" role="option">Austin</li>
    <li id="city-option-2" role="option" aria-selected="true">Boston</li>
    <li id="city-option-3" role="option">Chicago</li>
  </ul>
</div>

<div aria-live="polite" class="sr-only">3 suggestions available</div>
```

### Keyboard Behavior

- **Arrow Down**: Open listbox (if closed), move highlight to next option
- **Arrow Up**: Move highlight to previous option
- **Enter**: Select the highlighted option
- **Escape**: Close the listbox, clear input (or revert to selected value)
- **Typing**: Filters the listbox options

## Menu / Menubar

### Required ARIA

| Attribute | Element | Purpose |
|-----------|---------|---------|
| `role="menubar"` | Top-level container | Horizontal menu bar |
| `role="menu"` | Submenu container | Dropdown menu |
| `role="menuitem"` | Each item | Menu item |
| `role="menuitemcheckbox"` | Toggleable item | Checkable menu item |
| `role="menuitemradio"` | Radio-like item | Radio menu item |
| `aria-haspopup="menu"` | Parent item | Indicates it opens a submenu |
| `aria-expanded` | Parent item | Indicates submenu is open/closed |

### Code Example

```html
<nav aria-label="Application">
  <ul role="menubar">
    <li role="none">
      <button role="menuitem" aria-haspopup="menu" aria-expanded="false">
        File
      </button>
      <ul role="menu" aria-label="File">
        <li role="none"><button role="menuitem">New</button></li>
        <li role="none"><button role="menuitem">Open</button></li>
        <li role="none"><hr role="separator" /></li>
        <li role="none"><button role="menuitem">Save</button></li>
      </ul>
    </li>
    <li role="none">
      <button role="menuitem" aria-haspopup="menu" aria-expanded="false">
        Edit
      </button>
      <!-- Edit submenu -->
    </li>
  </ul>
</nav>
```

### Keyboard Behavior

- **Arrow Right/Left**: Navigate between menubar items
- **Arrow Down**: Open submenu, move to first item
- **Arrow Up**: Move to previous submenu item
- **Enter/Space**: Activate the focused menu item
- **Escape**: Close the current submenu, return focus to parent

## Tooltip

### Required ARIA

| Attribute | Element | Purpose |
|-----------|---------|---------|
| `role="tooltip"` | Tooltip element | Identifies the tooltip |
| `aria-describedby` | Trigger element | Points to the tooltip ID |

### Code Example

```html
<button aria-describedby="tooltip-1">
  <svg aria-hidden="true"><!-- info icon --></svg>
  Settings
</button>

<div id="tooltip-1" role="tooltip" class="tooltip">
  Configure your account preferences and notification settings.
</div>
```

### Behavior Rules

- Show on hover AND focus (both mouse and keyboard users must access it)
- Keep visible when the user moves the pointer to the tooltip content
- Dismiss with Escape key
- Do not put interactive content (links, buttons) inside tooltips -- use a popover instead
- Tooltip text must not repeat the trigger's accessible name

### Implementation Notes

Tooltips are for supplementary information only. If the information is essential, display it persistently or use a different pattern (inline text, help icon with popover).

## Tree View

### Required ARIA

| Attribute | Element | Purpose |
|-----------|---------|---------|
| `role="tree"` | Container | Identifies the tree widget |
| `role="treeitem"` | Each node | Identifies a tree node |
| `role="group"` | Child container | Groups child nodes under a parent |
| `aria-expanded="true/false"` | Parent node | Indicates expand/collapse state |
| `aria-selected` | Focused node | Indicates selection (if applicable) |
| `aria-level` | Each node | Depth level in the tree (1-based) |

### Code Example

```html
<ul role="tree" aria-label="File system">
  <li role="treeitem" aria-expanded="true" aria-level="1">
    src/
    <ul role="group">
      <li role="treeitem" aria-level="2" aria-expanded="false">
        components/
        <ul role="group">
          <li role="treeitem" aria-level="3">Button.tsx</li>
          <li role="treeitem" aria-level="3">Card.tsx</li>
        </ul>
      </li>
      <li role="treeitem" aria-level="2">index.ts</li>
    </ul>
  </li>
</ul>
```

### Keyboard Behavior

- **Arrow Down**: Move focus to the next visible treeitem
- **Arrow Up**: Move focus to the previous visible treeitem
- **Arrow Right**: Expand a collapsed node; if expanded, move to first child
- **Arrow Left**: Collapse an expanded node; if collapsed, move to parent
- **Home**: Move focus to the first node in the tree
- **End**: Move focus to the last visible node
- **Enter**: Activate the focused node (open file, select item)

## Alert and Live Regions

### Alert (Urgent)

Use `role="alert"` for important, time-sensitive information that requires immediate attention.

```html
<div role="alert">
  Your session will expire in 2 minutes. <a href="/extend">Extend session</a>.
</div>
```

Screen readers interrupt current speech to announce alerts immediately.

### Status (Polite)

Use `role="status"` or `aria-live="polite"` for non-urgent updates that should be announced when the screen reader is idle.

```html
<div role="status" aria-live="polite" aria-atomic="true">
  12 results found for "design tokens"
</div>
```

### Log

Use `aria-live="polite"` with `role="log"` for sequential updates like chat messages or activity feeds.

```html
<div role="log" aria-live="polite" aria-relevant="additions">
  <!-- New messages are appended here and announced -->
</div>
```

### Key Properties

| Property | Effect |
|----------|--------|
| `aria-live="polite"` | Announced when screen reader is idle |
| `aria-live="assertive"` | Interrupts current speech (use sparingly) |
| `aria-atomic="true"` | Announces the entire region, not just changed parts |
| `aria-relevant="additions"` | Only announce added content (default: additions text) |

### Common Mistakes

- Adding `aria-live` to a region that already contains content on page load -- this causes the entire content to be announced
- Using `assertive` for non-critical updates, creating a disruptive experience
- Not including `aria-atomic="true"` when the entire message must be read as a unit (e.g., "3 items in cart" not just "3")

## See Also

- [[wcag-checklist.md]] -- WCAG criteria that these ARIA patterns help satisfy
- [[keyboard-nav-guide.md]] -- Keyboard interaction patterns referenced in each widget
- [[inclusive-design.md]] -- Inclusive design principles that inform accessible widget design
- [[../../frontend-components/references/react-patterns.md]] -- React accessibility patterns using these ARIA implementations
- [[../../frontend-components/references/web-components.md]] -- ARIA in custom elements and Shadow DOM
- [[../../component-library/references/composition-patterns.md]] -- Component patterns that implement these ARIA widgets

**Back to:** [Accessibility Audit Skill](../SKILL.md)

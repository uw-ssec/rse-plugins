# State Management

Comprehensive reference for managing UI component states in design system libraries. Covers the five UI states model, state machines with XState, controlled vs uncontrolled component patterns, optimistic updates, form state management, and loading state implementation patterns.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [The Five UI States](#the-five-ui-states) | 14-65 | Empty, Loading, Partial, Error, and Ideal states with design requirements |
| [State Machines](#state-machines) | 67-115 | XState basics for modeling complex component state transitions |
| [Controlled vs Uncontrolled Components](#controlled-vs-uncontrolled-components) | 117-155 | State ownership patterns with implementation examples |
| [Optimistic Updates](#optimistic-updates) | 157-195 | Updating UI before server confirmation for perceived performance |
| [Form State Management](#form-state-management) | 197-235 | Validation, dirty tracking, submission states, and error display |
| [Loading State Patterns](#loading-state-patterns) | 237-275 | Skeleton screens, spinners, progress indicators, and choosing the right pattern |
| [See Also](#see-also) | 277-283 | Related references and skills |

## The Five UI States

Every component that displays data must handle five possible states. Designing only for the "happy path" creates interfaces that break when reality deviates from the ideal.

### 1. Empty State

No data exists yet. The user has not created items, the search returned zero results, or the feature is unused.

**Design requirements:**
- Explain why the area is empty in plain language
- Provide a clear call-to-action to populate the area
- Use an illustration or icon to soften the emptiness
- Never show a blank white space with no explanation

```tsx
function EmptyState({ title, description, action }) {
  return (
    <div role="status" className="empty-state">
      <EmptyIllustration />
      <h3>{title}</h3>
      <p>{description}</p>
      {action && <Button onClick={action.onClick}>{action.label}</Button>}
    </div>
  );
}
```

### 2. Loading State

Data is being fetched or computed. Show a skeleton, spinner, or progress indicator immediately. Announce loading state to screen readers via `aria-busy` or `aria-live`.

### 3. Partial State

Some data has loaded, but more exists. Render whatever data is available immediately. Indicate that more data exists with pagination or a "load more" button.

### 4. Error State

Something went wrong. Clearly identify the problem, explain what the user can do, and provide a recovery action.

```tsx
function ErrorState({ message, onRetry }) {
  return (
    <div role="alert" className="error-state">
      <ErrorIcon />
      <p>{message}</p>
      {onRetry && <Button onClick={onRetry} variant="secondary">Try again</Button>}
    </div>
  );
}
```

### 5. Ideal State

Everything works as expected. Display the content as designed with all interactive elements functional.

### State Transition Diagram

```
[Empty] --user creates data--> [Loading] --success--> [Ideal]
[Ideal] --refresh--> [Loading] --success--> [Ideal]
[Ideal] --refresh--> [Loading] --failure--> [Error]
[Ideal] --delete all--> [Empty]
[Error] --retry--> [Loading] --success--> [Ideal]
[Loading] --partial--> [Partial] --complete--> [Ideal]
```

## State Machines

State machines formalize valid states and transitions. They prevent impossible states and make complex interactions predictable.

### Why State Machines

Without a state machine, complex components accumulate boolean flags:

```ts
// Boolean soup -- can isLoading and isSuccess both be true?
const [isLoading, setIsLoading] = useState(false);
const [isError, setIsError] = useState(false);
const [isSuccess, setIsSuccess] = useState(false);
```

With a state machine, only valid states exist:

```ts
type State = 'idle' | 'loading' | 'success' | 'error';
```

### XState Example

```ts
import { createMachine, assign } from 'xstate';

const fetchMachine = createMachine({
  id: 'fetch',
  initial: 'idle',
  context: { data: null, error: null, retryCount: 0 },
  states: {
    idle: {
      on: { FETCH: 'loading' },
    },
    loading: {
      invoke: {
        src: 'fetchData',
        onDone: {
          target: 'success',
          actions: assign({ data: (_, event) => event.data }),
        },
        onError: {
          target: 'error',
          actions: assign({ error: (_, event) => event.data }),
        },
      },
    },
    success: {
      on: { REFRESH: 'loading' },
    },
    error: {
      on: {
        RETRY: {
          target: 'loading',
          actions: assign({ retryCount: (ctx) => ctx.retryCount + 1 }),
        },
      },
    },
  },
});
```

### Common Component State Machines

| Component | States | Key Transitions |
|-----------|--------|----------------|
| **Modal** | closed, opening, open, closing | open->opening->open, close->closing->closed |
| **Form** | idle, validating, submitting, success, error | submit->validating->submitting->success/error |
| **Dropdown** | closed, opening, open, navigating | click->opening->open, escape->closed |
| **Toast** | entering, visible, exiting, dismissed | show->entering->visible, timeout->exiting |
| **Infinite List** | idle, loading, loadingMore, error, complete | scroll->loadingMore->idle/complete |

## Controlled vs Uncontrolled Components

### Controlled Pattern

The parent owns the state. The component receives its current value as a prop.

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
    />
  );
}
```

### Uncontrolled Pattern

The component manages its own state internally.

```tsx
function Slider({ defaultValue = 50, onChangeEnd, min = 0, max = 100 }) {
  const [value, setValue] = useState(defaultValue);
  return (
    <input
      type="range"
      value={value}
      onChange={(e) => setValue(Number(e.target.value))}
      onMouseUp={() => onChangeEnd?.(value)}
    />
  );
}
```

### Hybrid Pattern (Design System Standard)

Accept an optional value prop. If provided, the component is controlled. If not, it manages its own state.

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

## Optimistic Updates

Optimistic updates show the result of an action immediately, before the server confirms it. This eliminates perceived latency for common operations.

### Pattern

```tsx
function TodoItem({ todo }) {
  const [optimisticDone, setOptimisticDone] = useState(todo.done);

  async function handleToggle() {
    const newValue = !optimisticDone;
    setOptimisticDone(newValue);

    try {
      await api.updateTodo(todo.id, { done: newValue });
    } catch {
      setOptimisticDone(!newValue); // Revert on failure
      toast.error('Failed to update. Please try again.');
    }
  }

  return (
    <label>
      <input type="checkbox" checked={optimisticDone} onChange={handleToggle} />
      {todo.title}
    </label>
  );
}
```

### When to Use Optimistic Updates

| Action | Use Optimistic? | Reason |
|--------|----------------|--------|
| Toggle checkbox | Yes | High success rate, easily reversible |
| Like/favorite | Yes | High success rate, easily reversible |
| Delete item | Cautiously | Show undo toast, revert if fails |
| Create item | No | Need server-generated ID |
| Payment/purchase | Never | Irreversible, must confirm |

### React 19 useOptimistic

```tsx
import { useOptimistic } from 'react';

function Likes({ count, liked }) {
  const [optimisticLiked, setOptimisticLiked] = useOptimistic(liked);

  async function handleLike() {
    setOptimisticLiked(!liked);
    await api.toggleLike();
  }

  return (
    <button onClick={handleLike} aria-pressed={optimisticLiked}>
      {optimisticLiked ? 'Liked' : 'Like'}
    </button>
  );
}
```

## Form State Management

### Form States

| State | Description | UI Behavior |
|-------|-------------|-------------|
| **Pristine** | No fields touched | Disable submit, hide validation |
| **Dirty** | At least one field changed | Enable submit, warn on navigation |
| **Validating** | Async validation in progress | Show field spinner, disable submit |
| **Invalid** | Validation errors exist | Show errors, highlight fields |
| **Submitting** | Form being sent | Disable all fields, show loading |
| **Submitted** | Sent successfully | Show success, redirect |
| **Failed** | Submission failed | Show error, preserve input |

### Validation Timing

| Strategy | When to Validate | Best For |
|----------|-----------------|----------|
| On submit | User clicks submit | Simple forms, low friction |
| On blur | User leaves the field | Medium-complexity forms |
| On change | Every keystroke | Real-time feedback (password strength) |
| Hybrid | On blur first, on change after error | Best balance |

### Accessible Error Display

```tsx
function FormField({ label, name, error, children }) {
  const id = useId();
  const errorId = `${id}-error`;

  return (
    <div>
      <label htmlFor={id}>{label}</label>
      {React.cloneElement(children, {
        id,
        name,
        'aria-invalid': !!error,
        'aria-describedby': error ? errorId : undefined,
      })}
      {error && (
        <p id={errorId} role="alert" className="error-message">{error}</p>
      )}
    </div>
  );
}
```

## Loading State Patterns

### Skeleton Screens

Skeletons mimic the shape of content, reducing perceived loading time and preventing layout shift.

```css
.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-gray-200) 25%,
    var(--color-gray-100) 50%,
    var(--color-gray-200) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
  border-radius: var(--radius-sm);
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

@media (prefers-reduced-motion: reduce) {
  .skeleton { animation: none; background: var(--color-gray-200); }
}
```

### Spinners

Use spinners for operations with unknown duration that lack a clear content shape:

```tsx
function Spinner({ size = 'md', label = 'Loading' }) {
  const sizes = { sm: '1rem', md: '1.5rem', lg: '2rem' };
  return (
    <svg role="status" aria-label={label} width={sizes[size]} height={sizes[size]} viewBox="0 0 24 24">
      <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" fill="none" opacity="0.25" />
      <path d="M12 2a10 10 0 019.95 9" stroke="currentColor" strokeWidth="3" fill="none" strokeLinecap="round">
        <animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="0.75s" repeatCount="indefinite" />
      </path>
    </svg>
  );
}
```

### Progress Indicators

Use progress bars when the completion percentage is known:

```tsx
function ProgressBar({ value, max = 100, label }) {
  const percentage = Math.round((value / max) * 100);
  return (
    <div role="progressbar" aria-valuenow={value} aria-valuemin={0} aria-valuemax={max} aria-label={label}>
      <div style={{ width: `${percentage}%` }} className="progress-fill" />
    </div>
  );
}
```

### Choosing the Right Pattern

| Scenario | Pattern | Reason |
|----------|---------|--------|
| Page load with known layout | Skeleton | Reduces perceived wait, prevents CLS |
| Button action | Inline spinner | Shows action is processing |
| File upload | Progress bar | Known completion percentage |
| Data table refresh | Overlay spinner | Preserves existing content |
| Infinite scroll | Skeleton rows | Matches expected content shape |

## See Also

- [[composition-patterns.md]] -- Component structures that contain and manage these states
- [[variant-systems.md]] -- Variant definitions for different state appearances
- [[../../accessibility-audit/references/aria-patterns.md]] -- ARIA live regions for announcing state changes
- [[../../frontend-components/references/react-patterns.md]] -- React Suspense and error boundaries
- [[../../design-handoff/references/qa-process.md]] -- QA process for verifying all state implementations

**Back to:** [Component Library Skill](../SKILL.md)

## Component States Table (Moved from SKILL.md)

| State | Description | Design Requirement |
|-------|-------------|-------------------|
| Empty | No data | Helpful message, illustration, add action |
| Loading | Data being fetched | Skeleton/spinner/progress |
| Partial | Some data, more coming | Render available, indicate more |
| Error | Something failed | Clear message, recovery, retry |
| Ideal | Works as expected | Full content |
| Disabled | Interaction unavailable | Reduced opacity, no pointer events, tooltip |
| Hover | Pointer over | Color/elevation shift |
| Focus | Keyboard focus | Visible focus ring (required) |
| Active/Pressed | Click/tap | Compressed/darkened |

## A11y Requirements by Component (Moved from SKILL.md)

| Component | Key Requirements |
|-----------|-----------------|
| Button | role, disabled+loading announced, Enter/Space activate |
| Input | Associated label, error linked via aria-describedby, required announced |
| Modal | Focus trap, Esc closes, focus returns to trigger, aria-modal |
| Tabs | role=tablist/tab/tabpanel, arrow nav, active state announced |
| Dropdown | role=listbox/menu, arrow nav, typeahead, Esc closes |
| Toast | role=alert or aria-live=polite, sufficient time, dismiss action |
| Table | th/td semantics, scope attrs, sortable announcement |

## Component Inventory (Moved from SKILL.md)

1. Screenshot every screen, group by page type.
2. Extract unique components — distinct = differs in structure/behavior/purpose.
3. Catalog variants per component.
4. Score by frequency × inconsistency; build high/high first.

[Back to Design System Creation](../index.md)

# Component API Design Guide

Principles and patterns for designing consistent, intuitive, and accessible component APIs.

---

## Prop Naming Conventions

### Consistent Vocabulary

Establish a standard vocabulary and use it across all components:

| Concept | Prop Name | Avoid |
|---------|-----------|-------|
| Visual style | `variant` | `type`, `kind`, `style`, `appearance` |
| Size | `size` | `dimension`, `scale` |
| Color scheme | `colorScheme` | `color`, `theme` |
| Disabled state | `disabled` | `isDisabled` (unless framework convention) |
| Loading state | `loading` | `isLoading`, `fetching` |
| Content | `children` | `content`, `text`, `label` (unless non-child content) |
| Fully expanded width | `fullWidth` | `block`, `fluid`, `stretch` |
| Open/closed state | `open` | `isOpen`, `visible`, `show` |

### Boolean Naming

Use adjectives or past participles. Do not prefix with `is` unless the framework convention requires it.

```tsx
// Preferred
<Modal open onClose={handleClose} />
<Button disabled loading />
<Input readOnly required />
```

---

## Required vs Optional Props

### Required Props

Only require what the component cannot function without:

```tsx
// Good: only truly required props are required
interface AvatarProps {
  src: string;                     // required -- no sensible default
  alt: string;                     // required -- accessibility
  size?: 'sm' | 'md' | 'lg';      // optional -- has default
}
```

### Sensible Defaults

Every optional prop should have a documented default value:

```tsx
function Avatar({ src, alt, size = 'md', rounded = true }: AvatarProps) {
  // ...
}
```

---

## Prop Types and Validation

### Union Types over Booleans

Prefer string unions when there are more than two options or the meaning is unclear:

```tsx
// Bad: what does primary={true} mean for other styles?
<Button primary />

// Good: explicit variant name
<Button variant="primary" />

// Bad: multiple booleans for mutually exclusive states
<Badge success />
<Badge warning />

// Good: single union prop
<Badge status="success" />
```

### Discriminated Unions for Conditional Props

```tsx
type LinkButtonProps = {
  as: 'a';
  href: string;
  target?: '_blank' | '_self';
};

type ActionButtonProps = {
  as?: 'button';
  onClick: () => void;
  type?: 'button' | 'submit';
};

type ButtonProps = (LinkButtonProps | ActionButtonProps) & {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
};
```

---

## Event / Callback Naming

Follow the `on[Event]` convention consistently:

```tsx
interface DialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;  // toggle pattern
  onClose?: () => void;                    // explicit close
}

interface InputProps {
  value: string;
  onChange: (value: string) => void;       // simplified value
  onBlur?: () => void;
  onFocus?: () => void;
}

interface SelectProps<T> {
  value: T;
  onChange: (value: T) => void;
  onSearchChange?: (query: string) => void;
}
```

### Value-First Callbacks

For simple components, pass the value directly instead of the raw event:

```tsx
// Preferred: consumer gets the value directly
onChange: (value: string) => void;

// Acceptable when consumer needs event details
onKeyDown: (e: React.KeyboardEvent) => void;
```

---

## Composition vs Configuration

### Configuration (Prop-Driven)

Simple components with predictable layouts:

```tsx
<Alert
  variant="warning"
  title="Unsaved changes"
  description="You have unsaved changes that will be lost."
  action={{ label: 'Save', onClick: handleSave }}
  dismissible
/>
```

### Composition (Children-Driven)

Complex components where consumers need layout control:

```tsx
<Alert variant="warning">
  <Alert.Icon />
  <Alert.Content>
    <Alert.Title>Unsaved changes</Alert.Title>
    <Alert.Description>You have unsaved changes.</Alert.Description>
  </Alert.Content>
  <Alert.Actions>
    <Button onClick={handleSave}>Save</Button>
    <Button variant="ghost" onClick={handleDiscard}>Discard</Button>
  </Alert.Actions>
</Alert>
```

### Decision Guide

| Factor | Configuration | Composition |
|--------|--------------|-------------|
| Layout flexibility | Fixed layout | Consumer controls layout |
| Number of slots | 1-3 simple slots | 4+ slots or complex nesting |
| Customization needs | Low | High |
| Learning curve | Lower | Higher |
| Use case examples | Badge, Tooltip, Avatar | Dialog, Card, Table, Form |

---

## Accessibility Props

### Built-in Accessibility

Handle common accessibility automatically:

```tsx
function IconButton({ icon, label, ...props }: IconButtonProps) {
  return (
    <button aria-label={label} {...props}>
      {icon}
    </button>
  );
}
```

### Escape Hatches

Always allow ARIA overrides through the rest props spread:

```tsx
function Tabs({ 'aria-label': ariaLabel = 'Tabs', ...props }: TabsProps) {
  return <div role="tablist" aria-label={ariaLabel} {...props} />;
}

// Consumer can override
<Tabs aria-label="Account settings navigation" />
```

### Required Accessibility Props

Some props should be required for accessibility:

```tsx
interface ImageProps {
  src: string;
  alt: string;          // Always required
}

interface IconButtonProps {
  icon: React.ReactNode;
  label: string;        // Required for accessible name
}
```

---

## Size / Variant / Color Conventions

### Standard Size Scale

```tsx
type Size = 'xs' | 'sm' | 'md' | 'lg' | 'xl';
```

Use the same size names across all components for consistency.

### Standard Variant Names

```tsx
type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'link' | 'destructive';
type AlertVariant = 'info' | 'success' | 'warning' | 'error';
type BadgeVariant = 'default' | 'success' | 'warning' | 'error' | 'info';
```

### Color Scheme Convention

```tsx
type ColorScheme = 'gray' | 'red' | 'orange' | 'yellow' | 'green' | 'blue' | 'purple';

<Tag colorScheme="green">Active</Tag>
<Tag colorScheme="red">Inactive</Tag>
```

---

## Forward Refs

All leaf components that render a single DOM element should forward refs:

```tsx
import { forwardRef } from 'react';

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ size = 'md', state = 'default', className, ...props }, ref) => {
    return (
      <input
        ref={ref}
        className={cn(inputVariants({ size, state }), className)}
        {...props}
      />
    );
  }
);
Input.displayName = 'Input';
```

**Why forward refs:**
- Focus management (`inputRef.current.focus()`)
- Element measurement (`ref.current.getBoundingClientRect()`)
- Tooltip/popover positioning libraries
- Third-party form library integration

---

## Slot APIs

For components with multiple customizable areas, use named slot props:

```tsx
interface CardProps {
  children: React.ReactNode;
  header?: React.ReactNode;
  footer?: React.ReactNode;
  media?: React.ReactNode;
  classNames?: {
    root?: string;
    header?: string;
    body?: string;
    footer?: string;
    media?: string;
  };
}

function Card({ children, header, footer, media, classNames }: CardProps) {
  return (
    <div className={cn('rounded-lg border bg-white', classNames?.root)}>
      {media && <div className={cn('overflow-hidden rounded-t-lg', classNames?.media)}>{media}</div>}
      {header && <div className={cn('border-b px-4 py-3', classNames?.header)}>{header}</div>}
      <div className={cn('px-4 py-4', classNames?.body)}>{children}</div>
      {footer && <div className={cn('border-t px-4 py-3', classNames?.footer)}>{footer}</div>}
    </div>
  );
}
```

---

## Documentation and Examples

### Prop Documentation Format

Every component should export its props interface with JSDoc comments:

```tsx
interface TooltipProps {
  /** The content displayed inside the tooltip */
  content: React.ReactNode;
  /** Which side of the trigger to display the tooltip */
  side?: 'top' | 'right' | 'bottom' | 'left';
  /** Delay in milliseconds before the tooltip appears */
  delayMs?: number;
  /** The trigger element */
  children: React.ReactNode;
}
```

### Usage Examples in Docs

Show simplest usage first, then add complexity:

```tsx
// Basic
<Tooltip content="Save document">
  <Button>Save</Button>
</Tooltip>

// With options
<Tooltip content="Delete permanently" side="bottom" delayMs={500}>
  <IconButton icon={<TrashIcon />} label="Delete" />
</Tooltip>
```

### Anti-Patterns to Document

Explicitly show what not to do:

```tsx
// Don't: tooltip for critical information
<Tooltip content="Required field">
  <Input />
</Tooltip>

// Do: visible label or helper text
<FormField label="Email" required helperText="We will never share your email.">
  <Input />
</FormField>
```

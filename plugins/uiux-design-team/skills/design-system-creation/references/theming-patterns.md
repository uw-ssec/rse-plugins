[Back to Design System Creation](../index.md)

# Design System Theming Patterns

Strategies for building multi-theme, multi-brand design systems with runtime and compile-time approaches.

---

## CSS Custom Properties Theming

The foundation of modern theming. Define tokens as CSS custom properties and swap their values per theme.

```css
/* tokens.css */
:root {
  /* Color tokens */
  --color-background: #ffffff;
  --color-surface: #f9fafb;
  --color-text-primary: #111827;
  --color-text-secondary: #6b7280;
  --color-primary: #2563eb;
  --color-primary-hover: #1d4ed8;
  --color-border: #e5e7eb;

  /* Typography tokens */
  --font-family-sans: 'Inter', system-ui, sans-serif;
  --font-family-mono: 'JetBrains Mono', monospace;

  /* Spacing tokens */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;

  /* Shadow tokens */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);

  /* Radius tokens */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;
}

/* Components consume tokens */
.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-lg);
  box-shadow: var(--shadow-sm);
}
```

---

## Multi-Brand Theming

Support multiple brands by swapping token sets. Each brand overrides the same custom property names.

```css
/* Brand A */
[data-brand='alpha'] {
  --color-primary: #2563eb;
  --color-primary-hover: #1d4ed8;
  --font-family-sans: 'Inter', system-ui, sans-serif;
  --radius-md: 8px;
}

/* Brand B */
[data-brand='beta'] {
  --color-primary: #059669;
  --color-primary-hover: #047857;
  --font-family-sans: 'DM Sans', system-ui, sans-serif;
  --radius-md: 4px;
}

/* Brand C */
[data-brand='gamma'] {
  --color-primary: #7c3aed;
  --color-primary-hover: #6d28d9;
  --font-family-sans: 'Poppins', system-ui, sans-serif;
  --radius-md: 12px;
}
```

```tsx
// Set brand at the app root
function App({ brand }: { brand: 'alpha' | 'beta' | 'gamma' }) {
  return (
    <div data-brand={brand}>
      <Router />
    </div>
  );
}
```

All components automatically adapt because they reference the same custom property names.

---

## Theme Switching (Light / Dark / Custom)

### Data Attribute Approach

```css
:root, [data-theme='light'] {
  --color-background: #ffffff;
  --color-surface: #f9fafb;
  --color-text-primary: #111827;
  --color-text-secondary: #6b7280;
  --color-border: #e5e7eb;
}

[data-theme='dark'] {
  --color-background: #0f172a;
  --color-surface: #1e293b;
  --color-text-primary: #f1f5f9;
  --color-text-secondary: #94a3b8;
  --color-border: #334155;
}

[data-theme='high-contrast'] {
  --color-background: #000000;
  --color-surface: #1a1a1a;
  --color-text-primary: #ffffff;
  --color-text-secondary: #cccccc;
  --color-border: #666666;
}
```

### Theme Switcher with System Preference Detection

```tsx
type Theme = 'light' | 'dark' | 'system';

function useTheme() {
  const [theme, setTheme] = useState<Theme>(() => {
    if (typeof window === 'undefined') return 'system';
    return (localStorage.getItem('theme') as Theme) ?? 'system';
  });

  useEffect(() => {
    const root = document.documentElement;
    let resolved = theme;

    if (theme === 'system') {
      resolved = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    root.setAttribute('data-theme', resolved);
    localStorage.setItem('theme', theme);
  }, [theme]);

  return { theme, setTheme };
}
```

---

## Theme Tokens

### Color Tokens

```css
:root {
  /* Primitive palette */
  --blue-50: #eff6ff;
  --blue-500: #3b82f6;
  --blue-600: #2563eb;
  --blue-700: #1d4ed8;

  /* Semantic aliases */
  --color-primary: var(--blue-600);
  --color-primary-hover: var(--blue-700);
  --color-primary-light: var(--blue-50);
}
```

### Typography Tokens

```css
:root {
  --font-size-xs: 0.75rem;    /* 12px */
  --font-size-sm: 0.875rem;   /* 14px */
  --font-size-base: 1rem;     /* 16px */
  --font-size-lg: 1.125rem;   /* 18px */
  --font-size-xl: 1.25rem;    /* 20px */
  --font-size-2xl: 1.5rem;    /* 24px */
  --font-size-3xl: 1.875rem;  /* 30px */
  --font-size-4xl: 2.25rem;   /* 36px */

  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  --line-height-tight: 1.25;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.75;

  --letter-spacing-tight: -0.02em;
  --letter-spacing-normal: 0;
  --letter-spacing-wide: 0.025em;
}
```

### Spacing Tokens

```css
:root {
  --space-0: 0;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;
}
```

### Shadow Tokens

```css
:root {
  --shadow-none: none;
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

[data-theme='dark'] {
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
}
```

---

## Theme Provider Patterns

### React Context Provider

```tsx
interface ThemeContextValue {
  theme: 'light' | 'dark' | 'system';
  resolvedTheme: 'light' | 'dark';
  setTheme: (theme: 'light' | 'dark' | 'system') => void;
  tokens: Record<string, string>;
}

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);

export function ThemeProvider({ children, defaultTheme = 'system' }: ThemeProviderProps) {
  const { theme, setTheme } = useTheme();
  const resolvedTheme = resolveTheme(theme);
  const tokens = resolvedTheme === 'dark' ? darkTokens : lightTokens;

  return (
    <ThemeContext.Provider value={{ theme, resolvedTheme, setTheme, tokens }}>
      <div data-theme={resolvedTheme}>
        {children}
      </div>
    </ThemeContext.Provider>
  );
}

export function useThemeContext() {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error('useThemeContext must be within ThemeProvider');
  return ctx;
}
```

### CSS Variables Provider (No JavaScript at Runtime)

```tsx
// Set data attribute on <html> during SSR or in a blocking script
// to prevent flash of wrong theme (FOWT)
<script>
  {`
    (function() {
      var theme = localStorage.getItem('theme') || 'system';
      if (theme === 'system') {
        theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      }
      document.documentElement.setAttribute('data-theme', theme);
    })();
  `}
</script>
```

---

## Runtime vs Compile-Time Theming

| Aspect | Runtime Theming | Compile-Time Theming |
|--------|----------------|---------------------|
| Mechanism | CSS custom properties, JS context | Separate CSS bundles, build-time token replacement |
| Theme switching | Instant, no page reload | Requires different build or stylesheet swap |
| Bundle size | Single bundle, all themes | Separate bundles per theme (smaller per theme) |
| Dynamic themes | Supports user-created themes | Fixed set of themes |
| Performance | Minimal overhead | Zero runtime cost |
| Complexity | Simple to implement | Build pipeline configuration |

**Recommendation:** Use CSS custom properties for runtime theming. Reserve compile-time theming for extreme performance requirements or when themes are known at deploy time.

---

## Theme Inheritance

Nested theme providers allow sections of the page to use different themes.

```tsx
<ThemeProvider theme="light">
  <Header />       {/* light theme */}
  <ThemeProvider theme="dark">
    <Sidebar />    {/* dark theme */}
  </ThemeProvider>
  <MainContent />  {/* light theme */}
</ThemeProvider>
```

With CSS custom properties, this works naturally via the cascade:

```html
<div data-theme="light">
  <header>...</header>
  <div data-theme="dark">
    <aside>Uses dark tokens because the data-theme="dark" scope overrides</aside>
  </div>
  <main>Uses light tokens</main>
</div>
```

---

## White-Labeling

White-labeling extends multi-brand theming to let external customers define their own brand tokens.

### Architecture

```
1. Define a token schema (required keys and types)
2. Customer provides token values via JSON or admin UI
3. Server generates a CSS file or injects inline custom properties
4. Application loads the customer-specific tokens at runtime
```

### Dynamic Token Injection

```tsx
function WhiteLabelProvider({ tenantId, children }: { tenantId: string; children: ReactNode }) {
  const { data: tokens } = useSWR(`/api/tenants/${tenantId}/tokens`, fetcher);

  if (!tokens) return <LoadingScreen />;

  const style = Object.entries(tokens).reduce(
    (acc, [key, value]) => ({ ...acc, [`--${key}`]: value }),
    {} as React.CSSProperties
  );

  return <div style={style}>{children}</div>;
}
```

### Token Schema Validation

```ts
const tokenSchema = z.object({
  'color-primary': z.string().regex(/^#[0-9a-f]{6}$/i),
  'color-primary-hover': z.string().regex(/^#[0-9a-f]{6}$/i),
  'font-family-sans': z.string(),
  'radius-md': z.string(),
  'logo-url': z.string().url(),
});

// Validate customer tokens before applying
function applyTenantTokens(raw: unknown) {
  const tokens = tokenSchema.parse(raw);
  // Apply tokens...
}
```

This schema ensures customers cannot break the design system by providing invalid token values.

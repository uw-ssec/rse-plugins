# CSS-in-JS Patterns

Comprehensive reference for CSS-in-JS approaches to styling. Covers the runtime vs build-time spectrum, styled-components patterns, Emotion patterns, Vanilla Extract for type-safe zero-runtime styles, Panda CSS for build-time utility-first styles, performance considerations, and decision guidance.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Runtime vs Build-Time](#runtime-vs-build-time) | 14-45 | The two categories of CSS-in-JS and their tradeoffs |
| [styled-components Patterns](#styled-components-patterns) | 47-100 | Tagged templates, theming, global styles, and dynamic props |
| [Emotion Patterns](#emotion-patterns) | 102-140 | The css prop, styled API, and Emotion-specific features |
| [Vanilla Extract](#vanilla-extract) | 142-190 | Zero-runtime, type-safe styling with static extraction |
| [Panda CSS](#panda-css) | 192-230 | Build-time, utility-first CSS-in-JS with type safety |
| [Performance Comparison](#performance-comparison) | 232-255 | Runtime cost, bundle size, and rendering performance across approaches |
| [Choosing the Right Approach](#choosing-the-right-approach) | 257-290 | Decision framework based on project requirements |
| [See Also](#see-also) | 292-298 | Related references and skills |

## Runtime vs Build-Time

CSS-in-JS libraries fall into two categories based on when they generate CSS.

### Runtime Libraries

Generate CSS in the browser at render time. Styles are computed, injected into `<style>` tags, and managed dynamically.

**Libraries**: styled-components, Emotion (runtime mode), Stitches (discontinued)

**Tradeoffs**:
- Dynamic: styles can depend on props, state, and runtime values
- Cost: JavaScript execution on every render to compute and inject styles
- SSR complexity: requires style extraction during server render to avoid FOUC
- Bundle: library code (8-15kb) plus style computation logic

### Build-Time Libraries

Extract CSS at compile time. The build step generates static CSS files; no style computation happens in the browser.

**Libraries**: Vanilla Extract, Panda CSS, Linaria, compiled (Meta)

**Tradeoffs**:
- Zero runtime cost: CSS is static, loaded like any stylesheet
- Type-safe: styles defined in TypeScript files benefit from full type checking
- Less dynamic: runtime-dependent styles require CSS custom properties or conditional class names
- Build complexity: requires build tool integration (Vite, webpack, esbuild plugins)

### The Spectrum

```
More Dynamic                                           More Performant
<-------------------------------------------------------------->
styled-components  Emotion  Stitches  Panda CSS  Vanilla Extract
     (runtime)    (hybrid)  (hybrid)  (build)      (build)
```

## styled-components Patterns

### Basic Usage

```tsx
import styled from 'styled-components';

const Button = styled.button`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
  background: ${({ theme }) => theme.colors.primary};
  color: white;
  border: none;
  cursor: pointer;
  transition: background-color 150ms ease;

  &:hover {
    background: ${({ theme }) => theme.colors.primaryHover};
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;
```

### Dynamic Props

```tsx
const Button = styled.button`
  background: ${({ $variant }) =>
    $variant === 'outline' ? 'transparent' : 'var(--color-primary)'};
  color: ${({ $variant }) =>
    $variant === 'outline' ? 'var(--color-primary)' : 'white'};
  border: ${({ $variant }) =>
    $variant === 'outline' ? '2px solid var(--color-primary)' : 'none'};
  padding: ${({ $size }) => {
    switch ($size) {
      case 'sm': return '0.25rem 0.75rem';
      case 'lg': return '0.75rem 1.5rem';
      default: return '0.5rem 1rem';
    }
  }};
`;

// Usage: <Button $variant="outline" $size="lg">Click</Button>
// Prefix with $ to prevent props from being forwarded to the DOM
```

### ThemeProvider

```tsx
import { ThemeProvider } from 'styled-components';

const lightTheme = {
  colors: {
    primary: '#3b82f6',
    primaryHover: '#2563eb',
    surface: '#ffffff',
    text: '#1a1a2e',
  },
  spacing: { sm: '0.5rem', md: '1rem', lg: '1.5rem' },
};

const darkTheme = {
  colors: {
    primary: '#60a5fa',
    primaryHover: '#93c5fd',
    surface: '#1a1a2e',
    text: '#e2e8f0',
  },
  spacing: lightTheme.spacing,
};

function App() {
  const [isDark, setIsDark] = useState(false);
  return (
    <ThemeProvider theme={isDark ? darkTheme : lightTheme}>
      <Layout />
    </ThemeProvider>
  );
}
```

### Global Styles

```tsx
import { createGlobalStyle } from 'styled-components';

const GlobalStyle = createGlobalStyle`
  *, *::before, *::after { box-sizing: border-box; }
  body {
    margin: 0;
    font-family: ${({ theme }) => theme.fonts.body};
    background: ${({ theme }) => theme.colors.surface};
    color: ${({ theme }) => theme.colors.text};
  }
`;

// Include <GlobalStyle /> once at the app root
```

## Emotion Patterns

Emotion offers two APIs: the `css` prop (requires Babel/SWC plugin) and the `styled` API (same as styled-components).

### The css Prop

```tsx
/** @jsxImportSource @emotion/react */
import { css } from '@emotion/react';

function Card({ featured, children }) {
  return (
    <div
      css={css`
        padding: var(--space-lg);
        background: var(--color-surface);
        border-radius: var(--radius-md);
        ${featured && css`
          border-left: 4px solid var(--color-primary);
          background: var(--color-surface-accent);
        `}
      `}
    >
      {children}
    </div>
  );
}
```

### Emotion styled API

```tsx
import styled from '@emotion/styled';

const Flex = styled.div`
  display: flex;
  align-items: ${({ $align }) => $align || 'stretch'};
  justify-content: ${({ $justify }) => $justify || 'flex-start'};
  gap: ${({ $gap }) => $gap || '0'};
  flex-direction: ${({ $direction }) => $direction || 'row'};
`;
```

### Emotion vs styled-components

| Feature | Emotion | styled-components |
|---------|---------|-------------------|
| `css` prop | Yes (first-class) | No |
| `styled` API | Yes (compatible) | Yes (original) |
| SSR | Automatic with framework plugins | Requires ServerStyleSheet |
| Bundle size | ~7kb | ~12kb |
| Object styles | First-class support | Supported via `css` helper |
| Performance | Slightly faster | Slightly slower |

### Object Styles in Emotion

```tsx
const cardStyles = css({
  padding: 'var(--space-lg)',
  background: 'var(--color-surface)',
  borderRadius: 'var(--radius-md)',
  '&:hover': {
    boxShadow: 'var(--shadow-md)',
  },
});
```

## Vanilla Extract

Vanilla Extract is a zero-runtime CSS-in-JS library that generates static CSS at build time from TypeScript files. It provides full type safety with no browser runtime cost.

### Style Files

Styles are defined in `.css.ts` files:

```ts
// Button.css.ts
import { style, styleVariants } from '@vanilla-extract/css';
import { vars } from './theme.css';

export const base = style({
  display: 'inline-flex',
  alignItems: 'center',
  justifyContent: 'center',
  fontWeight: 500,
  borderRadius: vars.radius.sm,
  transition: 'background-color 150ms ease',
  ':hover': {
    cursor: 'pointer',
  },
  ':disabled': {
    opacity: 0.5,
    cursor: 'not-allowed',
  },
});

export const variants = styleVariants({
  solid: [base, {
    background: vars.color.primary,
    color: 'white',
    border: 'none',
  }],
  outline: [base, {
    background: 'transparent',
    color: vars.color.primary,
    border: `2px solid ${vars.color.primary}`,
  }],
});

export const sizes = styleVariants({
  sm: { padding: '0.25rem 0.75rem', fontSize: vars.fontSize.sm },
  md: { padding: '0.5rem 1rem', fontSize: vars.fontSize.base },
  lg: { padding: '0.75rem 1.5rem', fontSize: vars.fontSize.lg },
});
```

### Theme Contract

```ts
// theme.css.ts
import { createThemeContract, createTheme } from '@vanilla-extract/css';

export const vars = createThemeContract({
  color: {
    primary: null,
    primaryHover: null,
    surface: null,
    onSurface: null,
  },
  radius: { sm: null, md: null, lg: null },
  fontSize: { sm: null, base: null, lg: null },
});

export const lightTheme = createTheme(vars, {
  color: {
    primary: '#3b82f6',
    primaryHover: '#2563eb',
    surface: '#ffffff',
    onSurface: '#1a1a2e',
  },
  radius: { sm: '0.25rem', md: '0.5rem', lg: '1rem' },
  fontSize: { sm: '0.875rem', base: '1rem', lg: '1.125rem' },
});

export const darkTheme = createTheme(vars, {
  color: {
    primary: '#60a5fa',
    primaryHover: '#93c5fd',
    surface: '#1a1a2e',
    onSurface: '#e2e8f0',
  },
  radius: { sm: '0.25rem', md: '0.5rem', lg: '1rem' },
  fontSize: { sm: '0.875rem', base: '1rem', lg: '1.125rem' },
});
```

### Recipes (Variant API)

```ts
import { recipe } from '@vanilla-extract/recipes';

export const button = recipe({
  base: {
    display: 'inline-flex',
    alignItems: 'center',
    fontWeight: 500,
  },
  variants: {
    variant: {
      solid: { background: vars.color.primary, color: 'white' },
      outline: { border: `2px solid ${vars.color.primary}` },
    },
    size: {
      sm: { padding: '0.25rem 0.75rem' },
      md: { padding: '0.5rem 1rem' },
    },
  },
  defaultVariants: { variant: 'solid', size: 'md' },
});

// Usage: <button className={button({ variant: 'outline', size: 'sm' })} />
```

## Panda CSS

Panda CSS is a build-time, utility-first CSS-in-JS library that combines the developer experience of Tailwind with the type safety of Vanilla Extract.

### Configuration

```ts
// panda.config.ts
import { defineConfig } from '@pandacss/dev';

export default defineConfig({
  preflight: true,
  include: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    tokens: {
      colors: {
        primary: { value: '#3b82f6' },
        surface: { value: '#ffffff' },
      },
      spacing: {
        sm: { value: '0.5rem' },
        md: { value: '1rem' },
      },
    },
    semanticTokens: {
      colors: {
        'button.bg': {
          value: { base: '{colors.primary}', _dark: '{colors.primary}' },
        },
      },
    },
  },
});
```

### Using Panda CSS

```tsx
import { css } from '../styled-system/css';

function Card({ featured, children }) {
  return (
    <div className={css({
      padding: 'md',
      bg: 'surface',
      borderRadius: 'md',
      ...(featured && {
        borderLeft: '4px solid',
        borderColor: 'primary',
      }),
    })}>
      {children}
    </div>
  );
}
```

### Recipes in Panda CSS

```ts
import { cva } from '../styled-system/css';

const button = cva({
  base: {
    display: 'inline-flex',
    alignItems: 'center',
    fontWeight: 'medium',
  },
  variants: {
    variant: {
      solid: { bg: 'primary', color: 'white' },
      outline: { border: '2px solid', borderColor: 'primary', color: 'primary' },
    },
    size: {
      sm: { px: '3', py: '1', fontSize: 'sm' },
      md: { px: '4', py: '2', fontSize: 'base' },
    },
  },
  defaultVariants: { variant: 'solid', size: 'md' },
});
```

### Panda CSS vs Tailwind

| Feature | Panda CSS | Tailwind |
|---------|-----------|----------|
| Type safety | Full TypeScript | No |
| Token integration | Built-in semantic tokens | Via config + CSS vars |
| Dynamic styles | Object syntax in JS | Conditional class names |
| Variant API | Built-in `cva` | Requires external CVA |
| Runtime cost | Zero | Zero |
| Learning curve | Higher | Medium |

## Performance Comparison

| Library | Runtime Cost | SSR Setup | Bundle Impact | First Paint |
|---------|-------------|-----------|---------------|-------------|
| **styled-components** | ~12kb + computation | ServerStyleSheet | Moderate | Slower |
| **Emotion** | ~7kb + computation | Framework-specific | Moderate | Slower |
| **Vanilla Extract** | 0kb | None needed | Static CSS only | Fastest |
| **Panda CSS** | 0kb | None needed | Static CSS only | Fastest |
| **CSS Modules** | 0kb | None needed | Static CSS only | Fastest |

### When Runtime Cost Matters

Runtime CSS-in-JS adds overhead on every render for components with dynamic styles. This becomes measurable when:

- Rendering large lists (100+ items) where each item has dynamic styles
- Frequent re-renders (scroll handlers, drag operations, animations)
- Low-powered devices (mobile, embedded)
- Server components (runtime CSS-in-JS is incompatible with React Server Components)

### React Server Components Compatibility

| Library | RSC Compatible | Notes |
|---------|---------------|-------|
| styled-components | No | Requires client runtime |
| Emotion | No | Requires client runtime |
| Vanilla Extract | Yes | Static CSS, no runtime |
| Panda CSS | Yes | Static CSS, no runtime |
| CSS Modules | Yes | Static CSS, no runtime |

## Choosing the Right Approach

### Decision Matrix

| Requirement | Best Choice |
|-------------|-------------|
| Maximum performance, zero runtime | Vanilla Extract or Panda CSS |
| Type-safe styles | Vanilla Extract or Panda CSS |
| Dynamic, prop-dependent styles | styled-components or Emotion |
| React Server Components | Vanilla Extract, Panda CSS, or CSS Modules |
| Smallest learning curve | styled-components (if familiar with CSS) |
| Utility-first with type safety | Panda CSS |
| Large team with strict design system | Vanilla Extract (enforces token usage) |
| Rapid prototyping | Emotion (css prop) or Panda CSS |
| Existing styled-components codebase | Stay with styled-components or migrate gradually |

### Migration Path

For teams moving from runtime to build-time:

1. **Phase 1**: Introduce Vanilla Extract or Panda CSS for new components
2. **Phase 2**: Migrate high-render-frequency components first (lists, tables, dynamic UIs)
3. **Phase 3**: Migrate remaining components
4. **Phase 4**: Remove runtime CSS-in-JS dependency

The migration can be gradual because build-time and runtime CSS-in-JS coexist in the same application.

## See Also

- [[bem-guide.md]] -- Traditional CSS naming convention as an alternative to CSS-in-JS
- [[tailwind-patterns.md]] -- Utility-first CSS compared to Panda CSS and styled approaches
- [[css-modules-guide.md]] -- Build-time scoped CSS without a JS authoring layer
- [[../../frontend-components/references/react-patterns.md]] -- React patterns that commonly use CSS-in-JS
- [[../../design-system-creation/references/theming-patterns.md]] -- Theme implementation across CSS-in-JS approaches
- [[../../design-tokens/references/platform-output.md]] -- Token output formats consumed by CSS-in-JS theme objects

**Back to:** [CSS Architecture Skill](../SKILL.md)

---
name: component-library
description: Use when implementing or extending a shared component library — scaffolding new components with CVA variants, writing Storybook stories, wiring visual regression, or auditing existing components for state and a11y coverage.
metadata:
   references:
   - references/composition-patterns.md
   - references/state-management.md
   - references/variant-systems.md
---

# Component Library

## Build Order (with validation gates)

1. **Tokens published** → verify with `rg -- '--color-' dist/tokens.css`.
2. **Layout primitives** (`Box`, `Stack`, `Flex`, `Grid`) → verify token consumption: `rg "#[0-9a-fA-F]{6}" src/primitives/` exits empty.
3. **Typography** (`Heading`, `Text`, `Label`).
4. **Button** → run a11y audit before proceeding: `npx test-storybook --url http://127.0.0.1:6006` zero violations.
5. **Form atoms** (`Input`, `Select`, `Checkbox`, `Radio`) → keyboard nav test passes.
6. **Containers** (`Card`, `Modal`, `Drawer`) → focus-trap test passes for Modal.
7. **Data** (`Table`, `List`) → axe-core audit on rendered story.
8. **Nav** (`Nav`, `Tabs`, `Breadcrumbs`).

Gate per tier: a11y audit clean + visual regression reviewed before next tier.

## Compound Component (Select)

```tsx
import { createContext, useContext, useState, ReactNode } from "react";

type Ctx = { value: string | null; setValue: (v: string) => void };
const SelectCtx = createContext<Ctx | null>(null);

export function Select({ children, defaultValue = null }:
  { children: ReactNode; defaultValue?: string | null }) {
  const [value, setValue] = useState<string | null>(defaultValue);
  return (
    <SelectCtx.Provider value={{ value, setValue }}>
      <div role="listbox" className="rounded-md border">{children}</div>
    </SelectCtx.Provider>
  );
}

Select.Option = function Option({ value, children }:
  { value: string; children: ReactNode }) {
  const ctx = useContext(SelectCtx)!;
  const selected = ctx.value === value;
  return (
    <button role="option" aria-selected={selected}
      onClick={() => ctx.setValue(value)}
      className={selected ? "bg-[var(--color-brand-500)] text-white" : ""}>
      {children}
    </button>
  );
};
```

## CVA Variant Definition

```ts
import { cva } from "class-variance-authority";
export const button = cva("inline-flex items-center font-medium rounded-md", {
  variants: {
    intent: { primary: "bg-primary text-white",
              outline: "border-2 border-primary text-primary",
              ghost:   "text-primary hover:bg-primary/10" },
    size:   { sm: "h-8 px-3 text-sm", md: "h-10 px-4", lg: "h-12 px-6 text-lg" }
  },
  compoundVariants: [
    { intent: "ghost", size: "sm", class: "underline-offset-2" }
  ],
  defaultVariants: { intent: "primary", size: "md" }
});
```

## Storybook Story (`Button.stories.tsx`)

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { Button } from "./Button";

const meta: Meta<typeof Button> = {
  component: Button,
  args: { children: "Click me" },
  argTypes: { intent: { control: "select", options: ["primary","outline","ghost"] },
              size:   { control: "select", options: ["sm","md","lg"] } },
  parameters: { a11y: { config: { rules: [{ id: "color-contrast", enabled: true }] } } }
};
export default meta;

export const Primary: StoryObj<typeof Button> = {};
export const Disabled: StoryObj<typeof Button> = { args: { disabled: true } };
export const Loading:  StoryObj<typeof Button> = { args: { children: "Loading…" } };
```

## Playwright Visual Regression (`tests/visual/button.spec.ts`)

```ts
import { test, expect } from "@playwright/test";

const stories = ["primary", "disabled", "loading"];
for (const id of stories) {
  test(`Button ${id} visual`, async ({ page }) => {
    await page.goto(`http://127.0.0.1:6006/iframe.html?id=button--${id}`);
    await expect(page.locator("#storybook-root"))
      .toHaveScreenshot(`button-${id}.png`, { maxDiffPixelRatio: 0.01 });
  });
}
```

Run: `npx playwright test tests/visual/ --update-snapshots` on intentional changes; fail-block on diffs in CI.

## Accessibility Audit (per-component gate)

```bash
# Headless axe-core on every Storybook story
npx test-storybook --url http://127.0.0.1:6006 --maxWorkers=2
# Or one-off:
npx @axe-core/cli http://127.0.0.1:6006/iframe.html?id=button--primary
```

Pass: zero serious/critical violations. Track moderate violations in issue tracker.

## References

- [Composition Patterns](references/composition-patterns.md) — compound, headless, polymorphic, refs
- [Variant Systems](references/variant-systems.md) — CVA, compound variants, type-safe APIs
- [State Management](references/state-management.md) — five UI states table, a11y requirements table, state machines

## Next Steps

- **[Design System Creation](../design-system-creation/SKILL.md)**: Ensure the library aligns with the broader design system governance
- **[Design Tokens](../design-tokens/SKILL.md)**: Consume tokens correctly and contribute component tokens back to the system
- **[Frontend Components](../frontend-components/SKILL.md)**: Implementation-specific guidance for React, Vue, and Svelte components
- **[Accessibility Audit](../accessibility-audit/SKILL.md)**: Validate component accessibility with automated and manual testing

---
name: motion-design
description: Use when adding or fixing UI animation, choosing duration/easing for a transition, debugging janky motion, implementing micro-interactions or page transitions, or auditing motion for prefers-reduced-motion compliance.
metadata:
   references:
   - references/animation-principles.md
   - references/easing-functions.md
   - references/scroll-animations.md
---

# Motion Design

Every animation needs a purpose. If you can't name what it communicates, don't ship it.

## Implementation Workflow

### Step 1 — Define the motion's job

Pick one: communicate spatial change, confirm a user action, direct attention, signal system status, or express brand personality. **If you can't pick one, skip the animation.**

### Step 2 — Choose pattern and budget

| Category | Purpose | Duration | Example |
|----------|---------|----------|---------|
| Micro-interaction | Immediate feedback | 100–200ms | Button press, toggle |
| State transition | Show change | 200–350ms | Modal open, route change |
| Entrance | Direct attention | 200–500ms | List items appear |
| Loading | Communicate wait | continuous | Skeleton, spinner |
| Scroll-linked | Create depth | frame-synced | Parallax, reveal |
| Celebratory | Delight | 500–1500ms | Success confetti |

Easing defaults: `ease-out` for entering, `ease-in` for leaving, `cubic-bezier(0.32, 0.72, 0, 1)` for elegant transitions, spring for direct manipulation.

### Step 3 — Implement

CSS micro-interaction:
```css
.button {
  transition: transform 150ms ease-out, box-shadow 150ms ease-out;
}
.button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,.15); }
.button:active { transform: translateY(0) scale(0.98); transition-duration: 75ms; }
```

CSS modal state transition:
```css
.modal-content {
  transform: translateY(16px) scale(0.96); opacity: 0;
  transition: transform 250ms cubic-bezier(0.32, 0.72, 0, 1), opacity 200ms ease-out;
}
.modal-content.open { transform: translateY(0) scale(1); opacity: 1; }
```

CSS skeleton shimmer:
```css
.skeleton {
  background: linear-gradient(90deg, var(--neutral-100) 25%, var(--neutral-200) 50%, var(--neutral-100) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
}
@keyframes shimmer { 0% { background-position: 200% 0 } 100% { background-position: -200% 0 } }
```

Framer Motion spring:
```jsx
import { motion } from 'framer-motion';
<motion.div
  whileHover={{ y: -4, scale: 1.02 }}
  whileTap={{ scale: 0.98 }}
  transition={{ type: 'spring', stiffness: 400, damping: 25 }}
/>
```

Framer Motion exit animations:
```jsx
import { AnimatePresence, motion } from 'framer-motion';
<AnimatePresence>
  {items.map(i => (
    <motion.div key={i.id}
      initial={{ opacity: 0, height: 0, y: -10 }}
      animate={{ opacity: 1, height: 'auto', y: 0 }}
      exit={{ opacity: 0, height: 0, y: 10 }}
      transition={{ duration: 0.25, ease: 'easeOut' }}
    />
  ))}
</AnimatePresence>
```

### Step 4 — Verify prefers-reduced-motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

**Checkpoint:** Toggle OS setting (macOS: System Settings → Accessibility → Display → Reduce motion). Reload page. All animations should disappear or become instantaneous. If anything still animates, find it and gate it.

### Step 5 — Profile and constrain

Chrome DevTools → Performance panel → CPU: 4× slowdown → Record interaction → verify ≥ 55fps in the FPS strip. Test on real budget Android if shipping consumer mobile.

**Constraints (enforce on every animation):**
- Animate only `transform` and `opacity`. Animating `width`/`top`/`margin` triggers layout — switch to `transform`.
- `will-change: transform` only on actively animating elements; remove after.
- Total screen transition ≤ 500ms; individual element ≤ 350ms.
- `requestAnimationFrame` for JS-driven animation, never `setInterval`.

**Pass:** sustained ≥ 55fps under 4× throttle. **Fail:** below 55fps → switch property to `transform`, remove drop-shadow during animation, or shorten duration.

## Deep Dive References

12 Principles → UI mapping with code in [references/animation-principles.md](references/animation-principles.md). Easing library and spring tuning in [references/easing-functions.md](references/easing-functions.md). Scroll-driven patterns (IntersectionObserver, scroll-timeline, parallax) in [references/scroll-animations.md](references/scroll-animations.md).

## Next Steps

[visual-design](../visual-design/SKILL.md) · [design-tokens](../design-tokens/SKILL.md) · [frontend-components](../frontend-components/SKILL.md) · [accessibility-audit](../accessibility-audit/SKILL.md)

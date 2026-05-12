---
name: motion-design
description: Apply the 12 principles of animation to UI design with purposeful transitions, micro-interactions, scroll effects, loading animations, and performance-optimized motion using CSS, Framer Motion, GSAP, and the View Transitions API.
metadata:
   references:
   - references/animation-principles.md
   - references/easing-functions.md
   - references/scroll-animations.md
---

# Motion Design

Motion is the voice of an interface. Static screens are blueprints; motion brings them to life. Well-designed motion communicates relationships between elements, guides attention, provides feedback, and creates personality. Poorly designed motion is distracting, disorienting, and performance-draining.

The cardinal rule: every animation must have a purpose. If you cannot articulate why something moves, it should not move.

## When to Animate

### The Decision Framework

Before adding any animation, answer three questions:

1. **Does this motion communicate something that static design cannot?** (Spatial relationship, state change, cause-and-effect)
2. **Does the user need this feedback?** (Confirmation of action, system status, error indication)
3. **Does this motion respect the user's time?** (Under 400ms for transitions, under 200ms for micro-interactions)

If the answer to any question is "no," do not animate.

### Animation Categories

| Category | Purpose | Duration | Examples |
|----------|---------|----------|----------|
| Micro-interactions | Immediate feedback | 100-200ms | Button press, toggle, checkbox |
| State transitions | Show change | 200-350ms | Page transition, modal open/close |
| Entrance animations | Direct attention | 200-500ms | List item appear, card enter |
| Loading & progress | Communicate wait | Continuous | Skeleton screens, spinners |
| Scroll-linked | Create depth | Frame-synced | Parallax, reveal on scroll |
| Celebratory | Delight | 500-1500ms | Success confetti, achievement |

## The 12 Principles Applied to UI

Disney's 12 principles of animation, originally developed for character animation, translate directly to interface design:

1. **Squash and Stretch** -- Buttons that compress on press and spring back on release. Toggles that stretch as they slide. This principle communicates materiality -- the element feels like it has physical substance.

2. **Anticipation** -- A slight pull-back before a card flies away on swipe. A button that dips slightly before the action executes. Anticipation prepares the user for what is about to happen.

3. **Staging** -- Direct the user's eye to the most important element. Dim the background when a modal opens. Highlight the changed element after a state update. Everything else becomes supporting cast.

4. **Straight Ahead vs. Pose to Pose** -- In UI, this maps to continuous animations (progress bars, loading spinners) vs. keyframe-defined transitions (modal open has distinct start, mid, and end poses).

5. **Follow Through and Overlapping Action** -- Elements that overshoot their target position and settle back (spring physics). A list where items arrive sequentially with staggered timing rather than all at once.

6. **Ease In, Ease Out** -- Never use linear timing for UI transitions. Natural motion accelerates and decelerates. Use `ease-out` for elements entering (fast start, gentle arrival), `ease-in` for elements leaving (gentle start, fast exit), and `ease-in-out` for elements moving between positions.

7. **Arcs** -- Natural motion follows curved paths, not straight lines. A menu that fans out in an arc, a card that follows a curved trajectory when dragged and released.

8. **Secondary Action** -- The ripple effect on Material Design buttons. A subtle bounce on a notification badge when a new count arrives. Secondary actions reinforce primary actions without distracting from them.

9. **Timing** -- The most critical principle for UI. Too fast and the user misses it. Too slow and the user waits. Micro-interactions: 100-200ms. Transitions: 200-350ms. Complex choreography: up to 500ms total.

10. **Exaggeration** -- A slight overshoot that makes a transition feel more alive. An error shake that is slightly wider than realistic. In UI, exaggeration should be subtle -- enough to feel dynamic, not enough to feel cartoon-like.

11. **Solid Drawing** -- In UI terms: consistent visual quality across all states. The animation should look polished at every frame, not just the start and end. No flickering, no layout shifts, no half-rendered intermediate states.

12. **Appeal** -- The animation should feel good. Spring physics feel more natural than linear easing. Slight overshoot feels more alive than exact positioning. The goal is an emotional response: "this feels nice to use."

## CSS Animation Patterns

### Micro-Interaction: Button Press

```css
.button {
  transition: transform 150ms ease-out, box-shadow 150ms ease-out;
}

.button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.button:active {
  transform: translateY(0px) scale(0.98);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
  transition-duration: 75ms;
}
```

### State Transition: Modal

```css
.modal-overlay {
  opacity: 0;
  transition: opacity 200ms ease-out;
}

.modal-overlay.open {
  opacity: 1;
}

.modal-content {
  transform: translateY(16px) scale(0.96);
  opacity: 0;
  transition: transform 250ms cubic-bezier(0.32, 0.72, 0, 1),
              opacity 200ms ease-out;
}

.modal-content.open {
  transform: translateY(0) scale(1);
  opacity: 1;
}
```

### Entrance: Staggered List

```css
.list-item {
  opacity: 0;
  transform: translateY(12px);
  animation: slideIn 300ms ease-out forwards;
}

.list-item:nth-child(1) { animation-delay: 0ms; }
.list-item:nth-child(2) { animation-delay: 50ms; }
.list-item:nth-child(3) { animation-delay: 100ms; }
.list-item:nth-child(4) { animation-delay: 150ms; }

@keyframes slideIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### Loading: Skeleton Screen

```css
.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-neutral-100) 25%,
    var(--color-neutral-200) 50%,
    var(--color-neutral-100) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
  border-radius: 4px;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

## Framer Motion Patterns

### Spring Physics

```jsx
import { motion } from 'framer-motion';

function Card({ children }) {
  return (
    <motion.div
      whileHover={{ y: -4, scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      transition={{
        type: "spring",
        stiffness: 400,
        damping: 25,
      }}
    >
      {children}
    </motion.div>
  );
}
```

### Layout Animations

```jsx
function ExpandableCard({ isExpanded, children }) {
  return (
    <motion.div
      layout
      transition={{
        layout: { duration: 0.3, ease: [0.32, 0.72, 0, 1] }
      }}
      style={{
        borderRadius: isExpanded ? '16px' : '8px',
      }}
    >
      <motion.div layout="position">
        {children}
      </motion.div>
    </motion.div>
  );
}
```

### AnimatePresence for Exit Animations

```jsx
import { AnimatePresence, motion } from 'framer-motion';

function NotificationList({ notifications }) {
  return (
    <AnimatePresence>
      {notifications.map((n) => (
        <motion.div
          key={n.id}
          initial={{ opacity: 0, height: 0, y: -10 }}
          animate={{ opacity: 1, height: 'auto', y: 0 }}
          exit={{ opacity: 0, height: 0, y: 10 }}
          transition={{ duration: 0.25, ease: 'easeOut' }}
        >
          {n.message}
        </motion.div>
      ))}
    </AnimatePresence>
  );
}
```

## Performance

### The Performance Budget

1. **Animate only `transform` and `opacity`.** These properties are composited by the GPU. Animating `width`, `height`, `top`, `left`, `margin`, or `padding` triggers layout recalculation and is orders of magnitude more expensive.

2. **Use `will-change` sparingly.** Apply `will-change: transform` only to elements that will definitely animate, and remove it after animation completes. Over-use wastes GPU memory.

3. **Respect `prefers-reduced-motion`.** Some users experience motion sickness, vestibular disorders, or simply prefer less motion. Always provide a reduced-motion alternative.

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

4. **Cap total animation duration.** A screen transition should complete within 500ms total. Individual element animations within 350ms. Users perceive anything longer as sluggish.

5. **Use `requestAnimationFrame` for JS animations.** Never use `setInterval` or `setTimeout` for frame-by-frame animation. `requestAnimationFrame` syncs with the browser's repaint cycle for smooth 60fps motion.

6. **Test on low-end devices.** Motion that feels smooth on a MacBook Pro may stutter on a budget Android phone. Profile animation performance on target devices.

## Deep Dive References

### [Animation Principles](references/animation-principles.md)

- 1. Squash and Stretch
- 2. Anticipation
- 3. Staging
- 4. Straight Ahead and Pose to Pose
- 5. Follow Through and Overlapping Action
- 6. Slow In and Slow Out (Ease In, Ease Out)
- 7. Arc
- 8. Secondary Action
- *...and 4 more sections*

### [Easing Functions](references/easing-functions.md)

- CSS Built-in Easing Keywords
- Cubic-Bezier Library
- Spring Physics Parameters
- Custom Bezier Design Methodology
- Quick Reference Table

### [Scroll Animations](references/scroll-animations.md)

- Intersection Observer API Patterns
- CSS Scroll-Driven Animations
- Parallax Techniques
- Scroll-Triggered Reveal Patterns
- Progress Indicators
- Performance Considerations

## Next Steps

- **[Visual Design](../visual-design/SKILL.md)**: Motion within the broader visual design context
- **[Design Tokens](../design-tokens/SKILL.md)**: Encode motion values (duration, easing) as tokens
- **[Frontend Components](../frontend-components/SKILL.md)**: Implement motion patterns in component code
- **[Accessibility Audit](../accessibility-audit/SKILL.md)**: Verify motion respects `prefers-reduced-motion`

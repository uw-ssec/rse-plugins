[Back to Motion Design Skill](../SKILL.md)

# Easing Functions Reference

Easing functions define the rate of change of an animation over time. They transform mechanical, linear movement into motion that feels natural, intentional, and weighted. This reference covers built-in CSS easings, a cubic-bezier library from major design systems, spring physics parameters, and methodology for designing custom curves.

---

## CSS Built-in Easing Keywords

### linear

```css
transition-timing-function: linear;
/* cubic-bezier(0, 0, 1, 1) */
```

Constant speed from start to finish. Rarely appropriate for UI transitions because it feels robotic and unnatural. Appropriate uses: progress bars, loading indicators, continuous rotation, opacity fades where mechanical precision is intentional.

### ease

```css
transition-timing-function: ease;
/* cubic-bezier(0.25, 0.1, 0.25, 1) */
```

The CSS default. Quick acceleration, gentle deceleration. A reasonable general-purpose easing but often too subtle for deliberate motion design. Good for: elements you want to animate but don't want to draw attention to the animation itself.

### ease-in

```css
transition-timing-function: ease-in;
/* cubic-bezier(0.42, 0, 1, 1) */
```

Starts slow, ends fast. Mimics an object accelerating from rest -- like a ball rolling downhill. In UI, use for elements **leaving** the viewport or **exiting** the scene. The acceleration communicates departure.

### ease-out

```css
transition-timing-function: ease-out;
/* cubic-bezier(0, 0, 0.58, 1) */
```

Starts fast, ends slow. Mimics an object decelerating to a stop -- like a ball rolling to rest on a flat surface. In UI, use for elements **entering** the viewport or **appearing**. The deceleration communicates arrival and settling.

### ease-in-out

```css
transition-timing-function: ease-in-out;
/* cubic-bezier(0.42, 0, 0.58, 1) */
```

Slow start, fast middle, slow end. Symmetric curve. Use for elements **moving within** the viewport -- repositioning, reordering, or transitioning between two visible states.

---

## Cubic-Bezier Library

### Material Design 3 Curves

Google's Material Design system defines motion curves based on emphasis and direction.

```css
:root {
  /* Standard easing: most transitions */
  --md-sys-motion-easing-standard: cubic-bezier(0.2, 0, 0, 1);

  /* Standard decelerate: entering elements */
  --md-sys-motion-easing-standard-decelerate: cubic-bezier(0, 0, 0, 1);

  /* Standard accelerate: exiting elements */
  --md-sys-motion-easing-standard-accelerate: cubic-bezier(0.3, 0, 1, 1);

  /* Emphasized easing: important transitions that need attention */
  --md-sys-motion-easing-emphasized: cubic-bezier(0.2, 0, 0, 1);

  /* Emphasized decelerate: dramatic entrance */
  --md-sys-motion-easing-emphasized-decelerate: cubic-bezier(0.05, 0.7, 0.1, 1);

  /* Emphasized accelerate: dramatic exit */
  --md-sys-motion-easing-emphasized-accelerate: cubic-bezier(0.3, 0, 0.8, 0.15);
}
```

**When to use Material curves:**
- Standard curves for routine UI changes (color, shadow, size)
- Emphasized curves for significant UI changes (page transitions, expanding cards, modal entrance)

### Apple HIG Curves

Apple's design system uses curves tuned for the feel of iOS/macOS interactions.

```css
:root {
  /* Default system curve (approximation of Apple's spring-based default) */
  --apple-easing-default: cubic-bezier(0.25, 0.1, 0.25, 1);

  /* Interactive feedback (tap, press) */
  --apple-easing-interactive: cubic-bezier(0.2, 0.8, 0.2, 1);

  /* Sheet/modal presentation */
  --apple-easing-sheet: cubic-bezier(0.32, 0.72, 0, 1);

  /* Dismiss/exit */
  --apple-easing-dismiss: cubic-bezier(0.4, 0, 1, 1);

  /* Bounce effect (overshoot) */
  --apple-easing-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);

  /* Snappy spring approximation */
  --apple-easing-spring: cubic-bezier(0.22, 1, 0.36, 1);
}
```

### Commonly Used Custom Curves

```css
:root {
  /* Snappy entrance: fast arrival, graceful settle */
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);

  /* Smooth entrance: gentle arrival */
  --ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);

  /* Confident exit: purpose-driven departure */
  --ease-in-expo: cubic-bezier(0.7, 0, 0.84, 0);

  /* Dramatic entrance with overshoot */
  --ease-out-back: cubic-bezier(0.34, 1.56, 0.64, 1);

  /* Subtle overshoot */
  --ease-out-back-gentle: cubic-bezier(0.2, 1.2, 0.4, 1);

  /* Elastic snap (strong overshoot + settle) */
  --ease-out-back-strong: cubic-bezier(0.18, 1.8, 0.4, 1);

  /* Smooth in-out for repositioning */
  --ease-in-out-quart: cubic-bezier(0.76, 0, 0.24, 1);

  /* Pronounced in-out with snap */
  --ease-in-out-expo: cubic-bezier(0.87, 0, 0.13, 1);

  /* Very fast start, long settle */
  --ease-out-circ: cubic-bezier(0, 0.55, 0.45, 1);

  /* Gentle, smooth, neutral */
  --ease-out-quad: cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
```

---

## Spring Physics Parameters

Spring-based animation produces the most natural-feeling motion because it follows real physics. Unlike cubic-bezier, springs don't have a fixed duration -- they resolve when the physics simulation settles.

### Core Spring Parameters

| Parameter | Description | Typical Range | Effect |
|-----------|-------------|---------------|--------|
| **stiffness** | How taut the spring is | 100-500 | Higher = faster, snappier |
| **damping** | How quickly oscillation decays | 10-40 | Higher = less bounce |
| **mass** | Weight of the animated object | 0.5-3 | Higher = more momentum, slower |

### Common Spring Presets

```js
const springPresets = {
  // Gentle, floaty entrance
  gentle: { stiffness: 120, damping: 14, mass: 1 },

  // Snappy, responsive feedback
  snappy: { stiffness: 300, damping: 20, mass: 0.8 },

  // Bouncy, playful interaction
  bouncy: { stiffness: 200, damping: 10, mass: 1 },

  // Stiff, no overshoot (like a critically damped spring)
  stiff: { stiffness: 400, damping: 35, mass: 1 },

  // Slow, heavy, dramatic
  heavy: { stiffness: 100, damping: 20, mass: 2.5 },

  // Quick and crisp (button press)
  quick: { stiffness: 500, damping: 30, mass: 0.5 },

  // Elastic, toy-like
  elastic: { stiffness: 180, damping: 8, mass: 1 },
};
```

### Spring Implementation

```js
/**
 * Simple spring physics simulation
 * Returns a function that produces values from 0 to 1 (with possible overshoot)
 */
function createSpring({ stiffness = 180, damping = 12, mass = 1 }) {
  return function animate(element, property, from, to, onComplete) {
    let position = from;
    let velocity = 0;
    const target = to;

    function step() {
      const displacement = position - target;
      const springForce = -stiffness * displacement;
      const dampingForce = -damping * velocity;
      const acceleration = (springForce + dampingForce) / mass;

      velocity += acceleration * (1 / 60);
      position += velocity * (1 / 60);

      element.style[property] = `${position}px`;

      const isSettled =
        Math.abs(displacement) < 0.5 && Math.abs(velocity) < 0.5;

      if (!isSettled) {
        requestAnimationFrame(step);
      } else {
        element.style[property] = `${target}px`;
        onComplete?.();
      }
    }

    requestAnimationFrame(step);
  };
}

// Usage
const bounceIn = createSpring({ stiffness: 200, damping: 10, mass: 1 });
bounceIn(myElement, 'top', -100, 0, () => console.log('settled'));
```

### CSS Spring Approximation

CSS does not natively support spring physics, but you can approximate springs with `linear()` easing (supported in modern browsers).

```css
/* Approximate a bouncy spring with linear() */
.spring-bounce {
  transition: transform 600ms linear(
    0, 0.009, 0.035, 0.078, 0.136, 0.207,
    0.29, 0.381, 0.478, 0.579, 0.681,
    0.783, 0.879, 0.967, 1.044, 1.108,
    1.157, 1.189, 1.205, 1.205, 1.189,
    1.161, 1.122, 1.076, 1.026, 0.976,
    0.931, 0.893, 0.865, 0.849, 0.845,
    0.853, 0.872, 0.899, 0.932, 0.966,
    0.998, 1.024, 1.042, 1.05, 1.049,
    1.041, 1.027, 1.01, 0.993, 0.979,
    0.969, 0.965, 0.966, 0.973, 0.984,
    0.996, 1.007, 1.015, 1.018, 1.017,
    1.012, 1.005, 0.998, 0.993, 0.991,
    0.992, 0.996, 1
  );
}
```

---

## Custom Bezier Design Methodology

### Understanding the Control Points

A cubic-bezier curve is defined by four values: `cubic-bezier(x1, y1, x2, y2)`.

- **(x1, y1)** controls the start of the curve (how the animation begins)
- **(x2, y2)** controls the end of the curve (how the animation ends)
- X values represent time (0 = start, 1 = end). Must be between 0 and 1.
- Y values represent progress (0 = start state, 1 = end state). Can exceed 0-1 for overshoot.

### Design Heuristics

**For entrance animations (ease-out family):**
- Set x1 low (0-0.3) for a fast start
- Set y1 high (0.7-1.5) for aggressive initial movement
- Set x2 low (0-0.4) and y2 at 1 for gentle landing
- Example starting point: `cubic-bezier(0.16, 1, 0.3, 1)`

**For exit animations (ease-in family):**
- Set x1 moderate (0.4-0.7) for a slow start
- Set y1 low (0-0.2) for gradual departure
- Set x2 high (0.8-1) and y2 moderate (0.4-0.8) for fast finish
- Example starting point: `cubic-bezier(0.55, 0, 1, 0.45)`

**For repositioning (ease-in-out family):**
- Set x1 moderate-high (0.4-0.8) for slow start
- Set y1 low (0-0.1)
- Set x2 low (0.1-0.4) for slow end
- Set y2 high (0.9-1)
- Example starting point: `cubic-bezier(0.65, 0, 0.35, 1)`

**For overshoot/bounce:**
- Set y1 > 1 (e.g., 1.56) to overshoot the target
- Higher y1 = more overshoot
- Values above 1.8 start to feel cartoonish
- Example: `cubic-bezier(0.34, 1.56, 0.64, 1)`

### Testing Your Curves

Always test easing curves in context, not in isolation:

1. Apply the curve to the actual element at the actual duration
2. Test on the slowest target device
3. Compare against the built-in `ease` -- your custom curve should be meaningfully different
4. Test with `prefers-reduced-motion` -- provide a simpler fallback

```css
/* Progressive enhancement for custom easing */
.element {
  /* Safe default */
  transition: transform 300ms ease-out;
}

@supports (transition-timing-function: cubic-bezier(0.16, 1, 0.3, 1)) {
  .element {
    transition: transform 300ms cubic-bezier(0.16, 1, 0.3, 1);
  }
}

@media (prefers-reduced-motion: reduce) {
  .element {
    transition: transform 0ms;
  }
}
```

---

## Quick Reference Table

| Use Case | Recommended Easing | Duration |
|----------|-------------------|----------|
| Hover feedback | `ease-out` or `cubic-bezier(0.16, 1, 0.3, 1)` | 100-150ms |
| Button press | `cubic-bezier(0.2, 0.8, 0.2, 1)` | 100-200ms |
| Element entrance | `cubic-bezier(0.16, 1, 0.3, 1)` | 200-350ms |
| Element exit | `cubic-bezier(0.55, 0, 1, 0.45)` | 150-250ms |
| Modal open | `cubic-bezier(0.34, 1.56, 0.64, 1)` | 250-350ms |
| Modal close | `cubic-bezier(0.55, 0, 1, 0.45)` | 200-300ms |
| Reposition/reorder | `cubic-bezier(0.65, 0, 0.35, 1)` | 250-400ms |
| Page transition | `cubic-bezier(0.87, 0, 0.13, 1)` | 300-500ms |
| Collapse/expand | `cubic-bezier(0.16, 1, 0.3, 1)` | 200-350ms |
| Notification enter | `cubic-bezier(0.34, 1.56, 0.64, 1)` | 300-400ms |
| Notification exit | `cubic-bezier(0.55, 0, 1, 0.45)` | 200ms |
| Color/opacity change | `ease` or `ease-out` | 150-250ms |

[Back to Motion Design Skill](../SKILL.md)

# Animation Principles for UI

Disney's 12 Principles of Animation, adapted for user interface design. These principles transform mechanical state changes into experiences that feel natural, intentional, and alive.

---

## 1. Squash and Stretch

**Definition:** Objects deform to show weight, mass, and flexibility during movement. The volume stays constant -- as something squashes wider, it gets shorter, and vice versa.

**UI Application:** Buttons, toggles, and draggable elements can subtly deform during interaction to communicate responsiveness and physicality. Use sparingly -- a little goes a long way in UI.

**Code Example:**

```css
.button:active {
  transform: scaleX(1.05) scaleY(0.95);
  transition: transform 100ms cubic-bezier(0.34, 1.56, 0.64, 1);
}

.button {
  transition: transform 200ms cubic-bezier(0.25, 0.1, 0.25, 1);
}
```

```js
// Spring-based squash and stretch on a draggable element
function applySquash(element, velocityY) {
  const squashAmount = Math.min(Math.abs(velocityY) * 0.002, 0.15);
  element.style.transform = `scaleX(${1 + squashAmount}) scaleY(${1 - squashAmount})`;
}
```

**Do:**
- Apply to elements the user directly manipulates (buttons, toggles, drag targets)
- Keep deformation subtle (5-15% maximum)
- Always return to the original shape

**Don't:**
- Apply to text content or data displays
- Use visible squash and stretch on page-level transitions
- Exaggerate beyond what feels physically plausible

---

## 2. Anticipation

**Definition:** A preparatory movement before the main action, signaling what is about to happen. A pitcher winds up before throwing; a character crouches before jumping.

**UI Application:** Small pre-motion cues that tell the user something is about to change. A button may shrink slightly before an action fires. A panel may shift a few pixels in the opposite direction before sliding open.

**Code Example:**

```css
.panel-trigger:active ~ .panel {
  transform: translateX(-8px);
  transition: transform 100ms ease-out;
}

.panel.is-opening {
  animation: slideInWithAnticipation 400ms cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

@keyframes slideInWithAnticipation {
  0%   { transform: translateX(-8px); opacity: 0; }
  15%  { transform: translateX(-12px); opacity: 0.3; }
  100% { transform: translateX(0); opacity: 1; }
}
```

**Do:**
- Use for actions that produce significant UI changes (opening panels, page transitions)
- Keep anticipation duration short (50-150ms) relative to the main action
- Use to build a sense of cause-and-effect

**Don't:**
- Add anticipation to every interaction (it creates sluggishness)
- Use for instant-feedback elements (toggles should feel immediate)
- Make the preparatory motion larger than the main motion

---

## 3. Staging

**Definition:** Presenting an idea so it is clear and unmistakable. Directing the audience's attention to the most important element in the scene.

**UI Application:** Drawing the user's attention to the right element at the right time. When a modal opens, the background dims. When a notification arrives, it animates into view while the rest of the page stays still.

**Code Example:**

```css
/* Dim everything else to stage the modal */
.backdrop {
  background: rgba(0, 0, 0, 0);
  transition: background 300ms ease;
}

.backdrop.is-active {
  background: rgba(0, 0, 0, 0.5);
}

/* Staged entrance for the focal element */
.modal {
  transform: translateY(24px) scale(0.95);
  opacity: 0;
  transition: all 300ms cubic-bezier(0.16, 1, 0.3, 1);
}

.modal.is-visible {
  transform: translateY(0) scale(1);
  opacity: 1;
}
```

**Do:**
- Dim, blur, or desaturate non-focal elements when staging important content
- Animate only the focal element; keep the rest static
- Use staging for modals, alerts, onboarding spotlights, and feature callouts

**Don't:**
- Animate multiple elements simultaneously without clear hierarchy
- Over-stage routine interactions (not everything needs a spotlight)
- Use staging so aggressively that the user feels trapped

---

## 4. Straight Ahead and Pose to Pose

**Definition:** Two animation approaches -- straight ahead (frame-by-frame, organic, spontaneous) vs. pose to pose (keyframe-defined, controlled, predictable).

**UI Application:** Most UI animation is pose-to-pose: we define start and end states and let CSS or JS interpolate. Straight-ahead is useful for particle effects, generative visuals, and physics simulations.

**Code Example:**

```css
/* Pose-to-pose: defined keyframes */
@keyframes fadeSlideIn {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card-enter {
  animation: fadeSlideIn 300ms ease-out forwards;
}
```

```js
// Straight-ahead: physics-driven, each frame computed from the last
function springAnimation(element, target, stiffness = 180, damping = 12) {
  let position = parseFloat(element.style.transform?.match(/translateY\((.+)px\)/)?.[1] || 0);
  let velocity = 0;

  function tick() {
    const force = -stiffness * (position - target);
    const dampingForce = -damping * velocity;
    velocity += (force + dampingForce) * (1 / 60);
    position += velocity * (1 / 60);

    element.style.transform = `translateY(${position}px)`;

    if (Math.abs(position - target) > 0.01 || Math.abs(velocity) > 0.01) {
      requestAnimationFrame(tick);
    }
  }
  requestAnimationFrame(tick);
}
```

**Do:**
- Default to pose-to-pose (CSS keyframes/transitions) for predictable UI transitions
- Use straight-ahead for organic, physics-based interactions (drag, fling, bounce)
- Combine both: keyframe the broad stroke, physics-simulate the details

**Don't:**
- Use straight-ahead for simple state changes (overkill)
- Use pose-to-pose when the end state is unknown (e.g., drag destination)

---

## 5. Follow Through and Overlapping Action

**Definition:** Elements don't stop all at once. Some parts continue moving after the main body stops (follow through). Different parts move at different rates (overlapping action).

**UI Application:** Staggered animations where child elements arrive slightly after their parent. Inertial scrolling where content continues to drift after the user stops swiping. A card's shadow settling after the card lands.

**Code Example:**

```css
/* Staggered entrance -- overlapping action */
.card-list .card {
  opacity: 0;
  transform: translateY(24px);
  animation: cardEnter 400ms ease-out forwards;
}

.card-list .card:nth-child(1) { animation-delay: 0ms; }
.card-list .card:nth-child(2) { animation-delay: 60ms; }
.card-list .card:nth-child(3) { animation-delay: 120ms; }
.card-list .card:nth-child(4) { animation-delay: 180ms; }

@keyframes cardEnter {
  to { opacity: 1; transform: translateY(0); }
}

/* Follow-through: shadow settles after card */
.card.landed {
  transform: translateY(0);
  transition: transform 300ms cubic-bezier(0.16, 1, 0.3, 1);
}

.card.landed::after {
  /* Shadow follows slightly behind */
  transition: box-shadow 450ms cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
```

**Do:**
- Stagger list item animations (40-80ms between items, cap at ~400ms total)
- Let secondary properties (shadow, background) trail the primary motion
- Use for entrance animations of groups

**Don't:**
- Stagger so slowly that the user waits for content (total stagger < 500ms)
- Apply follow-through to every element (focus on what the user is watching)
- Make stagger delays longer than the animation duration

---

## 6. Slow In and Slow Out (Ease In, Ease Out)

**Definition:** Movement starts slow, accelerates, and slows again at the end. Nothing in the real world starts or stops instantly.

**UI Application:** This is the single most important principle in UI animation. Linear motion feels robotic. Proper easing makes interfaces feel natural and polished.

**Code Example:**

```css
/* Standard ease-out for elements entering the screen */
.entering {
  transition: all 300ms cubic-bezier(0.16, 1, 0.3, 1);
}

/* Ease-in for elements leaving the screen */
.exiting {
  transition: all 200ms cubic-bezier(0.55, 0, 1, 0.45);
}

/* Ease-in-out for elements moving within the screen */
.moving {
  transition: all 250ms cubic-bezier(0.45, 0, 0.55, 1);
}
```

**Do:**
- Use ease-out for entrances (decelerating into view feels welcoming)
- Use ease-in for exits (accelerating out feels like departure)
- Use ease-in-out for on-screen repositioning
- Match easing to the physical metaphor (gravity, springs, friction)

**Don't:**
- Ever use `linear` for UI state transitions (except progress bars and loading spinners)
- Use the same easing for all animations (entrances and exits have different physics)

---

## 7. Arc

**Definition:** Natural movement follows curved paths, not straight lines. A ball thrown travels in a parabola.

**UI Application:** Elements that move across the screen can follow subtle curved paths instead of straight lines. Particularly effective for elements that "fly" from one position to another (shared element transitions, FAB menus).

**Code Example:**

```css
/* Curved path using separate X and Y transitions with different timing */
.flying-element {
  transition:
    transform 400ms cubic-bezier(0.16, 1, 0.3, 1),
    left 400ms cubic-bezier(0.16, 1, 0.3, 1),
    top 400ms cubic-bezier(0.5, 0, 0.1, 1); /* Different curve for vertical */
}

/* Using offset-path for true curved motion */
.arc-motion {
  offset-path: path('M 0 0 Q 150 -80 300 0');
  animation: followArc 500ms cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes followArc {
  from { offset-distance: 0%; }
  to   { offset-distance: 100%; }
}
```

**Do:**
- Use arcs for elements traveling long distances on screen
- Apply to FAB menu items expanding outward
- Use for shared element transitions between pages/views

**Don't:**
- Use arcs for short-distance movements (subtle shifts should be linear-path)
- Apply to purely vertical or horizontal movements (arcs are for diagonal travel)

---

## 8. Secondary Action

**Definition:** Supporting actions that reinforce the main action without drawing attention away from it. A character's hair bouncing as they walk.

**UI Application:** Subtle animations that complement the primary interaction. A ripple effect on a button click. An icon rotating inside a button as it transitions. A background gradient shifting as content scrolls.

**Code Example:**

```css
/* Primary action: button press feedback */
.button:active {
  transform: scale(0.97);
  transition: transform 100ms ease;
}

/* Secondary action: ripple effect */
.button::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%);
  transform: scale(0);
  opacity: 0;
}

.button:active::after {
  animation: ripple 400ms ease-out;
}

@keyframes ripple {
  0%   { transform: scale(0); opacity: 1; }
  100% { transform: scale(2.5); opacity: 0; }
}
```

**Do:**
- Use secondary actions to add richness to important interactions
- Keep secondary actions quieter/slower than the primary action
- Use for hover effects, focus indicators, loading state decorations

**Don't:**
- Let secondary actions compete with the primary for attention
- Add secondary actions to low-importance or frequent interactions
- Use more than one secondary action per primary action

---

## 9. Timing

**Definition:** The speed of an action defines its weight and emotional quality. Fast actions feel light and snappy; slow actions feel heavy and dramatic.

**UI Application:** Duration choices communicate urgency, importance, and physicality. This is perhaps the most practical principle for UI work.

**Recommended duration ranges:**

| Interaction Type | Duration | Rationale |
|-----------------|----------|-----------|
| Hover/focus feedback | 100-150ms | Must feel instant |
| Button press | 100-200ms | Direct manipulation, snappy |
| Toggle/switch | 150-250ms | Visible state change |
| Dropdown/popover open | 150-250ms | Revealing content |
| Modal entrance | 250-350ms | Significant UI change |
| Page transition | 300-500ms | Large-scale change |
| Complex orchestrated | 400-800ms | Multiple staggered elements |

**Code Example:**

```css
:root {
  --duration-instant: 100ms;
  --duration-fast:    150ms;
  --duration-normal:  250ms;
  --duration-slow:    350ms;
  --duration-slower:  500ms;
}
```

**Do:**
- Use shorter durations for direct manipulation (user-initiated)
- Use longer durations for system-initiated changes (notifications, data updates)
- Test on real devices -- animation that feels right on a fast laptop may lag on mobile

**Don't:**
- Exceed 500ms for any single element's animation (users perceive it as laggy)
- Use the same duration for all animations (variety in timing creates rhythm)

---

## 10. Exaggeration

**Definition:** Pushing movement beyond reality to make it clearer and more impactful. Not distortion for its own sake, but emphasis for communication.

**UI Application:** Slightly overshooting a target position before settling. A bounce on a success state. Scale changes that are 10-20% more than strictly necessary to ensure the user notices.

**Code Example:**

```css
/* Overshoot bounce for success confirmation */
@keyframes successBounce {
  0%   { transform: scale(0); }
  60%  { transform: scale(1.15); }  /* Overshoot */
  80%  { transform: scale(0.95); }  /* Settle back */
  100% { transform: scale(1); }     /* Rest */
}

.success-icon {
  animation: successBounce 500ms cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

**Do:**
- Use for confirmations, celebrations, and important state changes
- Exaggerate through overshoot and bounce, not through excessive scale
- Keep exaggeration proportional to importance (subtle for routine, bold for milestones)

**Don't:**
- Exaggerate routine interactions (it becomes exhausting)
- Use exaggeration for error states (errors should feel firm, not bouncy)
- Let exaggeration slow down the perceived interaction speed

---

## 11. Solid Drawing (Visual Consistency)

**Definition:** In traditional animation, solid drawing means consistent volume and perspective. In UI, this translates to consistent visual treatment across states and transitions.

**UI Application:** An element should maintain its visual identity across all states. The shape, proportion, and character should be preserved through hover, active, focus, and animated states.

**Code Example:**

```css
/* Consistent card treatment across states */
.card {
  border-radius: 12px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-primary);
  transition: all 250ms ease-out;
}

.card:hover {
  /* Elevate, but maintain the same visual identity */
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  /* Same border-radius, same background, same border */
}

.card:active {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  /* Reduced elevation but still the same card */
}
```

**Do:**
- Maintain border-radius, proportion, and color relationships across states
- Ensure animated elements look "correct" at every frame, not just start and end
- Use transforms (not dimension changes) to prevent layout shifts during animation

**Don't:**
- Change an element's fundamental visual identity during interaction
- Use animations that pass through awkward intermediate states
- Mix animation paradigms inconsistently (some elements spring, others linear)

---

## 12. Appeal

**Definition:** The quality that makes animation enjoyable to watch. Charm, personality, and craftsmanship.

**UI Application:** The cumulative effect of all the above principles working together. An interface with appeal feels polished, intentional, and delightful without being distracting.

**Code Example:**

```css
/* A micro-interaction with appeal: the like button */
.like-button {
  transition: transform 200ms cubic-bezier(0.34, 1.56, 0.64, 1);
}

.like-button:hover {
  transform: scale(1.1);
}

.like-button.is-liked {
  animation: heartPop 400ms cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes heartPop {
  0%   { transform: scale(1); }
  25%  { transform: scale(1.3); }
  50%  { transform: scale(0.9); }
  100% { transform: scale(1); }
}

/* Particle burst behind the heart */
.like-button.is-liked::before {
  content: '';
  position: absolute;
  inset: -8px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(239, 68, 68, 0.3) 0%, transparent 70%);
  animation: burstFade 500ms ease-out forwards;
}

@keyframes burstFade {
  0%   { transform: scale(0.5); opacity: 1; }
  100% { transform: scale(2); opacity: 0; }
}
```

**Do:**
- Invest animation polish in high-frequency, high-visibility interactions
- Test animations with real users -- what delights designers may annoy users
- Respect `prefers-reduced-motion` by providing reduced or no-motion alternatives

**Don't:**
- Add animation for the sake of animation
- Let appeal override usability (animation should never block or delay user tasks)
- Forget accessibility: always provide `prefers-reduced-motion` fallbacks

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

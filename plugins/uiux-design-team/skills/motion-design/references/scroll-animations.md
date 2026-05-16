[Back to Motion Design Skill](../SKILL.md)

# Scroll-Linked Animations

Patterns for animating elements in response to scroll position. Covers the Intersection Observer API, CSS Scroll-Driven Animations, parallax techniques, scroll-triggered reveals, progress indicators, and performance considerations.

---

## Intersection Observer API Patterns

The Intersection Observer API detects when elements enter or leave the viewport (or a specified container). It is the foundation of scroll-triggered animations in JavaScript.

### Basic Reveal on Scroll

```js
/**
 * Reveal elements as they enter the viewport.
 * Elements start hidden via CSS and get a class added when visible.
 */
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target); // Animate once, stop observing
      }
    });
  },
  {
    threshold: 0.15,   // Trigger when 15% of the element is visible
    rootMargin: '0px 0px -50px 0px', // Trigger 50px before the bottom edge
  }
);

document.querySelectorAll('[data-reveal]').forEach((el) => {
  observer.observe(el);
});
```

```css
/* Initial hidden state */
[data-reveal] {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 600ms cubic-bezier(0.16, 1, 0.3, 1),
              transform 600ms cubic-bezier(0.16, 1, 0.3, 1);
}

/* Revealed state */
[data-reveal].is-visible {
  opacity: 1;
  transform: translateY(0);
}

@media (prefers-reduced-motion: reduce) {
  [data-reveal] {
    opacity: 1;
    transform: none;
    transition: none;
  }
}
```

### Staggered Group Reveal

```js
const staggerObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const children = entry.target.querySelectorAll('[data-stagger-item]');
        children.forEach((child, index) => {
          child.style.transitionDelay = `${index * 60}ms`;
          child.classList.add('is-visible');
        });
        staggerObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.1 }
);

document.querySelectorAll('[data-stagger-group]').forEach((el) => {
  staggerObserver.observe(el);
});
```

```html
<ul data-stagger-group>
  <li data-stagger-item>First item</li>
  <li data-stagger-item>Second item</li>
  <li data-stagger-item>Third item</li>
  <li data-stagger-item>Fourth item</li>
</ul>
```

### Threshold-Based Progressive Reveal

```js
/**
 * Animate based on how much of the element is visible.
 * Useful for progress bars, skill meters, or gradual opacity changes.
 */
const progressObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      const ratio = entry.intersectionRatio;
      entry.target.style.setProperty('--visibility', ratio);
    });
  },
  {
    threshold: Array.from({ length: 20 }, (_, i) => i / 19), // 20 thresholds
  }
);
```

```css
.progressive-reveal {
  opacity: var(--visibility, 0);
  transform: translateY(calc((1 - var(--visibility, 0)) * 24px));
  transition: none; /* Driven by intersection ratio, not transition */
}
```

---

## CSS Scroll-Driven Animations

Modern browsers support scroll-driven animations natively in CSS, eliminating the need for JavaScript in many cases.

### Scroll Progress Animation

```css
/* Animate based on scroll position of the page */
@keyframes fadeSlideUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.scroll-reveal {
  animation: fadeSlideUp linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;
}
```

### Page-Level Scroll Progress Bar

```css
.progress-bar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: var(--accent-primary);
  transform-origin: left;
  animation: scaleProgress linear both;
  animation-timeline: scroll(root);
}

@keyframes scaleProgress {
  from { transform: scaleX(0); }
  to   { transform: scaleX(1); }
}
```

### View Timeline: Animate While in Viewport

```css
/* Element animates as it passes through the viewport */
.parallax-text {
  animation: slideAcross linear both;
  animation-timeline: view(block);
  animation-range: contain 0% contain 100%;
}

@keyframes slideAcross {
  from { transform: translateX(-50px); opacity: 0.5; }
  to   { transform: translateX(50px); opacity: 1; }
}
```

### Scroll-Triggered Sticky Header Shrink

```css
.site-header {
  position: sticky;
  top: 0;
  animation: shrinkHeader linear both;
  animation-timeline: scroll(root);
  animation-range: 0px 200px;
}

@keyframes shrinkHeader {
  from {
    padding-block: 2rem;
    font-size: 1.5rem;
  }
  to {
    padding-block: 0.75rem;
    font-size: 1rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
}
```

---

## Parallax Techniques

### CSS-Only Parallax with perspective

```css
.parallax-container {
  height: 100vh;
  overflow-x: hidden;
  overflow-y: auto;
  perspective: 1px;
  perspective-origin: center center;
}

.parallax-layer--back {
  transform: translateZ(-2px) scale(3);
  position: absolute;
  inset: 0;
  z-index: -1;
}

.parallax-layer--base {
  transform: translateZ(0);
  position: relative;
  z-index: 1;
}
```

### JavaScript Parallax with Scroll Position

```js
/**
 * Lightweight parallax using transform.
 * Each element defines its own speed via data-parallax-speed.
 */
function initParallax() {
  const elements = document.querySelectorAll('[data-parallax-speed]');

  function update() {
    const scrollY = window.scrollY;

    elements.forEach((el) => {
      const speed = parseFloat(el.dataset.parallaxSpeed) || 0.5;
      const rect = el.getBoundingClientRect();
      const centerY = rect.top + rect.height / 2;
      const viewportCenter = window.innerHeight / 2;
      const offset = (centerY - viewportCenter) * speed;

      el.style.transform = `translate3d(0, ${offset}px, 0)`;
    });

    requestAnimationFrame(update);
  }

  // Only run if user hasn't requested reduced motion
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    requestAnimationFrame(update);
  }
}

initParallax();
```

```html
<section class="hero">
  <div data-parallax-speed="-0.3">
    <img src="background.webp" alt="" role="presentation" />
  </div>
  <h1 data-parallax-speed="0.1">Welcome</h1>
</section>
```

### Multi-Layer Depth Parallax

```css
.scene {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
}

.scene__layer {
  position: absolute;
  inset: 0;
  will-change: transform;
}

.scene__layer--far    { --speed: 0.1; }
.scene__layer--mid    { --speed: 0.4; }
.scene__layer--near   { --speed: 0.8; }
.scene__layer--base   { --speed: 1.0; position: relative; }
```

```js
window.addEventListener('scroll', () => {
  document.querySelectorAll('.scene__layer').forEach((layer) => {
    const speed = getComputedStyle(layer).getPropertyValue('--speed');
    const offset = window.scrollY * parseFloat(speed);
    layer.style.transform = `translate3d(0, ${-offset}px, 0)`;
  });
}, { passive: true });
```

---

## Scroll-Triggered Reveal Patterns

### Reveal Direction Variants

```css
/* Fade up (default) */
[data-reveal="up"] {
  opacity: 0;
  transform: translateY(32px);
}

/* Fade down */
[data-reveal="down"] {
  opacity: 0;
  transform: translateY(-32px);
}

/* Fade left */
[data-reveal="left"] {
  opacity: 0;
  transform: translateX(32px);
}

/* Fade right */
[data-reveal="right"] {
  opacity: 0;
  transform: translateX(-32px);
}

/* Scale in */
[data-reveal="scale"] {
  opacity: 0;
  transform: scale(0.9);
}

/* Blur in */
[data-reveal="blur"] {
  opacity: 0;
  filter: blur(8px);
}

/* Common revealed state */
[data-reveal].is-visible {
  opacity: 1;
  transform: none;
  filter: none;
  transition: all 700ms cubic-bezier(0.16, 1, 0.3, 1);
}
```

### Counter / Number Ticker on Scroll

```js
function animateCounter(element, target, duration = 2000) {
  const start = 0;
  const startTime = performance.now();

  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);

    // Ease-out curve
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = Math.round(start + (target - start) * eased);

    element.textContent = current.toLocaleString();

    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }

  requestAnimationFrame(update);
}

// Trigger on scroll
const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      const target = parseInt(entry.target.dataset.countTo, 10);
      animateCounter(entry.target, target);
      counterObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('[data-count-to]').forEach((el) => {
  counterObserver.observe(el);
});
```

### Horizontal Scroll Section

```css
.horizontal-scroll {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
}

.horizontal-scroll__panel {
  flex: 0 0 100vw;
  scroll-snap-align: start;
  min-height: 100vh;
  display: grid;
  place-items: center;
}
```

---

## Progress Indicators

### Reading Progress Bar

```css
.reading-progress {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  background: var(--accent-primary);
  transform-origin: left;
  z-index: 9999;
  transition: transform 50ms linear;
}
```

```js
function updateReadingProgress() {
  const article = document.querySelector('article');
  if (!article) return;

  const bar = document.querySelector('.reading-progress');
  const rect = article.getBoundingClientRect();
  const articleTop = rect.top + window.scrollY;
  const articleHeight = rect.height;
  const viewportHeight = window.innerHeight;

  const scrolled = window.scrollY - articleTop;
  const total = articleHeight - viewportHeight;
  const progress = Math.max(0, Math.min(1, scrolled / total));

  bar.style.transform = `scaleX(${progress})`;
}

window.addEventListener('scroll', updateReadingProgress, { passive: true });
```

### Section Progress Dots

```css
.section-dots {
  position: fixed;
  right: 1.5rem;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  z-index: 100;
}

.section-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--fg-tertiary);
  transition: all 300ms ease-out;
  cursor: pointer;
}

.section-dot.is-active {
  background: var(--accent-primary);
  transform: scale(1.4);
}
```

---

## Performance Considerations

### The Golden Rules

1. **Only animate `transform` and `opacity`.** These are composited by the GPU and do not trigger layout or paint. Animating `top`, `left`, `width`, `height`, `margin`, or `padding` causes expensive reflows.

2. **Use `will-change` sparingly.** It tells the browser to prepare for animation by promoting the element to its own compositor layer. But every layer consumes GPU memory.

```css
/* Apply only when animation is imminent */
.card:hover {
  will-change: transform;
}

/* Remove after animation completes */
.card {
  will-change: auto;
}
```

3. **Use `passive: true` on scroll listeners.** This tells the browser the handler won't call `preventDefault()`, allowing smooth scrolling optimizations.

```js
window.addEventListener('scroll', handler, { passive: true });
```

4. **Debounce or throttle expensive scroll handlers.** Better yet, replace them with Intersection Observer where possible.

```js
function throttle(fn, wait = 16) {
  let lastTime = 0;
  return function (...args) {
    const now = Date.now();
    if (now - lastTime >= wait) {
      lastTime = now;
      fn.apply(this, args);
    }
  };
}

window.addEventListener('scroll', throttle(onScroll, 16), { passive: true });
```

5. **Prefer CSS Scroll-Driven Animations over JavaScript.** When browser support allows, CSS `animation-timeline: scroll()` and `animation-timeline: view()` run entirely on the compositor thread, offering far better performance than any JS-based approach.

6. **Batch DOM reads and writes.** Interleaving reads (getBoundingClientRect) and writes (style changes) causes layout thrashing.

```js
// Bad: read-write-read-write (forces multiple reflows)
elements.forEach((el) => {
  const rect = el.getBoundingClientRect(); // READ
  el.style.transform = `translateY(${rect.top * 0.5}px)`; // WRITE
});

// Good: batch reads, then batch writes
const rects = elements.map((el) => el.getBoundingClientRect()); // ALL READS
elements.forEach((el, i) => {
  el.style.transform = `translateY(${rects[i].top * 0.5}px)`; // ALL WRITES
});
```

7. **Respect `prefers-reduced-motion`.** Always provide a reduced or no-motion fallback for users who have requested it.

```css
@media (prefers-reduced-motion: reduce) {
  [data-reveal],
  [data-parallax-speed],
  .scroll-reveal {
    animation: none !important;
    transition: none !important;
    transform: none !important;
    opacity: 1 !important;
  }
}
```

```js
const prefersReducedMotion = window.matchMedia(
  '(prefers-reduced-motion: reduce)'
).matches;

if (prefersReducedMotion) {
  // Skip all scroll animation initialization
  document.querySelectorAll('[data-reveal]').forEach((el) => {
    el.classList.add('is-visible');
  });
}
```

[Back to Design Handoff](../../design-handoff.md)

# Design QA Process

## Overview

Design QA (Quality Assurance) is the process of verifying that the implemented product matches the intended design. It bridges the gap between what was designed and what was built, catching visual regressions, interaction discrepancies, and accessibility issues before users encounter them.

---

## Visual QA Checklist

### Typography Verification

- [ ] Font families match design specifications
- [ ] Font weights are correct for all text styles
- [ ] Font sizes match at all breakpoints
- [ ] Line heights produce correct visual spacing
- [ ] Letter spacing is applied where specified
- [ ] Text truncation works correctly (ellipsis, line clamping)
- [ ] Paragraph spacing matches design
- [ ] Text alignment is correct in all contexts
- [ ] Font rendering is clean (no sub-pixel issues, correct smoothing)

### Color Verification

- [ ] Background colors match design tokens
- [ ] Text colors match design tokens
- [ ] Border colors match specifications
- [ ] Interactive state colors correct (hover, focus, active, disabled)
- [ ] Status colors correct (success, warning, error, info)
- [ ] Gradient specifications match (direction, color stops)
- [ ] Opacity values correct for overlays and transparent elements
- [ ] Dark mode colors verified (if applicable)

### Spacing Verification

- [ ] Padding within components matches specifications
- [ ] Margins between components match specifications
- [ ] Grid gaps are correct
- [ ] Section spacing consistent with design
- [ ] Alignment is correct (centering, baseline alignment, edge alignment)
- [ ] Consistent spacing at all breakpoints

### Component Verification

- [ ] Border radius matches specifications
- [ ] Shadows match specifications (offset, blur, spread, color)
- [ ] Icon sizes match specifications per context
- [ ] Image aspect ratios maintained
- [ ] Component dimensions match (min/max width, height)

---

## Interaction QA Checklist

### Hover States

- [ ] All hoverable elements show hover effects
- [ ] Hover transitions are smooth (correct duration and easing)
- [ ] Hover does not trigger on touch devices (no sticky hover)
- [ ] Cursor changes appropriately (pointer for clickable, not-allowed for disabled)
- [ ] Hover effects are visually consistent with design specifications

### Focus States

- [ ] All focusable elements have visible focus indicators
- [ ] Focus ring meets contrast requirements (3:1 against adjacent colors)
- [ ] Focus-visible applies only on keyboard navigation (not mouse clicks)
- [ ] Focus ring does not cause layout shift
- [ ] Custom focus styles match design specifications

### Active/Pressed States

- [ ] Click/tap feedback is immediate and visible
- [ ] Active state visual treatment matches design
- [ ] Button depression effect (if specified) works correctly
- [ ] No delay between user action and visual feedback

### Disabled States

- [ ] Disabled elements are visually distinguished from enabled
- [ ] Disabled elements do not respond to hover
- [ ] Disabled elements do not respond to click/tap
- [ ] Disabled elements have correct cursor (not-allowed)
- [ ] Disabled elements have appropriate ARIA attributes

### Animations and Transitions

- [ ] Entry animations play correctly (direction, duration, easing)
- [ ] Exit animations play correctly
- [ ] Transition timing matches specifications
- [ ] Stagger timing correct for list/grid animations
- [ ] Animations respect prefers-reduced-motion
- [ ] No jank or frame drops during animations (60fps target)
- [ ] Loading spinners/skeletons display correctly

---

## Responsive QA Checklist

### Breakpoint Verification

Test at each defined breakpoint AND at intermediate sizes:

| Breakpoint | Width | Verification Items |
|-----------|-------|-------------------|
| Mobile small | 320px | Layout, typography, touch targets, content visibility |
| Mobile standard | 375px | Layout, images, navigation |
| Mobile large | 428px | Layout consistency |
| Tablet portrait | 768px | Grid changes, sidebar behavior, navigation |
| Tablet landscape | 1024px | Layout transitions, content density |
| Desktop small | 1280px | Full layout, sidebar, content width |
| Desktop standard | 1440px | Content max-width, spacing |
| Desktop large | 1920px | Content centering, background behavior |

### Layout Verification Per Breakpoint

- [ ] Grid columns adjust correctly at each breakpoint
- [ ] Content stacking order is logical on mobile
- [ ] No horizontal scrollbar appears (unless intentional, as in tables)
- [ ] Images scale and crop correctly
- [ ] Navigation transforms correctly (desktop to hamburger)
- [ ] Sidebar behavior matches specifications (hide, collapse, drawer)
- [ ] Modal/dialog sizing is appropriate for screen size
- [ ] Form layout adjusts correctly (stacked on mobile, inline on desktop)

### Content Reflow

- [ ] Content reflows at 320px width (WCAG 1.4.10)
- [ ] No content is lost when viewport narrows
- [ ] Text remains readable without horizontal scrolling
- [ ] Images do not overflow containers
- [ ] Tables have appropriate mobile treatment (scroll, collapse, or card layout)

---

## Accessibility QA Checklist

### Automated Testing

- [ ] axe-core reports 0 violations
- [ ] Lighthouse accessibility score above 95
- [ ] No console errors related to accessibility (missing labels, invalid ARIA)
- [ ] Valid HTML (no duplicate IDs, proper nesting)

### Keyboard Navigation

- [ ] All interactive elements reachable via Tab
- [ ] Tab order matches visual reading order
- [ ] No keyboard traps (except intentional modal traps)
- [ ] Escape closes modals, dropdowns, and popovers
- [ ] Enter/Space activates buttons and links
- [ ] Arrow keys navigate within composite widgets (tabs, menus)
- [ ] Skip link present and functional
- [ ] Focus returns correctly after modal close

### Screen Reader Testing

- [ ] All images have appropriate alt text
- [ ] Headings are hierarchical and descriptive
- [ ] Landmarks are correctly assigned (nav, main, aside, footer)
- [ ] Form fields have associated labels
- [ ] Error messages are announced (aria-live or role="alert")
- [ ] Status updates are announced (role="status")
- [ ] Dynamic content changes are communicated
- [ ] Custom widgets announce role, name, and state

### Visual Accessibility

- [ ] Text contrast meets 4.5:1 (AA) for normal text
- [ ] Text contrast meets 3:1 for large text
- [ ] UI component contrast meets 3:1
- [ ] Focus indicators meet 3:1 contrast
- [ ] Information not conveyed by color alone
- [ ] Text resizable to 200% without content loss
- [ ] Content readable with text spacing overrides applied

---

## Cross-Browser Testing

### Browser Matrix

| Browser | Priority | Versions |
|---------|----------|----------|
| Chrome | High | Latest 2 versions |
| Firefox | High | Latest 2 versions |
| Safari | High | Latest 2 versions |
| Edge | Medium | Latest 2 versions |
| Samsung Internet | Medium | Latest version |
| iOS Safari | High | Latest 2 iOS versions |
| Chrome Android | High | Latest version |

### Cross-Browser Verification

- [ ] Layout renders correctly in all target browsers
- [ ] Fonts render correctly (no missing glyphs, correct weights)
- [ ] CSS features degrade gracefully (backdrop-filter, container queries)
- [ ] JavaScript interactions work in all target browsers
- [ ] Form elements render acceptably (input types, date pickers)
- [ ] Scrolling behavior is consistent
- [ ] Animation performance is acceptable

---

## Device Testing Matrix

### Priority Devices

| Category | Devices | Key Tests |
|----------|---------|-----------|
| iPhone | SE (3rd gen), 15, 15 Pro Max | Touch targets, safe areas, Dynamic Island |
| Android | Pixel 7, Samsung Galaxy S24 | Various screen densities, system font sizes |
| Tablet | iPad (10th gen), iPad Pro | Landscape/portrait, split view |
| Desktop | MacBook Pro 14", Dell 27" monitor | Retina vs standard, wide aspect ratios |

---

## Bug Reporting Template

### Design QA Bug Report Format

```
Title: [Component/Page] - [Brief description of issue]

Severity: [Critical / High / Medium / Low]
Category: [Visual / Interaction / Responsive / Accessibility / Content]

Environment:
  Browser: Chrome 120
  Device: MacBook Pro 14"
  Viewport: 1440x900
  Theme: Light mode

Description:
  [What is the issue? What is wrong?]

Expected:
  [What should it look like/behave like? Reference the design specification.]

Actual:
  [What does it actually look like/behave like?]

Screenshot/Recording:
  [Attach screenshot or screen recording]

Design Reference:
  [Link to Figma frame/component showing expected state]

Steps to Reproduce:
  1. [Navigate to page/component]
  2. [Perform action]
  3. [Observe issue]
```

---

## Severity Levels

### Critical (P0)

- Feature is broken or unusable
- Data loss or security issue
- Blocking for launch
- Accessibility barrier preventing task completion

**Examples:** Form cannot be submitted, navigation links broken, keyboard trap with no escape, critical content invisible.

### High (P1)

- Feature works but with significant visual or interaction issues
- Noticeable deviation from design that affects user experience
- Accessibility issue affecting task efficiency

**Examples:** Wrong colors on primary CTA, missing hover states on all buttons, form labels not associated with inputs.

### Medium (P2)

- Minor visual discrepancy
- Inconsistency with design system
- Accessibility issue affecting polish but not function

**Examples:** Spacing off by 8px, wrong border radius on cards, missing loading state animation.

### Low (P3)

- Cosmetic issue unlikely to affect user experience
- "Nice to have" polish item
- Minor inconsistency

**Examples:** Subpixel rendering difference, icon 1px misaligned, transition easing slightly off.

---

## Pixel-Perfect vs Intent-Perfect

### The Spectrum of Fidelity

**Pixel-perfect:** Implementation matches design at the pixel level. Every measurement, color, and spacing is exact.

**Intent-perfect:** Implementation captures the intent and spirit of the design. Minor deviations are acceptable if the overall experience matches.

### Recommended Approach

Aim for **intent-perfect with defined tolerances:**

| Property | Tolerance | Rationale |
|----------|-----------|-----------|
| Colors | Exact match (token-based) | Tokens ensure exact mapping |
| Typography | Exact match | Tokens ensure exact mapping |
| Spacing | +/- 2px | Subpixel rendering can cause minor differences |
| Alignment | +/- 1px | Browser rendering differences |
| Border radius | Exact match | Usually a small set of values |
| Shadows | Visual match (not pixel-exact) | Rendering varies by browser |
| Animation timing | +/- 50ms | Perception threshold |

---

## Design QA Tools

| Tool | Purpose |
|------|---------|
| **Browser DevTools** | Inspect elements, measure spacing, check computed styles |
| **PixelSnap / xScope** | Measure on-screen dimensions and spacing |
| **Figma overlay** | Superimpose design over implementation for comparison |
| **Percy / Chromatic** | Visual regression testing (automated screenshot comparison) |
| **axe DevTools** | Automated accessibility testing |
| **Accessibility Insights** | Tab stop visualization, automated + manual testing |
| **Polypane** | Multi-viewport browser for responsive testing |

---

## QA Signoff Process

### Signoff Workflow

```
1. Developer marks feature as "Ready for Design QA"
2. Designer reviews against specifications using this checklist
3. Designer logs bugs with severity ratings
4. Developer addresses Critical and High bugs
5. Designer re-reviews fixed bugs
6. Designer marks feature as "Design QA Approved" or "Needs Revision"
7. Cycle repeats until approved
8. Final signoff documented in project management tool
```

### Signoff Criteria

Feature is approved when:
- Zero Critical (P0) bugs
- Zero High (P1) bugs
- Medium (P2) bugs triaged and scheduled (not blocking)
- Low (P3) bugs documented for backlog
- Accessibility automated tests pass
- Keyboard navigation verified
- Screen reader tested on primary flows
- Responsive layouts verified at defined breakpoints

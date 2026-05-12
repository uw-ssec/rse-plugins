---
name: accessibility-audit
description: Audit interfaces for WCAG 2.2 AA/AAA compliance covering perceivable, operable, understandable, and robust principles with ARIA patterns, keyboard navigation, color contrast verification, and inclusive design methodology.
metadata:
   references:
   - references/aria-patterns.md
   - references/contrast-guide.md
   - references/inclusive-design.md
   - references/keyboard-nav-guide.md
   - references/wcag-checklist.md
---

# Accessibility Audit

Accessibility is a requirement, not a feature. Every interface must be usable by people with permanent, temporary, and situational disabilities. This skill provides a systematic approach to auditing interfaces for WCAG 2.2 compliance, implementing ARIA patterns correctly, ensuring keyboard navigability, verifying color contrast, and applying inclusive design methodology.

An accessible interface is not a degraded version of the "real" interface. It is the real interface, built correctly from the start.

## Quick Start: Run an Accessibility Audit

Follow these six steps to audit any interface for accessibility compliance. Each step addresses a different category of barriers.

### Step 1: Check Semantic HTML

Semantic HTML is the foundation of accessibility. Screen readers, search engines, and assistive technologies rely on proper HTML elements to convey meaning.

- Verify the page has exactly one `<h1>` that describes the page purpose
- Confirm heading levels follow a logical hierarchy (H1 > H2 > H3) with no skipped levels
- Check that `<nav>`, `<main>`, `<aside>`, `<header>`, `<footer>` landmarks are used correctly
- Ensure lists use `<ul>`, `<ol>`, or `<dl>` rather than styled `<div>` elements
- Verify tables use `<th>`, `<caption>`, and proper `scope` attributes for data tables
- Confirm that `<button>` is used for actions and `<a>` is used for navigation

### Step 2: Test Keyboard Navigation

Every interactive element must be reachable and operable with a keyboard alone.

- Tab through the entire page from start to finish; verify logical focus order
- Confirm all interactive elements (links, buttons, inputs, custom controls) receive focus
- Test that custom components respond to expected keys (Enter, Space, Escape, Arrow keys)
- Verify no keyboard traps exist (focus can always be moved away from any element)
- Check that skip links are present and functional (skip to main content)
- Confirm modal dialogs trap focus within themselves and restore focus on close

### Step 3: Verify ARIA Usage

ARIA supplements HTML semantics but must never be used as a replacement for semantic HTML.

- Check that ARIA roles are used only when no native HTML element provides the semantics
- Verify all `aria-labelledby` and `aria-describedby` references point to existing element IDs
- Confirm `aria-expanded`, `aria-selected`, `aria-checked` states update dynamically
- Ensure `aria-live` regions announce dynamic content changes appropriately
- Validate that `aria-hidden="true"` is not applied to focusable elements
- Run an ARIA validator (axe, WAVE) to catch invalid attribute usage

### Step 4: Check Color Contrast

Insufficient contrast is the most common accessibility failure on the web.

- Test all text against its background using a contrast checker
- Normal text: minimum 4.5:1 ratio (AA), 7:1 ratio (AAA)
- Large text (18pt regular or 14pt bold): minimum 3:1 ratio (AA), 4.5:1 ratio (AAA)
- Non-text UI components and graphical objects: minimum 3:1 ratio
- Check contrast in all themes (light mode, dark mode, high contrast)
- Verify that focus indicators have sufficient contrast against all backgrounds

### Step 5: Test with Screen Reader

Automated tools catch approximately 30% of accessibility issues. Screen reader testing catches what automation misses.

- Test with at least one screen reader (VoiceOver on macOS, NVDA on Windows, TalkBack on Android)
- Verify all images have meaningful `alt` text (or `alt=""` for decorative images)
- Confirm form fields announce their labels and error states
- Test that dynamic content changes (alerts, notifications, live regions) are announced
- Verify custom components announce their role, name, and state correctly
- Check that the reading order matches the visual order

### Step 6: Review Content Accessibility

Content itself must be accessible beyond just its visual presentation.

- Verify link text is descriptive (not "click here" or "read more")
- Check that the page language is declared with `lang` attribute on `<html>`
- Confirm error messages clearly identify the field and describe how to fix the error
- Test that time-limited content provides mechanisms to extend or disable timers
- Verify multimedia has captions (video), transcripts (audio), and audio descriptions where needed
- Check that content does not rely solely on sensory characteristics (color, shape, position)

## WCAG 2.2 Overview

WCAG 2.2 organizes accessibility requirements under four principles, collectively known as POUR. Each principle contains guidelines, and each guideline contains testable success criteria at three conformance levels: A (minimum), AA (standard target), and AAA (enhanced).

### Perceivable

Information and user interface components must be presentable to users in ways they can perceive.

| Criterion | Level | Description |
|-----------|-------|-------------|
| **1.1.1 Non-text Content** | A | All non-text content has a text alternative that serves the equivalent purpose |
| **1.2.1 Audio-only and Video-only** | A | Alternatives provided for prerecorded audio-only and video-only media |
| **1.3.1 Info and Relationships** | A | Information, structure, and relationships conveyed visually are available programmatically |
| **1.3.2 Meaningful Sequence** | A | The reading sequence can be programmatically determined |
| **1.3.3 Sensory Characteristics** | A | Instructions do not rely solely on shape, color, size, position, or sound |
| **1.4.1 Use of Color** | A | Color is not used as the sole visual means of conveying information |
| **1.4.3 Contrast (Minimum)** | AA | Text has a contrast ratio of at least 4.5:1 (3:1 for large text) |
| **1.4.4 Resize Text** | AA | Text can be resized up to 200% without loss of content or functionality |
| **1.4.5 Images of Text** | AA | Text is used instead of images of text wherever possible |
| **1.4.11 Non-text Contrast** | AA | UI components and graphical objects have a contrast ratio of at least 3:1 |
| **1.4.12 Text Spacing** | AA | Content adapts to increased spacing without loss of information |
| **1.4.13 Content on Hover or Focus** | AA | Additional content triggered by hover/focus is dismissible, hoverable, and persistent |

### Operable

User interface components and navigation must be operable by all users.

| Criterion | Level | Description |
|-----------|-------|-------------|
| **2.1.1 Keyboard** | A | All functionality is available from a keyboard |
| **2.1.2 No Keyboard Trap** | A | Keyboard focus can be moved away from any component |
| **2.4.1 Bypass Blocks** | A | A mechanism is available to bypass repeated blocks of content |
| **2.4.2 Page Titled** | A | Pages have titles that describe topic or purpose |
| **2.4.3 Focus Order** | A | Focusable components receive focus in a meaningful sequence |
| **2.4.4 Link Purpose** | A | The purpose of each link can be determined from the link text or context |
| **2.4.6 Headings and Labels** | AA | Headings and labels describe topic or purpose |
| **2.4.7 Focus Visible** | AA | Keyboard focus indicator is visible |
| **2.4.11 Focus Not Obscured (Minimum)** | AA | Focused element is not entirely hidden by other content *(new in 2.2)* |
| **2.5.7 Dragging Movements** | AA | Functionality using dragging has a single-pointer alternative *(new in 2.2)* |
| **2.5.8 Target Size (Minimum)** | AA | Interactive targets are at least 24x24 CSS pixels *(new in 2.2)* |

### Understandable

Information and the operation of the user interface must be understandable.

| Criterion | Level | Description |
|-----------|-------|-------------|
| **3.1.1 Language of Page** | A | The default human language of each page can be programmatically determined |
| **3.1.2 Language of Parts** | AA | The language of each passage or phrase can be programmatically determined |
| **3.2.1 On Focus** | A | Components do not initiate a change of context when receiving focus |
| **3.2.2 On Input** | A | Changing a setting does not automatically cause a change of context |
| **3.2.6 Consistent Help** | A | Help mechanisms are presented in a consistent relative order *(new in 2.2)* |
| **3.3.1 Error Identification** | A | Input errors are automatically detected and described to the user in text |
| **3.3.2 Labels or Instructions** | A | Labels or instructions are provided for user input |
| **3.3.3 Error Suggestion** | AA | Suggestions for correcting input errors are provided when known |
| **3.3.7 Redundant Entry** | A | Information previously entered is auto-populated or available for selection *(new in 2.2)* |
| **3.3.8 Accessible Authentication (Minimum)** | AA | Authentication does not require cognitive function tests unless alternatives exist *(new in 2.2)* |

### Robust

Content must be robust enough to be interpreted by a wide variety of user agents, including assistive technologies.

| Criterion | Level | Description |
|-----------|-------|-------------|
| **4.1.2 Name, Role, Value** | A | All UI components have accessible names, roles, and states that can be programmatically determined |
| **4.1.3 Status Messages** | AA | Status messages can be programmatically determined without receiving focus |

## Common Accessibility Failures

These ten failures account for the vast majority of accessibility barriers found in audits. Fix these first for maximum impact.

| # | Failure | Quick Fix |
|---|---------|-----------|
| 1 | **Missing alt text** | Add descriptive `alt` to informative images; use `alt=""` for decorative images |
| 2 | **Low contrast text** | Increase contrast ratio to at least 4.5:1 for normal text, 3:1 for large text |
| 3 | **Missing form labels** | Associate every input with a `<label>` using matching `for`/`id` attributes |
| 4 | **No keyboard access** | Ensure all interactive elements are focusable; add `tabindex` and key event handlers to custom controls |
| 5 | **Missing focus indicators** | Never remove `outline` without providing a visible replacement; use `:focus-visible` for styling |
| 6 | **ARIA misuse** | Use semantic HTML elements first; only add ARIA when no native element provides the needed semantics |
| 7 | **Auto-playing media** | Provide a visible pause/stop control; respect `prefers-reduced-motion` media query |
| 8 | **Missing heading structure** | Use a proper H1-H6 hierarchy that reflects content structure; never skip heading levels |
| 9 | **Color-only indicators** | Add icons, text labels, or patterns alongside color to convey meaning |
| 10 | **Inaccessible custom controls** | Follow WAI-ARIA Authoring Practices patterns or replace with native HTML elements |

## Automated vs. Manual Testing

Automated accessibility testing catches approximately 30% of WCAG violations. The remaining 70% requires human judgment.

### What Automation Catches Well

- Missing alt text attributes
- Color contrast ratio violations
- Missing form labels
- Invalid ARIA attributes and roles
- Duplicate IDs
- Missing document language
- Empty buttons and links

**Recommended tools**: axe-core (browser extension and CI integration), Lighthouse (built into Chrome DevTools), WAVE (browser extension), pa11y (CLI tool for CI pipelines).

### What Requires Manual Testing

- Meaningful alt text quality (automation detects presence, not quality)
- Logical focus order and keyboard flow
- Screen reader experience and announcement quality
- Cognitive accessibility (clear language, logical flow)
- Context-dependent ARIA correctness
- Dynamic content updates and live region behavior
- Zoom and reflow at 200% and 400%
- Touch target adequacy on mobile devices

### Testing Strategy

1. **Automated first**: Run axe-core on every page. Fix all reported issues. This is the baseline.
2. **Keyboard audit**: Tab through every page and interactive flow. Document any elements that are unreachable, trapped, or out of order.
3. **Screen reader audit**: Test critical user flows with VoiceOver (macOS/iOS) and NVDA (Windows). Focus on forms, navigation, dynamic content, and error handling.
4. **Visual audit**: Check zoom behavior at 200% and 400%, verify focus indicators, test all color themes.
5. **Cognitive audit**: Review content clarity, error message helpfulness, navigation consistency, and form complexity.

## Deep Dive References

### [WCAG Checklist](references/wcag-checklist.md)

- Perceivable
- Operable
- Understandable
- Robust
- Testing Workflow
- Accessibility Audit: [Page/Component Name]

### [ARIA Patterns](references/aria-patterns.md)

- Dialog / Modal
- Tabs
- Accordion
- Combobox / Autocomplete
- Menu / Menubar
- Tooltip
- Tree View
- Alert and Live Regions

### [Keyboard Navigation Guide](references/keyboard-nav-guide.md)

- Focus Management Fundamentals
- Tab Order Optimization
- Roving Tabindex
- Focus Trapping
- Skip Navigation Links
- Keyboard Interaction Patterns
- Focus-Visible Styling

### [Contrast Guide](references/contrast-guide.md)

- Contrast Ratio Requirements
- Testing Tools
- Common Contrast Failures
- Non-Text Contrast
- Fixing Low-Contrast Patterns
- Contrast in Theming

### [Inclusive Design](references/inclusive-design.md)

- Inclusive Design Principles
- The Disability Spectrum
- Cognitive Accessibility
- Neurodivergent-Friendly Design
- Inclusive Interaction Patterns
- Measuring Inclusive Design

## Next Steps

After completing an accessibility audit, continue building inclusive interfaces:

- **[Inclusive Design](references/inclusive-design.md)**: Move beyond compliance to design that includes the widest possible range of users
- **[UX Writing](../ux-writing/SKILL.md)**: Write clear, helpful error messages and microcopy that supports all users
- **[Color Systems](../color-systems/SKILL.md)**: Build color palettes with contrast requirements baked in from the start
- **[Frontend Components](../frontend-components/SKILL.md)**: Implement accessible component patterns across React, Vue, Svelte, and Web Components

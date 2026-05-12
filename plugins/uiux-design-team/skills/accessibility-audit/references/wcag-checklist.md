# WCAG Checklist

Complete WCAG 2.2 Level A and AA success criteria organized by POUR principle (Perceivable, Operable, Understandable, Robust). Each criterion includes a description, common failure, fix example, and testing method for systematic accessibility compliance verification.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Perceivable](#perceivable) | 14-80 | Text alternatives, time-based media, adaptable content, and distinguishable presentation |
| [Operable](#operable) | 82-150 | Keyboard access, timing, seizures, navigation, and input modalities |
| [Understandable](#understandable) | 152-210 | Readable content, predictable behavior, and input assistance |
| [Robust](#robust) | 212-235 | Compatible markup and status messages |
| [Testing Workflow](#testing-workflow) | 237-265 | Automated, manual, and assistive technology testing sequence |
| [See Also](#see-also) | 267-273 | Related references and skills |

## Perceivable

Information and user interface components must be presentable to users in ways they can perceive.

### 1.1.1 Non-text Content (Level A)

**Requirement**: All non-text content has a text alternative that serves the equivalent purpose.

**Common failure**: Images used for information (icons, charts, infographics) missing `alt` text. Decorative images with non-empty `alt` text cluttering screen reader output.

**Fix**: Informative images get descriptive `alt`. Decorative images get `alt=""`. Complex images (charts, diagrams) get a brief `alt` plus a longer text description via `aria-describedby` or an adjacent text block.

**Test**: Run axe-core. Manually review `alt` text quality -- automation detects presence, not quality.

### 1.3.1 Info and Relationships (Level A)

**Requirement**: Information, structure, and relationships conveyed visually are available programmatically.

**Common failure**: Using `<div>` and CSS to create headings, lists, or tables instead of semantic HTML. Form fields visually grouped but not programmatically associated.

**Fix**: Use proper `<h1>`-`<h6>`, `<ul>`/`<ol>`, `<table>`, `<fieldset>`/`<legend>`. Associate labels with inputs using `for`/`id`.

**Test**: Disable CSS and verify the page still makes structural sense. Screen reader heading navigation should list all headings in order.

### 1.3.2 Meaningful Sequence (Level A)

**Requirement**: The reading sequence can be programmatically determined when it affects meaning.

**Common failure**: CSS reorders content visually but the DOM order is illogical. Flexbox `order` property creates a visual sequence that differs from the reading sequence.

**Fix**: Ensure DOM order matches visual order. If CSS reordering is necessary, verify screen reader and keyboard navigation follow a logical path.

**Test**: Tab through the page and verify focus order matches visual order. Linearize the page (disable CSS) and verify reading sequence.

### 1.4.1 Use of Color (Level A)

**Requirement**: Color is not used as the sole visual means of conveying information.

**Common failure**: Required form fields indicated only by red text. Error states shown only by changing border color. Chart data distinguished only by color.

**Fix**: Add text labels ("Required"), icons (warning triangle for errors), or patterns (hatching in charts) alongside color.

**Test**: View the interface in grayscale. All information should still be conveyed.

### 1.4.3 Contrast Minimum (Level AA)

**Requirement**: Text has a contrast ratio of at least 4.5:1 (normal text) or 3:1 (large text -- 18pt regular or 14pt bold).

**Common failure**: Light gray text on white backgrounds. Placeholder text with insufficient contrast. White text on light-colored brand backgrounds.

**Fix**: Adjust text or background color to meet ratio. Use a contrast checker during design, not after.

**Test**: Use axe-core, Lighthouse, or browser DevTools contrast checker. Check all themes (light, dark, high contrast).

### 1.4.4 Resize Text (Level AA)

**Requirement**: Text can be resized up to 200% without loss of content or functionality.

**Common failure**: Fixed-height containers cause text overflow. Absolutely positioned elements overlap when text is enlarged.

**Fix**: Use relative units (rem, em). Avoid fixed heights on text containers. Test with browser zoom at 200%.

**Test**: Set browser zoom to 200%. Verify all text is visible and no content is clipped or overlapped.

### 1.4.11 Non-text Contrast (Level AA)

**Requirement**: UI components (form controls, icons) and graphical objects have a contrast ratio of at least 3:1 against adjacent colors.

**Common failure**: Light gray borders on input fields. Icon-only buttons with insufficient contrast. Focus indicators that do not contrast with the background.

**Fix**: Ensure borders, icons, and interactive element boundaries meet 3:1 ratio.

**Test**: Use a contrast checker on UI element borders and icons against their backgrounds.

### 1.4.12 Text Spacing (Level AA)

**Requirement**: Content adapts without loss of information when users override line height to 1.5x, paragraph spacing to 2x, letter spacing to 0.12em, and word spacing to 0.16em.

**Common failure**: Fixed-height containers truncate text when spacing increases. Overlapping text or hidden overflow.

**Fix**: Use min-height instead of fixed height. Avoid `overflow: hidden` on text containers. Test with a text spacing bookmarklet.

**Test**: Apply text spacing overrides via browser extension or bookmarklet. Verify no content is lost.

### 1.4.13 Content on Hover or Focus (Level AA)

**Requirement**: Additional content triggered by hover or focus is dismissible (Escape), hoverable (user can move pointer to it), and persistent (stays visible until dismissed).

**Common failure**: Tooltips that disappear when the user moves to them. Popover content that cannot be dismissed without moving focus.

**Fix**: Ensure tooltips/popovers stay visible when hovered. Add Escape to dismiss. Do not auto-dismiss based on timeout.

**Test**: Hover over triggering elements. Move pointer to the additional content. Press Escape. Verify all three behaviors.

## Operable

User interface components and navigation must be operable by all users.

### 2.1.1 Keyboard (Level A)

**Requirement**: All functionality is available from a keyboard.

**Common failure**: Drag-and-drop without keyboard alternative. Custom controls only responding to click events. Hover-only interactions.

**Fix**: Add keyboard handlers (`onKeyDown`) to all interactive elements. Provide keyboard alternatives for drag-and-drop (move buttons, arrow key reordering).

**Test**: Unplug the mouse. Navigate the entire interface using only keyboard. Every action must be achievable.

### 2.1.2 No Keyboard Trap (Level A)

**Requirement**: Keyboard focus can be moved away from any component using standard navigation keys.

**Common failure**: Modal dialogs that trap focus but do not provide an exit mechanism. Embedded content (iframes, video players) that capture keyboard events.

**Fix**: Modal focus traps must release focus on Escape. Ensure all embedded content allows Tab to exit.

**Test**: Tab into every component. Verify you can always Tab or Escape out.

### 2.4.1 Bypass Blocks (Level A)

**Requirement**: A mechanism is available to bypass repeated blocks of content.

**Common failure**: No skip navigation link. Long navigation menus that must be tabbed through on every page.

**Fix**: Add a "Skip to main content" link as the first focusable element. Use ARIA landmarks (`<nav>`, `<main>`, `<aside>`).

**Test**: Tab from the top of the page. Verify a skip link appears and jumps focus to the main content.

### 2.4.3 Focus Order (Level A)

**Requirement**: Focusable components receive focus in a meaningful sequence.

**Common failure**: Tab order jumps between unrelated sections. Modal opens but focus stays behind the overlay. `tabindex` values greater than 0 creating unpredictable order.

**Fix**: Ensure DOM order matches visual order. Move focus to modals when opened. Never use `tabindex` greater than 0.

**Test**: Tab through every page and verify focus moves in a logical, predictable sequence.

### 2.4.7 Focus Visible (Level AA)

**Requirement**: Keyboard focus indicator is visible on all interactive elements.

**Common failure**: CSS `outline: none` without a replacement. Focus indicator indistinguishable from the element's default state. Focus indicator invisible on certain backgrounds.

**Fix**: Use `:focus-visible` to style a visible focus ring. Ensure the ring contrasts with all backgrounds.

```css
:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}
```

**Test**: Tab through the interface. Every focused element must have a clearly visible indicator.

### 2.4.11 Focus Not Obscured (Level AA) -- New in 2.2

**Requirement**: The focused element is not entirely hidden by other content (sticky headers, cookie banners, floating toolbars).

**Common failure**: Sticky navigation covers focused elements as the user tabs down the page.

**Fix**: Add `scroll-padding-top` equal to the sticky header height. Ensure floating elements do not fully occlude the focus indicator.

**Test**: Tab through pages with sticky headers. Verify focused elements are never fully obscured.

### 2.5.7 Dragging Movements (Level AA) -- New in 2.2

**Requirement**: Functionality that uses dragging has a single-pointer alternative.

**Common failure**: Kanban boards, sliders, and reorderable lists that only support drag-and-drop.

**Fix**: Add move buttons, select-then-place patterns, or arrow key alternatives alongside drag-and-drop.

**Test**: Attempt all drag-and-drop interactions using only a single pointer (click/tap) without dragging.

### 2.5.8 Target Size Minimum (Level AA) -- New in 2.2

**Requirement**: Interactive targets are at least 24x24 CSS pixels, unless the target is inline text, the user agent default, or there is sufficient spacing.

**Common failure**: Small icon buttons, close buttons, and navigation links below 24px.

**Fix**: Set minimum `min-width` and `min-height` of 24px on all interactive elements. For inline links, ensure adequate spacing.

**Test**: Use DevTools to measure interactive elements. Verify all meet 24x24px minimum.

## Understandable

Information and the operation of the user interface must be understandable.

### 3.1.1 Language of Page (Level A)

**Requirement**: The default human language of each page can be programmatically determined.

**Common failure**: Missing `lang` attribute on the `<html>` element.

**Fix**: Add `<html lang="en">` (or appropriate language code).

**Test**: Inspect the `<html>` element. Verify `lang` attribute is present and correct.

### 3.2.1 On Focus (Level A)

**Requirement**: Components do not initiate a change of context when receiving focus.

**Common failure**: Navigating to a form field triggers a page redirect. Focusing a dropdown automatically opens and changes page content.

**Fix**: Changes of context require explicit user action (click, Enter), never just focus.

**Test**: Tab to every interactive element. Verify no unexpected navigation, form submission, or context change occurs.

### 3.3.1 Error Identification (Level A)

**Requirement**: Input errors are automatically detected and described to the user in text.

**Common failure**: Error indicated only by red border with no text message. Generic "Form has errors" without identifying which field.

**Fix**: Display a specific error message adjacent to each invalid field. Use `aria-describedby` to associate the error with the input.

**Test**: Submit forms with invalid data. Verify each error is identified by text, not just color.

### 3.3.3 Error Suggestion (Level AA)

**Requirement**: When an input error is detected and suggestions are known, they are provided to the user.

**Common failure**: "Invalid email" without explaining the expected format. "Password too short" without stating the minimum length.

**Fix**: "Email must be in the format name@example.com" or "Password must be at least 8 characters."

**Test**: Trigger validation errors. Verify each error message explains how to fix the problem.

### 3.3.7 Redundant Entry (Level A) -- New in 2.2

**Requirement**: Information previously entered is auto-populated or available for selection when needed again.

**Common failure**: Multi-step forms that ask for the same information (address, email) on multiple steps.

**Fix**: Pre-fill previously entered data. Use select menus to choose from previously provided options.

**Test**: Complete multi-step flows. Verify no information is requested more than once unless security requires it.

### 3.3.8 Accessible Authentication (Level AA) -- New in 2.2

**Requirement**: Authentication does not require cognitive function tests (puzzles, memory) unless alternatives exist.

**Common failure**: CAPTCHA puzzles without audio or alternative options. Password-only login without passkey or autofill support.

**Fix**: Support password managers (do not block paste). Provide passkey/biometric alternatives. Use accessible CAPTCHA alternatives.

**Test**: Attempt authentication using a password manager. Verify paste is not blocked. Verify CAPTCHA has alternatives.

## Robust

Content must be robust enough to be interpreted by assistive technologies.

### 4.1.2 Name, Role, Value (Level A)

**Requirement**: All UI components have accessible names, roles, and states that can be programmatically determined.

**Common failure**: Custom components without ARIA roles. Buttons with no accessible name (icon-only without `aria-label`). State changes (expanded, selected, checked) not communicated.

**Fix**: Use semantic HTML or add ARIA attributes. Ensure every interactive element has an accessible name. Update `aria-expanded`, `aria-selected`, `aria-checked` dynamically.

**Test**: Run axe-core. Use a screen reader to navigate all custom components. Verify role, name, and state are announced correctly.

### 4.1.3 Status Messages (Level AA)

**Requirement**: Status messages can be programmatically determined without receiving focus.

**Common failure**: Success messages, error counts, and search result counts that appear visually but are not announced to screen readers.

**Fix**: Use `role="status"` or `aria-live="polite"` for non-urgent status. Use `role="alert"` for urgent messages.

```html
<div role="status" aria-live="polite">3 results found</div>
<div role="alert">Your session will expire in 2 minutes</div>
```

**Test**: Trigger status messages with a screen reader active. Verify they are announced without focus moving.

## Testing Workflow

### Recommended Sequence

1. **Automated scan**: Run axe-core or Lighthouse on every page. Fix all reported issues. This catches approximately 30% of barriers.

2. **Keyboard audit**: Tab through every page. Document unreachable elements, keyboard traps, and illogical focus order.

3. **Screen reader audit**: Test critical user flows with VoiceOver (macOS) or NVDA (Windows). Focus on forms, navigation, dynamic content, and error handling.

4. **Visual audit**: Check zoom at 200% and 400%. Verify focus indicators. Test all color themes for contrast.

5. **Cognitive audit**: Review error messages, form complexity, navigation consistency, and content clarity.

### Automated Tools

| Tool | Type | Best For |
|------|------|----------|
| **axe-core** | Browser extension, CI | Comprehensive rule coverage, developer-friendly |
| **Lighthouse** | Chrome DevTools | Quick overview, performance + a11y |
| **WAVE** | Browser extension | Visual overlay of issues on page |
| **pa11y** | CLI, CI | Automated pipeline testing |
| **eslint-plugin-jsx-a11y** | Linter | Catch issues during development |

### Testing Checklist Template

```markdown
## Accessibility Audit: [Page/Component Name]

- [ ] Automated scan (axe/Lighthouse) -- 0 violations
- [ ] Keyboard navigation -- all elements reachable, no traps
- [ ] Focus indicators -- visible on all interactive elements
- [ ] Screen reader -- roles, names, states announced correctly
- [ ] Color contrast -- all text meets 4.5:1 (AA)
- [ ] Zoom 200% -- no content loss or overlap
- [ ] Error handling -- errors identified, described, and recoverable
- [ ] Dynamic content -- live regions announce updates
```

## See Also

- [[aria-patterns.md]] -- Correct ARIA implementations for common widget patterns
- [[keyboard-nav-guide.md]] -- Focus management, roving tabindex, and keyboard interaction patterns
- [[contrast-guide.md]] -- Color contrast ratios, testing tools, and fix strategies
- [[inclusive-design.md]] -- Designing beyond compliance for the widest range of users
- [[../../design-handoff/references/qa-process.md]] -- Design QA process including accessibility verification

**Back to:** [Accessibility Audit Skill](../SKILL.md)

[Back to Design Handoff](../../design-handoff.md)

# Design Handoff Checklist

## Overview

A complete design handoff ensures developers have everything they need to implement a design accurately without guesswork. This checklist covers every aspect of handoff, from visual specifications to accessibility requirements to QA criteria.

---

## Visual Specifications

### Colors

- [ ] All colors specified using design token names (not raw hex values)
- [ ] Token names map to documented design token system
- [ ] Background colors for all surfaces (page, card, modal, sidebar)
- [ ] Text colors for all hierarchy levels (primary, secondary, disabled)
- [ ] Border colors for all UI components
- [ ] Interactive colors (hover, focus, active, selected states)
- [ ] Status colors (success, warning, error, info)
- [ ] Dark mode color mappings (if applicable)
- [ ] Opacity values for overlays, scrims, disabled states

### Typography

- [ ] Font family for each text style (headings, body, code, labels)
- [ ] Font weight for each text style
- [ ] Font size (px and rem)
- [ ] Line height (px and unitless ratio)
- [ ] Letter spacing (if non-default)
- [ ] Text transform (uppercase, capitalize, none)
- [ ] Maximum line lengths / container widths for readability
- [ ] Truncation rules (ellipsis after N lines, truncation point)
- [ ] Font files or CDN links provided (with licensing confirmation)

### Spacing

- [ ] Component internal padding (top, right, bottom, left or shorthand)
- [ ] Margins between components
- [ ] Grid gap values
- [ ] Section spacing (vertical rhythm between page sections)
- [ ] Spacing scale reference (link to design tokens or spacing system)
- [ ] Alignment specifications (flex alignment, text alignment)

### Icons and Imagery

- [ ] Icon set identified (library name, version)
- [ ] Icon sizes for each context (16px inline, 24px standard, 32px large)
- [ ] Icon color specifications (inherit text color, or specific token)
- [ ] Custom icons exported as SVG (optimized, with consistent viewBox)
- [ ] Image aspect ratios defined per context
- [ ] Image placeholder / fallback behavior specified
- [ ] Image loading strategy (lazy, eager, priority)

### Borders, Shadows, and Effects

- [ ] Border radius values for all component types
- [ ] Border width and style (solid, dashed, none)
- [ ] Box shadow specifications (offset, blur, spread, color)
- [ ] Elevation levels mapped to shadow values
- [ ] Background blur / backdrop-filter values (if used)
- [ ] Gradient specifications (type, direction, color stops)

---

## Interaction Specifications

### Hover States

- [ ] Background color change
- [ ] Text color change
- [ ] Border change
- [ ] Shadow change (elevation lift)
- [ ] Scale or transform
- [ ] Cursor type (pointer, default, not-allowed)
- [ ] Transition duration and easing

### Focus States

- [ ] Focus ring color and width
- [ ] Focus ring offset
- [ ] Focus-within behavior (for containers like cards)
- [ ] Differentiation between focus and focus-visible
- [ ] Focus ring appearance on dark backgrounds
- [ ] High contrast mode focus appearance

### Active/Pressed States

- [ ] Background color change
- [ ] Scale transform (if any)
- [ ] Shadow reduction (pressed-in effect)
- [ ] Duration of visual feedback

### Disabled States

- [ ] Visual treatment (opacity, color changes, grayscale)
- [ ] Cursor type (not-allowed)
- [ ] Interactive behavior (no hover effects, no click response)
- [ ] ARIA attribute (aria-disabled="true")

### Loading States

- [ ] Skeleton screen designs (if used)
- [ ] Spinner placement and size
- [ ] Loading text (if any)
- [ ] Button loading state (spinner replaces text, or inline spinner)
- [ ] Progressive loading behavior (what appears first)
- [ ] Minimum loading time (to prevent flash of loading state)

### Animation and Transitions

- [ ] Transition properties (which CSS properties animate)
- [ ] Duration for each transition type (micro: 100-200ms, standard: 200-400ms, complex: 400-600ms)
- [ ] Easing function (ease-out for entering, ease-in for exiting, ease-in-out for moving)
- [ ] Reduced motion alternative (prefers-reduced-motion behavior)
- [ ] Stagger timing for lists/grids (if applicable)
- [ ] Entry/exit animation specifications (from/to values)

---

## Responsive Behavior

### Breakpoints

- [ ] Breakpoint values defined (e.g., 320px, 768px, 1024px, 1280px, 1536px)
- [ ] Design provided for each relevant breakpoint
- [ ] Behavior between breakpoints documented (fluid or fixed)
- [ ] Container width maximums per breakpoint
- [ ] Preferred breakpoint system (min-width or max-width)

### Layout Changes

- [ ] Grid column changes per breakpoint
- [ ] Component stacking behavior (side-by-side to vertical)
- [ ] Sidebar visibility and behavior changes
- [ ] Navigation transformation (full to hamburger)
- [ ] Hero section layout changes
- [ ] Card layout changes (columns, sizing)
- [ ] Table behavior on small screens (horizontal scroll, card layout, or hide columns)

### Element Visibility

- [ ] Elements hidden at specific breakpoints (desktop-only, mobile-only)
- [ ] Show/hide rules documented
- [ ] Alternative content for hidden elements (e.g., mobile menu replaces desktop nav)

### Typography Scaling

- [ ] Heading size changes per breakpoint
- [ ] Body text size adjustments
- [ ] Line length management per breakpoint
- [ ] Spacing adjustments per breakpoint

---

## Content Specifications

### Copy and Text

- [ ] All UI copy provided (button labels, headings, descriptions)
- [ ] Placeholder text specified (form placeholders)
- [ ] Error messages for all validation scenarios
- [ ] Success messages for all action confirmations
- [ ] Empty state copy
- [ ] Loading state copy (if any)
- [ ] Tooltip text
- [ ] Maximum character counts per field/element

### Translations and Internationalization

- [ ] Strings identified for translation
- [ ] Text expansion allowances (up to 40% for German, 30% for French)
- [ ] RTL layout requirements (if applicable)
- [ ] Date, time, and number format specifications
- [ ] Currency display format
- [ ] Cultural considerations noted (color meaning, imagery, icons)

---

## Accessibility Requirements

### Structure

- [ ] Heading hierarchy defined (h1 through h6, no skipped levels)
- [ ] Landmark regions identified (nav, main, aside, footer)
- [ ] List structure identified (where to use ul, ol, dl)
- [ ] Table header scope defined (row, column)

### Interactive Elements

- [ ] ARIA roles for custom components
- [ ] ARIA states (expanded, selected, checked, pressed)
- [ ] Keyboard navigation patterns for each custom widget
- [ ] Focus management instructions (where focus goes on modal open/close, route change)
- [ ] Tab order verification (matches visual order)
- [ ] Skip link targets defined

### Content

- [ ] Alt text for all meaningful images
- [ ] Decorative images marked (alt="")
- [ ] Icon labels (aria-label or visually hidden text)
- [ ] Link text is descriptive (no "click here" or "read more")
- [ ] Form labels associated with inputs
- [ ] Error messages associated with fields (aria-describedby)

### Visual

- [ ] Color contrast verified (4.5:1 for text, 3:1 for UI components)
- [ ] Information not conveyed by color alone
- [ ] Focus indicators visible (3:1 contrast against adjacent colors)
- [ ] Touch targets meet minimum 24x24px (44x44px recommended)
- [ ] Text resizable to 200% without content loss
- [ ] Content reflows at 320px width without horizontal scrolling

---

## Asset Delivery

### Images

- [ ] Images exported in appropriate formats (WebP, PNG for transparency, JPEG for photos, SVG for vector)
- [ ] Multiple resolutions provided (1x, 2x, 3x) or source vector
- [ ] Image naming convention documented
- [ ] Image optimization performed (compressed without visible quality loss)
- [ ] Responsive image sources provided (srcset breakpoints)

### Icons

- [ ] Icon SVGs exported with consistent viewBox
- [ ] SVGs optimized (unnecessary paths removed, attributes cleaned)
- [ ] Icon naming convention matches design token names
- [ ] Sprite sheet or individual files (strategy documented)

### Fonts

- [ ] Font files provided (WOFF2 preferred, WOFF fallback)
- [ ] Font licensing verified for web use
- [ ] Font subset if full character set not needed
- [ ] Font display strategy specified (swap, optional, block)
- [ ] Fallback font stack specified

---

## Technical Constraints

### Performance

- [ ] Image size budgets communicated
- [ ] Animation performance considerations (GPU-accelerated properties preferred)
- [ ] Component lazy loading requirements
- [ ] Above-the-fold priority content identified
- [ ] Third-party script impact considered

### Browser and Device Support

- [ ] Target browser list defined
- [ ] Known CSS feature limitations noted (backdrop-filter, container queries, etc.)
- [ ] Progressive enhancement strategy documented
- [ ] Device testing priorities defined (which devices are critical)

### Integration

- [ ] API data structure awareness (what data is available for display)
- [ ] Dynamic content considerations (user-generated content, variable-length data)
- [ ] Authentication state variations (logged in vs. logged out views)
- [ ] Permission-based view variations

---

## QA Criteria

### Visual QA

- [ ] Design matches annotations at each breakpoint
- [ ] Colors match design tokens
- [ ] Typography matches specifications
- [ ] Spacing matches measurements
- [ ] Interactive states match designs (hover, focus, active, disabled)
- [ ] Animations match motion specifications

### Functional QA

- [ ] All interactive elements functional
- [ ] Form validation works as specified
- [ ] Navigation works correctly
- [ ] Edge cases handled (empty states, errors, long content)
- [ ] Loading states appear and resolve correctly

### Accessibility QA

- [ ] Keyboard navigation works for all interactions
- [ ] Screen reader announces all content correctly
- [ ] Color contrast meets requirements
- [ ] Focus indicators visible
- [ ] ARIA attributes correct

### Cross-Browser/Device QA

- [ ] Tested on target browsers
- [ ] Tested on target devices
- [ ] Responsive layouts verified at all breakpoints

---

## Handoff Delivery Format

### Recommended Delivery Package

```
Handoff Package:
├── Design file (Figma link with Dev Mode enabled)
├── Annotated screens (per page/flow)
├── Component specifications
├── Design tokens (JSON or CSS custom properties)
├── Assets folder
│   ├── Icons (SVG)
│   ├── Images (WebP/PNG/JPEG at multiple resolutions)
│   └── Fonts (WOFF2)
├── Content document (all copy, organized by page)
├── Accessibility specifications
├── Responsive specifications
└── QA checklist (filled with acceptance criteria)
```

---
name: audit-accessibility
description: WCAG 2.2 compliance audit covering automated checks, keyboard testing, screen reader testing, color contrast verification, and ARIA review with a prioritized remediation plan.
user-invocable: true
allowed-tools: []
---

# WCAG 2.2 Accessibility Audit

Run a comprehensive accessibility audit against WCAG 2.2 guidelines, led by @accessibility-specialist. This command walks through automated checks, manual testing, and generates a prioritized remediation plan.

## When to Use This Command

- Before launching a new product or feature
- During regular accessibility compliance reviews
- After receiving user complaints about accessibility barriers
- When preparing for legal compliance requirements (ADA, Section 508, EAA)
- As part of a design review or quality assurance process

## Conformance Targets

- **Level A**: Minimum compliance. Must fix all violations.
- **Level AA**: Standard target for most products. Required by most regulations.
- **Level AAA**: Enhanced accessibility. Target where feasible.

This audit targets **WCAG 2.2 Level AA** by default unless otherwise specified.

## Workflow

### Step 1: Define Audit Scope

@accessibility-specialist establishes what will be audited.

**Gather from the user:**
- What pages, screens, or components should be audited?
- Is there a URL, code, or design to evaluate?
- What is the conformance target (A, AA, or AAA)?
- Are there known accessibility issues to prioritize?
- What assistive technologies does your user base rely on?

**Scope definition:**
- List specific pages/views (e.g., homepage, checkout flow, settings)
- List specific components (e.g., navigation, forms, modals, data tables)
- Define the testing environment (browsers, screen readers, devices)

### Step 2: Automated Checks

@accessibility-specialist runs automated scanning using the `accessibility-audit` skill.

**Tools and what they catch:**

| Tool | Catches | Misses |
|------|---------|--------|
| **axe-core** | ~30-40% of WCAG issues: missing alt text, color contrast, missing labels, duplicate IDs, ARIA misuse | Context-dependent issues, keyboard traps, reading order, meaningful content |
| **Lighthouse** | Performance + accessibility score, common violations, best practices | Same limitations as automated tools generally |
| **WAVE** | Visual overlay of issues, structural outline, contrast analysis | Does not test dynamic content or interactions |

**Automated check categories:**
1. Missing or empty alt text on images
2. Form inputs without associated labels
3. Color contrast failures (text and UI components)
4. Missing document language declaration
5. Missing page titles
6. Duplicate ID attributes
7. Empty links and buttons
8. Missing heading hierarchy
9. ARIA attribute validity
10. Table structure issues

**Output**: List of automated findings with WCAG criterion, severity, and element location.

### Step 3: Manual Keyboard Testing

@accessibility-specialist performs keyboard-only navigation testing.

**Test procedure:**
1. Disconnect or disable the mouse/trackpad
2. Starting from the browser address bar, press Tab to enter the page

**Check each of these:**

| Test | Pass Criteria | WCAG Criterion |
|------|---------------|----------------|
| Tab order | Focus moves in logical reading order | 2.4.3 Focus Order |
| Focus visibility | Every focused element has a visible indicator | 2.4.7 Focus Visible |
| Interactive elements | All buttons, links, and controls are reachable | 2.1.1 Keyboard |
| No keyboard traps | Focus can always move away from any element | 2.1.2 No Keyboard Trap |
| Skip navigation | Skip-to-content link is present and functional | 2.4.1 Bypass Blocks |
| Modal dialogs | Focus is trapped within modal, Escape closes it | 2.4.3 Focus Order |
| Custom controls | All custom widgets are operable with keyboard | 2.1.1 Keyboard |
| Dropdowns/menus | Arrow keys navigate, Escape closes | 2.1.1 Keyboard |
| Target size | Interactive targets are at least 24x24px (AA) | 2.5.8 Target Size |

**Document findings:**
```
Element: [What element]
Location: [Where on the page]
Issue: [What fails]
Expected: [What should happen]
WCAG: [Criterion number and name]
```

### Step 4: Screen Reader Testing

@accessibility-specialist evaluates screen reader compatibility.

**Test with:**
- VoiceOver (macOS/iOS) + Safari
- NVDA (Windows) + Firefox or Chrome
- TalkWinds (Android) + Chrome

**Test procedure:**
1. Navigate the page using only screen reader commands
2. Verify all content is announced in a meaningful order
3. Check that interactive elements announce their role, name, and state

**Checklist:**

- [ ] Page title is announced on load
- [ ] Headings create a logical document outline (h1 > h2 > h3)
- [ ] Images have meaningful alt text (or are marked decorative)
- [ ] Form fields announce their labels when focused
- [ ] Required fields are announced as required
- [ ] Error messages are associated with their fields
- [ ] Buttons and links announce their purpose
- [ ] Dynamic content changes are announced (live regions)
- [ ] Tables have proper headers associated with data cells
- [ ] Lists are marked up as lists (ul/ol/dl)
- [ ] Landmarks define page regions (nav, main, aside, footer)

### Step 5: Color Contrast Verification

@accessibility-specialist checks all color combinations.

**Contrast requirements (WCAG 2.2 AA):**

| Element | Minimum Ratio | Tool |
|---------|---------------|------|
| Normal text (< 18px or < 14px bold) | 4.5:1 | Contrast checker |
| Large text (>= 18px or >= 14px bold) | 3:1 | Contrast checker |
| UI components and graphical objects | 3:1 | Contrast checker |
| Focus indicators | 3:1 against adjacent colors | Manual check |

**Check these specific combinations:**
1. Body text on background
2. Heading text on background
3. Link text on background (and link vs. surrounding text if not underlined)
4. Button text on button background
5. Placeholder text on input background
6. Disabled state text on background
7. Error text on background
8. Icon-only controls against background
9. Focus ring against background and focused element

**Also verify:**
- Information is not conveyed by color alone (use icons, patterns, or text)
- UI is usable in Windows High Contrast mode
- Dark mode maintains the same contrast standards

### Step 6: ARIA Audit

@accessibility-specialist reviews ARIA implementation.

**ARIA rules to verify:**

1. **First rule of ARIA**: Do not use ARIA if native HTML can do the job
2. **Roles**: Every ARIA role is valid and appropriate for the element
3. **States and properties**: aria-expanded, aria-selected, aria-checked match visual state
4. **Labels**: aria-label or aria-labelledby provides accessible names where needed
5. **Descriptions**: aria-describedby links supplementary information
6. **Live regions**: aria-live is used for dynamic content updates
7. **Hidden content**: aria-hidden is not applied to focusable elements
8. **Required properties**: All required ARIA properties are present for each role

**Common ARIA mistakes to check:**
- `role="button"` on a `<div>` instead of using a `<button>`
- `aria-hidden="true"` on a parent of focusable children
- Missing `aria-expanded` on disclosure triggers
- `aria-label` that duplicates visible text unnecessarily
- Live regions that are too verbose or missing entirely

### Step 7: Generate Prioritized Remediation Plan

@accessibility-specialist compiles all findings into an actionable plan.

**Severity classification:**

| Severity | Definition | Timeline |
|----------|------------|----------|
| **Critical** | Users cannot complete core tasks; legal risk; complete barrier | Fix immediately |
| **Major** | Significant barrier for assistive technology users; workaround exists but is burdensome | Fix within 2 weeks |
| **Minor** | Degraded experience but task completion is possible; best practice violation | Fix within 30 days |
| **Enhancement** | Exceeds AA requirements; improves experience beyond compliance | Plan for future sprint |

**Remediation plan format:**

```markdown
## Remediation Plan

### Critical Issues (Fix Immediately)
1. [Issue title] - [WCAG criterion]
   - Location: [Where]
   - Current: [What exists now]
   - Required: [What it should be]
   - Fix: [Specific code or design change]

### Major Issues (Fix Within 2 Weeks)
[Same format]

### Minor Issues (Fix Within 30 Days)
[Same format]

### Enhancements (Backlog)
[Same format]

## Summary
- Critical: [count]
- Major: [count]
- Minor: [count]
- Enhancements: [count]
- Estimated conformance level: [A / Partial AA / AA / Partial AAA]
```

## Related Skills

- `accessibility-audit` - Detailed WCAG audit methodology and criteria
- `color-systems` - Accessible color palette generation
- `component-library` - Accessible component patterns

## Related Commands

- `/generate-palette` - Create an accessible color palette from scratch
- `/design-review` - Broader design review that includes accessibility
- `/design-handoff` - Include accessibility specs in developer documentation

## Cross-Plugin Bridge (PROACTIVE)

When the accessibility audit produces a remediation plan:

- PROACTIVELY route to the **frontend-engineering-team** plugin's **@testing-engineer** to translate accessibility findings into automated test coverage (axe-core integration, keyboard navigation tests, ARIA attribute assertions).
- PROACTIVELY route to **@react-specialist** to implement ARIA patterns, focus management, and keyboard handling in React components.
- PROACTIVELY route to **@build-tooling-specialist** to configure accessibility linting rules (eslint-plugin-jsx-a11y) in the CI pipeline so violations are caught before they reach audit.

Accessibility findings should not remain in a document -- they should be translated into engineering implementation and automated prevention.

## Tips

- Automated tools catch only 30-40% of issues; manual testing is essential
- Test with real assistive technology, not just automated checkers
- Keyboard testing is the highest-value manual test; do it first
- Document the positive findings too; teams need to know what to preserve
- Accessibility is iterative; plan for regular audits, not one-time fixes

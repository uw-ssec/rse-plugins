# Inclusive Design

Comprehensive reference for inclusive design methodology. Covers Microsoft's inclusive design principles, the disability spectrum (permanent, temporary, situational), cognitive accessibility, neurodivergent-friendly design patterns, and practical techniques for designing interfaces that work for the widest range of human abilities.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Inclusive Design Principles](#inclusive-design-principles) | 14-50 | Microsoft's three principles and their application |
| [The Disability Spectrum](#the-disability-spectrum) | 52-95 | Permanent, temporary, and situational disabilities across modalities |
| [Cognitive Accessibility](#cognitive-accessibility) | 97-145 | Memory load, attention, language complexity, and decision fatigue |
| [Neurodivergent-Friendly Design](#neurodivergent-friendly-design) | 147-195 | Patterns for ADHD, autism, dyslexia, and anxiety |
| [Inclusive Interaction Patterns](#inclusive-interaction-patterns) | 197-235 | Multi-modal input, flexible timing, and error tolerance |
| [Measuring Inclusive Design](#measuring-inclusive-design) | 237-260 | Audit frameworks and inclusion metrics |
| [See Also](#see-also) | 262-268 | Related references and skills |

## Inclusive Design Principles

Microsoft's Inclusive Design methodology provides a practical framework for designing beyond compliance. It shifts the focus from "accessible" (meeting minimum standards) to "inclusive" (designing for the full range of human diversity).

### Principle 1: Recognize Exclusion

Exclusion happens when we solve problems only for people who are like us. Every design decision excludes someone. The question is not whether exclusion exists, but whether it is intentional or accidental.

**Practice**: When designing an interaction, ask "Who cannot use this?" For every feature, identify at least three scenarios where the current design excludes someone. This is not about perfection -- it is about awareness.

**Example**: A drag-and-drop interface excludes keyboard users, users with motor impairments, users on touch devices with limited dexterity, and users of assistive switch devices. Recognizing this exclusion is the first step to solving it.

### Principle 2: Solve for One, Extend to Many

Design for a specific excluded user, and the solution often benefits everyone. Curb cuts were designed for wheelchair users but help parents with strollers, delivery workers with carts, and travelers with suitcases.

**Practice**: Choose a specific persona with a specific disability. Design a solution that works for them. Then evaluate how that solution improves the experience for users without that disability.

**Example**: Designing clear, concise error messages for users with cognitive disabilities also helps users in a hurry, users operating in a second language, and users on small screens. Captions designed for deaf users also help people watching videos in loud environments.

### Principle 3: Learn from Diversity

People who have been excluded are experts in adaptation. Their workarounds, hacks, and strategies reveal design opportunities that mainstream users would never identify.

**Practice**: Include disabled users in your research. Do not just test with them -- learn from them. Their lived experience with barriers provides insights that able-bodied designers cannot achieve through simulation.

## The Disability Spectrum

Disability is not a binary state. Microsoft's inclusive design framework identifies three types of disability for each human ability:

### Touch (Motor/Dexterity)

| Permanent | Temporary | Situational |
|-----------|-----------|-------------|
| One arm | Arm injury | Holding a child |
| Tremor | Surgery recovery | Bumpy bus ride |
| Paralysis | Carpal tunnel | Wearing gloves |

**Design implications**: Large touch targets (minimum 44x44px for touch, 24x24px per WCAG 2.5.8), alternatives to drag-and-drop, alternatives to gestures (swipe, pinch), keyboard alternatives for all mouse-dependent interactions.

### See (Vision)

| Permanent | Temporary | Situational |
|-----------|-----------|-------------|
| Blind | Dilated eyes | Bright sunlight glare |
| Low vision | Eye infection | Small screen |
| Color blind | Migraine aura | Distracted driving |

**Design implications**: High contrast ratios, text alternatives for images, scalable text (zoom to 200%), do not rely on color alone, support screen readers, support `prefers-contrast` media query.

### Hear (Auditory)

| Permanent | Temporary | Situational |
|-----------|-----------|-------------|
| Deaf | Ear infection | Loud environment |
| Hard of hearing | Noise-induced hearing loss | Conference without headphones |

**Design implications**: Captions for video, transcripts for audio, visual indicators for audio alerts, do not rely on sound alone for notifications.

### Speak (Speech/Language)

| Permanent | Temporary | Situational |
|-----------|-----------|-------------|
| Non-verbal | Laryngitis | Heavy accent in foreign country |
| Stutter | Dental surgery | Noisy environment |

**Design implications**: Do not require voice input as the only method, provide text-based alternatives to voice interfaces, allow sufficient time for speech recognition.

### Think (Cognitive)

| Permanent | Temporary | Situational |
|-----------|-----------|-------------|
| Intellectual disability | Concussion | Sleep deprivation |
| Learning disability | Medication side effects | Multitasking |
| ADHD | Grief/emotional distress | Information overload |

**Design implications**: Simple language, consistent navigation, clear error messages, minimal cognitive load, progressive disclosure, undo capability.

## Cognitive Accessibility

Cognitive accessibility is the most overlooked category. Approximately 15-20% of the population has some form of cognitive or learning disability, and everyone experiences situational cognitive impairment (stress, fatigue, distraction).

### Reducing Memory Load

Users should not need to remember information from one part of the interface to use another.

- **Show, do not tell**: Display current state visually rather than requiring users to remember it
- **Breadcrumbs**: Show the user where they are in a navigation hierarchy
- **Progress indicators**: Show how far through a multi-step process the user has progressed
- **Autofill**: Pre-populate fields with previously entered data
- **Persistent context**: Show relevant context (order summary, selected options) throughout a flow

### Managing Attention

- **Minimize distractions**: Reduce animations, auto-playing media, and moving elements
- **Respect `prefers-reduced-motion`**: Disable or simplify animations for users who request it
- **Avoid interruptions**: Do not show unsolicited modals, pop-ups, or chat widgets during focused tasks
- **Clear visual hierarchy**: Make the most important action on each screen visually obvious
- **One primary action per screen**: Reduce decision fatigue by limiting choices

### Language Complexity

- **Plain language**: Write at an 8th-grade reading level (Flesch-Kincaid Grade Level 8 or below)
- **Avoid jargon**: Define technical terms or replace them with common words
- **Short sentences**: Target 15-20 words per sentence
- **Active voice**: "Click the button" not "The button should be clicked"
- **Consistent terminology**: Use the same word for the same concept everywhere

### Decision Fatigue

- **Smart defaults**: Choose the most common or safest option as the default
- **Progressive disclosure**: Show only what is needed now; hide advanced options behind an expandable section
- **Recommended options**: Highlight the recommended choice when multiple options exist
- **Undo over confirmation**: Instead of "Are you sure?" dialogs, allow easy undo after the action

## Neurodivergent-Friendly Design

### ADHD-Friendly Patterns

- **Break content into scannable chunks**: Short paragraphs, bullet points, clear headings
- **Reduce steps in workflows**: Combine steps where possible, pre-fill data
- **Save progress automatically**: Do not lose work if the user navigates away
- **Time management support**: Show estimated time for tasks, allow saving and returning later
- **Minimize context switching**: Keep related actions on the same screen
- **Avoid time pressure**: Do not use countdown timers unless absolutely necessary
- **Provide structure**: Checklists, step indicators, and clear next-action prompts

### Autism-Friendly Patterns

- **Predictable navigation**: Same layout, same position, same behavior on every page
- **Literal language**: Avoid idioms, metaphors, and ambiguous phrasing
- **Sensory considerations**: Offer reduced-motion, reduced-animation, and muted color options
- **Explicit instructions**: State exactly what to do, do not assume the user will infer the next step
- **Warning before changes**: Alert users before the interface changes state (page redirects, data loss)
- **Consistent visual design**: Uniform spacing, alignment, and component appearance

### Dyslexia-Friendly Patterns

- **Font choice**: Sans-serif fonts (Inter, Open Sans, Atkinson Hyperlegible) with distinct letter shapes
- **Text spacing**: Generous line height (1.5x minimum), paragraph spacing (1.5x line height)
- **Line length**: 50-75 characters per line; avoid very long lines
- **Contrast**: Avoid pure black on pure white; slight off-white backgrounds reduce visual stress
- **Left alignment**: Left-align text; avoid justified text which creates uneven word spacing
- **Support for text customization**: Allow users to adjust font size, spacing, and colors

### Anxiety-Friendly Patterns

- **Clear outcomes**: Tell users exactly what will happen when they take an action
- **Reversible actions**: Make undo easy and visible
- **No hidden costs**: Show all costs, requirements, and consequences upfront
- **Save as draft**: Allow saving incomplete work without commitment
- **Confirmation of success**: Clear success messages after important actions
- **Low-pressure language**: "Take your time" instead of "Act now before it's too late"

## Inclusive Interaction Patterns

### Multi-Modal Input

Every interaction should support at least two input modalities:

| Action | Mouse | Keyboard | Touch | Voice |
|--------|-------|----------|-------|-------|
| Navigate | Click links | Tab + Enter | Tap | Voice commands |
| Select | Click option | Arrow + Enter | Tap option | "Select [option]" |
| Scroll | Mouse wheel | Arrow keys / Space | Swipe | "Scroll down" |
| Drag | Click + drag | Arrow keys | Touch + drag | Not applicable |

### Flexible Timing

- Auto-saving toasts: Show for at least 5 seconds; provide an option to pause or extend
- Session timeouts: Warn before expiration; allow extension with a single action
- Animations: Respect `prefers-reduced-motion`; provide pause controls for auto-playing content
- Typing: Do not set arbitrary time limits on text input or form completion

### Error Tolerance

- **Prevent errors**: Constrain inputs (date pickers instead of free text, format masks)
- **Detect errors early**: Validate inline on blur, not just on submit
- **Describe errors clearly**: "Email must include @ and a domain (e.g., name@example.com)"
- **Preserve user input**: Never clear the form after a validation error
- **Offer undo**: For destructive actions, provide undo for 10-30 seconds after the action

## Measuring Inclusive Design

### Inclusion Audit Framework

1. **User diversity audit**: What demographic and ability groups are represented in your user research? Who is missing?
2. **Interaction audit**: For each core task, verify it works with keyboard, screen reader, touch, and single-pointer input
3. **Content audit**: Run readability analysis (Flesch-Kincaid); target Grade Level 8 or below
4. **Cognitive load audit**: Count the number of decisions, fields, and steps in each workflow; compare to industry benchmarks
5. **Sensory audit**: Verify all information is available through multiple sensory channels (not just visual or just auditory)

### Metrics

| Metric | Target | How to Measure |
|--------|--------|---------------|
| WCAG 2.2 AA compliance | 100% | Automated + manual audit |
| Task completion rate (assistive tech users) | Within 10% of mouse users | Usability testing |
| Reading level | Grade 8 or below | Flesch-Kincaid analysis |
| Form completion time | No more than 2x keyboard vs mouse | Task timing comparison |
| Error recovery rate | 90%+ self-recovery | Analytics: error -> success without support |

## See Also

- [[wcag-checklist.md]] -- WCAG compliance criteria that form the baseline for inclusive design
- [[aria-patterns.md]] -- ARIA implementations that enable assistive technology access
- [[keyboard-nav-guide.md]] -- Keyboard navigation for motor-inclusive design
- [[contrast-guide.md]] -- Visual contrast for vision-inclusive design
- [[../../ux-writing/SKILL.md]] -- Clear, accessible writing for cognitive inclusion

**Back to:** [Accessibility Audit Skill](../SKILL.md)

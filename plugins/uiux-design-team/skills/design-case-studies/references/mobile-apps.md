# Mobile Apps

In-depth case studies of mobile app design across three categories: Apple native apps (HIG in practice), Google Material apps (Material 3 implementation), and gesture-heavy UIs (Tinder, Maps, Snapchat). Each analysis examines touch target design, gesture vocabulary, and platform convention adherence.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Apple Native Apps](#apple-native-apps) | 14-72 | iOS system apps as HIG reference implementations |
| [Google Material Apps](#google-material-apps) | 74-130 | Material 3 applied in production Android apps |
| [Gesture-Heavy UIs](#gesture-heavy-uis) | 132-200 | Tinder, Maps, and Snapchat gesture vocabularies |
| [Touch Target Analysis](#touch-target-analysis) | 202-225 | Cross-platform touch target sizing and spacing |
| [Cross-Case Patterns](#cross-case-patterns) | 227-250 | Shared mobile design principles across all studies |

## Apple Native Apps

Apple's own iOS apps serve as the canonical reference for Human Interface Guidelines in practice. Studying them reveals not just what Apple recommends, but how Apple implements those recommendations when design tradeoffs arise.

### Settings App

The Settings app is the purest expression of list-based navigation on iOS. It demonstrates hierarchical drill-down: top-level categories (Wi-Fi, Bluetooth, General) lead to detail screens, which lead to sub-detail screens. Back navigation uses the system back button with the parent label.

**Key patterns:**
- **Grouped table views.** Related settings cluster in rounded-corner groups with a header label. Groups are separated by generous spacing. This is Gestalt Common Region applied to form controls.
- **Toggle placement.** Toggles sit at the right edge of the row, aligned consistently. The entire row is tappable, not just the toggle. This ensures the 44pt minimum touch target.
- **Destructive actions.** "Sign Out," "Reset All Settings," and "Erase All Content" use red text color to signal danger. They require confirmation with an explicit destructive-action confirmation sheet.
- **Search.** The search bar at the top of Settings searches across all setting names and descriptions. This solves the discoverability problem of deeply nested settings.

### Messages App

Messages demonstrates conversation-based design with a rich interaction model.

**Key patterns:**
- **Bubble layout.** Sent messages align right (blue). Received messages align left (gray). This spatial metaphor creates an instant visual distinction between participants.
- **Tapback reactions.** Long-press on a message reveals emoji reactions (heart, thumbs up/down, ha ha, exclamation, question). This provides lightweight response without interrupting the conversation flow.
- **Rich media inline.** Photos, links, audio messages, and app clips render inline within the conversation. The bubble stretches to accommodate media without breaking the conversation flow.
- **Swipe-to-reply.** Swiping right on a message initiates a threaded reply. The gesture is discoverable through visual affordance (a reply arrow appears during the swipe).

### Photos App

Photos demonstrates content-first design with intelligent organization.

**Key patterns:**
- **Pinch-to-zoom navigation.** In the photo grid, pinch gestures zoom between organization levels: Years, Months, Days, All Photos. This single gesture provides fluid navigation through temporal hierarchy.
- **Full-screen immersion.** Tapping a photo enters full-screen mode. All chrome disappears. The photo fills the screen. A single tap brings chrome back. This is Rams' principle 5 (unobtrusive) in its purest form.
- **Intelligent grouping.** The "For You" tab uses machine learning to surface memories, featured photos, and sharing suggestions. The design presents algorithmic output as editorial curation.
- **Edit non-destructively.** All photo edits are non-destructive. Users can revert to the original at any time. This removes the fear of experimentation.

### Maps App

Maps demonstrates gesture-rich navigation and contextual UI density.

**Key patterns:**
- **Bottom sheet pattern.** Search results, place details, and directions appear in a bottom sheet that can be dragged between collapsed, half-height, and full-height states. This preserves the map context while showing information.
- **Contextual density.** The map reduces UI elements at higher zoom levels (showing more map) and increases them at lower zoom levels (showing search, categories, bookmarks). The information density adapts to the user's context.
- **Look Around.** Street-level imagery uses a binocular-style viewport that responds to device motion. Pan by dragging; move forward by tapping.

## Google Material Apps

Google's Android apps implement Material Design 3 in production. Studying them reveals how Material's component system works at scale and where Google itself deviates from its own guidelines.

### Gmail

Gmail manages one of the most complex mobile UIs: a multi-account email client with labels, filters, search, compose, and integrations.

**Key patterns:**
- **FAB for compose.** The floating action button (circular, bottom-right) is the primary action: compose a new email. Material's guidance recommends one FAB per screen for the single most important action.
- **Swipe actions on rows.** Swiping a conversation left or right applies configurable actions (archive, delete, snooze, mark read). The background color reveals the action (green for archive, red for delete) before the swipe completes.
- **Bottom navigation.** Gmail uses a bottom navigation bar with 4 items (Mail, Meet, Spaces, Chat). Material recommends 3-5 items. Each item uses an SF-Symbols-style icon with a filled variant for the selected state.
- **Top app bar behavior.** The top app bar scrolls away on downward scroll and reappears on upward scroll. The search bar collapses into a search icon. This maximizes content space on small screens.

### Google Photos

Google Photos demonstrates Material's grid and card systems with large-scale photo management.

**Key patterns:**
- **Dynamic grid.** Photos display in a justified grid where each row fills the full width by adjusting photo crop. This maximizes screen usage while maintaining visual rhythm.
- **Gesture-based selection.** Long-press enters selection mode. Dragging across photos selects multiple items. A count badge appears in the toolbar. This gesture pattern reduces the friction of bulk operations.
- **Memories carousel.** Horizontal card carousel at the top of the library, using Material's carousel component pattern. Cards auto-advance on a timer and can be manually swiped.
- **Material transitions.** Tapping a photo uses Material's container transform transition: the thumbnail expands into the full-screen view, maintaining visual continuity. The user understands that the full-screen photo "is" the thumbnail they tapped.

### Google Maps

Google Maps on Android demonstrates Material's bottom sheet, search, and navigation patterns.

**Key patterns:**
- **Persistent search bar.** The search bar sits at the top as a prominent text field (Material's outlined text field variant). Tapping expands it into a full search experience with recent searches and suggestions.
- **Chip filters.** Below the search bar, horizontal scrolling chips (Restaurants, Gas, Hotels, Groceries) provide one-tap category filtering. Material chips are ideally suited for this filter pattern.
- **Navigation bottom sheet.** Turn-by-turn directions use a minimal bottom sheet showing the next maneuver. The sheet can be expanded for the full route overview. This layered information density keeps the map visible while providing instruction.
- **Material You theming.** Maps adopts the device's Dynamic Color palette, tinting the UI with the user's wallpaper-derived colors. The map itself remains unthemed for cartographic accuracy.

### Clock App

The Clock app is a clean demonstration of Material 3's tab, FAB, and animation patterns.

**Key patterns:**
- **Bottom tab navigation.** Alarm, Clock, Timer, Stopwatch tabs at the bottom. The selected tab uses Material's animated indicator (pill-shaped background that slides between tabs).
- **Time picker.** Material's dial time picker uses a circular interface for hour and minute selection. The dial pattern is distinctive to Material and does not exist in Apple's HIG.
- **FAB for primary action.** Each tab has a contextual FAB: "Add alarm" on the alarm tab, "Add timer" on the timer tab. The FAB content changes but the position and shape remain consistent.

## Gesture-Heavy UIs

Some mobile apps define their experience through novel gesture vocabularies. These gestures become so identified with the product that they influence the entire industry.

### Tinder (Swipe Interaction)

Tinder's swipe-to-decide gesture is one of the most influential mobile interaction patterns ever created.

**Gesture vocabulary:**
- **Swipe right** = Like (green heart indicator appears as card tilts)
- **Swipe left** = Pass (red X indicator appears as card tilts)
- **Swipe up** = Super Like (blue star indicator)
- **Tap** = View more photos/info

**Why it works:**
- **Physical metaphor.** Swiping a card away mimics shuffling through a physical deck. The gesture has an intuitive analog-world mapping.
- **Binary decision, minimal cognitive load.** Yes or no. The gesture reduces complex social evaluation to a single physical movement.
- **Commitment through motion.** The physical act of swiping creates a sense of decisiveness that a button tap does not. The user feels like they "did something."
- **Card stack affordance.** The visible card stack behind the current card signals "there is more." The stack depth creates a sense of abundance.

**Touch target analysis:** The entire card (approximately 300x400pt) is the interactive surface. This massively exceeds minimum touch target requirements, making the primary interaction nearly impossible to miss.

### Maps Pinch-to-Zoom

Pinch-to-zoom on mapping applications (Apple Maps, Google Maps) is the canonical multitouch gesture.

**Gesture vocabulary:**
- **Pinch in/out** = Zoom in/out (continuous, velocity-sensitive)
- **Two-finger rotate** = Rotate the map orientation
- **Two-finger tilt** = Switch between 2D and 3D perspective
- **Double-tap** = Zoom in one level
- **Two-finger tap** = Zoom out one level
- **Pan** = Move the map viewport

**Why it works:**
- **Direct manipulation.** The map moves under the user's fingers as if it were a physical surface. There is no abstraction between the gesture and the result.
- **Continuous control.** Zoom is not stepped -- it scales smoothly with finger distance. This creates a sense of physical control that discrete zoom buttons cannot match.
- **Momentum physics.** Releasing a pan gesture carries momentum. The map decelerates naturally, as if it has physical mass. This physics simulation creates a visceral sense of interacting with a real object.
- **Gesture composability.** Users can pan, zoom, and rotate simultaneously with two fingers. The gestures compose naturally without mode switching.

### Snapchat (Gesture Discovery)

Snapchat uses hidden gesture navigation that relies on spatial memory rather than visible affordances.

**Gesture vocabulary:**
- **Swipe left from camera** = Chat
- **Swipe right from camera** = Stories/Discover
- **Swipe down from camera** = Profile/Memories
- **Tap to capture** = Photo
- **Hold to capture** = Video
- **Swipe on captured media** = Apply filters

**Why it works (and does not):**
- **Works:** Once learned, the gesture navigation is extremely fast. Spatial consistency means the camera is always "home," chat is always left, stories always right. Power users navigate by muscle memory.
- **Does not work:** Zero discoverability. New users have no visual indication that swiping accesses other features. The learning curve is steep. Snapchat relies on social learning (friends showing friends) rather than interface affordance.

**Lesson:** Hidden gestures create expert-level speed but beginner-level confusion. Use hidden gestures only when social learning or onboarding can bridge the discovery gap.

## Touch Target Analysis

Touch targets must be large enough for imprecise finger input. Standards and best practices across platforms:

| Guideline | Minimum Size | Recommended Size | Spacing |
|-----------|-------------|-----------------|---------|
| Apple HIG | 44x44pt | 44x44pt or larger | 8pt between targets |
| Material Design | 48x48dp (touch target) | 48x48dp | 8dp between targets |
| WCAG 2.5.8 | 44x44 CSS px | 44x44 CSS px | No overlap with adjacent targets |

**Common violations:**

| Violation | Problem | Fix |
|-----------|---------|-----|
| Small icon buttons | 24x24px icons without padding | Add padding to expand tap area to 44x44px minimum |
| Close-together list actions | Edit and Delete buttons adjacent with no gap | Space actions 8px+ apart or use swipe actions |
| Text links in body | Inline links with only the text bounds as target | Increase line-height to expand vertical target |
| Tab bar crowding | 6+ items crammed into a tab bar | Limit to 5 items maximum; use "More" for overflow |

**Padding technique for small visual elements:**

```css
/* Visual element is 24px, but touch target is 44px */
.icon-button {
  width: 24px; height: 24px;
  padding: 10px;  /* (44 - 24) / 2 = 10px padding on each side */
  /* Total touch area: 44x44px */
}
```

## Cross-Case Patterns

**Platform convention adherence builds trust.** Apple native apps follow HIG. Google apps follow Material. When apps deviate, users notice and lose confidence. Follow platform conventions for navigation, gestures, and system interactions. Express brand through content, color, and typography.

**Gesture discoverability exists on a spectrum.** Standard gestures (tap, scroll, swipe back) need no instruction. Extended gestures (long-press, pinch-to-zoom) are somewhat discoverable. Novel gestures (Tinder swipe, Snapchat navigation) require explicit teaching. Match gesture complexity to your onboarding investment.

**Bottom-of-screen interaction is mobile-native.** Tab bars, bottom sheets, FABs, and compose buttons live at the bottom where thumbs naturally rest. Top-of-screen elements (search bars, navigation titles) are for reading, not frequent tapping.

**Transitions communicate spatial relationships.** Push transitions mean "going deeper." Slide-up transitions mean "modal overlay." Fade transitions mean "replacing content." Container transforms mean "expanding this item." Consistent spatial transitions build the user's mental model of the app's information architecture.

**Touch target sizing is non-negotiable.** Every case study enforces minimum 44pt (Apple) or 48dp (Material) touch targets. This is not a guideline to aspire to -- it is a hard requirement for usable mobile interfaces.

## See Also

- [[saas-dashboards.md]] -- Contrast mobile patterns with desktop-first SaaS dashboard design
- [[design-systems-in-practice.md]] -- Polaris, Carbon, and Atlassian design systems include mobile-specific guidance
- [[../../design-philosophies/references/apple-hig.md]] -- The philosophical foundation for Apple native app patterns
- [[../../design-philosophies/references/material-design.md]] -- Material Design 3 system that powers Google's app patterns
- [[../../responsive-design/references/breakpoint-strategy.md]] -- Mobile-first breakpoint strategy for responsive mobile web

**Back to:** [Design Case Studies Skill](../SKILL.md)

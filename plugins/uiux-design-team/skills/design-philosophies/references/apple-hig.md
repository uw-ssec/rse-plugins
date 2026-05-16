# Apple Human Interface Guidelines

A comprehensive reference on Apple's Human Interface Guidelines covering core principles (Clarity, Deference, Depth), the 2025 Liquid Glass update, SF Symbols, platform-specific guidance for iOS, macOS, watchOS, and visionOS, and App Store review compliance tips.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Core Principles](#core-principles) | 14-45 | Clarity, Deference, and Depth as the foundation of Apple design |
| [Liquid Glass (2025)](#liquid-glass-2025) | 47-80 | Translucent surfaces, adaptive materials, and the Liquid Glass design language |
| [SF Symbols](#sf-symbols) | 82-115 | The symbol library, rendering modes, and usage guidelines |
| [Platform-Specific Guidance](#platform-specific-guidance) | 117-185 | iOS, macOS, watchOS, and visionOS conventions |
| [App Store Review Compliance](#app-store-review-compliance) | 187-225 | Design-related review guidelines and common rejection causes |
| [When to Follow vs. Adapt](#when-to-follow-vs-adapt) | 227-250 | Decision framework for HIG adherence |

## Core Principles

Apple's Human Interface Guidelines are built on three foundational principles that inform every design decision across all Apple platforms.

### Clarity

Text is legible at every size. Icons are precise and lucid. Adornments are subtle and appropriate. A sharpened focus on functionality motivates the design. Negative space, color, fonts, graphics, and interface elements subtly highlight important content and convey interactivity.

**In practice:** Use Dynamic Type to ensure text scales with user preferences. Icons should be simple enough to be recognizable at small sizes. Labels should be precise -- "Paste and Match Style" rather than just "Paste." Avoid ambiguity in any interactive element.

### Deference

Fluid motion and a crisp, beautiful interface help people understand and interact with content while never competing with it. Content fills the entire screen. Translucency and blurring hint at more content below. Use of bezels, gradients, and drop shadows is minimal, keeping the interface light and airy while ensuring that content is paramount.

**In practice:** The interface should feel like a window to content, not a frame around it. Navigation bars, tab bars, and toolbars should be lightweight. Full-screen presentations use the entire viewport. Background materials (blurs, translucencies) provide context without competing for attention.

### Depth

Distinct visual layers and realistic motion convey hierarchy, impart vitality, and facilitate understanding. Touch and discoverability heighten delight and enable access to functionality and additional content without losing context. Transitions provide a sense of depth as you navigate through content.

**In practice:** Modal sheets slide up from below, suggesting a physical layer appearing above the content. Navigation transitions push content left or right, suggesting spatial movement through a stack of views. Drag-to-dismiss gestures give users physical control over interface layers.

## Liquid Glass (2025)

Apple's 2025 Liquid Glass design language, introduced at WWDC 2025, represents the most significant visual evolution since iOS 7's flat design. Liquid Glass replaces opaque UI chrome with translucent, responsive surfaces that adapt to the content behind them.

### Core Characteristics

**Translucent surfaces:** Navigation bars, tab bars, sidebars, and system controls use a glass-like material that reveals a blurred, tinted version of the content beneath. The translucency creates a sense of physical layering while keeping the interface lightweight.

**Adaptive tinting:** Liquid Glass surfaces pick up the dominant color of the content behind them. A music player with blue album art tints the navigation bar blue. A photo app scrolling through green landscape photos tints the toolbar green. This creates a dynamic, contextually responsive interface.

**Spectral highlights:** Glass surfaces feature subtle light reflections that respond to device tilt (on devices with motion sensors) or simulate ambient lighting. These highlights reinforce the glass metaphor and add a visceral layer of visual richness.

**Unified system UI:** Liquid Glass creates visual continuity across all Apple platforms and apps. The system controls, navigation elements, and toolbars share the glass treatment, creating a consistent experience regardless of the app.

### Design Implications

**Content matters more than ever.** With translucent chrome, the content behind the interface literally shows through. Low-quality images, cluttered layouts, and garish colors become more visible problems when they bleed through the UI surface.

**Color choices affect the entire interface.** Because Liquid Glass tints based on content, the colors in your app's content directly influence how system UI appears. Test with varied content to ensure the adaptive tinting produces acceptable results.

**Contrast and readability.** Translucent surfaces can reduce text contrast depending on background content. Apple provides vibrancy effects and material options (ultra-thin, thin, regular, thick) to control the blur intensity. Use thicker materials when text legibility over varied backgrounds is critical.

**Avoid fighting the glass.** Do not place opaque backgrounds behind areas where Liquid Glass should show through. Do not add custom blurs that conflict with the system material. Work with the glass, not against it.

### Implementing Liquid Glass

```swift
// SwiftUI -- system applies Liquid Glass automatically to standard components
NavigationStack {
    List { /* content */ }
    .navigationTitle("Library")
}

// UIKit -- use UINavigationBarAppearance for customization
let appearance = UINavigationBarAppearance()
appearance.configureWithDefaultBackground() // Liquid Glass default
navigationBar.standardAppearance = appearance
```

For web applications targeting Safari, use `-webkit-backdrop-filter: blur()` with `background-color` using alpha transparency to approximate the Liquid Glass effect.

## SF Symbols

SF Symbols is Apple's library of over 6,000 configurable symbols designed to integrate with San Francisco (SF), Apple's system font. Symbols automatically align with text, scale with Dynamic Type, and support multiple rendering modes.

### Rendering Modes

| Mode | Description | Use When |
|------|-------------|----------|
| Monochrome | Single color, inherits text color | In-line with text, toolbars, navigation |
| Hierarchical | Primary and secondary opacities of a single color | Depth and emphasis within a single symbol |
| Palette | Two or three custom colors | Brand-specific coloring, custom styling |
| Multicolor | Fixed, symbol-specific colors | Weather, file types, warnings (where inherent color matters) |

### Symbol Weights and Scales

SF Symbols are available in 9 weights (ultralight through black) and 3 scales (small, medium, large). Symbols automatically match the weight and scale of adjacent text.

**Best practice:** Do not set symbol weight independently from text weight. Let the system match them. Manual weight overrides break the visual harmony between text and symbols.

### Variable Value Symbols

Many SF Symbols support a variable value (0.0 to 1.0) for representing fill level, signal strength, progress, and volume. This enables smooth, data-driven symbol rendering without switching between discrete icons.

```swift
Image(systemName: "wifi", variableValue: 0.6)  // 60% signal strength
Image(systemName: "speaker.wave.3", variableValue: 0.3)  // Low volume
```

### Symbol Animations

SF Symbols 5+ supports built-in animation effects: bounce, pulse, variable color, scale, appear, disappear, and replace. These create consistent, system-standard animations without custom code.

### Custom Symbols

Create custom symbols using the SF Symbols template in Sketch, Figma, or Illustrator. Custom symbols must follow the template's alignment guides to ensure proper text alignment and Dynamic Type scaling.

**Rule:** Before creating a custom symbol, search the existing library. With 6,000+ symbols, the one you need probably already exists. Creating a custom symbol that duplicates an existing one creates inconsistency.

## Platform-Specific Guidance

### iOS

**Navigation patterns:** Tab bar at the bottom for top-level navigation (maximum 5 items). Navigation stack (back button) for hierarchical drilling. Modal sheets for interrupting workflows. Avoid hamburger menus -- they hide navigation and reduce discoverability.

**Touch targets:** Minimum 44x44 points. The system components handle this automatically; custom components must enforce it. Apply generous padding to interactive elements that are visually small.

**Safe areas:** Respect safe area insets for the notch, Dynamic Island, home indicator, and rounded corners. Use `safeAreaInset` in SwiftUI or `safeAreaLayoutGuide` in UIKit. Never clip content behind system UI elements.

**Gestures:** Support standard system gestures: swipe back for navigation, pull to refresh for lists, swipe actions on rows (delete, archive, pin), pinch to zoom on images. Do not hijack system gestures for custom purposes.

**Dynamic Type:** Support all 12 text sizes. Test your layout at the smallest and largest sizes. Use text styles (`.body`, `.headline`, `.caption`) rather than fixed point sizes. Truncation and scrolling should handle text that exceeds the designed space.

### macOS

**Menu bar:** macOS applications use the system menu bar. Include standard menus (File, Edit, View, Window, Help) with standard keyboard shortcuts. Menu items should follow macOS conventions (Cmd+Q to quit, Cmd+W to close window, Cmd+, for preferences).

**Window management:** Support window resizing, full screen, and Split View. Design layouts that adapt gracefully from minimum window size to full desktop width. Use sidebars (NavigationSplitView) for primary navigation.

**Pointer interactions:** macOS has hover states. Use them. Tooltips, hover previews, and subtle hover highlights improve discoverability. Right-click context menus provide efficient access to actions.

**Keyboard navigation:** Full keyboard navigability is expected on macOS. Tab order must be logical. Focus indicators must be visible. All actions must be accessible via keyboard or menu bar.

**Toolbar:** macOS toolbars appear below the title bar and contain frequently used actions. Use SF Symbols for toolbar items. Group related items with separator dividers.

### watchOS

**Glanceability:** watchOS interfaces must communicate in 2-3 seconds. Users glance at their watch, not study it. Use large text, minimal content, and high-contrast colors.

**Complications:** Design watch face complications that show the most critical information at a glance. Support all complication families (circular, rectangular, inline).

**Digital Crown:** The Digital Crown is watchOS's primary scrolling mechanism. Design scrollable content in single-axis lists. Support crown-based selection where appropriate.

**Tap targets:** Minimum 38 points on watch. The smaller screen demands fewer, larger interactive elements. Two or three actions per screen is usually the maximum.

**Notifications:** Design short-look and long-look notification layouts. Short-look appears briefly and must communicate the core information in one line. Long-look provides additional detail and action buttons.

### visionOS

**Spatial design:** visionOS interfaces exist in 3D space. Windows float in the user's environment. Volumes contain 3D content. Immersive spaces replace the real environment with virtual content.

**Eye tracking and gestures:** Interaction in visionOS uses eye tracking (look at an element) combined with hand gestures (pinch to select). Design hover states that respond to gaze -- elements should subtly highlight when looked at.

**Windows:** visionOS windows use glass material and float in space. Design for a default window size of approximately 1280 points wide. Windows can be resized and repositioned by the user.

**Depth and scale:** Elements closer to the viewer appear larger and more important. Use z-position to establish hierarchy. Avoid placing interactive elements too close to the user (closer than 0.5 meters in virtual space) as they become difficult to focus on.

**Comfort:** Design for extended use in spatial computing. Avoid requiring users to look up, down, or to extreme sides for extended periods. Place primary content at comfortable eye level.

## App Store Review Compliance

Design-related rejections are among the most common App Store review failures. These guidelines help avoid rejection.

### Common Design-Related Rejections

| Guideline | Rejection Reason | Fix |
|-----------|-----------------|-----|
| 4.0 Design | App uses web views for primary experience without native UI | Use native navigation, tab bars, and system components |
| 4.1 Copycats | App too closely resembles another app or Apple's own apps | Create distinctive visual identity; do not replicate Apple's app icons or UI |
| 4.2 Minimum Functionality | App is too simple (single-page, static content, wrapper around website) | Provide meaningful native functionality beyond what a website offers |
| 4.3 Spam | Multiple apps with very similar functionality | Consolidate into one app with clear differentiation |
| 2.3.3 Screenshots | Screenshots do not accurately reflect the app experience | Use actual app screenshots, not mockups or marketing renders |
| 2.4.1 Hardware Compatibility | App does not adapt to all supported screen sizes | Test on all supported devices; use Auto Layout |

### Design Best Practices for Review Compliance

**Use native components.** Reviewers look for standard iOS patterns: tab bars, navigation bars, table views, and standard gestures. Custom components are acceptable but should not replace standard navigation patterns entirely.

**Support Dynamic Type.** Apps that do not support Dynamic Type may be rejected for accessibility reasons, particularly if they target categories like Health, Education, or Productivity.

**Support Dark Mode.** While not strictly required, apps that do not support Dark Mode may receive lower ratings and reviewer feedback requesting it.

**Provide meaningful onboarding.** Apps that require account creation before showing any value face higher rejection rates. Show value first, then request account creation.

**Handle all states.** Empty states, loading states, and error states must be designed. Reviewers test edge cases. A blank screen when no data is available signals an incomplete app.

## When to Follow vs. Adapt

### Follow HIG Strictly When

- Building a **native iOS/macOS/watchOS/visionOS app** intended for the App Store
- Building an app in a **regulated category** (health, finance, education) where user trust is paramount
- Working with **limited design resources** -- HIG provides comprehensive defaults
- Building **utilities and productivity tools** where familiarity speeds adoption
- When **App Store approval** is critical and the team has limited review experience

### Adapt HIG When

- Building a **brand-forward consumer app** where distinctive identity matters (games, social, lifestyle)
- Building a **cross-platform app** that must feel consistent on iOS and Android
- Creating **marketing and onboarding flows** that require more visual expression
- When **user research** shows that HIG conventions conflict with your specific user needs
- Building **media and entertainment** apps where immersive experience trumps platform conventions

### The Adaptation Spectrum

| Level | Description | Example |
|-------|-------------|---------|
| Full compliance | System components, system fonts, system navigation | Apple's own apps (Notes, Calendar, Settings) |
| Themed compliance | Custom colors and typography within standard component structures | Banking apps, enterprise tools |
| Selective compliance | Custom components for core experience, system components for settings/navigation | Social media apps, creative tools |
| Minimal compliance | Fully custom UI, only using required system elements (status bar, gestures) | Games, immersive media apps |

Each level is appropriate depending on context. The key is intentional choice, not accidental deviation.

## See Also

- [[material-design.md]] -- Compare Apple's philosophy with Material Design for cross-platform decisions
- [[dieter-rams-principles.md]] -- Apple HIG is the most direct digital descendant of Rams' design philosophy
- [[emotional-design.md]] -- Apple excels at all three levels of Norman's emotional design model
- [[../../design-case-studies/references/mobile-apps.md]] -- Case studies of HIG applied in production iOS apps
- [[../../design-case-studies/references/brand-experiences.md]] -- Apple.com as a case study in brand-forward design

**Back to:** [Design Philosophies Skill](../SKILL.md)

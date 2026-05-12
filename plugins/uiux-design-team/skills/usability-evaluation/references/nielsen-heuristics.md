# Nielsen Heuristics

An extended reference for Jakob Nielsen's 10 usability heuristics. Each heuristic is presented with a detailed explanation, 3-4 common violations, 3-4 best-practice examples, remediation strategies, and severity assessment guidelines.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [H1: Visibility of System Status](#h1-visibility-of-system-status) | 14-40 | Keeping users informed about what is happening |
| [H2: Match Between System and Real World](#h2-match-between-system-and-real-world) | 42-68 | Speaking the user's language |
| [H3: User Control and Freedom](#h3-user-control-and-freedom) | 70-95 | Providing exits and undo capabilities |
| [H4: Consistency and Standards](#h4-consistency-and-standards) | 97-122 | Following conventions inside and outside the product |
| [H5: Error Prevention](#h5-error-prevention) | 124-149 | Preventing problems before they occur |
| [H6: Recognition Rather Than Recall](#h6-recognition-rather-than-recall) | 151-176 | Minimizing memory load |
| [H7: Flexibility and Efficiency of Use](#h7-flexibility-and-efficiency-of-use) | 178-203 | Accommodating novice and expert users |
| [H8: Aesthetic and Minimalist Design](#h8-aesthetic-and-minimalist-design) | 205-230 | Removing unnecessary information |
| [H9: Help Users Recover from Errors](#h9-help-users-recover-from-errors) | 232-257 | Designing useful error messages |
| [H10: Help and Documentation](#h10-help-and-documentation) | 259-283 | Providing accessible help resources |
| [See Also](#see-also) | 285-293 | Related references and skills |

## H1: Visibility of System Status

**The principle:** The system should always keep users informed about what is going on through appropriate feedback within reasonable time.

**Detailed explanation:** Users should never have to wonder "Did that work?" or "What is happening now?" Every action should produce visible feedback, every process should show progress, and every state should be clearly communicated. The Nielsen Norman Group's research shows that response time thresholds affect perception: under 100ms feels instant, 100ms-1s feels responsive, and over 1s requires progress indication.

**Common violations:**
- Form submission with no loading indicator -- the user clicks "Submit" and nothing visibly happens for 2-3 seconds
- File upload with no progress bar -- the user does not know if the upload started, its progress, or if it failed
- Background saves that provide no confirmation -- the user cannot tell if their work was saved
- Navigation that does not indicate the current page -- the user does not know where they are in the site

**Best-practice examples:**
- Gmail's sending indicator with undo option after composing an email
- Shopify's toast notifications confirming save actions with specific details ("Product saved")
- GitHub's progress bar during file upload with percentage and estimated time
- Linear's optimistic UI updates that show changes immediately with background sync indicators

**Remediation strategies:**
- Add loading spinners or skeleton screens for any operation over 200ms
- Use toast notifications for background actions (save, send, sync)
- Highlight the active navigation item with visual distinction (color, weight, indicator)
- Show progress bars with percentage for long operations (uploads, exports, imports)

**Severity assessment:** Violations are severity 3-4 when users cannot determine if critical actions succeeded (payment processing, form submission). Severity 1-2 for non-critical state visibility (current page indication, minor save confirmations).

## H2: Match Between System and Real World

**The principle:** The system should speak the users' language with words, phrases, and concepts familiar to the user rather than system-oriented terms.

**Detailed explanation:** Every label, message, and instruction should use vocabulary that the target user already knows. Technical jargon, internal company terminology, and developer-facing error codes alienate users. Information should be presented in a natural and logical order that matches how users think about the domain, not how the database is structured.

**Common violations:**
- Error messages displaying technical codes: "Error 500: Internal Server Error" or "NullReferenceException"
- Navigation labels using internal terminology: "Knowledge Base" instead of "Help" for a consumer product
- Form fields organized by database schema rather than user mental model (billing address before shipping address when users think shipping first)
- Date formats that do not match the user's locale (MM/DD/YYYY shown to European users)

**Best-practice examples:**
- Mailchimp's conversational error messages: "Hmm, that email address doesn't look right. Can you check it?"
- Stripe's documentation using developer-friendly but plain-English explanations alongside code examples
- Airbnb organizing search results by what travelers care about (price, location, amenities) not by listing ID or creation date
- Apple's use of everyday metaphors: "Trash," "Desktop," "Folders" rather than "Recycle Queue," "Home Screen," "Directories"

**Remediation strategies:**
- Conduct card sorting to discover users' natural vocabulary and mental models
- Replace all technical error codes with human-readable messages that suggest a next step
- Test labels with users: show them a navigation label and ask what they expect to find
- Localize date, number, and currency formats for the user's region

**Severity assessment:** Severity 3-4 when jargon prevents task completion (user cannot find a feature because the label is meaningless to them). Severity 1-2 when it causes momentary confusion but does not block progress.

## H3: User Control and Freedom

**The principle:** Users often perform actions by mistake. They need a clearly marked "emergency exit" to leave unwanted states without going through an extended process.

**Detailed explanation:** Users explore interfaces by trial and error. When they make a wrong turn, they need to get back easily. Support undo, redo, cancel, and back navigation at every level. Forcing users through multi-step processes to correct simple mistakes creates frustration and learned helplessness.

**Common violations:**
- No undo after deleting an item -- the action is permanent with no recovery
- Modal dialogs with no visible close button or escape key support
- Multi-step wizards with no back button or ability to jump to a previous step
- Accidental navigation away from unsaved work with no warning or auto-save

**Best-practice examples:**
- Google Docs' persistent undo with full version history accessible from the menu
- Slack's message edit and delete with undo period after deletion
- Notion's "Undo" toast that appears immediately after any destructive action
- Figma's version history allowing users to restore any previous state

**Remediation strategies:**
- Implement undo for all destructive actions (delete, remove, clear)
- Add confirmation dialogs for irreversible actions (account deletion, data export overwrite)
- Ensure every modal and overlay can be closed via close button, escape key, and clicking outside
- Auto-save user work and provide a "Discard changes" option rather than losing work on navigation

**Severity assessment:** Severity 4 when users lose data or cannot reverse a critical action. Severity 2-3 when they are stuck in a state but can eventually recover through alternative paths.

## H4: Consistency and Standards

**The principle:** Users should not have to wonder whether different words, situations, or actions mean the same thing. Follow platform conventions.

**Detailed explanation:** Consistency operates at two levels. Internal consistency means the same pattern, terminology, and behavior throughout your product. External consistency means following established conventions of the platform (iOS, Android, web) and the industry. When your product works like other products the user already knows, learning time approaches zero.

**Common violations:**
- Same action called different names on different pages ("Save" vs "Submit" vs "Confirm" for the same operation)
- Buttons that look identical but behave differently (some navigate, some submit forms, some open modals)
- Custom UI patterns where standard patterns exist (custom dropdown instead of native select, custom date picker that does not follow platform conventions)
- Inconsistent icon usage (gear icon means "Settings" on one page and "Preferences" on another)

**Best-practice examples:**
- Stripe's dashboard using consistent button hierarchy across every page (primary, secondary, danger)
- Apple's consistent use of standard iOS patterns (swipe to delete, pull to refresh, sheet presentation)
- GitHub's consistent action patterns (every destructive action is red, every creation action is green)
- Material Design's comprehensive component library ensuring consistency across Google products

**Remediation strategies:**
- Create and maintain a UI component library with documented usage guidelines
- Audit terminology across the product and create a content glossary
- Follow platform human interface guidelines (Apple HIG, Material Design, Windows Fluent)
- Establish naming conventions for actions: "Save" for persisting data, "Submit" for sending to review, "Create" for making new items

**Severity assessment:** Severity 2-3 when inconsistency causes confusion or errors. Severity 1 when it is merely aesthetic inconsistency without functional impact.

## H5: Error Prevention

**The principle:** Even better than good error messages is a careful design that prevents a problem from occurring in the first place.

**Detailed explanation:** There are two types of errors to prevent. Slips are unconscious errors (typos, mis-clicks). Mistakes are conscious errors based on incorrect mental models (choosing the wrong option because the labels are confusing). Design for both: constrain inputs to prevent slips, and clarify choices to prevent mistakes.

**Common violations:**
- Free-text input where a dropdown or date picker would prevent invalid entries
- Destructive buttons placed adjacent to constructive buttons with similar styling
- No confirmation before irreversible actions (permanent deletion, sending mass emails)
- Forms that accept any input and only validate on submission, allowing cascading errors

**Best-practice examples:**
- Google Calendar's smart input that parses "lunch with Sarah tomorrow at noon" into structured event data
- Amazon's address validation that catches typos and suggests corrections before checkout
- GitHub's branch protection rules that prevent force-pushing to main
- Stripe's card number field that auto-formats, validates in real-time, and rejects obviously invalid numbers

**Remediation strategies:**
- Use constrained inputs (dropdowns, date pickers, radio buttons) instead of free text where possible
- Validate input in real-time as the user types, not only on form submission
- Add confirmation steps for destructive or high-stakes actions
- Disable buttons until required conditions are met (disable "Submit" until all required fields are valid)
- Separate destructive and constructive actions visually and spatially

**Severity assessment:** Severity 3-4 when lack of prevention leads to data loss or costly errors. Severity 1-2 when it leads to minor inconvenience that is easily corrected.

## H6: Recognition Rather Than Recall

**The principle:** Minimize the user's memory load by making elements, actions, and options visible. The user should not have to remember information from one part of the interface to another.

**Detailed explanation:** Working memory is limited (7 plus or minus 2 items). Every piece of information the user must remember imposes cognitive load. Design the interface so that all necessary information is visible or easily retrievable at the point of decision.

**Common violations:**
- Referencing an item by ID on a confirmation page without showing its name or preview
- Requiring users to remember field requirements (password rules not shown until after failed submission)
- Navigation that hides sub-pages until hovered, requiring users to remember the menu structure
- Multi-step forms where later steps reference information entered in earlier steps without showing it

**Best-practice examples:**
- Amazon's checkout showing product thumbnails, names, and prices at every step, never just order IDs
- VS Code's command palette showing recently used commands at the top
- Google Search's auto-complete suggestions that help users recognize rather than recall queries
- Figma's showing the selected element's properties in a visible sidebar, not requiring users to remember values

**Remediation strategies:**
- Show contextual information at every decision point (product images on checkout, file names on confirmation)
- Provide search with autocomplete and recent items
- Use breadcrumbs to show the user's location in the hierarchy
- Display requirements and constraints inline with inputs, not in separate documentation

**Severity assessment:** Severity 2-3 when users must recall information to complete tasks. Severity 1 when recall is optional (power-user shortcuts).

## H7: Flexibility and Efficiency of Use

**The principle:** Accelerators, unseen by novice users, can speed up interaction for expert users so that the system can cater to both inexperienced and experienced users.

**Detailed explanation:** The same interface must serve first-time users who need guidance and power users who need speed. Layer the experience: provide discoverable, guided paths for novices and shortcuts, keyboard commands, and customization for experts.

**Common violations:**
- No keyboard shortcuts for frequent actions in productivity tools
- Forcing expert users through the same multi-step wizard every time (no templates, no "skip intro")
- No way to customize dashboards, default views, or frequently used settings
- Search that requires exact matches with no fuzzy matching or filters

**Best-practice examples:**
- Notion's slash commands that let power users create any block type without touching the toolbar
- Gmail's keyboard shortcuts (configurable, disabled by default so they do not confuse novices)
- Figma's "Quick Actions" (Cmd+/) that combines search, recent actions, and commands in one interface
- Linear's customizable workflows, keyboard navigation, and command palette for power users

**Remediation strategies:**
- Add keyboard shortcuts for the 10 most frequent actions and document them in a discoverable location
- Provide saved templates, presets, or defaults for repetitive tasks
- Allow dashboard and view customization (column order, default filters, saved views)
- Implement a command palette (Cmd+K / Ctrl+K) that provides universal search and action access

**Severity assessment:** Severity 2-3 when inefficiency causes significant time loss for frequent users. Severity 1 when it is a minor convenience improvement.

## H8: Aesthetic and Minimalist Design

**The principle:** Interfaces should not contain information that is irrelevant or rarely needed. Every extra unit of information competes with relevant information and diminishes its relative visibility.

**Detailed explanation:** This heuristic is about signal-to-noise ratio, not visual minimalism. A "clean" interface that hides necessary information is worse than a "busy" interface that shows everything the user needs. The goal is to ensure that the important elements are prominent and the unimportant elements are absent or de-emphasized.

**Common violations:**
- Dashboards showing every possible metric instead of the 3-5 most actionable ones
- Marketing-speak and filler text on screens where users need to take action
- Decorative elements that add visual noise without communicating information
- Settings pages that expose every configuration option on a single screen with no grouping

**Best-practice examples:**
- Stripe's dashboard surfacing only the most critical metrics with drill-down paths for details
- Linear's clean issue views that show only relevant metadata with progressive disclosure for details
- Apple's product pages that use generous whitespace to let each product feature breathe
- Basecamp's "What's most important?" approach to project dashboards

**Remediation strategies:**
- Audit every element on each screen: does this help the user accomplish their current task?
- Use progressive disclosure: show summary information by default, details on demand
- Move rarely-used options to secondary locations (advanced settings, overflow menus)
- Remove decorative elements that do not communicate information or reinforce brand

**Severity assessment:** Severity 2-3 when clutter obscures critical information or actions. Severity 1 when it is merely visual noise without functional impact.

## H9: Help Users Recover from Errors

**The principle:** Error messages should be expressed in plain language (no codes), precisely indicate the problem, and constructively suggest a solution.

**Detailed explanation:** Errors are inevitable. The quality of the error experience determines whether the user recovers and continues or gives up and leaves. Every error message should answer three questions: What happened? Why did it happen? What can the user do about it?

**Common violations:**
- Generic error messages: "Something went wrong. Please try again." (What went wrong? Will trying again help?)
- Technical error messages: "Error 422: Unprocessable Entity" (meaningless to non-developers)
- Error messages that blame the user: "Invalid input" (what was invalid? how should they fix it?)
- Errors that clear the user's work (form errors that reset all fields)

**Best-practice examples:**
- Stripe's form validation: "Your card number is incomplete" with the specific field highlighted
- GitHub's merge conflict interface showing exactly which lines conflict and providing resolution tools
- Mailchimp's friendly error pages with specific guidance: "We can't find that page. Here are some things you can try..."
- Slack's "We're having trouble connecting" message with a visible retry button and network status indicator

**Remediation strategies:**
- Write error messages in plain language following the pattern: "[What happened]. [Why]. [What to do next]."
- Highlight the specific field or element where the error occurred
- Preserve user input when displaying errors -- never clear the form
- Provide a clear path to resolution (retry button, help link, alternative action)
- Log technical details to the console for developers while showing human messages to users

**Severity assessment:** Severity 3-4 when poor error messages prevent task completion. Severity 2 when errors are confusing but the user can eventually resolve them. Severity 1 for cosmetic issues in error presentation.

## H10: Help and Documentation

**The principle:** Even though it is better if the system can be used without documentation, it may be necessary to provide help. Any such information should be easy to search, focused on the user's task, list concrete steps, and not be too large.

**Detailed explanation:** Help and documentation should be the last resort, not the first requirement. If users frequently need help for a task, the task itself should be redesigned. When help is necessary, it should be contextual (available at the point of need), searchable, task-oriented (not feature-oriented), and concise.

**Common violations:**
- No help content at all -- users are left to figure out complex features alone
- Help content that is feature-oriented ("The Export function allows you to...") rather than task-oriented ("How to export your data to Excel")
- Help documentation stored in a separate site with no in-app access
- Outdated documentation that does not match the current interface

**Best-practice examples:**
- Notion's contextual help tooltips that explain features at the point of use
- Stripe's documentation with interactive code examples that users can modify and test
- Figma's in-app tips that appear when users first encounter a feature, then disappear
- VS Code's "Getting Started" tab with task-oriented walkthroughs for common workflows

**Remediation strategies:**
- Provide in-app contextual help (tooltips, info icons, inline documentation)
- Structure help content around tasks ("How to...") not features ("The X feature")
- Implement full-text search in documentation with good results ranking
- Keep documentation in sync with the product through automated screenshot testing or regular audits
- Offer multiple help formats: text documentation, video tutorials, interactive walkthroughs

**Severity assessment:** Severity 2-3 when users cannot accomplish tasks without help and help is unavailable or unusable. Severity 1 when help exists but could be better organized or more contextual.

## See Also

- [[walkthrough-guide.md]] -- Use cognitive walkthroughs to evaluate specific task flows against these heuristics
- [[scoring-methods.md]] -- Quantify usability severity using the SUS questionnaire and severity rating scales
- [[../../user-research/references/interview-guide.md]] -- Conduct user interviews to validate heuristic evaluation findings
- [[../../accessibility-audit/SKILL.md]] -- Extend heuristic evaluation to include accessibility criteria
- [[../../information-architecture/references/navigation-guide.md]] -- Navigation patterns that support H1, H4, and H6

**Back to:** [Usability Evaluation Skill](../SKILL.md)

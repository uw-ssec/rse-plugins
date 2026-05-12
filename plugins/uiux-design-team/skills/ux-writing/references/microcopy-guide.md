# Microcopy Guide

Exhaustive patterns for every type of UI text with good and bad examples. This reference covers button labels, form labels, placeholder text, help text, tooltips, menu items, navigation labels, page titles, confirmation dialogs, success messages, empty states, and onboarding text.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Button Labels](#button-labels) | 14-42 | Action-specific button copy for every common interaction |
| [Form Text](#form-text) | 44-95 | Labels, placeholders, help text, and validation messages |
| [Tooltips and Help](#tooltips-and-help) | 97-125 | Contextual guidance that appears on demand |
| [Navigation and Page Titles](#navigation-and-page-titles) | 127-155 | Menu items, breadcrumbs, and page headings |
| [Confirmation Dialogs](#confirmation-dialogs) | 157-188 | Destructive actions, state changes, and user decisions |
| [Success and Status Messages](#success-and-status-messages) | 190-215 | Confirmation, progress, and completion copy |
| [Empty States and Onboarding](#empty-states-and-onboarding) | 217-250 | First-use experiences and zero-data screens |

## Button Labels

Buttons are the most important text on any screen. They tell users what will happen when they interact.

### Primary Action Buttons

| Context | Bad | Good | Why |
|---------|-----|------|-----|
| Creating an account | Submit | Create account | Specific verb describes the outcome |
| Saving changes | OK | Save changes | Confirms what "OK" actually does |
| Publishing content | Submit | Publish post | Names the action and the object |
| Sending a message | Send | Send message | Adds the object for clarity |
| Starting a trial | Continue | Start free trial | Names the value proposition |
| Uploading a file | Upload | Upload image | Specifies what is being uploaded |
| Generating a report | Go | Generate report | Describes the process that will begin |

### Secondary and Cancel Buttons

| Context | Bad | Good | Why |
|---------|-----|------|-----|
| Canceling form changes | Cancel | Discard changes | Clarifies what canceling does |
| Closing without saving | No | Don't save | States the consequence explicitly |
| Dismissing a notification | X | Dismiss | Accessible label for screen readers |
| Going back in a flow | Back | Back to settings | Names the destination |
| Skipping an optional step | Skip | Skip for now | Implies they can return later |

### Destructive Action Buttons

| Context | Bad | Good | Why |
|---------|-----|------|-----|
| Deleting a project | Yes | Delete project | Names the destructive action explicitly |
| Removing a team member | Remove | Remove Sarah from team | Names the person and the consequence |
| Canceling a subscription | Confirm | Cancel subscription | No ambiguity about what is being confirmed |
| Clearing all data | Reset | Clear all data | Specific about what is being reset |

### Button Copy Rules

1. **Start with a verb.** "Save draft" not "Draft save." The action comes first.
2. **Name the object when ambiguous.** "Delete" is ambiguous. "Delete project" is not.
3. **Match the button to the page heading.** If the heading says "Create a new project," the button says "Create project."
4. **Keep it under 4 words.** Long button labels signal a design problem, not a copy problem.

## Form Text

Forms are where users provide information. Every text element in a form either helps or hinders completion.

### Form Labels

Labels should be concise, specific, and placed directly above or beside the input.

| Bad | Good | Why |
|-----|------|-----|
| Name | Full name | "Name" is ambiguous (first? last? display?) |
| Email | Email address | Slightly more specific; helps autofill |
| Phone | Phone number | Consistent with "Email address" pattern |
| Address | Street address | Distinguishes from email or IP address |
| Password | Create a password | Distinguishes from "enter your existing password" |

### Placeholder Text

Placeholders show format examples, not instructions. They disappear on input, so they must not contain essential information.

| Bad | Good | Why |
|-----|------|-----|
| Enter your email | jane@example.com | Shows format instead of restating the label |
| Type here | Search projects... | Describes what happens in context |
| Enter date | MM/DD/YYYY | Shows the expected format |
| Enter your name | (leave empty) | The label is sufficient; placeholder adds noise |

**Rule:** Never use placeholder text as a replacement for labels. Placeholders disappear when the user starts typing, removing the context they need.

### Help Text

Help text appears below the input and provides guidance that does not fit in the label.

| Context | Bad Help Text | Good Help Text |
|---------|--------------|----------------|
| Password field | Must be strong | At least 8 characters with one number and one symbol |
| Username field | Choose a username | Letters, numbers, and underscores only. This cannot be changed later. |
| Bio field | Tell us about yourself | 160 characters max. Appears on your public profile. |
| URL field | Enter URL | Include https:// (e.g., https://example.com) |

### Inline Validation Messages

Validation messages appear when input does not meet requirements. They must be specific, not generic.

| Bad | Good | Why |
|-----|------|-----|
| Invalid input | Enter a valid email address (e.g., name@example.com) | Names the problem and shows the expected format |
| Required field | Add a project name to continue | Names the specific field and the consequence |
| Too short | Use at least 8 characters (you have 5) | States the requirement and the current state |
| Invalid format | Phone numbers should include 10 digits | States the expected format |
| Already exists | That username is taken. Try adding numbers or underscores. | Explains why and suggests a fix |

### Required vs. Optional Fields

- Mark optional fields, not required ones. Most fields are required; marking the minority reduces visual noise.
- Use the word "(optional)" next to the label, not an asterisk.
- Never use color alone to indicate required status.

## Tooltips and Help

### Tooltip Content

Tooltips provide additional context for elements that are otherwise clear enough to not need a label. They appear on hover or focus.

| Element | Bad Tooltip | Good Tooltip | Why |
|---------|------------|--------------|-----|
| Lock icon on a post | Info | Visible to team members only | Provides the actual information |
| Settings gear icon | Settings | Account settings | More specific than the generic label |
| Keyboard shortcut | Shortcut | Bold (Cmd+B) | Names the action and the shortcut |
| Disabled button | Disabled | Complete all required fields to continue | Explains why and how to enable |
| User avatar | User | Sarah Chen (Admin) | Shows the person's name and role |

### Tooltip Rules

1. **Never put essential information in a tooltip.** If the user must know it to complete a task, it belongs in the visible UI.
2. **Keep tooltips under 15 words.** Tooltips that require reading are failing at their job.
3. **Do not duplicate visible labels.** A tooltip that says "Settings" on a button labeled "Settings" adds nothing.
4. **Include keyboard shortcuts.** Tooltips on toolbar items should show the keyboard shortcut.

### Contextual Help Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| Inline help text | Always-visible guidance below a form field | "We'll send a confirmation to this address." |
| Tooltip | Supplementary info on hover/focus | "Last synced 5 minutes ago" |
| Help icon (?) | Complex concepts that need explanation | Clicking reveals: "API keys authenticate your requests. Keep them secret." |
| Expandable section | Detailed guidance for optional reading | "Learn more about webhooks" expands a paragraph |
| Guided tour | First-time feature introduction | Step-by-step overlay highlighting key UI elements |

## Navigation and Page Titles

### Navigation Labels

Navigation labels must be scannable, predictable, and hierarchical.

| Bad | Good | Why |
|-----|------|-----|
| Hub | Dashboard | "Hub" is vague; "Dashboard" is a recognized pattern |
| Stuff | Resources | Generic labels slow scanning |
| My Things | My Projects | Name the specific content type |
| Manage | Team Members | "Manage" requires a click to understand what is managed |
| More | Settings | "More" hides the content; name it if space allows |

### Breadcrumb Labels

Breadcrumbs show hierarchical location. Each segment should be clickable and use the same label as the page it links to.

```
Home > Projects > Website Redesign > Tasks
```

- Use the actual page title for each breadcrumb segment
- Separate with ">" or "/" consistently
- Truncate middle segments on mobile: "Home > ... > Tasks"
- The current page (last segment) is not a link

### Page Titles

Page titles appear in the browser tab and the page heading. They should be descriptive and unique.

| Bad | Good | Why |
|-----|------|-----|
| Page 1 | Create New Project | Describes the page's purpose |
| Dashboard | Project Dashboard | Adds context about which dashboard |
| Settings | Account Settings | Specifies which settings |
| Untitled | Invoice #2847 | Uses the specific object name |

**Browser tab pattern:** `Page Name - Section - Product Name`
Example: `Account Settings - Settings - Acme App`

## Confirmation Dialogs

Confirmation dialogs interrupt the user to verify a decision. They must be clear about what will happen and what will not happen.

### Destructive Action Confirmations

```
Title: Delete "Website Redesign"?

Body: This will permanently delete the project and all 47 tasks,
12 files, and 3 milestones inside it. This action cannot be undone.

Primary button: Delete project (destructive style)
Secondary button: Keep project
```

**Rules for destructive confirmations:**
1. **Name the object being destroyed** in the title ("Website Redesign," not just "this project").
2. **State the consequences** including what else will be affected (tasks, files, data).
3. **State irreversibility** clearly: "This action cannot be undone" or "You can restore this from trash for 30 days."
4. **Use a destructive-styled primary button** (red) with specific label ("Delete project," not "Yes").
5. **Use a safe secondary button** with a positive label ("Keep project," not "Cancel").

### State Change Confirmations

```
Title: Publish "Q4 Report"?

Body: This will make the report visible to all team members.
You can unpublish it later from the report settings.

Primary button: Publish report
Secondary button: Keep as draft
```

### Unsaved Changes Confirmation

```
Title: You have unsaved changes

Body: Do you want to save your changes before leaving?

Primary button: Save changes
Secondary button: Discard changes
Tertiary button: Cancel (return to editing)
```

**Three-button pattern:** When there are three distinct outcomes (save, discard, cancel), provide three buttons. Do not force a binary choice when three options exist.

### Permission Requests

```
Title: Allow notifications?

Body: We'll send you updates when someone comments on your
work or assigns you a task. You can change this in Settings.

Primary button: Allow notifications
Secondary button: Not now
```

**Rules for permission requests:**
- Explain the benefit, not just the request
- Tell users where to change the setting later
- Use "Not now" instead of "No" to reduce dismissal friction

## Success and Status Messages

### Success Messages (Toasts)

| Context | Bad | Good | Why |
|---------|-----|------|-----|
| Saving a document | Success! | Changes saved | Names what was saved |
| Sending an email | Done | Email sent to sarah@example.com | Confirms the recipient |
| Creating a project | Project created | "Website Redesign" created | Names the specific object |
| Uploading a file | Upload complete | 3 files uploaded to /assets | Counts items and names the location |
| Password change | Updated | Password updated | Names what was updated |

### Progress Messages

| Stage | Message | Purpose |
|-------|---------|---------|
| Starting | Generating your report... | Sets expectation about what is happening |
| In progress | Processing 847 of 2,340 records... | Shows progress with numbers |
| Almost done | Finalizing... | Signals the end is near |
| Complete | Report generated. 2,340 records processed. | Confirms completion with summary |

### Loading Messages

| Bad | Good | Why |
|-----|------|-----|
| Loading... | Preparing your dashboard... | Describes what is loading |
| Please wait | Connecting to server... | Explains why there is a wait |
| Loading... | Searching 10,000+ projects... | Provides context for the delay |

## Empty States and Onboarding

### First-Use Empty States

First-use empty states appear when the user has not yet added content.

**Structure:**
1. **Visual** (illustration or icon) -- Represents what this space is for
2. **Headline** -- Names the feature: "No projects yet"
3. **Description** -- Explains the value: "Projects help you organize tasks, deadlines, and team members in one place."
4. **CTA** -- Provides the first action: "Create your first project"

| Context | Bad Headline | Good Headline | Good Description |
|---------|-------------|---------------|------------------|
| Project list | No data | No projects yet | Create a project to organize your team's work in one place. |
| Notification center | Empty | All caught up | New notifications will appear here when someone mentions you or assigns you a task. |
| Search results | No results | No results for "flux capacitor" | Try different keywords or check your spelling. |
| Filtered list | Nothing here | No open tasks match these filters | Try adjusting your filters or clearing them to see all tasks. |

### Onboarding Text

Onboarding text guides new users through setup and first use.

**Step-by-step onboarding:**

| Step | Heading | Description |
|------|---------|-------------|
| 1 | What should we call you? | This appears on your profile and in notifications to your team. |
| 2 | Invite your team | Add team members by email. They'll get an invitation to join your workspace. |
| 3 | Create your first project | Give it a name and description. You can always change these later. |

**Onboarding rules:**
1. **Show value before asking for effort.** Let users explore before requiring account creation.
2. **One question per screen.** Do not combine name, email, and company on one screen.
3. **Reassure about reversibility.** "You can change this later" reduces decision anxiety.
4. **Use progressive profiling.** Ask for minimal information now; request more as the user engages.

### Inline Onboarding Tips

| Pattern | Example |
|---------|---------|
| Feature callout | "New: Try keyboard shortcuts. Press ? to see all shortcuts." |
| Empty state guidance | "Tip: Drag tasks between columns to update their status." |
| First-time tooltip | "This is your inbox. Messages from your team appear here." |
| Completion encouragement | "Great start! You've completed 2 of 5 setup steps." |

## See Also

- [[error-message-patterns.md]] -- Deep dive into error message types, tone calibration, and localization
- [[voice-tone-guide.md]] -- How to define and maintain consistent voice across all microcopy
- [[../../design-philosophies/references/emotional-design.md]] -- How microcopy contributes to behavioral and reflective emotional design
- [[../../design-case-studies/references/saas-dashboards.md]] -- Microcopy patterns in Stripe, Linear, and Notion
- [[../../wireframing/references/wireframe-patterns.md]] -- Wireframe annotations that specify microcopy requirements

**Back to:** [UX Writing Skill](../SKILL.md)

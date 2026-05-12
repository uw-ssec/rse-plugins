---
name: ux-writing
description: Write effective UI copy including microcopy, error messages, CTAs, onboarding flows, empty states, voice and tone documentation, help text, and localization-ready content that guides users through interfaces with clarity and empathy.
metadata:
   references:
   - references/error-message-patterns.md
   - references/microcopy-guide.md
   - references/voice-tone-guide.md
---

# UX Writing

Every word in the interface is a design decision. UX writing shapes how people navigate, understand, and feel about a product. A well-written error message can prevent a support ticket. A clear button label can increase conversions. A thoughtful empty state can turn confusion into confidence.

UX writing is not about filling in the blanks after design is done. It is an integral part of the design process, influencing layout, flow, and interaction patterns from the start.

## Quick Start: Write an Error Message

The fastest way to understand UX writing principles is through the most critical pattern: error messages. Every error message follows a three-part formula.

### The Formula: What Happened + Why + How to Fix It

**Before (bad):**
> Error: Invalid input

**After (good):**
> That email address doesn't look right. Check that it includes an "@" and a domain like "name@example.com".

**Before (bad):**
> Error 403: Forbidden

**After (good):**
> You don't have permission to view this page. Ask the project owner to share access with you.

**Before (bad):**
> Upload failed

**After (good):**
> That file is too large to upload. The maximum file size is 10 MB. Try compressing the image or choosing a smaller file.

### The Rules

1. **Say what happened** in plain language (not error codes)
2. **Explain why** without blaming the user (say "that file is too large" not "you uploaded a file that's too large")
3. **Tell them what to do next** with a specific, actionable suggestion
4. **Keep it brief** but never at the cost of clarity

## Microcopy Principles

Microcopy is the small text that guides users through interactions: button labels, form hints, tooltips, confirmation dialogs, and status messages.

### Core Principles

- **Clear over clever**: Wit is welcome when it does not sacrifice comprehension. "Got it" is better than "Roger that, Captain!"
- **Brief over verbose**: Respect the user's time and screen space. Cut every word that does not add meaning.
- **Specific over vague**: "Save to drafts" is better than "Save". "Delete this project and all its files" is better than "Delete".
- **Active voice**: "We saved your changes" not "Your changes have been saved"
- **Helpful tone**: Anticipate confusion and address it before it happens

### Common UI Text Patterns

| Element | Bad Example | Good Example | Why |
|---------|-------------|--------------|-----|
| Submit button | Submit | Create account | Specific verb describes the outcome |
| Cancel button | Cancel | Discard changes | Clarifies what canceling actually does |
| Delete confirmation | Are you sure? | Delete "Project Alpha"? This can't be undone. | Names the thing and states the consequence |
| Empty search | No results | No results for "fluxcapacitor". Try a different search term. | Reflects the query and suggests next steps |
| Loading state | Loading... | Preparing your dashboard... | Describes what is actually happening |
| Tooltip | Info | Visible to team members only | Provides the actual information |
| Form placeholder | Enter text here | jane@example.com | Shows format, not instructions |
| Success toast | Success | Invoice sent to jane@example.com | Confirms the specific action and object |

## Error Messages

Error messages are the most critical category of UX writing because they occur at moments of failure, frustration, and uncertainty.

### Anatomy of an Error Message

Every error message has up to four components:

1. **Summary**: One sentence describing what went wrong
2. **Explanation**: Why it happened (optional, include when helpful)
3. **Resolution**: What the user can do about it
4. **Action**: A button or link to take the next step (optional)

### Severity Levels

| Severity | Presentation | Use When |
|----------|-------------|----------|
| **Inline validation** | Red text below the field | A single form field has invalid input |
| **Field-level error** | Highlighted field with message | Submission attempted with errors |
| **Toast/snackbar** | Temporary overlay message | Non-blocking errors (network retry, save conflict) |
| **Banner** | Persistent banner at top of page | System-wide issues (maintenance, degraded service) |
| **Full page** | Dedicated error page | Fatal errors (404, 500, offline) |

### Five Error Message Rewrites

| Context | Before | After |
|---------|--------|-------|
| Password validation | Password too short | Use at least 8 characters for your password |
| Network timeout | Request timeout | That took too long. Check your connection and try again. |
| Rate limiting | Too many requests | You've hit the request limit. Wait a minute and try again. |
| Missing required field | Required | Add a project name to continue |
| File type mismatch | Invalid file type | Upload a PNG, JPG, or GIF image. PDFs aren't supported here. |

## Empty States

Empty states are underused opportunities to guide, educate, and encourage users. An empty screen is not a missing feature; it is a moment to build trust.

### Three Types of Empty States

**First-use empty state**: The user has never added content here.
- Show a visual (illustration or icon) that hints at what this space is for
- Write a headline that names the feature: "No projects yet"
- Write a description that explains the value: "Projects help you organize tasks, deadlines, and team members in one place."
- Provide a clear CTA: "Create your first project"

**User-cleared empty state**: The user has removed all content.
- Acknowledge the empty state: "All caught up!"
- Reinforce the value: "New tasks will appear here when assigned to you."
- Optionally provide a CTA: "Browse open tasks"

**Error empty state**: Content failed to load.
- Explain what went wrong: "Couldn't load your projects"
- Avoid blaming the user or the system excessively
- Provide a recovery action: "Try again" button
- Suggest an alternative: "Check your internet connection or visit our status page"

## Button & CTA Writing

Buttons are the most important text on any screen. They tell users what will happen when they click.

### Rules for Button Copy

- **Use specific verbs**: "Save draft", "Publish post", "Send invitation" not just "Submit"
- **Front-load the action**: "Delete account" not "Permanently remove your account from the system"
- **Match the context**: A button on a sign-up form should say "Create account", not "Submit"
- **Distinguish primary from secondary**: "Save changes" (primary) vs. "Discard" (secondary)

### Common CTA Patterns

| Action | Weak Label | Strong Label |
|--------|-----------|--------------|
| Creating something | Submit | Create project |
| Saving progress | OK | Save changes |
| Deleting something | Yes | Delete file |
| Upgrading a plan | Continue | Start free trial |
| Inviting someone | Add | Send invitation |
| Confirming a dialog | OK | Got it |
| Dismissing a warning | Close | Dismiss |
| Starting a process | Start | Generate report |

## Voice and Tone

Voice and tone are related but distinct. Understanding the difference is essential for consistent UX writing.

### Voice vs. Tone

**Voice** is the consistent personality of the product. It does not change. If your product voice is "confident, warm, and straightforward", it is always confident, warm, and straightforward.

**Tone** is the contextual expression of that voice. It changes based on the user's emotional state and the situation. A confident voice uses a reassuring tone in error messages and a celebratory tone in success states.

### Defining Voice Attributes

Pick 3-4 adjectives that describe your product's personality. For each, document:

| Attribute | This means | We do | We don't |
|-----------|-----------|-------|----------|
| **Confident** | We know our product and state things clearly | Use direct statements: "Your file is saved." | Hedge with uncertainty: "It looks like your file might be saved." |
| **Warm** | We treat users like real people | Use "you" and conversational phrasing | Sound robotic or corporate: "The user's session has been terminated." |
| **Straightforward** | We say what we mean without filler | Get to the point: "3 tasks remaining" | Pad with pleasantries: "Great news! You only have 3 tasks remaining!" |

### Tone Across Contexts

| Context | User's State | Tone | Example |
|---------|-------------|------|---------|
| Onboarding | Curious, uncertain | Encouraging, guiding | "Welcome! Let's set up your workspace in 3 steps." |
| Success | Relieved, accomplished | Celebratory, brief | "Payment processed. You're all set." |
| Error | Frustrated, confused | Empathetic, helpful | "Something went wrong. Here's what you can try." |
| Destructive action | Cautious, anxious | Clear, serious | "Delete this workspace? All projects and files will be permanently removed." |
| Waiting/loading | Impatient | Reassuring, transparent | "Generating your report. This usually takes about 30 seconds." |
| Empty state | Lost, disoriented | Encouraging, instructive | "No conversations yet. Start one by clicking New Message." |

## Deep Dive References

### [Microcopy Guide](references/microcopy-guide.md)

- Button Labels
- Form Text
- Tooltips and Help
- Navigation and Page Titles
- Confirmation Dialogs
- Success and Status Messages
- Empty States and Onboarding

### [Error Message Patterns](references/error-message-patterns.md)

- Error Anatomy
- Error Types
- Tone Calibration by Severity
- Localization Considerations
- Error Prevention Patterns
- Error Message Audit Checklist

### [Voice and Tone Guide](references/voice-tone-guide.md)

- Voice vs. Tone
- Defining Voice Attributes
- Tone Variation by Context
- Style Guide Essentials
- Inclusive Language Guidelines
- Voice Audit Process

## Next Steps

After establishing UX writing foundations, connect with related design disciplines:

- **[Accessibility Audit](../accessibility-audit/SKILL.md)**: Ensure all copy meets accessibility standards including screen reader compatibility
- **[User Research](../user-research/SKILL.md)**: Test copy effectiveness through usability testing and user interviews
- **[Information Architecture](../information-architecture/SKILL.md)**: Align copy with navigation labels, taxonomy, and content structure
- **[Design System Creation](../design-system-creation/SKILL.md)**: Document voice and tone as part of the design system

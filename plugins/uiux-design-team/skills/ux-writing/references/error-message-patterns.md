# Error Message Patterns

A comprehensive reference on error message anatomy, error types, tone calibration by severity, localization considerations, and error prevention patterns for building user-friendly error experiences.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Error Anatomy](#error-anatomy) | 14-45 | The three-part formula for every error message |
| [Error Types](#error-types) | 47-115 | Validation, permission, network, server, and not-found errors with templates |
| [Tone Calibration by Severity](#tone-calibration-by-severity) | 117-155 | Matching emotional tone to error severity |
| [Localization Considerations](#localization-considerations) | 157-195 | Writing errors that translate well across languages and cultures |
| [Error Prevention Patterns](#error-prevention-patterns) | 197-230 | Design patterns that prevent errors before they occur |
| [Error Message Audit Checklist](#error-message-audit-checklist) | 232-250 | Systematic quality check for all error messages in a product |

## Error Anatomy

Every error message must answer three questions for the user. Omitting any of the three creates confusion, frustration, or helplessness.

### The Three-Part Formula

**1. What happened?** -- State the problem in plain language. No error codes, no technical jargon, no system-oriented terminology. The user needs to understand the situation in their own terms.

**2. Why did it happen?** -- Explain the cause without blaming the user. Frame the cause as a condition rather than a user fault. Say "That file is too large" not "You uploaded a file that is too large."

**3. How do they fix it?** -- Provide a specific, actionable next step. Vague suggestions ("Try again later") are almost always less helpful than specific ones ("Check your internet connection, then try again").

### Formula in Practice

| Scenario | What Happened | Why | How to Fix |
|----------|---------------|-----|-----------|
| File upload failure | That file could not be uploaded. | It exceeds the 10 MB size limit. | Compress the file or choose a smaller one. |
| Login failure | We could not sign you in. | The email or password does not match our records. | Check your email and password, or reset your password. |
| Payment decline | Payment was not processed. | Your card was declined by the issuer. | Try a different payment method or contact your bank. |
| Rate limiting | Request could not be completed. | You have reached the rate limit for this action. | Wait a minute, then try again. |
| Session expiry | Your session has expired. | For security, sessions expire after 30 minutes of inactivity. | Sign in again to continue. |

### Anatomy Components

```
[Icon] [Summary: What happened]
[Explanation: Why it happened]
[Action: Button or link to resolve]
```

**Icon:** Use consistent semantic icons. A red circle with exclamation for errors. A yellow triangle for warnings. An orange circle for attention-needed. Icons provide instant severity recognition before the user reads the text.

**Summary line:** One sentence maximum. This is what the user reads first and may be all they read if they are scanning.

**Explanation:** One to two sentences. Optional for simple errors (inline validation) but necessary for complex errors (payment failures, system errors).

**Action:** A button, link, or instruction. "Try again," "Contact support," "Reset password," or "Go back to dashboard." Always provide an action -- never leave users at a dead end.

## Error Types

### Validation Errors

Validation errors occur when user input does not meet requirements. They should appear inline, near the field, and immediately after the user's attention leaves the field (on blur) or on form submission.

| Field | Bad Message | Good Message |
|-------|-------------|--------------|
| Email | Invalid email | Enter a valid email address (e.g., name@example.com) |
| Password | Too short | Use at least 8 characters for your password (you have 5) |
| Phone | Invalid phone | Enter a 10-digit phone number (e.g., 555-123-4567) |
| URL | Invalid URL | Include the full URL with https:// (e.g., https://example.com) |
| Date | Invalid date | Enter a date in MM/DD/YYYY format |
| Number range | Out of range | Enter a number between 1 and 100 |
| Required field | Required | Add a project name to continue |
| Character limit | Too long | 160 characters maximum (you have 203) |
| Unique constraint | Already exists | That username is taken. Try adding numbers or underscores. |
| Format mismatch | Invalid format | Enter the code in the format ABC-1234 |

**Validation error rules:**
- Show the error next to the field, not in a separate error summary (unless also showing a summary at the top for long forms)
- Show the expected format or requirement
- Show the user's current state when helpful ("you have 5" characters)
- Remove the error as soon as the input is corrected

### Permission Errors

Permission errors occur when the user attempts an action they are not authorized to perform.

| Context | Bad Message | Good Message |
|---------|-------------|--------------|
| Viewing a page | 403 Forbidden | You do not have permission to view this page. Ask the project owner to share access with you. |
| Editing a document | Access denied | This document is read-only for your role. Request edit access from the document owner. |
| Admin action | Not authorized | Only workspace admins can change billing settings. Contact your admin: admin@company.com |
| Expired invitation | Invalid link | This invitation has expired. Ask the person who invited you to send a new one. |

**Permission error rules:**
- Name the required permission or role
- Identify who can grant access (the owner, an admin, a specific person)
- Provide a way to request access when possible

### Network Errors

Network errors occur when communication between the client and server fails.

| Context | Bad Message | Good Message |
|---------|-------------|--------------|
| Request timeout | Timeout | That took too long. Check your internet connection and try again. |
| Connection lost | Error | You appear to be offline. Your changes will sync when you reconnect. |
| Slow connection | Loading... | This is taking longer than usual. You can wait or try refreshing the page. |
| DNS failure | Network error | Could not reach the server. Check your internet connection or try again in a few minutes. |

**Network error rules:**
- Never blame the user's internet (it might be the server)
- Use hedging language: "You appear to be offline" not "You are offline"
- Explain what happens to unsaved work
- Provide a retry action

### Server Errors

Server errors occur when the backend fails to process a request.

| Context | Bad Message | Good Message |
|---------|-------------|--------------|
| 500 Internal Server Error | Internal Server Error | Something went wrong on our end. Try again, and if the problem persists, contact support. |
| 502 Bad Gateway | Bad Gateway | Our servers are temporarily unavailable. This usually resolves in a few minutes. |
| 503 Service Unavailable | Service Unavailable | We are performing scheduled maintenance. We expect to be back by 3:00 PM EST. |
| Unexpected error | Unknown Error | Something unexpected happened. We have been notified and are looking into it. |

**Server error rules:**
- Take responsibility ("on our end," "we are looking into it")
- Provide a time estimate when possible
- Link to a status page if one exists
- Never expose stack traces, error codes, or technical details to users

### Not Found Errors

Not found errors occur when the requested resource does not exist.

| Context | Bad Message | Good Message |
|---------|-------------|--------------|
| 404 page | 404 Not Found | This page does not exist. It may have been moved or deleted. |
| Deleted resource | Not found | This project has been deleted. Check the trash to restore it, or return to the dashboard. |
| Broken link | Error | The page you are looking for could not be found. Here are some helpful links: [Dashboard] [Help Center] [Contact Us] |
| Search for deleted item | No results | No results found. The item may have been deleted or archived. |

**Not found error rules:**
- Suggest where the content might have moved
- Provide navigation options (search, home, popular pages)
- If the resource was deleted, mention the trash/archive if available

## Tone Calibration by Severity

Error tone must match the severity of the situation. Overly casual tone for serious errors trivializes the user's problem. Overly serious tone for minor errors creates unnecessary anxiety.

### Tone Scale

| Severity | Tone | Characteristics | Example |
|----------|------|----------------|---------|
| **Low** (inline validation) | Helpful, matter-of-fact | Short, instructional, no apology needed | "Use at least 8 characters" |
| **Medium** (recoverable error) | Empathetic, reassuring | Acknowledge the problem, provide clear resolution | "Could not save your changes. Try again." |
| **High** (data loss risk) | Serious, clear | No casual language, explicit about consequences and recovery | "This action cannot be undone. All data will be permanently deleted." |
| **Critical** (system failure) | Calm, responsible | Take ownership, provide timeline, link to status | "Our servers are experiencing issues. We are working on a fix and expect resolution within the hour." |

### Tone Calibration Rules

1. **Never use humor in error messages.** A clever 404 page is acceptable. A witty payment failure message is not. The user's frustration level is inversely proportional to how appropriate humor is.
2. **Never use exclamation marks.** "Something went wrong!" reads as either panic or false excitement. Neither is helpful.
3. **Never blame the user.** "You entered an invalid email" frames it as the user's fault. "That does not look like a valid email address" frames it as a condition.
4. **Use "we" for server errors, avoid "we" for user errors.** "We could not process your payment" (server-side ownership). "Enter a valid email address" (neutral, not "We need you to enter...").
5. **Avoid technical language.** "Authentication token expired" means nothing to most users. "Your session has ended" means something.

### Emotional Progression

For multi-step error recovery (e.g., multiple failed login attempts), the tone should progress:

| Attempt | Message | Tone Shift |
|---------|---------|-----------|
| First failure | Incorrect email or password. Try again. | Neutral, informative |
| Second failure | Still not matching. Double-check your email and password. | Slightly warmer, more helpful |
| Third failure | Having trouble? Reset your password or try a different email. | Empathetic, proactive |
| Locked out | For security, your account is temporarily locked. Try again in 15 minutes or reset your password. | Serious, explanation-focused |

## Localization Considerations

### Writing for Translation

Error messages must be written with translation in mind. Clever wordplay, idioms, and culturally specific references do not translate.

**Avoid:**
- Idioms: "Something went sideways" (does not translate)
- Contractions: "Can't" and "won't" cause inconsistency across languages
- Culturally specific references: "Houston, we have a problem"
- Puns and wordplay: "Oops, that file was a bit too big-gish"

**Prefer:**
- Simple declarative sentences: "The file exceeds the size limit."
- Consistent sentence structure: Subject-verb-object
- Standard vocabulary: Use the same word for the same concept throughout

### String Structure for Translation

| Bad (hard to translate) | Good (easy to translate) | Why |
|------------------------|--------------------------|-----|
| `"Upload failed for " + filename` | `"Could not upload {filename}"` | Placeholder syntax allows translators to reorder words |
| `count + " items deleted"` | `"{count} items deleted"` with pluralization rules | Languages have different plural forms |
| `"Error: " + errorMessage` | Separate strings for prefix and message | Concatenation assumes word order |

### Pluralization

Different languages have different plural rules. English has two forms (1 item, 2 items). Russian has three. Arabic has six. Use ICU message format or a localization library that handles plural rules:

```
{count, plural,
  =0 {No files were uploaded.}
  one {1 file was uploaded.}
  other {{count} files were uploaded.}
}
```

### Cultural Sensitivity

- Some cultures find directness rude. "Enter your email" may need softening to "Please enter your email address" in Japanese localization.
- Color associations for error states vary (red is not universally negative). Pair color with icons and text.
- Date, time, and number formats must localize (MM/DD/YYYY vs DD/MM/YYYY).
- Currency symbols, decimal separators, and thousand separators vary by locale.

## Error Prevention Patterns

The best error message is the one that never appears. These design patterns prevent errors before they occur.

### Input Constraints

| Pattern | Implementation | Prevents |
|---------|---------------|----------|
| Input masking | Phone: (___) ___-____ auto-formats as user types | Format errors |
| Character counter | "47/160 characters" visible as user types | Over-limit errors |
| Type-specific keyboards | `inputmode="numeric"` for phone numbers on mobile | Wrong character types |
| Date pickers | Calendar widget instead of free text | Invalid date entries |
| Autocomplete | Suggest valid options as user types | Spelling and format errors |
| Disabled submit | Submit button disabled until all required fields valid | Submission with missing data |

### Confirmation Patterns

| Pattern | Implementation | Prevents |
|---------|---------------|----------|
| Undo instead of confirm | "Message deleted. Undo" toast with 10-second window | Accidental deletion (without dialog interruption) |
| Type to confirm | "Type DELETE to confirm" for irreversible actions | Accidental destructive actions |
| Delay send | "Sending in 5 seconds... Cancel" | Accidental sends |
| Draft auto-save | Save draft automatically every 30 seconds | Data loss from browser crash or navigation |
| Exit warning | "You have unsaved changes" on navigation away | Accidental data loss |

### Smart Defaults

| Pattern | Implementation | Prevents |
|---------|---------------|----------|
| Timezone auto-detection | Pre-select timezone from browser | Wrong timezone selection |
| Currency from locale | Default to user's locale currency | Wrong currency selection |
| Suggested values | "Most teams choose [default]" | Decision paralysis and suboptimal choices |
| Remember preferences | Pre-fill from last submission | Repetitive data entry errors |

## Error Message Audit Checklist

Use this checklist to evaluate every error message in your product:

- [ ] **What happened** is stated in plain language (no error codes, no jargon)
- [ ] **Why it happened** is explained without blaming the user
- [ ] **How to fix it** provides a specific, actionable next step
- [ ] **Tone matches severity** (low=matter-of-fact, medium=empathetic, high=serious, critical=calm)
- [ ] **No technical language** (no "403," "null," "exception," "token," "parse")
- [ ] **No humor** in error states involving data loss, payment, or security
- [ ] **Specific, not generic** ("Enter a valid email" not "Invalid input")
- [ ] **Action available** (retry button, help link, support contact -- never a dead end)
- [ ] **Accessible** (error text associated with the field via aria-describedby, not color-only)
- [ ] **Translatable** (no idioms, no concatenated strings, no hardcoded plurals)
- [ ] **Consistent** (same error type uses same pattern across the entire product)
- [ ] **Tested** with real users to verify comprehension and recovery success

## See Also

- [[microcopy-guide.md]] -- Comprehensive patterns for all UI text types including non-error messages
- [[voice-tone-guide.md]] -- How brand voice adapts to error contexts
- [[../../design-philosophies/references/dieter-rams-principles.md]] -- Principle 6 (honest) and Principle 8 (thorough) applied to error states
- [[../../design-philosophies/references/emotional-design.md]] -- Error messages as behavioral-level emotional design
- [[../../design-handoff/references/annotation-guide.md]] -- How to annotate error states in design handoff documentation

**Back to:** [UX Writing Skill](../SKILL.md)

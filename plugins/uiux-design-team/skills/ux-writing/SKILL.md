---
name: ux-writing
description: Use when writing or auditing UI copy — button labels, error messages, empty states, onboarding flows, confirmation dialogs, tooltips, success toasts — or when establishing voice and tone documentation for a product.
metadata:
   references:
   - references/error-message-patterns.md
   - references/microcopy-guide.md
   - references/voice-tone-guide.md
---

# UX Writing

## End-to-End Workflow

For every piece of UI copy, run these five steps in order.

**1. Identify UI context.** Which pattern? (button, error, empty state, onboarding, success toast, confirmation, tooltip, placeholder) Match to a template in [Microcopy Guide](references/microcopy-guide.md) or [Error Message Patterns](references/error-message-patterns.md).

**2. Determine user emotional state.** Curious, frustrated, anxious, accomplished, lost? Look up the row in the Tone Across Contexts table in [Voice & Tone Guide](references/voice-tone-guide.md).

**3. Apply voice + tone.** Voice is constant (the product's personality). Tone shifts by context. Pick the tone row that matches step 2.

**4. Write the copy using a pattern below.**

**5. Validate against the checklist at the bottom.** If any item fails, revise.

## Pattern: Error Message (formula)

`What happened + Why (optional) + How to fix it`

| Before | After |
|--------|-------|
| Error: Invalid input | That email address doesn't look right. Check that it includes an "@" and a domain like name@example.com. |
| Error 403: Forbidden | You don't have permission to view this page. Ask the project owner to share access with you. |
| Upload failed | That file is too large. Max upload is 10 MB. Try compressing the image or choosing a smaller file. |
| Password too short | Use at least 8 characters for your password. |
| Request timeout | That took too long. Check your connection and try again. |
| Too many requests | You've hit the request limit. Wait a minute and try again. |
| Required | Add a project name to continue |
| Invalid file type | Upload a PNG, JPG, or GIF. PDFs aren't supported here. |

**Rules:**
1. Plain language, not error codes.
2. Don't blame the user ("That file is too large" not "You uploaded a file that's too large").
3. Always give a next step.
4. Brief, but never at the cost of clarity.

## Pattern: Severity → Presentation

| Severity | Presentation | Use when |
|----------|-------------|----------|
| Inline validation | Red text below field | One field invalid |
| Field-level error | Highlighted field + message | Submission with errors |
| Toast/snackbar | Temporary overlay | Non-blocking (network retry) |
| Banner | Persistent banner | System-wide (maintenance) |
| Full page | Dedicated error page | Fatal (404, 500, offline) |

## Pattern: Button / CTA

- Use specific verbs: "Save draft", "Publish post", "Send invitation" — not "Submit".
- Front-load the action: "Delete account" not "Permanently remove your account from the system".
- Match context: sign-up form → "Create account", not "Submit".

Full table: [Microcopy Guide → Button & CTA Patterns](references/microcopy-guide.md).

## Pattern: Empty State

Three types — first-use, user-cleared, error. Full templates in [Microcopy Guide → Empty State Type Templates](references/microcopy-guide.md).

## Voice vs. Tone (quick definitions)

- **Voice** = the product's consistent personality (does not change).
- **Tone** = how voice expresses in this specific context (changes with user emotional state).

Full voice attribute table and tone-by-context table: [Voice & Tone Guide](references/voice-tone-guide.md).

## Core Microcopy Principles

- **Clear over clever** — "Got it" beats "Roger that, Captain!"
- **Brief over verbose** — cut every word that doesn't add meaning.
- **Specific over vague** — "Save to drafts" beats "Save".
- **Active voice** — "We saved your changes" not "Your changes have been saved".

## Validation Checklist

For every piece of copy, confirm:

- [ ] Reads aloud naturally in under 3 seconds.
- [ ] No error codes, jargon, or internal system terms.
- [ ] User knows what to do next (action verb or clear path).
- [ ] No blame language ("you uploaded a bad file" → "that file isn't supported").
- [ ] Button label names the outcome, not "Submit"/"OK".
- [ ] Tone matches user emotional state (see Tone table).
- [ ] Localizable: no idioms, contractions handled, no concatenated strings.
- [ ] Plural and zero states both written ("0 results", "1 result", "5 results").
- [ ] Under context-appropriate length: button ≤ 3 words, toast ≤ 60 chars, error summary ≤ 12 words.

If any item fails → revise and re-validate.

## Deep Dive References

- [Microcopy Guide](references/microcopy-guide.md) — Buttons, forms, tooltips, navigation, dialogs, status messages, empty states
- [Error Message Patterns](references/error-message-patterns.md) — Anatomy, types, tone calibration, localization, prevention, audit checklist
- [Voice & Tone Guide](references/voice-tone-guide.md) — Voice attribute table, tone-by-context table, style guide essentials, inclusive language, audit process

## Next Steps

- **[Accessibility Audit](../accessibility-audit/SKILL.md)**: Verify copy works with screen readers
- **[User Research](../user-research/SKILL.md)**: Test copy effectiveness with users
- **[Information Architecture](../information-architecture/SKILL.md)**: Align copy with navigation labels
- **[Design System Creation](../design-system-creation/SKILL.md)**: Document voice and tone in the system

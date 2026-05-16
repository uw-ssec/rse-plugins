# Voice and Tone Guide

A comprehensive reference on defining brand voice through 4 voice attributes, varying tone by context, building style guide essentials, and writing inclusive language guidelines for consistent, respectful UX writing.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Voice vs. Tone](#voice-vs-tone) | 14-30 | The fundamental distinction between voice and tone |
| [Defining Voice Attributes](#defining-voice-attributes) | 32-80 | The 4-attribute framework for documenting brand voice |
| [Tone Variation by Context](#tone-variation-by-context) | 82-130 | How tone shifts across celebration, error, instruction, and marketing |
| [Style Guide Essentials](#style-guide-essentials) | 132-185 | Contractions, pronouns, technical terms, punctuation, and formatting |
| [Inclusive Language Guidelines](#inclusive-language-guidelines) | 187-235 | Writing that respects and includes all users |
| [Voice Audit Process](#voice-audit-process) | 237-250 | Evaluating and improving voice consistency across a product |

## Voice vs. Tone

**Voice** is the consistent personality of your product. It does not change. It is who you are. If your voice is confident, warm, and clear, it is always confident, warm, and clear -- in a success message, in an error, in marketing, and in documentation.

**Tone** is the contextual expression of that voice. It changes based on the user's emotional state and the situation. A confident voice uses a reassuring tone in error messages and a celebratory tone in success states. Tone is how you say it given the context.

**Analogy:** A person has one personality (voice) but adapts their demeanor (tone) to the situation. They are the same person at a funeral (somber tone) and a birthday party (cheerful tone), but their fundamental personality traits remain consistent.

Understanding this distinction is essential. Without it, teams either write with inconsistent personality across screens (no voice) or write with identical energy everywhere regardless of context (no tone variation).

## Defining Voice Attributes

The most effective approach is to define exactly 4 voice attributes. Fewer than 4 is too vague. More than 4 is too many to remember and apply consistently.

### The 4-Attribute Framework

For each attribute, document:

| Column | Purpose |
|--------|---------|
| **Attribute** | The adjective that describes the voice (e.g., "Confident") |
| **This means** | What the attribute looks like in practice |
| **We do** | Concrete examples of copy that embodies this attribute |
| **We don't** | Concrete examples of copy that violates this attribute |
| **Spectrum position** | Where this attribute sits between extremes (e.g., "Confident, not arrogant") |

### Example: Developer Tool Voice

| Attribute | This Means | We Do | We Don't |
|-----------|-----------|-------|----------|
| **Direct** | We state things plainly without filler or hedging | "Deployment failed. Check your build logs." | "It looks like there might have been an issue with your deployment process." |
| **Knowledgeable** | We know our domain and communicate with expertise | "The API returns a 429 when you exceed 100 requests per minute." | "Oops, something went wrong with the thing you were trying to do!" |
| **Respectful** | We value the user's time and intelligence | "3 errors in config.yml. See details." | "Great news! We found some little issues we can help you fix!" |
| **Supportive** | We help users succeed without condescending | "New to webhooks? Here's a 2-minute guide." | "WARNING: Webhooks are an advanced feature. Proceed with caution." |

### Example: Consumer Wellness App Voice

| Attribute | This Means | We Do | We Don't |
|-----------|-----------|-------|----------|
| **Warm** | We treat users like friends, not customers | "Welcome back. Ready to start your day?" | "User session initiated. Select a program." |
| **Encouraging** | We celebrate progress and normalize setbacks | "5 days in a row. You're building a habit." | "You missed 3 days. Get back on track!" |
| **Clear** | We explain without jargon or ambiguity | "Breathe in for 4 seconds, hold for 4, out for 4." | "Perform a 4-4-4 box breathing protocol cycle." |
| **Honest** | We set realistic expectations | "Most people notice changes after 2-3 weeks of daily practice." | "Transform your life in just 7 days!" |

### Spectrum Positioning

Each attribute should be positioned between two extremes to prevent misinterpretation:

| Attribute | Not This... | ...This... | ...Not This |
|-----------|-------------|-----------|-------------|
| Confident | Timid, hedging | Confident | Arrogant, condescending |
| Friendly | Robotic, corporate | Friendly | Overly casual, unprofessional |
| Playful | Boring, dry | Playful | Flippant, inappropriate in serious contexts |
| Expert | Dumbed down | Expert | Jargon-heavy, gatekeeping |

## Tone Variation by Context

### Celebration Contexts

When users accomplish something, the tone should acknowledge their achievement without excessive enthusiasm.

| User Action | Weak Tone | Appropriate Tone | Excessive Tone |
|-------------|-----------|-------------------|----------------|
| Completed setup | Done. | You're all set. Time to explore. | OMG YAAAAS! You did it! |
| First sale | Transaction complete. | Your first sale! $49.99 from Sarah Chen. | AMAZING!!! You just made your first EVER sale!!! |
| Reached milestone | 100 tasks done. | 100 tasks completed. That's a milestone. | WOW! 100 tasks! You're a productivity SUPERSTAR! |

**Celebration tone rules:**
- Match the significance of the achievement. A first sale deserves more acknowledgment than saving a draft.
- Use the user's data to personalize ("$49.99 from Sarah Chen" not just "a sale").
- Keep it brief. Celebration copy that requires reading has missed the point.

### Error Contexts

When something goes wrong, the tone should be empathetic without being emotional.

| Severity | Tone | Example |
|----------|------|---------|
| Minor (inline validation) | Matter-of-fact | "Use at least 8 characters" |
| Moderate (action failed) | Empathetic | "Could not save your changes. Try again." |
| Serious (data at risk) | Clear, serious | "Your changes have not been saved. Copy your work before refreshing." |
| Critical (system down) | Calm, responsible | "We are experiencing an outage. Our team is working on it. Updated status at status.example.com." |

**Error tone rules:**
- Never use humor, exclamation marks, or casual language.
- Take responsibility for system errors ("on our end").
- Avoid blame language for user errors ("That email doesn't look right" not "You entered an invalid email").

### Instructional Contexts

When teaching or guiding, the tone should be clear and confidence-building.

| Context | Weak Instruction | Strong Instruction |
|---------|------------------|-------------------|
| Onboarding | Follow the steps below. | Let's set up your workspace. This takes about 2 minutes. |
| Feature education | Click here to learn more. | Keyboard shortcuts save time. Press ? to see them all. |
| Complex task | Complete the form. | Start with your company name. We'll use it in invoices and emails to your clients. |

**Instructional tone rules:**
- Use second person ("you") and, sparingly, first person plural ("we'll," "let's").
- Provide time estimates ("about 2 minutes").
- Explain why, not just what.
- Break complex instructions into numbered steps.

### Marketing Contexts

Marketing copy has more tonal freedom than product copy, but the voice must remain consistent.

| Context | Product Tone | Marketing Tone |
|---------|-------------|----------------|
| Feature announcement | New: Filter tasks by priority. | Spend less time searching, more time doing. Priority filters are here. |
| Pricing page | $10/month per user, billed annually. | Everything your team needs to ship faster. Starting at $10/month. |
| Upgrade prompt | Upgrade to access advanced analytics. | See the full picture. Advanced analytics help you spot trends before they become problems. |

**Marketing tone rules:**
- Lead with the user benefit, not the feature.
- Use slightly more emotional language than product copy.
- Keep the same voice attributes. If the product is "direct," the marketing should also be direct, not flowery.

## Style Guide Essentials

### Contractions

| Decision | Guidance |
|----------|---------|
| Use contractions | For consumer products, friendly tools, and conversational voice ("You're all set," "Can't find what you need?") |
| Avoid contractions | For enterprise products, legal text, serious error messages, and formal contexts ("You are not authorized") |
| Be consistent | Choose one approach and apply it everywhere. Mixing "you're" and "you are" within the same product creates tonal inconsistency. |

### Pronouns

| Pronoun | Usage | Example |
|---------|-------|---------|
| **You/Your** | Address the user directly. Primary pronoun in product copy. | "Your changes have been saved." |
| **We/Our** | Refer to the product team. Use sparingly. | "We'll send a confirmation email." |
| **I/My** | Use in UI elements where the user is the agent (rare). | "My account," "I agree to the terms" |
| **They/Their** | Use as singular pronoun when gender is unknown. | "When a team member joins, they'll receive an email." |

### Technical Terms

| Decision | Guidance |
|----------|---------|
| Define on first use | "Webhooks (automatic notifications sent when events occur in your account)" |
| Use plain language equivalents | "Your web address" instead of "your URL" for non-technical audiences |
| Be consistent | Pick one term and use it everywhere. Do not alternate between "workspace," "organization," and "account." |
| Match user vocabulary | If your users say "repo," use "repo." If they say "repository," use "repository." |

### Capitalization

| Element | Convention | Example |
|---------|-----------|---------|
| Headings | Sentence case (capitalize first word only) | "Account settings" not "Account Settings" |
| Button labels | Sentence case | "Save changes" not "Save Changes" |
| Navigation items | Sentence case | "My projects" not "My Projects" |
| Product names | As branded | "GitHub," "macOS," "iPhone" |
| Feature names | Lowercase unless a proper noun | "dark mode" not "Dark Mode" |

### Numbers

| Context | Convention | Example |
|---------|-----------|---------|
| Counts under 10 | Spell out | "three tasks remaining" |
| Counts 10 and above | Use numerals | "47 tasks remaining" |
| Measurements | Always numerals | "5 MB," "3 minutes," "100%" |
| Dates | Consistent format | "February 16, 2026" or "Feb 16, 2026" (choose one) |
| Money | Currency symbol, two decimals | "$49.99" not "$49.99 USD" (unless multi-currency) |

### Punctuation

| Element | Rule |
|---------|------|
| Periods in UI copy | Use in full sentences. Omit in fragments, labels, and headings. |
| Oxford comma | Use it. "Tasks, projects, and milestones" not "Tasks, projects and milestones." |
| Exclamation marks | Use at most one per screen, and only in genuinely exciting moments. Never in errors. |
| Ellipsis | Use for truncated text ("Website Redesig...") and ongoing processes ("Saving..."). Not for dramatic effect. |

## Inclusive Language Guidelines

### Gender-Inclusive Language

| Instead of | Use |
|-----------|-----|
| He/she | They |
| Guys | Everyone, folks, team, people |
| Mankind | Humanity, people |
| Man-hours | Person-hours, work hours |
| Chairman | Chair, chairperson |
| Manmade | Artificial, synthetic, human-made |

### Ability-Inclusive Language

| Instead of | Use |
|-----------|-----|
| See the results | View the results, check the results |
| Click here | Select, choose, tap (context-appropriate) |
| Blind spot | Oversight, gap |
| Crippling bug | Critical bug, severe bug |
| Sanity check | Quick check, review, validation |
| Crazy, insane | Unexpected, surprising, remarkable |
| Dumb it down | Simplify, make accessible |

### Race and Culture-Inclusive Language

| Instead of | Use |
|-----------|-----|
| Blacklist/whitelist | Blocklist/allowlist, denylist/safelist |
| Master/slave | Primary/replica, leader/follower, main/secondary |
| Master branch | Main branch |
| Native feature | Built-in feature |
| Grandfathered | Legacy, exempt |

### Age-Inclusive Language

- Do not assume digital literacy. Provide clear instructions for all interactions.
- Avoid generational labels ("millennials prefer...") in product copy.
- Do not use youth-oriented slang in product interfaces ("lit," "slay," "vibe check").

### Writing for Global Audiences

- Avoid idioms and colloquialisms ("hit the ground running," "low-hanging fruit").
- Use simple sentence structures (subject-verb-object).
- Avoid humor that depends on cultural context.
- Use internationally recognized date and number formats, or localize them.

### Inclusive Design in Forms

- Provide inclusive options for gender (or make it optional/free-text).
- Do not require titles (Mr./Ms./Mrs./Dr.) unless legally necessary.
- Support international name formats (not everyone has a first name and last name).
- Support international address formats.
- Provide accessible alternatives for CAPTCHA.

## Voice Audit Process

### Step 1: Inventory

Collect every piece of user-facing text in the product: buttons, labels, errors, empty states, notifications, emails, tooltips, and onboarding flows.

### Step 2: Evaluate Against Attributes

For each piece of text, score it against the 4 voice attributes on a 1-5 scale. Text that scores below 3 on any attribute needs revision.

### Step 3: Identify Inconsistencies

Look for patterns: Does the onboarding use a warm tone while the error messages use a cold tone? Does the marketing copy use different terminology than the product? Document every inconsistency.

### Step 4: Prioritize Rewrites

Focus on high-traffic, high-emotion touchpoints first: error messages, onboarding, empty states, and confirmation dialogs. These are the moments where voice matters most.

### Step 5: Create a Living Style Guide

Document the voice attributes, tone variations, and rewritten examples in a shared resource. Update it as the product and brand evolve. Review quarterly.

## Quick-Reference Voice Attribute Table

For each chosen attribute, document what it means, what you do, and what you avoid.

| Attribute | This means | We do | We don't |
|-----------|-----------|-------|----------|
| **Confident** | We know our product and state things clearly | Direct statements: "Your file is saved." | Hedge with uncertainty: "It looks like your file might be saved." |
| **Warm** | We treat users like real people | Use "you" and conversational phrasing | Sound robotic: "The user's session has been terminated." |
| **Straightforward** | We say what we mean without filler | Get to the point: "3 tasks remaining" | Pad with pleasantries: "Great news! You only have 3 tasks remaining!" |
| **Helpful** | We anticipate needs and address them | Offer the next step inline | Leave users to figure it out |
| **Honest** | We name tradeoffs and limits | "Available on paid plans" | Bury limitations in fine print |

## Tone Across Contexts

| Context | User's State | Tone | Example |
|---------|-------------|------|---------|
| Onboarding | Curious, uncertain | Encouraging, guiding | "Welcome! Let's set up your workspace in 3 steps." |
| Success | Relieved, accomplished | Celebratory, brief | "Payment processed. You're all set." |
| Error | Frustrated, confused | Empathetic, helpful | "Something went wrong. Here's what you can try." |
| Destructive action | Cautious, anxious | Clear, serious | "Delete this workspace? All projects and files will be permanently removed." |
| Waiting/loading | Impatient | Reassuring, transparent | "Generating your report. This usually takes about 30 seconds." |
| Empty state | Lost, disoriented | Encouraging, instructive | "No conversations yet. Start one by clicking New Message." |

## See Also

- [[microcopy-guide.md]] -- Practical patterns for every UI text type, informed by voice and tone decisions
- [[error-message-patterns.md]] -- Error-specific tone calibration and message templates
- [[../../design-philosophies/references/emotional-design.md]] -- Voice and tone as reflective-level emotional design tools
- [[../../design-case-studies/references/e-commerce.md]] -- How Glossier, Aesop, and Apple use voice as a brand differentiator
- [[../../design-case-studies/references/brand-experiences.md]] -- Brand voice as a design material across digital experiences

**Back to:** [UX Writing Skill](../SKILL.md)

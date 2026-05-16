# Persona Templates

Comprehensive templates and patterns for creating evidence-based user personas that drive design decisions.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Full Persona Template](#full-persona-template) | 18-67 | Complete template with all standard fields and guidance |
| [Example Persona](#example-persona) | 69-115 | Filled-in persona for a SaaS product manager |
| [Proto-Persona Template](#proto-persona-template) | 117-153 | Lightweight format for early-stage research |
| [Persona Spectrum](#persona-spectrum) | 155-192 | Range-based approach instead of fixed archetypes |
| [Anti-Patterns](#anti-patterns) | 194-238 | Common mistakes that undermine persona effectiveness |
| [See Also](#see-also) | 240-246 | Related references and skills |

## Full Persona Template

Use this template when you have completed at least 5-8 user interviews and can ground every field in real data. Each field should be directly traceable to interview quotes, survey responses, or behavioral analytics.

```markdown
# [Persona Name] — [Archetype Label]

## Identity
- **Name:** [Realistic first name + last initial]
- **Role:** [Job title or primary life role]
- **Organization type:** [Company size, industry, stage]
- **Experience level:** [Years in role, technical proficiency]

## Demographics
- **Age range:** [5-year range, e.g., 30-35]
- **Location:** [Region or urban/suburban/rural]
- **Education:** [Relevant educational background]
- **Tech comfort:** [Low / Medium / High / Expert]

## Goals (prioritized)
1. [Primary goal — the thing they must accomplish]
2. [Secondary goal — important but not urgent]
3. [Aspirational goal — where they want to be in 1-2 years]

## Frustrations (prioritized)
1. [Biggest pain point — costs time, money, or credibility]
2. [Recurring annoyance — happens frequently, erodes satisfaction]
3. [Systemic blocker — organizational or environmental constraint]

## Behaviors
- **Daily tools:** [Software, platforms, communication channels]
- **Information sources:** [How they learn, stay current]
- **Decision process:** [How they evaluate and choose solutions]
- **Collaboration style:** [Async vs. sync, documentation habits]

## Jobs to Be Done
- **Primary JTBD:** "When [situation], I want to [motivation], so I can [expected outcome]."
- **Emotional JTBD:** "When [situation], I want to feel [emotion], so I can [outcome]."

## Scenarios
- **Typical day:** [Brief narrative of a representative workday]
- **Trigger moment:** [What event causes them to seek a solution]

## Representative Quote
> "[Direct quote or composite from interviews that captures their mindset]"

## Data Sources
- [Number] interviews conducted on [date range]
- [Survey name] with [N] respondents
- [Analytics source] behavioral data
```

**Guidance:** Every field should be defensible. If you cannot point to research data that supports a field, mark it as an assumption and flag it for validation.

## Example Persona

This persona was created from 7 interviews with product managers at B2B SaaS companies (Series A through Series C).

```markdown
# Priya K. — The Data-Driven PM

## Identity
- **Name:** Priya K.
- **Role:** Senior Product Manager
- **Organization type:** B2B SaaS, 80-200 employees, Series B
- **Experience level:** 5-8 years in product, high technical proficiency

## Demographics
- **Age range:** 30-35
- **Location:** Urban, US West Coast or remote
- **Education:** CS or business degree, often both
- **Tech comfort:** Expert

## Goals
1. Ship features that measurably improve retention metrics
2. Build a repeatable process for prioritizing the backlog
3. Transition from reactive feature requests to proactive product strategy

## Frustrations
1. User feedback is scattered across Slack, email, support tickets, and sales calls
   with no single source of truth
2. Stakeholders override data-backed priorities with anecdotes from one customer
3. Difficult to measure whether shipped features actually solved the intended problem

## Behaviors
- **Daily tools:** Linear, Figma, Slack, Amplitude, Notion
- **Information sources:** Lenny's Newsletter, podcasts during commute, peer PM Slack communities
- **Decision process:** Gathers quantitative evidence first, then validates with 3-5 user calls
- **Collaboration style:** Async-first, writes detailed PRDs, prefers Loom over meetings

## Jobs to Be Done
- **Primary JTBD:** "When I am planning next quarter's roadmap, I want to quantify
  which user problems matter most, so I can defend my prioritization to the executive team."
- **Emotional JTBD:** "When I present to leadership, I want to feel confident
  in my reasoning, so I can maintain credibility even when challenged."

## Scenarios
- **Typical day:** Starts with Amplitude dashboards, reviews user feedback digest,
  has 2-3 cross-functional syncs, writes specs in the afternoon
- **Trigger moment:** Quarterly planning approaches and she needs to justify why
  Feature X should be prioritized over Feature Y

## Representative Quote
> "I have a gut feeling about what to build, but gut feelings don't survive a board meeting.
> I need the data to back it up."

## Data Sources
- 7 interviews conducted Jan 10-24, 2026
- PM Workflow Survey with 43 respondents
- Amplitude behavioral data from 3 partner companies
```

## Proto-Persona Template

Use proto-personas when you do not yet have research data but need to align the team on shared assumptions before starting research. Proto-personas are hypotheses, not facts. They should be validated or replaced after interviews.

```markdown
# Proto-Persona: [Name]

## Who they are (our best guess)
- **Role:** [Assumed job title or role]
- **Context:** [Assumed environment and constraints]

## What they are trying to do
- [Assumed primary goal]
- [Assumed secondary goal]

## What gets in their way
- [Assumed frustration 1]
- [Assumed frustration 2]

## How they currently solve it
- [Current workaround or tool they use]

## Open questions (to validate in research)
- [ ] Is [assumption] actually true?
- [ ] Do they really prioritize [goal] over [other goal]?
- [ ] What are we missing about their context?
```

**Rules for proto-personas:**
- Label them clearly as "Proto-Persona" everywhere they appear
- Time-box their lifespan: they expire after 4-6 weeks or after the first round of interviews
- Treat every field as a hypothesis to be tested, not a fact to be designed against
- Use them to write screener surveys and interview guides, not to make design decisions

## Persona Spectrum

The persona spectrum approach replaces fixed archetypes with continuous ranges. This avoids the trap of designing for a single fictional individual and instead acknowledges that users exist on a continuum.

**How it works:** Instead of saying "Our persona is a 32-year-old product manager," define the spectrum along the dimensions that actually affect design decisions.

```markdown
# Persona Spectrum: [Product Name]

## Relevant Dimensions

### Technical Proficiency
Low ←————————————————→ High
[Non-technical users who     [Developers and power users
 need guided workflows]       who prefer keyboard shortcuts]

### Usage Frequency
Occasional ←————————————→ Daily
[Monthly check-ins,           [Lives in the product all day,
 low feature familiarity]      knows every shortcut]

### Decision Authority
Individual ←————————————→ Team Lead
[Makes personal choices,      [Decisions affect 10+ people,
 no approval needed]           needs audit trails and reports]

### Data Comfort
Narrative ←————————————→ Quantitative
[Prefers stories and          [Prefers charts, dashboards,
 qualitative evidence]         and statistical analysis]
```

**When to use the spectrum approach:**
- Your product serves a very diverse audience (e.g., a platform used by both individual creators and enterprise teams)
- Traditional personas are creating false precision (the team treats demographic details as requirements)
- You want to design for the extremes and verify that the middle is also served

**How to identify the right dimensions:** Look at your interview data for the variables that most strongly predict different behaviors, needs, and preferences. Demographics (age, gender, location) are rarely the right dimensions. Behavioral and attitudinal differences (technical skill, frequency of use, risk tolerance) are almost always more useful.

## Anti-Patterns

These common mistakes reduce persona effectiveness and can actively mislead the design team.

**Fictional demographics.** Assigning specific ages, hobbies, and personal details that are not supported by research. If you write "Sarah, 34, enjoys hiking and has two cats," the team will remember the cats and forget the goals. Only include details that influence design decisions.

**Stereotyping.** Building personas around demographic stereotypes rather than behavioral evidence. "Millennials prefer mobile" or "Executives don't have time to read" are assumptions that must be validated, not starting points.

**Too many personas.** Creating 8-12 personas dilutes focus. Most products need 2-4 personas. If you have more than 4, look for personas that can be merged based on overlapping goals and frustrations.

**The elastic persona.** A persona that is so broadly defined it can justify any design decision. If your persona's goals are "wants things to be easy" and "wants to save time," that describes every human, not a specific user segment.

**The aspirational persona.** Designing for the user you wish you had rather than the user you actually have. This is common in B2B products where the persona reflects the buyer (VP of Engineering) rather than the actual daily user (individual developer).

**Set-and-forget.** Creating personas once and never updating them. Users evolve, markets shift, and products change. Review and refresh personas at least annually or after major product pivots.

**No behavioral basis.** Building personas around demographics and psychographics rather than observable behaviors. Two users with identical demographics may use your product in completely different ways. Behavior is what matters for design.

**Ignoring non-users.** Only studying current users misses the people who tried and left, or who never tried at all. Include churned users and prospect non-adopters in your research to understand barriers to adoption.

## See Also

- [[interview-guide.md]] -- Structure interviews that generate the data needed to build strong personas
- [[synthesis-methods.md]] -- Synthesize interview data into the clusters that become personas
- [[jtbd-framework.md]] -- Define the jobs that give personas their purpose and design relevance
- [[journey-template.md]] -- Map the journey each persona takes through your product

**Back to:** [User Research Skill](../SKILL.md)

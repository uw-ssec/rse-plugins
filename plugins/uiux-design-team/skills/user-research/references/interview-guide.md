# Interview Guide

A complete guide to planning, conducting, and synthesizing user interviews that produce actionable design insights.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Interview Planning](#interview-planning) | 16-52 | Goals, screener criteria, recruitment, and logistics |
| [Script Structure](#script-structure) | 54-102 | Four-phase interview script with timing guidance |
| [Question Types](#question-types) | 104-157 | Open-ended, probing, clarifying, and hypothetical questions with examples |
| [Note-Taking Template](#note-taking-template) | 159-195 | Structured template for capturing observations during interviews |
| [Remote vs. In-Person](#remote-vs-in-person) | 197-225 | Considerations for each format and hybrid approaches |
| [Common Mistakes](#common-mistakes) | 227-264 | Frequent errors that compromise interview quality |
| [Post-Interview Synthesis](#post-interview-synthesis) | 266-295 | Processing raw notes into usable insights |
| [See Also](#see-also) | 297-303 | Related references and skills |

## Interview Planning

**Define research goals.** Before writing a single question, articulate what you need to learn. Frame goals as questions: "How do users currently discover new features?" not "Validate that users like the new onboarding." Research should seek understanding, not confirmation.

Write 3-5 research questions. Every interview question you later draft should trace back to one of these goals.

**Create a screener.** A screener survey identifies qualified participants. Include:
- Role or job title criteria (must match your target persona)
- Relevant experience criteria (e.g., "Has used a project management tool in the past 6 months")
- Disqualifying criteria (e.g., works at a competitor, works in UX research)
- A question that tests genuine experience rather than self-reported expertise

Example screener question: "In the past month, approximately how many times did you use [product category]?" This filters for active users rather than people who vaguely remember trying a tool once.

**Recruit participants.** Aim for 5-8 participants per persona segment. Sources include:
- Existing user base (support tickets, active accounts, community members)
- Recruitment panels (UserTesting, Respondent, User Interviews)
- Social media and professional communities
- Guerrilla recruiting (in relevant contexts only)

**Logistics:**
- Schedule 45-60 minutes per session (30 min interview + buffer)
- Record with consent (audio at minimum, video when possible)
- Have two team members present: one interviewer, one note-taker
- Prepare a consent form that explains recording, data usage, and confidentiality
- Offer appropriate compensation ($50-150 for consumer, $150-300 for professional/enterprise)

## Script Structure

A consistent script structure ensures coverage while maintaining conversational flow. Adapt the content but keep the phases.

**Phase 1: Introduction and Rapport (3-5 minutes)**

```
"Thank you for taking the time to speak with us today. I'm [name], and I'm a
[role] working on [product/project]. We're trying to understand how people
like you [broad topic area].

There are no right or wrong answers. We're here to learn from your experience.
Everything you share will be kept confidential and used only to improve our
product. Is it okay if we record this conversation for our notes?

Before we begin, do you have any questions for me?"
```

**Phase 2: Warm-Up Questions (5-7 minutes)**

Start with broad, easy questions that establish context and build comfort:
- "Tell me a little about your role and what a typical day looks like."
- "How long have you been in this role?"
- "What tools do you use most frequently in your work?"

These questions are not throwaway. They establish the participant's context, which you will need when interpreting their later answers.

**Phase 3: Core Questions (15-20 minutes)**

This is the heart of the interview. Structure questions around your research goals, moving from general to specific:
- Start with open-ended behavioral questions: "Walk me through the last time you..."
- Follow up with probing questions when you hear something interesting
- Explore pain points: "What was the hardest part of that experience?"
- Explore workarounds: "How do you handle that today?"
- Explore motivation: "Why is that important to you?"

Use the "critical incident technique": ask about a specific recent event rather than general habits. "Tell me about the last time you had to create a report for your manager" yields richer data than "How do you usually create reports?"

**Phase 4: Wrap-Up (3-5 minutes)**

```
"We're coming up on time. A few closing questions:
- Is there anything I should have asked but didn't?
- Is there anything else you'd like to share about your experience with [topic]?
- Would it be okay to follow up if we have additional questions?

Thank you so much for your time today. Your perspective is really valuable."
```

Always ask "Is there anything I should have asked?" -- participants frequently volunteer their most important insight when given this open door.

## Question Types

**Open-ended questions** -- Invite narrative responses. These are your primary tool.
- "Tell me about a time when..."
- "Walk me through how you..."
- "What happened next?"
- "How did that make you feel?"
- "What was going through your mind when..."

**Probing questions** -- Dig deeper into something the participant said.
- "You mentioned [X]. Can you tell me more about that?"
- "What do you mean by [term they used]?"
- "Why do you think that happened?"
- "How often does that occur?"
- "Can you give me a specific example?"

**Clarifying questions** -- Ensure you understand correctly.
- "So if I understand correctly, you're saying..."
- "When you say [X], do you mean [interpretation A] or [interpretation B]?"
- "Let me make sure I'm following: first you [A], then you [B]?"

**Hypothetical questions** -- Use sparingly, as hypothetical answers are unreliable.
- "If you could change one thing about this process, what would it be?" (acceptable)
- "Imagine you had a tool that could do [X]. How would you use it?" (acceptable with caution)

**Questions to AVOID:**

| Type | Bad Example | Why It Fails | Better Alternative |
|------|-------------|--------------|-------------------|
| Leading | "Don't you think the dashboard is confusing?" | Suggests the expected answer | "How would you describe your experience with the dashboard?" |
| Loaded | "How frustrated are you with the current process?" | Assumes frustration exists | "How do you feel about the current process?" |
| Closed | "Do you like the new feature?" | Produces yes/no with no depth | "Tell me about your experience with the new feature." |
| Future-predicting | "Would you use this feature?" | People cannot predict future behavior | "Tell me about a time when you needed to [thing the feature does]." |
| Double-barreled | "How do you feel about the speed and reliability?" | Asks two things at once | Ask about speed and reliability separately |

## Note-Taking Template

Use this template during each interview. The note-taker fills in real-time while the interviewer maintains eye contact and conversational flow.

```markdown
# Interview Notes

## Metadata
- **Participant:** [ID or pseudonym, never real name in shared docs]
- **Date:** [YYYY-MM-DD]
- **Duration:** [minutes]
- **Interviewer:** [name]
- **Note-taker:** [name]
- **Recording link:** [URL or file path]

## Context
- **Role:** [participant's role]
- **Experience:** [years, relevant background]
- **Tools mentioned:** [list tools they reference]

## Key Observations
### Goals
- [What are they trying to accomplish?]

### Pain Points
- [What frustrates them? Where do they struggle?]

### Workarounds
- [How do they solve problems the product doesn't solve?]

### Surprises
- [What did you hear that you didn't expect?]

### Notable Quotes
- "[Verbatim quote]" — context: [when/why they said it]
- "[Verbatim quote]" — context: [when/why they said it]

## Emotional Moments
- [Moment where participant showed strong emotion, positive or negative]

## Follow-Up Questions
- [Questions you wish you had asked or want to explore next time]

## Debrief Notes (filled in immediately after interview)
- **Top 3 takeaways:**
  1. [Most important thing learned]
  2. [Second most important]
  3. [Third most important]
- **How does this compare to other interviews?**
  [Patterns emerging, contradictions, new themes]
```

**Debrief immediately.** Within 15 minutes of ending the interview, the interviewer and note-taker should spend 5-10 minutes discussing their top takeaways. Memory degrades rapidly; capture impressions while they are fresh.

## Remote vs. In-Person

**In-person advantages:**
- Richer body language and environmental context
- Easier to build rapport and read emotional cues
- Can observe the physical workspace and tools
- Fewer technical disruptions

**Remote advantages:**
- Access to geographically diverse participants
- Lower recruitment cost and faster scheduling
- Participants may feel more comfortable in their own environment
- Built-in recording with most video tools

**Remote-specific considerations:**
- Ask participants to share their screen when discussing workflows
- Use the chat for links or follow-up questions without interrupting
- Account for video fatigue: keep remote sessions 5-10 minutes shorter
- Have a backup plan for technical failures (phone number, alternate platform)
- Test your recording setup before the first session

**Hybrid approach:** When possible, conduct the first 2-3 interviews in person to build deep understanding, then switch to remote for the remaining interviews to increase sample diversity.

## Common Mistakes

**Asking "would you" instead of "tell me about a time when."** Hypothetical questions produce hypothetical answers. People are terrible at predicting their own behavior. Always ground questions in past behavior. Instead of "Would you pay for this feature?" ask "Tell me about the last time you paid for a software tool. What made you decide to buy it?"

**Talking more than the participant.** The interviewer should speak roughly 20-30% of the time. If you are talking more than that, you are lecturing, not interviewing. Use silence as a tool: after the participant finishes speaking, wait 3-5 seconds before asking the next question. They will often fill the silence with their most candid thoughts.

**Asking questions in a fixed order regardless of flow.** The script is a guide, not a screenplay. If the participant naturally brings up a topic from later in your script, follow that thread. You can always circle back to missed questions.

**Seeking validation instead of understanding.** If you designed the feature, you are biased. Catch yourself when you feel pleased that a participant "gets it." Research is not a pitch meeting.

**Accepting surface-level answers.** When a participant says "It's fine," probe deeper: "When you say fine, what do you mean? Walk me through what that experience is actually like." Surface answers hide the real insights.

**Not recording.** Memory is unreliable. Even with a dedicated note-taker, you will miss details. Always record (with consent) and reference recordings during synthesis.

**Interviewing only happy users.** Your most insightful participants are often those who struggled, churned, or chose a competitor. Actively recruit users who had negative experiences.

**Skipping the debrief.** Failing to debrief immediately after each interview means losing context that will be impossible to reconstruct later. The debrief is not optional.

## Post-Interview Synthesis

After completing all interviews (not after each one individually), synthesize the data into actionable insights.

**Step 1 -- Review all notes and recordings.** Re-read every set of interview notes. Listen to or re-watch key moments from recordings. Highlight notable quotes, surprising observations, and recurring themes.

**Step 2 -- Create atomic notes.** Write each distinct observation on its own note (physical sticky note or digital equivalent). One observation per note. Include the participant ID so you can trace it back.

**Step 3 -- Affinity mapping.** Spread all notes out and group them by similarity. Do not pre-define categories; let themes emerge from the data. See the [Synthesis Methods](synthesis-methods.md) reference for the full affinity mapping process.

**Step 4 -- Write insight statements.** For each theme cluster, write a structured insight: "We observed [pattern]. We were surprised that [unexpected finding]. Because of this, we might [design implication]."

**Step 5 -- Identify personas.** If behavioral clusters emerge naturally, they may indicate distinct personas. See the [Persona Templates](persona-templates.md) reference for building personas from interview data.

**Step 6 -- Share findings.** Present insights to the broader team using quotes, themes, and recommendations. Anchor every recommendation in specific evidence. Never present an opinion without the data that supports it.

## See Also

- [[persona-templates.md]] -- Build personas from the behavioral clusters that emerge during interview synthesis
- [[synthesis-methods.md]] -- Full affinity mapping, empathy mapping, and How Might We framing processes
- [[jtbd-framework.md]] -- Use the JTBD lens during interviews to uncover the jobs users are hiring your product to do
- [[journey-template.md]] -- Map the journeys described in interviews into visual journey maps

**Back to:** [User Research Skill](../SKILL.md)

## Competitive Audit Process (moved from SKILL.md)

1. **Identify competitors** — 4-6 direct (same problem, same audience) + 2-3 indirect (different solution, same JTBD).
2. **Define criteria** — 8-12 dimensions: onboarding, feature parity, pricing, IA, visual quality, a11y, mobile, performance, content, support, integrations, community.
3. **Document** — screenshots, recorded task flows, strengths/weaknesses per criterion, consistent 1-5 scoring.
4. **Gap analysis** — criteria where all competitors score ≤ 2 = market-wide opportunity.
5. **Opportunity map** — 2×2 matrix on the two most differentiating criteria. Identify underserved quadrants. Position intentionally.

## Best Practices

- Never assume — talk to users.
- Recruit real users via screener; not friends/family/coworkers.
- Combine qual (why) + quant (how many).
- Anchor every recommendation in a specific observation; quote users.
- Maintain a research repository (Confluence, Dovetail, Notion).
- Triangulate findings across methods.

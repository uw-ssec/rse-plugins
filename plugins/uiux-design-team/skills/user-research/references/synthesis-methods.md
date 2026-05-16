# Synthesis Methods

Structured approaches for transforming raw research data into actionable insights, design principles, and team alignment.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Affinity Mapping](#affinity-mapping) | 16-62 | Step-by-step process for clustering observations into themes |
| [Empathy Map Template](#empathy-map-template) | 64-105 | Four-quadrant template for capturing user perspective |
| [Insight Statements](#insight-statements) | 107-143 | Formula for converting themes into actionable insights |
| [How Might We Generation](#how-might-we-generation) | 145-185 | Transforming insights into design challenges |
| [Research Repository](#research-repository) | 187-218 | Organizational memory for long-term research value |
| [Presenting to Stakeholders](#presenting-to-stakeholders) | 220-255 | Communicating findings to non-research audiences |
| [See Also](#see-also) | 257-262 | Related references and skills |

## Affinity Mapping

Affinity mapping is the most widely used synthesis method. It transforms individual observations into thematic clusters that reveal patterns across participants.

**Step 1 -- Write individual notes.** Take every distinct observation from your research and write it on its own note. One observation per note. Include the participant ID (e.g., P3) on each note for traceability. Aim for 50-200 notes across all interviews.

Examples of good atomic notes:
- "P3: Spends 20 min each morning manually copying data between two tools"
- "P5: Did not realize the export feature existed until month 3"
- "P1: Felt embarrassed presenting incomplete data to leadership"

Examples of notes that are too broad (split them):
- "P2: Has many frustrations with the dashboard" (which frustrations specifically?)

**Step 2 -- Spread and scan.** Lay all notes out where they are visible (physical wall, Miro/FigJam board). Read through them without organizing. Let patterns begin to emerge naturally.

**Step 3 -- Group by similarity.** Begin moving notes that seem related near each other. Do not pre-define categories. Instead, let the data tell you what the groups are. Work silently if doing this as a team (silent sorting prevents groupthink).

**Step 4 -- Name the clusters.** Once groups stabilize, write a label for each cluster that captures the theme. A good label is a complete phrase, not a single word. "Users struggle to find features they need" is better than "Discoverability."

**Step 5 -- Merge and split.** Review each cluster:
- If a cluster has more than 15 notes, it may contain sub-themes. Split it.
- If two clusters overlap significantly, merge them.
- If a cluster has fewer than 3 notes, it may be an outlier. Keep it visible but do not over-index on it.

**Step 6 -- Prioritize.** Not all themes are equal. Rank clusters by:
- Frequency: How many participants mentioned this?
- Severity: How much does this issue affect the user's ability to achieve their goal?
- Opportunity: How much could the experience improve if this were addressed?

**Step 7 -- Generate insights.** For each top-priority cluster, write a structured insight statement (see below).

**Facilitation tips for team affinity mapping:**
- Silent sorting first (10-15 minutes), then discussion
- No one "owns" a note; anyone can move any note
- Disagreements about grouping are data points, not problems
- Time-box the exercise: 45-60 minutes for sorting, 15-20 minutes for labeling

## Empathy Map Template

An empathy map captures a persona's perspective across four dimensions. Create one per persona, populated with data from research, not assumptions.

```
+---------------------------------------+---------------------------------------+
|              SAYS                      |              THINKS                   |
|                                        |                                       |
| Direct quotes from interviews:         | Inferred beliefs and internal monologue:|
|                                        |                                       |
| - "I spend half my day in meetings     | - Worries the team sees her as a       |
|   that should have been Slack messages" |   bottleneck rather than an enabler   |
|                                        |                                       |
| - "I wish I could just see the data    | - Suspects the quarterly goals are     |
|   without having to build a dashboard" |   unrealistic but hesitant to say so  |
|                                        |                                       |
| - "Our process works, it's just slow"  | - Wonders if competitors' tools are    |
|                                        |   actually better or just marketed     |
|                                        |   better                               |
+---------------------------------------+---------------------------------------+
|              DOES                      |              FEELS                    |
|                                        |                                       |
| Observable actions and behaviors:      | Emotional states and motivations:      |
|                                        |                                       |
| - Checks Slack first thing every       | - Frustrated by context-switching      |
|   morning before opening any tool      |   between 5+ tools                     |
|                                        |                                       |
| - Manually exports CSV files and       | - Anxious before stakeholder           |
|   reformats in spreadsheets            |   presentations                        |
|                                        |                                       |
| - Keeps a personal Notion doc with     | - Satisfied when a shipped feature     |
|   workarounds for tool limitations     |   gets positive user feedback          |
+---------------------------------------+---------------------------------------+
```

**Rules for empathy maps:**
- SAYS should contain verbatim quotes or near-verbatim paraphrases
- THINKS should be inferences clearly supported by behavioral evidence
- DOES should describe observable, specific actions (not generalizations)
- FEELS should name specific emotions, not vague sentiments ("anxious about deadlines" not "stressed")

**When to use empathy maps:**
- After interviews, to consolidate understanding of each persona
- During design sprints, to re-ground the team in the user's perspective
- Before ideation sessions, to ensure solutions address real emotional needs

## Insight Statements

An insight statement distills a theme from affinity mapping into a concise, actionable format. It bridges research findings and design implications.

**The formula:**

> "We observed [specific pattern from research]. We were surprised that [unexpected element of the pattern]. Because of this, we might [design hypothesis or implication]."

**Example 1:**
> "We observed that 6 out of 8 users check their analytics dashboard first thing in the morning. We were surprised that none of them trust the numbers without cross-referencing a spreadsheet. Because of this, we might need to add data source indicators and last-updated timestamps to build trust in dashboard accuracy."

**Example 2:**
> "We observed that users create personal workaround documents for processes our product should support. We were surprised that they prefer their workarounds to our official features. Because of this, we might need to study their workarounds to understand what our features are missing."

**Example 3:**
> "We observed that new users abandon the settings page within 15 seconds. We were surprised that the notification preferences, despite being clearly labeled, are never found. Because of this, we might need to surface notification controls in the context where notifications actually appear."

**Quality checks for insight statements:**
- Is the observation grounded in data (participant count, quotes, metrics)?
- Is the surprise genuinely unexpected, or just a restatement of the observation?
- Does the implication suggest a direction without prescribing a specific solution?
- Could this insight change a design decision? If not, it is too vague.

## How Might We Generation

"How Might We" (HMW) questions transform insight statements into open-ended design challenges that invite creative solutions without prescribing them.

**The conversion process:**

1. Start with an insight statement
2. Identify the core tension or unmet need
3. Reframe it as an open question beginning with "How might we..."

**Rules for good HMW questions:**
- Broad enough to allow multiple solutions
- Narrow enough to be actionable (not "How might we make users happy?")
- Focused on the user's need, not the product's feature
- Free of embedded solutions (not "How might we add a tooltip?")

**Example conversion:**

Insight: "Users feel overwhelmed by the dashboard on first login because there are 12 widgets competing for attention."

Too broad: "How might we improve the dashboard?"
Too narrow: "How might we reduce the dashboard to 4 widgets?"
Embedded solution: "How might we add an onboarding tour to the dashboard?"

Well-formed HMW questions from this insight:
- "How might we make the first dashboard experience feel manageable and guided?"
- "How might we help new users find the one widget that matters most to them?"
- "How might we progressively reveal dashboard complexity as users gain experience?"

**Generating HMW questions in practice:**
- Generate 3-5 HMW questions per insight statement
- Do this as a team exercise: each person writes HMW questions silently for 5 minutes, then share and discuss
- Vote on the most promising HMW questions to carry into ideation
- Keep a running list of all HMW questions; some will become relevant later

**Using HMW questions:**
- As prompts for brainstorming sessions
- As evaluation criteria for design concepts ("Does this solution answer our HMW?")
- As acceptance criteria for sprint planning
- As a way to reframe disagreements ("We disagree on the solution, but do we agree on the HMW?")

## Research Repository

A research repository is the organizational memory for user research. Without one, insights are trapped in slide decks that no one revisits, and teams repeat studies that were already done.

**What to store:**
- Raw data: interview recordings, transcripts, survey responses
- Processed data: affinity maps, empathy maps, insight statements
- Artifacts: personas, journey maps, competitive audits
- Metadata: study date, participants, research questions, methods used

**Structure:**

```
research-repository/
  studies/
    2026-01-user-onboarding/
      study-plan.md
      screener.md
      interview-guide.md
      notes/
        participant-01.md
        participant-02.md
      synthesis/
        affinity-map.md
        insights.md
      artifacts/
        personas.md
        journey-map.md
    2026-02-checkout-flow/
      ...
  insights/
    insight-library.md        (all insights, tagged and searchable)
  personas/
    current-personas.md       (living document, updated regularly)
```

**Maintenance principles:**
- Tag all insights with themes, products, and personas so they are searchable
- Review the repository quarterly; archive outdated studies, promote evergreen insights
- Link new studies to prior related studies to build cumulative understanding
- Make the repository accessible to the entire product team, not just researchers

## Presenting to Stakeholders

Research findings only matter if they change decisions. Presenting to non-research stakeholders requires translating raw findings into their language.

**Structure your presentation:**

1. **Context** (1-2 minutes): What question did we investigate? Why does it matter?
2. **Method** (1 minute): How did we study it? How many participants? What criteria?
3. **Key findings** (5-10 minutes): 3-5 top insights with supporting evidence (quotes, metrics, screenshots)
4. **Implications** (3-5 minutes): What should we do differently based on these findings?
5. **Open questions** (1-2 minutes): What do we still not know? What should we study next?

**Presentation principles:**
- Lead with the most surprising or high-impact finding
- Use direct quotes from participants (with permission); they are more persuasive than researcher interpretations
- Show, don't tell: include screenshots, video clips (15-30 seconds), and journey map snippets
- Quantify when possible: "6 of 8 participants struggled" is more concrete than "many users had difficulty"
- End with clear, prioritized recommendations, not a vague call to action
- Anticipate "so what?" for every slide. If you cannot answer it, cut the slide.

**Common stakeholder objections and responses:**
- "8 people is not statistically significant." -- Correct. Qualitative research does not aim for statistical significance. It aims for thematic saturation, which typically occurs at 5-8 participants per segment.
- "Our power users don't have this problem." -- That may be true. This finding applies to [segment]. Let us discuss which segment is the priority.
- "We already knew this." -- If we knew it, why have we not addressed it? Let us use this as the evidence to prioritize the fix.

## See Also

- [[persona-templates.md]] -- Use synthesis outputs to build and validate personas
- [[interview-guide.md]] -- The interviews that produce the raw data for synthesis
- [[jtbd-framework.md]] -- Apply JTBD framing to insight statements and HMW questions
- [[journey-template.md]] -- Translate synthesized insights into visual journey maps

**Back to:** [User Research Skill](../SKILL.md)

## Affinity Mapping Detail (moved from SKILL.md)

Write each observation on a separate sticky/card. Group related notes into clusters. Name each cluster with a theme. Merge or split until themes feel distinct and meaningful.

## Empathy Map Quadrants

- **Says** — direct quotes from interviews
- **Thinks** — inferred beliefs and concerns
- **Does** — observable actions
- **Feels** — emotional states (frustrated, anxious, confident)

## Insight Statement Template

> "We observed [observation]. We were surprised that [surprise]. Because of this, we might [hypothesis]."

## How Might We Generation

Transform insights into design challenges. Generate 3-5 HMW per insight. Use to seed ideation.

- Insight: Users feel overwhelmed by dashboard on first login.
- HMW: How might we make the first dashboard experience feel manageable and guided?

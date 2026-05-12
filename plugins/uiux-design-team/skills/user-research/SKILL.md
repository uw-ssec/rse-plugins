---
name: user-research
description: Conduct user research including persona creation, interview scripts, Jobs-to-Be-Done analysis, competitive audits, survey design, affinity mapping, and research synthesis to ground design decisions in real user evidence.
metadata:
   references:
   - references/interview-guide.md
   - references/jtbd-framework.md
   - references/persona-templates.md
   - references/synthesis-methods.md
---

# User Research

User research is the foundation of human-centered design. Every design decision should trace back to evidence gathered from real users rather than assumptions, stakeholder opinions, or industry trends. This skill provides structured methods for understanding who your users are, what they need, and why they behave the way they do. Whether you are launching a new product or refining an existing one, rigorous user research reduces risk, eliminates guesswork, and delivers experiences that resonate.

## Quick Start: Create a User Persona

Follow these five steps to build an evidence-based persona. Spend at minimum 5-8 user interviews before creating a primary persona.

**Step 1 -- Gather raw data.** Collect interview transcripts, survey responses, analytics, and support tickets. Look for recurring behavioral patterns rather than demographic coincidences.

**Step 2 -- Identify behavioral clusters.** Group users who share goals, frustrations, and workflows. These clusters will each become a distinct persona.

**Step 3 -- Draft the persona profile.** For each cluster, fill in the following structure:

```
Name:           [Realistic first name + last initial]
Role:           [Job title or life role]
Demographics:   [Age range, location, tech comfort]
Goals:          [2-3 primary objectives]
Frustrations:   [2-3 recurring pain points]
Behaviors:      [Key habits, tool preferences, workflows]
JTBD:           [Primary job story in JTBD format]
Quote:          [Verbatim or composite quote from research]
```

**Step 4 -- Validate.** Share persona drafts with teammates who participated in interviews. Confirm the persona feels like a real person they spoke with rather than a fictional character.

**Step 5 -- Socialize.** Pin the persona somewhere visible: a Confluence page, a Figma board, or printed on the team wall. Reference it in every design review.

**Example output:**

```
Name:           Maria T.
Role:           Product Manager at a mid-stage B2B SaaS company
Demographics:   32-38, urban, high tech fluency
Goals:          Ship features faster without sacrificing quality;
                Align engineering and design on priorities;
                Prove ROI of product improvements to leadership
Frustrations:   Too many tools that don't integrate;
                Stakeholders change requirements mid-sprint;
                Difficulty synthesizing user feedback at scale
Behaviors:      Lives in Slack and Linear; runs weekly user calls;
                prefers async communication over meetings
JTBD:           When I am planning the next quarter's roadmap,
                I want to quantify which user problems matter most,
                so I can defend my prioritization to the executive team.
Quote:          "I have a gut feeling about what to build, but gut
                feelings don't survive a board meeting."
```

## Research Methods

Choose the right method based on your research question, timeline, and available resources.

| Method              | When to Use                                    | Time Required | Output                        |
|---------------------|------------------------------------------------|---------------|-------------------------------|
| User Interviews     | Deep understanding of motivations and context  | 1-2 weeks     | Transcripts, insight themes   |
| Contextual Inquiry  | Observe real workflows in natural environment   | 1-3 weeks     | Field notes, workflow maps    |
| Surveys             | Quantify attitudes across a large population    | 1-2 weeks     | Statistical distributions     |
| Card Sorting        | Understand mental models for information        | 3-5 days      | Category groupings, dendrograms|
| Usability Testing   | Evaluate an existing design or prototype        | 1-2 weeks     | Task success rates, issues    |
| Diary Studies       | Capture behavior over time in natural context   | 2-4 weeks     | Longitudinal behavior data    |
| A/B Testing         | Compare measurable outcomes of two variants     | 1-4 weeks     | Statistical significance data |
| Analytics Review    | Identify behavioral patterns at scale           | 1-3 days      | Funnels, drop-offs, segments  |

Combine qualitative methods (interviews, contextual inquiry) with quantitative methods (surveys, analytics) for a complete picture. Qualitative tells you *why*. Quantitative tells you *how many*.

## Jobs-to-Be-Done

Jobs-to-Be-Done (JTBD) reframes design around the progress a user is trying to make rather than the features they request. The core format is the **job story**:

> "When [situation], I want to [motivation], so I can [expected outcome]."

There are three types of jobs:

**Functional jobs** -- The practical task the user needs to accomplish.
Example: "When I receive a customer support ticket, I want to see the customer's history at a glance, so I can resolve their issue without asking them to repeat themselves."

**Emotional jobs** -- How the user wants to feel (or avoid feeling) during the experience.
Example: "When I present analytics to my team, I want to feel confident in the accuracy, so I can avoid the embarrassment of sharing wrong numbers."

**Social jobs** -- How the user wants to be perceived by others.
Example: "When I share a design with stakeholders, I want it to look polished, so I can be seen as a competent and detail-oriented professional."

Design for all three job types. A product that nails the functional job but ignores the emotional job will feel cold and transactional.

## Competitive Audit

A competitive audit reveals market gaps and establishes a baseline for differentiation.

**Step 1 -- Identify competitors.** List 4-6 direct competitors (same problem, same audience) and 2-3 indirect competitors (different solution, same underlying job).

**Step 2 -- Define evaluation criteria.** Select 8-12 dimensions: onboarding flow, feature parity, pricing model, information architecture, visual design quality, accessibility, mobile experience, performance, content strategy, support channels, integrations, and community.

**Step 3 -- Document findings.** For each competitor, capture screenshots, record task flows, and note strengths and weaknesses per criterion. Use a consistent scoring scale (1-5 or Poor/Fair/Good/Excellent).

**Step 4 -- Gap analysis.** Identify criteria where all competitors score poorly. These are market-wide gaps where innovation is possible.

**Step 5 -- Opportunity map.** Plot competitors on a 2x2 matrix using the two most differentiating criteria. Identify underserved quadrants and position your product intentionally.

## Research Synthesis

Raw data becomes actionable only after synthesis. Follow this sequence to move from observations to design implications.

**Affinity mapping.** Write each observation on a separate sticky note or card. Group related notes into clusters. Name each cluster with a theme label. Merge or split clusters until themes feel distinct and meaningful.

**Empathy maps.** For each persona, populate four quadrants:
- **Says** -- Direct quotes from interviews
- **Thinks** -- Inferred beliefs and concerns
- **Does** -- Observable actions and behaviors
- **Feels** -- Emotional states (frustrated, anxious, confident)

**Insight statements.** Convert themes into structured insights using this formula:

> "We observed [observation]. We were surprised that [surprise]. Because of this, we might [hypothesis]."

Example: "We observed that users abandon the settings page within 15 seconds. We were surprised that they cannot find the notification preferences despite a clear label. Because of this, we might need to surface notification controls in the context where notifications appear."

**How Might We (HMW) framing.** Transform insights into design challenges:
- Insight: Users feel overwhelmed by the dashboard on first login.
- HMW: How might we make the first dashboard experience feel manageable and guided?

Generate 3-5 HMW questions per insight. Use them to seed ideation sessions.

## Best Practices

- **Never assume.** Validate every hypothesis with evidence. If you catch yourself saying "users probably want..." stop and go talk to them.
- **Recruit real users.** Friends, family, and coworkers are not representative. Use screener surveys to find participants who match your target persona.
- **Combine qualitative and quantitative.** Interviews explain *why*. Analytics and surveys quantify *how much*. Neither alone is sufficient.
- **Present findings, not opinions.** When sharing research, anchor every recommendation in a specific observation. Quote users directly. Show the data.
- **Maintain a research repository.** Store all transcripts, recordings, insights, and personas in a shared location. Research has a long shelf life when it is findable.
- **Triangulate.** Look for the same finding across multiple methods. A pain point mentioned in interviews, visible in analytics, and confirmed by support tickets is a high-confidence finding.

## Deep Dive References

### [Persona Templates](references/persona-templates.md)

- Full Persona Template
- Identity
- Demographics
- Goals (prioritized)
- Frustrations (prioritized)
- Behaviors
- Jobs to Be Done
- Scenarios
- *...and 14 more sections*

### [Interview Guide](references/interview-guide.md)

- Interview Planning
- Script Structure
- Question Types
- Note-Taking Template
- Metadata
- Context
- Key Observations
- Emotional Moments
- *...and 5 more sections*

### [Synthesis Methods](references/synthesis-methods.md)

- Affinity Mapping
- Empathy Map Template
- Insight Statements
- How Might We Generation
- Research Repository
- Presenting to Stakeholders

### [JTBD Framework](references/jtbd-framework.md)

- Origins and Core Theory
- Job Types
- Job Story Format
- Switch Interviews
- Forces Diagram
- Outcome-Driven Innovation
- JTBD vs. User Stories

## Next Steps

After completing user research, apply your findings with these related skills:

- **user-journey-mapping** -- Map the end-to-end experience your personas go through, identifying pain points and opportunities at each stage.
- **usability-evaluation** -- Evaluate existing designs against heuristics and walkthrough protocols informed by your research insights.

# Jobs-to-Be-Done Framework

A comprehensive guide to the Jobs-to-Be-Done theory, covering origins, job types, story formats, switch interviews, forces diagrams, outcome-driven innovation, and comparison with user stories.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Origins and Core Theory](#origins-and-core-theory) | 16-39 | Christensen and Ulwick's foundational JTBD concepts |
| [Job Types](#job-types) | 41-83 | Functional, emotional, and social jobs with examples |
| [Job Story Format](#job-story-format) | 85-136 | Template and 5 detailed examples across product categories |
| [Switch Interviews](#switch-interviews) | 138-175 | Uncovering what made someone adopt a new solution |
| [Forces Diagram](#forces-diagram) | 177-217 | The four forces that drive or resist behavior change |
| [Outcome-Driven Innovation](#outcome-driven-innovation) | 219-252 | Ulwick's framework for measuring job satisfaction |
| [JTBD vs. User Stories](#jtbd-vs-user-stories) | 254-290 | Comparison table and when to use each |
| [See Also](#see-also) | 292-298 | Related references and skills |

## Origins and Core Theory

Jobs-to-Be-Done theory originated from the work of Clayton Christensen (Harvard Business School) and Anthony Ulwick (Strategyn). The central premise: people do not buy products. They hire products to make progress in their lives.

Christensen's famous milkshake example illustrates the theory. A fast-food chain wanted to sell more milkshakes. Traditional market research segmented customers by demographics and asked what would make the milkshake better (thicker, more chocolate, cheaper). Sales did not improve. JTBD research asked a different question: "What job are you hiring the milkshake to do?" The answer: morning commuters hired the milkshake for a boring commute. The job was "give me something interesting and filling to consume during a 30-minute drive." The competition was not other milkshakes but bananas, bagels, and boredom.

**Core principles of JTBD:**
- **Jobs are stable.** Technologies, products, and solutions change. The underlying jobs rarely do. People have been hiring solutions for "communicate with distant people" for centuries, from letters to telegraph to phone to video calls.
- **Jobs are solution-agnostic.** The job exists independently of your product. Understanding the job means understanding what the user would do if your product did not exist.
- **Products are hired and fired.** Users adopt a product when it does the job better than alternatives. They abandon it when something better comes along or when it stops doing the job.
- **Context matters.** The same person may have different jobs in different situations. The job is defined by the situation, not the person.

## Job Types

JTBD distinguishes three types of jobs. Successful products address all three; mediocre products address only the functional job.

**Functional Jobs** -- The practical, task-oriented outcome the user needs to achieve. These are the most visible and the easiest to design for.

- "Help me track my team's progress across multiple projects without manually updating spreadsheets."
- "Help me find a restaurant that meets my dietary restrictions and is within a 15-minute walk."
- "Help me deploy a code change to production without downtime."

Functional jobs are necessary but not sufficient. A product that completes the functional job in an unpleasant way will be replaced by one that also addresses the emotional job.

**Emotional Jobs** -- How the user wants to feel (or avoid feeling) during and after the experience. These are often unspoken and discovered through careful observation rather than direct questions.

- "I want to feel in control of my project's direction, not surprised by problems I didn't see coming."
- "I want to feel confident presenting my work, not anxious that someone will find an error."
- "I want to feel like an expert when using this tool, not like I need to read documentation for every task."

Design implications of emotional jobs: reduce anxiety through transparency, build confidence through progressive disclosure, create a sense of mastery through intelligent defaults and smart suggestions.

**Social Jobs** -- How the user wants to be perceived by others. Social jobs influence tool selection, workflow choices, and willingness to recommend products.

- "I want my team to see me as organized and strategic, not as someone who is constantly scrambling."
- "I want my manager to see that I made this decision based on data, not intuition."
- "I want to be recognized as someone who uses modern, professional-grade tools."

Design implications of social jobs: make outputs shareable and presentation-ready, provide data exports that look good in stakeholder meetings, enable users to demonstrate their expertise.

## Job Story Format

The job story format replaces traditional user stories with a situation-driven structure that emphasizes context and motivation over role and feature.

**Template:**

> "When [specific situation or trigger], I want to [motivation or action], so I can [expected outcome or progress]."

**Detailed examples:**

**Example 1 -- Project Management Tool:**
> "When I am preparing for the Monday team standup and realize I don't know which tasks are blocked, I want to see a single view of all blocked items with the reason for each block, so I can address blockers proactively instead of discovering them during the meeting."

Functional job: Surface blocked tasks quickly.
Emotional job: Feel prepared and in control before the meeting.
Social job: Be perceived as a proactive leader who unblocks the team.

**Example 2 -- E-Commerce Platform:**
> "When I am buying a gift for a friend whose preferences I don't know well, I want to see curated gift suggestions organized by personality type and price range, so I can choose something thoughtful without spending hours browsing."

Functional job: Find an appropriate gift efficiently.
Emotional job: Feel confident the gift will be appreciated.
Social job: Be seen as someone who gives thoughtful, personal gifts.

**Example 3 -- Analytics Dashboard:**
> "When my CEO asks me 'How did last month's campaign perform?' in a hallway conversation, I want to pull up a clear summary on my phone within 10 seconds, so I can give an accurate answer without saying 'Let me get back to you.'"

Functional job: Access key metrics instantly.
Emotional job: Feel confident and credible in the moment.
Social job: Be perceived as someone who knows their numbers.

**Example 4 -- Design Collaboration Tool:**
> "When a developer asks me why I chose a specific spacing value, I want to show them the design token and its rationale in context, so I can maintain design consistency without repeating the same explanation every sprint."

Functional job: Communicate design decisions efficiently.
Emotional job: Avoid the frustration of repetitive justification.
Social job: Be respected as someone whose decisions are well-reasoned.

**Example 5 -- Customer Support Platform:**
> "When a customer calls back about an issue they reported last week and I have no context, I want to see the complete interaction history before I pick up the call, so I can continue the conversation without making the customer repeat their story."

Functional job: Access customer context before the interaction.
Emotional job: Feel competent and prepared during the call.
Social job: Be perceived by the customer as someone who cares about their experience.

## Switch Interviews

Switch interviews are a specialized JTBD interview technique that explores the moment a user decided to adopt a new solution. They reveal the forces that drove the switch and the barriers that almost prevented it.

**The timeline of switching:**

1. **First thought** -- When did you first think the old solution was not enough? What happened?
2. **Passive looking** -- Did you start noticing alternatives without actively searching? What caught your attention?
3. **Active looking** -- When did you start evaluating options? What triggered the shift from passive to active?
4. **Decision** -- What made you choose the new solution over alternatives? What was the final push?
5. **Consumption** -- When did you first use the new solution? What was that experience like?
6. **Satisfaction** -- Looking back, did the new solution do the job you hired it for?

**Interview questions for each phase:**

- "Take me back to the moment you first realized [old solution] wasn't working. What was happening?"
- "Before you searched for an alternative, did you notice any other options? Where?"
- "What made you start actively looking for something new? Was there a specific event?"
- "When you were comparing options, what were the top 2-3 things you looked for?"
- "Was there a moment where you almost didn't switch? What held you back?"
- "What was the first thing you did when you started using [new solution]?"
- "Now that you've been using it for [time], does it do what you expected?"

**What switch interviews reveal:**
- The real competitive alternatives (often surprising; the competition is not always who you think)
- The tipping point that turned passive dissatisfaction into active search
- The specific criteria that matter most during evaluation
- The anxieties and habits that almost prevented the switch
- Whether your product is being hired for the job you intended

## Forces Diagram

The forces diagram visualizes the four competing forces that determine whether a user will switch from their current solution to a new one. Two forces push toward change; two resist it.

```
                    PUSH OF CURRENT SITUATION
                    "My current tool doesn't do X"
                              |
                              v
    +----------------------------------------------------+
    |                                                    |
    |               SWITCHING BEHAVIOR                   |
    |               (adopting new solution)               |
    |                                                    |
    +----------------------------------------------------+
                              ^
                              |
                    PULL OF NEW SOLUTION
                    "The new tool promises to do X better"


              vs.


                    ANXIETY OF NEW SOLUTION
                    "What if the new tool has its own problems?"
                              |
                              v
    +----------------------------------------------------+
    |                                                    |
    |               STAYING BEHAVIOR                     |
    |               (keeping current solution)            |
    |                                                    |
    +----------------------------------------------------+
                              ^
                              |
                    HABIT OF CURRENT SOLUTION
                    "I already know how to use this, and my data is here"
```

**The four forces:**

1. **Push of the current situation** -- Dissatisfaction, frustration, or limitations of the current solution. "I can't do X." "It takes too long." "I keep making mistakes."

2. **Pull of the new solution** -- The appeal and promise of the alternative. "It looks easier." "My colleague recommended it." "The demo was impressive."

3. **Anxiety of the new solution** -- Fear, uncertainty, and risk associated with switching. "What if I lose my data?" "What if my team won't adopt it?" "What if it's actually harder?"

4. **Habit of the current solution** -- Inertia, familiarity, and switching costs. "I already know how to use this." "All my workflows are built around it." "It's good enough."

**Design implications:**
- Increase the pull: make the value proposition immediately tangible (free trial, demo, social proof)
- Reduce anxiety: offer data import, migration guides, money-back guarantees, gradual onboarding
- Acknowledge habits: provide familiar UI patterns, keyboard shortcuts from competing tools, compatibility modes
- You cannot control the push (you don't control competitors' failures), but you can make the pull and anxiety-reduction so strong that moderate push is sufficient

## Outcome-Driven Innovation

Anthony Ulwick's Outcome-Driven Innovation (ODI) framework extends JTBD with a quantitative method for measuring how well users' needs are being met.

**Core concept:** For every job, there are 50-150 desired outcomes that describe how the user measures success. Each outcome follows the format:

> "Minimize the [time/effort/likelihood] of [undesired outcome]."

Or:

> "Maximize the [likelihood/accuracy/completeness] of [desired outcome]."

**Examples for the job "Plan a team offsite":**
- Minimize the time it takes to find a venue that meets all requirements
- Minimize the likelihood of booking a venue that is too small for the group
- Maximize the likelihood that the agenda accommodates different working styles
- Minimize the effort required to coordinate travel for remote team members

**The opportunity algorithm:**
For each outcome, survey users on two dimensions (1-10 scale):
- **Importance:** How important is this outcome to you?
- **Satisfaction:** How satisfied are you with current solutions?

```
Opportunity Score = Importance + max(Importance - Satisfaction, 0)
```

High opportunity scores (high importance, low satisfaction) indicate underserved needs ripe for innovation. Low opportunity scores (low importance, or high satisfaction) indicate areas where current solutions are adequate.

**Using ODI results in design:**
- Prioritize features that address the highest-opportunity outcomes
- Avoid investing in outcomes that are already well-served (even if they are important)
- Segment users by their opportunity profiles to identify distinct market positions

## JTBD vs. User Stories

JTBD and user stories are complementary but serve different purposes. Understanding when to use each prevents confusion.

| Dimension | JTBD (Job Story) | User Story |
|-----------|-------------------|------------|
| **Format** | "When [situation], I want to [motivation], so I can [outcome]" | "As a [role], I want to [action], so that [benefit]" |
| **Focus** | The situation that triggers the need | The role of the person |
| **Scope** | Broad, solution-agnostic | Narrow, feature-specific |
| **When to use** | Strategy, research, product vision | Sprint planning, development tickets |
| **Audience** | Product managers, designers, researchers | Developers, QA, scrum teams |
| **Stability** | Long-lived (jobs rarely change) | Short-lived (completed per sprint) |
| **Abstraction** | High (does not prescribe a solution) | Low (describes a specific interaction) |
| **Origin** | Emerges from research and interviews | Derived from JTBD, requirements, or stakeholder requests |
| **Competition** | Other ways to get the job done (including non-digital) | Other features competing for sprint capacity |

**Relationship between the two:**

One JTBD can generate many user stories. The JTBD "When I am preparing for the Monday standup and need to see blocked tasks" might yield:
- "As a team lead, I want to filter the board by 'Blocked' status, so that I see only blocked items."
- "As a team lead, I want to see the reason for each block, so that I can address it."
- "As a team lead, I want to receive a Slack notification when a task is blocked, so that I don't have to check the board manually."

**Use JTBD when:**
- Defining product strategy and vision
- Conducting user research and interviews
- Evaluating competitive alternatives
- Deciding what to build (not how to build it)

**Use user stories when:**
- Writing development tickets for a sprint
- Breaking a JTBD into implementable pieces
- Defining acceptance criteria for a feature
- Communicating requirements to engineering

## See Also

- [[persona-templates.md]] -- Integrate JTBD into persona profiles for richer, behavior-driven archetypes
- [[interview-guide.md]] -- Use JTBD interview techniques (switch interviews, timeline) during user research
- [[synthesis-methods.md]] -- Apply JTBD framing when generating insight statements and HMW questions
- [[journey-template.md]] -- Map jobs to specific stages in the user journey

**Back to:** [User Research Skill](../SKILL.md)

## Job Types (moved from SKILL.md)

**Functional** — practical task.
Example: "When I receive a support ticket, I want to see customer history at a glance, so I can resolve without asking them to repeat themselves."

**Emotional** — how the user wants to feel.
Example: "When I present analytics to my team, I want to feel confident in the accuracy, so I can avoid the embarrassment of wrong numbers."

**Social** — how the user wants to be perceived.
Example: "When I share a design with stakeholders, I want it to look polished, so I can be seen as competent and detail-oriented."

Design for all three. A product that nails the functional but ignores the emotional feels cold and transactional.

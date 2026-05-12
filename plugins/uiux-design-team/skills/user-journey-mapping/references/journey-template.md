[Back to User Journey Mapping](../user-journey-mapping.md)

# Journey Map Template and Creation Process

## Overview

A journey map is a visualization of the process a person goes through to accomplish a goal. It documents the user's actions, thoughts, emotions, touchpoints, and pain points across a series of phases. Journey maps create shared understanding across teams, build empathy for the user, and surface actionable opportunities for improvement.

---

## Template Components

A complete journey map includes the following elements:

### Persona

The specific user whose journey is being mapped. Every journey map should be grounded in a real or research-based persona.

```markdown
**Persona:** Sarah Chen, 34
**Role:** Marketing Manager at a mid-size SaaS company
**Goal:** Evaluate and purchase a project management tool for her team of 12
**Tech comfort:** High (uses 10+ SaaS tools daily)
**Key frustration:** Has been burned by tools that promised integrations but delivered poorly
```

### Scenario

The specific situation and goal that defines the scope of the journey.

```markdown
**Scenario:** Sarah's team has outgrown their current spreadsheet-based
project tracking. She needs to evaluate options, get buy-in from her
director, and onboard her team within 30 days.
```

### Phases

The high-level stages of the journey, typically 4-7 phases representing distinct shifts in the user's activity or mindset.

```
| Awareness | Research | Evaluation | Decision | Onboarding | Adoption |
```

**Common phase patterns:**
- **Purchase journey:** Awareness > Consideration > Evaluation > Purchase > Post-Purchase
- **Onboarding journey:** Discovery > Signup > Setup > First Value > Habit Formation
- **Support journey:** Problem Recognition > Search for Help > Contact Support > Resolution > Follow-Up

### Actions

What the user does at each phase. These are observable, concrete behaviors.

```
Phase: Research
Actions:
- Google searches for "best project management tools 2025"
- Reads 3 comparison articles
- Visits 5 tool websites
- Watches 2 product demo videos
- Asks colleagues for recommendations on Slack
```

### Thoughts

What the user is thinking at each phase. Derived from user interviews, surveys, or empathy mapping.

```
Phase: Research
Thoughts:
- "There are so many options. How do I narrow this down?"
- "I need something that works with our existing tools, not another silo."
- "Will my team actually use this, or will they resist the change?"
```

### Emotions

The user's emotional state at each phase, typically represented on a positive-to-negative scale or with descriptive labels.

```
Phase: Research
Emotion: Overwhelmed (slightly negative)
- Excited about finding a solution but anxious about making the wrong choice
```

### Touchpoints

The specific channels, interfaces, or interactions where the user engages with the organization.

```
Phase: Research
Touchpoints:
- Google search results (organic listing)
- Company blog (comparison article)
- Product website (features page, pricing page)
- YouTube (product demo video)
- G2/Capterra (third-party review sites)
```

### Pain Points

Specific frustrations, obstacles, or negative experiences at each phase.

```
Phase: Evaluation
Pain Points:
- Free trial requires a credit card (barrier to trying)
- Feature comparison page does not include the competitor's specific features
- Demo scheduling requires a 3-day wait
- Trial environment is empty; hard to imagine real usage
```

### Opportunities

Ideas for improving the experience at each phase. These are the actionable outputs of the journey map.

```
Phase: Evaluation
Opportunities:
- Offer a no-credit-card free trial
- Pre-populate trial with sample data matching the user's industry
- Provide instant self-service demo alongside scheduled live demos
- Add a competitive comparison tool on the pricing page
```

---

## Emotional Curve Mapping

### What It Is

A visual line chart overlaid on the journey phases, showing the rise and fall of the user's emotional state throughout the experience. The emotional curve is often the most powerful communication element of a journey map.

### How to Create It

1. For each phase, rate the overall emotional valence on a scale of -3 to +3
2. Plot the ratings on a line chart across the horizontal phase axis
3. Label the peaks and valleys with the specific emotion and cause

```
Emotion
  +3  |                                          *
  +2  |         *                               / \
  +1  |        / \                             /   \
   0  |-------/---\-----------*---------------/-----\--------
  -1  |      /     \         / \             /       \
  -2  |     /       \       /   \           /         \
  -3  |    *         \     /     *         *
      |_____________________________________________
       Awareness  Research  Eval  Decision  Onboard  Adopt

      Peak: Decision (+3) "We picked the right tool!"
      Valley: Evaluation (-3) "This trial is useless with no data."
      Valley: Onboarding (-3) "Half my team can't figure out permissions."
```

### Identifying Critical Moments

- **Peaks:** Moments of delight; protect and amplify these
- **Valleys:** Moments of frustration; prioritize these for improvement
- **Steep drops:** Sudden negative shifts indicate broken expectations
- **Recovery slopes:** How quickly the user recovers from a valley indicates resilience of the relationship

---

## Journey Map Formats

### Current State Journey Map

Documents the existing experience as it happens today. This is the most common format and the foundation for improvement efforts.

**When to use:**
- Understanding the baseline experience
- Identifying pain points and opportunities
- Building empathy across teams
- Prioritizing UX improvements

**Data sources:** User interviews, surveys, analytics, support tickets, session recordings, field studies.

### Future State Journey Map

Visualizes the desired experience after improvements have been implemented. It is aspirational and design-driven.

**When to use:**
- Setting a vision for a redesign or new product
- Aligning stakeholders on the target experience
- Guiding design and development priorities
- Measuring progress toward the ideal

**Process:**
1. Start with the current state map
2. For each pain point, define the improved experience
3. For each opportunity, design the ideal interaction
4. Map the new emotional curve showing the expected improvement
5. Identify the gaps between current and future state

**Side-by-side gap analysis:**

| Stage | Current State | Future State | Change Required |
|-------|--------------|-------------|-----------------|
| Cart | Shipping cost revealed at checkout. Emotion: 2/5 | Shipping estimate on product page. Emotion target: 4/5 | Add shipping calculator to PDP |
| Payment | No trust badges. Emotion: 2/5 | Unified payment form with Apple Pay. Emotion target: 4/5 | Redesign payment UX |

### Day-in-the-Life Journey Map

Maps a user's entire day (or a significant portion), showing how a product fits into their broader life context. Not limited to interactions with your product.

**When to use:**
- Understanding the broader context of use
- Identifying moments when your product could add value
- Discovering unmet needs outside your current product scope
- Innovation and new product exploration

**Example phases:** Morning routine > Commute > Work morning > Lunch > Work afternoon > Commute > Evening

**Key insight:** Shows when and where your product competes for attention with other activities and tools.

---

## Journey Map Creation Process

### Step 1: Define Scope and Objectives

- Which persona are you mapping?
- What scenario and goal?
- What is the start and end point of the journey?
- What decisions will this map inform?

### Step 2: Gather Research Data

| Data Type | Source | What It Reveals |
|-----------|--------|-----------------|
| Qualitative interviews | 8-15 user interviews | Actions, thoughts, emotions, pain points |
| Survey data | 100+ responses | Quantitative validation of pain points |
| Analytics | Web/app analytics | Actual behavior, drop-off points, time spent |
| Support tickets | Support system | Common problems and frustrations |
| Session recordings | Hotjar, FullStory | Moment-by-moment behavior and confusion |
| Sales conversations | CRM notes | Decision factors, objections, competitor mentions |

### Step 3: Identify Phases

Review research data to identify natural transition points where the user's activity or mindset shifts. Name each phase with a gerund or noun that captures the activity (e.g., "Researching" or "Research").

### Step 4: Populate Each Lane

Working phase by phase, fill in:
1. Actions (from analytics and observation)
2. Thoughts (from interviews and surveys)
3. Emotions (from interviews and empathy mapping)
4. Touchpoints (from analytics and interviews)
5. Pain points (from all sources)
6. Opportunities (from team brainstorming)

### Step 5: Plot the Emotional Curve

Using the emotion data from each phase, create the emotional curve visualization. Validate with team members and, if possible, with users.

### Step 6: Identify Moments of Truth

Mark 2-3 critical moments that disproportionately influence the overall experience:
- **First impression:** The user's initial encounter with the product
- **Peak moment:** The most intensely positive or negative experience
- **End moment:** The user's last impression (recency effect)

### Step 7: Generate and Prioritize Opportunities

For each pain point, brainstorm improvement ideas. Prioritize using:
- Impact on the emotional curve (how much does this improve the experience?)
- Feasibility (can we implement this with current resources?)
- Reach (how many users are affected?)
- Strategic alignment (does this support business goals?)

---

## Stakeholder Presentation Tips

### Telling the Story

A journey map is most effective when presented as a narrative, not a chart.

**Structure for a 15-minute presentation:**

1. **Introduce the persona** (1 minute): Make the audience care about this person
2. **Set the scenario** (1 minute): What are they trying to accomplish and why?
3. **Walk through the journey** (8 minutes): Tell the story phase by phase, highlighting emotional peaks and valleys
4. **Call out the key pain points** (3 minutes): Focus on the 3 most impactful moments
5. **Present opportunities** (2 minutes): Show the prioritized improvement ideas

### Visual Design Tips

- Use a landscape/horizontal layout (journey maps are read left-to-right)
- Keep the emotional curve visually prominent
- Use icons and illustrations to make the map engaging
- Color-code pain points (red) and opportunities (green)
- Include real user quotes at key moments for emotional impact
- Keep text concise; the map should be scannable in 2 minutes

### Common Presentation Mistakes

- **Too much detail:** Overwhelming the audience with every data point
- **No narrative:** Presenting the map as a chart instead of a story
- **Missing the "so what":** Failing to connect pain points to actionable next steps
- **Wrong audience granularity:** Executives need the high-level story; designers need the detailed breakdown

---

## Journey Map Canvas

A one-page template for quick journey mapping, suitable for workshops and rapid alignment.

```markdown
# Journey Map Canvas

## Persona: _______________________________________________
## Scenario: ______________________________________________
## Goal: _________________________________________________

|              | Phase 1:     | Phase 2:     | Phase 3:     | Phase 4:     | Phase 5:     |
|              | _________    | _________    | _________    | _________    | _________    |
|--------------|-------------|-------------|-------------|-------------|-------------|
| **Actions**  |             |             |             |             |             |
| (What they   |             |             |             |             |             |
| do)          |             |             |             |             |             |
|--------------|-------------|-------------|-------------|-------------|-------------|
| **Thoughts** |             |             |             |             |             |
| (What they   |             |             |             |             |             |
| think)       |             |             |             |             |             |
|--------------|-------------|-------------|-------------|-------------|-------------|
| **Emotions** |             |             |             |             |             |
| (How they    |  +/- scale  |  +/- scale  |  +/- scale  |  +/- scale  |  +/- scale  |
| feel)        |             |             |             |             |             |
|--------------|-------------|-------------|-------------|-------------|-------------|
| **Touch-     |             |             |             |             |             |
| points**     |             |             |             |             |             |
|--------------|-------------|-------------|-------------|-------------|-------------|
| **Pain       |             |             |             |             |             |
| Points**     |             |             |             |             |             |
|--------------|-------------|-------------|-------------|-------------|-------------|
| **Opportu-   |             |             |             |             |             |
| nities**     |             |             |             |             |             |
|--------------|-------------|-------------|-------------|-------------|-------------|

## Key Moments of Truth:
1. ___________________________________________________________
2. ___________________________________________________________
3. ___________________________________________________________

## Top 3 Opportunities:
1. ___________________________________________________________
2. ___________________________________________________________
3. ___________________________________________________________

## Next Steps:
- [ ] ________________________________________________________
- [ ] ________________________________________________________
- [ ] ________________________________________________________
```

---

## Workshop Facilitation Guide

### Workshop Setup

**Duration:** 2-3 hours for a current-state map, 3-4 hours if including future-state.

**Participants:** 5-8 people from cross-functional roles (design, product, engineering, customer support, marketing). Fewer than 5 limits perspectives. More than 8 becomes unwieldy.

**Materials:**
- Printed research summaries (interview highlights, key analytics, support ticket themes)
- Large whiteboard or wall space with a pre-drawn template grid
- Sticky notes in 4 colors (one per row category)
- Dot stickers for voting on priorities

### Workshop Flow

**Phase 1: Align on scope (15 min)**
- Present the persona and scenario
- Review available research data
- Agree on the journey stages (5-7 stages)

**Phase 2: Map independently (20 min)**
- Each participant writes sticky notes for Actions, Thoughts, Pain Points, and Opportunities for each stage
- One idea per sticky note
- No discussion during this phase (prevents groupthink)

**Phase 3: Share and cluster (30 min)**
- Each participant places their sticky notes on the wall template
- Group similar notes together
- Discuss disagreements and clarify observations

**Phase 4: Draw the emotion curve (15 min)**
- Collectively rate each stage's emotion score
- Plot the curve and identify the valleys

**Phase 5: Prioritize opportunities (30 min)**
- Dot-vote on the most impactful opportunities (each participant gets 5 dots)
- Rank by total votes
- Assign owners and next steps

**Phase 6: Document (after workshop)**
- One person transfers the wall artifact into the digital template
- Share with all participants and stakeholders within 24 hours

### Facilitator Tips

- Keep the group grounded in research. When someone says "I think users feel..." redirect to "What did we observe in the interviews?"
- Use a parking lot for tangential discussions that are valuable but off-topic
- Ensure quieter participants have space to contribute (the independent writing phase helps)
- Time-box each phase strictly -- journey mapping workshops tend to expand beyond their allotted time

---

## Common Mistakes

### Mapping Without Research

A journey map built on assumptions is fiction. It feels productive but can actively mislead. Always base journey maps on user research data -- interviews, usability tests, analytics, or support tickets. If you lack data for a stage, flag it as an assumption and plan research to fill the gap.

### Scope Too Broad

A journey map that covers "the entire user experience from first awareness to churn" is too broad to be actionable. Focus on a single scenario with a clear beginning and end. Create multiple maps for multiple scenarios rather than one map that covers everything.

### Missing the Emotion Curve

A journey map without emotions is a process diagram. The emotion curve is the most valuable element because it reveals where the experience breaks down and where it delights. Without it, the map communicates what happens but not how it feels.

### Treating the Map as Permanent

Journey maps are snapshots of a specific moment. As you ship improvements, the journey changes. Revisit and update maps quarterly or after major releases.

### Not Sharing with Stakeholders

A journey map that lives in the design team's files has minimal impact. Share it visually in team spaces, reference it in sprint planning, and use it to justify prioritization decisions. The map's value comes from alignment, not from the artifact itself.

### Designing for the Happy Path Only

The most valuable journey maps include error states, edge cases, and recovery paths. What happens when the payment fails? When the delivery is late? When the user enters the wrong address? These unhappy paths often reveal the most critical opportunities.

---

## Validation and Iteration

### Validating the Journey Map

- **With users:** Present the map to 3-5 users and ask "Does this reflect your experience?"
- **With data:** Cross-reference against analytics to confirm behavioral claims
- **With frontline teams:** Sales and support staff can validate or challenge emotional assessments
- **With stakeholders:** Ensure the map aligns with organizational understanding and priorities

### Keeping the Map Alive

- Review and update quarterly or after major product changes
- Track improvements against identified pain points
- Measure emotional curve changes after implementing opportunities
- Create version numbers and change logs
- Store in an accessible, shared location (not buried in a slide deck)

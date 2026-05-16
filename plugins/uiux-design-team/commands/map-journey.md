---
name: map-journey
description: User journey mapping workflow that documents stages, touchpoints, actions, thoughts, feelings, pain points, and opportunities with an emotion curve visualization.
user-invocable: true
allowed-tools: []
---

# User Journey Mapping

Map the complete user journey through a product or service experience, led by @ux-researcher and @interaction-designer. This command produces a structured journey map that documents every stage, touchpoint, user action, thought, feeling, pain point, and opportunity.

## When to Use This Command

- Understanding the end-to-end user experience for a product or feature
- Identifying pain points and drop-off moments in an existing flow
- Aligning the team on the current state before redesigning
- Mapping a future-state ideal experience
- Communicating user experience findings to stakeholders

## Workflow

### Step 1: Define Journey Scope

@ux-researcher establishes the boundaries of the journey map.

**Gather from the user:**
- Which persona is taking this journey? (Use output from `/create-persona` if available)
- What is the journey type?
  - **Current state**: How users experience the product today
  - **Future state**: The ideal experience you are designing toward
  - **Day-in-the-life**: A broad view of the user's context beyond your product
- What is the starting trigger? (What event or need initiates the journey?)
- What is the end state? (What does completion or success look like?)
- How granular should the map be? (High-level overview vs. detailed task-level)

**Set the frame:**
- Time horizon: Minutes, hours, days, or weeks
- Channels: Web, mobile, email, phone, in-person, or cross-channel
- Scope boundary: Where the journey begins and ends for this map

### Step 2: Identify Journey Stages

@ux-researcher and @interaction-designer collaborate to define the major phases using the `user-journey-mapping` skill.

**Common stage framework:**

1. **Awareness** - User becomes aware of the need or discovers the product
2. **Consideration** - User evaluates options and explores the product
3. **Onboarding** - User begins using the product for the first time
4. **Usage** - User performs core tasks and workflows
5. **Retention** - User returns and deepens engagement
6. **Advocacy** - User recommends or shares the product

Adapt stages to fit the specific journey. Not every journey needs all stages. A checkout flow might have: Browse, Select, Configure, Review, Pay, Confirm.

**Output**: 4-7 named stages that represent the natural phases of this journey.

### Step 3: Map Touchpoints per Stage

For each stage, @interaction-designer identifies every touchpoint where the user interacts with the product, service, or brand.

**Touchpoint template:**

```
Stage: [Stage Name]
Touchpoints:
  - [Channel] - [Specific interaction point]
  - [Channel] - [Specific interaction point]
```

**Examples:**
```
Stage: Onboarding
Touchpoints:
  - Web - Sign-up form
  - Email - Welcome email with verification link
  - Web - Account setup wizard (3 steps)
  - Web - First-run tutorial overlay
  - Email - Day-2 tips email
```

Capture both digital and non-digital touchpoints. Include automated communications (emails, notifications) that occur between active interactions.

### Step 4: Document the User Experience at Each Touchpoint

For every touchpoint, document five dimensions:

#### Actions (What the user does)
Specific, observable behaviors. Use verb phrases.
- "Clicks the sign-up button"
- "Enters email and password"
- "Scans the dashboard for recent activity"

#### Thoughts (What the user is thinking)
Internal monologue, questions, and expectations.
- "Is this going to take long?"
- "Where do I find my recent orders?"
- "I wonder if this is secure"

#### Feelings (Emotional state)
Rate on a scale and name the emotion.
- Positive: Confident, excited, relieved, delighted
- Neutral: Curious, focused, indifferent
- Negative: Confused, frustrated, anxious, overwhelmed

#### Pain Points (What causes friction)
Specific problems, barriers, or annoyances.
- "Form requires information I don't have ready"
- "Loading takes 6+ seconds on mobile"
- "Error message doesn't explain what went wrong"

#### Opportunities (What could be improved)
Design improvements that address the pain points or enhance positive moments.
- "Pre-fill form fields from social login data"
- "Add skeleton loading states to reduce perceived wait"
- "Show inline validation with specific fix instructions"

### Step 5: Build the Emotion Curve

@ux-researcher plots the emotional journey across all stages.

**Emotion scale:**
```
+2  Delighted / Excited
+1  Satisfied / Confident
 0  Neutral / Focused
-1  Frustrated / Confused
-2  Angry / Abandoned
```

**Create the emotion curve:**

```
        Stage 1    Stage 2    Stage 3    Stage 4    Stage 5    Stage 6
+2  |                                                            *
+1  |    *                                  *
 0  |              *
-1  |                          *
-2  |
    +------------------------------------------------------------>
```

Annotate peaks and valleys:
- **Peaks**: What caused the positive moment? How can you amplify it?
- **Valleys**: What caused the negative moment? How can you eliminate or reduce it?
- **Recovery points**: Where does the experience recover? What drives that?

### Step 6: Identify Patterns and Opportunities

@ux-researcher and @interaction-designer analyze the complete map.

**Pattern analysis:**

1. **Moments of truth**: Touchpoints where users decide to continue or abandon
2. **Friction clusters**: Areas where multiple pain points stack up
3. **Delight opportunities**: Places where exceeding expectations creates loyalty
4. **Channel gaps**: Transitions between channels that break continuity
5. **Wait states**: Moments where the user is waiting with no feedback

**Prioritize opportunities:**

| Opportunity | Impact | Effort | Stage | Priority |
|------------|--------|--------|-------|----------|
| [Description] | High/Med/Low | High/Med/Low | [Stage] | P1/P2/P3 |

### Step 7: Create the Journey Map Document

Compile the complete journey map in a structured format:

```markdown
# Journey Map: [Journey Name]

**Persona**: [Persona name and brief description]
**Journey type**: Current state / Future state
**Scope**: [Starting trigger] to [End state]
**Date**: [When this map was created]

## Emotion Curve
[ASCII visualization]

## Stage-by-Stage Breakdown

### Stage 1: [Name]
**Duration**: [Time estimate]
**Touchpoints**: [List]
**User goal at this stage**: [What they want to accomplish]

| Dimension | Details |
|-----------|---------|
| Actions | [List] |
| Thoughts | [List] |
| Feelings | [Emotion + rating] |
| Pain Points | [List] |
| Opportunities | [List] |

[Repeat for each stage]

## Key Findings
1. [Most critical insight]
2. [Second insight]
3. [Third insight]

## Prioritized Opportunities
[Table from Step 6]

## Recommended Next Steps
1. [Action item]
2. [Action item]
3. [Action item]
```

## Related Skills

- `user-journey-mapping` - Detailed journey mapping methodology
- `user-research` - Research techniques to feed journey maps
- `usability-evaluation` - Evaluate specific touchpoints in the journey
- `information-architecture` - Optimize navigation and findability across stages

## Related Commands

- `/create-persona` - Build the persona who takes this journey
- `/evaluate-usability` - Deep-dive into specific problem touchpoints
- `/design-review` - Review designs for specific journey stages
- `/audit-accessibility` - Ensure every touchpoint is accessible

## Tips

- Start with the current-state map before designing the future state
- Use real user data wherever possible; mark assumptions clearly
- A journey map is a living document; update it as you learn more
- Focus on the valleys in the emotion curve; that is where the highest-impact work lives
- Share journey maps widely; they are one of the best tools for building organizational empathy

---
name: create-persona
description: Guided persona creation workflow that builds research-backed user persona cards with demographics, goals, frustrations, jobs-to-be-done, and usage scenarios.
user-invocable: true
allowed-tools: []
---

# Guided Persona Creation

Create a research-backed user persona through a structured process led by @ux-researcher. This command walks you through defining user segments, gathering data, and building a complete persona card that the team can reference throughout the design process.

## When to Use This Command

- Starting a new product or feature to define your target users
- Aligning the team on who you are designing for
- Replacing assumptions with structured user representations
- Updating existing personas with new research data
- Creating empathy maps or user profiles for stakeholder presentations

## Workflow

### Step 1: Define Research Context

@ux-researcher begins by establishing the project context.

**Gather from the user:**
- What product or feature are you designing for?
- What problem space does this address?
- Do you have existing research (interviews, surveys, analytics)?
- How many distinct user personas do you need?
- Are there existing personas to update or replace?

**Set scope:**
- Primary persona (the main user you design for)
- Secondary personas (important but not the primary focus)
- Anti-personas (who you are explicitly NOT designing for)

### Step 2: Identify User Segments

@ux-researcher helps identify distinct user groups using the `user-research` skill.

**Segmentation approaches:**

1. **Behavioral segmentation** - How do users interact with the product?
   - Usage frequency (daily, weekly, occasional)
   - Feature usage patterns
   - Task completion approaches (exploratory vs. goal-directed)

2. **Needs-based segmentation** - What are users trying to accomplish?
   - Primary goals and motivations
   - Pain points with current solutions
   - Unmet needs and desired outcomes

3. **Demographic segmentation** (use sparingly, behaviors matter more)
   - Role or job title
   - Technical proficiency
   - Industry or domain

**Output**: A list of 2-5 distinct user segments with brief descriptions of what makes each group unique.

### Step 3: Gather Data for Each Persona

@ux-researcher guides data collection. Use whichever sources are available:

**Qualitative sources:**
- User interviews (5-8 per segment is sufficient for patterns)
- Contextual inquiry or observation notes
- Support tickets and customer feedback
- Usability test recordings and notes

**Quantitative sources:**
- Analytics data (usage patterns, feature adoption, drop-off points)
- Survey results (satisfaction scores, task frequency)
- A/B test results and behavioral data

**Synthesis method:**
1. Identify recurring themes across sources
2. Look for patterns in goals, frustrations, and behaviors
3. Note direct quotes that capture the segment's voice
4. Map the relationship between demographics and behaviors

If no research data exists, @ux-researcher will guide the creation of a proto-persona based on team knowledge, clearly marked as hypothesis-driven and needing validation.

### Step 4: Build the Persona Card

For each persona, @ux-researcher constructs the following sections:

#### Identity

```
Name:        [Realistic first and last name]
Age:         [Age range, e.g., 28-35]
Role:        [Job title or life role]
Location:    [City/region type]
Photo note:  [Description of a representative photo to source]
```

#### Demographics and Context

- **Technical proficiency**: Novice / Intermediate / Advanced
- **Device usage**: Primary and secondary devices
- **Usage frequency**: How often they engage with this type of product
- **Key tools**: What tools and products they currently use

#### Goals (What They Want to Achieve)

List 3-5 goals ordered by priority:
1. Primary goal (the reason they use the product)
2. Secondary goals (additional value they seek)
3. Aspirational goal (what success looks like long-term)

#### Frustrations (What Gets in Their Way)

List 3-5 frustrations ordered by severity:
1. Biggest pain point with current solutions
2. Recurring annoyances
3. Fears or anxieties related to the problem space

#### Jobs to Be Done (JTBD)

Frame needs as JTBD statements:

```
When [situation],
I want to [motivation],
so I can [expected outcome].
```

Provide 2-3 JTBD statements covering:
- The core functional job
- An emotional job (how they want to feel)
- A social job (how they want to be perceived)

#### Representative Quote

A single sentence that captures the persona's attitude and primary need. This should sound like something a real person would say, drawn from interview data or synthesized from research themes.

```
"I just need to [core need] without [main frustration] so I can [desired outcome]."
```

#### Day-in-the-Life Scenario

Write a brief narrative (3-5 paragraphs) describing a typical day or workflow where this persona encounters the problem your product solves. Include:
- The context and trigger that starts the interaction
- What they currently do (including workarounds)
- The emotional state at key moments
- Where the product fits into their workflow

#### Behavioral Attributes (Spectrum Scales)

Rate on a 1-5 spectrum:

```
Tech-savvy    [1----2----3----4----5]  Tech-averse
Cautious      [1----2----3----4----5]  Risk-taking
Independent   [1----2----3----4----5]  Collaborative
Price-driven  [1----2----3----4----5]  Quality-driven
Task-focused  [1----2----3----4----5]  Exploratory
```

### Step 5: Validate with the Team

@ux-researcher guides validation:

1. **Reality check**: Does this persona match what the team observes in real users?
2. **Distinctness**: Is this persona clearly different from other personas?
3. **Actionability**: Can the team make design decisions based on this persona?
4. **Completeness**: Are there gaps that need more research?

**Validation questions to ask stakeholders:**
- "Have you met someone like this persona?"
- "What would you change about this description?"
- "Can you think of a real user who does NOT fit any of our personas?"

### Step 6: Format and Deliver

Provide the complete persona in a clean, referenceable format:
- Full persona card as structured markdown
- Quick-reference version (name, photo note, quote, top 3 goals, top 3 frustrations)
- JTBD statements as standalone reference
- Scenario narrative for empathy exercises

## Persona Quality Checklist

Before finalizing, verify:

- [ ] Based on real data (or clearly marked as proto-persona)
- [ ] Goals and frustrations are specific, not generic
- [ ] JTBD statements follow the correct format
- [ ] Quote sounds like a real person, not marketing copy
- [ ] Scenario includes emotional context, not just tasks
- [ ] Behavioral spectrums are honest (not all ideal traits)
- [ ] Persona is distinct from other personas in the set
- [ ] Team can use this to make specific design decisions

## Related Skills

- `user-research` - Research methodology and data collection
- `user-journey-mapping` - Map how this persona moves through your product
- `ab-testing-strategy` - Test hypotheses about persona behavior

## Related Commands

- `/map-journey` - Create a journey map for this persona
- `/evaluate-usability` - Test the interface against this persona's needs
- `/design-review` - Review designs with this persona's goals in mind

## Tips

- A good persona should make the team uncomfortable about at least one design decision
- If everyone on the team already agrees with the persona, it is probably too generic
- Proto-personas are useful starting points but schedule real research to validate them
- Revisit personas quarterly or when usage patterns shift significantly
- Keep the total number of personas small (2-4) to maintain focus

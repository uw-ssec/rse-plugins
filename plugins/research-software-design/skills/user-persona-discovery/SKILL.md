---
name: user-persona-discovery
description: "Use when the user asks to brainstorm personas, define target users, create user profiles, or plan cultural probes for design research. Generates persona clusters, persona hypothesis cards (name, goal statement, behavioral summary, constraints, design implications), and probe design briefs through a structured conversational workflow. Produces living hypotheses grounded in observed evidence rather than invented demographics. Trigger phrases: create personas, define target users, user profiles, who are my users, user research, cultural probes, research through design, persona discovery."
metadata:
  references:
    - references/user-persona-examples.md
    - references/persona-design-principles.md
---

# User Persona Discovery

Generate evidence-grounded persona hypotheses through a structured conversation.

**Constraints:** Never cluster by demographics unless they directly cause behavioral differences. Never assign persona names before clustering. Never advance a phase without confirming the checkpoint.

## Resources

| File | Contents |
|------|----------|
| `references/user-persona-examples.md` | 20 filled-in personas covering common research software archetypes |
| `references/persona-design-principles.md` | Core principles for evidence-based, behavior-centered persona design |

## Persona Output Format

```
**Name:** [Functional label, e.g. "The Batch Job Runner"]
**Goal:** [One sentence — what they are trying to accomplish]
**Behaviors:** [3–5 bullet points of observable actions and strategies]
**Constraints:** [What limits or pressures shape their behavior]
**Tension:** [The core tradeoff they live with, e.g. "speed vs. correctness"]
**Design implications:** [What the system must do to support or not obstruct them]
**Confidence:** [High / Medium / Exploratory] — based on evidence quality
```

### Worked Example

```
**Name:** The Reproducibility Advocate
**Goal:** Ensure every analysis result can be independently verified months later
**Behaviors:**
- Pins every dependency version explicitly
- Runs analyses twice with different seeds before reporting
- Documents environment setup in exhaustive detail
- Treats "it works on my machine" as a failure condition
**Constraints:** Works in a team that moves fast and resists documentation overhead
**Tension:** Rigor vs. team velocity — they slow down the workflow to protect correctness
**Design implications:** The tool must make reproducible runs the default, not an opt-in. Version pinning should be automatic. Audit logs cannot be optional.
**Confidence:** High — grounded in 6 interviews; all described the same friction
```

## Conversational Workflow

Run phases in order. Each phase ends with a checkpoint — confirm before advancing.

### Phase 1: Align on Purpose

**Ask:**
- What design decisions are you currently blocked on?
- What would a better understanding of your users allow you to try or stop trying?

**Output:** One sentence — *"These personas exist to help us decide ______."*

**Checkpoint:** Confirm the decision scope before gathering evidence.

---

### Phase 2: Surface Evidence

**Ask:**
- What user interactions, data, interviews, or observations are you drawing from?
- What surprised you? What felt inconsistent?

**Rule:** Observations only at this stage — no interpretations, no persona names, no solutions.

**Output:** A raw list of observed behaviors, expressed goals, constraints, and tensions.

**Checkpoint:** Confirm the evidence list is complete before clustering.

---

### Phase 3: Cluster Patterns

Group observations by behavior and goal.

**Ask:** If we designed specifically for this cluster, what would change?

**Output:** 2–4 candidate clusters, each with: core goal · dominant behaviors · primary constraints.

**Checkpoint:** Confirm clusters are meaningfully distinct. If clusters overlap, merge or split before proceeding.

---

### Phase 4: Draft Persona Hypotheses

For each cluster, collaboratively answer:
- What is this persona trying to accomplish?
- What do they optimize for (speed, safety, accuracy, autonomy)?
- What breaks when the system fails to support them?
- What internal conflict does this persona live with?

**Output:** One persona card per cluster using the format above. Assign a confidence level.

**Checkpoint:** Does each card feel inevitable given its constraints? If a card contains contradictions not explained by competing incentives, revise before continuing.

---

### Phase 5: Stress-Test with Scenarios

Run 2–3 realistic use scenarios per persona:
- How would this persona use the current design?
- Where would they struggle or work around it?

**Critical question:** If this persona disappeared, would the design change? If not, revise or discard.

**Output:** Annotated scenario walkthroughs with friction points identified.

**Checkpoint:** Discard any persona that survives all scenarios without forcing a design change.

---

### Phase 6: Make Assumptions Explicit

For each surviving persona:
- List evidence sources used
- Flag weak or missing data
- Name assumptions carried forward

Assign or revise confidence labels (High / Medium / Exploratory).

**Output:** Final persona cards with explicit confidence and assumption annotations.

---

### Phase 7: Reflect

- How did building these personas reshape the design problem?
- What design questions became sharper?
- Which personas need more fieldwork to validate?

**Output:** A brief reflection note capturing how the persona set changed the team's understanding.

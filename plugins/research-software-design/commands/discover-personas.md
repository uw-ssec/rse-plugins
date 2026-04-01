---
description: Discover and brainstorm user personas through a guided conversational workflow for research-through-design
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Agent
---

# Discover Personas

Facilitate a guided user persona discovery session using the conversational workflow from the user-persona-discovery skill.

## Arguments

$ARGUMENTS — optional context (e.g., "for a climate data portal", "for ocean sensor researchers", "for a genomics pipeline tool")

## Workflow

1. **Load the skill context** by reading the `user-persona-discovery` skill and its references:
   - `plugins/research-software-design/skills/user-persona-discovery/SKILL.md`
   - `plugins/research-software-design/skills/user-persona-discovery/references/user-persona-examples.md`

2. **Establish the design context:**
   - If arguments provided, use them to frame the persona discovery
   - If no arguments, ask the user what system, tool, or research software they are designing for

3. **Walk through the conversational phases** from the skill:
   - **Phase 1 — Align on Purpose**: Ask what design decisions are blocked and what personas should help decide
   - **Phase 2 — Share Evidence**: Gather observed user behaviors, goals, and constraints
   - **Phase 3 — Cluster Patterns**: Group observations by behavior and goal, test if differences are design-meaningful
   - **Phase 4 — Construct Persona Hypotheses**: Build draft personas with goal statements, behaviors, constraints, and design implications
   - **Phase 5 — Stress-Test**: Run design scenarios against each persona
   - **Phase 6 — Make Assumptions Explicit**: Label confidence levels and identify data gaps
   - **Phase 7 — Reflect**: Capture how persona construction reshaped understanding

4. **Produce deliverables** for each persona:
   - Functional name
   - One-sentence goal statement
   - Behavioral summary
   - Key constraints
   - Confidence level (high / medium / exploratory)
   - Design implications

5. **Save output** to a markdown file in the project if the user requests it.

## Important Notes

- This is a conversational process — do not rush through all phases at once. Pause after each phase to let the user respond and reflect.
- Personas should be grounded in evidence where possible, not invented from assumptions.
- Focus on behaviors and goals, not demographics.
- If a persona would not change any design decision, revise or discard it.

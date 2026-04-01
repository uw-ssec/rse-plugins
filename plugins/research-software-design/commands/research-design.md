---
description: Apply a research-through-design approach to a design and engineering problem using scientific literature
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Agent
  - WebSearch
  - WebFetch
---

# Research Design

Apply a Research-Through-Design approach to a design and engineering problem, using scientific literature and scholarly resources to inform iterative solution design.

## Arguments

$ARGUMENTS — the design problem or research question (e.g., "design a data pipeline for ocean sensor data", "explore approaches for CRISPR crop yield optimization")

## Workflow

1. **Frame the research question:**
   - If arguments provided, use them as the starting problem statement
   - If no arguments, ask the user to describe the design challenge they are facing
   - Clarify scope, constraints, and success criteria

2. **Literature and evidence gathering:**
   - Search for relevant scientific literature, technical approaches, and prior work
   - Summarize key findings, methods, and trade-offs from the literature
   - Identify gaps or unresolved questions

3. **Construct design artifacts:**
   - Propose candidate designs, architectures, or approaches informed by the evidence
   - Present trade-offs between candidates (performance, complexity, scalability, cost)
   - Identify technical constraints and dependencies

4. **Iterative refinement:**
   - Present the candidate design to the user for feedback
   - Refine based on user input, additional constraints, or new evidence
   - Repeat until the user is satisfied with the direction

5. **Produce deliverables:**
   - Design rationale document linking decisions to evidence
   - Architecture or process diagram description
   - Open questions and next steps for validation

6. **Save output** to a markdown file in the project if the user requests it.

## Important Notes

- This is an iterative process — design activity is the method of inquiry, not just the output.
- Ambiguity is expected. Present options and trade-offs rather than a single "correct" answer.
- Ground recommendations in evidence from literature and prior work, not assumptions.
- Frame open questions explicitly so they can guide future research or experimentation.

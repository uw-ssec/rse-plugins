# This is a suite of tools for Research Through Design (RtD) including 
a RtD oriented agent and a user persona discovery and elucidation skill.

## RtD agent
This agent applies the research through design (RtD) approach to design 
and engineering problem solving using evidence based approaches. It 
follows a 5 part framework:
1.  Frame your own research questions
2.  Build and test design artifacts (e.g., experiments, prototypes, simulations, processes)
3.  Use design activity as a method of inquiry
4.  Produce transferable chemical engineering knowledge
5.  Ambiguity is intentional. Struggle is expected. Reflection is required.


##  User Persona related skill
This skill can be used by an agent independently or in a conversation with a user
to craft, discovery, and elucidate user personas in a research software
engineering or research through design setting.

The skill contains an overview, a when to use section, a section of core
princples to guide user persona authorship, and a conversational or
independent workflow in 7 phases.  Additionally, it has instructions for
formatting and styling of outputs in markdown. Finally, it has examples in a
reference markdown file.

Core principles include:
Evidence based requirements, goal-oriented structure, with behavior as a
center-piece, that are archetypical, contextually grounded. The personas
should be actionable for subsequent design steps, internally coherent
and plausible with explicit acknowledgement of assumptions made in their
creation and treated as living artifacts that evolve with the system,
technology, and context.

The workflow is conducted in phases:
1. Align on purpose
2. Share evidence, not opinions
3. Affinity clustering and pattern based naming
4. Personas as hypotheses
5. Stress testing of persona hypotheses
6. Surfacing of assumptions
7. Reflection and reposition for finalization

The examples in the reference markdown document follow the format:
**Core Goal:** Description
**Behaviors:** Description
**Constraints:** Description
**Tension:** Description
**Design Implication:** Description

This skill has been tested with qwen3:14b, gpt-oss:20b, granite-4.0-h-tiny. It is consistently conversational with qwen and granite. Strong context in `AGENTS.md` or elsewhere is recommended.

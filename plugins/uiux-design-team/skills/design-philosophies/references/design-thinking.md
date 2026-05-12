# Design Thinking

A comprehensive reference on the Stanford d.school Design Thinking framework, the British Design Council's Double Diamond model, facilitation techniques for each phase, common mistakes that derail the process, and workshop planning guidance for design teams.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Stanford d.school: Five Phases](#stanford-dschool-five-phases) | 14-75 | Deep dive into Empathize, Define, Ideate, Prototype, and Test |
| [The Double Diamond Framework](#the-double-diamond-framework) | 77-115 | Discover, Define, Develop, Deliver with convergent/divergent thinking |
| [Facilitation Techniques](#facilitation-techniques) | 117-170 | Specific workshop methods for each phase |
| [Common Mistakes](#common-mistakes) | 172-210 | Anti-patterns that undermine the Design Thinking process |
| [Workshop Planning](#workshop-planning) | 212-240 | Structuring multi-day design sprints and single-session workshops |

## Stanford d.school: Five Phases

Design Thinking is not a linear process. The five phases overlap, repeat, and loop back. Treat them as modes of work rather than sequential steps. A team may empathize, jump to prototype, learn something that sends them back to define, and then ideate again. This iteration is not failure -- it is the process working correctly.

### Phase 1: Empathize

The empathy phase builds deep understanding of the people you are designing for. It requires setting aside assumptions and immersing yourself in the user's world.

**Methods:**
- **Contextual inquiry**: Observe users in their natural environment while they perform tasks. Take notes on workarounds, frustrations, and moments of delight.
- **Empathy interviews**: One-on-one conversations focused on feelings, motivations, and past experiences. Ask "why" five times to reach root causes.
- **Immersion**: Use the product or process yourself, under realistic constraints. Experience the pain points firsthand.
- **Diary studies**: Ask users to document their experiences over days or weeks to capture longitudinal patterns.

**Outputs:** Empathy maps, interview transcripts, observation notes, journey fragments, raw quotes.

**Time allocation:** 20-30% of the total design process. Skimping here guarantees you solve the wrong problem.

### Phase 2: Define

The define phase synthesizes empathy findings into a clear, actionable problem statement. This is where raw data becomes design direction.

**Methods:**
- **Affinity mapping**: Group observations into clusters. Let themes emerge from the data rather than imposing categories.
- **How Might We (HMW)**: Reframe problems as opportunities. "Users forget their passwords" becomes "How might we help users access their accounts without remembering credentials?"
- **Point of View (POV) statement**: "[User] needs [need] because [insight]." Example: "A busy project manager needs to see team progress at a glance because they have 30 seconds between meetings to check status."
- **Problem prioritization**: Use a 2x2 matrix (user impact vs. feasibility) to select which problems to solve first.

**Outputs:** POV statements, HMW questions, prioritized problem list, design principles.

**Common trap:** Writing a problem statement that already implies a solution. "Users need a dashboard" is a solution masquerading as a need. "Users need to understand team progress without interrupting their workflow" is a genuine need.

### Phase 3: Ideate

The ideate phase generates a wide range of possible solutions. Volume matters more than quality at this stage. The goal is 50 ideas, not 5 perfect ones.

**Methods:**
- **Crazy 8s**: Fold a sheet of paper into 8 panels. Sketch one idea per panel, one minute each. The time constraint forces quantity over polish.
- **Brain writing**: Each person writes 3 ideas on paper, passes it to the next person who builds on those ideas. Eliminates groupthink and dominant-voice bias.
- **Worst possible idea**: Deliberately generate terrible solutions, then invert them. "What if we made users fill out a 50-field form?" inverts to "What if we eliminated the form entirely?"
- **SCAMPER**: Substitute, Combine, Adapt, Modify, Put to other use, Eliminate, Reverse. Apply each verb to the current solution to generate alternatives.
- **How Might We voting**: Dot-vote on HMW questions to identify the most promising opportunity areas, then ideate specifically within those areas.

**Outputs:** Sketches, concept descriptions, idea clusters, shortlisted concepts.

**Rule:** Defer judgment during ideation. Criticism kills creativity. Evaluation happens later.

### Phase 4: Prototype

The prototype phase makes ideas tangible enough to test. Prototypes are learning tools, not deliverables. Build the minimum needed to answer your most critical question.

**Fidelity ladder:**

| Fidelity | Time to Build | Best For | Tools |
|----------|--------------|----------|-------|
| Paper sketches | 5-15 minutes | Testing layout concepts and flows | Paper, markers, sticky notes |
| Clickable wireframes | 1-4 hours | Testing navigation and task completion | Figma, Balsamiq, pen and paper with "click here" annotations |
| Interactive mockups | 1-3 days | Testing visual design and micro-interactions | Figma prototyping, Framer |
| Coded prototypes | 3-10 days | Testing real data, performance, and edge cases | HTML/CSS/JS, React, framework of choice |
| Wizard of Oz | Variable | Testing complex logic without building it | Human behind the curtain simulating the system |

**Rule:** Use the lowest fidelity that answers your question. If you need to know whether users understand the navigation structure, a paper prototype suffices. Do not build a coded prototype for a question paper can answer.

### Phase 5: Test

The test phase puts prototypes in front of real users to validate or invalidate assumptions. Testing is not about proving the design works -- it is about discovering where it fails.

**Methods:**
- **Think-aloud testing**: Ask users to narrate their thought process while performing tasks. "I'm looking for the settings... I expected it to be in the top right... Now I'm confused about what this icon means."
- **Task-based testing**: Give users specific tasks ("Find the billing settings and update your payment method") and observe success rate, time, and error paths.
- **A/B testing**: For higher-fidelity prototypes, compare two approaches with different user groups. Measure completion rate, time on task, and error rate.
- **Desirability testing**: Show users multiple design directions and ask them to select adjectives that describe each. Reveals emotional response beyond usability.

**Outputs:** Test findings, usability issues ranked by severity, validated or invalidated assumptions, iteration priorities.

**Rule:** Test with 5 users per round. Research shows 5 users uncover approximately 85% of usability problems. Run multiple rounds of 5 rather than one round of 15.

## The Double Diamond Framework

The British Design Council's Double Diamond is a visual model of the design process with four phases organized into two diamonds. Each diamond has a divergent phase (expanding possibilities) followed by a convergent phase (narrowing to decisions).

### Diamond 1: Problem Space

**Discover (Diverge):** Explore the problem space broadly. Research users, study the market, examine analogous products, gather data from multiple sources. Cast a wide net. Do not narrow prematurely.

- Talk to users, stakeholders, and domain experts
- Analyze support tickets, analytics, and competitive products
- Map the current experience end-to-end
- Identify all pain points, not just the obvious ones

**Define (Converge):** Synthesize research into a clear problem definition. From all the problems discovered, select the most important and most tractable ones to solve.

- Prioritize problems by user impact and business value
- Write clear problem statements
- Establish success criteria and metrics
- Align stakeholders on the chosen problem focus

### Diamond 2: Solution Space

**Develop (Diverge):** Generate a wide range of solutions for the defined problem. Explore different approaches, technologies, and interaction models. Prototype and test multiple concepts in parallel.

- Sketch multiple concepts (not just one)
- Build low-fidelity prototypes of the most promising ideas
- Test prototypes with users and gather feedback
- Iterate rapidly based on test results

**Deliver (Converge):** Select the strongest solution and refine it for production. Polish the design, document specifications, and prepare for implementation.

- Select the solution with the strongest test results
- Refine the design to production quality
- Write handoff documentation
- Plan for measurement and iteration post-launch

### Double Diamond vs. Design Thinking

The Double Diamond and Design Thinking are complementary. Design Thinking provides specific methods (empathy maps, Crazy 8s, think-aloud testing). The Double Diamond provides the strategic structure (when to diverge, when to converge). Use the Double Diamond as the macro framework and Design Thinking methods within each phase.

| Double Diamond Phase | Design Thinking Overlap | Key Activity |
|---------------------|------------------------|--------------|
| Discover | Empathize | User research, observation |
| Define | Define | Problem framing, HMW questions |
| Develop | Ideate + Prototype | Solution generation, prototyping |
| Deliver | Prototype + Test | Refinement, validation, handoff |

## Facilitation Techniques

### For Empathy Workshops

**Empathy Map Canvas (60 minutes):** Divide a large canvas into four quadrants -- Says, Thinks, Does, Feels. Teams fill each quadrant with sticky notes based on user research data. The tension between "Says" and "Does" often reveals the deepest insights.

**Experience Timeline (45 minutes):** Draw a horizontal timeline. Have participants map a user's experience chronologically, marking emotional highs and lows. Identify the moments that matter most -- the peaks, valleys, and transitions.

**Assumption Dump (30 minutes):** Before any research begins, have every team member write their assumptions about the user on sticky notes. Post them on a wall. After research, revisit and mark which assumptions were validated, invalidated, or remain untested. This makes bias visible.

### For Define Workshops

**Silent Affinity Mapping (45 minutes):** Print or write every research observation on individual sticky notes. In silence, team members group related notes. No talking allowed during grouping -- this prevents dominant voices from controlling the narrative. After grouping, discuss the themes that emerged.

**HMW Generation (30 minutes):** Read each insight statement aloud. For each, every participant writes 2-3 "How Might We" questions on sticky notes. Post all HMWs, then dot-vote to prioritize. Select the top 3-5 for ideation.

**Problem Statement Workshop (45 minutes):** Using the template "[User] needs [need] because [insight]," each team member writes 3 problem statements. Share and discuss. Collaborate to refine the strongest statement into the project's guiding problem definition.

### For Ideation Workshops

**Crazy 8s (15 minutes):** Each participant folds paper into 8 panels and sketches one idea per panel in one minute. No judgment, no erasing, no perfecting. After the timer, present top 2-3 ideas to the group.

**Design Studio (90 minutes):** Round 1 -- individuals sketch solutions independently (15 min). Round 2 -- present sketches, receive critique (30 min). Round 3 -- iterate based on feedback, combine promising elements from multiple sketches (15 min). Round 4 -- converge on 2-3 directions for prototyping (30 min).

**Reverse Brainstorm (30 minutes):** Ask "How could we make this problem WORSE?" Generate terrible ideas enthusiastically. Then flip each terrible idea into a good one. This technique loosens creative blocks and generates unexpected approaches.

### For Test Planning

**Test Script Writing (45 minutes):** Write 5-7 task scenarios that map to the research questions. For each task, define the success criteria, the expected path, and what you will observe. Pilot the script with a colleague before testing with real users.

**Rainbow Spreadsheet (post-testing):** Create a spreadsheet where each column is a participant and each row is an observation or usability issue. Color-code cells by severity. Patterns become visible when the same issue appears across multiple participants in the same color.

## Common Mistakes

### Jumping to Solutions

The most destructive mistake in Design Thinking. Teams skip empathy and definition because they "already know what to build." The result is a well-built solution to the wrong problem. The antidote is discipline: refuse to discuss solutions until the problem is defined and validated with user evidence.

**Warning signs:** Someone says "What if we just built..." in the first meeting. The team discusses features before talking to a single user. The problem statement sounds like a feature description.

### Skipping Empathy

Teams conduct one round of interviews, declare they "get it," and move on. Real empathy requires sustained exposure to user reality -- multiple interviews, contextual observation, and diary studies. Surface-level research produces surface-level insights.

**Warning signs:** Fewer than 5 user conversations. All interviews conducted by one person. No observation of actual user behavior (only self-reported descriptions).

### Premature Convergence

During ideation, the team latches onto the first reasonable idea and skips generating alternatives. This feels efficient but produces mediocre solutions. The best ideas rarely appear first. They emerge from the collision of many ideas.

**Warning signs:** The team has only one concept to prototype. Nobody pushed back on the chosen direction. The ideation session lasted 20 minutes.

### Confirmation Bias in Testing

Designing tests that confirm the team's preferred solution rather than genuinely challenging it. Asking leading questions, selecting friendly test participants, and interpreting ambiguous results as positive.

**Warning signs:** Every test participant "loved it." The team dismisses negative feedback as edge cases. Test tasks are so guided that failure is nearly impossible.

### Treating Phases as Checkboxes

Design Thinking is iterative. Treating the five phases as a linear checklist ("We did empathy, now we do define, then we ideate...") removes the feedback loops that make the process work. If testing reveals a flawed assumption, go back to empathy. If ideation reveals ambiguity in the problem, go back to define.

### Over-Investing in Prototypes

Building high-fidelity prototypes too early. When a team spends a week building a polished prototype, they become emotionally attached to it and resist evidence that it should be abandoned. Low-fidelity prototypes are disposable by design -- that disposability is their greatest advantage.

## Workshop Planning

### One-Day Design Sprint

| Time | Phase | Activity | Output |
|------|-------|----------|--------|
| 9:00-10:00 | Empathize | Share research findings, empathy map exercise | Shared understanding of user |
| 10:00-10:45 | Define | Silent affinity mapping, HMW generation | Prioritized HMW questions |
| 10:45-11:00 | Break | | |
| 11:00-12:00 | Ideate | Crazy 8s, design studio round 1 | 40+ solution sketches |
| 12:00-13:00 | Lunch | | |
| 13:00-14:00 | Ideate | Design studio rounds 2-3, dot voting | 2-3 shortlisted concepts |
| 14:00-15:30 | Prototype | Build paper or clickable prototypes | Testable prototypes |
| 15:30-16:30 | Test | Hallway testing with 3-5 people | Initial validation data |
| 16:30-17:00 | Reflect | Capture learnings, plan next steps | Action items and owner list |

### Multi-Day Design Sprint (5 Days)

Based on the Google Ventures Design Sprint methodology:

- **Monday -- Map and Target:** Map the problem space, choose a target area, interview experts
- **Tuesday -- Sketch:** Individual solution sketching, lightning demos of inspiring products
- **Wednesday -- Decide:** Present sketches, dot vote, storyboard the winning concept
- **Thursday -- Prototype:** Build a realistic facade prototype (looks real, is not real)
- **Friday -- Test:** Five user tests, debrief, decide next steps

### Facilitation Ground Rules

Post these visibly at the start of every workshop:

1. **One conversation at a time.** Side conversations fragment the group's thinking.
2. **Defer judgment during divergent phases.** Criticism is welcome during convergence, not during ideation.
3. **Build on others' ideas.** Use "Yes, and..." rather than "No, but..."
4. **Go for quantity.** More ideas increase the odds of finding great ones.
5. **Be visual.** Sketch, diagram, and map rather than just talking. Tangible beats abstract.
6. **Stay focused on the user.** When debates stall, ask "What would the user need here?"
7. **Timebox ruthlessly.** Constraints are creative fuel. Respect the clock.

## See Also

- [[gestalt-principles.md]] -- Visual organization principles applied during prototyping and layout decisions
- [[emotional-design.md]] -- Evaluate visceral, behavioral, and reflective impact during testing phases
- [[../../design-case-studies/references/saas-dashboards.md]] -- Real-world examples of Design Thinking applied to complex product design
- [[../../user-research/references/interview-guide.md]] -- Detailed interview methodology for the empathy phase
- [[../../user-research/references/synthesis-methods.md]] -- Affinity mapping and synthesis techniques for the define phase

**Back to:** [Design Philosophies Skill](../SKILL.md)

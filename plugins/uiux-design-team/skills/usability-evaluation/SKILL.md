---
name: usability-evaluation
description: Evaluate interface usability using Nielsen's 10 heuristics, cognitive walkthroughs, System Usability Scale scoring, severity ratings, and task analysis to identify and prioritize usability issues.
metadata:
   references:
   - references/nielsen-heuristics.md
   - references/scoring-methods.md
   - references/walkthrough-guide.md
---

# Usability Evaluation

Usability evaluation catches problems before users do. It is the systematic process of examining an interface against established principles and real user behavior to identify issues that make products difficult, confusing, or error-prone. Unlike user research which explores what to build, usability evaluation examines how well what you have built actually works.

There are two broad categories: **inspection methods** (experts evaluate the interface using principles) and **testing methods** (real users attempt tasks while observers note difficulties). This skill covers both, with emphasis on the inspection methods that can be performed quickly and repeatedly throughout the design process.

## Quick Start: Heuristic Evaluation

A heuristic evaluation can be completed in 2-4 hours and consistently surfaces 60-80% of usability issues when performed by 3-5 evaluators.

**Step 1 -- Select evaluators.** Choose 3-5 people with UX knowledge. More evaluators means more coverage, but returns diminish after 5.

**Step 2 -- Walk through the interface independently.** Each evaluator goes through every screen and interaction, comparing what they see against Nielsen's 10 heuristics (listed below).

**Step 3 -- Document each violation.** For every issue, record:
- Which heuristic is violated
- Where in the interface the violation occurs (screen, component, state)
- A description of the problem
- A severity rating (0-4)
- A suggested fix (optional but helpful)

**Step 4 -- Merge findings.** Combine all evaluators' findings into a single list. Consolidate duplicates and average severity ratings.

**Step 5 -- Prioritize and report.** Sort by severity. Present the top issues with screenshots and specific recommendations to stakeholders.

## Nielsen's 10 Heuristics

These ten principles, developed by Jakob Nielsen, form the standard framework for expert usability evaluation.

1. **Visibility of system status** -- The system should always keep users informed about what is going on through appropriate feedback within reasonable time. Progress bars, loading indicators, and state changes must be visible.

2. **Match between system and real world** -- The system should speak the users' language with words, phrases, and concepts familiar to the user rather than system-oriented terms. Follow real-world conventions and present information in a natural and logical order.

3. **User control and freedom** -- Users often perform actions by mistake. They need a clearly marked "emergency exit" to leave unwanted states without going through an extended process. Support undo, redo, and cancel.

4. **Consistency and standards** -- Users should not have to wonder whether different words, situations, or actions mean the same thing. Follow platform conventions. Internal consistency (within your product) and external consistency (with established patterns) both matter.

5. **Error prevention** -- Even better than good error messages is a careful design that prevents a problem from occurring in the first place. Eliminate error-prone conditions or check for them and present users with a confirmation option before they commit to the action.

6. **Recognition rather than recall** -- Minimize the user's memory load by making elements, actions, and options visible. The user should not have to remember information from one part of the interface to another. Instructions for use should be visible or easily retrievable.

7. **Flexibility and efficiency of use** -- Accelerators, unseen by novice users, can speed up interaction for expert users so that the system can cater to both inexperienced and experienced users. Allow users to tailor frequent actions.

8. **Aesthetic and minimalist design** -- Interfaces should not contain information that is irrelevant or rarely needed. Every extra unit of information in an interface competes with relevant information and diminishes its relative visibility.

9. **Help users recognize, diagnose, and recover from errors** -- Error messages should be expressed in plain language (no codes), precisely indicate the problem, and constructively suggest a solution.

10. **Help and documentation** -- Even though it is better if the system can be used without documentation, it may be necessary to provide help. Any such information should be easy to search, focused on the user's task, list concrete steps, and not be too large.

## Severity Ratings

Use a consistent 0-4 scale to rate every identified issue. Severity determines triage priority.

| Rating | Label       | Definition                                                                                  | Action                        |
|--------|-------------|--------------------------------------------------------------------------------------------|-------------------------------|
| 0      | Not a problem | Evaluator disagrees this is a usability issue                                              | No action needed              |
| 1      | Cosmetic    | Issue noticed but does not affect task completion; fix only if time allows                   | Backlog                       |
| 2      | Minor       | User is slowed down or confused but can still complete the task without help                 | Fix in next iteration         |
| 3      | Major       | User has significant difficulty; some users may fail the task or require assistance          | Fix before next release       |
| 4      | Catastrophe | User cannot complete the task at all; the product is unusable for this scenario              | Fix immediately               |

**Decision criteria for rating:**
- Does the issue prevent task completion? (If yes: 3 or 4)
- Does the issue occur on a critical path or an edge case? (Critical path increases severity)
- Can the user recover on their own? (If not: increase severity)
- How many users are affected? (Wide impact increases severity)

## Cognitive Walkthrough

A cognitive walkthrough simulates a new user's thought process step by step through a specific task. It is especially useful for evaluating onboarding flows and first-time experiences.

**Define the inputs:**
1. The user's goal (e.g., "Create and share a report with my team")
2. The action sequence needed to achieve the goal (list every click, input, and decision)
3. The user's expected knowledge and experience level

**For each action in the sequence, answer four questions:**

- **Q1: Will the user try to achieve the right effect?** Does the user know this step is necessary? Is the goal of this action clear?
- **Q2: Will the user notice that the correct action is available?** Is the button, link, or input visible? Does it look interactive?
- **Q3: Will the user associate the correct action with the desired effect?** Does the label or icon clearly communicate what will happen? Will the user understand that clicking this thing leads toward their goal?
- **Q4: If the correct action is performed, will the user see that progress is being made?** Does the system provide feedback? Does the next state clearly indicate the action was successful?

If the answer to any question is "no," you have found a usability issue. Document the step number, the failed question, and a recommendation for improvement.

## System Usability Scale (SUS)

The System Usability Scale is a standardized 10-question survey that produces a single score from 0-100 measuring perceived usability.

**The 10 questions** (each rated 1 = Strongly Disagree to 5 = Strongly Agree):

1. I think that I would like to use this system frequently.
2. I found the system unnecessarily complex.
3. I thought the system was easy to use.
4. I think that I would need the support of a technical person to use this system.
5. I found the various functions in this system were well integrated.
6. I thought there was too much inconsistency in this system.
7. I would imagine that most people would learn to use this system very quickly.
8. I found the system very cumbersome to use.
9. I felt very confident using the system.
10. I needed to learn a lot of things before I could get going with this system.

**Scoring formula:**
- For odd-numbered items (1, 3, 5, 7, 9): subtract 1 from the score
- For even-numbered items (2, 4, 6, 8, 10): subtract the score from 5
- Sum all adjusted scores and multiply by 2.5

**Interpretation:**
- Below 50: Unacceptable usability -- significant redesign needed
- 50-67: Marginal usability -- notable issues to address
- 68: Industry average
- 68-80: Good usability -- above average, minor improvements possible
- 80-90: Excellent usability -- users are satisfied and productive
- Above 90: Exceptional -- best-in-class experience

Administer the SUS after usability testing sessions to get a quantitative benchmark you can track over time.

## Deep Dive References

### [Nielsen Heuristics](references/nielsen-heuristics.md)

- H1: Visibility of System Status
- H2: Match Between System and Real World
- H3: User Control and Freedom
- H4: Consistency and Standards
- H5: Error Prevention
- H6: Recognition Rather Than Recall
- H7: Flexibility and Efficiency of Use
- H8: Aesthetic and Minimalist Design
- *...and 2 more sections*

### [Walkthrough Guide](references/walkthrough-guide.md)

- Overview
- Definition and When to Use
- Preparation Steps
- The Four Walkthrough Questions
- Action Sequence Analysis
- Step 6: Click "Add to Cart"
- Success and Failure Stories
- Comparison with Heuristic Evaluation
- *...and 11 more sections*

### [Scoring Methods](references/scoring-methods.md)

- Overview
- System Usability Scale (SUS)
- Single Ease Question (SEQ)
- NASA Task Load Index (NASA-TLX)
- SUPR-Q (Standardized User Experience Percentile Rank Questionnaire)
- Net Promoter Score (NPS)
- Task-Level Performance Metrics
- Combining Metrics: The Usability Scorecard
- *...and 1 more sections*

## Next Steps

After evaluating usability, apply your findings with these related skills:

- **accessibility-audit** -- Extend your evaluation to cover accessibility standards (WCAG), ensuring your interface works for users of all abilities.
- **user-research** -- When heuristic evaluation reveals suspected issues, validate them with real users through usability testing or interviews.

---
name: evaluate-usability
description: Guided usability evaluation using heuristic analysis, cognitive walkthrough, or expert review with severity-scored findings
user-invocable: true
allowed-tools: []
---

# Evaluate Usability

A guided usability evaluation command that produces a scored, actionable report. This command routes through **@ux-design-lead** to **@ux-researcher** for execution.

## Workflow

### Step 1: Select Evaluation Method

Ask the user which evaluation method to use. Each has different strengths.

**Prompt the user:**

> Which usability evaluation method should we use?
>
> **1. Heuristic Evaluation**
> Systematic inspection against Nielsen's 10 usability heuristics. Best for: catching broad usability issues across an interface. Speed: fast. Coverage: wide but shallow.
>
> **2. Cognitive Walkthrough**
> Task-based evaluation simulating a first-time user's thought process. Best for: evaluating learnability and task completion. Speed: moderate. Coverage: narrow but deep.
>
> **3. Expert Review**
> Comprehensive review combining heuristics, cognitive walkthrough, and domain expertise. Best for: thorough pre-launch evaluation. Speed: slower. Coverage: wide and deep.

Default to **Heuristic Evaluation** if the user does not specify.

Record as `$METHOD`.

### Step 2: Define Scope

Establish what is being evaluated.

**Prompt the user:**

> Please define the evaluation scope:
> - **Target:** What interface, page, flow, or component are we evaluating?
> - **User context:** Who are the primary users? What are their goals?
> - **Platform:** Web (desktop), web (mobile), native app, or responsive?
> - **Key tasks:** What are the 3-5 most critical user tasks to evaluate?

Record as `$SCOPE`.

If the method is **Cognitive Walkthrough**, also gather:
- The specific task sequence (step-by-step user actions)
- The expected user knowledge/experience level
- The success criteria for each step

### Step 3: Conduct Evaluation

#### Method A: Heuristic Evaluation

Evaluate the interface against each of **Nielsen's 10 Usability Heuristics**:

**H1. Visibility of System Status**
The system should always keep users informed about what is going on, through appropriate feedback within reasonable time.
- Is there feedback for every user action?
- Are loading states, progress indicators, and confirmations present?
- Does the user always know where they are in the system?
- Are state changes communicated clearly (saved, submitted, error)?

**H2. Match Between System and the Real World**
The system should speak the users' language, with words, phrases, and concepts familiar to the user.
- Is terminology user-friendly (not developer jargon)?
- Do icons match common mental models?
- Is information presented in a natural, logical order?
- Do metaphors and analogies make sense to the target audience?

**H3. User Control and Freedom**
Users often choose system functions by mistake and need a clearly marked "emergency exit."
- Can users undo/redo actions?
- Is there a clear way to cancel or go back?
- Can users easily dismiss dialogs and overlays?
- Are destructive actions reversible or confirmed?

**H4. Consistency and Standards**
Users should not have to wonder whether different words, situations, or actions mean the same thing.
- Is terminology consistent throughout?
- Do similar elements look and behave the same way?
- Does the design follow platform conventions?
- Are interaction patterns consistent (e.g., swipe, tap, click)?

**H5. Error Prevention**
Even better than good error messages is a careful design that prevents problems from occurring.
- Are dangerous actions gated by confirmation?
- Are form inputs validated before submission?
- Are constraints communicated upfront (character limits, required fields)?
- Does the design guide users away from error-prone paths?

**H6. Recognition Rather Than Recall**
Minimize the user's memory load by making objects, actions, and options visible.
- Are instructions visible or easily retrievable?
- Are recently used items accessible?
- Do form fields have labels (not just placeholders)?
- Is context preserved when navigating between screens?

**H7. Flexibility and Efficiency of Use**
Accelerators -- unseen by the novice user -- may speed up interaction for the expert user.
- Are keyboard shortcuts available for frequent actions?
- Can users customize or personalize their experience?
- Are there shortcuts for experienced users (bulk actions, quick filters)?
- Is the interface efficient for repeat/power users?

**H8. Aesthetic and Minimalist Design**
Dialogues should not contain information that is irrelevant or rarely needed.
- Is every element necessary and purposeful?
- Is visual noise minimized?
- Are calls to action clear and prominent?
- Is the visual hierarchy effective (most important things stand out)?

**H9. Help Users Recognize, Diagnose, and Recover from Errors**
Error messages should be expressed in plain language, precisely indicate the problem, and constructively suggest a solution.
- Are error messages human-readable (not error codes)?
- Do errors explain what went wrong AND how to fix it?
- Are inline validation errors specific and helpful?
- Do errors appear near the source of the problem?

**H10. Help and Documentation**
Even though it is better if the system can be used without documentation, it may be necessary to provide help.
- Is contextual help available where needed?
- Is documentation searchable?
- Are onboarding flows provided for complex features?
- Are tooltips or info icons used for non-obvious functionality?

#### Method B: Cognitive Walkthrough

For each step in the task sequence, answer these four questions:

1. **Will the user try to achieve the right effect?** Does the user's goal align with what the system expects at this step?
2. **Will the user notice that the correct action is available?** Is the needed control/link visible and recognizable?
3. **Will the user associate the correct action with the expected effect?** Does the label/icon clearly communicate what will happen?
4. **If the correct action is performed, will the user see that progress is being made?** Is there adequate feedback after the action?

Record a **pass/fail** for each question at each step, with notes on failures.

#### Method C: Expert Review

Combine both methods above, plus evaluate:

- **Information architecture:** Is content organized logically? Is navigation intuitive?
- **Accessibility:** WCAG 2.1 AA compliance, screen reader compatibility, keyboard navigation
- **Performance perception:** Do loading states and transitions feel responsive?
- **Emotional design:** Does the experience feel trustworthy, professional, and appropriate?
- **Edge cases:** Empty states, error states, first-time use, data extremes

### Step 4: Score Findings

Rate each finding using the **Nielsen Severity Rating Scale**:

| Rating | Severity | Description | Action |
|--------|----------|-------------|--------|
| **0** | Not a problem | Evaluator disagrees this is a usability issue | No action needed |
| **1** | Cosmetic | Does not affect usability unless time permits | Fix during polish phase |
| **2** | Minor | Small usability problem; low priority fix | Schedule for next iteration |
| **3** | Major | Important usability problem; high priority fix | Must fix before release |
| **4** | Catastrophic | Usability catastrophe; must be fixed before launch | Stop and fix immediately |

**Scoring criteria** -- severity is a combination of three factors:

- **Frequency:** How often does the problem occur? (rare, occasional, frequent)
- **Impact:** How difficult is it for users to overcome? (easy, moderate, hard)
- **Persistence:** Is it a one-time problem or does it recur? (one-time, recurring)

| | Easy to overcome | Moderate to overcome | Hard to overcome |
|---|---|---|---|
| **Rare + One-time** | Severity 1 | Severity 2 | Severity 3 |
| **Rare + Recurring** | Severity 2 | Severity 2 | Severity 3 |
| **Occasional + One-time** | Severity 1 | Severity 2 | Severity 3 |
| **Occasional + Recurring** | Severity 2 | Severity 3 | Severity 4 |
| **Frequent + One-time** | Severity 2 | Severity 3 | Severity 4 |
| **Frequent + Recurring** | Severity 3 | Severity 4 | Severity 4 |

### Step 5: Generate Report

Compile findings into a structured usability evaluation report.

**Report structure:**

```markdown
# Usability Evaluation Report

## Executive Summary
- Method used: [Heuristic / Cognitive Walkthrough / Expert Review]
- Scope: [What was evaluated]
- Date: [Evaluation date]
- Total findings: [Count]
- Severity breakdown: [X catastrophic, X major, X minor, X cosmetic]

## Severity Distribution Chart
| Severity | Count | Percentage |
|----------|-------|------------|
| 4 - Catastrophic | X | X% |
| 3 - Major | X | X% |
| 2 - Minor | X | X% |
| 1 - Cosmetic | X | X% |

## Findings

### Finding #1: [Short title]
- **Severity:** [0-4]
- **Heuristic violated:** [H1-H10, if applicable]
- **Location:** [Screen/component/flow]
- **Description:** [What the issue is]
- **Evidence:** [Why this is a problem, user impact]
- **Recommendation:** [Specific fix or improvement]
- **Effort estimate:** [Low / Medium / High]

### Finding #2: ...
[Repeat for each finding, ordered by severity descending]

## Prioritized Action Plan
1. [Highest severity items first]
2. [Group related fixes that can be addressed together]
3. [Quick wins -- low effort, high impact]

## Positive Findings
List things the design does well -- this provides balance and highlights patterns to preserve.

## Methodology Notes
Details about the evaluation approach, limitations, and assumptions.
```

## Delegation

1. **@ux-design-lead** receives the evaluation request, confirms scope, and selects the appropriate researcher.
2. **@ux-researcher** conducts the evaluation, scores findings, and produces the report.

## Quality Gates

Before delivering the report, verify:

- [ ] Every finding has a severity score with justification
- [ ] Every finding includes a specific, actionable recommendation
- [ ] Findings reference specific locations in the interface
- [ ] The report includes positive findings (not just problems)
- [ ] Severity distribution is reviewed for consistency (no inflation or deflation)
- [ ] Recommendations are feasible given the project's constraints
- [ ] The executive summary accurately reflects the findings

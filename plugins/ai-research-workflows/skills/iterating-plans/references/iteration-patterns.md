# Iterating Plans — Common Iteration Patterns

### Adding a phase

1. Read surrounding phases; research codebase patterns if needed.
2. Confirm: "I'll add a new Phase N for [topic], shifting current Phase N to
   Phase N+1. Tasks: [list]. OK?"
3. Use Edit to insert the phase; update phase numbering and cross-references.

### Updating success criteria

1. Read current criteria; determine Automated vs. Manual classification.
2. Confirm the addition (e.g., `curl` command → Automated, format check → Manual).
3. Use Edit to add to the appropriate section.

### Adjusting scope

1. Find all references to the feature being removed.
2. Confirm: "I'll remove [feature] tasks from [phase] and add it to 'What
   We're NOT Doing'. Does that cover it?"
3. Use Edit to remove tasks, update scope section, and remove related criteria.

### Incorporating experiment results

1. Read the experiment report (`experiment-*.md`) to understand the chosen approach.
2. Identify where the old approach is referenced.
3. Confirm: "I'll update Implementation Approach and Phase N tasks to use
   [approach B]. This affects [files]. Correct?"
4. Use Edit to update approach section and affected tasks; add experiment report
   to References.

### Splitting a complex phase

1. Read the phase; identify a logical split point.
2. Confirm: "I'll split Phase N into Phase N (tasks 1-X: [objective A]) and
   Phase N+1 (tasks X+1-Y: [objective B]). Each phase will be independently
   testable. Sound good?"
3. Use Edit to split; update subsequent phase numbering.

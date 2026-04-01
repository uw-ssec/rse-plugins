---
description: Update an existing implementation plan based on feedback
user-invocable: true
---

# Initial Response

When this command is invoked, parse the input to identify the plan file path and requested changes.

**If NO plan file provided** (e.g., `/iterate-plan`):
- Respond with:
  ```
  Which plan would you like to update?

  You can list recent plans with:
  ls -lt .agents/plan-*.md | head -5

  Please provide the plan file path and describe what changes to make.
  ```
- WAIT for user response

**If plan file provided but NO feedback** (e.g., `/iterate-plan .agents/plan-auth.md`):
- Read the plan file COMPLETELY
- Respond with:
  ```
  I've read the plan at `.agents/plan-auth.md`.

  What changes would you like to make? For example:
  - Add a new phase
  - Update success criteria
  - Adjust scope (add or remove features)
  - Split a phase into smaller steps
  - Update implementation approach based on new information
  - Incorporate experiment results

  Please describe what you'd like to change.
  ```
- WAIT for user response

**If BOTH plan file AND feedback provided** (e.g., `/iterate-plan .agents/plan-auth.md add a phase for database migration`):
- Proceed immediately to the process steps

# Iteration Philosophy

Plans evolve as understanding deepens or requirements change. Good iteration:

- **Surgical** — Make precise edits, not wholesale rewrites
- **Preserves value** — Keep good content that doesn't need changing
- **Maintains consistency** — New content follows existing patterns
- **Verifies assumptions** — Research code if changes require new technical understanding
- **Confirms understanding** — Check with user before making changes

Bad iteration:
- Rewriting sections that didn't need changes
- Breaking consistency between phases
- Making changes without understanding implications
- Adding content without verifying technical feasibility

# Process Steps

## Step 1: Read and Understand Current Plan

### Read the Existing Plan Completely

- Read the entire plan completely (avoid partial reads)
- Don't make changes based on memory — always read the current state

### Understand the Current Structure

Identify:
- How many phases exist
- What the current scope is
- What success criteria are defined
- What the implementation approach is
- What references are included

### Understand the Requested Changes

Parse what the user is asking for:
- Adding new phases or tasks
- Removing or reducing scope
- Updating success criteria
- Changing technical approach
- Incorporating new information
- Splitting complex phases
- Reordering phases

### Identify if Changes Require Codebase Research

Determine if you need to investigate code:
- **Research needed:** Changes introduce new technical requirements or alter approach
- **No research needed:** Changes are structural (reordering, splitting), clarifications, or minor scope adjustments

## Step 2: Research If Needed

**ONLY if changes require new technical understanding:**

### Conduct Research Tasks

Investigate as needed:
- "Find how [new requirement] is currently handled in the codebase"
- "Locate examples of [pattern] that the new phase should follow"
- "Analyze dependencies for [new component]"
- "Search for tests covering [related area]"

Launch multiple research tasks in parallel when possible.

### Wait for ALL Research to Complete

Do NOT proceed until all research returns results.

### Synthesize Research

Understand how findings affect the plan changes:
- What files need to be added to tasks
- What patterns should be referenced
- What success criteria should be added
- What risks or considerations should be noted

## Step 3: Present Understanding and Approach

**Before making any changes**, confirm your understanding:

```
I've read the plan and understand you want to [summary of requested changes].

Based on the current plan structure:
- Current phases: [list]
- Scope: [summary]

Proposed changes:
- [Change 1 description]
- [Change 2 description]

This will affect:
- [Section affected 1]
- [Section affected 2]

[If research was done]
Research findings:
- [Key finding that informs changes]

Does this match what you're looking for?
```

**Get user confirmation** before proceeding.

**If user says no:** Clarify the misunderstanding and adjust your approach.

**If user says yes:** Proceed to make changes.

## Step 4: Update the Plan

### Make Focused, Precise Edits

Make surgical changes to the plan:

**Good edits:**
- Add a new phase section between existing phases
- Update specific success criteria items
- Modify task descriptions within a phase
- Add file references to existing tasks

**Bad edits:**
- Replacing the entire plan
- Rewriting sections that don't need changes
- Changing formatting or structure unnecessarily

### Maintain Existing Structure

Unless explicitly changing structure:
- Keep the same phase format
- Follow the same task description pattern
- Use the same reference style
- Maintain the same level of detail

### Keep All File:Line References Accurate

When adding new tasks or phases:
- Include specific file paths and line numbers
- Research actual code locations if needed
- Follow the pattern: `path/to/file.ext:123-145`

### Update Success Criteria If Needed

When scope changes:
- Add new automated verification checks
- Add new manual verification steps
- Remove criteria that no longer apply
- **Maintain the split** between Automated and Manual verification

### Ensure Consistency

When making changes, ensure:
- **New phases follow existing pattern** — Same structure, same level of detail
- **Scope changes update "What We're NOT Doing"** — If adding features, check if scope boundary changed
- **Approach changes update "Implementation Approach"** — Technical strategy section should reflect new approach
- **New tasks follow codebase patterns** — Reference actual examples from the codebase

### Preserve Automated vs Manual Success Criteria Distinction

Keep separation clear:
```markdown
### Automated Verification
[Commands and checks that can run without human intervention]

### Manual Verification
[Steps requiring human testing and judgment]
```

## Step 5: Review

Present the changes made:

```
# Plan Updated

I've made the following changes to `.agents/plan-[slug].md`:

## Changes Made:
- [Change 1 with specific section]
- [Change 2 with specific section]
- [Change 3 with specific section]

## Impact:
- [How changes affect implementation]
- [New success criteria added/removed]

The plan now includes:
- [Summary of updated plan]

Would you like any further adjustments?
```

### Handle Further Iteration

If user wants more changes:
- Re-read the plan to get current state
- Apply the same process for additional changes
- Continue until user is satisfied

# Important Guidelines

## Be Skeptical

- **Don't blindly accept change requests that seem problematic**
  - "Adding that phase would conflict with Phase 2 because..."
  - "That scope change seems risky because..."

- **Question vague feedback**
  - "When you say 'make it more robust', do you mean...?"
  - "Can you clarify what 'better error handling' looks like?"

- **Verify technical feasibility with code research**
  - Don't add tasks without knowing they're possible
  - Research actual code to ensure changes are grounded in reality

## Be Surgical

- **Make precise edits, not wholesale rewrites**
  - Edit specific sections that need changes
  - Leave unchanged sections alone

- **Preserve good content that doesn't need changing**
  - Don't reformat or rewrite for style if content is good
  - Focus changes on what actually needs to be different

## Be Thorough

- **Read the entire existing plan before making changes**
  - You need full context to maintain consistency
  - Partial reads lead to broken references and inconsistencies

- **Research code patterns if changes require new technical understanding**
  - Don't guess at file paths or patterns
  - Spawn Explore sub-agents to find actual examples

## Be Interactive

- **Confirm understanding before making changes**
  - Show what you plan to change
  - Get user buy-in before editing

- **Show what you plan to change before doing it**
  - Describe the edits you'll make
  - Explain the impact

## No Open Questions

This is a BLOCKING REQUIREMENT:

- **If the requested change raises questions, ASK**
  - Don't guess what the user means
  - Don't make assumptions about requirements

- **Research or get clarification immediately**
  - Conduct research for technical questions
  - Ask the user for requirement questions

- **DO NOT update the plan with unresolved questions**
  - Plans must be complete specifications
  - Every decision must be made

# Common Iteration Patterns

## Adding a Phase

**User request:** "Add a phase for database migration before Phase 3"

**Your approach:**
1. Read the plan to understand Phases 2 and 3
2. Research database migration patterns in the codebase
3. Confirm: "I'll add a new Phase 3 for DB migration, and shift the current Phase 3 to Phase 4. This phase will include [tasks]. Does that work?"
4. Get confirmation
5. Use Edit to insert the new phase
6. Update phase numbering in subsequent phases
7. Update any cross-references

## Updating Success Criteria

**User request:** "Add verification for the new API endpoint"

**Your approach:**
1. Read the current success criteria
2. Determine if it's automated or manual verification
3. Confirm: "I'll add `curl http://localhost:8000/api/new-endpoint` to Automated Verification and checking response format to Manual Verification. Correct?"
4. Get confirmation
5. Use Edit to add to the appropriate section

## Adjusting Scope

**User request:** "Let's not implement the email notifications yet"

**Your approach:**
1. Read the plan to find all references to email notifications
2. Confirm: "I'll remove the email notification tasks from Phase 4 and add 'Email notifications' to the 'What We're NOT Doing' section. Does that cover it?"
3. Get confirmation
4. Use Edit to remove tasks and update scope section
5. Update success criteria to remove email-related checks

## Incorporating Experiment Results

**User request:** "Based on the experiment, let's use approach B instead of approach A"

**Your approach:**
1. Read the experiment report to understand approach B
2. Read the plan to identify where approach A is referenced
3. Confirm: "I'll update the Implementation Approach section to use approach B (JWT tokens) instead of approach A (sessions), and update Phase 2 tasks to implement JWT validation. This affects [files]. Correct?"
4. Get confirmation
5. Use Edit to update approach section and affected tasks
6. Add experiment report to References section

## Splitting a Complex Phase

**User request:** "Phase 3 is too big, split it into two phases"

**Your approach:**
1. Read Phase 3 to understand its tasks
2. Identify a logical split point
3. Confirm: "I'll split Phase 3 into: Phase 3 (tasks 1-3: setup), Phase 4 (tasks 4-6: implementation). This makes each phase independently testable. Sound good?"
4. Get confirmation
5. Use Edit to split the phase
6. Update phase numbering for subsequent phases

# Cross-Reference with Other Workflow Steps

**After iteration:**
- The updated plan is ready for `/implement`
- Can be iterated again if requirements change further
- Can be validated after implementation with `/validate`

**Iteration can incorporate:**
- Findings from `/research` (add file references)
- Results from `/experiment` (update approach)
- Feedback from `/validate` (adjust criteria)

# Quality Checklist

Before completing iteration, verify:

- [ ] Read the entire existing plan before making changes
- [ ] Ran research tasks if technical understanding was needed
- [ ] Confirmed understanding with user before editing
- [ ] Made precise edits without unnecessary rewrites
- [ ] Maintained consistency with existing structure
- [ ] Updated all affected sections (approach, criteria, references)
- [ ] Preserved automated vs manual verification split
- [ ] All file:line references are accurate
- [ ] No open questions remain in the updated plan
- [ ] User is satisfied with changes

Remember: Good iteration improves the plan while preserving its value. Bad iteration creates churn and inconsistency.

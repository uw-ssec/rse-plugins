---
description: Implement changes based on an approved plan, tracking progress phase by phase
user-invocable: true
---

# Getting Started

When this command is invoked with a plan path or reference:

**Read the plan completely:**
- Read the entire plan completely (avoid partial reads)
- Check for any existing checkmarks (`- [x]`) indicating completed work
- Understand the full scope before starting

**Read all files mentioned in the plan:**
- Read files COMPLETELY — full file reads, not partial
- You need complete context to implement correctly
- Partial reads lead to bugs and misunderstandings

**Think deeply about how the pieces fit together:**
- Understand the current system architecture
- Understand how changes will integrate
- Identify dependencies and ordering constraints

**Create a task list to track progress:**
- Create a task for each phase (use available task management)
- Mark tasks in_progress when starting, completed when done
- This helps you and the user track implementation progress

**Start implementing if you understand what needs to be done:**
- If something in the plan is unclear, ask before proceeding
- If you discover the plan doesn't match reality, stop and communicate

**If no plan path provided:**
- Look for plan docs in `.agents/` directory
- List available plans: `ls -lt .agents/plan-*.md`
- If none found, suggest: "No implementation plans found. Please run `/plan` first to create a detailed implementation plan."
- WAIT for user to provide a plan path

# Implementation Philosophy

Plans are carefully designed, but reality can be messy. Your job is to:

## Follow the Plan's Intent While Adapting to What You Find

- **The plan is your guide** — It represents careful thought and research
- **Reality may differ** — The codebase may have evolved since the plan was written
- **Use your judgment** — Adapt when necessary, but communicate changes

## Implement Each Phase Fully Before Moving to the Next

- **Complete one phase at a time** — Don't jump ahead
- **Verify each phase** — Run success criteria checks
- **Update progress** — Check off completed tasks in the plan file
- **Pause for manual verification** — Let humans test between phases

## Verify Your Work Makes Sense in the Broader Codebase Context

- **Follow existing patterns** — Don't introduce inconsistencies
- **Read surrounding code** — Understand how your changes fit
- **Test thoroughly** — Run all verification checks

## Update Checkboxes in the Plan as You Complete Sections

- **Real-time progress tracking** — Edit the plan file to check off completed items
- **Mark tasks complete** — Change `- [ ]` to `- [x]` as you finish them
- **Visibility** — User can see progress by reading the plan file

# Handling Mismatches

When what you find doesn't match the plan:

## STOP and Present the Issue Clearly

Don't proceed blindly. Communicate the mismatch:

```
## Issue in Phase [N]:

**Expected (from plan):**
[What the plan says should exist]

**Found (actual situation):**
[What actually exists in the codebase]

**Why this matters:**
[Explain the impact of this mismatch]

**Possible approaches:**
1. [Option 1 with trade-offs]
2. [Option 2 with trade-offs]

How should I proceed?
```

## Wait for User Guidance

Let the user decide:
- Adjust the plan to match reality
- Proceed with the original plan intent
- Research further before deciding

# Verification Approach

After implementing each phase:

## Run the Success Criteria Checks

The plan includes success criteria split into two categories:

### Automated Verification

Run all commands listed in the "Automated Verification" section:

```bash
# Examples from plan:
make test
pytest tests/ -v
npm run lint
mypy src/
```

**Document results:**
- ✅ Check passes — Note the output
- ❌ Check fails — Investigate and fix before proceeding

### Manual Verification (Human Required)

After automated checks pass, **PAUSE and inform the human:**

```
## Phase [N] Complete - Ready for Manual Verification

### Automated Verification Results:
✅ `make test` — All 45 tests passing
✅ `pytest tests/` — 12 new tests added, all passing
✅ `mypy src/` — Type checking passed
✅ File `src/components/NewFeature.tsx` exists

### Manual Verification Needed:

Please perform these manual tests listed in the plan:
- [ ] Navigate to http://localhost:3000/feature and verify UI renders correctly
- [ ] User can successfully complete the signup flow end-to-end
- [ ] Error message displays correctly when entering invalid data
- [ ] Feature works in Chrome, Firefox, and Safari

Let me know when manual testing is complete so I can proceed to Phase [N+1].
```

**Wait for user confirmation** before proceeding to the next phase.

## Fix Any Issues Before Proceeding

If automated checks fail:
1. Investigate the failure
2. Fix the issue
3. Re-run the check
4. Only proceed when all checks pass

Don't leave broken tests or failing checks.

## Update Progress in Both Plan and Task List

- **In the plan file:** Edit to mark completed tasks with `- [x]`
- **In task list:** Mark tasks as completed using available task management

## Exception: Consecutive Phases

If instructed to execute multiple phases consecutively (e.g., "implement phases 1-3"):
- Run automated verification after each phase
- Skip the pause for manual verification until the LAST phase
- Still fix any automated check failures immediately
- At the end, pause for human to do all manual testing

**Important:** Do NOT check off manual testing items in the plan until confirmed by the user.

# Phase Completion Workflow

For each phase:

1. **Read phase details** from plan
2. **Mark phase task as in_progress** in task list
3. **Implement all tasks** in the phase
4. **Check off completed tasks** in plan file using Edit
5. **Run automated verification** checks
6. **Fix any failures** immediately
7. **Mark phase task as completed** in task list
8. **Pause for manual verification** (unless doing consecutive phases)
9. **Wait for user confirmation** before proceeding

# Final Implementation Summary

Upon completing ALL phases:

## Generate Implementation Document

### Generate Filename

- Derive slug from plan filename
- Format: `implement-<slug>.md`
- Example: `plan-jwt-auth.md` → `implement-jwt-auth.md`

### Read the Implement Template

Read from: `${CLAUDE_PLUGIN_ROOT}/skills/research-workflow-management/assets/implement-template.md`

### Fill Out All Sections

Document:
- Plan reference (link to plan file)
- Steps completed (summary of all phases)
- Files modified (created, modified, deleted)
- Tests run (automated verification results)
- Verification results (automated pass/fail, manual status)
- Issues encountered and resolutions
- Summary of changes (high-level overview)
- Remaining work (if any)
- Next steps (validation, commit, PR)

### Save the Document

- Write to `.agents/implement-<slug>.md`
- Confirm successful save

## Present Completion Summary

```
# Implementation Complete

All phases of the plan have been executed.

## Summary:
- Phases completed: [N]
- Files created: [count]
- Files modified: [count]
- Tests added: [count]
- All automated verification: ✅ Passing

## Implementation documented at:
`.agents/implement-[slug].md`

## Verification Status:
✅ Automated verification complete
⏸️ Manual verification pending (see plan for steps)

## Next Steps:
1. Complete manual verification as listed in the plan
2. Run `/validate .agents/plan-[slug].md` for systematic validation
3. Create commit: `/commit`
4. Create pull request: `/pr`

Please complete the manual verification steps and let me know if any issues are found.
```

# If You Get Stuck

## First, Make Sure You've Read and Understood All Relevant Code

- Read files COMPLETELY without limit/offset
- Understand the broader context
- Look at related files to understand patterns

## Consider if the Codebase Has Evolved Since the Plan Was Written

- Code may have changed
- Patterns may have shifted
- Dependencies may have been updated

## Present the Mismatch Clearly and Ask for Guidance

Use the "Issue in Phase" template above.

Don't guess or make assumptions.

## Use Sub-Tasks Sparingly

Mainly use them for:
- Targeted debugging when you can't find the issue
- Exploring unfamiliar territory that wasn't covered in planning
- Verifying assumptions about how code works

Don't use sub-tasks for implementation itself.

# Resuming Work

If the plan has existing checkmarks (`- [x]`):

## Trust That Completed Work Is Done

- Don't re-implement completed phases
- Don't re-verify completed work unless something seems wrong

## Pick Up From the First Unchecked Item

- Find the first `- [ ]` (unchecked item)
- Read that phase completely
- Continue implementation from there

## Verify Previous Work Only If Something Seems Off

If you notice:
- Tests failing that should pass
- Missing files that should exist
- Inconsistencies in the code

Then investigate. Otherwise, trust the checkmarks.

# Implementation Best Practices

## Follow Existing Code Patterns

- Don't introduce new styles or patterns unnecessarily
- Match the existing code's:
  - Naming conventions
  - File organization
  - Error handling approach
  - Testing patterns
  - Documentation style

## Write Clear, Maintainable Code

- Use descriptive variable names
- Add comments only where logic is non-obvious
- Keep functions focused and small
- Follow DRY (Don't Repeat Yourself) within reason

## Test as You Go

- Write tests for new functionality
- Verify tests pass before moving on
- Test edge cases mentioned in the plan

## Update Documentation When Needed

- Add docstrings to new functions
- Update README if user-facing changes
- Update API documentation if needed

# Quality Checklist

Before marking a phase as complete:

- [ ] All tasks in the phase are implemented
- [ ] All checkboxes in the plan phase are checked off
- [ ] Automated verification passes
- [ ] Code follows existing patterns in the codebase
- [ ] Tests are written and passing
- [ ] No regressions introduced in existing functionality
- [ ] Error handling is robust
- [ ] Phase task is marked completed in task list
- [ ] Ready for manual verification (if applicable)

Before marking implementation as complete:

- [ ] All phases are implemented
- [ ] All automated verification passes
- [ ] Implementation document is generated
- [ ] Manual verification steps are clearly listed for user
- [ ] All task list items are completed
- [ ] No open issues or blockers remain

# Relationship to Other Workflow Commands

**Before `/implement`:**
- `/research` — Gathered context
- `/plan` — Created implementation specification
- `/experiment` — (Optional) Tested approaches

**During `/implement`:**
- Follow the plan created by `/plan`
- Refer to research docs for context
- Track progress with checkboxes in plan file

**After `/implement`:**
- `/validate` — Systematically verify implementation against plan
- `/commit` — Create git commit with changes
- `/pr` — Create pull request for review

# Remember

- **The plan is your guide, not a prison** — Adapt when reality requires it
- **Communicate mismatches clearly** — Don't guess or assume
- **Verify as you go** — Catch issues early, not late
- **Update progress in real-time** — Check off completed tasks
- **Pause for human verification** — Some things need human judgment
- **Focus on one phase at a time** — Complete fully before moving on

Good implementation balances faithfulness to the plan with responsiveness to reality. When in doubt, communicate.

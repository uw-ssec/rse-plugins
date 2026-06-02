---
name: implementing-plans
description: >-
  Use when an approved software implementation plan exists (.agents/plan-*.md)
  and you are ready to write code, run tests, and track progress phase-by-phase.
  Reads the full plan, implements each phase completely, runs automated
  verification (tests, linters, type-checks) after each phase, pauses for human
  manual verification, updates plan checkboxes in real-time, and writes a final
  implementation-summary document to .agents/ when all phases are done. Triggers:
  implement the plan, execute the plan, start building, run the plan, build the
  feature, code the solution, implement the architecture.
---

# Implementing Plans

Execute a phased implementation plan faithfully, adapting to reality while
tracking progress in real-time and verifying each phase before advancing.

## Interaction mode

Choose a mode before acting. Full protocol: `${CLAUDE_PLUGIN_ROOT}/skills/using-research-workflows/references/interaction-modes.md`.

1. **Explicit override wins** — "brainstorm / walk me through / help me think" → Collaborative; "just do it / don't ask / go ahead" → Direct.
2. **Else infer** — vague/exploratory phrasing, or required inputs missing → Collaborative; a specific directive with enough context → Direct.
3. **Else default** — this skill leans **Direct**.
4. **Hard stops, regardless of mode** — destructive, irreversible, or outward-facing actions always get a confirmation first.

## Starting the skill

If no plan path is given, list `ls -lt .agents/plan-*.md` and, in Collaborative
mode, ask which to implement; otherwise proceed (Direct).

When a plan is identified:

- Read the **entire plan** completely (avoid partial reads).
- Check for existing checkmarks (`- [x]`) indicating completed work.
- Read **all files mentioned in the plan** completely — partial reads cause bugs.
- Understand the full scope, architecture, and dependency ordering before starting.
- Create a task for each phase to track progress.

## Implementation rules

- Implement one phase fully before moving to the next; do not jump ahead.
- After each phase: run automated verification, fix failures, then pause for
  human manual verification before continuing.
- Follow existing code patterns — do not introduce inconsistencies.
- Edit the plan file in real-time: change `- [ ]` to `- [x]` as tasks
  complete. The user can track progress by reading the plan.
- Adapt to reality when the codebase differs from the plan, but communicate
  every deviation before proceeding.

## Handling mismatches

When what you find does not match the plan, **stop** and present the issue:

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

Wait for user guidance before continuing. Let the user decide whether to adjust
the plan, proceed with original intent, or research further.

## Verification after each phase

### Automated verification

Run all commands listed in the plan's "Automated Verification" section. Document
results:

- Check passes — note the output.
- Check fails — investigate and fix before proceeding.

### Manual verification (human required)

After automated checks pass, **pause** and inform the human:

```
## Phase [N] Complete - Ready for Manual Verification

### Automated Verification Results:
✅ `make test` — All 45 tests passing
✅ `pytest tests/` — 12 new tests added, all passing
✅ `mypy src/` — Type checking passed

### Manual Verification Needed:

Please perform these manual tests listed in the plan:
- [ ] [Manual step 1]
- [ ] [Manual step 2]

Let me know when manual testing is complete so I can proceed to Phase [N+1].
```

Wait for user confirmation before proceeding to the next phase.

### Exception: consecutive phases

If instructed to execute multiple phases consecutively (e.g., "implement phases
1-3"):

- Run automated verification after each phase.
- Skip the manual-verification pause until the **last** phase.
- Still fix any automated check failures immediately.
- At the end, pause for human to do all manual testing.

Do NOT check off manual testing items in the plan until confirmed by the user.

## Phase completion workflow

For each phase:

1. Read phase details from plan.
2. Mark phase task as in_progress in task list.
3. Implement all tasks in the phase.
4. Check off completed tasks in the plan file using Edit.
5. Run automated verification checks.
6. Fix any failures immediately.
7. Mark phase task as completed in task list.
8. Pause for manual verification (unless doing consecutive phases).
9. Wait for user confirmation before proceeding.

## Resuming work

If the plan has existing checkmarks (`- [x]`):

- Trust that completed work is done — do not re-implement completed phases.
- Pick up from the first unchecked item (`- [ ]`).
- Re-verify previous work only if tests are failing, files are missing, or you
  notice inconsistencies.

## If you get stuck

1. Make sure you have read all relevant files completely (no partial reads).
2. Consider whether the codebase has evolved since the plan was written.
3. Present the mismatch clearly using the "Issue in Phase" template above.
4. Do not guess or make assumptions.
5. Use sub-tasks sparingly — mainly for targeted debugging or exploring
   unfamiliar territory, never for implementation itself.

## Final implementation summary

Upon completing all phases:

**Generate filename** — derive slug from plan filename:
`plan-jwt-auth.md` → `implement-jwt-auth.md`.

**Read the template:**
`${CLAUDE_PLUGIN_ROOT}/skills/implementing-plans/assets/implement-template.md`

**Fill all sections:** plan reference, phases completed, files modified, tests
run, verification results (automated and manual), issues encountered, key
changes summary, remaining work, next steps.

**Save to** `.agents/implement-<slug>.md` and confirm.

**Present completion summary:**

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
2. Run the validating-implementations skill for systematic validation
3. Create commit
4. Create pull request
```

## Cross-references

Follows the `planning-implementations` skill; verify with
`validating-implementations`. For research code, capture provenance with
`ensuring-reproducibility` and robustness with `hardening-research-code`.

## Quality checklist

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
- [ ] Implementation document generated at `.agents/implement-<slug>.md`
- [ ] Manual verification steps clearly listed for user
- [ ] All task list items completed
- [ ] No open issues or blockers remain

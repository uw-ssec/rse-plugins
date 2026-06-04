---
name: implementing-plans
description: >-
  Use when an approved implementation plan (a .agents/plan-*.md file) exists
  and the next step is writing the code. Triggers: implement the plan, execute
  the plan, start building, run the plan.
---

# Implementing Plans

Execute a phased implementation plan faithfully, adapting to reality while
tracking progress in real-time and verifying each phase before advancing.

## Interaction mode

This skill leans **Direct** by default. For the full Collaborative-vs-Direct protocol and override rules, see the Interaction Modes reference in the `ai-research-workflows:using-research-workflows` skill.

## Checklist

Work through these in order and track them as tasks. Do not skip the review gates (steps 2, 5, and 7):

1. **Load the plan** — read the plan and every file it references, completely
2. **Review the plan critically** — raise concerns and confirm the working branch *before* writing code
3. **Implement one phase** — follow the plan, adapt to reality, record every deviation
4. **Verify the phase** — run automated checks; fix failures before advancing
5. **Pause for manual verification** — wait for human confirmation before the next phase (except consecutive phases)
6. **Repeat steps 3–5** until every phase is done
7. **Confirm completion** — all automated verification passes; nothing left unaccounted for on the branch
8. **Summarize & hand off** — write `.agents/implement-<slug>.md`; route to `ai-research-workflows:validating-implementations`

## Starting the skill

If no plan path is given, list `ls -lt .agents/plan-*.md` and, in Collaborative
mode, ask which to implement; otherwise proceed (Direct).

When a plan is identified:

- Read the **entire plan** completely (avoid partial reads).
- Check for existing checkmarks (`- [x]`) indicating completed work.
- Read **all files mentioned in the plan** completely — partial reads cause bugs.
- Understand the full scope, architecture, and dependency ordering before starting.
- Create a task for each phase to track progress.

## Review the plan before building

Before writing any code, review the plan critically — do not treat it as
infallible:

- **Sanity-check the approach.** Identify questions, gaps, or concerns about the
  plan's design, phase ordering, or success criteria. If anything looks wrong or
  unclear, raise it with the user before starting — do not silently "fix" the
  plan by improvising.
- **Confirm the plan's assumptions still hold.** Research code often depends on
  data availability, specific dependency versions, random seeds, or a particular
  environment. Verify these are in place; if a prerequisite is missing, surface
  it now rather than failing mid-phase.
- **Confirm the working branch.** Never start implementation on `main`/`master`
  without explicit user consent — work on a feature branch. This is a hard stop
  regardless of interaction mode.

If the plan is sound and the branch is set, proceed. If not, stop and resolve
the concerns first.

## Implementation rules

- Implement one phase fully before moving to the next; do not jump ahead.
- After each phase: run automated verification, fix failures, then pause for
  human manual verification before continuing.
- Follow existing code patterns — do not introduce inconsistencies.
- Edit the plan file in real-time: change `- [ ]` to `- [x]` as tasks
  complete. The user can track progress by reading the plan.
- Adapt to reality when the codebase differs from the plan, but communicate
  every deviation before proceeding.
- When a phase produces a result, figure, metric, or trained artifact, capture
  its provenance — environment, data version, seeds, exact commands — with
  `ai-research-workflows:ensuring-reproducibility` so the result can be reproduced.

## Handling mismatches

When what you find does not match the plan, **stop** and present the issue using
the mismatch report template in
`references/templates.md`.

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

## Resuming work

If the plan has existing checkmarks (`- [x]`):

- Trust that completed work is done — do not re-implement completed phases.
- Pick up from the first unchecked item (`- [ ]`).
- Re-verify previous work only if tests are failing, files are missing, or you
  notice inconsistencies.

## If you get stuck

1. Make sure you have read all relevant files completely (no partial reads).
2. Consider whether the codebase has evolved since the plan was written.
3. Present the mismatch using the "Issue in Phase" template in `references/templates.md`.
4. Do not guess or make assumptions.
5. Use sub-tasks sparingly — mainly for targeted debugging or exploring
   unfamiliar territory, never for implementation itself.

## Final implementation summary

Upon completing all phases, first confirm the work is genuinely done: every
phase's automated verification passes, no checklist item was silently skipped,
and you are not leaving changes on `main`/`master`. Then:

**Generate filename** — derive slug from plan filename:
`plan-jwt-auth.md` → `implement-jwt-auth.md`.

**Read the template:**
`assets/implement-template.md`

**Fill all sections:** plan reference, phases completed, files modified, tests
run, verification results (automated and manual), issues encountered, key
changes summary, remaining work, next steps.

**Save to** `.agents/implement-<slug>.md` and confirm.

**Present completion summary** using the implementation completion summary
template in
`references/templates.md`.

## Common Mistakes

- **Diving into code without reviewing the plan** — read and critically review
  the whole plan first; raise design or assumption concerns, and confirm you are
  on a feature branch (not `main`/`master`), before writing any code.
- **Implementing multiple phases before verifying** — always run automated
  checks and pause for manual verification after each phase before advancing.
- **Not pausing for manual verification** — automated checks passing is not
  sufficient; stop and explicitly request human confirmation of manual steps.
- **Checking off manual items the user has not confirmed** — do not mark manual
  verification tasks `[x]` until the user reports them done.
- **Plowing past a plan/reality mismatch** — when the codebase differs from the
  plan, stop and present the mismatch report; never silently adapt and continue.
- **Partial file reads causing bugs** — always read all files mentioned in the
  plan completely before starting implementation.

## Cross-references

Follows the `ai-research-workflows:planning-implementations` skill; verify with
`ai-research-workflows:validating-implementations`. For research code, capture provenance with
`ai-research-workflows:ensuring-reproducibility` and robustness with `ai-research-workflows:hardening-research-code`.

## Quality checklist

Before marking a phase as complete:

- [ ] All tasks in the phase are implemented
- [ ] All checkboxes in the plan phase are checked off
- [ ] Automated verification passes
- [ ] Code follows existing patterns in the codebase
- [ ] Tests are written and passing
- [ ] No regressions introduced in existing functionality
- [ ] Error handling is robust
- [ ] Phase is marked done in the task list
- [ ] Ready for manual verification (if applicable)

Before marking implementation as complete:

- [ ] Plan reviewed critically and working branch confirmed before building
- [ ] All phases are implemented
- [ ] All automated verification passes
- [ ] Implementation document generated at `.agents/implement-<slug>.md`
- [ ] Manual verification steps clearly listed for user
- [ ] All task-list items are done
- [ ] No open issues or blockers remain

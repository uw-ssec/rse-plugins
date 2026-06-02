---
name: validating-implementations
description: >-
  Use when an implementation is (claimed) complete and must be verified against
  its plan's success criteria — run automated checks, review code vs. spec, list
  manual tests, and produce an inline validation report. Triggers: validate the
  implementation, verify it matches the plan, is the implementation correct,
  check before PR.
---

# Validating Implementations

Systematically verify that a completed implementation satisfies every success
criterion in its plan, producing an inline validation report.

## Interaction mode

Choose a mode before acting. Full protocol: `${CLAUDE_PLUGIN_ROOT}/skills/using-research-workflows/references/interaction-modes.md`.

1. **Explicit override wins** — "brainstorm / walk me through / help me think" → Collaborative; "just do it / don't ask / go ahead" → Direct.
2. **Else infer** — vague/exploratory phrasing, or required inputs missing → Collaborative; a specific directive with enough context → Direct.
3. **Else default** — this skill leans **Direct**.
4. **Hard stops, regardless of mode** — destructive, irreversible, or outward-facing actions always get a confirmation first.

## Starting the skill

**If a plan path is provided**, read it completely — this is the specification
to validate against.

**If no plan path is given**, search `.agents/{plan,implement}-*.md`. If
multiple match, ask which to validate (Collaborative); if exactly one, proceed
(Direct). If none found, explain that validation requires a plan.

## Determine session context

**Existing session (implementation done in this conversation):**
- You have context about what was implemented; review recent conversation.
- You know which files were modified.

**Fresh session (reviewing past work):**
- No memory of implementation decisions; reconstruct from git and artifacts.
- Focus on observable facts: does the code match the plan, do tests pass, are
  success criteria met?
- Don't speculate about intent; note deviations without judging them.

## Gather implementation evidence

Before validating, understand what was actually done.

Check recent commits:

```bash
git log --oneline -n 10
git diff HEAD~3..HEAD --stat
```

Run tests to establish baseline:

```bash
make test
# or: pytest tests/ -v
# or: npm test
```

## Validation process

### Step 1: Read the plan completely

Read the entire plan (avoid partial reads). For each phase identify:

- Which files should be modified
- Success criteria that must pass
- Key functionality that should exist
- Tests that should be added

### Step 2: Investigate in parallel

Verify code, schema, and test coverage concurrently when possible:

- **Database/schema changes** — confirm migrations match plan specifications
  (tables, columns, indices).
- **Code changes** — confirm implementation follows patterns and matches the
  plan's design.
- **Test coverage** — find tests added for the feature; verify they cover the
  scenarios listed in the plan's Testing Strategy section.

Wait for ALL verification to complete before synthesizing.

### Step 3: Systematic per-phase validation

For each phase in the plan:

**Check completion status** — `- [x]` = claimed complete; `- [ ]` = incomplete.

**Verify actual code matches claimed completion** — don't trust checkmarks.
Read the code: are the files modified as described? Does the implementation
match the specification?

**Run automated verification** — execute EACH command from the plan's
"Automated Verification" section:

```bash
make test
pytest tests/ -v
npm run lint
mypy src/
```

Document results per check:

```markdown
- ✅ `make test` — All 45 tests passing (expected 45)
- ❌ `pytest tests/test_new_feature.py` — 2 tests failing (expected 0)
- ✅ `mypy src/` — Type checking passed
```

**If a check fails:**

1. Read the error output.
2. Identify the failing code.
3. Determine whether it is an implementation bug, a test bug, a plan mismatch,
   or an environmental issue.
4. Document the finding with root cause, location, and recommendation.

**Assess manual criteria** — for items in the plan's "Manual Verification"
section, list what needs human testing with clear, actionable steps. If in the
same session and the user already confirmed, note that; otherwise assume manual
testing is still needed.

## Validation report

Output the report inline in the conversation (no template file is used for
this skill).

### Implementation status per phase

```markdown
## Implementation Status

### Phase 1: [Name]
**Status:** ✅ Fully implemented | ⚠️ Partially implemented | ❌ Not started

**Details:**
- [Task 1]: ✅ Complete
- [Task 2]: ✅ Complete
- [Task 3]: ⚠️ Partially complete (details…)

### Phase 2: [Name]
[Continue for all phases…]
```

### Automated verification results

```markdown
## Automated Verification Results

### Passing Checks:
- ✅ `make test` — All 45 tests passing
- ✅ `npm run lint` — No linting errors
- ✅ `mypy src/` — Type checking passed

### Failing Checks:
- ❌ `pytest tests/test_auth.py::test_token_refresh` — failing with timeout error
  - **Root Cause:** Token refresh endpoint not handling concurrent requests
  - **Location:** `api/auth.py:123`
  - **Recommendation:** Add lock mechanism or queue

[No failing checks? State "All automated verification checks passed."]
```

### Code review findings

```markdown
## Code Review Findings

### What Matches Plan:
- [List items that match]

### Deviations from Plan:
- **Deviation 1:** [Description]
  - **Reason:** [If known]
  - **Impact:** [Operational / complexity effect]
  - **Assessment:** Acceptable | Problematic

[No deviations? State "Implementation matches plan exactly."]

### Potential Issues:
- [Issue with file:line reference and description]

[No issues? State "No issues identified."]
```

### Manual testing required

```markdown
## Manual Testing Required

1. **[Test area]**
   - [Step-by-step instructions]
   - [Expected outcome]

[Mark items completed if already tested in this session]
```

### Recommendations

```markdown
## Recommendations

### Critical (Must Fix Before Merge):
- [Item]

### Important (Should Fix):
- [Item]

### Nice to Have:
- [Item]

### Follow-Up Work:
- [Item]
```

## Presenting the report

After completing validation, open with:

```
# Validation Complete

I've validated the implementation against `.agents/plan-[slug].md`.

## Overall Status: ✅ Ready | ⚠️ Issues Found | ❌ Incomplete

## Summary:
- Phases: [X] of [Y] fully implemented
- Automated Checks: [X] passing, [Y] failing
- Manual Testing: [X] items require human verification
- Critical Issues: [X]
- Important Issues: [Y]
```

Then append the full report sections above.

Close with:

```
Would you like me to:
1. Fix the identified issues
2. Provide more detail on any specific finding
3. Run additional verification checks
```

## Special cases

### Implementation incomplete

```markdown
## Implementation Status: ❌ Incomplete

### Completed Phases:
- Phase 1: ✅ Complete

### Incomplete Phases:
- Phase 3: ⚠️ Partially complete (tasks 1-3 done, tasks 4-5 not started)
- Phase 4: ❌ Not started

**Recommendation:** Complete Phase 3 before validating further.
```

### No automated checks defined

```markdown
## Automated Verification: ⚠️ No Checks Defined

The plan does not include automated verification checks. Manual validation only
is insufficient for complex changes.

**Recommendation:** Add test commands, file-existence checks, or scripts to the
plan before re-validating.
```

### Failing tests

Document each failure using the "Failing Checks" format shown in the report
template above: command, error output, root cause, location, recommendation,
and priority (Critical / Important / Nice to Have).

## Quality checklist

Before delivering the report:

- [ ] Read the entire plan
- [ ] Ran all automated verification commands from the plan
- [ ] Documented pass/fail for each automated check
- [ ] Investigated root causes of any failures
- [ ] Reviewed actual code against plan specifications
- [ ] Identified all deviations from plan
- [ ] Listed clear manual testing steps
- [ ] Provided actionable recommendations
- [ ] Categorized issues by severity (critical, important, nice-to-have)
- [ ] All phases marked complete are actually done
- [ ] No regressions introduced in existing functionality
- [ ] Documentation updated if needed (README, API docs, docstrings)

## Cross-references

Validates the plan from the `planning-implementations` skill. For failures, fix
and re-run, or use `iterating-plans` if the plan itself was wrong.

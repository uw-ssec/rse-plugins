---
description: Validate that an implementation was correctly executed against its plan
user-invocable: true
---

# Initial Setup

When this command is invoked:

## Determine Context

Are you in an existing conversation or starting fresh?

**If existing conversation (implementation was done in this session):**
- You have context about what was implemented
- Review recent conversation to understand changes
- You know which files were modified

**If fresh conversation (reviewing past work):**
- Need to discover what was done through git and codebase analysis
- No memory of implementation decisions
- Must reconstruct what happened from artifacts

## Locate the Plan

**If plan path provided** (e.g., `/validate .agents/plan-auth.md`):
- Read the plan file COMPLETELY
- This is your specification to validate against

**If no plan path provided:**
- Search `.agents/` for plan and implement docs
- Use Glob: `.agents/{plan,implement}-*.md`
- If multiple found, ask user which plan to validate
- If none found, explain validation requires a plan

## Gather Implementation Evidence

Before validating, understand what was actually done:

### Check Recent Commits

```bash
# See recent commits
git log --oneline -n 10

# See changes in most recent commits
git diff HEAD~3..HEAD --stat
```

### Run Tests

```bash
# Run test suite to see current state
make test
# or
pytest tests/ -v
# or
npm test
```

This establishes baseline: are tests currently passing or failing?

# Validation Process

## Step 1: Context Discovery

### Read the Implementation Plan Completely

- Read the entire plan completely (avoid partial reads)
- Understand every phase
- Note all success criteria
- Identify key files and functionality

### Identify What Should Have Changed

Based on the plan:
- Which files should be modified?
- What success criteria should pass?
- What key functionality should exist?
- What tests should be added?

### Conduct Verification Research

Investigate in parallel when possible to verify:

**Database/schema changes:**
```
"Check if database migrations match the plan specifications at [file references]. Verify tables, columns, and indices were created as specified."
```

**Code changes:**
```
"Verify that the authentication middleware at api/middleware/auth.py implements JWT validation as specified in the plan. Check if the implementation follows the pattern described."
```

**Test coverage:**
```
"Find all tests added for the new feature. Verify they cover the scenarios listed in the plan's Testing Strategy section."
```

**Wait for ALL verification to complete** before synthesizing.

## Step 2: Systematic Validation

For each phase in the plan:

### Check Completion Status

Look for checkmarks in the plan:
- `- [x]` = Claimed as complete
- `- [ ]` = Not complete

### Verify the Actual Code Matches Claimed Completion

Don't trust checkmarks blindly. Read the code:
- Are the files actually modified as described?
- Does the implementation match the specification?
- Are the claimed changes actually present?

### Run Automated Verification

Execute EACH command from the "Automated Verification" section of the plan:

```bash
# Example commands from plan:
make test
pytest tests/ -v
npm run lint
mypy src/
curl http://localhost:8000/api/endpoint
```

**Document results:**
- ✅ **PASS**: Command succeeded, output as expected
- ❌ **FAIL**: Command failed, document error and investigate

### Document Pass/Fail Status

For each automated check:
```markdown
- ✅ `make test` — All 45 tests passing (expected 45)
- ❌ `pytest tests/test_new_feature.py` — 2 tests failing (expected 0)
- ✅ `mypy src/` — Type checking passed
```

### If Failures, Investigate Root Cause

When a check fails:
1. Read the error output carefully
2. Identify which code is causing the failure
3. Determine if it's:
   - Implementation bug (code doesn't work)
   - Test bug (test is wrong)
   - Plan mismatch (plan specification was unclear or wrong)
   - Environmental issue (missing dependency, config)

4. Document the finding

### Assess Manual Criteria

For items in the "Manual Verification" section:

**List what needs manual testing:**
```markdown
### Manual Testing Required:
- [ ] Navigate to http://localhost:3000/feature and verify UI renders correctly
- [ ] Test user signup flow end-to-end
- [ ] Verify error messages display correctly
- [ ] Test cross-browser compatibility (Chrome, Firefox, Safari)
```

**Provide clear steps** so the user knows exactly what to test.

**Check if manual testing was already done:**
- If in same session and user confirmed, note that
- If fresh session, assume manual testing is needed

## Step 3: Generate Validation Report

Create a comprehensive validation summary:

### Implementation Status Per Phase

```markdown
## Implementation Status

### Phase 1: [Name]
**Status:** ✅ Fully implemented | ⚠️ Partially implemented | ❌ Not started

**Details:**
- [Task 1]: ✅ Complete
- [Task 2]: ✅ Complete
- [Task 3]: ⚠️ Partially complete (details...)

### Phase 2: [Name]
[Continue for all phases...]
```

### Automated Verification Results

```markdown
## Automated Verification Results

### Passing Checks:
- ✅ `make test` — All 45 tests passing
- ✅ `npm run lint` — No linting errors
- ✅ `mypy src/` — Type checking passed
- ✅ File `src/components/NewFeature.tsx` exists

### Failing Checks:
- ❌ `pytest tests/test_auth.py::test_token_refresh` — Test failing with timeout error
  - **Root Cause:** Token refresh endpoint not handling concurrent requests
  - **Location:** `api/auth.py:123`
  - **Recommendation:** Add lock mechanism or queue

[No failing checks? State "All automated verification checks passed."]
```

### Code Review Findings

```markdown
## Code Review Findings

### What Matches Plan:
- JWT implementation follows pattern specified in plan
- Middleware integration at `api/middleware/auth.py` matches design
- Test coverage includes all specified scenarios

### Deviations from Plan:
- **Deviation 1:** Used Redis for token storage instead of in-memory
  - **Reason:** [Document if reason is known]
  - **Impact:** Requires Redis dependency, adds operational complexity
  - **Assessment:** Acceptable / Problematic

- **Deviation 2:** [Continue as needed]

[No deviations? State "Implementation matches plan exactly."]

### Potential Issues:
- Error handling in `api/auth.py:145` doesn't catch `ConnectionError`
- Missing input validation for email format in `api/users.py:67`
- Performance concern: N+1 query pattern in `api/auth.py:234`

[No issues found? State "No issues identified."]
```

### Manual Testing Required

```markdown
## Manual Testing Required

The following items from the plan's Manual Verification section require human testing:

1. **UI Rendering**
   - Navigate to http://localhost:3000/feature
   - Verify layout matches design
   - Check responsive behavior on mobile

2. **User Flow**
   - Complete signup flow end-to-end
   - Verify confirmation email received
   - Test login with new credentials

3. **Error Handling**
   - Enter invalid email format
   - Verify error message: "Invalid email format"
   - Verify form highlights the email field

4. **Cross-Browser Testing**
   - Test in Chrome, Firefox, Safari
   - Verify feature works in all browsers
   - Note any browser-specific issues

5. **Performance**
   - Load page with 1000 items
   - Verify page loads in under 2 seconds
   - Check for memory leaks with profiler

[Mark items completed if already tested in this session]
```

### Recommendations

```markdown
## Recommendations

### Critical (Must Fix Before Merge):
- Fix failing test: `test_token_refresh`
- Add error handling for `ConnectionError` in auth module

### Important (Should Fix):
- Add input validation for email format
- Address N+1 query pattern for better performance

### Nice to Have:
- Add additional test coverage for edge cases
- Improve error messages for better UX

### Follow-Up Work:
- Monitor Redis memory usage in production
- Consider adding rate limiting for auth endpoints
```

# Validation Checklist

Always verify:

- [ ] All phases marked complete are actually done
- [ ] All automated tests pass
- [ ] Code follows existing patterns in the codebase
- [ ] No regressions introduced in existing functionality
- [ ] Error handling is robust and complete
- [ ] Documentation updated if needed (README, API docs, docstrings)
- [ ] Manual test steps are clear and actionable
- [ ] All success criteria from plan are addressed

# Presenting the Validation Report

After completing validation, present the report to the user:

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

## Critical Issues:
[List critical issues if any, or state "None"]

## Automated Verification:
✅ [X] checks passing
❌ [Y] checks failing

[If failures, list them briefly]

## Manual Testing Required:
[Brief summary of what needs manual testing]

## Recommendations:
**Before merge:**
- [Critical fix 1]
- [Critical fix 2]

**Follow-up:**
- [Nice to have 1]

Full validation report is documented above. Would you like me to:
1. Fix the identified issues
2. Provide more detail on any specific finding
3. Run additional verification checks
```

# Relationship to Other Commands

## Recommended Workflow:

1. `/implement` — Execute the implementation
2. `/validate` — Verify implementation correctness (THIS COMMAND)
3. Fix any issues found
4. `/validate` again if significant fixes were made
5. Manual testing by human
6. Commit and create PR

## Validation Works Best:

- **After implementation is complete** — Can analyze the full set of changes
- **Before creating PR** — Catch issues before review
- **When resuming old work** — Verify what state the code is in

# If You're Validating in a Fresh Session

You won't have context about implementation decisions. This is OK:

**Focus on observable facts:**
- Does the code match the plan specification?
- Do the tests pass?
- Are the success criteria met?

**Don't speculate about intent:**
- Stick to what you can verify
- Note deviations without judging them
- Recommend investigation if something seems wrong but you can't confirm

# Quality Checklist for Validation

Before completing validation, verify:

- [ ] Read the entire plan
- [ ] Ran all automated verification commands from plan
- [ ] Documented pass/fail for each automated check
- [ ] Investigated root causes of any failures
- [ ] Reviewed actual code against plan specifications
- [ ] Identified all deviations from plan
- [ ] Listed clear manual testing steps
- [ ] Provided actionable recommendations
- [ ] Categorized issues by severity (critical, important, nice-to-have)

# Special Cases

## If Implementation is Incomplete

```markdown
## Implementation Status: ❌ Incomplete

### Completed Phases:
- Phase 1: ✅ Complete
- Phase 2: ✅ Complete

### Incomplete Phases:
- Phase 3: ⚠️ Partially complete (tasks 1-3 done, tasks 4-5 not started)
- Phase 4: ❌ Not started

**Recommendation:** Complete Phase 3 before validating further.
```

## If No Automated Checks Defined

```markdown
## Automated Verification: ⚠️ No Checks Defined

The plan does not include automated verification checks. This makes validation difficult.

**Recommendation:** Add automated checks to the plan:
- Test commands to run
- Files that should exist
- Scripts to verify functionality

Manual validation only is insufficient for complex changes.
```

## If Tests Are Failing

Document each failure:
```markdown
❌ `pytest tests/test_auth.py::test_token_refresh`

**Error Output:**
```
FAILED tests/test_auth.py::test_token_refresh - TimeoutError: Token refresh timeout
```

**Root Cause:** Token refresh endpoint not handling concurrent requests

**Location:** `api/auth.py:123`

**Recommendation:** Add lock mechanism or use queue for token refresh requests

**Priority:** Critical (breaks core functionality)
```

# Remember

- **Validation is systematic, not superficial** — Actually run the checks
- **Be thorough** — Don't skip steps or make assumptions
- **Be objective** — Report what is, not what you wish it was
- **Be actionable** — Provide clear next steps for fixing issues
- **Be honest** — Document problems even if they're inconvenient

Good validation catches issues before they reach production. It's worth the time investment.

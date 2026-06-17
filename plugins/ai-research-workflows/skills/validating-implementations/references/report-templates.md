# Validating Implementations — Report Templates

## Implementation Status per Phase

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

## Automated Verification Results

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

## Code Review Findings

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

## Manual Testing Required

```markdown
## Manual Testing Required

1. **[Test area]**
   - [Step-by-step instructions]
   - [Expected outcome]

[Mark items completed if already tested in this session]
```

## Recommendations

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

## Writing & presenting the report

Write the full report to `docs/rse/specs/validation-<slug>.md` (overwriting any
prior validation of the same plan — git preserves earlier verdicts) and present
the same content inline. Both open with the provenance line and header:

```
# Validation Complete

> Validated against `docs/rse/specs/plan-[slug].md` / `docs/rse/specs/implement-[slug].md`
> at commit `[short-sha]` on `[date]`.

## Overall Status: ✅ Ready | ⚠️ Issues Found | ❌ Incomplete

## Summary:
- Phases: [X] of [Y] fully implemented
- Automated Checks: [X] passing, [Y] failing
- Manual Testing: [X] items require human verification
- Critical Issues: [X]
- Important Issues: [Y]
```

Append the full report sections above, then close the document with a References
section:

```markdown
## References
- Plan: `docs/rse/specs/plan-[slug].md`
- Implementation: `docs/rse/specs/implement-[slug].md`
```

Close with:

```
Would you like me to:
1. Fix the identified issues
2. Provide more detail on any specific finding
3. Run additional verification checks
```

## Special Cases

### Implementation Incomplete

```markdown
## Implementation Status: ❌ Incomplete

### Completed Phases:
- Phase 1: ✅ Complete

### Incomplete Phases:
- Phase 3: ⚠️ Partially complete (tasks 1-3 done, tasks 4-5 not started)
- Phase 4: ❌ Not started

**Recommendation:** Complete Phase 3 before validating further.
```

### No Automated Checks Defined

```markdown
## Automated Verification: ⚠️ No Checks Defined

The plan does not include automated verification checks. Manual validation only
is insufficient for complex changes.

**Recommendation:** Add test commands, file-existence checks, or scripts to the
plan before re-validating.
```

### Failing Tests

Document each failure using the "Failing Checks" format shown above: command,
error output, root cause, location, recommendation, and priority (Critical /
Important / Nice to Have).

# Implementation Plan: [Feature/Change Name]

---
**Date:** [YYYY-MM-DD]
**Author:** AI Assistant
**Status:** Draft | Approved | In Progress | Complete
**Related Documents:**
- [Research: Related Topic](research-slug.md) *(if applicable)*
- [Experiment: Related Test](experiment-slug.md) *(if applicable)*

---

## Overview

[2-3 paragraphs explaining what this plan accomplishes, why it's needed, and the high-level approach.]

**Goal:** [Clear, concise statement of what success looks like]

**Motivation:** [Why are we doing this? What problem does it solve?]

## Current State Analysis

[Describe the existing system/code as it stands today. Include specific file references.]

**Existing Implementation:**
- `path/to/file1.ext:123-145` — [What currently exists here]
- `path/to/file2.ext:67` — [What currently exists here]

**Current Behavior:**
[Describe how the system currently works]

**Current Limitations:**
- [Limitation 1]
- [Limitation 2]

## Desired End State

[Describe what the system will look like after implementation]

**New Behavior:**
[Describe how the system will work after changes]

**Success Looks Like:**
- [Observable outcome 1]
- [Observable outcome 2]
- [Observable outcome 3]

## What We're NOT Doing

[Explicitly state what is out of scope. This prevents scope creep and clarifies boundaries.]

- [ ] [Out of scope item 1]
- [ ] [Out of scope item 2]
- [ ] [Out of scope item 3]

**Rationale:** [Why these are deliberately excluded]

## Implementation Approach

[High-level technical approach. What patterns will you follow? What architectural decisions have been made?]

**Technical Strategy:**
[Describe the overall technical approach]

**Key Architectural Decisions:**
1. **Decision:** [Decision description]
   - **Rationale:** [Why this choice]
   - **Trade-offs:** [What this enables/prevents]
   - **Alternatives considered:** [Other options and why they weren't chosen]

**Patterns to Follow:**
- [Existing pattern 1 from codebase] — See `path/to/example.ext:123`
- [Existing pattern 2 from codebase] — See `path/to/example.ext:456`

## Implementation Phases

Each phase's tasks are **bite-sized, test-first steps with real code/commands** —
no placeholders ("add appropriate error handling", "write tests for the above").
Sequence each unit of work as: failing test → run it (watch it fail) → minimal
implementation → run it (watch it pass) → commit.

### Phase 1: [Phase Name]

**Objective:** [What this phase accomplishes]

**Tasks:**
- [ ] **Write the failing test** for [specific behavior]
  - File: `tests/path/test_x.py` (new)

  ```python
  def test_specific_behavior():
      assert function(input) == expected
  ```

- [ ] **Run it, watch it fail:** `pytest tests/path/test_x.py::test_specific_behavior -v`
  → expect FAIL (function not defined)
- [ ] **Implement the minimal code** to pass — show the actual code, not a description
  - File: `src/path/x.py:lines`

  ```python
  def function(input):
      ...  # the real implementation
  ```

- [ ] **Run it, watch it pass:** `pytest tests/path/test_x.py::test_specific_behavior -v`
  → expect PASS
- [ ] **Commit:** `git commit -m "feat: [specific change]"`

**Dependencies:**
- [External dependency or prerequisite if any]

**Verification:**
- [ ] [Exact command that confirms this phase is complete, with expected output]

### Phase 2: [Phase Name]

**Objective:** [What this phase accomplishes]

**Tasks:**
- [ ] [Same bite-sized, test-first structure as Phase 1 — failing test → fail →
      minimal code → pass → commit, with real code and exact commands]

**Dependencies:**
- Requires Phase 1 completion

**Verification:**
- [ ] [Exact command that confirms this phase is complete, with expected output]

### Phase N: [Continue as needed]

[Add additional phases as needed. Each phase should be independently testable and build on previous phases.]

## Success Criteria

### Automated Verification

These checks can be run by execution agents without human intervention:

- [ ] `make test` passes
- [ ] `npm run lint` passes with no errors
- [ ] All unit tests pass: `pytest tests/`
- [ ] Type checking passes: `mypy src/`
- [ ] File `path/to/new/file.ext` exists
- [ ] [Add more automated checks]

### Manual Verification

These require human testing and judgment:

- [ ] UI renders correctly in browser at `http://localhost:3000/feature`
- [ ] User can successfully [perform action]
- [ ] Error messages are clear and helpful
- [ ] Performance is acceptable under normal load
- [ ] Edge case: [describe edge case] behaves correctly
- [ ] [Add more manual checks]

### Reproducibility & Correctness (research code)

For plans that produce a result, figure, metric, or trained artifact (omit only
when the change produces no reported result):

- [ ] Seeds, data versions, environment, and exact commands captured per
      `ai-research-workflows:ensuring-reproducibility`
- [ ] Numerical correctness criterion: expected value vs analytic case /
      reference implementation / invariant, with a justified tolerance
      (`ai-research-workflows:hardening-research-code`)
- [ ] The result reproduces in a clean environment

## Testing Strategy

**Unit Tests:**
- [ ] Test [component 1] behavior at `path/to/test_file.py`
- [ ] Test [component 2] edge cases at `path/to/test_file.py`
- [ ] Mock external dependencies: [list dependencies]

**Integration Tests:**
- [ ] Test [integration point 1]
- [ ] Test [integration point 2]

**Manual Testing:**
- [ ] Test scenario 1: [description]
- [ ] Test scenario 2: [description]

**Test Data Requirements:**
- [Test data needed]
- [How to set up test environment]

## Migration Strategy

[If applicable, describe how to migrate from the old implementation to the new one]

**Migration Steps:**
1. [Step 1]
2. [Step 2]

**Rollback Plan:**
[How to revert if something goes wrong]

**Backward Compatibility:**
[How existing functionality is preserved]

## Risk Assessment

**Potential Risks:**
1. **Risk:** [Description]
   - **Likelihood:** High | Medium | Low
   - **Impact:** High | Medium | Low
   - **Mitigation:** [How to reduce or handle this risk]

2. **Risk:** [Description]
   - **Likelihood:** High | Medium | Low
   - **Impact:** High | Medium | Low
   - **Mitigation:** [How to reduce or handle this risk]

## Edge Cases and Error Handling

[Document edge cases and how they should be handled]

**Edge Cases:**
1. **Case:** [Description]
   - **Expected Behavior:** [How system should respond]
   - **Implementation:** [Where/how this is handled]

**Error Scenarios:**
1. **Error:** [Description]
   - **Handling:** [How error is caught and communicated]

## Performance Considerations

[If applicable, discuss performance implications]

- **Expected Load:** [Description]
- **Performance Targets:** [Metrics]
- **Optimization Strategy:** [Approach]

## Documentation Updates

[List documentation that needs to be created or updated]

- [ ] Update README.md with [new information]
- [ ] Add docstrings to new functions
- [ ] Update API documentation at [location]
- [ ] [Additional documentation needs]

## Timeline Estimate

[Optional: Provide a rough estimate if helpful, but avoid overly precise predictions]

- Phase 1: [Rough estimate]
- Phase 2: [Rough estimate]
- Total: [Rough estimate]

**Note:** These are estimates and may change based on discoveries during implementation.

## Open Questions

[CRITICAL: This section should be EMPTY in the final plan. If there are open questions, they must be resolved before the plan is complete.]

---

## References

**Research Documents:**
- [Research: Topic Name](research-slug.md)

**Experiment Reports:**
- [Experiment: Approach Comparison](experiment-slug.md)

**Files Analyzed:**
- `path/to/file1.ext`
- `path/to/file2.ext`

**External Documentation:**
- [Link to relevant docs]

---

## Review History

[Track plan iterations and reviews]

### Version 1.0 — [Date]
- Initial plan created

### Version 1.1 — [Date] *(if applicable)*
- [Changes made during iteration]

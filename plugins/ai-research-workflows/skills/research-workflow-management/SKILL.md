---
name: research-workflow-management
description: "Use when the user asks for a structured technical research approach, a spike/proof of concept, feasibility investigation, or research-driven implementation planning. Guides a six-phase workflow (Research, Plan, Iterate Plan, Experiment, Implement, Validate) that generates concrete artifacts: research questions and findings, phased implementation plans with success criteria, experiment reports, implementation logs, and validation reports."
metadata:
  assets:
    - assets/research-template.md
    - assets/plan-template.md
    - assets/experiment-template.md
    - assets/implement-template.md
    - assets/handoff-template.md
---

# Research Workflow Management

Use this skill for complex software work that needs evidence before implementation.

## What This Skill Produces

All artifacts are written to `.agents/` in the project root:

| Artifact | Sections |
|----------|---------|
| `research-<slug>.md` | Scope, findings (with file refs), risks, open questions |
| `plan-<slug>.md` | Phases, success criteria (automated + manual), out-of-scope |
| `experiment-<slug>.md` | Hypothesis, setup, observations, recommendation |
| `implement-<slug>.md` | Per-phase progress, deviations, checks run |
| `validation-<slug>.md` | Criterion-by-criterion pass/fail with evidence |

## Six-Phase Workflow

1. **Research (`/research`)** — inspect code, document current behavior, list constraints.
   → `.agents/research-<slug>.md`

2. **Plan (`/plan`)** — create phased implementation plan with measurable criteria.
   → `.agents/plan-<slug>.md`

3. **Iterate Plan (`/iterate-plan`)** — update plan on new constraints; preserve consistency.
   → edited plan document (in-place)

4. **Experiment (`/experiment`, optional)** — run 2-3 alternatives and record evidence.
   → `.agents/experiment-<slug>.md`

5. **Implement (`/implement`)** — execute plan phase-by-phase; log deviations.
   → `.agents/implement-<slug>.md` + code changes

6. **Validate (`/validate`)** — check each criterion with automated + explicit manual checks.
   → `.agents/validation-<slug>.md`

## Concrete Example

```text
/research auth-system
```
Produces `.agents/research-auth-system.md` with content like:

```markdown
## Findings
- `src/auth.py:L42` — JWT decode uses HS256 with a hardcoded secret; risk: key rotation impossible.
- `src/middleware.py:L18` — Token expiry checked only in `auth_required`, not in API routes directly.

## Risks
- **HIGH** Secret rotation requires redeploy; tokens cannot be invalidated individually.

## Open Questions
1. Does the existing auth middleware support scoped permissions?
2. Which OAuth providers are in scope for initial rollout?
```

Then `/plan auth-system` produces `.agents/plan-auth-system.md`:

```markdown
## Phase 1: JWT Key Rotation
**Success Criteria (Automated):** `pytest tests/test_auth.py::test_rotate_key` passes.
**Success Criteria (Manual):** Old token rejected after rotation without service restart.

## Out of Scope
- Social OAuth login (deferred to Phase 2)
```

## Validation Checkpoints and Feedback Loop

1. **After Research:** confirm scope is complete and key unknowns are explicit.
2. **After Plan:** confirm every phase has success criteria and verification steps.
3. **After Experiment (if used):** choose one approach; update plan accordingly.
4. **During Implement:** after each phase, run listed automated checks. If fail → fix or update plan with rationale.
5. **Final Validate:** report pass/fail per criterion with evidence.

**If validation fails:** return to **Iterate Plan** or **Implement** and re-run validation. Do not continue silently.

## Template Assets

Templates are in `${CLAUDE_PLUGIN_ROOT}/skills/research-workflow-management/assets/`:

- `research-template.md` — scope, findings, risks, open questions
- `plan-template.md` — phases, criteria, out-of-scope
- `experiment-template.md` — hypothesis, observations, recommendation
- `implement-template.md` — phase log, deviations, checks
- `handoff-template.md` — summary for handoff to another agent or person

---
name: hardening-research-code
description: >-
  Use when research or scientific code must be made robust and trustworthy —
  define correctness criteria and add reference/golden tests,
  numerical-tolerance and regression checks, and stability checks. Triggers:
  harden this code, is this numerically correct, add regression tests vs known
  results, make the research code robust.
---

# Hardening Research Code

Make research and scientific code trustworthy: correct, regression-safe, and
numerically stable by establishing explicit criteria and backing them with
targeted tests.

## Interaction mode

Choose a mode before acting. Full protocol: `${CLAUDE_PLUGIN_ROOT}/skills/using-research-workflows/references/interaction-modes.md`.

1. **Explicit override wins** — "brainstorm / walk me through / help me think" → Collaborative; "just do it / don't ask / go ahead" → Direct.
2. **Else infer** — vague/exploratory phrasing, or required inputs missing → Collaborative; a specific directive with enough context → Direct.
3. **Else default** — this skill leans **Direct**.
4. **Hard stops, regardless of mode** — destructive, irreversible, or outward-facing actions always get a confirmation first.

## Purpose

Research code often starts as exploratory scripts. Hardening turns it into
trustworthy software: outputs are verifiably correct, regressions are caught
automatically, and numerical behavior is documented and bounded.

## Establish correctness criteria

Before writing any test, decide what "correct" means for this code:

- **Analytical / closed-form solutions** — does the code reproduce a result
  that can be derived by hand or from first principles? (e.g., the discrete
  Fourier transform of a pure sine wave has a single nonzero bin.)
- **Reference implementations** — does it match a trusted, established library
  or codebase on shared inputs?
- **Published results** — does it reproduce a table, figure, or metric from a
  paper within stated tolerances?
- **Conservation laws / invariants** — does a physical or mathematical
  invariant hold? (e.g., total energy is conserved, probability sums to 1,
  a rotation matrix has determinant 1.)

Document the chosen criterion explicitly before writing tests. A test without
a stated criterion is uninterpretable when it fails.

## Techniques

### Golden / reference tests

Compute expected outputs from a trusted source — an analytic formula, a
reference implementation, or a published dataset — and assert that the code
under test matches those outputs within tolerance. Store expected values and
any input data in a versioned file alongside the tests.

### Numerical-tolerance comparisons

Never use exact float equality. Always use absolute or relative tolerances
appropriate to the domain:

```
# strategy-level pseudocode — defer mechanics to python-testing skill
assert |result - expected| < atol + rtol * |expected|
```

Document the tolerance choice: what physical or numerical argument justifies
it? If tolerance is tightened or loosened later, the justification must be
updated.

### Regression tests pinned to accepted outputs

When no analytic reference exists, run the code on canonical inputs, inspect
the outputs manually, accept them as the current baseline, and pin them. Future
runs must stay within tolerance of that baseline. Update the baseline
deliberately, with a commit message explaining why the output changed.

### Stability checks

Perturb inputs, random seeds, data types (e.g., float32 vs float64), or batch
sizes, and verify that outputs vary by a bounded amount. A result that changes
dramatically under small perturbations is not trustworthy, regardless of how
close it is to a reference on the nominal input.

### Property / invariant checks

Assert structural properties that must hold regardless of the specific input
values: symmetry, monotonicity, conservation, idempotence, or range bounds.
These catch whole classes of bugs that value-comparison tests miss.

## Deferral

Defer pytest fixtures, parametrization, `numpy.testing` / `torch.testing`
assertion mechanics, and CI configuration to the
`scientific-python-development:python-testing` skill. This skill is the
research-specific strategy layer: **what** to validate and **why**. Apply the
same principles to R, Julia, Fortran, or any other runtime.

## Workflow

1. **Pick criteria** — choose from the options in "Establish correctness
   criteria" above; document the choice in a comment or README near the tests.
2. **Add the smallest tests that capture them** — one test per criterion; avoid
   testing implementation details.
3. **Run** — confirm tests pass on the current codebase.
4. **Record tolerances and reference-data location** — note the tolerance
   values and where reference/golden data lives. Cross-reference the
   `ensuring-reproducibility` skill for test-data provenance (content hashes,
   retrieval dates, lockfile references).

## Quality checklist

Before marking hardening complete:

- [ ] Correctness criteria are stated explicitly for each test
- [ ] All numerical comparisons use tolerances, not exact float equality
- [ ] Reference / golden data is versioned and its location is recorded
- [ ] Tests run in CI without manual intervention
- [ ] A failing test provides enough output to diagnose the problem

## Cross-references

Integrates with the `validating-implementations` skill (confirming the
hardened code still satisfies its plan's success criteria) and the
`ensuring-reproducibility` skill (provenance for reference data and pinned
baselines).

---
name: hardening-research-code
description: >-
  Use when research or scientific code must be trustworthy — verifiably correct,
  regression-safe, and numerically stable. Triggers: harden this code, is this
  numerically correct, add regression tests vs known results, make the research
  code robust.
---

# Hardening Research Code

Make research and scientific code trustworthy: correct, regression-safe, and
numerically stable by establishing explicit criteria and backing them with
targeted tests.

## Interaction mode

This skill leans **Direct** by default. For the full Collaborative-vs-Direct protocol and override rules, see the Interaction Modes reference in the `ai-research-workflows:using-research-workflows` skill.

## Purpose

Research code often starts as exploratory scripts. Hardening turns it into
trustworthy software: outputs are verifiably correct, regressions are caught
automatically, and numerical behavior is documented and bounded.

## Iron Law: a regression baseline is not a correctness check

Pinning the current outputs proves only that behavior *hasn't changed* — not
that it is *right*. Never label outputs as a verified or "golden" baseline until
they are checked against an independent reference (analytic limit, reference
implementation, published result, or invariant).

**Before falling back to regression-pinning, you MUST confirm no analytic limit,
reference implementation, or invariant is reasonably derivable.** If one is,
verify against it first — "the output looks plausible" is not verification. If
you pin outputs that have NOT been independently verified, label the baseline
`UNVERIFIED` so it is never mistaken for established-correct values, and say so
to whoever relies on it.

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

Choosing the bound: start from the floating-point floor — roughly machine
epsilon times the number of accumulating operations (`atol ≈ N · eps · scale`)
— and widen only for a documented reason (iterative-solver tolerance, stochastic
variance). Use `rtol` for values spanning orders of magnitude, `atol` for values
near zero. **Never tune the tolerance to make a failing test pass** — a bound
chosen to fit the result is a silent correctness hole; derive it from the
numerics, not the output.

### Regression tests pinned to accepted outputs

Use this only **after** confirming no analytic limit, reference implementation,
or invariant is reasonably derivable (see the Iron Law) — a regression baseline
is a fallback, not a substitute for verification. When it genuinely is the only
option: run the code on canonical inputs, check the outputs against whatever
partial criteria you can (ranges, signs, invariants, expected trends), and pin
them. Future runs must stay within tolerance of that baseline. **If the pinned
values were not verified against an independent reference, label the baseline
`UNVERIFIED`** so it is never mistaken for established-correct output. Update the
baseline deliberately, with a commit message explaining why the output changed.

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
3. **Run — and confirm each test can fail.** Confirm the tests pass on the
   current codebase, then confirm each correctness test actually *fails* when its
   criterion is violated (perturb the expected value or the input, watch it go
   red, then restore). A test that has never been seen to fail proves nothing.
4. **Record tolerances and reference-data location** — note the tolerance
   values and where reference/golden data lives. Cross-reference the
   `ai-research-workflows:ensuring-reproducibility` skill for test-data provenance (content hashes,
   retrieval dates, lockfile references).

## Red flags — STOP, you're locking in a wrong result

The deadline temptation is to pin whatever the script prints and call it hardened:

| Thought | Reality |
|---|---|
| "The output looks plausible, I'll pin it as the baseline" | Plausible ≠ correct. Check a derivable reference/invariant first; otherwise label it `UNVERIFIED`. |
| "There's an analytic case but it'd take a while to derive" | That derivation is the correctness anchor. Do it before pinning, or mark the baseline `UNVERIFIED`. |
| "`float ==` is fine here, it's the same machine" | It won't be the same machine in CI or for the next person. Use tolerances. |
| "I'll widen the tolerance so the test passes" | Tuning the bound to the result hides the bug. Derive the bound from the numerics. |
| "It passed on the first run, so it's correct" | A test never seen to fail proves nothing. Make it go red, then green. |

## Common Mistakes

- **Exact float equality** — using `==` on floating-point results fails on trivially different hardware or library versions; always use absolute or relative tolerances appropriate to the domain.
- **Tests with no stated correctness criterion** — a test that asserts a specific number without explaining why that number is correct is uninterpretable when it fails; document the analytical, reference, or published-result source for each expected value.
- **Un-versioned reference data** — storing golden outputs in a file without a version tag, content hash, or commit reference means a silent data change can break tests with no explanation; version reference data alongside the tests.
- **Testing implementation details** — asserting internal intermediate values rather than observable outputs couples tests to the implementation; test at the boundary where the correctness criterion applies.

## Quality checklist

Before marking hardening complete:

- [ ] Correctness criteria are stated explicitly for each test
- [ ] Each baseline is verified against an independent reference, or labeled `UNVERIFIED`
- [ ] Each correctness test has been seen to fail when its criterion is violated
- [ ] All numerical comparisons use tolerances, not exact float equality
- [ ] Reference / golden data is versioned and its location is recorded
- [ ] Tests run in CI without manual intervention
- [ ] A failing test provides enough output to diagnose the problem

## Cross-references

Integrates with the `ai-research-workflows:validating-implementations` skill (confirming the
hardened code still satisfies its plan's success criteria) and the
`ai-research-workflows:ensuring-reproducibility` skill (provenance for reference data and pinned
baselines).

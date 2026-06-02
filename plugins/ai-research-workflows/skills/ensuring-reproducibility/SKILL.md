---
name: ensuring-reproducibility
description: >-
  Use when a result, analysis, or experiment must be reproducible — capture
  environment, data references, random seeds, config, and exact commands as a
  provenance record, and verify by re-running. Triggers: make this
  reproducible, capture provenance, pin the environment for this result, why
  can't I reproduce X.
---

# Ensuring Reproducibility

Given a result, analysis, or experiment, capture enough provenance that someone
else — or future you — can reproduce it exactly.

## Interaction mode

Choose a mode before acting. Full protocol: `${CLAUDE_PLUGIN_ROOT}/skills/using-research-workflows/references/interaction-modes.md`.

1. **Explicit override wins** — "brainstorm / walk me through / help me think" → Collaborative; "just do it / don't ask / go ahead" → Direct.
2. **Else infer** — vague/exploratory phrasing, or required inputs missing → Collaborative; a specific directive with enough context → Direct.
3. **Else default** — this skill leans **Direct**.
4. **Hard stops, regardless of mode** — destructive, irreversible, or outward-facing actions always get a confirmation first.

## Purpose

Capture a provenance record sufficient for independent reproduction. A result
without a provenance record is a claim; with one, it is a reproducible finding.

## What to capture

A complete provenance record includes:

- **Environment** — interpreter or compiler version (e.g., `python 3.12.3`),
  OS, and the dependency lockfile that was active (e.g., `pixi.lock`,
  `uv.lock`, `requirements-frozen.txt`).
- **Data inputs** — file paths or URLs, plus a version tag, commit hash, or
  content hash (e.g., `sha256:abc123`) for each dataset. For remote data,
  record the retrieval date.
- **Random seeds** — every seed passed to NumPy, PyTorch, stdlib `random`, or
  any other RNG. If the code reads seeds from config, pin that config value.
- **Configuration and parameters** — all non-default flags, hyperparameters,
  or config file contents that affect the result.
- **Exact commands** — the full shell commands run, in order, so someone can
  copy-paste them into a clean environment:

  ```bash
  pixi run python train.py --config configs/baseline.yaml --seed 42
  pixi run python evaluate.py --checkpoint outputs/run-001/best.ckpt
  ```

### Where the record lives

Append a `## Reproducibility` section to the relevant artifact in `.agents/`:

- experiment result → `.agents/experiment-<slug>.md`
- implementation result → `.agents/implement-<slug>.md`
- no existing artifact → create `.agents/reproducibility-<slug>.md`

If reproducing someone else's work, note what was missing from their record.

## Deferral — environment pinning mechanics

This skill decides **what** provenance to record; separate skills handle
**how** to pin the environment:

- **conda + PyPI, multi-platform lockfiles** → defer to
  `scientific-python-development:pixi-package-manager`
- **PyPI-only lockfiles** → defer to `python-development:uv-package-manager`

This skill is language-agnostic at the strategy level. Apply the same
provenance principles to R, Julia, Rust, or any other runtime.

## Verify

Where feasible, reproduce from the record in a clean environment and confirm
the result matches. Steps:

1. Start from a fresh environment (new venv, container, or clean pixi/uv
   environment).
2. Install dependencies from the pinned lockfile only — no manual upgrades.
3. Run the exact commands recorded in the provenance record.
4. Compare outputs to the original result.

For nondeterministic outputs (parallelism, GPU float accumulation, stochastic
sampling with no fixed seed), define and document a tolerance:

```
Metric: validation accuracy
Expected: 0.847 ± 0.003 (3 independent runs with seeds 42, 123, 999)
```

Document the reproduction attempt — success, failure, and any tolerance
applied — in the provenance record.

## Quality checklist

Before marking reproducibility capture complete:

- [ ] Environment pinned: runtime version + lockfile reference recorded
- [ ] Data inputs referenced with versions or content hashes
- [ ] All random seeds recorded
- [ ] Commands are complete and copy-pasteable as written
- [ ] A reproduction attempt is documented (or explicitly deferred with reason)

## Cross-references

Integrates with the `running-experiments` and `implementing-plans` skills.
Both write `.agents/` artifacts that become the natural home for the
`## Reproducibility` section this skill appends.

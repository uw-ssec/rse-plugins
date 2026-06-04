---
name: ensuring-reproducibility
description: >-
  Use when a result, experiment, or analysis must be reproducible by others or
  by a future session. Triggers: make this reproducible, capture provenance, pin
  the environment for this result, why can't I reproduce X.
---

# Ensuring Reproducibility

Given a result, analysis, or experiment, capture enough provenance that someone
else — or future you — can reproduce it exactly.

## Interaction mode

This skill leans **Direct** by default. For the full Collaborative-vs-Direct protocol and override rules, see the Interaction Modes reference in the `ai-research-workflows:using-research-workflows` skill.

## Purpose

Capture a provenance record sufficient for independent reproduction. A result
without a provenance record is a claim; with one, it is a reproducible finding.

## Iron Law: a record is not done until it has been reproduced

Capturing the environment, code, data, seeds, and commands is **necessary but
not sufficient**. An unverified provenance record is a hypothesis, not a
reproducible finding. You MUST reproduce the result in a clean environment
before calling it reproducible.

**Deferring the clean-room reproduction is allowed ONLY when a fresh run is
technically impossible** — the original hardware, proprietary data, or licensed
software is genuinely unavailable. **Being short on time is never a valid
reason.** If a full re-run is too long for the time you have, run a *minimal*
reproduction (a smaller subset, fewer steps, one seed) in a clean environment —
verify something, never nothing.

## What to capture

A complete provenance record includes:

- **Environment** — interpreter or compiler version (e.g., `python 3.12.3`),
  OS, and the dependency lockfile that was active (e.g., `pixi.lock`,
  `uv.lock`, `requirements-frozen.txt`).
- **Code version** — the commit hash of the analysis/model code itself
  (`git rev-parse HEAD`); note if the working tree was dirty. Pinning the
  environment but not the code that produced the result defeats reproduction.
- **Hardware / accelerator** — for GPU, accelerated, or parallel runs, record
  the device, CUDA/driver version, and thread/process counts; these change
  numerical results and explain nondeterminism.
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

Append a `## Reproducibility` section to the relevant artifact in `docs/rse/specs/` (or its legacy `.agents/` location):

- experiment result → `docs/rse/specs/experiment-<slug>.md`
- implementation result → `docs/rse/specs/implement-<slug>.md`
- no existing artifact → create `docs/rse/specs/reproducibility-<slug>.md`

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

Reproduce from the record in a clean environment and confirm the result
matches. This is **required, not optional** (see the Iron Law above) — bounded
only by technical impossibility, never by time pressure. Steps:

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

## Red flags — STOP, you're rationalizing the skip

The clean-room reproduction is exactly the step a deadline tempts you to drop:

| Thought | Reality |
|---|---|
| "The env is right here, it'll reproduce fine" | "Right here" is not a clean room. An unverified record is a hypothesis. Run it fresh. |
| "No time to spin up a clean environment" | Time is never a valid deferral. Do a *minimal* clean-room run, don't skip. |
| "I'll do the clean-room run after submission" | Later never comes — and the number is already in the paper. Verify before you report it. |
| "It's deterministic, so it obviously reproduces" | Determinism is a claim until a fresh environment confirms it; deps, hardware, and unseeded RNG drift silently. |

## Common Mistakes

- **Environment without data provenance** — recording the lockfile but omitting dataset versions, content hashes, or retrieval dates leaves the biggest reproducibility gap; pin both environment and data.
- **Seeds in prose but not in config** — noting "we used seed 42" in a comment is not enough if the code reads seeds from a config file that was not pinned; capture the exact config state.
- **Never attempting a clean-room reproduction** — a provenance record that was never verified is a hypothesis, not a proof; always attempt at least one reproduction in a fresh environment, even a minimal one.
- **Commands that are not runnable as written** — paraphrased or abbreviated commands ("run the training script") fail when someone tries to follow them; every command must be copy-pasteable and correct.

## Quality checklist

Before marking reproducibility capture complete:

- [ ] Environment pinned: runtime version + lockfile reference recorded
- [ ] Data inputs referenced with versions or content hashes
- [ ] All random seeds recorded
- [ ] Code version (commit hash) and hardware/accelerator recorded where relevant
- [ ] Commands are complete and copy-pasteable as written
- [ ] The result was reproduced in a clean environment (at least a minimal run);
      deferral documented ONLY if a fresh run is technically impossible — never for time

## Cross-references

Integrates with the `ai-research-workflows:running-experiments` and `ai-research-workflows:implementing-plans` skills.
Both write `docs/rse/specs/` artifacts that become the natural home for the
`## Reproducibility` section this skill appends.

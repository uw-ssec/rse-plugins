# Design: Refresh `pixi-package-manager` skill to pixi 0.69.0

**Date:** 2026-05-29
**Status:** Approved (design phase)
**Target skill:** `plugins/scientific-python-development/skills/pixi-package-manager/`

## Problem

The `pixi-package-manager` skill was last touched against an early pixi release
and has drifted from current conventions:

- Uses the deprecated `[tool.pixi.project]` table instead of the current
  `[tool.pixi.workspace]` terminology.
- Leads with `pyproject.toml` but never explains the `pixi.toml` alternative
  that `pixi init` now produces by default.
- Pins CI to `prefix-dev/setup-pixi@v0.4.1` and uses deprecated
  `actions/upload-artifact@v3` / `codecov/codecov-action@v3`. Actions are
  pinned by mutable tag, not commit SHA.
- Omits genuinely useful newer surface area (`pixi global`, `pixi exec`,
  `pixi shell-hook`).
- **Records no metadata about which pixi version the guidance targets**, so
  there is no signal for when the skill next needs a refresh.

Latest pixi at time of writing: **0.69.0** (released 2026-05-20).
Latest `prefix-dev/setup-pixi`: **v0.9.6** (released 2026-05-21).

## Goals

1. Add version metadata so the skill states the pixi release it was verified
   against and the date of verification.
2. Correct outdated terminology, deprecated patterns, and stale CI action
   versions throughout the skill and its assets/references.
3. Add concise coverage of high-value new surface area without bloating the
   skill.
4. Harden the CI asset template by pinning all GitHub Actions to commit SHAs.

## Non-Goals (YAGNI)

- No full rewrite or restructure of the skill.
- No deep `pixi build` / rattler-build or distribution sections — pointers only.
- No new asset files; edit the three existing assets in place.
- No additions to the empty `scripts/` directory.
- No broad security section — SHA-pinning guidance stays scoped to the CI asset
  plus one explanatory sentence.

## Design

### 1. Version metadata (frontmatter)

Add structured fields to the `SKILL.md` YAML `metadata` block:

```yaml
metadata:
  pixi-version: "0.69.0"
  last-verified: "2026-05-29"
  assets:
    - assets/github-actions-pixi.yml
    - assets/pyproject-multi-env.toml
    - assets/pyproject-pixi-example.toml
  references:
    - references/common-issues.md
    - references/patterns.md
```

`pixi-version` is the release the guidance was verified against;
`last-verified` is the verification date. These become the values to bump on
each future refresh.

### 2. Terminology & correctness fixes

Apply across `SKILL.md`, `references/patterns.md`, `references/common-issues.md`,
and the three `assets/` files:

- **`[tool.pixi.project]` → `[tool.pixi.workspace]`** (and any prose referring
  to the pixi "project" table). Add a one-line note that `project` still works
  as a deprecated alias so existing manifests are not broken.
- **`[project]` (PEP 621) stays** — it is standard Python packaging metadata,
  not pixi-specific.
- Verify exact CLI flags against 0.69.0 during implementation and correct any
  drift — specifically the import flag (the skill currently shows
  `--import-environment`; confirm against `pixi init --import <file>`) and
  `--format pyproject`.

### 3. Manifest format handling

Keep **pyproject.toml as primary** (aligns with the scientific-Python-packaging
focus of the plugin). Add a short subsection under Core Concepts —
"pixi.toml vs pyproject.toml" — covering:

- `pixi init` defaults to a standalone `pixi.toml`.
- When to choose each (standalone tool/workflow vs. distributable Python package).
- That all examples in the skill map cleanly to both formats.

### 4. Targeted new-feature additions (concise)

- **`pixi global`** — install CLI tools globally (covers `pipx`/`condax` use
  cases). Add to the Quick Reference card and a short Core Concept note.
- **`pixi exec`** — run a tool in a temporary throwaway environment
  (e.g. `pixi exec ruff check`). Quick Reference entry.
- **`pixi shell-hook`** — activation for CI/scripting. Mention in CI / patterns.
- One-line pointers in Resources to **`pixi build`** (rattler-build backends)
  and the official **migration guides** (conda/poetry/uv). No full sections.

### 5. CI asset hardening (`assets/github-actions-pixi.yml`)

Pin every action to a full 40-char commit SHA with a trailing version comment
(GitHub-recommended supply-chain hardening; satisfies zizmor `unpinned-uses`):

```yaml
- uses: actions/checkout@<sha>          # v5.x.x
- uses: prefix-dev/setup-pixi@<sha>     # v0.9.6
- uses: actions/upload-artifact@<sha>   # v4.x.x
- uses: codecov/codecov-action@<sha>    # v5.x.x
```

- Resolve exact SHAs at implementation time via `git ls-remote --tags` /
  `gh api` so they are real and verifiable.
- Bump `actions/checkout` from v4 to **v5** (matches this repo's newer usage).
- Bump `actions/upload-artifact` v3 → v4 and `codecov/codecov-action` v3 → v5.
- Add one explanatory sentence in the skill body on why SHA-pinning matters
  (mutable tags are a supply-chain risk).

### 6. Resource link audit

Verify/update the Resources section links (docs URLs, `setup-pixi` action,
configuration reference) against the current pixi docs structure.

## Acceptance Criteria

- [x] `SKILL.md` frontmatter has `pixi-version: "0.69.0"` and
      `last-verified: "2026-05-29"`.
- [x] No remaining `[tool.pixi.project]` table headers; `[tool.pixi.workspace]`
      used instead, with a deprecation note (the old name still appears once, as
      a prose mention inside that deprecation note — intentional).
- [x] Manifest-format subsection present; pyproject.toml remains primary.
- [x] `pixi global`, `pixi exec`, and `pixi shell-hook` are covered concisely.
- [x] `assets/github-actions-pixi.yml` pins all four actions to real commit
      SHAs (independently re-resolved) with version comments. Pinned to the
      actual latest stable tags at implementation time: checkout v6.0.2,
      upload-artifact v7.0.1, codecov v6.0.1, setup-pixi v0.9.6 (newer than the
      v5/v4/v5 estimated in this spec).
- [x] Body contains a one-line rationale for SHA-pinning.
- [x] CLI flags shown in the skill verified against the installed pixi 0.69.0
      binary (`--import`, no `pixi list --export`, no `pixi task info`).
- [x] Resource links verified current (all 200, no `http://`).

## Files Touched

- `plugins/scientific-python-development/skills/pixi-package-manager/SKILL.md`
- `plugins/scientific-python-development/skills/pixi-package-manager/references/patterns.md`
- `plugins/scientific-python-development/skills/pixi-package-manager/references/common-issues.md`
- `plugins/scientific-python-development/skills/pixi-package-manager/assets/github-actions-pixi.yml`
- `plugins/scientific-python-development/skills/pixi-package-manager/assets/pyproject-pixi-example.toml`
- `plugins/scientific-python-development/skills/pixi-package-manager/assets/pyproject-multi-env.toml`

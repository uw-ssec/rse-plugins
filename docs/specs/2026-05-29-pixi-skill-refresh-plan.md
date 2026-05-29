# Pixi Package Manager Skill Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refresh the `pixi-package-manager` skill to current pixi 0.69.0 conventions, add version metadata to its frontmatter, and SHA-pin all GitHub Actions in its CI asset.

**Architecture:** Pure documentation edit. Modify `SKILL.md`, two reference files, and three asset files in place. No new files, no code. "Tests" are `grep`/validity assertions run against the edited files plus the repo's existing `validate-plugins` structural checks. Spec lives at `docs/specs/2026-05-29-pixi-skill-refresh-design.md`.

**Tech Stack:** Markdown, TOML, YAML; `gh` CLI for resolving action SHAs; `grep`/`jq` for verification.

---

## File Structure

All paths are under `plugins/scientific-python-development/skills/pixi-package-manager/`:

- `SKILL.md` — main skill body + YAML frontmatter. Gets version metadata, terminology fixes, the manifest-format subsection, new-command coverage, and the SHA-pinning rationale sentence.
- `references/patterns.md` — deep patterns. Terminology fixes (`[tool.pixi.project]` → `[tool.pixi.workspace]`).
- `references/common-issues.md` — troubleshooting. Terminology fixes only (it uses `[tool.pixi.environments]`/`target`, verify nothing references the old `project` table).
- `assets/pyproject-pixi-example.toml` — basic example. Terminology fix.
- `assets/pyproject-multi-env.toml` — multi-env example. Verify terminology (uses features/environments; check for `project` table).
- `assets/github-actions-pixi.yml` — CI template. SHA-pin all actions, bump versions.

Task ordering: the CI asset (Task 1) is independent and front-loaded because resolving SHAs requires network calls. Terminology (Task 2) is a mechanical sweep. Metadata (Task 3), manifest subsection (Task 4), and new-command coverage (Task 5) are additive edits to `SKILL.md`. Task 6 verifies flags/links. Task 7 is the final whole-skill validation.

---

## Task 1: SHA-pin and version-bump the CI asset

**Files:**
- Modify: `plugins/scientific-python-development/skills/pixi-package-manager/assets/github-actions-pixi.yml`

- [ ] **Step 1: Resolve the latest stable tag for each action**

Run each command and record the tag string it prints:

```bash
gh api repos/actions/checkout/tags --jq '.[0].name'
gh api repos/prefix-dev/setup-pixi/tags --jq '.[0].name'
gh api repos/actions/upload-artifact/tags --jq '.[0].name'
gh api repos/codecov/codecov-action/tags --jq '.[0].name'
```

Expected (approximate — use whatever the API returns, do not hardcode these):
- `actions/checkout` → `v5.x.x`
- `prefix-dev/setup-pixi` → `v0.9.6` or newer
- `actions/upload-artifact` → `v4.x.x`
- `codecov/codecov-action` → `v5.x.x`

If `setup-pixi` returns a tag older than `v0.9.6`, use `v0.9.6` (the version verified in the spec).

- [ ] **Step 2: Resolve the commit SHA each tag points to**

For each tag from Step 1, get the underlying commit SHA (this dereferences annotated tags correctly):

```bash
gh api repos/actions/checkout/commits/<tag> --jq '.sha'
gh api repos/prefix-dev/setup-pixi/commits/<tag> --jq '.sha'
gh api repos/actions/upload-artifact/commits/<tag> --jq '.sha'
gh api repos/codecov/codecov-action/commits/<tag> --jq '.sha'
```

Expected: each prints a 40-character hex SHA. Record tag + SHA pairs.

- [ ] **Step 3: Rewrite the asset with SHA-pinned actions**

Replace the entire file with the version below, substituting each `<sha>` with the real SHA from Step 2 and each comment with the matching tag from Step 1. Note the bumps: `setup-pixi` v0.4.1 → resolved tag, `upload-artifact` v3 → v4, `codecov-action` v3 → v5, `checkout` v4 → v5.

```yaml
# .github/workflows/test.yml
# Actions are pinned to full commit SHAs (with the tag in a comment) as a
# supply-chain hardening measure: a mutable tag like @v5 can be repointed to
# malicious code, a commit SHA cannot. Update the SHA when you bump the tag.
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]

    steps:
      - uses: actions/checkout@<sha>            # v5.x.x

      - name: Setup Pixi
        uses: prefix-dev/setup-pixi@<sha>       # v0.9.6
        with:
          pixi-version: latest
          cache: true

      - name: Install dependencies
        run: pixi install --environment test

      - name: Run tests
        run: pixi run test

      - name: Upload coverage
        uses: codecov/codecov-action@<sha>      # v5.x.x
        with:
          files: ./coverage.xml

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha>            # v5.x.x
      - uses: prefix-dev/setup-pixi@<sha>       # v0.9.6
      - run: pixi run format --check
      - run: pixi run lint

  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha>            # v5.x.x
      - uses: prefix-dev/setup-pixi@<sha>       # v0.9.6
      - run: pixi run --environment docs docs-build
      - uses: actions/upload-artifact@<sha>     # v4.x.x
        with:
          name: documentation
          path: docs/_build/html
```

(Note: `codecov-action` v5 renamed the `file:` input to `files:` — that change is included above.)

- [ ] **Step 4: Verify no unpinned actions remain**

Run:

```bash
grep -nE 'uses: .*@v[0-9]' plugins/scientific-python-development/skills/pixi-package-manager/assets/github-actions-pixi.yml
```

Expected: no output (every `uses:` should be `@<40-hex-sha>`, with the version only in a trailing comment).

- [ ] **Step 5: Verify every pinned SHA is 40 hex chars**

Run:

```bash
grep -oE '@[0-9a-f]{40}' plugins/scientific-python-development/skills/pixi-package-manager/assets/github-actions-pixi.yml | sort -u
```

Expected: 4 distinct SHAs printed (checkout, setup-pixi, upload-artifact, codecov), each 40 hex chars.

- [ ] **Step 6: Commit**

```bash
git add plugins/scientific-python-development/skills/pixi-package-manager/assets/github-actions-pixi.yml
git commit -m "fix(pixi-skill): SHA-pin and bump GitHub Actions in CI asset"
```

---

## Task 2: Replace deprecated `[tool.pixi.project]` terminology

**Files:**
- Modify: `plugins/scientific-python-development/skills/pixi-package-manager/SKILL.md`
- Modify: `plugins/scientific-python-development/skills/pixi-package-manager/references/patterns.md`
- Modify: `plugins/scientific-python-development/skills/pixi-package-manager/assets/pyproject-pixi-example.toml`
- Check: `references/common-issues.md`, `assets/pyproject-multi-env.toml`

- [ ] **Step 1: Find every occurrence of the old table name**

Run:

```bash
grep -rn '\[tool\.pixi\.project\]\|pixi\.project\|tool\.pixi\.project' \
  plugins/scientific-python-development/skills/pixi-package-manager/
```

Expected: at least `assets/pyproject-pixi-example.toml:10` (`[tool.pixi.project]`). Record every hit.

- [ ] **Step 2: Replace `[tool.pixi.project]` with `[tool.pixi.workspace]`**

In `assets/pyproject-pixi-example.toml`, change the table header:

```toml
[tool.pixi.workspace]
channels = ["conda-forge"]
platforms = ["linux-64", "osx-64", "osx-arm64", "win-64"]
```

Apply the same `[tool.pixi.project]` → `[tool.pixi.workspace]` replacement to every other hit found in Step 1 (across `SKILL.md` and `references/patterns.md` if present). `[project]` (PEP 621) and `[tool.pixi.environments]`/`[tool.pixi.feature.*]`/`[tool.pixi.tasks]`/`[tool.pixi.target.*]` tables are correct as-is — do NOT touch them.

- [ ] **Step 3: Add a deprecation note in SKILL.md**

In `SKILL.md`, inside the "pyproject.toml Integration" core-concept area (around the `[tool.pixi.*]` discussion), add this note:

```markdown
> **Terminology note:** pixi renamed the project-level table to
> `[tool.pixi.workspace]` (standalone manifests use `[workspace]`). The older
> `[tool.pixi.project]` / `[project]`-style pixi table still works as a
> deprecated alias, so existing manifests keep functioning — but new projects
> should use `workspace`.
```

- [ ] **Step 4: Verify no deprecated table headers remain**

Run:

```bash
grep -rn '\[tool\.pixi\.project\]' plugins/scientific-python-development/skills/pixi-package-manager/
```

Expected: no output. (The only allowed mention of the word "project" near pixi tables is the prose deprecation note from Step 3, which does not use the `[tool.pixi.project]` header form.)

- [ ] **Step 5: Verify the TOML asset is still parseable**

Run:

```bash
python -c "import tomllib,sys; tomllib.load(open(sys.argv[1],'rb')); print('OK')" \
  plugins/scientific-python-development/skills/pixi-package-manager/assets/pyproject-pixi-example.toml
```

Expected: `OK`. Repeat for `assets/pyproject-multi-env.toml`.

- [ ] **Step 6: Commit**

```bash
git add plugins/scientific-python-development/skills/pixi-package-manager/
git commit -m "fix(pixi-skill): use [tool.pixi.workspace] terminology with deprecation note"
```

---

## Task 3: Add version metadata to SKILL.md frontmatter

**Files:**
- Modify: `plugins/scientific-python-development/skills/pixi-package-manager/SKILL.md` (frontmatter, lines 1-12)

- [ ] **Step 1: Add `pixi-version` and `last-verified` fields**

Edit the frontmatter `metadata:` block so it reads:

```yaml
---
name: pixi-package-manager
description: Manage scientific Python dependencies and environments using pixi package manager with unified conda-forge and PyPI support, task automation, and reproducible lockfiles.
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
---
```

- [ ] **Step 2: Verify the frontmatter is valid YAML and contains the fields**

Run:

```bash
python -c "
import yaml
text = open('plugins/scientific-python-development/skills/pixi-package-manager/SKILL.md').read()
fm = text.split('---', 2)[1]
data = yaml.safe_load(fm)
assert data['metadata']['pixi-version'] == '0.69.0', data['metadata']
assert data['metadata']['last-verified'] == '2026-05-29', data['metadata']
print('OK')
"
```

Expected: `OK`.

- [ ] **Step 3: Commit**

```bash
git add plugins/scientific-python-development/skills/pixi-package-manager/SKILL.md
git commit -m "feat(pixi-skill): record pixi-version and last-verified in frontmatter"
```

---

## Task 4: Add "pixi.toml vs pyproject.toml" subsection

**Files:**
- Modify: `plugins/scientific-python-development/skills/pixi-package-manager/SKILL.md` (Core Concepts section, after concept 6 "pyproject.toml Integration")

- [ ] **Step 1: Add the subsection**

In `SKILL.md`, immediately after the "### 6. pyproject.toml Integration" block (before the "## Quick Start" heading), insert:

```markdown
### 7. Manifest Format: `pixi.toml` vs `pyproject.toml`

Pixi supports two manifest formats. This skill leads with `pyproject.toml`
because scientific Python work usually involves a distributable package, and
`pyproject.toml` is the standard single source of truth.

| Use `pyproject.toml` (this skill's default) | Use standalone `pixi.toml` |
|---------------------------------------------|----------------------------|
| You are building an installable Python package | The project is a workflow, analysis, or app, not a package |
| You want pip/build/uv compatibility | You want the leanest possible manifest |
| `pixi init --format pyproject` | `pixi init` (the default) |

Everything in this skill maps to both formats. The only difference is table
prefixes: `pyproject.toml` uses `[tool.pixi.*]` (e.g. `[tool.pixi.workspace]`,
`[tool.pixi.dependencies]`); a standalone `pixi.toml` drops the prefix
(`[workspace]`, `[dependencies]`).
```

- [ ] **Step 2: Verify the subsection landed and is well-formed**

Run:

```bash
grep -n 'Manifest Format: `pixi.toml` vs `pyproject.toml`' \
  plugins/scientific-python-development/skills/pixi-package-manager/SKILL.md
```

Expected: one matching line.

- [ ] **Step 3: Commit**

```bash
git add plugins/scientific-python-development/skills/pixi-package-manager/SKILL.md
git commit -m "docs(pixi-skill): add pixi.toml vs pyproject.toml subsection"
```

---

## Task 5: Add `pixi global`, `pixi exec`, `pixi shell-hook` coverage

**Files:**
- Modify: `plugins/scientific-python-development/skills/pixi-package-manager/SKILL.md` (Quick Reference "Essential Commands" + Resources)

- [ ] **Step 1: Add new commands to the Essential Commands block**

In `SKILL.md`, inside the "### Essential Commands" fenced bash block, append before its closing fence:

```bash
# Global tools (replaces pipx / condax for CLI utilities)
pixi global install ruff                  # install a CLI tool globally
pixi global list                          # list globally installed tools

# Run a tool in a temporary throwaway environment (no project needed)
pixi exec ruff check .                    # run ruff without installing it
pixi exec --spec python=3.12 python -V    # one-off env with a pinned spec

# Print activation for use in scripts / CI without a subshell
pixi shell-hook                           # emit activation commands
```

- [ ] **Step 2: Add a "Global tools and one-off execution" core concept**

After the new subsection from Task 4 ("### 7. Manifest Format..."), add:

```markdown
### 8. Global Tools and One-Off Execution

Not every tool belongs in a project environment:

- **`pixi global install <tool>`** installs a CLI tool into an isolated global
  environment on your `PATH` — the pixi-native replacement for `pipx`/`condax`
  (e.g. `ruff`, `pre-commit`, `jupyterlab`).
- **`pixi exec <cmd>`** runs a command in a temporary environment that is
  discarded afterward — ideal for trying a tool without adding a dependency, or
  for CI one-offs (`pixi exec --spec python=3.12 python -V`).
- **`pixi shell-hook`** prints the activation script for an environment without
  spawning a subshell, which is what you want in CI steps and wrapper scripts.
```

- [ ] **Step 3: Add pointers for build/migration in Resources**

In `SKILL.md` under "### Official Documentation" in the Resources section, add these bullets:

```markdown
- **Building packages (`pixi build`)**: https://pixi.sh/latest/build/getting_started/
- **Migration guides (conda, poetry, uv)**: https://pixi.sh/latest/switching_from/conda/
```

- [ ] **Step 4: Add the SHA-pinning rationale sentence**

In `SKILL.md`, in the "Leverage caching in CI/CD" / Performance or a CI-related bullet area (Best Practices Checklist → Performance), add this checklist item:

```markdown
- [ ] Pin GitHub Actions to commit SHAs (not mutable tags) in CI — see `assets/github-actions-pixi.yml`; a tag like `@v5` can be repointed to malicious code, a SHA cannot
```

- [ ] **Step 5: Verify all four additions are present**

Run:

```bash
grep -c 'pixi global install\|pixi exec\|pixi shell-hook' \
  plugins/scientific-python-development/skills/pixi-package-manager/SKILL.md
grep -n 'Global Tools and One-Off Execution\|Pin GitHub Actions to commit SHAs\|pixi.sh/latest/build' \
  plugins/scientific-python-development/skills/pixi-package-manager/SKILL.md
```

Expected: first command prints a count ≥ 4; second prints the three matching lines.

- [ ] **Step 6: Commit**

```bash
git add plugins/scientific-python-development/skills/pixi-package-manager/SKILL.md
git commit -m "docs(pixi-skill): add pixi global/exec/shell-hook and SHA-pinning guidance"
```

---

## Task 6: Verify CLI flags and resource links against pixi 0.69.0

**Files:**
- Modify (only if drift found): `SKILL.md`, `references/patterns.md`, `references/common-issues.md`

- [ ] **Step 1: Audit the import flag**

The skill shows `pixi init --format pyproject --import-environment` (SKILL.md) and
`pixi init --format pyproject --import-environment environment.yml` (patterns.md).
Verify the current flag name:

```bash
gh api repos/prefix-dev/pixi/contents/docs/reference/cli/pixi/init.md --jq '.content' \
  | base64 -d | grep -iE '\-\-import' || echo "flag not found as written"
```

Expected: confirms whether the flag is `--import` (taking a file argument) or `--import-environment`. If it is `--import`, update both files:
- `pixi init --format pyproject --import environment.yml`
- Remove the bare `--import-environment` (with no file) usage; `--import` requires a file argument.

If the audit is inconclusive, fetch `https://pixi.sh/latest/reference/cli/pixi/init/` and read the flags directly, then correct the skill to match.

- [ ] **Step 2: Spot-check other commands still exist**

Confirm these commands used in the skill are still valid in 0.69.0 (they are core and stable, but verify): `pixi add`, `pixi add --pypi`, `pixi add --feature`, `pixi install`, `pixi run`, `pixi shell`, `pixi task add`, `pixi update`, `pixi list`, `pixi tree`, `pixi search`, `pixi self-update`, `pixi clean cache`, `pixi list --export`.

```bash
gh api repos/prefix-dev/pixi/contents/docs/reference/cli/pixi.md --jq '.content' \
  | base64 -d | grep -oE '^\s*\[?`?pixi [a-z-]+' | sort -u || true
```

Expected: the listed subcommands appear. Fix any that were renamed/removed.

- [ ] **Step 3: Check links resolve (no 404s, all HTTPS)**

Run:

```bash
grep -ohE 'https://[a-zA-Z0-9./_-]+' \
  plugins/scientific-python-development/skills/pixi-package-manager/SKILL.md | sort -u \
  | while read -r url; do
      code=$(curl -s -o /dev/null -w '%{http_code}' -L --max-time 15 "$url")
      echo "$code  $url"
    done
```

Expected: every line starts with `200` (or `301`/`302` that resolve). Investigate any `404`. Also confirm there are zero `http://` (non-HTTPS) URLs:

```bash
grep -rn 'http://' plugins/scientific-python-development/skills/pixi-package-manager/ || echo "no http URLs - good"
```

Expected: `no http URLs - good` (the repo's validate-plugins workflow warns on non-HTTPS URLs).

- [ ] **Step 4: Commit (only if Step 1-3 made changes)**

```bash
git add plugins/scientific-python-development/skills/pixi-package-manager/
git commit -m "fix(pixi-skill): correct CLI flags and verify resource links for pixi 0.69.0"
```

If no changes were needed, skip the commit and note "flags/links already current" in the task checkpoint.

---

## Task 7: Final whole-skill validation

**Files:** none modified (verification only, unless issues surface)

- [ ] **Step 1: Confirm no deprecated terminology survived anywhere**

```bash
grep -rn '\[tool\.pixi\.project\]\|setup-pixi@v0\.4\|upload-artifact@v3\|codecov-action@v3' \
  plugins/scientific-python-development/skills/pixi-package-manager/
```

Expected: no output.

- [ ] **Step 2: Run the repo's plugin validation logic locally**

The `validate-plugins` workflow's URL scan is the relevant gate for a docs change:

```bash
grep -rn 'http://' plugins/scientific-python-development/skills/pixi-package-manager/ | grep -v localhost | grep -v 127.0.0.1 || echo "URL scan clean"
```

Expected: `URL scan clean`.

- [ ] **Step 3: Confirm all TOML assets parse and frontmatter is valid**

```bash
for f in plugins/scientific-python-development/skills/pixi-package-manager/assets/*.toml; do
  python -c "import tomllib,sys; tomllib.load(open(sys.argv[1],'rb')); print('OK', sys.argv[1])" "$f"
done
python -c "
import yaml
t=open('plugins/scientific-python-development/skills/pixi-package-manager/SKILL.md').read()
yaml.safe_load(t.split('---',2)[1]); print('frontmatter OK')
"
```

Expected: `OK` for each TOML asset and `frontmatter OK`.

- [ ] **Step 4: Optional — run the skill-reviewer agent**

Dispatch the `plugin-dev:skill-reviewer` agent against the edited skill to catch description/structure regressions. Apply any high-value suggestions; ignore noise. (Skip if not running in an environment with agent dispatch.)

- [ ] **Step 5: Final acceptance check against the spec**

Confirm each acceptance-criteria checkbox in `docs/specs/2026-05-29-pixi-skill-refresh-design.md` is satisfied. Tick them off in the spec file.

- [ ] **Step 6: Commit any final fixes**

```bash
git add plugins/scientific-python-development/skills/pixi-package-manager/ docs/specs/2026-05-29-pixi-skill-refresh-design.md
git commit -m "docs(pixi-skill): finalize refresh and tick spec acceptance criteria"
```

---

## Task 8: Run the Tessl skill review locally

Run Tessl's skill review locally with the `tessl` CLI (installed at
`~/.local/bin/tessl`) against the refreshed skill directory, and resolve its
findings. The repo's CI uses the same reviewer (`tesslio/skill-review@main`)
with a **fail-threshold of 80**, so treat a score ≥ 80 as the bar to clear
before opening a PR.

**Files:** none modified by default (only if Tessl flags issues in the skill)

- [ ] **Step 1: Run the review locally**

```bash
tessl skill review ./plugins/scientific-python-development/skills/pixi-package-manager
```

Expected: Tessl prints a score (0-100) and a list of findings for the skill.

- [ ] **Step 2: Address findings (only if score < 80 or findings are actionable)**

For each actionable finding, edit the relevant file under
`plugins/scientific-python-development/skills/pixi-package-manager/`, then re-run
the review:

```bash
tessl skill review ./plugins/scientific-python-development/skills/pixi-package-manager
```

Repeat until the score is ≥ 80. If a finding is a false positive or conflicts
with the spec, leave the skill as-is and record the rationale in the task
checkpoint rather than degrading the content to satisfy the linter.

- [ ] **Step 3: Confirm the final score and commit any fixes**

Re-run the review one last time to confirm score ≥ 80, then commit any edits
made in Step 2:

```bash
git add plugins/scientific-python-development/skills/pixi-package-manager/
git commit -m "docs(pixi-skill): address Tessl skill-review findings"
```

If no edits were needed, skip the commit and note the passing score in the
checkpoint.

---

## Self-Review Notes

- **Spec coverage:** Task 3 → metadata (goal 1); Tasks 2/6 → terminology + flags/links (goal 2); Tasks 4/5 → manifest subsection + new commands (goal 3); Task 1 → SHA-pinning (goal 4). All four spec goals covered; Task 7 verifies acceptance criteria.
- **Placeholders:** The only `<sha>` placeholders are in Task 1 and are explicitly resolved by Steps 1-2 before use — intentional, not a plan gap.
- **Consistency:** Table name is `[tool.pixi.workspace]` throughout; action version bumps (checkout v5, setup-pixi v0.9.6, upload-artifact v4, codecov v5) are stated identically in Task 1 and re-checked in Task 7.

---
name: supply-chain-ecosystem-quirks
description: Ecosystem-specific supply-chain gotchas for npm, PyPI, conda/pixi, cargo, and Go. Use when reviewing package.json + .npmrc, pyproject.toml + setup.py, pixi.toml + conda-lock.yml, Cargo.toml + .cargo/config.toml, or go.mod + GOPROXY config — any time a supply-chain recommendation depends on which ecosystem you're in. Loads ecosystem-specific reference docs on demand.
metadata:
  references:
    - references/npm-quirks.md
    - references/pypi-quirks.md
    - references/conda-pixi-quirks.md
    - references/cargo-go-quirks.md
---

# Supply Chain Ecosystem Quirks

## Threat Model

Each package manager has unique install-time execution vectors and config knobs that decide whether the general patterns from `supply-chain-dependency-security` and `supply-chain-hardened-ci-cd` actually hold. Escape hatches that need explicit auditing per ecosystem: npm `postinstall`, Python `.pth` and `setup.py`, unsigned conda channels, Cargo `build.rs`, `GOSUMDB=off`.

## Ecosystem Detection and References

Trigger files identify which ecosystem is in scope; each row lists the reference doc to load for the full checklist. Run the bash one-liner to auto-detect, or scan the trigger column manually.

| Ecosystem | Trigger files | Reference |
|-----------|---------------|-----------|
| npm / yarn / pnpm | `package.json`, `.npmrc`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` | `references/npm-quirks.md` |
| PyPI / pip / uv / poetry | `pyproject.toml`, `setup.py`, `requirements.txt`, `uv.lock`, `poetry.lock` | `references/pypi-quirks.md` |
| conda / pixi | `pixi.toml`, `pixi.lock`, `environment.yml`, `conda-lock.yml`, `.condarc` | `references/conda-pixi-quirks.md` |
| cargo | `Cargo.toml`, `Cargo.lock`, `.cargo/config.toml` | `references/cargo-go-quirks.md` |
| Go | `go.mod`, `go.sum`, `GOPROXY` env | `references/cargo-go-quirks.md` |

```bash
# Auto-detect: prints one line per ecosystem present, naming the reference doc to load
test -f package.json && echo "npm -> references/npm-quirks.md"
{ test -f pyproject.toml -o -f setup.py -o -f requirements.txt; } && echo "PyPI -> references/pypi-quirks.md"
{ test -f pixi.toml -o -f environment.yml -o -f conda-lock.yml; } && echo "conda -> references/conda-pixi-quirks.md"
test -f Cargo.toml && echo "cargo -> references/cargo-go-quirks.md"
test -f go.mod && echo "Go -> references/cargo-go-quirks.md"
```

If nothing prints, the project has no packaging-manifest layer this skill covers — return the no-op report (bottom of file).

## Quick-Check Battery

Run this block from the project root. Each line either prints nothing (PASS) or emits a `FAIL:` / `WARN:` line you can `grep FAIL:` on. Skip ecosystems not present.

```bash
# npm — install-time scripts, lockfile, CI command discipline
grep -q 'ignore-scripts=true' .npmrc 2>/dev/null || echo "npm FAIL: set ignore-scripts=true in .npmrc"
test ! -f package.json || test -f package-lock.json || echo "npm FAIL: package-lock.json not committed"
grep -rE 'npm (install|ci)' .github/workflows/ 2>/dev/null | grep -v 'npm ci' && echo "npm FAIL: CI must use 'npm ci'"

# PyPI — .pth code execution, PEP 517 isolation, custom build backend
find $(python -c 'import site;print(site.getsitepackages()[0])' 2>/dev/null) -name '*.pth' -exec grep -lE '^(import|exec|os\.|subprocess)' {} \; 2>/dev/null | sed 's/^/pypi FAIL: code-executing .pth: /'
grep -rE 'no-build-isolation' .github/workflows/ Makefile *.sh 2>/dev/null && echo "pypi FAIL: --no-build-isolation removes PEP 517 isolation"
grep -E '^backend-path' pyproject.toml 2>/dev/null && echo "pypi WARN: custom backend-path — audit build backend code"

# conda/pixi — channel discipline, escape hatches
grep -A 5 '^channels:' .condarc pixi.toml 2>/dev/null | grep -q 'defaults' && echo "conda WARN: 'defaults' channel present; prefer conda-forge"
grep -rE '(--no-deps|--no-pin|--force-reinstall)' .github/workflows/ Makefile *.sh 2>/dev/null && echo "conda FAIL: lockfile escape hatch in CI"

# cargo — build.rs surface, --locked discipline
find . -name 'build.rs' -not -path './target/*' 2>/dev/null | head -5 | sed 's/^/cargo INFO: build.rs present: /'
grep -rE 'cargo (build|test|run)' .github/workflows/ 2>/dev/null | grep -v -- '--locked' && echo "cargo FAIL: CI cargo without --locked"

# Go — GOPROXY/GOSUMDB integrity, -mod=readonly
go env GOSUMDB 2>/dev/null | grep -qE '^(off|)$' && echo "go FAIL: GOSUMDB is off or unset"
grep -rE 'go (build|test|run)' .github/workflows/ 2>/dev/null | grep -v 'mod=readonly\|mod=vendor' && echo "go WARN: CI go build without -mod=readonly"
```

Each printed line maps to one row in the report. For each FAIL, load the matching reference for full remediation guidance.

## Application Workflow

Run the four steps below in order. Each step is independently re-runnable.

### Step 1 — Detect ecosystems present

Run the auto-detect bash one-liner under `## Ecosystem Detection and References`. Record the printed reference paths — these are the only references to load.

### Step 2 — Run the quick-check battery

Run the `## Quick-Check Battery` block. Pipe to `tee quick-check.out`; every `FAIL:` line is a P1 finding handled in step 3, every `WARN:` is a P2.

### Step 3 — Load the matching reference for each FAIL or deep review

For each ecosystem flagged in step 2, or any ecosystem the user asked for a detailed review of, open `references/<eco>-quirks.md`. Each reference document follows the same shape: a threat-relevance paragraph plus 5-6 sectioned checks, each with a verifying command you can copy-paste. Map each section to PASS/WARN/FAIL using the section's verifying command.

### Step 4 — Cross-reference findings against general patterns

Compare each finding to the equivalent control in `supply-chain-dependency-security` (lockfiles, pinning, scanning) and `supply-chain-hardened-ci-cd` (OIDC, ephemeral runners, secret hygiene). If an ecosystem quirk conflicts with general guidance — for example, `pnpm`'s strict isolation makes the general "vendor dependencies" guidance unnecessary — the ecosystem-specific quirk wins for that ecosystem. Note the conflict in the report.

## Output: Ecosystem Quirks Report

Every PASS/WARN/FAIL must cite a `file:line` (or `absent`). Every remediation must name a concrete command, skill, or config knob.

```markdown
## Ecosystem Quirks Posture: <project>

### Ecosystems Detected
| Ecosystem | Evidence (trigger file path) | Reference loaded |
|-----------|------------------------------|------------------|

### Per-Ecosystem Findings
For each detected ecosystem:

#### <ecosystem>
| Quirk / control | PASS/WARN/FAIL | Evidence (file:line) | Remediation (command or skill) |
|-----------------|----------------|----------------------|-------------------------------|

### Cross-Ecosystem Conflicts with General Patterns
Cite any place an ecosystem quirk overrides `supply-chain-dependency-security` or `supply-chain-hardened-ci-cd`.

### Top Priority Actions
1. <highest-impact runnable remediation>
2. <second>
3. <third>
```

If no ecosystems detected: return `No supported package-manager manifests found; this skill does not apply.`

---
name: supply-chain-threat-awareness
description: Supply chain threat posture assessment for projects and packages. Use when reviewing a project's .github/workflows/*.yml, package.json, pyproject.toml, requirements.txt, pixi.toml, or lockfiles for exposure to active 2025–2026 campaigns. Covers Shai-Hulud (500+ npm packages), TeamPCP (Trivy, Checkmarx, LiteLLM, Bitwarden CLI, SAP CAP via tag hijacking), axios (100M weekly downloads), and LiteLLM .pth persistence — all attack patterns CVE scanners miss.
metadata:
  references:
    - references/campaigns/shai-hulud.md
    - references/campaigns/teampcp.md
    - references/campaigns/axios.md
    - references/campaigns/litellm-pth.md
    - references/posture-report-template.md
---

# Supply Chain Threat Awareness

## Threat Model

Maintainer account takeover and release-tag hijacking of widely-trusted packages are the dominant supply-chain threats in 2025–2026.

## CVE Scanner Limitations

Treat scanner-clean as necessary, not sufficient — the audit below covers what advisories miss.

## Active Campaigns

Each campaign has a deep-dive reference. Load on demand based on which applies to the project under review.

- **Shai-Hulud** — 500+ npm packages compromised via maintainer account takeover. → `references/campaigns/shai-hulud.md`
- **TeamPCP** — Trivy, Checkmarx, LiteLLM, Bitwarden CLI, SAP CAP via release-tag hijacking (March 2026). → `references/campaigns/teampcp.md`
- **axios** — 100M weekly npm downloads; maintainer account compromise. → `references/campaigns/axios.md`
- **LiteLLM 1.82.8** — Malicious `.pth` file for persistent Python execution. → `references/campaigns/litellm-pth.md`

## Audit Workflow

Run this assessment in order. Each step has a verifying command. Stop and remediate before continuing if any FAIL is critical (lockfile not committed, no `--ignore-scripts`, mutable action refs).

### Step 1 — Lockfile hygiene

```bash
# Check which lockfiles exist and are committed
git ls-files | grep -E '(package-lock\.json|yarn\.lock|pnpm-lock\.yaml|poetry\.lock|uv\.lock|pixi\.lock|conda-lock\.yml|Cargo\.lock|go\.sum)$'

# Check CI uses lockfile-respecting install commands
grep -rnE '(npm ci|yarn install --frozen-lockfile|pnpm install --frozen-lockfile|uv sync --frozen|poetry install|pixi install|cargo build --locked)' .github/workflows/
```

- [ ] Each detected ecosystem has a committed lockfile (verify with `git ls-files`).
- [ ] CI uses the lockfile-respecting install command — not bare `npm install` or `pip install`.
- [ ] CI caches scoped to the lockfile hash (e.g., `key: deps-${{ hashFiles('package-lock.json') }}`).

If any FAIL: STOP and fix before continuing — without lockfile hygiene, every other check is moot.

### Step 2 — Action pinning

```bash
# Find all mutable uses: refs
grep -nE '^\s*-?\s*uses:\s+[^@]+@[^a-f0-9]' .github/workflows/*.yml || echo "All uses: refs SHA-pinned"
```

- [ ] Every `uses:` ref is a 40-character commit SHA (not `@v4`, `@main`, `@latest`).
- [ ] Trailing comment after SHA records the human-readable version (e.g., `uses: actions/checkout@<sha>  # v4.2.2`).

If FAIL: run `/supply-chain-pin-actions` (dry-run first), then re-verify.

### Step 3 — Install-time execution

```bash
# Check npm scripts that run on install
test -f package.json && jq '.scripts | {preinstall, install, postinstall} // empty' package.json

# Check for ignore-scripts discipline
grep -rE '(npm ci.*--ignore-scripts|ignore-scripts\s*=\s*true)' .github/workflows/ .npmrc 2>/dev/null || echo "WARN: no --ignore-scripts found"

# Python .pth scan (run only if Python is on PATH)
command -v python >/dev/null && find "$(python -c 'import site; print(site.getsitepackages()[0])' 2>/dev/null)" -name "*.pth" -exec grep -lE '^(import|exec|os\.|subprocess)' {} \; 2>/dev/null
```

- [ ] `npm ci --ignore-scripts` in every CI install step OR `.npmrc` has `ignore-scripts=true`.
- [ ] No `.pth` file in Python `site-packages` contains executable Python (only path additions).
- [ ] `preinstall`/`postinstall` scripts in `package.json` are reviewed (or absent).

If FAIL: see `references/campaigns/shai-hulud.md` (postinstall vector) or `references/campaigns/litellm-pth.md` (`.pth` vector).

### Step 4 — Dependency velocity

```bash
# Last 10 lockfile updates with timestamps
git log --follow --pretty=format:"%h %ai %s" -10 package-lock.json 2>/dev/null
git log --follow --pretty=format:"%h %ai %s" -10 uv.lock 2>/dev/null
git log --follow --pretty=format:"%h %ai %s" -10 pixi.lock 2>/dev/null
```

- [ ] Lockfile updates spaced ≥7 days apart on average — no rapid-fire adds without cooldown.
- [ ] No unexpected version bumps without an explicit PR/changelog entry.

If FAIL: hold new deps ≥7 days before merging (most malicious releases yanked within hours).

### Step 5 — SBOM and provenance

```bash
# Check release workflow for SBOM/signing steps
grep -rE '(syft|cyclonedx|spdx|cosign|sigstore|--provenance|attest-build-provenance)' .github/workflows/
```

- [ ] SBOM generated for releases (CycloneDX or SPDX).
- [ ] Sigstore or npm provenance attestations applied.

If FAIL: see `supply-chain-sbom-provenance` skill (cross-link; not yet shipped in this PR).

## Output: Posture Report

When invoked for a posture review, produce the Markdown report defined in `references/posture-report-template.md`. The template specifies the required tables (campaign applicability, step results, top 3 priority actions) and the finding-entry rules (campaign name, `file:line`, blast radius, remediation command or skill).

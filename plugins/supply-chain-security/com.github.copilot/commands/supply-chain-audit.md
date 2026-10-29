---
description: Audit a research software project's supply-chain security posture across .github/workflows/, lockfiles, install scripts, and persistence vectors. Read-only. Produces a structured Markdown report with FAIL/WARN/PASS findings, file:line citations, and prioritized actions linking to remediation commands.
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# Supply Chain Audit

Audit a research software project's supply-chain security posture across CI workflows, lockfiles, install-time execution surfaces, and provenance signals — read-only, with prioritized remediation pointers.

## Arguments

`$ARGUMENTS` — Optional path to a project directory or a single workflow/lockfile (e.g., `/supply-chain-audit ./my-project` or `/supply-chain-audit .github/workflows/release.yml`). Defaults to the current working directory.

## Input Handling

**If the argument is a directory (or omitted):**
- Audit recursively from that root.
- Detect all five categories below in scope.

**If the argument is a single file:**
- If it is a workflow file (`.github/workflows/*.y*ml`), audit only the Action pinning, Workflow permissions, Install-time execution, and Provenance categories for that file.
- If it is a lockfile (e.g., `package-lock.json`, `uv.lock`, `Cargo.lock`), audit only the Lockfile hygiene category for that file.
- If the file type is not recognized, report and exit.

## Information Gathering

Before classifying findings, collect ground truth with these exact commands:

1. **Workflows** — `find .github/workflows -type f \( -name '*.yml' -o -name '*.yaml' \) 2>/dev/null`
2. **Lockfiles** — search for `package-lock.json yarn.lock pnpm-lock.yaml uv.lock poetry.lock pixi.lock conda-lock.yml Cargo.lock go.sum` at the repo root and any common subdirectories (`packages/*`, `services/*`, `crates/*`).
3. **npm scripts** — if `package.json` is present, run `jq '.scripts' package.json 2>/dev/null` to enumerate lifecycle hooks (`preinstall`, `postinstall`, etc.).
4. **Python `.pth` files** — if Python is on PATH, run `find $(python -c "import site; print(site.getsitepackages()[0])" 2>/dev/null) -name "*.pth" 2>/dev/null` and inspect contents (legitimate `.pth` files contain only path additions; executable code is a red flag).
5. **Secrets in workflow env** — `grep -rE 'secrets\.[A-Z_]+' .github/workflows/ 2>/dev/null` plus look for hardcoded token patterns (`ghp_`, `gho_`, `glpat-`, `npm_`, `AKIA`, etc.).

## Audit Categories

### 1. Action pinning

Every `uses:` reference in workflow files must point to a 40-character commit SHA, not a mutable ref (`@v4`, `@main`, `@latest`, `@release/v1`).

- Grep: `grep -nE '^\s*-?\s*uses:\s*[^@]+@' .github/workflows/*.y*ml`
- For each match, verify the ref after `@` is 40 hex characters.
- Flag every mutable ref with the source file and line number.
- Cross-link: `supply-chain-hardened-ci-cd` skill.
- Remediation: `/supply-chain-pin-actions` (dry-run by default).

### 2. Workflow permissions

`permissions:` must be declared at the workflow level or per-job. Deny-by-default (`permissions: {}` at the top of the file, with per-job opt-in) is preferred.

- Grep for `permissions:` blocks; verify their scope.
- Flag workflows with no `permissions:` at all (inherits broad defaults).
- Flag jobs that need narrow scopes but are using the workflow-level grant.
- Cross-link: `supply-chain-hardened-ci-cd`.
- Remediation: `/supply-chain-harden-workflow`.

### 3. Lockfile hygiene

Every detected ecosystem must have a committed lockfile, and CI must install via the lockfile-respecting command (e.g., `npm ci`, `uv sync --frozen`, `cargo build --locked`).

- For each detected lockfile, confirm `git ls-files | grep <lockfile>` shows it tracked.
- For each ecosystem, confirm CI references the locked-install command.
- Cross-link: `supply-chain-dependency-security`.
- Remediation: run `/supply-chain-lockfile-check` for a focused, per-lockfile report.

### 4. Install-time execution

Surface areas where dependency installation can execute arbitrary code.

- npm install steps in workflows: must pass `--ignore-scripts` (or be `npm ci --ignore-scripts`).
- Python `.pth` files in site-packages: list contents; benign `.pth` files only add paths. Executable content is a campaign signal.
- Cross-link: `supply-chain-ecosystem-quirks`.
- Campaign references:
  - `plugins/supply-chain-security/skills/supply-chain-threat-awareness/references/campaigns/shai-hulud.md`
  - `plugins/supply-chain-security/skills/supply-chain-threat-awareness/references/campaigns/litellm-pth.md`

### 5. Provenance

Release workflows should produce an SBOM and sign artifacts (Sigstore, or `npm publish --provenance`).

- Look for SBOM generation steps in release workflows (`syft`, `cyclonedx`, `anchore/sbom-action`).
- Look for signing steps (`sigstore/cosign-installer`, `--provenance` flag on `npm publish`).
- Cross-link: `supply-chain-sbom-provenance`.
- Remediation: apply `assets/sbom-workflow.yml` from that skill.

## Action Steps

### Step 1: Action pinning

- Read every workflow file from the Information Gathering step.
- For each `uses:` line, parse the ref after `@`.
- PASS: ref is 40 hex chars. WARN: ref is a tag like `v4` or `v4.2.2` (mutable but commonly trusted). FAIL: ref is a branch (`main`, `master`, `latest`, `release/v1`).

### Step 2: Workflow permissions

- For each workflow, locate top-level and job-level `permissions:`.
- PASS: workflow-level `permissions: {}` with per-job opt-in. WARN: workflow-level permissions declared but broader than needed. FAIL: no `permissions:` block at all.

### Step 3: Lockfile hygiene

- For each detected ecosystem, confirm both the lockfile is committed AND CI uses the locked install command.
- PASS: both present. WARN: lockfile committed but CI uses `npm install` instead of `npm ci`. FAIL: no lockfile committed.

### Step 4: Install-time execution

- Grep workflow run-steps for `npm install` and `npm ci`; check for `--ignore-scripts`.
- List Python `.pth` files; inspect content for non-path lines.
- PASS: install steps pinned with `--ignore-scripts`; `.pth` files contain only path additions. WARN: install steps without `--ignore-scripts` on trusted-only deps. FAIL: install runs untrusted deps without `--ignore-scripts`; or `.pth` file contains executable code.

### Step 5: Provenance

- Identify release workflows (triggered on `release:` or tag push).
- Check for SBOM generation and signing steps.
- PASS: SBOM produced and artifacts signed. WARN: SBOM produced but not signed (or vice versa). FAIL: no SBOM and no signing in release workflows.

## Output Summary

```markdown
## Supply Chain Audit Report: <path>

### Scan Coverage
- Workflows scanned: <n>
- Lockfiles detected: <list>
- Ecosystems detected: <list>

### Audit Results

| Category | Status | Findings |
|----------|--------|----------|
| Action pinning | PASS / WARN / FAIL | <count> findings |
| Workflow permissions | PASS / WARN / FAIL | <count> findings |
| Lockfile hygiene | PASS / WARN / FAIL | <count> findings |
| Install-time execution | PASS / WARN / FAIL | <count> findings |
| Provenance | PASS / WARN / FAIL | <count> findings |

### Findings (by severity)

#### FAIL (Must Fix)
- [ ] <file>:<line> — <description> — fix with: <`/command` or skill reference>

#### WARN (Should Fix)
- [ ] <file>:<line> — <description> — fix with: <`/command` or skill reference>

#### PASS
- [x] <what passed>

### Top 3 Priority Actions

1. <highest-impact remediation> — `/supply-chain-pin-actions <path>` (dry-run first)
2. <second priority> — <`/command` or skill>
3. <third priority> — <`/command` or skill>
```

## Important Notes

- **Read-only**: this command does not modify any files.
- Use `/supply-chain-pin-actions` to fix mutable action refs.
- Use `/supply-chain-harden-workflow` to apply the hardening playbook to a single workflow.
- Use `/supply-chain-lockfile-check` for narrow lockfile-only health.
- For active incidents, use `/supply-chain-incident <id>` instead.

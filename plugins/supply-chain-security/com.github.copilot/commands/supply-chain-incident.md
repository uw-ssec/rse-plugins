---
description: Walk through supply-chain incident response for an advisory, CVE, GHSA, package name, or campaign name. Engages the supply-chain-incident-responder agent. Performs the 4-point check (lockfile → CI cache → secrets → persistence) and produces a filled incident-report-template.md. Read-only.
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - WebFetch
---

# Supply Chain Incident Response

Walk through structured incident response for a named supply-chain advisory or campaign — enumerate the blast radius, fill out the incident report, and recommend rotation order without modifying any state.

## Arguments

`$ARGUMENTS` — **Required**. One of:

- A CVE or GHSA identifier (`CVE-2024-12345`, `GHSA-xxxx-xxxx-xxxx`).
- A package name with version range (e.g., `axios@<1.6.7`, `chalk@5.3.1`).
- A campaign name (e.g., `Shai-Hulud`, `TeamPCP`, `LiteLLM 1.82.8`).

If no argument is supplied, prompt for one before proceeding.

## Input Handling

**Branch 1: CVE or GHSA identifier**
- Fetch advisory via `WebFetch` from `https://github.com/advisories/<id>` (for GHSAs) or `https://nvd.nist.gov/vuln/detail/<id>` (for CVEs).
- Parse the affected package name, the affected version range, and the exposure window dates.

**Branch 2: Package name with version range**
- Use directly; do not fetch.

**Branch 3: Campaign name**
- Look for a campaign reference at `plugins/supply-chain-security/skills/supply-chain-threat-awareness/references/campaigns/<campaign>.md`.
- If present, load it for affected packages, exposure window, IoCs, and rotation guidance.
- If not present, treat as a freeform query and proceed with best-effort lookup via `WebFetch`.

## 4-Point Check

### 1. Lockfile

Search every detected lockfile for the affected package.

```bash
# Example for npm ecosystem
git grep -nE '"<package-name>"' '**/package-lock.json' '**/yarn.lock' '**/pnpm-lock.yaml'
```

Report each match with file:line and the resolved version. For Python, search `uv.lock`, `poetry.lock`, `pixi.lock`, `conda-lock.yml`. For Rust, `Cargo.lock`. For Go, `go.sum`.

### 2. CI cache

If `gh` CLI is available and the repo is on GitHub:

```bash
gh actions cache list --json key,createdAt,sizeInBytes,ref --limit 100
```

Identify caches created on or after the exposure window start date. Compromised dependencies may persist in CI cache even after lockfile fixes.

### 3. Secrets

Enumerate secrets that may have been exposed to the compromised step:

```bash
gh secret list
gh secret list --env <env>   # per-environment
```

Grep workflows for usage:

```bash
grep -rnE 'secrets\.[A-Z_]+|env:' .github/workflows/
```

Categorize each exposed secret by access type:
- **Registry**: npm tokens, PyPI tokens, Docker Hub PATs.
- **Cloud**: AWS/GCP/Azure keys, OIDC trust relationships.
- **Signing**: Sigstore/cosign keys, GPG keys.

### 4. Persistence

Hunt for installer-implanted artifacts. Ecosystem-specific:

- **npm**: `find node_modules/.bin -newer <date>` to find binaries added during the exposure window. Inspect `.npmrc` for unexpected registry overrides.
- **Python**: `find $(python -c 'import site;print(site.getsitepackages()[0])') -name "*.pth"` — inspect every `.pth` file; benign ones contain only path strings, malicious ones contain executable Python.
- **Cargo**: identify `build.rs` files in installed crates that built after the exposure window via `find ~/.cargo/registry -name build.rs -newer <date>`.

## Action Steps

1. Parse the advisory or campaign name and confirm the affected package(s), version range(s), and exposure window.
2. Run the lockfile check across every detected ecosystem.
3. Run the CI cache check (if `gh` and GitHub are available).
4. Enumerate secrets in scope and categorize by access type.
5. Run the ecosystem-specific persistence artifact hunt.
6. Fill the incident report template — see Output.
7. Recommend rotation order per `plugins/supply-chain-security/skills/supply-chain-incident-response/references/secret-rotation.md`.

## Output

Load the template from:

```
plugins/supply-chain-security/skills/supply-chain-incident-response/assets/incident-report-template.md
```

Produce a filled copy. Save to `incident-<id>-<YYYYMMDD>.md` in the current working directory unless the user supplies an alternate path.

The filled report must contain:

- Advisory identifiers and affected version range.
- Lockfile findings (file:line citations).
- CI cache findings (cache keys built during exposure).
- Secrets in scope, by category and recommended rotation order.
- Persistence artifacts found (or "none observed").
- Recommended next steps with explicit follow-up commands.

## Important Notes

- **Read-only**: this command does not rotate secrets, modify lockfiles, or invalidate caches. It enumerates the work and produces the report; the user runs the rotation/invalidation commands themselves.
- Engages the `supply-chain-incident-responder` agent for runbook judgment calls (severity classification, rotation order, communication templates).
- For tag-hijack incidents, also invoke `/supply-chain-pin-actions` after eradication to lock the workflow against recurrence.
- If `gh` CLI is unavailable, skip Step 3 but note in the report that CI cache must be reviewed manually.

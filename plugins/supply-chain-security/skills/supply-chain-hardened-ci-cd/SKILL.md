---
name: supply-chain-hardened-ci-cd
description: Hardened GitHub Actions release workflow patterns for supply-chain security. Use when reviewing or writing GitHub Actions release workflows (.github/workflows/*.yml). Contains SHA-pinning, OIDC trusted publishing, two-job build/publish split, --ignore-scripts, Pwn Request prevention, deny-by-default permissions, and egress hardening patterns. Triggered by March 2026 TeamPCP campaign that specifically hijacked release tags.
---

# Supply Chain Hardened CI/CD

## GitHub Actions Audit Checklist

Run on every `.github/workflows/*.yml` file reviewed. Flag each failure with its specific line.

- [ ] All `uses:` references pinned to **40-character commit SHAs** — not `@v4`, `@main`, etc.
  - March 2026 TeamPCP campaign specifically hijacked release tags on Trivy, Checkmarx, LiteLLM, Bitwarden CLI, SAP CAP
- [ ] `permissions: {}` at workflow level with per-job opt-in; no job has broader permissions than needed
- [ ] No `pull_request_target` trigger combined with `actions/checkout` of the PR head SHA (Pwn Request — runs with secrets in target repo context)
- [ ] Build and publish steps in **separate jobs**; registry credentials exist only in the publish job
- [ ] `npm ci --ignore-scripts` (or Python equivalent) in install steps — `preinstall`/`postinstall` hooks are the dominant execution vector
- [ ] No long-lived secrets where OIDC Trusted Publishing is available (PyPI, npm)
- [ ] GitHub environment with required reviewers gates the publish job
- [ ] Artifact verified (checksums, provenance) before publication
- [ ] Cache keys scoped to avoid cross-fork poisoning
- [ ] Egress firewall or `harden-runner` with `egress-policy: block` preferred for release jobs
- [ ] SBOM generated for releases; signatures verified (Sigstore, npm provenance)

## Key Hardening Patterns

### SHA-pinning

```yaml
# Bad
- uses: actions/checkout@v4

# Good
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
```

Verify the SHA belongs to the expected tag: `git -C <cloned-actions-repo> tag --points-at <sha>`

### OIDC Trusted Publishing (no long-lived tokens)

```yaml
permissions:
  id-token: write
  contents: read

- uses: pypa/gh-action-pypi-publish@release/v1
  # No TWINE_PASSWORD or API token needed
```

### Two-job split (build / publish)

```yaml
jobs:
  build:
    permissions:
      contents: read
    steps:
      - run: python -m build
      - uses: actions/upload-artifact@...

  publish:
    needs: build
    environment: pypi-release  # requires reviewer approval
    permissions:
      id-token: write
    steps:
      - uses: actions/download-artifact@...
      - uses: pypa/gh-action-pypi-publish@...
```

Registry credentials (OIDC or token) appear **only** in the publish job. The build job has no network write access.

### Deny-by-default permissions

```yaml
permissions: {}  # deny all at workflow level

jobs:
  test:
    permissions:
      contents: read  # minimum needed
```

### Pwn Request prevention

Never combine `pull_request_target` with checkout of the PR head:

```yaml
# Dangerous
on: pull_request_target
steps:
  - uses: actions/checkout@...
    with:
      ref: ${{ github.event.pull_request.head.sha }}  # executes untrusted code with secrets
```

Use `pull_request` (no secrets) or audit all code paths before accessing secrets in `pull_request_target`.

## Findings Format

For each finding: file path, line number, violation type (e.g., "mutable tag reference", "Pwn Request pattern"), and remediation (the exact SHA-pinned replacement or restructured job split).


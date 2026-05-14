# TeamPCP Campaign

**Vector:** GitHub release tag hijacking — replaced release artifacts after legitimate tagging.
**Targets (March 2026):** Trivy, Checkmarx, LiteLLM, Bitwarden CLI, SAP CAP.
**Key finding:** GitHub Actions workflows pinned to `@v3` or `@latest` were silently updated to malicious commits.

## Attack mechanics

1. Attacker compromises maintainer access to the action's repository.
2. Force-pushes the existing release tag (`v3`) to point at a malicious commit, OR releases a new patch under an existing major-tag alias (`@v3` resolves to the new tag).
3. Downstream workflows using `uses: org/action@v3` pull the malicious commit on next run.
4. Payload typically: exfiltrates GitHub Actions secrets, OIDC tokens, registry credentials.

## Indicators of exposure

- Any `.github/workflows/*.yml` uses `@v<n>`, `@main`, `@master`, or `@latest` for an affected action.
- A workflow run after the tag mutation completed using the hijacked action.

## Containment checklist

- [ ] Audit every `uses:` ref across `.github/workflows/*.yml`.
- [ ] For each mutable ref, resolve its current SHA and compare against last known-good SHA.
- [ ] Rotate every secret exposed to the affected workflow runs.
- [ ] Pin every `uses:` to a 40-char SHA going forward.

## References

- `supply-chain-hardened-ci-cd` skill (SHA-pinning patterns)
- `supply-chain-incident-response/references/runbook-tag-hijack.md`

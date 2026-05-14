# Runbook: GitHub Action Release Tag Hijacking (TeamPCP-style)

## Pattern

An attacker with write access to an action's repo (via compromised maintainer credentials, malicious contributor merge, or repo takeover) mutates an existing release tag — or publishes a new patch under a floating major-tag alias like `@v3` — to point at a malicious commit. Every workflow that pinned to the tag (rather than a 40-char SHA) now runs attacker code on its next execution, with whatever secrets and OIDC permissions the action had in scope. Detection requires comparing the tag's current SHA against the last known-good SHA from a successful run.

## Audit Step

For each `uses:` reference in workflows, resolve the tag's current SHA and compare against the SHA observed in a recent known-good run.

```bash
# Enumerate all uses: refs (action@ref form)
grep -hoE 'uses: [a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+@[^[:space:]]+' .github/workflows/*.yml | sort -u

# For each ref, resolve current SHA via gh api
for ref in $(grep -hoE 'uses: [a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+@[^[:space:]]+' .github/workflows/*.yml | sort -u); do
  spec="${ref#uses: }"
  action="${spec%@*}"
  tag="${spec#*@}"
  # 40-char hex = already SHA-pinned, immune to tag mutation
  if [[ "$tag" =~ ^[a-f0-9]{40}$ ]]; then
    echo "PINNED $spec"
  else
    sha=$(gh api "repos/$action/git/refs/tags/$tag" --jq '.object.sha' 2>/dev/null \
       || gh api "repos/$action/commits/$tag" --jq '.sha' 2>/dev/null)
    echo "FLOATING $spec -> $sha"
  fi
done
```

Compare each `FLOATING` SHA against the SHA recorded in the last successful workflow run (see Workflow Run Forensics below). Mismatch = potential hijack, treat as EXPOSED until proven otherwise. See `/supply-chain-pin-actions` for the SHA-pinning fix.

## Workflow Run Forensics

For each workflow that used the suspect action, enumerate runs during the exposure window and identify which secrets were in scope.

```bash
# Runs of a given workflow in the window
gh run list --workflow=<file>.yml --created ">=<exposure-start>" \
  --json databaseId,createdAt,headSha,conclusion,url

# For a specific run, list the secrets referenced in its job env/steps
gh api "repos/<owner>/<repo>/actions/runs/<run-id>/jobs" \
  --jq '.jobs[] | {name, steps: [.steps[] | .name]}'

# Dump the workflow file as it existed at that commit (to see env:/with: secrets)
gh api "repos/<owner>/<repo>/contents/.github/workflows/<file>.yml?ref=<headSha>" \
  --jq '.content' | base64 -d
```

Each run in the window where the action could have read secrets is a separate EXPOSED instance for the incident report.

## Secret Rotation Prioritization

The action only had access to whatever was passed via `env:`, `with:`, or available through `${{ secrets.* }}` and OIDC. Rotate in this order:

1. **Registry publishing tokens** (PyPI, npm, crates.io, Docker Hub) — attacker can publish malicious successor versions immediately.
2. **OIDC-issued cloud credentials** (AWS, GCP, Azure via federated identity) — short-lived but may already be in use; revoke active sessions.
3. **Signing keys** (cosign, GPG, Sigstore identity) — attacker can forge attestations on hijacked artifacts.
4. **Repo write tokens** (PATs, deploy keys, GH App installations) — used to escalate persistence into the repo itself.

Full procedures in `secret-rotation.md`.

## Hardening Going Forward

- Replace every floating tag with a 40-char SHA: `/supply-chain-pin-actions` (dry-run first).
- Add deny-by-default permissions to every workflow: `/supply-chain-harden-workflow`. An action that can't read secrets can't exfiltrate them on hijack.
- Enable Dependabot for `package-ecosystem: github-actions` so SHA bumps land via reviewable PRs.
- Cross-link to the `supply-chain-hardened-ci-cd` skill for end-to-end pipeline lockdown (minimal permissions, OIDC publishing, no PRs with secret access from forks).

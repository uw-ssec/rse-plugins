---
description: Apply the supply-chain hardening playbook to a single GitHub Actions workflow file — deny-by-default permissions, per-job opt-in, two-job build/publish split where applicable, --ignore-scripts on install steps, harden-runner injection, and environment-gated publish job. Dry-run by default — pass --apply to write. Refuses on workflows too divergent from a recognizable shape.
user-invocable: true
allowed-tools:
  - Read
  - Edit
  - Bash
---

# Supply Chain Harden Workflow

Apply a recognized hardening playbook to a single GitHub Actions workflow — deny-by-default permissions, per-job opt-in, ignore-scripts on installs, harden-runner injection, and environment gates on publish jobs.

## Arguments

- **First positional** (required): path to a single workflow file (e.g., `.github/workflows/release.yml`).
- `--apply`: write changes to disk. Without this flag the command runs in **dry-run mode** and only prints the diff with rationale.

Examples:
- `/supply-chain-harden-workflow .github/workflows/release.yml`
- `/supply-chain-harden-workflow .github/workflows/release.yml --apply`

## Hardening Playbook

For each transformation, evaluate applicability before proposing the change.

1. **Deny-by-default permissions** — add `permissions: {}` at the workflow level if absent. Then add per-job `permissions:` blocks specifying only the scopes that job needs (`contents: read`, `id-token: write`, `packages: write`, etc.). Eliminates the broad `GITHUB_TOKEN` defaults.

2. **Two-job build/publish split** — if the workflow has a single job that both builds and publishes artifacts, **refuse the split** and recommend manual restructure. Artifact handoff between jobs is structural and too risky to automate. Provide the recommended shape (build job uploads artifact; publish job consumes via `actions/download-artifact` and uses OIDC).

3. **`--ignore-scripts` on npm installs** — for `run: npm install ...` or `run: npm ci ...` steps, add `--ignore-scripts` if not already present. Prevents `preinstall`/`postinstall`/`prepublish` lifecycle hooks from compromised dependencies.

4. **`harden-runner` injection** — add as the first step of every job:

   ```yaml
   - uses: step-security/harden-runner@<sha>  # <version>
     with:
       egress-policy: audit
   ```

   Start with `audit` so legitimate egress is observed before tightening. The user should manually upgrade to `block` after one or two clean CI runs.

5. **Environment gate on publish jobs** — for any job using `pypa/gh-action-pypi-publish`, `npm publish`, or other registry-publishing actions, add an `environment:` field if absent. Suggest a name like `<registry>-release`. Tell the user to configure reviewer requirements in repo Settings → Environments after applying.

## Refusal Conditions

The command refuses (and always explains why) when:

- A single job both builds artifacts and publishes them — refuse the split; the user must manually restructure into two jobs with artifact handoff.
- A workflow uses a local action (`uses: ./.github/actions/...`) with embedded scripts that cannot be statically analyzed — refuse hardening of that step and note it in the output.
- The workflow file is not valid YAML — refuse and recommend running `yamllint` first.

## Action Steps

1. Read and YAML-parse the workflow file. If parsing fails, refuse.
2. For each transformation in the Playbook, evaluate applicability and either prepare an edit or record a refusal with its reason.
3. Build a unified diff from the prepared edits.
4. Print the diff plus a numbered "what this changes and why" rationale section.
5. If `--apply` was passed: edit the file in place; print the post-apply result.

## Output (dry-run)

```
## Harden Workflow — Dry Run: .github/workflows/release.yml

### Changes proposed
(unified diff)

### Rationale
1. Added `permissions: {}` at workflow level — deny-by-default.
2. Added `permissions: { contents: read }` to `build` job — minimum needed.
3. Added `permissions: { id-token: write, contents: read }` to `publish` job — OIDC token + checkout.
4. Added `--ignore-scripts` to `npm ci` step — prevents preinstall/postinstall script execution from compromised deps.
5. Added `step-security/harden-runner` as first step of each job — egress audit.
6. Added `environment: pypi-release` to `publish` job — gates with reviewer approval (configure in repo settings).

### Refusals
- None.

### Apply
Run with --apply to write changes.
```

## Important Notes

- **Default is dry-run** — `--apply` is required to write.
- This command applies a playbook; for one-off cases, use the `supply-chain-hardened-ci-cd` skill directly.
- For SHA-pinning of `uses:` refs, run `/supply-chain-pin-actions` separately — different concern, different refusal conditions.
- After applying, configure the GitHub Environment in repo Settings → Environments to add reviewer requirements; without that, the `environment:` field has no enforcement.
- The `harden-runner` ref should itself be SHA-pinned; run `/supply-chain-pin-actions` after this command to lock it down.

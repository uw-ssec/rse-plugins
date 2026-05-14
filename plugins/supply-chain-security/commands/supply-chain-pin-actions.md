---
description: Convert mutable GitHub Actions refs (@v4, @main, @latest) in .github/workflows/*.yml to 40-char commit SHAs with trailing tag comments. Dry-run by default — pass --apply to write. Refuses to apply when a SHA cannot be uniquely resolved or the ref is a branch name.
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Edit
  - Bash
  - WebFetch
---

# Supply Chain Pin Actions

Resolve every mutable `uses:` reference in GitHub Actions workflow files to an immutable 40-character commit SHA, with the original tag preserved as a trailing comment for human readability.

## Arguments

- **First positional** (optional): path to a single workflow file or a directory of workflow files. Defaults to `.github/workflows/`.
- `--apply`: write changes to disk. Without this flag the command runs in **dry-run mode** and only prints the diff.

Examples:
- `/supply-chain-pin-actions` — dry-run across `.github/workflows/`
- `/supply-chain-pin-actions .github/workflows/release.yml` — dry-run single file
- `/supply-chain-pin-actions --apply` — write changes after review

## Resolution Algorithm

For each line matching `uses: <owner>/<repo>@<ref>`:

1. **Already pinned**: if `<ref>` is exactly 40 hex characters, skip (already immutable).

2. **Tag ref**: if `<ref>` matches `v\d` or `v\d+\.\d+(\.\d+)?` (e.g., `v4`, `v4.2.2`), resolve via:

   ```bash
   gh api repos/<owner>/<repo>/git/refs/tags/<ref> --jq '.object.sha'
   ```

   If the returned object's `type` is `"tag"` (annotated tag), dereference one level to the underlying commit:

   ```bash
   gh api repos/<owner>/<repo>/git/tags/<sha> --jq '.object.sha'
   ```

3. **Branch ref**: if `<ref>` is `main`, `master`, `latest`, `release/v1`, or any name that does not match the tag pattern, **refuse to apply** — branch refs are mutable by design; the user must pick a tag.

4. **Annotation**: append the original ref as a trailing comment:

   ```
   uses: <owner>/<repo>@<sha>  # <ref>
   ```

## Refusal Conditions

The command refuses (and always explains why) when:

- `<ref>` is a branch name rather than a tag — user must pick a tag.
- A tag resolves to multiple SHAs (rare; usually a force-push or alias) — manual review required.
- The action repo is no longer accessible (404 from `gh api`) — manual review required.
- The `uses:` line is inside a comment block (starts with `#`) — already disabled.

## Action Steps

1. Glob workflow files under the target path.
2. For each file, parse all `uses:` lines.
3. For each ref, run the Resolution Algorithm; collect SHA resolutions and refusal reasons.
4. Build a unified diff per file showing the proposed change.
5. Print the combined diff plus a summary.
6. If `--apply` was passed:
   - For each file with non-refusal changes, edit in place.
   - Print: `<n> files modified; <n> refs pinned; <n> refs refused`.

## Output (dry-run mode)

```
## Pin Actions — Dry Run

### .github/workflows/release.yml

--- a/.github/workflows/release.yml
+++ b/.github/workflows/release.yml
@@ -10,7 +10,7 @@
       - uses: actions/checkout@v4
+      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
@@ -15,7 +15,7 @@
-      - uses: pypa/gh-action-pypi-publish@release/v1
+REFUSED: pypa/gh-action-pypi-publish@release/v1 — branch ref. Pick a tag (e.g., v1.10.3) and rerun.

### Summary
- 5 refs would be pinned across 3 files.
- 1 ref refused (branch ref). Resolve manually before applying.

### Apply
Run with --apply to write changes.
```

## Output (apply mode)

```
## Pin Actions — Applied

### .github/workflows/release.yml
- actions/checkout@v4 -> 11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2

### Summary
- 5 refs pinned across 3 files.
- 1 ref refused (branch ref). Resolve manually.

Verify the diff: git diff .github/workflows/
Commit when ready: git commit -am "ci: SHA-pin GitHub Actions"
```

## Important Notes

- **Default is dry-run** — `--apply` is required to write.
- Always review the diff before applying.
- The trailing tag comment is best-effort; it preserves the human-readable version next to the SHA.
- For full hardening (permissions, two-job split, harden-runner, environment gates), follow up with `/supply-chain-harden-workflow`.
- If `gh` CLI is not authenticated, the command will fail at SHA resolution — run `gh auth login` first.

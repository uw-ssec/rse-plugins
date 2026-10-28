---
name: merging-pull-requests
description: >-
  Use when an approved pull request should land — checking CI and conflict
  status first, picking squash or rebase, then deleting the merged branch and
  syncing the local clone. Triggers: merge this PR, land this, squash and merge,
  merge and clean up, is this ready to merge, ship this PR.
---

# Merging Pull Requests

Landing a change is irreversible in practice: the branch is deleted, the history
is rewritten into the base, and CI results become the record. Check before you
land, and never retry a failed merge destructively.

## Checklist

1. **Identify** — which PR
2. **Gate** — CI, conflicts, approvals
3. **Protect** — local uncommitted work
4. **Land** — with the repo's strategy
5. **Sync** — base branch and branch deletion
6. **Verify** — merged, closed, gone

## 1. Identify

```sh
gh pr view --json number,title,state,headRefName,baseRefName    # current branch
gh pr view <number> --json number,title,state,headRefName       # explicit
```

If the request names no PR and the current branch has none, list open PRs and
ask which one rather than guessing.

## 2. Gate

```sh
gh pr view <number> --json state,mergeable,mergeStateStatus,reviewDecision,statusCheckRollup
```

Read each field and act:

| Signal | Action |
| --- | --- |
| `state` is not `OPEN` | Stop — already merged or closed |
| `mergeable` is `CONFLICTING` | Stop. Report the conflict; do not attempt resolution here |
| failing checks in `statusCheckRollup` | Name the failing checks and ask before proceeding |
| `reviewDecision` is `CHANGES_REQUESTED` | Stop — unresolved review feedback |
| `reviewDecision` is `REVIEW_REQUIRED` | Say so and ask; branch protection may reject the merge anyway |

Never merge past a failing check without the user saying so in that exchange.

## 3. Protect local work

```sh
git status
```

Stash anything uncommitted before switching branches, and remember that you did:

```sh
git stash push -m "pre-merge stash"
```

## 4. Land

```sh
gh pr merge <number> --squash --delete-branch
```

Default to `--squash` unless the repo's history says otherwise — check
`git log --oneline -20` on the base for merge commits before deciding. Use
`--merge` or `--rebase` only when the user asks or the history clearly uses it.

If the merge fails, report the error and stop. Do not retry with a different
strategy, and do not attempt to force it.

## 5. Sync

```sh
BASE=$("${CLAUDE_PLUGIN_ROOT}/scripts/default-branch.sh")
git checkout "$BASE"
git pull origin "$BASE"
git fetch --prune
git branch -d <head-branch>        # safe delete only
git stash pop                      # only if step 3 stashed
```

`git branch -d` refuses to delete unmerged work. That refusal is a safety check,
not an obstacle — if it fires after a squash merge, the commits are in the base
under a new identity, so confirm that before overriding.

## 6. Verify

```sh
gh pr view <number> --json state,mergedAt
git branch -a --list '*<head-branch>*'
```

The PR should read `MERGED`; the branch listing should be empty. Report the PR
number, where it landed, and that the branch is gone from both sides. If a
linked issue did not auto-close, say so.

## Rules

- Never force-delete a branch with `-D` during cleanup.
- Always restore a stash you created.
- Never merge a PR with conflicts — that resolution belongs on the branch.
- If anything fails mid-sequence, stop and report state. Half-finished cleanup
  is recoverable; a destructive retry is not.

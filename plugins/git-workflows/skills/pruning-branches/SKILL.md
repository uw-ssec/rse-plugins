---
name: pruning-branches
description: >-
  Use when the branch list has grown unwieldy — categorizing every local and
  remote ref as merged, stale, orphaned, or active, then deleting the dead ones
  with confirmation. Triggers: clean up branches, delete merged branches, prune
  stale branches, my branch list is a mess, remove old branches, tidy up refs.
---

# Pruning Branches

Deletion is the one git operation with no undo button in the UI. Categorize
first, show the user, then delete only what they confirmed.

## Checklist

1. **Refresh** — fetch so the categories reflect reality
2. **Categorize** — every ref into exactly one bucket
3. **Present** — a table, grouped, with ages
4. **Confirm** — explicitly, per category
5. **Delete** — safe flags only
6. **Verify** — show what remains

## 1. Refresh and gather

Stale remote refs produce wrong categories, so fetch first:

```sh
git fetch --prune
BASE=$("${CLAUDE_PLUGIN_ROOT}/scripts/default-branch.sh")
```

Then gather in parallel:

```sh
git branch                                   # local
git branch -r | grep -v HEAD                 # remote
git branch --merged "$BASE"                  # merged into base
git for-each-ref --sort=-committerdate \
  --format='%(refname:short) %(committerdate:relative) %(upstream:track)' refs/heads/
```

## 2. Categorize

| Category | Definition |
| --- | --- |
| **Merged** | Appears in `git branch --merged <base>` |
| **Stale** | Newest commit older than 30 days and not merged |
| **Orphaned local** | Upstream shows `[gone]` — the remote was deleted |
| **Orphaned remote** | A remote ref no local branch tracks |
| **Active** | Recent commits, not merged |
| **Protected** | Never a candidate — see below |

**Protected refs** — never offer these for deletion:

- The default branch, whatever it is called
- `main` and `master`, always
- The currently checked-out branch
- Any branch named in `git config --get-all branch.protected`, plus anything the
  user names in the request

A squash-merged branch does **not** appear as merged, because the squash created
a new commit. Check whether its changes are in the base before treating it as
unmerged work.

## 3. Present

Show a table grouped by category: branch name, last commit age, local/remote
presence, and category. The user should be able to spot a mistake in one read.
If nothing qualifies, say so and stop.

## 4. Confirm

Never act on an ambiguous instruction. Ask which categories to clean, list the
exact branches that will be deleted, and wait. "All" means all *categories
offered*, never the protected refs.

## 5. Delete

```sh
git branch -d <name>                    # local; refuses unmerged work
git push origin --delete <name>         # remote
git fetch --prune                       # after remote deletions
```

`-d` refusing to delete is a safety check doing its job. Report the refusal,
say what unmerged commits exist, and ask before `-D`. Force-delete needs its own
explicit confirmation naming that branch — a blanket "yes, clean it up" earlier
does not cover it.

## 6. Verify

```sh
git branch -a
```

Show what was deleted and what remains, and confirm every protected ref is still
present. If a deletion failed partway, name which ones succeeded — a partial run
the user cannot see is worse than a failed one.

## Rules

- Never delete the default branch, `main`, `master`, or the current branch.
- Never `-D` without explicit per-branch confirmation.
- Always `git fetch --prune` before categorizing and after remote deletions.
- Show before deleting. Always.

---
name: pushing-branches
description: >-
  Use when local commits need to reach the remote — setting upstream tracking on
  a first publish, previewing what will be sent, and handling a rejected push.
  Refuses force-writes to shared history. Triggers: push this, push my work,
  push to origin, send this upstream, set upstream, my push was rejected.
---

# Pushing Branches

Publishing is the moment work stops being yours alone. Show the user what is
about to leave the machine before it leaves.

## Checklist

1. **Inspect** — branch, tracking state, working tree
2. **Preview** — the exact commits that will be sent
3. **Publish** — with or without `-u`, depending on tracking
4. **Verify** — confirm the remote now holds what you sent

## 1. Inspect

```sh
git status
git branch --show-current
git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null
```

The third command fails when no upstream is set — that is the signal for `-u`,
not an error.

If the working tree is dirty, say what is uncommitted and ask: commit it first
(see `git-workflows:committing-changes`), or publish only what is already
recorded? Do not decide silently.

## 2. Preview

With an upstream:

```sh
git log --oneline @{u}..HEAD
```

Without one, show everything that diverges from the default branch:

```sh
BASE=$("${CLAUDE_PLUGIN_ROOT}/scripts/default-branch.sh")
git log --oneline "$BASE"..HEAD
```

Never assume the default branch is `main`. `scripts/default-branch.sh` resolves
it from `origin/HEAD`, the remote, or the GitHub API, and fails loudly rather
than guessing.

List the commits for the user. If the list is empty, say the remote is already
current and stop — there is nothing to do.

## 3. Publish

```sh
git push -u origin "$(git branch --show-current)"   # first publish
git push                                            # already tracking
```

## 4. Verify

```sh
git status -sb
```

The branch should report as up to date with its upstream, with no ahead count.
Report the branch name and how many commits went out.

## When the push is rejected

A rejection means the remote moved. Do not reach for `--force`.

1. Show the user the rejection message verbatim.
2. Fetch and inspect: `git fetch origin && git log --oneline HEAD..@{u}`
3. Recommend `git pull --rebase` when your commits are unpublished, or a merge
   when others may have built on them.
4. Ask before running either. A rebase rewrites commit identity.

## Rules

- Never use `--force` or `-f` unless the user explicitly asks for it in that
  exchange. Prior approval does not carry forward.
- When force is explicitly requested, use `--force-with-lease`, which refuses to
  clobber commits you have not seen.
- Refuse outright to force-write the default branch or any protected branch.
  Explain why and stop; do not offer a workaround.
- Never push in a detached HEAD state. Say so and stop.

---
name: using-git-workflows
description: >-
  Use when about to touch version control or GitHub and it is not obvious which
  workflow skill applies, or when one request spans several steps. Routes to the
  right skill and carries the safety rules shared by all of them. Triggers on:
  which git skill, ship this work, take this from branch to merged, what is the
  git workflow here.
---

# Using Git Workflows

This plugin holds nine skills covering the path from an edited file to a merged,
released, documented change. This meta-skill makes you *use* the right one.

<EXTREMELY-IMPORTANT>
If there is even a 1% chance one of these skills applies to what you are about to
do, invoke it before acting — before running `git commit`, before `gh pr create`,
before deleting a branch.

These operations write to shared history. "It's a small commit" is exactly the
case where the convention slips and the secret gets staged.
</EXTREMELY-IMPORTANT>

## Instruction priority

1. **The user's explicit instructions** — highest.
2. **These skills** — override default behavior where they conflict.
3. **The default system prompt** — lowest.

"Just commit it, skip the ceremony" from the user wins. But "commit this" states
*what* to do — it is not permission to skip the secret screen or invent a scope.

## Choosing a skill

```text
Changes ready to record in history?      → committing-changes
Commits need to reach the remote?        → pushing-branches
Branch ready for review?                 → opening-pull-requests
PR approved and ready to land?           → merging-pull-requests
Work that needs tracking, not doing?     → filing-issues
A choice worth preserving with its why?  → recording-decisions
Branch list full of dead refs?           → pruning-branches
Time to cut a version?                   → publishing-releases
Shipped work needs written reference?    → documenting-work
```

Invoke by fully-qualified id: `git-workflows:committing-changes`.

## Shared helper

`${CLAUDE_PLUGIN_ROOT}/scripts/default-branch.sh [remote]` prints the repository's
default branch, resolving it from `origin/HEAD`, the remote, or the GitHub API
before falling back to a branch that actually exists. It exits non-zero rather
than guessing. Every skill that needs a base branch calls it instead of
re-deriving one inline.

## Common chains

**Ship a change** — `committing-changes` → `pushing-branches` →
`opening-pull-requests` → *review* → `merging-pull-requests`

**Cut a release** — `merging-pull-requests` → `documenting-work` →
`publishing-releases`

**Housekeeping** — `pruning-branches`, then `filing-issues` for whatever the
cleanup surfaced.

Right-sizing means picking the minimal matching skill, not running the whole
chain. It never means zero skills for an operation that writes history.

## Distinctions that get confused

| Situation | Skill | Not |
| --- | --- | --- |
| Capturing *why* an option won | `recording-decisions` | `documenting-work` |
| Reference material kept beside the code | `documenting-work` | `recording-decisions` |
| A defect or a task to be done | `filing-issues` | `recording-decisions` |
| Deleting one merged branch after a PR | `merging-pull-requests` | `pruning-branches` |
| Deleting many accumulated dead refs | `pruning-branches` | `merging-pull-requests` |

## Rules that hold across every skill

**Discover, never assume.** Resolve the default branch with
`${CLAUDE_PLUGIN_ROOT}/scripts/default-branch.sh`, take commit scopes from
`git log`, and read the merge strategy off the repo in front of you. `main` is a
guess; a scope vocabulary imported from another project is noise.

**Show before you write.** Preview the commits, the branch deletions, the tag.
The user should be able to stop you before an irreversible step, not after.

**Confirm irreversible steps in the exchange where they happen.** Pushing a tag,
force-writing, force-deleting a branch. Approval does not carry forward from an
earlier turn.

**Stage and delete by name.** Never `git add -A`, never a wildcard deletion.

**Screen for secrets** before anything enters history. Rewriting published
history to remove a key is a bad day for everyone with a clone.

**Bodies go in files.** Issue, PR, discussion, and release bodies contain
backticks, `$`, and tables that shell heredocs mangle. Use `--body-file` or
`--notes-file`.

**Verify with evidence, then report.** Re-read what you created with
`gh ... --json` or `git log`, and say what you checked. If something could not
be verified, say that instead of omitting it.

**No AI attribution.** Never add `Co-Authored-By` trailers, "Generated with"
lines, or model names to commit messages, PR bodies, issues, discussions, tags,
or release notes.

# git-workflows

Git and GitHub workflow skills for Research Software Engineers — from an edited
file to a merged, released, documented change, with the same conventions every
time.

The behavior lives in **skills**, so it applies whether you type `/commit` or
just say "commit this". The slash commands are thin wrappers that delegate to
the skill of the same name.

## Skills

| Skill | Use when |
| --- | --- |
| `using-git-workflows` | Unsure which skill applies, or the request spans several steps |
| `committing-changes` | Changes are ready to record in history |
| `pushing-branches` | Local commits need to reach the remote |
| `opening-pull-requests` | A branch is ready for review |
| `merging-pull-requests` | An approved PR should land |
| `filing-issues` | Work needs tracking rather than doing |
| `recording-decisions` | A choice and its rationale should outlive the chat |
| `pruning-branches` | The branch list has filled with dead refs |
| `publishing-releases` | It is time to cut a version |
| `documenting-work` | Shipped work needs written reference material |

## Commands

| Command | Delegates to |
| --- | --- |
| `/commit` | `committing-changes` |
| `/push` | `pushing-branches` |
| `/create-pr` | `opening-pull-requests` |
| `/merge-pr` | `merging-pull-requests` |
| `/create-issue` | `filing-issues` |
| `/create-discussion` | `recording-decisions` |
| `/clean-branches` | `pruning-branches` |
| `/release` | `publishing-releases` |
| `/docs` | `documenting-work` |

## Shared helper

`scripts/default-branch.sh [remote]` prints the repository's default branch. It
tries `origin/HEAD`, then the remote, then the GitHub API, then a branch that
demonstrably exists — and exits non-zero rather than guessing. Skills call it
instead of assuming `main`, which is wrong in any repo using `master`, `trunk`,
or a release branch.

## Typical chains

**Ship a change**

```text
/commit → /push → /create-pr → review → /merge-pr
```

**Cut a release**

```text
/merge-pr → /docs → /release
```

## What these skills will not do

They are deliberately conservative about operations that cannot be undone:

- No `git add -A` or `git add .` — files are staged by name, after a screen for
  credentials, build output, and OS droppings
- No force-push without an explicit request in that exchange, and never to a
  protected branch
- No `git branch -D` without per-branch confirmation
- No merge past failing checks or unresolved review feedback without a decision
  from you
- No tag pushed before you confirm

## Assumptions

- `git` and the [GitHub CLI](https://cli.github.com/) (`gh`), authenticated
- Conventional commit messages, unless the repo's own history says otherwise
- The default branch is **discovered**, never assumed to be `main`

Nothing here is specific to one project. Commit scopes come from the repo's own
log, the docs build comes from whichever docs system the repo actually uses, and
release artifacts come from what the project actually ships.

## Requirements

`gh` needs `repo` scope for issues, pull requests, and releases, plus
`read:discussion` and `write:discussion` for `/create-discussion`. Check with
`gh auth status`.

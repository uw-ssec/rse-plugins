---
name: opening-pull-requests
description: >-
  Use when a finished branch needs to be proposed for review — drafting the
  title and summary from every commit on the branch, writing a test plan,
  linking the issue it closes, and requesting reviewers. Triggers: open a PR,
  create a pull request, put this up for review, draft a PR description, PR this
  branch, request review from someone.
---

# Opening Pull Requests

The description is the reviewer's entry point. Write it from the whole branch,
not from the last commit — the reviewer is reading the diff against the base,
and that is what the summary must explain.

## Checklist

1. **Gather** — branch state and every commit under review
2. **Resolve** — uncommitted work and an unpublished branch
3. **Draft** — title, summary, changes, test plan
4. **Open** — with reviewers and issue linkage
5. **Verify** — read the created PR back

## 1. Gather

Run in parallel, deriving the base rather than assuming it:

```sh
BASE=$("${CLAUDE_PLUGIN_ROOT}/scripts/default-branch.sh")
git status
git branch --show-current
git log --oneline "$BASE"..HEAD      # every commit under review
git diff "$BASE"...HEAD --stat       # three dots: the diff a reviewer sees
```

Use `...` for the diff. Two dots include changes the base picked up since you
branched, which are not yours to explain.

## 2. Resolve blockers

- **Uncommitted changes** — ask whether to commit them first
  (`git-workflows:committing-changes`) or open the PR without them.
- **Unpublished branch** — publish it (`git-workflows:pushing-branches`) before
  opening; `gh` cannot open a PR for a branch the remote has never seen.
- **On the base branch** — stop. A PR from the base to itself is not a thing.
  Offer to move the commits onto a new branch.

## 3. Draft

**Title** — conventional commit format, under 70 characters, covering the branch
as a whole. If the branch name carries a hint (`feat/`, `fix/`), it is usually
the right type.

**Body** — write to a file, never inline. Bodies contain backticks, `$`, and
tables that a shell heredoc will mangle:

```markdown
## Summary

<1-3 bullets: what changed and why it was worth doing>

## Changes

<specific changes, grouped by area when the branch touches several>

## Test plan

- [ ] <a specific thing a reviewer can actually run or check>
- [ ] <another>

Closes #N
```

The test plan is the part reviewers rely on and the part most often padded.
"Tests pass" is not a test plan. Name the command, the file, or the behavior to
exercise. Omit any section that would be filler — an empty *Changes* heading is
worse than no heading.

## 4. Open

```sh
gh pr create --base "$BASE" \
  --title "type(scope): description" \
  --body-file <scratchpad>/pr-body.md \
  --reviewer <login> --assignee <login>
```

Add `--draft` when the work is still moving. Reviewers must have read access to
the repo — a login without it makes the whole command fail, so if `gh` rejects a
reviewer, open the PR first and report the reviewer problem separately rather
than dropping the PR.

## 5. Verify

```sh
gh pr view --json number,title,url,isDraft,reviewRequests,assignees
```

Confirm the title, the reviewers, and the issue link all took. Return the URL.
If a requested reviewer is missing from the response, say so — silently opening
a PR nobody was asked to review is the failure mode worth catching here.

## Rules

- Never open a PR from the default branch into itself.
- Always include a test plan with concrete, checkable items.
- Link the issue with `Closes #N` when one exists, so the merge closes it.
- Never add `Co-Authored-By` trailers, AI attribution, or "Generated with" lines
  to PR titles or bodies.

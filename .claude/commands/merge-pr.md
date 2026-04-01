Merge a pull request and clean up branches.

## Arguments

$ARGUMENTS — PR number or URL (optional, defaults to current branch's PR)

## Instructions

1. Determine the PR:
   - If `$ARGUMENTS` is provided, use it as the PR number or URL
   - If not, find the PR for the current branch: `gh pr view --json number,title,state,headRefName`

2. Check PR status:
   - `gh pr view <number> --json state,mergeable,mergeStateStatus,statusCheckRollup,title,headRefName`
   - If checks are failing, warn the user and ask whether to proceed
   - If there are merge conflicts, tell the user and stop

3. Check for local uncommitted changes:
   - `git status`
   - If there are unstaged changes, stash them before proceeding: `git stash`

4. Merge the PR:
   ```bash
   gh pr merge <number> --squash --delete-branch
   ```
   Use `--squash` by default (consistent with this repo's history).

5. Clean up locally:
   - Switch to main if not already: `git checkout main`
   - Pull the merged changes: `git pull origin main`
   - Prune stale remote refs: `git fetch --prune`
   - Delete the local branch if it still exists: `git branch -d <branch-name>`
   - If changes were stashed, restore them: `git stash pop`

6. Verify cleanup:
   - `git branch -a | grep <branch-name>` to confirm branch is gone everywhere

7. Confirm: "PR #N merged into main. Branch `<name>` deleted locally and remotely."

## Rules

- Default merge strategy is `--squash` (produces clean linear history)
- If user asks for a merge commit, use `--merge` instead
- If user asks for rebase, use `--rebase` instead
- NEVER force-delete branches (`-D`), use `-d` which is safe
- Always restore stashed changes after merge
- If the merge fails, do NOT retry destructively — report the error

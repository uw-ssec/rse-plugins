Push the current branch to the remote repository.

## Instructions

1. Run `git status` to check:
   - Current branch name
   - Whether there are uncommitted changes (warn the user if so)
   - Whether the branch tracks a remote
2. Run `git log --oneline origin/$(git branch --show-current)..HEAD 2>/dev/null` to see unpushed commits. If the remote branch doesn't exist yet, show all commits since diverging from `main`.
3. Show the user what will be pushed (branch name + commit list).
4. Push:
   - If the branch has no upstream yet: `git push -u origin <branch-name>`
   - If it already tracks a remote: `git push`
5. Confirm success.

## Rules

- NEVER force push (`--force`, `-f`) unless the user explicitly asks
- NEVER force push to `main` or `master` — warn the user and refuse
- If there are uncommitted changes, ask whether to commit first (using /commit conventions) or push what's already committed
- If push is rejected due to remote changes, suggest `git pull --rebase` and ask before proceeding

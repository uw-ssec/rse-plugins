---
description: Open a pull request for the current branch with a test plan
user-invocable: true
---

Use the `git-workflows:opening-pull-requests` skill to handle this request.

Arguments (optional title, reviewers, or base branch): $ARGUMENTS

If no arguments were provided, draft the pull request from every commit on the branch and ask who should review before opening.

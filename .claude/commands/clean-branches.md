Clean up local and remote git branches.

## Arguments

$ARGUMENTS — optional: "all", "stale", "merged", or a specific branch name. If omitted, prompt the user.

## Instructions

1. Run these commands in parallel to gather branch information:
   - `git branch` (local branches)
   - `git branch -r` (remote branches, exclude HEAD)
   - `git branch --merged main` (branches merged into main)
   - `git for-each-ref --sort=-committerdate --format='%(refname:short) %(committerdate:relative) %(upstream:track)' refs/heads/` (local branches with age and tracking status)

2. Categorize each branch (excluding `main` and `feedback-screenshots`):

   | Category | Definition |
   |----------|-----------|
   | **Merged** | Branch is in `git branch --merged main` output |
   | **Stale** | Last commit is older than 30 days |
   | **Orphaned remote** | Remote branch exists but no local branch tracks it |
   | **Orphaned local** | Local branch exists but remote is gone (`[gone]` tracking status) |
   | **Active** | Has recent commits and is not merged |

3. If `$ARGUMENTS` is empty or unclear:
   - Display a summary table of all branches grouped by category with branch name, last commit age, and local/remote status
   - Ask the user which categories to clean: merged, stale, orphaned, or all
   - Wait for the user's response before proceeding

4. If `$ARGUMENTS` specifies a category or "all":
   - Show the list of branches that will be deleted
   - Ask for confirmation before proceeding

5. Delete branches:
   - Local branches: `git branch -d <name>` (safe delete, merged only) or `git branch -D <name>` (if user confirms force delete for unmerged)
   - Remote branches: `git push origin --delete <name>`
   - Run `git fetch --prune` after remote deletions

6. Confirm results: show what was deleted and what remains.

## Rules

- NEVER delete `main`, `master`, or `feedback-screenshots` branches
- NEVER force-delete (`-D`) without explicit user confirmation
- Always show what will be deleted before doing it
- If a branch has unmerged commits, warn the user and ask before force-deleting
- Run `git fetch --prune` at the end to clean up stale remote refs
- If there are no branches to clean, say so and exit

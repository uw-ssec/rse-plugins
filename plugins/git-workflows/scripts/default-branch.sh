#!/usr/bin/env bash
# Print the repository's default branch name (main, master, develop, ...).
#
# Resolution order: the local origin/HEAD symref, then the remote's advertised
# HEAD, then the GitHub API, then a branch that demonstrably exists. Exits
# non-zero rather than guessing, so a caller never silently proceeds against
# "main" in a repo whose default branch is something else.
#
# Usage: default-branch.sh [remote]      # remote defaults to "origin"

set -uo pipefail

remote="${1:-origin}"

# A remote the caller named but git does not have is a caller error, not a
# reason to fall through to a local branch that happens to share the name.
if ! git remote get-url "$remote" >/dev/null 2>&1; then
    printf 'default-branch: no such remote: %s\n' "$remote" >&2
    exit 1
fi

# 1. Local symbolic ref. Fastest, but unset on many fresh clones.
if ref=$(git symbolic-ref --short "refs/remotes/${remote}/HEAD" 2>/dev/null); then
    printf '%s\n' "${ref#"${remote}/"}"
    exit 0
fi

# 2. Ask the remote, which also caches the answer for next time.
if git remote set-head "$remote" --auto >/dev/null 2>&1 \
    && ref=$(git symbolic-ref --short "refs/remotes/${remote}/HEAD" 2>/dev/null); then
    printf '%s\n' "${ref#"${remote}/"}"
    exit 0
fi

# 3. GitHub API, for when the remote is only reachable through gh auth.
if command -v gh >/dev/null 2>&1 \
    && ref=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name 2>/dev/null) \
    && [ -n "$ref" ]; then
    printf '%s\n' "$ref"
    exit 0
fi

# 4. Last resort: a branch that actually exists. Still never a blind guess.
for candidate in main master trunk develop; do
    if git show-ref --verify --quiet "refs/remotes/${remote}/${candidate}" \
        || git show-ref --verify --quiet "refs/heads/${candidate}"; then
        printf '%s\n' "$candidate"
        exit 0
    fi
done

printf 'default-branch: cannot determine the default branch for remote %s\n' "$remote" >&2
exit 1

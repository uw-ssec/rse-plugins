#!/bin/bash
# Turn the copied files into a git repo whose history encodes the planted findings:
#  - secret-rotation check: master key ciphertext IDENTICAL across the incident window
#  - version-lag: vulnerable pin from April, fix advisory in April, upgrade in late October
set -euo pipefail
cd /app/deploy
git init -q
git config user.email "audit@example.org"
git config user.name "Audit Sample"
git config commit.gpgsign false

# Commit 1 (April): initial deployment, vulnerable version, original master key
git add -A
GIT_AUTHOR_DATE="2026-04-08T10:00:00+00:00" GIT_COMMITTER_DATE="2026-04-08T10:00:00+00:00" \
  git commit -q -m "deploy: initial prod + staging on gateway v2.3.0"

# Commit 2 (October 22, pre-incident): unrelated change; env file untouched
mkdir -p prod
echo "# post-migration note: verify firewall rules" > prod/NOTES.md
git add -A
GIT_AUTHOR_DATE="2026-10-22T09:00:00+00:00" GIT_COMMITTER_DATE="2026-10-22T09:00:00+00:00" \
  git commit -q -m "chore: note after state migration"

# Commit 3 (October 30, post-incident): upgrade BOTH envs, add salt key to staging only
git add -A
GIT_AUTHOR_DATE="2026-10-30T21:00:00+00:00" GIT_COMMITTER_DATE="2026-10-30T21:00:00+00:00" \
  git commit -q -m "fix: upgrade gateway to v2.9.2 after incident" --allow-empty

git branch -q -M main
git checkout -q -b audit-snapshot
echo "history initialized"

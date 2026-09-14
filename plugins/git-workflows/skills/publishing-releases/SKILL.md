---
name: publishing-releases
description: >-
  Use when cutting a version — deciding the semver bump from the commit log,
  rolling the changelog, tagging, and creating the GitHub release with any build
  artifacts attached. Triggers: cut a release, tag a version, bump the version,
  release this, publish v1.2.0, prepare the changelog for release.
---

# Publishing Releases

A tag is permanent. Verify the preconditions before creating one, and get
confirmation before anything is pushed.

## Checklist

1. **Check readiness** — clean tree, correct branch, up to date
2. **Determine the version** — from the commits since the last tag
3. **Roll the changelog**
4. **Commit, tag, push** — after confirmation
5. **Build artifacts** — if this project ships any
6. **Create the release**
7. **Verify** — tag, release, and assets all present

## 1. Check readiness

```sh
BASE=$("${CLAUDE_PLUGIN_ROOT}/scripts/default-branch.sh")
git branch --show-current       # must equal "$BASE"
git status --porcelain          # must be empty
git pull origin "$BASE"
```

Stop if the branch is not the default branch or the tree is dirty. Releases are
cut from the release branch, never from a feature branch.

## 2. Determine the version

```sh
git tag --sort=-v:refname | head -1              # current; v0.1.0 if none exist
git log --oneline "$(git describe --tags --abbrev=0)"..HEAD
```

If the user named `patch`, `minor`, or `major`, use it. Otherwise infer:

| Bump | Trigger in the commit range |
| --- | --- |
| `major` | A `!` marker or a `BREAKING CHANGE:` footer |
| `minor` | Any `feat:` commit |
| `patch` | Only fixes, refactors, docs, chores |

State the inferred bump and the reasoning before proceeding. Pre-1.0 projects
often hold breaking changes at `minor` — follow the project's own tag history.

## 3. Roll the changelog

Read `CHANGELOG.md`. If `[Unreleased]` is empty or absent, say so and ask how to
proceed rather than inventing entries.

Rename `[Unreleased]` to `[X.Y.Z] - YYYY-MM-DD` using today's real date, then add
a fresh empty `[Unreleased]` above it.

## 4. Commit, tag, push

Confirm with the user before this step. Everything after it is public.

```sh
git add CHANGELOG.md
git commit -m "chore(release): prepare vX.Y.Z"
git tag -a vX.Y.Z -m "vX.Y.Z"
git push origin "$BASE" --follow-tags
```

## 5. Build artifacts

Only if the project ships them. Detect what it builds rather than assuming:
`pyproject.toml` implies `python -m build`; a `plugins/` tree implies per-plugin
archives; many repos ship nothing and this step is skipped entirely.

When archiving directories, exclude junk:

```sh
zip -r ../<name>_<version>.zip <dir>/ -x "*.DS_Store" "*__pycache__/*" "*.pyc"
```

Build artifacts are upload inputs. Never commit them; delete them after upload.

## 6. Create the release

```sh
PREV=$(git tag --sort=-v:refname | sed -n 2p)
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
gh release create vX.Y.Z --title "vX.Y.Z" \
  --notes-file <scratchpad>/notes.md \
  <artifact files...>
```

Notes carry the changelog section for this version plus a compare link built
from the current remote — `https://github.com/$REPO/compare/$PREV...vX.Y.Z` —
never a URL copied from another project.

## 7. Verify

```sh
gh release view vX.Y.Z --json tagName,url,assets
git tag --sort=-v:refname | head -3
```

Confirm the tag exists on the remote and every expected asset uploaded. Report
the release URL. If an asset is missing, say which one — a release that looks
published but ships nothing is the failure worth catching.

## Rules

- Never release from a feature branch or a dirty tree.
- Tags are always `vX.Y.Z`. Never move or delete a published tag; supersede it.
- Confirm before pushing the tag — that is the point of no return.
- Never commit build artifacts.
- Never add AI attribution or "Generated with" lines to the release commit, tag
  message, or notes.

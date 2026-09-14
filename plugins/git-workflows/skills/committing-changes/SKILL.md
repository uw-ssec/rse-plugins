---
name: committing-changes
description: >-
  Use when finished edits need to be recorded into git history — writing the
  commit message, choosing a conventional type and scope, screening for secrets,
  and staging files by name. Covers amend requests and pre-commit hook failures.
  Triggers: commit this, commit my changes, write a commit message, save this to
  git, stage and commit, what type should this commit be.
---

# Committing Changes

A commit message is read far more often than it is written — during review, during
a bisect, during an archaeology session two years from now. Spend the effort here.

## Checklist

1. **Survey** — what changed, and how does this repo write messages?
2. **Screen** — secrets and junk files must not enter history
3. **Stage** — by name, never wholesale
4. **Compose** — type, scope, imperative subject, body explaining *why*
5. **Commit** — heredoc form, so the body survives shell quoting
6. **Verify** — confirm the commit landed and holds what you intended

## 1. Survey

Run in parallel:

```sh
git status              # never -uall; it buries you in ignored paths
git diff --stat         # unstaged
git diff --cached --stat  # staged
git log --oneline -15   # how this repo actually writes messages
```

Match the repo you are in. If its history has no scopes, do not introduce them
for one commit. If it does not use conventional commits at all, follow what it
uses — consistency with the surrounding history beats the convention below.

## 2. Screen before staging

Never commit:

- Credential-bearing files — `.env`, `.env.local`, `*.pem`, `*.key`, anything
  matching `credentials`, `secrets`, or `id_rsa`
- OS and editor droppings — `.DS_Store`, `Thumbs.db`, `*.swp`
- Build output and caches — `__pycache__/`, `.pytest_cache/`, `dist/`, `*.pyc`

If any are already staged, unstage them and tell the user. If a credential file
was staged, say so plainly — that is a near-miss worth naming, not a quiet fix.
If the file should never be committed anywhere, offer to add it to `.gitignore`.

## 3. Stage by name

```sh
git add path/to/one.py path/to/two.md
```

Never `git add -A`, `git add .`, or `git add -u`. Wholesale staging is how the
credential file and the stray scratch script get in. Name every path.

## 4. Compose the message

```text
type(scope): short imperative description

Body explaining why this change exists, what it replaces, or what
constraint forced it. Wrap at 72 columns.
```

**Subject line** — under 72 characters, imperative mood ("add", not "added" or
"adds"), no trailing period. It completes the sentence "this commit will ___".

**Type** — pick from the repo's own vocabulary if it has one, else:

| Type | When to use |
| --- | --- |
| `feat` | New capability a user can see |
| `fix` | Corrects broken behavior |
| `refactor` | Restructures without changing behavior |
| `docs` | Documentation only |
| `test` | Adds or updates tests |
| `perf` | Measurably faster or lighter |
| `style` | Formatting and whitespace, no logic |
| `chore` | Maintenance, dependencies, config |
| `ci` | Pipelines and automation |
| `build` | Build system and packaging |

**Scope** — optional, and derived from *this* repo, never from a fixed list.
Read `git log --oneline -30`, collect the scopes already in use, and reuse one
when it fits. If the repo uses no scopes, omit it. If the change spans several
areas, omit it rather than inventing a compound.

**Body** — explain the why. The diff already shows the what. Skip the body only
when the subject genuinely says everything.

## 5. Commit

Use the heredoc form so backticks, `$`, and newlines in the body survive:

```sh
git commit -m "$(cat <<'MSG'
fix(loader): tolerate NaN-padded columns in v2 archives

v2 archives pad short columns with NaN rather than truncating, so the
strict length check rejected every file written after the format change.
MSG
)"
```

## 6. Verify

```sh
git status
git log -1 --stat
```

Confirm the intended files are in the commit and nothing unexpected rode along.
State what landed. If a pre-commit hook failed, fix the underlying problem and
make a **new** commit — never `--amend` to paper over it, and never `--no-verify`.

## Rules

- Never skip hooks with `--no-verify`. A failing hook is information.
- Never `--amend` unless the user explicitly asks. It rewrites published history.
- Never add `Co-Authored-By` trailers, AI attribution, or "Generated with" lines
  to commit messages.
- One logical change per commit. If the diff needs the word "and" twice to
  describe, split it.

Commit staged and unstaged changes to the current branch.

## Instructions

1. Run `git status` (never use `-uall`) and `git diff --stat` to see all changes.
2. Run `git log --oneline -5` to see the commit message style for this repo.
3. Analyze ALL changes (staged + unstaged) and determine:
   - The conventional commit type: `feat`, `fix`, `refactor`, `docs`, `chore`, `style`, `test`, `perf`, `ci`, `build`
   - An optional scope in parentheses based on what area changed (e.g., `marketing`, `platform`, `developer`, `billing`, `db`, `auth`, `worker`, `ui`, `tokens`)
   - A concise imperative description of WHY, not WHAT
4. Do NOT commit files that likely contain secrets (`.env`, `.env.local`, credentials, API keys). Warn if any are staged.
5. Do NOT commit `.DS_Store` files.
6. Stage relevant untracked files by name (never use `git add -A` or `git add .`).
7. Create the commit using this format:

```
git commit -m "$(cat <<'EOF'
type(scope): short imperative description

Optional body explaining the why, not the what.
Multi-line is fine for complex changes.
EOF
)"
```

8. Run `git status` after to verify success.
9. If a pre-commit hook fails, fix the issue and create a NEW commit (never amend).

## Conventional Commit Types

| Type | When to use |
|------|------------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `docs` | Documentation only |
| `chore` | Maintenance, deps, config |
| `style` | Formatting, whitespace (not CSS) |
| `test` | Adding or updating tests |
| `perf` | Performance improvement |
| `ci` | CI/CD changes |
| `build` | Build system or tooling |

## Rules

- Keep the first line under 72 characters
- Use imperative mood ("add" not "added", "fix" not "fixed")
- Scope is optional but preferred when changes are localized
- Never skip hooks (`--no-verify`)
- Never amend unless explicitly asked

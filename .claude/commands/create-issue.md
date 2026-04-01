Create a GitHub issue for tracking work.

## Arguments

$ARGUMENTS — a description of the issue to create

## Instructions

1. Based on `$ARGUMENTS`, determine:
   - **Type**: `feat`, `fix`, `refactor`, `docs`, `chore`, `perf`, `ci`, `build`, `test`
   - **Scope**: the area of the codebase affected (e.g., `marketing`, `platform`, `developer`, `billing`, `db`, `auth`, `worker`, `ui`, `tokens`, `infra`)
   - **Title**: conventional commit format: `type(scope): short imperative description`

2. Draft a structured issue body with relevant sections:

```bash
gh issue create --title "type(scope): description" --body "$(cat <<'EOF'
## Summary

<1-2 sentences describing the problem or feature>

## Requirements

<bulleted list of specific requirements or acceptance criteria>
- [ ] Requirement 1
- [ ] Requirement 2

## Context

<any relevant context, links, or background — omit if not needed>

## Implementation Notes

<optional technical direction or constraints — omit if not needed>
EOF
)"
```

3. Return the issue URL and number to the user.

## Title Convention

| Type | Example |
|------|---------|
| `feat(marketing)` | `feat(marketing): add testimonial carousel to landing page` |
| `fix(auth)` | `fix(auth): resolve PKCE exchange failure on second localhost port` |
| `refactor(db)` | `refactor(db): normalize ingredient tables to reduce duplication` |
| `docs(guides)` | `docs(guides): add Stripe webhook deployment checklist` |
| `chore(deps)` | `chore(deps): upgrade React to 19.3` |

## Rules

- Title must use conventional commit format: `type(scope): description`
- Keep title under 70 characters
- Use imperative mood ("add" not "adds", "fix" not "fixes")
- Requirements section should have checkboxes for trackable items
- Omit sections that aren't relevant (don't pad with empty sections)
- If `$ARGUMENTS` is vague, ask clarifying questions before creating

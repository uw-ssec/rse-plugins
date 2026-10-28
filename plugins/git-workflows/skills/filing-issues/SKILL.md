---
name: filing-issues
description: >-
  Use when work needs a tracked ticket before or instead of doing it — turning a
  bug report, feature request, or leftover TODO into a typed, scoped GitHub
  issue with acceptance criteria. Triggers: file an issue, open a ticket, track
  this, make an issue for this, log this bug, write up acceptance criteria.
---

# Filing Issues

An issue is a contract with your future self. It has to survive the loss of the
conversation that produced it — assume the reader has none of today's context.

## Checklist

1. **Clarify** — enough substance to be actionable?
2. **Classify** — type, scope, title
3. **Draft** — body with acceptance criteria
4. **File** — via `--body-file`
5. **Verify** — read it back

## 1. Clarify first

If the request is too vague to write acceptance criteria for, ask before filing.
A ticket saying "fix the loader" helps no one. What is needed:

- For a bug: what happened, what was expected, how to reproduce it
- For a feature: the problem it solves, not just the solution imagined
- For a refactor: what is hard today that would get easier

Ask the smallest question that unblocks the write-up, not a questionnaire.

## 2. Classify

**Title** — `type(scope): short imperative description`, under 70 characters.

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `perf`, `chore`, `ci`, `build`.

Scope is the area affected, drawn from the repo's own history
(`git log --oneline -30`) or its directory layout — never from a fixed list.

| Example |
| --- |
| `fix(auth): reject expired tokens on the refresh path` |
| `feat(loader): support v2 archive column padding` |
| `refactor(db): normalize ingredient tables to cut duplication` |
| `docs(guides): add deployment checklist for webhooks` |

## 3. Draft the body

Write to a file. Include only the sections that carry weight:

```markdown
## Summary

<1-2 sentences on the problem or the capability>

## Requirements

- [ ] <specific, checkable outcome>
- [ ] <another>

## Context

<background, links, prior discussion — omit if there is none>

## Implementation Notes

<technical direction or constraints — omit if there is none>
```

Requirements are checkboxes because they get ticked during review. Write each so
a reader can tell whether it is done without asking you. For a bug, replace
*Requirements* with reproduction steps plus expected versus actual behavior.

Do not pad. An empty *Context* heading signals the template was filled in rather
than the problem thought through.

## 4. File

```sh
gh issue create --title "type(scope): description" \
  --body-file <scratchpad>/issue.md \
  --assignee <login> --label <label>
```

Only pass `--label` values that already exist — `gh` fails on unknown labels.
Check with `gh label list` when unsure.

## 5. Verify

```sh
gh issue view <number> --json number,title,url,labels,assignees
```

Before returning, search for a duplicate: `gh issue list --search "<key terms>"`.
If one exists, say so and offer to comment on it instead of leaving two open
tickets for one problem. Return the URL and number.

## Rules

- Title uses conventional format and imperative mood ("add", not "adds").
- Requirements must be checkable, not aspirational.
- Omit sections rather than filling them with placeholder text.
- Never add AI attribution or "Generated with" lines to the title or body.

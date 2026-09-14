---
name: recording-decisions
description: >-
  Use when a choice and its rationale should outlive the conversation — posting
  it as a GitHub Discussion capturing why an option won, which alternatives lost,
  and what would reverse it. For durable reference material that belongs beside
  the code, prefer documenting-work. Triggers: capture this decision, write an
  ADR, record why we chose this, post a discussion, log this learning.
---

# Recording Decisions

A bare verdict gets re-litigated in three months. The reasoning is the artifact —
especially the options that lost, which no other document ever keeps.

## Where this belongs

| The artifact is... | Put it in |
| --- | --- |
| A choice, with reasoning and rejected alternatives | A Discussion — this skill |
| Reference someone needs open while writing code | The docs tree — `git-workflows:documenting-work` |
| A defect or a task to be done | An issue — `git-workflows:filing-issues` |

## Checklist

1. **Find the substance** — from the request or the session just completed
2. **Check the venue** — are Discussions even enabled?
3. **Pick a category** — from the repo's real list
4. **Search for a prior entry** on the same question
5. **Write and post** via `--body-file`
6. **Verify** — read it back

## 1. Find the substance

If given a topic, use it. If not, draw from what was just worked through: the
question asked, the evidence gathered, the conclusion reached, and what was
tried and abandoned along the way.

## 2. Check the venue

```sh
gh repo view --json nameWithOwner,visibility,hasDiscussionsEnabled
```

If Discussions are disabled, **ask before enabling**. It is a repo settings
change, and on a public repo it opens a world-visible surface. Only after
approval:

```sh
gh repo edit <owner/repo> --enable-discussions
```

## 3. Pick a category

Never hardcode a category name or ID — they differ per repo:

```sh
gh api graphql -f query='
{ repository(owner:"OWNER", name:"REPO") {
    discussionCategories(first:20) { nodes { id name description } } } }'
```

Default to `General` for decision records. Use `Q&A` when the entry resolves a
specific question someone will later search for. Announce which you chose.

## 4. Search first

```sh
gh api graphql -f query='
{ search(query:"repo:OWNER/REPO <key terms>", type:DISCUSSION, first:10) {
    nodes { ... on Discussion { number title url } } } }'
```

If the question already has an entry, extend it with a comment instead of
opening a second one that splits the record.

## 5. Write and post

Write the body to a file — decision bodies carry tables, backticks, and `$` that
a heredoc will mangle.

```markdown
**Decision: <the answer in a few words>.** <One line on why it is recorded.>

## Why

<Bullets. Each anchored to a `path/file.py:line` or a concrete constraint,
never a generality.>

<A closing line naming the general principle, so the entry transfers to the
next similar question.>

## What we considered instead

<Table: Option | Why it lost. Only when something was rejected — this is the
part that makes the entry worth keeping.>

## Open threads

<Adjacent things noticed but unresolved, and what would settle each.>

## Revisit if

<The conditions that would flip this. Close by saying whether any hold today.>
```

Post it:

```sh
gh api graphql -f query='
mutation($repo:ID!,$cat:ID!,$title:String!,$body:String!) {
  createDiscussion(input:{repositoryId:$repo,categoryId:$cat,title:$title,body:$body}) {
    discussion { number url } } }' \
  -f repo=<repo-id> -f cat=<category-id> -f title="<title>" -F body=@<file>
```

`gh discussion create --body-file` is simpler where available, but it is a
preview command missing from older `gh` — fall back to the mutation above.

## 6. Verify

Open the posted URL and confirm the tables and code spans rendered. Report which
category it landed in, and whether Discussions had to be enabled.

## Rules

- The title states the decision, not the topic: "we are not adding a queue layer"
  beats "queue layer discussion".
- Anchor claims to `path/file.py:line` so a reader can verify rather than trust.
- Record what you are unsure about, flagged as unresolved. Do not quietly drop it.
- Never enable Discussions on a public repo without explicit approval.
- Never add AI attribution or "Generated with" lines to the title or body.

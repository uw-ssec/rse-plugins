---
name: iterating-plans
description: >-
  Use when an existing implementation plan needs changes before or during
  execution. Triggers: update the plan, change the plan, add a phase, revise
  scope, incorporate experiment results.
---

# Iterating Plans

Revise an existing `.agents/plan-*.md` with focused, surgical edits that
preserve good content and maintain internal consistency.

## Interaction mode

This skill leans **Collaborative** by default. For the full Collaborative-vs-Direct protocol and override rules, see the Interaction Modes reference in the `ai-research-workflows:using-research-workflows` skill.

## Starting the skill

If the plan file or the requested change is missing, enter Collaborative mode
and ask for it (list recent plans with `ls -lt .agents/plan-*.md | head -5`).

## Process

### Step 1: Read and understand the current plan

Read the entire plan completely (avoid partial reads). Identify:

- Number of phases, current scope, defined success criteria, implementation
  approach, and included references.

Parse the requested change: adding/removing phases or tasks, updating success
criteria, changing technical approach, incorporating new information, splitting
or reordering phases.

Determine whether the change requires codebase research:

- **Research needed** — changes introduce new technical requirements or alter
  approach
- **No research needed** — structural changes (reordering, splitting),
  clarifications, or minor scope adjustments

### Step 2: Research if needed

Only if changes require new technical understanding:

- Investigate in parallel: how a new requirement is currently handled, examples
  of a pattern the new phase should follow, dependencies for a new component,
  tests covering a related area.
- **Wait for all research to complete** before proceeding.
- Synthesize: what files need adding to tasks, what patterns to reference, what
  success criteria to add, what risks to note.

### Step 3: Confirm understanding before editing

Before making any changes, present:

```
I've read the plan and understand you want to [summary of requested changes].

Current state:
- Phases: [list]
- Scope: [summary]

Proposed changes:
- [Change 1]
- [Change 2]

Sections affected:
- [Section 1]
- [Section 2]

[If research was done] Key findings:
- [Finding]

Does this match what you're looking for?
```

Get user confirmation. If the user says no, clarify and adjust; only proceed on yes.

### Step 4: Update the plan — surgical edits

Make focused, precise edits to the plan in place (`.agents/plan-*.md`).

**Good edits:** add a new phase section between existing phases; update specific
success criteria items; modify task descriptions within a phase; add file
references to existing tasks.

**Bad edits:** replace the entire plan; rewrite sections that don't need
changes; change formatting or structure unnecessarily.

Maintain existing structure unless explicitly changing it: same phase format,
same task description pattern, same reference style, same level of detail.

When adding tasks or phases include specific `path/to/file.ext:123-145`
references — research actual code locations if needed.

When scope changes update success criteria (add/remove items) and preserve the
**Automated vs. Manual verification split**:

```markdown
### Automated Verification
[Commands and checks that run without human intervention]

### Manual Verification
[Steps requiring human testing and judgment]
```

Ensure consistency: new phases follow existing structure; scope changes update
"What We're NOT Doing"; approach changes update "Implementation Approach"; new
tasks reference actual codebase examples.

### Step 5: Present the changes

```
# Plan Updated

Changes to `.agents/plan-[slug].md`:

## Changes Made
- [Change 1 — specific section]
- [Change 2 — specific section]

## Impact
- [How changes affect implementation]
- [New/removed success criteria]

Would you like any further adjustments?
```

If the user wants more changes, re-read the plan first and apply the same process.

## Important guidelines

**Be skeptical** — push back on changes that conflict with existing phases;
question vague feedback ("when you say 'more robust', do you mean...?"); verify
technical feasibility with code research before adding tasks.

**Be surgical** — edit only what needs changing; don't reformat or rewrite for
style.

**Be thorough** — read the entire plan before editing; never guess at file paths.

**No open questions** — this is a BLOCKING REQUIREMENT. If a requested change
raises questions, ask or research immediately. Do NOT update the plan with
unresolved questions; plans must be complete specifications.

## Common iteration patterns

For the five detailed patterns (adding a phase, updating success criteria,
adjusting scope, incorporating experiment results, splitting a complex phase),
see `references/iteration-patterns.md`.

## Common Mistakes

- **Rewriting whole sections instead of surgical edits** — only change what the
  user asked to change; preserve structure, formatting, and unaffected content.
- **Editing without confirming first** — always present the proposed changes and
  get user confirmation before writing to the plan file.
- **Leaving open questions in the plan** — if a requested change raises
  unresolved questions, ask or research immediately; never commit ambiguity to
  the plan.
- **Skipping research when technical changes require it** — changing approach or
  adding phases that reference new code requires investigating the codebase first.
- **Breaking internal consistency** — after edits, verify that phase numbering,
  scope statements, success criteria, and references are still coherent.

## Cross-references

After iterating, execute with the `ai-research-workflows:implementing-plans` skill. Incorporate
`.agents/experiment-*.md` results when revising the technical approach.

## Quality checklist

Before completing, verify:

- [ ] Read the entire existing plan before making changes
- [ ] Ran research tasks if technical understanding was needed
- [ ] Confirmed understanding with user before editing
- [ ] Made precise edits without unnecessary rewrites
- [ ] Maintained consistency with existing structure
- [ ] Updated all affected sections (approach, criteria, references)
- [ ] Preserved Automated vs. Manual verification split
- [ ] All file:line references are accurate
- [ ] No open questions remain in the updated plan
- [ ] User is satisfied with changes

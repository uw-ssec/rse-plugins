---
description: Create a handoff document to transfer work context to another session
user-invocable: true
---

## When to use

Invoke `/handoff` when:

- The current session will end (timebox, context limit, end of workday) and work is not complete
- You want another session or contributor to resume the same work without losing context
- A long-running workflow has paused between phases and needs a clean restart point

**Example triggers:**
- "Create a handoff so I can resume tomorrow"
- "Summarize context for the next session"
- "I'm running low on context — hand off to a new conversation"

**Do not invoke `/handoff`** for:
- Completed work that needs documentation — use `/implement` or `/validate` outputs, or a standard commit message
- Work that fits in the current session with no resume step needed

# Create Handoff

You are tasked with writing a handoff document to transfer your work context to another agent in a new session. The handoff must be **thorough but concise** — compact and summarize your context without losing key details of what you're working on.

## Process

### 1. Gather Context

Collect all necessary information to write the handoff. Run these in parallel when possible:

**Git state:**
- Current branch name
- Current commit hash (short)
- Summary of uncommitted changes (`git status` and `git diff --stat`)

**Workflow artifacts:**
Search for existing workflow documents in the `.agents/` directory:
- Find files matching `.agents/research-*.md` (research documents)
- Find files matching `.agents/plan-*.md` (plan documents)
- Find files matching `.agents/experiment-*.md` (experiment documents)
- Find files matching `.agents/implement-*.md` (implementation documents)
- Find files matching `.agents/handoff-*.md` (previous handoff documents)

**Session context:**
- Review the conversation to understand what tasks were worked on
- Identify the current workflow phase (Research, Plan, Iterate Plan, Experiment, Implement, Validate)
- Note which workflow artifacts were produced or referenced in this session

### 2. Determine What's Relevant

From the gathered context, identify:

- **Tasks:** What was being worked on and the status of each (completed, in progress, planned)
- **Current phase:** Where in the workflow cycle the work currently sits
- **Artifacts:** Which `.agents/` documents are relevant to this work
- **Critical files:** The 2-3 most important files the next session must read first
- **Recent changes:** What code was modified in this session (use `file:line` references)
- **Learnings:** Important discoveries, patterns, or gotchas
- **Next steps:** What the next session should do, in priority order

### 3. Generate the Handoff Document

**Generate the filename:**
- Format: `handoff-YYYY-MM-DD-HH-MM-<slug>.md`
- Where `YYYY-MM-DD-HH-MM` is the current date and time
- Where `<slug>` is a brief kebab-case description of the work
- Example: `handoff-2025-06-15-14-30-auth-system-refactor.md`

**Read the handoff template:**
- Read the template from `${CLAUDE_PLUGIN_ROOT}/skills/research-workflow-management/assets/handoff-template.md`
- Use it as the structure for your document

**Fill out all sections:**
- Replace all placeholder text with actual content
- Remove artifact sections that don't apply (e.g., if no experiments were run, remove the Experiment Reports section)
- Be specific — use `file:line` references, not vague descriptions
- Include the recommended next command based on the current workflow phase

**Save the document:**
- Save to `.agents/handoff-YYYY-MM-DD-HH-MM-<slug>.md`

### 4. Present the Handoff

After saving, present a concise summary to the user:

```
## Handoff Created

**File:** `.agents/handoff-<filename>.md`
**Current Phase:** [phase]
**Status:** [brief status of work]

### Quick Summary
[2-3 sentence summary of what was done and what's next]

### For the Next Session
Start by running:
> Read the handoff document at `.agents/handoff-<filename>.md` and resume the work described within.

Or to continue with the workflow:
> /[recommended-command] [relevant arguments]
```

## Writing Guidelines

- **More information, not less.** This template defines the minimum. Always include more if necessary.
- **Be thorough and precise.** Include both top-level objectives and lower-level details.
- **Avoid excessive code snippets.** Prefer `path/to/file.ext:line` references that the next session can follow. Only include code blocks when describing an error being debugged or a critical pattern.
- **Cross-reference workflow artifacts.** Link to research, plan, experiment, and implementation documents by filename so the next session can read them.
- **State the recommended next command.** Based on where you are in the workflow, tell the next session which `/command` to run next.
- **Include learnings.** The next session doesn't have your context — capture non-obvious insights about the codebase, patterns that matter, or gotchas encountered.

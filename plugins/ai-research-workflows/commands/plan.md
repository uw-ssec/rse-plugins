---
description: Create a detailed implementation plan through interactive research and iteration
user-invocable: true
---

# Initial Response

When this command is invoked, determine what context you have:

**If argument AND research doc reference provided** (e.g., `/plan add JWT auth @research-auth-system.md`):
- Read the referenced research document immediately and FULLY
- Read any other mentioned files immediately and FULLY
- Begin the planning process with this context

**If argument provided but no research doc reference** (e.g., `/plan add JWT auth`):
- Look for existing research docs in `.agents/` that match the topic
- Use Glob: `.agents/research-*.md` to find candidates
- If matching research found, read it and reference it
- If no research found, suggest: "I can proceed, but running `/research [topic]` first would provide valuable context. Should I proceed with planning or would you like to research first?"
- Proceed based on user's preference

**If no argument provided:**
- Respond with:
  ```
  What would you like me to plan?

  Available research documents in .agents/:
  [List any research-*.md files found, or state "None found"]

  I can help you plan:
  - New feature implementations
  - Refactoring or architectural changes
  - Bug fixes requiring multiple file changes
  - Integration of new technologies or patterns

  Please describe what you want to implement.
  ```
- WAIT for the user's response before proceeding

# Planning Philosophy

Plans are not just task lists — they are technical specifications that bridge understanding and execution.

**Good plans are:**
- **Interactive** — Built through dialog, not written in isolation
- **Skeptical** — Question vague requirements and verify assumptions
- **Thorough** — Based on actual code investigation, not guesses
- **Actionable** — Include specific file paths, line numbers, and concrete steps
- **Testable** — Define clear, measurable success criteria
- **Realistic** — Acknowledge constraints and define scope boundaries

**Plans must NOT have:**
- Open questions or unresolved decisions
- Vague requirements or ambiguous acceptance criteria
- Guesses about how code works without verification
- Unrealistic scope or hand-waving about complexity

# Process Steps

## Step 1: Context Gathering & Initial Analysis

### Read All Mentioned Files Immediately

**CRITICAL:** If the user or research docs mention specific files, read them FIRST in the main context.

- Read entire files completely (avoid partial reads)
- DO NOT delegate sub-tasks before reading these files yourself
- You need this context to ask informed questions and make good decisions

### Read Existing Research Documents

- Look in `.agents/` for relevant `research-*.md` files
- Read any research that relates to the planning topic
- This provides architectural context and existing patterns

### Conduct Initial Research

Now that you have core context, conduct additional research in parallel if possible:

**Research areas to investigate:**
- "Find related files that implement similar functionality"
- "Analyze the current implementation of [component]"
- "Find patterns in the codebase for [technical concern]"
- "Search for existing tests that cover [area]"

**Wait for ALL research to complete** before synthesizing.

### Cross-Reference Requirements with Actual Code

- Verify that your understanding matches reality
- Check if similar features exist that you can learn from
- Identify integration points and dependencies

### Present Informed Understanding and Focused Questions

DO NOT ask questions that can be answered by reading code. Instead:

**Good questions:**
- "Should this feature support [edge case]?" — requires product decision
- "What's the priority: performance or flexibility?" — requires product decision
- "How should this behave when [ambiguous scenario]?" — requires clarification

**Bad questions (just read the code):**
- "Which database are you using?" — read the code
- "How is authentication currently implemented?" — read the code or research doc
- "What framework is this?" — obvious from code structure

If you have good questions, ask the user to get answers before proceeding.

## Step 2: Research & Discovery

Based on user responses and initial findings, continue research as needed.

### Create Task List

Create a task list to track your research and planning activities:
- Major research areas to explore
- Components to analyze
- Patterns to investigate
- Sections of plan to write

### Conduct Comprehensive Research

Investigate the following areas in parallel if possible:
- How existing code handles similar requirements
- What patterns the codebase follows
- Where integration points exist
- What tests currently cover related areas
- What dependencies are already available

**Launch research in parallel** when your environment supports it.

### Wait for ALL Research to Complete

Do NOT proceed until all research has returned results.

### Synthesize and Present Findings

Compile research into coherent understanding:
- Current state of related code
- Patterns that should be followed
- Integration points identified
- Potential challenges discovered

Present findings with design options:

```
Based on codebase research, I see two main approaches:

**Approach 1: [Name]**
- Pros: [...]
- Cons: [...]
- Follows pattern in `path/to/example.ext:123`

**Approach 2: [Name]**
- Pros: [...]
- Cons: [...]
- Introduces new pattern, rationale: [...]

Which approach fits your requirements better?
```

Get user feedback on the approach before continuing.

## Step 3: Plan Structure Development

Before writing detailed implementation steps, establish the plan structure:

**Create initial outline:**
```
I propose breaking this into [N] phases:

Phase 1: [Name] — [What it accomplishes]
Phase 2: [Name] — [What it accomplishes]
Phase 3: [Name] — [What it accomplishes]

This ordering allows:
- [Benefit 1]
- [Benefit 2]
- Testing after each phase

Does this structure make sense?
```

**Get feedback** before writing detailed steps. Adjusting structure early is cheaper than rewriting detailed plans.

## Step 4: Detailed Plan Writing

Now write the comprehensive plan document.

### Generate Filename

- Derive slug from command argument (lowercase, hyphenated)
- Format: `plan-<slug>.md`
- Example: `/plan add JWT auth` → `.agents/plan-jwt-auth.md`

### Read the Plan Template

Read from: `${CLAUDE_PLUGIN_ROOT}/skills/research-workflow-management/assets/plan-template.md`

### Fill Out All Sections Thoroughly

**Required sections:**

1. **Overview** — What, why, and high-level how
2. **Current State Analysis** — Existing code with file:line references
3. **Desired End State** — What success looks like
4. **What We're NOT Doing** — Explicit scope boundaries
5. **Assumptions** — Unverified beliefs the plan depends on
6. **Implementation Approach** — Technical strategy and key decisions
7. **Implementation Phases** — Detailed, phased steps with checkboxes
8. **Success Criteria** — Split into Automated and Manual sections
9. **Testing Strategy** — Unit, integration, and manual tests
10. **References** — Research docs, files analyzed, external docs

**Critical requirements:**

- **Each phase must have:**
  - Clear objective stating what's accomplished
  - Specific tasks with file paths and line numbers
  - Dependencies on prior phases if any
  - Verification steps

- **Success Criteria must be split:**
  - **Automated Verification** — Commands that can be run without human intervention (`make test`, `pytest`, file existence checks, etc.)
  - **Manual Verification** — Steps requiring human testing (UI behavior, UX, edge cases, performance under real conditions)

- **Each task must include:**
  - Specific files to modify: `path/to/file.ext:lines`
  - What changes to make
  - How to verify the change

**Write with specificity:**
- Not: "Add authentication"
- But: "Add JWT token validation in `api/middleware/auth.py:45` following the pattern from `api/middleware/session.py:23-34`"

### Ensure NO Open Questions Remain

**CRITICAL:** The final plan must NOT contain any open questions.

If you encounter uncertainties while writing:
1. STOP writing the plan
2. Research the code to find answers, OR
3. Ask the user to get clarification
4. Resume writing only after questions are resolved

**Unacceptable:**
```markdown
## Open Questions
- Should we use JWT or sessions? (TBD)
- Which database table should store this? (Need to investigate)
```

**Every decision must be made before the plan is complete.**

### Save the Plan

- Create `.agents/` directory if needed: `mkdir -p .agents`
- Write to `.agents/plan-<slug>.md`
- Confirm successful save

## Step 5: Review & Iterate

Present the plan to the user:

```
# Implementation Plan Complete

I've created a detailed plan at `.agents/plan-[slug].md`.

## Summary:
- [High-level summary of approach]
- [Number] phases
- [Key architectural decision]

## Phases:
1. Phase 1: [Name] — [Brief description]
2. Phase 2: [Name] — [Brief description]
3. Phase 3: [Name] — [Brief description]

## Success Criteria:
- Automated: [Count] checks
- Manual: [Count] checks

Please review the plan. I'd especially appreciate feedback on:
- **Phasing:** Does the phase breakdown make sense?
- **Success Criteria:** Are these the right metrics?
- **Technical Details:** Does the implementation approach look sound?
- **Edge Cases:** Did I miss any scenarios?

Would you like me to adjust anything?
```

### Handle Feedback

If the user has feedback:
1. Read the plan again to refresh context
2. Research code if needed to address feedback
3. Make surgical edits to update the plan
4. Confirm changes address the feedback
5. Ask if further iteration is needed

If the user requests major changes, consider using `/iterate-plan` command instead.

# Important Guidelines

## Be Skeptical

- **Question vague requirements** — "What should happen when...?"
- **Identify potential issues early** — "This could conflict with..."
- **Don't assume — verify with code** — Read, don't guess

## Be Interactive

- **Don't write the full plan in one shot** — Build it iteratively
- **Get buy-in at each major step** — Structure, then approach, then details
- **Allow course corrections** — User feedback might change direction

## Be Thorough

- **Read all context files COMPLETELY** — Full file reads, not partial
- **Research actual code patterns** — Don't invent patterns
- **Include specific file paths and line numbers** — Enable developer navigation
- **Write measurable success criteria** — "Tests pass" not "Works well"

## Be Practical

- **Focus on incremental, testable changes** — Each phase should be verifiable
- **Consider migration and rollback** — How to deploy safely
- **Think about edge cases** — What breaks this?
- **Include "what we're NOT doing"** — Prevent scope creep

## No Open Questions in Final Plan

This is a BLOCKING REQUIREMENT:

- If you have unresolved questions, STOP and resolve them
- Research code to find answers
- Ask the user to get clarification
- Only finalize the plan when ALL decisions are made

**The plan is a specification, not a brainstorming document.**

# Assumptions Guidelines

Assumptions are beliefs the plan depends on that you have NOT fully verified through direct code inspection or testing. They are distinct from:

- **Verified facts** (belong in Current State Analysis) — things you confirmed by reading code
- **Prerequisites** (belong in Testing Strategy or Dependencies) — things that must exist before running
- **Decisions** (belong in Implementation Approach) — choices you made deliberately
- **Open questions** (must be resolved before plan is final) — things you haven't decided yet

## How to identify real assumptions

Ask yourself: "If this turns out to be false, would my plan break?"

- If yes AND you verified it by reading code - it's a **fact**, put in Current State Analysis
- If yes AND you inferred it from docs/convention - it's an **assumption**, document it
- If yes AND you haven't decided yet - it's an **open question**, resolve it first

## Categories to check

When writing the Assumptions section, consider these categories:

1. **Library/framework internals** — behavior you rely on but didn't verify in source code
2. **Concurrency & isolation** — thread safety, data separation under parallel access
3. **Data characteristics** — volume, format stability, schema guarantees
4. **Environment & infrastructure** — services, network, permissions assumed available
5. **External API contracts** — response formats, rate limits, idempotency guarantees

## Relationship to other sections

- During `/implement`: assumptions should be verified as implementation proceeds
- During `/validate`: check whether any assumptions were invalidated
- During `/iterate-plan`: if an assumption proves wrong, update the plan accordingly

# Success Criteria Guidelines

Always separate success criteria into two categories:

## Automated Verification

Checks that execution agents can run without human intervention:

```markdown
### Automated Verification

- [ ] `make test` passes with no failures
- [ ] `pytest tests/ -v` shows all tests passing
- [ ] `npm run lint` produces no errors
- [ ] `mypy src/` type checking passes
- [ ] File `src/components/NewFeature.tsx` exists
- [ ] `git grep "deprecated_function"` returns no results
```

## Manual Verification

Steps requiring human testing and judgment:

```markdown
### Manual Verification

- [ ] Navigate to http://localhost:3000/feature and verify UI renders correctly
- [ ] User can successfully complete the signup flow end-to-end
- [ ] Error message "Invalid email format" displays when entering malformed email
- [ ] Page loads in under 2 seconds with 1000 items
- [ ] Feature works correctly in Chrome, Firefox, and Safari
- [ ] Edge case: Multiple simultaneous requests don't cause data corruption
```

**Why this matters:**
- Automated checks can be run by implementation agents during `/implement`
- Manual checks tell humans what to test after implementation
- Clear separation enables efficient division of verification labor

# Cross-Reference with Other Workflow Steps

**This plan will be used by:**
- `/implement` — To execute the plan phase-by-phase
- `/validate` — To verify implementation against success criteria

**This plan should reference:**
- Research documents from `/research` in the References section
- Experiment reports from `/experiment` if approaches were tested

**Use relative links:**
```markdown
## References

**Research Documents:**
- [Research: Auth System](research-auth-system.md)

**Experiment Reports:**
- [Experiment: JWT vs Session](experiment-jwt-vs-session.md)
```

# Quality Checklist

Before completing the plan, verify:

- [ ] All referenced files have been read completely
- [ ] All research has been completed
- [ ] User has been consulted on approach and structure
- [ ] Plan uses the official template from assets/
- [ ] Plan is saved to `.agents/plan-<slug>.md`
- [ ] Every phase has specific file:line references
- [ ] Success criteria are split into Automated and Manual
- [ ] Success criteria are measurable and concrete
- [ ] "What We're NOT Doing" section is filled out
- [ ] Assumptions are genuinely unverified beliefs (not restated facts or prerequisites)
- [ ] NO open questions remain in the plan
- [ ] References section links to research and experiment docs
- [ ] Task list shows plan completion

Remember: A good plan is worth the time investment. It prevents wasted implementation effort and ensures alignment before coding begins.

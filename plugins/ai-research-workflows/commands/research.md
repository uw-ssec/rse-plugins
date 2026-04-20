---
description: Research a codebase or topic to build context for a task
user-invocable: true
---

# CRITICAL DIRECTIVE

YOUR ONLY JOB IS TO DOCUMENT AND EXPLAIN THE CODEBASE AS IT EXISTS TODAY.

- DO NOT suggest improvements or changes unless the user explicitly asks
- DO NOT critique the implementation or identify problems
- ONLY describe what exists, where it exists, how it works, and how components interact
- You are creating a technical map/documentation of the existing system

You and all sub-agents are documentarians, not evaluators. Document what IS, not what SHOULD BE.

# Initial Setup

When this command is invoked:

**If argument provided** (e.g., `/research authentication system`):
- Proceed immediately to the research steps below
- Use the argument as the research topic/question

**If no argument provided:**
- Respond with:
  ```
  What would you like me to research?

  I can help you understand:
  - How a specific feature or system works
  - Where functionality is implemented
  - How components interact with each other
  - Architecture patterns in the codebase
  - Existing implementations you can follow

  Please provide a research question or area of interest.
  ```
- WAIT for the user's response before proceeding

# Steps to Follow

Once you have the research question/topic, follow these steps:

## Step 1: Read Directly Mentioned Files First

**CRITICAL:** If the user mentions specific files in their research query, read those files FIRST.

- Read entire files completely (avoid partial reads)
- Read these files yourself in the main context BEFORE delegating any sub-tasks
- This gives you immediate context and helps you formulate better research queries

Example:
```
User: "/research how authentication works in auth.py and session.py"
→ You MUST read auth.py and session.py completely first
→ THEN delegate broader exploration tasks if available
```

## Step 2: Analyze and Decompose the Research Question

Break down the user's query into composable research areas:

- Identify specific components, patterns, or concepts to investigate
- Determine what needs to be found (WHERE things live)
- Determine what needs to be understood (HOW things work)
- Identify connections between different parts of the system

Create a task list to track all research subtasks:
- Create a task for each major research area (use available task management capabilities)
- Mark tasks as in_progress when starting, completed when done
- This helps both you and the user track progress

## Step 3: Conduct Parallel Research for Comprehensive Coverage

If your environment supports parallel research tasks (such as delegating to specialized agents or spawning concurrent investigations), use this capability to research different aspects simultaneously. This maximizes efficiency and minimizes context usage.

**Research task types:**
- Tasks to find WHERE files and components live
- Tasks to understand HOW specific code works
- Tasks to find examples of existing patterns
- All research should be documentarian-focused, not evaluative

**Key principles:**
- Each research task should be specific and focused
- Each task should do read-only operations (no modifications)
- Tasks should provide concrete file paths and line numbers
- Tasks should explain mechanisms, not judge them

**Example research task descriptions:**
```
"Find all files that implement authentication. List the files with brief descriptions of what each does. Search comprehensively using available tools."

"Read the authentication module at path/to/auth.py and explain how the login flow works step-by-step. Include file:line references for key operations."

"Find examples of how JWT tokens are validated in the codebase. Show the pattern with file references."

"Map out how the authentication system integrates with the session management system. Trace the data flow between components."
```

**Launch research in parallel when possible:**
- Execute multiple research tasks concurrently if supported
- Don't wait between launches — initiate them all at once
- This significantly speeds up comprehensive research

## Step 4: Wait for ALL Research Tasks to Complete and Synthesize Findings

**Wait for completion:**
- Do NOT proceed until all research tasks have returned their results
- Each task will provide findings based on their specific query

**Synthesize findings:**
- Compile all research results into a coherent narrative
- Connect findings across different components
- Include specific file paths and line numbers for reference
- Highlight patterns, connections, and architectural decisions
- Answer the user's specific questions with concrete evidence from the code

**Structure your synthesis:**
- Group related findings by component or concern
- Show how different parts of the system work together
- Identify patterns that repeat across the codebase
- Document data flows and call hierarchies
- Include code examples where illuminating

## Step 5: Generate Research Document

**Create output directory:**
```bash
mkdir -p .agents
```

**Generate filename:**
- Derive a slug from the command argument (lowercase, hyphenated)
- Format: `research-<slug>.md`
- Example: `/research authentication system` → `.agents/research-authentication-system.md`

**Use the research template:**
- Read the template from: `${CLAUDE_PLUGIN_ROOT}/skills/research-workflow-management/assets/research-template.md`
- Fill in all sections with your synthesized findings
- Include file paths and line numbers throughout
- Ensure the document is self-contained and readable independently

**Write the document:**
- Write the completed document to `.agents/research-<slug>.md`
- Confirm the file was created successfully

## Step 6: Present Findings

Present a concise summary to the user:

```
# Research Complete: [Topic Name]

I've documented [summary of what was researched] in `.agents/research-[slug].md`.

## Key Findings:
- [Key finding 1]
- [Key finding 2]
- [Key finding 3]

## Important File References:
- `path/to/file1.ext:123` — [What's here]
- `path/to/file2.ext:456` — [What's here]

The research document includes:
- [Section 1 description]
- [Section 2 description]
- [Section 3 description]

Do you have any follow-up questions about [the topic]?
```

**Make it easy for the user:**
- Include key file references for easy navigation (use `file:line` format)
- Highlight the most important discoveries
- Offer to answer follow-up questions

## Step 7: Handle Follow-Up Questions

If the user has follow-up questions:

**Process:**
1. Read the existing research document to understand what was already covered
2. Identify what additional research is needed
3. Conduct additional research as necessary to investigate the follow-up
4. Wait for all research to complete
5. Synthesize the new findings

**Update the document:**
- Edit the existing research document to append new findings
- Add a new section: `## Follow-up Research [timestamp]`
- Include the follow-up question and your findings
- Maintain the same level of detail and file references

**Example follow-up section:**
```markdown
## Follow-up Research [2024-01-15 14:30]

**Question:** How does the authentication system handle token refresh?

**Findings:**
[Your research findings with file references]
```

# Important Notes

## Efficiency Through Parallelization
- ALWAYS use parallel research when your environment supports it
- Launching 3-5 concurrent research tasks is better than sequential investigation
- This protects your main context and speeds up comprehensive research

## Fresh Research
- Always run fresh codebase research — never rely solely on existing documents
- The codebase may have changed since any prior documentation was written
- Your research should reflect the current state of the code

## Concrete References
- Focus on finding concrete file paths and line numbers for developer reference
- Developers need to know WHERE to look, not just WHAT exists
- Include specific line ranges for important code sections

## Self-Contained Documents
- Research documents should be self-contained with all necessary context
- Someone reading the document later should understand the findings without additional context
- Include enough detail that the document can inform planning or implementation

## Research Task Guidelines
- Each research task should be specific and focused on read-only operations
- Do NOT frame research as evaluation or problem identification
- Frame queries as "find", "explain", "document", "trace", "map out"

## Documentation Focus
- CRITICAL: You and all research tasks are documentarian-focused, not evaluative
- REMEMBER: Document what IS, not what SHOULD BE
- Do NOT critique architecture or suggest improvements unless explicitly asked
- Your job is to create a clear, accurate technical map of the existing system

## File Reading
- Always read mentioned files COMPLETELY before delegating sub-tasks
- Complete file context is essential for accurate research
- Partial reads can miss critical information

# Cross-Reference with Planning

If the user proceeds to planning after research:
- The plan command will automatically look for research documents in `.agents/`
- Use consistent naming: `research-<slug>.md`
- Plans will reference your research in their References section

# Example Workflow

```
User: /research how error handling works

You:
1. Create task list for tracking
2. Analyze: Need to find WHERE error handling is, HOW it works, WHAT patterns exist
3. Conduct parallel research (if supported):
   - "Find all files that implement error handling or exception classes"
   - "Read error_handler.py and explain how errors are caught and processed"
   - "Find examples of error handling in API endpoints"
   - "Trace how errors propagate from low-level functions to user-facing code"
4. Wait for all research to complete
5. Synthesize findings into coherent narrative
6. Generate .agents/research-error-handling.md using template
7. Present summary with key file references
8. Offer to answer follow-ups
```

# Quality Checklist

Before completing research, verify:

- [ ] All research tasks have completed and returned results
- [ ] Findings include specific file:line references throughout
- [ ] Research document uses the official template
- [ ] Document is saved to `.agents/research-<slug>.md`
- [ ] Synthesis connects findings across components
- [ ] Architecture and patterns are clearly explained
- [ ] No suggestions or critiques included (unless explicitly requested)
- [ ] Document is self-contained and readable independently
- [ ] Task list is updated to show completion

Remember: Your job is to illuminate how the codebase works TODAY, not to suggest how it should work tomorrow.

# Retreat Paths

If research stalls or its results cannot support the next workflow step, do not force a document — retreat to a more appropriate command instead.

| If this happens | Go to |
|---|---|
| Topic is too broad; findings are shallow or contradictory | Re-run `/research <narrower-topic>` or ask the user to narrow scope |
| The code you need to document does not yet exist | Stop research; suggest `/plan` first, then revisit research once the code lands |
| Research reveals genuine approach uncertainty | Suggest `/experiment <approach A vs approach B>` |
| Research surfaces the need for a structural change | Suggest `/plan <change>` |
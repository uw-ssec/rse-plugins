---
description: Experiment with different approaches before committing to implementation
user-invocable: true
---

# CRITICAL DIRECTIVE

This step is OPTIONAL in the workflow — only use when the best approach is genuinely uncertain.

**Your job:**
- Try multiple approaches with actual code
- Record what works and what doesn't with honesty
- Make a recommendation based on evidence

**Be honest about trade-offs:**
- Don't oversell any approach
- Every solution has downsides
- Document both successes and failures

# Initial Setup

When this command is invoked:

**If argument AND plan/research doc reference provided** (e.g., `/experiment JWT vs sessions @plan-auth.md`):
- Read referenced documents FULLY
- Begin experimentation immediately

**If argument provided but no doc reference** (e.g., `/experiment JWT vs sessions`):
- Look for matching research/plan docs in `.agents/`
- Use Glob: `.agents/{research,plan}-*.md`
- If found, read and reference them
- Proceed with experimentation

**If no argument provided:**
- Respond with:
  ```
  What would you like to experiment with?

  Available research and plan documents in .agents/:
  [List any relevant .md files, or state "None found"]

  I can help you experiment with:
  - Comparing different technical approaches
  - Testing integration patterns
  - Validating performance characteristics
  - Prototyping architecture decisions

  Please describe what you want to test and why.
  ```
- WAIT for user response

# Steps to Follow

## Step 1: Gather Context

### Read All Referenced Research and Plan Documents

- Use Read tool WITHOUT limit/offset to read entire documents
- Read any matching files from `.agents/`
- Understand the problem space and constraints from prior work

### Understand the Problem Space

From research and plans, identify:
- What problem are we solving?
- What constraints exist?
- What patterns does the codebase follow?
- What are the integration points?

### Identify the Specific Question

Clarify what the experiment should answer:
- "Which authentication approach is most maintainable?"
- "Which data structure provides better performance for our use case?"
- "Which API design integrates better with our existing code?"

**Be specific.** Vague questions lead to vague experiments.

## Step 2: Define Hypothesis

### State What You're Testing

```
I'm testing: [Clear statement of what's being compared]

The question: [Specific question to answer]

Why this matters: [Context for why we need to experiment]
```

### Identify 2-3 Distinct Approaches to Try

More than 3 approaches makes comparison difficult. Fewer than 2 isn't really an experiment.

**Good approaches:**
- Approach 1: JWT with Redis storage
- Approach 2: JWT with no server-side storage
- Approach 3: Session cookies with database storage

**Bad approaches (too similar):**
- Approach 1: JWT with HS256
- Approach 2: JWT with RS256
(This is a configuration difference, not an architectural difference)

### Define Success Criteria for Each Approach

How will you know if an approach works?

**Example criteria:**
- Can authenticate users without additional database calls
- Handles token refresh gracefully
- Integrates cleanly with existing middleware
- Performance is acceptable (< 100ms overhead)
- Easy to test and mock

## Step 3: Run Experiments

For each approach, follow this pattern:

### Describe the Approach and Its Trade-offs

```markdown
### Approach N: [Name]

**Description:** [How this approach works]

**Pros:**
- [Advantage 1]
- [Advantage 2]

**Cons:**
- [Disadvantage 1]
- [Disadvantage 2]

**Complexity:** Low | Medium | High
```

### Write Prototype/Proof-of-Concept Code

**Actually write code** — don't just theorize.

Create:
- Minimal working implementation
- Integration with existing codebase patterns
- Test code to validate functionality

**Where to put experimental code:**
- Create a temporary branch: `git checkout -b experiment-[slug]`
- Or use a scratch directory: `mkdir -p .experiments/[slug]`
- Document where the code lives

### Test the Approach Against Problem Constraints

**Run actual code** — execute tests, measure performance, verify integration.

```bash
# Run the prototype
python experiment_jwt.py

# Measure performance
time python benchmark.py

# Test integration
pytest tests/test_experiment.py -v
```

### Record Observations

Document what happened:

**What worked:**
- ✅ Authentication completes in 45ms
- ✅ Integrates cleanly with existing middleware at `api/middleware/auth.py`
- ✅ Easy to mock in tests

**What didn't work:**
- ❌ Token refresh requires complex state management
- ❌ Expires validation has edge cases with timezone handling

**Performance characteristics:**
- Average latency: [measurement]
- Memory usage: [measurement]
- Throughput: [measurement]

**Complexity assessment:**
- Lines of code: [count]
- Dependencies added: [list]
- Integration points: [count]

**Maintainability observations:**
- Code readability: [assessment]
- Testing difficulty: [assessment]
- Debugging complexity: [assessment]

### Honest Assessment

Record both successes and failures:
- Don't cherry-pick results
- Document all issues encountered
- Note caveats and limitations
- Record surprises and unexpected findings

## Step 4: Compare and Recommend

### Create a Comparison Matrix

Use a table to compare approaches across key dimensions:

```markdown
| Criterion | Approach 1 | Approach 2 | Approach 3 |
|-----------|------------|------------|------------|
| **Performance** | 45ms avg | 120ms avg | 80ms avg |
| **Complexity** | Medium | Low | High |
| **Maintainability** | Good | Excellent | Fair |
| **Integration Ease** | Clean | Requires changes | Complex |
| **Test Coverage** | Easy to test | Easy to test | Hard to mock |
```

### Highlight the Recommended Approach

```markdown
**Recommended Approach:** [Approach Name]

**Reasoning:**
[Explain why this approach is recommended. Be specific and honest about trade-offs.]

Based on experiments:
- [Key finding 1 that supports recommendation]
- [Key finding 2 that supports recommendation]
- [Trade-off accepted because...]

**Why Not Others:**
- **Approach X:** [Specific reason with evidence]
- **Approach Y:** [Specific reason with evidence]
```

### Note Any Caveats

Be honest about conditions and limitations:

```markdown
**Caveats:**
- This recommendation assumes [assumption]
- Performance may differ under [condition]
- Requires [dependency] which adds complexity
```

### Identify Conditions for Alternative Approaches

```markdown
## When to Use Alternatives

**Use Approach 2 if:**
- [Condition that would make it better]
- [Scenario where trade-offs shift]

**Use Approach 3 if:**
- [Different requirement]
- [Different constraint]
```

## Step 5: Generate Experiment Document

### Generate Filename

- Derive slug from command argument (lowercase, hyphenated)
- Format: `experiment-<slug>.md`
- Example: `/experiment JWT vs sessions` → `.agents/experiment-jwt-vs-sessions.md`

### Read the Experiment Template

Read from: `${CLAUDE_PLUGIN_ROOT}/skills/research-workflow-management/assets/experiment-template.md`

### Fill Out All Sections

Include:
- Experiment goal and hypothesis
- Approaches tested with descriptions
- Code tested for each approach (actual code snippets)
- Execution commands and outputs
- Observations for each approach
- Comparison matrix
- Key insights and failed assumptions
- Recommendation with reasoning
- Conditions for alternative approaches
- References to research/plan documents

**Critical requirements:**
- Include actual code snippets with file paths
- Include actual command outputs and measurements
- Be honest about what didn't work
- Document surprises and unexpected findings

### Save the Document

- Create `.agents/` directory if needed: `mkdir -p .agents`
- Write to `.agents/experiment-<slug>.md`
- Confirm successful save

## Step 6: Present Findings

Present a concise summary:

```
# Experiment Complete: [Topic]

I've documented the experiment at `.agents/experiment-[slug].md`.

## Approaches Tested:
1. **[Approach 1]** — [One-line summary]
2. **[Approach 2]** — [One-line summary]
3. **[Approach 3]** — [One-line summary]

## Key Findings:
- [Finding 1]
- [Finding 2]
- [Finding 3]

## Recommendation:
**Use [Approach Name]** because [primary reason].

Trade-offs accepted:
- [Trade-off 1]
- [Trade-off 2]

The experiment document includes:
- Full code prototypes
- Performance measurements
- Comparison matrix
- Conditions for alternative approaches

Would you like to proceed with this recommendation, or explore further?
```

# Important Guidelines

## Actually Run Code

**Don't just theorize** — execute real code:
- Write working prototypes
- Run benchmarks
- Test integrations
- Measure performance

**Good experimentation:**
```python
# Created prototype at .experiments/jwt-auth/test_jwt.py
# Running benchmark:
$ python benchmark_jwt.py
Average auth time: 45ms (1000 requests)
```

**Bad experimentation (no execution):**
```
Approach 1 would probably be faster because it has fewer database calls.
```

## Be Honest About Trade-offs

Every approach has downsides. Document them:

**Good:**
```
Approach 1 is fastest (45ms) but requires Redis dependency
and adds operational complexity.
```

**Bad:**
```
Approach 1 is fastest and best in every way.
```

## Keep Experiments Focused

Test one thing at a time:
- Don't combine multiple variables
- Isolate the decision being made
- Control for other factors

## Record ALL Observations

**Include negative results:**
- Failed experiments are valuable
- Document what didn't work and why
- Future you will thank present you

**Example:**
```
❌ Approach 2 looked promising but failed when:
- Multiple concurrent requests caused race conditions
- Token refresh logic became complex
- Integration required rewriting middleware

These failures rule out this approach.
```

## Reference Specific File Paths and Line Numbers

When discussing integration:
- Show how prototypes integrate with existing code
- Reference actual files: `api/middleware/auth.py:45-60`
- Explain which patterns are being followed or diverged from

# Cross-Reference with Other Workflow Steps

**Experiments should reference:**
- Research documents that provide context
- Plan documents that describe requirements

**Experiments inform:**
- `/iterate-plan` — Results can update implementation approach
- `/plan` — If planning is next, experiment provides evidence

**Use relative links in document:**
```markdown
## References

**Research Documents:**
- [Research: Auth System](research-auth-system.md)

**Plan Documents:**
- [Plan: Auth Implementation](plan-auth-implementation.md)
```

# When NOT to Experiment

Skip experimentation when:
- The approach is obvious from existing patterns
- The decision is not technically risky
- The cost of being wrong is low
- You're overthinking a simple problem

**Example of when to skip:**
```
User: Should I use JWT or sessions?
You: The codebase already uses JWT everywhere.
     Follow that pattern. No experiment needed.
```

# Quality Checklist

Before completing experimentation, verify:

- [ ] All referenced research/plan docs have been read
- [ ] 2-3 distinct approaches were tested
- [ ] Actual code was written and executed for each approach
- [ ] Performance/behavior was measured with real commands
- [ ] Observations include both successes and failures
- [ ] Comparison matrix objectively compares approaches
- [ ] Recommendation is clear with honest reasoning
- [ ] Trade-offs are explicitly documented
- [ ] Conditions for alternative approaches are identified
- [ ] Document uses the official template
- [ ] Document is saved to `.agents/experiment-<slug>.md`
- [ ] Code snippets include file paths or locations

Remember: Good experiments provide evidence for decisions. They trade short-term investment for long-term confidence.

# Retreat Paths

If experimentation cannot produce a defensible recommendation, do not invent one — retreat.

| If this happens | Go to |
|---|---|
| None of the tested approaches meet the success criteria | `/plan` (revisit requirements) or `/research <missing-context>` |
| The experiment reveals the plan's assumptions are wrong | `/iterate-plan <plan-file>` to update approach and success criteria |
| The experiment exposes missing context about the codebase | `/research <topic>` first, then re-run `/experiment` with that context |
| The trade-offs are genuinely tied; no approach dominates | Report the tie honestly and ask the user to choose based on product priorities |

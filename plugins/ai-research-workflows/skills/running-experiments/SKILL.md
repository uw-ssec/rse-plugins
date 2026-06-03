---
name: running-experiments
description: >-
  Use when the best technical approach is genuinely uncertain and a head-to-head
  prototype comparison is needed before committing to a design. Triggers: should
  I use X or Y, compare approaches, benchmark, which is faster or simpler.
---

# Running Experiments

An OPTIONAL step — only use when the best approach is genuinely uncertain.
Prototype 2-3 distinct approaches with real code, measure them honestly, then
recommend one based on evidence.

## Iron Law: an experiment is real measured code, or it is not an experiment

Every approach you compare must be **actually built and run**. You may never
estimate, reason about, or "fill in" an approach's result — not even the one
everyone is "sure" is slower. A comparison with one side measured and the other
assumed is an opinion with a number stapled to one half; do not present it as an
experiment, and never let it be cited as one in a design doc. If you genuinely
cannot build an approach, say so and label the claim an *unverified assumption*
— never dress it up as a benchmark.

## Interaction mode

This skill leans **Collaborative** by default. For the full Collaborative-vs-Direct protocol and override rules, see the Interaction Modes reference in the `ai-research-workflows:using-research-workflows` skill.

## Starting the skill

If no question is given, enter Collaborative mode and ask what to compare and why.

If a question is provided, look for matching context in `.agents/` (glob
`.agents/{research,plan}-*.md`) and read any relevant documents fully before
proceeding.

## Process

### Step 1: Gather context

- Read all referenced research/plan documents **completely**.
- From those docs, identify: the problem, constraints, codebase patterns, and
  integration points.
- Clarify the specific, measurable question the experiment must answer.

### Step 2: Define hypothesis

State the question, what is being compared, and why the decision matters.

Identify **2-3 distinct approaches**. More than 3 makes comparison difficult;
fewer than 2 is not an experiment. "JWT HS256 vs RS256" is a configuration
difference, not an architectural one — approaches must be architecturally
distinct.

Define success criteria for each: how will you know if it works?

### Step 3: Run experiments

For each approach:

1. **Describe the approach** — pros, cons, complexity rating (Low/Medium/High).

2. **Write and isolate prototype code** — actually write code, do not theorize.
   Isolate it in a temporary branch (`git checkout -b experiment-<slug>`) OR a
   scratch directory (`mkdir -p .experiments/<slug>`). Document where the code
   lives.

3. **Execute** — run tests, benchmarks, and integration checks with real
   commands:

   ```bash
   python experiment_jwt.py
   time python benchmark.py
   pytest tests/test_experiment.py -v
   ```

   For any performance claim, run each benchmark **multiple times and report
   variance** (not a single number), fix seeds, and hold the environment and
   input constant across approaches — you are comparing the design, not the
   noise. Capture the conditions per `ai-research-workflows:ensuring-reproducibility`.

4. **Record observations honestly** — successes and failures both. Include
   performance metrics, complexity assessment (lines of code, dependencies,
   integration points), and maintainability notes. Failed experiments are
   valuable; document them.

### Step 4: Compare and recommend

Create a comparison matrix across key dimensions (performance, complexity,
maintainability, integration ease, test coverage). Then:

```markdown
**Recommended Approach:** [Name]

**Reasoning:** [Specific evidence from experiments]

**Why Not Others:**
- **Approach X:** [Evidence-based reason]
- **Approach Y:** [Evidence-based reason]

**Caveats:** [Conditions where this might not apply]
```

Identify conditions under which an alternative approach would be preferable.

### Step 5: Generate experiment document

Derive a slug from the experiment question (lowercase, hyphenated).

Read the template:
`assets/experiment-template.md`

Fill all sections: goal, hypothesis, approaches, actual code snippets with file
paths, execution commands and outputs, observations (positive and negative),
comparison matrix, key insights, recommendation, and conditions for alternatives.

Save to `.agents/experiment-<slug>.md` (create `.agents/` if needed).

### Step 6: Present findings

Summarize concisely:

```
# Experiment Complete: [Topic]

Documented at `.agents/experiment-[slug].md`.

Approaches: [Approach 1] / [Approach 2] / [Approach 3]

Key findings: [2-3 bullets]

Recommendation: Use [Approach] because [primary reason].
Trade-offs accepted: [list]

Would you like to proceed, or explore further?
```

## When NOT to experiment

Skip experimentation when:
- The approach is obvious from existing codebase patterns.
- The decision is not technically risky.
- The cost of being wrong is low.
- You are overthinking a simple problem.

Example: the codebase already uses JWT everywhere — follow that pattern, no
experiment needed.

## Important guidelines

**Keep experiments focused** — test one architectural variable at a time;
control for other factors.

**Record ALL observations** — negative results are data; document what was tried
and why it was rejected.

**Reference specific file paths** — use `path/to/file.ext:lines` notation to
show how prototypes integrate with existing code.

## Cross-references

Experiments reference research and plan documents in `.agents/`. Results inform
the `ai-research-workflows:iterating-plans` and `ai-research-workflows:planning-implementations` skills. To make a chosen
approach reproducible, use `ai-research-workflows:ensuring-reproducibility`.

## Red flags — STOP, you're fabricating a comparison

| Thought | Reality |
|---|---|
| "We both know X is slower, no need to build it" | Then it costs little to confirm. An unbuilt side is not an experiment. Build both. |
| "No time to build the other approach" | Then it is not an experiment — label it an unverified assumption, don't write it up as a benchmark. |
| "I'll estimate the loop version from experience" | Estimates are opinions. Measure it, or don't claim a comparison. |
| "One run is enough for the number" | One run is noise. Repeat, report variance, fix seeds, hold inputs constant. |

## Common Mistakes

- **Theorizing instead of running code** — describing what an approach "would probably do" without actually writing and executing a prototype produces opinions, not data; always run real commands.
- **Estimating one side of the comparison** — building the favored approach and assuming the other's result is not a head-to-head experiment; measure every approach you compare.
- **Cherry-picking results** — reporting only the winning approach's successes while omitting failures skews the comparison; document what was tried and why it was rejected for every approach.
- **Approaches that are not meaningfully distinct** — comparing two configuration variants (e.g., HS256 vs RS256) instead of architecturally different designs collapses into a config choice, not a real experiment.
- **Running an experiment when the answer is already known** — if the codebase already uses a pattern consistently, follow it; experimentation on settled questions wastes time and produces noise.

## Quality checklist

Before completing, verify:

- [ ] All referenced research/plan docs read completely
- [ ] 2-3 architecturally distinct approaches tested
- [ ] Actual code written and executed for each approach
- [ ] Performance/behavior measured with real commands
- [ ] Observations include both successes and failures
- [ ] Comparison matrix objectively covers key dimensions
- [ ] Recommendation is clear with honest reasoning
- [ ] Trade-offs explicitly documented
- [ ] Conditions for alternative approaches identified
- [ ] Template used from `assets/experiment-template.md`
- [ ] Document saved to `.agents/experiment-<slug>.md`
- [ ] Code snippets include file paths or locations

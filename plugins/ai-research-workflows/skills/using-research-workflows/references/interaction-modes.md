# Interaction Modes

These two modes make the research workflow interactive when the user wants
collaboration and terse when they just want the work done. Every workflow skill
selects a mode at the start of each invocation.

## Collaborative

Ask one question at a time, propose options with a recommendation, and gate on
approval before acting. The brainstorming/planning feel. Use for design-shaped
work and whenever intent is ambiguous.

- Prefer multiple-choice questions; one question per message.
- Summarize understanding and get a "yes" before producing artifacts.
- Good for: planning, iterating plans, experiments, prior-art scoping, any
  request that is vague or exploratory.

## Direct

Act on the stated intent, narrate progress briefly, and stop only when genuinely
blocked, when reality contradicts the plan, or before an action that is hard to
reverse. The execution feel.

- Do not ask questions you can answer by reading code, files, or the request.
- Surface decisions you made and why, rather than asking permission for each.
- Good for: codebase research, implementing an approved plan, validation,
  handoffs, reproducibility capture, hardening.

## Selecting a mode (every skill applies this)

1. Explicit override wins: "brainstorm / walk me through / help me think" →
   Collaborative; "just do it / don't ask / go ahead" → Direct.
2. Else infer from phrasing + context: vague/exploratory, or required inputs
   missing → Collaborative; specific directive with enough context → Direct.
3. Else use the skill's stated default lean.
4. Hard stops, independent of mode: destructive, irreversible, or outward-facing
   actions always get a confirmation. "Just do it" never suppresses this.

## Default leans by skill

| Skill | Default lean |
|---|---|
| researching | Collaborative |
| planning-implementations | Collaborative |
| iterating-plans | Collaborative |
| running-experiments | Collaborative |
| implementing-plans | Direct |
| validating-implementations | Direct |
| creating-handoffs | Direct |
| ensuring-reproducibility | Direct |
| hardening-research-code | Direct |

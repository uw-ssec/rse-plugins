# AI Research Workflows Plugin

A skills-first Claude Code plugin for Research Software Engineers and researchers. It covers the full arc of research-software work — from understanding code and surveying prior art through planning, experimentation, implementation, validation, reproducibility, and handoff. The plugin is interactive when you want collaboration (ask questions, propose options, gate on approval) and direct when you don't (act on intent, narrate briefly, stop only when blocked). Skills auto-trigger from natural language — no slash command required.

**Version:** 0.2.0

## Background & Motivation

Research software is written under pressures that general-purpose development rarely faces all at once: it is exploratory and fast-changing, its correctness is often the actual research result, it must be reproducible by others (and by your future self), and it is frequently handed between students, collaborators, and sessions. AI coding assistants are excellent at *writing* code — but used ad hoc, they tend to skip the very rigor research demands. They jump into edits before understanding the existing code or the prior art, lose the reasoning behind decisions when a session ends, and rarely stop to capture provenance or to verify that a result actually holds.

This plugin exists to put that structure back. It encodes the research-software lifecycle — understand, survey prior art, plan, experiment, implement, validate, reproduce, harden, hand off — as a set of composable **skills** that trigger from plain natural language. Each phase produces a durable, cross-linked Markdown document under `docs/rse/specs/`, so the *context and the decisions* survive beyond a single conversation and transfer cleanly to the next person or session. The aim is to keep an AI assistant honest about the parts of research engineering that are easiest to skip and most expensive to lose.

### Principles

- **Skills, not ceremony.** Describe the task in natural language and the right skill loads; slash commands are just shortcuts. You are never forced through a rigid pipeline — invoke a single skill or chain the whole arc.
- **Durable context.** Every phase writes a versionable artifact to `docs/rse/specs/`, committed to version control alongside the code it describes. Plans cite the research that informed them; implementations cite their plan; handoffs cite everything. Context is a file in your repo, not a chat log.
- **Adaptive interaction.** Collaborative when you want to think together, Direct when you just want the work done — chosen per request (see [Interaction modes](#interaction-modes)).
- **Strategy over mechanics.** The skills decide *what* and *why*, and defer the *how* of environments, tests, packaging, and docs to specialist plugins (see [Cross-plugin deferral](#cross-plugin-deferral)) — so this plugin stays language-agnostic and avoids duplicating their guidance.
- **Research-grade rigor is first-class.** Reproducibility (provenance capture) and hardening (correctness, regression, and stability checks) are dedicated skills, not afterthoughts.

It is built for the needs of Research Software Engineers and researchers. Examples lean toward scientific Python, but the strategy-level guidance applies to any language or runtime.

## Contents

This plugin ships with 1 agent, 10 skills, and 9 commands.

- **1 Agent:** Research Workflow Orchestrator
- **10 Skills:** 7 workflow skills + 2 research-software skills + 1 meta-skill
- **9 Commands:** thin wrappers that invoke the corresponding skill

## Skills

### Workflow skills (7)

| Skill | What it does | Default lean | Output |
|---|---|---|---|
| `researching` | Understand existing code and/or survey external prior work, tools, and methods — produces a combined research doc | Collaborative | `docs/rse/specs/research-<slug>.md` |
| `planning-implementations` | Design a feature, refactor, or multi-file change before coding — phased approach, component dependencies, Automated and Manual success criteria | Collaborative | `docs/rse/specs/plan-<slug>.md` |
| `iterating-plans` | Revise an existing plan with surgical edits — add/remove/split phases, adjust scope, update success criteria, incorporate experiment results | Collaborative | Updated `docs/rse/specs/plan-<slug>.md` |
| `running-experiments` | Compare 2–3 technical approaches with real prototype code and measurements before committing to a design | Collaborative | `docs/rse/specs/experiment-<slug>.md` |
| `implementing-plans` | Execute an approved plan phase by phase — write code, run automated verification after each phase, pause for human verification, track progress with real-time checkmarks | Direct | `docs/rse/specs/implement-<slug>.md` + updated plan |
| `validating-implementations` | Systematically verify a completed implementation against its plan's success criteria — run automated checks, review code vs. spec, list manual tests | Direct | Inline validation report |
| `creating-handoffs` | Produce a handoff document that transfers full working context — state, artifacts, key files, learnings, and next steps — to the next session with no information loss | Direct | `docs/rse/specs/handoff-<timestamp>-<slug>.md` |

### Research-software skills (2)

| Skill | What it does | Default lean | Output |
|---|---|---|---|
| `ensuring-reproducibility` | Capture environment, data references, random seeds, config, and exact commands as a provenance record for a result, analysis, or experiment; verify by re-running | Direct | `## Reproducibility` section in relevant `docs/rse/specs/` doc |
| `hardening-research-code` | Make research/scientific code trustworthy — define correctness criteria, add golden/reference tests, numerical-tolerance checks, and regression guards | Direct | Tests added to codebase |

### Meta-skill (1)

| Skill | What it does |
|---|---|
| `using-research-workflows` | Choose and sequence the right workflow skill; explains Collaborative vs. Direct interaction modes. Use when unsure which skill to invoke. |

## Commands

Commands are thin wrappers — each invokes the corresponding skill. Skills also **auto-trigger from natural language**: describe the task and the right skill loads automatically.

| Command | Invokes skill | Short description |
|---|---|---|
| `/research` | `researching` | Understand existing code and/or survey external prior art |
| `/plan` | `planning-implementations` | Create a phased implementation plan |
| `/iterate-plan` | `iterating-plans` | Revise an existing plan |
| `/experiment` | `running-experiments` | Compare approaches with real prototype code |
| `/implement` | `implementing-plans` | Execute an approved plan phase by phase |
| `/validate` | `validating-implementations` | Verify implementation against plan criteria |
| `/handoff` | `creating-handoffs` | Write a context-transfer document |
| `/reproduce` | `ensuring-reproducibility` | Capture provenance so a result can be reproduced |
| `/harden` | `hardening-research-code` | Add correctness and regression tests to research code |

## Interaction modes

Every skill begins by choosing one of two modes:

- **Collaborative** — asks one focused question at a time, proposes options with a recommendation, and gates on your approval before producing artifacts. Use for brainstorming, planning, and exploratory work where your input shapes the outcome.
- **Direct** — acts on stated intent, narrates progress briefly, and stops only when genuinely blocked or before an irreversible action. Use when the task is clear and you want results without back-and-forth.

**How the mode is chosen:**

1. Explicit user phrasing wins: "brainstorm / walk me through / help me think" → Collaborative; "just do it / don't ask / go ahead" → Direct.
2. Otherwise infer: vague or exploratory phrasing, or required inputs missing → Collaborative; a specific directive with enough context → Direct.
3. Else use the skill's default lean (shown in the tables above).
4. Hard stops regardless of mode: destructive, irreversible, or outward-facing actions always require confirmation.

Full protocol: [`skills/using-research-workflows/references/interaction-modes.md`](skills/using-research-workflows/references/interaction-modes.md)

## `docs/rse/specs/` — workflow artifacts

All workflow documents are saved to `docs/rse/specs/` in the project root, and are **meant to be committed to version control** alongside the code they describe — they are the durable decision record, not scratch files. The directory is created automatically on first use.

Documents from an earlier version of this plugin may live in a legacy `.agents/` directory. Skills still **read** from `.agents/` as a fallback when a document isn't found under `docs/rse/specs/`, but always **write** new documents to `docs/rse/specs/`.

| Document type | Naming pattern | Example |
|---|---|---|
| Research (codebase and/or prior art) | `research-<slug>.md` | `research-auth-system.md` |
| Implementation plan | `plan-<slug>.md` | `plan-oauth-support.md` |
| Experiment report | `experiment-<slug>.md` | `experiment-jwt-vs-session.md` |
| Implementation summary | `implement-<slug>.md` | `implement-oauth-support.md` |
| Handoff | `handoff-<timestamp>-<slug>.md` | `handoff-20240315-auth-system.md` |

Documents cross-link using relative paths (`## References` sections), creating a navigable graph of technical decisions: a plan links to the research docs that informed it; an implementation summary links back to the plan; a handoff document cites all relevant artifacts. Legacy `prior-art-<slug>.md` documents from earlier versions are still read when present.

## Cross-plugin deferral

Some activities are intentionally delegated to specialist plugins:

| Need | Defer to |
|---|---|
| Conda / pixi environment management | `scientific-python-development:pixi-package-manager` |
| pip / uv environment management | `python-development:uv-package-manager` |
| Writing or running Python tests | `scientific-python-development:python-testing` |
| Python packaging and distribution | `scientific-python-development:python-packaging` |
| Sphinx / MkDocs / Quarto documentation | `scientific-python-development:scientific-documentation` |
| Community health files (CODE_OF_CONDUCT, CONTRIBUTING) | `project-management:community-health-files` |
| Project handoff (end-of-engagement summary) | `project-management:project-handoff` |
| Heavy multi-source, fact-checked research | `deep-research` |

## Workflow patterns

### Pattern 1: Full workflow (complex changes)

For significant features or architectural changes requiring thorough documentation:

```
/research [topic]           → Understand current code and/or external prior art
/plan [feature]             → Create phased implementation plan
/experiment [comparison]    → (Optional) Prototype and compare approaches
/iterate-plan [adjustments] → Refine plan based on findings
/implement [plan-file]      → Execute plan with per-phase verification
/validate [plan-file]       → Verify against success criteria
/reproduce [result]         → Capture provenance for key results
```

### Pattern 2: Simple feature (known pattern)

For straightforward additions that follow existing patterns:

```
/research [existing patterns]
/plan [new feature]
/implement [plan-file]
/validate [plan-file]
```

### Pattern 3: Rapid iteration (approach already clear)

When you have enough context and just need to plan and build:

```
/plan [feature]
/iterate-plan [scope adjustment]
/implement [plan-file]
```

### Pattern 4: Research only (building context)

For understanding a codebase without immediate implementation intent:

```
/research [system A]
/research [system B]
[Documents in docs/rse/specs/ available for future planning]
```

### Pattern 5: Research-first (prior art informs design)

For work where design decisions depend on what already exists in the field:

```
/research [domain / question]    → Understand existing code and/or survey external approaches
/plan [feature]                  → planning-implementations picks up research doc automatically
```

## Installation

This plugin is part of the `uw-ssec/rse-plugins` collection. To install from the marketplace:

```bash
# Add the rse-plugins marketplace
claude plugin marketplace add uw-ssec/rse-plugins

# Install the plugin
claude plugin install ai-research-workflows@rse-plugins
```

To use directly from a local clone:

```bash
git clone https://github.com/uw-ssec/rse-plugins.git
```

Verify installation:

```bash
/help
```

## Contributing

We welcome contributions to this plugin. You can:

- **Add or improve skills** — extend workflow guidance in `skills/`
- **Enhance commands** — update command prompts in `commands/`
- **Improve the agent** — adjust orchestration in `agents/`
- **Report issues** — open an issue on [GitHub](https://github.com/uw-ssec/rse-plugins/issues) with the label `ai-research-workflows`
- **Share examples** — contribute real-world usage patterns

See the main repository [CONTRIBUTING.md](../../CONTRIBUTING.md) for detailed guidelines.

## License

This plugin is part of the RSE Plugins project. See [LICENSE](LICENSE) file for details.

## Authors

SSEC Research Team — [https://github.com/uw-ssec](https://github.com/uw-ssec)

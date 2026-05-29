---
name: research-workflow-management
description: Orchestration skill for the six-phase AI research workflow (Research → Plan → Iterate → Experiment → Implement → Validate). Loaded by the research-workflow-orchestrator agent to select the next workflow command, enforce `.agents/` naming, and wire cross-references between phase documents.
user-invocable: false
metadata:
  assets:
    - assets/research-template.md
    - assets/plan-template.md
    - assets/experiment-template.md
    - assets/implement-template.md
    - assets/handoff-template.md
---

# Research Workflow Management

Orchestrates six slash commands into a single auditable workflow. Each phase produces a markdown artifact under `.agents/` that the next phase consumes.

## Phase → Command → Artifact

| Phase | Command | Input | Artifact |
|-------|---------|-------|----------|
| Research | `/research <topic>` | topic string | `.agents/research-<slug>.md` |
| Plan | `/plan <feature>` | feature name | `.agents/plan-<slug>.md` |
| Iterate Plan | `/iterate-plan <plan-file> <changes>` | existing plan + edit brief | edits plan in place |
| Experiment | `/experiment <question>` | approach question | `.agents/experiment-<slug>.md` |
| Implement | `/implement <plan-file>` | approved plan path | `.agents/implement-<slug>.md` |
| Validate | `/validate <plan-file>` | plan path | inline validation report |

Slugs are lowercased-hyphenated from the argument: `/research "Auth System"` → `research-auth-system.md`.

## Decision Tree — Which Command Next

```
Need to understand existing code?
  → /research <topic>

Ready to design an implementation?
  ├─ research docs already exist?
  │    → /plan <feature>
  └─ no research?
       → /research first, then /plan

Plan exists but needs edits?
  → /iterate-plan .agents/plan-<slug>.md "<changes>"

Uncertain which approach wins?
  → /experiment "<A vs B question>"

Plan is approved?
  → /implement .agents/plan-<slug>.md

Implementation claimed complete?
  → /validate .agents/plan-<slug>.md
```

Command-level trigger details live in each command file's `## When to use` section — do not duplicate them here.

## Concrete Command Examples

```bash
# 1. Build context on an unfamiliar subsystem
/research "How does the auth middleware verify session tokens"
# → .agents/research-how-does-the-auth-middleware-verify-session-tokens.md

# 2. Plan a feature that builds on that research
/plan "Add OAuth2 provider to auth system"
# → .agents/plan-add-oauth2-provider-to-auth-system.md

# 3. Adjust the plan after review feedback
/iterate-plan .agents/plan-add-oauth2-provider-to-auth-system.md \
  "Split Phase 2 into token-exchange and refresh-flow subphases"

# 4. Compare approaches when the plan is ambiguous
/experiment "JWT in HttpOnly cookie vs Bearer header for SPA clients"

# 5. Execute the approved plan
/implement .agents/plan-add-oauth2-provider-to-auth-system.md

# 6. Verify the implementation against plan criteria
/validate .agents/plan-add-oauth2-provider-to-auth-system.md
```

## Cross-Referencing Rules

Every artifact links back to the artifacts that informed it. Use relative markdown links inside `.agents/`:

- **Plan docs** include a `## References` section listing every research doc consulted
- **Experiment docs** reference both the research and the plan that motivated them
- **Implement docs** reference the exact plan file being executed
- **Validation reports** reference both the plan and the implement doc

Example (inside `plan-auth-system.md`):

```markdown
## References

- [Research: Auth System](research-auth-system.md)
- [Research: Session Storage](research-session-storage.md)
```

This creates a navigable graph: every claim in any document traces back to the research that supports it.

## Success Criteria Format

Plans must split success criteria into two groups so `/validate` can execute the automated half:

```markdown
## Success Criteria

### Automated
- [ ] `pytest tests/auth/` passes
- [ ] `ruff check src/auth/` reports zero errors
- [ ] `mypy src/auth/` reports zero errors

### Manual
- [ ] Login flow works end-to-end in staging
- [ ] Session persists across browser restart
```

`/validate` runs each Automated command verbatim and records pass/fail with output; it lists Manual items for the human to confirm.

## Templates

Templates live in `${CLAUDE_PLUGIN_ROOT}/skills/research-workflow-management/assets/`. Commands load them directly — do not inline template content into this skill.

- `research-template.md`
- `plan-template.md`
- `experiment-template.md`
- `implement-template.md`
- `handoff-template.md`

## Additional Resources

- **`references/checklists.md`** — Full per-phase quality-gate checklists. Load when executing a phase and needing a complete pre-commit checklist.

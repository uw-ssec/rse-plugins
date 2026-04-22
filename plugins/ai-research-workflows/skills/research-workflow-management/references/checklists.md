# Per-Phase Checklists

Detailed checklists for each workflow phase. Load when executing a specific phase and needing a complete quality gate.

## Research Phase (`/research`)

- [ ] Read referenced files completely (no partial reads)
- [ ] Use parallel sub-agents when exploring >2 independent areas
- [ ] Include specific file paths and line numbers (`path/to/file.py:42`)
- [ ] Document patterns and current behavior, not critiques
- [ ] Save to `.agents/research-<slug>.md`

**Verification:** `test -f .agents/research-<slug>.md && grep -q '^## ' .agents/research-<slug>.md`

## Plan Phase (`/plan`)

- [ ] Reference existing research docs in `## References` section
- [ ] Read all context files completely before delegating sub-tasks
- [ ] Ask focused questions that cannot be answered from code alone
- [ ] Split success criteria into **Automated** (commands) and **Manual** (human checks)
- [ ] Include `## What We're NOT Doing` section
- [ ] Resolve every open question before marking the plan complete
- [ ] Save to `.agents/plan-<slug>.md`

**Verification:** Confirm plan contains `## Success Criteria`, `## Phases`, and `## What We're NOT Doing`.

## Iterate Plan Phase (`/iterate-plan`)

- [ ] Verify assumptions with code research before editing
- [ ] Confirm understanding with user before applying changes
- [ ] Preserve existing phase numbering and cross-references
- [ ] Edit the plan in place, not as a new file

## Experiment Phase (`/experiment`, optional)

- [ ] State hypothesis and success criteria up front
- [ ] Actually run prototype code — no pure theorizing
- [ ] Record failures alongside successes
- [ ] Produce a comparison table with trade-offs
- [ ] End with a single recommendation and reasoning
- [ ] Save to `.agents/experiment-<slug>.md`

## Implement Phase (`/implement`)

- [ ] Read the plan and all referenced files completely
- [ ] Create a task list mirroring the plan's phases
- [ ] Implement phases sequentially (never in parallel)
- [ ] Update plan checkmarks (`[ ]` → `[x]`) as sections complete
- [ ] Run the plan's automated verification commands after each phase
- [ ] Pause for human verification between phases
- [ ] Stop and flag any divergence between plan and reality
- [ ] Save implementation summary to `.agents/implement-<slug>.md`

## Validate Phase (`/validate`)

- [ ] Read the plan completely before running checks
- [ ] Execute every automated verification command listed in the plan
- [ ] Record pass/fail for each Success Criteria item with command output
- [ ] List manual testing steps the user must run
- [ ] Identify and flag deviations from the plan
- [ ] Provide actionable next steps (iterate, fix, or ship)

**Verification commands typically include:**
- `<test command>` — e.g. `pytest tests/`, `npm test`, `cargo test`
- `<lint command>` — e.g. `ruff check .`, `eslint src/`
- `<type check>` — e.g. `mypy .`, `tsc --noEmit`
- `<build>` — e.g. `npm run build`, `cargo build --release`

The specific commands come from the plan's Success Criteria section, not this skill.

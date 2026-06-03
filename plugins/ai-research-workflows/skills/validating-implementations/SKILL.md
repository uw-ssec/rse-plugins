---
name: validating-implementations
description: >-
  Use when an implementation is (claimed) complete and must be checked against
  its plan before shipping. Triggers: validate the implementation, verify it
  matches the plan, is the implementation correct, check before PR.
---

# Validating Implementations

Systematically verify that a completed implementation satisfies every success
criterion in its plan, producing an inline validation report.

## Interaction mode

This skill leans **Direct** by default. For the full Collaborative-vs-Direct protocol and override rules, see `${CLAUDE_PLUGIN_ROOT}/skills/using-research-workflows/references/interaction-modes.md`.

## Starting the skill

**If a plan path is provided**, read it completely — this is the specification
to validate against.

**If no plan path is given**, search `.agents/{plan,implement}-*.md`. If
multiple match, ask which to validate (Collaborative); if exactly one, proceed
(Direct). If none found, explain that validation requires a plan.

## Determine session context

**Existing session (implementation done in this conversation):**
- You have context about what was implemented; review recent conversation.
- You know which files were modified.

**Fresh session (reviewing past work):**
- No memory of implementation decisions; reconstruct from git and artifacts.
- Focus on observable facts: does the code match the plan, do tests pass, are
  success criteria met?
- Don't speculate about intent; note deviations without judging them.

## Gather implementation evidence

Before validating, understand what was actually done.

Check recent commits:

```bash
git log --oneline -n 10
git diff HEAD~3..HEAD --stat
```

Run tests to establish baseline:

```bash
make test
# or: pytest tests/ -v
# or: npm test
```

## Validation process

### Step 1: Read the plan completely

Read the entire plan (avoid partial reads). For each phase identify:

- Which files should be modified
- Success criteria that must pass
- Key functionality that should exist
- Tests that should be added

### Step 2: Investigate in parallel

Verify code, schema, and test coverage concurrently when possible:

- **Database/schema changes** — confirm migrations match plan specifications
  (tables, columns, indices).
- **Code changes** — confirm implementation follows patterns and matches the
  plan's design.
- **Test coverage** — find tests added for the feature; verify they cover the
  scenarios listed in the plan's Testing Strategy section.

Wait for ALL verification to complete before synthesizing.

### Step 3: Systematic per-phase validation

For each phase in the plan:

**Check completion status** — `- [x]` = claimed complete; `- [ ]` = incomplete.

**Verify actual code matches claimed completion** — don't trust checkmarks.
Read the code: are the files modified as described? Does the implementation
match the specification?

**Run automated verification** — execute EACH command from the plan's
"Automated Verification" section:

```bash
make test
pytest tests/ -v
npm run lint
mypy src/
```

Document results per check:

```markdown
- ✅ `make test` — All 45 tests passing (expected 45)
- ❌ `pytest tests/test_new_feature.py` — 2 tests failing (expected 0)
- ✅ `mypy src/` — Type checking passed
```

**If a check fails:**

1. Read the error output.
2. Identify the failing code.
3. Determine whether it is an implementation bug, a test bug, a plan mismatch,
   or an environmental issue.
4. Document the finding with root cause, location, and recommendation.

**Assess manual criteria** — for items in the plan's "Manual Verification"
section, list what needs human testing with clear, actionable steps. If in the
same session and the user already confirmed, note that; otherwise assume manual
testing is still needed.

## Validation report

Output the report inline in the conversation. Use the section templates and
presentation/special-case blocks from
`${CLAUDE_PLUGIN_ROOT}/skills/validating-implementations/references/report-templates.md`.

The report contains these sections in order:

1. **Implementation Status** — per-phase completion status with task-level detail
2. **Automated Verification Results** — pass/fail for each command, with root
   cause and recommendation for failures
3. **Code Review Findings** — what matches the plan, deviations, potential issues
4. **Manual Testing Required** — actionable steps for items needing human testing
5. **Recommendations** — grouped by Critical / Important / Nice to Have / Follow-Up

## Common Mistakes

- **Trusting plan checkmarks without running the checks** — a `- [x]` in the
  plan means nothing until you execute the verification command and confirm the
  output yourself.
- **Reporting "looks done" without executing automated verification** — always
  run every command in the plan's "Automated Verification" section; do not
  substitute code inspection for running the checks.
- **Not separating automated vs. manual results** — clearly distinguish what was
  machine-verified from what still requires human testing; never mark manual
  items done unless the user confirmed them in this session.
- **Speculating about intent on deviations** — in a fresh session, document
  deviations as observable facts and ask if their reason matters; do not invent
  explanations.
- **Stopping at the first failure** — run all checks regardless of early
  failures so the report captures the full picture.

## Quality checklist

Before delivering the report:

- [ ] Read the entire plan
- [ ] Ran all automated verification commands from the plan
- [ ] Documented pass/fail for each automated check
- [ ] Investigated root causes of any failures
- [ ] Reviewed actual code against plan specifications
- [ ] Identified all deviations from plan
- [ ] Listed clear manual testing steps
- [ ] Provided actionable recommendations
- [ ] Categorized issues by severity (critical, important, nice-to-have)
- [ ] All phases marked complete are actually done
- [ ] No regressions introduced in existing functionality
- [ ] Documentation updated if needed (README, API docs, docstrings)

## Cross-references

Validates the plan from the `planning-implementations` skill. For failures, fix
and re-run, or use `iterating-plans` if the plan itself was wrong.

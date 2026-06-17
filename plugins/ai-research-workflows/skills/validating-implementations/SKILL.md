---
name: validating-implementations
description: >-
  Use when an implementation is (claimed) complete and must be checked against
  its plan before shipping. Triggers: validate the implementation, verify it
  matches the plan, is the implementation correct, check before PR.
---

# Validating Implementations

Systematically verify that a completed implementation satisfies every success
criterion in its plan, producing a validation report — written to `docs/rse/specs/validation-<slug>.md` and also presented inline.

## Iron Law: no verdict without fresh output you produced yourself

A validation verdict is only as good as the evidence behind it. Checkmarks in
the plan (`- [x]`), a teammate's "all 45 tests green, ready for PR" report, and
"it looks done" are **claims, not evidence**. Do not give a verdict until you
have re-run every automated verification command yourself and read the actual
code against each success criterion. Trust nothing you did not see with your own
eyes — no matter who reported it or how reliable they seem. "Just confirm it's
good" is a request to validate, not to rubber-stamp someone else's report.

## Interaction mode

This skill leans **Direct** by default. For the full Collaborative-vs-Direct protocol and override rules, see the Interaction Modes reference in the `ai-research-workflows:using-research-workflows` skill.

## Starting the skill

**If a plan path is provided**, read it completely — this is the specification
to validate against.

**If no plan path is given**, search `docs/rse/specs/{plan,implement}-*.md` (then legacy `.agents/{plan,implement}-*.md`). If
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
- **Reproducibility & correctness (research code)** — if the implementation
  produces results, metrics, or figures, confirm seeds, data versions,
  environment, and exact commands were captured
  (`ai-research-workflows:ensuring-reproducibility`) and that numerical results
  meet their stated criteria/tolerances
  (`ai-research-workflows:hardening-research-code`). Re-run to confirm reported
  numbers actually reproduce.

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

Produce the report once, then **both** write it to a durable file and present it
inline. Use the section templates and presentation/special-case blocks from
`references/report-templates.md`.

### Write the validation document

Derive the slug from the plan being validated (`docs/rse/specs/plan-<slug>.md` →
`<slug>`; e.g. `plan-oauth-support.md` → `oauth-support`). Write the full report
to `docs/rse/specs/validation-<slug>.md`, overwriting any previous validation of
the same plan — git history preserves earlier verdicts. Create `docs/rse/specs/`
if it does not exist.

Record provenance at the top so a reader knows exactly what this verdict covers:

> Validated against `plan-<slug>.md` / `implement-<slug>.md` at commit
> `<short-sha>` (`git rev-parse --short HEAD`) on `<date>`.

End the document with a `## References` section linking back to the plan and
implementation docs with relative paths.

### Present inline

Present the same report inline in the conversation (Direct mode: write the file,
then show the report and confirm its path). The report contains these sections in
order:

1. **Implementation Status** — per-phase completion status with task-level detail
2. **Automated Verification Results** — pass/fail for each command, with root
   cause and recommendation for failures
3. **Code Review Findings** — what matches the plan, deviations, potential issues
4. **Manual Testing Required** — actionable steps for items needing human testing
5. **Recommendations** — grouped by Critical / Important / Nice to Have / Follow-Up

## Red flags — STOP, you're about to rubber-stamp

| Thought | Reality |
|---|---|
| "The engineer said all tests pass, I'll confirm" | A teammate's green report is an unverified claim, same as a checkmark. Re-run it yourself. |
| "All phases are checked `[x]`, looks done" | Checkmarks are claims. Nothing is verified until you see fresh output. |
| "Re-running takes 10 minutes, just sign off" | The 10 minutes is the cost of a verdict you can stand behind. Run it. |
| "The numbers look reasonable" | For research results, "reasonable" isn't reproduced. Confirm they re-run within tolerance. |

## Common Mistakes

- **Trusting a teammate's green report** — a Slack "all tests pass, ready for
  PR" is an unverified claim exactly like a checkmark; re-run every command
  yourself before any verdict.
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
- [ ] Ran all automated verification commands from the plan **myself** (not trusting reports or checkmarks)
- [ ] For research results: confirmed reproducibility capture and that reported numbers re-run within tolerance
- [ ] Documented pass/fail for each automated check
- [ ] Investigated root causes of any failures
- [ ] Reviewed actual code against plan specifications
- [ ] Identified all deviations from plan
- [ ] Listed clear manual testing steps
- [ ] Provided actionable recommendations
- [ ] Categorized issues by severity (critical, important, nice-to-have)
- [ ] Saved the report to `docs/rse/specs/validation-<slug>.md` with provenance + References
- [ ] All phases marked complete are actually done
- [ ] No regressions introduced in existing functionality
- [ ] Documentation updated if needed (README, API docs, docstrings)

## Cross-references

Validates the plan from the `ai-research-workflows:planning-implementations` skill. For failures, fix
and re-run, or use `ai-research-workflows:iterating-plans` if the plan itself was wrong.

---
name: usability-evaluation
description: Use when auditing an existing interface for usability issues, when running a heuristic evaluation or cognitive walkthrough, when scoring an SUS survey, or when prioritizing UX bugs by severity.
metadata:
   references:
   - references/nielsen-heuristics.md
   - references/scoring-methods.md
   - references/walkthrough-guide.md
---

# Usability Evaluation

## Heuristic evaluation workflow

1. **Recruit 3-5 evaluators** with UX knowledge (returns diminish past 5).
2. **Each evaluates independently** against Nielsen's 10 heuristics — record screen, heuristic, description, severity, fix.
3. **Merge** — dedupe, average severity.
4. **Calibrate** — evaluators review each other's severity ratings together; resolve disagreements > 1 point. Goal: inter-rater agreement on severity within ±1.
5. **Prioritize and report** — sort by severity desc; deliver top issues with screenshots + fixes.

**Pass/fail gates before sign-off:**
- All severity-4 issues have an owner and a fix landing this release.
- No severity-3 issue is "won't fix" without explicit product approval.

## Nielsen's 10 heuristics (cheat sheet)

1. Visibility of system status
2. Match between system and real world
3. User control and freedom
4. Consistency and standards
5. Error prevention
6. Recognition rather than recall
7. Flexibility and efficiency of use
8. Aesthetic and minimalist design
9. Help users recognize, diagnose, and recover from errors
10. Help and documentation

Full descriptions: [nielsen-heuristics.md](references/nielsen-heuristics.md).

## Severity scale

| Rating | Label | Definition | Action |
|--------|-------|------------|--------|
| 0 | Not a problem | Disagreement; not a usability issue | None |
| 1 | Cosmetic | Noticed but doesn't affect task | Backlog |
| 2 | Minor | Slows user; can still complete | Next iteration |
| 3 | Major | Significant difficulty; some fail | Before next release |
| 4 | Catastrophe | Cannot complete task | Immediate |

## Finding template (use this exact format)

```
ID: HE-018
Screen: Checkout > Shipping Address
Component: AddressForm
State: Empty / first-load

Heuristic violated: H5 (Error prevention) + H9 (Help recover from errors)

Description:
The ZIP code input accepts arbitrary characters and the form does not
validate until submit. Users entering letters or short ZIPs see the
generic top-of-form error "Please fix the highlighted fields" with no
indication that ZIP is the culprit. Screenshot: see Fig. 18 — error
banner is 3 viewports above the failing field on mobile.

Severity: 3 (Major)
Frequency: occurs to every user with input error · Impact: high
Persistence: until user finds the right field

Recommended fix:
1. Apply inputmode="numeric" pattern="\d{5}(-\d{4})?" maxlength="10".
2. Validate on blur; show inline error directly under the field.
3. Auto-scroll to first invalid field on submit.
4. Replace generic banner with specific message ("ZIP code must be 5 digits").

Effort: S (frontend only) · Owner: TBD
```

## Cognitive walkthrough (4 questions per step)

Inputs: user goal, action sequence, expected experience level.

For each step, answer:
- Q1: Will the user try to achieve the right effect? (Is this step's purpose clear?)
- Q2: Will the user notice the correct action is available? (Visible? Looks interactive?)
- Q3: Will the user associate the action with the desired effect? (Label/icon clear?)
- Q4: Will the user see progress after acting? (Feedback present?)

Any "no" = a usability finding. Document step number, failed question, recommendation. Full method: [walkthrough-guide.md](references/walkthrough-guide.md).

## SUS quick reference

Administer the 10-item SUS questionnaire post-task. Score:
- Odd items: score − 1
- Even items: 5 − score
- Sum × 2.5 = SUS score (0-100)

**Benchmarks:** < 50 unacceptable · 50-67 marginal · 68 industry avg · 68-80 good · 80-90 excellent · > 90 best-in-class.

Full questionnaire, alternative scales (SEQ, NASA-TLX, SUPR-Q), scorecards: [scoring-methods.md](references/scoring-methods.md).

## When to use which method

| Goal | Method |
|------|--------|
| Quick sweep of any screen | Heuristic evaluation (2-4 hrs, 3-5 evaluators) |
| Onboarding / first-time UX | Cognitive walkthrough |
| Benchmark perceived usability over releases | SUS survey post-test |
| Per-task difficulty | Single Ease Question (SEQ) |
| Validate suspected issues with real users | Moderated usability testing (5-8 participants) |

## Next Steps

- **[Accessibility Audit](../accessibility-audit/SKILL.md)** — extend to WCAG 2.2
- **[User Research](../user-research/SKILL.md)** — validate suspected issues with users

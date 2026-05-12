---
name: ab-testing-strategy
description: Use when designing or analyzing an A/B test, calculating sample size for an experiment, evaluating whether a variant won, debugging surprising experiment results, or choosing between frequentist and Bayesian analysis for a design change.
metadata:
   references:
   - references/analysis-methods.md
   - references/hypothesis-template.md
   - references/test-design-guide.md
---

# A/B Testing Strategy

## Workflow

### Step 1 — Write the hypothesis

Format: **"If we [change], then [metric] will [direction by amount] because [evidence]."**

Example: "If we cut sign-up fields from 6 to 3, completion rate will increase by 15% because reducing form length lowers perceived effort (Baymol 2023)."

**Checkpoint — verify all four before Step 2:**
- [ ] Specific (names the change and metric)
- [ ] Measurable (already instrumented in analytics)
- [ ] Grounded (cites research, heuristic, or prior data)
- [ ] Falsifiable (can be proven wrong)

### Step 2 — Pick metrics

- **Primary:** one — conversion, completion, revenue/user.
- **Guardrails (1–2):** must not degrade — load time, error rate, downstream retention.
- **Counter:** monitor for side effects — lead quality if form shortened, completion speed if friction added.

**Checkpoint:** Confirm all metrics are instrumented and flowing to your analytics destination *before* launching. Verify by inspecting the last 24h of events for non-zero counts.

### Step 3 — Calculate sample size

```python
# sample_size.py — required n per variant
from math import ceil
from scipy.stats import norm

def sample_size_per_variant(baseline_rate, mde_absolute, alpha=0.05, power=0.80):
    """Two-proportion z-test, two-sided."""
    z_alpha = norm.ppf(1 - alpha / 2)
    z_beta  = norm.ppf(power)
    p1 = baseline_rate
    p2 = baseline_rate + mde_absolute
    p_bar = (p1 + p2) / 2
    numerator = (z_alpha * (2 * p_bar * (1 - p_bar)) ** 0.5
                 + z_beta * (p1 * (1 - p1) + p2 * (1 - p2)) ** 0.5) ** 2
    n = numerator / (mde_absolute ** 2)
    return ceil(n)

# Example: baseline 5%, detect lift to 6% (MDE = 0.01)
print(sample_size_per_variant(0.05, 0.01))  # → 7,663 per variant
```

Divide total n by daily traffic to get duration. **Always run a minimum of one full business cycle (7–14 days)** even if n is reached earlier, to absorb day-of-week effects.

### Step 4 — Launch & wait

Do not peek. Peeking at p < 0.05 ten times inflates false-positive rate to ~40%.

**Checkpoint:** Set a calendar alert for the predetermined end date. Do not analyze before.

### Step 5 — Analyze

```python
# analyze.py — chi-squared significance + 95% CI for absolute lift
from scipy.stats import chi2_contingency, norm

def analyze_ab(visitors_a, conv_a, visitors_b, conv_b, alpha=0.05):
    table = [[conv_a, visitors_a - conv_a],
             [conv_b, visitors_b - conv_b]]
    chi2, p, _, _ = chi2_contingency(table, correction=False)
    p1, p2 = conv_a / visitors_a, conv_b / visitors_b
    diff = p2 - p1
    se = (p1 * (1 - p1) / visitors_a + p2 * (1 - p2) / visitors_b) ** 0.5
    z = norm.ppf(1 - alpha / 2)
    ci = (diff - z * se, diff + z * se)
    return {"p_value": p, "lift_abs": diff, "lift_rel": diff / p1, "ci_95": ci, "significant": p < alpha}

print(analyze_ab(10000, 500, 10000, 580))
# → {'p_value': 0.0098, 'lift_abs': 0.008, 'lift_rel': 0.16, 'ci_95': (0.0019, 0.0141), 'significant': True}
```

**Decision rule:**
- `p < 0.05` AND CI excludes 0 AND no guardrail degraded → **ship B**.
- `p < 0.05` AND any guardrail dropped beyond its tolerance → **do not ship; investigate trade-off**.
- `p ≥ 0.05` → **inconclusive**. Either accept null or extend if powered sample wasn't reached.

Always check segment-level results (mobile vs desktop, new vs returning) — opposing effects can cancel in aggregate.

## Reference Cheatsheet

| Variable | Default |
|----------|---------|
| Alpha (significance) | 0.05 |
| Power (1 − β) | 0.80 |
| Minimum runtime | 1–2 weeks |
| Peeking allowed | Only with sequential / Bayesian methods |

## Deep Dive References

- [references/hypothesis-template.md](references/hypothesis-template.md) — hypothesis framework, 10 examples, outcome documentation
- [references/test-design-guide.md](references/test-design-guide.md) — test types, allocation, QA checklist, common mistakes
- [references/analysis-methods.md](references/analysis-methods.md) — frequentist vs Bayesian, sequential testing, multiple comparison correction, practical vs statistical significance, common pitfalls

## Next Steps

- **usability-evaluation** — when a variant wins, run heuristic eval to understand *why*.
- **user-research** — when results surprise, run qualitative follow-up.

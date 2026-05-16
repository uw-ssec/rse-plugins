[Back to AB Testing Strategy](../ab-testing-strategy.md)

# A/B Test Design Guide

## Overview

Proper test design is the foundation of trustworthy experimentation. A poorly designed test wastes traffic, produces misleading results, and erodes organizational confidence in experimentation. This guide covers test types, traffic allocation, duration planning, segmentation, common mistakes, QA, and documentation.

---

## Test Types

### A/B Test (Split Test)

The simplest and most common design. Traffic is split between a control (A) and a single variant (B).

**When to use:**
- Testing a single, specific change
- Limited traffic that cannot support multiple variants
- When you need the fastest path to a clear result

**Strengths:** Easy to implement, easy to analyze, requires the least traffic.

**Limitations:** Tests only one change at a time; cannot reveal interaction effects between multiple changes.

### A/B/n Test

Traffic is split among a control and two or more variants (B, C, D, etc.).

**When to use:**
- Comparing multiple alternative designs against the control
- Exploring a range of approaches before committing
- When you have sufficient traffic to power all variants

**Considerations:**
- Each additional variant increases the total sample size required
- With k variants, you need approximately k times the per-variant sample size
- Apply multiple comparison correction when comparing variants against each other
- Limit to 3-4 variants maximum to keep tests manageable

```
Traffic split example (4 variants):
Control: 25% | Variant B: 25% | Variant C: 25% | Variant D: 25%
```

### Multivariate Test (MVT)

Tests multiple factors simultaneously to understand individual and combined effects.

**When to use:**
- Optimizing multiple page elements at once (headline, image, CTA)
- Understanding interaction effects between elements
- High-traffic pages where you can afford large sample sizes

**Design types:**
- **Full factorial:** Tests every combination of all factor levels. A test with 3 headlines x 2 images x 2 CTAs = 12 combinations.
- **Fractional factorial:** Tests a strategically chosen subset of combinations to reduce traffic requirements while still estimating main effects.

**Considerations:**
- Traffic requirements grow multiplicatively with each factor
- Analysis is more complex (requires ANOVA or regression)
- Results can be harder to communicate to stakeholders
- Reserve for high-traffic pages (100,000+ visitors per test period)

### Multi-Armed Bandit

An adaptive algorithm that dynamically shifts traffic toward the better-performing variant during the test.

**When to use:**
- Short-lived campaigns (promotions, seasonal events)
- When minimizing opportunity cost matters more than statistical rigor
- When you want to exploit the winner faster

**How it works:**
1. Start with equal traffic allocation
2. Periodically update allocation based on observed performance
3. Winning variant receives progressively more traffic
4. Common algorithms: Thompson Sampling, Upper Confidence Bound (UCB), Epsilon-Greedy

**Trade-offs:**
- Reduces regret (lost conversions from showing the worse variant)
- Weaker statistical guarantees compared to fixed-allocation tests
- Harder to measure precise effect sizes
- Not suitable when you need rigorous causal inference

---

## Traffic Allocation Strategies

### Equal Split (Recommended Default)

Split traffic evenly between control and variant(s). This maximizes statistical power.

```
2 variants: 50% / 50%
3 variants: 33% / 33% / 33%
4 variants: 25% / 25% / 25% / 25%
```

### Unequal Split

Allocate more traffic to the control to reduce risk.

**When to use:**
- Testing a risky change that could significantly harm the experience
- Organizational requirement to limit exposure to untested variants
- Running holdout experiments for long-term measurement

```
Low-risk test: 50% control / 50% variant
Medium-risk test: 70% control / 30% variant
High-risk test: 90% control / 10% variant
```

**Impact on power:** A 90/10 split requires approximately 2.8x the total sample size compared to a 50/50 split to achieve the same statistical power.

### Ramp-Up Strategy

Start with a small percentage and gradually increase to full allocation.

```
Day 1-2: 5% of traffic (QA and sanity check)
Day 3-4: 25% of traffic (early signal monitoring)
Day 5+: 50% of traffic (full test)
```

**Benefits:**
- Catches implementation bugs before full exposure
- Limits blast radius of broken variants
- Allows monitoring of guardrail metrics at low risk

---

## Test Duration Calculator Methodology

### Minimum Duration Formula

```
Minimum days = Required sample size per variant / Daily traffic per variant
```

### Factors That Affect Duration

1. **Traffic volume:** More traffic = shorter tests
2. **Baseline conversion rate:** Lower rates need more data
3. **Minimum Detectable Effect:** Smaller effects need more data
4. **Number of variants:** More variants split available traffic
5. **Significance level and power:** Stricter thresholds need more data

### Additional Duration Rules

- **Minimum of 7 days:** Always run tests for at least one full business cycle (Mon-Sun) to capture day-of-week effects
- **Minimum of 2 business cycles:** 14 days is preferred to confirm weekly patterns
- **Avoid holidays and anomalies:** Exclude or extend through promotional periods, outages, or seasonal shifts
- **Maximum recommended duration:** 4-6 weeks; beyond this, cookie churn and external changes introduce bias

### Duration Estimation Table

| Daily Visitors | Baseline Rate | 5% Relative MDE | 10% Relative MDE | 20% Relative MDE |
|---------------|---------------|------------------|-------------------|-------------------|
| 1,000 | 3% | 278 days | 70 days | 18 days |
| 5,000 | 3% | 56 days | 14 days | 7 days* |
| 10,000 | 3% | 28 days | 7 days* | 7 days* |
| 50,000 | 3% | 7 days* | 7 days* | 7 days* |
| 1,000 | 10% | 75 days | 19 days | 7 days* |
| 10,000 | 10% | 8 days | 7 days* | 7 days* |

*Minimum 7-day rule applies even when sample size is reached sooner.

---

## Segmentation Approaches

### Pre-Test Segmentation (Stratification)

Define segments before the test and ensure balanced randomization within each.

**Common stratification variables:**
- Device type (mobile, desktop, tablet)
- New vs returning visitors
- Geographic region
- Traffic source (organic, paid, direct, referral)
- User plan tier (free, paid, enterprise)

**Benefits:** Reduces variance, improves power, prevents Simpson's paradox.

### Post-Test Segmentation (Subgroup Analysis)

Analyze results within segments after the test concludes.

**Guidelines:**
- Only analyze segments defined in the experiment brief
- Treat subgroup results as exploratory, not confirmatory
- Require larger effect sizes for subgroup significance
- Avoid cherry-picking favorable segments
- Document all segments analyzed, including non-significant ones

### Heterogeneous Treatment Effects

Some changes work differently for different user groups. Use interaction analysis to identify:

```
Example: A simplified checkout helps mobile users (+12%) but
slightly hurts desktop users (-2%). The overall result (+4%)
masks the true story.
```

---

## Avoiding Common Mistakes

### Changing Tests Mid-Flight

**Problem:** Modifying the variant, traffic allocation, or target audience during a running test invalidates the statistical framework.

**Solution:** If a change is necessary, stop the current test, document the reason, and launch a new test with a fresh randomization and sample.

### Too Many Variations

**Problem:** Each additional variant dilutes traffic and extends test duration. With 8 variants at 1,000 visitors/day, a test that would take 14 days with 2 variants takes 56 days.

**Solution:** Limit to 2-4 variants. Use RICE scoring to select the most promising hypotheses.

### Wrong Metrics

**Problem:** Optimizing for a proxy metric (clicks) that does not correlate with the business outcome (revenue).

**Solution:** Validate that your primary metric is causally linked to business value. Use revenue-per-visitor or similar downstream metrics when possible.

### Insufficient Test Duration

**Problem:** Stopping a test after 3 days because it reached significance ignores day-of-week effects and novelty/primacy effects.

**Solution:** Always run for at least 7 days. Use sequential testing methods if early stopping is needed.

### Sample Ratio Mismatch (SRM)

**Problem:** The observed traffic split (e.g., 48.2% / 51.8%) deviates significantly from the intended split (50/50), indicating a bug in randomization.

**Solution:** Run a chi-squared test on the sample sizes. If p < 0.001, investigate and discard the test. Common causes: bot traffic, redirect failures, caching issues.

### Interaction Effects Between Tests

**Problem:** Running multiple overlapping tests on the same users creates confounding effects.

**Solution:** Use mutual exclusion (isolate test audiences) or interaction testing. At minimum, log which tests each user is enrolled in.

---

## QA Checklist

Complete before launching any test:

### Technical QA
- [ ] Variant renders correctly on all target devices and browsers
- [ ] Variant loads within acceptable performance thresholds
- [ ] Tracking fires correctly for all events in both control and variant
- [ ] Randomization assigns users consistently across sessions
- [ ] No flickering or flash of original content (FOOC) before variant loads
- [ ] Variant works with ad blockers, VPNs, and privacy tools
- [ ] Server-side or client-side implementation matches the test design
- [ ] No JavaScript errors introduced by the variant code

### Data QA
- [ ] Primary metric baseline matches recent historical data
- [ ] Events are being captured in the analytics platform
- [ ] Sample ratio is within expected bounds after first 24 hours
- [ ] No data pipeline delays or missing data segments
- [ ] Revenue and transactional data reconcile with source systems

### Process QA
- [ ] Experiment brief is complete and approved
- [ ] Hypothesis is documented with rationale
- [ ] Sample size and duration are pre-calculated
- [ ] Stakeholders are informed of the test launch
- [ ] Escalation plan exists if guardrail metrics are breached
- [ ] Test does not overlap with conflicting experiments

---

## Results Documentation Template

Complete after every test, regardless of outcome.

```markdown
# Test Results: [Test Name]

## Summary
- **Test ID:** [ID]
- **Owner:** [Name]
- **Launch date:** [YYYY-MM-DD]
- **End date:** [YYYY-MM-DD]
- **Duration:** [X days]
- **Total sample size:** [N per variant]
- **Outcome:** [Winner / Inconclusive / Loser]

## Hypothesis
If [change], then [effect], because [rationale].

## Results

### Primary Metric: [Metric Name]
| Variant | Sample Size | Metric Value | Lift vs Control | CI (95%) | p-value |
|---------|-------------|-------------|-----------------|----------|---------|
| Control | [N] | [Value] | -- | -- | -- |
| Variant B | [N] | [Value] | [X%] | [low, high] | [p] |

### Secondary Metrics
[Table with same format]

### Guardrail Metrics
[Table confirming no degradation]

## Segmentation Analysis
[Key segment breakdowns and notable heterogeneous effects]

## Data Quality
- Sample ratio mismatch check: [Pass / Fail]
- Data completeness: [X%]
- Any anomalies observed: [Description]

## Decision
- [ ] Ship Variant B to 100%
- [ ] Do not ship; revert to control
- [ ] Inconclusive; extend or re-run with larger MDE
- [ ] Iterate: launch follow-up test based on learnings

## Learnings
[What did we learn? How does this inform future tests?]

## Follow-Up Actions
- [Action item 1]
- [Action item 2]
```

---

## Test Velocity Best Practices

- Maintain a backlog of 10+ scored and prioritized hypotheses
- Aim for 2-4 concurrent tests (on non-overlapping audiences)
- Target 2-4 test conclusions per month
- Document every result, including inconclusive tests
- Review test learnings monthly with the broader team
- Track cumulative impact of shipped experiments on key metrics

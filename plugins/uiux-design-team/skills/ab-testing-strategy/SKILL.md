---
name: ab-testing-strategy
description: Design and analyze A/B tests with hypothesis formation, variant creation, sample size calculation, statistical significance evaluation, and results analysis to make data-driven design decisions.
metadata:
   references:
   - references/analysis-methods.md
   - references/hypothesis-template.md
   - references/test-design-guide.md
---

# A/B Testing Strategy

A/B testing turns opinions into evidence. When the team debates whether a green or blue button converts better, or whether a short form outperforms a long one, an A/B test settles the question with data. This skill covers the full lifecycle of A/B testing: forming a hypothesis, designing the test, calculating sample requirements, running the experiment, and analyzing results.

A/B testing is not a substitute for user research. It answers "which option performs better?" but not "why do users struggle?" Pair A/B testing with qualitative research for a complete understanding.

## Quick Start: Design an A/B Test

Follow these five steps to go from a design question to a statistically valid answer.

**Step 1 -- Form a hypothesis.** State what you believe will happen and why. Use the format:

> "If we [change], then [metric] will [improve/decrease] because [rationale]."

Example: "If we reduce the sign-up form from 6 fields to 3 fields, then sign-up completion rate will increase by 15% because fewer fields reduce perceived effort and time commitment."

**Step 2 -- Choose your metric.** Select one primary metric that directly measures success. Add 1-2 guardrail metrics to ensure you are not causing harm elsewhere.

**Step 3 -- Create the variant.** Design the alternative experience. Change only one variable at a time. If you change the button color and the headline simultaneously, you cannot attribute results to either change.

**Step 4 -- Calculate sample size.** Determine how many users you need and how long the test must run to reach statistical significance. Use the formulas in the Sample Size section below.

**Step 5 -- Run and analyze.** Launch the test, wait for the full duration (do not peek), then analyze results using confidence intervals and practical significance.

## Hypothesis Formation

Every A/B test begins with a clear hypothesis. A hypothesis without rationale is just a guess.

**The hypothesis format:**

> "If we [specific change to the interface], then [specific measurable metric] will [increase/decrease by estimated amount] because [evidence-based rationale]."

**Three well-formed examples:**

1. "If we add social proof (customer count) above the pricing table, then the free-to-paid conversion rate will increase by 8% because social proof reduces uncertainty during purchase decisions."

2. "If we replace the hamburger menu with a visible bottom navigation bar on mobile, then task completion rate will increase by 12% because persistent navigation reduces the number of taps required to switch sections."

3. "If we add inline field validation to the checkout form, then form abandonment rate will decrease by 20% because users can correct errors immediately instead of encountering them all at submission."

**Requirements for a good hypothesis:**
- **Specific:** Names exactly what changes and what metric to measure
- **Measurable:** The outcome can be tracked with existing analytics
- **Grounded:** The "because" cites user research, heuristics, or industry data
- **Falsifiable:** It is possible for the test to prove the hypothesis wrong

## Key Metrics

Select metrics carefully. The wrong metric can lead you to optimize for something that does not matter.

**Primary metrics** -- The single metric that defines whether the test succeeds or fails:
- Conversion rate (sign-ups, purchases, upgrades)
- Task completion rate
- Engagement rate (clicks, time on task, feature adoption)
- Revenue per user

**Guardrail metrics** -- Metrics that must not degrade, even if the primary metric improves:
- Page load time (performance)
- Error rate (reliability)
- Bounce rate (engagement)
- Support ticket volume (user satisfaction)
- Downstream retention (long-term impact)

**Counter metrics** -- Metrics that might get worse as a side effect of the change. Monitor them actively:
- If you simplify a form, counter metric might be data quality or lead qualification rate
- If you add friction (e.g., a confirmation step), counter metric might be completion speed

Define all three metric types before launching the test. If the primary metric improves but a guardrail metric degrades, the test result is ambiguous and needs further investigation.

## Sample Size and Duration

Running a test without sufficient sample size is worse than not running a test at all. Underpowered tests produce false positives and false negatives that lead to bad decisions.

**Key variables:**
- **Baseline conversion rate** -- Your current metric value (e.g., 5% sign-up rate)
- **Minimum detectable effect (MDE)** -- The smallest improvement worth detecting (e.g., a 10% relative lift from 5% to 5.5%)
- **Statistical significance level (alpha)** -- Probability of a false positive, typically 0.05 (5%)
- **Statistical power (1 - beta)** -- Probability of detecting a real effect, typically 0.80 (80%)

**Simplified sample size estimation:**

For a two-sided test with alpha = 0.05 and power = 0.80:

```
n per variant = 16 * p * (1 - p) / (MDE)^2

Where:
  p   = baseline conversion rate (as a decimal)
  MDE = minimum detectable effect (as an absolute change)
```

Example: Baseline = 5% (0.05), you want to detect a lift to 6% (MDE = 0.01):
```
n = 16 * 0.05 * 0.95 / (0.01)^2
n = 16 * 0.0475 / 0.0001
n = 7,600 per variant
n = 15,200 total
```

**Duration:** Divide total sample by daily traffic to determine how many days the test needs to run. Always run tests for at least one full business cycle (typically 1-2 weeks) to account for day-of-week effects, even if you reach the sample size earlier.

## Statistical Significance

Statistical significance tells you whether the observed difference is likely real or could be due to random chance.

**p-value** -- The probability of observing a result as extreme as yours if there were truly no difference between variants. Convention: p < 0.05 means statistically significant.

**Confidence interval** -- The range within which the true effect likely falls. A 95% confidence interval that does not cross zero indicates statistical significance.

**Why you must NOT peek at results early:**
- Checking results multiple times during a test inflates the false positive rate. If you check 10 times at p < 0.05, your actual false positive rate approaches 40%.
- Decide the sample size and duration before the test starts. Analyze only when complete.
- If you must monitor results during the test, use **sequential testing** methods (e.g., Bayesian approaches or group sequential designs) that account for multiple looks.

## Common Pitfalls

- **Testing too many things at once.** If you change the headline, button color, and layout simultaneously, you cannot determine which change caused the result. Test one variable at a time. If you need to test combinations, use multivariate testing with appropriate sample sizes.
- **Stopping too early.** A test that looks like a winner after 100 visitors may reverse after 1,000. Commit to the predetermined sample size.
- **Ignoring segments.** An overall neutral result may hide a strong positive effect for mobile users and a strong negative effect for desktop users. Always check segment-level results.
- **Novelty effect.** Users may interact more with a variant simply because it is new. Run the test long enough for novelty to wear off (at least 2 weeks).
- **Not having a clear hypothesis.** Testing without a hypothesis is fishing for results. You will find "significant" differences by chance alone.
- **Survivorship bias.** Only measuring users who complete a flow ignores users who dropped off. Measure from the point of exposure, not the point of completion.

## Deep Dive References

### [Hypothesis Template](references/hypothesis-template.md)

- Hypothesis Framework
- 10 Detailed Examples
- Variable Identification
- Test Variables
- Success Metrics and Kill Criteria
- Outcome Documentation
- Hypothesis
- Results
- *...and 3 more sections*

### [Test Design Guide](references/test-design-guide.md)

- Overview
- Test Types
- Traffic Allocation Strategies
- Test Duration Calculator Methodology
- Segmentation Approaches
- Avoiding Common Mistakes
- QA Checklist
- Results Documentation Template
- *...and 9 more sections*

### [Analysis Methods](references/analysis-methods.md)

- Overview
- Frequentist vs Bayesian Approaches
- Sample Size Calculation
- Statistical Significance
- Effect Size
- Multiple Comparison Correction
- Sequential Testing
- Practical Significance vs Statistical Significance
- *...and 2 more sections*

## Next Steps

After completing A/B testing, continue with these related skills:

- **usability-evaluation** -- When a variant wins, conduct heuristic evaluation to understand which usability principles explain the improvement.
- **user-research** -- When test results are surprising, conduct qualitative research (interviews, usability tests) to understand the "why" behind the numbers.

[Back to AB Testing Strategy](../ab-testing-strategy.md)

# Statistical Analysis Methods for A/B Tests

## Overview

Choosing the right statistical analysis method determines whether your A/B test conclusions are trustworthy. This reference covers the two dominant paradigms, key metrics, correction methods, and common pitfalls that undermine test validity.

---

## Frequentist vs Bayesian Approaches

### Frequentist (Classical) Approach

The frequentist framework treats probability as the long-run frequency of events. You define a null hypothesis (no difference between variants), collect data, and calculate the probability of observing your results if the null hypothesis were true.

**Key characteristics:**
- Fixed sample size determined before the test
- Binary outcome: reject or fail to reject the null hypothesis
- Results expressed as p-values and confidence intervals
- Does not assign probability to hypotheses themselves

**When to use:**
- Regulatory or compliance environments requiring established methodology
- Simple A/B tests with one primary metric
- When stakeholders are familiar with p-values

```
Example interpretation:
"We observed a 4.2% lift in conversion rate (p = 0.03, 95% CI: [1.1%, 7.3%]).
We reject the null hypothesis at the 0.05 significance level."
```

### Bayesian Approach

The Bayesian framework incorporates prior beliefs and updates them with observed data to produce a posterior distribution of the treatment effect.

**Key characteristics:**
- Prior distribution encodes existing knowledge
- Posterior distribution updates as data arrives
- Results expressed as probability of one variant beating another
- Naturally supports sequential testing and early stopping

**When to use:**
- When you want to monitor results continuously
- When "probability of being best" is more intuitive for stakeholders
- When incorporating prior knowledge from previous tests
- When you need flexible stopping rules

```
Example interpretation:
"There is a 96.4% probability that Variant B outperforms the Control.
The expected lift is 3.8% with a 95% credible interval of [0.9%, 6.7%]."
```

### Comparison Summary

| Aspect | Frequentist | Bayesian |
|--------|-------------|----------|
| Stopping rule | Fixed sample size | Flexible / continuous |
| Output | p-value, CI | Posterior probability |
| Prior knowledge | Not incorporated | Explicitly modeled |
| Interpretation | "How surprising is this data?" | "How likely is the hypothesis?" |
| Computational cost | Lower | Higher |
| Peeking problem | Severe if uncontrolled | Naturally handled |

---

## Sample Size Calculation

Calculating the required sample size before launching a test prevents underpowered experiments and wasted traffic.

### Required Inputs

1. **Baseline conversion rate (p):** Your current metric value
2. **Minimum Detectable Effect (MDE):** The smallest effect worth detecting
3. **Significance level (alpha):** Typically 0.05 (5% false positive rate)
4. **Statistical power (1 - beta):** Typically 0.80 (80% chance of detecting a real effect)

### Formula (Two-Proportion Z-Test)

```
n = (Z_alpha/2 + Z_beta)^2 * (p1(1-p1) + p2(1-p2)) / (p1 - p2)^2

Where:
  Z_alpha/2 = 1.96 (for alpha = 0.05, two-tailed)
  Z_beta    = 0.84 (for power = 0.80)
  p1        = baseline conversion rate
  p2        = p1 + minimum detectable effect
  n         = sample size per variant
```

### Practical Guidelines

- **Lower baseline rates** require larger samples to detect the same relative lift
- **Smaller MDE** dramatically increases required sample size (quadratic relationship)
- Always calculate for the **primary metric** before launching
- Account for variant count: more variants require more total traffic
- Typical web tests: 1,000 to 100,000+ visitors per variant

---

## Statistical Significance

### P-Values

The p-value is the probability of observing a result at least as extreme as the one measured, assuming the null hypothesis is true.

**Interpreting p-values correctly:**
- p < 0.05 does NOT mean there is a 95% chance the variant is better
- p < 0.05 means: if there were truly no difference, you would see data this extreme less than 5% of the time
- A p-value is NOT the probability that the null hypothesis is true
- Smaller p-values indicate stronger evidence against the null hypothesis

### Confidence Intervals

A 95% confidence interval means: if you repeated the experiment many times, 95% of the computed intervals would contain the true parameter value.

**Why confidence intervals matter more than p-values:**
- They show the range of plausible effect sizes
- They communicate uncertainty about the magnitude of the effect
- A statistically significant result with a tiny CI may not be practically significant

```
Good reporting:
"Conversion rate increased by 3.2% (95% CI: [1.4%, 5.0%], p = 0.001)"

This tells you:
- The point estimate (3.2% lift)
- The plausible range (1.4% to 5.0%)
- The statistical significance (p = 0.001)
```

---

## Effect Size

### Cohen's d

Cohen's d measures the standardized difference between two means, independent of sample size.

```
d = (Mean_B - Mean_A) / Pooled_Standard_Deviation
```

**Benchmarks (Cohen's conventions):**
| d Value | Interpretation |
|---------|----------------|
| 0.2 | Small effect |
| 0.5 | Medium effect |
| 0.8 | Large effect |

**Why report effect size:**
- Large samples can make trivial differences statistically significant
- Effect size tells you whether the difference matters in practice
- Enables comparison across different experiments
- Essential for meta-analysis of multiple tests

### Relative vs Absolute Effect

Always report both:
- **Absolute:** "Conversion rate increased from 3.0% to 3.3%" (0.3 percentage point increase)
- **Relative:** "Conversion rate increased by 10%" (relative to baseline)

Relative effects can be misleading when the baseline is small.

---

## Multiple Comparison Correction

When testing multiple metrics or variants simultaneously, the probability of at least one false positive increases.

### The Problem

With alpha = 0.05 and 20 independent metrics:
```
P(at least one false positive) = 1 - (1 - 0.05)^20 = 64.2%
```

### Bonferroni Correction

The simplest and most conservative correction. Divide the significance level by the number of comparisons.

```
Adjusted alpha = alpha / number_of_comparisons

Example: Testing 5 metrics at alpha = 0.05
Adjusted alpha = 0.05 / 5 = 0.01
Each metric must reach p < 0.01 to be significant
```

**Limitations:** Overly conservative with many comparisons, increasing false negatives.

### Alternative Methods

- **Holm-Bonferroni:** Step-down procedure, less conservative than Bonferroni
- **Benjamini-Hochberg (FDR):** Controls the false discovery rate instead of family-wise error rate; more powerful for exploratory analysis
- **Pre-registration:** Declare primary metric upfront; secondary metrics are exploratory

### Practical Recommendation

1. Designate ONE primary metric for the statistical decision
2. List secondary metrics as exploratory (no correction needed if labeled as such)
3. Define guardrail metrics that must not degrade significantly
4. Apply Bonferroni or Holm-Bonferroni only when multiple metrics are all decision-critical

---

## Sequential Testing

Sequential testing allows you to analyze results as data accumulates without inflating false positive rates.

### Group Sequential Methods

- Pre-define a fixed number of interim analyses (looks)
- Use adjusted significance boundaries at each look (e.g., O'Brien-Fleming, Pocock)
- O'Brien-Fleming: conservative early, liberal late (preferred in practice)
- Pocock: equal boundaries at each look

### Always Valid Inference (Confidence Sequences)

A modern approach that allows continuous monitoring:
- Produces confidence intervals valid at any stopping time
- Wider than fixed-sample CIs (the cost of flexibility)
- Well-suited for tech companies with continuous deployment

---

## Practical Significance vs Statistical Significance

A result can be statistically significant but practically meaningless. Always evaluate both.

**Framework for decision-making:**

| Statistical Sig? | Practical Sig? | Action |
|-------------------|----------------|--------|
| Yes | Yes | Ship the winning variant |
| Yes | No | Do not ship; effect is real but too small to matter |
| No | Uncertain | Increase sample size or accept as inconclusive |
| No | No | Revert to control; test a bolder hypothesis next |

**Define practical significance before the test:**
- "We need at least a 2% relative lift to justify the engineering cost"
- "Revenue per user must increase by at least $0.50"

---

## Common Pitfalls

### Peeking (Repeated Significance Testing)

Checking results daily and stopping when p < 0.05 inflates the false positive rate far beyond 5%. Over a typical 30-day test with daily checks, the actual false positive rate can exceed 30%.

**Mitigation:** Use sequential testing methods or commit to a fixed sample size.

### Simpson's Paradox

A trend that appears in aggregated data reverses when the data is segmented. This occurs when the mix of segments differs between variants.

```
Example:
- Desktop users: Control 5.0%, Variant 5.2% (Variant wins)
- Mobile users: Control 3.0%, Variant 3.1% (Variant wins)
- Overall: Control 4.2%, Variant 4.0% (Control wins!)

This happens when Variant received disproportionately more mobile traffic.
```

**Mitigation:** Verify randomization balance across key segments. Use stratified randomization.

### Other Common Mistakes

- **Underpowered tests:** Running tests without sufficient sample size leads to inconclusive results or false negatives
- **Testing too many variants:** Each additional variant increases required traffic linearly
- **Ignoring novelty/primacy effects:** New designs may perform differently short-term vs long-term
- **Survivorship bias:** Analyzing only users who completed the funnel instead of all who entered
- **Contamination between variants:** Users seeing both variants (cross-device, shared accounts)
- **Wrong randomization unit:** Randomizing at pageview level when the metric is per-user

---

## Recommended Analysis Workflow

1. Verify randomization (check covariate balance between groups)
2. Compute the primary metric difference and confidence interval
3. Check statistical significance against pre-registered alpha
4. Compute effect size (Cohen's d or relative lift)
5. Evaluate practical significance against the pre-defined threshold
6. Inspect secondary and guardrail metrics (apply correction if needed)
7. Segment analysis for heterogeneous treatment effects
8. Document results, limitations, and next steps

## Statistical Significance (Detailed)

**p-value** — the probability of observing a result as extreme as the one obtained if there were truly no difference. Convention: p < 0.05 means statistically significant.

**Confidence interval** — the range within which the true effect likely falls. A 95% CI that does not cross zero indicates significance.

**Why you must not peek at results early:**
- Checking results multiple times during a test inflates the false-positive rate. Checking 10 times at α=0.05 pushes the actual false-positive rate near 40%.
- Decide sample size and duration before launch. Analyze only when complete.
- If interim monitoring is required, use sequential testing methods (Bayesian or group sequential designs) that account for multiple looks.

## Common Pitfalls

- **Testing too many things at once** — if you change headline, button color, and layout simultaneously, you can't attribute the result. Run multivariate (MVT) with the appropriate larger sample if combinations are needed.
- **Stopping too early** — a 100-visitor "winner" routinely reverses by 1,000. Commit to the planned n.
- **Ignoring segments** — neutral overall can hide +mobile / −desktop. Always segment-check.
- **Novelty effect** — users interact more with new things. Run ≥ 2 weeks for novelty to wear off.
- **No clear hypothesis** — fishing finds spurious "significance" by chance.
- **Survivorship bias** — measure from exposure, not from completion.

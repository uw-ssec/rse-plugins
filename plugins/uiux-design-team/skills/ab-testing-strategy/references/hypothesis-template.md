# Hypothesis Template

A framework for writing well-structured A/B test hypotheses, with 10 detailed examples across different product types, a variable identification guide, success metric selection, and outcome documentation templates.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [Hypothesis Framework](#hypothesis-framework) | 14-45 | The template structure and requirements for a good hypothesis |
| [10 Detailed Examples](#10-detailed-examples) | 47-135 | Hypotheses for e-commerce, SaaS, content, mobile, and B2B products |
| [Variable Identification](#variable-identification) | 137-175 | Independent, dependent, and confounding variables in test design |
| [Success Metrics and Kill Criteria](#success-metrics-and-kill-criteria) | 177-215 | Defining win conditions and when to stop a test early |
| [Outcome Documentation](#outcome-documentation) | 217-245 | Recording and sharing test results regardless of outcome |
| [See Also](#see-also) | 247-255 | Related references and skills |

## Hypothesis Framework

### The Template

Every A/B test hypothesis should follow this structure:

```
If we [specific change to the interface],
then [specific measurable metric] will [direction] by [estimated amount]
because [evidence-based rationale].
```

### Requirements for Each Component

**"If we [change]"** -- Must be specific and implementable. Not "improve the checkout" but "reduce the checkout form from 6 fields to 3 by removing company name, phone, and fax."

**"Then [metric] will [direction]"** -- Must name one primary metric that can be measured with existing analytics. Not "the experience will be better" but "checkout completion rate will increase."

**"By [amount]"** -- Include a specific estimated effect size. This forces you to think about whether the change is large enough to produce a measurable effect and feeds directly into sample size calculations. Not "will increase" but "will increase by 10-15%."

**"Because [rationale]"** -- Ground the hypothesis in evidence. Cite user research findings, support ticket data, competitive analysis, heuristic evaluation results, or industry benchmarks. Not "because it seems better" but "because our user interviews revealed that 60% of users described the current form as 'too long' and 3 of 8 participants abandoned at the phone number field."

### What Makes a Bad Hypothesis

| Problem | Example | Fix |
|---------|---------|-----|
| Vague change | "If we improve the page" | Specify exactly what changes |
| Unmeasurable outcome | "Users will be happier" | Name a trackable metric |
| No estimated effect | "Conversion will increase" | Estimate a percentage |
| No rationale | "Because it looks better" | Cite evidence |
| Multiple changes | "If we change the color AND layout AND copy" | Test one variable at a time |

## 10 Detailed Examples

### Example 1: E-Commerce -- Form Reduction

```
If we reduce the checkout form from 6 fields to 3 fields
  (removing company name, phone number, and fax number),
then checkout completion rate will increase by 12-18%
because our analytics show 34% drop-off at the form step,
  and usability testing revealed that 5 of 8 participants
  questioned why personal purchase required company information.
```

**Primary metric:** Checkout completion rate
**Guardrail metrics:** Order value, return rate, support ticket volume
**Kill criteria:** If completion rate drops by more than 5% after 3 days

### Example 2: SaaS -- Onboarding Simplification

```
If we replace the 7-step onboarding wizard with a single-page
  setup that pre-selects defaults based on the user's role selection,
then the percentage of users reaching "first value" within 24 hours
  will increase by 20-25%
because our journey map shows a 45% drop-off between steps 3 and 5,
  and interview participants described the wizard as "tedious" and
  "asking questions I don't know the answers to yet."
```

**Primary metric:** First-value activation within 24 hours
**Guardrail metrics:** 7-day retention, feature adoption breadth, support tickets

### Example 3: E-Commerce -- Social Proof

```
If we add a "X people are viewing this item" indicator
  and "Y sold in the last 24 hours" counter to product pages,
then add-to-cart rate will increase by 8-12%
because social proof research (Cialdini) shows that scarcity
  and popularity signals increase purchase intent,
  and competitor analysis shows 4 of 5 top competitors
  use similar indicators.
```

**Primary metric:** Add-to-cart rate
**Guardrail metrics:** Return rate, customer satisfaction (CSAT)

### Example 4: Content -- Article Layout

```
If we move the article table of contents from a collapsible sidebar
  to a persistent sticky left rail visible on scroll,
then average scroll depth will increase by 15-20%
  and time on page will increase by 10-15%
because our session recordings show that 70% of users never open
  the collapsible TOC, and eye-tracking studies indicate that
  persistent navigation aids increase content engagement.
```

**Primary metric:** Average scroll depth
**Guardrail metrics:** Bounce rate, next-article click-through

### Example 5: Mobile App -- Bottom Navigation

```
If we replace the hamburger menu with a visible bottom
  navigation bar showing the 5 core sections,
then daily active feature breadth (number of distinct sections
  visited per session) will increase by 25-30%
because mobile usability research (NNGroup) shows that hidden
  navigation reduces discoverability by 50%,
  and our analytics show 78% of sessions never open the hamburger menu.
```

**Primary metric:** Feature breadth (sections visited per session)
**Guardrail metrics:** Task completion time, error rate

### Example 6: B2B -- Pricing Page

```
If we restructure the pricing page from a feature comparison matrix
  to a role-based recommendation ("Best for teams of 1-10" /
  "Best for teams of 10-50" / "Best for enterprise"),
then pricing page to trial conversion will increase by 10-15%
because our sales call transcripts reveal that 65% of prospects
  ask "which plan is right for my team size?" and the current
  matrix requires comparing 40+ feature rows.
```

**Primary metric:** Pricing page to trial conversion rate
**Guardrail metrics:** Plan distribution, upgrade rate within 30 days

### Example 7: SaaS -- Empty States

```
If we replace the blank empty states in the dashboard with
  contextual templates and guided first actions,
then the percentage of new users who create their first item
  within the first session will increase by 30-40%
because cognitive walkthrough analysis identified 3 severity-3
  issues at empty states where users did not know what action
  to take, and 4 of 6 interviewed churned users cited
  "didn't know where to start" as their primary reason for leaving.
```

**Primary metric:** First-item creation rate within first session
**Guardrail metrics:** Item quality score, 14-day retention

### Example 8: E-Commerce -- Shipping Transparency

```
If we display estimated shipping cost on the product page
  (before the user adds to cart),
then cart abandonment rate will decrease by 15-20%
because our funnel analysis shows that 28% of cart abandonment
  occurs immediately after shipping costs are revealed at checkout,
  and Baymard Institute research identifies unexpected costs as
  the number one reason for cart abandonment (48% of users).
```

**Primary metric:** Cart abandonment rate
**Guardrail metrics:** Add-to-cart rate, average order value

### Example 9: Content -- CTA Placement

```
If we add an inline email signup form after the third paragraph
  of blog posts (in addition to the existing end-of-article form),
then email signup conversion rate from blog traffic will
  increase by 40-60%
because our scroll depth data shows that only 35% of visitors
  reach the end-of-article CTA, and the average reading depth
  is 45% of article length, which corresponds to roughly
  paragraph 3-4 for our typical article length.
```

**Primary metric:** Email signup conversion rate from blog traffic
**Guardrail metrics:** Bounce rate, average time on page, scroll depth

### Example 10: Mobile -- Biometric Login

```
If we offer Face ID / Touch ID as the default login method
  (with password fallback accessible via "Use password instead"),
then login success rate will increase by 8-12%
  and average login time will decrease by 60-70%
because our error logs show that 23% of login attempts fail
  due to incorrect passwords, and industry data from Apple shows
  that biometric authentication has a 95%+ success rate
  versus 75% for password entry on mobile keyboards.
```

**Primary metric:** Login success rate
**Guardrail metrics:** Security incident rate, password reset requests

## Variable Identification

### Independent Variable (What You Change)

The independent variable is the single thing you manipulate between the control and variant. Identify it precisely.

**Good:** "The number of form fields (6 in control, 3 in variant)"
**Bad:** "The checkout experience" (too vague, could encompass many changes)

### Dependent Variable (What You Measure)

The dependent variable is the metric you expect to change as a result of your manipulation. It must be:
- Measurable with existing instrumentation
- Sensitive enough to detect the expected effect size
- Recorded at the user level (not page level) for proper statistical analysis

### Confounding Variables (What Could Corrupt Results)

Confounding variables are factors other than your independent variable that could affect the dependent variable. Identify and control for them.

| Confounding Variable | Risk | Mitigation |
|---------------------|------|------------|
| Day-of-week effects | Traffic patterns differ on weekdays vs weekends | Run test for at least 1 full week |
| Seasonal effects | Holiday shopping, end of quarter | Avoid launching tests during known anomalies |
| Marketing campaigns | Email blast drives different traffic quality | Coordinate with marketing on test schedule |
| Technical issues | One variant loads slower due to unoptimized code | Performance-test both variants before launch |
| Novelty effect | Users interact more with the new variant because it is new | Run test for at least 2 weeks |

### Documenting Variables

```markdown
## Test Variables

**Independent variable:** [What is being changed]
- Control: [Description of current state]
- Variant: [Description of changed state]

**Dependent variable (primary):** [Metric name and how it is measured]
**Dependent variables (guardrail):** [List of guardrail metrics]

**Confounding variables identified:**
1. [Variable] -- Mitigated by [strategy]
2. [Variable] -- Mitigated by [strategy]
```

## Success Metrics and Kill Criteria

### Defining Win Conditions

Before launching any test, define exactly what constitutes a win:

**Minimum detectable effect (MDE):** The smallest improvement that would be worth implementing. If a 2% lift is not worth the engineering effort to ship, your MDE should be higher.

**Practical significance threshold:** The effect size below which the result, even if statistically significant, is not worth acting on. A statistically significant 0.1% lift on a metric may not justify the complexity of maintaining the variant.

**Decision framework:**

| Outcome | Statistical Significance | Practical Significance | Action |
|---------|------------------------|----------------------|--------|
| Clear win | p < 0.05 | Above MDE | Ship the variant |
| Marginal win | p < 0.05 | Below MDE | Do not ship -- effect too small |
| No difference | p >= 0.05 | N/A | Keep the control, learn from the data |
| Clear loss | p < 0.05 | Above MDE (negative) | Keep the control, investigate why |
| Guardrail breach | Any | Any | Stop the test, investigate |

### Kill Criteria

Define conditions that trigger an immediate test stop:

- **Revenue drop:** If revenue per user in the variant drops below [X]% of control for [Y] consecutive days
- **Error rate spike:** If error rates in the variant exceed [X]% above baseline
- **Severe UX degradation:** If task completion rate drops below [X]%
- **Technical failure:** If variant page load time exceeds [X]ms

Document kill criteria before the test starts. Assign a specific person responsible for monitoring.

## Outcome Documentation

### Test Results Template

Regardless of whether the test wins, loses, or shows no difference, document the results:

```markdown
# Test Results: [Test Name]

**Dates:** [Start] to [End]
**Duration:** [X] days
**Sample size:** [Control: n] [Variant: n]

## Hypothesis
[Copy from test plan]

## Results

| Metric | Control | Variant | Lift | p-value | Significant? |
|--------|---------|---------|------|---------|-------------|
| [Primary] | [value] | [value] | [%] | [value] | Yes/No |
| [Guardrail 1] | [value] | [value] | [%] | [value] | Yes/No |
| [Guardrail 2] | [value] | [value] | [%] | [value] | Yes/No |

## Decision
[Ship / Do not ship / Iterate]

## Learnings
1. [What we learned about our users]
2. [What we learned about our product]
3. [What we would do differently next time]

## Follow-Up Actions
- [ ] [Action item with owner]
- [ ] [Action item with owner]
```

### Sharing Results

- Share all test results, including failures. Failed tests contain the most learning.
- Present results to the broader team within one week of test completion.
- Add results to a central test repository so future teams can reference past experiments.
- Connect results to the original user research that motivated the hypothesis.

## See Also

- [[test-design-guide.md]] -- Design the test architecture after forming your hypothesis
- [[analysis-methods.md]] -- Analyze results using statistical methods once the test completes
- [[../../user-research/references/interview-guide.md]] -- Conduct the research that provides hypothesis rationale
- [[../../usability-evaluation/references/nielsen-heuristics.md]] -- Use heuristic violations to generate hypothesis ideas
- [[../../user-journey-mapping/references/journey-template.md]] -- Identify journey pain points that become test hypotheses

**Back to:** [A/B Testing Strategy Skill](../SKILL.md)

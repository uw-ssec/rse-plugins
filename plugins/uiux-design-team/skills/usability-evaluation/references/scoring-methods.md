[Back to Usability Evaluation](../usability-evaluation.md)

# Usability Scoring Methods

## Overview

Quantitative usability metrics transform subjective user experience into comparable, trackable numbers. This reference covers the most widely used standardized questionnaires, task-level metrics, and interpretation guidelines. Each method includes its scoring methodology, when to use it, and how to benchmark results.

---

## System Usability Scale (SUS)

### What It Is

The SUS is a 10-item questionnaire that provides a quick, reliable measure of perceived usability. Created by John Brooke in 1986, it is the most widely used standardized usability questionnaire in the world.

### The 10 Questions

Each item is rated on a 5-point Likert scale (1 = Strongly Disagree, 5 = Strongly Agree):

1. I think that I would like to use this system frequently.
2. I found the system unnecessarily complex.
3. I thought the system was easy to use.
4. I think that I would need the support of a technical person to use this system.
5. I found the various functions in this system were well integrated.
6. I thought there was too much inconsistency in this system.
7. I would imagine that most people would learn to use this system very quickly.
8. I found the system very cumbersome to use.
9. I felt very confident using the system.
10. I needed to learn a lot of things before I could get going with this system.

### Scoring Methodology

1. For odd-numbered items (1, 3, 5, 7, 9): subtract 1 from the score
2. For even-numbered items (2, 4, 6, 8, 10): subtract the score from 5
3. Sum all 10 adjusted scores
4. Multiply the sum by 2.5 to get the SUS score (0-100 scale)

```
Example calculation:
Raw scores: 4, 2, 5, 1, 4, 2, 5, 1, 4, 2

Odd items: (4-1) + (5-1) + (4-1) + (5-1) + (4-1) = 3+4+3+4+3 = 17
Even items: (5-2) + (5-1) + (5-2) + (5-1) + (5-2) = 3+4+3+4+3 = 17
Sum: 17 + 17 = 34
SUS Score: 34 * 2.5 = 85
```

### Interpretation

| SUS Score | Grade | Adjective Rating | Percentile |
|-----------|-------|-------------------|------------|
| 90-100 | A+ | Best Imaginable | 96-100% |
| 80-89 | A | Excellent | 85-96% |
| 70-79 | B | Good | 65-85% |
| 60-69 | C | OK / Fair | 41-65% |
| 50-59 | D | Poor | 15-41% |
| 0-49 | F | Awful | 0-15% |

**Key benchmarks:**
- Average SUS score across 500+ studies: **68**
- A score of 68 is the 50th percentile (median)
- Scores above 80 indicate strong usability
- Scores below 50 indicate serious usability issues

### When to Use

- After usability testing sessions to get an overall impression
- To track usability over time across product versions
- To compare usability across competing products
- As a complement to task-level metrics

### Sample Size

- Minimum: 8-12 participants for a reliable mean estimate
- For comparison between two designs: 20+ per group

---

## Single Ease Question (SEQ)

### What It Is

A single question asked immediately after a user completes (or attempts) a task: "Overall, how easy or difficult was this task?"

### Scale

7-point scale from 1 (Very Difficult) to 7 (Very Easy).

### Scoring

Simply average the responses across all participants for each task.

### Interpretation

| Mean SEQ | Interpretation |
|----------|----------------|
| 5.5+ | Easy; task design is effective |
| 4.5-5.4 | Moderate; some room for improvement |
| Below 4.5 | Difficult; task needs redesign |

**Key benchmark:**
- Average SEQ across published studies: **5.5**
- The 25th percentile is approximately 4.8

### When to Use

- After every task in a usability test
- When you need per-task difficulty assessment with minimal participant burden
- To identify which specific tasks are most problematic
- To correlate with task completion rate and time on task

### Advantages

- Extremely low participant burden (one question)
- Captures immediate, task-specific perception
- Highly correlated with other usability measures
- Easy to administer and analyze

---

## NASA Task Load Index (NASA-TLX)

### What It Is

A multi-dimensional assessment tool that measures perceived workload across six subscales. Originally developed for aerospace applications, it is widely used in UX when cognitive load is a concern.

### The Six Subscales

Each rated on a 21-point scale (0-100 in increments of 5):

1. **Mental Demand:** How mentally demanding was the task?
2. **Physical Demand:** How physically demanding was the task?
3. **Temporal Demand:** How hurried or rushed was the pace?
4. **Performance:** How successful were you in accomplishing the task? (inverted)
5. **Effort:** How hard did you have to work to achieve your level of performance?
6. **Frustration:** How insecure, discouraged, irritated, stressed, and annoyed were you?

### Scoring Methodology

**Raw TLX (simplified, commonly used):**
Average the six subscale scores. Range: 0-100.

**Weighted TLX (original method):**
1. Participants complete 15 pairwise comparisons of the subscales
2. Each comparison: "Which contributed more to workload: Mental Demand or Effort?"
3. Count how many times each subscale was selected (0-5, total = 15)
4. Multiply each subscale score by its weight
5. Sum and divide by 15

### Interpretation

| Raw TLX Score | Workload Level |
|---------------|---------------|
| 0-20 | Very low workload |
| 21-40 | Low workload |
| 41-60 | Moderate workload |
| 61-80 | High workload |
| 81-100 | Very high workload |

### When to Use

- Evaluating tasks with significant cognitive complexity
- Comparing workload between alternative interface designs
- Assessing data entry, configuration, or analytical workflows
- When time pressure is a factor in the task design

---

## SUPR-Q (Standardized User Experience Percentile Rank Questionnaire)

### What It Is

An 8-item questionnaire designed specifically for measuring website usability and user experience. It provides scores across four dimensions.

### The Four Dimensions

1. **Usability** (based on SUS items): General ease of use
2. **Trust/Credibility:** Confidence in the site and its content
3. **Loyalty:** Likelihood of returning and recommending
4. **Appearance:** Visual appeal and design quality

### Scoring

- Each item rated on a 5-point Likert scale
- Scores are converted to percentile ranks based on a large normative database
- Overall SUPR-Q score is the average of all item scores

### Interpretation

| Percentile | Interpretation |
|------------|----------------|
| 75th+ | Top quartile; strong user experience |
| 50th-74th | Above average |
| 25th-49th | Below average; improvement needed |
| Below 25th | Bottom quartile; significant issues |

### When to Use

- Benchmarking a website against industry peers
- Tracking website UX over time
- Comparing redesign before/after
- When you need a comprehensive website-specific measure beyond usability alone

---

## Net Promoter Score (NPS)

### What It Is

A single-question measure of customer loyalty and satisfaction: "How likely are you to recommend [product/service] to a friend or colleague?"

### Scale

0-10 scale where 0 = Not at all likely and 10 = Extremely likely.

### Scoring

Participants are classified into three groups:
- **Promoters (9-10):** Loyal enthusiasts who will recommend
- **Passives (7-8):** Satisfied but not enthusiastic; vulnerable to competition
- **Detractors (0-6):** Unhappy customers who may damage the brand

```
NPS = % Promoters - % Detractors

Example:
50 responses: 20 Promoters, 15 Passives, 15 Detractors
NPS = (20/50 * 100) - (15/50 * 100) = 40% - 30% = +10
```

### Interpretation

| NPS Score | Interpretation |
|-----------|----------------|
| 70+ | World class (rare) |
| 50-69 | Excellent |
| 30-49 | Good |
| 0-29 | Needs improvement |
| Below 0 | Critical; more detractors than promoters |

**Industry benchmarks vary significantly:**
- SaaS average: 30-40
- E-commerce average: 40-50
- Financial services average: 20-30

### Limitations

- Single question captures sentiment but not actionable specifics
- The 0-6 detractor range is asymmetric and debated
- Cultural differences affect scoring tendencies
- Always follow up with an open-ended "Why did you give that score?"

### When to Use

- Tracking overall satisfaction across time
- Comparing against industry benchmarks
- As a lagging indicator of product health
- Always combine with qualitative feedback for actionability

---

## Task-Level Performance Metrics

### Task Completion Rate (Effectiveness)

The most fundamental usability metric: did the user successfully complete the task?

**Calculation:**
```
Completion rate = (Number of successful completions / Total attempts) * 100
```

**Scoring variants:**
- **Binary:** Success (1) or Failure (0)
- **Partial credit:** Full success (1), Partial success with help (0.5), Failure (0)

**Benchmarks:**
- Average across published studies: **78%**
- Tasks below 60% completion need urgent redesign
- Target: 90%+ for critical flows (checkout, sign-up)

### Time on Task (Efficiency)

How long it takes users to complete a task, measured from first action to successful completion.

**Analysis approach:**
- Report **median** time, not mean (task times are typically right-skewed)
- Remove outliers (>3 standard deviations or incomplete tasks)
- Compare against a benchmark or expert completion time

**Interpretation:**
```
Efficiency ratio = Expert time / Observed median time

Ratio > 0.7: Efficient design
Ratio 0.4-0.7: Moderate inefficiency; look for bottlenecks
Ratio < 0.4: Significant inefficiency; redesign the flow
```

### Error Rate

The frequency and nature of errors committed during task completion.

**Types of errors to track:**
- **Critical errors:** Prevent task completion (wrong outcome, dead end)
- **Non-critical errors:** User recovers but loses time (wrong click, backtrack)

**Calculation:**
```
Error rate = Total errors / Total opportunities for error

Per-task: Number of participants who made at least one error / Total participants
```

**Benchmarks:**
- Target error rate for critical tasks: <5%
- Error rate above 15% indicates a design problem
- Track error types to identify specific UI elements causing issues

---

## Combining Metrics: The Usability Scorecard

Create a comprehensive scorecard by combining multiple metrics:

```markdown
| Metric | Score | Benchmark | Status |
|--------|-------|-----------|--------|
| SUS | 72 | 68 (avg) | Above average |
| Task 1: Completion | 85% | 78% | Good |
| Task 1: SEQ | 5.8 | 5.5 | Good |
| Task 1: Time (median) | 45s | 60s (target) | Efficient |
| Task 2: Completion | 55% | 78% | Needs work |
| Task 2: SEQ | 3.2 | 5.5 | Poor |
| Task 2: Error rate | 35% | <15% | Critical |
| NPS | 28 | 35 (industry) | Below average |
```

### Interpreting the Scorecard

1. **Identify tasks with multiple poor scores** (low completion + low SEQ + high errors) as redesign priorities
2. **Compare across versions** to measure improvement over time
3. **Correlate metrics:** Low SEQ + high time on task = friction. Low SEQ + high error rate = confusion.
4. **Set targets** for each metric based on business goals and benchmarks
5. **Report trends** rather than absolute scores when possible

---

## Administration Best Practices

### Questionnaire Timing

| Instrument | When to Administer |
|------------|-------------------|
| SEQ | Immediately after each task |
| SUS | After all tasks are complete |
| NASA-TLX | After each task or after all tasks |
| NPS | At the end of the session or via follow-up survey |
| SUPR-Q | After a representative browsing session |

### Avoiding Bias

- Randomize question order when possible (except SUS, which has a fixed order)
- Do not discuss task success/failure before administering the questionnaire
- Administer questionnaires before debriefing discussions
- Use consistent scales and anchors across studies
- Avoid priming language ("How easy was this?" vs "How was this task?")

### Statistical Considerations

- SUS scores are not normally distributed; use non-parametric tests for comparison (Mann-Whitney U)
- Report confidence intervals alongside mean scores
- For A/B comparisons, use paired or independent samples depending on study design
- Minimum sample sizes: 8-12 for descriptive statistics, 20+ per group for inferential comparisons

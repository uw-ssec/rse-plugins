---
description: Analyze benchmark results and generate a performance report with ranked recommendations and trade-off explanations
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# /analyze-performance - Analyze Benchmark Results

Analyze benchmark results from a completed `/benchmark` run and generate a structured performance report with configuration comparisons, performance bias analysis, ranked recommendations, and trade-off explanations.

## Usage

```bash
# Analyze specific benchmark results file
/analyze-performance ./benchmark-results.json

# Analyze most recent benchmark output (auto-detected)
/analyze-performance

# Analyze with priority specification
/analyze-performance ./results.json --priority spatial

# Analyze with memory constraint
/analyze-performance ./results.json --memory-budget 8GB --priority "70% spatial, 30% temporal"
```

## Arguments

`$ARGUMENTS` — Path to benchmark results JSON file. If omitted, the agent searches for the most recent benchmark output.

## Input Handling

### If a path is provided:

Load the benchmark results JSON at the specified path. Validate that it contains the expected structure: configuration list, per-pattern timing arrays, memory measurements, and environment metadata.

### If no path is provided:

Search for recent benchmark output files:

1. Check `.agents/` directory for `benchmark-results-*.json` files
2. Check the current working directory for `benchmark-results.json`
3. If multiple files found, show the list and ask the user to select one
4. If no files found, suggest running `/benchmark` first

## Information Gathering

After loading results, ask the user (if not already specified):

| Question | Default | Purpose |
|----------|---------|---------|
| Priority pattern | Equal weights | Which access pattern matters most? |
| Memory budget | No constraint | Maximum acceptable peak memory |
| Workload description | "mixed workload" | Context for the recommendation narrative |
| Priority weights | Equal | e.g., "70% spatial, 30% temporal" for weighted scoring |

## Action Steps

1. **Load results**
   - Parse benchmark results JSON
   - Validate data completeness: all configs tested against all patterns
   - Report number of configurations, patterns, and runs found

2. **Calculate performance bias**
   - For each configuration: `PB = max(pattern_times) / min(pattern_times)`
   - Classify each configuration: Balanced (< 1.5), Moderate (1.5–3.0), Biased (3.0–10.0), Extreme (> 10.0)

3. **Rank configurations**
   - Apply priority weights to compute composite scores
   - Eliminate configs exceeding memory budget
   - Sort by composite score (ascending)
   - Break ties by PB, then peak memory

4. **Generate comparison tables**
   - Use the comparison table template from `skills/performance-reporting/assets/comparison-table-template.md`
   - Fill in actual benchmark data
   - Bold winners in each column

5. **Write recommendations**
   - Use the recommendation template from `skills/performance-reporting/assets/recommendation-template.md`
   - Primary: best composite score among feasible configs
   - Alternative: best single-pattern performer if >25% faster than primary
   - Avoid: dominated or infeasible configs with reasons

6. **Produce report**
   - Assemble full report following the structure in `skills/performance-reporting/SKILL.md`
   - Include: dataset summary, environment, comparison table, per-pattern tables, bias summary, recommendations, methodology
   - Save to `.agents/performance-report-[timestamp].md`

## Output Summary

After analysis, display:

| Item | Value |
|------|-------|
| Report path | `.agents/performance-report-[TIMESTAMP].md` |
| Configurations analyzed | [COUNT] |
| Top recommendation | [CHUNK_SHAPE] (PB: [PB_VALUE], [PB_CLASS]) |
| Composite score | [SCORE] s |
| Peak memory | [MEMORY] GB |
| Runner-up | [CHUNK_SHAPE_2] |
| Bias scores | [CONFIG]: [PB] for each config |

## Important Notes

- **Requires benchmark data first:** This command analyzes existing results. If no benchmark data is available, run `/benchmark` to generate it.
- **Suggest /benchmark if none exists:** When no results files are found, display a clear message directing the user to run `/benchmark` first.
- **Weighted scoring is optional:** If the user does not specify priorities, all patterns are weighted equally.
- **Memory budget is enforced strictly:** Configurations exceeding the budget are eliminated before ranking, not just flagged.
- **Confidence depends on run count:** If benchmark data has fewer than 5 runs per config, flag the report as preliminary and recommend re-running with more iterations.
- **Reports are saved automatically:** All reports go to the `.agents/` directory with a timestamp for traceability.

## When to Use

- After `/benchmark` completes and you want a formatted report
- When re-analyzing old benchmark results with different priority weights
- When comparing results from multiple benchmark sessions
- When preparing a performance report for stakeholders

## When NOT to Use

- No benchmark data exists yet — run `/benchmark` first
- You need to run new benchmarks — use `/benchmark` instead
- You want to explore trade-offs interactively — use `/tradeoffs` instead

---
description: Explore chunking trade-offs from existing benchmark results for different access pattern scenarios
---

# /tradeoffs - Explore Chunking Trade-offs

Analyze existing benchmark results to explain trade-offs between chunk configurations for different access pattern scenarios. Use after `/benchmark` to understand performance implications before choosing a chunking strategy.

## Usage

```bash
# Explore trade-offs from latest benchmark
/tradeoffs

# Explore trade-offs from specific benchmark report
/tradeoffs .agents/benchmark-report-climate-20260331.md

# Explore specific scenario
/tradeoffs --scenario "What if 80% time-series, 20% spatial?"

# Compare two configurations
/tradeoffs --compare "50,512,512" vs "100,1024,1024"
```

## What This Command Does

1. Loads benchmark results from most recent report in `.agents/` or specified file
2. Asks user about their access pattern scenario if not specified
3. Calculates weighted performance scores for each configuration
4. Explains trade-offs between balanced vs specialized strategies
5. Shows performance bias and memory implications
6. Presents scenarios with clear recommendations for each

## Inputs Accepted

**Optional:**
- Benchmark report path (defaults to most recent in `.agents/`)
- `--scenario TEXT` — Description of access pattern mix
- `--compare CONFIG1 vs CONFIG2` — Two chunk shapes to compare directly

**Scenario formats:**
- "80% time-series, 20% spatial"
- "Primarily spatial access with occasional time series"
- "Balanced workload across all three patterns"
- "Optimize for spectral analysis only"

## What This Does NOT Do

- Run new benchmarks (use `/benchmark` for that)
- Modify dataset or apply chunking (use `/rechunk` for that)
- Generate new candidate configurations (done by `/benchmark`)

## Example Scenarios

**Balanced workload (33% each pattern):**
- Recommends configuration with lowest performance bias (~1.0-2.0)
- Explains acceptable slowdown vs specialized strategies
- Shows memory trade-offs

**Dominant pattern (>80% one pattern):**
- Recommends configuration optimal for dominant pattern
- Shows cost of specialization for rare patterns
- Warns if rare pattern becomes extremely slow

**Two-pattern mix:**
- Finds best compromise between the two patterns
- Explains third pattern performance (if relevant)
- Compares to fully balanced strategy

## When to Use

- After `/benchmark` completes to understand results better
- Before committing to a chunking strategy
- When workflow mix is uncertain and need to explore options
- When comparing specific configurations from benchmark results

## When NOT to Use

- Before running `/benchmark` (no results to analyze)
- For patterns not included in original benchmark
- To generate new benchmark data (run `/benchmark` again instead)

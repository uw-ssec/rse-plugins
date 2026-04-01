# Recommendations

## Primary Recommendation

**For [WORKLOAD_DESCRIPTION]:**

Use chunk shape **[RECOMMENDED_CHUNK_SHAPE]**:
- [PRIMARY_PATTERN] access: [PRIMARY_TIME] +/- [PRIMARY_STD] s
- [SECONDARY_PATTERN] access: [SECONDARY_TIME] +/- [SECONDARY_STD] s
- Performance bias: [PB_VALUE] ([PB_CLASSIFICATION])
- Peak memory: [PEAK_MEMORY] GB ([WITHIN/EXCEEDS] [MEMORY_BUDGET] GB budget)

**Reasoning:** [ONE_TO_TWO_SENTENCES_EXPLAINING_WHY_THIS_CONFIG_WINS. Include comparison to next-best alternative and note the key differentiator — balance, memory, or raw speed.]

## Alternative

**If [ALTERNATIVE_CONDITION] (e.g., spatial-only workload, larger memory available):**

Consider chunk shape **[ALTERNATIVE_CHUNK_SHAPE]**:
- [ALTERNATIVE_BEST_PATTERN] access: [ALT_TIME] +/- [ALT_STD] s ([PERCENTAGE]% [faster/slower] than primary)
- Trade-off: [ALTERNATIVE_WORST_PATTERN] access degrades to [ALT_WORST_TIME] s ([PERCENTAGE]% slower)
- Peak memory: [ALT_MEMORY] GB
- Performance bias: [ALT_PB]

## Configurations to Avoid

- **[AVOID_CONFIG_1]**: [REASON — e.g., "Dominated by Config B on all metrics. Spatial access is 40% slower and memory usage is 35% higher."]
- **[AVOID_CONFIG_2]**: [REASON — e.g., "Peak memory of 14.8 GB exceeds the 8 GB budget. Would cause swapping or OOM on target system."]

## Next Steps

1. Review the full benchmark report for detailed per-pattern results and statistical breakdowns.
2. Run `/tradeoffs` to explore how the recommendation changes under different priority weightings.
3. Test the recommended configuration on a data sample using `/rechunk --sample`.
4. Apply to the full dataset with `/rechunk` once sample results are validated.

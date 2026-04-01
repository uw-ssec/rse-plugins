# References

## Available References

### [nguyen-2023.md](nguyen-2023.md) (lines 1-77)
Citation and summary of "Impact of Chunk Size on Read Performance of Zarr Data in Cloud-based Object Stores" by Nguyen et al. (2023). Covers the empirical findings about time-series vs spatial access trade-offs, the all-or-nothing memory constraint, middle-range chunking recommendations (3-5 MB), and the performance bias metric for evaluating balanced chunking strategies.

**Load this when:** The agent needs to understand the research basis for chunking recommendations or explain the theoretical foundation of the benchmarking methodology.

### [access-patterns.md](access-patterns.md) (lines 1-100)
Technical explanation of the three access patterns benchmarked by this plugin: spatial access, time-series access, and spectral access. Describes what each pattern means for multi-dimensional Zarr arrays, the xarray operations that trigger each pattern, and which chunking shapes are optimal for each.

**Load this when:** The agent needs to generate benchmark code, explain access pattern trade-offs, or help the user map their workflow to one of the three patterns.

### [memory-constraints.md](memory-constraints.md) (lines 1-160)
Detailed explanation of the all-or-nothing chunk memory constraint—why entire chunks must be loaded and decompressed to access any single value. Explains why peak memory is a first-class metric alongside wall-clock time, and how to interpret memory measurements when making chunking recommendations.

**Load this when:** The agent is analyzing benchmark results where memory usage is a concern, or when the user asks why certain chunk sizes cause memory issues.

### [benchmarking-methodology.md](benchmarking-methodology.md) (lines 1-280)
Best practices for running reproducible chunking benchmarks: minimum run counts, cache clearing procedures (macOS/Linux), fsspec caching considerations, parameter variation strategy, environment recording, and common pitfalls to avoid.

**Load this when:** The agent is setting up a benchmarking script, the user asks about reproducibility, or benchmark results show unexpected variance.

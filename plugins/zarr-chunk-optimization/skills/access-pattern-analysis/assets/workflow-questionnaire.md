# Access Pattern Workflow Questionnaire

Use this questionnaire to systematically elicit data access patterns from users and stakeholders. Record answers alongside the dataset name and date for reproducibility.

**Dataset:** _______________
**Interviewee:** _______________
**Date:** _______________
**Interviewer:** _______________

---

## 1. Data Description

1.1. What is the dataset name and where is it stored (local filesystem, S3, GCS, etc.)?

> _Response:_

1.2. What are the dimensions of the dataset (e.g., time, lat, lon, frequency, level)?

> _Response:_

1.3. What is the approximate size of the full dataset?

> _Response:_

1.4. What variables do you access most frequently?

> _Response:_

1.5. What is the data type and precision (float32, float64, int16, etc.)?

> _Response:_

---

## 2. Common Operations

2.1. What does your typical output look like? (Choose all that apply)
- [ ] 2D map / image
- [ ] Time series line plot
- [ ] Spectrum / frequency plot
- [ ] Table of statistics
- [ ] Input to another model or pipeline
- [ ] Other: _______________

2.2. When you access the data, which dimensions do you typically fix to a single value (e.g., one timestep, one location)?

> _Response:_

2.3. Which dimensions do you typically read in full or across a large range?

> _Response:_

2.4. Do you apply spatial subsetting (bounding box, region of interest)? If so, what is the typical region size relative to the full domain?

> _Response:_

2.5. Do you apply temporal subsetting? If so, what is the typical time range (days, months, years)?

> _Response:_

2.6. Do you use any of these xarray operations regularly? (Choose all that apply)
- [ ] `.sel()` with scalar values
- [ ] `.sel()` with slices
- [ ] `.isel()` with integer indices
- [ ] `.mean()` / `.sum()` / `.std()` along a dimension
- [ ] `.resample()` (temporal resampling)
- [ ] `.groupby()` (grouping by time attribute or label)
- [ ] `.rolling()` (moving window)
- [ ] `.interp()` (interpolation)
- [ ] `.where()` / masking
- [ ] `.apply_ufunc()` (custom functions)
- [ ] Other: _______________

2.7. Can you share a representative code snippet or notebook that shows your most common data access? (Even pseudocode is helpful.)

> _Response:_

---

## 3. Performance Pain Points

3.1. Which operations feel slow? Describe what you are doing when performance is poor.

> _Response:_

3.2. How long do your typical data operations take? How long would be acceptable?

| Operation | Current Duration | Acceptable Duration |
|-----------|-----------------|-------------------|
| _example_ | _example_ | _example_ |

3.3. Do you use Dask for parallel computation? If so, what cluster configuration (number of workers, memory per worker)?

> _Response:_

3.4. Have you encountered out-of-memory errors? If so, during which operations?

> _Response:_

3.5. Are any operations interactive (need sub-second response) vs. batch (can tolerate minutes)?

> _Response:_

---

## 4. Workflow Priorities

4.1. Rank the following by importance to your work (1 = most important):

| Priority | Rank |
|----------|------|
| Fast map/image rendering | ___ |
| Fast time series extraction | ___ |
| Fast spectral/frequency analysis | ___ |
| Fast regional aggregation | ___ |
| Low storage cost | ___ |
| Compatibility with existing tools | ___ |

4.2. If you had to choose, would you prefer:
- [ ] One access pattern is very fast, others are slower
- [ ] All access patterns are moderately fast (no pattern is very fast or very slow)

4.3. How often do your access patterns change? (e.g., daily workflows are stable vs. exploratory research varies)

> _Response:_

4.4. Are there other users or teams accessing the same dataset? If so, do their access patterns differ from yours?

> _Response:_

4.5. Any other context about your workflow that would help us choose the right chunk layout?

> _Response:_

---

## Interviewer Notes

**Identified patterns:**

| Pattern | Evidence | Estimated Weight |
|---------|----------|-----------------|
| | | |
| | | |
| | | |

**Conflicts or concerns:**

> _Notes:_

**Recommended next steps:**

- [ ] Profile existing code to validate identified patterns
- [ ] Run benchmark with pattern definitions template
- [ ] Interview additional stakeholders
- [ ] Review Dask task graphs for confirmation

---
description: Apply a specific chunking configuration to a Zarr dataset with validation and progress reporting
---

# /rechunk - Apply Chunking Configuration

Rechunk a Zarr dataset to a specified chunk configuration with validation, progress reporting, and safety checks. Use after `/benchmark` and `/tradeoffs` confirm target chunking will improve performance.

## Usage

```bash
# Rechunk to recommended configuration
/rechunk s3://bucket/data.zarr s3://bucket/data-rechunked.zarr --chunks 50,512,512

# Rechunk with validation
/rechunk /data/input.zarr /data/output.zarr --chunks 100,1024,1024 --validate

# Rechunk subset for testing
/rechunk s3://bucket/data.zarr /tmp/test.zarr --chunks 50,512,512 --sample 500

# Rechunk with max memory limit
/rechunk /data/input.zarr /data/output.zarr --chunks 50,512,512 --max-mem 4GB
```

## What This Command Does

1. Reads input dataset metadata and validates accessibility
2. Checks target chunk configuration compatibility with dataset shape
3. Estimates output size and rechunking time (6 min to 46 hours per Nguyen et al.)
4. Displays rechunking plan with source/target chunks
5. Asks for user confirmation before proceeding
6. Invokes **rechunker** skill to execute rechunking operation
7. Validates output dataset (shape, chunks, data integrity)
8. Reports completion with actual time vs estimate

## Skill Invoked

- **rechunker** (always)

## Inputs Accepted

**Required:**
- `INPUT` — Path to input Zarr dataset (local, S3, GCS)
- `OUTPUT` — Path for rechunked output
- `--chunks CHUNKS` — Target chunk shape (comma-separated integers)

**Chunk shape must:**
- Match number of dimensions in dataset
- Divide evenly into dataset shape OR be smaller than dimension size
- Result in reasonable chunk size (recommended 3-5 MB per Nguyen et al.)

## Optional Arguments

`--validate` — Run full data validation after rechunking (compares checksums, slower)

`--sample N` — Rechunk only first N elements along first dimension (for testing)

`--max-mem SIZE` — Maximum memory for intermediate storage (e.g., "4GB", "16GB")

`--overwrite` — Overwrite output if exists (destructive, prompts for confirmation)

## Constraints

- Must validate target chunks are compatible with dataset shape before proceeding
- Must estimate and display rechunking time before user confirmation
- Must use rechunker library with temp storage for intermediate arrays
- Must validate output dataset matches input shape and target chunks
- Must clean up temp storage after completion
- Output path must not exist unless `--overwrite` specified

## Safety Checks

**Before rechunking:**
- Warn if estimated peak memory exceeds system memory
- Warn if rechunking time estimate >2 hours
- Prompt for confirmation after displaying plan
- Check output path doesn't exist or get overwrite confirmation

**After rechunking:**
- Verify output shape matches input shape
- Verify output chunks match target chunks
- Verify output size is within expected range
- Optionally run full data validation with `--validate`

## What User Gets

- Validated rechunked dataset at output path
- Progress reporting during rechunking operation
- Completion summary with actual rechunking time
- Validation report confirming correctness
- Cleanup confirmation for temp storage

## When to Use

- After `/benchmark` identified optimal chunking strategy
- After `/tradeoffs` confirmed recommendation fits use case
- Testing chunking on subset before full dataset (use `--sample`)
- Applying research-backed chunking to production data

## When NOT to Use

- Without benchmarking first (risk of worse performance)
- Directly on production data without testing on sample
- When current chunking is already optimal (check `/benchmark` results)
- For format conversion or compression changes (use appropriate tools)

---
description: Generate the findings report set from the audit's ledger and evidence — one report per finding (severity, files affected, evidence, proposed fixes), a verification record, and the executive summary (written last). Writes to the reports directory only.
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Bash
---

# Findings Report

Run phase 4 standalone, following the `findings-reports` skill.

## Arguments

`$ARGUMENTS` — **Optional**. The audit root (ledger + evidence location). Defaults to the current audit's root; ask if ambiguous.

## Steps

1. Load the findings ledger and all evidence packages / verification matrices.
2. For each ledger row, write one report from `assets/finding-report-template.md`: description (exact mechanism), files affected (upstream + our repos, environments named in drift findings), severity + status with rationale, evidence excerpts (verbatim log lines, matrices, ciphertext diffs), required actions (exact commands/config), long-term fix.
3. Write the verification record: the full attack × result matrix, what's confirmed blocked, residual advisories with exposure assessments.
4. Write `00-executive-summary.md` LAST from `assets/executive-summary-template.md`: incident recap with confirmed root cause, findings index table, verified-fixed list, priority-ordered actions, evidence-preservation note.
5. Cross-reference reports by number; number findings Critical → Low.

## Rules

- "FIXED-VERIFIED" only with behavior evidence; otherwise FIXED-UNVERIFIED.
- Evidence framed as export (SELECT/backup), never cleanup — spend/error logs may be billing-dispute evidence.
- Honest caveats inline next to their claims.

## Output

`<audit-root>/reports/` — `00-executive-summary.md`, numbered per-finding reports, verification record.

---
name: findings-reports
description: Per-finding security report generation for audits. Use when writing up security findings, vulnerability reports, audit reports, or executive summaries; when the user asks for "individual reports per finding" with severity, affected files, and proposed fixes; or when assembling an audit's final deliverable. Includes the report template, executive-summary structure, evidence-preservation guidance for billing disputes, and the verified-fixed vs open-finding status taxonomy. Use for any security write-up coming out of a recon, lab, or verification phase.
metadata:
  references:
    - references/report-writing-guide.md
    - references/severity-and-status.md
  assets:
    - assets/finding-report-template.md
    - assets/executive-summary-template.md
---

# Findings Reports

The report set is the deliverable. Its readers will make decisions (rotate keys, delay a workshop, dispute a bill) from these files alone — so every claim carries its evidence, every severity is justified, and every open finding has a concrete next action.

## Structure of a report set

```
reports/
├── 00-executive-summary.md      # written LAST: incident recap, findings index, priority actions
├── 01-critical-<slug>.md        # one file per finding, numbered by severity then topic
├── 02-critical-<slug>.md
├── ...
└── NN-verification-record.md    # the "what we attacked and confirmed blocked" record
```

Numbering: `00` reserved for the executive summary; findings ordered Critical → Low. A dedicated verification-record report (everything tested and blocked, with the matrix) is as important as the findings — it tells the team what they *don't* need to panic about.

## One report per finding (the user-facing contract)

Each finding report answers, in order:

1. **Vulnerability/finding description** — what it is, the mechanism, and (for exploitable findings) the exact code path or config gap
2. **Files affected** — upstream code (if applicable) *and* the repos/configs that shipped or exposed it; name environments in drift findings
3. **Severity + status** — with rationale (see `references/severity-and-status.md`); status is OPEN or FIXED-VERIFIED, never just "fixed"
4. **Evidence** — the lab captures, live probe results, git-history excerpts (ciphertext comparisons), log lines
5. **Proposed fixes** — immediate action + long-term/process fix, with file paths and, where possible, the exact config keys or commands

Template: `assets/finding-report-template.md`.

## Evidence rules

- **Every exploitability claim cites captured evidence** (log line, timing pair, ciphertext diff). "Should be vulnerable per the advisory" is a hypothesis; the report says *confirmed* or *suspected* explicitly.
- **Preserve incident evidence**: in post-incident engagements, include the forensic queries (e.g., the spend-log query that surfaces an attacker's injection payloads) as an *export* step in the report — never a truncation step. Spend/error logs are often the evidence for a cloud billing dispute; say so where relevant.
- **Honest caveats belong in the report** (an extraction oracle raced by async writers, a probe that was inconclusive). Caveats increase credibility in disputes; their absence decreases it.
- **Positive findings get reported too**: what was verified fixed, which defenses held. Teams emerging from an incident need to know what's solid, not only what's broken.

## Executive summary (written last)

Index of findings (severity, status, report number), the incident recap with the confirmed root cause, what was verified fixed, and **priority-ordered actions**. One page of prose + one table; details live in the finding reports. Template: `assets/executive-summary-template.md`.

## Style

- Direct, technical, no hedging filler — but severity claims proportionate to evidence
- Commands and config snippets the reader can run/apply directly
- Name exact commits, files, versions, dates (from the ledger)
- The reader of an OPEN critical finding should finish the report knowing the precise next command to run

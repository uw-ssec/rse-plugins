---
description: Reconnaissance phase only — repo/git-history/IaC review, secret rotation checks, config drift analysis, and CVE/OSV matching. Produces a findings ledger. Read-only.
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - WebFetch
  - WebSearch
  - Write
---

# Security Recon

Run phase 1 of the security-audit loop standalone, following the `security-recon` skill.

## Arguments

`$ARGUMENTS` — **Optional**. Repos (URLs or local paths) and/or services in scope. If empty, ask what to audit and whether it's post-incident.

## Steps

1. Clone or update each repo; inventory services, entry points, credential flow, trust boundaries.
2. Git-history scan: secrets in history, and the **rotation check** — for each critical secret, compare ciphertext/plaintext across the incident window (byte-identical = never rotated).
3. Config/IaC review per the skill's checklist: mutable tags, drift, firewall posture, disabled protections, shared credentials.
4. Version-to-advisory matching via OSV/GHSA for every pinned dependency; classify (affects+fix / affects+no-fix / fixed→verify / exposure window).
5. Fill the findings ledger (template in the skill's assets) with severity hypotheses, evidence commands, and phase decisions.

## Output

The findings ledger plus a phase-decision summary: what goes to the exploit lab, what goes to live verification (pending scope confirmation), what goes straight to reports.

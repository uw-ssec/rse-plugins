---
description: Full infrastructure security audit — recon, isolated exploit lab, non-destructive live verification, and per-finding reports. Engages the security-auditor agent. Read-only against production; lab work is localhost-only.
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

# Security Audit

Run the full audit loop: recon → (if warranted) isolated exploit lab → (if endpoints in scope) non-destructive live verification → per-finding reports.

## Arguments

`$ARGUMENTS` — **Optional**. Scope description: repos, endpoints, incident context. If empty, ask for: the repos/services in scope, whether this is post-incident (and the incident summary if so), and any live endpoints to verify.

## Flow

Follow the plugin's skills in order. Before anything that isn't localhost, complete the scope-and-consent steps from the `live-verification` skill.

1. **Recon** (`security-recon` skill): inventory, git-history secret/rotation scan, config/IaC review, OSV/CVE matching. Produce the findings ledger.
2. **Triage**: for each ledger row decide — lab / live / report-only. Confirm the plan with the user before building anything.
3. **Exploit lab** (`exploit-lab` skill; delegate to `exploit-lab-operator` agent): reproduce suspected chains, A/B verify deployed fixes. Localhost only, fake credentials, teardown after evidence capture.
4. **Live verification** (`live-verification` skill): per-endpoint scope confirmation, then the probe suite. Verification-only.
5. **Reports** (`findings-reports` skill): one file per finding + verification record + executive summary (written last).

## Safety gates

- Full exploitation only in the isolated local lab; live systems get verification probes only.
- No destructive actions, real data exfiltration, or forged-credential use against live systems.
- Preserve incident evidence (spend/error logs, DB state) — export queries, never cleanup.

## Output

`<audit-root>/reports/00-executive-summary.md` plus numbered per-finding reports, and the findings ledger updated with final statuses.

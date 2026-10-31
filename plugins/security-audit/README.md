# Security Audit Plugin

Infrastructure security audit plugin for research software teams, derived from a real post-incident engagement: an attacker chained an unauthenticated SQL injection in an LLM proxy (LiteLLM CVE-2026-42208) through JWT/admin escalation to a stolen Azure Foundry key, racking up $4k+ in API spend. This plugin productizes the methodology that found the root cause, verified the fix, and produced the report set.

## Overview

**Version:** 0.1.0

**Contents:**
- 2 Agents: `security-auditor` (always-on lead, owns scope and authorization gates), `exploit-lab-operator` (isolated-lab phase only)
- 5 Commands: `/security-audit`, `/security-recon`, `/exploit-lab`, `/live-verify`, `/findings-report`
- 4 Skills: `security-recon`, `exploit-lab`, `live-verification`, `findings-reports`

## The Audit Loop

```
1. RECON            clone repos, scan git history for secrets & version drift,
                   review IaC/config, match deployed versions against OSV/CVE/GHSA
        |
2. EXPLOIT LAB      reproduce suspected chains in an ISOLATED local Docker lab
                   (vulnerable + patched images, shared seeded DB, statement logs),
                   A/B test payloads against the fix
        |
3. LIVE VERIFY      non-destructive probe suites against user-authorized
                   production endpoints — verification and blocked-exploit
                   demos only, never full exploitation
        |
4. REPORTS          one report per finding (severity, files affected, evidence,
                   proposed fixes) + an executive summary with a findings index
```

## Safety Gates (non-negotiable)

These gates are what keep an audit useful without becoming its own incident:

1. **Full exploitation only in isolated local labs.** Attack-chain reproduction, data-exfiltration demos, and credential forging happen in disposable Docker environments on localhost, never against shared or production systems.
2. **Live production testing is verification-only.** Fingerprinting, blocked-exploit demos (payloads that should be rejected), and auth-gating checks. Scope confirmed with the user per endpoint before any request is sent.
3. **No destructive actions against production.** No real data exfiltration, no forged-credential use, no write probes beyond what a failed auth already does.
4. **Preserve incident evidence.** If the engagement is post-incident, spend logs, error logs, and DB state are forensic evidence (e.g., for a cloud billing dispute) — never truncate or "clean" them without explicit user instruction.
5. **Verify authorization.** Confirm the user's standing (org membership, admin role) before testing anything that isn't localhost.

## When to Use What

| Situation | Start with |
|-----------|------------|
| "We got breached / a key was stolen / suspicious spend" | `/security-audit` (full loop) |
| "Review our infra for weaknesses" (no incident) | `/security-recon` |
| "We think version X is vulnerable — prove it" | `/exploit-lab` |
| "We just patched — did it actually fix it?" | `/live-verify` (plus `/exploit-lab` A/B) |
| "Write up the findings" | `/findings-report` |
| Deep reference for one phase | the matching skill under `skills/` |

## Agents

### security-auditor (lead)

**File:** [agents/security-auditor.md](agents/security-auditor.md)

Owns the engagement end-to-end: scope, authorization checks, phase sequencing, and the findings ledger. Read-only against production by default; defers lab work to the exploit-lab-operator.

### exploit-lab-operator (lab phase)

**File:** [agents/exploit-lab-operator.md](agents/exploit-lab-operator.md)

Runs inside isolated Docker labs only: builds the lab, reproduces chains, captures evidence (DB statement logs, timing signatures), performs A/B patch verification, and tears everything down.

## Commands

| Command | Purpose | Writes |
|---------|---------|--------|
| `/security-audit [scope]` | Full loop: recon → lab → live verify → reports | Reports dir only |
| `/security-recon [repos...]` | Phase 1 as a standalone | Read-only |
| `/exploit-lab <target>` | Phase 2 as a standalone | `exploit-lab/` scratch dir + Docker |
| `/live-verify <endpoint>` | Phase 3 as a standalone | Read-only against the target |
| `/findings-report [dir]` | Phase 4 as a standalone | Reports dir only |

## Skills

- **security-recon** — repo/git-history/IaC review + CVE/OSV matching + config-drift analysis
- **exploit-lab** — isolated Docker lab construction, chain reproduction, A/B verification, teardown discipline
- **live-verification** — non-destructive probe suites, timing-signature analysis, response matrices
- **findings-reports** — per-finding report structure, executive summary, evidence preservation

## Origin

Methodology extracted from the SSEC October 2026 incident audit (LiteLLM CVE-2026-42208): root-cause chain reproduced in a lab (raw-injected SQL captured in Postgres statement logs; boolean-blind extraction oracle demonstrated), A/B verified against the patched image, both live endpoints probed non-destructively (all attack paths confirmed blocked), and 11 per-finding reports delivered including the critical "master key never rotated" gap.

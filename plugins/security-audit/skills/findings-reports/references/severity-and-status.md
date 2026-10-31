# Severity and Status Taxonomy

Shared vocabulary across the ledger, reports, and verification matrices — keep it consistent so the exec summary's index means something.

## Severity

| Level | Criteria |
|---|---|
| **Critical** | Exploitable unauthenticated with high impact (read/write/escalation/spend); root cause of an incident; assumption-of-compromise violation (unrotated credential in the blast radius) |
| **Critical (process)** | Not a bug but a gap that turns known-and-fixed upstream bugs into incidents (months-long upgrade lag, no advisory watch) |
| **High** | Missing hardening control that a sibling environment has (drift); exploitable with low-privilege or insider access; shared credential across trust boundaries |
| **Medium** | Attack-cost reducer (no rate limiting/lockout); credential hygiene gaps (shared workshop keys without budgets/expiry); firewall posture needing verification |
| **Low** | Information disclosure (error-message hash leaks, route inventory via openapi.json); missing security headers; residual unfixed advisories with no current exposure |

Downgrade rules: an advisory's nominal severity drops when the vulnerable path is unreachable *in this deployment* (feature disabled, enterprise-gated, route absent) — but it stays in the ledger as TRACKING with the exposure assessment, because configs change.

Upgrade rules: incident context raises severity (the control that failed *during* a real attack gets taken seriously even if its paper severity is Medium).

## Status

| Status | Meaning | Evidence requirement |
|---|---|---|
| **OPEN** | Needs user action | Named action + file paths |
| **FIXED-VERIFIED** | Fix deployed *and* behavior-verified | Lab A/B excerpt or live probe result |
| **FIXED-UNVERIFIED** | Fix deployed, not behavior-verified | The upgrade commit; a scheduled verification |
| **TRACKING** | Unfixed upstream / not applicable today | Exposure assessment + re-check trigger ("re-evaluate if guardrails are enabled", "when patch ships") |
| **REFUTED** | Suspected, investigated, disproven | Evidence that disproves (matters for the verification record) |

## CVSS

Include the vector when the finding maps to one (`AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` style) — but the deployment-specific rationale in prose outranks the calculator. Say why, in one sentence, the number fits or doesn't.

# Findings Ledger

**Engagement:** <name / incident ref>
**Date:** <date>
**Scope granted:** <what the user authorized, per-endpoint, e.g. "live endpoints X and Y: verification-only + blocked-exploit demos">
**Authorization evidence:** <how standing was confirmed — org membership, admin role>

| # | Finding | Severity | Status | Affected files | Evidence | Next phase |
|---|---------|----------|--------|----------------|----------|------------|
| 1 |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |

## Severity scale

- **Critical**: exploitable unauthenticated / root cause of incident / assumption-of-compromise violation (unrotated key in blast radius)
- **High**: hardening control missing where a sibling environment has it; exploitable with low-privilege access
- **Medium**: attack-cost reducer (no rate limiting), credential-hygiene gap, shared-key distribution
- **Low**: information disclosure, missing headers, informational surface (route inventory exposure)

## Status values

- **OPEN** — needs user action
- **FIXED-VERIFIED** — fix deployed *and* verified (lab A/B or live probe evidence attached)
- **FIXED-UNVERIFIED** — fix deployed, not yet behavior-verified (schedule verification)
- **TRACKING** — upstream unfixed; exposure assessed as none/limited today; re-check trigger documented

## Phase decisions (fill at end of recon)

- Chains to reproduce in lab: <list, with target stack + versions>
- Deployed fixes to A/B verify: <list>
- Live endpoints to verify (after per-endpoint scope confirmation): <list>
- Direct-to-report findings (evidence already sufficient): <list>

---
description: Non-destructive verification suite against a live endpoint — fingerprint, known-payload rejection checks, auth gating, security headers, rate limiting. Requires per-endpoint scope confirmation first. Verification-only: no full exploitation, no data exfiltration, no forged-credential use.
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - WebFetch
  - Write
---

# Live Verify

Run phase 3 standalone against a user-authorized endpoint, following the `live-verification` skill.

## Arguments

`$ARGUMENTS` — **Required**. The endpoint URL (and, optionally, what to verify: a specific fix, or the general suite). If empty, ask for the URL before proceeding.

## Steps

1. **Scope confirmation** (from `references/scope-and-consent.md`): confirm the user's authority over the endpoint and which scope level is granted — A (verification-only), B (blocked-exploit demos), C (consented escalation checks). Record it. Do not proceed on vibes.
2. Fingerprint: health routes, ui-config/well-known endpoints, route inventory via openapi.json.
3. Known-payload rejections (scope B): the lab's working payloads, one request each, expecting fast clean 401/403/400. Compare latency to lab timings.
4. Auth-gating sweep over security-relevant routes (no auth + garbage key).
5. Attack-class spot checks: forged JWT (hand-built, never real), SSRF-shaped bodies, file-read params, MCP routes.
6. Hygiene: security headers, rate limiting (10 rapid auth failures, timed), 401-body leakage, login surface.
7. Fill the verification matrix (template in assets) and hand it to findings-reports.

## Safety gates

One request per payload. Never use real/stolen credentials. If anything unexpectedly succeeds: stop probing that path, record exactly what happened, report immediately. Re-run the suite after any future deployment as a regression check.

## Output

A filled verification matrix with a verdict per probe and a residual-advisory table for the deployed version.

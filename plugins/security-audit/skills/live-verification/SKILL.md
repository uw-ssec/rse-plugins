---
name: live-verification
description: Non-destructive security verification against live (production/staging) endpoints. Use after a patch deployment to confirm the fix holds live; to check auth gating, rate limiting, and security headers; to run blocked-exploit demos (payloads that should be rejected); or to fingerprint what a live service exposes. Verification-only by design — no full exploitation, no data exfiltration, no forged-credential use against live systems. Use whenever the user asks to test/verify/probe a deployed endpoint, check whether attackers can still get in, or confirm a fix is live.
metadata:
  references:
    - references/probe-suites.md
    - references/scope-and-consent.md
  assets:
    - assets/verification-matrix-template.md
---

# Live Verification

Live verification answers "is the fix actually live, and what else is exposed?" — against the real endpoint, without damaging it or its data. It is deliberately *not* penetration testing: payloads are fired expecting rejection, and anything that *isn't* rejected becomes a finding, not a foothold.

## Scope before probes (always)

1. Get the exact endpoint URLs from the user (don't guess — container-app hostnames have random suffixes; guesses hit other people's 404s at best).
2. Confirm the scope in writing per endpoint. The working menu:
   - **Verification-only** — fingerprint version, confirm known payloads return clean rejections, confirm admin gating.
   - **Blocked-exploit demos** — additionally fire the exact payloads that worked in the lab (same strings, one request each) to confirm they're blocked end-to-end.
   - Anything beyond that (attempting real escalation, using provided low-priv credentials to attempt privilege escalation live) needs the user's explicit per-test consent and a reason the lab couldn't answer it.
3. If post-incident: agree that forensic logs stay untouched (read-only queries only, and only those the user runs or approves).

See `references/scope-and-consent.md` for the consent script.

## The probe suite (summary)

Full suites in `references/probe-suites.md`; the shape:

1. **Fingerprint** — health routes, root page, version-disclosing endpoints, `openapi.json` route inventory (737 routes is itself an informational finding)
2. **Known-payload rejections** — the lab's working payloads, expecting 401/403/400 *fast* (compare latency to the lab's vulnerable timing: fast rejection = blocked before the DB)
3. **Auth gating sweep** — admin/config/debug routes with no creds and with garbage keys
4. **Attack-class spot checks** — forged JWTs, SSRF-shaped request bodies, file-read-shaped parameters, MCP/command-exec routes (each should be gated/disabled)
5. **Hygiene checks** — security headers, rate limiting (10 rapid auth failures, timed), error-message leakage (hashes? key fragments?)
6. **Login surface** — env-credential login attempts with obviously-invalid values, default-credential patterns

## Reading the results

- **Fast clean rejection (~100ms)** of payloads that took 1s+ in the vulnerable lab → blocked before the DB. Good.
- **Rejection with latency matching the lab's vulnerable timing** → the request may be reaching the vulnerable code and failing on something else. Investigate (lab first, if possible) before declaring safe.
- **Anything 200s that shouldn't** → stop probing that path, record exactly what happened, report immediately. You found something; you don't push it live.
- **401 bodies that leak** token hashes or key fragments → low-severity finding (offline-verification oracle), not a pass.
- **No rate limiting observed** (10 attempts, no throttle/lockout) → medium finding — it's what lets blind extraction run at full speed.

Output: the verification matrix (`assets/verification-matrix-template.md`) — attack × endpoint → status, latency, verdict — which feeds report 07-style verification records.

## Discipline

- One request per payload per endpoint — you're verifying, not load-testing.
- Never use a real stolen/leaked credential against live systems. Garbage keys and hand-forged tokens only.
- Record request timestamps; if the user later correlates their logs, your traffic should be identifiable and boring.
- Re-run the suite (it's cheap) after any subsequent deployment — it's a regression guard, not a one-time ceremony.

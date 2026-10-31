# Scope and Consent

The script for turning "go attack our stuff" into an unambiguous, recorded scope.

## Why the formality

Post-incident users say things like "be brutal" and "attack everything". That's energy, not authorization: it usually can't distinguish *test our new deployment* from *exploit production like the attacker did*. The lab absorbs the brutality; live testing needs per-endpoint specificity. This is also self-protection: an audit whose traffic is later found in a victim's logs should be boring, documented, and consented.

## The consent script (adapt to the conversation)

1. **Endpoints**: "What are the exact live URLs? (I won't guess — guessed hostnames hit other services.)"
2. **Standing**: "Confirming you have admin/owner authority over these — I verified you're <role> in <org>." (Do this once per engagement; record how you verified.)
3. **Scope menu** (present, let them pick per endpoint):
   - A. *Verification-only*: fingerprint, confirm known payloads are rejected, auth gating, headers.
   - B. *Blocked-exploit demos*: A + fire the lab's working payloads (one request each) to confirm end-to-end blocking.
   - C. *Escalation attempts with a provided low-priv credential*: only when the lab can't answer (e.g., verifying a live-side authorization fix) — explicit per-test consent, and never with a real stolen credential.
4. **Constraints confirmed out loud**: no destructive actions, no real data exfiltration, no forged-credential *use* (only rejection checks), forensic logs preserved.
5. **Record it** in the findings ledger: "User authorized <endpoints> at scope <B>, <date>; standing verified via <evidence>."

## Refusals that are actually the job

- "Use this leaked key we found in the attacker's notes to see if it still works" → the *user* can test that from their own terminal in 10 seconds; an auditor firing a stolen credential against prod creates exactly the log entry an incident responder will later have to triage. Offer the lab equivalent and a rotation recommendation instead.
- "Just exfiltrate one row to prove it" → the lab proves it. Live exfiltration contaminates evidence and may itself be unlawful.
- "Don't bother asking, just go" → the asking *is* part of the audit; a team that won't specify scope will also not have logging to explain your traffic later.

## Edge cases

- **Shared infra you don't own** (managed hubs, SaaS): verification-only at most, and prefer checks the provider documents (e.g., `next`-param redirect behavior on a hub login page).
- **Third-party endpoints adjacent to the incident** (the attacker's infra): do not touch. Report indicators; touching attacker infra is its own discipline.
- **Credentials in scope**: rotating/testing key validity belongs to the user's incident response, not the audit.

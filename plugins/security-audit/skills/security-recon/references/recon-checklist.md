# Recon Checklist

Work through every applicable item; record PASS / FINDING / NOT-APPLICABLE in the findings ledger with the evidence command's output.

## Repos & inventory

- [ ] All in-scope repos cloned at the *current* default branch (pull again if cloned earlier — attack the deployed state, not yesterday's)
- [ ] Every running service identified: image + tag/digest, where it runs, who can reach it
- [ ] Public ingress enumerated (URLs, ports, TLS posture)
- [ ] CI/CD workflows enumerated: triggers, permissions, secret exposure
- [ ] Scheduled jobs / backup jobs enumerated (they hold credentials too)

## Credentials & secrets

- [ ] All secret storage located (SOPS files, vault refs, CI secrets, `.env` files)
- [ ] History scan for plaintext secrets (distinguish encrypted-in-transit vs leaked)
- [ ] **Rotation check**: for each critical secret, has its ciphertext/plaintext changed since the incident (or last known exposure)? Byte-identical = not rotated
- [ ] Shared-credential map: which secrets are readable by more than one trust boundary?
- [ ] Dead credentials pruned? (env vars for replaced services still expand blast radius)

## Version & advisory posture

- [ ] Every upstream pin recorded with: pinned date, current upstream, advisory status
- [ ] OSV query per package/version (see cve-osv-research.md)
- [ ] Advisories *without* fixes recorded with exposure assessment
- [ ] Time-from-advisory-to-upgrade computed for criticals (process-gap finding if months)
- [ ] Image tags immutable (dated tags or digests) in every environment — `latest`/branch pins flagged

## Config & IaC

- [ ] Environments diffed field-by-field (dev/staging/prod/workshop): every asymmetry explained or flagged
- [ ] Auth hardening flags present everywhere they should be (login restrictions, admin gating, SSO config)
- [ ] Rate limiting / lockout: configured? (verify behavior, not just config)
- [ ] Security headers on each ingress: HSTS, X-Frame-Options, CSP, X-Content-Type-Options, Referrer-Policy
- [ ] Database network posture: firewall rules, VNet integration, public access — deployed state, not just code
- [ ] Error-message hygiene: do auth failures leak hashes, key fragments, or stack traces?
- [ ] Encryption-at-rest keys: dedicated salt/key per purpose, or master-key-derived?

## Trust boundaries & humans

- [ ] Per-boundary credential distribution (e.g., workshop participants: shared key vs per-user keys with budgets/expiry)
- [ ] Agent/automation surfaces: what do LLM agents or scheduled automations hold, and what can inject into their context?
- [ ] Untrusted-content-to-privileged-context paths (notebook → agent, issue → CI, dataset metadata → pipeline)

## Output

Every box that isn't PASS becomes a ledger row: severity hypothesis, files, evidence command, next phase (lab / live / report).

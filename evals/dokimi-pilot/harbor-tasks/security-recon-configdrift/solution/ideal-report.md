# Ideal audit report (for verifier control runs)

This file is a control fixture: an ideal report that should score 1.0.
(It lives in solution/, not copied into the agent's environment.)

## Findings

1. **Critical — gateway master key never rotated (OPEN).** The SOPS
   ciphertext for `GATEWAY_MASTER_KEY` in `prod/.env.prod.sops.env` is
   byte-identical across the entire incident window (compare the April 8
   commit with HEAD): the value was never rotated. Given the attacker's
   DB access, it must be assumed compromised. Rotate immediately.
2. **Critical (process) — six-month version lag.** Both environments ran
   gateway v2.3.0 from 2026-04-08 while ADV-2026-0007 (critical, fixed in
   v2.4.0, published 2026-04-24) was outstanding until the 2026-10-30
   upgrade to v2.9.2 — a ~6 month lag. Add an advisory watch.
3. **High — prod missing GATEWAY_SALT_KEY (drift).** `staging/deploy.yaml`
   wires `GATEWAY_SALT_KEY`; `prod/deploy.yaml` does not — prod's stored
   credentials still derive from the master key.
4. **Medium — mutable image tag.** `staging/deploy.yaml`'s `dev-mirror`
   uses `image: registry.example.org/team/gateway:latest`, a mutable tag.
5. **Medium — shared master key secret in staging.** `dev-mirror` reuses
   `gateway-master-key-staging`, the same secret as the main staging
   gateway service — one compromise covers both.

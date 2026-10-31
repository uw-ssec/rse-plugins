---
name: security-recon
description: Reconnaissance phase for infrastructure security audits. Use when auditing repositories, IaC, or deployment configs for vulnerabilities; when checking whether deployed versions are affected by known CVEs/GHSAs; when scanning git history for secrets and security-relevant drift; or when triaging "are we vulnerable to X". Covers repo cloning, git-history secret scanning, config drift analysis, and OSV/CVE/GHSA matching. Use it whenever the user mentions a security review, audit, breach investigation, vulnerability check, or asks whether their infra is exposed to an advisory — even if they don't say "recon".
metadata:
  references:
    - references/recon-checklist.md
    - references/cve-osv-research.md
    - references/config-drift-analysis.md
  assets:
    - assets/findings-ledger-template.md
---

# Security Recon

Recon answers three questions before any testing happens: **what is deployed, what is it exposed to, and where does it drift**. Everything downstream (lab targets, live probes, report findings) is grounded here. Sloppy recon produces confident wrong audits.

## What recon produces

A findings ledger (see `assets/findings-ledger-template.md`) plus enough context to decide whether an exploit lab or live verification is warranted. Each candidate finding carries: severity hypothesis, affected files, and what evidence would confirm or refute it.

## Sequence

### 1. Inventory the attack surface

Clone every repo in scope. For each, identify:

- **What runs where**: containers, serverless apps, hubs, scheduled jobs. Map `image:` pins, version files, dependency pins.
- **Entry points**: public ingress (container app URLs, hub front doors), internal services, CI/CD workflows, webhooks.
- **Credential flow**: where secrets live (SOPS files, vault refs, env files), who reads them, what they unlock. This is the blast-radius map — when something is stolen, you'll trace it along these edges.
- **Trust boundaries**: which systems talk to which across a boundary you don't control (e.g., a public JupyterHub egressing to your proxy).

### 2. Git-history secret and drift scan

Current tree state is not enough — secrets leak in history and fixes lag in deployed branches.

```bash
# Scan history for secret-shaped strings (then verify: encrypted != leaked)
git log -p --all | grep -E "(api[_-]?key|secret|password|token)=[^$.{]" | head

# SOPS/AES-encrypted values are fine IF the decryption keys are held elsewhere.
# Ciphertext that never changes across an incident window = secret never rotated.
git log --format="%h %ad %s" --date=short -- <env-file>
git show <old-commit>:<env-file> | grep <SECRET_NAME>   # compare ciphertext with HEAD
```

The **rotation check** is the highest-value git-history move in a post-incident audit: byte-identical SOPS ciphertext from before the incident to now means the secret was *not* rotated, whatever the team believes. (In the origin engagement this found the un-rotated master key — the top finding, missed by everyone.)

Also check: when was the vulnerable version pinned, when did the fix ship upstream, when did *this* repo adopt it? A six-month gap between advisory and upgrade is itself a findings-report item (process gap).

### 3. Config and IaC review

Read the deployment configs and infrastructure code as an attacker would: what must be true for each service to be reachable, and what would have to fail for protections to silently not apply?

High-yield patterns:

- **Mutable image tags** (`:latest`, `:main-<sha>` branch builds) — non-reproducible, can silently run unreviewed code, and historically how deployments stayed vulnerable after fixes shipped.
- **Config drift between environments** — prod missing a hardening control that staging/dev has (or vice versa). Diff the configs field by field.
- **Firewall "allow all services" rules** (`0.0.0.0→0.0.0.0` style) — may be dead config if the server is VNet-integrated, but verify the deployed state before assuming; also flag the code path so a future re-deploy can't re-open it.
- **Disabled-by-default protections**: rate limiting, HSTS, login restrictions. Absence is the finding — check response headers and behavior, not just config files.
- **Shared credentials across trust boundaries** — one API key in every participant's environment is one screenshot away from theft.

See `references/recon-checklist.md` for the full checklist and `references/config-drift-analysis.md` for the drift methodology.

### 4. Version-to-advisory matching

For every pinned upstream dependency, determine which advisories affect the *deployed* version. See `references/cve-osv-research.md` for details, but the core loop:

```bash
# OSV: authoritative for PyPI/npm/cargo ecosystems
curl -s -X POST https://api.osv.dev/v1/query -d \
  '{"package": {"name": "<pkg>", "ecosystem": "PyPI"}, "version": "<deployed>"}'
```

Key discipline: **an advisory with no fix available still goes in the ledger** (with an exposure assessment), and **an advisory fixed in the deployed version gets a verification note, not a pass** — "should be fixed" is confirmed in the lab or live phase, not assumed.

### 5. Triage into phases

End recon with an explicit decision, recorded in the ledger:

- **Suspected exploitable chain** → exploit lab (reproduce it, then A/B against the patch).
- **Deployed fix to verify** → live verification (and/or lab A/B).
- **Pure config/process findings** (unrotated keys, drift, missing headers) → straight to reports; they need evidence, not exploitation.

## Interlocking with other skills

- Hand suspected chains and patch-verification tasks to the **exploit-lab** skill / exploit-lab-operator agent.
- Hand live endpoint checks to the **live-verification** skill (after scope confirmation).
- Feed the ledger to **findings-reports**.

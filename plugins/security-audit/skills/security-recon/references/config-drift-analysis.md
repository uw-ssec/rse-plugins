# Config Drift Analysis

Environment drift is where "we fixed it" quietly fails: the fix lands in one environment and not another. This is the systematic diff.

## Method

### 1. Pair every environment

List all environments (dev / staging / prod / workshop / ephemeral). For each *pair* that shares a codebase (usually prod vs everything else), diff the corresponding config files field by field:

```bash
diff <(cat azure/prod/llmaven-config.yaml) <(cat azure/iss-workshop/llmaven-config.yaml)
```

YAML diffs are noisy; normalize first (strip comments, sort keys) or diff field-by-field on the keys you care about: `image`, `key_vault_secret_refs`, `general_settings`, ingress/traffic options, replicas, timeouts.

### 2. Categorize every asymmetry

For each difference, one of three labels:

- **EXPLAINED-INTENTIONAL**: e.g., prod has more replicas. Note it, move on.
- **UNEXPLAINED DRIFT**: same-purpose field differs with no documented reason → finding. Example from origin engagement: workshop env had `LITELLM_SALT_KEY` wired through Key Vault; prod did not — prod's stored credentials still derived from the master key.
- **BOTH-WRONG**: the field is missing/mutable in *both* (e.g., `image: ...:latest` in dev and workshop while prod moved to dated tags) → finding for each environment, one report.

### 3. Check the "shadow" surfaces

Drift hides in places field-diffs miss:

- **Env files**: one environment's SOPS env file may carry dead variables (services replaced months ago) — each is blast radius with no benefit.
- **Defaults**: an environment that *omits* a key inherits the upstream default. When one env sets `disable_something: true` and the other says nothing, the other is running with it enabled.
- **Job configs**: backup jobs, sidecars, and scheduled tasks drift independently of main services (different image pins, missing timeouts).
- **Infrastructure code paths**: a firewall or access flag in IaC that's conditionally applied (`if allow_azure_services:`) — check what the *deployed* state actually resolved to, and whether a state-loss recovery (see git history for "lost state" workarounds) could re-apply the wide-open variant.

### 4. Verify live where cheap

Config says what *should* be; behavior says what *is*. For header/hardening drift, one unauthenticated request settles it:

```bash
curl -sI https://<endpoint>/ | grep -iE "strict-transport|referrer-policy|x-frame"
```

Drift findings feed the ledger with severity = impact of the missing control in the environment that lacks it, and always name both environments in "files affected".

# Secret Rotation Runbook

## Safe Rotation Order

For every credential type below: **issue the new credential first, deploy it to all consumers, verify, then revoke the old one.** Never revoke first unless you have a confirmed list of consumers — surprise revocations break production and provide cover for further attacker action. The only exception: if you have direct evidence the old credential is actively in use by the attacker (e.g., outbound traffic from your CI to an unknown host), revoke immediately and accept the downtime.

## PyPI Tokens

1. Generate replacement: `https://pypi.org/manage/account/token/` → scope to single project where possible.
2. Update consumer: `gh secret set PYPI_API_TOKEN --body "<new>"`.
3. Verify with a no-op release dry-run (`twine upload --repository testpypi dist/*`).
4. Revoke old token from the same management page.
5. **Durable fix:** migrate to OIDC trusted publishing — see `supply-chain-hardened-ci-cd`. Eliminates the long-lived token entirely.

## npm Tokens

```bash
# List all tokens for the account
npm token list
# Create a replacement (publish + automation read scope)
npm token create --read-only=false --cidr=0.0.0.0/0
# Update CI
gh secret set NPM_TOKEN --body "<new>"
# Verify a publish dry-run
npm publish --dry-run
# Revoke the old token by ID
npm token revoke <old-token-id>
```

**Durable fix:** enable npm OIDC trusted publishing (`id-token: write` + `npm publish --provenance`). See `supply-chain-hardened-ci-cd`.

## GitHub Actions Secrets

```bash
# Enumerate
gh secret list
gh secret list --env <env-name>
gh secret list --org <org>

# For each compromised secret: regenerate at the source-of-truth provider, then:
gh secret set <NAME> --body "<new-value>"
gh secret set <NAME> --env <env> --body "<new-value>"

# Old values still cached in any in-progress run — cancel them
gh run list --status in_progress --json databaseId --jq '.[].databaseId' \
  | xargs -I{} gh run cancel {}
```

Workflow-level secrets (`env:` at job level) and `${{ secrets.* }}` references are equivalent in scope — rotate both.

## Signing Keys (cosign, GPG)

**Cosign keyless (Sigstore Fulcio):** no long-lived key, but if a signed artifact was produced by the bad version, treat its attestation as untrusted and re-sign from a clean rebuild. Record the bad attestation's Rekor entry UUID in the incident report for downstream consumers.

**Cosign with persistent key:**
```bash
# Revoke the cert via Rekor (record the entry, then re-sign with new key)
cosign tree <artifact>
# Generate a new key pair
cosign generate-key-pair
# Update CI
gh secret set COSIGN_PRIVATE_KEY < cosign.key
gh secret set COSIGN_PASSWORD --body "<new>"
```

**GPG:**
```bash
# Revoke the old key
gpg --gen-revoke <key-id> > revoke.asc
gpg --import revoke.asc
gpg --keyserver keys.openpgp.org --send-keys <key-id>
# Generate replacement
gpg --full-generate-key
```

## Cloud Credentials

**AWS:**
```bash
aws iam list-access-keys --user-name <user>
aws iam create-access-key --user-name <user>     # deploy this to CI
aws iam update-access-key --access-key-id <old> --status Inactive --user-name <user>
aws iam delete-access-key --access-key-id <old> --user-name <user>
```

**GCP:**
```bash
gcloud iam service-accounts keys list --iam-account=<sa>@<proj>.iam.gserviceaccount.com
gcloud iam service-accounts keys create new.json --iam-account=<sa>@<proj>.iam.gserviceaccount.com
gcloud iam service-accounts keys delete <old-key-id> --iam-account=<sa>@<proj>.iam.gserviceaccount.com
```

**Azure:**
```bash
az ad sp credential list --id <sp-app-id>
az ad sp credential reset --id <sp-app-id>       # issues a new secret
az ad sp credential delete --id <sp-app-id> --key-id <old-key-id>
```

**Durable fix for all three:** federate to GitHub OIDC. AWS via `configure-aws-credentials` with `role-to-assume`, GCP via `google-github-actions/auth` with Workload Identity Federation, Azure via `azure/login` with `client-id` + `tenant-id`. No long-lived secrets in `gh secret list`.

## Durable Fix: OIDC Trusted Publishing

OIDC eliminates long-lived secrets entirely — each workflow run issues a short-lived token cryptographically bound to the run's identity (repo + workflow + ref). Every rotation here is an opportunity to migrate the consumer to OIDC instead. The next "rotate the PyPI token" task should become "delete the PyPI token, set up trusted publishing." Cross-link to `supply-chain-hardened-ci-cd` for the full migration playbook for PyPI, npm, AWS, GCP, and Azure.

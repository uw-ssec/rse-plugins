# Sigstore Cookbook

## What Sigstore Provides

Sigstore is keyless signing for software artifacts. The signer authenticates via OIDC (GitHub Actions, Google, Microsoft, etc.); Fulcio issues a short-lived X.509 cert (~10 min validity) bound to that OIDC identity; cosign signs the artifact with that cert; the signature and cert are logged to Rekor, a public append-only transparency log. There are no long-lived signing keys to rotate, leak, or revoke — the identity proof lives in the transparency log entry.

## Sign an Artifact in CI

```yaml
# .github/workflows/release.yml
permissions:
  id-token: write      # required: lets the job request an OIDC token from GitHub
  contents: write      # required: lets the job upload to the release
jobs:
  sign:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha>
      - uses: sigstore/cosign-installer@<sha>
        with:
          cosign-release: 'v2.4.1'
      - name: Sign artifact
        run: |
          cosign sign-blob \
            --yes \
            --bundle artifact.sigstore \
            artifact.tar.gz
```

`--yes` skips the interactive "are you sure" prompt — required in non-interactive CI. The `--bundle` flag writes a self-contained signature bundle (cert + signature + Rekor entry) to one file, which is what verifiers consume.

## Verify a Downstream Artifact

```bash
cosign verify-blob \
  --bundle artifact.sigstore \
  --certificate-identity-regexp "https://github.com/sigstore/cosign/.github/workflows/release.yml@refs/tags/v.+" \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  artifact.tar.gz
```

The GitHub Actions OIDC issuer is always `https://token.actions.githubusercontent.com`. The `--certificate-identity-regexp` pins which repo, workflow file, and ref produced the signature — never use a bare `--certificate-identity` that omits the workflow path, or a regex broad enough to match a different repo.

Worked example — verify a release of cosign itself:

```bash
curl -LO https://github.com/sigstore/cosign/releases/download/v2.4.1/cosign-linux-amd64
curl -LO https://github.com/sigstore/cosign/releases/download/v2.4.1/cosign-linux-amd64-keyless.sig
curl -LO https://github.com/sigstore/cosign/releases/download/v2.4.1/cosign-linux-amd64-keyless.pem
cosign verify-blob \
  --certificate cosign-linux-amd64-keyless.pem \
  --signature cosign-linux-amd64-keyless.sig \
  --certificate-identity-regexp "https://github.com/sigstore/cosign/.github/workflows/release.yaml@refs/tags/v.+" \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  cosign-linux-amd64
```

## Transparency Log Lookup

Every Sigstore signature is publicly logged to Rekor. Anyone can audit:

```bash
# Show the Rekor log entry attached to a signed OCI artifact
cosign tree ghcr.io/<owner>/<image>:<tag>

# Search Rekor by artifact hash
rekor-cli search --artifact <sha256-of-artifact>

# Fetch a specific log entry
rekor-cli get --uuid <entry-uuid>
```

If a maintainer's identity was compromised, the malicious signature still shows up in Rekor — bound to the attacker's OIDC identity, signed at a timestamp out of band with normal releases. The log itself is the audit trail.

## Common Failure Modes

- **Missing `id-token: write` permission** — `cosign sign-blob` fails with "no OIDC token". Add it to the job's `permissions:` block (not just at the workflow level if jobs override).
- **Clock skew on the runner** — Fulcio rejects certs whose `notBefore` is in the future. Self-hosted runners with bad NTP fail intermittently. Fix: run `timedatectl status` or `chronyc tracking` on the runner.
- **Wrong `--certificate-identity-regexp`** — `cosign verify-blob` reports "no matching signatures". The regex must match the exact workflow file path and ref pattern in the signing cert. Inspect the cert with `cosign verify-blob --insecure-ignore-tlog ... --output-file -` or `openssl x509 -in cert.pem -text` to read the SAN URI.
- **Expired short-lived cert + offline verification** — Fulcio certs expire ~10 minutes after issue. Verification uses the Rekor log entry's `integratedTime` to bind the signature to a moment the cert was valid, so online verification still works years later. But fully air-gapped verification fails unless you cached the Rekor entry at sign time (use the `--bundle` flag, which embeds it).
- **Forgot to upload the `.sigstore` bundle** — release page has the artifact but no signature. Add the `gh release upload` step or use `actions/attest-build-provenance` which writes to the GitHub attestation API automatically.

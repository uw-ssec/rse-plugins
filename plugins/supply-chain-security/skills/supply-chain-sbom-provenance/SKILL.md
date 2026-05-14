---
name: supply-chain-sbom-provenance
description: SBOM generation and provenance verification for research software releases. Use when reviewing or writing release workflows that publish to PyPI, npm, GHCR, or similar registries; when verifying a downstream artifact's signatures or attestations; or when evaluating SLSA level for a release pipeline. Covers CycloneDX/SPDX SBOM generation with syft, Sigstore keyless signing with cosign, npm provenance, and SLSA build levels.
metadata:
  references:
    - references/sigstore-cookbook.md
    - references/slsa-levels.md
  assets:
    - assets/sbom-workflow.yml
---

# Supply Chain SBOM and Provenance

## Threat Model

SBOM and provenance catch tag-hijack and maintainer account-takeover: the artifact digest stops matching the signed attestation even when CVE scanners report clean. CVE scanners cannot detect these attacks; only cryptographic attestations tied to the build pipeline can.

## Decision Matrix

| Registry | Mechanism | Key management | SLSA level | Complexity |
|----------|-----------|----------------|-----------|-----------|
| PyPI | OIDC trusted publishing + Sigstore | Keyless via GitHub OIDC | L2-L3 | Low |
| npm | npm provenance (`--provenance`) | Keyless via GitHub OIDC | L2 | Low |
| GHCR | `actions/attest-build-provenance` | Keyless via GitHub OIDC | L2-L3 | Low |
| Docker Hub | cosign keyless | Sigstore (Fulcio short-lived cert) | L2 | Medium |
| Self-hosted (no OIDC) | cosign with hardware key | KMS or YubiKey | L3 if hermetic | High |

Pick the lowest-complexity row for your registry. PyPI/npm/GHCR default to GitHub-OIDC keyless — no secrets to rotate.

## Generation Workflow

Run these steps in order in the release job. Each is independently runnable for local debugging.

### Step 1 — Build artifact and capture its digest

```bash
# Build whatever artifact the project ships (wheel, tarball, container)
python -m build                            # → dist/*.whl, dist/*.tar.gz
sha256sum dist/* > dist/SHA256SUMS         # record digests for the attestation
```

### Step 2 — Generate CycloneDX SBOM with syft

```bash
# Scan the built directory (works for source trees, dirs, OCI images)
syft dir:. -o cyclonedx-json=sbom.cdx.json

# Or scan an already-built artifact
syft dist/myproject-1.0.0.tar.gz -o cyclonedx-json=dist/sbom.cdx.json
```

### Step 3 — Sign artifact and SBOM with Sigstore keyless

In CI, prefer the GitHub-native attestation action (writes to the public attestation API):

```yaml
permissions:
  id-token: write      # required for OIDC
  attestations: write  # required for attest-build-provenance
- uses: actions/attest-build-provenance@<sha>  # v3.0.0
  with:
    subject-path: 'dist/*'
```

Or sign each artifact directly with cosign keyless (works for any registry):

```bash
cosign sign-blob --yes --bundle artifact.sigstore artifact.tar.gz
```

See `references/sigstore-cookbook.md` for `permissions:` block and failure modes.

### Step 4 — Attach SBOM and signatures to the release

```bash
gh release upload "${GITHUB_REF_NAME}" \
  dist/sbom.cdx.json \
  dist/*.sigstore \
  dist/SHA256SUMS
```

Drop-in workflow that wires all four steps together: `assets/sbom-workflow.yml`. For a one-shot SBOM-only scan from any source tree: `syft dir:. -o cyclonedx-json=sbom.cdx.json`.

## Verification Checklist

Run each item below downstream or in the project's pre-release smoke test.

- [ ] Bundle present. Check: `gh attestation list <artifact>` or release page for `*.sigstore`.
- [ ] Signature verifies:
  ```bash
  cosign verify-blob \
    --bundle artifact.sigstore \
    --certificate-identity-regexp "https://github.com/<owner>/<repo>/.github/workflows/.+" \
    --certificate-oidc-issuer https://token.actions.githubusercontent.com \
    artifact.tar.gz
  ```
- [ ] SBOM digest matches. Check: `sha256sum artifact.tar.gz` appears in `sbom.cdx.json` (`metadata.component.hashes`) or `SHA256SUMS`.
- [ ] `certificate-identity` is the expected repo + workflow path (not a fork, not a different workflow).
- [ ] Rekor log timestamp falls in the expected release window. Check: `cosign tree <artifact>`.

If any item fails, treat as unverified — do not install.

## Quick Recipes

Complementary recipes for scenarios beyond the standard release pipeline above.

**npm publish with provenance (alternative to syft+cosign for npm packages):**
```bash
npm publish --provenance --access public
```
Requires `permissions: id-token: write` in the publish job and an OIDC-enabled npm account.

**Verify a GitHub attestation (consumer side, no Sigstore tooling needed):**
```bash
gh attestation verify artifact.tar.gz --owner <owner>
```
Uses the `gh` CLI to verify build-provenance attestations published via `actions/attest-build-provenance`. Faster than `cosign verify-blob` when the artifact is from a GitHub-hosted repo.

**Generate an SBOM from a built container image (instead of source tree):**
```bash
syft <registry>/<image>:<tag> -o spdx-json=sbom.spdx.json
```
Use this when shipping container images to GHCR or Docker Hub. Format is SPDX (alternative to CycloneDX); both are accepted by GitHub's attestation infrastructure.

## Output: Provenance Posture Report

When invoked for a release-pipeline review, produce a Markdown report with the structure below. Every PASS/WARN/FAIL must cite a `file:line` from the workflows or "absent" if the control is missing entirely.

```markdown
## Provenance Posture: <project>

### Generation Posture
| Criterion | PASS/WARN/FAIL | Evidence |
|-----------|----------------|----------|
| SBOM generated for releases | ... | <workflow file:line or "absent"> |
| SBOM format (CycloneDX/SPDX) | ... | <format detected> |
| Sigstore signing in release workflow | ... | <workflow file:line> |
| npm provenance enabled (npm projects) | ... | <evidence or N/A> |
| SLSA level achieved | ... | <level + reasoning, see references/slsa-levels.md> |

### Verification Posture
| Criterion | PASS/WARN/FAIL | Evidence |
|-----------|----------------|----------|
| Downstream verification documented | ... | <README/docs reference> |
| Attestation references build pipeline | ... | <evidence> |

### Top 3 Priority Actions
1. <highest-impact upgrade> — apply `assets/sbom-workflow.yml` or follow `references/sigstore-cookbook.md`
2. <second priority>
3. <third priority>
```

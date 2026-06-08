---
name: container-security
description: Use when the user asks about container image vulnerabilities, scanning Docker images, generating SBOMs, signing images with cosign, hardening container images, or adding security checks in CI/CD. Performs scan -> triage -> remediate/suppress -> re-scan -> sign -> verify workflow using Trivy/Grype/syft/cosign.
metadata:
  references:
    - references/image-scanning.md
    - references/hardening-guide.md
    - references/supply-chain-security.md
    - references/security-operations.md
  assets:
    - assets/trivy-config.yaml
    - assets/security-scan-workflow.yml
---

# Container Security

## Use When

- The user needs to scan container images for vulnerabilities before release/deploy.
- The user asks to harden Dockerfiles or runtime container settings.
- The user needs SBOM generation, image signing, or signature verification.
- The user wants CI/CD security gates for container builds.

## Primary Actions

- Run vulnerability scans with Trivy or Grype.
- Triage findings and decide fix vs documented suppression.
- Harden image build/runtime configuration (non-root, minimal base, reduced privileges).
- Generate SBOMs with syft and sign images with cosign.
- Add CI gates and post-fix re-scan checks.

## End-to-End Workflow With Validation Gates

1. **Scan** image (`trivy image` or `grype`).
2. **Triage** by severity and fix availability.
3. **Remediate or suppress** with documented rationale.
4. **Re-scan** and confirm policy threshold (for example no CRITICAL/HIGH).
5. **Generate SBOM** and attach/store artifact.
6. **Sign image** with cosign.
7. **Verify signature** and publish.

If any gate fails, return to step 2 before shipping.

## Quick Commands

```bash
# Scan and fail on high/critical
trivy image --severity HIGH,CRITICAL --exit-code 1 myapp:latest
grype myapp:latest --fail-on high

# SBOM
syft myapp:latest -o spdx-json > sbom.spdx.json

# Sign + verify
cosign sign myregistry/myapp:latest
cosign verify myregistry/myapp:latest
```

## Keep SKILL.md Lean; Use Deep References

- Scanning flags, output formats, CI patterns:
  [references/image-scanning.md](references/image-scanning.md)
- Hardening details and Dockerfile/runtime patterns:
  [references/hardening-guide.md](references/hardening-guide.md)
- SBOM/signing/provenance deep dive:
  [references/supply-chain-security.md](references/supply-chain-security.md)
- Validation gates, suppression policy, and failure recovery:
  [references/security-operations.md](references/security-operations.md)

## Ready-to-Use Assets

- [assets/trivy-config.yaml](assets/trivy-config.yaml)
- [assets/security-scan-workflow.yml](assets/security-scan-workflow.yml)

---
name: container-security
description: Container security scanning with Trivy and Grype, image hardening, supply chain security with SBOM generation, signing with cosign, and CI integration for automated vulnerability detection.
metadata:
  references:
    - references/image-scanning.md
    - references/hardening-guide.md
    - references/supply-chain-security.md
  assets:
    - assets/trivy-config.yaml
    - assets/security-scan-workflow.yml
---

# Container Security

Secure your container images from build to deploy. This skill covers vulnerability scanning with industry-standard tools like Trivy and Grype, hardening containers to minimize attack surface, and establishing supply chain security through SBOM generation and image signing. Whether you are shipping research software, deploying services, or publishing container images for community use, these practices help you catch known vulnerabilities early, enforce security baselines, and provide verifiable provenance for your artifacts.

**Key Tools:**
- **Trivy**: Comprehensive vulnerability scanner for containers, filesystems, and IaC
- **Grype**: Fast vulnerability scanner focused on container images and SBOMs
- **cosign**: Container image signing and verification from the Sigstore project
- **syft**: SBOM generator for container images and filesystems

## Resources in This Skill

| Resource | Description |
|----------|-------------|
| [references/image-scanning.md](references/image-scanning.md) | Deep reference for Trivy, Grype, scan types, severity levels, and CI integration |
| [references/hardening-guide.md](references/hardening-guide.md) | Deep reference for non-root users, minimal bases, capabilities, seccomp, and secrets |
| [references/supply-chain-security.md](references/supply-chain-security.md) | Deep reference for SBOM generation, cosign signing, SLSA provenance, and verification |
| [assets/trivy-config.yaml](assets/trivy-config.yaml) | Ready-to-use Trivy configuration file with recommended defaults |
| [assets/security-scan-workflow.yml](assets/security-scan-workflow.yml) | GitHub Actions workflow for PR scanning, SARIF upload, and nightly scans |

## Quick Reference Card

### Scanner Comparison

| Feature | Trivy | Grype | Snyk | Docker Scout |
|---------|-------|-------|------|--------------|
| **License** | Apache-2.0 | Apache-2.0 | Proprietary | Proprietary |
| **OS Packages** | Yes | Yes | Yes | Yes |
| **Language Deps** | Yes | Yes | Yes | Yes |
| **IaC Scanning** | Yes | No | Yes | No |
| **SBOM Input** | Yes | Yes | Yes | No |
| **Config Scanning** | Yes | No | Yes | No |
| **CI Integration** | Excellent | Good | Excellent | Good |
| **Offline Mode** | Yes | Yes | No | No |
| **Speed** | Fast | Fast | Moderate | Fast |
| **SARIF Output** | Yes | Yes | Yes | Yes |

### Severity Levels

| Level | CVSS Score | Action |
|-------|-----------|--------|
| CRITICAL | 9.0–10.0 | Fix immediately, block deployments |
| HIGH | 7.0–8.9 | Fix before next release |
| MEDIUM | 4.0–6.9 | Plan remediation |
| LOW | 0.1–3.9 | Track, fix opportunistically |
| UNKNOWN | N/A | Investigate, treat as MEDIUM |

### Quick Commands

```bash
# Trivy: scan a container image
trivy image myapp:latest

# Trivy: scan and fail on CRITICAL/HIGH
trivy image --severity CRITICAL,HIGH --exit-code 1 myapp:latest

# Trivy: scan a Dockerfile for misconfigurations
trivy config Dockerfile

# Grype: scan a container image
grype myapp:latest

# Grype: fail on high severity or above
grype myapp:latest --fail-on high

# Generate SBOM with syft
syft myapp:latest -o spdx-json > sbom.spdx.json

# Sign an image with cosign (keyless)
cosign sign myregistry/myapp:latest

# Verify a signed image
cosign verify myregistry/myapp:latest
```

## When to Use This Skill

Use this skill when you need to secure container images and container-based workflows:

- Building container images for research software or services and need to scan for known vulnerabilities
- Hardening containers before deploying to production or shared infrastructure
- Establishing supply chain security with SBOMs and image signing for published artifacts
- Integrating automated security scanning into CI/CD pipelines
- Preparing for compliance requirements that mandate vulnerability reporting
- Evaluating and choosing between vulnerability scanning tools
- Responding to a reported CVE that may affect your container images
- Setting up nightly scans to catch newly disclosed vulnerabilities

## Image Scanning Basics

Container images can contain vulnerabilities in OS packages, language-specific dependencies, and configuration files. Scanners compare the contents of your image against vulnerability databases (NVD, GitHub Advisory Database, OS vendor databases) to identify known issues.

**Three types of scanning:**

**Image scan** analyzes a built container image by inspecting its layers for installed packages and matching them against vulnerability databases. This is the most common scan type and catches vulnerabilities in both OS packages and application dependencies.

```bash
# Scan a local or remote image
trivy image python:3.12-slim
grype python:3.12-slim
```

**Filesystem scan** analyzes a local directory, which is useful for scanning your project before building an image. This catches vulnerabilities in lock files and dependency manifests.

```bash
# Scan a project directory
trivy fs --scanners vuln .
grype dir:.
```

**Configuration scan** checks Dockerfiles, Kubernetes manifests, and other IaC files for misconfigurations such as running as root, using `latest` tags, or copying secrets.

```bash
# Scan Dockerfile for misconfigurations
trivy config Dockerfile
trivy config k8s/
```

## Trivy Setup and Usage

Trivy is a comprehensive scanner maintained by Aqua Security that covers vulnerabilities, misconfigurations, and secrets.

**Installation:**
```bash
# macOS
brew install trivy

# Linux (Debian/Ubuntu)
sudo apt-get install -y wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/trivy.list
sudo apt-get update && sudo apt-get install -y trivy

# Docker (no installation needed)
docker run aquasec/trivy image myapp:latest
```

**Common usage patterns:**
```bash
# Full scan with all scanners
trivy image --scanners vuln,misconfig,secret myapp:latest

# Output as JSON for programmatic processing
trivy image --format json --output results.json myapp:latest

# Output as SARIF for GitHub Security tab
trivy image --format sarif --output trivy-results.sarif myapp:latest

# Ignore unfixed vulnerabilities
trivy image --ignore-unfixed myapp:latest

# Use a configuration file
trivy image --config trivy.yaml myapp:latest
```

See [assets/trivy-config.yaml](assets/trivy-config.yaml) for a ready-to-use configuration file.

## Grype Setup and Usage

Grype is a fast, focused vulnerability scanner from Anchore that pairs well with the syft SBOM generator.

**Installation:**
```bash
# macOS
brew install grype

# Linux (install script)
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin

# Docker
docker run anchore/grype myapp:latest
```

**Common usage patterns:**
```bash
# Scan an image
grype myapp:latest

# Output as JSON
grype myapp:latest -o json > grype-results.json

# Fail on specific severity
grype myapp:latest --fail-on critical

# Scan from an SBOM
syft myapp:latest -o spdx-json > sbom.json
grype sbom:sbom.json

# Only show fixed vulnerabilities (actionable)
grype myapp:latest --only-fixed
```

## Interpreting Scan Results

When you run a scan, you will see a table of vulnerabilities. Understanding what to act on is critical.

**Key fields in scan results:**
- **CVE ID**: The unique identifier for the vulnerability (e.g., CVE-2024-1234)
- **Severity**: CRITICAL, HIGH, MEDIUM, LOW based on CVSS score
- **Package**: The affected package name and installed version
- **Fixed Version**: The version that resolves the vulnerability (if available)
- **Description**: Brief summary of the vulnerability

**Prioritization strategy:**

1. Fix CRITICAL vulnerabilities with available fixes immediately
2. Fix HIGH vulnerabilities with available fixes before releasing
3. For unfixed vulnerabilities, evaluate whether the affected code path is reachable in your application
4. Suppress known false positives or accepted risks using ignore files

**Suppressing known issues:**

Create a `.trivyignore` file to suppress accepted risks:
```
# Accepted risk: not exploitable in our context
CVE-2024-1234

# Waiting for upstream fix, tracked in ISSUE-567
CVE-2024-5678
```

For Grype, use a `.grype.yaml` configuration:
```yaml
ignore:
  - vulnerability: CVE-2024-1234
    reason: "Not exploitable in our usage"
```

## Hardening Checklist

Apply these hardening measures to reduce the attack surface of your container images:

**1. Run as non-root user:**
```dockerfile
RUN useradd --create-home --shell /bin/bash appuser
USER appuser
```

**2. Use a minimal base image:**
```dockerfile
# Prefer distroless or scratch
FROM gcr.io/distroless/python3-debian12
# Or Chainguard images
FROM cgr.dev/chainguard/python:latest
```

**3. Enable read-only root filesystem:**
```bash
docker run --read-only --tmpfs /tmp myapp:latest
```

**4. Drop all capabilities:**
```bash
docker run --cap-drop ALL myapp:latest
# Add back only what is needed
docker run --cap-drop ALL --cap-add NET_BIND_SERVICE myapp:latest
```

**5. No shell in production images:**
```dockerfile
# Use distroless or multi-stage builds that exclude shell
FROM scratch
COPY --from=builder /app /app
ENTRYPOINT ["/app"]
```

**6. Never COPY secrets into the image:**
```dockerfile
# WRONG: secrets baked into image layer
COPY credentials.json /app/credentials.json

# RIGHT: use build secrets (not persisted in layers)
RUN --mount=type=secret,id=credentials cat /run/secrets/credentials
```

See [references/hardening-guide.md](references/hardening-guide.md) for the complete hardening reference.

## Supply Chain Security

Supply chain security ensures that your container images are trustworthy and verifiable from source to deployment.

**SBOM Generation:**

A Software Bill of Materials (SBOM) lists every component in your image, making it possible to check for vulnerabilities after deployment.

```bash
# Generate SBOM with syft
syft myapp:latest -o spdx-json > sbom.spdx.json
syft myapp:latest -o cyclonedx-json > sbom.cdx.json

# Generate SBOM with trivy
trivy image --format spdx-json --output sbom.spdx.json myapp:latest
```

**Image Signing with cosign:**

Sign images so consumers can verify they came from you and have not been tampered with.

```bash
# Keyless signing (uses OIDC identity, recommended)
cosign sign myregistry/myapp@sha256:abc123...

# Key-based signing
cosign generate-key-pair
cosign sign --key cosign.key myregistry/myapp@sha256:abc123...

# Verification
cosign verify myregistry/myapp:latest
```

**Dependency Pinning:**

Pin base images by digest to ensure reproducible builds:
```dockerfile
# Instead of a mutable tag
FROM python:3.12-slim@sha256:abc123def456...
```

See [references/supply-chain-security.md](references/supply-chain-security.md) for the complete supply chain security reference.

## CI Integration

Automate security scanning in your CI/CD pipeline to catch vulnerabilities before they reach production.

**Scan on pull request:** Run Trivy or Grype on every PR that modifies the Dockerfile or dependencies. Fail the check if CRITICAL vulnerabilities are found.

**Upload results to GitHub Security tab:** Use SARIF output to surface vulnerabilities in the GitHub Security tab alongside code scanning alerts.

**Nightly scans:** Schedule scans to catch newly disclosed vulnerabilities in existing images.

**Block on critical:** Configure your pipeline to fail when CRITICAL severity issues are detected, preventing deployment of known-vulnerable images.

See [assets/security-scan-workflow.yml](assets/security-scan-workflow.yml) for a ready-to-use GitHub Actions workflow.

## Common Mistakes

- **Scanning only at build time**: New CVEs are disclosed daily. Run nightly scans on deployed images, not just at build time.
- **Ignoring unfixed vulnerabilities**: Even without a patch, you may be able to mitigate by switching base images or removing the affected package.
- **Using `latest` tags for base images**: Tags are mutable. Pin base images by digest for reproducible, auditable builds.
- **Running as root**: Most applications do not need root. Default to a non-root user and only escalate if absolutely necessary.
- **Suppressing without documenting**: Every suppressed CVE should have a reason and a tracking issue for follow-up.
- **Scanning only the final image**: Multi-stage builds can leak vulnerabilities through builder stages. Scan intermediate stages too.
- **Skipping config scanning**: Dockerfile misconfigurations (running as root, COPY secrets) are just as dangerous as package vulnerabilities.

## Best Practices

### Scanning
- Scan images in CI on every PR and on a nightly schedule
- Use SARIF output to integrate with GitHub Security tab
- Block merges on CRITICAL vulnerabilities
- Scan both OS packages and language-specific dependencies
- Keep scanner databases updated (Trivy and Grype update automatically)

### Hardening
- Always run as a non-root user
- Use minimal base images (distroless, scratch, Chainguard)
- Drop all Linux capabilities and add back only what is required
- Enable read-only root filesystem with tmpfs for writable paths
- Never bake secrets into image layers

### Supply Chain
- Generate SBOMs for every released image
- Sign images with cosign before pushing to a registry
- Pin base images by digest, not tag
- Verify signatures before deploying images
- Store SBOMs alongside images in your registry

### CI/CD
- Fail pipelines on CRITICAL and HIGH severity findings
- Upload SARIF results to GitHub Security for centralized tracking
- Run nightly scans to catch newly disclosed CVEs
- Cache vulnerability databases to speed up CI scans
- Include security scanning in your definition of done

## Resources

### Official Documentation
- **Trivy**: https://aquasecurity.github.io/trivy/
- **Grype**: https://github.com/anchore/grype
- **cosign**: https://docs.sigstore.dev/cosign/overview/
- **syft**: https://github.com/anchore/syft
- **Sigstore**: https://www.sigstore.dev/

### Vulnerability Databases
- **NVD (National Vulnerability Database)**: https://nvd.nist.gov/
- **GitHub Advisory Database**: https://github.com/advisories
- **OSV (Open Source Vulnerabilities)**: https://osv.dev/

### Standards and Frameworks
- **SLSA (Supply-chain Levels for Software Artifacts)**: https://slsa.dev/
- **SPDX (Software Package Data Exchange)**: https://spdx.dev/
- **CycloneDX**: https://cyclonedx.org/
- **CIS Docker Benchmark**: https://www.cisecurity.org/benchmark/docker

### Container Base Images
- **Chainguard Images**: https://www.chainguard.dev/chainguard-images
- **Google Distroless**: https://github.com/GoogleContainerTools/distroless
- **Docker Official Images**: https://hub.docker.com/search?q=&image_filter=official

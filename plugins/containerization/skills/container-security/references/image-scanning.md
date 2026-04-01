# Image Scanning — Deep Reference

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| Trivy CLI Reference | 15–65 | Installation, core commands, and output format options for Trivy |
| Grype CLI Reference | 66–112 | Installation, core commands, and output format options for Grype |
| Scan Types | 113–168 | Image, filesystem, config, repository, and SBOM scan modes |
| Severity Levels and CVSS Scores | 169–207 | How severity is assigned, CVSS v3 scoring, and prioritization |
| .trivyignore and Suppression Policies | 208–262 | Suppressing false positives and accepted risks in Trivy and Grype |
| False Positive Management | 263–310 | Identifying, documenting, and managing false positives across tools |
| Scanning in CI | 311–389 | GitHub Actions integration for Trivy and Grype with SARIF upload |
| Scanner Comparison | 390–432 | Feature matrix comparing Trivy, Grype, Snyk, and Docker Scout |

---

## Trivy CLI Reference

### Installation

```bash
# macOS (Homebrew)
brew install trivy

# Linux (Debian/Ubuntu)
sudo apt-get install -y wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | \
  sudo tee /etc/apt/sources.list.d/trivy.list
sudo apt-get update && sudo apt-get install -y trivy

# Docker (no installation required)
docker run --rm aquasec/trivy image myapp:latest

# Binary release (Linux/macOS)
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
```

### Core Commands

```bash
# Scan a container image for vulnerabilities
trivy image myapp:latest

# Scan with specific severity threshold
trivy image --severity CRITICAL,HIGH myapp:latest

# Scan and exit with code 1 if vulnerabilities found (for CI)
trivy image --exit-code 1 --severity CRITICAL myapp:latest

# Scan only for vulnerabilities (skip misconfig, secret)
trivy image --scanners vuln myapp:latest

# Scan for vulnerabilities and misconfigurations
trivy image --scanners vuln,misconfig myapp:latest

# Scan a local filesystem / project directory
trivy fs --scanners vuln .

# Scan a Dockerfile or Kubernetes manifest for misconfigurations
trivy config Dockerfile
trivy config k8s/deployment.yaml

# Scan a git repository (remote)
trivy repo https://github.com/org/repo

# Generate SBOM from an image
trivy image --format spdx-json --output sbom.spdx.json myapp:latest
```

### Output Formats

```bash
# Table (default, human-readable)
trivy image myapp:latest

# JSON (programmatic processing)
trivy image --format json --output results.json myapp:latest

# SARIF (GitHub Security tab integration)
trivy image --format sarif --output trivy.sarif myapp:latest

# Template-based output (custom formats)
trivy image --format template --template "@contrib/html.tpl" --output report.html myapp:latest

# CycloneDX SBOM format
trivy image --format cyclonedx --output sbom.cdx.json myapp:latest
```

## Grype CLI Reference

### Installation

```bash
# macOS (Homebrew)
brew install grype

# Linux (install script)
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin

# Docker (no installation required)
docker run --rm anchore/grype myapp:latest

# Verify installation
grype version
```

### Core Commands

```bash
# Scan a container image
grype myapp:latest

# Scan and fail on a severity threshold
grype myapp:latest --fail-on critical
grype myapp:latest --fail-on high

# Scan a local directory
grype dir:.
grype dir:/path/to/project

# Scan an SBOM file
grype sbom:sbom.spdx.json
grype sbom:sbom.cdx.json

# Show only vulnerabilities with available fixes
grype myapp:latest --only-fixed

# Show only specific severity levels
grype myapp:latest --only-notfixed
```

### Output Formats

```bash
# Table (default, human-readable)
grype myapp:latest

# JSON (programmatic processing)
grype myapp:latest -o json > grype-results.json

# CycloneDX (for integration with other tools)
grype myapp:latest -o cyclonedx-json > grype-results.cdx.json

# SARIF (GitHub Security tab integration)
grype myapp:latest -o sarif > grype.sarif

# Template-based output
grype myapp:latest -o template -t /path/to/template.tmpl
```

### Database Management

```bash
# Update vulnerability database manually
grype db update

# Check database status
grype db status

# Use a specific database
grype db import /path/to/vulnerability.db
```

## Scan Types

### Image Scan

Analyzes a built container image by inspecting its layers. This is the most common scan type. Trivy and Grype both extract the image filesystem and check installed OS packages (apk, apt, yum) and language-specific dependencies (pip, npm, gem, go modules) against vulnerability databases.

```bash
# Scan a local image
trivy image myapp:latest
grype myapp:latest

# Scan a remote image (pulled from registry)
trivy image ghcr.io/org/myapp:v1.2.3
grype ghcr.io/org/myapp:v1.2.3

# Scan a tarball
trivy image --input myapp.tar
grype docker-archive:myapp.tar
```

### Filesystem Scan

Scans a local directory for vulnerabilities in dependency manifests and lock files. Useful for scanning before building an image.

```bash
# Trivy filesystem scan
trivy fs --scanners vuln /path/to/project
trivy fs --scanners vuln,secret .

# Grype directory scan
grype dir:.
grype dir:/path/to/project
```

**Supported manifests:** `requirements.txt`, `Pipfile.lock`, `poetry.lock`, `package-lock.json`, `go.sum`, `Gemfile.lock`, `Cargo.lock`, and many more.

### Config Scan

Checks Dockerfiles, Kubernetes manifests, Terraform files, and other IaC for misconfigurations. Only Trivy supports this mode natively.

```bash
# Scan a Dockerfile
trivy config Dockerfile

# Scan Kubernetes manifests
trivy config k8s/

# Scan Terraform files
trivy config terraform/
```

**Common misconfigurations detected:**
- Running as root user
- Using `latest` tag for base images
- Exposing unnecessary ports
- Missing health checks
- Using ADD instead of COPY
- Secrets in environment variables

### Repository Scan

Scan a remote git repository without cloning it locally.

```bash
trivy repo https://github.com/org/repo
trivy repo --branch develop https://github.com/org/repo
```

### SBOM Scan

Scan an existing SBOM file for vulnerabilities. This decouples SBOM generation from vulnerability matching.

```bash
# Generate SBOM first
syft myapp:latest -o spdx-json > sbom.spdx.json

# Scan the SBOM
trivy sbom sbom.spdx.json
grype sbom:sbom.spdx.json
```

## Severity Levels and CVSS Scores

### CVSS v3 Score Ranges

The Common Vulnerability Scoring System (CVSS) provides a numerical score from 0.0 to 10.0 that reflects the severity of a vulnerability. Scanners map these scores to severity labels.

| Severity | CVSS v3 Range | Meaning |
|----------|--------------|---------|
| CRITICAL | 9.0–10.0 | Easily exploitable, severe impact, often remotely exploitable without authentication |
| HIGH | 7.0–8.9 | Significant impact, may require some conditions to exploit |
| MEDIUM | 4.0–6.9 | Moderate impact, typically requires local access or specific conditions |
| LOW | 0.1–3.9 | Minor impact, difficult to exploit |
| NONE | 0.0 | Informational, no security impact |
| UNKNOWN | N/A | No CVSS score assigned yet; treat as MEDIUM until assessed |

### Prioritization Guidelines

**Fix immediately (block deployments):**
- CRITICAL severity with a fix available
- Any severity if actively exploited in the wild (check CISA KEV catalog)

**Fix before next release:**
- HIGH severity with a fix available
- CRITICAL severity without a fix (evaluate workarounds)

**Plan remediation:**
- MEDIUM severity with a fix available
- HIGH severity without a fix

**Track and review:**
- LOW severity
- Vulnerabilities in packages not in your execution path

### CVSS Vector Components

A CVSS vector string like `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` breaks down as:
- **AV** (Attack Vector): Network, Adjacent, Local, Physical
- **AC** (Attack Complexity): Low, High
- **PR** (Privileges Required): None, Low, High
- **UI** (User Interaction): None, Required
- **S** (Scope): Unchanged, Changed
- **C/I/A** (Confidentiality/Integrity/Availability Impact): None, Low, High

## .trivyignore and Suppression Policies

### Trivy: .trivyignore

Create a `.trivyignore` file in your project root to suppress specific vulnerabilities.

**Basic format:**
```
# Comment explaining why this CVE is suppressed
CVE-2024-1234

# Another suppressed CVE with tracking reference
# Tracked in: https://github.com/org/repo/issues/567
CVE-2024-5678
```

**Expiration-based suppression (Trivy 0.49+):**
```yaml
# .trivyignore.yaml (YAML format with expiration)
vulnerabilities:
  - id: CVE-2024-1234
    reason: "Not exploitable in our context, re-evaluate in 90 days"
    expires: 2025-06-01
  - id: CVE-2024-5678
    reason: "Waiting for upstream fix"
    expires: 2025-04-15
    paths:
      - "usr/lib/libexample.so"
```

**Using .trivyignore in commands:**
```bash
# Default: reads .trivyignore from current directory
trivy image myapp:latest

# Specify a custom ignore file
trivy image --ignorefile custom-ignores.txt myapp:latest

# Ignore unfixed vulnerabilities entirely
trivy image --ignore-unfixed myapp:latest
```

### Grype: Suppression via Configuration

Grype uses a `.grype.yaml` configuration file for suppressions:

```yaml
ignore:
  - vulnerability: CVE-2024-1234
  - vulnerability: CVE-2024-5678
    package:
      name: libexample
      type: deb
    reason: "Not exploitable in our context"
```

**Using Grype ignore rules:**
```bash
# Grype reads .grype.yaml from current directory automatically
grype myapp:latest

# Specify a custom config
grype myapp:latest --config /path/to/.grype.yaml
```

### Suppression Policy Guidelines

- Every suppressed vulnerability MUST have a documented reason
- Set expiration dates on suppressions (90 days maximum)
- Track suppressed CVEs in your issue tracker
- Review suppressions quarterly
- Never suppress an entire severity level; suppress individual CVEs

## False Positive Management

### Identifying False Positives

A false positive occurs when a scanner reports a vulnerability that does not actually affect your application. Common causes:

**Package name collisions:** A vulnerability in a package with the same name but different ecosystem (e.g., a Ruby gem vs a Python package both named `json`).

**Patched but unreported:** Your OS vendor has backported a fix but the scanner database has not yet recorded it.

**Not in execution path:** The vulnerable code exists in the image but is never called by your application.

**Version detection errors:** The scanner misidentifies the installed version of a package.

### Verification Steps

1. **Check the CVE details:** Read the CVE description on NVD or the vendor advisory to understand the vulnerable code path.
2. **Verify the installed version:** Run `dpkg -l <package>` or `rpm -q <package>` inside the container to confirm the actual installed version.
3. **Check vendor advisories:** Debian, Ubuntu, Red Hat, and Alpine maintain their own vulnerability trackers that may show a different status.
4. **Test exploitability:** For critical findings, verify whether the vulnerable code path is reachable in your application.

### Documentation Template

When suppressing a vulnerability, document it with this template:

```markdown
## CVE-2024-1234 — Suppressed

- **Package:** libexample 1.2.3
- **Severity:** HIGH (CVSS 7.5)
- **Reason:** The vulnerable function `parse_xml()` is not called by our application.
  We do not process XML input in any code path.
- **Verified by:** @username on 2025-01-15
- **Expiration:** 2025-04-15
- **Tracking issue:** https://github.com/org/repo/issues/123
```

### Cross-Scanner Validation

When a finding seems suspicious, validate it with a second scanner:

```bash
# Scan with Trivy
trivy image --format json myapp:latest > trivy-results.json

# Scan with Grype
grype myapp:latest -o json > grype-results.json

# Compare: if only one scanner reports it, investigate further
```

## Scanning in CI

### GitHub Actions: Trivy

```yaml
name: Container Security Scan

on:
  pull_request:
    paths:
      - 'Dockerfile'
      - 'requirements*.txt'
      - 'pyproject.toml'
      - 'poetry.lock'

jobs:
  trivy-scan:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Build image
        run: docker build -t ${{ github.repository }}:${{ github.sha }} .

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: '${{ github.repository }}:${{ github.sha }}'
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'

      - name: Upload Trivy scan results to GitHub Security tab
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: 'trivy-results.sarif'
```

### GitHub Actions: Grype

```yaml
name: Grype Security Scan

on:
  pull_request:
    paths:
      - 'Dockerfile'
      - 'requirements*.txt'

jobs:
  grype-scan:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Build image
        run: docker build -t ${{ github.repository }}:${{ github.sha }} .

      - name: Scan image with Grype
        uses: anchore/scan-action@v4
        id: grype-scan
        with:
          image: '${{ github.repository }}:${{ github.sha }}'
          fail-build: true
          severity-cutoff: critical
          output-format: sarif

      - name: Upload Grype scan results
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: ${{ steps.grype-scan.outputs.sarif }}
```

### Nightly Scan Pattern

```yaml
name: Nightly Security Scan

on:
  schedule:
    # Run at 2 AM UTC every day
    - cron: '0 2 * * *'
  workflow_dispatch:

jobs:
  nightly-scan:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      issues: write
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Pull latest production image
        run: docker pull ghcr.io/${{ github.repository }}:latest

      - name: Run Trivy scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'ghcr.io/${{ github.repository }}:latest'
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'

      - name: Upload results to GitHub Security tab
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: 'trivy-results.sarif'
```

## Scanner Comparison

### Feature Matrix

| Feature | Trivy | Grype | Snyk | Docker Scout |
|---------|-------|-------|------|--------------|
| **License** | Apache-2.0 | Apache-2.0 | Proprietary (free tier) | Proprietary (free tier) |
| **OS Package Scanning** | Yes | Yes | Yes | Yes |
| **Language Dependency Scanning** | Yes | Yes | Yes | Yes |
| **Dockerfile Misconfiguration** | Yes | No | Yes (via IaC) | No |
| **Kubernetes Manifest Scanning** | Yes | No | Yes | No |
| **Terraform/IaC Scanning** | Yes | No | Yes | No |
| **Secret Detection** | Yes | No | No | No |
| **SBOM Generation** | Yes | No (use syft) | No | Yes |
| **SBOM as Input** | Yes | Yes | Yes | No |
| **SARIF Output** | Yes | Yes | Yes | Yes |
| **JSON Output** | Yes | Yes | Yes | Yes |
| **Offline Mode** | Yes | Yes | No | No |
| **GitHub Action** | Official | Official | Official | Official |
| **Database Updates** | Automatic | Automatic | Automatic | Automatic |
| **Fix Suggestions** | No | No | Yes | Yes |
| **License Scanning** | Yes | No | Yes | Yes |
| **Vulnerability Database** | NVD, vendor advisories | NVD, vendor advisories | Snyk DB (proprietary) | Docker DB, NVD |

### Choosing a Scanner

**Choose Trivy when:**
- You want a single tool for vulnerability, misconfiguration, and secret scanning
- You need IaC scanning alongside container scanning
- You prefer fully open-source tools with no vendor lock-in
- You want built-in SBOM generation

**Choose Grype when:**
- You want a fast, focused vulnerability scanner
- You are already using syft for SBOM generation
- You need to scan SBOMs as a primary input
- You prefer Anchore's vulnerability matching approach

**Choose both when:**
- You want cross-validation of findings
- You want defense in depth for critical workloads

**Consider Snyk or Docker Scout when:**
- You need fix suggestions and upgrade guidance
- You want a managed service with a web dashboard
- Your organization already has a Snyk or Docker subscription

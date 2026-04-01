# Supply Chain Security — Deep Reference

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| SBOM Generation | 15–85 | Generating SBOMs with syft, trivy, and docker sbom in SPDX and CycloneDX formats |
| Image Signing with cosign | 86–161 | Keyless and key-based signing, verification, and Sigstore integration |
| SLSA Provenance and Attestation | 162–218 | SLSA levels, provenance generation, and attestation with cosign |
| Base Image Provenance | 219–265 | Verified publishers, Chainguard images, and verifying base image origins |
| Dependency Pinning | 266–327 | Digest pinning for base images, lock files, and reproducible builds |
| Verification in CI | 328–400 | Automating cosign verify, policy enforcement, and admission controllers |
| Software Bill of Materials Formats | 401–449 | SPDX vs CycloneDX format comparison and tooling ecosystem |

---

## SBOM Generation

A Software Bill of Materials (SBOM) is a complete inventory of every component, library, and dependency in your container image. SBOMs enable you to quickly determine whether a newly disclosed vulnerability affects any of your deployed images, even months after they were built.

### syft (Recommended)

syft from Anchore is a purpose-built SBOM generator that supports multiple output formats:

```bash
# Install syft
brew install syft                    # macOS
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin  # Linux

# Generate SPDX SBOM from container image
syft myapp:latest -o spdx-json > sbom.spdx.json

# Generate CycloneDX SBOM
syft myapp:latest -o cyclonedx-json > sbom.cdx.json

# Generate from a local directory
syft dir:. -o spdx-json > project-sbom.spdx.json

# Generate from a Docker archive
syft docker-archive:myapp.tar -o spdx-json > sbom.spdx.json

# Include file metadata and hashes
syft myapp:latest -o spdx-json --file-metadata > sbom-full.spdx.json
```

### Trivy SBOM

Trivy can generate SBOMs as part of its scanning workflow:

```bash
# Generate SPDX SBOM
trivy image --format spdx-json --output sbom.spdx.json myapp:latest

# Generate CycloneDX SBOM
trivy image --format cyclonedx --output sbom.cdx.json myapp:latest

# Scan an existing SBOM for vulnerabilities
trivy sbom sbom.spdx.json
```

### Docker SBOM (Docker Desktop)

Docker Desktop includes built-in SBOM generation via the `docker sbom` command:

```bash
# Generate SBOM (requires Docker Desktop)
docker sbom myapp:latest
docker sbom myapp:latest --format spdx-json > sbom.spdx.json
docker sbom myapp:latest --format cyclonedx-json > sbom.cdx.json
```

### SBOM Storage and Distribution

Store SBOMs alongside your container images for consumers to retrieve:

```bash
# Attach SBOM as an OCI artifact (using cosign)
cosign attach sbom --sbom sbom.spdx.json myregistry/myapp:latest

# Attach SBOM using ORAS (OCI Registry As Storage)
oras attach myregistry/myapp:latest sbom.spdx.json:application/spdx+json

# Store in a dedicated registry path
crane push sbom.spdx.json myregistry/myapp:latest-sbom
```

### Scanning SBOMs for Vulnerabilities

Decouple SBOM generation from vulnerability scanning to scan the same SBOM against updated databases:

```bash
# Generate once
syft myapp:latest -o spdx-json > sbom.spdx.json

# Scan repeatedly as databases update
trivy sbom sbom.spdx.json
grype sbom:sbom.spdx.json
```

## Image Signing with cosign

cosign from the Sigstore project enables you to sign container images so that consumers can verify the image came from you and has not been tampered with.

### Keyless Signing (Recommended)

Keyless signing uses your OIDC identity (GitHub, Google, Microsoft) to sign images. No key management required.

```bash
# Install cosign
brew install cosign                   # macOS
go install github.com/sigstore/cosign/v2/cmd/cosign@latest  # Go

# Sign an image (interactive OIDC flow)
cosign sign myregistry/myapp@sha256:abc123...

# Sign in CI with GitHub Actions OIDC
# (uses the GitHub Actions OIDC token automatically)
cosign sign --yes myregistry/myapp@sha256:abc123...
```

**How keyless signing works:**

1. cosign requests an OIDC identity token from your identity provider
2. The Sigstore Fulcio CA issues a short-lived certificate bound to your identity
3. The signature and certificate are recorded in the Rekor transparency log
4. Anyone can verify the signature against the transparency log without needing your key

### Key-Based Signing

For environments without OIDC, use traditional key pairs:

```bash
# Generate a key pair
cosign generate-key-pair
# Creates cosign.key (private, keep secret) and cosign.pub (public, distribute)

# Sign with the private key
cosign sign --key cosign.key myregistry/myapp@sha256:abc123...

# Verify with the public key
cosign verify --key cosign.pub myregistry/myapp:latest
```

### Verification

```bash
# Verify keyless signature (checks Fulcio + Rekor)
cosign verify myregistry/myapp:latest

# Verify with identity constraints
cosign verify \
  --certificate-identity "user@example.com" \
  --certificate-oidc-issuer "https://accounts.google.com" \
  myregistry/myapp:latest

# Verify GitHub Actions identity
cosign verify \
  --certificate-identity "https://github.com/org/repo/.github/workflows/build.yml@refs/heads/main" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  myregistry/myapp:latest

# Verify with a public key
cosign verify --key cosign.pub myregistry/myapp:latest
```

### Signing in GitHub Actions

```yaml
- name: Sign image with cosign
  uses: sigstore/cosign-installer@v3

- name: Sign the image
  env:
    COSIGN_EXPERIMENTAL: "true"
  run: |
    cosign sign --yes myregistry/myapp@${{ steps.build.outputs.digest }}
```

### Signing Multiple Architectures

For multi-architecture images, sign the manifest list (index):

```bash
# Sign the multi-arch manifest
cosign sign myregistry/myapp@sha256:manifestlist-digest...

# Verify works for any platform
cosign verify myregistry/myapp:latest
```

## SLSA Provenance and Attestation

SLSA (Supply-chain Levels for Software Artifacts) is a framework for describing the integrity of software artifacts. Provenance records how and where an artifact was built.

### SLSA Levels

| Level | Requirements | Meaning |
|-------|-------------|---------|
| SLSA 1 | Provenance exists | Build process is documented |
| SLSA 2 | Hosted build, signed provenance | Build ran on a managed service, provenance is signed |
| SLSA 3 | Hardened builds, non-falsifiable provenance | Build environment is isolated, provenance cannot be forged |
| SLSA 4 | Two-person review, hermetic builds | Full supply chain control |

### Generating Provenance with GitHub Actions

```yaml
- name: Generate SLSA provenance
  uses: slsa-framework/slsa-github-generator/.github/workflows/generator_container_slsa3.yml@v2.0.0
  with:
    image: myregistry/myapp
    digest: ${{ steps.build.outputs.digest }}
```

### Attestation with cosign

Attestations are signed statements about an artifact. Provenance is one type of attestation.

```bash
# Create and sign an attestation
cosign attest --predicate provenance.json --type slsaprovenance \
  myregistry/myapp@sha256:abc123...

# Verify an attestation
cosign verify-attestation --type slsaprovenance \
  myregistry/myapp:latest

# Custom attestation (e.g., vulnerability scan results)
cosign attest --predicate scan-results.json --type vuln \
  myregistry/myapp@sha256:abc123...
```

### Provenance JSON Structure

```json
{
  "_type": "https://in-toto.io/Statement/v0.1",
  "predicateType": "https://slsa.dev/provenance/v0.2",
  "subject": [
    {
      "name": "myregistry/myapp",
      "digest": { "sha256": "abc123..." }
    }
  ],
  "predicate": {
    "builder": { "id": "https://github.com/actions/runner" },
    "buildType": "https://github.com/slsa-framework/slsa-github-generator/container@v1",
    "invocation": {
      "configSource": {
        "uri": "git+https://github.com/org/repo@refs/heads/main",
        "digest": { "sha1": "def456..." }
      }
    },
    "materials": [
      {
        "uri": "docker://python:3.12-slim",
        "digest": { "sha256": "789abc..." }
      }
    ]
  }
}
```

## Base Image Provenance

Knowing where your base images come from and whether they are trustworthy is fundamental to supply chain security.

### Verified Publishers

Use base images from verified, trusted sources:

| Source | Trust Level | Examples |
|--------|------------|---------|
| Docker Official Images | High | `python:3.12`, `node:20`, `postgres:16` |
| Docker Verified Publisher | High | `bitnami/postgresql`, `nginx/nginx-ingress` |
| Chainguard Images | Very High | `cgr.dev/chainguard/python`, `cgr.dev/chainguard/node` |
| Google Distroless | High | `gcr.io/distroless/python3-debian12` |
| OS Vendor Images | High | `ubuntu:24.04`, `alpine:3.19` |
| Random Docker Hub Images | Low | `someuser/someimage` — audit before using |

### Verifying Base Images

```bash
# Verify Docker Official Image signatures
docker trust inspect python:3.12-slim

# Verify Chainguard image signatures
cosign verify cgr.dev/chainguard/python:latest \
  --certificate-oidc-issuer="https://token.actions.githubusercontent.com" \
  --certificate-identity-regexp=".*chainguard.*"

# Check image provenance
cosign verify-attestation --type slsaprovenance \
  cgr.dev/chainguard/python:latest
```

### Auditing Base Image Contents

```bash
# List packages in a base image
docker run --rm python:3.12-slim dpkg -l
docker run --rm alpine:3.19 apk list --installed

# Generate SBOM of base image
syft python:3.12-slim -o spdx-json > base-sbom.spdx.json

# Scan base image for vulnerabilities
trivy image python:3.12-slim
```

## Dependency Pinning

Mutable tags (`:latest`, `:3.12`) can change without notice. Pin dependencies by digest for reproducible and auditable builds.

### Digest Pinning for Base Images

```dockerfile
# WRONG: Mutable tag can change
FROM python:3.12-slim

# RIGHT: Pinned by digest (immutable)
FROM python:3.12-slim@sha256:abc123def456...

# Find the current digest
docker manifest inspect python:3.12-slim | jq -r '.config.digest'
# Or use crane
crane digest python:3.12-slim
```

### Automated Digest Updates

Use Renovate or Dependabot to automatically update pinned digests:

**Renovate configuration (renovate.json):**
```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"],
  "docker": {
    "pinDigests": true
  }
}
```

**Dependabot configuration (.github/dependabot.yml):**
```yaml
version: 2
updates:
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
```

### Lock Files in Containers

Ensure dependency lock files are used during image builds:

```dockerfile
# Python: use exact versions from lock file
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Better: use pip-compile with hashes
COPY requirements.txt .
RUN pip install --no-cache-dir --require-hashes -r requirements.txt

# Node.js: use ci for deterministic installs
COPY package.json package-lock.json ./
RUN npm ci --production

# Go: use go.sum for verification
COPY go.mod go.sum ./
RUN go mod download && go mod verify
```

### Multi-Stage Dependency Verification

```dockerfile
FROM python:3.12-slim@sha256:abc123... AS builder
COPY requirements.txt .
RUN pip install --no-cache-dir --require-hashes --prefix=/install -r requirements.txt

# Verify installed packages
RUN pip check --prefix=/install

FROM python:3.12-slim@sha256:abc123...
COPY --from=builder /install /usr/local
COPY . /app
USER 1001
CMD ["python", "/app/main.py"]
```

## Verification in CI

Automate supply chain verification in your CI/CD pipeline to enforce policies before deployment.

### Verify Signatures Before Deployment

```yaml
name: Verify and Deploy

on:
  workflow_dispatch:
    inputs:
      image:
        description: 'Image to deploy'
        required: true

jobs:
  verify-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Install cosign
        uses: sigstore/cosign-installer@v3

      - name: Verify image signature
        run: |
          cosign verify \
            --certificate-identity "https://github.com/org/repo/.github/workflows/build.yml@refs/heads/main" \
            --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
            ${{ inputs.image }}

      - name: Verify SBOM attestation
        run: |
          cosign verify-attestation --type spdxjson \
            --certificate-identity "https://github.com/org/repo/.github/workflows/build.yml@refs/heads/main" \
            --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
            ${{ inputs.image }}

      - name: Deploy
        run: |
          # Only reached if verification passes
          kubectl set image deployment/myapp app=${{ inputs.image }}
```

### Policy Enforcement with Kyverno

Kyverno can enforce that all deployed images are signed:

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: verify-image-signatures
spec:
  validationFailureAction: Enforce
  background: false
  rules:
    - name: verify-cosign-signature
      match:
        any:
          - resources:
              kinds:
                - Pod
      verifyImages:
        - imageReferences:
            - "myregistry/*"
          attestors:
            - entries:
                - keyless:
                    issuer: "https://token.actions.githubusercontent.com"
                    subject: "https://github.com/org/repo/*"
```

### Policy Enforcement with Sigstore Policy Controller

```yaml
apiVersion: policy.sigstore.dev/v1beta1
kind: ClusterImagePolicy
metadata:
  name: require-signed-images
spec:
  images:
    - glob: "myregistry/**"
  authorities:
    - keyless:
        identities:
          - issuer: "https://token.actions.githubusercontent.com"
            subjectRegExp: "https://github.com/org/repo/.*"
        ctlog:
          url: "https://rekor.sigstore.dev"
```

### Complete CI Verification Pipeline

```yaml
name: Full Supply Chain Verification

on:
  pull_request:
    branches: [main]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: sigstore/cosign-installer@v3

      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Generate SBOM
        run: syft myapp:${{ github.sha }} -o spdx-json > sbom.spdx.json

      - name: Scan for vulnerabilities
        run: grype sbom:sbom.spdx.json --fail-on critical

      - name: Push image
        run: |
          docker tag myapp:${{ github.sha }} myregistry/myapp:${{ github.sha }}
          docker push myregistry/myapp:${{ github.sha }}

      - name: Sign image
        run: cosign sign --yes myregistry/myapp@$(crane digest myregistry/myapp:${{ github.sha }})

      - name: Attach SBOM
        run: cosign attach sbom --sbom sbom.spdx.json myregistry/myapp@$(crane digest myregistry/myapp:${{ github.sha }})
```

## Software Bill of Materials Formats

### SPDX vs CycloneDX

| Feature | SPDX | CycloneDX |
|---------|------|-----------|
| **Standard Body** | Linux Foundation | OWASP |
| **ISO Standard** | ISO/IEC 5962:2021 | ECMA-424 |
| **Primary Focus** | License compliance + security | Security + component analysis |
| **File Formats** | JSON, RDF, YAML, tag-value, XML | JSON, XML, Protobuf |
| **Vulnerability Tracking** | Via external references | Native VEX support |
| **License Expression** | SPDX License Expressions (native) | Supported |
| **Government Adoption** | US Executive Order 14028 | US Executive Order 14028 |
| **Tool Support** | syft, trivy, docker sbom | syft, trivy, docker sbom |

### SPDX JSON Structure (Abbreviated)

```json
{
  "spdxVersion": "SPDX-2.3",
  "dataLicense": "CC0-1.0",
  "SPDXID": "SPDXRef-DOCUMENT",
  "name": "myapp-sbom",
  "packages": [
    {
      "SPDXID": "SPDXRef-Package-python-3.12.3",
      "name": "python",
      "versionInfo": "3.12.3",
      "supplier": "Organization: Python Software Foundation",
      "downloadLocation": "https://www.python.org",
      "licenseConcluded": "PSF-2.0"
    }
  ]
}
```

### CycloneDX JSON Structure (Abbreviated)

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.5",
  "serialNumber": "urn:uuid:...",
  "version": 1,
  "components": [
    {
      "type": "library",
      "name": "python",
      "version": "3.12.3",
      "purl": "pkg:generic/python@3.12.3",
      "licenses": [
        { "license": { "id": "PSF-2.0" } }
      ]
    }
  ]
}
```

### Choosing a Format

**Choose SPDX when:**
- License compliance is a primary concern
- Your organization or customers require ISO standard compliance
- You need to exchange SBOMs with government agencies

**Choose CycloneDX when:**
- Security analysis is the primary concern
- You need native VEX (Vulnerability Exploitability eXchange) support
- You want tighter integration with OWASP tools

**When in doubt:** Generate both. syft and trivy support both formats with a single command:

```bash
syft myapp:latest -o spdx-json > sbom.spdx.json
syft myapp:latest -o cyclonedx-json > sbom.cdx.json
```

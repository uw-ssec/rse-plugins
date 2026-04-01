# Base Image Selection -- Deep Reference

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| Image Families | 16-108 | Official, distroless, alpine, slim, scratch overview |
| Comparison Table | 110-132 | Side-by-side comparison of image families by size, features |
| Language Runtime Images | 134-202 | Python, Node, Rust, Go, R, Julia runtime image options |
| Pinning Strategies | 204-267 | Tag pinning, digest pinning, combined strategies |
| Update Cadence and Security | 269-341 | How often to update, automated PR bots, CVE scanning |
| When to Use Each | 343-400 | Decision tree for choosing the right base image |

---

## Image Families

### Official Images

Docker Official Images are maintained by Docker in partnership with upstream projects. They follow consistent conventions, receive timely security updates, and are the default starting point for most Dockerfiles.

```dockerfile
FROM python:3.12
FROM node:22
FROM golang:1.23
FROM rust:1.82
FROM ubuntu:24.04
FROM debian:bookworm
```

**Characteristics:**
- Full operating system with shell, package manager, and common utilities
- Largest image size (typically 500 MB - 1.5 GB)
- Best compatibility with compiled extensions and system libraries
- Available on Docker Hub under library/ namespace

### Slim Variants

Slim images strip out documentation, man pages, and less commonly used packages from the official images. They keep the package manager and shell.

```dockerfile
FROM python:3.12-slim
FROM node:22-slim
FROM debian:bookworm-slim
```

**Characteristics:**
- 3-5x smaller than full official images
- Still have apt/dpkg for installing system dependencies
- Shell available for debugging
- Good default for production images that need apt

### Alpine

Alpine Linux uses musl libc instead of glibc and apk instead of apt. Images are very small but can cause compatibility issues with software that assumes glibc.

```dockerfile
FROM python:3.12-alpine
FROM node:22-alpine
FROM alpine:3.20
```

**Characteristics:**
- Very small (5-50 MB base)
- Uses musl libc (not glibc) -- some compiled packages may not work
- Uses apk package manager
- Compiled Python wheels from PyPI may not install (need to build from source)
- Good for Go, bad for Python/R with compiled extensions

**When Alpine causes problems:**
- Python packages with C extensions may need to be compiled from source (slow)
- `numpy`, `pandas`, `scipy` take much longer to install on Alpine
- DNS resolution behaves differently with musl
- Some Go programs using cgo may have issues

### Distroless

Google's distroless images contain only the application runtime and its dependencies. No shell, no package manager, no coreutils.

```dockerfile
FROM gcr.io/distroless/python3-debian12
FROM gcr.io/distroless/cc-debian12
FROM gcr.io/distroless/static-debian12
FROM gcr.io/distroless/java21-debian12
```

**Characteristics:**
- No shell (cannot `docker exec -it container sh`)
- No package manager
- Uses glibc (not musl)
- Minimal attack surface
- Use `:debug` tag during development for a busybox shell

### Scratch

The empty image. Zero files, zero bytes. Only usable with statically linked binaries.

```dockerfile
FROM scratch
```

**Characteristics:**
- 0 bytes
- No shell, no libc, no certificates, no timezone data
- Must copy everything the application needs
- Ideal for Go binaries compiled with `CGO_ENABLED=0`

---

## Comparison Table

| Image | Base Size | Shell | Package Manager | libc | Best For |
|-------|----------|-------|----------------|------|----------|
| `ubuntu:24.04` | 78 MB | bash | apt | glibc | Full development, system deps |
| `debian:bookworm` | 116 MB | bash | apt | glibc | Stable production base |
| `debian:bookworm-slim` | 74 MB | bash | apt | glibc | Production with apt needs |
| `alpine:3.20` | 7 MB | sh | apk | musl | Minimal with shell |
| `distroless/static` | 2 MB | no | no | no | Static binaries |
| `distroless/cc` | 20 MB | no | no | glibc | Dynamic binaries |
| `distroless/python3` | 52 MB | no | no | glibc | Python without shell |
| `scratch` | 0 MB | no | no | no | Fully static binaries |
| `python:3.12` | 1.0 GB | bash | apt | glibc | Python dev/build stage |
| `python:3.12-slim` | 150 MB | bash | apt | glibc | Python production |
| `python:3.12-alpine` | 55 MB | sh | apk | musl | Python (simple deps only) |
| `node:22` | 1.1 GB | bash | apt | glibc | Node dev/build stage |
| `node:22-slim` | 200 MB | bash | apt | glibc | Node production |
| `node:22-alpine` | 55 MB | sh | apk | musl | Node (no native addons) |
| `rust:1.82` | 1.5 GB | bash | apt | glibc | Rust build stage |
| `golang:1.23` | 800 MB | bash | apt | glibc | Go build stage |
| `rocker/r-ver:4.4` | 800 MB | bash | apt | glibc | R runtime |

---

## Language Runtime Images

### Python

| Image | Use Case | Notes |
|-------|----------|-------|
| `python:3.12` | Build stage | Full image with gcc, make for compiling extensions |
| `python:3.12-slim` | Production runtime | Recommended default for production |
| `python:3.12-alpine` | Minimal production | Avoid if using numpy/scipy/pandas |
| `python:3.12-bookworm` | Specific Debian version | When you need a specific Debian release |
| `gcr.io/distroless/python3-debian12` | Hardened production | No shell, minimal surface |

**Choosing between slim and alpine for Python:**
- Use `slim` if you install any packages with C extensions
- Use `alpine` only if all your dependencies are pure Python
- The time saved by alpine's smaller download is lost if you need to compile C extensions from source

### Node.js

| Image | Use Case | Notes |
|-------|----------|-------|
| `node:22` | Build stage | Full image for native addon compilation |
| `node:22-slim` | Production runtime | Recommended default |
| `node:22-alpine` | Minimal production | Fine for most Node apps (no native addons) |
| `node:22-bookworm` | Specific Debian version | When you need a specific Debian release |

Node.js on Alpine works well because most npm packages are pure JavaScript. Only use the full image or slim if you have native addons (node-gyp).

### Rust

| Image | Use Case | Notes |
|-------|----------|-------|
| `rust:1.82` | Build stage only | Never use as final image |
| `gcr.io/distroless/cc-debian12` | Final (dynamic linking) | Has glibc for dynamic Rust binaries |
| `gcr.io/distroless/static-debian12` | Final (static linking) | For `target x86_64-unknown-linux-musl` |
| `scratch` | Final (fully static) | Smallest possible, needs CA certs copied |
| `debian:bookworm-slim` | Final (need debugging) | When you need shell access |

### Go

| Image | Use Case | Notes |
|-------|----------|-------|
| `golang:1.23` | Build stage only | Never use as final image |
| `scratch` | Final (CGO_ENABLED=0) | Recommended for static binaries |
| `gcr.io/distroless/static-debian12` | Final (with CA certs) | Includes certificates, timezone data |
| `alpine:3.20` | Final (need shell) | When debugging access is needed |

### R

| Image | Use Case | Notes |
|-------|----------|-------|
| `rocker/r-ver:4.4` | Base R runtime | Version-locked R installation |
| `rocker/rstudio:4.4` | RStudio Server | Interactive development |
| `rocker/tidyverse:4.4` | R + tidyverse | Pre-installed tidyverse packages |
| `rocker/verse:4.4` | R + tidyverse + tex | For R Markdown / Quarto rendering |
| `rocker/geospatial:4.4` | R + spatial | GDAL, GEOS, PROJ pre-installed |
| `rocker/cuda:4.4` | R + CUDA | GPU computing support |

The rocker images are the standard for R containers. They handle R's complex system dependency requirements.

### Julia

| Image | Use Case | Notes |
|-------|----------|-------|
| `julia:1.11` | General purpose | Official Julia image |
| `julia:1.11-bullseye` | Specific Debian | When you need a specific OS |
| `julia:1.11-alpine` | Minimal | For simple Julia scripts |

---

## Pinning Strategies

### Tag Pinning

Pin to a specific version tag to avoid unexpected changes when the upstream image updates:

```dockerfile
# BAD: could change at any time
FROM python:latest

# OKAY: pinned to minor version, patch updates still happen
FROM python:3.12

# BETTER: pinned to patch version
FROM python:3.12.7

# GOOD: pinned to patch + OS variant
FROM python:3.12.7-slim-bookworm
```

**Tag pinning levels:**

| Pin Level | Example | Stability | Security Updates |
|-----------|---------|-----------|-----------------|
| `latest` | `python:latest` | None | Automatic |
| Major | `python:3` | Low | Automatic |
| Minor | `python:3.12` | Medium | Automatic patches |
| Patch | `python:3.12.7` | High | Manual update needed |
| Patch + OS | `python:3.12.7-slim-bookworm` | Highest | Manual update needed |

### Digest Pinning

Pin to a specific image digest (SHA256 hash) for absolute reproducibility. The digest identifies an exact image manifest -- it cannot change.

```dockerfile
# Pinned by digest
FROM python:3.12.7-slim-bookworm@sha256:abc123def456...

# Find the digest
# docker inspect --format='{{index .RepoDigests 0}}' python:3.12.7-slim-bookworm
```

**Advantages:**
- Immutable -- guaranteed to be the exact same image every time
- Protects against tag mutation (tags can be moved to point at different images)
- Required for high-security environments

**Disadvantages:**
- Must manually update the digest for security patches
- Harder to read than version tags
- Different digests for different platforms (amd64 vs arm64)

### Combined Strategy (Recommended)

Use both tag and digest for human readability plus machine reproducibility:

```dockerfile
# Human-readable tag + machine-verifiable digest
FROM python:3.12.7-slim-bookworm@sha256:abc123def456...
```

Tools like Renovate and Dependabot can automatically update both the tag and digest when new versions are released.

---

## Update Cadence and Security

### How Often to Update Base Images

| Update Type | Frequency | Trigger |
|------------|-----------|---------|
| Security patches | Within 24-48 hours | CVE published for base image |
| Minor version bumps | Monthly | New patch release of language runtime |
| Major version bumps | Per release cycle | Language major version release |
| OS version changes | Yearly | New Debian/Ubuntu LTS |

### Automated PR Bots

Use dependency update bots to receive pull requests when base images or pinned versions change:

**Renovate (recommended for Docker):**

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"],
  "dockerfile": {
    "enabled": true,
    "pinDigests": true
  }
}
```

**Dependabot:**

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
```

### CVE Scanning

Scan images for known vulnerabilities as part of your CI pipeline:

```bash
# Docker Scout (built into Docker Desktop)
docker scout cves myapp:latest

# Trivy
trivy image myapp:latest

# Grype
grype myapp:latest
```

GitHub Actions integration:

```yaml
- name: Scan image for vulnerabilities
  uses: aquasecurity/trivy-action@0.28.0
  with:
    image-ref: myapp:latest
    format: 'sarif'
    output: 'trivy-results.sarif'
    severity: 'CRITICAL,HIGH'

- name: Upload scan results
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: 'trivy-results.sarif'
```

---

## When to Use Each

### Decision Tree

```
What are you building?
|
+-- Static binary (Go with CGO_ENABLED=0)?
|   => Final image: scratch or distroless/static
|
+-- Dynamic binary (Rust, C/C++, Go with CGO)?
|   |
|   +-- Need shell for debugging?
|   |   => Final image: debian:bookworm-slim or alpine
|   |
|   +-- No shell needed?
|       => Final image: distroless/cc
|
+-- Interpreted language (Python, Node, R, Julia)?
|   |
|   +-- Python with compiled extensions (numpy, scipy)?
|   |   => Final image: python:X.Y-slim (NOT alpine)
|   |
|   +-- Python with pure-Python deps only?
|   |   => Final image: python:X.Y-slim or python:X.Y-alpine
|   |
|   +-- Node.js?
|   |   |
|   |   +-- Has native addons (node-gyp)?
|   |   |   => Final image: node:X-slim
|   |   |
|   |   +-- Pure JavaScript only?
|   |       => Final image: node:X-slim or node:X-alpine
|   |
|   +-- R?
|   |   => Final image: rocker/r-ver:X.Y
|   |
|   +-- Julia?
|       => Final image: julia:X.Y
|
+-- Need full OS for system integration?
    => ubuntu:24.04 or debian:bookworm
```

### Quick Recommendation Table

| Scenario | Recommended Base | Reason |
|----------|-----------------|--------|
| Python web service | `python:3.12-slim` | Balanced size and compatibility |
| Python data science | `python:3.12-slim` + apt deps | Needs glibc for numpy/scipy |
| Node.js API | `node:22-slim` | Most packages are pure JS |
| Rust CLI tool | `distroless/cc` or `scratch` | Binary does not need OS |
| Go microservice | `scratch` + CA certs | Static binary |
| R analysis pipeline | `rocker/r-ver:4.4` | Handles R system deps |
| C/C++ application | `debian:bookworm-slim` | Needs runtime .so files |
| Multi-arch build | `debian:bookworm-slim` | Best cross-platform support |
| Security-critical | `distroless/*` | Minimal attack surface |
| Development / debugging | `*-slim` or full variant | Need shell and tools |

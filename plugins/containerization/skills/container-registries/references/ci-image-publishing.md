# CI Image Publishing -- Deep Reference

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| docker/build-push-action | 16-122 | Core action setup, inputs, outputs, and usage patterns |
| Matrix Builds for Multi-Arch | 124-224 | Platform matrix strategies, QEMU, native runners |
| Caching Strategies | 226-317 | gha cache, registry cache, inline cache, layer caching |
| Conditional Publishing | 319-398 | Path filters, branch guards, environment gates |
| Release-Triggered Builds | 400-502 | GitHub Release events, tag extraction, changelog |
| Attestation with SBOM | 504-587 | Build provenance, SBOM generation, SLSA attestation |

---

## docker/build-push-action

### Overview

The `docker/build-push-action` is the standard GitHub Action for building and pushing Docker images. It wraps Docker Buildx and supports multi-platform builds, caching, and OCI metadata.

### Basic Setup

```yaml
name: Build and Push

on:
  push:
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-buildx-action@v3

      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/metadata-action@v5
        id: meta
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=semver,pattern={{major}}
            type=sha

      - uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

### Key Inputs

| Input | Description | Default |
|-------|-------------|---------|
| `context` | Build context path | `.` |
| `file` | Dockerfile path | `{context}/Dockerfile` |
| `push` | Push image after build | `false` |
| `tags` | Image tags (newline-separated) | none |
| `labels` | OCI labels | none |
| `platforms` | Target platforms | runner's platform |
| `cache-from` | Cache sources | none |
| `cache-to` | Cache destinations | none |
| `build-args` | Build arguments | none |
| `target` | Target build stage | none |
| `provenance` | Generate provenance attestation | `true` |
| `sbom` | Generate SBOM attestation | `false` |

### Key Outputs

| Output | Description |
|--------|-------------|
| `imageid` | Image content-addressable ID |
| `digest` | Image manifest digest |
| `metadata` | Build result metadata |

### docker/metadata-action Tag Types

The metadata action generates tags based on Git events:

```yaml
tags: |
  # Semantic version from git tag (v1.2.3 -> 1.2.3, 1.2, 1)
  type=semver,pattern={{version}}
  type=semver,pattern={{major}}.{{minor}}
  type=semver,pattern={{major}}

  # Git short SHA (sha-a1b2c3d)
  type=sha

  # Branch name (main, develop)
  type=ref,event=branch

  # PR number (pr-42)
  type=ref,event=pr

  # Raw string
  type=raw,value=latest,enable={{is_default_branch}}

  # Schedule (nightly)
  type=schedule,pattern=nightly

  # Edge (latest commit on default branch)
  type=edge
```

---

## Matrix Builds for Multi-Arch

### Using QEMU Emulation

The simplest approach uses QEMU to emulate non-native architectures. This is slower but requires only a single runner.

```yaml
steps:
  - uses: docker/setup-qemu-action@v3

  - uses: docker/setup-buildx-action@v3

  - uses: docker/build-push-action@v6
    with:
      platforms: linux/amd64,linux/arm64
      push: true
      tags: ghcr.io/myorg/myapp:v1.0.0
```

**Performance considerations:**
- ARM builds on x86 runners are 2-5x slower due to emulation
- Compilation-heavy builds (Rust, C++) can be 10x slower under QEMU
- Consider native runners for performance-critical builds

### Native Multi-Platform with Matrix Strategy

For faster builds, use a matrix strategy with platform-specific runners and merge the results:

```yaml
jobs:
  build:
    runs-on: ${{ matrix.runner }}
    strategy:
      matrix:
        include:
          - platform: linux/amd64
            runner: ubuntu-latest
          - platform: linux/arm64
            runner: ubuntu-24.04-arm

    steps:
      - uses: docker/setup-buildx-action@v3

      - uses: docker/build-push-action@v6
        id: build
        with:
          platforms: ${{ matrix.platform }}
          tags: ghcr.io/myorg/myapp:v1.0.0
          outputs: type=image,push-by-digest=true,name-canonical=true,push=true

      - name: Export digest
        run: |
          mkdir -p /tmp/digests
          digest="${{ steps.build.outputs.digest }}"
          touch "/tmp/digests/${digest#sha256:}"

      - uses: actions/upload-artifact@v4
        with:
          name: digests-${{ matrix.platform }}
          path: /tmp/digests/*

  merge:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          path: /tmp/digests
          pattern: digests-*
          merge-multiple: true

      - uses: docker/setup-buildx-action@v3

      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Create manifest list and push
        working-directory: /tmp/digests
        run: |
          docker buildx imagetools create \
            --tag ghcr.io/myorg/myapp:v1.0.0 \
            $(printf 'ghcr.io/myorg/myapp@sha256:%s ' *)
```

### Platform-Specific Build Arguments

Some builds need different arguments per platform:

```dockerfile
ARG TARGETPLATFORM
RUN case "${TARGETPLATFORM}" in \
      "linux/amd64") ARCH="x86_64" ;; \
      "linux/arm64") ARCH="aarch64" ;; \
    esac && \
    curl -L "https://example.com/binary-${ARCH}" -o /usr/local/bin/tool
```

---

## Caching Strategies

### GitHub Actions Cache (gha)

Uses GitHub's cache infrastructure. Fast for small-to-medium images with frequent builds.

```yaml
- uses: docker/build-push-action@v6
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

**Limits:**
- 10 GB per repository (shared across all workflows)
- Evicts least recently used entries when full
- `mode=max` caches all layers (not just the final image layers)

### Registry Cache

Stores cache layers in a dedicated tag in the container registry. Works across CI providers and is not limited by GitHub cache size.

```yaml
- uses: docker/build-push-action@v6
  with:
    cache-from: type=registry,ref=ghcr.io/myorg/myapp:buildcache
    cache-to: type=registry,ref=ghcr.io/myorg/myapp:buildcache,mode=max
```

**Advantages:**
- No size limit (limited only by registry storage)
- Shared across branches, runners, and CI providers
- Persistent (does not evict like GitHub cache)

**Disadvantages:**
- Slower than gha cache (network transfer to/from registry)
- Consumes registry storage

### Inline Cache

Embeds cache metadata into the image itself. Simplest to set up but only caches layers included in the final image.

```yaml
- uses: docker/build-push-action@v6
  with:
    cache-from: type=registry,ref=ghcr.io/myorg/myapp:latest
    cache-to: type=inline
```

**Limitation:** Only caches final stage layers. Multi-stage build intermediate stages are not cached with inline mode.

### Combining Caches

You can specify multiple cache sources. Buildx checks them in order:

```yaml
- uses: docker/build-push-action@v6
  with:
    cache-from: |
      type=gha
      type=registry,ref=ghcr.io/myorg/myapp:buildcache
    cache-to: type=gha,mode=max
```

### Cache Performance Comparison

| Cache Type | Speed | Persistence | Multi-Stage | Size Limit |
|-----------|-------|-------------|-------------|------------|
| gha | Fast | Evicts LRU | Yes (mode=max) | 10 GB/repo |
| registry | Moderate | Persistent | Yes (mode=max) | Registry limit |
| inline | Fast | Persistent | No (final only) | None |
| local | Fastest | Runner only | Yes | Disk space |

### Cache Debugging

If builds are not hitting cache, check:

```bash
# View cache details in build output
docker buildx build --progress=plain .

# Check if cache-from is resolving
# Look for "importing cache manifest from..." in build logs
```

Common cache-busting causes:
- Base image update (different digest)
- Build argument change
- File modification that invalidates COPY layer
- Different build context

---

## Conditional Publishing

### Path-Based Triggers

Only build when relevant files change:

```yaml
on:
  push:
    branches: [main]
    paths:
      - 'Dockerfile'
      - 'src/**'
      - 'requirements.txt'
      - 'pyproject.toml'
      - 'uv.lock'
      - '.github/workflows/publish.yml'
```

### Branch Guards

Publish different tags from different branches:

```yaml
- uses: docker/metadata-action@v5
  id: meta
  with:
    images: ghcr.io/${{ github.repository }}
    tags: |
      type=raw,value=latest,enable=${{ github.ref == 'refs/heads/main' }}
      type=raw,value=edge,enable=${{ github.ref == 'refs/heads/develop' }}
      type=semver,pattern={{version}},enable=${{ startsWith(github.ref, 'refs/tags/v') }}
```

### Environment Protection

Require approval before publishing to production registries:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    environment: production  # requires approval
    steps:
      - uses: docker/build-push-action@v6
        with:
          push: true
```

### Build Without Push (PR Validation)

On pull requests, build the image to verify it compiles but do not push:

```yaml
on:
  pull_request:
    paths: ['Dockerfile', 'src/**']

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: docker/build-push-action@v6
        with:
          push: false  # build only, do not push
          tags: ghcr.io/myorg/myapp:pr-${{ github.event.number }}
```

### Conditional Push Logic

Use GitHub Actions expressions for fine-grained control:

```yaml
- uses: docker/build-push-action@v6
  with:
    push: ${{ github.event_name != 'pull_request' }}
    tags: ${{ steps.meta.outputs.tags }}
```

---

## Release-Triggered Builds

### Publish on GitHub Release

Trigger image publishing when a GitHub Release is created:

```yaml
name: Publish on Release

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-buildx-action@v3

      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/metadata-action@v5
        id: meta
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=semver,pattern={{major}}

      - uses: docker/build-push-action@v6
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Tag Extraction

The `metadata-action` automatically extracts version components from git tags:

| Git Tag | `{{version}}` | `{{major}}.{{minor}}` | `{{major}}` |
|---------|--------------|----------------------|-------------|
| `v1.2.3` | `1.2.3` | `1.2` | `1` |
| `v2.0.0-rc.1` | `2.0.0-rc.1` | (skipped) | (skipped) |
| `v0.1.0` | `0.1.0` | `0.1` | `0` |

Pre-release tags (containing `-`) are only matched by the `{{version}}` pattern by default.

### Including Release Notes

Pass release information as build arguments or labels:

```yaml
- uses: docker/build-push-action@v6
  with:
    build-args: |
      VERSION=${{ github.event.release.tag_name }}
      COMMIT=${{ github.sha }}
    labels: |
      org.opencontainers.image.version=${{ github.event.release.tag_name }}
      org.opencontainers.image.revision=${{ github.sha }}
```

### Dual Registry Publishing

Publish to multiple registries from a single build:

```yaml
- uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}

- uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}

- uses: docker/metadata-action@v5
  id: meta
  with:
    images: |
      ghcr.io/${{ github.repository }}
      docker.io/${{ secrets.DOCKERHUB_USERNAME }}/${{ github.event.repository.name }}
```

---

## Attestation with SBOM

### Build Provenance

Docker Buildx can generate provenance attestations that record how an image was built:

```yaml
- uses: docker/build-push-action@v6
  with:
    push: true
    provenance: true  # default in recent versions
    tags: ghcr.io/myorg/myapp:v1.0.0
```

Provenance attestations include:
- Build timestamps
- Builder identity (GitHub Actions workflow)
- Source repository and commit
- Build parameters
- Base image references

### SBOM Generation

Generate a Software Bill of Materials as a build attestation:

```yaml
- uses: docker/build-push-action@v6
  with:
    push: true
    sbom: true
    tags: ghcr.io/myorg/myapp:v1.0.0
```

The SBOM is attached as an OCI attestation alongside the image. Consumers can retrieve it:

```bash
# View attestations
docker buildx imagetools inspect ghcr.io/myorg/myapp:v1.0.0 --format '{{json .Provenance}}'

# Extract SBOM
docker buildx imagetools inspect ghcr.io/myorg/myapp:v1.0.0 --format '{{json .SBOM}}'
```

### Post-Build SBOM with syft

For more control over SBOM format and content, generate it after building:

```yaml
- uses: docker/build-push-action@v6
  id: build
  with:
    push: true
    tags: ghcr.io/myorg/myapp:v1.0.0

- uses: anchore/sbom-action@v0
  with:
    image: ghcr.io/myorg/myapp:v1.0.0
    format: spdx-json
    output-file: sbom.spdx.json

- name: Attach SBOM to image
  run: |
    cosign attach sbom \
      --sbom sbom.spdx.json \
      ghcr.io/myorg/myapp@${{ steps.build.outputs.digest }}
```

### SLSA Provenance

For SLSA Level 3 provenance (non-forgeable build attestation), use the SLSA GitHub generator:

```yaml
- uses: slsa-framework/slsa-github-generator/.github/workflows/generator_container_slsa3.yml@v2.0.0
  with:
    image: ghcr.io/myorg/myapp
    digest: ${{ needs.build.outputs.digest }}
  secrets:
    registry-username: ${{ github.actor }}
    registry-password: ${{ secrets.GITHUB_TOKEN }}
```

### Verifying Attestations

Consumers can verify attestations before pulling:

```bash
# Verify provenance
cosign verify-attestation \
  --type slsaprovenance \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  --certificate-identity-regexp '^https://github.com/myorg/myapp/' \
  ghcr.io/myorg/myapp:v1.0.0

# Verify SBOM attachment
cosign verify-attestation \
  --type spdx \
  ghcr.io/myorg/myapp:v1.0.0
```

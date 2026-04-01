---
name: container-registries
description: Container image publishing to GHCR, Docker Hub, ECR, and ACR with CI/CD automation, image tagging strategies, and multi-architecture builds.
metadata:
  references:
    - references/ghcr-publishing.md
    - references/ci-image-publishing.md
  assets:
    - assets/ghcr-publish-workflow.yml
    - assets/docker-hub-publish-workflow.yml
---

# Container Registries

A comprehensive guide to publishing container images to container registries for research software projects. This skill covers registry setup and authentication, image tagging strategies, multi-architecture builds with Docker Buildx, and CI/CD automation for publishing images on push, tag, and release events. Whether you are publishing to GitHub Container Registry (GHCR), Docker Hub, Amazon ECR, or Azure ACR, these patterns help you ship container images reliably, reproducibly, and securely.

## Resources in This Skill

This skill includes supporting materials for container registry tasks:

**References** (detailed guides -- consult the table of contents in each file and read specific sections as needed):
- `references/ghcr-publishing.md` - GHCR setup and publishing: PAT vs GITHUB_TOKEN authentication, visibility settings, org-level packages, linking images to repos, cleanup actions, and OCI artifact storage
- `references/ci-image-publishing.md` - CI image publishing: docker/build-push-action usage, matrix builds for multi-arch, caching strategies (gha, registry), conditional publishing, release-triggered builds, and attestation with SBOM

**Assets** (ready-to-use workflow templates):
- `assets/ghcr-publish-workflow.yml` - GitHub Actions workflow for building and publishing images to GHCR on tag push with multi-architecture support and OCI metadata
- `assets/docker-hub-publish-workflow.yml` - GitHub Actions workflow for building and publishing images to Docker Hub with automated tagging

## Quick Reference Card

### Registry Comparison

| Feature | GHCR | Docker Hub | AWS ECR | Azure ACR |
|---------|------|------------|---------|-----------|
| **Free Tier** | Unlimited public | 1 repo (free), rate-limited pulls | 500 MB (free tier) | None (pay-as-you-go) |
| **Private Repos** | Included with GitHub plan | 1 free, then paid | Unlimited (paid) | Unlimited (paid) |
| **Pull Rate Limits** | None for public | 100/6h anon, 200/6h auth | None | None |
| **OCI Artifacts** | Yes | Yes | Yes | Yes |
| **Image Signing** | cosign, Notation | cosign, DCT | cosign, Notation | Notation, cosign |
| **Vulnerability Scan** | Via GitHub (Dependabot) | Docker Scout | Amazon Inspector | Microsoft Defender |
| **Multi-Arch** | Yes | Yes | Yes | Yes |
| **SBOM Attach** | Yes | Yes | Yes | Yes |

### Login Commands

```bash
# GHCR (GitHub Container Registry)
echo "$GITHUB_TOKEN" | docker login ghcr.io -u USERNAME --password-stdin

# Docker Hub
echo "$DOCKERHUB_TOKEN" | docker login -u USERNAME --password-stdin

# AWS ECR (requires AWS CLI)
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

# Azure ACR (requires Azure CLI)
az acr login --name myregistry
```

### Image Naming Convention

```
<registry>/<namespace>/<image>:<tag>

# Examples
ghcr.io/myorg/myapp:v1.2.3
docker.io/myuser/myapp:latest
123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:sha-abc1234
myregistry.azurecr.io/myapp:2024.01.15
```

## When to Use

Use this skill when you need to:

- Publish container images to GHCR, Docker Hub, ECR, or ACR
- Set up CI/CD pipelines for automated image publishing
- Choose and implement an image tagging strategy (semver, SHA, date-based)
- Build and publish multi-architecture images (amd64, arm64)
- Configure authentication for container registries in CI environments
- Set up image retention policies and cleanup stale images
- Link GHCR images to GitHub repositories for discoverability
- Evaluate which container registry fits your project

## Registry Comparison

### Pricing and Limits

**GHCR (GitHub Container Registry):**
- Free for public images, storage and bandwidth included with GitHub plan
- Private images count against GitHub storage quotas (Actions and Packages share a pool)
- No pull rate limits for public images
- Best choice for open-source projects already on GitHub

**Docker Hub:**
- Free tier allows one private repo and unlimited public repos
- Anonymous pulls limited to 100 per 6 hours per IP; authenticated pulls limited to 200 per 6 hours
- Pro/Team/Business plans remove rate limits and add more private repos
- Widest ecosystem support and largest public image library

**AWS ECR:**
- Pay-per-use: $0.10/GB/month storage, $0.09/GB data transfer
- ECR Public is free with generous limits (50 GB storage, 500 GB/month bandwidth)
- No pull rate limits for private repos within the same AWS account
- Best choice for AWS-deployed workloads

**Azure ACR:**
- Basic tier starts at ~$5/month with 10 GB storage
- Standard and Premium tiers add geo-replication, retention policies, and content trust
- Best choice for Azure-deployed workloads

### When to Choose Which

| Scenario | Recommended Registry |
|----------|---------------------|
| Open-source project on GitHub | GHCR |
| Widest community distribution | Docker Hub |
| AWS-deployed application | ECR |
| Azure-deployed application | ACR |
| Multi-cloud or registry-agnostic | GHCR or Docker Hub |
| Air-gapped / self-hosted | Harbor, GitLab Registry, or ECR |

## Image Tagging Strategies

Tags identify specific versions of a container image. A good tagging strategy makes it easy to deploy specific versions, roll back, and audit what is running.

### Semantic Versioning (semver)

Apply version tags from git tags. Publish multiple granularity levels so consumers can pin to a major, minor, or patch version.

```
myapp:1.2.3    # exact version
myapp:1.2      # latest patch in 1.2.x
myapp:1        # latest minor in 1.x
```

### Git SHA

Tag images with the short git commit SHA for traceability from image back to source code.

```
myapp:sha-a1b2c3d
```

### Latest

The `latest` tag points to the most recent build from the default branch. It is mutable and should not be used for production deployments, but it is convenient for development.

```
myapp:latest
```

### Date-Based

Useful for nightly or periodic builds where semver does not apply.

```
myapp:2024.01.15
myapp:nightly-2024-01-15
```

### Recommended Combination

Apply multiple tags to each image for flexibility:

```bash
# On a release tag (v1.2.3):
myapp:1.2.3
myapp:1.2
myapp:1
myapp:sha-a1b2c3d
myapp:latest

# On a default branch push (no tag):
myapp:sha-a1b2c3d
myapp:edge
```

The `docker/metadata-action` in GitHub Actions automates this tagging strategy. See the asset workflows for examples.

## GHCR Setup

GitHub Container Registry stores images alongside your code in the GitHub ecosystem.

**Enable GHCR for your account:**
1. GHCR is enabled by default for all GitHub accounts and organizations
2. Images are published under `ghcr.io/<owner>/<image>`

**Authentication in GitHub Actions:**
```yaml
- uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
```

The `GITHUB_TOKEN` is automatically available in Actions and has `packages:write` permission when configured. No PAT is needed for same-repo publishing.

**Linking images to repositories:**

Add the `org.opencontainers.image.source` label to your Dockerfile so GHCR links the image to your repository:

```dockerfile
LABEL org.opencontainers.image.source="https://github.com/myorg/myrepo"
```

**Visibility:** New packages inherit the repository's visibility. You can change visibility in Settings > Packages.

See `references/ghcr-publishing.md` for the complete GHCR reference.

## Docker Hub

Docker Hub is the default registry for Docker and has the largest collection of public images.

**Authentication in GitHub Actions:**
```yaml
- uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}
```

Use access tokens (not passwords) for CI authentication. Create them at https://hub.docker.com/settings/security.

**Automated builds:** Docker Hub's built-in automated builds from GitHub have been deprecated for free accounts. Use GitHub Actions with `docker/build-push-action` instead.

See `assets/docker-hub-publish-workflow.yml` for a ready-to-use workflow.

## AWS ECR and Azure ACR Overview

### AWS ECR

```yaml
# GitHub Actions login
- uses: aws-actions/configure-aws-credentials@v4
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: us-east-1

- uses: aws-actions/amazon-ecr-login@v2
```

ECR requires creating a repository before pushing. Use lifecycle policies to automatically expire old images.

### Azure ACR

```yaml
# GitHub Actions login
- uses: azure/docker-login@v2
  with:
    login-server: myregistry.azurecr.io
    username: ${{ secrets.ACR_USERNAME }}
    password: ${{ secrets.ACR_PASSWORD }}
```

ACR supports geo-replication for global distribution and integrates with Azure services natively.

## Multi-Architecture Builds

Build images that run on both `linux/amd64` (x86_64) and `linux/arm64` (Apple Silicon, AWS Graviton) using Docker Buildx.

**Setup Buildx:**
```bash
# Create and use a buildx builder
docker buildx create --name mybuilder --use
docker buildx inspect --bootstrap
```

**Build and push multi-arch image:**
```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag ghcr.io/myorg/myapp:v1.0.0 \
  --push .
```

**In GitHub Actions (using docker/build-push-action):**
```yaml
- uses: docker/setup-qemu-action@v3
- uses: docker/setup-buildx-action@v3
- uses: docker/build-push-action@v6
  with:
    platforms: linux/amd64,linux/arm64
    push: true
    tags: ghcr.io/myorg/myapp:v1.0.0
```

QEMU provides cross-platform emulation. Builds for non-native architectures are slower (2-5x) but produce genuine multi-arch manifests.

## CI/CD Publishing Patterns

### Publish on Tag Push

The most common pattern: publish a new image when a version tag is pushed.

```yaml
on:
  push:
    tags: ['v*']
```

### Publish on Release

Publish when a GitHub release is created, ensuring only reviewed releases produce images.

```yaml
on:
  release:
    types: [published]
```

### Publish on Default Branch Push

Publish an `edge` or `latest` tag on every push to the default branch for continuous delivery.

```yaml
on:
  push:
    branches: [main]
```

### Conditional Publishing

Only publish when Dockerfile or dependency files change:

```yaml
on:
  push:
    paths:
      - 'Dockerfile'
      - 'requirements.txt'
      - 'pyproject.toml'
```

See `references/ci-image-publishing.md` for advanced patterns.

## Image Retention and Cleanup

Container registries can accumulate thousands of images over time. Set up retention policies to control costs and reduce clutter.

**GHCR cleanup with GitHub Actions:**
```yaml
- uses: actions/delete-package-versions@v5
  with:
    package-name: myapp
    package-type: container
    min-versions-to-keep: 10
    delete-only-untagged-versions: true
```

**ECR lifecycle policy:**
```json
{
  "rules": [{
    "rulePriority": 1,
    "selection": {
      "tagStatus": "untagged",
      "countType": "sinceImagePushed",
      "countUnit": "days",
      "countNumber": 30
    },
    "action": { "type": "expire" }
  }]
}
```

**ACR retention:** Use `az acr config retention update` to set days-to-retain for untagged manifests.

## Authentication in CI

### Secrets Management

Never hardcode credentials. Use CI platform secret stores:

| CI Platform | Secret Mechanism |
|-------------|-----------------|
| GitHub Actions | `secrets.GITHUB_TOKEN` (auto), repository secrets |
| GitLab CI | CI/CD variables (masked, protected) |
| CircleCI | Environment variables, contexts |
| Jenkins | Credentials plugin |

### OIDC / Workload Identity (Recommended)

Avoid long-lived credentials by using OIDC federation:

```yaml
# AWS with OIDC
- uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::123456789:role/github-actions
    aws-region: us-east-1

# Azure with OIDC
- uses: azure/login@v2
  with:
    client-id: ${{ secrets.AZURE_CLIENT_ID }}
    tenant-id: ${{ secrets.AZURE_TENANT_ID }}
    subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
```

## Common Mistakes

1. **Using `latest` as a deployment tag** -- The `latest` tag is mutable and does not guarantee a specific version. Use semver or SHA tags for deployments.

2. **Hardcoding registry credentials** -- Never put tokens or passwords in workflow files. Use CI secret stores or OIDC federation.

3. **Not setting up image cleanup** -- Untagged and old images accumulate quickly. Configure retention policies or scheduled cleanup actions.

4. **Skipping multi-arch builds** -- If your users run on ARM (Apple Silicon, Graviton), a single-platform image forces emulation or fails outright.

5. **Publishing on every commit** -- Publish on tags or releases for versioned software. Use `edge` or `sha-*` tags for continuous delivery builds.

6. **Forgetting to link GHCR images to repos** -- Without the `org.opencontainers.image.source` label, GHCR images are orphaned from their source repository.

7. **Using passwords instead of tokens** -- Docker Hub and GHCR support access tokens with scoped permissions. Avoid using account passwords.

8. **Not caching builds in CI** -- Without caching, every CI build downloads and installs everything from scratch. Use `cache-from` with registry or gha cache.

## Best Practices

- [ ] Use semver tags plus SHA tags for every published image
- [ ] Automate publishing with CI/CD (never push manually from local machines)
- [ ] Use `docker/metadata-action` to generate consistent tags and OCI labels
- [ ] Enable multi-architecture builds (amd64 + arm64) for broad compatibility
- [ ] Authenticate with OIDC / workload identity where supported (avoid long-lived tokens)
- [ ] Set up image retention policies to clean up untagged and old images
- [ ] Add `org.opencontainers.image.source` label to link images to source repositories
- [ ] Cache Docker layers in CI to speed up builds (gha cache or registry cache)
- [ ] Sign images with cosign for supply chain security (cross-reference container-security skill)
- [ ] Scan images before publishing (cross-reference container-security skill)
- [ ] Use access tokens with minimal scopes instead of account passwords
- [ ] Test multi-arch images on target platforms before publishing

## Resources

### Official Documentation
- **GHCR**: https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry
- **Docker Hub**: https://docs.docker.com/docker-hub/
- **AWS ECR**: https://docs.aws.amazon.com/AmazonECR/latest/userguide/
- **Azure ACR**: https://learn.microsoft.com/en-us/azure/container-registry/

### CI/CD Actions
- **docker/login-action**: https://github.com/docker/login-action
- **docker/build-push-action**: https://github.com/docker/build-push-action
- **docker/metadata-action**: https://github.com/docker/metadata-action
- **docker/setup-buildx-action**: https://github.com/docker/setup-buildx-action
- **docker/setup-qemu-action**: https://github.com/docker/setup-qemu-action

### Multi-Architecture
- **Docker Buildx**: https://docs.docker.com/build/building/multi-platform/
- **QEMU User Emulation**: https://github.com/multiarch/qemu-user-static

### Image Signing and Security
- **cosign**: https://docs.sigstore.dev/cosign/overview/
- **Docker Content Trust**: https://docs.docker.com/engine/security/trust/
- **Notation**: https://notaryproject.dev/

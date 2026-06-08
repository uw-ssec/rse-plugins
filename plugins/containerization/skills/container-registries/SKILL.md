---
name: container-registries
description: Use when the user needs to publish or push container images, set up Docker registry authentication, configure CI/CD pipelines for container deployment, or work with GHCR, Docker Hub, ECR, or ACR. Creates and updates publishing workflows, tagging strategy, and multi-architecture build pipelines with post-push validation.
metadata:
  references:
    - references/ghcr-publishing.md
    - references/ci-image-publishing.md
    - references/registry-operations.md
  assets:
    - assets/ghcr-publish-workflow.yml
    - assets/docker-hub-publish-workflow.yml
---

# Container Registries

## Use When

- The user asks to publish/push container images to GHCR, Docker Hub, ECR, or ACR.
- The user asks for `docker`/CI workflow setup for registry authentication.
- The user asks about image tags (`latest`, semver, SHA) or release-triggered publishing.
- The user needs multi-architecture image builds (`linux/amd64`, `linux/arm64`).

## Primary Actions

- Generate or update CI workflows for registry login, build, and push.
- Configure tag generation strategy (semver + SHA + optional latest/edge).
- Configure Buildx/QEMU for multi-architecture builds.
- Add post-publish validation commands and recovery checks.

## Quick Commands

```bash
# Login examples
echo "$GITHUB_TOKEN" | docker login ghcr.io -u USERNAME --password-stdin
echo "$DOCKERHUB_TOKEN" | docker login -u USERNAME --password-stdin

# Build and push multi-arch
docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/myorg/myapp:v1.2.3 --push .

# Post-publish validation
docker buildx imagetools inspect ghcr.io/myorg/myapp:v1.2.3
docker manifest inspect ghcr.io/myorg/myapp:v1.2.3
```

## Validation-First Publishing Workflow

1. **Authenticate** with registry credentials or OIDC.
2. **Build and push** with deterministic tags.
3. **Validate image exists** with `imagetools inspect`.
4. **Validate multi-arch manifest** with `docker manifest inspect`.
5. **Smoke pull** target tag to confirm availability.
6. **If failed:** check auth scopes/role permissions, tag generation, and pushed digest.

## Registry Selection (Quick)

| Scenario | Recommended Registry |
|----------|----------------------|
| GitHub-hosted open-source project | GHCR |
| Broadest public distribution | Docker Hub |
| AWS deployment target | ECR |
| Azure deployment target | ACR |

## Keep SKILL.md Lean; Use Deep References

- GHCR details (tokens, visibility, repo linking, package management):
  [references/ghcr-publishing.md](references/ghcr-publishing.md)
- CI build/push details (build-push-action, matrix multi-arch, cache, release patterns):
  [references/ci-image-publishing.md](references/ci-image-publishing.md)
- Authentication workflows, post-publish validation, failure recovery, and retention:
  [references/registry-operations.md](references/registry-operations.md)

## Ready-to-Use Workflows

- [assets/ghcr-publish-workflow.yml](assets/ghcr-publish-workflow.yml)
- [assets/docker-hub-publish-workflow.yml](assets/docker-hub-publish-workflow.yml)

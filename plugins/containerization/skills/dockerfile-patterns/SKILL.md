---
name: dockerfile-patterns
description: Use when the user asks about writing, optimizing, or debugging Dockerfiles, containerizing applications, or building Docker images with docker build. Covers multi-stage builds, layer caching, base image selection, security hardening, and language-specific patterns for Python, Node, Rust, R, Go, Julia, and C/C++.
metadata:
  references:
    - references/multi-stage-builds.md
    - references/layer-caching.md
    - references/base-image-selection.md
    - references/build-validation-and-ops.md
  assets:
    - assets/python-dockerfile.dockerfile
    - assets/node-dockerfile.dockerfile
    - assets/rust-dockerfile.dockerfile
    - assets/r-dockerfile.dockerfile
---

# Dockerfile Patterns

## Primary Actions

- Create production-ready Dockerfiles for common language stacks.
- Reduce image size with multi-stage build separation.
- Improve build speed with layer-cache-friendly ordering.
- Apply baseline security hardening defaults.
- Choose fit-for-purpose base images for runtime constraints.

## Quick Build Pattern

```dockerfile
FROM python:3.11 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt
COPY . .

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY --from=builder /app /app
RUN useradd -u 1001 -m appuser
USER 1001
ENTRYPOINT ["python", "-m", "myapp"]
```

## Validation Workflow

1. Build the image (`docker build`).
2. Run startup check (`docker run --rm <image> --help` or equivalent).
3. For services, run a smoke check with expected command/port.
4. Run vulnerability scan before release (`trivy image` or `docker scout cves`).
5. If validation fails, revise Dockerfile and rebuild.

## Language Templates

- [assets/python-dockerfile.dockerfile](assets/python-dockerfile.dockerfile)
- [assets/node-dockerfile.dockerfile](assets/node-dockerfile.dockerfile)
- [assets/rust-dockerfile.dockerfile](assets/rust-dockerfile.dockerfile)
- [assets/r-dockerfile.dockerfile](assets/r-dockerfile.dockerfile)

## Deep References

- Multi-stage design patterns:
  [references/multi-stage-builds.md](references/multi-stage-builds.md)
- Layer caching patterns and cache debugging:
  [references/layer-caching.md](references/layer-caching.md)
- Base image selection decision guidance:
  [references/base-image-selection.md](references/base-image-selection.md)
- Validation gates, `.dockerignore`, security defaults, and common failure patterns:
  [references/build-validation-and-ops.md](references/build-validation-and-ops.md)

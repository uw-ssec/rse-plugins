---
name: dockerfile-patterns
description: Core Dockerfile best practices including multi-stage builds, layer caching, security hardening, base image selection, and language-specific patterns for Python, Node, Rust, R, Go, Julia, and C/C++.
metadata:
  references:
    - references/multi-stage-builds.md
    - references/layer-caching.md
    - references/base-image-selection.md
  assets:
    - assets/python-dockerfile.dockerfile
    - assets/node-dockerfile.dockerfile
    - assets/rust-dockerfile.dockerfile
    - assets/r-dockerfile.dockerfile
---

# Dockerfile Patterns

A comprehensive guide to writing production-quality Dockerfiles for research software. This skill covers Dockerfile instruction usage, multi-stage build patterns, layer caching strategies, base image selection, security hardening, and language-specific templates for Python, Node.js, Rust, R, Go, Julia, and C/C++. These patterns help produce container images that are small, secure, reproducible, and fast to build.

## Resources in This Skill

This skill includes supporting materials for Dockerfile authoring tasks:

**References** (detailed guides -- consult the table of contents in each file and read specific sections as needed):
- `references/multi-stage-builds.md` - Multi-stage build patterns: build vs runtime separation, builder patterns by language (Python, Node, Rust, Go, C/C++), distroless and scratch final images, build arguments, conditional stages, and CI vs production targets
- `references/layer-caching.md` - Layer caching mechanics: how Docker caches layers, dependency-first patterns, BuildKit cache mounts for pip/npm/cargo/apt, CI caching strategies (GitHub Actions, registry cache, inline cache), and debugging cache misses
- `references/base-image-selection.md` - Base image selection: image families (official, distroless, alpine, slim, scratch), comparison tables, language runtime images, pinning strategies (tag, digest), update cadence, and a decision tree for choosing the right base

**Assets** (ready-to-use Dockerfile templates):
- `assets/python-dockerfile.dockerfile` - Multi-stage Python Dockerfile with uv/pip, virtual environment copying, non-root user, and health check
- `assets/node-dockerfile.dockerfile` - Multi-stage Node.js Dockerfile with npm ci, production-only dependencies, and non-root user
- `assets/rust-dockerfile.dockerfile` - Multi-stage Rust Dockerfile with cargo-chef dependency caching, release build, and distroless final image
- `assets/r-dockerfile.dockerfile` - R Dockerfile based on rocker/r-ver with pak package management and non-root user

## Quick Reference Card

### Base Images by Language

| Language | Base Image | Slim Variant | Size (approx.) |
|----------|-----------|--------------|-----------------|
| Python | `python:3.12` | `python:3.12-slim` | 1 GB / 150 MB |
| Node.js | `node:22` | `node:22-slim` | 1 GB / 200 MB |
| Rust | `rust:1.82` | N/A (use multi-stage) | 1.5 GB / <50 MB final |
| R | `rocker/r-ver:4.4` | N/A | 800 MB |
| Go | `golang:1.23` | N/A (use scratch) | 800 MB / <20 MB final |
| Julia | `julia:1.11` | N/A | 500 MB |
| C/C++ | `gcc:14` / `ubuntu:24.04` | N/A (use multi-stage) | varies |

### Essential Dockerfile Instructions at a Glance

| Instruction | Purpose | Example |
|-------------|---------|---------|
| `FROM` | Set base image | `FROM python:3.12-slim AS build` |
| `RUN` | Execute command in new layer | `RUN pip install --no-cache-dir -r requirements.txt` |
| `COPY` | Copy files from context or stage | `COPY --from=build /app /app` |
| `WORKDIR` | Set working directory | `WORKDIR /app` |
| `ENTRYPOINT` | Set main executable | `ENTRYPOINT ["python", "-m", "myapp"]` |
| `CMD` | Default arguments to entrypoint | `CMD ["--help"]` |
| `ARG` | Build-time variable | `ARG PYTHON_VERSION=3.12` |
| `ENV` | Runtime environment variable | `ENV PYTHONUNBUFFERED=1` |
| `EXPOSE` | Document listening port | `EXPOSE 8000` |
| `HEALTHCHECK` | Container health probe | `HEALTHCHECK CMD curl -f http://localhost:8000/health` |
| `USER` | Set non-root user | `USER 1001` |
| `LABEL` | Add metadata | `LABEL org.opencontainers.image.source="https://..."` |

## When to Use

Use this skill when you need to:

- Write a new Dockerfile for a research software project
- Reduce Docker image size using multi-stage builds
- Speed up Docker builds by improving layer caching
- Choose the right base image for a given language or runtime
- Harden a Dockerfile for production (non-root user, minimal surface area, no secrets)
- Containerize applications in Python, Node.js, Rust, R, Go, Julia, or C/C++
- Debug slow Docker builds or cache invalidation issues
- Set up .dockerignore to avoid copying unnecessary files
- Add health checks, OCI labels, or other production metadata to images

## Dockerfile Instruction Reference

### FROM

Sets the base image for a build stage. Every Dockerfile must start with `FROM`. Use `AS` to name stages in multi-stage builds.

```dockerfile
# Single stage
FROM python:3.12-slim

# Named stages for multi-stage builds
FROM rust:1.82 AS builder
FROM debian:bookworm-slim AS runtime
```

Pin images to specific versions rather than using `latest` to ensure reproducible builds.

### RUN

Executes a command and commits the result as a new layer. Combine related commands with `&&` to reduce layers, and clean up caches in the same layer to keep images small.

```dockerfile
# Bad: creates three layers, apt cache persists
RUN apt-get update
RUN apt-get install -y curl
RUN rm -rf /var/lib/apt/lists/*

# Good: single layer, cache cleaned
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*
```

### COPY

Copies files from the build context or from a previous build stage. Prefer `COPY` over `ADD` unless you need URL fetching or tar auto-extraction.

```dockerfile
# Copy from build context
COPY requirements.txt .
COPY src/ ./src/

# Copy from a named build stage
COPY --from=builder /app/target/release/myapp /usr/local/bin/myapp
```

### WORKDIR

Sets the working directory for subsequent instructions. Creates the directory if it does not exist. Prefer `WORKDIR` over `RUN mkdir && cd`.

```dockerfile
WORKDIR /app
```

### ENTRYPOINT and CMD

`ENTRYPOINT` defines the main executable. `CMD` provides default arguments that can be overridden at runtime. Always use the exec form (JSON array) to ensure proper signal handling.

```dockerfile
# Exec form (preferred) -- PID 1 receives signals correctly
ENTRYPOINT ["python", "-m", "myapp"]
CMD ["--port", "8000"]

# Shell form (avoid) -- runs under /bin/sh, signals not forwarded
ENTRYPOINT python -m myapp
```

### ARG and ENV

`ARG` defines build-time variables (not available at runtime). `ENV` sets runtime environment variables that persist in the image.

```dockerfile
# Build-time only
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim

# Runtime
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
```

### EXPOSE

Documents which ports the container listens on. This is metadata only -- it does not publish the port. Use `-p` at runtime to publish.

```dockerfile
EXPOSE 8000
```

### HEALTHCHECK

Defines a command to test whether the container is healthy. The Docker daemon runs this periodically.

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

### USER

Sets the user (and optionally group) for subsequent instructions and the running container. Always switch to a non-root user before `ENTRYPOINT`.

```dockerfile
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --shell /bin/false appuser
USER 1001
```

### LABEL

Adds metadata to the image. Use OCI standard label keys for interoperability.

```dockerfile
LABEL org.opencontainers.image.title="My App" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.source="https://github.com/org/repo" \
      org.opencontainers.image.licenses="MIT"
```

## Multi-Stage Build Patterns

Multi-stage builds separate the build environment from the runtime environment, producing smaller and more secure final images. The build stage installs compilers, development headers, and build tools. The runtime stage copies only the compiled artifacts or installed packages.

See `references/multi-stage-builds.md` for full coverage including per-language builder patterns, distroless and scratch final images, build arguments, conditional stages, and CI vs production targets.

**Basic pattern:**

```dockerfile
# Stage 1: Build
FROM python:3.12 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt
COPY . .

# Stage 2: Runtime
FROM python:3.12-slim
COPY --from=builder /install /usr/local
COPY --from=builder /app /app
WORKDIR /app
USER 1001
ENTRYPOINT ["python", "-m", "myapp"]
```

## Language-Specific Patterns

### Python (pip / uv / conda)

Python Dockerfiles should install dependencies in a virtual environment or with `--prefix` so they can be copied cleanly to a slim runtime image. Pin dependency versions with a lockfile.

```dockerfile
# Using uv (fast Python package installer)
FROM python:3.12-slim AS builder
RUN pip install uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY . .

FROM python:3.12-slim
COPY --from=builder /app /app
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
USER 1001
ENTRYPOINT ["python", "-m", "myapp"]
```

See `assets/python-dockerfile.dockerfile` for a complete template.

### Node.js (npm / yarn)

Use `npm ci` for deterministic installs. Copy `package.json` and `package-lock.json` first to leverage caching. In the runtime stage, install only production dependencies.

```dockerfile
FROM node:22-slim AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:22-slim
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev
COPY --from=builder /app/dist ./dist
USER 1001
ENTRYPOINT ["node", "dist/index.js"]
```

See `assets/node-dockerfile.dockerfile` for a complete template.

### Rust (cargo)

Rust benefits significantly from multi-stage builds because the compiler toolchain is large (~1.5 GB). Use `cargo-chef` for dependency caching, then copy only the release binary to a minimal final image.

```dockerfile
FROM rust:1.82 AS chef
RUN cargo install cargo-chef
WORKDIR /app

FROM chef AS planner
COPY . .
RUN cargo chef prepare --recipe-path recipe.json

FROM chef AS builder
COPY --from=planner /app/recipe.json recipe.json
RUN cargo chef cook --release --recipe-path recipe.json
COPY . .
RUN cargo build --release

FROM gcr.io/distroless/cc-debian12
COPY --from=builder /app/target/release/myapp /usr/local/bin/myapp
ENTRYPOINT ["myapp"]
```

See `assets/rust-dockerfile.dockerfile` for a complete template.

### R (pak / renv)

R Dockerfiles use the `rocker/r-ver` base image family. Use `pak` for fast, reliable package installation. System library dependencies are the main challenge -- `pak` can detect and install them automatically.

```dockerfile
FROM rocker/r-ver:4.4
RUN R -e "install.packages('pak', repos = 'https://r-lib.github.io/p/pak/stable/')"
WORKDIR /app
COPY DESCRIPTION .
RUN R -e "pak::local_install_deps()"
COPY . .
USER 1001
ENTRYPOINT ["Rscript", "main.R"]
```

See `assets/r-dockerfile.dockerfile` for a complete template.

### Go

Go produces statically linked binaries by default, making it ideal for scratch or distroless final images.

```dockerfile
FROM golang:1.23 AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /app/myapp ./cmd/myapp

FROM scratch
COPY --from=builder /app/myapp /myapp
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
ENTRYPOINT ["/myapp"]
```

### Julia

Julia containers should precompile packages in the build stage to avoid startup latency at runtime.

```dockerfile
FROM julia:1.11 AS builder
WORKDIR /app
COPY Project.toml Manifest.toml ./
RUN julia --project=. -e 'using Pkg; Pkg.instantiate(); Pkg.precompile()'
COPY . .

FROM julia:1.11
WORKDIR /app
COPY --from=builder /app /app
USER 1001
ENTRYPOINT ["julia", "--project=.", "main.jl"]
```

### C/C++

C/C++ projects need compilers and build tools only during the build stage. Copy the compiled binary and its runtime library dependencies to a minimal final image.

```dockerfile
FROM ubuntu:24.04 AS builder
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential cmake && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
RUN cmake -B build -DCMAKE_BUILD_TYPE=Release && \
    cmake --build build --parallel

FROM ubuntu:24.04
RUN apt-get update && \
    apt-get install -y --no-install-recommends libstdc++6 && \
    rm -rf /var/lib/apt/lists/*
COPY --from=builder /app/build/myapp /usr/local/bin/myapp
USER 1001
ENTRYPOINT ["myapp"]
```

## .dockerignore Best Practices

A `.dockerignore` file excludes files from the build context, reducing build time and preventing sensitive or unnecessary files from entering the image.

```
# Version control
.git
.gitignore

# CI/CD
.github/
.gitlab-ci.yml

# IDE and editor files
.vscode/
.idea/
*.swp
*.swo

# Documentation
docs/
*.md
!README.md

# Test and development files
tests/
__pycache__/
*.pyc
.pytest_cache/
.coverage
htmlcov/
node_modules/
.tox/
.nox/

# Build artifacts (language-specific)
target/          # Rust
dist/            # Python/Node (if rebuilding in container)
build/           # C/C++/general

# Environment and secrets
.env
.env.*
*.pem
*.key
credentials.json

# Docker files (avoid recursive builds)
Dockerfile*
docker-compose*.yml
.dockerignore
```

**Key principle:** Start by ignoring everything, then explicitly include what the build needs. This is safer than trying to exclude everything harmful:

```
# Ignore everything
*

# Allow only what the build needs
!src/
!pyproject.toml
!uv.lock
!README.md
```

## Security Defaults

### Non-Root USER

Never run containers as root in production. Create a dedicated user and switch before `ENTRYPOINT`.

```dockerfile
# Create a non-root user
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --create-home --shell /bin/false appuser

# Own application files
RUN chown -R 1001:1001 /app

# Switch to non-root
USER 1001
```

### Minimal Base Images

Use the smallest base image that meets your requirements. Fewer packages mean fewer CVEs.

| Image | Shell | Package Manager | glibc | Use When |
|-------|-------|----------------|-------|----------|
| `scratch` | No | No | No | Static binaries (Go, Rust) |
| `distroless` | No | No | Yes | Compiled languages needing glibc |
| `alpine` | Yes | apk | musl | Need shell but want minimal image |
| `*-slim` | Yes | apt | Yes | Need apt but want smaller image |

### No Secrets in Images

Never embed secrets (API keys, passwords, tokens) in Dockerfiles. They persist in image layers even if deleted in a later layer.

```dockerfile
# WRONG: secret persists in layer history
RUN echo "password123" > /app/.env
RUN rm /app/.env  # still in previous layer!

# WRONG: build arg visible in docker history
ARG DB_PASSWORD
RUN echo $DB_PASSWORD > /tmp/init.sql

# RIGHT: use runtime secrets
ENV DB_HOST=db.example.com
# Pass secrets at runtime: docker run -e DB_PASSWORD=... myapp
# Or use Docker secrets / mounted credential files
```

## Common Mistakes

1. **Using `latest` tag** -- Always pin base image versions for reproducible builds. `FROM python:latest` may break without warning when the upstream image updates.

2. **Running as root** -- Containers run as root by default. Always add `USER` before `ENTRYPOINT` to drop privileges.

3. **Copying everything before installing dependencies** -- `COPY . .` before `RUN pip install` invalidates the dependency cache on every source code change. Copy only the lockfile first.

4. **Not using .dockerignore** -- Without it, the entire build context (including `.git`, `node_modules`, test data) is sent to the daemon, slowing builds and bloating images.

5. **Installing dev dependencies in production images** -- Use `--omit=dev`, `--no-dev`, or multi-stage builds to exclude development-only packages from the final image.

6. **Shell form for ENTRYPOINT** -- `ENTRYPOINT python app.py` runs under `/bin/sh -c`, which does not forward signals. Use exec form: `ENTRYPOINT ["python", "app.py"]`.

7. **Embedding secrets in layers** -- Build arguments and files added in earlier layers are visible in `docker history`. Use runtime environment variables or mounted secrets instead.

8. **Not cleaning up in the same layer** -- `RUN apt-get install && rm -rf /var/lib/apt/lists/*` must be one layer. Cleaning up in a separate `RUN` does not reduce image size because the previous layer still contains the cache.

9. **Missing HEALTHCHECK** -- Without a health check, orchestrators cannot distinguish between a running container and a healthy one. Add `HEALTHCHECK` for any long-running service.

10. **Ignoring multi-platform builds** -- If your image runs on both amd64 and arm64, test on both. Some packages (especially compiled Python extensions) may not have pre-built wheels for all architectures.

## Best Practices

- [ ] Pin base image versions (`python:3.12-slim`, not `python:latest`)
- [ ] Use multi-stage builds to separate build and runtime environments
- [ ] Copy dependency lockfiles before source code for optimal caching
- [ ] Use `--no-cache-dir` (pip) or `npm ci` for deterministic installs
- [ ] Combine related `RUN` commands with `&&` to minimize layers
- [ ] Clean up package manager caches in the same layer they are created
- [ ] Add a `.dockerignore` to exclude unnecessary files from the build context
- [ ] Run as a non-root `USER` (UID 1001+)
- [ ] Use exec form `["..."]` for `ENTRYPOINT` and `CMD`
- [ ] Add `HEALTHCHECK` for long-running services
- [ ] Add OCI `LABEL` metadata (source, version, license)
- [ ] Never embed secrets in the image; use runtime environment variables or mounted secrets
- [ ] Use BuildKit cache mounts (`--mount=type=cache`) for package manager caches
- [ ] Scan images for vulnerabilities with `docker scout`, `trivy`, or `grype`
- [ ] Keep final images under 500 MB for interpreted languages, under 50 MB for compiled languages

## Resources

### Official Documentation
- **Dockerfile Reference**: https://docs.docker.com/reference/dockerfile/
- **Docker Build Best Practices**: https://docs.docker.com/build/building/best-practices/
- **BuildKit**: https://docs.docker.com/build/buildkit/
- **Multi-Stage Builds**: https://docs.docker.com/build/building/multi-stage/

### Base Image Sources
- **Docker Official Images**: https://hub.docker.com/search?image_filter=official
- **Google Distroless**: https://github.com/GoogleContainerTools/distroless
- **Chainguard Images**: https://www.chainguard.dev/chainguard-images
- **Rocker Project (R)**: https://rocker-project.org/

### Security and Scanning
- **Docker Scout**: https://docs.docker.com/scout/
- **Trivy**: https://github.com/aquasecurity/trivy
- **Grype**: https://github.com/anchore/grype
- **Snyk Container**: https://snyk.io/product/container-vulnerability-management/

### Language-Specific Guides
- **Python in Docker**: https://docs.docker.com/language/python/
- **Node.js in Docker**: https://docs.docker.com/language/nodejs/
- **Rust in Docker**: https://docs.docker.com/language/rust/
- **Go in Docker**: https://docs.docker.com/language/golang/
- **Rocker R Images**: https://rocker-project.org/images/

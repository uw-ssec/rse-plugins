# Multi-Stage Builds -- Deep Reference

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| Why Multi-Stage | 17-66 | Build vs runtime separation, image size, security benefits |
| Basic Two-Stage Pattern | 68-128 | Generic template with detailed comments |
| Builder Pattern by Language | 130-316 | Python, Node, Rust, Go, C/C++ builder patterns |
| Minimizing Final Image | 318-382 | Copy only artifacts, distroless, scratch |
| Build Arguments and Conditional Stages | 384-461 | ARG, target stages, conditional logic |
| CI vs Production Targets | 463-548 | --target flag, docker-bake, stage selection |
| Common Mistakes | 550-636 | Leaking build tools, missing libraries, wrong COPY paths |

---

## Why Multi-Stage

### Build vs Runtime Separation

A typical build environment includes compilers, development headers, build tools, and source code. None of these belong in a production image. Multi-stage builds let you use a full build environment in one stage and copy only the compiled output to a minimal runtime stage.

**Without multi-stage (everything in one image):**

```dockerfile
FROM python:3.12
RUN apt-get update && apt-get install -y build-essential
COPY . /app
WORKDIR /app
RUN pip install .
# Image contains: compiler, headers, source, pip cache, final app
# Typical size: 1.2 GB
```

**With multi-stage (build separated from runtime):**

```dockerfile
FROM python:3.12 AS builder
RUN apt-get update && apt-get install -y build-essential
COPY . /app
WORKDIR /app
RUN pip install --prefix=/install .

FROM python:3.12-slim
COPY --from=builder /install /usr/local
# Image contains: only the runtime and installed packages
# Typical size: 200 MB
```

### Image Size

Smaller images mean faster pulls, faster deployments, less storage cost, and reduced attack surface. Multi-stage builds routinely reduce image sizes by 5-10x.

| Language | Single-stage | Multi-stage | Reduction |
|----------|-------------|-------------|-----------|
| Python | 1.2 GB | 150-250 MB | 5-8x |
| Node.js | 1.0 GB | 150-200 MB | 5-7x |
| Rust | 1.5 GB | 20-80 MB | 20-75x |
| Go | 800 MB | 5-20 MB | 40-160x |
| C/C++ | 600 MB | 10-50 MB | 12-60x |

### Security

Build stages may contain credentials for private registries, source code you do not want to distribute, and tools with known vulnerabilities. None of these carry over to the final stage unless you explicitly `COPY` them.

---

## Basic Two-Stage Pattern

The fundamental multi-stage pattern uses two stages: `builder` and `runtime`.

```dockerfile
# ==============================================================================
# Stage 1: Builder
# Purpose: Install dependencies, compile code, prepare artifacts
# This stage is discarded after build -- its contents do not affect final image
# ==============================================================================
FROM <base-image-with-build-tools> AS builder

# Set working directory for the build
WORKDIR /app

# Copy dependency specification first (for layer caching)
# Only re-runs install when these files change
COPY <lockfile> <manifest> ./

# Install dependencies
# Use --prefix, --target, or virtual environment to isolate installed packages
RUN <install-dependencies-command>

# Copy the rest of the source code
# This layer is invalidated on every source change, but dependencies are cached
COPY . .

# Build/compile the application
RUN <build-command>

# ==============================================================================
# Stage 2: Runtime
# Purpose: Minimal image containing only what is needed to run the application
# This is the final image that gets tagged and pushed
# ==============================================================================
FROM <minimal-base-image> AS runtime

# Set working directory
WORKDIR /app

# Copy only the built artifacts from the builder stage
COPY --from=builder /app/<artifact> ./<artifact>

# Create non-root user
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --shell /bin/false appuser
USER 1001

# Document the port
EXPOSE <port>

# Health check for orchestrators
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD <health-check-command> || exit 1

# Use exec form for proper signal handling
ENTRYPOINT ["<executable>"]
CMD ["<default-args>"]
```

---

## Builder Pattern by Language

### Python

Python dependencies should be installed into a virtual environment or `--prefix` directory that can be cleanly copied to the runtime stage.

```dockerfile
# Builder: full Python image with build tools for compiled extensions
FROM python:3.12 AS builder

# Install system build dependencies for compiled packages (numpy, scipy, etc.)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gfortran \
        libopenblas-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy and install the application
COPY . .
RUN pip install --no-cache-dir .

# Runtime: slim image with only the Python runtime
FROM python:3.12-slim

# Copy the virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY --from=builder /app /app

USER 1001
ENTRYPOINT ["python", "-m", "myapp"]
```

**Using uv (faster alternative to pip):**

```dockerfile
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

### Node.js

Node builds typically produce a `dist/` directory from a build step. The runtime stage only needs `node_modules` (production) and the built output.

```dockerfile
FROM node:22-slim AS builder
WORKDIR /app

# Install all dependencies (including devDependencies for build)
COPY package.json package-lock.json ./
RUN npm ci

# Build the application (TypeScript compile, webpack, etc.)
COPY . .
RUN npm run build

# Runtime: fresh install with production dependencies only
FROM node:22-slim
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --omit=dev && npm cache clean --force

# Copy built output from builder
COPY --from=builder /app/dist ./dist

USER 1001
EXPOSE 3000
ENTRYPOINT ["node", "dist/index.js"]
```

### Rust

Rust compiles to native binaries. The build stage is large (compiler + crate registry) but the final binary can run on scratch or distroless.

```dockerfile
FROM rust:1.82 AS chef
RUN cargo install cargo-chef
WORKDIR /app

# Plan: analyze dependencies without building
FROM chef AS planner
COPY . .
RUN cargo chef prepare --recipe-path recipe.json

# Build: install dependencies first (cached), then build
FROM chef AS builder
COPY --from=planner /app/recipe.json recipe.json
RUN cargo chef cook --release --recipe-path recipe.json
COPY . .
RUN cargo build --release

# Runtime: minimal image with just the binary
FROM gcr.io/distroless/cc-debian12
COPY --from=builder /app/target/release/myapp /usr/local/bin/myapp
USER 1001
ENTRYPOINT ["myapp"]
```

### Go

Go produces statically linked binaries by default with `CGO_ENABLED=0`, so the final image can use `scratch`.

```dockerfile
FROM golang:1.23 AS builder
WORKDIR /app

# Download dependencies first for caching
COPY go.mod go.sum ./
RUN go mod download

# Build static binary
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /app/myapp ./cmd/myapp

# Runtime: empty image
FROM scratch
# Copy CA certificates for HTTPS
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
# Copy timezone data if needed
COPY --from=builder /usr/share/zoneinfo /usr/share/zoneinfo
COPY --from=builder /app/myapp /myapp

USER 1001
EXPOSE 8080
ENTRYPOINT ["/myapp"]
```

### C/C++

C/C++ projects need compilers and build systems only during the build stage. Identify runtime library dependencies with `ldd` and copy them to the final image.

```dockerfile
FROM ubuntu:24.04 AS builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        pkg-config \
        libssl-dev \
        libcurl4-openssl-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
RUN cmake -B build -DCMAKE_BUILD_TYPE=Release && \
    cmake --build build --parallel $(nproc)

# Runtime: only the binary and its runtime dependencies
FROM ubuntu:24.04
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libssl3 \
        libcurl4 && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/build/myapp /usr/local/bin/myapp
USER 1001
ENTRYPOINT ["myapp"]
```

---

## Minimizing Final Image

### Copy Only Artifacts

The single most important rule: copy only what the application needs to run. Everything else stays in the builder stage.

| Language | What to Copy | What to Leave Behind |
|----------|-------------|---------------------|
| Python | Virtual environment, app code | pip cache, build-essential, .pyc files |
| Node.js | `node_modules` (prod), `dist/` | devDependencies, src/, test/ |
| Rust | Release binary | Compiler, crate registry, target/debug |
| Go | Static binary, CA certs | Compiler, GOPATH, go.sum |
| C/C++ | Binary, runtime .so files | Compiler, cmake, headers, .o files |

### Using Distroless

Google's distroless images contain only a language runtime and its dependencies. No shell, no package manager, no utilities. This minimizes attack surface.

```dockerfile
# Python distroless
FROM gcr.io/distroless/python3-debian12
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
ENV PYTHONPATH=/opt/venv/lib/python3.12/site-packages
ENTRYPOINT ["python", "-m", "myapp"]

# Java distroless
FROM gcr.io/distroless/java21-debian12
COPY --from=builder /app/target/myapp.jar /app/myapp.jar
ENTRYPOINT ["java", "-jar", "/app/myapp.jar"]

# Static binary (C, Go, Rust without glibc)
FROM gcr.io/distroless/static-debian12
COPY --from=builder /app/myapp /myapp
ENTRYPOINT ["/myapp"]

# Binary needing glibc (Rust with glibc, C/C++)
FROM gcr.io/distroless/cc-debian12
COPY --from=builder /app/myapp /myapp
ENTRYPOINT ["/myapp"]
```

**Trade-offs:**
- No shell means you cannot `docker exec` into the container for debugging
- No package manager means no runtime patching
- Use `:debug` variants (e.g., `gcr.io/distroless/cc-debian12:debug`) during development -- these include a busybox shell

### Using Scratch

`scratch` is the empty image -- zero bytes, zero files. Suitable only for fully static binaries.

```dockerfile
FROM scratch
COPY --from=builder /app/myapp /myapp
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
ENTRYPOINT ["/myapp"]
```

**Requirements for scratch:**
- Binary must be statically linked (no dynamic library dependencies)
- Must copy CA certificates if making HTTPS requests
- Must copy timezone data if using `time.Local`
- No USER instruction (no `/etc/passwd`), but you can use numeric UID

---

## Build Arguments and Conditional Stages

### ARG with FROM

Build arguments can parameterize the base image version:

```dockerfile
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim AS builder
# ...

FROM python:${PYTHON_VERSION}-slim AS runtime
# ...
```

Build with a different version:

```bash
docker build --build-arg PYTHON_VERSION=3.11 -t myapp:py311 .
```

### Target Stages

You can stop the build at a specific stage using `--target`:

```dockerfile
FROM python:3.12 AS builder
# ... install and build ...

FROM python:3.12-slim AS test
COPY --from=builder /opt/venv /opt/venv
COPY . .
RUN pytest

FROM python:3.12-slim AS production
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
USER 1001
ENTRYPOINT ["python", "-m", "myapp"]
```

```bash
# Run tests only
docker build --target test -t myapp:test .

# Build production image (skips test stage unless it is a dependency)
docker build --target production -t myapp:prod .
```

### Conditional Installation

Use build arguments to toggle features:

```dockerfile
ARG INSTALL_DEV=false

FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements*.txt ./

RUN if [ "$INSTALL_DEV" = "true" ]; then \
        pip install --no-cache-dir -r requirements-dev.txt; \
    else \
        pip install --no-cache-dir -r requirements.txt; \
    fi

COPY . .
```

```bash
# Production
docker build -t myapp:prod .

# Development (with dev dependencies)
docker build --build-arg INSTALL_DEV=true -t myapp:dev .
```

---

## CI vs Production Targets

### Using --target in CI

Structure your Dockerfile with named stages that CI can target independently:

```dockerfile
# Base dependencies shared by all stages
FROM python:3.12-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Linting stage
FROM base AS lint
RUN pip install --no-cache-dir ruff mypy
COPY . .
RUN ruff check . && mypy .

# Test stage
FROM base AS test
RUN pip install --no-cache-dir pytest pytest-cov
COPY . .
RUN pytest --cov=myapp

# Production stage
FROM python:3.12-slim AS production
COPY --from=base /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . /app
WORKDIR /app
USER 1001
ENTRYPOINT ["python", "-m", "myapp"]
```

CI pipeline:

```yaml
steps:
  - name: Lint
    run: docker build --target lint .
  - name: Test
    run: docker build --target test .
  - name: Build production image
    run: docker build --target production -t myapp:latest .
```

### Docker Bake

For complex multi-target builds, use Docker Bake (`docker-bake.hcl`):

```hcl
# docker-bake.hcl
group "default" {
  targets = ["production"]
}

group "ci" {
  targets = ["lint", "test"]
}

target "lint" {
  target = "lint"
  output = ["type=cacheonly"]
}

target "test" {
  target = "test"
  output = ["type=cacheonly"]
}

target "production" {
  target = "production"
  tags = ["myapp:latest"]
  platforms = ["linux/amd64", "linux/arm64"]
}
```

```bash
# CI: run lint and test
docker buildx bake ci

# Deploy: build production for multiple platforms
docker buildx bake production
```

---

## Common Mistakes

### 1. Leaking Build Tools into the Final Image

```dockerfile
# WRONG: runtime image contains build-essential (300+ MB of compilers)
FROM python:3.12 AS builder
RUN apt-get update && apt-get install -y build-essential
COPY . .
RUN pip install .
# Missing second FROM -- this IS the final image

# RIGHT: separate runtime stage
FROM python:3.12-slim
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
```

### 2. Missing Runtime Libraries

Compiled Python extensions (numpy, pandas, scipy) may depend on shared libraries that exist in the builder but not in the slim runtime.

```dockerfile
# WRONG: numpy needs libopenblas but slim image does not have it
FROM python:3.12-slim
COPY --from=builder /opt/venv /opt/venv
# Crashes at runtime: ImportError: libopenblas.so.0: cannot open shared object file

# RIGHT: install runtime library dependencies in the final stage
FROM python:3.12-slim
RUN apt-get update && \
    apt-get install -y --no-install-recommends libopenblas0 && \
    rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
```

**Debugging:** Run `ldd /opt/venv/lib/python3.12/site-packages/numpy/core/_multiarray_umath.cpython-312-x86_64-linux-gnu.so` in the builder to identify shared library dependencies.

### 3. Wrong COPY Paths

```dockerfile
# WRONG: copies the entire /usr/local, including pip, setuptools, etc.
COPY --from=builder /usr/local /usr/local

# BETTER: copy only site-packages
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# BEST: use a virtual environment for clean isolation
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
```

### 4. Not Using --from with the Correct Stage Name

```dockerfile
# WRONG: stage name is case-sensitive and must match exactly
FROM python:3.12 AS Builder
# ...
COPY --from=builder /app /app  # Error: stage "builder" not found

# RIGHT: match the case
COPY --from=Builder /app /app
```

### 5. Copying Source Code When Only Artifacts Are Needed

```dockerfile
# WRONG: copies entire source tree into runtime image
COPY --from=builder /app /app
# Runtime image now contains: source code, tests, docs, .git, etc.

# RIGHT: copy only what is needed
COPY --from=builder /app/dist /app/dist
COPY --from=builder /opt/venv /opt/venv
```

### 6. Forgetting CA Certificates in Scratch Images

```dockerfile
# WRONG: HTTPS requests will fail
FROM scratch
COPY --from=builder /app/myapp /myapp

# RIGHT: copy certificates
FROM scratch
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /app/myapp /myapp
```

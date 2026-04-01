---
description: Create a Dockerfile for a project by analyzing its language, dependencies, and structure
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Containerize

Create a production-ready Dockerfile by analyzing the project's language, dependencies, and structure.

## Arguments

`$ARGUMENTS` — Optional path to the project directory or a brief description of the project (e.g., `/containerize ./my-api` or `/containerize Python FastAPI service`).

## Input Handling

**If argument provided:**
- If the argument is a path, use it as the project root directory
- If the argument is a description, use it as context for container generation and default to the current working directory

**If no argument provided:**
- Use the current working directory as the project root
- Auto-detect the language and framework from project files

## Information Gathering

Before generating any files, analyze the project to detect:

### Language Detection

Scan the project root for configuration files to determine the primary language and ecosystem:

| File Present | Detected Language |
|-------------|-------------------|
| `pyproject.toml`, `setup.py`, `setup.cfg`, `requirements.txt` | Python |
| `Cargo.toml` | Rust |
| `package.json` | Node.js |
| `go.mod` | Go |
| `Project.toml` | Julia |
| `DESCRIPTION`, `NAMESPACE` | R |
| `CMakeLists.txt`, `Makefile`, `meson.build` | C/C++ |
| `*.sln`, `*.csproj`, `*.fsproj` | .NET |
| `mix.exs` | Elixir |
| `build.gradle`, `pom.xml` | Java |

### Additional Detection

- **Package manager**: pip/uv/conda/poetry (Python), npm/yarn/pnpm (Node), cargo (Rust), etc.
- **Test framework**: pytest, jest, cargo test, go test, testthat, etc.
- **Entry point**: main module, CLI script, server entrypoint, or library package
- **GPU requirements**: Check for CUDA, ROCm, or GPU-related dependencies
- **Multi-service indicators**: Look for docker-compose.yml, multiple service directories, or microservice patterns
- **Dev environment**: Check for `.vscode/` directory presence

## Action Steps

### Step 1: Detect Project Language and Structure

Scan the project root using the detection heuristics above. Determine:

- Primary language and version (e.g., Python 3.12, Node 20, Rust 1.77)
- Package manager and lockfile present
- Whether the project is a library, CLI tool, web service, or notebook-based workflow
- Test framework in use
- Entry point file or command
- Any existing Dockerfile or Containerfile (warn if found)

If multiple languages are detected, ask the user which is the primary language for the container, or suggest a multi-stage approach.

### Step 2: Select Base Image

Reference the `dockerfile-patterns` skill for recommended base images per language:

- **Python**: `python:<version>-slim` (default), `python:<version>-bookworm` (if system deps needed), or `mambaforge` / `condaforge/miniforge3` for conda environments
- **Rust**: `rust:<version>-slim` for build, `debian:bookworm-slim` or `distroless` for runtime
- **Node.js**: `node:<version>-slim` for build, `node:<version>-alpine` for runtime
- **Go**: `golang:<version>` for build, `gcr.io/distroless/static-debian12` for runtime
- **Julia**: `julia:<version>` official image
- **R**: `rocker/r-ver:<version>` from the Rocker project
- **C/C++**: `gcc:<version>` or `debian:bookworm-slim` with build-essential
- **.NET**: `mcr.microsoft.com/dotnet/sdk:<version>` for build, `mcr.microsoft.com/dotnet/runtime:<version>` for runtime

For GPU workloads, reference the `gpu-containers` skill for NVIDIA CUDA or ROCm base images.

### Step 3: Generate Multi-Stage Dockerfile

Generate a Dockerfile using multi-stage builds by default:

**Build stage:**
- Install build dependencies and compilers
- Copy dependency manifests first (for layer caching)
- Install dependencies
- Copy source code
- Run build/compile step if applicable
- Run tests (as a build validation gate)

**Runtime stage:**
- Use minimal base image
- Create a non-root user (e.g., `appuser` with UID 1000)
- Copy only built artifacts and runtime dependencies from build stage
- Set appropriate `WORKDIR`
- Add `HEALTHCHECK` if the project is a service
- Add descriptive `LABEL` metadata (maintainer, version, description, source URL)
- Set `ENTRYPOINT` and/or `CMD`
- Expose ports if applicable

Pin all base image versions to specific tags (never use `latest`). Include inline comments explaining each stage and non-obvious decisions.

### Step 4: Generate .dockerignore

Create a `.dockerignore` file to minimize build context. Include:

**Universal ignores:**
```
.git
.github
.vscode
.idea
*.md
LICENSE
.env
.env.*
docker-compose*.yml
Dockerfile*
.dockerignore
```

**Language-specific ignores** (based on detected language):
- Python: `__pycache__/`, `*.pyc`, `.venv/`, `.tox/`, `.pytest_cache/`, `dist/`, `*.egg-info/`
- Node.js: `node_modules/`, `.next/`, `coverage/`, `.nuxt/`
- Rust: `target/`
- Go: vendor/ (if not vendoring)
- R: `.Rhistory`, `.RData`, `renv/library/`
- Julia: `.julia/`

### Step 5: Generate docker-compose.yml (Conditional)

If multi-service patterns are detected (e.g., separate API and worker directories, database configuration files, or the user describes a multi-service setup):

- Generate a `docker-compose.yml` with service definitions
- Include volume mounts for development
- Add health checks for services
- Define a shared network
- Reference the `compose-orchestration` skill for best practices

If the project is a single service, skip this step.

### Step 6: Generate devcontainer.json (Conditional)

If a `.vscode/` directory is present in the project:

- Create `.devcontainer/devcontainer.json`
- Reference the `devcontainers` skill for configuration patterns
- Include appropriate VS Code extensions for the detected language
- Mount the workspace correctly
- Configure port forwarding if the project is a service

If no `.vscode/` directory is found, skip this step.

## Output Summary

After generating all files, present a summary:

```
## Containerized: <project-name>

### Language Detected: <language> <version>
### Base Image: <base-image>

### Files Created:
- Dockerfile — Multi-stage build (<build-image> -> <runtime-image>)
- .dockerignore — Excludes <N> patterns from build context
- docker-compose.yml — <if generated: service definitions> | <if skipped: not needed>
- .devcontainer/devcontainer.json — <if generated: dev environment> | <if skipped: no .vscode/ detected>

### Build & Run:
  docker build -t <project-name> .
  docker run --rm -p <port>:<port> <project-name>

### Next Steps:
1. Review the generated Dockerfile and adjust versions or dependencies as needed
2. Test the build: `docker build -t <project-name> .`
3. Run the container: `docker run --rm <project-name>`
4. Run `/container-audit` to verify best practices and security
5. (Optional) Push to a registry — see the `container-registries` skill
6. (Optional) Generate Singularity/Apptainer definition — see the `singularity-apptainer` skill
```

## Important Notes

- **Check before overwriting**: If a Dockerfile, .dockerignore, docker-compose.yml, or devcontainer.json already exists, warn the user and ask before overwriting.
- **Multi-stage by default**: Always generate multi-stage Dockerfiles unless the project is trivially simple (e.g., a single-file script). Multi-stage builds reduce image size and attack surface.
- **Pin versions**: Never use `latest` tags for base images. Pin to specific versions (e.g., `python:3.12-slim`, not `python:latest`).
- **Never include secrets**: Do not copy `.env` files, credentials, API keys, or private keys into the container. If the project needs runtime secrets, use environment variables or mount secrets at runtime.
- **Non-root user**: Always create and switch to a non-root user in the runtime stage.
- **Suggest audit**: After generating the Dockerfile, recommend running `/container-audit` to verify best practices and catch any issues.
- **Layer caching**: Order Dockerfile instructions to maximize layer cache hits — copy dependency manifests before source code.
- **Research software considerations**: For scientific computing, ensure numerical libraries (BLAS, LAPACK, HDF5) are correctly linked. For GPU workloads, reference the `gpu-containers` skill.

---
description: Audit an existing Dockerfile or container image for best practices, security, and optimization opportunities
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# Container Audit

Audit a Dockerfile for best practices, security vulnerabilities, and size optimization opportunities.

## Arguments

`$ARGUMENTS` — Optional path to a Dockerfile or container image name (e.g., `/container-audit ./services/api/Dockerfile` or `/container-audit ghcr.io/org/image:v1.2`).

## Input Handling

**If path provided:**
- If the argument is a file path, audit that specific Dockerfile or Containerfile
- If the argument is an image name (contains `/` or `:`), attempt to analyze the image if Docker/Podman is available

**If no argument provided:**
- Search the current working directory for `Dockerfile`, `Containerfile`, `Dockerfile.*`, or `*.dockerfile`
- If multiple Dockerfiles are found, list them and ask the user which to audit
- If none found, report that no Dockerfile was found and suggest running `/containerize` first

## Information Gathering

Before running the audit, collect context:

1. **Read the Dockerfile** — Parse all instructions, stages, and comments
2. **Detect base image(s)** — Identify all `FROM` instructions and their tags/digests
3. **Check for docker-compose.yml** — If present, note service definitions and volume mounts
4. **Check for .dockerignore** — If missing, flag as a finding; if present, assess coverage
5. **Check project language** — Detect from surrounding project files to contextualize recommendations
6. **Check for .devcontainer/** — Note if devcontainer configuration exists

## Audit Categories

### 1. Best Practices

Check the Dockerfile against established best practices:

- **Multi-stage build**: Is the Dockerfile using multi-stage builds to separate build and runtime? Flag single-stage builds that include build tools in the final image.
- **COPY vs ADD**: Flag uses of `ADD` where `COPY` would suffice. `ADD` should only be used for tar extraction or remote URLs.
- **Specific image tags**: Flag use of `latest` tag or missing tags on `FROM` instructions. Recommend pinning to specific versions.
- **WORKDIR usage**: Check that `WORKDIR` is set before `COPY`/`RUN` instructions instead of using `cd` in `RUN` commands.
- **Combined RUN instructions**: Flag sequences of multiple `RUN` instructions that could be combined to reduce layers (e.g., `apt-get update && apt-get install` in separate `RUN` steps).
- **Instruction ordering**: Check that less-frequently-changing instructions come before frequently-changing ones.
- **SHELL instruction**: Check if a non-default shell is set when using shell-specific features.
- **ARG and ENV usage**: Verify build arguments have defaults where appropriate and environment variables are used for runtime configuration.

### 2. Security

Assess security posture of the container:

- **Non-root user**: Check that the final stage runs as a non-root user via `USER` instruction. Flag containers that run as root.
- **Secrets exposure**: Scan for `COPY` or `ADD` of sensitive files (`.env`, `*.pem`, `*.key`, `credentials.*`, `*secret*`). Scan for hardcoded passwords or tokens in `ENV` or `RUN` instructions.
- **Base image age**: If the base image tag is a dated release, flag potentially outdated images with known vulnerabilities.
- **Base image pinning**: Recommend pinning by digest (`@sha256:...`) for reproducible builds in production.
- **HEALTHCHECK**: Check if a `HEALTHCHECK` instruction is defined for service containers.
- **Minimal base image**: Recommend `slim`, `alpine`, or `distroless` variants if a full OS image is used unnecessarily.
- **Package manager cleanup**: Check that `apt-get`, `yum`, or `apk` caches are cleaned in the same `RUN` layer as the install.
- **SUID/SGID binaries**: Recommend removing setuid/setgid binaries in the final image if security-critical.

### 3. Size Optimization

Identify opportunities to reduce image size:

- **Unnecessary packages**: Flag installation of recommended/suggested packages (e.g., `apt-get install` without `--no-install-recommends`).
- **Build artifacts in final stage**: Check that build tools, compilers, and development headers are not present in the final runtime stage.
- **Leftover cache files**: Check for package manager caches, pip cache, npm cache, or temporary files left in the image.
- **.dockerignore coverage**: Verify that `.dockerignore` excludes `.git/`, `node_modules/`, `__pycache__/`, test fixtures, documentation, and other non-essential files.
- **Layer count**: Flag excessive number of layers when instructions could be consolidated.
- **COPY granularity**: Flag `COPY . .` early in the Dockerfile that could be split into dependency-first patterns.

### 4. Caching

Evaluate layer caching efficiency:

- **Layer ordering**: Verify that dependency installation comes before source code copy. The pattern should be: copy lockfile -> install deps -> copy source.
- **Dependency-first pattern**: Check that `COPY requirements.txt .` (or equivalent lockfile) precedes `COPY . .` to avoid reinstalling dependencies on every source change.
- **BuildKit cache mounts**: Suggest `--mount=type=cache` for package manager caches (pip, npm, apt, cargo) if not already used.
- **Conditional copy**: Flag patterns that unnecessarily invalidate the cache (e.g., copying the entire project when only a subset is needed for a build step).
- **.dockerignore effectiveness**: Check that frequently-changing files that are not needed at build time are excluded.

### 5. Supply Chain

Assess supply chain security and reproducibility:

- **Base image provenance**: Check that base images come from trusted sources (official Docker Hub images, verified publishers, or organization-controlled registries).
- **Pinning by digest**: Recommend SHA256 digest pinning for production Dockerfiles to ensure reproducible builds (e.g., `python:3.12-slim@sha256:abc123...`).
- **SBOM generation**: Suggest adding `--sbom=true` to build commands or using tools like Syft for software bill of materials.
- **Dependency lockfiles**: Verify that lockfiles (`poetry.lock`, `package-lock.json`, `Cargo.lock`, etc.) are copied and used during install rather than resolving at build time.
- **Signed images**: Recommend signing images with Cosign or Docker Content Trust for published images.
- **Provenance attestation**: Suggest SLSA provenance attestation for images published to registries.

## Action Steps

### Step 1: Static Analysis

Read the Dockerfile and evaluate it against all Best Practices checks:

- Parse each instruction and track instruction order, layer count, and stage structure
- Flag all Best Practices findings with severity (PASS, WARN, FAIL)
- Note which base images are used and their tags

### Step 2: Security Check

Evaluate the Dockerfile against all Security checks:

- Scan for root user, secrets, and sensitive file patterns
- Check for HEALTHCHECK presence
- Evaluate base image choices for minimal attack surface
- Flag all Security findings with severity

### Step 3: Size Analysis

Evaluate the Dockerfile against all Size Optimization checks:

- Identify unnecessary packages and leftover caches
- Check for build artifacts leaking into the final stage
- Assess .dockerignore coverage
- Estimate potential size reduction for each finding

### Step 4: Caching Analysis

Evaluate the Dockerfile against all Caching checks:

- Verify layer ordering follows dependency-first pattern
- Check for BuildKit cache mount opportunities
- Identify cache-busting patterns

### Step 5: Optional Trivy Scan

If `trivy` is available on the system:

- Run `trivy config <Dockerfile>` for Dockerfile misconfiguration scanning
- If an image name was provided and the image is available locally, run `trivy image <image>` for vulnerability scanning
- Incorporate Trivy findings into the report

If `trivy` is not available, note it in the report and recommend installation for deeper vulnerability analysis.

### Step 6: Generate Report

Compile all findings into a structured audit report.

## Output Summary

Present the audit results in this format:

```
## Container Audit Report: <Dockerfile path>

### Base Image: <base-image>
### Stages: <N> (build, runtime, etc.)
### Total Instructions: <N>

### Audit Results

| Category        | Status | Findings |
|----------------|--------|----------|
| Best Practices | PASS / WARN / FAIL | <count> findings |
| Security       | PASS / WARN / FAIL | <count> findings |
| Size           | PASS / WARN / FAIL | <count> findings |
| Caching        | PASS / WARN / FAIL | <count> findings |
| Supply Chain   | PASS / WARN / FAIL | <count> findings |

### Findings (by priority)

#### FAIL (Must Fix)
- [ ] <finding description and remediation>

#### WARN (Should Fix)
- [ ] <finding description and remediation>

#### PASS
- [x] <what passed>

### Priority Actions
1. <most impactful fix>
2. <second most impactful fix>
3. <third most impactful fix>

### Estimated Impact
- Security: <improvement description>
- Image Size: ~<estimated reduction> reduction possible
- Build Time: ~<estimated improvement> with caching fixes
```

## Important Notes

- **Read-only by default**: This command does not modify any files. It only reads and analyzes the Dockerfile and related configuration.
- **Suggest /containerize to regenerate**: If the audit reveals many issues, suggest running `/containerize` to generate a new Dockerfile from scratch rather than patching the existing one.
- **Context matters**: Some findings may be acceptable depending on the project's requirements. For example, running as root may be necessary in certain HPC environments. Present findings as recommendations, not mandates.
- **Trivy is recommended but optional**: The audit provides value without Trivy through static analysis alone. Trivy adds vulnerability scanning depth.
- **Reference skills for remediation**: Point users to the relevant skills (`dockerfile-patterns`, `container-security`, `gpu-containers`) for detailed guidance on fixing findings.
- **Scope is single Dockerfile**: If auditing a project with multiple Dockerfiles, run the audit separately for each one.

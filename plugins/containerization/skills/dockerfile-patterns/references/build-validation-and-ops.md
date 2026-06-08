# Build Validation and Operational Checks

## Validation Workflow

After writing or updating a Dockerfile:

1. Build image

```bash
docker build -t myapp:test .
```

2. Basic startup check

```bash
docker run --rm myapp:test --help
```

3. Runtime smoke check (service images)

```bash
docker run --rm -p 8000:8000 myapp:test
```

4. Security check before publish

```bash
trivy image --severity HIGH,CRITICAL myapp:test
# or
docker scout cves myapp:test
```

If checks fail, adjust Dockerfile and rebuild.

## .dockerignore Essentials

Exclude:

- `.git/`, editor files, and CI metadata
- language caches/build artifacts (`__pycache__`, `target/`, `node_modules/`)
- local env/secrets (`.env`, `*.pem`, `*.key`)

## Security Defaults

- Use a pinned base image tag or digest.
- Run as non-root user.
- Do not embed secrets with `ARG`/`ENV`.
- Prefer minimal runtime base image for final stage.

## Common Failure Patterns

1. Cache misses due to copying full source too early.
2. Large images from single-stage builds.
3. Signal handling bugs from shell-form `ENTRYPOINT`.
4. Hidden secret leakage from build layers/history.

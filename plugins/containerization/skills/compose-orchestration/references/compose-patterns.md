# Compose Patterns — Deep Reference

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| Multi-File Compose | 17–89 | Base + override pattern, explicit file composition with -f flags |
| Profiles for Optional Services | 90–163 | Tagging services with profiles for conditional startup |
| Extend and Include Directives | 164–229 | Reusing service definitions across files with extend and include |
| Variable Interpolation and .env Files | 230–292 | Environment variable substitution, defaults, .env loading order |
| GPU Service Configuration | 293–360 | Reserving GPU devices for ML/scientific workloads |
| Build Context Patterns | 361–458 | Context, dockerfile, target, args, and multi-stage builds |
| Compose Watch for Development | 459–527 | File watching with sync, rebuild, and sync+restart actions |

---

## Multi-File Compose

Docker Compose supports layering multiple files to separate concerns. The most common pattern is a base file with a development override.

### Default Merge Behavior

When you run `docker compose up`, Compose automatically merges two files if they exist:

1. `compose.yml` (or `docker-compose.yml`)
2. `compose.override.yml` (or `docker-compose.override.yml`)

```
project/
├── compose.yml              # Base configuration (production-like)
├── compose.override.yml     # Auto-merged development overrides
├── compose.prod.yml         # Explicit production overrides
├── compose.test.yml         # Explicit test overrides
└── .env
```

### Explicit File Composition

Use `-f` flags to specify exactly which files to merge:

```bash
# Development (auto-merge — no flags needed)
docker compose up -d

# Production (explicit files)
docker compose -f compose.yml -f compose.prod.yml up -d

# Testing
docker compose -f compose.yml -f compose.test.yml up -d

# Multiple overrides (merged left to right)
docker compose -f compose.yml -f compose.prod.yml -f compose.monitoring.yml up -d
```

### Merge Rules

When Compose merges files, later values override earlier ones:

- **Scalar values** (image, command): replaced entirely
- **Mappings** (environment, labels): merged key-by-key; later keys win
- **Sequences** (ports, volumes): concatenated (duplicates are not removed)

```yaml
# compose.yml
services:
  api:
    environment:
      LOG_LEVEL: warning
      DATABASE_URL: postgresql://prod-host/db

# compose.override.yml
services:
  api:
    environment:
      LOG_LEVEL: debug            # Overrides "warning"
      DEBUG: "true"               # Added
      # DATABASE_URL is preserved from base
```

### COMPOSE_FILE Environment Variable

Set `COMPOSE_FILE` to avoid typing `-f` repeatedly:

```bash
# In your shell profile or .envrc
export COMPOSE_FILE=compose.yml:compose.prod.yml
docker compose up -d   # Uses both files
```

## Profiles for Optional Services

Profiles let you define services that only start when explicitly activated. This keeps the default `docker compose up` lightweight.

### Defining Profiles

```yaml
services:
  api:
    image: myapp:latest
    # No profiles key — always starts

  worker:
    image: myapp:latest
    command: celery worker
    # No profiles key — always starts

  debug-shell:
    image: nicolaka/netshoot
    profiles:
      - debug
    # Only starts with --profile debug

  prometheus:
    image: prom/prometheus:latest
    profiles:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    profiles:
      - monitoring

  pgadmin:
    image: dpage/pgadmin4:latest
    profiles:
      - tools
      - debug                    # Belongs to multiple profiles
```

### Activating Profiles

```bash
# Default services only (api, worker)
docker compose up -d

# Add debug tools
docker compose --profile debug up -d

# Add monitoring stack
docker compose --profile monitoring up -d

# Combine profiles
docker compose --profile debug --profile monitoring up -d

# Via environment variable
COMPOSE_PROFILES=debug,monitoring docker compose up -d
```

### Profile Dependencies

If a profiled service is listed in `depends_on` of an always-on service, Compose will start it regardless of profile activation:

```yaml
services:
  api:
    depends_on:
      - redis              # redis starts even if it has a profile
  redis:
    image: redis:7-alpine
    profiles:
      - cache
```

## Extend and Include Directives

### extend

Reuse a service definition from the same or another file:

```yaml
# common.yml
services:
  base-python:
    image: python:3.12-slim
    environment:
      PYTHONUNBUFFERED: "1"
      PYTHONDONTWRITEBYTECODE: "1"
    restart: unless-stopped
```

```yaml
# compose.yml
services:
  api:
    extends:
      file: common.yml
      service: base-python
    command: uvicorn app.main:app --host 0.0.0.0
    ports:
      - "8000:8000"

  worker:
    extends:
      file: common.yml
      service: base-python
    command: celery -A tasks worker
```

**Limitations of `extends`:**
- Cannot extend services that use `depends_on`, `volumes_from`, or `links`
- Networks and volumes are not inherited
- Only single-level extension (no chaining)

### include

Import entire compose files as sub-projects (Compose v2.20+):

```yaml
# compose.yml
include:
  - path: ./database/compose.yml
    project_directory: ./database
    env_file: ./database/.env

  - path: ./monitoring/compose.yml

services:
  api:
    build: .
    depends_on:
      - db                    # Defined in database/compose.yml
```

**Advantages of `include`:**
- Each included file is a self-contained project
- Build contexts are relative to the included file
- Environment files are scoped independently
- Better for large projects with separate teams

## Variable Interpolation and .env Files

### Substitution Syntax

```yaml
services:
  api:
    image: myapp:${TAG}                    # Required — fails if unset
    image: myapp:${TAG:-latest}            # Default value if unset or empty
    image: myapp:${TAG-latest}             # Default value only if unset
    image: myapp:${TAG:?Tag is required}   # Error message if unset or empty
    image: myapp:${TAG?Tag is required}    # Error message only if unset
```

### .env File Loading Order

Compose resolves variables in this priority (highest first):

1. Shell environment variables
2. Values from `--env-file` flag
3. Values from `env_file` directive in the compose file
4. Values from `.env` file in the project directory
5. Default values in `${VAR:-default}` syntax

### .env File Format

```bash
# .env
# Comments start with #
POSTGRES_USER=researcher
POSTGRES_PASSWORD=s3cret!value    # Inline comments NOT supported
POSTGRES_DB=research_db

# Quoted values (quotes are stripped)
APP_NAME="My Research App"
DESCRIPTION='Single-quoted also works'

# Multi-line values are NOT supported in .env files
# Use config files or secrets for multi-line content
```

### Escaping and Special Characters

```bash
# Use double quotes for values with spaces or special chars
PASSWORD="p@ss w0rd!"

# Dollar signs must be escaped with $$ in compose files
services:
  api:
    command: echo "$$HOME"         # Literal $HOME inside container
```

### Validating Interpolation

```bash
# Preview the resolved compose file
docker compose config

# Check a specific service
docker compose config --services
```

## GPU Service Configuration

For machine learning and scientific computing workloads that require GPU access.

### NVIDIA GPU Reservation

```yaml
services:
  training:
    image: pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1               # Number of GPUs (or "all")
              capabilities: [gpu]
    environment:
      NVIDIA_VISIBLE_DEVICES: all
      NVIDIA_DRIVER_CAPABILITIES: compute,utility
    volumes:
      - ./models:/workspace/models
      - ./data:/workspace/data
```

### Multiple GPU Configurations

```yaml
services:
  # Use all available GPUs
  training-full:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]

  # Use specific GPUs by ID
  training-gpu0:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              device_ids: ["0"]
              capabilities: [gpu]

  # Request specific GPU memory
  inference:
    deploy:
      resources:
        limits:
          memory: 8G
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

### Prerequisites

- NVIDIA Container Toolkit must be installed on the host
- The Docker daemon must be configured to use the nvidia runtime
- Verify with: `docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi`

## Build Context Patterns

### Basic Build

```yaml
services:
  api:
    build: ./api                     # Context directory containing Dockerfile
```

### Full Build Configuration

```yaml
services:
  api:
    build:
      context: .                     # Build context (files available to COPY)
      dockerfile: docker/Dockerfile.api   # Path to Dockerfile (relative to context)
      target: production             # Multi-stage build target
      args:
        PYTHON_VERSION: "3.12"
        PIP_INDEX_URL: ${PIP_INDEX_URL:-https://pypi.org/simple/}
      labels:
        com.example.build-date: "${BUILD_DATE}"
      cache_from:
        - type=registry,ref=myregistry/api:cache
      platforms:
        - linux/amd64
        - linux/arm64
      shm_size: "2gb"               # Shared memory (useful for ML builds)
    image: myregistry/api:${TAG:-dev}  # Tag the built image
```

### Multi-Stage Build Targets

A single Dockerfile can define multiple stages. Use `target` to select which stage to build:

```dockerfile
# Dockerfile
FROM python:3.12-slim AS base
COPY pyproject.toml .
RUN pip install --no-cache-dir .

FROM base AS development
RUN pip install --no-cache-dir debugpy pytest
CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "uvicorn", "app.main:app", "--reload"]

FROM base AS production
COPY src/ /app/src/
USER 1000:1000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

```yaml
# compose.yml (production)
services:
  api:
    build:
      context: .
      target: production

# compose.override.yml (development)
services:
  api:
    build:
      context: .
      target: development
```

### Build with SSH Keys (private repos)

```yaml
services:
  api:
    build:
      context: .
      ssh:
        - default                    # Forward the default SSH agent
```

```bash
docker compose build --ssh default
```

### Conditional Builds

```yaml
services:
  api:
    # Use pre-built image in CI, build locally in development
    image: myregistry/api:${TAG:-latest}
    build:
      context: .
    # `docker compose up` uses the image if available
    # `docker compose build` builds from source
    # `docker compose up --build` always rebuilds
```

## Compose Watch for Development

Compose Watch (v2.22+) monitors file changes and automatically syncs, rebuilds, or restarts services. It replaces the need for external file watchers or volume-based live reload on some platforms.

### Watch Actions

| Action | Behavior | Use Case |
|--------|----------|----------|
| `sync` | Copies changed files into the running container | Source code changes |
| `rebuild` | Rebuilds the image and recreates the container | Dependency changes |
| `sync+restart` | Syncs files then restarts the container | Config file changes |

### Configuration

```yaml
services:
  api:
    build: .
    develop:
      watch:
        # Sync source code (no rebuild needed)
        - action: sync
          path: ./src
          target: /app/src
          ignore:
            - "**/__pycache__"
            - "**/*.pyc"

        # Sync+restart for config changes
        - action: sync+restart
          path: ./config
          target: /app/config

        # Full rebuild when dependencies change
        - action: rebuild
          path: ./pyproject.toml

        - action: rebuild
          path: ./requirements.txt

        # Rebuild when Dockerfile changes
        - action: rebuild
          path: ./Dockerfile
```

### Running Watch

```bash
# Start services and watch for changes
docker compose watch

# Watch specific services
docker compose watch api worker

# Combine with up (start then watch)
docker compose up -d && docker compose watch
```

### Watch vs Bind Mounts

| Feature | Bind Mounts | Compose Watch |
|---------|-------------|---------------|
| Performance on macOS/Windows | Slower (filesystem translation) | Fast (native copy) |
| Rebuild on dependency change | Manual | Automatic |
| Config change restart | Manual | Automatic |
| Setup complexity | Low | Medium |
| Works without Compose | Yes (any container runtime) | No (Compose-specific) |

For Linux hosts, bind mounts are typically fast enough. Compose Watch is most beneficial on macOS and Windows where filesystem mounting has overhead.

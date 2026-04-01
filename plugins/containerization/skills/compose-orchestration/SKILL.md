---
name: compose-orchestration
description: Docker Compose patterns for multi-service research applications including web APIs, databases, message queues, Jupyter notebooks, and development workflows.
metadata:
  references:
    - references/compose-patterns.md
    - references/networking-volumes.md
  assets:
    - assets/web-app-compose.yml
    - assets/research-stack-compose.yml
    - assets/development-compose.yml
---

# Docker Compose Orchestration

A comprehensive guide to orchestrating multi-service research applications with Docker Compose. This skill covers compose file structure, service patterns for scientific workloads, environment management, networking, volume strategies, and development workflow optimization. Whether you are standing up a Jupyter-backed research stack or deploying a production API with a database and cache layer, the patterns and templates here will get you running quickly and correctly.

## Resources in This Skill

| Resource | Path | Purpose |
|----------|------|---------|
| Compose Patterns Reference | [references/compose-patterns.md](references/compose-patterns.md) | Multi-file compose, profiles, extend/include, variable interpolation, GPU config, build contexts, Compose Watch |
| Networking & Volumes Reference | [references/networking-volumes.md](references/networking-volumes.md) | Network drivers, DNS resolution, port mapping, volume types, NFS, permissions, persistence strategies |
| Web App Compose Template | [assets/web-app-compose.yml](assets/web-app-compose.yml) | FastAPI/Flask + PostgreSQL + Redis ready-to-use template |
| Research Stack Compose Template | [assets/research-stack-compose.yml](assets/research-stack-compose.yml) | JupyterLab + REST API + PostgreSQL for research workflows |
| Development Compose Override | [assets/development-compose.yml](assets/development-compose.yml) | Development override with live reload, debug ports, relaxed health checks |

## Quick Reference Card

### Compose File Structure

```yaml
# Top-level keys in a compose.yml
services:     # Container definitions (required)
networks:     # Custom network definitions
volumes:      # Named volume definitions
configs:      # Configuration objects (Swarm / recent Compose)
secrets:      # Sensitive data references
```

### Key Directives

```bash
# Lifecycle
docker compose up -d                  # Start all services detached
docker compose down                   # Stop and remove containers
docker compose down -v                # Stop and remove containers + volumes

# Multi-file
docker compose -f compose.yml -f compose.override.yml up -d

# Profiles
docker compose --profile debug up -d  # Start services tagged with "debug"

# Logs and status
docker compose logs -f api            # Follow logs for a service
docker compose ps                     # List running services
docker compose top                    # Show running processes

# Exec and run
docker compose exec api bash          # Shell into running container
docker compose run --rm api pytest    # One-off command in new container

# Build
docker compose build                  # Build all images
docker compose build --no-cache api   # Rebuild without cache

# Watch (development)
docker compose watch                  # Auto-sync / rebuild on file changes
```

## When to Use

- Standing up a multi-service research application (API + database + cache)
- Running JupyterLab alongside backend services for interactive analysis
- Creating reproducible development environments for a team
- Prototyping microservice architectures for scientific pipelines
- Managing worker queues for batch processing or ML training jobs
- Providing a single-command setup for contributors (`docker compose up`)
- Isolating services with custom networks and persistent volumes

## Compose File Structure

A compose file defines five top-level objects. Only `services` is required.

### services

Each service maps to one container. Key fields:

```yaml
services:
  api:
    image: python:3.12-slim          # Use a pre-built image
    build: ./api                     # Or build from a Dockerfile
    ports:
      - "8000:8000"                  # HOST:CONTAINER
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
    volumes:
      - ./src:/app/src               # Bind mount for development
    depends_on:
      db:
        condition: service_healthy   # Wait for dependency health check
    restart: unless-stopped
```

### networks

```yaml
networks:
  backend:
    driver: bridge                   # Default; most common
  frontend:
    driver: bridge
```

### volumes

```yaml
volumes:
  pg-data:                           # Named volume (managed by Docker)
  redis-data:
```

### configs

```yaml
configs:
  app-config:
    file: ./config/app.yml           # Injected into containers
```

### secrets

```yaml
secrets:
  db-password:
    file: ./secrets/db-password.txt  # Mounted at /run/secrets/<name>
```

## Service Patterns

### Web App + Database

The classic pattern: a Python API backed by PostgreSQL and optionally Redis for caching or task queues.

See [assets/web-app-compose.yml](assets/web-app-compose.yml) for a complete template.

```yaml
services:
  api:
    build: .
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
  db:
    image: postgres:16-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
```

### Jupyter + Backend

A JupyterLab notebook server connected to an API and database for interactive research. Notebooks are bind-mounted so work persists outside the container.

See [assets/research-stack-compose.yml](assets/research-stack-compose.yml) for a complete template.

### Worker Queue

A pattern for background processing with a message broker:

```yaml
services:
  worker:
    build: .
    command: celery -A tasks worker --loglevel=info
    depends_on:
      broker:
        condition: service_healthy
  broker:
    image: rabbitmq:3-management-alpine
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "check_running"]
```

## Environment Management

### .env Files

Compose automatically loads a `.env` file in the project directory:

```bash
# .env
POSTGRES_USER=researcher
POSTGRES_PASSWORD=changeme
POSTGRES_DB=research_db
API_PORT=8000
```

### Variable Substitution

Reference variables in compose files with `${VAR}` syntax:

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "${DB_PORT:-5432}:5432"      # Default value with :-
```

### Multiple .env Files

```yaml
services:
  api:
    env_file:
      - .env                        # Shared variables
      - .env.local                   # Local overrides (git-ignored)
```

## Development vs Production

Use the override pattern to keep a clean base file and layer development-specific settings on top.

```
project/
├── compose.yml                  # Base (production-like)
├── compose.override.yml         # Auto-loaded dev overrides
├── compose.prod.yml             # Explicit production overrides
└── .env
```

Compose automatically merges `compose.yml` + `compose.override.yml`. For production, specify files explicitly:

```bash
# Development (automatic override)
docker compose up -d

# Production (explicit files)
docker compose -f compose.yml -f compose.prod.yml up -d
```

See [assets/development-compose.yml](assets/development-compose.yml) for a development override template.

## Health Checks and Dependencies

### Health Check Configuration

```yaml
services:
  db:
    image: postgres:16-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
```

### Dependency Conditions

```yaml
services:
  api:
    depends_on:
      db:
        condition: service_healthy   # Wait until healthy
      migrations:
        condition: service_completed_successfully  # Run-once task
```

Available conditions:
- `service_started` — container has started (default)
- `service_healthy` — health check passes
- `service_completed_successfully` — container exited with code 0

## Named Volumes and Bind Mounts

### Named Volumes (data persistence)

```yaml
services:
  db:
    volumes:
      - pg-data:/var/lib/postgresql/data

volumes:
  pg-data:                           # Docker manages lifecycle
```

### Bind Mounts (development)

```yaml
services:
  api:
    volumes:
      - ./src:/app/src:cached        # Host path → container path
      - ./config:/app/config:ro      # Read-only mount
```

### tmpfs (ephemeral scratch)

```yaml
services:
  worker:
    tmpfs:
      - /tmp:size=256m
```

## Networking

By default, Compose creates a single network for the project. All services can reach each other by service name.

### Custom Networks for Isolation

```yaml
services:
  api:
    networks:
      - frontend
      - backend
  db:
    networks:
      - backend                      # Not reachable from frontend

networks:
  frontend:
  backend:
```

### DNS Resolution

Services resolve each other by name. For example, `api` can connect to `db` using hostname `db`:

```python
DATABASE_URL = "postgresql://user:pass@db:5432/mydb"
```

## Profiles

Tag services so they only start when a profile is explicitly activated:

```yaml
services:
  api:
    # No profile — always starts

  debug-tools:
    image: nicolaka/netshoot
    profiles:
      - debug                        # Only starts with --profile debug

  monitoring:
    image: grafana/grafana
    profiles:
      - monitoring
```

```bash
docker compose up -d                          # api only
docker compose --profile debug up -d          # api + debug-tools
docker compose --profile debug --profile monitoring up -d  # all three
```

## Common Mistakes

1. **Using `depends_on` without `condition: service_healthy`** — The service starts before the dependency is actually ready to accept connections.
2. **Storing secrets in `environment` blocks** — Use Docker secrets or `.env` files that are git-ignored instead.
3. **Not using named volumes for database data** — Bind mounts can cause permission issues; named volumes are portable and Docker-managed.
4. **Hardcoding ports** — Use variable substitution (`${API_PORT:-8000}:8000`) so team members can avoid conflicts.
5. **Missing `restart` policy** — Services will not restart after a crash unless you set `restart: unless-stopped` or `restart: on-failure`.
6. **Forgetting `--rm` with `docker compose run`** — One-off containers accumulate and waste disk space.
7. **Bind-mounting over container directories with important content** — The host directory replaces the container directory entirely, hiding installed packages or built assets.
8. **Running containers as root when not necessary** — Set `user:` in the service or use a non-root base image.

## Best Practices

1. **Pin image tags** — Use `postgres:16-alpine`, not `postgres:latest`.
2. **Use health checks on every stateful service** — Databases, caches, and message brokers should all have health checks.
3. **Separate concerns with networks** — Only expose services that need to communicate with each other.
4. **Use the override pattern** — Keep `compose.yml` production-like; layer dev settings with `compose.override.yml`.
5. **Parameterize with `.env`** — Avoid hardcoded values; use variable substitution for ports, credentials, and image tags.
6. **Prefer named volumes over bind mounts for data** — Named volumes are faster on macOS/Windows and avoid permission issues.
7. **Use `profiles` for optional services** — Monitoring, debugging, and admin tools should not start by default.
8. **Add `restart: unless-stopped`** — Ensures services recover from crashes without restarting after manual stops.
9. **Use multi-stage builds** — Keep production images small; use a development target for tooling.
10. **Document the stack** — Add comments in the compose file explaining non-obvious configuration.

## Resources

- **Docker Compose Specification**: https://docs.docker.com/reference/compose-file/
- **Compose CLI Reference**: https://docs.docker.com/reference/cli/docker/compose/
- **Docker Volumes**: https://docs.docker.com/engine/storage/volumes/
- **Docker Networking**: https://docs.docker.com/engine/network/
- **Compose Watch**: https://docs.docker.com/compose/how-tos/file-watch/
- **Compose Profiles**: https://docs.docker.com/compose/how-tos/profiles/
- **Environment Variables in Compose**: https://docs.docker.com/compose/how-tos/environment-variables/

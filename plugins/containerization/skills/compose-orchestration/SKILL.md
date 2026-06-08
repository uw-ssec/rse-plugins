---
name: compose-orchestration
description: Use when the user asks about Docker Compose configuration, docker-compose.yml/compose.yml files, multi-container setups, container networking, or local container orchestration for development. Creates and configures Compose stacks for web APIs, databases, message queues, workers, and Jupyter workflows; sets up service dependencies and health checks; and troubleshoots startup/connectivity issues.
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

## Use When

- The user asks to create or fix a `compose.yml` / `docker-compose.yml` file.
- The user needs a multi-container stack (API + database + cache/queue + worker).
- The user asks about container networking, volumes, profiles, or environment variables in Compose.
- The user needs a reproducible containerized development environment.

## Primary Actions

- Generate or update Compose service definitions with correct dependencies.
- Add health checks and `depends_on` conditions for reliable startup order.
- Configure environment variables, port mappings, and volume strategy.
- Set up development overrides and profile-based optional services.
- Debug container startup, readiness, and inter-service connectivity.

## Startup Workflow With Validation Checkpoints

1. **Define stack** — create/update `compose.yml` services, networks, and volumes.
2. **Validate config** — run `docker compose config` and fix schema/merge issues.
3. **Start services** — run `docker compose up -d`.
4. **Check status** — run `docker compose ps`; confirm expected services are up.
5. **Verify health** — confirm health checks pass for stateful dependencies.
6. **Verify connectivity** — test service-to-service access (e.g., API -> DB hostname).
7. **Inspect logs** — run `docker compose logs -f <service>` for failing services.

If a checkpoint fails, fix compose configuration and repeat from step 2.

## Quick Command Reference

```bash
# Validate and start
docker compose config
docker compose up -d

# Inspect and debug
docker compose ps
docker compose logs -f api
docker compose exec api sh

# Stop/cleanup
docker compose down
docker compose down -v

# Multi-file and profiles
docker compose -f compose.yml -f compose.override.yml up -d
docker compose --profile debug up -d
```

## Minimal Compose Pattern

```yaml
services:
  api:
    build: .
    depends_on:
      db:
        condition: service_healthy
    environment:
      DATABASE_URL: postgresql://user:pass@db:5432/app
    ports:
      - "8000:8000"

  db:
    image: postgres:16-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  pg-data:
```

## Keep in SKILL.md; Deep Details in References

- Compose patterns (multi-file, profiles, env interpolation, GPU, watch):
  [references/compose-patterns.md](references/compose-patterns.md)
- Networking and volume deep dives:
  [references/networking-volumes.md](references/networking-volumes.md)

## Common Pitfalls (Top 4)

1. Using `depends_on` without health conditions for databases/queues.
2. Hardcoding secrets directly in Compose files.
3. Using bind mounts for persistent DB data instead of named volumes.
4. Skipping `docker compose config` before `up`, missing merge/interpolation errors.

## Templates

- [assets/web-app-compose.yml](assets/web-app-compose.yml)
- [assets/research-stack-compose.yml](assets/research-stack-compose.yml)
- [assets/development-compose.yml](assets/development-compose.yml)

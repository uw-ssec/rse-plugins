# devcontainer.json -- Deep Reference

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| Complete Schema Reference | 17-99 | All top-level properties with types, defaults, and descriptions |
| Lifecycle Scripts | 101-200 | initializeCommand, onCreateCommand, postCreateCommand, and more |
| remoteUser | 202-257 | User configuration, UID/GID mapping, file permissions |
| Mounts | 259-332 | Volume mounts, bind mounts, tmpfs, named volumes |
| Environment Variables | 334-400 | containerEnv, remoteEnv, .env files, variable substitution |
| Secrets Forwarding | 402-476 | Codespaces secrets, local secret forwarding, SSH agent |
| Docker Compose Integration | 478-548 | Multi-service setups, service selection, shared volumes |

---

## Complete Schema Reference

### Image and Build Properties

| Property | Type | Description |
|----------|------|-------------|
| `image` | string | Docker image to use (mutually exclusive with `build` and `dockerComposeFile`) |
| `build.dockerfile` | string | Path to Dockerfile relative to devcontainer.json |
| `build.context` | string | Docker build context path (default: `.`) |
| `build.args` | object | Build arguments passed to `docker build --build-arg` |
| `build.target` | string | Multi-stage build target |
| `build.cacheFrom` | string[] | Cache sources for the build |
| `build.options` | string[] | Additional `docker build` CLI arguments |
| `dockerComposeFile` | string/string[] | Path to Docker Compose file(s) |
| `service` | string | Compose service to connect to (required with dockerComposeFile) |

### Runtime Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `name` | string | none | Display name for the dev container |
| `workspaceFolder` | string | `/workspaces/<repo>` | Path inside container for workspace |
| `workspaceMount` | string | auto | Custom workspace mount string |
| `remoteUser` | string | `"root"` or image default | User for VS Code operations |
| `containerUser` | string | `"root"` or image default | User for running the container |
| `remoteEnv` | object | none | Environment variables for VS Code terminal |
| `containerEnv` | object | none | Environment variables for the container |
| `forwardPorts` | (number\|string)[] | none | Ports to auto-forward |
| `portsAttributes` | object | none | Per-port settings (label, protocol, visibility) |
| `appPort` | number/string/array | none | Ports to publish (docker run -p) |
| `runArgs` | string[] | none | Additional `docker run` arguments |
| `shutdownAction` | string | `"stopContainer"` | Action on VS Code close: `stopContainer` or `none` |
| `overrideCommand` | boolean | `true` | Override container CMD with `sleep infinity` |
| `init` | boolean | `false` | Run an init process (tini) as PID 1 |
| `privileged` | boolean | `false` | Run container in privileged mode |
| `capAdd` | string[] | none | Linux capabilities to add |
| `securityOpt` | string[] | none | Security options |

### Customization Properties

| Property | Type | Description |
|----------|------|-------------|
| `features` | object | Dev container features to install |
| `customizations.vscode.extensions` | string[] | VS Code extensions to install |
| `customizations.vscode.settings` | object | VS Code settings overrides |
| `customizations.codespaces` | object | GitHub Codespaces-specific settings |

### Lifecycle Properties

| Property | Type | Description |
|----------|------|-------------|
| `initializeCommand` | string/object | Runs on host before container build |
| `onCreateCommand` | string/object | Runs after container first created |
| `updateContentCommand` | string/object | Runs after create and on content updates |
| `postCreateCommand` | string/object | Runs after create + updateContent |
| `postStartCommand` | string/object | Runs every time container starts |
| `postAttachCommand` | string/object | Runs every time VS Code attaches |
| `waitFor` | string | Which lifecycle step to wait for before attaching |

### Codespaces Properties

| Property | Type | Description |
|----------|------|-------------|
| `hostRequirements.cpus` | number | Minimum CPU cores |
| `hostRequirements.memory` | string | Minimum memory (e.g., `"8gb"`) |
| `hostRequirements.storage` | string | Minimum storage (e.g., `"32gb"`) |
| `hostRequirements.gpu` | boolean/object | GPU requirement |
| `secrets` | object | Secret definitions for Codespaces |

### Variable Substitution

Dev container properties support these variables:

| Variable | Value |
|----------|-------|
| `${localWorkspaceFolder}` | Host path to workspace |
| `${containerWorkspaceFolder}` | Container path to workspace |
| `${localWorkspaceFolderBasename}` | Workspace folder name |
| `${localEnv:VAR_NAME}` | Host environment variable |
| `${containerEnv:VAR_NAME}` | Container environment variable |
| `${devcontainerId}` | Unique ID for the dev container |

---

## Lifecycle Scripts

### Execution Order

When a dev container is created and started, lifecycle scripts run in this order:

```
1. initializeCommand     (on host, before container build)
2. onCreateCommand        (in container, first creation only)
3. updateContentCommand   (in container, after create and on content changes)
4. postCreateCommand      (in container, after updateContent)
5. postStartCommand       (in container, every start)
6. postAttachCommand      (in container, every VS Code attach)
```

On subsequent starts (not first creation), only steps 5 and 6 run.

### initializeCommand

Runs on the **host machine** before the container is built. Use for host-side prerequisites.

```jsonc
{
  // Check that Docker is running
  "initializeCommand": "docker info > /dev/null 2>&1 || echo 'Docker is not running'"
}
```

### onCreateCommand

Runs once when the container is first created. Good for one-time setup that does not depend on workspace content.

```jsonc
{
  "onCreateCommand": "sudo apt-get update && sudo apt-get install -y graphviz"
}
```

### updateContentCommand

Runs after `onCreateCommand` and again whenever workspace content changes (e.g., after a Codespaces prebuild updates). Good for dependency installation.

```jsonc
{
  "updateContentCommand": "pip install -e '.[dev]'"
}
```

### postCreateCommand

Runs after `updateContentCommand`. The most commonly used hook. Good for final setup that depends on both the container and workspace content.

```jsonc
{
  // Single command
  "postCreateCommand": "pip install -e '.[dev]' && pre-commit install",

  // Multiple named commands (run in parallel)
  "postCreateCommand": {
    "install": "pip install -e '.[dev]'",
    "hooks": "pre-commit install",
    "data": "python scripts/setup_test_db.py"
  }
}
```

### postStartCommand

Runs every time the container starts (including restarts). Good for tasks that should run fresh on each start.

```jsonc
{
  "postStartCommand": "git fetch --all --prune"
}
```

### postAttachCommand

Runs every time VS Code attaches to the container. Good for starting background services that should run while the editor is connected.

```jsonc
{
  "postAttachCommand": "nohup python -m http.server 8000 &"
}
```

### waitFor

Controls which lifecycle step VS Code waits for before showing the editor:

```jsonc
{
  // Show editor immediately after container starts (don't wait for postCreateCommand)
  "waitFor": "onCreateCommand"
}
```

Options: `"initializeCommand"`, `"onCreateCommand"`, `"updateContentCommand"`, `"postCreateCommand"` (default), `"postStartCommand"`

---

## remoteUser

### User Configuration

The `remoteUser` property sets which user VS Code uses for terminal sessions, extension processes, and file operations inside the container.

```jsonc
{
  // Use the vscode user (created by Microsoft dev container images)
  "remoteUser": "vscode",

  // Use root (not recommended for daily development)
  "remoteUser": "root"
}
```

### Microsoft Dev Container Images

Microsoft's dev container images create a `vscode` user (UID 1000) by default. The `remoteUser` is set to `vscode` automatically for these images.

### Custom Users

If using a custom Dockerfile, create a user and set remoteUser:

```dockerfile
# In Dockerfile
RUN useradd --create-home --shell /bin/bash devuser
```

```jsonc
{
  "remoteUser": "devuser"
}
```

### containerUser vs remoteUser

- `containerUser`: User for running the container process itself (the `sleep infinity` command)
- `remoteUser`: User for VS Code operations (terminals, extensions, file access)

Most of the time, set only `remoteUser` and leave `containerUser` at default.

### File Permissions

When `remoteUser` is non-root, ensure the workspace directory is owned by that user:

```jsonc
{
  "remoteUser": "vscode",
  "postCreateCommand": "sudo chown -R vscode:vscode ${containerWorkspaceFolder}"
}
```

Microsoft dev container images handle this automatically.

---

## Mounts

### Bind Mounts

Mount host directories into the container:

```jsonc
{
  "mounts": [
    // Mount host SSH keys (read-only)
    "source=${localEnv:HOME}/.ssh,target=/home/vscode/.ssh,type=bind,readonly",

    // Mount a data directory
    "source=${localWorkspaceFolder}/data,target=/data,type=bind,consistency=cached"
  ]
}
```

### Named Volumes

Persist data across container rebuilds:

```jsonc
{
  "mounts": [
    // Persist pip cache across rebuilds
    "source=pip-cache,target=/home/vscode/.cache/pip,type=volume",

    // Persist cargo registry
    "source=cargo-registry,target=/usr/local/cargo/registry,type=volume",

    // Persist node_modules
    "source=node-modules,target=${containerWorkspaceFolder}/node_modules,type=volume"
  ]
}
```

### tmpfs Mounts

In-memory filesystem for temporary data:

```jsonc
{
  "mounts": [
    "source=tmpfs,target=/tmp,type=tmpfs"
  ]
}
```

### Workspace Mount Customization

Override the default workspace mount:

```jsonc
{
  // Default (automatically set)
  "workspaceMount": "source=${localWorkspaceFolder},target=/workspaces/${localWorkspaceFolderBasename},type=bind,consistency=cached",
  "workspaceFolder": "/workspaces/${localWorkspaceFolderBasename}",

  // Custom mount point
  "workspaceMount": "source=${localWorkspaceFolder},target=/app,type=bind,consistency=cached",
  "workspaceFolder": "/app"
}
```

### Mount Consistency Options

| Option | Behavior | Performance | Use Case |
|--------|----------|-------------|----------|
| `consistent` | Full consistency (default) | Slowest on macOS | Small projects |
| `cached` | Host writes visible in container eventually | Fast reads | Most projects (recommended) |
| `delegated` | Container writes visible on host eventually | Fastest | Build output, caches |

---

## Environment Variables

### containerEnv

Set environment variables for all processes in the container:

```jsonc
{
  "containerEnv": {
    "PYTHONPATH": "/workspace/src",
    "DATABASE_URL": "postgresql://localhost:5432/myapp",
    "ENVIRONMENT": "development"
  }
}
```

### remoteEnv

Set environment variables only for VS Code processes (terminals, extensions):

```jsonc
{
  "remoteEnv": {
    "PATH": "/workspace/.venv/bin:${containerEnv:PATH}",
    "VIRTUAL_ENV": "/workspace/.venv"
  }
}
```

### .env Files

Load environment variables from a file:

```jsonc
{
  // Load from .devcontainer/.env
  "runArgs": ["--env-file", ".devcontainer/.env"]
}
```

```bash
# .devcontainer/.env
DATABASE_URL=postgresql://localhost:5432/myapp
REDIS_URL=redis://localhost:6379
DEBUG=true
```

### Variable Substitution in Values

Environment variables support substitution:

```jsonc
{
  "remoteEnv": {
    // Reference a host environment variable
    "API_KEY": "${localEnv:API_KEY}",

    // Reference a container environment variable
    "FULL_PATH": "${containerEnv:PATH}:/custom/bin",

    // Default value if not set
    "LOG_LEVEL": "${localEnv:LOG_LEVEL:info}"
  }
}
```

---

## Secrets Forwarding

### GitHub Codespaces Secrets

Define expected secrets in devcontainer.json. Users configure values in GitHub Settings > Codespaces > Secrets.

```jsonc
{
  "secrets": {
    "API_KEY": {
      "description": "API key for the external data service",
      "documentationUrl": "https://docs.example.com/api-keys"
    },
    "DATABASE_PASSWORD": {
      "description": "Password for the research database"
    }
  }
}
```

Secrets are available as environment variables inside the Codespace.

### Local Development Secrets

For local dev containers, pass secrets via environment variables or env files:

```jsonc
{
  // Forward host environment variable to container
  "remoteEnv": {
    "API_KEY": "${localEnv:API_KEY}"
  }
}
```

Or use a `.env` file that is not committed to version control:

```jsonc
{
  "runArgs": ["--env-file", ".devcontainer/.env.local"]
}
```

Add `.devcontainer/.env.local` to `.gitignore`.

### SSH Agent Forwarding

Forward your host SSH agent to the container for git operations:

```jsonc
{
  // VS Code handles SSH agent forwarding automatically on Linux/macOS
  // On Windows, ensure ssh-agent service is running

  // For explicit SSH key mounting (alternative to agent forwarding)
  "mounts": [
    "source=${localEnv:HOME}/.ssh,target=/home/vscode/.ssh,type=bind,readonly"
  ]
}
```

### GPG Key Forwarding

Forward GPG keys for commit signing:

```jsonc
{
  "mounts": [
    "source=${localEnv:HOME}/.gnupg,target=/home/vscode/.gnupg,type=bind"
  ],
  "postCreateCommand": "git config --global gpg.program gpg2"
}
```

---

## Docker Compose Integration

### Basic Compose Setup

```jsonc
// .devcontainer/devcontainer.json
{
  "name": "App with Database",
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace",
  "forwardPorts": [5432, 6379],
  "postCreateCommand": "pip install -e '.[dev]'"
}
```

```yaml
# .devcontainer/docker-compose.yml
services:
  app:
    build:
      context: ..
      dockerfile: .devcontainer/Dockerfile
    volumes:
      - ..:/workspace:cached
    # Keep container running (overrideCommand: true handles this)
    command: sleep infinity

  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: devpassword
      POSTGRES_DB: myapp_dev
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  pgdata:
```

### Multiple Compose Files

Layer Compose files for different environments:

```jsonc
{
  "dockerComposeFile": [
    "docker-compose.yml",
    "docker-compose.dev.yml"
  ],
  "service": "app"
}
```

### Service Communication

Services in the same Compose network can reach each other by service name:

```python
# In your application code
DATABASE_URL = "postgresql://postgres:devpassword@db:5432/myapp_dev"
REDIS_URL = "redis://redis:6379"
```

### Extending Existing Compose Files

If your project already has a `docker-compose.yml` for deployment, extend it for development:

```yaml
# .devcontainer/docker-compose.yml
services:
  app:
    extends:
      file: ../docker-compose.yml
      service: app
    volumes:
      - ..:/workspace:cached
    command: sleep infinity
    # Override production settings for development
    environment:
      DEBUG: "true"
      LOG_LEVEL: "debug"
```

### Health Checks in Development

Wait for services to be ready before running setup commands:

```jsonc
{
  "postCreateCommand": {
    "wait-for-db": "until pg_isready -h db -p 5432; do sleep 1; done",
    "migrate": "python manage.py migrate",
    "install": "pip install -e '.[dev]'"
  }
}
```

### Shared Volumes

Share data between services using named volumes:

```yaml
services:
  app:
    volumes:
      - shared-data:/data

  worker:
    volumes:
      - shared-data:/data

volumes:
  shared-data:
```

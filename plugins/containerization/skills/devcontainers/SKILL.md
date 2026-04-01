---
name: devcontainers
description: Development container configuration for VS Code and GitHub Codespaces including devcontainer.json, features, multi-container setups, and language-specific templates for reproducible research environments.
metadata:
  references:
    - references/devcontainer-json.md
    - references/features-and-customization.md
  assets:
    - assets/python-devcontainer.json
    - assets/rust-devcontainer.json
    - assets/node-devcontainer.json
---

# Dev Containers

A comprehensive guide to development containers for reproducible research environments. Dev containers define your entire development environment -- editor extensions, tools, runtimes, and dependencies -- as code in a `devcontainer.json` file. This skill covers devcontainer.json configuration, features, language-specific templates, multi-container setups with Docker Compose, GitHub Codespaces integration, and lifecycle hooks. Dev containers ensure that every contributor works in an identical environment, eliminating "works on my machine" issues.

## Resources in This Skill

This skill includes supporting materials for dev container tasks:

**References** (detailed guides -- consult the table of contents in each file and read specific sections as needed):
- `references/devcontainer-json.md` - Complete devcontainer.json reference: lifecycle scripts, remoteUser, mounts, environment variables, secrets forwarding, and Docker Compose integration
- `references/features-and-customization.md` - Features and customization: official features, community features, creating custom features, VS Code customizations, Codespaces prebuilds, dotfiles, and machine types

**Assets** (ready-to-use devcontainer.json templates):
- `assets/python-devcontainer.json` - Python devcontainer with Pylance, Jupyter, Ruff, and scientific computing extensions
- `assets/rust-devcontainer.json` - Rust devcontainer with rust-analyzer, LLDB debugger, and cargo tools
- `assets/node-devcontainer.json` - Node.js devcontainer with ESLint, Prettier, and testing extensions

## Quick Reference Card

### Minimal devcontainer.json

```jsonc
// .devcontainer/devcontainer.json
{
  "name": "My Project",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "features": {
    "ghcr.io/devcontainers/features/python:1": { "version": "3.12" }
  },
  "customizations": {
    "vscode": {
      "extensions": ["ms-python.python"]
    }
  },
  "postCreateCommand": "pip install -e '.[dev]'"
}
```

### Key Properties

| Property | Purpose | Example |
|----------|---------|---------|
| `image` | Base container image | `"mcr.microsoft.com/devcontainers/python:3.12"` |
| `build.dockerfile` | Custom Dockerfile | `"Dockerfile"` |
| `features` | Add tools/runtimes | `{"ghcr.io/devcontainers/features/node:1": {}}` |
| `forwardPorts` | Auto-forward ports | `[8000, 5432]` |
| `postCreateCommand` | Run after container create | `"pip install -e '.[dev]'"` |
| `postStartCommand` | Run on every start | `"git fetch --all"` |
| `remoteUser` | Non-root user | `"vscode"` |
| `mounts` | Additional volumes | See reference |
| `customizations.vscode.extensions` | VS Code extensions | `["ms-python.python"]` |
| `customizations.vscode.settings` | VS Code settings | `{"python.defaultInterpreterPath": "/usr/local/bin/python"}` |

### File Location

Dev container configuration lives in one of these locations:

```
.devcontainer/devcontainer.json          # standard (recommended)
.devcontainer.json                        # root-level alternative
.devcontainer/<name>/devcontainer.json    # named configurations
```

## When to Use

Use this skill when you need to:

- Set up a reproducible development environment for a research project
- Configure VS Code extensions and settings for a team
- Create GitHub Codespaces configurations for instant cloud development
- Add development tools (linters, formatters, debuggers) to a container
- Set up multi-container development environments (app + database + cache)
- Configure language-specific development environments (Python, Rust, Node.js)
- Customize dev container lifecycle (install dependencies on create, run setup scripts)
- Enable GPU access in development containers
- Share consistent development environments across a team or lab

## devcontainer.json Structure

The `devcontainer.json` file is the core configuration. It can reference a pre-built image or a custom Dockerfile.

### Image-Based Configuration

The simplest approach uses a pre-built image:

```jsonc
{
  "name": "Python 3.12",
  "image": "mcr.microsoft.com/devcontainers/python:3.12",
  "postCreateCommand": "pip install -e '.[dev]'",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance"
      ]
    }
  }
}
```

### Dockerfile-Based Configuration

For custom environments, point to a Dockerfile:

```jsonc
{
  "name": "Custom Environment",
  "build": {
    "dockerfile": "Dockerfile",
    "context": "..",
    "args": {
      "PYTHON_VERSION": "3.12"
    }
  },
  "postCreateCommand": "pip install -e '.[dev]'"
}
```

### Docker Compose Configuration

For multi-container setups (app + database, etc.):

```jsonc
{
  "name": "Full Stack",
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace",
  "postCreateCommand": "pip install -e '.[dev]'"
}
```

See `references/devcontainer-json.md` for the complete schema reference.

## Pre-Built vs Custom Dockerfiles

### Pre-Built Images (Recommended for Most Projects)

Microsoft publishes dev container images with common tools pre-installed:

| Image | Contents |
|-------|----------|
| `mcr.microsoft.com/devcontainers/base:ubuntu` | Ubuntu with git, zsh, common tools |
| `mcr.microsoft.com/devcontainers/python:3.12` | Python with pip, pylint, venv |
| `mcr.microsoft.com/devcontainers/typescript-node:22` | Node.js with npm, yarn |
| `mcr.microsoft.com/devcontainers/rust:1` | Rust with cargo, rustfmt, clippy |
| `mcr.microsoft.com/devcontainers/universal:2` | Multi-language (Python, Node, Go, Java, .NET) |

**Advantages:** Fast startup, no build step, maintained by Microsoft.
**Disadvantages:** May include tools you don't need, less control over versions.

### Custom Dockerfile (For Specialized Needs)

Use a custom Dockerfile when you need:
- Specific system libraries (HDF5, GDAL, FFTW)
- Exact version pinning beyond what features offer
- Private package repositories
- GPU development tools

```dockerfile
# .devcontainer/Dockerfile
FROM mcr.microsoft.com/devcontainers/python:3.12

# Install system libraries for scientific computing
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libhdf5-dev \
        libgdal-dev \
        libfftw3-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python tools
RUN pip install --no-cache-dir \
    ruff mypy pytest jupyter
```

## Features

Features are modular, shareable units of installation code. They add tools, runtimes, or configuration to a dev container without modifying the Dockerfile.

```jsonc
{
  "features": {
    // Official features (from devcontainers org)
    "ghcr.io/devcontainers/features/python:1": { "version": "3.12" },
    "ghcr.io/devcontainers/features/node:1": { "version": "22" },
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/github-cli:1": {},

    // Community features
    "ghcr.io/devcontainers-contrib/features/ruff:1": {},
    "ghcr.io/devcontainers-contrib/features/poetry:2": {}
  }
}
```

**Key benefits:**
- Composable: mix and match tools from different sources
- Versioned: pin to major/minor versions for stability
- Cacheable: features are cached for faster rebuilds

See `references/features-and-customization.md` for the full features reference.

## Language-Specific Configurations

### Python (Scientific Computing)

```jsonc
{
  "name": "Python Science",
  "image": "mcr.microsoft.com/devcontainers/python:3.12",
  "features": {
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-toolsai.jupyter",
        "charliermarsh.ruff"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "[python]": {
          "editor.defaultFormatter": "charliermarsh.ruff",
          "editor.formatOnSave": true
        }
      }
    }
  },
  "postCreateCommand": "pip install -e '.[dev]'"
}
```

See `assets/python-devcontainer.json` for a complete template.

### Rust

```jsonc
{
  "name": "Rust",
  "image": "mcr.microsoft.com/devcontainers/rust:1",
  "customizations": {
    "vscode": {
      "extensions": [
        "rust-lang.rust-analyzer",
        "vadimcn.vscode-lldb"
      ],
      "settings": {
        "rust-analyzer.check.command": "clippy"
      }
    }
  },
  "postCreateCommand": "cargo build"
}
```

See `assets/rust-devcontainer.json` for a complete template.

### Node.js

```jsonc
{
  "name": "Node.js",
  "image": "mcr.microsoft.com/devcontainers/typescript-node:22",
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode"
      ]
    }
  },
  "postCreateCommand": "npm install"
}
```

See `assets/node-devcontainer.json` for a complete template.

## Multi-Container Dev Environments

Use Docker Compose when your development environment requires multiple services:

```yaml
# .devcontainer/docker-compose.yml
services:
  app:
    build:
      context: ..
      dockerfile: .devcontainer/Dockerfile
    volumes:
      - ..:/workspace:cached
    command: sleep infinity

  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: devpassword
      POSTGRES_DB: myapp
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  pgdata:
```

```jsonc
// .devcontainer/devcontainer.json
{
  "name": "Full Stack",
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace",
  "forwardPorts": [5432, 6379],
  "postCreateCommand": "pip install -e '.[dev]'"
}
```

## GitHub Codespaces

Dev containers are the configuration format for GitHub Codespaces. Any repository with a `.devcontainer/devcontainer.json` can be opened in Codespaces.

**Codespaces-specific settings:**

```jsonc
{
  "hostRequirements": {
    "cpus": 4,
    "memory": "8gb",
    "storage": "32gb"
  },
  "secrets": {
    "API_KEY": {
      "description": "API key for the data service",
      "documentationUrl": "https://example.com/docs/api-keys"
    }
  }
}
```

**Prebuilds:** Configure prebuilds in your repository settings to pre-build the dev container image, reducing Codespace startup time from minutes to seconds.

## VS Code Extensions and Settings

### Extensions

Extensions are installed automatically when the container is created:

```jsonc
{
  "customizations": {
    "vscode": {
      "extensions": [
        // Use the full extension ID from the VS Code marketplace
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-toolsai.jupyter",
        "charliermarsh.ruff",
        "eamodio.gitlens",
        "github.copilot"
      ]
    }
  }
}
```

### Settings

Override VS Code settings for the dev container:

```jsonc
{
  "customizations": {
    "vscode": {
      "settings": {
        "editor.formatOnSave": true,
        "editor.rulers": [88],
        "files.trimTrailingWhitespace": true,
        "terminal.integrated.defaultProfile.linux": "zsh",
        "python.testing.pytestEnabled": true
      }
    }
  }
}
```

## Lifecycle Hooks

Dev containers support several lifecycle hooks that run at different points:

| Hook | When It Runs | Use Case |
|------|-------------|----------|
| `initializeCommand` | Before container build (on host) | Check prerequisites |
| `onCreateCommand` | After container is created (first time only) | One-time setup |
| `updateContentCommand` | After create, and on content updates | Install dependencies |
| `postCreateCommand` | After create + updateContent | Install dev deps, setup |
| `postStartCommand` | Every time container starts | Fetch latest data |
| `postAttachCommand` | Every time VS Code attaches | Start background services |

```jsonc
{
  "postCreateCommand": "pip install -e '.[dev]' && pre-commit install",
  "postStartCommand": "git fetch --all --prune"
}
```

Commands can be strings (run in shell) or arrays (exec form):

```jsonc
{
  "postCreateCommand": {
    "pip": "pip install -e '.[dev]'",
    "pre-commit": "pre-commit install",
    "data": "python scripts/download_test_data.py"
  }
}
```

## GPU in Dev Containers

### NVIDIA GPU

```jsonc
{
  "image": "mcr.microsoft.com/devcontainers/python:3.12",
  "features": {
    "ghcr.io/devcontainers/features/nvidia-cuda:1": {
      "installCudnn": true,
      "cudaVersion": "12.4"
    }
  },
  "runArgs": ["--gpus", "all"],
  "postCreateCommand": "pip install torch --index-url https://download.pytorch.org/whl/cu124"
}
```

### Codespaces GPU

GPU-enabled Codespaces require a machine type with GPU support (available on GitHub Enterprise or by request):

```jsonc
{
  "hostRequirements": {
    "gpu": true
  }
}
```

## Common Mistakes

1. **Putting devcontainer.json in the wrong location** -- It must be in `.devcontainer/devcontainer.json` or `.devcontainer.json` at the repository root. Nested paths like `src/.devcontainer/` are not detected.

2. **Not using `postCreateCommand` for dependency installation** -- Installing dependencies in the Dockerfile means they are baked into the image and not updated. Use `postCreateCommand` to install from the current lockfile.

3. **Forgetting `forwardPorts`** -- Ports exposed by services (databases, dev servers) are not automatically forwarded. Add them to `forwardPorts` or they will not be accessible from the host.

4. **Using root as the default user** -- Dev container images create a `vscode` user by default. Ensure file permissions work for this user. Set `"remoteUser": "vscode"` explicitly.

5. **Not caching Codespaces prebuilds** -- Without prebuilds, every Codespace creation runs the full build. Enable prebuilds in repository settings to reduce startup time.

6. **Installing too many features** -- Each feature adds layers and startup time. Only add features you actually use. Prefer a custom Dockerfile for complex setups.

7. **Hardcoding paths** -- Use `${containerWorkspaceFolder}` instead of hardcoded paths. The workspace mount point may differ between local dev containers and Codespaces.

8. **Missing Docker Compose volumes** -- Without a volume mount, source code changes on the host are not reflected in the container. Use `- ..:/workspace:cached` for bind mounts.

## Best Practices

- [ ] Place `devcontainer.json` in `.devcontainer/` for discoverability
- [ ] Use pre-built images from `mcr.microsoft.com/devcontainers/` when possible
- [ ] Pin feature versions to major version (`features/python:1`, not `:latest`)
- [ ] Use `postCreateCommand` for dependency installation (not Dockerfile RUN)
- [ ] Set `remoteUser` to a non-root user (typically `"vscode"`)
- [ ] Add `forwardPorts` for all services your development workflow needs
- [ ] Include essential VS Code extensions in `customizations.vscode.extensions`
- [ ] Use `postStartCommand` for actions that should run on every container start
- [ ] Enable Codespaces prebuilds for repositories with long build times
- [ ] Keep the dev container close to production (same OS, same Python version)
- [ ] Use named configurations (`.devcontainer/<name>/devcontainer.json`) for multi-environment repos
- [ ] Document required secrets in the `secrets` property for Codespaces users
- [ ] Test dev containers locally before relying on Codespaces

## Resources

### Official Documentation
- **Dev Containers Specification**: https://containers.dev/
- **VS Code Dev Containers**: https://code.visualstudio.com/docs/devcontainers/containers
- **GitHub Codespaces**: https://docs.github.com/en/codespaces
- **devcontainer.json Reference**: https://containers.dev/implementors/json_reference/

### Features
- **Official Features**: https://github.com/devcontainers/features
- **Community Features**: https://github.com/devcontainers-contrib/features
- **Feature Specification**: https://containers.dev/implementors/features/

### Templates
- **Official Templates**: https://github.com/devcontainers/templates
- **Microsoft Dev Container Images**: https://mcr.microsoft.com/en-us/catalog?search=devcontainers

### Tools
- **Dev Container CLI**: https://github.com/devcontainers/cli
- **GitHub Codespaces Prebuilds**: https://docs.github.com/en/codespaces/prebuilding-your-codespaces

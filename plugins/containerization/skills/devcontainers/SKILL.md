---
name: devcontainers
description: Use when the user asks to create, configure, or troubleshoot dev containers, devcontainer.json files, or GitHub Codespaces setups. Creates and configures devcontainer.json, adds features and lifecycle hooks, supports Docker Compose dev environments, and validates container setup for reproducible development.
metadata:
  references:
    - references/devcontainer-json.md
    - references/features-and-customization.md
    - references/validation-and-troubleshooting.md
  assets:
    - assets/python-devcontainer.json
    - assets/rust-devcontainer.json
    - assets/node-devcontainer.json
---

# Dev Containers

## Primary Actions

- Create or update `.devcontainer/devcontainer.json`.
- Configure features, editor extensions, and lifecycle hooks.
- Set up multi-container dev environments via Docker Compose.
- Configure Codespaces-specific requirements when needed.
- Diagnose and fix container startup/build/runtime issues.

## Minimal Template

```jsonc
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

## Validation Workflow

1. Create/update `devcontainer.json`.
2. Validate build:

```bash
devcontainer build --workspace-folder .
```

3. Rebuild/reopen container in editor.
4. Verify lifecycle hooks and required extensions.
5. If using Compose, verify dependent services are healthy/reachable.
6. If failures occur, fix config and repeat from step 2.

## Deep References

- Full `devcontainer.json` schema and lifecycle hooks:
  [references/devcontainer-json.md](references/devcontainer-json.md)
- Features, customization, prebuilds, machine options:
  [references/features-and-customization.md](references/features-and-customization.md)
- Validation and troubleshooting workflow:
  [references/validation-and-troubleshooting.md](references/validation-and-troubleshooting.md)

## Templates

- [assets/python-devcontainer.json](assets/python-devcontainer.json)
- [assets/rust-devcontainer.json](assets/rust-devcontainer.json)
- [assets/node-devcontainer.json](assets/node-devcontainer.json)

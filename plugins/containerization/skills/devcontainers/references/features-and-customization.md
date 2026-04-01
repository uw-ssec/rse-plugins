# Features and Customization -- Deep Reference

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| Official Features | 18-96 | Catalog of features maintained by the devcontainers org |
| Community Features | 98-146 | Third-party features, discovery, and quality considerations |
| Creating Custom Features | 148-276 | Feature structure, devcontainer-feature.json, install scripts |
| Feature Options | 278-353 | Parameterizing features, option types, defaults |
| VS Code Customizations | 355-461 | Extensions, settings, keybindings, and editor configuration |
| Codespaces Prebuilds | 463-520 | Prebuild configuration, triggers, caching, and optimization |
| Dotfiles | 522-582 | Dotfiles repositories, automatic setup, customization |
| Machine Types | 584-640 | Codespaces machine types, resource requirements, GPU |

---

## Official Features

### Overview

Official features are maintained by the `devcontainers` organization and published to `ghcr.io/devcontainers/features/`. They are the most stable and well-tested option.

### Language Runtimes

| Feature | Image | Key Options |
|---------|-------|-------------|
| Python | `ghcr.io/devcontainers/features/python:1` | `version`, `installTools` |
| Node.js | `ghcr.io/devcontainers/features/node:1` | `version`, `nodeGypDependencies` |
| Go | `ghcr.io/devcontainers/features/go:1` | `version`, `golangciLintVersion` |
| Rust | `ghcr.io/devcontainers/features/rust:1` | `version`, `profile` |
| Java | `ghcr.io/devcontainers/features/java:1` | `version`, `installGradle`, `installMaven` |
| .NET | `ghcr.io/devcontainers/features/dotnet:2` | `version` |
| Ruby | `ghcr.io/devcontainers/features/ruby:1` | `version` |
| PHP | `ghcr.io/devcontainers/features/php:1` | `version` |

### Developer Tools

| Feature | Image | Purpose |
|---------|-------|---------|
| Docker-in-Docker | `ghcr.io/devcontainers/features/docker-in-docker:2` | Run Docker inside the container |
| Docker-from-Docker | `ghcr.io/devcontainers/features/docker-outside-of-docker:1` | Use host Docker socket |
| GitHub CLI | `ghcr.io/devcontainers/features/github-cli:1` | `gh` command for GitHub operations |
| Azure CLI | `ghcr.io/devcontainers/features/azure-cli:1` | `az` command for Azure |
| AWS CLI | `ghcr.io/devcontainers/features/aws-cli:1` | `aws` command for AWS |
| kubectl | `ghcr.io/devcontainers/features/kubectl-helm-minikube:1` | Kubernetes tools |
| Terraform | `ghcr.io/devcontainers/features/terraform:1` | IaC tool |
| NVIDIA CUDA | `ghcr.io/devcontainers/features/nvidia-cuda:1` | GPU compute in dev containers |

### Shell and Common Utilities

| Feature | Image | Purpose |
|---------|-------|---------|
| Common Utilities | `ghcr.io/devcontainers/features/common-utils:2` | zsh, oh-my-zsh, git, curl, etc. |
| Git | `ghcr.io/devcontainers/features/git:1` | Specific git version |
| Git LFS | `ghcr.io/devcontainers/features/git-lfs:1` | Git Large File Storage |
| SSH Server | `ghcr.io/devcontainers/features/sshd:1` | SSH into the container |

### Usage Example

```jsonc
{
  "features": {
    "ghcr.io/devcontainers/features/python:1": {
      "version": "3.12",
      "installTools": true
    },
    "ghcr.io/devcontainers/features/node:1": {
      "version": "22"
    },
    "ghcr.io/devcontainers/features/github-cli:1": {},
    "ghcr.io/devcontainers/features/docker-in-docker:2": {
      "dockerDashComposeVersion": "v2"
    }
  }
}
```

### Version Pinning

```jsonc
{
  "features": {
    // Pin to major version (recommended -- gets minor/patch updates)
    "ghcr.io/devcontainers/features/python:1": {},

    // Pin to exact version (most stable)
    "ghcr.io/devcontainers/features/python:1.2.3": {},

    // Latest (not recommended -- may break)
    "ghcr.io/devcontainers/features/python:latest": {}
  }
}
```

---

## Community Features

### Discovery

Community features are published by third parties and available on the Dev Containers feature index:

- **Browse**: https://containers.dev/features
- **GitHub org**: https://github.com/devcontainers-contrib/features

### Popular Community Features

| Feature | Image | Purpose |
|---------|-------|---------|
| Ruff | `ghcr.io/devcontainers-contrib/features/ruff:1` | Python linter/formatter |
| Poetry | `ghcr.io/devcontainers-contrib/features/poetry:2` | Python dependency management |
| Homebrew | `ghcr.io/meaningful-ooo/devcontainer-features/homebrew:2` | macOS-style package manager |
| Nix | `ghcr.io/devcontainers-contrib/features/nix-installer:1` | Nix package manager |
| Just | `ghcr.io/devcontainers-contrib/features/just:1` | Command runner |
| Starship | `ghcr.io/devcontainers-contrib/features/starship:1` | Shell prompt |
| Pre-commit | `ghcr.io/devcontainers-contrib/features/pre-commit:2` | Git pre-commit hooks |
| uv | `ghcr.io/devcontainers-contrib/features/uv:1` | Fast Python package installer |

### Quality Considerations

When evaluating community features:

1. **Check maintenance status**: Look at the repository's last commit date and issue response time
2. **Review the install script**: Features run as root during container build -- review `install.sh` for security
3. **Check compatibility**: Some features may conflict with others or with specific base images
4. **Pin versions**: Community features may have breaking changes -- pin to specific versions
5. **Fallback plan**: If a community feature breaks, be prepared to install the tool in your Dockerfile instead

### Using Community Features

```jsonc
{
  "features": {
    // Community features use the same syntax as official ones
    "ghcr.io/devcontainers-contrib/features/ruff:1": {
      "version": "latest"
    },
    "ghcr.io/devcontainers-contrib/features/poetry:2": {
      "version": "1.8"
    }
  }
}
```

---

## Creating Custom Features

### Feature Structure

A dev container feature is a directory or repository with this structure:

```
my-feature/
  devcontainer-feature.json   # Feature metadata and options
  install.sh                  # Installation script (runs as root)
  README.md                   # Documentation (auto-generated)
```

### devcontainer-feature.json

```json
{
  "id": "my-tool",
  "version": "1.0.0",
  "name": "My Tool",
  "description": "Installs my-tool for development",
  "options": {
    "version": {
      "type": "string",
      "default": "latest",
      "description": "Version of my-tool to install"
    },
    "installExtras": {
      "type": "boolean",
      "default": false,
      "description": "Install optional extra components"
    }
  },
  "installsAfter": [
    "ghcr.io/devcontainers/features/common-utils"
  ],
  "containerEnv": {
    "MY_TOOL_HOME": "/usr/local/my-tool"
  }
}
```

### install.sh

The installation script runs as root during container build:

```bash
#!/bin/bash
set -e

# Options from devcontainer-feature.json are available as environment variables
# prefixed with the option name in uppercase
VERSION="${VERSION:-latest}"
INSTALL_EXTRAS="${INSTALLEXTRAS:-false}"

echo "Installing my-tool version ${VERSION}..."

# Install dependencies
apt-get update
apt-get install -y --no-install-recommends curl ca-certificates

# Download and install
if [ "$VERSION" = "latest" ]; then
    curl -fsSL https://example.com/install.sh | bash
else
    curl -fsSL "https://example.com/releases/v${VERSION}/install.sh" | bash
fi

# Optional extras
if [ "$INSTALL_EXTRAS" = "true" ]; then
    my-tool install-extras
fi

# Clean up
apt-get clean
rm -rf /var/lib/apt/lists/*

echo "my-tool ${VERSION} installed successfully"
```

### Publishing Features

Publish features to GHCR using the devcontainer CLI:

```bash
# Install the CLI
npm install -g @devcontainers/cli

# Build and publish
devcontainer features publish ./my-feature \
  --registry ghcr.io \
  --namespace myorg/features
```

After publishing, the feature is available as:
```jsonc
{
  "features": {
    "ghcr.io/myorg/features/my-tool:1": {
      "version": "2.0"
    }
  }
}
```

### Local Features

For features specific to a single project, use a local path:

```jsonc
{
  "features": {
    "./my-feature": {
      "version": "1.0"
    }
  }
}
```

Place the feature directory relative to `devcontainer.json`:
```
.devcontainer/
  devcontainer.json
  my-feature/
    devcontainer-feature.json
    install.sh
```

---

## Feature Options

### Option Types

Features support these option types:

| Type | JSON Type | Example |
|------|-----------|---------|
| `string` | string | `"version": "3.12"` |
| `boolean` | boolean | `"installTools": true` |
| `enum` | string (restricted) | `"variant": "slim"` |

### Defining Options

```json
{
  "options": {
    "version": {
      "type": "string",
      "default": "latest",
      "description": "Tool version to install",
      "proposals": ["latest", "1.0", "2.0"]
    },
    "variant": {
      "type": "string",
      "enum": ["full", "slim", "minimal"],
      "default": "full",
      "description": "Installation variant"
    },
    "installDocs": {
      "type": "boolean",
      "default": false,
      "description": "Install documentation"
    }
  }
}
```

### Using Options in install.sh

Options are available as uppercased environment variables:

```bash
#!/bin/bash
set -e

# "version" option -> $VERSION
# "variant" option -> $VARIANT
# "installDocs" option -> $INSTALLDOCS

echo "Version: ${VERSION}"
echo "Variant: ${VARIANT}"
echo "Install docs: ${INSTALLDOCS}"

case "${VARIANT}" in
    full)    install_full "${VERSION}" ;;
    slim)    install_slim "${VERSION}" ;;
    minimal) install_minimal "${VERSION}" ;;
esac
```

### Passing Options in devcontainer.json

```jsonc
{
  "features": {
    "ghcr.io/myorg/features/my-tool:1": {
      "version": "2.0",
      "variant": "slim",
      "installDocs": true
    }
  }
}
```

---

## VS Code Customizations

### Extensions

Install VS Code extensions automatically when the container is created:

```jsonc
{
  "customizations": {
    "vscode": {
      "extensions": [
        // Language support
        "ms-python.python",
        "ms-python.vscode-pylance",
        "rust-lang.rust-analyzer",

        // Formatting and linting
        "charliermarsh.ruff",
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",

        // Productivity
        "eamodio.gitlens",
        "github.copilot",
        "ms-toolsai.jupyter",

        // Containers and infrastructure
        "ms-azuretools.vscode-docker",
        "ms-kubernetes-tools.vscode-kubernetes-tools"
      ]
    }
  }
}
```

### Finding Extension IDs

1. Open VS Code Marketplace or the Extensions panel
2. Find the extension
3. The ID is in the format `publisher.extensionName`
4. Or use the command palette: "Extensions: Copy Extension ID"

### Settings

Override VS Code settings for the dev container:

```jsonc
{
  "customizations": {
    "vscode": {
      "settings": {
        // Editor
        "editor.formatOnSave": true,
        "editor.rulers": [88, 120],
        "editor.tabSize": 4,
        "files.trimTrailingWhitespace": true,
        "files.insertFinalNewline": true,

        // Python
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "python.testing.pytestEnabled": true,
        "python.testing.pytestArgs": ["tests/"],
        "[python]": {
          "editor.defaultFormatter": "charliermarsh.ruff",
          "editor.formatOnSave": true,
          "editor.codeActionsOnSave": {
            "source.fixAll.ruff": "explicit",
            "source.organizeImports.ruff": "explicit"
          }
        },

        // Terminal
        "terminal.integrated.defaultProfile.linux": "zsh",

        // Files
        "files.exclude": {
          "**/__pycache__": true,
          "**/.pytest_cache": true,
          "**/node_modules": true
        }
      }
    }
  }
}
```

### Tool-Specific Customizations

Dev containers also support customizations for other tools:

```jsonc
{
  "customizations": {
    // JetBrains IDEs
    "jetbrains": {
      "plugins": ["com.intellij.plugins.watcher"]
    },

    // GitHub Codespaces
    "codespaces": {
      "openFiles": ["README.md", "src/main.py"]
    }
  }
}
```

---

## Codespaces Prebuilds

### What are Prebuilds?

Prebuilds create a pre-configured dev container image in advance, so starting a Codespace is nearly instant (seconds instead of minutes).

### Configuring Prebuilds

1. Go to repository Settings > Codespaces > Prebuilds
2. Click "Set up prebuild"
3. Configure:
   - **Branch**: Which branch(es) to prebuild (typically `main`)
   - **Regions**: Which data center regions to prebuild in
   - **Trigger**: When to rebuild (push, schedule, or configuration change)

### Prebuild Triggers

| Trigger | When It Fires | Best For |
|---------|--------------|----------|
| Push to branch | Every push to configured branch | Active development |
| Configuration change | When devcontainer.json changes | Stable projects |
| Scheduled | On a cron schedule | Projects with external dependencies |

### Optimizing Prebuild Time

1. **Move heavy installs to the Dockerfile or features**: These are cached as Docker layers
2. **Use `updateContentCommand` for dependency installation**: Runs during prebuild
3. **Move quick setup to `postStartCommand`**: Does not block prebuild
4. **Cache package manager data with volumes**:

```jsonc
{
  "mounts": [
    "source=pip-cache,target=/root/.cache/pip,type=volume"
  ]
}
```

### Prebuild Lifecycle

During a prebuild, the following lifecycle steps run:
1. Container is built (Dockerfile + features)
2. `onCreateCommand` runs
3. `updateContentCommand` runs
4. `postCreateCommand` runs

When a user creates a Codespace from a prebuild:
1. Pre-built image is loaded (fast)
2. `postStartCommand` runs
3. `postAttachCommand` runs

### Costs

- Prebuilds consume GitHub Actions minutes
- Stored prebuild images consume Codespaces storage
- Configure retention to limit storage costs

---

## Dotfiles

### Overview

Dotfiles let you personalize your dev container with your shell configuration, aliases, and tools. GitHub Codespaces and VS Code dev containers both support automatic dotfiles setup.

### Codespaces Dotfiles

Configure in GitHub Settings > Codespaces > Dotfiles:

1. Set your dotfiles repository (e.g., `username/dotfiles`)
2. Set the install command (default: looks for `install.sh`, `setup.sh`, or `bootstrap.sh`)
3. Codespaces clones your dotfiles repo and runs the install script on every new Codespace

### Dotfiles Repository Structure

```
dotfiles/
  .bashrc
  .zshrc
  .gitconfig
  .vimrc
  install.sh       # Installation script
```

### Example install.sh

```bash
#!/bin/bash
set -e

DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Symlink dotfiles
for file in .bashrc .zshrc .gitconfig .vimrc; do
    if [ -f "$DOTFILES_DIR/$file" ]; then
        ln -sf "$DOTFILES_DIR/$file" "$HOME/$file"
    fi
done

# Install additional tools
if command -v apt-get &> /dev/null; then
    sudo apt-get update && sudo apt-get install -y ripgrep fd-find fzf
fi

echo "Dotfiles installed successfully"
```

### Local Dev Container Dotfiles

For local VS Code dev containers, configure in VS Code settings:

```json
{
  "dotfiles.repository": "username/dotfiles",
  "dotfiles.targetPath": "~/dotfiles",
  "dotfiles.installCommand": "install.sh"
}
```

---

## Machine Types

### Codespaces Machine Types

GitHub Codespaces offers several machine types:

| Machine | CPUs | Memory | Storage | Use Case |
|---------|------|--------|---------|----------|
| 2-core | 2 | 8 GB | 32 GB | Light editing, small projects |
| 4-core | 4 | 16 GB | 32 GB | Most development (default) |
| 8-core | 8 | 32 GB | 64 GB | Large projects, compilation |
| 16-core | 16 | 64 GB | 128 GB | Data science, ML training |
| 32-core | 32 | 128 GB | 128 GB | Heavy compilation, large datasets |
| GPU | 4+ | 16+ GB | 64+ GB | ML/AI development (limited availability) |

### Specifying Requirements

Use `hostRequirements` to set minimum machine requirements:

```jsonc
{
  "hostRequirements": {
    "cpus": 4,
    "memory": "8gb",
    "storage": "32gb"
  }
}
```

Users can always choose a larger machine, but Codespaces will not offer machines below the minimum.

### GPU Machine Types

GPU-enabled Codespaces are available on GitHub Enterprise or by request:

```jsonc
{
  "hostRequirements": {
    "cpus": 4,
    "memory": "16gb",
    "storage": "64gb",
    "gpu": true
  },
  "features": {
    "ghcr.io/devcontainers/features/nvidia-cuda:1": {
      "installCudnn": true
    }
  },
  "runArgs": ["--gpus", "all"]
}
```

### Cost Optimization

- Use the smallest machine that meets your needs
- Set idle timeout in GitHub Settings > Codespaces to auto-stop unused Codespaces
- Use prebuilds to reduce active compute time
- Delete Codespaces you are no longer using

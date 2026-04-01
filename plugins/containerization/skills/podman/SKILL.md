---
name: podman
description: Rootless container management with Podman including Docker CLI compatibility, systemd integration, pod management, Quadlet, and Podman Compose for research environments.
metadata:
  references:
    - references/rootless-containers.md
    - references/docker-compatibility.md
  assets:
    - assets/podman-compose-example.yml
    - assets/quadlet-example.container
---

# Podman

A comprehensive guide to using Podman for rootless, daemonless container management in research environments. Podman provides a Docker-compatible CLI without requiring a root-level daemon, making it a natural fit for shared HPC clusters, institutional workstations, and security-conscious deployments. This skill covers the Docker-to-Podman migration path, rootless container setup, pod management, systemd integration via Quadlet, Podman Compose, building images with Buildah, and registry operations.

## Resources in This Skill

This skill includes supporting materials for Podman-based container workflows:

**References** (detailed guides -- consult the table of contents in each file and read specific sections as needed):
- `references/rootless-containers.md` - Rootless container architecture: user namespace mapping, subuid/subgid configuration, storage drivers, rootless networking (slirp4netns, pasta), volume permissions, cgroup v2 requirements, and troubleshooting
- `references/docker-compatibility.md` - Docker compatibility layer: CLI compatibility matrix, Dockerfile support, Compose compatibility, socket emulation with podman-docker, known differences in networking/volumes/build behavior, and a migration checklist

**Assets** (ready-to-use templates):
- `assets/podman-compose-example.yml` - Research stack compose file adapted for Podman with JupyterLab, REST API, and PostgreSQL
- `assets/quadlet-example.container` - Systemd Quadlet unit file for auto-starting a containerized research service

## Quick Reference Card

### Docker-to-Podman Command Mapping

| Docker Command | Podman Equivalent | Notes |
|----------------|-------------------|-------|
| `docker run` | `podman run` | Identical syntax |
| `docker build` | `podman build` | Uses Buildah under the hood |
| `docker compose up` | `podman compose up` | Requires podman-compose or docker-compose with Podman socket |
| `docker ps` | `podman ps` | Identical syntax |
| `docker images` | `podman images` | Identical syntax |
| `docker pull` | `podman pull` | Searches multiple registries by default |
| `docker push` | `podman push` | Identical syntax |
| `docker exec` | `podman exec` | Identical syntax |
| `docker logs` | `podman logs` | Identical syntax |
| `docker inspect` | `podman inspect` | Identical syntax |
| `docker volume` | `podman volume` | Identical syntax |
| `docker network` | `podman network` | Uses Netavark by default (not Docker bridge) |
| `docker login` | `podman login` | Identical syntax |
| `docker tag` | `podman tag` | Identical syntax |
| `docker save/load` | `podman save/load` | Identical syntax |
| `docker system prune` | `podman system prune` | Identical syntax |
| N/A | `podman pod create` | Pod management (no Docker equivalent) |
| N/A | `podman generate systemd` | Generate systemd units (legacy; use Quadlet) |
| N/A | `podman generate kube` | Generate Kubernetes YAML from running containers |
| `docker swarm` | N/A | Podman does not support Swarm; use Kubernetes |

### Essential Podman Commands

```bash
# Container lifecycle
podman run -d --name myapp -p 8000:8000 myimage:latest
podman stop myapp
podman rm myapp
podman start myapp

# Rootless info
podman info --format '{{.Host.Security.Rootless}}'
podman unshare cat /proc/self/uid_map

# Pod management
podman pod create --name research -p 8888:8888 -p 8000:8000
podman run -d --pod research --name jupyter jupyter/scipy-notebook
podman pod stop research
podman pod rm research

# System
podman system info
podman system prune --all --force
podman system migrate            # After major upgrades
```

## When to Use

Use this skill when you need to:

- Run containers without root privileges on shared infrastructure (HPC, lab workstations)
- Migrate an existing Docker workflow to Podman
- Manage containers with systemd integration for auto-start on boot
- Group related containers into pods (Kubernetes-style)
- Use Quadlet to declare containers as systemd units
- Build OCI images without a Docker daemon
- Run containers on a system where Docker is not installed or not permitted
- Generate Kubernetes YAML from running containers for deployment migration

## Podman vs Docker

Podman and Docker both manage OCI containers, but they differ in architecture and security posture.

### Architecture

| Aspect | Docker | Podman |
|--------|--------|--------|
| Daemon | Central daemon (dockerd) running as root | No daemon; each command is a fork-exec |
| Root requirement | Daemon runs as root; rootless mode is optional | Rootless by default |
| Process model | Containers are children of the daemon | Containers are children of the calling process |
| Init system | Requires separate restart config | Native systemd integration via Quadlet |
| Compose | docker compose (built-in plugin) | podman compose (wrapper) or podman-compose (Python) |
| Swarm | Built-in orchestration | Not supported; use Kubernetes |
| Build engine | BuildKit | Buildah (integrated) |
| Image format | OCI / Docker | OCI / Docker |

### When Docker Might Be Better

- You need Docker Swarm for orchestration
- Your CI/CD pipeline is tightly coupled to the Docker socket
- Your team is already productive with Docker and has no need to change
- You depend on Docker Desktop features (GUI, extensions, Dev Environments)

### When Podman Is the Better Choice

- Your institution prohibits root-level daemons on shared systems
- You want containers to start and stop with systemd
- You need Kubernetes YAML generation from running containers
- You want a daemonless architecture (no single point of failure)
- You are working on RHEL, CentOS Stream, or Fedora where Podman ships by default

## Rootless Container Setup

Rootless mode runs containers entirely within a user's namespace, requiring no elevated privileges. This is Podman's default mode.

### Prerequisites

```bash
# Check kernel support for user namespaces
sysctl user.max_user_namespaces
# Should return a value > 0 (e.g., 15000)

# Verify subuid/subgid entries exist for your user
grep $USER /etc/subuid
grep $USER /etc/subgid
# Expected output: username:100000:65536

# If missing, add them (requires root once)
sudo usermod --add-subuids 100000-165535 --add-subgids 100000-165535 $USER
podman system migrate
```

### First Run

```bash
# Verify rootless mode is active
podman info --format '{{.Host.Security.Rootless}}'
# true

# Run a test container
podman run --rm docker.io/library/alpine echo "Rootless works"
```

See `references/rootless-containers.md` for detailed coverage of user namespace mapping, storage drivers, networking, and volume permissions.

## Docker CLI Compatibility

### Alias Approach

The simplest migration path is to alias `docker` to `podman`:

```bash
# Add to ~/.bashrc or ~/.zshrc
alias docker=podman
```

This works for most single-container workflows. Commands like `docker run`, `docker build`, `docker pull`, and `docker exec` are fully compatible.

### Podman-Docker Package

For deeper compatibility, install the `podman-docker` package, which provides a `docker` binary that calls `podman` and emulates the Docker socket:

```bash
# Fedora / RHEL / CentOS
sudo dnf install podman-docker

# Ubuntu / Debian
sudo apt install podman-docker

# This also provides /var/run/docker.sock emulation via podman.socket
sudo systemctl enable --now podman.socket
```

### Socket Emulation

Some tools (like VS Code Dev Containers or Testcontainers) require a Docker-compatible socket. Podman can provide one:

```bash
# User-level socket (rootless)
systemctl --user enable --now podman.socket
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/podman/podman.sock

# System-level socket (rootful, for tools requiring /var/run/docker.sock)
sudo systemctl enable --now podman.socket
```

### Compose Compatibility

Podman supports Compose through two paths:

```bash
# Option 1: podman compose (uses docker-compose or podman-compose under the hood)
podman compose up -d

# Option 2: Install podman-compose (Python reimplementation)
pip install podman-compose
podman-compose up -d

# Option 3: Use docker-compose with Podman socket
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/podman/podman.sock
docker-compose up -d
```

See `references/docker-compatibility.md` for the full CLI compatibility matrix and known behavioral differences.

## Podman Compose vs Docker Compose

Podman Compose supports most Docker Compose features but has some differences:

| Feature | Docker Compose | Podman Compose |
|---------|---------------|----------------|
| `depends_on` with conditions | Full support | Supported (podman-compose 1.1+) |
| `profiles` | Full support | Supported |
| `build` | BuildKit | Buildah |
| `secrets` (file-based) | Full support | Supported |
| `networks` (custom drivers) | Full support | Netavark only |
| `deploy` (resource limits) | Swarm/Compose v2 | Limited |
| Watch mode | `docker compose watch` | Not available |
| GPU passthrough | `deploy.resources.reservations.devices` | `--device` via CLI or CDI |

```bash
# Validate a compose file with Podman
podman compose config

# Start services in detached mode
podman compose up -d

# View logs
podman compose logs -f

# Tear down
podman compose down
```

See `assets/podman-compose-example.yml` for a research stack template adapted for Podman.

## Pod Management

Pods are a Podman-specific concept (borrowed from Kubernetes) that groups multiple containers sharing a network namespace and optionally other namespaces. All containers in a pod share `localhost`.

### Creating and Using Pods

```bash
# Create a pod with published ports
podman pod create --name research-stack \
    -p 8888:8888 \
    -p 8000:8000 \
    -p 5432:5432

# Add containers to the pod
podman run -d --pod research-stack \
    --name jupyter \
    -e JUPYTER_TOKEN=changeme \
    quay.io/jupyter/scipy-notebook:latest

podman run -d --pod research-stack \
    --name api \
    myresearch-api:latest

podman run -d --pod research-stack \
    --name db \
    -e POSTGRES_PASSWORD=changeme \
    docker.io/library/postgres:16-alpine

# Containers communicate over localhost within the pod
# The API can reach the database at localhost:5432
```

### Pod Lifecycle

```bash
podman pod list                    # List all pods
podman pod inspect research-stack  # Show pod details
podman pod top research-stack      # Show processes in all containers
podman pod stop research-stack     # Stop all containers in the pod
podman pod start research-stack    # Start all containers in the pod
podman pod rm research-stack       # Remove the pod and its containers
podman pod rm -f research-stack    # Force-remove (stops first)
```

### Generating Kubernetes YAML from Pods

```bash
# Generate a Kubernetes Pod manifest from a running pod
podman generate kube research-stack > research-stack.yml

# Apply it to a Kubernetes cluster
kubectl apply -f research-stack.yml

# Or replay it with Podman
podman play kube research-stack.yml
```

## Systemd Integration and Quadlet

Quadlet is the modern way to manage Podman containers with systemd. You write declarative `.container` files (similar to systemd unit files) and systemd manages the container lifecycle.

### Quadlet File Locations

```
~/.config/containers/systemd/     # Rootless (per-user)
/etc/containers/systemd/          # Rootful (system-wide)
```

### Using Quadlet

```bash
# 1. Write a .container file (see assets/quadlet-example.container)
cp quadlet-example.container ~/.config/containers/systemd/research-api.container

# 2. Reload systemd to pick up the new unit
systemctl --user daemon-reload

# 3. Start the service
systemctl --user start research-api

# 4. Enable auto-start on login
systemctl --user enable research-api

# 5. Persist user services after logout (lingering)
loginctl enable-linger $USER

# Check status
systemctl --user status research-api
journalctl --user -u research-api -f
```

See `assets/quadlet-example.container` for an annotated Quadlet unit file.

### Legacy: podman generate systemd

The older approach generates systemd unit files from running containers. Quadlet is preferred for new setups.

```bash
# Generate a unit file from a running container (deprecated approach)
podman generate systemd --new --name mycontainer > ~/.config/systemd/user/mycontainer.service
systemctl --user daemon-reload
systemctl --user enable --now mycontainer
```

## Podman Machine (macOS / Windows)

On macOS and Windows, Podman runs containers inside a Linux virtual machine managed by `podman machine`.

```bash
# Initialize a machine (downloads a Fedora CoreOS image)
podman machine init

# Start the machine
podman machine start

# Check machine status
podman machine list
podman machine info

# SSH into the machine for debugging
podman machine ssh

# Stop the machine
podman machine stop

# Customize resources
podman machine init --cpus 4 --memory 8192 --disk-size 100

# Set the machine to rootful mode (for tools that require root)
podman machine set --rootful
```

### macOS-Specific Notes

- Podman Desktop provides a GUI (alternative to Docker Desktop)
- File sharing between host and VM uses virtiofs (fast) or 9p
- The Podman socket is automatically forwarded to the host
- Rosetta 2 can run amd64 containers on Apple Silicon (with `--platform linux/amd64`)

## Building Images (Buildah)

Podman delegates image building to Buildah. All `podman build` commands use Buildah under the hood. You can also use Buildah directly for more advanced workflows.

### Building with Podman

```bash
# Standard build (same syntax as docker build)
podman build -t myimage:latest .

# Multi-platform build
podman build --platform linux/amd64,linux/arm64 -t myimage:latest .

# Build with build arguments
podman build --build-arg PYTHON_VERSION=3.12 -t myimage:latest .

# Build from a specific Dockerfile
podman build -f Containerfile -t myimage:latest .
```

### Buildah Direct Usage

```bash
# Create a container from a base image
container=$(buildah from python:3.12-slim)

# Run commands inside
buildah run $container pip install numpy pandas

# Copy files in
buildah copy $container ./app /app

# Set the entrypoint
buildah config --entrypoint '["python", "-m", "myapp"]' $container

# Commit to an image
buildah commit $container myimage:latest
```

### Containerfile vs Dockerfile

Podman accepts both `Containerfile` and `Dockerfile`. The syntax is identical. `Containerfile` is the OCI-standard name, and Podman searches for it first.

## Registry Operations

### Configuring Registries

Podman searches multiple registries by default. Configure them in `/etc/containers/registries.conf` or `~/.config/containers/registries.conf`:

```toml
# Short-name resolution order
unqualified-search-registries = ["docker.io", "quay.io", "ghcr.io"]
```

### Login and Push

```bash
# Log in to a registry
podman login docker.io
podman login ghcr.io
podman login quay.io

# Tag and push
podman tag myimage:latest ghcr.io/myorg/myimage:latest
podman push ghcr.io/myorg/myimage:latest

# Pull from a specific registry
podman pull docker.io/library/python:3.12-slim
```

### Skopeo for Registry Inspection

```bash
# Inspect a remote image without pulling it
skopeo inspect docker://docker.io/library/python:3.12-slim

# Copy between registries
skopeo copy docker://docker.io/myimage:latest docker://ghcr.io/myorg/myimage:latest

# Copy to a local directory (OCI layout)
skopeo copy docker://myimage:latest oci:./myimage-oci:latest
```

## Common Mistakes

1. **Expecting Docker socket at /var/run/docker.sock** -- Podman's rootless socket is at `$XDG_RUNTIME_DIR/podman/podman.sock`. Enable it with `systemctl --user enable --now podman.socket` and set `DOCKER_HOST` accordingly.

2. **Forgetting to configure subuid/subgid** -- Rootless containers require subordinate UID/GID ranges. Without them, `podman run` fails with user namespace errors. Check `/etc/subuid` and `/etc/subgid`.

3. **Using `--privileged` to fix permission errors** -- This defeats the purpose of rootless containers. Instead, understand user namespace ID mapping and set volume ownership correctly.

4. **Ignoring cgroup v2 requirements** -- Rootless resource limits (CPU, memory) require cgroup v2. On older systems with cgroup v1, these flags are silently ignored.

5. **Confusing Podman Compose with Docker Compose** -- They are separate tools. `podman compose` is a thin wrapper that delegates to `docker-compose` or `podman-compose`. Install one of them first.

6. **Not enabling linger for user services** -- Without `loginctl enable-linger`, rootless systemd services (including Quadlet containers) stop when the user logs out.

7. **Assuming Docker volumes carry over** -- Podman stores volumes in a different location than Docker. Migrating from Docker requires re-creating volumes and copying data.

8. **Using `podman generate systemd` for new setups** -- This command is deprecated. Use Quadlet `.container` files instead for systemd integration.

9. **Forgetting `podman machine start` on macOS** -- Unlike Docker Desktop, Podman does not always auto-start the VM. Run `podman machine start` after a reboot or check with `podman machine list`.

10. **Pulling unqualified image names without configuring registries** -- Running `podman pull python:3.12` prompts interactively for which registry to use. Configure `unqualified-search-registries` in `registries.conf` or use fully qualified names like `docker.io/library/python:3.12`.

## Best Practices

- [ ] Use rootless mode by default; only use rootful when absolutely necessary
- [ ] Configure `unqualified-search-registries` to include `docker.io` to avoid interactive prompts
- [ ] Use Quadlet `.container` files for systemd-managed services instead of `podman generate systemd`
- [ ] Enable lingering (`loginctl enable-linger`) for user services that must survive logout
- [ ] Use pods to group related containers that need to share a network namespace
- [ ] Set `DOCKER_HOST` to the Podman socket when using tools that expect Docker
- [ ] Use `Containerfile` as the default name for build files (OCI standard)
- [ ] Pin image tags and use fully qualified registry names (`docker.io/library/python:3.12-slim`)
- [ ] Run `podman system migrate` after major Podman upgrades
- [ ] Use `podman auto-update` with Quadlet for automatic container image updates
- [ ] Keep secrets out of images; use `--secret` flag or environment variables at runtime
- [ ] Test on both amd64 and arm64 if your research group uses mixed architectures

## Resources

### Official Documentation
- **Podman Documentation**: https://docs.podman.io/
- **Podman Desktop**: https://podman-desktop.io/
- **Buildah Documentation**: https://buildah.io/
- **Skopeo Documentation**: https://github.com/containers/skopeo

### Rootless and Security
- **Rootless Podman**: https://github.com/containers/podman/blob/main/docs/tutorials/rootless_tutorial.md
- **Podman Security**: https://docs.podman.io/en/latest/markdown/podman.1.html

### Systemd and Quadlet
- **Quadlet Documentation**: https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
- **Running Containers with Systemd**: https://www.redhat.com/en/blog/quadlet-podman

### Compose and Pods
- **Podman Compose**: https://github.com/containers/podman-compose
- **Pod Management**: https://docs.podman.io/en/latest/markdown/podman-pod.1.html
- **Playing Kubernetes YAML**: https://docs.podman.io/en/latest/markdown/podman-kube-play.1.html

### Migration
- **Docker to Podman Migration**: https://podman.io/docs/installation
- **Podman vs Docker**: https://www.redhat.com/en/topics/containers/what-is-podman

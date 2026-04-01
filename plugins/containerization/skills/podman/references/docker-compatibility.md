# Docker Compatibility -- Deep Reference

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| CLI Compatibility Matrix | 16-98 | Command-by-command comparison of Docker and Podman CLI support |
| Dockerfile Compatibility | 100-151 | Dockerfile/Containerfile instruction support, BuildKit differences |
| Compose Compatibility | 153-216 | Compose file features, podman-compose vs docker-compose, limitations |
| Socket Emulation | 218-282 | podman-docker package, socket paths, DOCKER_HOST, systemd socket activation |
| Known Differences | 284-354 | Behavioral differences in networking, volumes, build, restart, and logging |
| Migration Checklist | 356-404 | Step-by-step checklist for moving a project from Docker to Podman |

---

## CLI Compatibility Matrix

Podman implements the Docker CLI interface. Most commands work identically. The table below covers every major command group.

### Container Commands

| Command | Docker | Podman | Compatibility |
|---------|--------|--------|---------------|
| `run` | Yes | Yes | Full -- identical flags |
| `exec` | Yes | Yes | Full |
| `start` | Yes | Yes | Full |
| `stop` | Yes | Yes | Full |
| `restart` | Yes | Yes | Full |
| `rm` | Yes | Yes | Full |
| `kill` | Yes | Yes | Full |
| `pause` / `unpause` | Yes | Yes | Full |
| `logs` | Yes | Yes | Full |
| `inspect` | Yes | Yes | Full |
| `cp` | Yes | Yes | Full |
| `diff` | Yes | Yes | Full |
| `top` | Yes | Yes | Full |
| `stats` | Yes | Yes | Full |
| `port` | Yes | Yes | Full |
| `wait` | Yes | Yes | Full |
| `attach` | Yes | Yes | Full |
| `rename` | Yes | Yes | Full |
| `update` | Yes | Yes | Partial -- limited resource updates in rootless |

### Image Commands

| Command | Docker | Podman | Compatibility |
|---------|--------|--------|---------------|
| `build` | Yes | Yes | Full (uses Buildah; no BuildKit features like `--secret` syntax) |
| `pull` | Yes | Yes | Full (multi-registry by default) |
| `push` | Yes | Yes | Full |
| `images` / `image ls` | Yes | Yes | Full |
| `rmi` / `image rm` | Yes | Yes | Full |
| `tag` | Yes | Yes | Full |
| `save` / `load` | Yes | Yes | Full |
| `import` / `export` | Yes | Yes | Full |
| `history` | Yes | Yes | Full |
| `image prune` | Yes | Yes | Full |

### System Commands

| Command | Docker | Podman | Compatibility |
|---------|--------|--------|---------------|
| `info` | Yes | Yes | Full (different output fields) |
| `version` | Yes | Yes | Full |
| `system prune` | Yes | Yes | Full |
| `system df` | Yes | Yes | Full |
| `events` | Yes | Yes | Full |
| `login` / `logout` | Yes | Yes | Full |

### Network Commands

| Command | Docker | Podman | Compatibility |
|---------|--------|--------|---------------|
| `network create` | Yes | Yes | Partial -- Netavark backend, not Docker bridge |
| `network ls` | Yes | Yes | Full |
| `network rm` | Yes | Yes | Full |
| `network inspect` | Yes | Yes | Full (different output format) |
| `network connect/disconnect` | Yes | Yes | Full |

### Volume Commands

| Command | Docker | Podman | Compatibility |
|---------|--------|--------|---------------|
| `volume create` | Yes | Yes | Full |
| `volume ls` | Yes | Yes | Full |
| `volume rm` | Yes | Yes | Full |
| `volume inspect` | Yes | Yes | Full |
| `volume prune` | Yes | Yes | Full |

### Docker-Only Commands (No Podman Equivalent)

| Command | Purpose | Podman Alternative |
|---------|---------|-------------------|
| `docker swarm` | Swarm orchestration | Use Kubernetes + `podman generate kube` |
| `docker service` | Swarm services | Use Kubernetes |
| `docker stack` | Swarm stacks | Use Kubernetes or Compose |
| `docker config` (Swarm) | Swarm configs | Use Kubernetes ConfigMaps |
| `docker context` | Manage Docker contexts | `podman system connection` |

## Dockerfile Compatibility

### Instruction Support

Podman (via Buildah) supports all standard Dockerfile instructions:

| Instruction | Support | Notes |
|-------------|---------|-------|
| `FROM` | Full | Multi-stage, `AS` naming, `--platform` |
| `RUN` | Full | `--mount=type=cache` supported |
| `COPY` | Full | `--from=stage` supported |
| `ADD` | Full | URL fetching, tar extraction |
| `WORKDIR` | Full | |
| `ENV` | Full | |
| `ARG` | Full | |
| `EXPOSE` | Full | Metadata only |
| `VOLUME` | Full | |
| `USER` | Full | |
| `CMD` | Full | |
| `ENTRYPOINT` | Full | |
| `HEALTHCHECK` | Full | |
| `LABEL` | Full | |
| `SHELL` | Full | |
| `STOPSIGNAL` | Full | |
| `ONBUILD` | Full | |

### BuildKit-Specific Features

Docker's BuildKit introduces features that may not have direct Podman equivalents:

| Feature | Docker (BuildKit) | Podman (Buildah) |
|---------|-------------------|------------------|
| `RUN --mount=type=cache` | Yes | Yes (Buildah 1.28+) |
| `RUN --mount=type=secret` | Yes | Yes (Buildah 1.28+) |
| `RUN --mount=type=ssh` | Yes | Yes (Buildah 1.28+) |
| `RUN --mount=type=bind` | Yes | Yes |
| `COPY --link` | Yes | Yes (Buildah 1.29+) |
| `#syntax=` directive | Yes | Not supported |
| Heredoc syntax (`<<EOF`) | Yes | Yes (Buildah 1.29+) |
| Named build contexts (`--build-context`) | Yes | Yes (Podman 4.2+) |

### Containerfile vs Dockerfile

Podman searches for build files in this order:
1. `Containerfile`
2. `Dockerfile`

Both file names work identically. `Containerfile` is the OCI-standard name. Use `-f` to specify an alternative:

```bash
podman build -f Containerfile.dev -t myimage:dev .
```

## Compose Compatibility

### Compose File Support

Podman supports Compose files through `podman compose` (a thin wrapper) or `podman-compose` (a Python reimplementation). The table below covers Compose file features.

| Feature | Docker Compose | podman compose | podman-compose |
|---------|---------------|----------------|----------------|
| `services` | Yes | Yes | Yes |
| `networks` | Yes | Partial (Netavark) | Partial |
| `volumes` (named) | Yes | Yes | Yes |
| `volumes` (bind mount) | Yes | Yes | Yes |
| `depends_on` | Yes | Yes | Yes (1.1+) |
| `depends_on` with conditions | Yes | Yes | Yes (1.1+) |
| `healthcheck` | Yes | Yes | Yes |
| `profiles` | Yes | Yes | Yes |
| `build` | Yes (BuildKit) | Yes (Buildah) | Yes (Buildah) |
| `env_file` | Yes | Yes | Yes |
| `secrets` (file-based) | Yes | Yes | Partial |
| `configs` | Yes | Partial | Limited |
| `deploy.resources` | Swarm/Compose | Limited | Limited |
| `deploy.replicas` | Swarm/Compose | Not supported | Not supported |
| `watch` | Yes | Not supported | Not supported |
| `include` | Yes | Yes | Not supported |
| `extends` | Yes | Yes | Yes |
| GPU passthrough | Yes (`deploy.resources`) | Via `--device` | Via `--device` |

### podman compose vs podman-compose

These are different tools:

| Aspect | `podman compose` | `podman-compose` |
|--------|------------------|------------------|
| Type | Wrapper script (calls docker-compose or podman-compose) | Standalone Python tool |
| Install | Included with Podman 4.7+ | `pip install podman-compose` |
| Backend | Delegates to external tool | Native Podman API |
| Feature set | Depends on backend | Subset of Docker Compose |
| Recommended | Yes (with docker-compose as backend) | For simple stacks |

### Using Docker Compose with Podman

You can use the original `docker-compose` binary with Podman by pointing it at the Podman socket:

```bash
# Start the Podman socket
systemctl --user enable --now podman.socket

# Set DOCKER_HOST
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/podman/podman.sock

# Use docker-compose normally
docker-compose up -d
docker-compose logs
docker-compose down
```

### Compose Networking Differences

Docker Compose creates a bridge network per project. Podman Compose does the same, but uses Netavark as the backend. Key differences:

- DNS resolution works the same way (services reachable by name)
- Network driver options differ (no `overlay` driver in rootless Podman)
- `network_mode: host` works in both
- `network_mode: service:other` works in podman-compose 1.1+

## Socket Emulation

### podman-docker Package

The `podman-docker` package provides full Docker CLI emulation:

```bash
# Install
sudo dnf install podman-docker    # Fedora/RHEL
sudo apt install podman-docker    # Debian/Ubuntu

# What it provides:
# 1. /usr/bin/docker symlink → podman
# 2. docker.socket systemd unit → podman.socket
# 3. /var/run/docker.sock emulation
```

### Socket Paths

| Mode | Socket Path | Activation |
|------|-------------|------------|
| Rootless | `$XDG_RUNTIME_DIR/podman/podman.sock` | `systemctl --user enable --now podman.socket` |
| Rootful | `/run/podman/podman.sock` | `sudo systemctl enable --now podman.socket` |
| Docker compat | `/var/run/docker.sock` | `sudo systemctl enable --now podman.socket` (with podman-docker) |

### DOCKER_HOST Configuration

Set `DOCKER_HOST` so Docker-compatible tools find the Podman socket:

```bash
# Rootless
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/podman/podman.sock

# Add to shell profile for persistence
echo 'export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/podman/podman.sock' >> ~/.bashrc

# Rootful (for system-wide tools)
export DOCKER_HOST=unix:///run/podman/podman.sock
```

### Tools That Require Socket Emulation

| Tool | Works with Podman Socket | Notes |
|------|--------------------------|-------|
| VS Code Dev Containers | Yes | Set `DOCKER_HOST` or configure in settings |
| Testcontainers | Yes | Set `DOCKER_HOST` and `TESTCONTAINERS_RYUK_DISABLED=true` |
| GitLab Runner | Yes | Configure `DOCKER_HOST` in runner config |
| GitHub Actions (self-hosted) | Yes | Set environment in runner service |
| Terraform Docker provider | Yes | Set `host` in provider config |
| Portainer | Partial | Some features require Docker API extensions |

### Systemd Socket Activation

The Podman socket activates on demand (no persistent daemon):

```bash
# Enable socket activation (rootless)
systemctl --user enable podman.socket
systemctl --user start podman.socket

# Verify the socket is listening
systemctl --user status podman.socket
curl --unix-socket $XDG_RUNTIME_DIR/podman/podman.sock http://localhost/_ping
# Response: OK
```

## Known Differences

### Networking

| Behavior | Docker | Podman |
|----------|--------|--------|
| Default network backend | Docker bridge (libnetwork) | Netavark |
| DNS resolution | Built-in DNS server | aardvark-dns |
| Privileged port binding | Works with root daemon | Requires sysctl or rootful mode |
| Host networking | `--network host` | `--network host` (same) |
| Custom bridge subnet | `--subnet` on `docker network create` | `--subnet` on `podman network create` |
| Inter-container ping | Works by default | Requires pasta (slirp4netns blocks ICMP) |
| IPv6 support | Full | Full (Netavark) |

**Impact:** Most networking works identically. The main friction point is privileged ports in rootless mode and ICMP behavior with slirp4netns.

### Volumes

| Behavior | Docker | Podman (rootless) |
|----------|--------|-------------------|
| Named volume location | `/var/lib/docker/volumes/` | `~/.local/share/containers/storage/volumes/` |
| Bind mount permissions | Matches host user | UID mapping may cause mismatches |
| SELinux labels | `:z` / `:Z` optional (daemon handles) | `:z` / `:Z` required on SELinux systems |
| `:U` flag (auto-chown) | Not supported | Supported (Podman-specific) |
| Volume drivers | Plugin ecosystem | Limited (local only in rootless) |

**Impact:** Volume permission issues are the most common migration problem. Use `--userns=keep-id`, `podman unshare chown`, or the `:U` flag.

### Build Behavior

| Behavior | Docker (BuildKit) | Podman (Buildah) |
|----------|-------------------|------------------|
| Build daemon | BuildKit (daemon-based) | Buildah (daemonless) |
| `#syntax=` parser directive | Supported | Not supported |
| `--secret` flag | Supported | Supported (Buildah 1.28+) |
| Build cache | Persistent daemon cache | Per-invocation (use `--layers`) |
| `--cache-from` / `--cache-to` | Registry cache support | Limited |
| Multi-platform build | `docker buildx build` | `podman build --platform` |
| Build output export | `--output type=local` | `--output type=local` (Buildah 1.29+) |

**Impact:** Build caching behavior differs. Docker's daemon retains cache across builds automatically. Podman's Buildah uses `--layers` for layer caching but does not persist a build cache daemon.

### Restart Policies

| Behavior | Docker | Podman |
|----------|--------|--------|
| `--restart always` | Daemon restarts container | No daemon; use systemd/Quadlet |
| `--restart unless-stopped` | Daemon restarts container | No daemon; use systemd/Quadlet |
| `--restart on-failure` | Daemon restarts container | Supported via conmon (limited) |

**Impact:** Podman has no daemon to restart containers. For reliable restart, use Quadlet (systemd integration) instead of `--restart` policies.

### Logging

| Behavior | Docker | Podman |
|----------|--------|--------|
| Default log driver | `json-file` | `journald` (on systemd systems) or `k8s-file` |
| `docker logs` | Reads from log driver | `podman logs` reads from configured driver |
| Log rotation | Configurable per-container | Managed by journald or file rotation |
| External log drivers (Fluentd, Splunk) | Plugin support | Limited |

**Impact:** If scripts parse Docker JSON logs, they may need adjustment for Podman's default journald logging. Set `--log-driver=json-file` for Docker-compatible behavior.

### Container Lifecycle

| Behavior | Docker | Podman |
|----------|--------|--------|
| Container process parent | dockerd | User's shell / systemd |
| Container survives daemon restart | Yes (live-restore) | N/A (no daemon) |
| Container survives user logout | Via daemon | Only with `loginctl enable-linger` |
| Container manager PID 1 | containerd-shim | conmon |

## Migration Checklist

Use this checklist when migrating a project from Docker to Podman.

### Pre-Migration Assessment

- [ ] Identify all Docker commands used in scripts, CI/CD, and documentation
- [ ] Check if any Docker Swarm features are used (not supported in Podman)
- [ ] Inventory all `docker-compose.yml` files and check for unsupported features
- [ ] List tools that connect to the Docker socket (CI runners, IDEs, test frameworks)
- [ ] Check if the target system has cgroup v2 (required for rootless resource limits)
- [ ] Verify kernel version supports unprivileged user namespaces (5.11+ recommended)

### System Setup

- [ ] Install Podman, Buildah, and Skopeo
- [ ] Install pasta (or slirp4netns) for rootless networking
- [ ] Install aardvark-dns and Netavark for container DNS
- [ ] Configure `/etc/subuid` and `/etc/subgid` for all container users
- [ ] Configure `/etc/containers/registries.conf` with `unqualified-search-registries`
- [ ] Install `podman-docker` if you need Docker CLI compatibility
- [ ] Enable Podman socket: `systemctl --user enable --now podman.socket`

### Script and CI Migration

- [ ] Replace `docker` with `podman` in scripts (or use alias/podman-docker)
- [ ] Replace `docker compose` with `podman compose` or set `DOCKER_HOST`
- [ ] Replace `docker buildx build` with `podman build --platform`
- [ ] Update CI/CD environment variables to set `DOCKER_HOST`
- [ ] Replace `--restart always` with Quadlet `.container` files for systemd
- [ ] Test all volume mounts for UID mapping issues (add `:Z`, `:U`, or `--userns=keep-id`)
- [ ] Update port mappings if any use privileged ports (< 1024)

### Validation

- [ ] Run the full test suite with Podman
- [ ] Verify compose services start and communicate correctly
- [ ] Check that volumes persist data across container restarts
- [ ] Validate image builds produce identical results
- [ ] Test container auto-start on boot (Quadlet + linger)
- [ ] Confirm monitoring and logging tools receive container metrics/logs
- [ ] Run `podman system info` and verify expected configuration

### Documentation Updates

- [ ] Update README and contributing guides to reference Podman
- [ ] Add Podman-specific troubleshooting to project documentation
- [ ] Document the `DOCKER_HOST` setting for team members using Docker-compatible tools
- [ ] Update Makefiles, Justfiles, or Taskfiles with Podman commands

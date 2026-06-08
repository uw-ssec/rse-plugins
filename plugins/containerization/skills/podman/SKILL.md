---
name: podman
description: Use when the user asks about Podman, rootless containers, Quadlet/systemd units, Podman Compose, or migrating Docker workflows to Podman. Creates and manages rootless Podman containers, maps Docker commands, configures podman run/build/compose flows, and sets up systemd-managed services.
metadata:
  references:
    - references/rootless-containers.md
    - references/docker-compatibility.md
    - references/operations-and-troubleshooting.md
  assets:
    - assets/podman-compose-example.yml
    - assets/quadlet-example.container
---

# Podman

## Primary Actions

- Run and manage rootless Podman containers.
- Translate Docker workflows to Podman equivalents.
- Configure Podman Compose for multi-service stacks.
- Create systemd-managed services using Quadlet.
- Troubleshoot rootless, socket, and service lifecycle issues.

## Quick Command Map (Differences from Docker)

```bash
# Docker socket compatibility
systemctl --user enable --now podman.socket
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/podman/podman.sock

# Pod operations (Podman-specific)
podman pod create --name app-pod

# Quadlet service management
systemctl --user daemon-reload
systemctl --user enable --now my-service
```

## Rootless Container Example

```bash
# Run a container without root — this is the Podman default
podman run --rm -it alpine sh

# Verify rootless mode
podman info --format '{{ .Host.Security.Rootless }}'   # should print: true

# Verify user namespace mapping (uid 0 in container = your UID on host)
podman unshare cat /proc/self/uid_map
```

## Quadlet Unit Example

Place `.container` files in `~/.config/containers/systemd/` (user) or `/etc/containers/systemd/` (system):

```ini
# ~/.config/containers/systemd/myapp.container
[Unit]
Description=My App Container

[Container]
Image=docker.io/library/nginx:alpine
PublishPort=8080:80
Volume=%h/data:/usr/share/nginx/html:Z

[Service]
Restart=always

[Install]
WantedBy=default.target
```

```bash
# Load and start
systemctl --user daemon-reload
systemctl --user enable --now myapp

# Validate
systemctl --user status myapp
journalctl --user -u myapp -n 50
```

See [assets/quadlet-example.container](assets/quadlet-example.container) for a more complete example.

## Translate Docker → Podman

| Docker | Podman | Notes |
|--------|--------|-------|
| `docker run` | `podman run` | Identical flags; rootless by default |
| `docker build` | `podman build` | Identical Dockerfile syntax |
| `docker ps` | `podman ps` | Same output |
| `docker compose up` | `podman-compose up` | Or use Docker Compose CLI via socket |
| `docker system prune` | `podman system prune` | Same |
| Daemon required | No daemon | Podman is daemonless |

## Validation Workflow

1. **Verify rootless mode:**
   ```bash
   podman info --format '{{ .Host.Security.Rootless }}'   # → true
   podman unshare cat /proc/self/uid_map                   # → uid mapping present
   ```

2. **Run a basic rootless container:**
   ```bash
   podman run --rm hello-world
   ```

3. **For Compose, validate config before up:**
   ```bash
   podman-compose config
   podman-compose up --dry-run   # if supported by your version
   ```

4. **For Quadlet, verify systemd unit status and logs:**
   ```bash
   systemctl --user status myapp
   journalctl --user -u myapp --since "5 minutes ago"
   ```

5. If failures occur, fix and re-run the relevant check.

## Deep References

- Rootless architecture, networking, volume permissions:
  [references/rootless-containers.md](references/rootless-containers.md)
- Docker compatibility details and known differences:
  [references/docker-compatibility.md](references/docker-compatibility.md)
- Validation and troubleshooting playbook:
  [references/operations-and-troubleshooting.md](references/operations-and-troubleshooting.md)

# Podman Operations and Troubleshooting

## Validation Workflow

1. Verify rootless mode and namespace mappings:

```bash
podman info --format '{{.Host.Security.Rootless}}'
podman unshare cat /proc/self/uid_map
```

2. Verify basic container lifecycle:

```bash
podman run --rm docker.io/library/alpine echo ok
podman ps -a
```

3. If using compose:

```bash
podman compose config
podman compose up -d
podman compose ps
```

4. If using Quadlet:

```bash
systemctl --user daemon-reload
systemctl --user start my-service
systemctl --user status my-service
```

5. If failures occur, fix config and re-run from step 1.

## Common Failure Patterns

1. Missing `/etc/subuid` or `/etc/subgid` entries for rootless users.
2. Tool expecting Docker socket (`/var/run/docker.sock`) without Podman socket export.
3. User service stops at logout because linger is not enabled.
4. Compose feature mismatch when using incompatible compose implementation.

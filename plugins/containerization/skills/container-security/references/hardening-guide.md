# Container Hardening — Deep Reference

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| Non-Root User Configuration | 15–72 | USER directive, numeric UIDs, file permissions, and debugging |
| Minimal Base Images | 73–133 | Distroless, scratch, Chainguard, and Alpine comparisons |
| Read-Only Root Filesystem | 134–181 | Enabling --read-only, tmpfs mounts, and Kubernetes configuration |
| Capability Management | 182–237 | Dropping capabilities, adding specific ones, and auditing |
| Seccomp and AppArmor Profiles | 238–301 | Default profiles, custom seccomp policies, and AppArmor basics |
| Secrets Management | 302–369 | Build secrets with --mount=type=secret, runtime secrets, and anti-patterns |
| Network Security | 370–414 | Minimizing exposed ports, internal networks, and network policies |
| CIS Docker Benchmark Highlights | 415–470 | Key recommendations from the CIS Docker Benchmark |

---

## Non-Root User Configuration

Running containers as root is one of the most common and dangerous misconfigurations. If an attacker escapes the application, they have root access to the container filesystem and potentially the host.

### USER Directive in Dockerfile

```dockerfile
# Create a dedicated user with no login shell
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --shell /usr/sbin/nologin --create-home appuser

# Set ownership of application files
COPY --chown=appuser:appgroup . /app

# Switch to non-root user
USER appuser

# Or use numeric UID (preferred for Kubernetes compatibility)
USER 1001
```

### Why Numeric UIDs

Kubernetes and some container runtimes resolve usernames at container startup. Using numeric UIDs avoids dependency on `/etc/passwd` being present (important for distroless and scratch images).

```dockerfile
# Preferred: numeric UID
USER 1001

# Also works but requires /etc/passwd
USER appuser
```

### File Permission Patterns

```dockerfile
# Ensure the app user can read application files
COPY --chown=1001:1001 . /app

# Make scripts executable
RUN chmod +x /app/entrypoint.sh

# Ensure writable directories exist with correct ownership
RUN mkdir -p /app/data /app/tmp && chown -R 1001:1001 /app/data /app/tmp
```

### Multi-Stage Build with Non-Root

```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --shell /usr/sbin/nologin --create-home appuser
COPY --from=builder /install /usr/local
COPY --chown=1001:1001 . /app
WORKDIR /app
USER 1001
CMD ["python", "main.py"]
```

### Debugging Non-Root Issues

```bash
# Check which user the container runs as
docker run --rm myapp:latest whoami
docker run --rm myapp:latest id

# Test with a specific user override
docker run --rm --user 1001:1001 myapp:latest ls -la /app

# Temporarily run as root for debugging (never in production)
docker run --rm --user root myapp:latest sh
```

## Minimal Base Images

The fewer packages in your base image, the smaller your attack surface. Every installed package is a potential source of vulnerabilities.

### Comparison of Base Image Options

| Base Image | Size | Shell | Package Manager | Use Case |
|------------|------|-------|-----------------|----------|
| `ubuntu:24.04` | ~77 MB | Yes | apt | Development, full tooling needed |
| `python:3.12-slim` | ~52 MB | Yes | apt + pip | Python apps needing some OS tools |
| `alpine:3.19` | ~7 MB | Yes | apk | Small images, musl-based |
| `gcr.io/distroless/python3` | ~52 MB | No | None | Production Python apps |
| `cgr.dev/chainguard/python` | ~30 MB | No | None | Production, verified provenance |
| `scratch` | 0 MB | No | None | Statically compiled binaries |

### Distroless Images

Distroless images from Google contain only the application runtime and its dependencies. No shell, no package manager, no utilities.

```dockerfile
# Multi-stage: build in full image, run in distroless
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/app/deps -r requirements.txt

FROM gcr.io/distroless/python3-debian12
COPY --from=builder /app/deps /app/deps
COPY . /app
WORKDIR /app
ENV PYTHONPATH=/app/deps
CMD ["main.py"]
```

### Scratch Images

For statically compiled binaries (Go, Rust), use `scratch` for the absolute minimum:

```dockerfile
FROM golang:1.22 AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 go build -o /app/server .

FROM scratch
COPY --from=builder /app/server /server
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 1001
ENTRYPOINT ["/server"]
```

### Chainguard Images

Chainguard images are minimal, hardened, and come with verified provenance and SBOMs:

```dockerfile
FROM cgr.dev/chainguard/python:latest
COPY --chown=nonroot:nonroot . /app
WORKDIR /app
CMD ["main.py"]
```

Chainguard images run as non-root by default and have zero or near-zero known CVEs at time of publication.

## Read-Only Root Filesystem

A read-only root filesystem prevents attackers from modifying binaries, writing malicious scripts, or tampering with configuration files inside the container.

### Docker Run

```bash
# Enable read-only root filesystem
docker run --read-only myapp:latest

# Add tmpfs for directories that need to be writable
docker run --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=64m \
  --tmpfs /var/run:rw,noexec,nosuid,size=1m \
  myapp:latest
```

### Docker Compose

```yaml
services:
  app:
    image: myapp:latest
    read_only: true
    tmpfs:
      - /tmp:size=64m
      - /var/run:size=1m
    volumes:
      - app-data:/app/data  # Named volume for persistent writable data
```

### Kubernetes

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
    - name: app
      image: myapp:latest
      securityContext:
        readOnlyRootFilesystem: true
      volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: data
          mountPath: /app/data
  volumes:
    - name: tmp
      emptyDir:
        medium: Memory
        sizeLimit: 64Mi
    - name: data
      persistentVolumeClaim:
        claimName: app-data
```

### Common Writable Paths

Applications may need writable access to:
- `/tmp` — Temporary files
- `/var/run` — PID files, sockets
- `/var/log` — Log files (prefer stdout/stderr instead)
- `/app/data` — Application-specific data directory
- `/home/appuser/.cache` — Cache directories

Mount each as tmpfs or a volume rather than making the entire filesystem writable.

## Capability Management

Linux capabilities break the monolithic root privilege into fine-grained permissions. By default, Docker grants a subset of capabilities. For hardened containers, drop all and add back only what is needed.

### Default Docker Capabilities

Docker grants these capabilities by default: `CHOWN`, `DAC_OVERRIDE`, `FSETID`, `FOWNER`, `MKNOD`, `NET_RAW`, `SETGID`, `SETUID`, `SETFCAP`, `SETPCAP`, `NET_BIND_SERVICE`, `SYS_CHROOT`, `KILL`, `AUDIT_WRITE`.

Most applications need very few of these.

### Drop All, Add Specific

```bash
# Drop all capabilities
docker run --cap-drop ALL myapp:latest

# Drop all, add back specific ones
docker run --cap-drop ALL --cap-add NET_BIND_SERVICE myapp:latest

# Common capabilities to add back
docker run --cap-drop ALL \
  --cap-add NET_BIND_SERVICE \  # Bind to ports below 1024
  --cap-add CHOWN \             # Change file ownership
  --cap-add SETUID \            # Set UID (for init systems)
  --cap-add SETGID \            # Set GID (for init systems)
  myapp:latest
```

### Docker Compose

```yaml
services:
  app:
    image: myapp:latest
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
```

### Kubernetes

```yaml
securityContext:
  capabilities:
    drop:
      - ALL
    add:
      - NET_BIND_SERVICE
```

### Auditing Required Capabilities

To determine which capabilities your application actually needs:

```bash
# Run with all capabilities dropped and observe failures
docker run --cap-drop ALL myapp:latest

# Use capsh to check current capabilities inside a container
docker run --rm myapp:latest capsh --print

# Use pscap or getpcaps on the host to inspect running container
# (requires audit tools installed)
pscap | grep <container-pid>
```

### Common Capability Requirements

| Capability | When Needed |
|-----------|-------------|
| `NET_BIND_SERVICE` | Binding to ports below 1024 |
| `CHOWN` | Changing file ownership at runtime |
| `SETUID` / `SETGID` | Running process managers, init systems |
| `SYS_PTRACE` | Debugging, profiling (never in production) |
| `NET_RAW` | Ping, raw network sockets |
| `DAC_OVERRIDE` | Bypassing file permission checks |

## Seccomp and AppArmor Profiles

### Seccomp Profiles

Seccomp (Secure Computing Mode) filters system calls available to a container. Docker applies a default seccomp profile that blocks approximately 44 dangerous syscalls.

**Default profile:** Blocks `mount`, `reboot`, `swapon`, `clock_settime`, `kexec_load`, and other system administration calls.

```bash
# Run with default seccomp profile (automatic in Docker)
docker run myapp:latest

# Run with no seccomp profile (less secure, for debugging)
docker run --security-opt seccomp=unconfined myapp:latest

# Run with a custom seccomp profile
docker run --security-opt seccomp=custom-profile.json myapp:latest
```

**Custom seccomp profile example:**

```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": ["SCMP_ARCH_X86_64"],
  "syscalls": [
    {
      "names": [
        "read", "write", "open", "close", "stat", "fstat",
        "mmap", "mprotect", "munmap", "brk", "ioctl",
        "access", "pipe", "select", "sched_yield",
        "socket", "connect", "accept", "sendto", "recvfrom",
        "bind", "listen", "getsockname", "getpeername",
        "clone", "execve", "exit", "exit_group",
        "futex", "epoll_create", "epoll_ctl", "epoll_wait"
      ],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

### Generating a Custom Profile

Use tools to trace which syscalls your application actually uses:

```bash
# Use strace to identify required syscalls
docker run --rm --security-opt seccomp=unconfined \
  strace -c -f myapp:latest 2>&1 | tail -20

# Use OCI seccomp bpf hook to generate profiles automatically
# See: https://github.com/containers/oci-seccomp-bpf-hook
```

### AppArmor Profiles

AppArmor provides Mandatory Access Control (MAC) by restricting what files, capabilities, and network access a container can use.

```bash
# Run with default Docker AppArmor profile
docker run myapp:latest

# Run with a custom AppArmor profile
docker run --security-opt apparmor=my-custom-profile myapp:latest

# Disable AppArmor (less secure, for debugging)
docker run --security-opt apparmor=unconfined myapp:latest
```

**Custom AppArmor profile example:**
```
#include <tunables/global>
profile my-container-profile flags=(attach_disconnected) {
  #include <abstractions/base>
  network inet tcp,
  network inet udp,
  deny /etc/shadow r,
  deny /proc/*/mem rw,
  /app/** r,
  /app/data/** rw,
  /tmp/** rw,
}
```

## Secrets Management

Never bake secrets into container images. Image layers are stored permanently and can be extracted by anyone with access to the image.

### Anti-Patterns (Never Do This)

```dockerfile
# WRONG: Secret in ENV (visible in image metadata)
ENV DATABASE_PASSWORD=supersecret

# WRONG: Secret COPYed into image (persisted in layer)
COPY credentials.json /app/credentials.json

# WRONG: Secret in ARG (visible in build history)
ARG API_KEY=mysecretkey
RUN curl -H "Authorization: Bearer $API_KEY" https://example.com
```

### Build Secrets (Docker BuildKit)

Use `--mount=type=secret` to access secrets during build without persisting them in layers:

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Secret is available during this RUN but NOT stored in the layer
RUN --mount=type=secret,id=pip_index_url \
    PIP_INDEX_URL=$(cat /run/secrets/pip_index_url) \
    pip install --no-cache-dir -r requirements.txt

# For .netrc authentication
RUN --mount=type=secret,id=netrc,target=/root/.netrc \
    pip install --no-cache-dir -r requirements.txt
```

**Building with secrets:**
```bash
# Pass secret from environment variable
echo "$PIP_INDEX_URL" | docker build --secret id=pip_index_url -t myapp .

# Pass secret from file
docker build --secret id=pip_index_url,src=.secrets/pip-index-url.txt -t myapp .

# Pass .netrc file
docker build --secret id=netrc,src=$HOME/.netrc -t myapp .
```

### Runtime Secrets

Pass secrets at runtime rather than baking them into images:

```bash
# Environment variables (simple, visible in process table)
docker run -e DATABASE_URL="postgresql://user:pass@host/db" myapp:latest

# Docker secrets (Swarm mode)
echo "supersecret" | docker secret create db_password -
docker service create --secret db_password myapp:latest

# Mounted files (most secure for Docker)
docker run -v /path/to/secrets:/run/secrets:ro myapp:latest
```

### Kubernetes Secrets

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  database-url: "postgresql://user:pass@host/db"
---
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: app
      image: myapp:latest
      volumeMounts:
        - name: secrets
          mountPath: /run/secrets
          readOnly: true
  volumes:
    - name: secrets
      secret:
        secretName: app-secrets
```

### Verifying No Secrets in Images

```bash
# Check image history for secret leaks
docker history myapp:latest

# Scan for secrets with Trivy
trivy image --scanners secret myapp:latest

# Extract and inspect layers
docker save myapp:latest | tar -xf - -C /tmp/image-layers
# Inspect each layer for secrets
```

## Network Security

### Minimize Exposed Ports

Only expose ports that your application actually needs:

```dockerfile
# Only expose the application port
EXPOSE 8080

# Do NOT expose debug, management, or database ports
# EXPOSE 5432  # No — database should not be in the app container
# EXPOSE 9090  # No — debug/metrics should use internal networks
```

### Docker Networks

```bash
# Create an internal network (no external access)
docker network create --internal backend-net

# Attach containers to the internal network
docker run --network backend-net --name db postgres:16
docker run --network backend-net --name app myapp:latest

# Only the reverse proxy gets external access
docker network create frontend-net
docker run --network frontend-net --network backend-net --name proxy nginx
```

### Docker Compose Network Isolation

```yaml
services:
  app:
    image: myapp:latest
    networks:
      - backend
  db:
    image: postgres:16
    networks:
      - backend
  proxy:
    image: nginx:latest
    ports:
      - "443:443"
    networks:
      - frontend
      - backend

networks:
  frontend:
  backend:
    internal: true  # No external access
```

### Kubernetes Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: app-network-policy
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: proxy
      ports:
        - port: 8080
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: database
      ports:
        - port: 5432
```

## CIS Docker Benchmark Highlights

The CIS Docker Benchmark provides comprehensive security recommendations. These are the most impactful items for container image security.

### Host Configuration (Selected)

- **2.1**: Restrict network traffic between containers (use `--icc=false` or network policies)
- **2.5**: Use a centralized logging driver (do not rely on container-local logs)
- **2.8**: Enable user namespace support for additional isolation

### Docker Daemon Configuration (Selected)

- **3.1**: Verify Docker daemon audit logging is enabled
- **3.7**: Restrict TLS access to the Docker daemon socket

### Container Images (Selected)

- **4.1**: Create a non-root user in Dockerfiles
- **4.2**: Use trusted and verified base images
- **4.3**: Do not install unnecessary packages
- **4.4**: Scan images for vulnerabilities before deployment
- **4.6**: Add HEALTHCHECK instructions to Dockerfiles
- **4.9**: Use COPY instead of ADD in Dockerfiles
- **4.10**: Do not store secrets in Dockerfiles

### Container Runtime (Selected)

- **5.2**: Verify AppArmor profile is enabled
- **5.3**: Verify SELinux or seccomp profile is enabled
- **5.4**: Do not run containers as root
- **5.12**: Mount container root filesystem as read-only
- **5.15**: Do not share the host network namespace
- **5.25**: Restrict container from acquiring additional privileges (`--security-opt=no-new-privileges`)

### Quick Compliance Check

```bash
# Use Docker Bench for Security to audit your host and containers
docker run --rm --net host --pid host --userns host --cap-add audit_control \
  -e DOCKER_CONTENT_TRUST=$DOCKER_CONTENT_TRUST \
  -v /var/lib:/var/lib:ro \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /etc:/etc:ro \
  docker/docker-bench-security

# Check a specific container's security posture
docker inspect --format '{{.Config.User}}' myapp:latest          # Should not be empty or root
docker inspect --format '{{.HostConfig.ReadonlyRootfs}}' <id>     # Should be true
docker inspect --format '{{.HostConfig.CapDrop}}' <id>            # Should include ALL
```

### Recommended SecurityContext (Kubernetes)

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1001
  runAsGroup: 1001
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop:
      - ALL
  seccompProfile:
    type: RuntimeDefault
```

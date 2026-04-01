# Networking & Volumes — Deep Reference

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| Network Drivers | 17–78 | Bridge, host, overlay, and macvlan driver characteristics and usage |
| DNS Resolution Between Services | 79–155 | How services discover each other by name, aliases, and custom DNS |
| Port Mapping and Exposure | 156–228 | Publishing ports to the host, expose vs ports, protocol options |
| Volume Types | 229–301 | Named, anonymous, bind, and tmpfs volume characteristics |
| NFS and Remote Volumes | 302–372 | Mounting NFS shares and remote storage as Docker volumes |
| Volume Permissions and Ownership | 373–446 | Solving UID/GID mismatches between host and container |
| Data Persistence Strategies | 447–513 | Backup, migration, and lifecycle patterns for persistent data |

---

## Network Drivers

Docker provides several network drivers. In Compose, the default is `bridge`.

### bridge (default)

Isolated network on a single host. Services communicate by container name.

```yaml
networks:
  app-net:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16     # Optional: custom subnet
```

**When to use:** Most single-host applications. This is the right choice for development and most research workloads.

### host

The container shares the host's network stack directly. No port mapping is needed (or possible).

```yaml
services:
  api:
    network_mode: host
```

**When to use:** Performance-sensitive applications where network overhead matters, or when the container needs access to host network interfaces. Not available on macOS or Windows Docker Desktop.

### overlay

Multi-host networking for Docker Swarm clusters.

```yaml
networks:
  swarm-net:
    driver: overlay
    attachable: true                 # Allow standalone containers to attach
```

**When to use:** Distributed applications across multiple Docker hosts. Requires Swarm mode.

### macvlan

Assigns a MAC address to the container, making it appear as a physical device on the network.

```yaml
networks:
  physical-net:
    driver: macvlan
    driver_opts:
      parent: eth0                   # Host interface
    ipam:
      config:
        - subnet: 192.168.1.0/24
          gateway: 192.168.1.1
```

**When to use:** When the container needs to appear as a separate host on the physical network (e.g., legacy protocols, DHCP).

## DNS Resolution Between Services

### Automatic DNS

Compose creates a default network and registers each service name as a DNS entry:

```yaml
services:
  api:
    image: myapp:latest
  db:
    image: postgres:16-alpine
```

From inside the `api` container:

```bash
# These all resolve to the db container's IP
ping db
curl http://db:5432
psql -h db -U user
```

### Network Aliases

Give a service additional DNS names:

```yaml
services:
  db:
    image: postgres:16-alpine
    networks:
      backend:
        aliases:
          - database
          - postgres
          - pghost
```

Now `db`, `database`, `postgres`, and `pghost` all resolve to the same container within the `backend` network.

### Multiple Networks and DNS Scope

A service is only resolvable by name from containers on the same network:

```yaml
services:
  api:
    networks:
      - frontend
      - backend           # Can reach db

  web:
    networks:
      - frontend           # Cannot reach db

  db:
    networks:
      - backend            # Not on frontend

networks:
  frontend:
  backend:
```

### Custom DNS Servers

```yaml
services:
  api:
    dns:
      - 8.8.8.8
      - 8.8.4.4
    dns_search:
      - example.com
```

## Port Mapping and Exposure

### ports — Publish to Host

```yaml
services:
  api:
    ports:
      # Short syntax: HOST:CONTAINER
      - "8000:8000"
      - "8443:443"

      # Bind to specific interface
      - "127.0.0.1:8000:8000"        # Localhost only
      - "0.0.0.0:8000:8000"          # All interfaces (default)

      # Dynamic host port (Docker picks an available port)
      - "8000"                        # Maps to random host port

      # UDP protocol
      - "5000:5000/udp"

      # Long syntax (more explicit)
      - target: 8000                  # Container port
        published: "8000"             # Host port
        protocol: tcp
        host_ip: 127.0.0.1
```

### expose — Container-Only

`expose` documents which ports a service uses but does not publish them to the host. Other services on the same network can still reach them.

```yaml
services:
  db:
    expose:
      - "5432"                       # Accessible to other services, not the host
```

### Port Conflicts

Avoid hardcoded ports by using variables:

```yaml
services:
  api:
    ports:
      - "${API_PORT:-8000}:8000"
  db:
    ports:
      - "${DB_PORT:-5432}:5432"
```

### When Not to Publish Ports

Internal services that only other containers need to reach should not have `ports` entries. This improves security:

```yaml
services:
  api:
    ports:
      - "8000:8000"                  # Public-facing
  db:
    # No ports — only reachable from within the Docker network
    expose:
      - "5432"
  redis:
    # No ports — internal cache only
    expose:
      - "6379"
```

## Volume Types

### Named Volumes

Managed by Docker. Data persists until the volume is explicitly removed.

```yaml
services:
  db:
    volumes:
      - pg-data:/var/lib/postgresql/data

volumes:
  pg-data:
    driver: local
    labels:
      com.example.description: "PostgreSQL data"
```

```bash
# Inspect
docker volume inspect project_pg-data

# List
docker volume ls

# Remove (data is lost!)
docker volume rm project_pg-data
```

### Anonymous Volumes

Created without a name. Harder to manage and reuse. Avoid in most cases.

```yaml
services:
  api:
    volumes:
      - /app/node_modules            # Anonymous volume
```

### Bind Mounts

Map a host directory directly into the container:

```yaml
services:
  api:
    volumes:
      - ./src:/app/src               # Relative to compose file
      - /data/datasets:/app/data:ro  # Absolute path, read-only
      - ./config:/app/config:cached  # macOS performance hint
```

**Consistency flags (macOS/Windows):**
- `consistent` — full consistency (default, slowest)
- `cached` — host writes are immediately visible; container writes may be delayed
- `delegated` — container writes are immediately visible; host writes may be delayed

### tmpfs Volumes

In-memory filesystem. Data is lost when the container stops.

```yaml
services:
  worker:
    tmpfs:
      - /tmp:size=512m,mode=1777
      - /run
```

**When to use:** Scratch space, temporary files, sensitive data that should not persist to disk.

## NFS and Remote Volumes

### NFS Volume

Mount an NFS share as a Docker volume:

```yaml
volumes:
  shared-data:
    driver: local
    driver_opts:
      type: nfs
      o: "addr=192.168.1.100,nfsvers=4,rw,soft,timeo=30"
      device: ":/exports/research-data"
```

```yaml
services:
  api:
    volumes:
      - shared-data:/app/data
```

### CIFS/SMB Volume

Mount a Windows share:

```yaml
volumes:
  smb-data:
    driver: local
    driver_opts:
      type: cifs
      o: "username=${SMB_USER},password=${SMB_PASS},uid=1000,gid=1000"
      device: "//fileserver/research"
```

### SSHFS Volume (with plugin)

```bash
# Install the plugin
docker plugin install vieux/sshfs

# Use in compose
```

```yaml
volumes:
  remote-data:
    driver: vieux/sshfs
    driver_opts:
      sshcmd: "user@remote-host:/data"
      password: "${SSH_PASS}"
```

### External Volumes

Reference a volume created outside of Compose:

```yaml
volumes:
  shared-data:
    external: true
    name: research-shared-data       # Actual volume name
```

```bash
# Create the volume first
docker volume create research-shared-data
```

## Volume Permissions and Ownership

### The UID/GID Problem

Files created inside a container use the container user's UID/GID. On bind mounts, these map directly to the host, which can cause permission issues.

```bash
# Container runs as root (UID 0) — files on host are owned by root
# Container runs as UID 1000 — files on host are owned by UID 1000
```

### Solutions

**1. Match UIDs between host and container:**

```dockerfile
# Dockerfile
ARG UID=1000
ARG GID=1000
RUN groupadd -g ${GID} appuser && \
    useradd -u ${UID} -g ${GID} -m appuser
USER appuser
```

```yaml
services:
  api:
    build:
      args:
        UID: "${UID:-1000}"
        GID: "${GID:-1000}"
```

**2. Use the `user` directive:**

```yaml
services:
  api:
    user: "${UID:-1000}:${GID:-1000}"
```

**3. Use named volumes (avoids host permission issues):**

```yaml
volumes:
  app-data:                          # Docker manages permissions internally
```

**4. Fix permissions with an init script:**

```yaml
services:
  api:
    entrypoint: ["/bin/sh", "-c"]
    command: ["chown -R 1000:1000 /app/data && exec su-exec appuser python app.py"]
```

### Jupyter-Specific Permissions

The official Jupyter images run as user `jovyan` (UID 1000). When bind-mounting:

```yaml
services:
  jupyter:
    image: quay.io/jupyter/scipy-notebook:latest
    user: root                       # Start as root for permission fixes
    environment:
      NB_UID: "${UID:-1000}"
      NB_GID: "${GID:-100}"
      CHOWN_HOME: "yes"
    volumes:
      - ./notebooks:/home/jovyan/work
```

## Data Persistence Strategies

### Backup Named Volumes

```bash
# Backup a volume to a tar archive
docker run --rm \
  -v project_pg-data:/source:ro \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/pg-data-$(date +%Y%m%d).tar.gz -C /source .

# Restore from backup
docker run --rm \
  -v project_pg-data:/target \
  -v $(pwd)/backups:/backup \
  alpine tar xzf /backup/pg-data-20240101.tar.gz -C /target
```

### Database Dump and Restore

```bash
# PostgreSQL dump (while container is running)
docker compose exec db pg_dump -U ${POSTGRES_USER} ${POSTGRES_DB} > backup.sql

# Restore
docker compose exec -T db psql -U ${POSTGRES_USER} ${POSTGRES_DB} < backup.sql
```

### Volume Lifecycle in Compose

```bash
# Start services (creates volumes if they don't exist)
docker compose up -d

# Stop services (volumes are preserved)
docker compose down

# Stop services AND remove volumes (data is lost!)
docker compose down -v

# Remove only unused volumes
docker volume prune
```

### Migration Between Environments

```bash
# Export a volume
docker run --rm -v project_pg-data:/data -v $(pwd):/export \
  alpine tar czf /export/pg-data.tar.gz -C /data .

# Copy to another machine
scp pg-data.tar.gz user@remote-host:~/

# Import on the new host
docker volume create project_pg-data
docker run --rm -v project_pg-data:/data -v $(pwd):/import \
  alpine tar xzf /import/pg-data.tar.gz -C /data
```

### Preventing Accidental Data Loss

1. **Never use `docker compose down -v` in production** — it removes all named volumes
2. **Label important volumes** — makes them easier to identify during cleanup
3. **Use `external: true`** — prevents Compose from removing volumes it did not create
4. **Automate backups** — schedule regular dumps or volume snapshots
5. **Test restore procedures** — a backup you have never restored is not a backup

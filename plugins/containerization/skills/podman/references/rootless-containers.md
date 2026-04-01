# Rootless Containers -- Deep Reference

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| User Namespace Mapping | 17-73 | How user namespaces map UIDs/GIDs, the pause process, and ID range allocation |
| subuid/subgid Configuration | 75-132 | Configuring subordinate UID/GID ranges, common pitfalls, and multi-user setups |
| Storage Configuration | 134-205 | Storage drivers for rootless (overlay, fuse-overlayfs, vfs), storage.conf settings |
| Networking in Rootless Mode | 207-288 | slirp4netns, pasta, port forwarding limitations, DNS, and performance tuning |
| Volume Permissions and Ownership | 290-351 | UID mapping in bind mounts, :Z/:z SELinux labels, --userns=keep-id |
| Cgroup v2 Requirements | 353-421 | Checking cgroup version, enabling cgroup v2, resource limit support |
| Troubleshooting Common Issues | 423-518 | Error messages, diagnostics, and solutions for frequent rootless problems |

---

## User Namespace Mapping

### How User Namespaces Work

Rootless containers rely on Linux user namespaces to map the container's UID 0 (root) to an unprivileged UID on the host. Inside the container, processes appear to run as root and have full capabilities. Outside the container, those same processes run as a normal user with no elevated privileges.

```
Host UID        Container UID     Meaning
────────        ─────────────     ───────
1000            0                 Your user becomes container root
100000          1                 First subordinate UID
100001          2                 Second subordinate UID
...             ...               ...
165535          65536             Last subordinate UID
```

### The Pause Process

Podman uses an "infra" or "pause" process to hold the user namespace alive between container invocations. This process is named `catatonit` or `podman pause` and runs in the background.

```bash
# Check for the pause process
ps aux | grep -E 'catatonit|conmon'

# If the pause process is not running, Podman creates one automatically
# You can clean up stale pause processes with:
podman system migrate
```

### ID Range Allocation

Each rootless user needs a dedicated range of subordinate UIDs and GIDs. The default allocation is 65536 IDs starting from a base (commonly 100000). This range must not overlap with other users.

```bash
# View your allocated range
podman unshare cat /proc/self/uid_map

# Output: 0 1000 1          (your UID maps to container root)
#         1 100000 65536     (subordinate range for container UIDs 1-65536)

# View the host-side mapping
podman info --format '{{.Host.IDMappings.UIDMap}}'
```

### Multi-Container UID Consistency

All rootless containers for the same user share the same UID mapping. This means:
- A file created as UID 1000 inside container A is also UID 1000 inside container B
- Volume data is consistent across containers for the same user
- Different host users have different mappings, so shared volumes between users require care

```bash
# Verify consistent mapping across containers
podman run --rm alpine id           # uid=0(root) gid=0(root)
podman run --rm alpine touch /tmp/test && ls -ln /tmp/test
# Host sees the file owned by your UID (e.g., 1000)
```

## subuid/subgid Configuration

### File Format

The `/etc/subuid` and `/etc/subgid` files define subordinate UID and GID ranges for each user. Each line has the format:

```
username:start_id:count
```

Example entries:

```
researcher:100000:65536
labuser:200000:65536
```

This gives `researcher` UIDs 100000-165535 and `labuser` UIDs 200000-265535.

### Checking Configuration

```bash
# Check if your user has subuid/subgid entries
grep $USER /etc/subuid
grep $USER /etc/subgid

# Both files must have entries. If either is missing, rootless will fail.
```

### Adding Entries

```bash
# Method 1: usermod (preferred)
sudo usermod --add-subuids 100000-165535 --add-subgids 100000-165535 $USER

# Method 2: Direct edit (if usermod is unavailable)
echo "$USER:100000:65536" | sudo tee -a /etc/subuid
echo "$USER:100000:65536" | sudo tee -a /etc/subgid

# After adding entries, migrate Podman's state
podman system migrate
```

### Common Pitfalls

1. **Overlapping ranges** -- If two users share the same subordinate range, containers from one user can access files created by the other. Always use non-overlapping ranges.

2. **Insufficient range size** -- Some containers run multiple users internally (e.g., PostgreSQL creates a `postgres` user). A range of 65536 is the standard minimum. Do not reduce it.

3. **Missing entries after user creation** -- Some distributions do not automatically create subuid/subgid entries for new users. Check after `useradd`.

4. **NFS or LDAP home directories** -- If `/etc/subuid` is not on local storage, or if the user comes from LDAP/SSSD, you may need to configure subuid/subgid through your directory service or create local entries.

```bash
# Verify the range is sufficient
awk -F: -v user="$USER" '$1 == user {print "Range size:", $3}' /etc/subuid
# Should print: Range size: 65536
```

## Storage Configuration

### Storage Drivers

Rootless Podman supports several storage drivers. The driver affects performance, compatibility, and disk usage.

| Driver | Kernel Requirement | Performance | Notes |
|--------|-------------------|-------------|-------|
| `overlay` (native) | Kernel 5.11+ with unprivileged overlay | Best | Preferred on modern kernels |
| `fuse-overlayfs` | FUSE support | Good | Fallback for older kernels |
| `vfs` | None | Poor | Copy-on-write disabled; large disk usage |

### Checking Your Storage Driver

```bash
podman info --format '{{.Store.GraphDriverName}}'
# Desired output: overlay

# If you see "vfs", your kernel may not support unprivileged overlay
# Install fuse-overlayfs as a fallback:
# Fedora/RHEL: sudo dnf install fuse-overlayfs
# Ubuntu/Debian: sudo apt install fuse-overlayfs
```

### storage.conf

The storage configuration file controls where images, containers, and volumes are stored.

```bash
# User-level config (rootless)
~/.config/containers/storage.conf

# System-level config (rootful)
/etc/containers/storage.conf
```

Key settings:

```toml
[storage]
# Where images and containers are stored (rootless default)
graphroot = "/home/username/.local/share/containers/storage"

# Temporary storage for running containers
runroot = "/run/user/1000/containers"

[storage.options]
# Storage driver
driver = "overlay"

[storage.options.overlay]
# Mount options for overlay
mount_program = "/usr/bin/fuse-overlayfs"   # Only if using fuse-overlayfs
```

### Disk Usage Management

Rootless storage lives in your home directory. Monitor and clean up regularly:

```bash
# Check disk usage
podman system df

# Detailed breakdown
podman system df -v

# Clean up unused images, containers, and volumes
podman system prune --all --volumes

# Remove all build cache
podman builder prune --all
```

## Networking in Rootless Mode

### Network Backends

Rootless containers cannot directly create network interfaces or bind to privileged ports (< 1024). Podman uses userspace networking to work around this.

#### slirp4netns (Legacy Default)

slirp4netns provides user-mode TCP/IP networking. It creates a virtual network interface inside the user namespace using a TAP device.

```bash
# Verify slirp4netns is installed
which slirp4netns

# Run a container with slirp4netns (explicit)
podman run --network slirp4netns:port_handler=rootlesskit -d -p 8080:80 nginx
```

**Characteristics:**
- Lower throughput than root networking (~1-3 Gbps vs 10+ Gbps)
- No ICMP (ping does not work from within containers by default)
- Each container gets its own network namespace

#### pasta (Modern Default)

pasta (Pack A Subtle Tap Abstraction) is the modern replacement for slirp4netns, offering better performance and more features.

```bash
# Check if pasta is available
which pasta

# Podman uses pasta by default on newer versions
podman run -d -p 8080:80 nginx
# Automatically uses pasta if available

# Explicit pasta configuration
podman run --network pasta -d -p 8080:80 nginx
```

**Characteristics:**
- Higher throughput than slirp4netns (~5-8 Gbps)
- ICMP support (ping works)
- Lower memory overhead
- Available in Podman 5.0+ as the default

### Port Forwarding

```bash
# Map host port 8080 to container port 80
podman run -d -p 8080:80 nginx

# Binding to privileged ports (< 1024) requires sysctl
# Option 1: Allow unprivileged port binding (system-wide)
sudo sysctl -w net.ipv4.ip_unprivileged_port_start=80

# Option 2: Use a port above 1024 and reverse-proxy
podman run -d -p 8080:80 nginx
```

### DNS Resolution

Containers in rootless mode resolve DNS using the host's `/etc/resolv.conf` by default. For inter-container communication:

```bash
# Containers on the same Podman network can resolve each other by name
podman network create research-net
podman run -d --network research-net --name db postgres:16-alpine
podman run -d --network research-net --name api myimage
# "api" can reach "db" by hostname
```

### Performance Tuning

```bash
# Check current network backend
podman info --format '{{.Host.NetworkBackend}}'

# For high-throughput workloads, consider rootful mode or pasta
# pasta performance tip: increase socket buffer sizes
sudo sysctl -w net.core.rmem_max=16777216
sudo sysctl -w net.core.wmem_max=16777216
```

## Volume Permissions and Ownership

### The UID Mapping Problem

When you bind-mount a host directory into a rootless container, the UIDs inside the container do not match the UIDs on the host. This frequently causes "Permission denied" errors.

```bash
# Problem: container process runs as UID 0 (root) inside,
# but that maps to your user UID (e.g., 1000) on the host.
# If the container process runs as UID 999 (e.g., postgres),
# that maps to UID 100999 on the host, which has no permissions.

podman run -v ./data:/var/lib/postgresql/data postgres:16-alpine
# ERROR: Permission denied
```

### Solution 1: --userns=keep-id

Maps your host UID to the same UID inside the container. Useful when the container process runs as a non-root user matching your host UID.

```bash
podman run --userns=keep-id -v ./data:/app/data:Z myimage
# Your host UID (1000) maps to UID 1000 inside the container
```

### Solution 2: podman unshare chown

Change the ownership of host files to match the container's expected UID, as seen from the user namespace.

```bash
# PostgreSQL expects UID 999 inside the container.
# In the rootless user namespace, UID 999 maps to host UID 100999.
podman unshare chown -R 999:999 ./pgdata

# Now the container can read/write the directory
podman run -v ./pgdata:/var/lib/postgresql/data:Z postgres:16-alpine
```

### Solution 3: :U Volume Flag

The `:U` flag tells Podman to automatically chown the volume contents to match the container user's mapped UID.

```bash
podman run -v ./data:/var/lib/postgresql/data:U postgres:16-alpine
# Podman chowns ./data to the mapped UID before starting the container
```

**Warning:** The `:U` flag modifies the ownership of host files. Only use it on directories dedicated to that container.

### SELinux Labels (:Z and :z)

On SELinux-enabled systems (RHEL, Fedora, CentOS), bind mounts require relabeling:

```bash
# :z -- shared label (multiple containers can access)
podman run -v ./shared:/data:z myimage

# :Z -- private label (only this container can access)
podman run -v ./private:/data:Z myimage

# Without :z or :Z on SELinux systems, you get "Permission denied"
```

## Cgroup v2 Requirements

### Why Cgroup v2 Matters

Resource limits (CPU, memory, I/O) in rootless mode require cgroup v2 with delegation enabled. Cgroup v1 does not support unprivileged resource control.

### Checking Your Cgroup Version

```bash
# Method 1: Check the filesystem
stat -fc %T /sys/fs/cgroup/
# "cgroup2fs" = cgroup v2
# "tmpfs" = cgroup v1

# Method 2: Podman info
podman info --format '{{.Host.CgroupVersion}}'
# "v2" or "v1"
```

### Enabling Cgroup v2

If your system uses cgroup v1, you can switch to v2:

```bash
# GRUB-based systems (Fedora, RHEL, Ubuntu)
sudo grubby --update-kernel=ALL --args="systemd.unified_cgroup_hierarchy=1"
# Or edit /etc/default/grub:
# GRUB_CMDLINE_LINUX="... systemd.unified_cgroup_hierarchy=1"
sudo grub2-mkconfig -o /boot/grub2/grub.cfg
sudo reboot
```

### Resource Limits in Rootless Mode

With cgroup v2, rootless containers support:

```bash
# Memory limit
podman run --memory 2g myimage

# CPU limit
podman run --cpus 2.0 myimage

# CPU shares (relative weight)
podman run --cpu-shares 512 myimage

# Block I/O weight
podman run --blkio-weight 200 myimage
```

Without cgroup v2, these flags are silently ignored in rootless mode. Podman does not error out -- it simply has no mechanism to enforce them.

### Cgroup Delegation

Systemd must delegate cgroup control to user sessions. This is usually enabled by default on modern distributions:

```bash
# Check if delegation is enabled
cat /sys/fs/cgroup/user.slice/user-$(id -u).slice/cgroup.controllers
# Should list: cpuset cpu io memory pids

# If controllers are missing, create a delegate config:
sudo mkdir -p /etc/systemd/system/user@.service.d
sudo tee /etc/systemd/system/user@.service.d/delegate.conf <<EOF
[Service]
Delegate=cpu cpuset io memory pids
EOF
sudo systemctl daemon-reload
```

## Troubleshooting Common Issues

### Error: "cannot clone: Operation not permitted"

**Cause:** User namespaces are disabled in the kernel.

```bash
# Check
sysctl user.max_user_namespaces
# If 0, enable:
sudo sysctl -w user.max_user_namespaces=15000
echo "user.max_user_namespaces=15000" | sudo tee /etc/sysctl.d/userns.conf
```

### Error: "ERRO[0000] cannot find UID/GID mappings"

**Cause:** Missing `/etc/subuid` or `/etc/subgid` entries.

```bash
# Fix
sudo usermod --add-subuids 100000-165535 --add-subgids 100000-165535 $USER
podman system migrate
```

### Error: "permission denied" on bind-mounted volumes

**Cause:** UID mismatch between host and container, or missing SELinux labels.

```bash
# Diagnosis: check what UID the container expects
podman run --rm myimage id
# Then chown the volume to the mapped UID
podman unshare chown -R <container-uid>:<container-gid> ./myvolume
# Or use :U flag
podman run -v ./myvolume:/data:U myimage
# On SELinux systems, add :Z
podman run -v ./myvolume:/data:Z myimage
```

### Error: "rootlessport cannot expose privileged port"

**Cause:** Attempting to bind to a port below 1024.

```bash
# Fix: lower the unprivileged port threshold
sudo sysctl -w net.ipv4.ip_unprivileged_port_start=80
echo "net.ipv4.ip_unprivileged_port_start=80" | sudo tee /etc/sysctl.d/rootless-ports.conf
```

### Containers Fail After Reboot

**Cause:** Rootless storage or network state is stale after reboot.

```bash
# Reset Podman state
podman system migrate
podman system renumber
```

### Slow Image Pulls

**Cause:** Using the vfs storage driver (no copy-on-write).

```bash
# Check your driver
podman info --format '{{.Store.GraphDriverName}}'
# If "vfs", switch to overlay or fuse-overlayfs
# Edit ~/.config/containers/storage.conf and set driver = "overlay"
podman system reset   # WARNING: deletes all images and containers
```

### Container Cannot Resolve DNS

**Cause:** `/etc/resolv.conf` contains `nameserver 127.0.0.53` (systemd-resolved stub).

```bash
# Fix: use the actual upstream DNS in the container
podman run --dns 8.8.8.8 myimage
# Or configure Podman to use a specific DNS
# In ~/.config/containers/containers.conf:
# [containers]
# dns_servers = ["8.8.8.8", "8.8.4.4"]
```

### "WARN[0000] aardvark-dns" or Network Plugin Errors

**Cause:** Missing or outdated network stack components (Netavark, aardvark-dns).

```bash
# Install or update
sudo dnf install aardvark-dns netavark    # Fedora/RHEL
sudo apt install aardvark-dns netavark    # Ubuntu 24.04+

# Reset network configuration
podman system reset --force
```

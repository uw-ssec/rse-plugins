# Layer Caching -- Deep Reference

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| How Docker Layer Caching Works | 16-66 | Layer mechanics, cache invalidation rules, cache keys |
| Dependency-First Pattern | 68-157 | COPY lockfile, install, COPY source pattern by language |
| BuildKit Cache Mounts | 159-254 | --mount=type=cache for pip, npm, cargo, apt, and Go |
| CI Caching Strategies | 256-353 | GitHub Actions cache, registry cache, inline cache |
| Cache Debugging | 355-430 | docker history, --no-cache, --progress=plain, BuildKit logs |
| Common Cache Busters | 432-503 | Changing files, ARG changes, timestamp-based operations |

---

## How Docker Layer Caching Works

### Layer Mechanics

Every instruction in a Dockerfile creates a layer. Docker caches each layer and reuses it if nothing has changed. When Docker evaluates a build step, it checks whether the instruction and its inputs are identical to a previously cached layer. If they match, Docker skips execution and reuses the cached result.

The cache check works differently depending on the instruction:

| Instruction | Cache Key |
|-------------|-----------|
| `RUN` | The command string itself (not its output) |
| `COPY` / `ADD` | Checksum of the files being copied |
| `FROM` | The image digest |
| `ARG` / `ENV` | The variable value |

### Cache Invalidation Rules

Docker's layer cache is sequential: if any layer's cache is invalidated, all subsequent layers are also invalidated. This is the most important caching concept.

```
Layer 1: FROM python:3.12-slim        [cached]
Layer 2: WORKDIR /app                  [cached]
Layer 3: COPY requirements.txt .       [INVALIDATED - file changed]
Layer 4: RUN pip install -r req...     [must rebuild - previous layer changed]
Layer 5: COPY . .                      [must rebuild]
Layer 6: RUN python setup.py build     [must rebuild]
```

**Key rules:**
1. A `RUN` layer is cached if the command string is identical (byte-for-byte) to a previous build
2. A `COPY` or `ADD` layer is cached if the checksum of all copied files matches
3. Once a cache miss occurs, every subsequent layer is rebuilt
4. The cache is local to the build machine by default (see CI Caching Strategies for remote caching)

### Cache Key Subtleties

```dockerfile
# These two are DIFFERENT cache keys (extra space)
RUN pip install numpy
RUN pip install  numpy

# ARG values affect cache of subsequent RUN instructions
ARG VERSION=1.0
RUN echo $VERSION  # cache invalidated when VERSION changes

# ENV changes do NOT invalidate RUN cache (they are part of the layer metadata)
ENV APP_VERSION=1.0
RUN echo "building"  # same cache key regardless of APP_VERSION
```

---

## Dependency-First Pattern

The most impactful caching optimization is to copy dependency lockfiles before source code. Dependencies change infrequently compared to source code, so this pattern lets Docker reuse the expensive dependency installation layer across most builds.

### General Pattern

```dockerfile
# Step 1: Copy ONLY dependency specification files
COPY <lockfile> <manifest> ./

# Step 2: Install dependencies (cached until lockfile changes)
RUN <install-command>

# Step 3: Copy the rest of the source code
COPY . .

# Step 4: Build (runs on every source change, but dependencies are cached)
RUN <build-command>
```

### Python

```dockerfile
# Copy lockfile first
COPY requirements.txt .
# or: COPY pyproject.toml uv.lock ./

# Install (cached until requirements.txt changes)
RUN pip install --no-cache-dir -r requirements.txt

# Copy source (invalidates on every change, but pip install is cached)
COPY . .
```

### Node.js

```dockerfile
# Copy package manifests first
COPY package.json package-lock.json ./

# Install (cached until package-lock.json changes)
RUN npm ci

# Copy source
COPY . .
RUN npm run build
```

### Rust

```dockerfile
# Using cargo-chef for dependency caching
COPY --from=planner /app/recipe.json recipe.json

# Install dependencies only (cached until Cargo.toml/Cargo.lock change)
RUN cargo chef cook --release --recipe-path recipe.json

# Copy source and build
COPY . .
RUN cargo build --release
```

### Go

```dockerfile
# Copy module files first
COPY go.mod go.sum ./

# Download dependencies (cached until go.mod/go.sum change)
RUN go mod download

# Copy source and build
COPY . .
RUN go build -o /app/myapp ./cmd/myapp
```

### R

```dockerfile
# Copy DESCRIPTION (which lists dependencies)
COPY DESCRIPTION .

# Install dependencies (cached until DESCRIPTION changes)
RUN R -e "pak::local_install_deps()"

# Copy source
COPY . .
```

---

## BuildKit Cache Mounts

BuildKit cache mounts persist package manager caches across builds without including them in the image layer. This is faster than `--no-cache-dir` because previously downloaded packages do not need to be re-fetched.

Enable BuildKit:

```bash
export DOCKER_BUILDKIT=1
# or use docker buildx build
```

### pip (Python)

```dockerfile
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

### uv (Python)

```dockerfile
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen
```

### npm (Node.js)

```dockerfile
RUN --mount=type=cache,target=/root/.npm \
    npm ci
```

### yarn (Node.js)

```dockerfile
RUN --mount=type=cache,target=/usr/local/share/.cache/yarn \
    yarn install --frozen-lockfile
```

### cargo (Rust)

```dockerfile
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/app/target \
    cargo build --release && \
    cp target/release/myapp /usr/local/bin/myapp
```

### apt (Debian/Ubuntu)

```dockerfile
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt/lists \
    apt-get update && \
    apt-get install -y --no-install-recommends build-essential
```

With apt cache mounts, you do not need `rm -rf /var/lib/apt/lists/*` because the cache is not part of the layer.

### Go modules

```dockerfile
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download
```

### Multiple Cache Mounts

You can combine multiple cache mounts in a single RUN:

```dockerfile
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt/lists \
    --mount=type=cache,target=/root/.cache/pip \
    apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    pip install -r requirements.txt
```

### Cache Mount Options

```dockerfile
# Specify cache ID to share across different Dockerfiles
RUN --mount=type=cache,id=pip-cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Read-only cache (for parallel builds that should not write)
RUN --mount=type=cache,target=/root/.cache/pip,readonly \
    pip install -r requirements.txt

# Specify sharing mode (locked = exclusive access)
RUN --mount=type=cache,target=/root/.cache/pip,sharing=locked \
    pip install -r requirements.txt
```

---

## CI Caching Strategies

### GitHub Actions Cache

Use the `actions/cache` action to persist Docker layer cache between CI runs:

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Cache Docker layers
  uses: actions/cache@v4
  with:
    path: /tmp/.buildx-cache
    key: ${{ runner.os }}-buildx-${{ hashFiles('**/Dockerfile') }}-${{ hashFiles('**/requirements.txt', '**/package-lock.json', '**/Cargo.lock') }}
    restore-keys: |
      ${{ runner.os }}-buildx-${{ hashFiles('**/Dockerfile') }}-
      ${{ runner.os }}-buildx-

- name: Build
  uses: docker/build-push-action@v6
  with:
    context: .
    push: false
    cache-from: type=local,src=/tmp/.buildx-cache
    cache-to: type=local,dest=/tmp/.buildx-cache-new,mode=max

# Avoid cache growing unbounded
- name: Move cache
  run: |
    rm -rf /tmp/.buildx-cache
    mv /tmp/.buildx-cache-new /tmp/.buildx-cache
```

### Registry Cache

Push cache layers to a container registry so all CI runners and developers can share them:

```yaml
- name: Build with registry cache
  uses: docker/build-push-action@v6
  with:
    context: .
    push: true
    tags: ghcr.io/org/myapp:latest
    cache-from: type=registry,ref=ghcr.io/org/myapp:cache
    cache-to: type=registry,ref=ghcr.io/org/myapp:cache,mode=max
```

Command-line equivalent:

```bash
docker buildx build \
    --cache-from type=registry,ref=ghcr.io/org/myapp:cache \
    --cache-to type=registry,ref=ghcr.io/org/myapp:cache,mode=max \
    -t ghcr.io/org/myapp:latest \
    --push .
```

### Inline Cache

Inline cache embeds cache metadata in the image itself. Simpler than registry cache but less efficient (only caches the final stage by default):

```yaml
- name: Build with inline cache
  uses: docker/build-push-action@v6
  with:
    context: .
    push: true
    tags: ghcr.io/org/myapp:latest
    cache-from: type=inline
    cache-to: type=inline
```

### GitHub Actions Cache Backend (gha)

The most integrated option for GitHub Actions -- uses the GitHub Actions cache directly:

```yaml
- name: Build
  uses: docker/build-push-action@v6
  with:
    context: .
    push: false
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

### Comparison

| Strategy | Shared Across | Setup Complexity | Cache Size Limit |
|----------|--------------|-----------------|-----------------|
| Local (`/tmp`) | Same runner | Low | Disk space |
| Registry | All runners + devs | Medium | Registry storage |
| Inline | Image pullers | Low | Image size |
| GHA | Same repository | Low | 10 GB per repo |

---

## Cache Debugging

### docker history

Inspect the layers of a built image to see what each layer contains and its size:

```bash
docker history myapp:latest
```

Output shows each layer's size, command, and creation time. Large layers indicate opportunities for optimization.

### --no-cache

Force a complete rebuild to verify the Dockerfile works without cached layers:

```bash
docker build --no-cache -t myapp:latest .
```

### --progress=plain

Show full build output including cache hit/miss information:

```bash
docker build --progress=plain -t myapp:latest .
```

Look for lines like:
```
#8 CACHED
#9 RUN pip install -r requirements.txt
```

`CACHED` means the layer was reused. Lines without `CACHED` were rebuilt.

### BuildKit Debug Output

For detailed cache behavior, enable BuildKit debug logging:

```bash
BUILDKIT_PROGRESS=plain docker build -t myapp:latest . 2>&1 | grep -E "(CACHED|DONE|importing)"
```

### Inspecting Cache Contents

List BuildKit cache entries:

```bash
docker buildx du
```

Clear BuildKit cache:

```bash
docker buildx prune
# or clear everything
docker buildx prune --all
```

### Comparing Layer Sizes

Use `docker image inspect` to see layer digests and sizes:

```bash
docker image inspect myapp:latest --format '{{range .RootFS.Layers}}{{println .}}{{end}}'
```

Use `dive` (third-party tool) for interactive layer exploration:

```bash
# Install: https://github.com/wagoodman/dive
dive myapp:latest
```

---

## Common Cache Busters

### 1. Copying Files That Change Frequently

```dockerfile
# BAD: COPY . . includes files that change every commit (README, docs, etc.)
# This invalidates the cache for every subsequent layer
COPY . .
RUN pip install -r requirements.txt  # reinstalls every time!

# GOOD: copy only what pip needs first
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

### 2. ARG Changes Invalidating Downstream Layers

```dockerfile
ARG BUILD_DATE
# Every layer after this ARG is cache-busted when BUILD_DATE changes
RUN pip install -r requirements.txt  # rebuilt every time BUILD_DATE changes!

# BETTER: put volatile ARGs after expensive operations
RUN pip install -r requirements.txt
ARG BUILD_DATE
LABEL build_date=$BUILD_DATE
```

### 3. Timestamp-Based Operations

```dockerfile
# BAD: apt-get update fetches new package lists every time
# (but the RUN string is identical, so it looks cached until COPY changes above it)
RUN apt-get update && apt-get install -y curl

# The real problem: if a previous COPY invalidated the cache,
# apt-get update runs again and may install different package versions
# Use --mount=type=cache or pin package versions for reproducibility
```

### 4. Non-Deterministic Commands

```dockerfile
# BAD: git clone fetches latest, breaking reproducibility
RUN git clone https://github.com/org/repo.git

# GOOD: pin to a specific commit
RUN git clone https://github.com/org/repo.git && \
    cd repo && git checkout abc1234

# BETTER: use COPY from the build context instead of cloning
COPY vendor/repo /app/vendor/repo
```

### 5. Changing File Permissions After COPY

```dockerfile
# BAD: two layers, chmod invalidates cache independently
COPY . .
RUN chmod +x entrypoint.sh

# GOOD: set permissions in one step
COPY --chmod=755 entrypoint.sh .
# or
COPY . .
RUN chmod +x entrypoint.sh  # at least in the same layer as any subsequent operations
```

### 6. Different .dockerignore Patterns

If `.dockerignore` changes, the set of files sent to the build context changes, which can invalidate `COPY` layers even if the actually-used files have not changed. Keep `.dockerignore` stable.

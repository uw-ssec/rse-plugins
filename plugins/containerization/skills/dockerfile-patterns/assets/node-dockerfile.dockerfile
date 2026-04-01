# ==============================================================================
# Multi-Stage Node.js Dockerfile Template
# Pattern: Build stage compiles TypeScript/bundles assets, runtime stage runs
#          production code with production-only dependencies.
# ==============================================================================

# --- Build Arguments ---------------------------------------------------------
ARG NODE_VERSION=22

# ==============================================================================
# Stage 1: Builder
# Installs all dependencies (including devDependencies), compiles TypeScript,
# bundles assets, or runs any build step. This stage is discarded.
# ==============================================================================
FROM node:${NODE_VERSION}-slim AS builder

WORKDIR /app

# Copy package manifests first for layer caching.
# npm ci installs from package-lock.json for deterministic builds.
# Dependencies are only reinstalled when these files change.
COPY package.json package-lock.json ./

# Install ALL dependencies (including devDependencies needed for build).
# npm ci is preferred over npm install for CI/Docker:
#   - Deletes node_modules before installing (clean state)
#   - Installs exact versions from package-lock.json
#   - Fails if package-lock.json is out of sync with package.json
RUN npm ci

# Copy the application source code.
COPY . .

# Build the application (TypeScript compile, webpack, vite, etc.).
# Remove or modify this line if your project does not have a build step.
RUN npm run build

# ==============================================================================
# Stage 2: Runtime
# Minimal image with production dependencies only and the built output.
# No devDependencies, no source TypeScript, no build tools.
# ==============================================================================
FROM node:${NODE_VERSION}-slim AS runtime

WORKDIR /app

# Copy package manifests and install production dependencies only.
# --omit=dev excludes devDependencies (test frameworks, linters, etc.)
COPY package.json package-lock.json ./
RUN npm ci --omit=dev && \
    npm cache clean --force

# Copy the built application from the builder stage.
# Adjust the source path to match your build output directory.
COPY --from=builder /app/dist ./dist

# If your app needs additional files at runtime (e.g., templates, static assets),
# copy them explicitly:
# COPY --from=builder /app/public ./public
# COPY --from=builder /app/views ./views

# Create a non-root user.
# The node image includes a 'node' user (UID 1000), but creating a dedicated
# user with a higher UID avoids conflicts with host user namespaces.
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --create-home --shell /bin/false appuser && \
    chown -R 1001:1001 /app

# Switch to non-root user.
USER 1001

# Set Node.js to production mode.
# This affects Express.js behavior, logging levels, and some npm packages.
ENV NODE_ENV=production

# Document the port this application listens on.
EXPOSE 3000

# Health check for container orchestrators.
# Adjust the endpoint and port to match your application.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (r) => { process.exit(r.statusCode === 200 ? 0 : 1) })" || exit 1

# OCI standard labels.
LABEL org.opencontainers.image.title="my-node-app" \
      org.opencontainers.image.description="Description of your Node.js application" \
      org.opencontainers.image.version="0.1.0" \
      org.opencontainers.image.source="https://github.com/org/repo" \
      org.opencontainers.image.licenses="MIT"

# Use exec form for proper signal handling (SIGTERM forwarded to Node process).
ENTRYPOINT ["node", "dist/index.js"]

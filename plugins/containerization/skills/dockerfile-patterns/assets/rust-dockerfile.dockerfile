# ==============================================================================
# Multi-Stage Rust Dockerfile Template
# Uses cargo-chef for dependency caching.
# Pattern: Plan dependencies -> cook (cache) -> build -> copy binary to minimal image
# ==============================================================================

# --- Build Arguments ---------------------------------------------------------
ARG RUST_VERSION=1.82

# ==============================================================================
# Stage 1: Chef
# Base stage with cargo-chef installed. Used by planner and builder stages.
# ==============================================================================
FROM rust:${RUST_VERSION} AS chef

# Install cargo-chef for dependency caching.
# cargo-chef analyzes your project's dependencies and creates a "recipe"
# that can be cooked (compiled) separately from your source code.
RUN cargo install cargo-chef

WORKDIR /app

# ==============================================================================
# Stage 2: Planner
# Analyzes the project and generates a recipe.json that captures all
# dependency information without including source code.
# ==============================================================================
FROM chef AS planner

# Copy the full source tree to analyze dependencies.
COPY . .

# Generate the recipe file. This captures Cargo.toml, Cargo.lock, and
# dependency graph information.
RUN cargo chef prepare --recipe-path recipe.json

# ==============================================================================
# Stage 3: Builder
# Cooks the recipe (compiles dependencies only), then builds the application.
# The cook step is cached as long as dependencies do not change, making
# rebuilds after source-only changes very fast.
# ==============================================================================
FROM chef AS builder

# Install system dependencies needed for compilation.
# Add libraries here if your crate depends on system libraries.
# Examples: libssl-dev (reqwest/native-tls), libpq-dev (diesel/postgres),
#           protobuf-compiler (prost/tonic)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        pkg-config \
        libssl-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy the recipe from the planner stage.
COPY --from=planner /app/recipe.json recipe.json

# Cook: compile all dependencies defined in the recipe.
# This layer is cached as long as Cargo.toml and Cargo.lock do not change.
# Even large dependency trees (tokio, serde, etc.) only compile once.
RUN cargo chef cook --release --recipe-path recipe.json

# Copy the application source code.
COPY . .

# Build the application in release mode.
# Dependencies are already compiled from the cook step, so only your
# crate's source code is compiled here.
RUN cargo build --release

# Verify the binary exists and is executable.
RUN test -f /app/target/release/myapp

# ==============================================================================
# Stage 4: Runtime
# Minimal final image containing only the compiled binary.
# Uses distroless for security (no shell, no package manager).
# ==============================================================================

# --- Option A: Distroless (recommended for production) -----------------------
# gcr.io/distroless/cc-debian12 includes glibc and libgcc.
# Use gcr.io/distroless/static-debian12 if linking with musl (fully static).
FROM gcr.io/distroless/cc-debian12 AS runtime

# --- Option B: Scratch (smallest possible, needs static linking) -------------
# Uncomment the following and comment out Option A if you compile with
# --target x86_64-unknown-linux-musl for a fully static binary.
# FROM scratch AS runtime
# COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# Copy the release binary from the builder stage.
COPY --from=builder /app/target/release/myapp /usr/local/bin/myapp

# Run as non-root. Distroless images support numeric UIDs.
USER 1001

# Document the port (adjust to match your application).
EXPOSE 8080

# OCI standard labels.
LABEL org.opencontainers.image.title="my-rust-app" \
      org.opencontainers.image.description="Description of your Rust application" \
      org.opencontainers.image.version="0.1.0" \
      org.opencontainers.image.source="https://github.com/org/repo" \
      org.opencontainers.image.licenses="MIT"

# Use exec form. Since there is no shell in distroless, only exec form works.
ENTRYPOINT ["myapp"]

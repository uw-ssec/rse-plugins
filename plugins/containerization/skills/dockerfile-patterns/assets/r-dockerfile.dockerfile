# ==============================================================================
# R Dockerfile Template
# Base: rocker/r-ver (version-locked R installation)
# Package Manager: pak (fast, reliable R package installation)
# ==============================================================================

# --- Build Arguments ---------------------------------------------------------
# R version. See https://rocker-project.org/images/ for available versions.
ARG R_VERSION=4.4

# ==============================================================================
# Stage 1: Base
# Uses the rocker/r-ver image which provides a version-locked R installation
# on Debian. The rocker project handles R's complex system dependency
# requirements (Fortran, BLAS/LAPACK, etc.).
# ==============================================================================
FROM rocker/r-ver:${R_VERSION}

# Install pak for fast, dependency-aware package installation.
# pak resolves dependencies, detects required system libraries, and installs
# them automatically on supported platforms.
RUN R -e "install.packages('pak', repos = 'https://r-lib.github.io/p/pak/stable/')"

# Install system libraries commonly needed by R packages.
# pak can auto-detect many of these, but pre-installing common ones saves time.
# Customize this list based on your project's package dependencies.
# Common mappings:
#   - sf / terra: libgdal-dev, libgeos-dev, libproj-dev
#   - xml2: libxml2-dev
#   - httr / curl: libcurl4-openssl-dev, libssl-dev
#   - textshaping / ragg: libharfbuzz-dev, libfribidi-dev, libfreetype6-dev
#   - magick: libmagick++-dev
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libcurl4-openssl-dev \
        libssl-dev \
        libxml2-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy DESCRIPTION file first for dependency layer caching.
# R package dependencies are declared in the DESCRIPTION file.
# This layer is only re-run when DESCRIPTION changes.
COPY DESCRIPTION .

# Install all dependencies listed in DESCRIPTION using pak.
# pak::local_install_deps() reads DESCRIPTION and installs Imports and Depends.
# The ask = FALSE flag prevents interactive prompts.
RUN R -e "pak::local_install_deps(ask = FALSE)"

# --- Alternative: renv-based installation (uncomment if using renv) ----------
# COPY renv.lock .
# COPY renv/ renv/
# COPY .Rprofile .
# RUN R -e "renv::restore()"
# -----------------------------------------------------------------------------

# Copy the application source code.
# This layer is invalidated on every source change, but package installation
# above is cached as long as DESCRIPTION does not change.
COPY . .

# Optional: install the package itself (if this is an R package project).
# This makes the package's functions available via library(mypackage).
# Remove this line if this is a script-based project, not a package.
# RUN R -e "pak::local_install(ask = FALSE)"

# Create a non-root user.
# The rocker images run as root by default; switch for production.
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --create-home --shell /bin/false appuser && \
    chown -R 1001:1001 /app

# Switch to non-root user.
USER 1001

# Document the port if running a Shiny app or Plumber API.
# Shiny default: 3838, Plumber default: 8000
# EXPOSE 3838

# OCI standard labels.
LABEL org.opencontainers.image.title="my-r-app" \
      org.opencontainers.image.description="Description of your R application" \
      org.opencontainers.image.version="0.1.0" \
      org.opencontainers.image.source="https://github.com/org/repo" \
      org.opencontainers.image.licenses="MIT"

# Use exec form for proper signal handling.
# For a script-based project:
ENTRYPOINT ["Rscript", "main.R"]

# --- Alternative entrypoints ------------------------------------------------
# For a Shiny application:
# ENTRYPOINT ["R", "-e", "shiny::runApp('/app', host='0.0.0.0', port=3838)"]
#
# For a Plumber API:
# ENTRYPOINT ["R", "-e", "plumber::plumb('/app/plumber.R')$run(host='0.0.0.0', port=8000)"]
#
# For an R package's command-line interface:
# ENTRYPOINT ["Rscript", "-e", "mypackage::main()"]
# -----------------------------------------------------------------------------

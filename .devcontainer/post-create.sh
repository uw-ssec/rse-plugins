#!/usr/bin/env bash
# Post-create script for GitHub Codespaces
# Installs Claude Code, Copilot CLI with RSE plugins, and sets up .github/ directory

set -euo pipefail

log() { echo "[post-create] $*"; }

echo ""
echo "=== Setting up RSE Plugins Codespace ==="
echo ""

# --- Install Claude Code CLI ---
log "Installing Claude Code CLI..."
curl -fsSL https://claude.ai/install.sh | bash

# --- Install GitHub Copilot CLI ---
log "Installing GitHub Copilot CLI..."
if ! command -v copilot &>/dev/null; then
    curl -fsSL https://gh.io/copilot-install | bash
else
    log "Copilot CLI already installed, skipping."
fi

# Verify copilot is available
if ! command -v copilot &>/dev/null; then
    log "ERROR: Copilot CLI not found after install. Aborting."
    exit 1
fi

# --- Register RSE plugins marketplace ---
log "Registering uw-ssec/rse-plugins marketplace..."
copilot plugin marketplace add uw-ssec/rse-plugins

# --- Install all RSE plugins ---
log "Installing RSE plugins..."
PLUGINS=(
    "ai-research-workflows@rse-plugins"
    "scientific-python-development@rse-plugins"
    "project-management@rse-plugins"
    "scientific-domain-applications@rse-plugins"
    "holoviz-visualization@rse-plugins"
    "gaia-data-downloader@rse-plugins"
    "zarr-chunk-optimization@rse-plugins"
    "zarr-data-format@rse-plugins"
    "research-software-design@rse-plugins"
)

for plugin in "${PLUGINS[@]}"; do
    log "  Installing ${plugin}..."
    copilot plugin install "${plugin}"
done

# --- Copy agents and skills to .github/ for workspace discovery ---
log "Copying agents and skills to .github/..."
mkdir -p .github/agents
mkdir -p .github/skills

for plugin_dir in plugins/*/; do
    if [ -d "${plugin_dir}agents" ]; then
        cp -r "${plugin_dir}agents"/* .github/agents/ 2>/dev/null || true
    fi
done

for plugin_dir in community-plugins/*/; do
    if [ -d "${plugin_dir}agents" ]; then
        cp -r "${plugin_dir}agents"/* .github/agents/ 2>/dev/null || true
    fi
done

for plugin_dir in plugins/*/; do
    if [ -d "${plugin_dir}skills" ]; then
        cp -r "${plugin_dir}skills"/* .github/skills/ 2>/dev/null || true
    fi
done

for plugin_dir in community-plugins/*/; do
    if [ -d "${plugin_dir}skills" ]; then
        cp -r "${plugin_dir}skills"/* .github/skills/ 2>/dev/null || true
    fi
done

# --- Conditionally download OAI-compatible Copilot VSIX ---
VSIX_ENV=".devcontainer/oai-compatible-copilot-vsix.env"
VSIX_CACHE_DIR="${HOME}/.cache/oai-compatible-copilot"

if [ -z "${LITELLM_BASE_URL:-}" ]; then
    log "No LITELLM_BASE_URL set. Skipping OAI-compatible Copilot VSIX download."
    log "To use a LiteLLM gateway, set LITELLM_BASE_URL and LITELLM_API_KEY as Codespace secrets and rebuild."
else
    log "LiteLLM gateway detected. Downloading OAI-compatible Copilot VSIX..."

    if [ ! -f "${VSIX_ENV}" ]; then
        log "WARNING: ${VSIX_ENV} not found. Skipping VSIX download."
    else
        # Load pinned VSIX metadata
        # shellcheck source=/dev/null
        source "${VSIX_ENV}"

        # Validate required variables
        if [ -z "${VSIX_RELEASE_TAG:-}" ] || [ -z "${VSIX_FILENAME:-}" ] || [ -z "${EXPECTED_VSIX_SHA256:-}" ]; then
            log "WARNING: Missing required variables in ${VSIX_ENV}. Skipping VSIX download."
        elif ! echo "${EXPECTED_VSIX_SHA256}" | grep -qE '^[0-9a-f]{64}$'; then
            log "WARNING: EXPECTED_VSIX_SHA256 is not a valid 64-character hex SHA256. Skipping."
        elif echo "${VSIX_FILENAME}" | grep -qE '(\.\.|/)'; then
            log "WARNING: VSIX_FILENAME contains unsafe path characters. Skipping."
        else
            mkdir -p "${VSIX_CACHE_DIR}"
            VSIX_PATH="${VSIX_CACHE_DIR}/${VSIX_FILENAME}"

            # Re-download if missing or hash mismatch
            NEEDS_DOWNLOAD=true
            if [ -f "${VSIX_PATH}" ]; then
                ACTUAL_SHA256="$(sha256sum "${VSIX_PATH}" | awk '{print $1}')"
                if [ "${ACTUAL_SHA256}" = "${EXPECTED_VSIX_SHA256}" ]; then
                    log "Cached VSIX is valid. Skipping download."
                    NEEDS_DOWNLOAD=false
                else
                    log "Cached VSIX SHA256 mismatch. Re-downloading..."
                    rm -f "${VSIX_PATH}"
                fi
            fi

            if [ "${NEEDS_DOWNLOAD}" = "true" ]; then
                DOWNLOAD_URL="https://github.com/uw-ssec/oai-compatible-copilot/releases/download/${VSIX_RELEASE_TAG}/${VSIX_FILENAME}"
                log "Downloading VSIX from ${DOWNLOAD_URL}..."

                DOWNLOAD_OK=true
                curl -fsSL --tlsv1.2 --retry 3 --retry-delay 2 \
                    -o "${VSIX_PATH}" "${DOWNLOAD_URL}" || DOWNLOAD_OK=false

                if [ "${DOWNLOAD_OK}" = "true" ]; then
                    ACTUAL_SHA256="$(sha256sum "${VSIX_PATH}" | awk '{print $1}')"
                    if [ "${ACTUAL_SHA256}" != "${EXPECTED_VSIX_SHA256}" ]; then
                        log "WARNING: Downloaded VSIX SHA256 mismatch. Removing."
                        rm -f "${VSIX_PATH}"
                    else
                        log "VSIX downloaded and verified successfully."
                    fi
                else
                    log "WARNING: VSIX download failed. Default Copilot models will be used."
                    rm -f "${VSIX_PATH}"
                fi
            fi
        fi
    fi
fi

# --- Summary ---
echo ""
echo "=== Setup Complete ==="
echo ""
echo "Agents in .github/agents: $(ls -1 .github/agents/ 2>/dev/null | wc -l | tr -d ' ')"
echo "Skills in .github/skills: $(ls -1 .github/skills/ 2>/dev/null | wc -l | tr -d ' ')"
echo ""
echo "Claude Code and GitHub Copilot CLI are ready to use."
echo "Run 'copilot' in the terminal to get started."

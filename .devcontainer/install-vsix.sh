#!/usr/bin/env bash
# Post-attach script for GitHub Codespaces
# Installs OAI-compatible Copilot VSIX and configures VS Code gateway settings
# if LiteLLM credentials are present. Non-fatal on failure.

set -uo pipefail

VSIX_ENV=".devcontainer/oai-compatible-copilot-vsix.env"
VSIX_CACHE_DIR="${HOME}/.cache/oai-compatible-copilot"
MACHINE_SETTINGS_DIR="${HOME}/.vscode-server/data/Machine"
MACHINE_SETTINGS="${MACHINE_SETTINGS_DIR}/settings.json"

# Guard: skip if LiteLLM gateway is not configured
if [ -z "${LITELLM_BASE_URL:-}" ]; then
    exit 0
fi

echo "[install-vsix] LiteLLM gateway detected. Installing OAI-compatible Copilot extension..."

# Load pinned VSIX metadata
if [ ! -f "${VSIX_ENV}" ]; then
    echo "[install-vsix] WARNING: ${VSIX_ENV} not found. Skipping VSIX install."
    exit 0
fi

# shellcheck source=/dev/null
source "${VSIX_ENV}"

# Validate required variables
if [ -z "${VSIX_FILENAME:-}" ] || [ -z "${EXPECTED_VSIX_SHA256:-}" ]; then
    echo "[install-vsix] WARNING: Missing required variables in ${VSIX_ENV}. Skipping."
    exit 0
fi

VSIX_PATH="${VSIX_CACHE_DIR}/${VSIX_FILENAME}"

# Validate VSIX filename contains no path traversal characters
if echo "${VSIX_FILENAME}" | grep -qE '(\.\.|/)'; then
    echo "[install-vsix] WARNING: VSIX_FILENAME contains unsafe path characters. Skipping."
    exit 0
fi

# Verify cached VSIX exists and matches expected SHA256
if [ ! -f "${VSIX_PATH}" ]; then
    echo "[install-vsix] WARNING: VSIX not found in cache (${VSIX_PATH}). Run rebuild to re-download."
    exit 0
fi

ACTUAL_SHA256="$(sha256sum "${VSIX_PATH}" | awk '{print $1}')"
if [ "${ACTUAL_SHA256}" != "${EXPECTED_VSIX_SHA256}" ]; then
    echo "[install-vsix] WARNING: VSIX SHA256 mismatch. Skipping installation."
    exit 0
fi

# Find VS Code CLI binary
CODE_BIN=""
for candidate in \
    "/vscode/vscode-server/bin/linux-x64/*/bin/remote-cli/code" \
    "${HOME}/.vscode-server/bin/*/bin/remote-cli/code" \
    "/usr/local/bin/code"; do
    # shellcheck disable=SC2086
    match="$(ls ${candidate} 2>/dev/null | head -1 || true)"
    if [ -n "${match}" ] && [ -x "${match}" ]; then
        CODE_BIN="${match}"
        break
    fi
done

if [ -z "${CODE_BIN}" ]; then
    echo "[install-vsix] WARNING: VS Code CLI not found. Skipping VSIX installation."
    exit 0
fi

# Install VSIX if not already installed
EXTENSION_ID="johnny-zhao.oai-compatible-copilot"
if "${CODE_BIN}" --list-extensions 2>/dev/null | grep -qi "${EXTENSION_ID}"; then
    echo "[install-vsix] OAI-compatible Copilot extension already installed."
else
    echo "[install-vsix] Installing VSIX..."
    if ! "${CODE_BIN}" --install-extension "${VSIX_PATH}" --force 2>/dev/null; then
        echo "[install-vsix] WARNING: VSIX install failed. Default Copilot will be used."
        exit 0
    fi
    echo "[install-vsix] VSIX installed successfully."
fi

# Write machine-level VS Code settings to route Copilot Chat through the gateway
mkdir -p "${MACHINE_SETTINGS_DIR}"

# Merge or create settings.json
if [ -f "${MACHINE_SETTINGS}" ]; then
    # Use python3 to merge settings (available via the python devcontainer feature)
    python3 - <<PYEOF
import json, sys

path = "${MACHINE_SETTINGS}"
try:
    with open(path, "r") as f:
        settings = json.load(f)
except (json.JSONDecodeError, FileNotFoundError):
    settings = {}

settings["oai-compatible-copilot.baseUrl"] = "${LITELLM_BASE_URL}/v1"
settings["oai-compatible-copilot.models"] = [
    {"name": "gpt-5.4-mini", "isDefault": True},
    {"name": "gpt-oss-120b"}
]

with open(path, "w") as f:
    json.dump(settings, f, indent=2)
    f.write("\n")

print("[install-vsix] VS Code gateway settings written.")
PYEOF
else
    cat > "${MACHINE_SETTINGS}" <<JSON
{
  "oai-compatible-copilot.baseUrl": "${LITELLM_BASE_URL}/v1",
  "oai-compatible-copilot.models": [
    {"name": "gpt-5.4-mini", "isDefault": true},
    {"name": "gpt-oss-120b"}
  ]
}
JSON
    echo "[install-vsix] VS Code gateway settings written."
fi

echo "[install-vsix] Copilot Chat will use the LiteLLM gateway models."

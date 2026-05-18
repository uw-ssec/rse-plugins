#!/usr/bin/env bash
# Post-start script for GitHub Codespaces
# Configures Copilot CLI to route through LiteLLM gateway if credentials are present

set -euo pipefail

echo ""
echo "=== RSE Plugins Codespace ==="
echo ""

BASHRC="${HOME}/.bashrc"
GATEWAY_MARKER='# >>> litellm-gateway-env (rse-plugins) >>>'

if [ -n "${LITELLM_BASE_URL:-}" ] && [ -n "${LITELLM_API_KEY:-}" ]; then
    echo "[post-start] LiteLLM gateway detected. Configuring Copilot CLI environment..."

    # Write gateway env vars to ~/.bashrc idempotently
    if ! grep -qF "${GATEWAY_MARKER}" "${BASHRC}" 2>/dev/null; then
        {
            echo ""
            echo "${GATEWAY_MARKER}"
            echo "export COPILOT_PROVIDER_BASE_URL=\"${LITELLM_BASE_URL}/v1\""
            echo "export COPILOT_PROVIDER_API_KEY=\"${LITELLM_API_KEY}\""
            echo "export COPILOT_MODEL=\"gpt-5.4-mini\""
            echo "export COPILOT_PROVIDER_WIRE_API=\"responses\""
            echo "# <<< litellm-gateway-env (rse-plugins) <<<"
        } >> "${BASHRC}"
    fi

    echo "[post-start] Mode: LiteLLM gateway (${LITELLM_BASE_URL})"
    echo "[post-start] Copilot CLI will route through the gateway in new terminal sessions."
    echo "[post-start] Copilot Chat will use the OAI-compatible extension (configured on attach)."
else
    echo "[post-start] Mode: Default GitHub Copilot"
    echo "[post-start] Using your GitHub Copilot subscription models."
    echo "[post-start] To use a LiteLLM gateway instead, set LITELLM_BASE_URL and"
    echo "[post-start] LITELLM_API_KEY as Codespace secrets and rebuild the container."
fi

echo ""
echo "[post-start] Ready. Run 'copilot' in the terminal to get started."

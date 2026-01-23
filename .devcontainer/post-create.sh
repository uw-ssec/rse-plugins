#!/bin/bash
# Post-create script for GitHub Codespaces
# Installs Claude Code and copies plugin agents/skills to .github directory

set -e

echo "=== Setting up RSE Agents Codespace ==="

# Install Claude Code CLI globally
echo "Installing Claude Code CLI..."
npm install -g @anthropic-ai/claude-code

# Create .github/agents and .github/skills directories
echo "Creating .github/agents and .github/skills directories..."
mkdir -p .github/agents
mkdir -p .github/skills

# Copy agents from plugins directory
echo "Copying agents from plugins..."
if [ -d "plugins" ]; then
    for plugin_dir in plugins/*/; do
        if [ -d "${plugin_dir}agents" ]; then
            cp -r "${plugin_dir}agents"/* .github/agents/ 2>/dev/null || true
            echo "  - Copied agents from ${plugin_dir}"
        fi
    done
fi

# Copy agents from community-plugins directory
echo "Copying agents from community-plugins..."
if [ -d "community-plugins" ]; then
    for plugin_dir in community-plugins/*/; do
        if [ -d "${plugin_dir}agents" ]; then
            cp -r "${plugin_dir}agents"/* .github/agents/ 2>/dev/null || true
            echo "  - Copied agents from ${plugin_dir}"
        fi
    done
fi

# Copy skills from plugins directory
echo "Copying skills from plugins..."
if [ -d "plugins" ]; then
    for plugin_dir in plugins/*/; do
        if [ -d "${plugin_dir}skills" ]; then
            cp -r "${plugin_dir}skills"/* .github/skills/ 2>/dev/null || true
            echo "  - Copied skills from ${plugin_dir}"
        fi
    done
fi

# Copy skills from community-plugins directory
echo "Copying skills from community-plugins..."
if [ -d "community-plugins" ]; then
    for plugin_dir in community-plugins/*/; do
        if [ -d "${plugin_dir}skills" ]; then
            cp -r "${plugin_dir}skills"/* .github/skills/ 2>/dev/null || true
            echo "  - Copied skills from ${plugin_dir}"
        fi
    done
fi

# Summary
echo ""
echo "=== Setup Complete ==="
echo "Agents copied to .github/agents:"
ls -1 .github/agents/ 2>/dev/null || echo "  (none)"
echo ""
echo "Skills copied to .github/skills:"
ls -1 .github/skills/ 2>/dev/null || echo "  (none)"
echo ""
echo "Claude Code is ready to use!"

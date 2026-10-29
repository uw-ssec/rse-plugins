---
description: Build AI-powered natural language data exploration interfaces with Lumen AI
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Lumen AI

Build conversational data exploration interfaces powered by LLMs.

## Arguments

$ARGUMENTS — describe the goal (e.g., "natural language query interface for this database", "custom AI analyst for sales data", "RAG-powered analytics dashboard")

## Workflow

1. **Understand the requirements:**
   - Data sources to connect
   - LLM provider (OpenAI, Anthropic, local via Ollama)
   - Domain-specific context or custom agents needed
   - RAG with document context if applicable

2. **Design the Lumen AI configuration:**
   - Data source connections
   - LLM provider setup and API keys
   - Custom agent definitions for domain expertise
   - Document sources for RAG context

3. **Implement** the Lumen AI application:
   - Configure data sources
   - Set up LLM integration
   - Define custom tools and agents if needed
   - Add document context for RAG

4. **Verify** the application works:
   ```bash
   lumen serve ai_dashboard.yaml --show
   ```

5. **Report** the configuration and usage instructions.

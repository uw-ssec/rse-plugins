# LLM Provider Configuration

Comprehensive guide to configuring different LLM providers with Lumen AI.

## Table of Contents
- [OpenAI Configuration](#openai-configuration)
- [Anthropic Claude Configuration](#anthropic-claude-configuration)
- [Mistral Configuration](#mistral-configuration)
- [Google Gemini Configuration](#google-gemini-configuration)
- [Local Models with Ollama](#local-models-with-ollama)
- [Local Models with LlamaCPP](#local-models-with-llamacpp)
- [Provider Selection Guide](#provider-selection-guide)

## OpenAI Configuration

### Setup

```bash
export OPENAI_API_KEY="sk-..."
```

### Configuration

```python
import lumen.ai as lmai

# Default: uses gpt-4o-mini
lmai.llm.llm_type = "openai"
lmai.llm.model = "gpt-4o"  # Or gpt-4o-mini, gpt-4-turbo
lmai.llm.temperature = 0.1  # 0.0-2.0, lower = more deterministic
```

### Available Models
- **gpt-4o**: Best overall performance, balanced cost
- **gpt-4o-mini**: Fast, cost-effective, good for development
- **gpt-4-turbo**: High performance, higher cost

### Best For
- Production workloads
- Complex SQL generation
- Balanced performance/cost ratio

## Anthropic Claude Configuration

### Setup

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Configuration

```python
import lumen.ai as lmai

lmai.llm.llm_type = "anthropic"
lmai.llm.model = "claude-3-5-sonnet-20241022"
lmai.llm.temperature = 0.1
```

### Available Models
- **claude-3-5-sonnet-20241022**: Best reasoning, SQL generation
- **claude-3-opus**: Highest capability
- **claude-3-haiku**: Fast, cost-effective

### Best For
- Complex analytical reasoning
- SQL query generation
- High-quality explanations

## Mistral Configuration

### Setup

```bash
export MISTRAL_API_KEY="..."
```

### Configuration

```python
import lumen.ai as lmai

lmai.llm.llm_type = "mistral"
lmai.llm.model = "mistral-large-latest"
```

### Available Models
- **mistral-large-latest**: Most capable
- **mistral-medium**: Balanced
- **mistral-small**: Cost-effective

### Best For
- European data residency requirements
- Cost-sensitive deployments

## Google Gemini Configuration

### Setup

```bash
export GOOGLE_API_KEY="..."
```

### Configuration

```python
import lumen.ai as lmai

lmai.llm.llm_type = "google"
lmai.llm.model = "gemini-1.5-pro"
```

### Available Models
- **gemini-1.5-pro**: Best performance
- **gemini-1.5-flash**: Fast, efficient

### Best For
- Google Cloud integrations
- High context length needs

## Local Models with Ollama

### Installation

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull models
ollama pull llama3.1
ollama pull mistral
ollama pull codellama
```

### Configuration

```python
import lumen.ai as lmai

lmai.llm.llm_type = "ollama"
lmai.llm.model = "llama3.1"
lmai.llm.base_url = "http://localhost:11434"
```

### Recommended Models
- **llama3.1**: Best open-source all-around
- **mistral**: Good performance
- **codellama**: Code-focused tasks

### Best For
- Full data privacy (no external API calls)
- No API costs
- Sensitive data environments
- Development without API limits

## Local Models with LlamaCPP

### Installation

```bash
pip install llama-cpp-python
```

### Configuration

```python
import lumen.ai as lmai

lmai.llm.llm_type = "llamacpp"
lmai.llm.model_path = "./models/llama-3.1-8B-Instruct.gguf"
```

### Best For
- Maximum control over deployment
- Custom model fine-tuning
- Air-gapped environments

## Provider Selection Guide

### Production Use Cases

| Use Case | Recommended Provider | Model | Reasoning |
|----------|---------------------|-------|-----------|
| Business analytics | OpenAI | gpt-4o | Best balance of performance and cost |
| Complex SQL | Anthropic | claude-3-5-sonnet | Superior reasoning |
| High-volume queries | OpenAI | gpt-4o-mini | Cost-effective |
| Sensitive data | Ollama | llama3.1 | Full local control |
| European deployment | Mistral | mistral-large | Data residency |

### Development Use Cases

| Use Case | Recommended Provider | Model | Reasoning |
|----------|---------------------|-------|-----------|
| Rapid testing | OpenAI | gpt-4o-mini | Fast, cheap |
| No API budget | Ollama | llama3.1 | Free local |
| Feature development | Anthropic | claude-3-haiku | Quick iterations |

### Performance Comparison

**Query Speed** (fastest to slowest):
1. Claude 3 Haiku
2. GPT-4o-mini
3. Gemini 1.5 Flash
4. GPT-4o
5. Claude 3.5 Sonnet
6. Local models (varies by hardware)

**Quality** (best to good):
1. Claude 3.5 Sonnet
2. GPT-4o
3. Claude 3 Opus
4. Gemini 1.5 Pro
5. Mistral Large
6. Local models (varies by model size)

**Cost** (cheapest to expensive per 1M tokens):
1. Ollama/Local (free)
2. GPT-4o-mini (~$0.15-0.60)
3. Claude 3 Haiku (~$0.25-1.25)
4. Gemini 1.5 Flash (~$0.35-1.05)
5. Claude 3.5 Sonnet (~$3-15)
6. GPT-4o (~$2.50-10)

### Configuration Best Practices

**Use environment variables**:
```python
import os
lmai.llm.api_key = os.getenv("OPENAI_API_KEY")
```

**Never hardcode secrets**:
```python
# ❌ Bad
lmai.llm.api_key = "sk-..."

# ✅ Good
lmai.llm.api_key = os.getenv("OPENAI_API_KEY")
```

**Switch providers easily**:
```python
# Configuration dict for easy switching
LLM_CONFIGS = {
    "production": {
        "llm_type": "anthropic",
        "model": "claude-3-5-sonnet-20241022",
        "temperature": 0.1
    },
    "development": {
        "llm_type": "openai",
        "model": "gpt-4o-mini",
        "temperature": 0.1
    },
    "local": {
        "llm_type": "ollama",
        "model": "llama3.1",
        "base_url": "http://localhost:11434"
    }
}

# Apply configuration
env = os.getenv("ENVIRONMENT", "development")
config = LLM_CONFIGS[env]
for key, value in config.items():
    setattr(lmai.llm, key, value)
```

### Advanced Configuration

**Timeout settings**:
```python
lmai.llm.timeout = 60  # seconds
```

**Retry logic**:
```python
lmai.llm.max_retries = 3
lmai.llm.retry_delay = 1  # seconds
```

**Custom headers** (for proxies, enterprise):
```python
lmai.llm.headers = {
    "X-Custom-Header": "value"
}
```

### Troubleshooting

**API key not working**:
```python
import os
print(os.getenv("OPENAI_API_KEY"))  # Should not be None
```

**Network issues**:
```bash
# Test OpenAI connection
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Test Anthropic connection
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"
```

**Rate limits**:
- OpenAI: Tier-based (upgrade account tier)
- Anthropic: Request-per-minute limits
- Solution: Implement exponential backoff, upgrade tier, or use local models

**Model not found**:
```python
# List available models
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
models = openai.Model.list()
print([m.id for m in models.data])
```

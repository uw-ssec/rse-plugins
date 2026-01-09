# Deployment Guide

Complete guide to deploying Lumen AI applications in development and production environments.

## Table of Contents
- [Development Deployment](#development-deployment)
- [Production Deployment](#production-deployment)
- [Docker Deployment](#docker-deployment)
- [Environment Configuration](#environment-configuration)
- [Security Best Practices](#security-best-practices)
- [Monitoring and Logging](#monitoring-and-logging)

## Development Deployment

### Local Testing

```bash
# Launch with auto-reload
lumen-ai serve app.py --autoreload --show

# Specify port
lumen-ai serve app.py --port 5007

# Load dataset
lumen-ai serve app.py data/sales.csv
```

### Development Server Options

```bash
# Full development setup
panel serve app.py \
  --autoreload \
  --show \
  --port 5007 \
  --dev
```

**Options**:
- `--autoreload`: Reload on file changes
- `--show`: Open browser automatically
- `--port`: Specify port (default: 5006)
- `--dev`: Enable development mode with better error messages

## Production Deployment

### Basic Production Server

```bash
panel serve app.py \
  --port 80 \
  --address 0.0.0.0 \
  --num-procs 4 \
  --allow-websocket-origin=analytics.company.com
```

**Key options**:
- `--num-procs`: Number of worker processes
- `--address`: Bind to all interfaces (0.0.0.0)
- `--allow-websocket-origin`: Allowed domains

### With Authentication

```bash
panel serve app.py \
  --oauth-provider=generic \
  --oauth-key=${OAUTH_KEY} \
  --oauth-secret=${OAUTH_SECRET} \
  --oauth-redirect-uri=https://analytics.company.com/oauth-callback \
  --cookie-secret=${COOKIE_SECRET}
```

### With HTTPS

```bash
panel serve app.py \
  --ssl-certfile=/path/to/cert.pem \
  --ssl-keyfile=/path/to/key.pem \
  --port 443
```

### Behind Nginx Reverse Proxy

**Nginx configuration**:
```nginx
server {
    listen 80;
    server_name analytics.company.com;

    location / {
        proxy_pass http://localhost:5006;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Run application**:
```bash
panel serve app.py \
  --port 5006 \
  --num-procs 4 \
  --allow-websocket-origin=analytics.company.com
```

## Docker Deployment

### Basic Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .
COPY data/ ./data/
COPY docs/ ./docs/

# Expose port
EXPOSE 5006

# Run application
CMD ["panel", "serve", "app.py", \
     "--port", "5006", \
     "--address", "0.0.0.0", \
     "--num-procs", "2"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  lumen-ai:
    build: .
    ports:
      - "80:5006"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - DATABASE_URL=${DATABASE_URL}
      - LUMEN_TITLE=Analytics AI
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5006"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - lumen-ai
    restart: unless-stopped
```

### Build and Run

```bash
# Build image
docker build -t lumen-ai-app .

# Run container
docker run -d \
  --name lumen-ai \
  -p 80:5006 \
  -e ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY} \
  -v $(pwd)/data:/app/data \
  lumen-ai-app

# With docker-compose
docker-compose up -d
```

### Multi-Stage Build (Optimized)

```dockerfile
# Build stage
FROM python:3.11 as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application
COPY app.py .
COPY data/ ./data/

EXPOSE 5006
CMD ["panel", "serve", "app.py", "--port", "5006", "--address", "0.0.0.0"]
```

## Environment Configuration

### Environment Variables

```bash
# LLM Provider
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
MISTRAL_API_KEY=...

# Database
DATABASE_URL=postgresql://user:pass@host/db

# Application
LUMEN_TITLE="Analytics AI"
LUMEN_ACCENT_COLOR="#00aa41"
LOG_LEVEL=INFO

# Security
COOKIE_SECRET=generate-random-secret
OAUTH_KEY=...
OAUTH_SECRET=...
```

### Configuration File

```python
# config.py
import os
from typing import Dict, Any

def get_config() -> Dict[str, Any]:
    """Load configuration from environment."""
    env = os.getenv("ENVIRONMENT", "development")

    configs = {
        "development": {
            "llm_type": "openai",
            "model": "gpt-4o-mini",
            "debug": True,
            "autoreload": True
        },
        "production": {
            "llm_type": "anthropic",
            "model": "claude-3-5-sonnet-20241022",
            "debug": False,
            "num_procs": 4
        }
    }

    return configs.get(env, configs["development"])
```

### Load Configuration

```python
# app.py
import lumen.ai as lmai
from config import get_config

config = get_config()

# Apply LLM config
lmai.llm.llm_type = config["llm_type"]
lmai.llm.model = config["model"]

# Create UI
ui = lmai.ExplorerUI(...)
```

## Security Best Practices

### 1. Never Commit Secrets

```bash
# .gitignore
.env
secrets.yaml
*.key
*.pem
config/production.py
```

### 2. Use Environment Variables

```python
import os

# ✅ Good
lmai.llm.api_key = os.getenv("OPENAI_API_KEY")

# ❌ Bad
lmai.llm.api_key = "sk-..."
```

### 3. Implement Rate Limiting

```python
from panel.io.server import RateLimiter

# Limit requests per user
rate_limiter = RateLimiter(
    max_requests=100,
    window=60  # seconds
)
```

### 4. Row-Level Security

```sql
-- PostgreSQL RLS
ALTER TABLE sales ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_sales_policy ON sales
FOR SELECT
TO authenticated_user
USING (user_id = current_user_id());
```

### 5. Validate User Input

```python
class SecureAgent(Agent):
    async def respond(self, query: str):
        # Sanitize input
        query = self.sanitize(query)

        # Validate length
        if len(query) > 1000:
            yield "❌ Query too long"
            return

        # Process safely
        result = await self.process(query)
        yield result

    def sanitize(self, text: str) -> str:
        """Remove potentially dangerous content."""
        # Remove SQL injection attempts
        dangerous = ["DROP", "DELETE", "TRUNCATE", "ALTER"]
        for word in dangerous:
            text = text.replace(word, "")
        return text
```

### 6. Secure Headers

```python
# In Panel app
app = pn.template.FastListTemplate(...)

# Add security headers
app.config.headers = {
    "X-Frame-Options": "DENY",
    "X-Content-Type-Options": "nosniff",
    "Strict-Transport-Security": "max-age=31536000",
    "Content-Security-Policy": "default-src 'self'"
}
```

## Monitoring and Logging

### Application Logging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('lumen-ai.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class MonitoredAgent(Agent):
    async def respond(self, query: str):
        logger.info(f"Query received: {query}")

        try:
            result = await self.process(query)
            logger.info("Query processed successfully")
            yield result

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            yield "Error occurred"
```

### Performance Monitoring

```python
import time
from functools import wraps

def monitor_performance(func):
    """Decorator to monitor agent performance."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()

        result = await func(*args, **kwargs)

        duration = time.time() - start
        logger.info(f"{func.__name__} took {duration:.2f}s")

        return result
    return wrapper

class PerformantAgent(Agent):
    @monitor_performance
    async def respond(self, query: str):
        # Agent logic
        pass
```

### Health Checks

```python
import panel as pn

# Health check endpoint
def health_check():
    """Health check for load balancers."""
    return {"status": "healthy", "timestamp": str(datetime.now())}

# Add to Panel app
pn.state.add_periodic_callback(health_check, 30000)  # Every 30s
```

### Error Tracking

```python
# Integration with Sentry
import sentry_sdk

sentry_sdk.init(
    dsn="https://...@sentry.io/...",
    traces_sample_rate=0.1,
    environment=os.getenv("ENVIRONMENT", "development")
)

# Errors automatically tracked
```

## Scalability

### Horizontal Scaling

```yaml
# kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: lumen-ai
spec:
  replicas: 3
  selector:
    matchLabels:
      app: lumen-ai
  template:
    metadata:
      labels:
        app: lumen-ai
    spec:
      containers:
      - name: lumen-ai
        image: lumen-ai:latest
        ports:
        - containerPort: 5006
        env:
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: lumen-secrets
              key: api-key
---
apiVersion: v1
kind: Service
metadata:
  name: lumen-ai-service
spec:
  selector:
    app: lumen-ai
  ports:
  - port: 80
    targetPort: 5006
  type: LoadBalancer
```

### Load Balancing

```bash
# Multiple workers
panel serve app.py --num-procs 8

# Behind load balancer
# Use sticky sessions for WebSocket connections
```

### Caching Strategy

```python
from functools import lru_cache

class CachedAgent(Agent):
    @lru_cache(maxsize=100)
    def get_data(self, table: str):
        """Cache frequently accessed data."""
        return self.source.get(table)

    async def respond(self, query: str):
        # Use cached data
        data = self.get_data("sales")
        # Process...
```

## Troubleshooting

### Application Won't Start

```bash
# Check port availability
lsof -i :5006

# Check logs
tail -f lumen-ai.log

# Test configuration
python -c "import app; print('OK')"
```

### WebSocket Connection Issues

```nginx
# Ensure Nginx forwards WebSocket properly
proxy_http_version 1.1;
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "upgrade";
```

### Performance Issues

```python
# Profile slow agents
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Run agent
await agent.respond(query)

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)
```

## Related Resources

- [Security Best Practices](../best-practices.md#security)
- [Performance Optimization](../best-practices.md#performance)
- [Troubleshooting Guide](troubleshooting.md)

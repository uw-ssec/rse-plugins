# Lumen Deployment Guide

## Overview

Production deployment guide for Lumen dashboards including Docker, cloud platforms, and best practices.

**When to use this guide**:
- Deploying dashboards to production
- Containerizing with Docker
- Cloud deployment (AWS, GCP, Azure)
- Security and authentication setup

## Quick Start

### Local Development

```bash
# Development server with auto-reload
lumen serve dashboard.yaml --autoreload --show

# Specific port
lumen serve dashboard.yaml --port 5007
```

### Production Server

```bash
# Production with multiple processes
panel serve dashboard.yaml \
  --port 80 \
  --num-procs 4 \
  --allow-websocket-origin=dashboard.company.com
```

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY dashboard.yaml .
COPY data/ ./data/

# Expose port
EXPOSE 5006

# Run application
CMD ["lumen", "serve", "dashboard.yaml", \
     "--port", "5006", \
     "--address", "0.0.0.0"]
```

### requirements.txt

```
lumen>=0.10.0
panel>=1.3.0
holoviews>=1.18.0
pandas>=2.0.0
# Add your specific dependencies
psycopg2-binary  # For PostgreSQL
duckdb  # For DuckDB
```

### Build and Run

```bash
# Build image
docker build -t lumen-dashboard .

# Run container
docker run -p 5006:5006 \
  -e DATABASE_URL="postgresql://..." \
  lumen-dashboard
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  dashboard:
    build: .
    ports:
      - "5006:5006"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - API_KEY=${API_KEY}
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

## Cloud Deployment

### Heroku

```bash
# Create Procfile
echo "web: lumen serve dashboard.yaml --port $PORT --address 0.0.0.0" > Procfile

# Deploy
heroku create my-dashboard
git push heroku main
```

### AWS (ECS/Fargate)

1. Build and push Docker image to ECR
2. Create ECS task definition
3. Create ECS service with ALB

### Google Cloud Run

```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/lumen-dashboard

# Deploy
gcloud run deploy lumen-dashboard \
  --image gcr.io/PROJECT_ID/lumen-dashboard \
  --platform managed \
  --port 5006 \
  --allow-unauthenticated
```

### Azure Container Apps

```bash
# Create container app
az containerapp create \
  --name lumen-dashboard \
  --resource-group myResourceGroup \
  --image myregistry.azurecr.io/lumen-dashboard:latest \
  --target-port 5006 \
  --ingress external
```

## Security

### Environment Variables

```yaml
# dashboard.yaml
sources:
  database:
    type: postgres
    connection_string: ${DATABASE_URL}  # From environment

  api:
    type: rest
    url: ${API_URL}
    headers:
      Authorization: Bearer ${API_TOKEN}
```

```bash
# Set environment variables
export DATABASE_URL="postgresql://user:password@host/db"
export API_TOKEN="secret_token"
```

### Authentication

#### OAuth Authentication

```bash
# Serve with OAuth
lumen serve dashboard.yaml \
  --oauth-provider=generic \
  --oauth-key=${OAUTH_KEY} \
  --oauth-secret=${OAUTH_SECRET} \
  --oauth-redirect-uri=https://dashboard.com/oauth-callback
```

#### Basic Authentication

```python
# app.py
import panel as pn
from lumen.dashboard import Dashboard

pn.config.basic_auth = {
    'username': 'password',
    'admin': 'admin_password'
}

dashboard = Dashboard.from_spec('./dashboard.yaml')
dashboard.servable()
```

### HTTPS/SSL

```bash
# Nginx reverse proxy
server {
    listen 443 ssl;
    server_name dashboard.company.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:5006;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_http_version 1.1;
    }
}
```

## Performance Optimization

### Caching

```yaml
sources:
  cached_data:
    type: postgres
    connection_string: ${DATABASE_URL}
    cache: true
    cache_dir: ./cache
    cache_timeout: 3600  # 1 hour
```

### Connection Pooling

```yaml
sources:
  database:
    type: postgres
    connection_string: ${DATABASE_URL}
    pool_size: 10
    max_overflow: 20
```

### Multiple Processes

```bash
# Run with multiple worker processes
panel serve dashboard.yaml \
  --num-procs 4 \
  --port 80
```

## Monitoring

### Health Check Endpoint

```python
# health.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

### Logging

```python
# Configure logging
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dashboard.log'),
        logging.StreamHandler()
    ]
)
```

### Metrics

```bash
# Enable Panel telemetry
panel serve dashboard.yaml \
  --profiler=pyinstrument \
  --log-level=info
```

## Best Practices

### 1. Use Environment Variables

```yaml
# ✅ Good: Environment variables for secrets
sources:
  db:
    connection_string: ${DATABASE_URL}

# ❌ Bad: Hardcoded credentials
sources:
  db:
    connection_string: postgresql://user:password@host/db
```

### 2. Enable Caching

```yaml
# ✅ Good: Cache expensive queries
sources:
  data:
    type: postgres
    cache: true
    cache_timeout: 3600
```

### 3. Health Checks

```dockerfile
# ✅ Good: Docker health check
HEALTHCHECK CMD curl --fail http://localhost:5006/health || exit 1
```

### 4. Resource Limits

```yaml
# docker-compose.yml
services:
  dashboard:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port
lsof -i :5006

# Kill process
kill -9 PID
```

### WebSocket Connection Issues

```bash
# Ensure WebSocket origin allowed
panel serve dashboard.yaml \
  --allow-websocket-origin=dashboard.company.com \
  --allow-websocket-origin=www.dashboard.company.com
```

### Memory Issues

```python
# Limit data in pipeline
transforms:
  - type: head
    n: 100000  # Limit rows
```

## Summary

**Key concepts**:
- Use Docker for containerization
- Deploy to cloud platforms (AWS, GCP, Azure, Heroku)
- Secure with authentication and HTTPS
- Optimize with caching and connection pooling
- Monitor with logging and health checks

**Deployment checklist**:
- [ ] Environment variables for secrets
- [ ] Docker containerization
- [ ] HTTPS/SSL enabled
- [ ] Authentication configured
- [ ] Caching enabled
- [ ] Health checks implemented
- [ ] Logging configured
- [ ] Resource limits set
- [ ] Monitoring in place

## References

- [Panel Deployment Guide](https://panel.holoviz.org/user_guide/Deploy.html)
- [Docker Documentation](https://docs.docker.com/)
- [Heroku Python Guide](https://devcenter.heroku.com/articles/python-gunicorn)
- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)

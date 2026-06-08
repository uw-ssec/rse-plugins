# Registry Operations -- Auth, Validation, and Retention

## CI Authentication Patterns

Use short-lived credentials where possible.

### GHCR (same repository)

```yaml
permissions:
  contents: read
  packages: write

steps:
  - uses: docker/login-action@v3
    with:
      registry: ghcr.io
      username: ${{ github.actor }}
      password: ${{ secrets.GITHUB_TOKEN }}
```

### Docker Hub

```yaml
- uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}
```

### AWS ECR (OIDC)

```yaml
permissions:
  id-token: write
  contents: read

steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789012:role/gha-ecr-push
      aws-region: us-east-1
  - uses: aws-actions/amazon-ecr-login@v2
```

### Azure ACR (OIDC)

```yaml
permissions:
  id-token: write
  contents: read

steps:
  - uses: azure/login@v2
    with:
      client-id: ${{ secrets.AZURE_CLIENT_ID }}
      tenant-id: ${{ secrets.AZURE_TENANT_ID }}
      subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
  - uses: azure/docker-login@v2
    with:
      login-server: myregistry.azurecr.io
```

## Post-Publish Validation Commands

Run these checks after push:

```bash
# Verify tag exists remotely
docker buildx imagetools inspect ghcr.io/myorg/myapp:v1.2.3

# Verify manifest contains expected platforms
docker manifest inspect ghcr.io/myorg/myapp:v1.2.3

# Smoke pull
docker pull ghcr.io/myorg/myapp:v1.2.3
```

## Failure Recovery Playbook

1. **Auth failure (401/403):** confirm token scope or OIDC role permissions.
2. **Push denied:** verify repository/package exists and target namespace is correct.
3. **Missing tags:** inspect `docker/metadata-action` outputs in CI logs.
4. **Multi-arch incomplete:** rebuild and re-run manifest inspection.
5. **Flaky build cache:** retry once with no cache for the failing target.

## Retention and Cleanup

### GHCR cleanup

```yaml
- uses: actions/delete-package-versions@v5
  with:
    package-name: myapp
    package-type: container
    min-versions-to-keep: 10
    delete-only-untagged-versions: true
```

### ECR lifecycle policy

```json
{
  "rules": [
    {
      "rulePriority": 1,
      "selection": {
        "tagStatus": "untagged",
        "countType": "sinceImagePushed",
        "countUnit": "days",
        "countNumber": 30
      },
      "action": { "type": "expire" }
    }
  ]
}
```

### ACR retention

```bash
az acr config retention update --registry myregistry --status Enabled --days 30 --type UntaggedManifests
```

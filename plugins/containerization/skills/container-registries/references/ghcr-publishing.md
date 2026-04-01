# GHCR Publishing -- Deep Reference

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| GHCR Setup | 17-63 | Enabling GHCR, image naming, initial configuration |
| PAT vs GITHUB_TOKEN | 65-134 | Authentication methods, scopes, when to use each |
| Visibility Settings | 136-175 | Public vs private packages, inheritance, changing visibility |
| Org-Level Packages | 177-232 | Organization package management, permissions, teams |
| Linking to Repos | 234-285 | OCI labels, automatic linking, manual linking in UI |
| Cleanup Actions | 287-378 | Deleting old versions, retention policies, scheduled cleanup |
| OCI Artifacts | 380-427 | Storing Helm charts, SBOMs, signatures alongside images |

---

## GHCR Setup

### Enabling GHCR

GitHub Container Registry is enabled by default for all GitHub accounts (personal and organization). No additional setup is required to start pushing images.

Images are published under the pattern:

```
ghcr.io/<owner>/<image>:<tag>
```

Where `<owner>` is your GitHub username or organization name.

### First Push

To push your first image:

```bash
# Build the image
docker build -t ghcr.io/myuser/myapp:v1.0.0 .

# Authenticate
echo "$GITHUB_TOKEN" | docker login ghcr.io -u myuser --password-stdin

# Push
docker push ghcr.io/myuser/myapp:v1.0.0
```

The package is created automatically on first push. You do not need to create it in the GitHub UI beforehand.

### Image Naming Rules

- Image names must be lowercase
- Image names can contain letters, digits, hyphens, periods, and underscores
- Maximum length is 128 characters for the full path
- Nested paths are supported: `ghcr.io/myorg/project/subcomponent:tag`

### Storage and Bandwidth

- Public packages: free, unlimited bandwidth
- Private packages: count against your GitHub storage quota (shared with GitHub Actions artifacts)
- GitHub Free: 500 MB storage, 1 GB bandwidth/month for private packages
- GitHub Pro/Team: higher limits included
- GitHub Enterprise: configurable limits

---

## PAT vs GITHUB_TOKEN

### GITHUB_TOKEN (Recommended for GitHub Actions)

The `GITHUB_TOKEN` is automatically generated for each GitHub Actions workflow run. It requires no manual secret configuration and is scoped to the repository.

```yaml
permissions:
  packages: write
  contents: read

steps:
  - uses: docker/login-action@v3
    with:
      registry: ghcr.io
      username: ${{ github.actor }}
      password: ${{ secrets.GITHUB_TOKEN }}
```

**Permissions required:**
- `packages: write` -- to push images
- `packages: read` -- to pull private images
- `contents: read` -- to checkout code (standard)

**Limitations of GITHUB_TOKEN:**
- Cannot access packages in other repositories
- Cannot delete package versions (requires PAT or API)
- Cannot manage package settings (visibility, access)
- Scoped to the single workflow run

### Personal Access Token (PAT)

Use a PAT when you need cross-repository access, local development pushes, or package management operations.

**Classic PAT scopes:**
- `read:packages` -- pull images
- `write:packages` -- push images
- `delete:packages` -- delete image versions

**Fine-grained PAT permissions:**
- Packages: Read, Write, or Admin

```bash
# Local development with PAT
echo "$PAT" | docker login ghcr.io -u myuser --password-stdin
docker push ghcr.io/myuser/myapp:dev
```

### When to Use Each

| Scenario | Authentication |
|----------|---------------|
| GitHub Actions (same repo) | `GITHUB_TOKEN` |
| GitHub Actions (cross-repo) | Fine-grained PAT stored as secret |
| Local development | PAT or `gh auth token` |
| CI outside GitHub (Jenkins, CircleCI) | PAT stored as CI secret |
| Package deletion | PAT with `delete:packages` scope |
| Automated cleanup | PAT or GitHub App token |

### Using gh CLI for Authentication

```bash
# Login with gh CLI (interactive)
gh auth login --scopes packages:write

# Use gh token for Docker login
echo "$(gh auth token)" | docker login ghcr.io -u $(gh api user --jq .login) --password-stdin
```

---

## Visibility Settings

### Default Visibility

New packages inherit visibility from the repository they are linked to:
- Public repository -> public package
- Private repository -> private package
- No linked repository -> private package

### Changing Visibility

**In the GitHub UI:**
1. Navigate to your profile or organization
2. Go to Packages tab
3. Select the package
4. Settings > Change visibility

**Via API:**
```bash
# Not directly available via REST API for containers
# Use the GitHub UI or GitHub CLI
gh api orgs/myorg/packages/container/myapp -X PATCH \
  --field visibility=public
```

### Visibility Rules

- Public packages can be pulled by anyone without authentication
- Private packages require authentication with appropriate permissions
- Changing a public package to private does not revoke existing pulls but prevents new unauthenticated access
- Organization packages respect team permissions

### Public Package Benefits

- No pull rate limits
- No bandwidth charges
- Discoverable in GitHub search
- Anyone can use the image without authentication

---

## Org-Level Packages

### Organization Package Management

Organization administrators can manage packages across the organization:

```bash
# List all packages in an organization
gh api orgs/myorg/packages?package_type=container --paginate \
  --jq '.[].name'

# View package versions
gh api orgs/myorg/packages/container/myapp/versions --paginate \
  --jq '.[] | "\(.id) \(.metadata.container.tags | join(","))"'
```

### Team Permissions

Grant teams access to packages:

1. Navigate to the package settings
2. Under "Manage access", add teams
3. Assign role: Read, Write, or Admin

**Role capabilities:**

| Role | Pull | Push | Delete | Settings |
|------|------|------|--------|----------|
| Read | Yes | No | No | No |
| Write | Yes | Yes | No | No |
| Admin | Yes | Yes | Yes | Yes |

### Repository Connection

Packages can be connected to repositories, which:
- Inherits the repository's visibility by default
- Shows the package in the repository's Packages sidebar
- Allows `GITHUB_TOKEN` from that repository to push/pull

```yaml
# In your workflow, GITHUB_TOKEN can push to packages connected to the repo
- uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
```

### Organization Policies

Organization owners can configure:
- Default package visibility for new packages
- Which teams can create packages
- Package creation permissions for organization members

---

## Linking to Repos

### Automatic Linking via OCI Labels

The recommended way to link a GHCR image to its source repository is with OCI labels in the Dockerfile:

```dockerfile
LABEL org.opencontainers.image.source="https://github.com/myorg/myrepo"
LABEL org.opencontainers.image.description="My application"
LABEL org.opencontainers.image.licenses="MIT"
```

When you push an image with this label, GHCR automatically links it to the specified repository. This enables:
- The package appears in the repository's "Packages" sidebar
- `GITHUB_TOKEN` from that repository can push/pull
- Repository visibility is inherited by default

### Using docker/metadata-action

The `docker/metadata-action` automatically generates OCI labels from your repository metadata:

```yaml
- uses: docker/metadata-action@v5
  id: meta
  with:
    images: ghcr.io/${{ github.repository }}
    labels: |
      org.opencontainers.image.title=My App
      org.opencontainers.image.description=Description here

- uses: docker/build-push-action@v6
  with:
    push: true
    tags: ${{ steps.meta.outputs.tags }}
    labels: ${{ steps.meta.outputs.labels }}
```

This action automatically sets `org.opencontainers.image.source` to the repository URL.

### Manual Linking in the UI

If an image was pushed without the source label:
1. Go to your profile or organization > Packages
2. Select the package
3. Settings > "Connect a repository"
4. Search for and select the repository

### Multiple Repositories

A single package can only be linked to one repository. If you need to publish images from multiple repositories to the same package, designate one as the primary source and use PATs for cross-repo pushes.

---

## Cleanup Actions

### Why Cleanup Matters

Active projects can generate hundreds of image versions. Untagged images (manifests without tags) accumulate from superseded builds and consume storage.

### actions/delete-package-versions

The official action for cleaning up package versions:

```yaml
name: Cleanup old container images
on:
  schedule:
    - cron: '0 2 * * 0'  # Weekly on Sunday at 2 AM

jobs:
  cleanup:
    runs-on: ubuntu-latest
    permissions:
      packages: write
    steps:
      - uses: actions/delete-package-versions@v5
        with:
          package-name: myapp
          package-type: container
          min-versions-to-keep: 10
          delete-only-untagged-versions: true
```

### Advanced Cleanup with the API

For more control, use the GitHub API directly:

```bash
# List all versions (including untagged)
gh api orgs/myorg/packages/container/myapp/versions --paginate \
  --jq '.[] | select(.metadata.container.tags | length == 0) | .id'

# Delete a specific version
gh api orgs/myorg/packages/container/myapp/versions/12345 -X DELETE
```

### Cleanup Strategies

**Keep N most recent tagged versions:**
```yaml
- uses: actions/delete-package-versions@v5
  with:
    package-name: myapp
    package-type: container
    min-versions-to-keep: 20
```

**Delete untagged only (safest):**
```yaml
- uses: actions/delete-package-versions@v5
  with:
    package-name: myapp
    package-type: container
    delete-only-untagged-versions: true
    min-versions-to-keep: 5
```

**Delete versions older than N days:**
```yaml
- uses: actions/delete-package-versions@v5
  with:
    package-name: myapp
    package-type: container
    min-versions-to-keep: 5
    delete-only-pre-release-versions: true
```

### Third-Party Cleanup Tools

- **ghcr-cleanup-action**: More granular filtering by tag pattern, age, and keep patterns
- **container-retention-policy**: Policy-based cleanup with dry-run support

```yaml
# Example: ghcr-cleanup-action with tag filtering
- uses: vlaurin/action-ghcr-prune@v0.6.0
  with:
    token: ${{ secrets.PAT }}
    organization: myorg
    container: myapp
    keep-younger-than: 30  # days
    keep-tags-regexes: '^v\d+\.\d+\.\d+$'  # keep semver tags
    prune-untagged: true
```

---

## OCI Artifacts

### Beyond Container Images

GHCR supports OCI artifacts, which means you can store more than just container images. Any OCI-compliant artifact can be pushed, including:

- **Helm charts**: Package and distribute Helm charts via GHCR
- **SBOMs**: Attach Software Bill of Materials to images
- **Signatures**: Store cosign signatures alongside images
- **WASM modules**: Distribute WebAssembly modules
- **Custom artifacts**: Any file packaged as an OCI artifact

### Pushing Helm Charts

```bash
# Package the chart
helm package mychart/

# Push to GHCR
helm push mychart-1.0.0.tgz oci://ghcr.io/myorg/charts

# Pull from GHCR
helm pull oci://ghcr.io/myorg/charts/mychart --version 1.0.0
```

### Attaching SBOMs

```bash
# Generate SBOM with syft
syft ghcr.io/myorg/myapp:v1.0.0 -o spdx-json > sbom.spdx.json

# Attach SBOM to the image using cosign
cosign attach sbom --sbom sbom.spdx.json ghcr.io/myorg/myapp:v1.0.0

# Or use ORAS to push as a separate artifact
oras push ghcr.io/myorg/myapp:v1.0.0-sbom \
  --artifact-type application/spdx+json \
  sbom.spdx.json
```

### Attaching Signatures

```bash
# Sign with cosign (keyless)
cosign sign ghcr.io/myorg/myapp@sha256:abc123...

# The signature is stored as a separate OCI artifact in the same repository
# Verify
cosign verify ghcr.io/myorg/myapp:v1.0.0
```

### ORAS (OCI Registry As Storage)

ORAS is a general-purpose tool for pushing any file to an OCI registry:

```bash
# Install ORAS
brew install oras

# Push a file
oras push ghcr.io/myorg/artifacts/mydata:v1.0.0 \
  --artifact-type application/vnd.myorg.data \
  data.tar.gz

# Pull a file
oras pull ghcr.io/myorg/artifacts/mydata:v1.0.0
```

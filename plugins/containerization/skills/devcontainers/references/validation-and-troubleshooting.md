# Validation and Troubleshooting -- Dev Containers

## Validation Workflow

Use this sequence after creating or editing `.devcontainer/devcontainer.json`:

1. **Validate build**

```bash
devcontainer build --workspace-folder .
```

2. **Open/rebuild in editor**

- VS Code: "Dev Containers: Rebuild and Reopen in Container"

3. **Verify lifecycle hooks**

- Confirm `postCreateCommand` succeeds on first create.
- Confirm `postStartCommand` runs on restart.

4. **Verify extensions and settings**

- Confirm required extensions are installed.
- Confirm key settings apply in the container session.

5. **Verify service connectivity (if Compose)**

```bash
docker compose ps
docker compose logs -f <service>
```

6. **Fix and rebuild**

- If any check fails, update config and repeat from step 1.

## Common Failure Patterns

1. **Build fails on missing system packages**
   - Fix Dockerfile/feature configuration and rebuild.
2. **Dependencies not installed**
   - Move setup to `postCreateCommand` or fix command path.
3. **Port not reachable**
   - Add `forwardPorts` entry and rebuild.
4. **Permission errors on mounted workspace**
   - Set `remoteUser` appropriately and align UID/GID strategy.
5. **GPU unavailable**
   - Confirm host toolkit/driver setup and `runArgs`/feature configuration.

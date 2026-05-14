---
description: Check lockfile health across all detected ecosystems (npm, PyPI, conda/pixi, cargo, Go). Verifies committed status, CI usage, hash pinning, floating versions, and cooldown discipline. Narrower than /supply-chain-audit. Read-only.
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# Supply Chain Lockfile Check

Focused, per-ecosystem lockfile health check — verifies that every detected ecosystem has a committed lockfile, that CI installs from it, that hashes are pinned where supported, and that updates respect cooldown discipline.

## Arguments

`$ARGUMENTS` — Optional path to a project directory. Defaults to the current working directory.

## Detected Lockfiles

| Lockfile | Ecosystem | CI invocation |
|----------|-----------|---------------|
| `package-lock.json` | npm | `npm ci` |
| `yarn.lock` | yarn | `yarn install --frozen-lockfile` |
| `pnpm-lock.yaml` | pnpm | `pnpm install --frozen-lockfile` |
| `uv.lock` | uv | `uv sync --frozen` |
| `poetry.lock` | poetry | `poetry install --no-update` |
| `pixi.lock` | pixi | `pixi install` |
| `conda-lock.yml` | conda | `conda-lock install` |
| `Cargo.lock` | cargo | `cargo build --locked` |
| `go.sum` | Go | `go mod download` (with `GOFLAGS=-mod=readonly`) |

## Per-Lockfile Checks

For each detected lockfile, evaluate:

1. **Committed** — file is tracked in git.
   ```bash
   git ls-files | grep <lockfile>
   ```
2. **Used in CI** — at least one workflow invokes the lockfile-respecting install command.
   ```bash
   grep -rnE '<install-command>' .github/workflows/
   ```
3. **Hash-pinned** — where the lockfile format supports it, hashes are present (npm `integrity:`, uv `hashes`, Cargo `checksum`).
4. **No floating versions in source manifest** — e.g., `package.json` has no `*` or `latest`; `pyproject.toml` has no unbounded `>=` without an upper bound; `Cargo.toml` uses precise version requirements.
5. **Cooldown discipline** — lockfile commits should be spaced (recommendation: ≥7 days between bulk updates) to allow community detection of compromised releases.
   ```bash
   git log --follow --pretty=format:"%h %ai" <lockfile> | head -20
   ```

## Output

```markdown
## Lockfile Check Report: <path>

### Detected Ecosystems
- <ecosystem>: <lockfile path>

### Per-Lockfile Health

#### <lockfile>

| Criterion | PASS/WARN/FAIL | Evidence |
|-----------|----------------|----------|
| Committed | ... | ... |
| Used in CI | ... | <workflow file:line referencing the install command> |
| Hash-pinned | ... | ... |
| No floating versions | ... | ... |
| Cooldown discipline | ... | <last 5 lockfile commits with timestamps> |

### Recommended Actions
- <fix>: <command or skill reference>
```

## Important Notes

- **Read-only**: this command does not modify lockfiles or workflows.
- For broader supply-chain posture (action pinning, permissions, provenance), run `/supply-chain-audit`.
- For incident-specific lockfile triage (a particular CVE or compromised package), run `/supply-chain-incident <advisory>`.
- Cooldown discipline is a heuristic — emergency security updates are an exception, not a violation.

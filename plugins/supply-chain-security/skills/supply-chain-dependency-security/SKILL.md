---
name: supply-chain-dependency-security
description: Dependency and lockfile supply-chain security review with 2025–2026 attack campaign patterns. Use when reviewing package.json, pyproject.toml, requirements.txt, pixi.toml, conda-lock.yml, or any lockfile; when evaluating a new dependency for addition; or when responding to a supply-chain compromise incident. Contains patterns for detecting maintainer-account-takeover style attacks that CVE scanners miss.
---

# Supply Chain Dependency Security

## Threat Model (2025–2026)

The dominant supply-chain threat is **maintainer account takeover of legitimate, widely-trusted packages** — not typosquatting. Your CVE scanner will not catch these.

Active campaigns:
- **Shai-Hulud**: 500+ npm packages compromised via maintainer account takeover
- **TeamPCP**: Trivy, Checkmarx, LiteLLM, Bitwarden CLI, SAP CAP — targeted at security tooling
- **axios**: 100M weekly downloads; compromise via release tag hijack
- **LiteLLM 1.82.8**: malicious `.pth` file injected for persistent execution on every Python startup

## Review Checklist

### Lockfiles

- [ ] Lockfile committed (`package-lock.json`, `yarn.lock`, `poetry.lock`, `uv.lock`, `pixi.lock`, `conda-lock.yml`)
- [ ] Lockfile is used in CI (`npm ci`, `pip install --require-hashes`, `uv sync --frozen`, `pixi install`)
- [ ] No floating version specs in production paths (e.g., `*`, `>=x` without upper bound in lockfile-less environments)

### Install-time script execution

- [ ] `npm ci --ignore-scripts` (or `ignore-scripts=true` in `.npmrc`) in all CI environments
- [ ] `preinstall`/`postinstall` hooks are the dominant execution vector — verify no hooks run untrusted code
- [ ] Python: check for unexpected `.pth` files that execute on every interpreter start:
  ```bash
  find $(python -c "import site; print(site.getsitepackages()[0])") -name "*.pth"
  ```

### Dependency freshness and cooldown

- [ ] New dependencies are held for ≥7 days before merging — most malicious releases are yanked within hours
- [ ] Version pins in lockfile match expected package metadata (author, homepage, hash)
- [ ] No unpinned `latest` or `*` in production dependency specs

### Incident response

When a compromise is reported:
1. Identify affected version range from the advisory
2. Check if that version range is in the lockfile
3. Check if the install was cached (CI cache may still contain the compromised version)
4. Rotate any secrets or tokens accessible from the CI environment where the package ran
5. Check for persistence artifacts: `.pth` files, `postinstall` side effects, modified `node_modules/.bin/`

## Findings format

Name the vulnerability class, cite the package name + version + advisory or campaign name, state blast radius (what can the package access at install time), and propose the fix (version pin, lockfile update, `--ignore-scripts`).

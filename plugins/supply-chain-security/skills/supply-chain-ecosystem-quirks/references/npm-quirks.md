# npm / yarn / pnpm Supply Chain Quirks

## Threat Relevance

npm's install-time script execution is the single most-exploited supply-chain vector in the JavaScript ecosystem. The Shai-Hulud worm propagates via `postinstall` scripts; the `ua-parser-js`, `coa`, and `rc` compromises all executed payloads at `npm install` time before any project code ran. Yarn classic shares this default; only `pnpm` (since v7) and `yarn berry` (Plug'n'Play mode) ship safer defaults. Lockfile discipline, registry-proxy config, and provenance attestations are the other config knobs that decide whether the general "pin and scan" advice from `supply-chain-dependency-security` actually holds for a Node project.

## Install-Time Script Execution

Every `npm install` runs `preinstall`, `install`, and `postinstall` scripts from every dependency, transitively. This is the Shai-Hulud landing zone.

Disable globally via `.npmrc`:

```bash
echo "ignore-scripts=true" >> .npmrc
grep -q 'ignore-scripts=true' .npmrc && echo "PASS: scripts disabled"
```

Or per-command in CI:

```bash
npm ci --ignore-scripts
```

`pnpm` v7+ disables lifecycle scripts for non-allowlisted packages by default — see `pnpm.onlyBuiltDependencies` in `package.json`. `yarn berry` (v2+) with PnP mode does not run install scripts unless explicitly enabled via `enableScripts: true` in `.yarnrc.yml`. Call this out when recommending a package manager: switching from npm to pnpm reduces this attack surface without code changes.

## .npmrc Knobs That Affect Security

Audit `.npmrc` (project root and `~/.npmrc`) for these settings. Each line below is the desired state plus the verifying command.

- `package-lock=true` — always commit the lockfile.
  `grep -q 'package-lock=true' .npmrc || echo "WARN: package-lock not pinned"`
- `audit-level=high` or `critical` — fail `npm audit` on real issues only.
  `grep -E 'audit-level=(high|critical)' .npmrc`
- `fund=false` — suppresses funding-prompt noise that hides real warnings.
  `grep -q 'fund=false' .npmrc`
- `save-exact=true` — defaults installs to exact versions instead of `^x.y.z` ranges.
  `grep -q 'save-exact=true' .npmrc`
- `engine-strict=true` — refuses installs on the wrong Node version.
  `grep -q 'engine-strict=true' .npmrc`

## npm ci vs npm install

`npm ci` requires `package-lock.json` to exist and refuses to modify it; it deletes `node_modules/` first and installs exactly what the lock specifies. `npm install` will silently rewrite the lockfile to match new ranges in `package.json` if it finds satisfying versions. In CI, always use `npm ci`. The failure mode if you don't:

```bash
# in CI, this silently upgrades patches across the dep tree
npm install        # BAD: rewrites package-lock.json, defeats pin discipline
npm ci             # GOOD: respects the lockfile, fails if lock is out of sync
```

Verify CI uses `npm ci`: `grep -rE 'npm (install|ci)' .github/workflows/ | grep -v 'npm ci'`.

## npm Provenance Attestations

`npm publish --provenance` (npm v9.5+) generates a Sigstore attestation tied to the GitHub Actions workflow that built the package. The attestation is uploaded to the public Sigstore Rekor log and displayed on the npm registry page.

```bash
# In a publish job with permissions: id-token: write
npm publish --provenance --access public
```

Verify a consumed package:

```bash
npm audit signatures
```

Cross-link: see `supply-chain-sbom-provenance` for the full Sigstore/SLSA story and `references/sigstore-cookbook.md` in that skill for the `permissions:` block.

## pnpm and Yarn Berry Specifics

`pnpm` uses a content-addressable store with symlinks — no flat `node_modules/`, and each package only sees its direct deps. This kills the implicit-dependency attack class (a transitive can't be `require()`'d unless declared). Lifecycle scripts gated by `pnpm.onlyBuiltDependencies` in `package.json`:

```json
{ "pnpm": { "onlyBuiltDependencies": ["esbuild", "sharp"] } }
```

`yarn berry` (v2+) PnP mode replaces `node_modules/` with a `.pnp.cjs` resolver file. No filesystem dependency tree means no install scripts can write to it. Switch via `yarn set version berry && yarn config set nodeLinker pnp`.

Both options reduce install-time-script attack surface versus npm classic — recommend either when the project is willing to migrate.

## References

- npm docs: <https://docs.npmjs.com/cli/v10/configuring-npm/npmrc>
- npm provenance: <https://docs.npmjs.com/generating-provenance-statements>
- pnpm onlyBuiltDependencies: <https://pnpm.io/package_json#pnpmonlybuiltdependencies>
- Shai-Hulud writeup: cross-link to `supply-chain-threat-awareness`

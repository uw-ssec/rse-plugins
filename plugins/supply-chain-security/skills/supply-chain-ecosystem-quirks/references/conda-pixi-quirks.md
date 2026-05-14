# conda / pixi Supply Chain Quirks

## Threat Relevance

The conda ecosystem covers compiled scientific software (CUDA, GDAL, BLAS, etc.) that PyPI wheels often can't provide reproducibly. But conda's trust model is fundamentally different from npm/PyPI: there is no cryptographic package signing in mainstream use as of 2026 — trust is derived from channel reputation. That makes channel discipline, lockfile use, and the install escape hatches (`--no-deps`, `--no-pin`, `--force-reinstall`) the primary supply-chain controls. The general "verify signatures" advice from `supply-chain-sbom-provenance` does not apply to conda packages; document this gap for stakeholders.

## Channel Priority and the defaults Channel Risk

`conda-forge` is the community-governed channel with reviewer-gated PRs and reproducible recipes. `defaults` (Anaconda Inc.) has different governance, different versions, and as of 2024 a commercial license for orgs above a revenue threshold. Pixi defaults to `conda-forge`; classic conda defaults to `defaults` first.

Audit `.condarc` or `pixi.toml`:

```bash
conda config --show channels
grep -A 5 '^channels:' .condarc pixi.toml 2>/dev/null
```

If `defaults` is at the top of the channel list, evaluate whether the project can switch to conda-forge-only:

```bash
conda config --remove channels defaults
conda config --add channels conda-forge
conda config --set channel_priority strict
```

`channel_priority: strict` prevents conda from satisfying a package from a lower-priority channel when a higher-priority channel has it — closes the dependency-confusion-style attack where a name-squat on a lower channel substitutes for a trusted package.

## pixi.lock vs conda-lock.yml

`pixi` produces a single multi-platform `pixi.lock` (one file, one or more platforms encoded inside). `conda-lock` is the legacy tool, producing one `conda-<platform>.lock` per platform. Both encode exact package URLs and `md5`/`sha256` hashes; both should be committed.

Lockfile-respecting installs (CI):

```bash
pixi install --frozen        # fails if pixi.lock is out of sync with pixi.toml
conda-lock install --name <env> conda-linux-64.lock
```

`pixi install` (no flag) updates `pixi.lock` if `pixi.toml` changed. Use `--frozen` in CI to refuse silent updates.

## --no-deps and --no-pin (Escape Hatches)

These flags bypass solver constraints and lockfiles. Any of them in CI scripts is a P1 finding.

```bash
grep -rE '(--no-deps|--no-pin|--force-reinstall|--no-update-deps)' \
  .github/workflows/ Makefile *.sh *.yml 2>/dev/null
```

Legitimate uses are rare — usually a workaround for an unsolvable env. If found, replace with a pinned, lockfile-driven recipe or document the exception in the project README with a justification.

## Signed Channel Verification (the Gap)

As of 2026, conda-forge packages are not cryptographically signed. There is an experimental conda-content-trust system using TUF, but it is not on by default and not used by the major channels. The trust chain is:

- HTTPS to the channel (transport integrity only)
- Channel's own review process (conda-forge requires PR review, defaults is opaque)
- Per-package `md5`/`sha256` recorded in repodata (channel-attested, not third-party-signed)

This is a real gap versus npm provenance and PyPI's Sigstore. Document it for stakeholders rather than papering over: there is no `cosign verify` equivalent for conda packages today. Mitigations are channel discipline (above), lockfile pinning, and SBOM generation post-install via `syft <env-path>`.

## pixi run / conda run Sandbox Status

`pixi run <cmd>` and `conda run -n <env> <cmd>` activate the env and execute the command. Neither sandboxes the command — the script has the same filesystem and network access as the shell. Treat any `pixi run` / `conda run` line in CI the same way you'd treat a raw `bash -c` — the env-activation indirection does not add security.

Audit:

```bash
grep -rE '(pixi run|conda run)' .github/workflows/ 2>/dev/null
```

Cross-link to `supply-chain-hardened-ci-cd` for the broader "treat all CI commands as untrusted code execution" pattern.

## References

- conda-content-trust (experimental): <https://github.com/conda/conda-content-trust>
- pixi lockfile: <https://pixi.sh/latest/features/lockfile/>
- conda-forge governance: <https://conda-forge.org/docs/orga/governance/>
- channel priority semantics: <https://conda.io/projects/conda/en/latest/user-guide/concepts/installing-with-conda.html#strict-channel-priority>

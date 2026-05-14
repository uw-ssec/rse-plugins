# PyPI / pip / uv / poetry Supply Chain Quirks

## Threat Relevance

Python's packaging history has accumulated several arbitrary-code-execution surfaces that don't exist in other ecosystems: `.pth` files run at every interpreter start, `setup.py` runs at install for source distributions, custom `build_wheel` backends run in build-isolated subprocesses, and `--no-build-isolation` removes the isolation. LiteLLM 1.82.8 exploited `.pth` execution; PyTorch nightly compromises came through `setup.py`. The general "pin to lockfile and scan" pattern from `supply-chain-dependency-security` doesn't help if the install step itself runs adversary-controlled Python.

## .pth Files (LiteLLM 1.82.8 Vector)

A `.pth` file in `site-packages/` is normally a list of directory paths, one per line, that Python adds to `sys.path` at startup via `site.addsitedir`. But Python's `site` module also executes any line that starts with `import` or `exec`. A malicious package that drops a single `.pth` file gets persistent, every-interpreter-start code execution — no `import` of the package required.

Detect rogue `.pth` files:

```bash
find $(python -c "import site; print(site.getsitepackages()[0])") \
  -name "*.pth" -exec grep -lE '^(import|exec|os\.|subprocess)' {} \;
```

A legitimate `.pth` file looks like `./relative/path/to/module`. Anything matching the regex above is executing code at interpreter start. Investigate every match.

## setup.py Execution at Install

Legacy sdist packages execute `setup.py` (arbitrary Python) at install time. PEP 517 build isolation runs this in a temporary venv, which limits some damage but still grants the script full filesystem read, outbound network, and write to the build temp dir. Wheel installs skip this — wheels are pre-built artifacts.

Force the source path (and trigger `setup.py`):

```bash
pip install --no-binary <pkg> <pkg>   # forces source build, runs setup.py
```

Prefer wheels in CI and lockfiles:

```bash
pip install --only-binary :all: -r requirements.txt
```

If a package has no wheels for your platform, audit its `setup.py` before installing, or build the wheel once in a sandboxed environment and host it on an internal index.

## build_wheel and backend-path in pyproject.toml

PEP 517 lets a project declare a custom build backend in `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"
# or, dangerously:
backend-path = ["./_custom_build"]   # backend is project-supplied code
```

A `backend-path` pointing to project code means installing the package executes that project-supplied backend in an isolated env. `pip install --no-build-isolation` removes the isolation, putting the backend's code in the user's Python.

Audit:

```bash
grep -E '^(build-backend|backend-path)' pyproject.toml
grep -rE 'no-build-isolation' .github/workflows/ Makefile *.sh 2>/dev/null
```

Flag any `--no-build-isolation` in CI and any non-standard `build-backend`.

## OIDC Trusted Publishing for PyPI

The modern way to publish to PyPI from GitHub Actions — no long-lived API tokens.

Setup steps:

1. On <https://pypi.org/manage/account/publishing/>, register a trusted publisher: owner, repo, workflow filename, environment (optional but recommended).
2. In the publish workflow, grant `id-token: write` and use the official action:

```yaml
permissions:
  id-token: write
jobs:
  release:
    environment: pypi
    steps:
      - uses: pypa/gh-action-pypi-publish@release/v1
```

3. No `PYPI_API_TOKEN` secret. PyPI verifies the GitHub OIDC token against the trusted-publisher record at upload time.

Cross-link: `supply-chain-hardened-ci-cd` for the broader OIDC + permissions story; `supply-chain-sbom-provenance` for PyPI's automatic Sigstore attestation on OIDC uploads.

## uv and poetry Lockfile Differences

`uv.lock` (uv v0.4+) is a TOML lockfile with per-package hashes and platform markers. `poetry.lock` is a TOML lockfile with hashes. Both must be committed.

Lockfile-respecting installs (CI):

```bash
uv sync --frozen           # uv: fail if lockfile is out of sync
poetry install --no-update # poetry: never modify the lockfile
pip install --require-hashes -r requirements.txt  # pip-tools compiled
```

Plain `pip install -r requirements.txt` does not enforce hashes unless the requirements file uses `--hash=sha256:...` lines. Generate hash-pinned requirements with `pip-compile --generate-hashes` (pip-tools) or `uv pip compile --generate-hashes`.

## References

- PEP 517 build backends: <https://peps.python.org/pep-0517/>
- PyPI trusted publishing: <https://docs.pypi.org/trusted-publishers/>
- uv lockfile: <https://docs.astral.sh/uv/concepts/projects/lock/>
- `.pth` mechanism: Python `site` module docs, `site.addsitedir`

---
name: code-quality-tools
description: Use when the user asks about setting up linting, type checking, code formatting, or pre-commit hooks for Python projects, or mentions ruff, mypy, or pre-commit configuration. Configure and use automated code quality tools (ruff, mypy, pre-commit) for scientific Python projects. Covers linting rules, type checking configuration, formatting, and CI integration.
metadata:
  assets:
    - assets/pre-commit-config.yaml
    - assets/pyproject-ruff-mypy.toml
  references:
    - references/common-issues.md
    - references/configuration-patterns.md
    - references/type-hints.md
---

# Code Quality Tools for Scientific Python

## Quick Reference Card

### Installation
```bash
pixi add --feature dev ruff mypy pre-commit   # recommended
pip install ruff mypy pre-commit               # pip fallback
```

### Essential Commands
```bash
# Ruff
ruff check .                   # lint
ruff check --fix .             # lint + auto-fix
ruff format .                  # format
ruff check --fix . && ruff format .   # full quality pass

# MyPy
mypy src/                      # type-check project
mypy --strict src/             # strict mode

# Pre-commit
pre-commit install              # register git hook (once per clone)
pre-commit run --all-files      # run on whole repo
pre-commit autoupdate           # bump hook versions
```

### Minimal `pyproject.toml` (scientific Python)
```toml
[tool.ruff]
target-version = "py310"
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "NPY"]
ignore = ["E501"]
fixable = ["ALL"]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]

[tool.ruff.lint.pydocstyle]
convention = "numpy"

[tool.mypy]
python_version = "3.10"
check_untyped_defs = true
warn_return_any = true
show_error_codes = true

[[tool.mypy.overrides]]
module = ["scipy.*", "matplotlib.*", "numpy.*"]
ignore_missing_imports = true
```

### Minimal `.pre-commit-config.yaml`
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.11.0
    hooks:
      - id: mypy
        args: [--ignore-missing-imports]
```

See `assets/pyproject-ruff-mypy.toml` and `assets/pre-commit-config.yaml` for complete annotated templates (including nbstripout, check-yaml, check-toml, pandas-vet rules, etc.).

---

## Tool and Configuration Reference

| Reference | Contents |
|-----------|----------|
| `references/configuration-patterns.md` | Ruff rule selection for scientific Python (NPY, PD, D, ANN); mypy strictness ladder; per-file ignores; fixing common warnings (F401, B006, NPY002) |
| `references/type-hints.md` | Gradual adoption strategy; `NDArray[np.float64]` patterns; Optional/Union; TypedDict for structured returns |
| `references/common-issues.md` | ruff vs black conflicts; mypy missing imports; pre-commit slow on large repos; too many legacy errors; CI failures |

Non-obvious gotchas:
- **Ruff rule `E501` (line too long)**: disable it — ruff format manages line length and they conflict if both are active.
- **`NPY002`**: flags `np.random.rand()` as legacy; the fix is `np.random.default_rng(seed=...).random()`. Worth enabling for reproducibility in scientific code.
- **MyPy `ignore_missing_imports`**: set per-module in `[[tool.mypy.overrides]]`, not globally — global ignores hide real errors in your own code.
- **Pre-commit mypy vs CI mypy**: mypy in pre-commit runs without your installed package, so imports of your own package fail. Either pass `--ignore-missing-imports` in pre-commit args or keep mypy in CI only.
- **Legacy code with hundreds of ruff errors**: use `ruff check --add-noqa .` to baseline all existing violations with `# noqa` comments, then enforce clean code going forward. Remove `# noqa` comments incrementally.
- **`from __future__ import annotations`**: required as the first import for any file using forward references or `X | Y` union syntax on Python < 3.10.

---

## Setup Workflow (New Project)

A sequenced checklist with validation steps.

### Step 1 — Install tools
```bash
pixi add --feature dev ruff mypy pre-commit
```
**Verify:** `ruff --version && mypy --version && pre-commit --version`

### Step 2 — Add configuration to `pyproject.toml`
Copy the minimal config from the Quick Reference Card above, adjusting `target-version` to match your Python support floor.

**Verify:**
```bash
ruff check .     # should report errors (not crash)
mypy src/        # should report errors or "Success"
```

### Step 3 — Fix existing issues
```bash
ruff check --fix .    # auto-fix what ruff can
ruff format .         # apply formatting
```
For a legacy codebase with many errors: `ruff check --add-noqa .` to baseline, then commit.

**Verify:** `ruff check .` returns zero errors.

### Step 4 — Create `.pre-commit-config.yaml` and install hook
```bash
# Create the file (use asset template or minimal snippet above)
pre-commit install
pre-commit run --all-files   # first-run check of entire repo
```
**Verify:** running `git commit` on a dirty file now triggers ruff automatically.

### Step 5 — Add to CI
```yaml
# .github/workflows/quality.yml
- name: Lint
  run: ruff check .
- name: Format check
  run: ruff format --check .
- name: Type check
  run: mypy src/
```
**Verify:** CI passes on a clean branch; a branch with a deliberate type error fails the mypy step.

### Step 6 — Gradual mypy adoption (existing code)
Start with `check_untyped_defs = true` only. Add type hints to new functions. Once coverage is reasonable, enable `disallow_untyped_defs = true`. See `references/type-hints.md` for NumPy array annotation patterns.

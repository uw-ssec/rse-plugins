# Manifest Formats, Terminology, and Pixi vs uv

## Pixi vs uv

Choose **pixi** for compiled/conda-forge packages (NumPy, SciPy, GDAL),
multi-language stacks, mixed conda + PyPI graphs, or multi-platform lockfiles.
Choose **uv** for pure-Python, PyPI-only projects where it is simpler and faster.

## pyproject.toml integration

Put pixi config under `[tool.pixi.*]` in a standard `pyproject.toml`; it coexists
with pip/uv tooling and keeps a single source of truth for a distributable package.

## Terminology: `workspace` (not `project`)

pixi renamed the project-level table to `[tool.pixi.workspace]` (standalone
manifests use `[workspace]`). The older `[tool.pixi.project]` / `[project]`-style
pixi table still works as a deprecated alias, so existing manifests keep
functioning — but new projects should use `workspace`.

## Manifest format: `pixi.toml` vs `pyproject.toml`

This skill leads with `pyproject.toml` (the standard single source of truth for
distributable packages); standalone `pixi.toml` is the leaner alternative.

| Use `pyproject.toml` (this skill's default) | Use standalone `pixi.toml` |
|---------------------------------------------|----------------------------|
| You are building an installable Python package | The project is a workflow, analysis, or app, not a package |
| You want pip/build/uv compatibility | You want the leanest possible manifest |
| `pixi init --format pyproject` | `pixi init` (the default) |

All examples map to both formats: `pyproject.toml` prefixes tables with
`[tool.pixi.*]`; a standalone `pixi.toml` drops the prefix
(`[tool.pixi.workspace]` → `[workspace]`, `[tool.pixi.dependencies]` →
`[dependencies]`).

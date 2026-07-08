# Pixi Best Practices Checklist

## Project Setup
- [ ] Use `pixi init --format pyproject` for new projects
- [ ] Set explicit Python version constraint (`python>=3.11,<3.13`)
- [ ] Organize dependencies by source (conda vs PyPI)
- [ ] Create separate features for dev, test, docs environments
- [ ] Define useful tasks for common workflows
- [ ] Set up `.gitignore` to exclude `.pixi/` directory

## Dependency Management
- [ ] Prefer conda-forge for compiled scientific packages (NumPy, SciPy, GDAL)
- [ ] Use PyPI only for pure Python or conda-unavailable packages
- [ ] Pin exact versions for reproducible research
- [ ] Use version ranges for libraries (allow updates)
- [ ] Specify solve groups for independent environment solving
- [ ] Use `pixi update` regularly to get security patches

## Reproducibility
- [ ] Commit `pixi.lock` to version control
- [ ] Include all platforms in lockfile for cross-platform teams
- [ ] Pin a minimum pixi version (`pixi workspace requires-pixi set ">=0.72"`) so collaborators and CI use a compatible pixi
- [ ] Document environment recreation steps in README
- [ ] Use exact version pins for published research
- [ ] Test environment from scratch periodically
- [ ] Archive environments for long-term preservation

## Performance
- [ ] Use pixi's parallel downloads (automatic)
- [ ] Leverage caching in CI/CD (`prefix-dev/setup-pixi` action)
- [ ] Keep environments minimal (only necessary dependencies)
- [ ] Use solve groups to isolate independent environments
- [ ] Clean old packages with `pixi clean cache`
- [ ] Pin GitHub Actions to commit SHAs (not mutable tags) in CI — see `assets/github-actions-pixi.yml`; a tag like `@v5` can be repointed to malicious code, a SHA cannot

## Development Workflow
- [ ] Define tasks for common operations (test, lint, format)
- [ ] Use task dependencies for complex workflows
- [ ] Create environment-specific tasks when needed
- [ ] Use `pixi shell` for interactive development
- [ ] Use `pixi run` for automated scripts and CI
- [ ] Test in clean environment before releasing

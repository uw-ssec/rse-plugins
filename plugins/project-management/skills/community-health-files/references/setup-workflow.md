# Setup Workflow and Validation

## New Project Setup Flow

1. Create baseline files:

- `README.md`, `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`
- `SECURITY.md`, `SUPPORT.md`, `CITATION.cff`
- `.github/ISSUE_TEMPLATE/*`, `.github/PULL_REQUEST_TEMPLATE.md`

2. Fill templates with project-specific values.

3. Validate citation metadata:

```bash
cffconvert --validate
```

4. Validate GitHub templates:

- Open “new issue” and “new PR” flows and confirm forms render correctly.

5. Check GitHub community profile page and resolve missing items.

If validation fails, update files and re-run checks.

## High-Value Defaults

- Prefer permissive license for broad reuse unless project policy requires copyleft.
- Include citation metadata for research software attribution.
- Keep security reporting channel private and monitored.

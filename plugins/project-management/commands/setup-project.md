---
description: Scaffold a new project with community health files and standard structure for any language
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Setup Project Command

When this command is invoked, initialize a new research software project with community health files and standard open-source infrastructure.

## Input Handling

**If argument provided** (e.g., `/setup-project my-climate-tool`):
- Use the argument as the project name
- Proceed to project setup

**If no argument provided:**
- Ask the user:
  ```
  What is the name of your new project?

  I'll create a project with:
  - Community health files (README, CONTRIBUTING, LICENSE, CODE_OF_CONDUCT, SECURITY, CITATION.cff)
  - Issue and PR templates
  - .gitignore for your language

  Optionally:
  - Set up CI/CD (requires the GitHub plugin)
  - Add a Dockerfile (requires the containerization plugin)

  Please provide a project name (kebab-case recommended, e.g., `climate-analysis-tool`).
  ```
- WAIT for the user's response before proceeding

## Information Gathering

Before creating files, ask the user for essential configuration (use defaults if they want to proceed quickly):

1. **Brief project description** (one sentence)
2. **License** — Default: BSD-3-Clause (common for research software). Options: MIT, Apache-2.0, GPL-3.0
3. **Primary language** — Python, R, Julia, Rust, Go, Node.js, C/C++, Other
4. **Author/organization name** — Default: detect from `gh` config or git config

If the user says "use defaults" or "just create it", proceed with all defaults.

## Project Scaffolding Steps

### Step 1: Create Directory Structure

Create the standard project scaffold with universal infrastructure files:

```
<project-name>/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml
│   │   └── feature_request.yml
│   └── PULL_REQUEST_TEMPLATE.md
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── CITATION.cff
└── .gitignore
```

Note: Language-specific directories (src/, tests/, docs/, lib/, etc.) and project configuration files (pyproject.toml, Cargo.toml, package.json, etc.) should be created using language-specific tooling. This command scaffolds the universal project infrastructure that every project needs regardless of language.

### Step 2: Generate Community Health Files

Use the `community-health-files` skill as reference for content and templates.

- **README.md**: Use the README template from `community-health-files` skill assets. Customize with project name, description, and badge placeholders appropriate for the chosen language.
- **CONTRIBUTING.md**: Use the CONTRIBUTING template. Customize with project name and language-appropriate development setup guidance.
- **LICENSE**: Generate the selected license with current year and author name.
- **CODE_OF_CONDUCT.md**: Use Contributor Covenant v2.1 template.
- **SECURITY.md**: Use SECURITY template with project name.
- **CITATION.cff**: Use CITATION template. Fill in project name, description, author, and current date.

### Step 3: Generate Issue and PR Templates

- **Bug report** (`bug_report.yml`): GitHub issue form with description, reproduction steps, expected/actual behavior, environment info (language-neutral).
- **Feature request** (`feature_request.yml`): GitHub issue form with problem statement, proposed solution, alternatives considered.
- **PR template** (`PULL_REQUEST_TEMPLATE.md`): Checklist with description, type of change, testing done, and documentation updated.

### Step 4: Language-Specific Configuration (User Responsibility)

The project scaffold includes community health files and GitHub templates. Language-specific project configuration should be created using the appropriate tooling:

- **Python:** `pip install hatch && hatch new` or configure `pyproject.toml` manually
- **Rust:** `cargo init`
- **Node.js:** `npm init`
- **R:** `usethis::create_package()`
- **Go:** `go mod init`
- **Julia:** `Pkg.generate()`
- **C/C++:** Create a `CMakeLists.txt` or `Makefile` as appropriate

This command focuses on the universal project infrastructure that every project needs regardless of language.

### Step 5: CI/CD Setup (Optional — Requires GitHub Plugin)

If you have the GitHub plugin installed, run `/ci-setup` to generate GitHub Actions CI/CD workflows tailored to your project's language and tooling.

### Step 6: Pre-commit Hooks (Optional — Requires GitHub Plugin)

If you have the GitHub plugin installed, it can configure pre-commit hooks appropriate for your project's language.

### Step 7: Generate .gitignore

Generate a `.gitignore` based on the project's primary language. Include universal entries:

- `.DS_Store`, `Thumbs.db`
- `.env`, `*.log`
- Editor files: `.vscode/`, `.idea/`

Add language-specific patterns based on the selected language (e.g., `__pycache__/` for Python, `target/` for Rust, `node_modules/` for Node.js, `.Rhistory` for R).

## Output Summary

After creating all files, present a summary:

```
## Project Created: <project-name>

### Files Created:
- README.md — Project description, installation, quickstart
- CONTRIBUTING.md — Contribution guidelines with development setup
- LICENSE — <license-type>
- CODE_OF_CONDUCT.md — Contributor Covenant v2.1
- SECURITY.md — Security reporting policy
- CITATION.cff — Academic citation metadata
- .github/ISSUE_TEMPLATE/bug_report.yml — Bug report form
- .github/ISSUE_TEMPLATE/feature_request.yml — Feature request form
- .github/PULL_REQUEST_TEMPLATE.md — PR checklist
- .gitignore — <language> .gitignore

### Next Steps:
1. `cd <project-name>`
2. `git init && git add . && git commit -m "Initial project scaffold"`
3. `gh repo create <project-name> --public --source=. --push`
4. Set up language-specific project configuration (see Step 4 above)
5. (Optional) Install GitHub plugin and run `/ci-setup` for CI/CD workflows

### Customize:
- Update README.md with detailed project description
- Add language-specific configuration files
- Update CITATION.cff with all authors and ORCIDs
- Customize issue templates for your project's needs
```

## Important Notes

- **Check before overwriting**: If any files already exist in the target directory, warn the user and ask before overwriting.
- **Validate YAML**: Ensure all generated configuration files are syntactically valid.
- **Use templates**: Reference the `community-health-files` skill asset templates for community health files.
- **Respect user choices**: Honor the license and language the user specified.
- **Universal infrastructure only**: This command scaffolds community health files and GitHub templates. Language-specific project configuration is the user's responsibility.

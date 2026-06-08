---
name: community-health-files
description: Generates and configures open-source project files including README, CONTRIBUTING, LICENSE, CODE_OF_CONDUCT, SECURITY, and CITATION.cff, and sets up GitHub issue/PR templates following community best practices. Use when the user asks about setting up a new open-source project, creating README/CONTRIBUTING/LICENSE/CODE_OF_CONDUCT/SECURITY/CITATION.cff files, adding GitHub issue or PR templates, or improving repository community standards.
metadata:
  references:
    - references/license-guide.md
    - references/citation-format.md
    - references/github-templates.md
    - references/setup-workflow.md
  assets:
    - assets/readme-template.md
    - assets/contributing-template.md
    - assets/code-of-conduct-template.md
    - assets/security-template.md
    - assets/citation-template.cff
---

# Community Health Files

## Primary Actions

- Create baseline community files for open-source repositories.
- Generate/adjust contribution, conduct, security, and support policies.
- Provide CITATION.cff metadata for research software citation.
- Create issue/PR templates for consistent triage and review.

## Core File Set

- Required: `README.md`, `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`
- Recommended: `SECURITY.md`, `SUPPORT.md`, `CITATION.cff`, issue/PR templates

## Minimal CITATION.cff Example

```yaml
cff-version: 1.2.0
message: "If you use this software, please cite it as below."
title: "MyProject"
version: 1.0.0
date-released: "2024-01-15"
authors:
  - family-names: "Smith"
    given-names: "Jane"
    orcid: "https://orcid.org/0000-0000-0000-0000"
repository-code: "https://github.com/org/myproject"
doi: "10.5281/zenodo.1234567"
license: MIT
```

Required fields: `cff-version`, `message`, `title`, `authors`. Add `version`, `date-released`, and `doi` for a complete academic citation.

## Minimal GitHub Issue Template (Bug Report)

Place at `.github/ISSUE_TEMPLATE/bug_report.yml`:

```yaml
name: Bug Report
description: Report a reproducible bug
labels: ["bug"]
body:
  - type: textarea
    id: description
    attributes:
      label: Describe the bug
      placeholder: A clear description of what went wrong.
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Steps to reproduce
      placeholder: "1. Run `command`\n2. See error"
    validations:
      required: true
  - type: input
    id: environment
    attributes:
      label: Environment
      placeholder: "OS, Python version, package version"
```

## Setup and Validation Workflow

1. Create baseline files using templates below.
2. Fill project-specific metadata (name, maintainers, contacts, citation fields).
3. Validate `CITATION.cff`:
   ```bash
   pip install cffconvert
   cffconvert --validate
   ```
   **If validation fails:** check `date-released` is `YYYY-MM-DD`, `authors` is a list, and all required fields are present. Common error: `version` field must be a string (`"1.0.0"`, not `1.0.0`).
4. Verify issue/PR templates render in GitHub UI by opening a new issue in the repository.
5. Check repository Community Standards page (`github.com/org/repo/community`) and address flagged gaps.

## Templates

- [assets/readme-template.md](assets/readme-template.md)
- [assets/contributing-template.md](assets/contributing-template.md)
- [assets/code-of-conduct-template.md](assets/code-of-conduct-template.md)
- [assets/security-template.md](assets/security-template.md)
- [assets/citation-template.cff](assets/citation-template.cff)

## Deep References

- License selection and compatibility:
  [references/license-guide.md](references/license-guide.md)
- CITATION.cff fields and academic citation patterns:
  [references/citation-format.md](references/citation-format.md)
- GitHub issue/PR template details:
  [references/github-templates.md](references/github-templates.md)
- Setup sequence and validation checkpoints:
  [references/setup-workflow.md](references/setup-workflow.md)

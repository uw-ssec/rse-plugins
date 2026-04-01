# GitHub Issue and PR Templates Reference

Complete reference for creating, customizing, and managing GitHub issue
forms, PR templates, and organization-level community health defaults.

**Backlinks:** Used by the `community-health-files` skill and the
`project-onboarding-specialist` agent when scaffolding templates. Also
referenced by the `documentation-validator` agent for completeness checks.

## Table of Contents

| Line | Section | Description |
|------|---------|-------------|
| 27   | Quick Reference | File locations and minimal examples |
| 60   | Issue Form Syntax | YAML form schema: types, fields, validation |
| 145  | Input Types | Detailed reference for all 5 input types |
| 245  | Bug Report Template | Complete research software bug report form |
| 310  | Feature Request Template | Complete feature request form |
| 360  | PR Template | Pull request template with checklist |
| 400  | Template Chooser | config.yml for directing users to the right template |
| 430  | Organization-Level Defaults | .github repository for org-wide templates |
| 465  | Template Design Principles | Best practices for research software templates |
| 500  | Troubleshooting | Common issues and fixes |
| 525  | External Resources | GitHub docs and community examples |

---

## Quick Reference

### File Locations

```
.github/
├── ISSUE_TEMPLATE/
│   ├── bug_report.yml        # Bug report issue form
│   ├── feature_request.yml   # Feature request issue form
│   └── config.yml            # Template chooser configuration
├── PULL_REQUEST_TEMPLATE.md  # Default PR template
└── PULL_REQUEST_TEMPLATE/    # (Alternative) multiple PR templates
    ├── default.md
    └── release.md
```

### Minimal Issue Form

```yaml
name: Bug Report
description: Report a bug
labels: ["bug"]
body:
  - type: textarea
    id: description
    attributes:
      label: Description
      description: What happened?
    validations:
      required: true
```

### Minimal PR Template

```markdown
## Description
<!-- Describe your changes -->

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
```

## Issue Form Syntax

GitHub issue forms use YAML to define structured forms. Each form has a
top-level configuration and a `body` array of input elements.

### Top-Level Fields

```yaml
name: "Bug Report"              # Required. Shown in template chooser.
description: "Report a bug"     # Required. Shown in template chooser.
title: "[Bug]: "                # Optional. Pre-filled issue title.
labels: ["bug", "triage"]       # Optional. Auto-applied labels.
projects: ["org/1"]             # Optional. Auto-add to project board.
assignees:                      # Optional. Auto-assign to users.
  - username1
body:                           # Required. Array of form elements.
  - type: ...
```

### Body Element Structure

Every element in `body` has:

```yaml
- type: markdown | input | textarea | dropdown | checkboxes
  id: unique_identifier         # Required for input types (not markdown)
  attributes:                   # Type-specific configuration
    label: "Field Label"        # Required for input types
    description: "Help text"    # Optional
    placeholder: "Example..."   # Optional
    value: "Default value"      # Optional
  validations:
    required: true | false      # Optional, default false
```

**Rules:**
- `id` must be unique within the form
- `id` becomes the field key in the submitted issue body
- `markdown` type does NOT have `id` or `validations`
- Labels appear as the field heading
- Descriptions appear as smaller help text below the label

### Labels and Projects

Labels in templates are auto-applied when the issue is created:

```yaml
labels: ["bug", "needs-triage"]
```

Labels must already exist in the repository. If a label doesn't exist,
the issue will still be created but without that label.

**Tip:** Create a standard label taxonomy. See the GitHub plugin's
issue-triage skill for a recommended label set.

## Input Types

### markdown

Displays static text. Used for instructions, section headers, and context.
Does NOT create a form field.

```yaml
- type: markdown
  attributes:
    value: |
      ## Environment Information

      Please provide details about your setup so we can reproduce the issue.
```

**Use cases:** Section headers, instructions, links to docs, warnings.

### input

Single-line text input.

```yaml
- type: input
  id: version
  attributes:
    label: "Version"
    description: "Which version are you using?"
    placeholder: "e.g., 1.2.3"
  validations:
    required: true
```

**Use cases:** Version numbers, OS names, short identifiers.

### textarea

Multi-line text area. Supports markdown rendering in the submitted issue.

```yaml
- type: textarea
  id: steps
  attributes:
    label: "Steps to Reproduce"
    description: "Provide a minimal reproducible example"
    placeholder: |
      1. Install the package
      2. Run the following code:
      ```
      import mypackage
      mypackage.do_thing()
      ```
      3. Observe the error
    render: bash  # Optional: syntax highlighting for the field
  validations:
    required: true
```

**The `render` attribute:** When set, the field renders as a code block
with the specified language highlighting. The user's input is wrapped in
triple backticks automatically.

Valid render languages: Any GitHub-supported language identifier (python,
bash, json, yaml, r, rust, go, julia, cpp, etc.).

**Use cases:** Bug descriptions, code examples, error logs, detailed text.

### dropdown

Single or multi-select dropdown menu.

```yaml
- type: dropdown
  id: severity
  attributes:
    label: "Severity"
    description: "How severe is this issue?"
    options:
      - "Critical - crashes or data loss"
      - "Major - feature broken, no workaround"
      - "Minor - feature broken, workaround exists"
      - "Cosmetic - visual or documentation issue"
    multiple: false  # Set to true for multi-select
  validations:
    required: true
```

**Use cases:** Severity levels, categories, environment selection, component
selection.

### checkboxes

One or more checkboxes. Useful for acknowledgments and multi-select options.

```yaml
- type: checkboxes
  id: terms
  attributes:
    label: "Acknowledgments"
    options:
      - label: "I have searched existing issues for duplicates"
        required: true
      - label: "I am using the latest version"
      - label: "I have read the contributing guidelines"
```

**Use cases:** Duplicate check acknowledgment, terms acceptance, feature
selection, environment checklist.

**Note:** Individual checkbox items can be independently required, unlike
other input types where `required` applies to the whole field.

## Bug Report Template

A comprehensive bug report template for research software:

```yaml
name: Bug Report
description: Report a bug or unexpected behavior
title: "[Bug]: "
labels: ["bug", "needs-triage"]
body:
  - type: markdown
    attributes:
      value: |
        Thank you for reporting a bug. Please fill out the sections below
        so we can reproduce and fix the issue.

  - type: textarea
    id: description
    attributes:
      label: Description
      description: A clear description of what the bug is.
    validations:
      required: true

  - type: textarea
    id: reproduce
    attributes:
      label: Steps to Reproduce
      description: >-
        Provide a minimal, complete, and verifiable example.
        Include code, data (or synthetic data), and the exact commands used.
      placeholder: |
        1. Install: ...
        2. Run:
        ```
        # minimal code that triggers the bug
        ```
        3. See error
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What did you expect to happen?
    validations:
      required: true

  - type: textarea
    id: actual
    attributes:
      label: Actual Behavior
      description: What actually happened? Include full error messages or tracebacks.
      render: shell
    validations:
      required: true

  - type: input
    id: version
    attributes:
      label: Version
      description: Which version of this software are you using?
      placeholder: "e.g., 1.2.3"
    validations:
      required: true

  - type: dropdown
    id: os
    attributes:
      label: Operating System
      options:
        - Linux
        - macOS
        - Windows
        - HPC / cluster
        - Other
    validations:
      required: true

  - type: textarea
    id: environment
    attributes:
      label: Environment Details
      description: >-
        Language/runtime version, package manager, relevant dependency versions,
        or any other environment details.
      placeholder: |
        Language version: ...
        Package manager: ...
        Key dependency versions: ...
      render: shell

  - type: checkboxes
    id: checks
    attributes:
      label: Verification
      options:
        - label: I have searched existing issues for duplicates
          required: true
        - label: I can reproduce this on the latest released version
```

## Feature Request Template

```yaml
name: Feature Request
description: Suggest a new feature or enhancement
title: "[Feature]: "
labels: ["enhancement"]
body:
  - type: textarea
    id: problem
    attributes:
      label: Problem Statement
      description: >-
        What problem does this feature solve? Describe the use case.
        "I'm frustrated when..." or "It would be useful to..."
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: >-
        Describe the solution you'd like. Include API sketches, pseudocode,
        or example usage if applicable.

  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives Considered
      description: >-
        What alternatives have you considered? Include workarounds you
        currently use.

  - type: dropdown
    id: scope
    attributes:
      label: Scope
      options:
        - "New feature"
        - "Enhancement to existing feature"
        - "Performance improvement"
        - "Documentation improvement"
        - "Developer experience"

  - type: checkboxes
    id: contribution
    attributes:
      label: Contribution
      options:
        - label: "I would be willing to submit a PR for this feature"
```

## PR Template

Place at `.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## Description

<!-- Describe the changes and their purpose. Link to related issues. -->

Closes #

## Type of Change

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that changes existing behavior)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)
- [ ] CI/CD or infrastructure change

## Checklist

- [ ] My code follows the project's coding conventions
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing tests pass locally
- [ ] I have updated documentation as needed
- [ ] I have added an entry to CHANGELOG.md (if applicable)

## Testing

<!-- Describe the tests you ran and how to reproduce them. -->
```

## Template Chooser

Create `.github/ISSUE_TEMPLATE/config.yml` to customize the template
chooser:

```yaml
blank_issues_enabled: false  # Disable blank issue creation
contact_links:
  - name: Documentation
    url: https://project.readthedocs.io
    about: Check the documentation before filing an issue
  - name: Discussions
    url: https://github.com/org/project/discussions
    about: Ask questions and get help from the community
  - name: Security Vulnerabilities
    url: https://github.com/org/project/security/advisories/new
    about: Report security vulnerabilities privately
```

**`blank_issues_enabled: false`** forces users to use a template. This
improves issue quality but may frustrate users with edge cases. Consider
leaving it `true` for smaller projects.

**`contact_links`** appear alongside issue templates in the chooser. Use
them to redirect users to documentation, discussions, or security reporting
before they file an issue.

## Organization-Level Defaults

The special `.github` repository (no other name — literally `.github`) at
the organization level provides default templates for all repositories.

### How It Works

1. Create a repository named `.github` in your organization
2. Add templates in `.github/ISSUE_TEMPLATE/` and `.github/PULL_REQUEST_TEMPLATE.md`
3. Any repository without its own templates inherits from the org `.github` repo

### Precedence

Repository-level templates override organization-level templates completely.
There is no merging — if a repo has any issue templates, the org-level
templates are ignored.

### What Can Be Shared

| File | Org-Level Supported |
|------|-------------------|
| Issue templates | Yes |
| PR template | Yes |
| CODE_OF_CONDUCT.md | Yes |
| CONTRIBUTING.md | Yes |
| SECURITY.md | Yes |
| SUPPORT.md | Yes |
| FUNDING.yml | Yes |
| LICENSE | No (must be per-repo) |
| README.md | No (must be per-repo) |

**Note:** For deeper guidance on GitHub organization management, see the
GitHub plugin's github-org-management skill.

## Template Design Principles

### For Research Software Projects

1. **Require reproducibility information.** Bug reports should request
   minimal reproducible examples, environment details, and version numbers.

2. **Don't over-require fields.** Make description and reproduction steps
   required; make environment details and severity optional. Too many
   required fields discourage reporting.

3. **Use dropdowns for structured data.** Operating system, severity, and
   scope are better as dropdowns than free text — easier to triage.

4. **Include a duplicate check.** The "I have searched existing issues"
   checkbox reduces duplicate filing by prompting users to search first.

5. **Link to documentation.** Use the template chooser's `contact_links`
   to direct users to docs before they file an issue.

6. **Language-neutral fields.** Use "Version" not "Python version". Use
   "Environment Details" not "pip list output". This keeps templates
   useful for any language.

7. **Separate bug reports from feature requests.** They have different
   information needs and different triage workflows.

### PR Template Design

1. **Link to issues.** Include a `Closes #` field to encourage PR-issue linking.
2. **Checklist over prose.** Checklists are faster to complete and easier to review.
3. **Include testing expectations.** Remind contributors to add tests.
4. **Keep it short.** A PR template over 20 lines discourages contributions.

## Troubleshooting

### Template Not Appearing

- File must be in `.github/ISSUE_TEMPLATE/` (not `.github/templates/`)
- YAML must be valid — test with `python -c "import yaml; yaml.safe_load(open('file.yml'))"`
- `name` and `description` are required top-level fields
- File extension must be `.yml` or `.yaml`

### Labels Not Applied

- Labels must already exist in the repository
- Label names are case-sensitive
- Create labels first: `gh label create "bug" --description "Bug report" --color d73a4a`

### Form Fields Not Rendering

- `id` must be unique across all fields in the form
- `type` must be one of: `markdown`, `input`, `textarea`, `dropdown`, `checkboxes`
- `render` attribute only works on `textarea` type
- `options` is required for `dropdown` and `checkboxes` types

### PR Template Not Used

- File must be named exactly `PULL_REQUEST_TEMPLATE.md` (case-sensitive)
- Must be in `.github/` directory (or repository root)
- Only one default PR template is supported; multiple templates require
  query parameter: `?template=release.md`

## External Resources

- [GitHub: Creating Issue Forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms) — Official YAML syntax reference
- [GitHub: Creating PR Templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository) — PR template documentation
- [GitHub: Template Chooser](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository#configuring-the-template-chooser) — config.yml documentation
- [GitHub: Organization .github Repository](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file) — Org-level defaults
- [GitHub: Community Profile](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories) — Community health score

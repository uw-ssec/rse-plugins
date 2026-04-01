---
name: community-health-files
description: Templates and guidance for creating community health files (README, CONTRIBUTING, LICENSE, CODE_OF_CONDUCT, SECURITY, CITATION.cff, issue/PR templates) for open-source research software projects in any language.
metadata:
  references:
    - references/license-guide.md
    - references/citation-format.md
    - references/github-templates.md
  assets:
    - assets/readme-template.md
    - assets/contributing-template.md
    - assets/code-of-conduct-template.md
    - assets/security-template.md
    - assets/citation-template.cff
---

# Community Health Files for Research Software Projects

A comprehensive guide to creating and maintaining community health files for open-source research software projects. Community health files define how contributors interact with your project, set expectations for behavior, and establish processes for contributions, security reporting, and citation. This skill follows GitHub community standards and adds specific guidance for scientific software and research engineering contexts.

## Quick Reference Card

**Community Health Files Checklist:**

| File | Purpose | Priority | Location |
|------|---------|----------|----------|
| `README.md` | Project overview, installation, usage | Required | Root |
| `LICENSE` | Legal terms for use and distribution | Required | Root |
| `CONTRIBUTING.md` | How to contribute to the project | Required | Root or `.github/` |
| `CODE_OF_CONDUCT.md` | Community behavior standards | Required | Root or `.github/` |
| `SECURITY.md` | How to report vulnerabilities | Recommended | Root or `.github/` |
| `SUPPORT.md` | How to get help | Recommended | Root or `.github/` |
| `CITATION.cff` | How to cite the software | Recommended | Root |
| `FUNDING.yml` | Sponsorship and funding links | Optional | `.github/` |
| `.github/ISSUE_TEMPLATE/` | Structured issue reporting | Recommended | `.github/` |
| `.github/PULL_REQUEST_TEMPLATE.md` | PR checklist and guidelines | Recommended | `.github/` |
| `CHANGELOG.md` | Record of notable changes | Recommended | Root |
| `GOVERNANCE.md` | Decision-making and leadership | Optional | Root or `.github/` |

**Quick Setup Commands:**

```bash
# Create standard community files from templates
mkdir -p .github/ISSUE_TEMPLATE

# Files in project root
touch README.md LICENSE CONTRIBUTING.md CODE_OF_CONDUCT.md
touch SECURITY.md SUPPORT.md CITATION.cff CHANGELOG.md

# Files in .github/
touch .github/FUNDING.yml
touch .github/PULL_REQUEST_TEMPLATE.md
touch .github/ISSUE_TEMPLATE/bug_report.yml
touch .github/ISSUE_TEMPLATE/feature_request.yml
touch .github/ISSUE_TEMPLATE/config.yml
```

**GitHub Community Profile:**
GitHub automatically detects these files and shows a "Community Standards" checklist at `https://github.com/<owner>/<repo>/community`. Completing all recommended files earns a full community profile score.

## When to Use This Skill

- Setting up a new open-source research software project from scratch
- Improving the community health profile of an existing project
- Creating standardized templates for an organization's repositories
- Adding citation metadata so researchers can properly cite your software
- Establishing contribution guidelines for a research software project
- Setting up security disclosure policies for scientific tools
- Creating issue and PR templates for consistent project management
- Preparing a research codebase for public release or peer review
- Setting up organization-level defaults in a `.github` repository
- Migrating from informal project management to structured community standards

## Standard Community Health Files

### 1. README.md

The README is the front door of your project. It is the first file most visitors read and serves as the primary documentation entry point.

**What it should contain:**

- Project name, logo, and badges (CI status, coverage, PyPI version, license)
- One-paragraph description of what the project does and why it exists
- Installation instructions (pip, conda, from source)
- Quick start example showing the most common use case
- Links to full documentation
- How to cite the project (brief, with link to CITATION.cff)
- Contributing link and license summary
- Acknowledgments and funding sources

**Best practices for scientific software:**

- Include a DOI badge if the software is archived on Zenodo
- Show a scientific use case in the quick start, not just a trivial example
- Link to any associated publications or preprints
- Mention the scientific domain and target audience clearly
- Include a "Related Projects" section to help users find alternatives

See [assets/readme-template.md](assets/readme-template.md) for a complete template.

### 2. LICENSE

The LICENSE file defines the legal terms under which others can use, modify, and distribute your software. Choosing the right license is critical for scientific software because it affects whether others can use your code in their research.

**Common licenses for research software projects:**

| License | Type | Key Feature | Used By |
|---------|------|-------------|---------|
| BSD 3-Clause | Permissive | Simple, allows commercial use | NumPy, SciPy, scikit-learn |
| MIT | Permissive | Very simple, minimal restrictions | Many Node.js and small projects |
| Apache 2.0 | Permissive | Patent protection clause | TensorFlow, Arrow, many Rust/Go projects |
| GPL 3.0 | Copyleft | Derivative works must be open source | Some research tools |
| LGPL 3.0 | Weak copyleft | Libraries can be used in proprietary code | Some scientific libraries |

**Recommendations for research software:**

- **BSD 3-Clause** is the most common choice in the research software ecosystem
- Apache-2.0 is common in Rust and Go projects; MIT is prevalent in the Node.js ecosystem
- Permissive licenses maximize adoption and reuse in research
- Always include the full license text, not just a reference
- Use SPDX identifiers in your project configuration (`pyproject.toml`, `Cargo.toml`, `package.json`, etc.)
- If your project has multiple contributors, consider a contributor license agreement (CLA)

### 3. CONTRIBUTING.md

The CONTRIBUTING file tells potential contributors how to participate in your project. Clear contribution guidelines reduce friction and encourage community involvement.

**Key sections:**

- How to report bugs (link to issue template)
- How to suggest enhancements
- Development environment setup (clone, install, test)
- Code style guidelines and linting tools
- Testing requirements (what tests to write, how to run them)
- Pull request process (branch naming, review expectations, CI checks)
- Commit message conventions
- Documentation requirements
- Communication channels (mailing list, Slack, Discourse, GitHub Discussions)

**Best practices for scientific software:**

- Include instructions for setting up a development environment with scientific dependencies
- Mention how to run the full test suite including slow or integration tests
- Describe how to add new algorithms or scientific functionality
- Explain how to contribute to documentation, especially API docs and tutorials
- Note any domain expertise needed for reviewing certain types of changes
- Reference the code of conduct prominently

See [assets/contributing-template.md](assets/contributing-template.md) for a complete template.

### 4. CODE_OF_CONDUCT.md

The Code of Conduct establishes community behavior standards and provides a framework for addressing unacceptable behavior. It signals that your project is welcoming and inclusive.

**Recommended standard: Contributor Covenant v2.1**

The Contributor Covenant is the most widely adopted code of conduct in open source. It is used by thousands of projects across many language ecosystems including Python, Rust, Go, and JavaScript.

**Key elements:**

- Pledge to make participation harassment-free
- Examples of positive and negative behavior
- Enforcement responsibilities and scope
- Reporting mechanism with contact information
- Consequence ladder (correction, warning, temporary ban, permanent ban)

**Best practices for scientific software:**

- Adapt the code of conduct for academic and research contexts
- Include guidelines about respectful scientific discourse and disagreement
- Name specific enforcement contacts (not just a generic email)
- Connect to your institution's policies if applicable
- Review and update annually

See [assets/code-of-conduct-template.md](assets/code-of-conduct-template.md) for a complete template.

### 5. SECURITY.md

The SECURITY policy tells users and researchers how to responsibly disclose security vulnerabilities. Even scientific software can have security implications, particularly tools that handle data, run on shared infrastructure, or interact with external services.

**Key sections:**

- Supported versions (which versions receive security updates)
- How to report a vulnerability (private channel, not public issues)
- What information to include in a report
- Expected response timeline
- Disclosure policy and coordination
- Scope of security concerns

**Best practices for scientific software:**

- Acknowledge that data integrity is a security concern for research tools
- Mention any compliance requirements (HIPAA, FERPA, export controls)
- Provide a dedicated security email or use GitHub's private vulnerability reporting
- Commit to a reasonable response timeline (e.g., 48 hours for acknowledgment)
- Credit reporters in security advisories (with their permission)

See [assets/security-template.md](assets/security-template.md) for a complete template.

### 6. SUPPORT.md

The SUPPORT file tells users where and how to get help. It reduces noise in issue trackers by directing questions to appropriate channels.

**Recommended contents:**

```markdown
# Getting Help

## Documentation
- Full documentation: https://my-project.readthedocs.io
- API reference: https://my-project.readthedocs.io/en/latest/api/
- Tutorials: https://my-project.readthedocs.io/en/latest/tutorials/

## Asking Questions
- **GitHub Discussions**: For general questions and community discussion
- **Stack Overflow**: Tag your question with `my-project`
- **Mailing list**: dev@my-project.org

## Reporting Bugs
- Use the [bug report template](https://github.com/org/repo/issues/new?template=bug_report.yml)
- Include a minimal reproducible example
- Include your environment details (OS, Python version, package versions)

## Feature Requests
- Use the [feature request template](https://github.com/org/repo/issues/new?template=feature_request.yml)

## Security Issues
- See [SECURITY.md](SECURITY.md) for reporting vulnerabilities
- Do NOT file security issues as public GitHub issues
```

### 7. FUNDING.yml

The FUNDING file enables the "Sponsor" button on your GitHub repository. Place it at `.github/FUNDING.yml`.

**Example for scientific projects:**

```yaml
# .github/FUNDING.yml
github: [maintainer-username]
open_collective: project-name
custom:
  - https://numfocus.org/donate-to-project
  - https://your-institution.edu/donate
```

**Supported platforms:**

- `github` - GitHub Sponsors
- `open_collective` - Open Collective
- `ko_fi` - Ko-fi
- `tidelift` - Tidelift
- `community_bridge` - LFX Mentorship
- `custom` - Up to 4 custom URLs

### 8. CHANGELOG.md

A changelog records all notable changes to the project, organized by version. It helps users understand what changed between releases and whether they need to update.

**Recommended format (Keep a Changelog):**

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- New spectral analysis function `compute_power_spectrum()`

### Changed
- Improved performance of `fit_model()` by 3x

### Fixed
- Fixed incorrect unit conversion in `transform_coordinates()`

## [1.0.0] - 2025-01-15

### Added
- Initial release with core analysis functions
- Documentation and tutorials
- Full test coverage
```

**Categories:** Added, Changed, Deprecated, Removed, Fixed, Security

## The .github Organization-Level Defaults Pattern

GitHub supports organization-level default community health files. When a repository does not have its own version of a file, GitHub falls back to the organization's `.github` repository.

**How it works:**

1. Create a repository named `.github` in your organization (e.g., `org-name/.github`)
2. Place community health files in the root or in a `profile/` directory
3. These files serve as defaults for all repositories in the organization

**Supported files for organization defaults:**

- `CODE_OF_CONDUCT.md`
- `CONTRIBUTING.md`
- `FUNDING.yml` (in `.github/` directory)
- `GOVERNANCE.md`
- `SECURITY.md`
- `SUPPORT.md`
- `ISSUE_TEMPLATE/` and `PULL_REQUEST_TEMPLATE.md`

**Files NOT supported as organization defaults:**

- `README.md` (must be per-repository)
- `LICENSE` (must be per-repository)
- `CITATION.cff` (must be per-repository)

**Directory structure for an organization `.github` repo:**

```
.github/
├── profile/
│   └── README.md          # Organization profile (shown on org page)
├── CODE_OF_CONDUCT.md     # Default for all repos
├── CONTRIBUTING.md         # Default for all repos
├── SECURITY.md             # Default for all repos
├── SUPPORT.md              # Default for all repos
├── FUNDING.yml             # Default funding links
├── GOVERNANCE.md           # Default governance
├── ISSUE_TEMPLATE/
│   ├── bug_report.yml      # Default bug report template
│   ├── feature_request.yml # Default feature request template
│   └── config.yml          # Issue template chooser config
└── PULL_REQUEST_TEMPLATE.md
```

**Best practice:** Define common standards at the organization level and override only when a specific project has unique requirements.

> **Note:** The GitHub plugin provides deeper guidance on organization-level defaults and platform mechanics.

## CITATION.cff for Academic Projects

The Citation File Format (CFF) is a human- and machine-readable file format that provides citation metadata for software. GitHub natively parses `CITATION.cff` and displays a "Cite this repository" button.

**Why it matters for scientific software:**

- Software citation is increasingly recognized as essential for reproducible research
- Journals and funding agencies now expect proper software citation
- CITATION.cff integrates with Zenodo, Zotero, and other reference managers
- GitHub renders a formatted citation with APA and BibTeX export options

**Required fields:**

```yaml
cff-version: 1.2.0
message: "If you use this software, please cite it as below."
title: "My Scientific Package"
authors:
  - family-names: "Smith"
    given-names: "Jane"
    orcid: "https://orcid.org/0000-0000-0000-0000"
type: software
```

**Recommended additional fields:**

```yaml
version: "1.0.0"
date-released: "2025-01-15"
doi: "10.5281/zenodo.1234567"
license: "BSD-3-Clause"
url: "https://github.com/org/my-package"
repository-code: "https://github.com/org/my-package"
keywords:
  - "scientific computing"
  - "data analysis"
  - "astronomy"
abstract: "A one-paragraph description of the software."
```

**Citing a related publication:**

```yaml
preferred-citation:
  type: article
  title: "My Package: A Tool for Scientific Analysis"
  authors:
    - family-names: "Smith"
      given-names: "Jane"
  journal: "Journal of Open Source Software"
  year: 2025
  volume: 10
  issue: 100
  start: 1234
  doi: "10.21105/joss.01234"
```

**Validation:** Use the `cffconvert` tool to validate your CITATION.cff:

```bash
pip install cffconvert
cffconvert --validate
```

See [assets/citation-template.cff](assets/citation-template.cff) for a complete template.

## Issue Templates

GitHub supports YAML-based issue forms that provide structured fields for reporters. Place these in `.github/ISSUE_TEMPLATE/`.

### Bug Report Template

```yaml
# .github/ISSUE_TEMPLATE/bug_report.yml
name: Bug Report
description: Report a bug or unexpected behavior
labels: ["bug", "triage"]
body:
  - type: markdown
    attributes:
      value: |
        Thank you for reporting a bug. Please fill out the sections below
        to help us reproduce and fix the issue.

  - type: textarea
    id: description
    attributes:
      label: Bug Description
      description: A clear description of the bug
    validations:
      required: true

  - type: textarea
    id: reproduction
    attributes:
      label: Steps to Reproduce
      description: Minimal code example or steps to reproduce the bug
      placeholder: |
        ```
        # Minimal code or steps that trigger the bug
        ```
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What you expected to happen

  - type: textarea
    id: actual
    attributes:
      label: Actual Behavior
      description: What actually happened (include error messages and tracebacks)

  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: Your environment details
      placeholder: |
        - OS: [e.g., Ubuntu 22.04, macOS 14, Windows 11]
        - Language/runtime version: [e.g., Python 3.12, Rust 1.75, Node 20]
        - Package version: [e.g., 1.2.3]
        - Installation method: [e.g., pip, conda, cargo, npm, source]
    validations:
      required: true
```

### Feature Request Template

```yaml
# .github/ISSUE_TEMPLATE/feature_request.yml
name: Feature Request
description: Suggest a new feature or enhancement
labels: ["enhancement"]
body:
  - type: textarea
    id: description
    attributes:
      label: Feature Description
      description: A clear description of the feature you would like
    validations:
      required: true

  - type: textarea
    id: motivation
    attributes:
      label: Motivation
      description: Why is this feature needed? What problem does it solve?
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives Considered
      description: Any alternative solutions or workarounds you have considered

  - type: textarea
    id: context
    attributes:
      label: Additional Context
      description: Any other context, references, or screenshots
```

### Template Chooser Configuration

```yaml
# .github/ISSUE_TEMPLATE/config.yml
blank_issues_enabled: false
contact_links:
  - name: Questions and Discussion
    url: https://github.com/org/repo/discussions
    about: Ask questions and discuss ideas here
  - name: Security Vulnerabilities
    url: https://github.com/org/repo/security/advisories/new
    about: Report security vulnerabilities privately
```

## Pull Request Template

Place at `.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## Description

<!-- Briefly describe the changes in this PR -->

## Related Issues

<!-- Link to related issues: Fixes #123, Closes #456 -->

## Type of Change

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)
- [ ] CI/CD or infrastructure change

## Checklist

- [ ] I have read the [CONTRIBUTING](CONTRIBUTING.md) guidelines
- [ ] My code follows the project's code style
- [ ] I have added tests that prove my fix/feature works
- [ ] All new and existing tests pass
- [ ] I have updated the documentation as needed
- [ ] I have added an entry to the changelog (if applicable)
- [ ] My changes do not introduce new warnings

## Testing

<!-- Describe the tests you ran and how to reproduce them -->

## Screenshots (if applicable)

<!-- Add screenshots to help explain your changes -->
```

## Best Practices for Research Software Projects

### Open Science and Transparency

1. **Choose permissive licenses** to maximize adoption in the research community
2. **Archive releases on Zenodo** to get DOIs for each version
3. **Include CITATION.cff** so researchers can cite your software properly
4. **Document algorithms and methods** with references to publications
5. **Provide example data and notebooks** for reproducibility
6. **Publish in JOSS** (Journal of Open Source Software) for peer review and visibility

### Reproducibility

1. **Pin dependency versions** in CI and documentation examples
2. **Use containerization** (Docker, Singularity) for complex environments
3. **Document data formats** and provide sample data files
4. **Include random seed management** for stochastic methods
5. **Version your data** alongside your code when possible
6. **Provide environment specification files** appropriate for your language (requirements.txt, environment.yml, Cargo.lock, package-lock.json, etc.)

### Community Engagement

1. **Respond to issues and PRs promptly** (even if just to acknowledge receipt)
2. **Label issues clearly** for new contributor discoverability (`good first issue`, `help wanted`)
3. **Write a detailed CONTRIBUTING.md** with setup instructions
4. **Use GitHub Discussions** for questions and ideas (keep issues for actionable items)
5. **Recognize all contributors** (code, docs, design, testing, mentoring)
6. **Hold regular community meetings** or office hours for larger projects
7. **Create a GOVERNANCE.md** once the project has multiple maintainers

### Scientific Software Specific Considerations

1. **Validate against known results** - include tests that compare against published values
2. **Document physical units** - clearly state what units your functions expect and return
3. **Handle edge cases in domain** - NaN values, empty datasets, boundary conditions
4. **Provide domain-specific issue templates** - include fields for scientific context
5. **Credit data sources** - acknowledge datasets, catalogs, and databases used
6. **Follow field conventions** - use standard variable names, coordinate systems, and formats

## File Templates

Ready-to-use templates are available in the `assets/` directory:

- **[assets/readme-template.md](assets/readme-template.md)** - Complete README template for research software projects
- **[assets/contributing-template.md](assets/contributing-template.md)** - Contribution guidelines template
- **[assets/code-of-conduct-template.md](assets/code-of-conduct-template.md)** - Contributor Covenant v2.1 adapted for scientific communities
- **[assets/security-template.md](assets/security-template.md)** - Security policy template
- **[assets/citation-template.cff](assets/citation-template.cff)** - CITATION.cff template for academic software

## Reference Guides

Detailed reference documentation for complex topics. Agents should consult the table of contents in each file and read specific sections as needed.

- **[references/license-guide.md](references/license-guide.md)** - License selection for research software: decision flowchart, permissive vs copyleft comparison, SPDX identifiers for all languages, license compatibility matrix, CLA/DCO guidance, and funding agency requirements
- **[references/citation-format.md](references/citation-format.md)** - Citation File Format (CFF) specification: required/recommended fields, ORCID integration, Zenodo DOI minting, JOSS requirements, preferred-citation for papers, and language-specific patterns
- **[references/github-templates.md](references/github-templates.md)** - GitHub issue forms and PR templates: YAML form syntax, all 5 input types, complete bug report and feature request examples, template chooser config, and organization-level defaults

## Community Health Files Checklist

Use this checklist when setting up or auditing a project:

- [ ] README.md exists with project description, installation, and usage
- [ ] LICENSE file is present with appropriate open-source license
- [ ] CONTRIBUTING.md explains how to contribute
- [ ] CODE_OF_CONDUCT.md establishes behavior standards
- [ ] SECURITY.md describes vulnerability reporting process
- [ ] SUPPORT.md directs users to help resources
- [ ] CITATION.cff provides citation metadata (for academic projects)
- [ ] .github/FUNDING.yml configured (if accepting sponsorship)
- [ ] Issue templates created for bug reports and feature requests
- [ ] Pull request template includes checklist and description fields
- [ ] CHANGELOG.md tracks notable changes per release
- [ ] GitHub community profile shows green checkmarks
- [ ] Organization-level defaults considered (for multi-repo orgs)
- [ ] All contact emails and URLs are current and monitored
- [ ] Templates have been tested by creating sample issues and PRs

## Resources

- **GitHub Community Health Files**: <https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions>
- **Contributor Covenant**: <https://www.contributor-covenant.org/>
- **Citation File Format**: <https://citation-file-format.github.io/>
- **Keep a Changelog**: <https://keepachangelog.com/>
- **Choose a License**: <https://choosealicense.com/>
- **JOSS (Journal of Open Source Software)**: <https://joss.theoj.org/>
- **Zenodo**: <https://zenodo.org/>
- **Scientific Python Development Guide**: <https://learn.scientific-python.org/development/>
- **GitHub Issue Forms**: <https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests>
- **All Contributors**: <https://allcontributors.org/>
- **REUSE (License Compliance)**: <https://reuse.software/>
- **Software Sustainability Institute**: <https://www.software.ac.uk/>

# Contributing to [Project Name]

Thank you for your interest in contributing to [Project Name]! This document
provides guidelines and instructions for contributing. We value all forms of
contribution, including code, documentation, bug reports, feature requests,
and community support.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)
- [Getting Help](#getting-help)

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code. Please report unacceptable
behavior to [conduct@example.com].

## How to Contribute

There are many ways to contribute to [Project Name]:

- **Report bugs** by opening a [bug report issue](https://github.com/ORG/REPO/issues/new?template=bug_report.yml)
- **Suggest features** by opening a [feature request](https://github.com/ORG/REPO/issues/new?template=feature_request.yml)
- **Fix bugs** by submitting pull requests for open issues labeled [`bug`](https://github.com/ORG/REPO/labels/bug)
- **Add features** by submitting pull requests for approved feature requests
- **Improve documentation** by fixing typos, adding examples, or writing tutorials
- **Review pull requests** by providing constructive feedback
- **Help others** by answering questions in [GitHub Discussions](https://github.com/ORG/REPO/discussions)

### Good First Issues

If you are new to the project, look for issues labeled
[`good first issue`](https://github.com/ORG/REPO/labels/good%20first%20issue).
These are specifically curated to be approachable for newcomers.

## Reporting Bugs

Before reporting a bug, please:

1. **Search existing issues** to see if the bug has already been reported
2. **Update to the latest version** to check if the bug has been fixed
3. **Create a minimal reproducible example** that demonstrates the issue

When filing a bug report, include:

- A clear and descriptive title
- Steps to reproduce the behavior
- Expected behavior vs. actual behavior
- Error messages and full tracebacks
- Your environment details:
  - Operating system and version
  - Language/runtime version
  - Package version
  - How you installed the package
  - Versions of key dependencies

## Suggesting Enhancements

Enhancement suggestions are welcome. When suggesting a feature:

- **Describe the problem** your feature would solve
- **Describe the solution** you would like
- **Describe alternatives** you have considered
- **Provide context** such as links to related discussions, papers, or implementations

For scientific features, please include:

- References to relevant publications or algorithms
- Example use cases from your research domain
- Sample input/output data if applicable

## Development Setup

### Prerequisites

- [Language/Runtime] >= [version]
- Git
- A GitHub account

### Setting Up Your Development Environment

1. **Fork the repository** on GitHub

2. **Clone your fork:**

   ```bash
   git clone https://github.com/YOUR-USERNAME/REPO.git
   cd REPO
   ```

3. **Add the upstream remote:**

   ```bash
   git remote add upstream https://github.com/ORG/REPO.git
   ```

4. **Install dependencies using your project's package manager:**

   <!-- Replace with the appropriate commands for your ecosystem. Examples: -->

   ```bash
   # Python
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e ".[dev]"

   # Rust
   # cargo build

   # Node.js
   # npm install

   # Or if using pixi (multi-language):
   # pixi install
   ```

5. **Install pre-commit hooks (if applicable):**

   ```bash
   pre-commit install
   ```

6. **Verify your setup by running the tests:**

   ```bash
   # Run the project's test suite using the appropriate test runner
   ```

## Making Changes

### Branch Naming

Create a descriptive branch name from the latest `main`:

```bash
git checkout main
git pull upstream main
git checkout -b your-branch-name
```

Use these prefixes for branch names:

- `fix/` - Bug fixes (e.g., `fix/incorrect-unit-conversion`)
- `feature/` - New features (e.g., `feature/add-spectral-analysis`)
- `docs/` - Documentation changes (e.g., `docs/update-installation-guide`)
- `refactor/` - Code refactoring (e.g., `refactor/simplify-io-module`)
- `test/` - Test additions or improvements (e.g., `test/add-edge-case-tests`)

### Commit Messages

Write clear, descriptive commit messages:

```
Short summary of change (50 characters or less)

More detailed explanation if needed. Wrap at 72 characters. Explain
the problem this commit solves and why this approach was chosen.

- Bullet points are fine
- Use a hyphen for list items

Fixes #123
```

**Guidelines:**

- Use the imperative mood ("Add feature" not "Added feature")
- First line is a concise summary (50 characters or less)
- Separate the summary from the body with a blank line
- Reference relevant issues and pull requests

## Code Style

This project follows the coding conventions established by the community for its primary language.

### Formatting and Linting

We use automated tools to enforce consistent code style. If the project uses [pre-commit](https://pre-commit.com/), hooks run automatically on each commit.

<!-- Replace the tools below with those used by your project. Examples by ecosystem:
     Python:  ruff (linting + formatting), mypy (type checking)
     Rust:    cargo fmt (formatting), cargo clippy (linting)
     Node.js: eslint (linting), prettier (formatting)
     Go:      gofmt (formatting), golangci-lint (linting)
-->

To run code quality checks manually:

```bash
# Run all pre-commit hooks (if configured)
pre-commit run --all-files

# Or run your language-specific linter and formatter directly
```

### Code Conventions

- Follow the established style guide for your language
- Use type annotations where supported by the language
- Write documentation comments for all public functions, classes, and modules
- Keep functions focused and reasonably sized
- Prefer clear, readable code over clever solutions

### Documentation Comment Example

<!-- Replace with a documentation comment example in your project's language and style. -->

## Testing

All contributions must include appropriate tests.

<!-- Replace with the test framework and commands used by your project. Examples:
     Python:  pytest
     Rust:    cargo test
     Node.js: npm test / jest / vitest
     Go:      go test ./...
-->

### Running Tests

```bash
# Run all tests
# <your test command here>

# Run a specific test file
# <your test command for a single file>

# Run with coverage report
# <your coverage command here>
```

### Writing Tests

- Place tests in the project's designated test directory, mirroring the source structure
- Follow the naming conventions of the test framework
- Test edge cases and error conditions
- Use parameterized tests for verifying multiple inputs
- Use shared fixtures or helpers for common test data
- Aim for at least 90% code coverage for new code

## Documentation

Good documentation is essential for scientific software. When contributing:

- **Update docstrings** for any functions or classes you change
- **Update the user guide** if you add or change features
- **Add examples** that demonstrate real-world usage
- **Update the changelog** (CHANGELOG.md) with a summary of your changes

### Building Documentation Locally

```bash
# Install documentation dependencies (if separate from dev dependencies)
# <your install command here>

# Build the docs
cd docs
make html

# View the docs (opens in browser)
open _build/html/index.html  # macOS
xdg-open _build/html/index.html  # Linux
```

## Pull Request Process

1. **Ensure your branch is up to date** with the latest `main`:

   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push your branch** to your fork:

   ```bash
   git push origin your-branch-name
   ```

3. **Open a pull request** against the `main` branch of the upstream repository

4. **Fill out the PR template** completely, including:
   - Description of the changes
   - Related issue numbers
   - Type of change
   - Testing details
   - Checklist completion

5. **Wait for review.** A maintainer will review your PR and may request changes.
   Please respond to feedback promptly and push additional commits as needed.

6. **CI checks must pass.** All automated tests, linting, and other checks must
   pass before your PR can be merged.

### PR Review Guidelines

- Be open to feedback and willing to make changes
- Explain your design decisions when asked
- Keep PRs focused on a single change when possible
- Large changes should be discussed in an issue first

## Release Process

Releases are managed by the project maintainers. The general process is:

1. Update the version number
2. Update CHANGELOG.md
3. Create a release tag
4. CI automatically builds and publishes the release
5. Update documentation

## Getting Help

If you need help with your contribution:

- **GitHub Discussions**: Ask questions in the [Q&A category](https://github.com/ORG/REPO/discussions/categories/q-a)
- **Issue comments**: Ask for clarification on specific issues
- **Documentation**: Check the [development guide](https://project-name.readthedocs.io/en/latest/development/)

Thank you for contributing to [Project Name]!

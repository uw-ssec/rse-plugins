# Vale Configuration Reference

Complete reference for configuring Vale as a prose linter for research
software documentation. Covers installation, configuration, style packages,
custom rules, and CI integration.

**Backlinks:** Used by the `documentation-validation` skill and the
`documentation-validator` agent when setting up or troubleshooting Vale.
Also referenced by the `community-health-files` skill for prose quality
in community health files.

## Table of Contents

| Line | Section | Description |
|------|---------|-------------|
| 30   | Quick Start | Install Vale and run your first check in 60 seconds |
| 60   | .vale.ini Configuration | Complete config file reference with all options |
| 120  | Style Packages | Available style packages and when to use each |
| 195  | Style Selection Guide | Decision matrix for choosing styles |
| 225  | Custom Rules | Writing project-specific Vale rules (substitution, existence, etc.) |
| 320  | Vocabulary | Project-specific term lists: accept and reject |
| 365  | Scoping and File Types | Control which files and sections Vale checks |
| 405  | Integration | Editor plugins, pre-commit hooks, GitHub Actions |
| 460  | Configuration Recipes | Ready-to-use configs for common documentation scenarios |
| 510  | Troubleshooting | Common issues and how to fix them |
| 545  | External Resources | Vale docs, style package repos, community resources |

---

## Quick Start

```bash
# Install Vale
# macOS
brew install vale

# Linux (snap)
sudo snap install vale

# Any platform (with Go)
go install github.com/errata-ai/vale/v3/cmd/vale@latest

# Any platform (pre-built binary)
# Download from https://github.com/errata-ai/vale/releases
```

Create a minimal `.vale.ini` in your project root:

```ini
StylesPath = .vale/styles
MinAlertLevel = suggestion

Packages = proselint, write-good

[*.md]
BasedOnStyles = Vale, proselint, write-good
```

Run Vale:

```bash
# Sync style packages (run once, and after changing Packages)
vale sync

# Lint all markdown files
vale docs/
vale README.md CONTRIBUTING.md

# Lint with specific output format
vale --output=JSON docs/
```

## .vale.ini Configuration

The `.vale.ini` (or `_vale.ini` on Windows) file configures Vale's behavior.
It uses INI format with global options and per-file-type sections.

### Global Options

```ini
# Where Vale stores downloaded style packages
StylesPath = .vale/styles

# Minimum alert level to display: suggestion, warning, error
MinAlertLevel = suggestion

# Style packages to download (space or comma separated)
Packages = proselint, write-good, Google

# Vocabulary name (see line 320)
Vocab = MyProject
```

### File Type Sections

Sections use glob patterns to match files:

```ini
# Apply to all Markdown files
[*.md]
BasedOnStyles = Vale, proselint, write-good

# Apply to reStructuredText files
[*.rst]
BasedOnStyles = Vale, write-good

# Apply to specific directories
[docs/tutorials/*.md]
BasedOnStyles = Vale, Google
# Override: disable a specific rule in tutorials
Google.Passive = NO

# Apply to HTML files
[*.html]
BasedOnStyles = Vale, proselint
```

### Rule Overrides

Control individual rules within a section:

```ini
[*.md]
BasedOnStyles = Vale, proselint, write-good

# Disable a rule entirely
write-good.Passive = NO

# Downgrade a rule from error to warning
Vale.Spelling = warning

# Upgrade a rule from suggestion to error
proselint.Cliches = error
```

Override levels: `YES` (enable at default level), `NO` (disable),
`suggestion`, `warning`, `error`.

### Ignore Patterns

```ini
# Ignore code blocks in Markdown
# (Vale does this automatically for fenced code blocks)

# Ignore specific file patterns
[!docs/generated/**]
# Files in docs/generated/ are not checked
```

### Transform Options

```ini
[*.md]
# Treat Markdown as HTML after conversion
Transform = md-to-html

# For AsciiDoc files
[*.adoc]
Transform = adoc-to-html
```

## Style Packages

Style packages are collections of rules. Install them via `Packages` in
`.vale.ini` and download with `vale sync`.

### proselint

General-purpose writing style checks based on expert writing advice.

```ini
Packages = proselint
[*.md]
BasedOnStyles = proselint
```

**What it checks:**
- Cliches and mixed metaphors
- Redundancy ("advance planning", "end result")
- Jargon and unnecessarily complex language
- Hedging ("somewhat", "possibly")
- Sexism and bias in language

**Best for:** General documentation, README files, user guides.

**Alert level:** Mostly warnings and suggestions. Not overly strict.

### write-good

Naive linter for English prose, focused on readability.

```ini
Packages = write-good
[*.md]
BasedOnStyles = write-good
```

**What it checks:**
- Passive voice
- Weasel words ("many", "various", "very")
- "There is/There are" constructions
- Adverb overuse
- Wordy phrases

**Best for:** First-pass readability improvement. Good for catching
passive voice in scientific writing.

**Caveat:** Can be noisy for technical documentation where passive voice
is sometimes appropriate (e.g., "The function is called with...").
Consider `write-good.Passive = NO` if false positives are excessive.

### Google

Google's developer documentation style guide.

```ini
Packages = Google
[*.md]
BasedOnStyles = Google
```

**What it checks:**
- Use of "please" and "sorry" (avoid in technical docs)
- Contractions (use them — more natural)
- Second person ("you") vs. first person ("we")
- Sentence length and complexity
- Specific word choices (e.g., "click" vs "click on")
- Oxford commas
- Heading capitalization

**Best for:** Developer-facing documentation, API docs, tutorials.

**Caveat:** Opinionated about style. May conflict with academic writing
conventions. Best for developer docs, not research papers.

### Microsoft

Microsoft's writing style guide.

```ini
Packages = Microsoft
[*.md]
BasedOnStyles = Microsoft
```

**What it checks:** Similar to Google but with Microsoft-specific preferences.
More comprehensive vocabulary and terminology checks.

**Best for:** Windows-focused documentation, Azure/cloud docs.

### alex

Checks for insensitive or inconsiderate writing.

```ini
Packages = alex
[*.md]
BasedOnStyles = alex
```

**What it checks:**
- Gendered language
- Ableist language
- Racial or ethnic bias
- LGBTQ+ insensitivity

**Best for:** Ensuring inclusive language in community-facing documentation
(README, CONTRIBUTING, CODE_OF_CONDUCT).

## Style Selection Guide

Choose styles based on your documentation type:

| Documentation Type | Recommended Styles |
|-------------------|-------------------|
| README / CONTRIBUTING | `Vale, proselint, write-good` |
| API reference docs | `Vale, Google` |
| Tutorials / how-to | `Vale, Google, write-good` |
| Research paper / methods | `Vale, proselint` (fewer false positives) |
| Community files (CoC, Security) | `Vale, proselint, alex` |
| All documentation | `Vale, proselint` (safe default) |

**Starting recommendation for research software:**

```ini
Packages = proselint, write-good

[*.md]
BasedOnStyles = Vale, proselint, write-good
write-good.Passive = suggestion  # Downgrade passive voice
write-good.TooWordy = suggestion
```

This catches real issues without being overwhelming. Add `Google` later
for developer-facing docs if desired.

## Custom Rules

Create project-specific rules in `.vale/styles/YourProject/`.

### Rule Types

Vale supports several rule extension points:

#### substitution

Flag a word and suggest a replacement.

```yaml
# .vale/styles/MyProject/Terminology.yml
extends: substitution
message: "Use '%s' instead of '%s'."
level: warning
ignorecase: true
swap:
  big data: large dataset
  datasource: data source
  e-mail: email
  utilize: use
  in order to: to
  at this point in time: now
```

#### existence

Flag words or patterns that should not appear.

```yaml
# .vale/styles/MyProject/Jargon.yml
extends: existence
message: "Avoid jargon: '%s'. Define the term or use a simpler alternative."
level: warning
ignorecase: true
tokens:
  - synergy
  - leverage  # as a verb
  - paradigm
  - TODO
  - FIXME
  - HACK
```

#### occurrence

Flag words that appear too many times.

```yaml
# .vale/styles/MyProject/Repetition.yml
extends: occurrence
message: "'%s' appears %d times in this section. Consider varying your language."
level: suggestion
scope: paragraph
max: 3
token: '\b(\w+)\b'
```

#### conditional

Flag a word only if another word is not present.

```yaml
# .vale/styles/MyProject/AcronymDefinition.yml
extends: conditional
message: "Define the acronym '%s' before using it."
level: warning
first: '(?:API|CLI|CI|HPC|RSE|DOI)'
second: 'Application Programming Interface|Command.Line Interface|Continuous Integration|High.Performance Computing|Research Software Engineer|Digital Object Identifier'
```

#### consistency

Enforce consistent usage of one form over another.

```yaml
# .vale/styles/MyProject/Consistency.yml
extends: consistency
message: "Use '%s' consistently. You've used both '%s' and '%s'."
level: error
either:
  dataset: data set
  email: e-mail
  filename: file name
  open source: open-source  # as adjective
```

### File Structure

```
.vale/
├── styles/
│   ├── MyProject/
│   │   ├── Terminology.yml
│   │   ├── Jargon.yml
│   │   ├── Consistency.yml
│   │   └── AcronymDefinition.yml
│   └── Vocab/
│       └── MyProject/
│           ├── accept.txt
│           └── reject.txt
└── .gitkeep
```

## Vocabulary

Vocabulary files define project-specific terminology that Vale should accept
or reject, regardless of style rules.

### accept.txt

Words that Vale should always accept (not flag as misspellings or jargon):

```
# .vale/styles/Vocab/MyProject/accept.txt
# Domain-specific terms
NetCDF
HDF5
xarray
NumPy
FITS
WCS
photometry
spectroscopy

# Project-specific terms
MyProject
mytool

# Abbreviations
RSE
HPC
CI/CD
```

### reject.txt

Words that Vale should always flag:

```
# .vale/styles/Vocab/MyProject/reject.txt
# Deprecated terms
master branch
whitelist
blacklist
sanity check
```

### Linking Vocabulary to Configuration

```ini
# .vale.ini
Vocab = MyProject
# This tells Vale to look in .vale/styles/Vocab/MyProject/
```

## Scoping and File Types

### Supported File Types

Vale natively understands these markup formats:

| Format | Extension | Scope Support |
|--------|-----------|--------------|
| Markdown | `.md` | Headings, code blocks, links, lists |
| reStructuredText | `.rst` | Directives, roles, code blocks |
| AsciiDoc | `.adoc` | Blocks, macros |
| HTML | `.html` | Tags, attributes |
| Org | `.org` | Org-mode syntax |
| DITA XML | `.dita` | DITA elements |

### Scope Control

Vale automatically skips code blocks. You can also control scoping:

```ini
# Skip specific heading levels
[*.md]
# Only check prose, not code
BlockIgnores = (?s) *({{% highlight .* %}}.*?{{% /highlight %}})

# Skip specific sections by pattern
TokenIgnores = (\$[^\n$]+\$)  # Skip inline LaTeX math
```

### Inline Ignoring

Disable Vale for specific lines or sections:

```markdown
<!-- vale off -->
This text is not checked by Vale.
<!-- vale on -->

This text IS checked.

<!-- vale Google.Passive = NO -->
This sentence is allowed to be passive.
<!-- vale Google.Passive = YES -->
```

## Integration

### Editor Plugins

| Editor | Plugin |
|--------|--------|
| VS Code | [Vale VSCode](https://marketplace.visualstudio.com/items?itemName=ChrisChinchilla.vale-vscode) |
| Neovim | [null-ls](https://github.com/jose-elias-alvarez/null-ls.nvim) or [nvim-lint](https://github.com/mfussenegger/nvim-lint) |
| Sublime Text | [SublimeLinter-vale](https://github.com/SublimeLinter/SublimeLinter-vale) |
| Emacs | [flycheck-vale](https://github.com/abingham/flycheck-vale) |

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/errata-ai/vale
    rev: v3.9.1  # Use latest version
    hooks:
      - id: vale
        args: [--config=.vale.ini]
        # Only check documentation files:
        files: \.(md|rst|adoc)$
```

### GitHub Actions

```yaml
name: Documentation Quality
on:
  pull_request:
    paths: ['**.md', '**.rst', 'docs/**']

jobs:
  vale:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: errata-ai/vale-action@reviewdog
        with:
          reporter: github-pr-review
          # Posts inline comments on PR
```

**The `reviewdog` reporter** posts Vale findings as inline PR review comments,
making it easy to address issues during code review.

### Makefile Target

```makefile
.PHONY: lint-docs
lint-docs:
	vale sync
	vale docs/ README.md CONTRIBUTING.md
```

## Configuration Recipes

### Research Software Default

```ini
StylesPath = .vale/styles
MinAlertLevel = suggestion
Vocab = MyProject
Packages = proselint, write-good

[*.md]
BasedOnStyles = Vale, proselint, write-good
write-good.Passive = suggestion
write-good.TooWordy = suggestion

[docs/api/*.md]
BasedOnStyles = Vale
# API docs have different conventions
```

### Strict Documentation (Pre-Release)

```ini
StylesPath = .vale/styles
MinAlertLevel = warning
Vocab = MyProject
Packages = proselint, write-good, Google

[*.md]
BasedOnStyles = Vale, proselint, write-good, Google
Google.Passive = warning
Google.We = NO  # Allow "we" in research context

[CONTRIBUTING.md]
BasedOnStyles = Vale, proselint, write-good, alex
# Check inclusivity in contributor-facing docs
```

### Minimal (Getting Started)

```ini
StylesPath = .vale/styles
MinAlertLevel = warning
Packages = proselint

[*.md]
BasedOnStyles = Vale, proselint
```

## Troubleshooting

### "No styles found"

Run `vale sync` after adding or changing `Packages` in `.vale.ini`. Vale
does not auto-download style packages.

### Too Many False Positives

1. Downgrade noisy rules: `write-good.Passive = suggestion`
2. Add domain terms to `accept.txt` vocabulary
3. Use inline `<!-- vale off -->` for justified exceptions
4. Consider removing overly opinionated style packages

### Vale Not Finding .vale.ini

Vale searches for config in this order:
1. `--config` flag
2. Current directory
3. Parent directories (walks up)
4. Home directory

Verify: `vale ls-config` shows your configuration.

### Slow Performance on Large Docs

- Run Vale only on changed files in CI (use `paths:` filter in GitHub Actions)
- Exclude generated documentation directories
- Use `MinAlertLevel = warning` to reduce output volume

### Code Blocks Being Checked

Vale skips fenced code blocks (` ``` `) automatically. If code is being
checked, ensure:
- Code blocks are properly fenced (triple backticks)
- Indented code blocks (4 spaces) are also skipped in Markdown
- `render` attribute in issue templates wraps input in code blocks

## External Resources

- [Vale Documentation](https://vale.sh/docs/) — Official docs and tutorials
- [Vale GitHub](https://github.com/errata-ai/vale) — Source and releases
- [Vale Studio](https://vale.sh/studio/) — Browser-based rule testing
- [proselint](https://github.com/errata-ai/proselint) — Style package based on expert writing advice
- [write-good](https://github.com/errata-ai/write-good) — Style package for readability
- [Google Developer Style](https://github.com/errata-ai/Google) — Google's documentation style
- [Microsoft Style](https://github.com/errata-ai/Microsoft) — Microsoft's writing style
- [alex](https://github.com/errata-ai/alex) — Inclusive language checking
- [Vale Action](https://github.com/errata-ai/vale-action) — GitHub Actions integration

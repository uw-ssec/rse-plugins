# Documentation Validation Tools Reference

Complete reference for all documentation validation tools: markdownlint,
HTMLProofer, doc8, link checkers, and language-specific documentation testing.

**Backlinks:** Used by the `documentation-validation` skill and the
`documentation-validator` agent when setting up validation pipelines or
troubleshooting tool configuration. Complements `references/VALE_CONFIGURATION.md`
(prose linting) and `references/DOCUMENTATION_STANDARDS.md` (quality criteria).

## Table of Contents

| Line | Section | Description |
|------|---------|-------------|
| 28   | Tool Decision Matrix | Which tool for which job |
| 55   | markdownlint | Markdown formatting and syntax validation |
| 145  | HTMLProofer | Link checking and HTML validation for generated docs |
| 215  | doc8 | reStructuredText linting |
| 255  | Link Checking | Dedicated link validation tools and strategies |
| 310  | Language-Specific Doc Testing | Doctest tools for Python, Rust, R, Go, Julia |
| 420  | Notebook Validation | Testing Jupyter notebooks with nbval and pytest-notebook |
| 470  | CI Pipeline Assembly | Combining tools in GitHub Actions workflows |
| 530  | Pre-commit Integration | Adding doc validation to pre-commit hooks |
| 565  | Makefile Targets | Standard make targets for documentation validation |
| 590  | Performance Tips | Speeding up validation in large projects |
| 615  | External Resources | Tool repositories and documentation links |

---

## Tool Decision Matrix

| Need | Tool | Scope |
|------|------|-------|
| Markdown formatting | markdownlint | `.md` files |
| Prose quality | Vale | `.md`, `.rst`, `.adoc` (see `references/VALE_CONFIGURATION.md`) |
| reStructuredText syntax | doc8 | `.rst` files |
| Broken links in HTML docs | HTMLProofer | Built HTML in `_build/` |
| Broken links in Markdown | markdown-link-check | `.md` files |
| Python code in docs | pytest --doctest-glob | `.md`, `.rst`, `.py` |
| Rust code in docs | cargo test --doc | `///` doc comments |
| R code in docs | testthat + knitr | vignettes, roxygen |
| Go code in docs | go test | `_test.go` examples |
| Julia code in docs | Documenter doctests | docstrings |
| Jupyter notebooks | nbval, pytest-notebook | `.ipynb` |
| CITATION.cff validity | cffconvert | `CITATION.cff` (see `references/CITATION_FORMAT.md`) |
| YAML/TOML syntax | yamllint, taplo | config files |

## markdownlint

markdownlint validates Markdown formatting and consistency. It catches
structural issues that prose linters like Vale miss.

### Installation

```bash
# Via npm (recommended — most features)
npm install -g markdownlint-cli2

# Via Ruby gem
gem install mdl

# Via Docker
docker run -v $PWD:/workdir ghcr.io/igorshubovych/markdownlint-cli2-docker:latest "**/*.md"
```

### Configuration

Create `.markdownlint.yaml` (or `.markdownlint-cli2.yaml`) in the project root:

```yaml
# .markdownlint.yaml
# See https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md

# Disable rules
MD013: false            # Line length (often impractical for docs)
MD033: false            # Inline HTML (needed for badges, details tags)
MD041: false            # First line should be heading (not for all files)

# Configure rules
MD007:                  # Unordered list indentation
  indent: 2
MD024:                  # Multiple headings with same content
  siblings_only: true   # Allow same heading in different sections
MD029:                  # Ordered list prefix
  style: "ordered"      # 1. 2. 3. (not 1. 1. 1.)
```

### Key Rules

| Rule | Description | Default |
|------|-------------|---------|
| MD001 | Heading level increment (no skipping h2 → h4) | error |
| MD003 | Heading style consistency (ATX vs setext) | error |
| MD007 | Unordered list indentation | warning |
| MD009 | Trailing spaces | error |
| MD012 | Multiple consecutive blank lines | error |
| MD013 | Line length | warning (often disabled) |
| MD022 | Headings should be surrounded by blank lines | error |
| MD024 | Multiple headings with same content | warning |
| MD025 | Multiple top-level headings | error |
| MD031 | Fenced code blocks surrounded by blank lines | error |
| MD032 | Lists surrounded by blank lines | error |
| MD033 | Inline HTML | warning (often disabled) |
| MD034 | Bare URLs | warning |
| MD040 | Fenced code blocks should have a language | warning |
| MD041 | First line should be a top-level heading | warning |

### Running markdownlint

```bash
# Check all Markdown files
markdownlint-cli2 "**/*.md"

# Check specific files
markdownlint-cli2 README.md CONTRIBUTING.md "docs/**/*.md"

# Fix auto-fixable issues
markdownlint-cli2 --fix "**/*.md"

# Ignore specific files
markdownlint-cli2 --config .markdownlint.yaml "#node_modules" "**/*.md"
```

### Inline Disabling

```markdown
<!-- markdownlint-disable MD013 -->
This very long line is allowed because we disabled the line length rule.
<!-- markdownlint-enable MD013 -->

<!-- markdownlint-disable-next-line MD033 -->
<details><summary>Click to expand</summary>
Content here
</details>
```

## HTMLProofer

HTMLProofer validates links, images, and HTML structure in built
documentation. It works on the HTML output of documentation generators
(Sphinx, MkDocs, Jekyll, etc.).

### Installation

```bash
# Ruby gem
gem install html-proofer

# Docker
docker run -v $PWD/_build/html:/site ghcr.io/gjtorikian/html-proofer /site
```

### Running HTMLProofer

```bash
# Check built HTML docs
htmlproofer _build/html/ \
  --ignore-urls "/localhost/,/127.0.0.1/" \
  --ignore-status-codes "403,429" \
  --allow-hash-href \
  --check-external-hash

# Common options
htmlproofer _build/html/ \
  --ignore-urls "/doi.org/"        # DOI links sometimes reject crawlers \
  --no-enforce-https               # Don't require HTTPS for all links \
  --swap-urls "^/project/:/"       # Fix base URL issues
```

### Configuration

```ruby
# Rakefile or Ruby script for more control
HTMLProofer.check_directory('./_build/html', {
  assume_extension: '.html',
  check_external_hash: true,
  check_favicon: false,
  check_opengraph: false,
  ignore_urls: [
    /localhost/,
    /doi\.org/,         # DOI links rate-limit aggressively
    /example\.com/,     # Placeholder URLs in templates
  ],
  ignore_status_codes: [403, 429],
  typhoeus: {
    ssl_verifypeer: false,  # For self-signed certs in CI
    timeout: 30,
  },
}).run
```

### What HTMLProofer Checks

| Check | Description |
|-------|-------------|
| Links | Broken internal and external links |
| Images | Missing image files, empty alt text |
| Scripts | Missing script files |
| HTML validity | Basic HTML structure issues |
| Hash fragments | Anchor links (#section) resolve to actual IDs |

### Rate Limiting and External Links

External link checking can be slow and flaky. Strategies:

1. **Cache results:** HTMLProofer has a built-in cache:
   ```bash
   htmlproofer _build/html/ --cache '{"timeframe": {"external": "1w"}}'
   ```

2. **Separate internal and external checks:**
   - Internal links: Check on every PR (fast, reliable)
   - External links: Check weekly in scheduled CI (slow, flaky)

3. **Ignore known-flaky URLs:**
   ```bash
   --ignore-urls "/doi.org/,/arxiv.org/"
   ```

## doc8

doc8 validates reStructuredText files for syntax and style issues.

### Installation

```bash
pip install doc8
```

### Configuration

```ini
# setup.cfg or .doc8.ini
[doc8]
max-line-length = 99
ignore-path = docs/_build,docs/generated
ignore-path-errors = docs/release-notes.rst;D001
```

### Running doc8

```bash
# Check all RST files in docs/
doc8 docs/

# With custom config
doc8 --config .doc8.ini docs/

# Ignore specific errors
doc8 --ignore D001 docs/  # D001 = line too long
```

### doc8 Error Codes

| Code | Description |
|------|-------------|
| D000 | Invalid RST syntax |
| D001 | Line too long |
| D002 | Trailing whitespace |
| D003 | Tab character found |
| D004 | No newline at end of file |
| D005 | No newline at end of section |

## Link Checking

### markdown-link-check

Checks links directly in Markdown files (no HTML build required).

```bash
# Install
npm install -g markdown-link-check

# Check a file
markdown-link-check README.md

# Check all Markdown files
find . -name '*.md' -exec markdown-link-check {} \;
```

Configuration (`.markdown-link-check.json`):

```json
{
  "ignorePatterns": [
    { "pattern": "^https://example\\.com" },
    { "pattern": "^#" }
  ],
  "replacementPatterns": [
    { "pattern": "^/docs/", "replacement": "https://project.readthedocs.io/en/latest/" }
  ],
  "httpHeaders": [
    { "urls": ["https://github.com"], "headers": { "Accept": "text/html" } }
  ],
  "timeout": "20s",
  "retryOn429": true,
  "retryCount": 3
}
```

### lychee

Fast link checker written in Rust. Handles large documentation sets well.

```bash
# Install
cargo install lychee
# or
brew install lychee

# Check all docs
lychee "**/*.md" "**/*.rst" --exclude "example\\.com"

# Check with GitHub token (avoids rate limiting)
GITHUB_TOKEN=xxx lychee "**/*.md"
```

## Language-Specific Doc Testing

### Python: pytest doctest

Test code examples embedded in documentation:

```bash
# Test code blocks in Markdown files
pytest --doctest-glob="*.md" docs/

# Test code blocks in RST files
pytest --doctest-glob="*.rst" docs/

# Test docstrings in Python source
pytest --doctest-modules src/
```

**Configuration (pyproject.toml):**
```toml
[tool.pytest.ini_options]
addopts = "--doctest-glob='*.md' --doctest-glob='*.rst'"
doctest_optionflags = ["NORMALIZE_WHITESPACE", "ELLIPSIS"]
```

**Requirements:**
- Code blocks must start with `>>>` (Python doctest format)
- Expected output follows the `>>>` line
- Use `...` for continuation lines
- Use `# doctest: +SKIP` to skip untestable examples

### Rust: cargo test --doc

Rust tests all code examples in doc comments by default:

```bash
# Test all documentation examples
cargo test --doc

# Test docs for a specific module
cargo test --doc -- module_name
```

**How it works:** Every fenced code block in `///` doc comments is compiled
and run. Blocks marked with `no_run` are compiled but not executed. Blocks
marked with `ignore` are skipped entirely.

```rust
/// Adds two numbers.
///
/// # Examples
///
/// ```
/// let result = mylib::add(2, 3);
/// assert_eq!(result, 5);
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

### R: testthat + knitr

```r
# Run examples in roxygen documentation
devtools::run_examples()

# Test vignettes (Rmd files)
devtools::test()  # Runs testthat tests
devtools::build_vignettes()  # Builds and tests Rmd vignettes
```

**R-specific tools:**
- `roxygen2`: Generates documentation from comments
- `pkgdown`: Builds documentation websites
- `spelling::spell_check_package()`: Spell checks documentation
- `urlchecker::url_check()`: Checks URLs in package documentation

### Go: testable examples

Go has a built-in convention for testable examples in `_test.go` files:

```go
func ExampleAdd() {
    result := Add(2, 3)
    fmt.Println(result)
    // Output: 5
}
```

```bash
# Run all tests including examples
go test ./...

# Run only example tests
go test -run Example ./...
```

### Julia: Documenter doctests

Julia's `Documenter.jl` tests code blocks in docstrings:

```julia
"""
    add(a, b)

Add two numbers.

# Examples
```jldoctest
julia> add(2, 3)
5
```
"""
function add(a, b)
    return a + b
end
```

```bash
# Run doctests via Documenter
julia --project=docs -e 'using Documenter; doctest(MyPackage)'
```

## Notebook Validation

### nbval

Tests that Jupyter notebook outputs match saved outputs:

```bash
pip install nbval

# Validate all notebooks
pytest --nbval docs/notebooks/

# Validate but allow output changes (just check execution succeeds)
pytest --nbval-lax docs/notebooks/

# Skip specific cells
# Add metadata to cell: {"tags": ["nbval-skip"]}
```

### pytest-notebook

More flexible notebook testing with configurable comparison:

```bash
pip install pytest-notebook

# Run notebook tests
pytest --nb-test-files docs/notebooks/
```

**Configuration (pyproject.toml):**
```toml
[tool.pytest.ini_options]
nb_test_files = "docs/notebooks/*.ipynb"
nb_diff_ignore = ["/cells/*/outputs/*/text", "/metadata"]
```

### Notebook-Specific Considerations

- **Execution time:** Notebooks with expensive computations need timeout configuration
- **Data dependencies:** Notebooks may need test data — ensure it's available in CI
- **Environment consistency:** Pin notebook kernel to match CI environment
- **Output stability:** Floating-point outputs and timestamps change between runs — use `--nbval-lax` or configure tolerances

## CI Pipeline Assembly

### Complete Documentation CI Workflow

```yaml
name: Documentation Quality
on:
  pull_request:
    paths: ['**.md', '**.rst', 'docs/**', '.vale.ini', '.markdownlint.yaml']

jobs:
  markdown-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: DavidAnson/markdownlint-cli2-action@v19
        with:
          globs: "**/*.md"

  prose-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: errata-ai/vale-action@reviewdog
        with:
          reporter: github-pr-review

  link-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: lycheeverse/lychee-action@v2
        with:
          args: "--exclude example\\.com '**/*.md'"

  # Run separately on a schedule for external links:
  external-links:
    if: github.event_name == 'schedule'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: lycheeverse/lychee-action@v2
        with:
          args: "'**/*.md' '**/*.rst'"
```

### Adding Doc Testing to Existing CI

```yaml
# Add to an existing test job
- name: Test documentation examples
  run: |
    # Python
    pytest --doctest-glob="*.md" --doctest-glob="*.rst" docs/

    # Or Rust
    cargo test --doc

    # Or Go
    go test -run Example ./...
```

## Pre-commit Integration

```yaml
# .pre-commit-config.yaml
repos:
  # Markdown formatting
  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.43.0
    hooks:
      - id: markdownlint
        args: ["--config", ".markdownlint.yaml"]

  # Prose quality (Vale)
  - repo: https://github.com/errata-ai/vale
    rev: v3.9.1
    hooks:
      - id: vale
        args: ["--config", ".vale.ini"]
        files: \.(md|rst)$

  # Link checking (fast, internal only)
  - repo: https://github.com/tcort/markdown-link-check
    rev: v3.12.2
    hooks:
      - id: markdown-link-check
        args: ["--config", ".markdown-link-check.json"]

  # YAML validation (for issue templates, CI workflows)
  - repo: https://github.com/adrienverge/yamllint
    rev: v1.35.1
    hooks:
      - id: yamllint
        args: ["-c", ".yamllint.yaml"]
```

## Makefile Targets

```makefile
.PHONY: lint-docs check-links test-docs validate-docs

# Individual targets
lint-docs:
	vale sync && vale docs/ README.md CONTRIBUTING.md
	markdownlint-cli2 "**/*.md"

check-links:
	lychee --exclude "example\.com" "**/*.md"

test-docs:
	pytest --doctest-glob="*.md" docs/

# Combined target
validate-docs: lint-docs check-links test-docs
	@echo "All documentation validation passed"
```

## Performance Tips

### Large Documentation Sets

1. **Parallelize in CI:** Run Vale, markdownlint, and link checks as
   separate CI jobs (they're independent).

2. **Check only changed files in PRs:**
   ```bash
   git diff --name-only HEAD~1 -- '*.md' | xargs vale
   ```

3. **Cache external link results:** HTMLProofer and lychee both support caching.

4. **Separate internal and external link checks:** Internal links are fast
   and reliable — check on every PR. External links are slow and flaky —
   check on a schedule.

5. **Skip generated files:** Exclude `_build/`, `generated/`, `node_modules/`
   from validation.

### CI Time Budget

| Tool | Typical Time | Notes |
|------|-------------|-------|
| markdownlint | 2-5 seconds | Very fast |
| Vale | 5-15 seconds | Depends on style package count |
| lychee (internal) | 5-10 seconds | Fast for internal links |
| lychee (external) | 30-120 seconds | Network-bound, flaky |
| HTMLProofer | 10-60 seconds | Depends on doc size and external links |
| pytest doctest | Varies | Depends on example complexity |

## External Resources

- [markdownlint Rules](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md) — Complete rule reference
- [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2) — CLI tool
- [HTMLProofer](https://github.com/gjtorikian/html-proofer) — HTML validation tool
- [doc8](https://github.com/PyCQA/doc8) — RST linting
- [lychee](https://github.com/lycheeverse/lychee) — Fast link checker
- [markdown-link-check](https://github.com/tcort/markdown-link-check) — Markdown link checker
- [nbval](https://github.com/computationalmodelling/nbval) — Notebook validation
- [pytest-notebook](https://github.com/chrisjsewell/pytest-notebook) — Notebook testing
- [yamllint](https://github.com/adrienverge/yamllint) — YAML linting
- [taplo](https://github.com/tamasfe/taplo) — TOML formatting and validation
- [Vale Documentation](https://vale.sh/docs/) — See also `references/VALE_CONFIGURATION.md`
- [Diataxis Framework](https://diataxis.fr/) — See also `references/DOCUMENTATION_STANDARDS.md`

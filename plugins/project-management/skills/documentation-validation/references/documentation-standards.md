# Documentation Standards for Research Software

Comprehensive reference for documentation frameworks, completeness criteria,
and quality metrics applied to research software projects in any language.

**Backlinks:** Used by the `documentation-validation` skill and the
`documentation-validator` agent when auditing documentation completeness.
Also referenced by the `project-onboarding-specialist` agent when scaffolding
new project documentation.

## Table of Contents

| Line | Section | Description |
|------|---------|-------------|
| 29   | The Diataxis Framework | Four documentation types: tutorials, how-to, reference, explanation |
| 95   | Applying Diataxis | Mapping the framework to research software documentation |
| 150  | Completeness Criteria | What "complete documentation" means at each maturity level |
| 215  | README Standards | What makes a great README for research software |
| 275  | API Documentation | Standards for function/class/module reference docs |
| 320  | Readability Metrics | Flesch-Kincaid, sentence length, and practical guidelines |
| 360  | Documentation Debt | Identifying, measuring, and reducing documentation debt |
| 400  | The Documentation System | docs-as-code, build tools, hosting |
| 445  | Accessibility | Making documentation accessible to all users |
| 480  | Internationalization | Supporting non-English documentation |
| 500  | Quality Checklist | Quick pass/fail checklist for documentation reviews |
| 530  | External Resources | Frameworks, guides, and community standards |

---

## The Diataxis Framework

Diataxis (from Greek: "across" + "arrangement") organizes documentation into
four types based on two axes: what the user needs (learning vs. working) and
how the content is structured (practical vs. theoretical).

```
                    PRACTICAL                  THEORETICAL
                ┌─────────────────┬─────────────────────┐
                │                 │                     │
   LEARNING     │   TUTORIALS     │    EXPLANATION      │
   (study)      │   Learning-     │    Understanding-   │
                │   oriented      │    oriented         │
                │                 │                     │
                ├─────────────────┼─────────────────────┤
                │                 │                     │
   WORKING      │   HOW-TO        │    REFERENCE        │
   (apply)      │   Task-         │    Information-     │
                │   oriented      │    oriented         │
                │                 │                     │
                └─────────────────┴─────────────────────┘
```

### Tutorials

**Purpose:** Help a newcomer learn by doing. Walk them through a complete
experience with guaranteed success.

**Characteristics:**
- Learning-oriented, not task-oriented
- Follows a specific sequence of steps
- Works on first attempt (tested instructions)
- Builds confidence — avoids choices and digressions
- Focuses on concrete actions, not abstract concepts
- Has a meaningful result the learner can see

**Research software example:** "Analyze your first FITS file with astropy"
— walks through opening a file, reading headers, plotting data.

### How-To Guides

**Purpose:** Help a practitioner accomplish a specific task. Assumes basic
knowledge.

**Characteristics:**
- Task-oriented ("How to X")
- Addresses a specific real-world need
- Assumes the reader knows the basics
- Flexible — allows the reader to adapt to their situation
- Can reference other how-to guides
- Ordered by the task's logical steps, not by concepts

**Research software example:** "How to mask bad pixels in your data
reduction pipeline" — addresses a specific need, assumes familiarity
with the tool.

### Reference

**Purpose:** Provide accurate, comprehensive technical information for
users who already know what they're looking for.

**Characteristics:**
- Information-oriented
- Comprehensive and accurate above all else
- Structured by the code itself (classes, functions, modules)
- Terse and precise (not conversational)
- Kept in sync with the code (often auto-generated)
- Does not explain concepts or teach — just documents what exists

**Research software example:** API reference generated from docstrings:
function signatures, parameter types, return values, exceptions.

### Explanation

**Purpose:** Provide understanding. Explain why things work the way they do.

**Characteristics:**
- Understanding-oriented
- Discusses concepts, design decisions, alternatives, history
- Can be opinionated ("We chose X because...")
- Provides context that helps users make their own decisions
- Does not include step-by-step instructions
- May reference academic papers, algorithms, or domain concepts

**Research software example:** "How the coordinate transformation system
works" — explains the mathematical framework, design choices, and
trade-offs.

## Applying Diataxis

### Mapping to Research Software Documentation

| Diataxis Type | Common Locations | Examples |
|--------------|-----------------|----------|
| Tutorials | `docs/tutorials/`, README quickstart | "Getting started with X", "Your first analysis" |
| How-To | `docs/how-to/`, FAQ, cookbook | "How to configure parallel processing", "How to export to HDF5" |
| Reference | `docs/api/`, auto-generated docs | API reference, configuration options, CLI flags |
| Explanation | `docs/explanation/`, architecture docs | "Design decisions", "How the solver works", "Data model" |

### Where Each Type Lives

**README.md** should contain:
- A mini-tutorial (quickstart section)
- Links to full tutorials and how-to guides
- Brief explanation of what the project does and why

**CONTRIBUTING.md** should contain:
- How-to guides for contributing (how to set up, how to test, how to submit)
- Reference for code style and conventions
- Explanation of the project's development philosophy

**Dedicated docs/ directory** should contain:
- Full tutorials for learning
- How-to guides for common tasks
- Auto-generated API reference
- Explanation of architecture and design decisions

### Common Anti-Patterns

1. **Tutorial that's actually reference.** Listing every function parameter
   in a "getting started" guide. Keep tutorials focused on the happy path.

2. **How-to guide that's actually a tutorial.** A "How to query the database"
   guide that starts with "First, install the package..." — skip basics in
   how-to guides.

3. **Reference with too much explanation.** Function docstrings that include
   three paragraphs of theory. Put theory in explanation docs and link to it.

4. **Explanation that's actually a how-to.** "Understanding configuration"
   that's really "How to configure X." Rename it and restructure.

## Completeness Criteria

### Level 1: Minimum Viable Documentation

Every project, no matter how small, must have:

- [ ] README with: what it does, how to install, basic usage example
- [ ] LICENSE file
- [ ] Installation instructions that work on first attempt

### Level 2: Contributor-Ready

Projects that accept contributions need:

- [ ] Everything in Level 1
- [ ] CONTRIBUTING.md with development setup instructions
- [ ] At least one tutorial or getting-started guide
- [ ] API reference for public functions/classes
- [ ] CHANGELOG or release notes

### Level 3: Production-Ready

Projects used in production or by external teams:

- [ ] Everything in Levels 1-2
- [ ] CODE_OF_CONDUCT.md
- [ ] SECURITY.md
- [ ] CITATION.cff (for research software)
- [ ] How-to guides for common tasks
- [ ] Configuration reference
- [ ] Error message documentation or troubleshooting guide
- [ ] Versioned documentation (matching software versions)

### Level 4: Community-Sustained

Projects with active community adoption:

- [ ] Everything in Levels 1-3
- [ ] Architecture/design explanation docs
- [ ] Migration guides between major versions
- [ ] FAQ or discussions
- [ ] Multiple tutorials for different audiences
- [ ] Localized documentation (if international audience)
- [ ] Accessibility compliance

### Assessing Current Level

To determine a project's documentation level, use the
`assets/validation-checklist.md` for a detailed item-by-item assessment.

## README Standards

A research software README should follow this structure:

### Essential Sections (in order)

1. **Title and Badges** — Project name, CI status, version, license
2. **One-Sentence Description** — What the project does (not how)
3. **Key Features** — 3-5 bullet points of core capabilities
4. **Installation** — Primary install method, must work on first attempt
5. **Quick Start** — Minimal working example (5-15 lines of code)
6. **Documentation Link** — Link to full docs if they exist
7. **Contributing** — Link to CONTRIBUTING.md
8. **Citation** — How to cite (link to CITATION.cff)
9. **License** — License name and link to LICENSE file

### Quality Signals

**Good README characteristics:**
- Installation instructions succeed on first attempt in a clean environment
- Quick start example runs without modification and produces meaningful output
- Each section is complete and self-contained
- Links to external docs are not broken
- Domain-specific terms are defined or linked on first use

**README anti-patterns:**
- Installation instructions skip prerequisites
- Quick start example requires undocumented dependencies
- "See docs for details" without a working link
- Badges for services that aren't actually configured
- More than 50% of the README is API documentation

### README Length Guide

| Project Stage | Recommended Length |
|--------------|-------------------|
| Alpha / internal | 50-100 lines |
| Beta / public | 100-250 lines |
| Stable / released | 150-400 lines |

If your README exceeds 400 lines, move content to dedicated documentation.

## API Documentation

### Documentation Coverage Goals

| Level | Coverage |
|-------|---------|
| Minimum | All public functions have a one-line summary |
| Good | All public functions have parameters, returns, and examples |
| Excellent | All public functions have parameters, returns, raises, examples, and cross-references |

### Language-Agnostic Standards

Regardless of language, every public API element should document:

1. **Summary** — One-line description of what it does
2. **Parameters** — Name, type, description, default value
3. **Returns** — Type and description of return value
4. **Errors/Exceptions** — What errors can be raised and when
5. **Examples** — At least one working example
6. **See Also** — Links to related functions or concepts

### Language-Specific Conventions

| Language | Convention | Tool |
|----------|-----------|------|
| Python | NumPy-style or Google-style docstrings | Sphinx + autodoc |
| Rust | `///` doc comments with examples | rustdoc |
| R | roxygen2 comments | pkgdown |
| Julia | `\"\"\"` docstrings | Documenter.jl |
| Go | `//` comments on exported symbols | godoc |
| C/C++ | Doxygen comments | Doxygen |
| JavaScript/TypeScript | JSDoc comments | TypeDoc |

## Readability Metrics

### Flesch-Kincaid Grade Level

Target: **Grade 8-12** for technical documentation. Research papers often
score 14-18; documentation should be more accessible.

Formula: `0.39 * (words/sentences) + 11.8 * (syllables/words) - 15.59`

### Practical Readability Guidelines

| Metric | Target | Why |
|--------|--------|-----|
| Average sentence length | 15-25 words | Shorter sentences are easier to parse |
| Paragraph length | 3-5 sentences | Long paragraphs lose readers |
| Heading frequency | Every 200-400 words | Headings provide navigation and structure |
| Code example frequency | Every 300-500 words | Examples anchor abstract concepts |
| Passive voice usage | <20% of sentences | Active voice is clearer and more direct |
| Jargon density | Define on first use | New readers need definitions |

### Measuring Readability

Vale's `proselint` and `write-good` styles catch many readability issues.
For quantitative measurement:

- **Vale:** Built-in readability metrics via custom rules
- **Hemingway Editor:** Web-based readability analysis (hemingwayapp.com)
- **readability-score (npm):** CLI tool for batch readability analysis

## Documentation Debt

### What Is Documentation Debt?

Documentation debt accumulates when:
- Features are added without documentation
- APIs change but docs are not updated
- Setup instructions become outdated
- Code examples reference removed functionality

### Measuring Documentation Debt

**Coverage ratio:** `documented_public_symbols / total_public_symbols`

**Freshness score:** Compare documentation last-modified dates to code
last-modified dates. Stale documentation (docs older than code) is a debt
indicator.

**Broken link count:** Number of internal and external broken links.

**Setup success rate:** Can a new contributor follow the setup instructions
and run tests on first attempt?

### Reducing Documentation Debt

1. **Add doc checks to CI** — Fail builds when public API lacks documentation
2. **Require docs in PR checklist** — No feature without documentation
3. **Schedule doc sprints** — Dedicated time for documentation improvement
4. **Track doc issues** — Label documentation issues and triage them
5. **Auto-generate what you can** — API reference should come from code

## The Documentation System

### docs-as-code

Treat documentation like code:
- Store in version control alongside code
- Review in pull requests
- Build and deploy automatically
- Test (links, examples, linting)

### Build Tools by Language

| Language | Build Tool | Hosting |
|----------|-----------|---------|
| Python | Sphinx, MkDocs | ReadTheDocs, GitHub Pages |
| Rust | rustdoc, mdBook | docs.rs, GitHub Pages |
| R | pkgdown | GitHub Pages |
| Julia | Documenter.jl | GitHub Pages |
| Go | godoc | pkg.go.dev |
| JavaScript | Docusaurus, TypeDoc | Vercel, Netlify |
| Any | Jupyter Book | GitHub Pages, ReadTheDocs |

### Versioned Documentation

For libraries with multiple supported versions, serve versioned docs:
- ReadTheDocs supports versioning natively
- GitHub Pages can use subdirectories (`/v1/`, `/v2/`)
- Include a version switcher in the documentation UI

## Accessibility

### WCAG Guidelines for Documentation

- **Text alternatives** for images (alt text on diagrams, described figures)
- **Color contrast** of at least 4.5:1 for body text
- **Keyboard navigation** in documentation sites (skip links, focus management)
- **Semantic HTML** in generated documentation (proper heading hierarchy)
- **Readable fonts** at default browser size (minimum 16px body text)

### Research-Specific Accessibility

- **Figure descriptions** for plots and data visualizations
- **Mathematical notation** in accessible formats (MathJax/KaTeX, not images)
- **Code examples** with syntax highlighting that works with screen readers
- **Table summaries** for data tables

## Internationalization

For projects with international audiences:

- **Write in simple English** — avoid idioms, colloquialisms, and cultural references
- **Use consistent terminology** — create and maintain a glossary
- **Support translation** — use tools like Sphinx's i18n support or Crowdin
- **Mark translatable strings** — separate prose from code in documentation
- **Date/number formats** — use ISO 8601 dates and specify units

## Quality Checklist

Quick pass/fail checklist for documentation reviews:

### Structure
- [ ] README exists with installation, quickstart, and links to full docs
- [ ] CONTRIBUTING exists with development setup
- [ ] Documentation is organized by Diataxis type (or equivalent)
- [ ] Navigation is clear and consistent

### Content
- [ ] All public APIs are documented
- [ ] At least one tutorial exists for getting started
- [ ] Code examples run without modification
- [ ] Domain-specific terms are defined
- [ ] Error messages are documented or searchable

### Quality
- [ ] No broken links (internal or external)
- [ ] Prose passes Vale linting with minimal issues
- [ ] Sentences average under 25 words
- [ ] Headings appear every 200-400 words
- [ ] Documentation is current with the latest release

### Maintenance
- [ ] Documentation is in version control
- [ ] Doc quality checks run in CI
- [ ] PRs include documentation updates when needed
- [ ] Stale documentation is flagged and updated regularly

## External Resources

- [Diataxis Framework](https://diataxis.fr/) — The definitive guide to documentation structure
- [Write the Docs](https://www.writethedocs.org/) — Community and resources for documentarians
- [Google Technical Writing Courses](https://developers.google.com/tech-writing) — Free technical writing courses
- [The Turing Way: Documentation](https://the-turing-way.netlify.app/reproducible-research/rdm.html) — Research documentation best practices
- [Scientific Python Development Guide: Docs](https://learn.scientific-python.org/development/guides/docs/) — Python-specific documentation guidance
- [JOSS Review Criteria](https://joss.readthedocs.io/en/latest/review_criteria.html) — What JOSS reviewers check for documentation
- [ReadTheDocs](https://readthedocs.org/) — Free documentation hosting
- [Keep a Changelog](https://keepachangelog.com/) — Changelog format standard
- [Hemingway Editor](https://hemingwayapp.com/) — Readability analysis tool
- [WCAG 2.1 Guidelines](https://www.w3.org/TR/WCAG21/) — Web accessibility standards

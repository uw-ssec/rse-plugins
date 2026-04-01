# Citation File Format (CFF) Reference

Complete reference for creating, validating, and maintaining CITATION.cff
files for research software projects.

**Backlinks:** Used by the `community-health-files` skill, the
`project-onboarding-specialist` agent, and the `documentation-validator`
agent when creating or validating citation metadata.

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| Quick Reference | 30–52 | Minimal valid CITATION.cff with all required fields |
| Required Fields | 53–98 | Fields every CITATION.cff must have |
| Recommended Fields | 99–182 | Fields that improve discoverability and accuracy |
| Author Metadata | 183–253 | Names, ORCID, affiliations, and author ordering |
| Version and Release | 254–285 | Version syncing, DOI, release dates |
| Preferred Citation | 286–337 | Citing a paper instead of (or alongside) the software |
| Identifiers | 338–373 | DOI, SWHID, URL — linking to persistent archives |
| Validation | 374–416 | Tools and CI integration for CFF validation |
| Integration with Zenodo | 417–434 | Auto-archiving and DOI minting via Zenodo |
| Integration with JOSS | 435–457 | Journal of Open Source Software requirements |
| Language-Specific Patterns | 458–486 | How CFF interacts with pyproject.toml, Cargo.toml, etc. |
| Common Mistakes | 487–509 | Frequent CFF errors and how to fix them |
| External Resources | 510–520 | CFF specification, tools, and guides |

---

## Quick Reference

Minimal valid CITATION.cff:

```yaml
cff-version: 1.2.0
message: "If you use this software, please cite it as below."
type: software
title: "My Research Tool"
version: "1.0.0"
date-released: "2025-01-15"
authors:
  - given-names: Jane
    family-names: Doe
    orcid: "https://orcid.org/0000-0001-2345-6789"
    affiliation: "University of Example"
license: BSD-3-Clause
repository-code: "https://github.com/org/my-research-tool"
```

This is the minimum. The sections below explain each field and the
additional fields that improve citation quality.

## Required Fields

These fields are required by the CFF specification:

### cff-version

```yaml
cff-version: 1.2.0
```

Always use `1.2.0` — this is the current CFF specification version. Do
not change this unless a new CFF specification is released.

### message

```yaml
message: "If you use this software, please cite it as below."
```

A human-readable message explaining how to cite the software. The example
above is the conventional phrasing. You may customize it:

```yaml
message: "Please cite both the software and the associated paper (see preferred-citation)."
```

### title

```yaml
title: "My Research Tool"
```

The name of the software. Use the canonical name (not the package name
or repository name, unless they are the same).

### authors

```yaml
authors:
  - given-names: Jane
    family-names: Doe
```

At least one author is required. See line 145 for complete author metadata
guidance including ORCID, affiliations, and ordering.

## Recommended Fields

These fields are not required but significantly improve citation quality:

### type

```yaml
type: software
```

Valid values: `software` (default) or `dataset`. Use `software` for code
projects.

### version

```yaml
version: "1.2.0"
```

The current version of the software. Should match the version in your
project configuration file. See line 205 for version syncing strategies.

### date-released

```yaml
date-released: "2025-01-15"
```

ISO 8601 date (YYYY-MM-DD) of the current release. Update this with each
release.

### license

```yaml
license: BSD-3-Clause
```

SPDX license identifier. Must match the LICENSE file in the repository.
See `references/LICENSE_GUIDE.md` for SPDX identifiers.

### repository-code

```yaml
repository-code: "https://github.com/org/project"
```

URL of the source code repository.

### url

```yaml
url: "https://project.readthedocs.io"
```

URL of the project website or documentation (if different from the repository).

### doi

```yaml
doi: "10.5281/zenodo.1234567"
```

The DOI for the software. See line 295 for details on DOI types and when
to use concept vs. version DOIs.

### abstract

```yaml
abstract: >-
  A brief description of the software and its purpose.
  Use YAML block scalar syntax for multi-line abstracts.
```

### keywords

```yaml
keywords:
  - climate modeling
  - data analysis
  - NetCDF
```

Keywords improve discoverability in citation databases.

## Author Metadata

### Complete Author Entry

```yaml
authors:
  - given-names: Jane
    family-names: Doe
    email: "jane.doe@example.edu"
    orcid: "https://orcid.org/0000-0001-2345-6789"
    affiliation: "Department of Physics, University of Example"
```

### ORCID

Always include ORCID identifiers when available. The ORCID must be a full
URL:

```yaml
# Correct:
orcid: "https://orcid.org/0000-0001-2345-6789"

# Wrong:
orcid: "0000-0001-2345-6789"
```

**Why ORCID matters:** ORCID disambiguates authors with similar names and
links citations across databases. It is increasingly required by journals
and funding agencies.

### Name Particles and Suffixes

```yaml
authors:
  - given-names: Ludwig
    name-particle: van
    family-names: Beethoven

  - given-names: Martin Luther
    family-names: King
    name-suffix: Jr.
```

### Entity Authors (Organizations)

```yaml
authors:
  - name: "The Astropy Collaboration"
    website: "https://www.astropy.org"
```

Use entity authors for large collaborations where individual authorship
is impractical.

### Author Ordering

CFF does not prescribe author ordering. Follow your field's conventions:
- **Physics/Astronomy:** Alphabetical or by contribution
- **Biology/Medicine:** First author = primary contributor, last = PI
- **Computer Science:** First author = primary contributor

Document your ordering convention in CONTRIBUTING.md so new contributors
understand how authorship works.

### Handling Many Authors

For projects with many contributors, decide on a threshold. Common approaches:
1. List all contributors who made significant code contributions
2. List core maintainers + "The [Project] Contributors"
3. Use an entity author for the collaboration

## Version and Release

### Syncing Version with Project Config

The `version` in CITATION.cff should match your canonical version source.
Strategies for keeping them in sync:

**Manual update:** Update CITATION.cff version and date-released as part of
your release checklist. Simple but error-prone.

**Automated with CI:** Add a CI check that verifies the CITATION.cff version
matches the canonical source:

```bash
# Python example: compare pyproject.toml and CITATION.cff versions
PYPROJECT_VERSION=$(python -c "import tomllib; print(tomllib.load(open('pyproject.toml','rb'))['project']['version'])")
CFF_VERSION=$(grep '^version:' CITATION.cff | awk '{print $2}' | tr -d '"')
[ "$PYPROJECT_VERSION" = "$CFF_VERSION" ] || echo "Version mismatch!"
```

**Release tooling integration:** Tools like `python-semantic-release`,
`cargo-release`, and `release-please` can be configured to update
CITATION.cff automatically.

### date-released

Update on every release. Format is ISO 8601:

```yaml
date-released: "2025-06-15"
```

## Preferred Citation

Use `preferred-citation` when you want users to cite a paper instead of
(or in addition to) the software itself.

### Citing a Journal Article

```yaml
message: "If you use this software, please cite the paper below."
preferred-citation:
  type: article
  title: "My Research Tool: A Framework for Climate Data Analysis"
  authors:
    - given-names: Jane
      family-names: Doe
      orcid: "https://orcid.org/0000-0001-2345-6789"
    - given-names: John
      family-names: Smith
  journal: "Journal of Open Source Software"
  year: 2025
  volume: 10
  issue: 95
  start: 1234
  doi: "10.21105/joss.01234"
```

### Citing Both Software and Paper

```yaml
message: "If you use this software, please cite both the software and the paper."
preferred-citation:
  type: article
  title: "The Paper Title"
  # ... paper fields
# The top-level fields describe the software itself
# Users should cite both
```

### Conference Proceedings

```yaml
preferred-citation:
  type: conference-paper
  title: "My Tool: Efficient Analysis of Large Datasets"
  authors:
    - given-names: Jane
      family-names: Doe
  collection-title: "Proceedings of SciPy 2025"
  year: 2025
  doi: "10.25080/example"
```

## Identifiers

### DOI (Digital Object Identifier)

```yaml
doi: "10.5281/zenodo.1234567"
```

Two types of DOIs for software:
- **Concept DOI:** Points to all versions (e.g., `10.5281/zenodo.1234567`).
  Always resolves to the latest version.
- **Version DOI:** Points to a specific version (e.g., `10.5281/zenodo.1234568`).

**Recommendation:** Use the **concept DOI** in the top-level `doi` field so
the citation always resolves. Include the version-specific DOI in the
`identifiers` section:

```yaml
doi: "10.5281/zenodo.1234567"
identifiers:
  - type: doi
    value: "10.5281/zenodo.1234568"
    description: "DOI for version 1.2.0"
```

### Software Heritage ID (SWHID)

```yaml
identifiers:
  - type: swh
    value: "swh:1:dir:abc123..."
    description: "Software Heritage archive"
```

Software Heritage provides permanent archival of source code.

## Validation

### Command-Line Validation

```bash
# Install the CFF validation tool
pip install cffconvert

# Validate CITATION.cff
cffconvert --validate

# Convert to BibTeX
cffconvert -f bibtex

# Convert to APA
cffconvert -f apalike
```

### CI Validation with GitHub Actions

```yaml
name: CITATION.cff
on:
  push:
    paths: ['CITATION.cff']
  pull_request:
    paths: ['CITATION.cff']

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: citation-file-format/cffconvert-github-action@2.0.0
        with:
          args: "--validate"
```

### Online Validation

Upload your CITATION.cff to https://citation-file-format.github.io/ for
browser-based validation and format conversion.

## Integration with Zenodo

Zenodo automatically reads CITATION.cff when creating a release archive.

**Setup:**
1. Link your GitHub repository to Zenodo at https://zenodo.org/account/settings/github/
2. Create a CITATION.cff with complete metadata
3. Create a GitHub release — Zenodo automatically archives it and mints a DOI
4. Update CITATION.cff with the minted DOI

**Zenodo-specific fields:** Zenodo reads `title`, `version`, `date-released`,
`authors`, `license`, `keywords`, and `abstract` directly from CITATION.cff.

**`.zenodo.json` vs `CITATION.cff`:** If both exist, Zenodo prefers
`.zenodo.json`. For most projects, CITATION.cff alone is sufficient. Use
`.zenodo.json` only if you need Zenodo-specific metadata that CFF cannot
express.

## Integration with JOSS

The [Journal of Open Source Software](https://joss.theoj.org/) requires
a CITATION.cff file for submissions.

**JOSS requirements:**
- `cff-version: 1.2.0`
- At least one author with ORCID
- `repository-code` must point to a public repository
- `license` must be an OSI-approved license
- `version` should correspond to the reviewed version

**After JOSS acceptance:** Update CITATION.cff to include the JOSS paper
as `preferred-citation`:

```yaml
preferred-citation:
  type: article
  journal: "Journal of Open Source Software"
  doi: "10.21105/joss.XXXXX"
  # ... other fields
```

## Language-Specific Patterns

### Python

CITATION.cff version should match `pyproject.toml` version. Some tools
(like `setuptools-scm`) can help keep them in sync.

### Rust

No standard integration. Include CITATION.cff in the repository root.
`Cargo.toml` version should match.

### R

R has its own citation mechanism via `CITATION` file (not CITATION.cff).
For maximum compatibility, include both:
- `CITATION.cff` for GitHub integration and Zenodo
- `inst/CITATION` for R's `citation()` function

### Julia

Julia uses `CITATION.bib` by convention. For maximum compatibility, include
both CITATION.cff and CITATION.bib.

### Node.js / Go / C++

No language-specific citation mechanisms. CITATION.cff in the repository
root is the standard.

## Common Mistakes

1. **ORCID without full URL.** Use `https://orcid.org/0000-...`, not just
   the numeric identifier.

2. **Version mismatch.** CITATION.cff version doesn't match the project
   configuration file. Add a CI check (see line 205).

3. **Missing date-released.** Often forgotten when manually updating.
   Use ISO 8601 format: `YYYY-MM-DD`.

4. **Wrong DOI type.** Using a version-specific DOI as the top-level `doi`
   means the citation becomes outdated. Use the concept DOI.

5. **Invalid YAML.** Unquoted special characters, wrong indentation, or
   missing colons. Always validate with `cffconvert --validate`.

6. **Not updating after release.** CITATION.cff should be updated with
   each release (version, date-released, potentially DOI).

7. **Missing preferred-citation after paper publication.** If your software
   has an associated paper, add it as `preferred-citation`.

## External Resources

- [CFF Specification](https://citation-file-format.github.io/cff-initializer-guide/) — Official specification and initializer tool
- [CFF Schema](https://github.com/citation-file-format/citation-file-format/blob/main/schema-guide.md) — Complete schema documentation
- [cffconvert](https://github.com/citation-file-format/cffconvert) — CLI validation and format conversion tool
- [CFF GitHub Action](https://github.com/citation-file-format/cffconvert-github-action) — CI validation
- [Zenodo](https://zenodo.org/) — Research data archival and DOI minting
- [JOSS](https://joss.theoj.org/) — Journal of Open Source Software
- [ORCID](https://orcid.org/) — Researcher identifier registry
- [Software Heritage](https://www.softwareheritage.org/) — Permanent source code archive
- [FORCE11 Software Citation Principles](https://doi.org/10.7717/peerj-cs.86) — Foundational principles for software citation

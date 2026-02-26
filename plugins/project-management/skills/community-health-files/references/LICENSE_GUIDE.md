# License Selection Guide for Research Software

Comprehensive reference for choosing, applying, and managing licenses in
open-source research software projects across any language.

**Backlinks:** Used by the `community-health-files` skill and the
`project-onboarding-specialist` agent when scaffolding new projects or
advising on license selection.

## Table of Contents

| Line | Section | Description |
|------|---------|-------------|
| 28   | Quick Decision Guide | Flowchart for choosing a license in 30 seconds |
| 55   | Permissive Licenses | BSD-3-Clause, MIT, Apache-2.0 — when to use each |
| 120  | Copyleft Licenses | GPL-3.0, LGPL-3.0 — when copyleft is appropriate |
| 162  | SPDX Identifiers | Standard identifiers for project configuration files |
| 195  | License Compatibility | Matrix of which licenses can be combined |
| 232  | Applying a License | Step-by-step: LICENSE file, headers, config files |
| 277  | Contributor Agreements | CLA vs DCO — when each is needed |
| 318  | Research-Specific Considerations | Funding mandates, data licensing, patents |
| 370  | Dual and Multi-Licensing | When and how to offer multiple licenses |
| 395  | Common Mistakes | Frequent licensing errors and how to avoid them |
| 420  | External Resources | Authoritative references and tools |

---

## Quick Decision Guide

Use this flowchart to choose a license quickly. For nuanced situations, read
the detailed sections below.

```
Is this funded by a grant with license requirements?
├── YES → Use the mandated license (check grant terms)
└── NO
    ├── Do you want maximum adoption and reuse?
    │   ├── YES → Is patent protection important?
    │   │   ├── YES → Apache-2.0
    │   │   └── NO → BSD-3-Clause (research default) or MIT
    │   └── NO
    │       ├── Must derivative works stay open source?
    │       │   ├── YES → GPL-3.0
    │       │   └── NO → Is this a library used by others?
    │       │       ├── YES → LGPL-3.0
    │       │       └── NO → GPL-3.0
    └── Special cases:
        ├── Data/documentation only → CC-BY-4.0
        ├── Public domain dedication → CC0-1.0
        └── Mixed code + data → Dual license (see line 370)
```

**Default recommendation for research software:** BSD-3-Clause. It is widely
used across scientific computing ecosystems (NumPy, SciPy, pandas, scikit-learn,
Astropy, xarray, yt, many JOSS-published packages) and maximizes reuse in
both academic and commercial settings.

## Permissive Licenses

Permissive licenses allow broad reuse with minimal restrictions. The three
most common for research software:

### BSD-3-Clause (Recommended Default)

```
BSD 3-Clause License

Copyright (c) [year], [copyright holder]

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.
```

**When to use:** Default choice for research software. The "no endorsement"
clause (clause 3) prevents others from implying your institution endorses
their work — important for universities and research organizations.

**Ecosystem adoption:** NumPy, SciPy, scikit-learn, pandas, Astropy, xarray,
Dask, napari, MDAnalysis, yt, sunpy.

### MIT

```
MIT License

Copyright (c) [year] [copyright holder]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software...
```

**When to use:** Simplest permissive license. No endorsement clause. Common
in the JavaScript/Node.js, Ruby, and Rust ecosystems. Appropriate when you
want maximum simplicity and don't need the endorsement protection.

**Ecosystem adoption:** Ruby on Rails, Node.js ecosystem, Rust crate ecosystem,
jQuery, React, Vue.js, .NET.

### Apache-2.0

**When to use:** When explicit patent protection is important. Includes a
patent grant — contributors explicitly license their patents to users. More
complex than BSD-3 or MIT.

**Ecosystem adoption:** Apache projects, Android, TensorFlow, Kubernetes,
many Google and Apache Foundation projects.

**Key difference from BSD-3/MIT:** Contains an explicit patent grant (Section 3)
and a patent retaliation clause (if you sue for patent infringement, your
license is terminated). Important for software that may involve patented
algorithms.

**Compatibility note:** Apache-2.0 is compatible with GPL-3.0 but NOT with
GPL-2.0.

## Copyleft Licenses

Copyleft licenses require derivative works to use the same (or compatible)
license. Use when you want to ensure all modifications remain open source.

### GPL-3.0

**When to use:** When you want to ensure all derivative works and
modifications remain open source. Appropriate for standalone applications
that you don't intend for use as libraries.

**Key provision:** Any software that links to or incorporates GPL-3.0 code
must also be released under GPL-3.0 (or a compatible license).

**Research impact:** Some commercial and government organizations cannot use
GPL-licensed software due to policy restrictions. This may limit adoption.

### LGPL-3.0

**When to use:** Copyleft for libraries — allows proprietary software to
link against your library without triggering copyleft for the entire
application. Modifications to your library itself must remain open source.

**Key provision:** Software can link to an LGPL library without adopting
the LGPL, but modifications to the library itself must be released under LGPL.

**Example use case:** You want your library to be widely usable (including
by proprietary software), but you want improvements to the library itself
to always be open source.

## SPDX Identifiers

Always use SPDX identifiers for machine-readable license specification.
These are the standard identifiers recognized across all ecosystems.

| License | SPDX Identifier | OSI Approved |
|---------|-----------------|--------------|
| BSD 3-Clause | `BSD-3-Clause` | Yes |
| MIT | `MIT` | Yes |
| Apache 2.0 | `Apache-2.0` | Yes |
| GPL 3.0 | `GPL-3.0-only` | Yes |
| GPL 3.0+ | `GPL-3.0-or-later` | Yes |
| LGPL 3.0 | `LGPL-3.0-only` | Yes |
| Creative Commons BY 4.0 | `CC-BY-4.0` | No (not for software) |
| Public Domain | `CC0-1.0` | No |

### Using SPDX in Project Configuration

**Python (pyproject.toml):**
```toml
[project]
license = {text = "BSD-3-Clause"}
# or with a license file:
license = {file = "LICENSE"}
```

**Rust (Cargo.toml):**
```toml
[package]
license = "BSD-3-Clause"
```

**Node.js (package.json):**
```json
{ "license": "BSD-3-Clause" }
```

**R (DESCRIPTION):**
```
License: BSD_3_clause + file LICENSE
```

**Go (go.mod does not have a license field):**
Include a LICENSE file in the repository root. Go tooling detects it
automatically.

**Julia (Project.toml):**
```toml
license = "BSD-3-Clause"
```

## License Compatibility

When combining code from multiple projects, licenses must be compatible.
This matrix shows which combinations are allowed:

```
                 BSD-3  MIT  Apache-2.0  LGPL-3.0  GPL-3.0
BSD-3-Clause      Y     Y      Y           Y         Y
MIT               Y     Y      Y           Y         Y
Apache-2.0        Y     Y      Y           Y         Y
LGPL-3.0          -     -      -           Y         Y
GPL-3.0           -     -      -           -         Y

Y = Can include code from the row license in a project under the column license
- = Not compatible (the more restrictive license dominates)
```

**Key rules:**
1. Permissive licenses (BSD-3, MIT, Apache-2.0) can be combined freely
2. GPL-3.0 code can absorb any permissive-licensed code
3. LGPL-3.0 code can absorb permissive code but not GPL
4. You CANNOT take GPL code and put it in a BSD/MIT project
5. Apache-2.0 is NOT compatible with GPL-2.0 (but IS with GPL-3.0)

**Practical implication:** If you depend on a GPL-3.0 library and link to
it, your project must also be GPL-3.0 compatible.

## Applying a License

### Step 1: Create the LICENSE File

Place a LICENSE (or LICENSE.txt) file in the repository root containing the
full license text. Use the exact text from https://opensource.org/licenses/
or https://choosealicense.com/.

```bash
# Example: generate BSD-3-Clause license
# Replace [year] and [fullname] with actual values
curl -sL "https://choosealicense.com/licenses/bsd-3-clause/" | \
  # Or simply copy the template from this skill's assets
```

### Step 2: Add License to Project Configuration

Use the SPDX identifier in your project's configuration file (see line 162
for language-specific examples).

### Step 3: Add License Headers (Optional)

Some organizations require license headers in every source file. This is
common for Apache-2.0 and GPL projects but uncommon for BSD/MIT.

**Apache-2.0 header example:**
```
// Copyright [year] [owner]
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
```

**When to add headers:**
- Required by your organization's policy
- Using Apache-2.0 (recommended by the Apache Foundation)
- Multi-file projects where the LICENSE file might not be distributed
  with individual files

**When NOT to add headers:**
- BSD-3 or MIT projects (the LICENSE file is sufficient)
- Projects where headers add noise without value
- Small projects where the LICENSE file always accompanies the code

### Step 4: Verify License in CITATION.cff

Ensure the `license` field in CITATION.cff matches the LICENSE file:

```yaml
license: BSD-3-Clause
```

See `references/CITATION_FORMAT.md` for complete CITATION.cff guidance.

## Contributor Agreements

Contributor agreements clarify the intellectual property status of
contributions. There are two main approaches:

### Developer Certificate of Origin (DCO)

A lightweight attestation where contributors certify they have the right
to submit their contribution. Implemented via `Signed-off-by` lines in
git commits.

```bash
git commit -s -m "Add feature X"
# Produces: Signed-off-by: Name <email>
```

**Enforcement:** Use the [DCO GitHub App](https://github.com/apps/dco) to
automatically check that all commits are signed off.

**When to use:** Most research software projects. The DCO is lightweight,
doesn't require legal review, and is well-understood in open source.

### Contributor License Agreement (CLA)

A formal legal document where contributors grant specific rights (typically
copyright license and patent license) to the project maintainers.

**When to use:**
- Your organization's legal team requires it
- You need the ability to relicense in the future
- Commercial dual-licensing is planned

**When NOT to use:**
- Most research software projects (DCO is sufficient)
- Small community projects (CLAs discourage contributions)

**Tools:** [CLA Assistant](https://cla-assistant.io/) automates CLA signing
via GitHub pull requests.

## Research-Specific Considerations

### Funding Agency Requirements

Some funding agencies mandate specific licenses:

| Agency | Typical Requirement |
|--------|-------------------|
| NSF | Often requires open access; no specific license mandate but expects compliance with data sharing policies |
| NIH | Requires open access for publications; software increasingly expected to be open source |
| DOE | Often requires permissive licensing for government-funded code |
| EU Horizon Europe | Recommends open access; EUPL is an option but permissive licenses are also accepted |
| Wellcome Trust | Requires open access |

**Always check your specific grant terms.** The information above is general
guidance and may not reflect current policy.

### Data vs. Code Licensing

Code and data have different licensing needs:

| Content Type | Recommended License |
|-------------|-------------------|
| Source code | BSD-3-Clause, MIT, Apache-2.0 |
| Documentation | CC-BY-4.0 |
| Data (sharable) | CC-BY-4.0 or CC0-1.0 |
| Data (restricted) | Custom data use agreement |
| Trained models | Varies — check training data licenses |

**Key principle:** Software licenses (BSD, MIT, GPL) are designed for code.
Creative Commons licenses are designed for creative works. Don't use CC
licenses for code or software licenses for data.

### Patent Considerations

If your software implements patented algorithms:
- Apache-2.0 includes an explicit patent grant
- BSD-3 and MIT do NOT include patent grants
- Consider whether your institution's patent policy affects license choice
- Consult your technology transfer office if patents are involved

## Dual and Multi-Licensing

Dual licensing offers the software under two or more licenses. Users choose
which license applies to their use.

**Common patterns:**

1. **Permissive + Copyleft:** Offer under both MIT and GPL-3.0. Users who
   want permissive terms use MIT; users whose project is already GPL use GPL.

2. **Open Source + Commercial:** Offer under GPL-3.0 (free for open source
   use) and a commercial license (paid, for proprietary use).

3. **Code + Data split:** Code under BSD-3-Clause, data under CC-BY-4.0.
   Document this clearly in the README.

**How to implement dual licensing:**

```
# In LICENSE file:
This project is dual-licensed under BSD-3-Clause and Apache-2.0.
You may use this software under either license, at your option.

See LICENSE-BSD and LICENSE-APACHE for the full text of each license.
```

## Common Mistakes

1. **No LICENSE file at all.** Without an explicit license, the code is
   under exclusive copyright — nobody can legally use it. Always include
   a LICENSE file.

2. **LICENSE file doesn't match project config.** The SPDX identifier in
   pyproject.toml/Cargo.toml/package.json should match the LICENSE file.

3. **Using CC licenses for code.** Creative Commons licenses are not
   designed for software. Use BSD-3, MIT, or Apache-2.0 instead.

4. **Copying GPL code into a BSD project.** License compatibility only
   flows one way — permissive into copyleft, not the other way.

5. **Forgetting to update the year.** The copyright year should reflect
   when the code was created. Many projects use a year range (2020-2025)
   and update it annually.

6. **Not checking dependency licenses.** Your project's license must be
   compatible with all dependency licenses. A single GPL dependency makes
   your project effectively GPL.

7. **Custom or modified license text.** Never modify the text of a standard
   license. If you need custom terms, consult a lawyer.

## External Resources

- [Choose a License](https://choosealicense.com/) — Interactive license chooser
- [SPDX License List](https://spdx.org/licenses/) — Canonical license identifiers
- [OSI Approved Licenses](https://opensource.org/licenses/) — Full list of OSI-approved licenses
- [tl;drLegal](https://tldrlegal.com/) — Plain-English license summaries
- [REUSE Specification](https://reuse.software/) — Best practices for license and copyright information
- [GitHub Licensing Guide](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository) — GitHub-specific licensing guidance
- [Scientific Python Development Guide: Licensing](https://learn.scientific-python.org/development/guides/gha-pure/) — Python-specific guidance
- [The Turing Way: Licensing](https://the-turing-way.netlify.app/reproducible-research/licensing.html) — Research software licensing guidance

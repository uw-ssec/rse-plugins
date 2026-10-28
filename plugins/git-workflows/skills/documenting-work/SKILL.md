---
name: documenting-work
description: >-
  Use when finished work needs written reference material in the repository —
  detecting the docs system in use, writing or extending pages, wiring
  navigation, and building to confirm nothing broke. For a choice and its
  rationale, prefer recording-decisions. Triggers: document this, write the
  docs, update the documentation, add a guide, document what we built.
---

# Documenting Work

Documentation that duplicates an existing page is worse than none — now two
pages disagree and neither is trusted. Read what exists before writing.

## Checklist

1. **Detect** the docs system; do not assume one
2. **Gather** what changed
3. **Survey** existing pages for a home
4. **Write** — extend before creating
5. **Wire** navigation
6. **Verify** — build it and fix what breaks
7. **Report**

## 1. Detect the docs system

Look for the config before writing anything:

| Marker | System | Build command |
| --- | --- | --- |
| `mkdocs.yml` | MkDocs | `mkdocs build --strict` |
| `docs/conf.py` | Sphinx | `sphinx-build -W docs docs/_build` |
| `docusaurus.config.js` | Docusaurus | `npm run build` |
| `_quarto.yml` | Quarto | `quarto render` |
| `book.toml` | mdBook | `mdbook build` |
| None of these | Plain Markdown | No build step |

If the project uses a task runner (`pixi.toml`, `Makefile`, `noxfile.py`), prefer
its documented target — `pixi run docs-build`, `make docs` — over calling the
tool directly, so you get the project's real configuration.

If there is no docs system at all, say so and ask where the material should go
rather than inventing a tree.

## 2. Gather what changed

```sh
git log --oneline -20
BASE=$("${CLAUDE_PLUGIN_ROOT}/scripts/default-branch.sh")
git diff "$BASE"...HEAD --stat
```

## 3. Survey before writing

Read the docs index and the section you are about to touch. Decide honestly
whether this extends an existing page or needs a new one. Extending is almost
always right.

## 4. Write

Cover what the material actually calls for — omit what does not apply:

- **What changed** — the capability, the contract, the schema, the config
- **How it fits** — components and data flow; a diagram when relationships are
  the hard part
- **Why it is this way** — trade-offs taken, approaches abandoned and why

Style:

- Level-1 heading, then a 1-2 sentence summary of what the page is for
- Imperative voice in guides: "Run the migration", not "You should run"
- Tables for structured data — config keys, environment variables, field maps
- Never skip heading levels
- Relative links between pages, so they survive a move
- Use the features the detected system actually supports; MkDocs Material
  admonitions inside a Sphinx build render as broken text

## 5. Wire navigation

A page absent from the nav is a page nobody finds. Add it to `mkdocs.yml` nav,
the Sphinx `toctree`, the Docusaurus sidebar — whatever this system uses —
matching the surrounding indentation and naming style.

## 6. Build — the verification gate

Run the build command from step 1. A strict build catches broken links, missing
nav entries, and malformed directives. Fix every error, then build again.

If the project has no build step, verify by reading the rendered Markdown and
checking that each relative link resolves to a file that exists.

## 7. Report

List files created or updated with paths, nav entries added, and the build
result. If the build did not run, say why rather than implying it passed.

## Rules

- Never delete existing documentation — extend or supersede it.
- Read before writing. Duplicate pages are the common failure here.
- Every new page gets a nav entry.
- The build must pass before the work is done.

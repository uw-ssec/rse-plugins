# Supply Chain Security Plugin — Expansion Design

**Date:** 2026-05-14
**Status:** Proposed
**Author:** Cordero Core (with brainstorming assistance)
**Builds on:** PR #102 (`feat/supply-chain-security-skills`) — adds 3 skills
**Related:** UWS-58

---

## Problem

The `supply-chain-security` plugin introduced in PR #102 ships three skills covering hardened CI/CD, dependency security, and threat awareness. The plugin is functional but skill-only — it has no agents to coordinate work, no slash commands for users to invoke, and only one of two structural axes is covered (capability-shaped, no ecosystem-shaped guidance for npm/PyPI/conda/pixi/cargo/Go quirks).

One of the three skills (`supply-chain-threat-awareness`) currently fails the Tessl PR Skill Review with a score of 73 (threshold is 80), blocking PR #102 from merging.

## Goals

1. Expand the plugin into a flagship supply-chain-security capability with agents, commands, and additional skills.
2. Apply progressive disclosure best practices (`references/`, `assets/`) to all new skills and to the failing `supply-chain-threat-awareness` skill.
3. Ensure every changed `SKILL.md` passes the Tessl review (≥80, target ≥85 local).
4. Keep transformation actions safe — read-only by default, dry-run preview before any write.

## Non-goals

- Restructure the two skills already scoring 100 (`supply-chain-hardened-ci-cd`, `supply-chain-dependency-security`). Risk vs reward doesn't justify it; can be a follow-up PR.
- Cover ecosystems beyond npm, PyPI, conda/pixi, cargo, Go in this round (no R/CRAN, no Maven, no NuGet).
- Build a separate `supply-chain-secret-rotation` skill. Rotation lives inside `supply-chain-incident-response/references/secret-rotation.md` and inside future updates to `supply-chain-hardened-ci-cd`.
- Auto-rotate secrets or auto-publish anything. Commands operate on local files only; users remain in control of registry actions.

## Architecture

### Final plugin structure

```
plugins/supply-chain-security/
├── .claude-plugin/plugin.json
├── README.md                                    (updated for new components)
├── agents/
│   ├── supply-chain-security-expert.md          (NEW — always-on lead)
│   └── supply-chain-incident-responder.md       (NEW — IR specialist)
├── commands/
│   ├── supply-chain-audit.md                    (NEW — read-only)
│   ├── supply-chain-incident.md                 (NEW — read-only walkthrough)
│   ├── supply-chain-lockfile-check.md           (NEW — read-only)
│   ├── supply-chain-pin-actions.md              (NEW — dry-run by default)
│   └── supply-chain-harden-workflow.md          (NEW — dry-run by default)
└── skills/
    ├── supply-chain-hardened-ci-cd/             (UNCHANGED — Tessl 100)
    │   └── SKILL.md
    ├── supply-chain-dependency-security/        (UNCHANGED — Tessl 100)
    │   └── SKILL.md
    ├── supply-chain-threat-awareness/           (RESTRUCTURED — fix Tessl 73 → ≥85)
    │   ├── SKILL.md
    │   └── references/campaigns/
    │       ├── shai-hulud.md
    │       ├── teampcp.md
    │       ├── axios.md
    │       └── litellm-pth.md
    ├── supply-chain-sbom-provenance/            (NEW)
    │   ├── SKILL.md
    │   ├── references/
    │   │   ├── sigstore-cookbook.md
    │   │   └── slsa-levels.md
    │   └── assets/sbom-workflow.yml
    ├── supply-chain-incident-response/          (NEW)
    │   ├── SKILL.md
    │   ├── references/
    │   │   ├── runbook-account-takeover.md
    │   │   ├── runbook-tag-hijack.md
    │   │   └── secret-rotation.md
    │   └── assets/incident-report-template.md
    └── supply-chain-ecosystem-quirks/           (NEW)
        ├── SKILL.md
        └── references/
            ├── npm-quirks.md
            ├── pypi-quirks.md
            ├── conda-pixi-quirks.md
            └── cargo-go-quirks.md
```

**Totals added by this design:** 2 agents, 5 commands, 3 new skills, 1 restructured skill, 13 reference docs, 2 assets.

### Component boundaries

| Component | Engages when | Writes files? |
|-----------|--------------|---------------|
| `supply-chain-security-expert` (agent) | Posture audits, hardening recs, advisory work | No (recommends only) |
| `supply-chain-incident-responder` (agent) | Active CVE/advisory/compromise reported | No (recommends only) |
| `/supply-chain-audit` | User audits a repo | No |
| `/supply-chain-incident` | User responds to a named advisory/campaign | No |
| `/supply-chain-lockfile-check` | User checks lockfile health | No |
| `/supply-chain-pin-actions` | Convert mutable refs to SHAs in workflows | Yes, with `--apply` |
| `/supply-chain-harden-workflow` | Apply hardening playbook to one workflow | Yes, with `--apply` |
| All skills | Loaded by agents/commands as needed | N/A |

**Key invariants:**
- Agents never write files directly — all writes go through transformation commands the user invokes.
- Transformation commands always preview a unified diff first; `--apply` is required to write.
- Read-only commands link to transformation commands in their findings (composable workflow).

## Agents

### `supply-chain-security-expert.md` (always-on lead)

Frontmatter (excerpt):
```yaml
name: supply-chain-security-expert
description: Expert in defending research software against 2025-2026 supply-chain attacks. Covers GitHub Actions hardening, dependency hygiene, SBOM/provenance, threat posture, and ecosystem-specific gotchas (npm, PyPI, conda/pixi, cargo, Go).
color: red
model: inherit
skills:
  - supply-chain-hardened-ci-cd
  - supply-chain-dependency-security
  - supply-chain-threat-awareness
  - supply-chain-sbom-provenance
  - supply-chain-ecosystem-quirks
```

**Body sections:** Purpose · Workflow patterns (audit / harden / advise) · Constraints · Decision-making framework · Key preferences · Behavioral traits · Response approach · Escalation strategy · Completion criteria.

**Defers to incident-responder when:** active CVE/advisory/compromise reported; user mentions "we got popped" / "compromised dep" / "need to rotate"; package they depend on is in a published advisory.

**Constraints (non-exhaustive):**
- Read-only by its own actions; never edits files.
- Always recommends `/supply-chain-audit` before recommending `/supply-chain-pin-actions` or `/supply-chain-harden-workflow` (audit-then-fix flow).
- Treats CVE-scanner-clean as necessary, not sufficient.

### `supply-chain-incident-responder.md` (narrow specialist)

Frontmatter (excerpt):
```yaml
name: supply-chain-incident-responder
description: Incident-response specialist for active supply-chain compromises. Engages on Shai-Hulud-style maintainer takeovers, TeamPCP-style tag hijacks, and any active dependency advisory. Owns the lockfile-check → CI-cache-check → secret-rotation → persistence-artifact-hunt runbook end-to-end.
color: red
model: inherit
skills:
  - supply-chain-incident-response
  - supply-chain-dependency-security
  - supply-chain-threat-awareness
  - supply-chain-ecosystem-quirks
```

**Workflow phases:** Triage → Containment → Eradication → Recovery → Post-incident.

**Constraints (non-exhaustive):**
- Always runs the 4-point check (lockfile, CI cache, secrets, persistence) before declaring an incident contained.
- Documents every action for the post-incident report.
- Defers to lead expert for proactive hardening recommendations after the incident is closed.

## Commands

### Read-only

**`/supply-chain-audit [path]`**
- Tools: `Read, Glob, Grep, Bash`
- Walks the repo: `.github/workflows/*.yml`, lockfiles, `package.json` scripts, Python `site-packages/*.pth`, `.npmrc`, secrets in env.
- Output: structured Markdown report — counts per category, FAIL/WARN/PASS table, prioritized findings with `file:line`, top-3 priority actions, links to remediation skills/commands.
- Mirrors `/container-audit` shape.

**`/supply-chain-incident <advisory-or-package>`**
- Tools: `Read, Glob, Grep, Bash, WebFetch`
- Engages incident-responder agent. Argument can be a CVE ID, GHSA, package name, or campaign name.
- Walks user through: confirm scope from advisory → lockfile check → CI cache check → secret rotation prompts → persistence artifact hunt.
- Output: filled-in incident report from `assets/incident-report-template.md`.

**`/supply-chain-lockfile-check [path]`**
- Tools: `Read, Glob, Grep, Bash`
- Narrow: lockfile health only (committed? CI usage? hash-pinned? floating versions? cooldown discipline visible from git history?).
- Output: short Markdown — one section per detected lockfile, PASS/WARN/FAIL on each criterion, recommended fix.

### Transformation (dry-run by default; `--apply` to write)

**`/supply-chain-pin-actions [path] [--apply]`**
- Tools: `Read, Glob, Grep, Edit, Bash, WebFetch`
- Scans `.github/workflows/*.yml`, finds every mutable `uses:` ref (`@v4`, `@main`, `@latest`), resolves each to the 40-char SHA via `gh api repos/<owner>/<repo>/git/refs/tags/<tag>` or `git ls-remote`, adds the tag as a trailing `# v4.2.2` comment.
- Default behavior: prints unified diff per file and stops.
- Refuses to apply if a SHA can't be uniquely resolved.

**`/supply-chain-harden-workflow <path> [--apply]`**
- Tools: `Read, Edit, Bash`
- Targets one workflow file. Applies the hardening playbook from `supply-chain-hardened-ci-cd`: deny-by-default `permissions: {}`, per-job opt-in, two-job build/publish split where appropriate, `--ignore-scripts` on install steps, `harden-runner` step injection, `environment:` gate suggestion on publish job.
- Default behavior: unified diff preview + a "what this changes and why" summary.
- Refuses to apply if the file is too divergent from a recognizable shape.

### Cross-cutting conventions

1. Every command's output contract is part of its `description` so the model produces the right artifact.
2. Transformation commands always preview-then-apply; never silent writes.
3. Read-only commands link to transformation commands in their findings (composable workflow).

## Skills

### Existing skills

- **`supply-chain-hardened-ci-cd/SKILL.md`** — unchanged (Tessl 100).
- **`supply-chain-dependency-security/SKILL.md`** — unchanged (Tessl 100).
- **`supply-chain-threat-awareness/SKILL.md`** — restructured:
  - Add `## Output: Posture Report` section (the missing element that scored it 73).
  - Tighten description to name file paths (`.github/workflows/*.yml`, `package.json`, `pyproject.toml`, `pixi.toml`).
  - Move campaign deep-dives to `references/campaigns/` (one file per campaign), declared in `metadata.references`.
  - SKILL.md keeps a one-paragraph summary of each campaign + the new output contract.

### New skills

All three follow the five-element Tessl bar (see Tessl strategy below). All three use progressive disclosure (`references/`, `assets/` declared in `metadata`).

**`supply-chain-sbom-provenance/SKILL.md`**
- Use when: generating an SBOM, configuring Sigstore signing, verifying a downstream artifact's provenance, evaluating SLSA level for a release pipeline.
- Body: Threat model → Quick decision matrix (npm provenance vs Sigstore vs SLSA generator) → Generation checklist → Verification checklist → `## Output: Provenance Posture Report`.
- `references/sigstore-cookbook.md` — cosign sign/verify recipes, keyless flow with OIDC, transparency log lookup.
- `references/slsa-levels.md` — what each SLSA level (1-4) requires, how to graduate, what's reasonable for research software.
- `assets/sbom-workflow.yml` — drop-in GitHub Actions job (CycloneDX SBOM via syft, Sigstore attestation, release asset upload).

**`supply-chain-incident-response/SKILL.md`**
- Use when: an advisory, CVE, or campaign report names a dependency or action this project uses. Engaged by `/supply-chain-incident` and the incident-responder agent.
- Body: Triage flow → 4-point check (lockfile, CI cache, secrets, persistence) → Containment / Eradication / Recovery / Post-incident phases → `## Output: Incident Report` (filled template).
- `references/runbook-account-takeover.md` — Shai-Hulud-style maintainer compromise (npm focus).
- `references/runbook-tag-hijack.md` — TeamPCP-style retroactive tag mutation; SHA-pinning audit, action repo verification, GitHub Actions cache invalidation.
- `references/secret-rotation.md` — per-platform rotation (PyPI tokens, npm tokens, GitHub Actions secrets, signing keys, cloud creds via OIDC); safe-rotation order; OIDC migration as the durable fix.
- `assets/incident-report-template.md` — Markdown template (scope, timeline, eradication actions, residual risk, prevention items).

**`supply-chain-ecosystem-quirks/SKILL.md`**
- Use when: a recommendation depends on ecosystem specifics.
- Body: Pure progressive-disclosure index. Brief one-paragraph summary per ecosystem, then "load `references/<eco>-quirks.md` for the deep dive." Compact checklist of "which reference applies to your project" + `## Output: Ecosystem Quirks Report`.
- `references/npm-quirks.md` — preinstall/postinstall/install hooks, `.npmrc` knobs, `npm ci` vs `npm install`, npm provenance attestations.
- `references/pypi-quirks.md` — `.pth` files (LiteLLM-class persistence), `setup.py` execution at install, `build_wheel`/`backend-path` in `pyproject.toml`, OIDC trusted publishing recipes.
- `references/conda-pixi-quirks.md` — channel priority and `defaults` channel risk, `pixi.lock` vs `conda-lock.yml`, `--no-deps` and `--no-pin`, signed channel verification status.
- `references/cargo-go-quirks.md` — Cargo `build.rs` arbitrary execution, `.cargo/config.toml` registries, Go `//go:generate` directives, GOPROXY and `GOSUMDB` discipline.

### Skill cross-linking

Cross-links happen in prose, not via shared imports — keeps each skill standalone-readable:
- `supply-chain-incident-response` references campaigns from `supply-chain-threat-awareness`.
- `supply-chain-sbom-provenance` references `supply-chain-hardened-ci-cd`'s two-job split for the publish job.
- `supply-chain-ecosystem-quirks` is referenced by `supply-chain-dependency-security` and `supply-chain-incident-response`.

## Tessl-passing strategy

The Tessl GitHub Action runs on every changed `SKILL.md` and fails if any score is below 80. Threshold is set at the workflow level. Every changed skill must clear 80.

### Five-element bar (every changed/new SKILL.md gets these in this order)

1. **Trigger-rich description** — names file paths, manifest types, or events.
2. **Threat or context paragraph** — one short paragraph framing the *why*, with a concrete campaign or recent CVE as evidence.
3. **Verifiable checklist** — each item answers "what would I run or read to confirm this?"
4. **At least one runnable example** — code block showing bad pattern, good pattern, and diff.
5. **`## Output:` section** — explicit output contract: artifact, sections, fields.

### Per-skill risk + mitigation

| Skill | Risk | Mitigation |
|-------|------|------------|
| `supply-chain-threat-awareness` (restructured) | Low — near-miss at 73 | Add output contract + tighten description |
| `supply-chain-sbom-provenance` (new) | Low — concrete tools, file triggers | All five elements from start |
| `supply-chain-incident-response` (new) | Medium — IR can drift narrative | Phase-ordered checklists + templated output |
| `supply-chain-ecosystem-quirks` (new) | High — short index skill | Compact form of all five elements; explicit ≥85 target |

### Local validation loop

Before push, run `tessl skill review <path>` on each modified/new SKILL.md. Target: every skill ≥85 locally → ≥80 in CI with margin. If any skill scores 70-79 in CI, identify weak element from log and revise. If a skill scores <70, demote to a `references/` doc within a related skill — don't ship as a top-level SKILL.md.

### CI surface area

When the expanded PR opens, Tessl reviews **4 changed SKILL.md files** (threat-awareness modified + 3 new). The two unchanged skills (hardened-ci-cd, dependency-security) are not re-reviewed.

## Implementation order

1. Restructure `supply-chain-threat-awareness` (fix the Tessl 73 first — unblocks PR #102 if shipped standalone).
2. Add the three new skills with full progressive disclosure.
3. Add the two agents.
4. Add the five commands.
5. Update `README.md` and bump `plugin.json` version (0.1.0 → 0.2.0).
6. Run Tessl locally on all 4 changed SKILL.md files.
7. Push and open expanded PR (or update PR #102 in place).

## Open questions

None blocking. Decisions made during brainstorming:
- Scope: comprehensive empire (option C).
- Write model: mixed read-only / write-with-dry-run (option C).
- Skill carving: hybrid capability + ecosystem-quirks reference skill (option C).
- Agent split: lead + incident-responder (option A).
- Existing-skill rework depth: light alignment — fix threat-awareness only (option B).

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Restructured threat-awareness re-scores below 80 | Low | Blocks PR | Local validation gate before push; add more verifiable checklist items |
| `supply-chain-ecosystem-quirks` (short index skill) scores below 80 | Medium | Blocks PR | Pre-push local Tessl run; if <80, fold ecosystem references into `dependency-security/references/` instead of a standalone skill |
| Transformation commands write incorrect changes | Medium | User trust | Dry-run default; refuse-to-apply on ambiguity; explicit `--apply` flag |
| `/supply-chain-pin-actions` resolves wrong SHA for a tag | Low | Silent supply-chain risk | Verify against `git ls-remote` upstream; print resolved SHA in diff for human review |
| Plugin sprawl reduces discoverability | Low | UX | Updated README with clear "when to use what" guide |

## Success criteria

- All 4 changed/new SKILL.md files pass Tessl in CI (≥80, target ≥85 local).
- Both agents load and route to correct skills when invoked.
- All 5 commands are user-invocable and produce documented output.
- Read-only commands never write files.
- Transformation commands never write without `--apply`.
- README documents the full agent/command/skill surface and gives a "when to use what" decision guide.
- Plugin version bumped to 0.2.0.

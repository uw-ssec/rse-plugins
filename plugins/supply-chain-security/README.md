# Supply Chain Security Plugin

A flagship plugin for defending research software projects against the 2025–2026 wave of open-source supply-chain attacks — maintainer account takeovers, release-tag hijacking, lifecycle-script execution, CI secret harvesting, and persistence-on-Python-restart `.pth` injection. Derived from the UW SSEC Open Source Supply Chain Security document.

## Overview

**Version:** 0.2.0

**Contents:**
- 2 Agents: `supply-chain-security-expert` (always-on lead), `supply-chain-incident-responder` (active incidents)
- 5 Commands: `/supply-chain-audit`, `/supply-chain-incident`, `/supply-chain-lockfile-check`, `/supply-chain-pin-actions`, `/supply-chain-harden-workflow`
- 6 Skills: `supply-chain-hardened-ci-cd`, `supply-chain-dependency-security`, `supply-chain-threat-awareness`, `supply-chain-sbom-provenance`, `supply-chain-incident-response`, `supply-chain-ecosystem-quirks`

## Why This Exists

CVE scanners and Dependabot catch known-vulnerable versions. They do **not** catch:

- Maintainer account takeover of a package that was clean yesterday (Shai-Hulud: 500+ npm packages)
- Release-tag hijacking after a legitimate release (TeamPCP: Trivy, Checkmarx, LiteLLM, Bitwarden CLI, SAP CAP)
- Malicious `.pth` files that persist across Python restarts (LiteLLM 1.82.8)
- GitHub Actions `@v4` references silently updated to malicious commits

This plugin provides agents that coordinate the work, slash commands for concrete user actions, and skills that contain the deep checklists, patterns, runbooks, and ecosystem-specific quirks needed to close those gaps.

## When to Use What

| Situation | Start with |
|-----------|------------|
| New project — establish baseline supply-chain posture | `/supply-chain-audit` |
| Reviewing a single workflow file | `supply-chain-hardened-ci-cd` skill |
| Reviewing dependencies or a lockfile | `/supply-chain-lockfile-check` or `supply-chain-dependency-security` skill |
| Got a CVE/GHSA/advisory naming a dep we use | `/supply-chain-incident <id>` |
| Workflows have `@v4` / `@main` / `@latest` refs | `/supply-chain-pin-actions` (dry-run first) |
| Workflow needs hardening (permissions, two-job split, etc.) | `/supply-chain-harden-workflow <file>` (dry-run first) |
| Adding SBOM / Sigstore signing to a release pipeline | `supply-chain-sbom-provenance` skill |
| Question about npm/PyPI/conda/pixi/cargo/Go-specific gotchas | `supply-chain-ecosystem-quirks` skill |

## Agents

### supply-chain-security-expert (always-on lead)

**File:** [agents/supply-chain-security-expert.md](agents/supply-chain-security-expert.md)

Owns proactive posture work, hardening recommendations, SBOM/provenance upgrades, and ecosystem-specific guidance. Read-only by its own actions — writes happen through user-invoked transformation commands. Defers active incidents to the incident responder.

### supply-chain-incident-responder (incident specialist)

**File:** [agents/supply-chain-incident-responder.md](agents/supply-chain-incident-responder.md)

Engages when an advisory, CVE, GHSA, or campaign report names a dependency or GitHub Action this project uses. Owns the lockfile → CI cache → secrets → persistence 4-point check end-to-end and produces a filled incident report.

## Commands

### Read-only

| Command | Purpose |
|---------|---------|
| `/supply-chain-audit [path]` | Full posture audit across workflows, lockfiles, install scripts, persistence vectors. Structured Markdown report with FAIL/WARN/PASS findings. |
| `/supply-chain-incident <id>` | Walk through 4-point check for an advisory/CVE/campaign. Produces a filled incident report. |
| `/supply-chain-lockfile-check [path]` | Narrow lockfile-only health check. |

### Transformation (dry-run by default; `--apply` to write)

| Command | Purpose |
|---------|---------|
| `/supply-chain-pin-actions [path] [--apply]` | Convert mutable `uses:` refs to 40-char SHAs with trailing tag comments. Refuses on branch refs. |
| `/supply-chain-harden-workflow <file> [--apply]` | Apply the hardening playbook to one workflow. Refuses if the workflow needs a manual restructure (e.g., single-job build+publish). |

## Skills

| Skill | Purpose | Progressive disclosure |
|-------|---------|------------------------|
| `supply-chain-hardened-ci-cd` | GitHub Actions release workflow hardening checklist | — |
| `supply-chain-dependency-security` | Dependency and lockfile security review | — |
| `supply-chain-threat-awareness` | Posture assessment against active campaigns | `references/campaigns/` (Shai-Hulud, TeamPCP, axios, LiteLLM .pth), `references/posture-report-template.md` |
| `supply-chain-sbom-provenance` | SBOM generation, Sigstore signing, SLSA levels | `references/` (sigstore cookbook, slsa levels), `assets/sbom-workflow.yml` |
| `supply-chain-incident-response` | IR runbook owning the 4-point check | `references/` (account-takeover runbook, tag-hijack runbook, secret rotation), `assets/incident-report-template.md` |
| `supply-chain-ecosystem-quirks` | Ecosystem-specific install-time execution gotchas | `references/` (npm, PyPI, conda/pixi, cargo, Go quirks) |

## Plugin Structure

```
supply-chain-security/
├── .claude-plugin/plugin.json
├── README.md
├── agents/
│   ├── supply-chain-security-expert.md
│   └── supply-chain-incident-responder.md
├── commands/
│   ├── supply-chain-audit.md
│   ├── supply-chain-incident.md
│   ├── supply-chain-lockfile-check.md
│   ├── supply-chain-pin-actions.md
│   └── supply-chain-harden-workflow.md
└── skills/
    ├── supply-chain-hardened-ci-cd/SKILL.md
    ├── supply-chain-dependency-security/SKILL.md
    ├── supply-chain-threat-awareness/
    │   ├── SKILL.md
    │   └── references/
    │       ├── campaigns/{shai-hulud,teampcp,axios,litellm-pth}.md
    │       └── posture-report-template.md
    ├── supply-chain-sbom-provenance/
    │   ├── SKILL.md
    │   ├── references/{sigstore-cookbook,slsa-levels}.md
    │   └── assets/sbom-workflow.yml
    ├── supply-chain-incident-response/
    │   ├── SKILL.md
    │   ├── references/{runbook-account-takeover,runbook-tag-hijack,secret-rotation}.md
    │   └── assets/incident-report-template.md
    └── supply-chain-ecosystem-quirks/
        ├── SKILL.md
        └── references/{npm,pypi,conda-pixi,cargo-go}-quirks.md
```

## Safety model

- **Agents are read-only.** They recommend, audit, and walk through runbooks — they don't edit files. Writes happen through slash commands the user invokes deliberately.
- **Read-only commands** never modify files: `/supply-chain-audit`, `/supply-chain-incident`, `/supply-chain-lockfile-check`.
- **Transformation commands** preview a unified diff first and require `--apply` to write: `/supply-chain-pin-actions`, `/supply-chain-harden-workflow`. They refuse to write under risky conditions (branch refs, ambiguous SHAs, single-job build+publish workflows).

## License

This plugin is part of the RSE Plugins project and is licensed under the BSD-3-Clause License. See [LICENSE](../../LICENSE) for details.

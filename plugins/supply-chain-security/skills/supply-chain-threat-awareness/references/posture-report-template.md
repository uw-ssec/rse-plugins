# Posture Report Template

Use this template when producing the output of a supply-chain threat-posture review. Fill in every cell — `UNKNOWN` is a valid value when evidence is missing and signals a gap to investigate.

```markdown
## Supply Chain Threat Posture: <project>

### Active Campaign Applicability

| Campaign | Applicable | Evidence |
|----------|------------|----------|
| Shai-Hulud | YES/NO/UNKNOWN | <package and lockfile line, or reason "no npm deps"> |
| TeamPCP | YES/NO/UNKNOWN | <action and workflow line, or reason "no GHA"> |
| axios | YES/NO/UNKNOWN | <package and lockfile line> |
| LiteLLM .pth | YES/NO/UNKNOWN | <Python deps and .pth scan result> |

### Audit Workflow Results

| Step | PASS | WARN | FAIL | Findings |
|------|------|------|------|----------|
| 1 — Lockfile hygiene | <n> | <n> | <n> | <file:line>: <description> |
| 2 — Action pinning | <n> | <n> | <n> | <file:line>: <description> |
| 3 — Install-time execution | <n> | <n> | <n> | <file:line>: <description> |
| 4 — Dependency velocity | <n> | <n> | <n> | <file:line>: <description> |
| 5 — SBOM and provenance | <n> | <n> | <n> | <file:line>: <description> |

### Top 3 Priority Actions

1. <highest-impact remediation> — run `/supply-chain-<command>` or follow `<skill>`
2. <second priority> — <command or skill>
3. <third priority> — <command or skill>
```

## Finding entry rules

For each finding, the entry MUST include:

- Campaign or pattern name (e.g., "TeamPCP — mutable action ref").
- `file:line` citation (the workflow, lockfile, or manifest where the issue lives).
- Blast radius (which secrets/environments would be exposed if exploited).
- Remediation: a specific slash command or skill name (e.g., `/supply-chain-pin-actions`, `supply-chain-hardened-ci-cd`).

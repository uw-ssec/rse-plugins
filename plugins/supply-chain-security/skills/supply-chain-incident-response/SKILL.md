---
name: supply-chain-incident-response
description: Incident-response runbook for supply-chain compromises. Use when an advisory, CVE, GHSA, or campaign report names a dependency or GitHub Action this project uses; when responding to a Shai-Hulud-style maintainer takeover; or when a TeamPCP-style tag hijack is reported. Walks the lockfile-check → CI-cache-check → secret-rotation → persistence-artifact-hunt 4-point check end-to-end.
metadata:
  references:
    - references/runbook-account-takeover.md
    - references/runbook-tag-hijack.md
    - references/secret-rotation.md
  assets:
    - assets/incident-report-template.md
---

# Supply Chain Incident Response

## Threat Model

Scanner-clean post-advisory does not mean clean during the exposure window. The 4-point check (lockfile, CI cache, secrets, persistence) is the irreducible work to determine what the bad version actually touched.

## Triage Flow

Run in order. Each step has a verifying command and a concrete output. Do not advance until the previous step's output is captured.

### Step 1 — Parse the advisory

```bash
# If GHSA: fetch and parse
gh api /advisories/<id> --jq '{summary, affected: .vulnerabilities | map({pkg: .package.name, range: .vulnerable_version_range})}'

# If CVE: lookup on GitHub
gh api search/issues --raw-field q="<cve-id>" --jq '.items[].html_url' | head -5
```

Output: affected package names, version ranges, and exposure window (publish time of bad version → yank time, or now if unyanked).

### Step 2 — Determine when this project resolved the bad version

```bash
# Show lockfile history for the affected package
git log --oneline --follow -p -- <lockfile> | grep -B 2 -E "<affected-package>"
```

Output: commits and timestamps showing when this project pinned the bad version. Cross-reference against the exposure window from Step 1 to confirm overlap. If no overlap → PASS, stop here, document.

Scope determination (which lockfiles even mention the package) is the Lockfile item in the 4-Point Check below — go there next.

## The 4-Point Check

For each item: run the command, record PASS / EXPOSED / UNKNOWN with evidence for the incident report.

1. **Lockfile** — did any of our lockfiles resolve to the affected version?
   ```bash
   # Search every ecosystem's lockfile + manifest in one pass
   for pkg in <pkg1> <pkg2>; do
     git grep -nE "\"$pkg\"|^$pkg\\s|^$pkg==" -- '**/lock*' 'pyproject.toml' 'package.json' 'pixi.toml' 'Cargo.toml' 'go.mod'
   done
   ```
2. **CI cache** — did any workflow cache contain a build that used the affected version during the exposure window?
   ```bash
   gh actions cache list --sort created --order desc --json key,createdAt | jq '.[] | select(.createdAt > "<exposure-start>")'
   ```
3. **Secrets** — what secrets were in scope when the bad version executed?
   ```bash
   gh secret list && grep -rE 'env:|secrets\.' .github/workflows/
   ```
4. **Persistence** — did the bad version leave any artifact that survives?
   ```bash
   # Python .pth
   find $(python -c "import site; print(site.getsitepackages()[0])" 2>/dev/null) -name "*.pth" 2>/dev/null
   # npm bin/
   find node_modules/.bin -type f -newer <date>
   ```

Every result feeds the incident report's 4-Point Check Results table.

## Phases

### Containment

Pin a known-good version in the lockfile. Invalidate every CI cache built during the exposure window (`gh actions cache delete <key>`). Disable any workflow that ran the affected version until eradication is complete (`gh workflow disable <file>`).
Done when: every lockfile pin is updated and every cached artifact from the window is purged.

### Eradication

Rotate every secret enumerated in the 4-point check using `references/secret-rotation.md`. Hunt persistence artifacts using the appropriate runbook: `references/runbook-account-takeover.md` for npm/PyPI maintainer takeover, `references/runbook-tag-hijack.md` for GitHub Action tag hijack.
Done when: every in-scope secret has a new value AND every persistence artifact is removed.

### Recovery

Rebuild the project from the clean lockfile with no caches (`gh workflow run <release> --field skip-cache=true`). Verify the rebuilt artifacts' provenance using the `supply-chain-sbom-provenance` skill if SBOM/attestations are configured.
Done when: rebuilt artifact matches expected provenance and tests pass.

### Post-incident

Fill `assets/incident-report-template.md`. Update posture using the `supply-chain-threat-awareness` skill. File a GHSA at `https://github.com/<owner>/<repo>/security/advisories/new` if this project itself shipped an affected version.
Done when: incident report is complete and prevention items are linked to skills/commands.

## Choose Your Runbook

- Maintainer account takeover (Shai-Hulud-style npm/PyPI compromise) → `references/runbook-account-takeover.md`
- Release tag hijacking (TeamPCP-style GitHub Action mutation) → `references/runbook-tag-hijack.md`
- Secret rotation (every incident, regardless of vector) → `references/secret-rotation.md`

## Output: Incident Report

Produce a filled copy of `assets/incident-report-template.md`. Every section must be populated — leave none as placeholder. Each 4-point check item gets PASS / EXPOSED / UNKNOWN with evidence (`file:line`, run URL, cache key, or "absent") and a follow-up action. Every Prevention Item must link to a skill or `/command` in this plugin.

# Supply Chain Incident Report

**Incident ID:** <unique id, e.g., SC-2026-001>
**Date detected:** <YYYY-MM-DD HH:MM TZ>
**Date contained:** <YYYY-MM-DD HH:MM TZ>
**Date eradicated:** <YYYY-MM-DD HH:MM TZ>
**Date recovered:** <YYYY-MM-DD HH:MM TZ>
**Status:** <Active / Contained / Eradicated / Recovered / Closed>

## Scope

**Advisory or campaign:** <CVE-XXXX-XXXX, GHSA-xxxx-xxxx-xxxx, or campaign name>
**Affected package(s) and version range(s):**
- `<package>` `<range>`

**Exposure window:** <YYYY-MM-DD HH:MM TZ> to <YYYY-MM-DD HH:MM TZ>

**Confirmed exposure:**
- [ ] Lockfile resolved an affected version: <evidence — file:line>
- [ ] CI cache contained an affected version: <evidence — workflow run ID>
- [ ] Workflow execution touched an affected version: <evidence — run URL>
- [ ] Production deployment included an affected version: <evidence>

## 4-Point Check Results

| Check | Status | Evidence | Action |
|-------|--------|----------|--------|
| Lockfile | PASS / EXPOSED / UNKNOWN | <evidence> | <action taken> |
| CI cache | PASS / EXPOSED / UNKNOWN | <evidence> | <action taken> |
| Secrets | PASS / EXPOSED / UNKNOWN | <evidence> | <action taken> |
| Persistence | PASS / EXPOSED / UNKNOWN | <evidence> | <action taken> |

## Timeline

| Time | Event | Actor |
|------|-------|-------|
| <YYYY-MM-DD HH:MM TZ> | <event> | <actor> |

## Eradication Actions

For each: command run, output observed, result.

1. <action>
   - Command: `<command>`
   - Result: <outcome>

## Residual Risk

<Anything not fully eradicated; ongoing monitoring required.>

## Prevention Items

Link each to a skill or command in this plugin:
- [ ] <prevention item> — `<skill or /command>`

## Lessons Learned

<What detection or response gap allowed this; what changes prevent recurrence.>

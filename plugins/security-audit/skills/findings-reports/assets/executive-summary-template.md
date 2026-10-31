# <Infrastructure/Project> Security Audit — Executive Summary

**Date:** <date>
**Scope:** <repos, deployments, integrations audited>
**Method:** static review of all repos + git history; live-fire exploit verification in an isolated local lab (Docker: <stack versions>, shared seeded DB); non-destructive verification suites against live endpoints (user-authorized, scope <A/B>).

---

## Root cause of the incident (if post-incident; CONFIRMED EXPLOITABLE / refuted)

**<CVE/GHSA — severity> — <one-line description>.** <Deployed where, from when until when — the exposure window.> Attack chain, as verified in the lab:

1. <step>
2. <step>
3. <step → impact>

---

## Findings index

| # | Finding | Severity | Status | Report |
|---|---|---|---|---|
| 1 |  | Critical | OPEN | 01 |
| 2 |  | Critical | FIXED-VERIFIED | 02 |
| ... |  |  |  |  |

## What's verified FIXED (live tests)

- <bullet per verified defense, with the probe evidence reference>

## Top priority actions (in order)

1. <the single most urgent action — usually credential rotation in the blast radius>
2. ...
3. ...

<Note on evidence preservation: which logs/tables hold incident evidence and the queries to export them — needed for <billing dispute/forensics> — before any rotation or cleanup.>

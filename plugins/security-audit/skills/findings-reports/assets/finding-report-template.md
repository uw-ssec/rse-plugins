# Finding NN — <Title>

**Severity:** <Critical | High | Medium | Low> (<CVSS vector if applicable>)
**Status:** <OPEN — action required | FIXED-VERIFIED | TRACKING (unfixed upstream, exposure: none/limited)>
**References:** <CVE / GHSA / advisory links, if applicable>

## 1. Vulnerability / finding description

<What it is and the mechanism. For exploitable findings: the exact code path — which function interpolates/mishandles what, reachable from where, authenticated or not. For config/process findings: what control is missing and what it fails to prevent.>

## 2. Files affected

**Upstream (if applicable):**
- `<file>` — <role in the vulnerability>

**Our repos / configs:**
- `<repo>/<file>` — <what shipped/exposed it, since when (commit + date)>

## 3. Evidence

<Labeled excerpts: DB statement log lines, response matrices (payload × status × latency), git-history ciphertext comparisons, header checks. Pull from the evidence package / verification matrix; don't paraphrase the load-bearing lines.>

## 4. Severity rationale

<Why this severity: reachability (unauth?), impact (read/write/escalation/spend), and incident context (was this part of the attack path?).>

## 5. Required actions (if OPEN)

1. <Immediate action, with exact command/config change>
2. <Follow-on: rotation, re-issue, audit of related tables/keys>
3. <Detection: alert/query that would catch this class in future>

## 6. Long-term / process fix

<CI gate, advisory watch, drift lint, per-user keys — the change that prevents recurrence, with file paths where it would live.>

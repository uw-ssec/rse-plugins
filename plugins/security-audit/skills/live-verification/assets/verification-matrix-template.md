# Verification Matrix: <deployment name>

**Date:** <date>
**Endpoint(s):** <urls>
**Scope granted:** <A/B/C from scope-and-consent, per endpoint>
**Deployed version:** <from fingerprint / user statement — mark assumed vs confirmed>

| # | Attack | Payload / method | Result (status / latency / body excerpt) | Verdict |
|---|---|---|---|---|
| 1 | <e.g., SQLi tautology> | `Bearer x' OR '1'='1` | 401, 0.12s, "Virtual Key expected..." | ✅ Blocked |
| 2 | SQLi UNION | | | |
| 3 | SQLi stacked+sleep | | | (no 3s delay → not executed) |
| 4 | Forged JWT alg=none | | | |
| 5 | Admin gating /key/list | | | |
| 6 | SSRF-shaped body | | | |
| 7 | File-read param | | | |
| 8 | Env-credential login | | | |
| 9 | MCP command-exec route | | | |
| 10 | Security headers | (list present/missing) | | ℹ️ finding if missing |
| 11 | Rate limiting (10 rapid 401s) | <wall time, throttle?> | | ⚠️ finding if absent |
| 12 | 401 body leakage | (hash/fragment present?) | | ℹ️ finding if present |

## Timing signature note

<compare live latencies to lab timings; fast rejection vs lab's slow DB-error times>

## Residual advisories (deployed version)

| Advisory | Severity | Fix available | Exposure here |
|---|---|---|---|
|  |  |  |  |

## Conclusion

<one paragraph: what's verified blocked, what remains open, links to findings reports>

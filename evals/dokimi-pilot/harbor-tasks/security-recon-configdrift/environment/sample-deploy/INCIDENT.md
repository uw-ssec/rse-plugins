# Incident context (synthetic)

On Monday 2026-10-26 an attacker began probing our production API gateway.
Logs show repeated SQL-injection-shaped authentication attempts (2,100+),
followed by successful authenticated admin API calls using a stolen virtual
key, and finally exfiltration of our cloud provider credential (upstream
key used by the gateway), which was used for ~$4,000 of fraudulent API
spend. The cloud credential was rotated on 2026-10-29.

Upstream project: `api-gateway` (PyPI). The relevant upstream advisory is
**ADV-2026-0007** (critical; unauthenticated SQL injection in the proxy
API-key verification path; fixed in v2.4.0, published 2026-04-24).

We upgraded the gateway images on 2026-10-30. We want to know what else
needs fixing.

The full history of this repo is in git; the deployed configs are under
`prod/` and `staging/`.

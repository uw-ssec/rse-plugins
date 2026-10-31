# Probe Suites

Runnable patterns for each probe family. All are read-only or auth-failure-only by construction. Adapt paths/fields to the target's framework.

## 1. Fingerprint

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://$EP/health/liveliness
curl -s https://$EP/.well-known/<app>-ui-config        # config booleans (sso? ui? mcp?)
curl -s https://$EP/openapi.json | python3 -c "import json,sys; print(len(json.load(sys.stdin)['paths']), 'routes')"
```

Route inventory: list security-relevant paths (config, key, user, team, sso, mcp, debug, secret, spend, utils, login, password) — each becomes a gating probe.

## 2. Known-payload rejections (the lab's payloads, verbatim)

```python
for name, p in {"tautology": "x' OR '1'='1",
                "subquery": 'x\' OR (SELECT COUNT(*) FROM "Table")>0 AND \'1\'=\'1',
                "union": "x' UNION SELECT 1,2,3--",
                "stacked": "x'; SELECT pg_sleep(3)--"}.items():
    t0=time.time()
    # POST /chat/completions (or the vulnerable route) with Bearer p; record code, latency, body[:150]
```

Verdict per payload: `code in (401,403,400)` AND `latency < ~0.2s` AND body shows pre-DB rejection → blocked.

## 3. Auth-gating sweep

```python
for path in ["/key/list","/user/list","/team/list","/config/list","/spend/logs",
             "/debug/asyncio-tasks","/jwt/key/mapping/list","/config_overrides/vault"]:
    probe(path, hdrs={"Authorization":"Bearer sk-garbage"})   # expect 401
    probe(path)                                               # no auth    expect 401
```

Enterprise-gated features returning 403 "enterprise-only" = not enabled = fine.

## 4. Attack-class spot checks

**Forged JWT** (never a real token):
```python
h = b64(json.dumps({"alg":"none"})); p = b64(json.dumps({"sub":"attacker","scope":"<admin-scope>","exp":9999999999}))
probe("/key/list", hdrs={"Authorization": f"Bearer {h}.{p}."})   # expect 401 + "JWT auth not enabled" (if JWT unused)
```

**SSRF-shaped body / file-read-shaped param** (with garbage key):
```python
probe("/user/update","POST",{"user_id":"x","user_config":{"api_base":"http://169.254.169.254/"}})
probe("/utils/transform","POST",{"vertex_ai_credentials":"/proc/self/environ"})
# expect 401 (auth first) or explicit "not allowed in request body" blocklists
```

**Privilege-escalation shapes** (metadata forging, salt-key confusion) — in the lab by default; live only with explicit per-test consent:
```python
probe("/key/generate","POST",{"metadata":{"secret":'{"user_role":"proxy_admin"}'}})
```

**MCP / command-exec routes:**
```python
probe("/mcp-rest/test/connection","POST",{"command":"id"})     # expect 401
probe("/v1/mcp/registry.json")                                  # expect 404 "not enabled"
```

## 5. Hygiene checks

**Headers:**
```bash
curl -sI https://$EP/ | grep -iE "strict-transport-security|referrer-policy|x-frame-options|content-security-policy|x-content-type-options"
```

**Rate limiting** (time it):
```python
t0=time.time()
for i in range(10):
    probe("/key/list", hdrs={"Authorization": f"Bearer sk-garbage-{i}"})  # count 401s, measure wall time
# no throttle/lockout in ~10 rapid failures → finding
```

**Error leakage:** inspect 401 bodies for `Key Hash (Token) =<sha256>` or key prefix/suffix disclosure — each is an offline-verification oracle finding.

**Login surface:**
```python
probe("/login","POST",{"username":"admin","password":"admin"})        # default creds
probe("/login","POST",{"username":"admin","password":"sk-1234"})      # env-credential login (should be disabled if configured)
```

## Timing-signature cheatsheet

| Observation | Meaning |
|---|---|
| Lab-vuln payload → ~1s+ or clean `pg_sleep` delay | injected SQL executed in DB |
| Same payload live → 401 in ~100ms | blocked pre-DB (good) |
| Same payload live → 401 but ~1s | possibly reaching vulnerable code, failing later — investigate |
| UNION errors in lab vs clean 401 live | parameterization present |

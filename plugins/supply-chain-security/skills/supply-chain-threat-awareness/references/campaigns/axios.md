# axios Campaign

**Vector:** Maintainer account compromise; malicious version pushed to npm registry.
**Scale:** axios has ~100M weekly npm downloads — exposure is essentially the entire JS ecosystem.

## Attack mechanics

1. Maintainer account compromised (mechanism varies — phishing, leaked token, weak 2FA).
2. Malicious patch version published to the npm registry.
3. Any project resolving `^x.y.z` or running `npm install` (without lockfile or `npm ci`) within the window pulls the bad version.

## Indicators of exposure

- Lockfile resolved an affected axios version.
- A CI build ran `npm install` (not `npm ci`) during the attack window.

## Containment checklist

- [ ] Pin axios to a known-good version in the lockfile.
- [ ] Switch `npm install` to `npm ci` everywhere in CI.
- [ ] Verify no `postinstall` ran with secrets in scope.
- [ ] Monitor npm provenance feed for any future releases.

## References

- `supply-chain-dependency-security` skill (lockfile patterns)
- npm provenance/audit feeds

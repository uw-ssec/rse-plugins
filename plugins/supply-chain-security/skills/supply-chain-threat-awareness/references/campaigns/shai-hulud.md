# Shai-Hulud Campaign

**Vector:** Maintainer account takeover of legitimate npm packages.
**Scale:** 500+ packages compromised.
**Targeting:** Widely-used transitive dependencies (high blast radius via dependency graph).
**Detection gap:** Packages appear legitimate; no CVE issued at time of attack. Scanners that compare against published advisories miss the live window.

## Attack mechanics

1. Attacker phishes or credential-stuffs a maintainer's npm account.
2. Publishes a malicious patch version of one or more packages the maintainer owns.
3. Payload typically: postinstall script that exfiltrates env vars (CI tokens, npm tokens, GitHub tokens) to an attacker-controlled endpoint.
4. Within hours, npm registry yanks the version once reported — but caches and lockfiles already pin the bad version downstream.

## Indicators of exposure

- Lockfile resolved a version of an affected package within the attack window.
- CI cache contains a `node_modules/` directory built from the affected version.
- A `postinstall` script ran in any environment with secrets.

## Containment checklist

- [ ] Identify affected version range from the advisory.
- [ ] `grep -r '"<package>": ' package-lock.json yarn.lock` to confirm pin.
- [ ] Invalidate CI cache scoped to the lockfile hash.
- [ ] Rotate every secret accessible from any CI run after the bad version was pinned.
- [ ] Run `npm ci --ignore-scripts` going forward; pin to a known-good prior version.

## References

- npm registry advisory feed
- `supply-chain-incident-response/references/runbook-account-takeover.md`

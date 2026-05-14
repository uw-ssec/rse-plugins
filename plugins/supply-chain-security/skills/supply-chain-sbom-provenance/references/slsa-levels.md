# SLSA Build Levels for Research Software

## What SLSA Is

SLSA (Supply-chain Levels for Software Artifacts) is a graduated framework for build-provenance maturity. Each level adds verifiable claims about how an artifact was produced: that it was built at all (L1), that the build platform is trusted and the provenance is signed (L2), and that the build is hermetic and the provenance unforgeable (L3). Higher levels reduce the set of trusted parties a downstream consumer must rely on.

## SLSA Build L1

**Requires:** Provenance exists — a document describes how the artifact was built. Provenance may be unsigned and may originate from any environment, including a developer's laptop.

**The project must:** Generate a provenance document at release time (even by hand: which commit, which command, which timestamp). Publish it alongside the artifact.

**Reasonable for:** Getting started. Surface area for an attacker is identical to L0 (anyone with publish credentials can lie), but the consumer at least has something to inspect.

## SLSA Build L2

**Requires:** Provenance is **signed** by the build platform, and the build runs on a **hosted, trusted build service** (GitHub Actions, GitLab CI, Google Cloud Build, etc. — not a developer laptop). The provenance binds the artifact digest to the source commit and the build pipeline definition.

**The project must:** Use GitHub Actions with `actions/attest-build-provenance` (writes to the GitHub attestation API) **or** sign artifacts with cosign keyless via OIDC. No long-lived signing keys needed; Sigstore handles certificate issuance and Rekor handles the transparency log. Verify with `gh attestation verify` or `cosign verify-blob`.

**Reasonable for:** Most research software releases. Effort: one workflow step. Catches tag hijacking, account takeover on the maintainer's local box, and most release-asset tampering scenarios.

## SLSA Build L3

**Requires:** Hermetic, isolated build environment — the build cannot reach the network mid-build except to fetch the explicitly declared inputs, and cannot influence subsequent builds. Provenance is **non-falsifiable**: the build platform's signing key is not accessible to the build job itself, so a compromised build script cannot forge its own attestation. Two-party control on pipeline changes.

**The project must:** Beyond L2, isolate the build (no `curl | bash` mid-build; declare all deps in the lockfile and let the build platform fetch them in a controlled step), pin the pipeline definition itself by SHA, and use a build platform that signs out-of-band (GitHub's attest-build-provenance qualifies in many configurations; bespoke runners do not).

**Reasonable for:** Security-critical packages and security tooling itself — code signing tools, SBOM generators, CVE scanners, auth libraries. The blast radius of compromise justifies the engineering cost.

## Recommendation for Research Software

**Default target: L2.** Almost every project benefits and the cost is one workflow step. Use `actions/attest-build-provenance` or cosign keyless via GitHub OIDC.

**Target L3 if** the project itself is security tooling — for example, a plugin that audits supply-chain posture, a key-management library, or a signature-verification tool. Downstream consumers of security tooling have outsized trust placed in it, and the project should match that trust with L3-grade provenance.

For the workflow patterns that achieve L2/L3 (action pinning, hardened runners, hermetic builds), cross-reference the `supply-chain-hardened-ci-cd` skill.

## Common Pitfalls

- **Building outside CI** — releases assembled on a maintainer's laptop have no verifiable provenance. Even if signed, the cert binds to the maintainer's personal identity, not a build pipeline. Stays at L1 regardless of how strong the signature is.
- **Signing locally with a personal key** — bypasses Sigstore's transparency log and ties release integrity to one person's key hygiene. L1 at best. Move signing into CI.
- **Not pinning the build pipeline itself** — workflow uses `actions/checkout@main`. The pipeline definition is part of the trusted compute base; if it floats, your attestation reflects whatever `@main` happened to be at build time. Required for L3, recommended at L2. Use SHA pins with version comments.
- **Not publishing provenance** — generating an attestation that never leaves the runner is functionally L0. Upload to the GitHub attestation API (`actions/attest-build-provenance` does this automatically) or attach the `.sigstore` bundle to the release.
- **Confusing "signed release" with "signed provenance"** — signing the tarball proves *someone with the key* produced it. Signing the provenance (which binds tarball-digest → commit → workflow-run-id) proves *which build* produced it. L2 requires the latter.

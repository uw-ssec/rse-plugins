# Audit a small deployment repo after an incident

`/app/deploy` is a git repository with two environments (`prod/`, `staging/`)
of an API gateway deployment, plus an incident write-up (`INCIDENT.md`).

The incident: an attacker exploited the gateway (see `INCIDENT.md` for the
upstream advisory reference). The team upgraded the gateway images on
2026-10-30 and rotated the cloud provider credential. They want a security
reconnaissance review of what *else* needs fixing.

Perform a recon-only audit (no network access is available; do not attempt
to reach any live service):

1. Review the deployment configs in `prod/` and `staging/` for weaknesses,
   including drift between the two environments.
2. Review the git history of this repository for security-relevant facts,
   especially whether secrets were rotated after the incident.
3. Connect the version history to the upstream advisory timeline in
   `INCIDENT.md`.

Write your findings to `/app/deploy/audit-report.md` as a numbered list of
findings. For each finding include: a short title with severity, one or two
sentences describing the problem with the specific file(s) affected, and a
one-line recommended action. Findings should be concrete and tied to
evidence in the repo (file paths, git history, ciphertext, versions).

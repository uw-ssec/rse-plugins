# Report Writing Guide

Notes on the judgments the templates don't capture.

## Lead with the decision, support with the evidence

Each finding report exists so someone can act. The first sentence states the finding; the severity/status header states the urgency; everything after is the justification. A reader who stops after the header should still make the right call.

## Severity calibration

Severity is about *this deployment's* exposure, not the advisory's CVSS alone:

- An advisory scored 9.8 with no reachable path in this deployment (feature disabled, route 404) is a TRACKING note, not a Critical.
- A CVSS-7 config gap that was *the* enabler of a real incident (e.g., no rate limiting → 2,100 unnoticed injection attempts) earns its Medium-plus with incident context.
- Process findings (six-month upgrade lag) can be Critical *as process* — they're what turn known-and-fixed upstream bugs into incidents. Label them clearly ("Critical (process)") so they aren't dismissed as not-a-bug.

## Status honesty

- "FIXED-VERIFIED" requires behavior evidence (lab A/B or live probe), not just "we merged the upgrade commit".
- "Fixed" without verification is "FIXED-UNVERIFIED" — schedule the verification; say so in the report.
- "OPEN" findings each carry a concrete action; an OPEN finding without a next step is a complaint, not a finding.

## The verification record is a deliverable

After an incident, the team's anxious question is "are they still in?" The verification-record report (attack matrix, everything blocked, with timings) answers it with evidence. Write it deliberately, not as an appendix.

## Evidence preservation section (post-incident only)

Where relevant, a finding or the exec summary includes the forensic-export queries — spend logs that captured attacker payloads, error logs, tables to audit for attacker-inserted rows — explicitly ordered *before* rotation steps, and framed as export (SELECT), never cleanup (DELETE/TRUNCATE). Note what the evidence supports (billing dispute, timeline reconstruction) so nobody destroys it to "tidy up".

## Writing mechanics

- Quote log lines and ciphertexts verbatim in fenced blocks; summarize everything else.
- Dates and commit hashes everywhere — drift and rotation findings live on them.
- Put per-finding caveats inline ("extraction raced by async writers; oracle itself proven") — a caveat next to a claim reads as rigor, one at the end of the report reads as doubt.
- Cross-reference reports by number ("see report 02") — the set should read as a unit.
- End every OPEN-critical report with the exact next command the operator should run.

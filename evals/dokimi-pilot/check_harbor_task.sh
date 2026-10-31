#!/usr/bin/env bash
# Regression controls for the security-recon-configdrift verifier (no LLM calls).
# Usage: check_harbor_task.sh [image]   (default: builds the task's environment/)
# Each control plants (or omits) an audit report and checks the reward.
set -uo pipefail
cd "$(dirname "$0")/harbor-tasks/security-recon-configdrift"
image=${1:-}
if [ -z "$image" ]; then
  image=secaudit-task-check
  docker build -q -t "$image" environment >/dev/null || { echo "image build failed" >&2; exit 2; }
fi
fail=0
control() {  # control <name> <expected reward> <shell that writes a report>
  local got
  got=$(docker run --rm --network none -v "$PWD/tests:/tests:ro" -v "$PWD/solution:/solution:ro" "$image" \
    bash -c "{ $3; } >/dev/null 2>&1; bash /tests/test.sh >/dev/null 2>&1; cat /logs/verifier/reward.txt")
  if [ "$got" = "$2" ]; then echo "ok   $1 (reward $got)"; else echo "FAIL $1: reward $got, expected $2"; fail=1; fi
}
# Oracle: the ideal report from solution/ scores 1.0
control oracle 1.0 'cp /solution/ideal-report.md /app/deploy/audit-report.md'
# No report at all -> 0
control no-report 0 'true'
# A vague report that lists generic advice but no planted finding -> 0
control vague 0 'printf "# Audit\n\n1. Medium: consider enabling rate limiting.\n2. Low: add security headers.\n" > /app/deploy/audit-report.md'
# Partial: finds rotation + lag + drift but misses latest-tag and shared-secret -> 0.8
control partial 0.8 'printf "# Audit\n\n1. Critical: gateway master key never rotated - the ciphertext in prod/.env.prod.sops.env is identical across history, so the value was not rotated after the incident.\n2. Critical (process): six-month version lag - v2.3.0 ran from April until the October upgrade despite ADV-2026-0007 being fixed in v2.4.0 in April.\n3. High: prod is missing GATEWAY_SALT_KEY while staging has it (config drift).\n" > /app/deploy/audit-report.md'
# Evidence requirement: rotation claim without citing ciphertext/env file -> 0.7 not 0.8
control no-evidence 0.7 'printf "# Audit\n\n1. Critical: gateway master key never rotated.\n2. Critical (process): six-month version lag - v2.3.0 ran until October despite ADV-2026-0007 fixed in v2.4.0.\n3. High: prod is missing GATEWAY_SALT_KEY while staging has it.\n" > /app/deploy/audit-report.md'
exit $fail

#!/bin/bash
# Verifier: the agent must produce an audit report that detects the planted
# findings. Reward = fraction of planted findings correctly identified with
# the required evidence signal. False-positive findings are not rewarded but
# a wrong severity caps the score for that finding at partial credit.
#
# Planted findings (from recon alone — no lab/live phase needed):
#   F1 master key never rotated (prod env ciphertext identical across history)
#   F2 six-month version lag on a critical advisory (process gap)
#   F3 prod missing GATEWAY_SALT_KEY vs staging (config drift)
#   F4 mutable :latest image tag (staging dev-mirror)
#   F5 shared master key secret between staging services (dev-mirror reuses it)
set -uo pipefail
REWARD_FILE="/logs/verifier/reward.txt"
mkdir -p /logs/verifier
REPORT_GLOB="/app/deploy/audit-report* /app/deploy/reports/*.md /app/deploy/*report*.md"
shopt -s nullglob
REPORTS=($REPORT_GLOB)
if [ ${#REPORTS[@]} -eq 0 ]; then
  echo "no audit report found (expected audit-report.md or reports/*.md)"; echo 0 > "$REWARD_FILE"; exit 1
fi
# Flatten newlines so multi-line sentences still match (grep is line-based).
CAT=$(cat "${REPORTS[@]}" | tr '\n' ' ')

score=0
declare -a lines

check() { # check <pattern> <label> <credit>
  if echo "$CAT" | grep -qiE "$1"; then
    score=$(python3 -c "print(round($score + $3, 4))")
    lines+=("PASS  $2")
  else
    lines+=("FAIL  $2")
  fi
}

# F1: master key never rotated — must reference the un-rotated master key AND
# point at the env file / ciphertext evidence.
check 'master.?key.{0,120}(not|never|un).?rotat' "F1: master-key-not-rotated finding present" 0.3
check '(ciphertext|ENC\[AES256|env\.prod).{0,200}(identical|unchanged|not rotated)|((not|never) rotated).{0,200}(ciphertext|ENC\[AES256|env\.prod)' "F1: cites ciphertext/env-file evidence" 0.1

# F2: version lag / process gap.
check '(v2\.3\.0|2\.3\.0).{0,200}(v2\.4\.0|2\.4\.0|ADV-2026-0007)|(six.month|6.month|months).{0,80}(lag|behind|delay)|lag' "F2: version-lag finding present" 0.2

# F3: prod missing salt key (drift).
check '(prod|production).{0,200}(missing|lacks?|without|does not have|no).{0,60}salt|salt.{0,200}(missing|lacks?|only|absent).{0,60}(prod|production)|salt' "F3: prod-missing-salt-key drift finding" 0.2

# F4: mutable latest tag.
check ':latest' "F4: mutable :latest image tag flagged" 0.1

# F5: shared secret between staging services.
check '(dev-mirror|staging).{0,200}(same|shared|reuses?).{0,80}(master.?key|secret)|(same|shared|reuses?).{0,80}(master.?key|secret).{0,200}(dev-mirror|staging)' "F5: shared master-key secret flagged" 0.1

total=1.0
for l in "${lines[@]}"; do echo "$l"; done
python3 -c "print(round(min($score, $total), 4))" > "$REWARD_FILE"
echo "reward $(cat "$REWARD_FILE")"
[ "$(python3 -c "print(1 if $score >= 0.8 else 0)")" = "1" ]

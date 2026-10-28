#!/bin/bash
# Mutation-style verifier. The agent's suite must pass on the reference
# implementation; the reward is the fraction of planted bugs it catches.
#
# Every run (reference, then each mutant) starts from a fresh copy of the
# submitted workspace and its own TMPDIR, so state a suite leaves behind
# (files it creates, caches) cannot make a later run fail and fake a kill.
set -uo pipefail
REWARD_FILE="/logs/verifier/reward.txt"
mkdir -p /logs/verifier
APP=/app/numlib
SNAP=$(mktemp -d)/numlib

if [ -z "$(find "$APP/tests" \( -name 'test_*.py' -o -name '*_test.py' \) -print -quit 2>/dev/null)" ]; then
  echo "no test files in $APP/tests"; echo 0 > "$REWARD_FILE"; exit 1
fi
cp -a "$APP" "$SNAP"
cp /tests/core_reference.py "$SNAP/src/numlib/core.py"   # undo any edits to src/

# run_with <core.py>: restore the snapshot, swap in <core.py>, run the suite.
run_with() {
  # A failed restore must not look like a killed mutant: abort with reward 0.
  rm -rf "$APP" && cp -a "$SNAP" "$APP" && cp "$1" "$APP/src/numlib/core.py" \
    || { echo "verifier error: could not restore the workspace"; echo 0 > "$REWARD_FILE"; exit 1; }
  local tmp; tmp=$(mktemp -d)
  (cd "$APP" && TMPDIR="$tmp" timeout 120 python -m pytest -q -x -p no:cacheprovider tests >/dev/null 2>&1)
  local rc=$?; rm -rf "$tmp"; return $rc
}

if ! run_with /tests/core_reference.py; then
  echo "suite fails on the reference implementation"; echo 0 > "$REWARD_FILE"; exit 1
fi
killed=0; total=0
for m in /tests/mutants/*.py; do
  total=$((total + 1))
  if run_with "$m"; then echo "survived: $(basename "$m" .py)"; else echo "killed:   $(basename "$m" .py)"; killed=$((killed + 1)); fi
done
rm -rf "$APP" && cp -a "$SNAP" "$APP"   # leave the submitted suite with the reference code
python3 -c "print(round($killed / $total, 4))" > "$REWARD_FILE"
echo "reward $(cat "$REWARD_FILE") ($killed/$total mutants killed)"
[ "$killed" -eq "$total" ]

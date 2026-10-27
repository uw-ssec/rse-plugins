#!/bin/bash
# Mutation-style verifier. The agent's suite must pass on the reference
# implementation; the reward is the fraction of planted bugs it catches.
set -uo pipefail
REWARD_FILE="/logs/verifier/reward.txt"
mkdir -p /logs/verifier
CORE=/app/numlib/src/numlib/core.py
run_suite() { (cd /app/numlib && timeout 120 python -m pytest -q -x -p no:cacheprovider tests >/dev/null 2>&1); }

if [ -z "$(find /app/numlib/tests \( -name 'test_*.py' -o -name '*_test.py' \) -print -quit 2>/dev/null)" ]; then
  echo "no test files in /app/numlib/tests"; echo 0 > "$REWARD_FILE"; exit 1
fi
cp /tests/core_reference.py "$CORE"   # undo any edits to src/
if ! run_suite; then
  echo "suite fails on the reference implementation"; echo 0 > "$REWARD_FILE"; exit 1
fi
killed=0; total=0
for m in /tests/mutants/*.py; do
  total=$((total + 1))
  cp "$m" "$CORE"
  if run_suite; then echo "survived: $(basename "$m" .py)"; else echo "killed:   $(basename "$m" .py)"; killed=$((killed + 1)); fi
done
cp /tests/core_reference.py "$CORE"
python3 -c "print(round($killed / $total, 4))" > "$REWARD_FILE"
echo "reward $(cat "$REWARD_FILE") ($killed/$total mutants killed)"
[ "$killed" -eq "$total" ]

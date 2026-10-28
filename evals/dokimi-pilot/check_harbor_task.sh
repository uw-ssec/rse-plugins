#!/usr/bin/env bash
# Regression controls for the python-testing-numlib verifier (no LLM calls).
# Usage: check_harbor_task.sh [image]   (default: builds the task's environment/)
# Each control runs a known test suite through tests/test.sh and checks the reward.
set -uo pipefail
cd "$(dirname "$0")/harbor-tasks/python-testing-numlib"
image=${1:-}
if [ -z "$image" ]; then
  image=numlib-task-check
  docker build -q -t "$image" environment >/dev/null || { echo "image build failed" >&2; exit 2; }
fi
fail=0
control() {  # control <name> <expected reward> <shell that writes a suite>
  local got
  got=$(docker run --rm --network none -v "$PWD/tests:/tests:ro" -v "$PWD/solution:/solution:ro" "$image" \
    bash -c "{ $3; } >/dev/null 2>&1; bash /tests/test.sh >/dev/null 2>&1; cat /logs/verifier/reward.txt")
  if [ "$got" = "$2" ]; then echo "ok   $1 (reward $got)"; else echo "FAIL $1: reward $got, expected $2"; fail=1; fi
}
control oracle 1.0 'bash /solution/solve.sh'
control no-tests 0 'true'
control stateless-smoke 0.0 'mkdir -p tests && printf "from numlib import trapezoid\ndef test_runs():\n    trapezoid([0,1],[0,1])\n" > tests/test_smoke.py'
# A suite that only passes on its first run must not fail every mutant run.
control stateful-cwd 0.0 'mkdir -p tests && printf "from pathlib import Path\ndef test_once():\n    Path(\"suite-created-file\").touch(exist_ok=False)\n" > tests/test_state.py'
control stateful-tmpdir 0.0 'mkdir -p tests && printf "import tempfile\nfrom pathlib import Path\ndef test_once():\n    Path(tempfile.gettempdir(), \"marker\").touch(exist_ok=False)\n" > tests/test_state.py'
exit $fail

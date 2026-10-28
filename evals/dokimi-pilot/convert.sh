#!/usr/bin/env bash
# Build dokimi inputs for the pilot skills into out/<skill>/.
set -euo pipefail
testcases=$(cd "${1:?usage: convert.sh <rse-plugins-testcases checkout>}" && pwd)
[ -d "$testcases/plugins" ] || { echo "not a testcases checkout: $testcases" >&2; exit 1; }
cd "$(dirname "$0")"
# Skill catalog for trigger sets: the two plugin trees only (copied, since
# dokimi does not follow symlinks and .pixi/ vendors unrelated SKILL.md files).
catalog=$(mktemp -d)
trap 'rm -rf "$catalog"' EXIT
cp -R ../../plugins ../../community-plugins "$catalog/"
while read -r skill path; do
  extra=()
  if [ -f "cases/$skill/quality-extra.json" ]; then extra=(--extra-quality "cases/$skill/quality-extra.json"); fi
  # design-tokens has no rse-plugins-testcases cases; its quality set is extras only.
  if [ "$skill" = design-tokens ]; then extra+=(--no-testcases); fi
  python testcases_to_dokimi.py --testcases "$testcases" --skill-path "$path" \
    --trigger "cases/$skill/trigger.json" ${extra[@]+"${extra[@]}"} --out "out/$skill"
  dokimi questions import "out/$skill/evals.json" -o "out/$skill/questions.v2.json"
  # Lints the queries against the catalog and writes the skill-catalog: arm input.
  dokimi catalog trigger-set --catalog "$catalog" --trigger-set "out/$skill/trigger.reach.json" \
    --format questions --strict --out "out/$skill/trigger.questions.json"
done <<'SKILLS'
pixi-package-manager plugins/scientific-python-development/skills/pixi-package-manager
python-testing plugins/scientific-python-development/skills/python-testing
design-tokens plugins/uiux-design-team/skills/design-tokens
SKILLS

#!/usr/bin/env bash
# Free lexical (BM25) routing floor for each pilot skill against the full
# catalog. Add --model/--provider (and --max-usd) for the model-backed run.
set -euo pipefail
cd "$(dirname "$0")"
repo=$(cd ../.. && pwd)
# The catalog is the two plugin trees only; other SKILL.md files under the
# repo (e.g. ones vendored in .pixi/) are not competitors.
catalog=$(mktemp -d)
trap 'rm -rf "$catalog"' EXIT
cp -R "$repo/plugins" "$repo/community-plugins" "$catalog/"  # dokimi does not follow symlinks
while read -r skill path; do
  dokimi novelty routing --artifact "skill:$repo/$path" --catalog "$catalog" \
    --queries "cases/$skill/routing-queries.json" --out "out/$skill/routing-bm25" "$@"
done <<'SKILLS'
pixi-package-manager plugins/scientific-python-development/skills/pixi-package-manager
python-testing plugins/scientific-python-development/skills/python-testing
design-tokens plugins/uiux-design-team/skills/design-tokens
SKILLS

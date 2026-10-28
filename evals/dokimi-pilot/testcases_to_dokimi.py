"""Convert rse-plugins-testcases YAML and pilot trigger sets to dokimi inputs.

Quality: every ``expect_skill: true`` case in <testcases>/<skill path>/evals/*.yaml
(plus optional extra cases from a JSON list of {id, prompt, criteria}) becomes a
row of a skill-creator ``evals.json``; ``dokimi questions import`` reads that
into questions.v2, with ``criteria`` as the grading expectations.

Trigger: a JSON list of {id, prompt, expected_skill} becomes a google/skill-reach
QuerySet, which the ``skill-catalog:`` arm reads. ``expect_skill: false``
testcases join it as ``expected_skill: null`` negatives.

Usage:
  python testcases_to_dokimi.py --testcases DIR --skill-path plugins/x/skills/y \
      [--no-testcases] [--extra-quality extra.json] [--trigger trigger.json] --out OUTDIR

A skill must have testcases under <testcases>/<skill path>/evals/ unless
--no-testcases says it has none on purpose.
"""

import argparse
import json
from pathlib import Path

import yaml


def load_testcases(root: Path, skill_path: str, allow_missing: bool) -> list[dict]:
    evals = root / skill_path / "evals"
    files = sorted(evals.glob("*.y*ml"))
    if not files:
        # A missing or empty directory would silently shrink the evaluation.
        if allow_missing:
            return []
        raise SystemExit(f"{evals}: no testcases (pass --no-testcases if the skill has none)")
    cases = []
    for path in files:
        case = yaml.safe_load(path.read_text())
        missing = {"prompt", "criteria", "expect_skill"} - set(case)
        if missing:
            raise SystemExit(f"{path}: missing {sorted(missing)}")
        cases.append({"id": path.stem, **case})
    return cases


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--testcases", type=Path, required=True)
    ap.add_argument("--skill-path", required=True)
    ap.add_argument("--no-testcases", action="store_true",
                    help="the skill has no rse-plugins-testcases cases; use --extra-quality only")
    ap.add_argument("--extra-quality", type=Path)
    ap.add_argument("--trigger", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    skill = Path(args.skill_path).name
    cases = load_testcases(args.testcases, args.skill_path, args.no_testcases)
    if args.extra_quality:
        cases += [{**c, "expect_skill": True} for c in json.loads(args.extra_quality.read_text())]

    evals = [
        {"id": i, "name": c["id"], "prompt": c["prompt"], "expectations": list(c["criteria"])}
        for i, c in enumerate((c for c in cases if c["expect_skill"]), start=1)
    ]
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "evals.json").write_text(json.dumps({"skill_name": skill, "evals": evals}, indent=1))

    queries = []
    if args.trigger:
        queries = [
            {"query_id": q["id"], "text": q["prompt"], "expected_skill": q["expected_skill"],
             **({"kind": "out_of_scope"} if q["expected_skill"] is None else {})}
            for q in json.loads(args.trigger.read_text())
        ]
    queries += [
        {"query_id": f"testcases-{c['id']}", "text": c["prompt"], "expected_skill": None, "kind": "out_of_scope"}
        for c in cases if not c["expect_skill"]
    ]
    if queries:
        query_set = {"catalog_id": "rse-plugins", "queries": queries}
        (args.out / "trigger.reach.json").write_text(json.dumps(query_set, indent=1))
    print(f"{skill}: {len(evals)} quality cases, {len(queries)} trigger queries")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Helpers for the skill quality-check PR workflow (skill-quality-check.yml).

select     Print the skill directories a pull request touches, one per line.
           A skill is plugins/<plugin>/skills/<skill>/ or the same under
           community-plugins/, and counts only if its SKILL.md still exists
           (a deleted skill has nothing to score). When the gate itself
           changed (the workflow or this script), every skill is selected so
           the new gate is exercised on the whole catalog.

summarize  Read each skill's skillevaluator-quality.json and print a Markdown
           table for the job summary. Exits 1 unless every skill's checker
           exited 0 and its report says it passed, so a crash, a missing
           report or a stale one can't pass silently.

Usage:
    python skill-quality.py select --base <sha> --head <sha> [--root .]
    python skill-quality.py summarize --reports <dir> --skills <file> --exits <file> --min-score 70
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SKILL_DIR = re.compile(r"^((?:community-)?plugins/[^/]+/skills/[^/]+)/")
GATE_FILES = {".github/workflows/skill-quality-check.yml", ".github/scripts/skill-quality.py"}


def changed_files(root: Path, base: str, head: str) -> list[str]:
    """Paths changed between the merge base of base and head, and head.

    --no-renames reports a move as a delete plus an add, so the skill a file
    left is selected as well as the one it moved into.
    """
    out = subprocess.run(
        ["git", "diff", "--name-only", "--no-renames", "-z", f"{base}...{head}"],
        cwd=root, check=True, capture_output=True, text=True,
    ).stdout
    return [p for p in out.split("\0") if p]


def all_skills(root: Path) -> list[str]:
    return sorted(
        str(p.parent.relative_to(root))
        for top in ("plugins", "community-plugins")
        for p in (root / top).glob("*/skills/*/SKILL.md")
    )


def select(root: Path, paths: list[str]) -> list[str]:
    if GATE_FILES & set(paths):
        return all_skills(root)
    dirs = {m.group(1) for p in paths if (m := SKILL_DIR.match(p))}
    return sorted(d for d in dirs if (root / d / "SKILL.md").is_file())


def report_name(skill_dir: str) -> str:
    """Report subdirectory for a skill; the full path keeps same-named skills apart."""
    return skill_dir.replace("/", "__")


def read_exits(path: Path) -> dict[str, int]:
    """skill<TAB>exit-code lines written by the workflow's run step."""
    exits = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        skill, _, code = line.rpartition("\t")
        if skill:
            exits[skill] = int(code)
    return exits


def summarize(reports: Path, skills: list[str], min_score: int, exits: dict[str, int]) -> tuple[str, bool]:
    """A skill passes only if quality-check exited 0 *and* its report says it passed.

    Requiring both means neither a crash next to a stale report nor a report
    that is missing can turn into a pass.
    """
    lines = [
        f"### Skill quality check (SkillEvaluator `quality-check`, min score {min_score})",
        "",
        "| Skill | Score | Grade | Result |",
        "| --- | ---: | :---: | --- |",
    ]
    ok = True
    for skill in skills:
        code = exits.get(skill)
        report = reports / report_name(skill) / "skillevaluator-quality.json"
        try:
            data = json.loads(report.read_text(encoding="utf-8"))
            summary = data["quality_summary"][0]
            score, grade, passed = summary["overall_score"], summary["grade"], bool(data["overall_passed"])
        except (OSError, ValueError, KeyError, IndexError, TypeError):
            lines.append(f"| `{skill}` | — | — | ❌ no readable report (checker exit {code}) |")
            ok = False
            continue
        if code is None:
            result = "❌ checker did not run"
        elif not passed:
            result = "❌ below min score"
        elif code != 0:
            result = f"❌ checker exited {code}"
        else:
            result = "✅ pass"
        ok = ok and result == "✅ pass"
        lines.append(f"| `{skill}` | {score:.1f} | {grade} | {result} |")
    if not skills:
        lines.append("| _no skills changed_ | | | |")
    return "\n".join(lines) + "\n", ok


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("select")
    s.add_argument("--base", required=True)
    s.add_argument("--head", required=True)
    s.add_argument("--root", type=Path, default=Path("."))
    m = sub.add_parser("summarize")
    m.add_argument("--reports", type=Path, required=True)
    m.add_argument("--skills", type=Path, required=True, help="file with one skill directory per line")
    m.add_argument("--min-score", type=int, required=True)
    m.add_argument("--exits", type=Path, required=True, help="skill<TAB>exit-code per line")
    args = ap.parse_args(argv)

    if args.cmd == "select":
        root = args.root.resolve()
        print("\n".join(select(root, changed_files(root, args.base, args.head))))
        return 0
    skills = [line for line in args.skills.read_text(encoding="utf-8").splitlines() if line]
    table, ok = summarize(args.reports, skills, args.min_score, read_exits(args.exits))
    sys.stdout.write(table)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Helpers for the skill quality-check PR workflow (skill-quality-check.yml).

select     Print the skill directories a pull request touches, one per line.
           A skill is plugins/<plugin>/skills/<skill>/ or the same under
           community-plugins/, and counts only if its SKILL.md still exists
           (a deleted skill has nothing to score). When the gate itself
           changed (the workflow or this script), every skill is selected so
           the new gate is exercised on the whole catalog.

summarize  Read each skill's skillevaluator-quality.json and print a Markdown
           table for the job summary. Exits 1 if any skill failed or has no
           readable report, so a missing report can't pass silently.

Usage:
    python skill-quality.py select --base <sha> --head <sha> [--root .]
    python skill-quality.py summarize --reports <dir> --skills <file> --min-score 70
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
    """Paths changed between the merge base of base and head, and head."""
    out = subprocess.run(
        ["git", "diff", "--name-only", "-z", f"{base}...{head}"],
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


def summarize(reports: Path, skills: list[str], min_score: int) -> tuple[str, bool]:
    lines = [
        f"### Skill quality check (SkillEvaluator `quality-check`, min score {min_score})",
        "",
        "| Skill | Score | Grade | Result |",
        "| --- | ---: | :---: | --- |",
    ]
    ok = True
    for skill in skills:
        report = reports / report_name(skill) / "skillevaluator-quality.json"
        try:
            data = json.loads(report.read_text(encoding="utf-8"))
            summary = data["quality_summary"][0]
            score, grade, passed = summary["overall_score"], summary["grade"], bool(data["overall_passed"])
        except (OSError, ValueError, KeyError, IndexError, TypeError):
            lines.append(f"| `{skill}` | — | — | ❌ no readable report |")
            ok = False
            continue
        ok = ok and passed
        lines.append(f"| `{skill}` | {score:.1f} | {grade} | {'✅ pass' if passed else '❌ below min score'} |")
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
    args = ap.parse_args(argv)

    if args.cmd == "select":
        root = args.root.resolve()
        print("\n".join(select(root, changed_files(root, args.base, args.head))))
        return 0
    skills = [line for line in args.skills.read_text(encoding="utf-8").splitlines() if line]
    table, ok = summarize(args.reports, skills, args.min_score)
    sys.stdout.write(table)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

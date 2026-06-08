#!/usr/bin/env python3
"""Render a GitHub Actions step summary from review and eval JSON result files.

Usage:
    python render-eval-summary.py \\
        --reviews-dir /tmp/all-reviews \\
        --evals-dir   /tmp/all-evals \\
        --threshold   80 \\
        --output      /path/to/output

The script reads all *.json files from the two input directories, merges them
by skill name, and writes a Markdown summary.
"""

import argparse
import json
import os
import sys
from pathlib import Path


def load_json_files(directory: str) -> list[dict]:
    """Load and return all *.json files from directory as a flat list."""
    p = Path(directory)
    if not p.exists():
        return []

    records = []
    for f in sorted(p.glob("*.json")):
        try:
            records.append(json.loads(f.read_text()))
        except json.JSONDecodeError as e:
            print(f"Warning: could not parse {f}: {e}", file=sys.stderr)

    return records


def format_token_count(value: str) -> str:
    """Format a token count string with thousands separators, or return '—'."""
    if not value:
        return "—"

    try:
        return f"{int(value):,}"
    except ValueError:
        return value


def to_float(value):
    if value is None or value == "":
        raise TypeError
    if isinstance(value, str):
        value = value.strip().rstrip("%")
    return float(value)


def get_pass_status_icon(rate_str: str | float, threshold: str | float) -> str:
    """Return '✅' or '❌' based on whether rate_str meets the threshold."""
    try:
        return "✅" if float(rate_str) >= float(threshold) else "❌"
    except (ValueError, TypeError):
        return "❌"


def format_rate_cell(rate: str, passed: str, total: str, threshold: int) -> str:
    """Format a pass-rate table cell, e.g. '✅ 90.0% (9/10)'."""
    if not rate:
        return "—"

    icon = get_pass_status_icon(rate, threshold)
    return f"{icon} {rate}% ({passed}/{total})"


def format_delta_cell(skill_rate: str | float, base_rate: str | float) -> str:
    """Format the Δ column between skill and baseline pass rates."""
    try:
        delta = to_float(skill_rate) - to_float(base_rate)
    except (ValueError, TypeError):
        return "—"

    if delta > 0:
        return f"+{delta:.1f}pp"
    elif delta < 0:
        return f"{delta:.1f}pp"
    return "0pp"


def render_case_table(row: dict, label: str) -> list[str]:
    """Return Markdown lines for the per-case breakdown table of one mode row."""
    results = row.get("results", [])
    if not results:
        return []

    rate = row.get("pass_rate", "")
    passed = row.get("passed", "")
    total = row.get("total", "")
    tokens = format_token_count(row.get("total_tokens", ""))
    time = row.get("total_time") or "—"

    lines = [
        f"**{label} — Pass rate: {passed}/{total} ({rate}%)** "
        f"| Time: {time}s | Tokens: {tokens}",
        "",
        "| # | Case | Status | Criteria | Time | Tokens |",
        "|---|------|--------|:--------:|-----:|-------:|",
    ]
    for i, case in enumerate(results, 1):
        name = case.get("name", "")
        status = (
            "PASS"
            if case.get("criteria_passed") == case.get("criteria_total")
               and case.get("status") == "completed"
            else "FAIL"
        )
        criteria = f"{case.get('criteria_passed')}/{case.get('criteria_total')}"
        elapsed = f"{case.get('elapsed')}s"
        tok = str(case.get("tokens", ""))
        lines.append(f"| {i} | {name} | {status} | {criteria} | {elapsed} | {tok} |")

    lines.append("")
    return lines


def format_skill_label(skill: str) -> str:
    """Format skill as 'plugin :: skill' when given a standard skill path."""
    parts = [p for p in skill.split("/") if p]
    # Expected: plugins/<plugin>/skills/<skill> or community-plugins/<plugin>/skills/<skill>
    if len(parts) >= 4 and parts[2] == "skills":
        plugin = parts[1]
        skill_name = parts[3]
        return f"{plugin} :: {skill_name}"
    return skill


def render_skill(skill: str, review: dict, skill_evals: list[dict], threshold: int) -> list[str]:
    """Return all Markdown lines for a single skill section."""
    lines: list[str] = []

    # Section header
    skill_label = format_skill_label(skill)
    lines += ["---", "", f"# {skill_label}", ""]

    # Validation checks
    val = review.get("validation", "")
    errors = review.get("errors", "")
    warnings = review.get("warnings", "")
    rev_score = review.get("review_score", "")
    desc = review.get("description", "")
    content = review.get("content", "")
    val_block = review.get("validation_block", "")
    judge_block = review.get("judge_block", "")

    val_status = "✅ PASSED" if val == "PASSED" else "❌ FAILED"
    try:
        judge_status = "✅ PASSED" if int(rev_score) >= threshold else "❌ FAILED"
    except (ValueError, TypeError):
        judge_status = "❌ FAILED"

    lines += [
        f"## {val_status} Validation Checks",
        "",
        f"Errors: {errors} | Warnings: {warnings}",
        "",
        "<details><summary>Validation Checks Detail</summary>",
        "",
        "```",
        val_block,
        "```",
        "</details>",
        "",
    ]

    # LLM judge evaluation
    lines += [
        f"## {judge_status} LLM Judge Evaluation",
        "",
        f"**Score: {rev_score}%**",
        "",
        "| Check | Score |",
        "|-------|-------|",
        f"| Description | {desc}% |",
        f"| Content | {content}% |",
        "",
        "<details><summary>Judge Evaluation Detail</summary>",
        "",
        "```",
        judge_block,
        "```",
        "</details>",
        "",
    ]

    # Eval results summary table
    lines += ["## 📊 Eval Results", ""]

    models = sorted({r["model"] for r in skill_evals if r.get("model")})

    if not models:
        lines += ["No evals", ""]
    else:
        lines += [
            "| Model | Baseline | Skill | Δ | Tokens Used (skill) |",
            "|-------|:--------:|:-----:|:-:|--------------------:|",
        ]
        for model in models:
            s_row = next(
                (
                    r
                    for r in skill_evals
                    if r.get("model") == model and r.get("mode") == "skill"
                ),
                {},
            )
            b_row = next(
                (
                    r
                    for r in skill_evals
                    if r.get("model") == model and r.get("mode") == "baseline"
                ),
                {},
            )
            s_cell = format_rate_cell(
                s_row.get("pass_rate", ""),
                s_row.get("passed", ""),
                s_row.get("total", ""),
                threshold,
            )
            b_cell = format_rate_cell(
                b_row.get("pass_rate", ""),
                b_row.get("passed", ""),
                b_row.get("total", ""),
                threshold,
            )
            d_cell = format_delta_cell(s_row.get("pass_rate", ""), b_row.get("pass_rate", ""))
            tk_cell = format_token_count(s_row.get("total_tokens", ""))
            lines.append(f"| `{model}` | {b_cell} | {s_cell} | {d_cell} | {tk_cell} |")

        lines.append("")

        # Per-model detail
        for model in models:
            s_row = next(
                (
                    r
                    for r in skill_evals
                    if r.get("model") == model and r.get("mode") == "skill"
                ),
                {},
            )
            b_row = next(
                (
                    r
                    for r in skill_evals
                    if r.get("model") == model and r.get("mode") == "baseline"
                ),
                {},
            )

            s_rate = s_row.get("pass_rate", "")
            s_pass = s_row.get("passed", "")
            s_total = s_row.get("total", "")
            header = f"{s_rate}% ({s_pass}/{s_total})" if s_rate else "No evals"

            lines += [
                f"<details><summary><code>{model}</code>: {header}</summary>",
                "",
            ]
            lines += render_case_table(s_row, "Skill")
            lines += render_case_table(b_row, "Baseline")
            lines += ["</details>", ""]

    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reviews-dir", default="/tmp/all-reviews")
    parser.add_argument("--evals-dir", default="/tmp/all-evals")
    parser.add_argument("--threshold", type=int, default=80)
    parser.add_argument(
        "--output",
        default=os.environ.get("GITHUB_STEP_SUMMARY", "/dev/stdout"),
        help="File to append Markdown to (default: $GITHUB_STEP_SUMMARY or stdout)",
    )
    args = parser.parse_args()

    reviews = load_json_files(args.reviews_dir)
    evals = load_json_files(args.evals_dir)

    if not reviews and not evals:
        with open(args.output, "a") as fh:
            fh.write("No evaluation results found.\n")
        return

    # Index reviews by skill name; index evals as list per skill
    review_by_skill: dict[str, dict] = {}
    for r in reviews:
        skill = r.get("skill", "")
        if skill:
            review_by_skill[skill] = r

    evals_by_skill: dict[str, list[dict]] = {}
    for e in evals:
        skill = e.get("skill", "")
        if skill:
            evals_by_skill.setdefault(skill, []).append(e)

    all_skills = sorted(set(review_by_skill) | set(evals_by_skill))

    lines: list[str] = ["# Evaluation Summary", ""]
    for skill in all_skills:
        lines += render_skill(
            skill,
            review_by_skill.get(skill, {}),
            evals_by_skill.get(skill, []),
            args.threshold,
        )

    with open(args.output, "a") as fh:
        fh.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()

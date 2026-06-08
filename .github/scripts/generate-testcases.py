#!/usr/bin/env python3
"""Generate eval testcases for newly added skills using the LiteLLM proxy."""

import argparse
import json
import os
import re
import sys
from pathlib import Path

import yaml
from openai import OpenAI

SYSTEM_PROMPT = """\
You generate evaluation test cases for AI coding-assistant skills.

Each skill has a SKILL.md that defines when and how it should be invoked.
Your job is to generate realistic eval cases that test whether the skill
triggers correctly and produces quality output.

## Eval YAML format

Always use a YAML block scalar (`|`) for the `prompt` field — prompts often contain
colons, JSON, or quotes that break inline YAML values.

```yaml
name: <Short human-readable name>
prompt: |
  <Realistic user message that would trigger (or not) the skill>
criteria:
  - <Specific, verifiable assertion about the response>
  - <Another specific assertion>
expect_skill: true   # false for the negative-trigger case
timeout: 600         # use 600 for all cases including the negative-trigger case
```

## Rules

- Generate **5–6 cases total**: 4–5 positive (`expect_skill: true`), exactly 1 negative (`expect_skill: false`).
- Positive cases must cover distinct use cases mentioned in the skill.
- Criteria must be **specific and verifiable** by a separate judge LLM.
  Good: "Uses @pytest.mark.parametrize decorator"
  Bad:  "Output follows best practices"
- If a test case needs a file in the workspace, always include it as a `files:` entry with inline `content:` — never reference an external file path without content, as it will not exist at eval time.
- Prompts must sound like a real developer wrote them, not like a test case.
- The negative-trigger prompt should be plausibly related but clearly outside scope.
- Files must be sequentially numbered starting at 001. The last file must be the negative-trigger case, named `NNN-negative-trigger.yaml`.

## Output format

Return a JSON array only — no markdown fences, no explanation:

[
  {
    "filename": "001-kebab-case-name.yaml",
    "content": "name: ...\\nprompt: ...\\ncriteria:\\n  - ...\\nexpect_skill: true\\ntimeout: 600\\n"
  },
  ...
]
"""

USER_PROMPT = """\
Skill path: {skill_path}

SKILL.md content:
{skill_content}

Generate 5–6 evaluation test cases for this skill.
"""


def extract_json_array(text: str) -> list:
    text = text.strip()
    if text.startswith("["):
        return json.loads(text)
    match = re.search(r"\[[\s\S]*\]", text)
    if match:
        return json.loads(match.group())
    raise ValueError(f"No JSON array found in response:\n{text[:500]}")


def validate_testcase(content: str, filename: str) -> None:
    data = yaml.safe_load(content)
    if not isinstance(data, dict):
        raise ValueError(f"{filename}: content did not parse as a YAML mapping")
    required = {"name", "prompt", "expect_skill"}
    missing = required - set(data.keys())
    if missing:
        raise ValueError(f"{filename}: missing required fields: {missing}")
    if "criteria" not in data and "grading" not in data:
        raise ValueError(f"{filename}: must have 'criteria' or 'grading'")


def generate_for_skill(
    skill_path: str,
    skill_root: Path,
    client: OpenAI,
    model: str,
) -> list[dict]:
    skill_content = (skill_root / skill_path).read_text()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT.format(
                skill_path=skill_path,
                skill_content=skill_content,
            )},
        ],
        temperature=0.7,
        max_tokens=4096,
    )
    return extract_json_array(response.choices[0].message.content)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skills", required=True, help="JSON array of SKILL.md paths")
    parser.add_argument("--skill-root", required=True, help="Root dir containing skill files")
    parser.add_argument("--output-dir", required=True, help="Output root for generated evals")
    parser.add_argument("--model", default="claude-sonnet-4-6")
    args = parser.parse_args()

    skills: list[str] = json.loads(args.skills)
    if not skills:
        print("No skills to process")
        return

    client = OpenAI(
        api_key=os.environ["LITELLM_API_KEY"],
        base_url=os.environ["LITELLM_PROXY_URL"].rstrip("/") + "/v1",
    )

    skill_root = Path(args.skill_root)
    output_root = Path(args.output_dir)
    errors: list[tuple[str, str]] = []
    warnings: list[str] = []

    for skill_path in skills:
        print(f"\nGenerating testcases for: {skill_path}")
        evals_dir = output_root / Path(skill_path).parent / "evals"

        try:
            testcases = generate_for_skill(skill_path, skill_root, client, args.model)
        except Exception as exc:
            print(f"  ERROR: {exc}", file=sys.stderr)
            errors.append((skill_path, str(exc)))
            continue

        evals_dir.mkdir(parents=True, exist_ok=True)
        for tc in testcases:
            filename: str = tc["filename"]
            content: str = tc["content"]
            try:
                validate_testcase(content, filename)
            except Exception as exc:
                msg = f"{filename}: {exc}"
                print(f"  WARNING {msg} (written anyway)", file=sys.stderr)
                warnings.append(msg)
            out_file = evals_dir / filename
            out_file.write_text(content)
            print(f"  Written: {out_file}")

    if warnings:
        warnings_file = output_root / ".validation-warnings"
        warnings_file.write_text("\n".join(warnings) + "\n")

    if errors:
        print(f"\n{len(errors)} skill(s) failed generation:", file=sys.stderr)
        for path, msg in errors:
            print(f"  {path}: {msg}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

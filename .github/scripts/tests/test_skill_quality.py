import json
import subprocess

import pytest
from conftest import _load


@pytest.fixture(scope="session")
def sq():
    return _load("skill-quality")


def git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True).stdout.strip()


@pytest.fixture
def repo(tmp_path):
    """A repo with three skills on its base commit."""
    git(tmp_path, "init", "-q", "-b", "main")
    git(tmp_path, "config", "user.email", "t@example.com")
    git(tmp_path, "config", "user.name", "t")
    git(tmp_path, "config", "commit.gpgsign", "false")
    for d in ("plugins/a/skills/one", "plugins/a/skills/two", "community-plugins/c/skills/three"):
        (tmp_path / d).mkdir(parents=True)
        (tmp_path / d / "SKILL.md").write_text("---\nname: x\n---\n", encoding="utf-8")
    (tmp_path / "README.md").write_text("r\n", encoding="utf-8")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "base")
    return tmp_path


def commit(repo, edits):
    base = git(repo, "rev-parse", "HEAD")
    for path, text in edits.items():
        p = repo / path
        if text is None:
            p.unlink()
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "change")
    return base, git(repo, "rev-parse", "HEAD")


def selected(sq, repo, base, head):
    return sq.select(repo, sq.changed_files(repo, base, head))


def test_selects_skills_with_changed_files_including_nested_references(sq, repo):
    base, head = commit(repo, {
        "plugins/a/skills/one/SKILL.md": "changed\n",
        "community-plugins/c/skills/three/references/deep/notes.md": "new\n",
        "README.md": "changed\n",
    })
    assert selected(sq, repo, base, head) == ["community-plugins/c/skills/three", "plugins/a/skills/one"]


def test_ignores_non_skill_paths(sq, repo):
    base, head = commit(repo, {"README.md": "x\n", "plugins/a/README.md": "x\n", "plugins/a/agents/x.md": "x\n"})
    assert selected(sq, repo, base, head) == []


def test_skips_a_deleted_skill(sq, repo):
    base, head = commit(repo, {"plugins/a/skills/two/SKILL.md": None})
    assert selected(sq, repo, base, head) == []


def test_skill_dir_without_skill_md_is_not_selected(sq, repo):
    base, head = commit(repo, {"plugins/a/skills/draft/notes.md": "wip\n"})
    assert selected(sq, repo, base, head) == []


@pytest.mark.parametrize("gate", [".github/workflows/skill-quality-check.yml", ".github/scripts/skill-quality.py"])
def test_changing_the_gate_selects_every_skill(sq, repo, gate):
    base, head = commit(repo, {gate: "changed\n"})
    assert selected(sq, repo, base, head) == [
        "community-plugins/c/skills/three", "plugins/a/skills/one", "plugins/a/skills/two",
    ]


def test_diff_is_against_the_merge_base(sq, repo):
    """A skill changed only on the base branch after the PR branched is not the PR's change."""
    fork = git(repo, "rev-parse", "HEAD")
    git(repo, "checkout", "-q", "-b", "pr")
    _, head = commit(repo, {"plugins/a/skills/one/SKILL.md": "pr\n"})
    git(repo, "checkout", "-q", "main")
    _, base = commit(repo, {"plugins/a/skills/two/SKILL.md": "main moved\n"})
    assert fork != base
    assert selected(sq, repo, base, head) == ["plugins/a/skills/one"]


def write_report(reports, skill, sq, score, passed):
    d = reports / sq.report_name(skill)
    d.mkdir(parents=True)
    payload = {"overall_passed": passed, "quality_summary": [{"overall_score": score, "grade": "B" if score >= 80 else "D"}]}
    (d / "skillevaluator-quality.json").write_text(json.dumps(payload), encoding="utf-8")


def test_summary_passes_when_every_skill_passes(sq, tmp_path):
    write_report(tmp_path, "plugins/a/skills/one", sq, 85.0, True)
    table, ok = sq.summarize(tmp_path, ["plugins/a/skills/one"], 70)
    assert ok
    assert "| `plugins/a/skills/one` | 85.0 | B | ✅ pass |" in table


def test_summary_fails_on_a_failing_skill(sq, tmp_path):
    write_report(tmp_path, "plugins/a/skills/one", sq, 85.0, True)
    write_report(tmp_path, "plugins/a/skills/two", sq, 61.0, False)
    table, ok = sq.summarize(tmp_path, ["plugins/a/skills/one", "plugins/a/skills/two"], 70)
    assert not ok
    assert "❌ below min score" in table


def test_summary_fails_on_a_missing_report(sq, tmp_path):
    table, ok = sq.summarize(tmp_path, ["plugins/a/skills/one"], 70)
    assert not ok
    assert "no readable report" in table


def test_summary_fails_on_a_malformed_report(sq, tmp_path):
    d = tmp_path / sq.report_name("plugins/a/skills/one")
    d.mkdir()
    (d / "skillevaluator-quality.json").write_text('{"overall_passed": true}', encoding="utf-8")
    _, ok = sq.summarize(tmp_path, ["plugins/a/skills/one"], 70)
    assert not ok


def test_summary_with_no_skills_passes(sq, tmp_path):
    table, ok = sq.summarize(tmp_path, [], 70)
    assert ok
    assert "no skills changed" in table


def test_same_named_skills_get_separate_reports(sq):
    assert sq.report_name("plugins/a/skills/x") != sq.report_name("community-plugins/a/skills/x")


def test_summarize_cli_exit_code(sq, tmp_path):
    write_report(tmp_path, "plugins/a/skills/two", sq, 61.0, False)
    skills = tmp_path / "skills.txt"
    skills.write_text("plugins/a/skills/two\n", encoding="utf-8")
    assert sq.main(["summarize", "--reports", str(tmp_path), "--skills", str(skills), "--min-score", "70"]) == 1

import json
import os
import shutil
import tomllib

import pytest
from conftest import SCRIPTS, _load, run_step, workflow_step

SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"


@pytest.fixture(scope="session")
def ap():
    return _load("agent_plugins")


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data if isinstance(data, str) else json.dumps(data, indent=4) + "\n", encoding="utf-8")


def skill(root, plugin, name, body=""):
    write(root / plugin / "skills" / name / "SKILL.md", f"---\nname: {name}\ndescription: Does {name}.\n---\n{body}")


@pytest.fixture
def repo(tmp_path, ap):
    """Two synced plugins: one with skills and MCP, one community plugin."""
    write(tmp_path / ".claude-plugin/marketplace.json", {
        "name": "rse-plugins",
        "owner": {"name": "UW SSEC Team"},
        "metadata": {"description": "test"},
        "plugins": [
            {"name": "alpha", "source": "./plugins/alpha", "category": "development", "strict": False},
            {"name": "beta", "source": "./community-plugins/beta", "category": "data-science", "strict": False},
        ],
    })
    for plugin, name in (("plugins/alpha", "alpha"), ("community-plugins/beta", "beta")):
        write(tmp_path / plugin / "plugin.json", {"$schema": SCHEMA, "name": name, "version": "1.0.0",
                                                  "description": f"{name} plugin", "license": "BSD-3-Clause"})
    skill(tmp_path, "plugins/alpha", "one", "See [two](references/two.md) and `[x](../x.md)`.\n")
    write(tmp_path / "plugins/alpha/skills/one/references/two.md", "# two\n")
    skill(tmp_path, "plugins/alpha", "three")
    write(tmp_path / "plugins/alpha/.mcp.json", {"mcpServers": {"s": {"command": "docker"}}})
    write(tmp_path / "plugins/alpha/mcp.json", {"$schema": MCP_SCHEMA, "mcpServers": {
        "s": {"type": "stdio", "command": "docker", "args": ["-v", "${PLUGIN_DATA}/s:/data"]}}})
    skill(tmp_path, "community-plugins/beta", "four")
    assert ap.sync(tmp_path) == 0
    return tmp_path


def problems(ap, root):
    return ap.check(root, run_claude=False)


def test_synced_repo_passes(ap, repo):
    assert problems(ap, repo) == []


def test_sync_generates_every_client_manifest(ap, repo):
    claude = json.loads((repo / "plugins/alpha/.claude-plugin/plugin.json").read_text())
    assert claude == {"name": "alpha", "version": "1.0.0", "description": "alpha plugin", "license": "BSD-3-Clause"}
    entry = json.loads((repo / ".claude-plugin/marketplace.json").read_text())["plugins"][0]
    assert entry["description"] == "alpha plugin" and entry["category"] == "development" and entry["strict"] is False
    codex = json.loads((repo / ".agents/plugins/marketplace.json").read_text())
    assert codex["plugins"][1] == {"name": "beta", "source": {"source": "local", "path": "./community-plugins/beta"},
                                   "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                                   "category": "Data Science"}
    cursor = json.loads((repo / ".cursor-plugin/marketplace.json").read_text())
    assert [p["source"] for p in cursor["plugins"]] == ["./plugins/alpha", "./community-plugins/beta"]
    assert not (repo / "plugins/alpha/.cursor-plugin/plugin.json").exists()


def test_sync_is_idempotent(ap, repo, capsys):
    capsys.readouterr()
    ap.sync(repo)
    assert capsys.readouterr().out == ""


def test_drift_fails_until_synced(ap, repo):
    m = json.loads((repo / "plugins/alpha/plugin.json").read_text())
    m["description"] = "changed"
    write(repo / "plugins/alpha/plugin.json", m)
    errs = problems(ap, repo)
    assert any(".claude-plugin/plugin.json: out of date" in e for e in errs)
    assert any(".claude-plugin/marketplace.json: out of date" in e for e in errs)
    ap.sync(repo)
    assert problems(ap, repo) == []


@pytest.mark.parametrize("change, message", [
    ({"category": "x"}, "unknown field 'category'"),
    ({"$schema": "https://example.com/s.json"}, "$schema must be"),
    ({"name": "Alpha"}, "breaks the Agent Plugins name rules"),
    ({"name": "gamma"}, "differs from its directory"),
    ({"keywords": "a,b"}, "keywords must be a list of strings"),
    ({"author": {"name": "a", "twitter": "b"}}, "author may only hold"),
    ({"extensions": {"com.example": True}}, "extensions must map namespaces to objects"),
])
def test_manifest_rules(ap, repo, change, message):
    m = json.loads((repo / "plugins/alpha/plugin.json").read_text())
    write(repo / "plugins/alpha/plugin.json", {**m, **change})
    assert any(message in e for e in problems(ap, repo))


def test_missing_root_manifest_fails(ap, repo):
    (repo / "plugins/alpha/plugin.json").unlink()
    errs = problems(ap, repo)
    assert any("plugins/alpha/plugin.json: missing" in e for e in errs)


def test_plugin_missing_from_catalog_fails(ap, repo):
    write(repo / "plugins/gamma/plugin.json", {"$schema": SCHEMA, "name": "gamma"})
    assert any("no entry for ./plugins/gamma" in e for e in problems(ap, repo))


def test_claude_mcp_without_portable_mcp_fails(ap, repo):
    # Codex stops reading .mcp.json once plugin.json exists, so the server would vanish.
    (repo / "plugins/alpha/mcp.json").unlink()
    assert any("plugins/alpha/mcp.json: missing" in e for e in problems(ap, repo))


@pytest.mark.parametrize("server, message", [
    ({"command": "docker"}, "type must be one of"),
    ({"type": "stdio", "command": "docker", "toolAliases": {}}, "not allowed for type 'stdio'"),
    ({"type": "stdio", "command": "docker", "args": ["-v", "${HOME}/x:/x"]}, "${HOME} is never expanded"),
    ({"type": "stdio", "command": "docker", "env": {"PLUGIN_DATA": "x"}}, "must not set PLUGIN_ROOT or PLUGIN_DATA"),
    ({"type": "stdio", "command": "docker run"}, "one executable token"),
    ({"type": "stdio", "command": "docker", "cwd": "/tmp"}, "cwd must start with"),
    ({"type": "stdio", "command": "docker", "cwd": "./../../outside"}, "resolves outside the plugin root or data"),
    ({"type": "stdio", "command": "docker", "cwd": "${PLUGIN_ROOT}/.."}, "resolves outside the plugin root or data"),
    ({"type": "stdio", "command": "docker", "cwd": "${PLUGIN_DATA}/../x"}, "resolves outside the plugin root or data"),
    ({"type": "stdio", "command": "./../bin/server"}, "command './../bin/server' resolves outside"),
    ({"type": "stdio", "command": "../bin/server"}, "bare executable name or a ./ plugin-relative path"),
    ({"type": "stdio", "command": "bin/server"}, "bare executable name or a ./ plugin-relative path"),
    ({"type": "streamable-http"}, "missing ['url']"),
])
def test_mcp_rules(ap, repo, server, message):
    write(repo / "plugins/alpha/mcp.json", {"$schema": MCP_SCHEMA, "mcpServers": {"s": server}})
    assert any(message in e for e in problems(ap, repo))


def test_mcp_contained_paths_pass(ap, repo):
    write(repo / "plugins/alpha/bin/server", "#!/bin/sh\n")
    write(repo / "plugins/alpha/mcp.json", {"$schema": MCP_SCHEMA, "mcpServers": {
        "a": {"type": "stdio", "command": "./bin/server", "cwd": "./bin"},
        "b": {"type": "stdio", "command": "docker", "cwd": "${PLUGIN_ROOT}"},
        "c": {"type": "stdio", "command": "docker", "cwd": "${PLUGIN_DATA}/cache/../state"}}})
    assert problems(ap, repo) == []


@pytest.mark.parametrize("field", ["cwd", "command"])
def test_mcp_symlink_escape_fails(ap, repo, tmp_path_factory, field):
    outside = tmp_path_factory.mktemp("outside")
    (repo / "plugins/alpha/link").symlink_to(outside, target_is_directory=True)
    server = {"type": "stdio", "command": "docker", "cwd": "./link"} if field == "cwd" else \
        {"type": "stdio", "command": "./link/server"}
    write(repo / "plugins/alpha/mcp.json", {"$schema": MCP_SCHEMA, "mcpServers": {"s": server}})
    assert any("resolves outside" in e for e in problems(ap, repo))


def test_mcp_extra_top_level_field_fails(ap, repo):
    write(repo / "plugins/alpha/mcp.json", {"$schema": MCP_SCHEMA, "mcpServers": {}, "resourcePaths": {}})
    assert any("must hold exactly $schema" in e for e in problems(ap, repo))


@pytest.mark.parametrize("body, message", [
    ("See [three](../../three/SKILL.md).\n", "leaves the skill"),
    ("[ref]: ../../README.md\n", "leaves the skill"),
    ("- [[../../three/SKILL.md]]\n", "leaves the skill"),
    ("![img](/assets/x.png)\n", "leaves the skill"),
    ("See [gone](references/gone.md).\n", "points at nothing"),
])
def test_skill_links_must_stay_inside_and_resolve(ap, repo, body, message):
    write(repo / "plugins/alpha/skills/one/references/two.md", body)
    assert any(message in e for e in problems(ap, repo))


def test_links_in_code_urls_and_assets_are_ignored(ap, repo):
    write(repo / "plugins/alpha/skills/one/references/two.md",
          "````markdown\n```\nx\n```\n[a](../../x.md)\n````\n`[b](../y.md)` [c](https://example.com) [d](#top)\n")
    write(repo / "plugins/alpha/skills/one/assets/template.md", "[Contributing](CONTRIBUTING.md) [up](../../x.md)\n")
    assert problems(ap, repo) == []


def test_symlink_out_of_skill_fails(ap, repo):
    (repo / "plugins/alpha/skills/one/shared").symlink_to(repo / "plugins/alpha/skills/three")
    assert any("resolves outside its skill" in e for e in problems(ap, repo))


@pytest.mark.parametrize("frontmatter, message", [
    ("name: other\ndescription: d\n", "must equal the lowercase-hyphenated directory name"),
    ("name: one\n", "description must be a string of 1-1024 characters"),
    ("name: one\ndescription: d\ncolor: red\n", "frontmatter field 'color'"),
    ("name: one\ndescription: [d]\n", "description must be a string"),
    ("name: one\ndescription: d\nlicense: [MIT]\n", "license must be a string"),
    ("name: one\ndescription: d\nmetadata: x\n", "metadata must be a mapping"),
    ("name: one\ndescription: 'a: b\n", "frontmatter is not a YAML mapping"),
    ("- one\n", "frontmatter is not a YAML mapping"),
])
def test_skill_frontmatter(ap, repo, frontmatter, message):
    write(repo / "plugins/alpha/skills/one/SKILL.md", f"---\n{frontmatter}---\nbody\n")
    assert any(message in e for e in problems(ap, repo))


@pytest.mark.parametrize("frontmatter", [
    "name: one # a YAML comment\ndescription: d\n",
    "name: 'one'\ndescription: 'Has a # inside quotes'\n",
    "name: one\ndescription: >-\n  Folded\n  text.\nmetadata:\n  references:\n    - references/two.md\n",
])
def test_skill_frontmatter_is_read_as_yaml(ap, repo, frontmatter):
    write(repo / "plugins/alpha/skills/one/SKILL.md", f"---\n{frontmatter}---\nbody\n")
    assert problems(ap, repo) == []


@pytest.mark.parametrize("skills, ok", [
    ("skills:\n  - one\n", True),
    ("", True),
    ("skills: one\n", False),
    ("skills:\n  one: x\n", False),
])
def test_agent_skills_must_be_a_list(ap, repo, skills, ok):
    # Copilot CLI silently skips an agent whose skills is a string; Claude Code accepts it.
    write(repo / "plugins/alpha/agents/a.md", f"---\nname: a\ndescription: d\n{skills}---\nbody\n")
    ap.sync(repo)
    errs = problems(ap, repo)
    assert (errs == []) if ok else any("agents/a.md: skills must be a YAML list" in e for e in errs)


def claude_stub(tmp_path, monkeypatch, report):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    (bin_dir / "claude").write_text(f"#!/usr/bin/env bash\ncat <<'EOF'\n{json.dumps(report)}\nEOF\n")
    (bin_dir / "claude").chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}:{os.environ['PATH']}")


def test_claude_null_manifest_fails_despite_exit_zero(ap, tmp_path, monkeypatch):
    claude_stub(tmp_path, monkeypatch, {"success": True, "manifest": None, "contents": []})
    errs = ap.claude_validate([tmp_path])
    assert len(errs) == 1 and "found no manifest" in errs[0]


def test_claude_manifest_warning_fails(ap, tmp_path, monkeypatch):
    claude_stub(tmp_path, monkeypatch, {"success": False, "manifest": {
        "file": "p", "errors": [], "warnings": [{"path": "category"}]}, "contents": []})
    assert len(ap.claude_validate([tmp_path])) == 1


def test_claude_component_error_fails_and_warning_is_reported(ap, tmp_path, monkeypatch, capsys):
    claude_stub(tmp_path, monkeypatch, {"success": False, "manifest": {"file": "p", "errors": [], "warnings": []},
                                        "contents": [{"file": "a.md", "errors": ["bad yaml"], "warnings": []},
                                                     {"file": "CLAUDE.md", "errors": [],
                                                      "warnings": [{"message": "not loaded"}]}]})
    errs = ap.claude_validate([tmp_path])
    assert errs == [f"{tmp_path}: a.md: ['bad yaml']"]
    assert "CLAUDE.md: not loaded" in capsys.readouterr().err


def test_repository_is_in_sync(ap):
    assert ap.check(SCRIPTS.parents[1], run_claude=False) == []


def test_copilot_copies_are_generated_and_required(ap, repo):
    # Copilot CLI reads agents/commands only from com.github.copilot/ once plugin.json exists.
    write(repo / "plugins/alpha/agents/a.md", "---\nname: a\ndescription: d\n---\n")
    copy = repo / "plugins/alpha/com.github.copilot/agents/a.md"
    assert any("com.github.copilot/agents/a.md: missing" in e for e in problems(ap, repo))
    ap.sync(repo)
    assert copy.read_text() == (repo / "plugins/alpha/agents/a.md").read_text() and not copy.is_symlink()
    assert not (repo / "plugins/alpha/com.github.copilot/commands").exists()
    assert problems(ap, repo) == []

    write(repo / "plugins/alpha/agents/a.md", "---\nname: a\ndescription: changed\n---\n")
    assert any("a.md: missing or differs" in e for e in problems(ap, repo))
    ap.sync(repo)
    assert "changed" in copy.read_text()

    write(repo / "plugins/alpha/com.github.copilot/agents/old.md", "x")
    assert any("old.md: copies nothing" in e for e in problems(ap, repo))
    ap.sync(repo)
    assert problems(ap, repo) == []


def test_copilot_symlink_checked_out_as_file_fails_and_sync_repairs(ap, repo):
    # Without core.symlinks a directory symlink becomes a text file holding its target.
    write(repo / "plugins/alpha/agents/a.md", "agent\n")
    write(repo / "plugins/alpha/com.github.copilot/agents", "../agents")
    errs = problems(ap, repo)
    assert any("agents/a.md: missing or differs" in e for e in errs)
    assert any("com.github.copilot/agents: copies nothing" in e for e in errs)
    ap.sync(repo)
    assert (repo / "plugins/alpha/com.github.copilot/agents/a.md").read_text() == "agent\n"
    assert problems(ap, repo) == []


DECODE_DOC = 'gh api "repos/o/r/contents/.github/workflows/ci.yml?ref=abc" \\\n  --jq \'.content\' | base64 -d\n'


@pytest.mark.parametrize("body, flagged", [
    (DECODE_DOC, False),
    ("gh api repos/o/r/contents/payload --jq '.content' | base64 -d | sh\n", True),
    ("  --jq '.content' | base64 -d | sh\n", True),
    ("  --jq '.content' | base64 -d \\\n  | sh\n", True),
    ("  --jq .content | base64 -d\n", True),
    ("echo aGk= | base64 -d | sh\n", True),
])
def test_dangerous_pattern_scan_exempts_only_the_decode_only_line(tmp_path, body, flagged):
    script = workflow_step("validate-plugins.yml", "Security scan - Dangerous patterns")
    write(tmp_path / ".claude-plugin/marketplace.json", {"plugins": [{"source": "./plugins/p"}]})
    write(tmp_path / "plugins/p/skills/s/references/runbook.md", f"```bash\n{body}```\n")
    proc, _ = run_step(script, tmp_path, {})
    assert (proc.returncode != 0) == flagged, proc.stdout + proc.stderr
    assert ("No dangerous patterns detected" in proc.stdout) != flagged


def test_ci_runs_the_script_through_pixi_tasks():
    tasks = tomllib.loads((SCRIPTS.parents[1] / "pixi.toml").read_text(encoding="utf-8"))["feature"]["ci"]["tasks"]
    assert tasks["plugins-check"]["cmd"] == "python .github/scripts/agent_plugins.py check"
    assert tasks["plugins-check-claude"]["cmd"] == "python .github/scripts/agent_plugins.py check --claude"
    assert "pixi run plugins-check\n" in workflow_step("validate-plugins.yml", "Check Agent Plugins manifests and skills")
    assert "pixi run plugins-check-claude" in workflow_step("validate-plugins.yml", "Validate with Claude Code")


@pytest.mark.skipif(shutil.which("jq") is None, reason="needs jq")
def test_json_scans_skip_the_pixi_environment(tmp_path):
    # setup-pixi installs the environment in .pixi/ inside the checkout; its packages aren't ours to validate.
    (tmp_path / ".pixi/envs/ci").mkdir(parents=True)
    (tmp_path / ".pixi/envs/ci/vendored.json").write_text('{"a": 1, "a": 2', encoding="utf-8")
    write(tmp_path / "plugins/p/plugin.json", {"name": "p"})
    proc, _ = run_step(workflow_step("validate-plugins.yml", "Validate JSON files"), tmp_path, {})
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "plugin.json" in proc.stdout and ".pixi" not in proc.stdout
    dup = _load("check_duplicate_json_keys")
    assert list(dup.iter_json_files([tmp_path])) == [tmp_path / "plugins/p/plugin.json"]
    (tmp_path / "plugins/p/plugin.json").write_text("{", encoding="utf-8")
    proc, _ = run_step(workflow_step("validate-plugins.yml", "Validate JSON files"), tmp_path, {})
    assert proc.returncode != 0

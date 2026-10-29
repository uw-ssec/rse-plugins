#!/usr/bin/env python3
"""Keep the plugins installable across clients, following Agent Plugins v1.0.0.

Usage:
    agent_plugins.py sync            # regenerate every derived manifest from the sources
    agent_plugins.py check           # fail on drift or on a broken package (CI runs this)
    agent_plugins.py check --claude  # also run `claude plugin validate --strict`

Sources of truth:

- ``<plugin>/plugin.json``: the portable Agent Plugins manifest. Every shared
  field (name, version, description, author, homepage, repository, license,
  keywords) is edited here and nowhere else.
- ``.claude-plugin/marketplace.json``: the catalog. It owns the plugin list,
  its order, each plugin's ``source``, and the Claude-only ``category`` and
  ``strict`` fields.

Generated from them (``sync`` writes, ``check`` compares):

- ``<plugin>/.claude-plugin/plugin.json``: Claude Code doesn't read the
  portable manifest, so it gets a copy of the shared fields;
- the shared fields of each ``.claude-plugin/marketplace.json`` entry;
- ``.agents/plugins/marketplace.json`` (Codex);
- ``.cursor-plugin/marketplace.json`` (Cursor). There is deliberately no
  ``.cursor-plugin/plugin.json``: without one, Cursor loads each package as an
  Agent Plugin (skills and MCP only) instead of parsing the Claude-format
  agents and commands as Cursor components;
- ``<plugin>/com.github.copilot/{agents,commands}``: copies of the plugin's
  ``agents/`` and ``commands/``. Once root plugin.json exists, Copilot CLI
  loads agents and commands only from its ``com.github.copilot/`` extension
  directory. Edit the originals; ``sync`` refreshes the copies and removes
  stale ones.

Package checks, for every plugin:

- plugin.json follows the closed manifest schema and its name is the directory;
- every directory under plugins/ and community-plugins/ is in the catalog;
- each skills/<dir>/SKILL.md has Agent Skills frontmatter whose name is <dir>;
- no file, symlink or relative Markdown/wiki link inside a skill resolves
  outside that skill, and every relative link resolves to a file (installed
  skills are copied on their own, so a link to ../sibling breaks);
- a plugin with a Claude ``.mcp.json`` also ships a portable ``mcp.json``
  (once root plugin.json exists, Codex reads only mcp.json), and mcp.json
  follows the closed MCP schema. A stdio ``command`` that is a path and every
  ``cwd`` stay inside the plugin root (or the plugin data directory), after
  ``..`` and symlinks are resolved;
- an agent's ``skills`` frontmatter is a list. Copilot CLI silently drops an
  agent whose ``skills`` is a plain string, while Claude Code accepts it.

Needs PyYAML, so frontmatter is read the way clients read it.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
PLUGIN_PARENTS = ("plugins", "community-plugins")
CATALOG = Path(".claude-plugin/marketplace.json")
CODEX_CATALOG = Path(".agents/plugins/marketplace.json")
CURSOR_CATALOG = Path(".cursor-plugin/marketplace.json")
# With a root plugin.json, Copilot CLI reads agents and commands only from its
# extension directory, so each gets a generated copy of the Claude Code files.
# Copies, not symlinks: a checkout without core.symlinks (the Windows default)
# turns a symlink into a one-line text file.
COPILOT_DIR = "com.github.copilot"
COPILOT_COMPONENTS = ("agents", "commands")

PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
SHARED = ["name", "version", "description", "author", "homepage", "repository", "license", "keywords"]
MANIFEST_FIELDS = {"$schema", *SHARED, "extensions"}
PLUGIN_NAME = re.compile(r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]{0,62}[a-z0-9])?$")
SKILL_NAME = re.compile(r"^(?!.*--)[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
SKILL_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
MCP_VARIANTS = {
    "stdio": ({"type", "command"}, {"args", "env", "cwd"}),
    "streamable-http": ({"type", "url"}, {"headers"}),
    "sse": ({"type", "url"}, {"headers"}),
}
CWD = re.compile(r"^(?:\./|\$\{PLUGIN_ROOT\}(?:/|$)|\$\{PLUGIN_DATA\}(?:/|$))")

# Markdown link targets: inline [t](x) / ![t](x), reference definitions, and [[wiki]] links.
INLINE_LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*<?([^)\s>]+)>?(?:\s+[\"'][^\"']*[\"'])?\s*\)")
REF_DEF = re.compile(r"^\s{0,3}\[[^\]\n]+\]:\s*<?(\S+?)>?(?:\s|$)", re.M)
WIKI_LINK = re.compile(r"\[\[([^\]|#\n]+)(?:[#|][^\]\n]*)?\]\]")
FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})")
EXTERNAL = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|#|//)", re.I)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(data) -> str:
    return json.dumps(data, indent=4, ensure_ascii=False) + "\n"


def plugin_dirs(root: Path) -> list[Path]:
    return sorted(d for parent in PLUGIN_PARENTS if (root / parent).is_dir()
                  for d in (root / parent).iterdir() if d.is_dir())


def inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


# --- generation -------------------------------------------------------------

def shared(manifest: dict) -> dict:
    return {k: manifest[k] for k in SHARED if k in manifest}


def expected_files(root: Path) -> dict[Path, str]:
    """Every generated file and its expected content. Raises ValueError on unusable sources."""
    catalog = load(root / CATALOG)
    manifests = {}
    for entry in catalog.get("plugins", []):
        src = entry.get("source")
        if not (isinstance(src, str) and src.startswith("./")):
            continue
        path = root / src / "plugin.json"
        if not path.is_file():
            raise ValueError(f"{path.relative_to(root)}: missing; it is the source for every other manifest")
        manifests[src] = load(path)

    out: dict[Path, str] = {}
    entries = []
    for entry in catalog.get("plugins", []):
        src = entry.get("source")
        if src not in manifests:
            entries.append(entry)
            continue
        m = manifests[src]
        out[root / src / ".claude-plugin" / "plugin.json"] = dump(shared(m))
        new = {"name": m["name"], "source": src}
        new.update({k: v for k, v in shared(m).items() if k != "name"})
        new.update({k: v for k, v in entry.items() if k not in new and k not in SHARED})
        entries.append(new)
    out[root / CATALOG] = dump({**catalog, "plugins": entries})

    local = [(e, manifests[e["source"]]) for e in entries if e.get("source") in manifests]
    out[root / CODEX_CATALOG] = dump({
        "name": catalog["name"],
        "interface": {"displayName": catalog["name"]},
        "plugins": [{
            "name": m["name"],
            "source": {"source": "local", "path": e["source"]},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "category": e.get("category", "other").replace("-", " ").title(),
        } for e, m in local],
    })
    out[root / CURSOR_CATALOG] = dump({
        "name": catalog["name"],
        "owner": catalog["owner"],
        "metadata": catalog.get("metadata", {}),
        "plugins": [{"name": m["name"], "source": e["source"], "description": m.get("description", "")}
                    for e, m in local],
    })
    return out


def expected_copies(root: Path) -> dict[Path, Path]:
    """Every Copilot extension copy and the file it copies."""
    out = {}
    for pdir in plugin_dirs(root):
        for c in COPILOT_COMPONENTS:
            src = pdir / c
            if src.is_dir():
                out.update({pdir / COPILOT_DIR / c / f.relative_to(src): f
                            for f in src.rglob("*") if f.is_file() and "__pycache__" not in f.parts})
    return out


def copy_problems(root: Path) -> tuple[list[Path], list[Path]]:
    """(copies that are missing or differ, files in the extension directories that copy nothing)."""
    want = expected_copies(root)
    stale = [p for p, src in want.items()
             if p.is_symlink() or not p.is_file() or p.read_bytes() != src.read_bytes()]
    extra = [f for pdir in plugin_dirs(root) if (pdir / COPILOT_DIR).exists()
             for f in sorted((pdir / COPILOT_DIR).rglob("*"))
             if (f.is_file() or f.is_symlink()) and f not in want]
    return stale, extra


def sync(root: Path) -> int:
    for path, text in expected_files(root).items():
        if not path.exists() or path.read_text(encoding="utf-8") != text:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
            print(f"wrote {path.relative_to(root)}")
    stale, extra = copy_problems(root)
    want = expected_copies(root)
    for path in extra:
        path.unlink()
        print(f"removed {path.relative_to(root)}")
    for path in stale:
        for parent in [path, *path.parents]:  # a symlinked file or directory on the way
            if parent.is_symlink():
                parent.unlink()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(want[path].read_bytes())
        print(f"copied {path.relative_to(root)}")
    for pdir in plugin_dirs(root):  # drop directories the removals emptied
        for d in sorted((pdir / COPILOT_DIR).rglob("*"), reverse=True) if (pdir / COPILOT_DIR).is_dir() else []:
            if d.is_dir() and not any(d.iterdir()):
                d.rmdir()
        if (pdir / COPILOT_DIR).is_dir() and not any((pdir / COPILOT_DIR).iterdir()):
            (pdir / COPILOT_DIR).rmdir()
    return 0


# --- checks -----------------------------------------------------------------

def check_manifest(pdir: Path, root: Path, errors: list[str]) -> None:
    path = pdir / "plugin.json"
    rel = path.relative_to(root)
    if not path.is_file():
        errors.append(f"{rel}: missing (Agent Plugins requires a root plugin.json)")
        return
    m = load(path)
    if not isinstance(m, dict):
        errors.append(f"{rel}: must be a JSON object")
        return
    for k in sorted(set(m) - MANIFEST_FIELDS):
        errors.append(f"{rel}: unknown field {k!r}; the schema is closed (client fields go in extensions"
                      " or the client's own manifest)")
    if m.get("$schema") != PLUGIN_SCHEMA:
        errors.append(f"{rel}: $schema must be {PLUGIN_SCHEMA}")
    name = m.get("name")
    if not (isinstance(name, str) and PLUGIN_NAME.match(name)):
        errors.append(f"{rel}: name {name!r} breaks the Agent Plugins name rules")
    elif name != pdir.name:
        errors.append(f"{rel}: name {name!r} differs from its directory {pdir.name!r}")
    for k in ("version", "description", "homepage", "repository", "license"):
        if k in m and not isinstance(m[k], str):
            errors.append(f"{rel}: {k} must be a string")
    author = m.get("author")
    if author is not None and (not isinstance(author, dict) or set(author) - {"name", "email", "url"}
                               or not all(isinstance(v, str) for v in author.values())):
        errors.append(f"{rel}: author may only hold string name, email and url")
    kw = m.get("keywords")
    if kw is not None and not (isinstance(kw, list) and all(isinstance(x, str) for x in kw)):
        errors.append(f"{rel}: keywords must be a list of strings")
    ext = m.get("extensions")
    if ext is not None and not (isinstance(ext, dict) and all(isinstance(v, dict) for v in ext.values())):
        errors.append(f"{rel}: extensions must map namespaces to objects")


def check_mcp(pdir: Path, root: Path, errors: list[str]) -> None:
    path = pdir / "mcp.json"
    rel = path.relative_to(root)
    if (pdir / ".mcp.json").is_file() and not path.is_file():
        errors.append(f"{rel}: missing; {pdir.name} ships a Claude .mcp.json, and once plugin.json exists"
                      " Agent Plugins clients (Codex) load MCP servers only from mcp.json")
        return
    if not path.is_file():
        return
    m = load(path)
    if not isinstance(m, dict) or set(m) != {"$schema", "mcpServers"} or m["$schema"] != MCP_SCHEMA:
        errors.append(f"{rel}: must hold exactly $schema ({MCP_SCHEMA}) and mcpServers")
        return
    if not isinstance(m["mcpServers"], dict):
        errors.append(f"{rel}: mcpServers must be an object")
        return
    for name, server in m["mcpServers"].items():
        where = f"{rel}: server {name!r}"
        if not isinstance(server, dict) or server.get("type") not in MCP_VARIANTS:
            errors.append(f"{where}: type must be one of {sorted(MCP_VARIANTS)}")
            continue
        required, optional = MCP_VARIANTS[server["type"]]
        if missing := required - set(server):
            errors.append(f"{where}: missing {sorted(missing)}")
        if extra := set(server) - required - optional:
            errors.append(f"{where}: fields {sorted(extra)} are not allowed for type {server['type']!r}")
        if server["type"] == "stdio":
            cmd = server.get("command")
            if not isinstance(cmd, str) or not cmd or " " in cmd or "${" in cmd:
                errors.append(f"{where}: command must be one executable token with no placeholders")
            elif cmd.startswith("./"):
                if not inside(pdir / cmd, pdir):
                    errors.append(f"{where}: command {cmd!r} resolves outside the plugin root")
            elif "/" in cmd or "\\" in cmd:
                errors.append(f"{where}: command must be a bare executable name or a ./ plugin-relative path")
            if not all(isinstance(a, str) for a in server.get("args", [])):
                errors.append(f"{where}: args must be strings")
            env = server.get("env", {})
            if not isinstance(env, dict) or not all(isinstance(v, str) for v in env.values()):
                errors.append(f"{where}: env must map names to strings")
            elif {"PLUGIN_ROOT", "PLUGIN_DATA"} & set(env):
                errors.append(f"{where}: env must not set PLUGIN_ROOT or PLUGIN_DATA")
            if "cwd" in server:
                cwd = server["cwd"]
                if not (isinstance(cwd, str) and CWD.match(cwd)):
                    errors.append(f"{where}: cwd must start with ./, ${{PLUGIN_ROOT}} or ${{PLUGIN_DATA}}")
                elif not cwd_contained(cwd, pdir):
                    errors.append(f"{where}: cwd {cwd!r} resolves outside the plugin root or data directory")
            texts = [*server.get("args", []), *env.values(), server.get("cwd", "")]
            for t in texts:
                for var in re.findall(r"\$\{([^}]*)\}", t if isinstance(t, str) else ""):
                    if var not in ("PLUGIN_ROOT", "PLUGIN_DATA"):
                        errors.append(f"{where}: ${{{var}}} is never expanded by Agent Plugins clients")


def cwd_contained(cwd: str, pdir: Path) -> bool:
    """Whether a stdio cwd stays inside the root its form names, after `..` and symlinks."""
    if cwd.startswith("${PLUGIN_DATA}"):
        # The data directory is created by the client, so only `..` can escape it here.
        data = Path("/plugin-data")
        return Path(os.path.normpath(data / cwd[len("${PLUGIN_DATA}"):].lstrip("/"))).is_relative_to(data)
    rest = cwd[len("${PLUGIN_ROOT}"):] if cwd.startswith("${PLUGIN_ROOT}") else cwd
    return inside(pdir / rest.lstrip("/"), pdir)


def frontmatter(text: str):
    """The parsed YAML frontmatter, None if absent, or the YAMLError if it doesn't parse."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 3)
    if end < 0:
        return None
    try:
        return yaml.safe_load(text[4:end + 1]) or {}
    except yaml.YAMLError as e:
        return e


def link_targets(text: str):
    """(line number, target) for every link outside fenced code blocks and inline code."""
    fence = None
    for n, line in enumerate(text.splitlines(), 1):
        m = FENCE.match(line)
        if m:
            marker = m.group(2)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not line[m.end():].strip():
                fence = None
            continue
        if fence:
            continue
        line = re.sub(r"`[^`]*`", "", line)
        for rx in (INLINE_LINK, REF_DEF, WIKI_LINK):
            for target in rx.findall(line):
                yield n, target.strip()


def check_skills(pdir: Path, root: Path, errors: list[str]) -> None:
    sdir = pdir / "skills"
    if not sdir.is_dir():
        return
    for skill in sorted(p for p in sdir.iterdir() if p.is_dir()):
        md = skill / "SKILL.md"
        srel = skill.relative_to(root)
        if not inside(skill, pdir):
            errors.append(f"{srel}: resolves outside its plugin ({skill.resolve()})")
            continue
        if not md.is_file():
            errors.append(f"{srel}: no SKILL.md")
            continue
        fm = frontmatter(md.read_text(encoding="utf-8"))
        if fm is None:
            errors.append(f"{srel}/SKILL.md: no YAML frontmatter")
            continue
        if not isinstance(fm, dict):
            errors.append(f"{srel}/SKILL.md: frontmatter is not a YAML mapping ({fm})")
            continue
        if fm.get("name") != skill.name or not SKILL_NAME.match(skill.name):
            errors.append(f"{srel}/SKILL.md: name {fm.get('name')!r} must equal the lowercase-hyphenated"
                          f" directory name {skill.name!r}")
        desc = fm.get("description")
        if not isinstance(desc, str) or not 1 <= len(desc) <= 1024:
            errors.append(f"{srel}/SKILL.md: description must be a string of 1-1024 characters")
        for k in ("license", "compatibility", "allowed-tools"):
            if k in fm and not isinstance(fm[k], str):
                errors.append(f"{srel}/SKILL.md: {k} must be a string")
        # The spec wants string values; this repo's skills list their references under metadata.
        if not isinstance(fm.get("metadata", {}), dict):
            errors.append(f"{srel}/SKILL.md: metadata must be a mapping")
        for k in sorted(set(fm) - SKILL_FIELDS, key=str):
            errors.append(f"{srel}/SKILL.md: frontmatter field {k!r} is not in the Agent Skills spec")
        for f in sorted(skill.rglob("*")):
            frel = f.relative_to(root)
            if "__pycache__" in f.parts:
                continue
            if not inside(f, skill):
                errors.append(f"{frel}: resolves outside its skill ({f.resolve()})")
                continue
            # assets/ holds output templates whose links point into the user's project.
            if f.suffix != ".md" or not f.is_file() or "assets" in f.relative_to(skill).parts[:1]:
                continue
            for n, target in link_targets(f.read_text(encoding="utf-8")):
                if EXTERNAL.match(target):
                    continue
                path = target.split("#", 1)[0].split("?", 1)[0]
                if not path:
                    continue
                dest = (skill if path.startswith("/") else f.parent) / path.lstrip("/")
                if path.startswith("/") or not inside(dest, skill):
                    errors.append(f"{frel}:{n}: link {target!r} leaves the skill; a skill installed on its"
                                  " own can't follow it")
                elif not dest.exists() and not dest.with_suffix(".md").exists():
                    errors.append(f"{frel}:{n}: link {target!r} points at nothing")


def check_agents(pdir: Path, root: Path, errors: list[str]) -> None:
    for md in sorted((pdir / "agents").glob("*.md")):
        rel = md.relative_to(root)
        fm = frontmatter(md.read_text(encoding="utf-8"))
        if fm is None:
            continue
        if not isinstance(fm, dict):
            errors.append(f"{rel}: frontmatter is not a YAML mapping ({fm})")
            continue
        skills = fm.get("skills")
        if skills is not None and not (isinstance(skills, list) and all(isinstance(x, str) for x in skills)):
            errors.append(f"{rel}: skills must be a YAML list of names; Copilot CLI silently skips an agent"
                          " whose skills is a single string")


def check(root: Path, run_claude: bool) -> list[str]:
    errors: list[str] = []
    catalog = load(root / CATALOG)
    listed = {e.get("source") for e in catalog.get("plugins", [])}
    for pdir in plugin_dirs(root):
        src = "./" + pdir.relative_to(root).as_posix()
        if src not in listed:
            errors.append(f"{CATALOG}: no entry for {src}; add one with its category so every client can"
                          " install it")
        check_manifest(pdir, root, errors)
        check_mcp(pdir, root, errors)
        check_skills(pdir, root, errors)
        check_agents(pdir, root, errors)
    try:
        for path, text in expected_files(root).items():
            if not path.is_file() or path.read_text(encoding="utf-8") != text:
                errors.append(f"{path.relative_to(root)}: out of date; run .github/scripts/agent_plugins.py sync")
    except (ValueError, KeyError) as e:
        errors.append(str(e))
    stale, extra = copy_problems(root)
    for path in stale:
        errors.append(f"{path.relative_to(root)}: missing or differs from its original; Copilot CLI loads agents"
                      " and commands only from com.github.copilot/. Run .github/scripts/agent_plugins.py sync")
    for path in extra:
        errors.append(f"{path.relative_to(root)}: copies nothing in agents/ or commands/; run"
                      " .github/scripts/agent_plugins.py sync")
    if run_claude:
        errors += claude_validate([*plugin_dirs(root), root])
    return errors


def claude_validate(targets: list[Path]) -> list[str]:
    exe = shutil.which("claude")
    if not exe:
        return ["--claude: the claude CLI is not on PATH"]
    errors = []
    for t in targets:
        proc = subprocess.run([exe, "plugin", "validate", "--strict", "--json", str(t)],
                              capture_output=True, text=True, check=False)
        try:
            out = json.loads(proc.stdout)
        except json.JSONDecodeError:
            errors.append(f"{t}: claude plugin validate printed no JSON (exit {proc.returncode}): {proc.stderr[:300]}")
            continue
        manifest = out.get("manifest")
        # The exit status can't be trusted either way: a directory Claude can't
        # read as a plugin exits 0 with manifest null, and --strict exits 1 on
        # a component warning. Decide from the report.
        if not manifest:
            errors.append(f"{t}: claude plugin validate failed or found no manifest: {json.dumps(out)[:600]}")
            continue
        if manifest.get("errors") or manifest.get("warnings"):
            errors.append(f"{t}: {manifest.get('file')}: {manifest.get('errors')} {manifest.get('warnings')}")
        # Component errors fail; component warnings (such as an unloaded root
        # CLAUDE.md) are reported for the plugin's maintainers.
        for item in out.get("contents") or []:
            if item.get("errors"):
                errors.append(f"{t}: {item.get('file')}: {item['errors']}")
            for w in item.get("warnings") or []:
                print(f"warning: {item.get('file')}: {w.get('message')}", file=sys.stderr)
    return errors


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["sync", "check"])
    ap.add_argument("--claude", action="store_true", help="check: also run claude plugin validate --strict")
    ap.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    if args.command == "sync":
        return sync(args.root)
    errors = check(args.root, args.claude)
    for e in errors:
        print(f"error: {e}", file=sys.stderr)
    print(f"{len(plugin_dirs(args.root))} plugins: {'OK' if not errors else f'{len(errors)} problems'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

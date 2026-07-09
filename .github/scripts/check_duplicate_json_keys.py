#!/usr/bin/env python3
"""Fail CI if any JSON file contains duplicate keys within an object.

The sibling ``jq empty`` validation step accepts duplicate keys: JSON parsers
keep the *last* value for a repeated key, so a duplicated key is silently
collapsed rather than reported as invalid. In ``.claude-plugin/marketplace.json``
that last-wins behavior can drop an entire plugin entry from the catalog — and
because the security scans build their target list from that catalog, the
dropped plugin's files stop being scanned. This check walks every JSON file and
rejects duplicate keys so that class of defect fails loudly.

Usage:
    check_duplicate_json_keys.py [ROOT ...]

Each ROOT may be a directory (scanned recursively for ``*.json``) or a single
JSON file. Defaults to the current directory.
"""

from __future__ import annotations

import json
import pathlib
import sys

# Directories that never contain first-party JSON worth validating.
SKIP_DIR_PARTS = {".git", "node_modules"}


def reject_duplicates(pairs):
    """object_pairs_hook that raises on the first duplicate key it sees."""
    seen = set()
    for key, _value in pairs:
        if key in seen:
            raise ValueError(f"duplicate key: {key!r}")
        seen.add(key)
    return dict(pairs)


def iter_json_files(roots):
    for root in roots:
        path = pathlib.Path(root)
        candidates = [path] if path.is_file() else sorted(path.rglob("*.json"))
        for candidate in candidates:
            # tsconfig*.json is JSONC (allows comments); the jq step skips it too.
            if candidate.name.startswith("tsconfig"):
                continue
            if SKIP_DIR_PARTS.intersection(candidate.parts):
                continue
            yield candidate


def main(argv):
    roots = argv[1:] or ["."]
    failed = False
    for path in iter_json_files(roots):
        try:
            json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
        except ValueError as exc:
            print(f"::error file={path}::{exc}")
            print(f"❌ {path}: {exc}")
            failed = True

    if failed:
        print("Duplicate JSON keys detected — each JSON object must have unique keys.")
        return 1
    print("✅ No duplicate JSON keys detected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

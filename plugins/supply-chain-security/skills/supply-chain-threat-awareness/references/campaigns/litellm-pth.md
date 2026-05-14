# LiteLLM 1.82.8 — `.pth` Persistence Campaign

**Vector:** Malicious `.pth` file shipped inside a Python package.
**Persistence mechanism:** Python loads every `.pth` file in `site-packages` on every interpreter start. A `.pth` file with a leading `import ...` line executes that import.

## Attack mechanics

1. Compromised PyPI release ships a `.pth` file containing executable Python (`import os; os.system(...)`).
2. After `pip install`, the file lives in `site-packages/`.
3. Every subsequent `python ...` invocation triggers the payload — survives package upgrades and uninstalls if the `.pth` file isn't deleted.

## Indicators of exposure

```bash
find $(python -c "import site; print(site.getsitepackages()[0])") -name "*.pth" -exec sh -c 'echo "=== {} ==="; cat {}' \;
```

Look for `.pth` files containing `import` statements other than benign path additions. A normal `.pth` file contains only directory paths, one per line.

## Containment checklist

- [ ] Run the find command above; flag any `.pth` file containing executable Python.
- [ ] Identify which package shipped the `.pth` file (`pip show <pkg>` and inspect `RECORD`).
- [ ] Pin to a known-good prior version in the lockfile.
- [ ] Delete the malicious `.pth` file from every venv where it landed.
- [ ] Rotate any secret that was accessible to a Python process started after install.

## References

- `supply-chain-dependency-security` skill (Python install-time execution)
- `supply-chain-ecosystem-quirks/references/pypi-quirks.md`

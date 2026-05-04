from pathlib import Path


def file_contains(output, context):
    cfg = context["config"]
    file = Path(cfg["file"])
    if not file.exists():
        return False
    contains_key = cfg["contains_key"]
    value = context["vars"][contains_key]
    content = file.read_text()
    return value in content

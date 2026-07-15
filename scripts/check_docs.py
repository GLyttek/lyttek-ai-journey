#!/usr/bin/env python3
"""Check local Markdown links and README coverage for numbered chapters."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
REMOTE_PREFIXES = ("http://", "https://", "mailto:", "data:")


def local_link_errors() -> list[str]:
    errors: list[str] = []
    for document in sorted(ROOT.rglob("*.md")):
        if ".git" in document.parts:
            continue
        text = document.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().split("#", 1)[0]
            if not target or target.startswith(REMOTE_PREFIXES):
                continue
            resolved = (document.parent / unquote(target)).resolve()
            if not resolved.exists():
                source = document.relative_to(ROOT)
                errors.append(f"{source}: missing local target {raw_target!r}")
    return errors


def chapter_index_errors() -> list[str]:
    readme = README.read_text(encoding="utf-8")
    errors: list[str] = []
    for chapter in sorted((ROOT / "docs").glob("[0-9][0-9]_*.md")):
        relative = chapter.relative_to(ROOT).as_posix()
        if relative not in readme:
            errors.append(f"README.md: numbered chapter is not indexed: {relative}")
    return errors


def main() -> int:
    errors = local_link_errors() + chapter_index_errors()
    if errors:
        print("Documentation checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    chapter_count = len(list((ROOT / "docs").glob("[0-9][0-9]_*.md")))
    print(f"Documentation checks passed: local links valid, {chapter_count} chapters indexed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

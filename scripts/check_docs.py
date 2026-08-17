#!/usr/bin/env python3
"""Check Markdown links and README coverage for numbered chapters."""

from __future__ import annotations

import argparse
import concurrent.futures
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlsplit, urlunsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
REMOTE_PREFIXES = ("http://", "https://", "mailto:", "data:")
HTTP_PREFIXES = ("http://", "https://")
USER_AGENT = "lyttek-ai-journey-doc-check/1.0"


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


def normalized_http_links() -> list[str]:
    links: set[str] = set()
    for document in sorted(ROOT.rglob("*.md")):
        if ".git" in document.parts:
            continue
        text = document.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip()
            if not target.startswith(HTTP_PREFIXES):
                continue
            parts = urlsplit(target)
            links.add(urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, "")))
    return sorted(links)


def probe_http_link(url: str, timeout: float) -> tuple[str, str]:
    """Return (severity, message) for one URL.

    Only a confirmed 404 or 410 is a documentation failure. Access controls,
    rate limits, server errors, and network failures are reported as warnings
    because a public CI runner cannot distinguish them reliably from a dead URL.
    """

    headers = {"User-Agent": USER_AGENT, "Range": "bytes=0-0"}
    try:
        request = Request(url, headers=headers, method="GET")
        with urlopen(request, timeout=timeout) as response:
            response.read(1)
            return "ok", f"{response.status} {url}"
    except HTTPError as exc:
        if exc.code in {404, 410}:
            return "error", f"{exc.code} {url}"
        return "warning", f"HTTP {exc.code} {url}"
    except (URLError, TimeoutError, OSError) as exc:
        reason = getattr(exc, "reason", exc)
        return "warning", f"{type(reason).__name__}: {url}"


def external_link_results(timeout: float, workers: int) -> tuple[list[str], list[str], int]:
    links = normalized_http_links()
    errors: list[str] = []
    warnings: list[str] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(probe_http_link, url, timeout): url for url in links}
        for future in concurrent.futures.as_completed(futures):
            severity, message = future.result()
            if severity == "error":
                errors.append(message)
            elif severity == "warning":
                warnings.append(message)
    return sorted(errors), sorted(warnings), len(links)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--external",
        action="store_true",
        help="also probe external HTTP links; confirmed 404/410 responses fail",
    )
    parser.add_argument("--timeout", type=float, default=30.0, help="per-link timeout in seconds")
    parser.add_argument("--workers", type=int, default=8, help="parallel external probes")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = local_link_errors() + chapter_index_errors()
    warnings: list[str] = []
    external_count = 0
    if args.external:
        external_errors, warnings, external_count = external_link_results(
            timeout=args.timeout,
            workers=max(1, args.workers),
        )
        errors.extend(f"external link: {error}" for error in external_errors)

    if warnings:
        print("External links not conclusively verified:")
        for warning in warnings:
            print(f"- {warning}")

    if errors:
        print("Documentation checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    chapter_count = len(list((ROOT / "docs").glob("[0-9][0-9]_*.md")))
    summary = f"Documentation checks passed: local links valid, {chapter_count} chapters indexed"
    if args.external:
        summary += f", {external_count} external links checked ({len(warnings)} inconclusive)"
    print(f"{summary}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

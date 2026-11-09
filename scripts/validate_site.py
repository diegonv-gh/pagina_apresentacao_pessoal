#!/usr/bin/env python3
"""Check that local files referenced by the static site exist."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
HTML_FILE = ROOT / "index.html"
CSS_FILE = ROOT / "style.css"
REFERENCE_ATTRIBUTES = {"src", "href", "data-img"}
CSS_URL_PATTERN = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.IGNORECASE)


class ReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[tuple[str, int]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name.lower() in REFERENCE_ATTRIBUTES and value:
                self.references.append((value, self.getpos()[0]))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)


def is_external_or_fragment(reference: str) -> bool:
    return reference.startswith(("#", "//")) or bool(urlsplit(reference).scheme)


def resolve_local_reference(reference: str, source_file: Path) -> Path | None:
    if is_external_or_fragment(reference):
        return None

    path = unquote(urlsplit(reference).path)
    if not path:
        return None

    if path.startswith("/"):
        path = path.lstrip("/")
        return ROOT / path
    return source_file.parent / path


def main() -> int:
    if not HTML_FILE.is_file() or not CSS_FILE.is_file():
        print("Required site entry files index.html and style.css must exist.", file=sys.stderr)
        return 1

    parser = ReferenceParser()
    parser.feed(HTML_FILE.read_text(encoding="utf-8"))

    errors: list[str] = []
    for reference, line in parser.references:
        target = resolve_local_reference(reference, HTML_FILE)
        if target is not None and not target.is_file():
            errors.append(f"index.html:{line}: local reference not found: {reference}")

    css_text = CSS_FILE.read_text(encoding="utf-8")
    for match in CSS_URL_PATTERN.finditer(css_text):
        reference = match.group(2).strip()
        target = resolve_local_reference(reference, CSS_FILE)
        if target is not None and not target.is_file():
            line = css_text.count("\n", 0, match.start()) + 1
            errors.append(f"style.css:{line}: local reference not found: {reference}")

    if errors:
        print("Site reference validation failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1

    print("Site reference validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""A tiny jemdoc-style renderer for this personal homepage.

It supports the subset used by index.jemdoc: title lines, paragraphs, lists,
raw HTML blocks, and per-page CSS declarations.
"""

from __future__ import annotations

import html
import os
import re
import sys
from pathlib import Path


DEFAULT_SITE_URL = "https://wang-mingjun.github.io/"


def site_url() -> str:
    """Return the canonical site root, with one trailing slash."""
    value = os.environ.get("HOMEPAGE_URL", DEFAULT_SITE_URL).strip()
    if not re.fullmatch(r"https://[^\s/]+(?:/[^\s]*)?", value):
        raise ValueError("HOMEPAGE_URL must be an absolute HTTPS URL")
    return value.rstrip("/") + "/"


def inline_markup(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    text = re.sub(r"\[(https?://[^\s\]]+)\s+([^\]]+)\]", r'<a href="\1">\2</a>', text)
    return text


def render(source: Path) -> str:
    title = "Mingjun Wang"
    description = (
        "Mingjun Wang is a Ph.D. student in Computer Science and Engineering "
        "at The Chinese University of Hong Kong, working on AI4EDA, "
        "flow-oriented 3D IC EDA design automation, circuit representation "
        "learning, and fault simulation."
    )
    css_files: list[str] = []
    canonical_url = site_url()
    body: list[str] = []
    paragraph: list[str] = []
    in_raw = False
    in_list = False

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            body.append("<p>" + inline_markup(" ".join(paragraph)) + "</p>")
            paragraph = []

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            body.append("</ul>")
            in_list = False

    for raw_line in source.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()

        if line.startswith("# jemdoc:"):
            css_match = re.search(r"addcss\{([^}]+)\}", line)
            if css_match:
                css_files.append(css_match.group(1))
            title_match = re.search(r"addtitle\{([^}]+)\}", line)
            if title_match:
                title = title_match.group(1)
            continue

        if in_raw:
            if line == "~~~":
                in_raw = False
            else:
                body.append(raw_line)
            continue

        if line == "~~~html":
            flush_paragraph()
            close_list()
            in_raw = True
            continue

        if not line:
            flush_paragraph()
            close_list()
            continue

        if line.startswith("==="):
            flush_paragraph()
            close_list()
            body.append(f"<h3>{inline_markup(line[3:].strip())}</h3>")
        elif line.startswith("=="):
            flush_paragraph()
            close_list()
            body.append(f"<h2>{inline_markup(line[2:].strip())}</h2>")
        elif line.startswith("="):
            flush_paragraph()
            close_list()
            body.append(f"<h1>{inline_markup(line[1:].strip())}</h1>")
        elif line.startswith("- "):
            flush_paragraph()
            if not in_list:
                body.append("<ul>")
                in_list = True
            body.append(f"<li>{inline_markup(line[2:].strip())}</li>")
        else:
            paragraph.append(line)

    flush_paragraph()
    close_list()

    css_tags = "\n".join(
        f'  <link rel="stylesheet" href="{html.escape(css)}" type="text/css" />'
        for css in dict.fromkeys(css_files)
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="{html.escape(description)}" />
  <meta property="og:title" content="{html.escape(title)}" />
  <meta property="og:description" content="{html.escape(description)}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{html.escape(canonical_url)}" />
  <meta property="og:image" content="{html.escape(canonical_url)}assets/photo.jpg" />
  <meta name="theme-color" content="#1F3A93" />
  <meta name="generator" content="jemdoc-style renderer" />
  <link rel="icon" type="image/png" sizes="512x512" href="favicon.png" />
  <link rel="shortcut icon" type="image/png" href="favicon.png" />
  <link rel="icon" type="image/png" sizes="48x48" href="assets/favicon-48.png?v=20260716" />
  <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png?v=20260716" />
  <link rel="icon" type="image/png" sizes="192x192" href="assets/icon-192.png?v=20260716" />
  <link rel="apple-touch-icon" sizes="180x180" href="assets/apple-touch-icon.png?v=20260716" />
  <link rel="canonical" href="{html.escape(canonical_url)}" />
  <title>{html.escape(title)}</title>
{css_tags}
</head>
<body>
{chr(10).join(body)}
</body>
</html>
"""


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: render_jemdoc.py index.jemdoc")
    source = Path(sys.argv[1])
    output = source.with_suffix(".html")
    output.write_text(render(source), encoding="utf-8")
    print(f"generated {output}")


if __name__ == "__main__":
    main()

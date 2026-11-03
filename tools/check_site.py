#!/usr/bin/env python3
"""Offline release checks: python3 tools/check_site.py."""

import collections
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import unicodedata
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

from export_cv_publications import Publications
from render_jemdoc import render

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "index.html").read_text(encoding="utf-8")
errors = []


def check(condition, message):
    if not condition:
        errors.append(message)


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.anchors = []
        self.sections = []
        self.voids = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
        self.stack = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag not in self.voids:
            self.stack.append(tag)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "section" and "id" in attrs:
            self.sections.append(attrs["id"])
        if tag == "img":
            check("alt" in attrs, "Image is missing alt text")
        if tag == "a":
            href = attrs.get("href", "")
            if href.startswith("#"):
                self.anchors.append(href[1:])
            if href.startswith("https://"):
                check(attrs.get("target") == "_blank" and "noopener" in attrs.get("rel", "").split(), f"External link lacks safe new-tab attributes: {href}")
        for key in ("src", "href"):
            value = attrs.get(key, "")
            url = urlsplit(value)
            if value and not url.scheme and not url.netloc and url.path:
                check((ROOT / unquote(url.path.lstrip("/"))).is_file(), f"Missing local asset: {value}")

    def handle_endtag(self, tag):
        if tag in self.voids:
            return
        check(bool(self.stack) and self.stack[-1] == tag, f"Mismatched HTML closing tag: {tag}")
        if self.stack:
            self.stack.pop()

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.voids:
            self.handle_endtag(tag)


page = Page()
page.feed(html)
check(not page.stack, "Unclosed HTML tags")
check(len(page.ids) == len(set(page.ids)), "Duplicate element IDs")
check(all(anchor in page.ids for anchor in page.anchors), "Broken internal anchor")
check(page.sections == ["about", "news", "research", "education", "publications", "experience", "awards", "service", "skills", "contact"], "Unexpected section order")
check(html == render(ROOT / "index.jemdoc"), "index.html is stale; render index.jemdoc first")
check('<link rel="canonical" href="https://wang-mingjun.github.io/"' in html, "Incorrect canonical URL")
check(not re.search(r"noindex|nofollow", html, re.I), "Unexpected indexing block")
check((ROOT / "googleeb48c6bcf48b80a4.html").read_text().strip() == "google-site-verification: googleeb48c6bcf48b80a4.html", "Incorrect Google verification file")
duplicate = ROOT / "googleeb48c6bcf48b80a4 (1).html"
if duplicate.exists():
    check(duplicate.read_bytes() == (ROOT / "googleeb48c6bcf48b80a4.html").read_bytes(), "Downloaded verification file differs from public file")
check("Disallow: /" not in (ROOT / "robots.txt").read_text(), "robots.txt blocks the website")
tree = ET.parse(ROOT / "sitemap.xml")
check(tree.findtext("{*}url/{*}loc") == "https://wang-mingjun.github.io/", "Incorrect sitemap URL")

publications = Publications()
publications.feed(html)
check(len(publications.records) == 21, "Expected 21 accepted/published papers")
check(collections.Counter(p["type"] for p in publications.records) == {"Conference": 19, "Journal": 2}, "Incorrect Conference/Journal counts")
check(len({p["title"] for p in publications.records}) == 21, "Duplicate publication")
check(all("Mingjun Wang" in p["authors"] for p in publications.records), "Missing author on a paper")
check(all(p["link"].startswith("https://") for p in publications.records), "Publication lacks a public record link")
check(sum(p["authors"].startswith("Mingjun Wang") or "Mingjun Wang†" in p["authors"] for p in publications.records) == 12, "Expected 12 first/co-first-author papers")
check(any(p["title"].startswith("MigSizer:") for p in publications.records), "Confirmed accepted MigSizer paper is missing")
survey = next(p for p in publications.records if p["title"].startswith("LLM-Assisted Circuit Verification:"))
check("Invited Paper" in survey["honors"], "ASP-DAC 2026 survey invitation is missing")
check(len(re.findall(r'<p class="authors">.*?<strong>Mingjun Wang[†‡]?</strong>', html)) == 21, "Owner not bold in every paper")
hoist = next(p for p in publications.records if p["title"].startswith("HOIST:"))
check("Mingjun Wang‡" in hoist["authors"] and "Binwu Zhu‡" in hoist["authors"] and "Mingjun Wang†" not in hoist["authors"], "Incorrect HOIST corresponding-author marks")
domsim = next(p for p in publications.records if p["title"].startswith("DomSim:"))
check("2026" in domsim["meta"] and "Zhongkai Yu, Zheng Liang" in domsim["authors"] and "Jing Ye, Xiaowei Li, Bei Yu, Huawei Li" in domsim["authors"], "DomSim final publication record differs")
check(html.count("Jul. 2023 — Mar. 2025") == 1 and html.count("Sep. 2021 — Jan. 2025") == 1, "Experience dates changed")
check(html.count("1st Prize — EDA²") == 1, "Duplicate EDA award")
for award in ["3rd Prize (Team Competition)", "Merit Student", "Future Star"]:
    check(award in html, f"Website missing audited award: {award}")
check("Huawei Intelligent Base Scholarship" not in html, "Outdated Huawei award name")
check("3.77/4.0" in html and "3.78/4.0" not in html, "Website GPA differs from the owner's confirmed value")
for word in ["DistillTune", "ADAPT:", "Graph World Models", "Patents", "18518983880", "SILICA-Bench_Technical"]:
    check(word not in html, f"Private/non-accepted material in public HTML: {word}")

cv_text = subprocess.check_output(["pdftotext", str(ROOT / "assets/cv.pdf"), "-"], text=True)
cv_text = unicodedata.normalize("NFKC", cv_text)
check("3.77/4.0" in cv_text and "3.78/4.0" not in cv_text, "Public CV GPA differs from the owner's confirmed value")
for name in ["CU-3D:", "HOIST:", "Distill3D:", "MigSizer:", "LLM4EDA / AI4EDA", "Co-corresponding"]:
    check(name in cv_text, f"Public CV missing {name}")
for award in ["Third Prize, Team Competition", "Merit Student", "Future Star"]:
    check(award in cv_text, f"Public CV missing audited award: {award}")
for word in ["18518983880", "DistillTune", "ADAPT:", "CN119272672A"]:
    check(word not in cv_text, f"Private material in public CV: {word}")

if errors:
    raise SystemExit("FAILED:\n" + "\n".join("- " + error for error in errors))
print("PASS: render, HTML, assets, anchors, metadata, Google verification, 21 publications, public CV and content boundaries")

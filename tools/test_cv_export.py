#!/usr/bin/env python3
"""Regression checks for CV export; optionally inspect compiled PDF targets."""

import argparse
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

from export_cv_publications import Publications, export, tex, tex_url

ROOT = Path(__file__).resolve().parents[1]


class ExportTests(unittest.TestCase):
    def test_url_keeps_tilde_and_escapes_tex_syntax(self):
        self.assertEqual(tex_url("https://example.org/~name/a_b?q=one&x=20%25#s"),
                         r"https://example.org/~name/a\_b?q=one\&x=20\%25\#s")
        self.assertEqual(tex_url("https://example.org/{x} ^"),
                         r"https://example.org/\%7Bx\%7D\%20\%5E")
        self.assertEqual(tex("a~b"), r"a\textasciitilde{}b")

    def test_real_publication_export(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "papers.tex"
            export(ROOT / "index.jemdoc", path)
            result = path.read_text()
        self.assertEqual(result.count(r"\publication{"), 22)
        cu3d = next(line for line in result.splitlines() if "{CU-3D:" in line)
        self.assertIn(r"\href{https://arxiv.org/pdf/2611.11475v2}{CU-3D:", cu3d)
        self.assertIn(r"\textbf{Mingjun Wang}\textsuperscript{\dag}, Guanqi Li\textsuperscript{\dag}, Yihan Wen", cu3d)
        self.assertEqual(cu3d.count(r"\textsuperscript{\dag}"), 2)
        spectra = next(line for line in result.splitlines() if "SPECTRA-3D" in line)
        self.assertIn(r"Guanqi Li\textsuperscript{\dag}, \textbf{Mingjun Wang}\textsuperscript{\dag}, Siqi Hong", spectra)
        self.assertIn("Dresden", spectra)
        poster = next(line for line in result.splitlines() if "CircuitNet 3.0:" in line)
        self.assertTrue(poster.endswith("{Poster}"))
        self.assertTrue(spectra.endswith("Accepted.}{}"))
        self.assertNotIn("{Co-first", result)
        self.assertIn(r"\href{https://www.cse.cuhk.edu.hk/~byu/", result)
        self.assertNotIn(r"\href{https://www.cse.cuhk.edu.hk/\textasciitilde", result)


def check_pdf(path):
    parser = Publications()
    parser.feed((ROOT / "index.jemdoc").read_text())
    expected = {r["link"] for r in parser.records if r["link"]}
    output = subprocess.check_output(["pdfinfo", "-url", str(path)], text=True)
    actual = {m.group(1) for line in output.splitlines()
              if (m := re.match(r"\s*\d+\s+Annotation\s+(\S+)\s*$", line))}
    missing = expected - actual
    if missing:
        raise AssertionError(f"PDF has missing or altered publication targets: {sorted(missing)}")
    if any("{" in url or "}" in url or "textasciitilde" in url for url in actual):
        raise AssertionError("PDF contains LaTeX artifacts in URL annotations")
    print(f"PASS: {path.name}: all {len(expected)} unique publication URLs preserved")


if __name__ == "__main__":
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument("--pdf", type=Path, action="append", default=[])
    options = args.parse_args()
    result = unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(ExportTests))
    if not result.wasSuccessful():
        raise SystemExit(1)
    for pdf in options.pdf:
        check_pdf(pdf)

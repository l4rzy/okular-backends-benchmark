# SPDX-License-Identifier: GPL-3.0-or-later
import copy
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

import run_pdfium


def summary():
    return {"timestamp_utc": "2026-11-14T12:00:00+00:00", "run_id": "123-1",
            "run_url": "https://example.invalid/run", "mupdf_commit": "a" * 40,
            "pdfium_commit": "b" * 40, "pdfium_library_sha256": "c" * 64,
            "cpu_model": "test CPU", "corpus_sha256": "d" * 64,
            "configuration": {"repeats": 2, "pages": 2, "width": 1200, "seed": 1},
            "score": {"median": 2, "ci95": [1.5, 2.5]},
            "documents": [{"id": "one", "pages": 2, "ratio_median": 2,
                           "mupdf_median_ms": 10, "pdfium_median_ms": 20}]}


class TestPdfium(unittest.TestCase):
    def test_primary_render_excludes_other_phases(self):
        report = {"document_id": "one", "page_count": 2,
                  "samples": [{"phase": phase, "page": page, "ok": True,
                               "cached_before": phase == "cached", "elapsed_ms": elapsed}
                              for phase, page, elapsed in
                              [("first_page", 0, 2), ("sequential", 1, 3), ("cached", 0, 100)]]}
        self.assertEqual(run_pdfium.render_time(report, 20), 5)
        for change in ({"ok": False}, {"elapsed_ms": float("nan")},
                       {"elapsed_ms": 0}, {"cached_before": True}, {"page": 1}):
            with self.subTest(change=change):
                bad = copy.deepcopy(report)
                bad["samples"][0].update(change)
                with self.assertRaises(ValueError):
                    run_pdfium.render_time(bad, 20)
        report["samples"].pop(1)
        with self.assertRaises(ValueError):
            run_pdfium.render_time(report, 20)

    def test_chart_and_tables_are_separate_from_poppler(self):
        latest = summary()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            readme = root / "README.md"
            readme.write_text("Poppler history stays here\n")
            page = root / "PDFIUM.md"
            page.write_text("Custom introduction\n")
            rendered = run_pdfium.update_markdown(page, [latest], latest)
            page.write_text(rendered)
            self.assertEqual(run_pdfium.update_markdown(page, [latest], latest), rendered)
            self.assertIn("Custom introduction", rendered)
            self.assertIn("(pdfium-trend.svg)", rendered)
            self.assertIn("| one | 2 | 2.000× | 10.000 | 20.000 |", rendered)
            self.assertIn("2.000× (1.500–2.500)", rendered)
            self.assertEqual(readme.read_text(), "Poppler history stays here\n")
            chart = root / "pdfium-trend.svg"
            run_pdfium.plot_trend([latest], chart)
            self.assertTrue(ET.parse(chart).getroot().tag.endswith("svg"))
            self.assertIn("PDFium / MuPDF-NG", chart.read_text())


if __name__ == "__main__":
    unittest.main()

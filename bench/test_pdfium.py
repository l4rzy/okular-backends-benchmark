# SPDX-License-Identifier: GPL-3.0-or-later
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
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
    def test_installed_package_discovery(self):
        with tempfile.TemporaryDirectory() as directory:
            plugin = Path(directory) / "okularGenerator_mupdfng.so"
            plugin.write_bytes(b"installed plugin")
            with patch.object(run_pdfium.subprocess, "check_output", side_effect=[
                "okular-mupdf-ng 1.2.3-1\n",
                f"okular-mupdf-ng /usr/\nokular-mupdf-ng {plugin}\n",
            ]):
                discovered, metadata = run_pdfium.installed_mupdf_package("okular-mupdf-ng")
            self.assertEqual(discovered, plugin)
            self.assertEqual(metadata["version"], "okular-mupdf-ng 1.2.3-1")
            self.assertEqual(metadata["plugin_sha256"], run_pdfium.common.file_hash(plugin))
            with patch.object(run_pdfium.subprocess, "check_output", side_effect=[
                "okular-mupdf-ng 1.2.3-1\n", "okular-mupdf-ng /usr/\n",
            ]):
                with self.assertRaisesRegex(ValueError, "Expected one installed"):
                    run_pdfium.installed_mupdf_package("okular-mupdf-ng")

    def test_packaged_run_without_mupdf_checkout(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin = root / "okularGenerator_mupdfng.so"
            pdfium = root / "pdfium-backend"
            pdfium_plugin = pdfium / "build/plugins/okular_generators/okularGenerator_pdfium.so"
            library = pdfium / "pdfium/lib/libpdfium.so"
            harness = root / "harness"
            for path in (plugin, pdfium_plugin, library, harness):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"fixture")
            package = {"name": "okular-mupdf-ng", "version": "okular-mupdf-ng 1.2.3-1"}
            paper = {"id": "one", "path": root / "one.pdf", "pages": 1, "sha256": "paper"}

            def trial(command, timeout):
                backend = command[command.index("--backend") + 1]
                return {"status": "ok", "page_count": 1, "samples": [
                    {"phase": "first_page", "page": 0, "width": 1200, "height": 1600,
                     "ok": True, "cached_before": False, "elapsed_ms": 2 if backend == "pdfium" else 1}]}

            arguments = ["run_pdfium.py", "--mupdf-package", "okular-mupdf-ng",
                         "--source-dir", str(root / "absent-mupdf-checkout"),
                         "--pdfium-source-dir", str(pdfium), "--harness", str(harness),
                         "--results-dir", str(root / "results"), "--run-id", "123-1",
                         "--run-url", "https://example.invalid/run", "--repeats", "2",
                         "--output", str(root / "samples.jsonl")]
            with (patch.object(run_pdfium.sys, "argv", arguments),
                  patch.object(run_pdfium, "installed_mupdf_package", return_value=(plugin, package)),
                  patch.object(run_pdfium, "git_value", return_value="b" * 40) as git,
                  patch.object(run_pdfium.common, "load_corpus", return_value=([paper], {"sha256": "corpus"})),
                  patch.object(run_pdfium.common, "run_trial", side_effect=trial)):
                self.assertEqual(run_pdfium.main(), 0)
                git.assert_called_once_with(pdfium, "rev-parse", "HEAD")
            result = json.loads((root / "results/reports-pdfium/123-1.json").read_text())
            self.assertIsNone(result["mupdf_commit"])
            self.assertEqual(result["mupdf_package"], package)
            self.assertEqual(result["score"]["median"], 2)
            self.assertIn(package["version"], (root / "results/PDFIUM.md").read_text())
            self.assertTrue((root / "results/pdfium-trend.svg").is_file())

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

# SPDX-License-Identifier: GPL-3.0-or-later
import argparse
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import run


class TestRunner(unittest.TestCase):
    def test_source_and_benchmark_provenance_are_separate(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            (source / "cmake").mkdir()
            (source / "cmake/mupdf.version").write_text("1.2.3\nchecksum\n")

            def command_output(command):
                if command[0] == "git":
                    if command[-1] == "HEAD":
                        return "plugin-commit" if command[2] == str(source) else "benchmark-commit"
                    return ""
                return "test version"

            with patch.object(run, "command_output", side_effect=command_output):
                environment = run.collect_environment({}, source)
            self.assertEqual(environment["source_commit"], "plugin-commit")
            self.assertEqual(environment["benchmark_commit"], "benchmark-commit")
            self.assertFalse(environment["source_dirty"])
            self.assertFalse(environment["benchmark_dirty"])
            self.assertEqual(environment["versions"]["mupdf"], "1.2.3")

    def test_manifest_verification(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            corpus = root / "corpus"
            corpus.mkdir()
            pdf = corpus / "paper.pdf"
            pdf.write_bytes(b"fixture")
            paper = {"arxiv_id": "paper", "path": "corpus/paper.pdf", "sha256": run.file_hash(pdf)}
            manifest = corpus / "manifest.json"
            def write(papers):
                manifest.write_text(json.dumps({"papers": papers, "corpus_version": 1}))
            write([paper])
            papers, metadata = run.load_corpus(manifest)
            self.assertEqual(papers[0]["path"], pdf)
            self.assertEqual(metadata["sha256"], run.file_hash(manifest))
            for entries in ([], [paper, paper], [{**paper, "sha256": "wrong"}],
                            [{**paper, "path": "../outside.pdf"}]):
                with self.subTest(entries=entries):
                    write(entries)
                    with self.assertRaises(ValueError):
                        run.load_corpus(manifest)

    def test_pdf_path(self):
        for path in ("a.pdf", "a.PDF"):
            with self.subTest(path=path):
                self.assertEqual(run.pdf_path(path), Path(path))
        for path in ("a.txt", "a.epub", "a.pdf.zip", "a"):
            with self.subTest(path=path), self.assertRaises(argparse.ArgumentTypeError):
                run.pdf_path(path)

    def test_backend_order(self):
        for trial, expected in [(0, ("mupdfng", "poppler")), (1, ("poppler", "mupdfng")),
                                (2, ("mupdfng", "poppler"))]:
            with self.subTest(trial=trial):
                self.assertEqual(run.backend_order(trial), expected)

    def test_percentile(self):
        for values, fraction, expected in [([5], .95, 5), ([4, 1, 3, 2], .5, 2),
                                           (list(range(1, 101)), .95, 95)]:
            with self.subTest(values=values):
                self.assertEqual(run.percentile(values, fraction), expected)

    def test_process_results(self):
        cases = [("print('not json')", "error"),
                 ("import sys; print('{\"status\":\"ok\"}'); sys.exit(1)", "error"),
                 ("print('{\"status\":\"ok\"}')", "ok"),
                 ("print('[]')", "error")]
        for code, status in cases:
            with self.subTest(code=code):
                report = run.run_trial([sys.executable, "-c", code], 5)
                self.assertEqual(report["status"], status)

    def test_timeout(self):
        report = run.run_trial([sys.executable, "-c", "import time; time.sleep(10)"], .05)
        self.assertEqual(report["status"], "error")
        self.assertIn("timeout", report["error"])

    def test_start_failure(self):
        report = run.run_trial([sys.executable + "/missing"], 5)
        self.assertEqual(report["status"], "error")
        self.assertIn("Cannot start harness", report["error"])

    def test_summary_separates_cache_hits_and_excludes_failed_trials(self):
        report = {"status": "ok", "pdf": "x.pdf", "backend": "poppler", "open_ms": 3,
                  "open_to_first_page_ms": 5, "samples": [
                      {"ok": True, "phase": "random", "cached_before": False, "elapsed_ms": 2},
                      {"ok": True, "phase": "random", "cached_before": True, "elapsed_ms": .01}]}
        failed = json.loads(json.dumps(report))
        failed["status"] = "error"
        groups = run.summarize([report, failed])
        self.assertEqual(groups[("x.pdf", "poppler", "random", "miss")], [2])
        self.assertEqual(groups[("x.pdf", "poppler", "random", "hit")], [.01])
        self.assertEqual(groups[("x.pdf", "poppler", "open", "-")], [3])


if __name__ == "__main__":
    unittest.main()

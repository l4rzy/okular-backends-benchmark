# SPDX-License-Identifier: GPL-3.0-or-later
import argparse
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import run


class TestRunner(unittest.TestCase):
    def test_package_environment_without_source_checkout(self):
        package = {"name": "okular-mupdf-ng", "version": "okular-mupdf-ng 1.2.3-1",
                   "plugin_sha256": "c" * 64}
        with patch.object(run, "command_output", return_value="") as command:
            environment = run.collect_environment({}, None, package)
        self.assertIsNone(environment["source_commit"])
        self.assertFalse(environment["source_dirty"])
        self.assertEqual(environment["mupdf_package"], package)
        self.assertEqual(environment["versions"]["mupdf"], package["version"])
        self.assertFalse(any("None" in call.args[0] for call in command.call_args_list))

    def test_packaged_runner_without_source_checkout(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin = root / "mupdfng.so"
            harness = root / "harness"
            plugin.touch()
            harness.touch()
            package = {"name": "okular-mupdf-ng", "version": "okular-mupdf-ng 1.2.3-1",
                       "plugin_sha256": run.file_hash(plugin)}
            paper = {"id": "one", "path": root / "one.pdf", "sha256": "pdf", "pages": 1}
            output = root / "samples.jsonl"
            commands = []

            def trial(command, timeout):
                commands.append(command)
                return {"status": "ok", "plugin_path": str(plugin), "pdf": str(paper["path"]),
                        "backend": command[command.index("--backend") + 1],
                        "open_ms": 1, "open_to_first_page_ms": 2, "samples": []}

            argv = ["run.py", "--mupdf-package", "okular-mupdf-ng", "--source-dir", str(root / "absent"),
                    "--pdfium-plugin", str(plugin),
                    "--harness", str(harness), "--manifest", str(root / "manifest.json"),
                    "--repeats", "2", "--output", str(output)]
            with (patch.object(sys, "argv", argv),
                  patch.object(run, "installed_mupdf_package", return_value=(plugin, package)),
                  patch.object(run, "load_corpus", return_value=([paper], {})),
                  patch.object(run, "collect_environment", return_value={"mupdf_package": package}) as environment,
                  patch.object(run, "run_trial", side_effect=trial),
                  patch.object(sys, "stdout", io.StringIO()), patch.object(sys, "stderr", io.StringIO())):
                self.assertEqual(run.main(), 0)
                environment.assert_called_once_with({}, None, package)
            self.assertEqual([command[command.index("--backend") + 1] for command in commands],
                             ["mupdfng", "poppler", "pdfium", "pdfium", "poppler", "mupdfng"])
            self.assertEqual(len(output.read_text().splitlines()), 6)
            self.assertEqual(json.loads(output.read_text().splitlines()[0])["environment"]["mupdf_package"], package)

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
            paper = {"arxiv_id": "paper", "path": "corpus/paper.pdf", "sha256": run.file_hash(pdf), "pages": 14}
            manifest = corpus / "manifest.json"
            def write(papers):
                manifest.write_text(json.dumps({"papers": papers, "corpus_version": 1}))
            write([paper])
            papers, metadata = run.load_corpus(manifest)
            self.assertEqual(papers[0]["path"], pdf)
            self.assertEqual(metadata["sha256"], run.file_hash(manifest))
            for entries in ([], [paper, paper], [{**paper, "sha256": "wrong"}], [{**paper, "pages": 0}],
                            [{**paper, "path": "../outside.pdf"}]):
                with self.subTest(entries=entries):
                    write(entries)
                    with self.assertRaises(ValueError):
                        run.load_corpus(manifest)

    def test_first_failure_stops_repeated_trials_and_passes_expected_pages(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "cmake").mkdir()
            (root / "cmake/mupdf.version").touch()
            harness = root / "harness"
            harness.touch()
            plugin = root / "plugin.so"
            plugin.touch()
            output = root / "results.jsonl"
            paper = {"id": "paper", "path": root / "paper.pdf", "sha256": "test", "pages": 14}
            argv = ["run.py", "--source-dir", str(root), "--harness", str(harness),
                    "--mupdf-plugin", str(plugin), "--manifest", str(root / "manifest.json"),
                    "--repeats", "30", "--output", str(output)]
            failure = {"status": "error", "error": "Page count mismatch", "exit_code": 1, "stderr": ""}
            with patch.object(sys, "argv", argv), patch.object(run, "load_corpus", return_value=([paper], {})), \
                 patch.object(run, "collect_environment", return_value={}), \
                 patch.object(run, "run_trial", return_value=failure) as trial, \
                 patch.object(sys, "stdout", io.StringIO()), patch.object(sys, "stderr", io.StringIO()):
                self.assertEqual(run.main(), 1)
            trial.assert_called_once()
            command = trial.call_args.args[0]
            self.assertEqual(command[command.index("--expected-pages") + 1], "14")
            self.assertEqual(len(output.read_text().splitlines()), 1)
            self.assertEqual(json.loads(output.read_text())["status"], "error")

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

    def test_three_backend_order_balances_positions(self):
        orders = [run.three_backend_order(trial) for trial in range(6)]
        for position in range(3):
            for backend in ("mupdfng", "poppler", "pdfium"):
                self.assertEqual(sum(order[position] == backend for order in orders), 2)
        self.assertEqual(run.three_backend_order(6), orders[0])

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

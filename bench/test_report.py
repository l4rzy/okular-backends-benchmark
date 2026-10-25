# SPDX-License-Identifier: GPL-3.0-or-later
import copy
import gzip
import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

import report


COMMIT = "a" * 40
REPOSITORY = "l4rzy/okular-mupdf-ng"
RUN_URL = "https://github.com/l4rzy/okular-backends-benchmark/actions/runs/123"


def fixture():
    manifest = {"papers": [{"arxiv_id": name, "sha256": name, "title": name, "pages": 2}
                           for name in ("one", "two")]}
    environment = {"source_commit": COMMIT, "source_dirty": False,
                   "benchmark_commit": "b" * 40, "benchmark_dirty": False,
                   "plugin_build": {"CMAKE_BUILD_TYPE": "Release", "ENABLE_MU_DEBUG": "OFF",
                                    "DISABLE_WORKER_SANDBOX": "OFF"},
                   "protocol": "test", "protocol_sha256": "test", "cpu_model": "test CPU",
                   "machine": "x86_64", "versions": {"compiler": "test", "okular": "test", "poppler": "test"}}
    rows = []
    for paper in manifest["papers"]:
        for trial in (1, 2):
            for backend in ("mupdfng", "poppler"):
                # Document ratios 2 and 8 give an equal-weight geometric score of 4.
                elapsed = (2 if paper["arxiv_id"] == "one" else 8) if backend == "poppler" else 1
                rows.append({"environment": copy.deepcopy(environment), "status": "ok", "exit_code": 0,
                             "configuration": {"repeats": 2, "pages": 2, "width": 1200, "seed": 1},
                             "corpus": {"sha256": "manifest"}, "document_id": paper["arxiv_id"],
                             "pdf_sha256": paper["sha256"], "page_count": 2, "backend": backend,
                             "trial": trial, "seed": trial, "plugin_sha256": backend, "plugin_version": "1",
                             "qt_version": "6", "sandbox_enforcement": "Relaxed", "open_ms": 1, "open_to_first_page_ms": 2,
                             "timestamp_utc": "2026-10-25T12:00:00+00:00",
                             "samples": [{"phase": phase, "page": page, "width": 1200, "height": 1600,
                                          "cached_before": False, "ok": True, "elapsed_ms": elapsed}
                                         for page, phase in enumerate(("first_page", "sequential"))]})
    return rows, manifest


def summarize(rows, manifest):
    return report.build_summary(rows, manifest, "manifest", COMMIT, REPOSITORY, "123-1", RUN_URL)


class TestReport(unittest.TestCase):
    def test_workflow_url_belongs_to_benchmark_repo(self):
        rows, manifest = fixture()
        with self.assertRaisesRegex(ValueError, "workflow run URL"):
            report.build_summary(rows, manifest, "manifest", COMMIT, REPOSITORY, "123-1",
                                 f"https://github.com/{REPOSITORY}/actions/runs/123")

    def test_equal_document_weight_and_paired_ratios(self):
        rows, manifest = fixture()
        summary = summarize(rows, manifest)
        self.assertAlmostEqual(summary["score"]["median"], 4)
        self.assertEqual(summary["score"]["n"], 2)
        self.assertEqual([doc["ratios"]["render_ms"]["median"] for doc in summary["documents"]], [2, 8])
        self.assertEqual(summary["score"]["ci95"], [4, 4])

    def test_rejects_invalid_runs(self):
        cases = {
            "failed": lambda r: r[0].update(status="error"),
            "missing": lambda r: r.pop(),
            "duplicate": lambda r: r.append(copy.deepcopy(r[0])),
            "pdf hash": lambda r: r[0].update(pdf_sha256="wrong"),
            "manifest hash": lambda r: r[0]["corpus"].update(sha256="wrong"),
            "dirty": lambda r: [v["environment"].update(source_dirty=True) for v in r],
            "dirty benchmark": lambda r: [v["environment"].update(benchmark_dirty=True) for v in r],
            "debug": lambda r: [v["environment"]["plugin_build"].update(ENABLE_MU_DEBUG="ON") for v in r],
            "sandbox": lambda r: [v["environment"]["plugin_build"].update(DISABLE_WORKER_SANDBOX="ON") for v in r],
            "cache hit": lambda r: r[0]["samples"][0].update(cached_before=True),
            "wrong page": lambda r: r[0]["samples"][0].update(page=1),
            "wrong page count": lambda r: r[0].update(page_count=1),
            "wrong enforcement": lambda r: r[0].update(sandbox_enforcement="Strict"),
            "mismatched seed": lambda r: r[0].update(seed=99),
            "nan": lambda r: r[0]["samples"][0].update(elapsed_ms=float("nan")),
        }
        for name, mutate in cases.items():
            with self.subTest(name=name):
                rows, manifest = fixture()
                mutate(rows)
                with self.assertRaises(ValueError):
                    summarize(rows, manifest)

    def test_uses_median_of_paired_ratios(self):
        rows, manifest = fixture()
        for row in rows:
            if row["document_id"] == "one":
                elapsed = 3 if row["trial"] == 2 else (4 if row["backend"] == "poppler" else 1)
                for sample in row["samples"]:
                    sample["elapsed_ms"] = elapsed
        summary = summarize(rows, manifest)
        # Median(4/1, 3/3) = 2.5, whereas ratio of the timing medians is 1.75.
        self.assertEqual(summary["documents"][0]["ratios"]["render_ms"]["median"], 2.5)

    def test_readme_preserves_license_and_replaces_history(self):
        rows, manifest = fixture()
        summary = summarize(rows, manifest)
        original = "# Corpus\n\nCC BY attribution retained.\n"
        first = report.update_readme(original, [summary])
        second = report.update_readme(first, [summary])
        self.assertEqual(first, second)
        self.assertTrue(second.startswith(original))
        self.assertIn(COMMIT[:12], second)
        self.assertIn("4.000×", second)
        with self.assertRaises(ValueError):
            report.update_readme(report.START, [summary])

    def test_publish_creates_readable_artifacts_and_svg(self):
        rows, manifest = fixture()
        summary = summarize(rows, manifest)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = root / "samples.jsonl"
            raw.write_text("\n".join(json.dumps(row) for row in rows))
            corpus = root / "manifest.json"
            corpus.write_text(json.dumps(manifest))
            target = root / "results"
            destination = report.publish(raw, corpus, target, summary)
            self.assertEqual(gzip.decompress((destination / "samples.jsonl.gz").read_bytes()), raw.read_bytes())
            self.assertEqual(json.loads((destination / "summary.json").read_text())["commit"], COMMIT)
            self.assertIn("Per-document results", (destination / "report.md").read_text())
            self.assertTrue(ET.parse(target / "trend.svg").getroot().tag.endswith("svg"))
            with self.assertRaises(FileExistsError):
                report.publish(raw, corpus, target, summary)


if __name__ == "__main__":
    unittest.main()

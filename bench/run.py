#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Run paired Okular backend trials, preserving successes and failures as JSONL."""

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import signal
import statistics
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent
PROTOCOL = "pdf-render-v1"


def positive_int(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def pdf_path(value):
    path = Path(value)
    if path.suffix.lower() != ".pdf":
        raise argparse.ArgumentTypeError(f"Expected a .pdf file: {value}")
    return path


def backend_order(trial):
    return ("poppler", "mupdfng") if trial % 2 else ("mupdfng", "poppler")


def percentile(values, fraction):
    """Nearest-rank percentile; report sample counts alongside results."""
    ordered = sorted(values)
    return ordered[max(0, math.ceil(len(ordered) * fraction) - 1)]


def run_trial(command, timeout):
    environment = os.environ.copy()
    environment.update(QT_QPA_PLATFORM="offscreen", QT_QPA_PLATFORMTHEME="generic")
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True, env=environment, start_new_session=True)
    except OSError as error:
        return {"status": "error", "error": f"Cannot start harness: {error}",
                "exit_code": None, "stderr": ""}
    with process:
        timed_out = False
        try:
            stdout, stderr = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            # Include workers, including when opening blocks before the Qt timer runs.
            os.killpg(process.pid, signal.SIGKILL)
            stdout, stderr = process.communicate()
        try:
            report = json.loads(stdout)
            if not isinstance(report, dict) or report.get("status") not in ("ok", "error"):
                raise ValueError("invalid report schema")
        except (ValueError, TypeError):
            report = {"status": "error", "error": "Harness returned no valid JSON report",
                      "stdout": stdout}
        if timed_out:
            report.update(status="error", error="Trial exceeded wall-clock timeout")
        elif process.returncode:
            report.update(status="error", error=report.get("error", "Harness exited unsuccessfully"))
        report.update(exit_code=process.returncode, stderr=stderr)
        return report


def summarize(reports):
    groups = defaultdict(list)
    for report in reports:
        # Keep failures in raw results, but exclude incomplete trials from timings.
        if report["status"] != "ok":
            continue
        prefix = (report["pdf"], report["backend"])
        groups[(*prefix, "open", "-")].append(report["open_ms"])
        groups[(*prefix, "open_to_first_page", "-")].append(report["open_to_first_page_ms"])
        for sample in report["samples"]:
            if sample["ok"]:
                cache = "hit" if sample["cached_before"] else "miss"
                groups[(*prefix, sample["phase"], cache)].append(sample["elapsed_ms"])
    return groups


def file_hash(path):
    with Path(path).open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def load_corpus(manifest_path):
    manifest_path = manifest_path.resolve()
    manifest = json.loads(manifest_path.read_text())
    root = manifest_path.parent.parent
    papers = []
    identifiers = set()
    for paper in manifest["papers"]:
        identifier = paper["arxiv_id"]
        path = (root / paper["path"]).resolve()
        if identifier in identifiers or not path.is_relative_to(root) or path.suffix.lower() != ".pdf":
            raise ValueError(f"Invalid or duplicate corpus entry: {identifier}")
        if file_hash(path) != paper["sha256"]:
            raise ValueError(f"Corpus checksum mismatch: {path}")
        if type(paper["pages"]) is not int or paper["pages"] < 1:
            raise ValueError(f"Invalid corpus page count: {identifier}")
        identifiers.add(identifier)
        papers.append({"id": identifier, "path": path, "sha256": paper["sha256"], "pages": paper["pages"]})
    if not papers:
        raise ValueError("Corpus manifest has no papers")
    return papers, {"version": manifest["corpus_version"], "sha256": file_hash(manifest_path)}


def command_output(command):
    try:
        environment = os.environ.copy()
        environment.update(QT_QPA_PLATFORM="offscreen", QT_QPA_PLATFORMTHEME="generic")
        return subprocess.check_output(command, stderr=subprocess.DEVNULL, text=True,
                                       timeout=15, env=environment).strip()
    except (OSError, subprocess.SubprocessError):
        return "unavailable"


def collect_environment(settings, source_dir):
    cpu_info = Path("/proc/cpuinfo")
    cpu_model = platform.processor()
    if cpu_info.exists():
        cpu_model = next((line.split(":", 1)[1].strip() for line in cpu_info.read_text().splitlines()
                          if line.startswith("model name")), cpu_model)
    protocol_hash = hashlib.sha256()
    for name in ("main.cpp", "workload.hpp", "run.py", "report.py"):
        protocol_hash.update(name.encode())
        protocol_hash.update((ROOT / "bench" / name).read_bytes())
    return {"platform": platform.platform(), "machine": platform.machine(),
            "cpu_model": cpu_model, "logical_cpus": os.cpu_count(),
            "available_cpus": len(os.sched_getaffinity(0)),
            "python": platform.python_version(), "plugin_build": settings,
            "protocol": PROTOCOL, "protocol_sha256": protocol_hash.hexdigest(),
            "source_commit": command_output(["git", "-C", str(source_dir), "rev-parse", "HEAD"]),
            "source_dirty": command_output(["git", "-C", str(source_dir), "status", "--porcelain"]) != "",
            "benchmark_commit": command_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"]),
            "benchmark_dirty": command_output(["git", "-C", str(ROOT), "status", "--porcelain"]) != "",
            "runner_image": os.environ.get("ImageOS", "local"),
            "runner_image_version": os.environ.get("ImageVersion", "local"),
            "container_image": os.environ.get("BENCH_CONTAINER_IMAGE", "local"),
            "versions": {"poppler": command_output(["pkg-config", "--modversion", "poppler-qt6"]),
                         "okular": command_output(["okular", "--version"]),
                         "compiler": command_output([settings.get("CMAKE_CXX_COMPILER", "c++"), "--version"]),
                         "mupdf": (source_dir / "cmake/mupdf.version").read_text().splitlines()[0]}}


def build_settings(plugin):
    for directory in Path(plugin).parents:
        cache = directory / "CMakeCache.txt"
        if cache.is_file():
            keys = {"CMAKE_BUILD_TYPE", "CMAKE_CXX_COMPILER", "ENABLE_LTO", "ENABLE_MU_DEBUG", "ENABLE_BUILD_TREE_WORKER",
                    "DISABLE_WORKER_SANDBOX", "USE_SYSTEM_MUPDF", "MUPDF_OPTIMIZED_BUILD", "MUPDF_CJK_FALLBACK"}
            return {line.split(":", 1)[0]: line.split("=", 1)[1]
                    for line in cache.read_text().splitlines()
                    if ":" in line and "=" in line and line.split(":", 1)[0] in keys}
    return {}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdfs", nargs="*", type=pdf_path, help="explicit PDF paths (instead of --manifest)")
    parser.add_argument("--manifest", type=Path, help="versioned corpus/manifest.json in the results checkout")
    parser.add_argument("--source-dir", type=Path, default=ROOT.parent / "okular-mupdf-ng",
                        help="plugin source checkout (default: sibling okular-mupdf-ng)")
    parser.add_argument("--harness", type=Path, default=ROOT / "bench/build/okular-bench")
    parser.add_argument("--mupdf-plugin", type=Path, help="default: SOURCE_DIR/build-release generator")
    parser.add_argument("--poppler-plugin", type=Path, help="default: discover installed Qt 6 generator")
    parser.add_argument("--repeats", type=positive_int, default=30)
    parser.add_argument("--pages", type=positive_int, default=20)
    parser.add_argument("--width", type=positive_int, default=1200)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--timeout", type=positive_int, default=120, help="whole trial timeout, seconds")
    parser.add_argument("--page-timeout-ms", type=positive_int, default=30000)
    parser.add_argument("--output", type=Path, help="new JSONL output file; existing files are never overwritten")
    args = parser.parse_args()
    args.source_dir = args.source_dir.resolve()
    if not (args.source_dir / "cmake/mupdf.version").is_file():
        parser.error("--source-dir must point to the okular-mupdf-ng source checkout")
    if args.mupdf_plugin is None:
        args.mupdf_plugin = args.source_dir / "build-release/bin/okular_generators/okularGenerator_mupdfng.so"
    if args.width > 16384 or not 0 <= args.seed <= 2**32 - 1:
        parser.error("width must be <=16384 and seed must be uint32")
    if bool(args.pdfs) == bool(args.manifest):
        parser.error("Provide --manifest or explicit PDF paths")
    try:
        if args.manifest:
            papers, corpus = load_corpus(args.manifest)
        else:
            papers = [{"id": path.name, "path": path.resolve(), "sha256": file_hash(path)} for path in args.pdfs]
            if len({paper["id"] for paper in papers}) != len(papers):
                raise ValueError("Explicit PDFs must have unique filenames")
            corpus = {"version": "adhoc", "sha256": hashlib.sha256(json.dumps(
                [(paper["id"], paper["sha256"]) for paper in papers]).encode()).hexdigest()}
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))
    for path in [args.harness, args.mupdf_plugin, *([args.poppler_plugin] if args.poppler_plugin else [])]:
        if not path.is_file():
            parser.error(f"File not found: {path}. Build the plugin separately; see bench/README.md.")
    settings = build_settings(args.mupdf_plugin)
    if settings.get("ENABLE_MU_DEBUG") == "ON" or settings.get("CMAKE_BUILD_TYPE") == "Debug":
        parser.error("Build the release plugin with -DENABLE_MU_DEBUG=OFF before benchmarking")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = args.output or ROOT / f"bench/results/{timestamp}-{os.getpid()}.jsonl"
    output.parent.mkdir(parents=True, exist_ok=True)
    environment = collect_environment(settings, args.source_dir)
    configuration = {"repeats": args.repeats, "pages": args.pages, "width": args.width, "seed": args.seed}
    reports = []
    try:
        destination = output.open("x")
    except FileExistsError:
        parser.error(f"Output already exists: {output}")
    with destination:
        for paper in papers:
            pdf = paper["path"]
            for trial in range(args.repeats):
                seed = (args.seed + trial) % 2**32
                for backend in backend_order(trial):
                    command = [str(args.harness.resolve()), "--backend", backend, "--pdf", str(pdf),
                               "--width", str(args.width), "--pages", str(args.pages),
                               "--seed", str(seed), "--timeout-ms", str(args.page_timeout_ms)]
                    plugin = args.mupdf_plugin if backend == "mupdfng" else args.poppler_plugin
                    if plugin:
                        command.extend(["--library", str(plugin.resolve())])
                    if "pages" in paper:
                        command.extend(["--expected-pages", str(paper["pages"])])
                    print(f"{pdf.name}: {backend}, trial {trial + 1}/{args.repeats}", file=sys.stderr)
                    report = run_trial(command, args.timeout)
                    report.update(schema_version=2, trial=trial + 1, pdf=str(pdf), pdf_sha256=paper["sha256"],
                                  document_id=paper["id"], corpus=corpus, configuration=configuration,
                                  backend=backend, environment=environment, command=command,
                                  timestamp_utc=datetime.now(timezone.utc).isoformat())
                    if report.get("plugin_path"):
                        report["plugin_sha256"] = file_hash(report["plugin_path"])
                    destination.write(json.dumps(report) + "\n")
                    destination.flush()
                    reports.append(report)
                    if report["status"] != "ok":
                        print(f"  ERROR: {report['error']} (stderr saved in JSONL)", file=sys.stderr)
                        print(f"Stopped after the first failure. Results: {output}", file=sys.stderr)
                        return 1
    print("\nPDF / backend / phase / cache: n, median ms, p95 ms (only when n >= 20)")
    for (pdf, backend, phase, cache), values in sorted(summarize(reports).items()):
        p95 = f"{percentile(values, 0.95):.3f}" if len(values) >= 20 else "-"
        print(f"{Path(pdf).name} / {backend} / {phase} / {cache}: "
              f"{len(values)}, {statistics.median(values):.3f}, {p95}")
    failures = sum(report["status"] != "ok" for report in reports)
    print(f"\nResults: {output}\nTrials: {len(reports)}, failed: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

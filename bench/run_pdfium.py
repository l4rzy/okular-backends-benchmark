#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Run an independent MuPDF-NG vs PDFium benchmark and update PDFIUM.md."""

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import platform
import random
import statistics
import subprocess
import sys

import run as common


ROOT = Path(__file__).resolve().parent.parent
START = "<!-- pdfium-history:start -->"
END = "<!-- pdfium-history:end -->"
LATEST_START = "<!-- pdfium-latest:start -->"
LATEST_END = "<!-- pdfium-latest:end -->"


def git_value(path, *args):
    return subprocess.check_output(["git", "-C", str(path), *args], text=True).strip()


def cpu_model():
    info = Path("/proc/cpuinfo")
    if info.exists():
        return next((line.split(":", 1)[1].strip() for line in info.read_text().splitlines()
                     if line.startswith("model name")), platform.processor())
    return platform.processor()


def render_time(report, pages):
    if any(not sample["ok"] or not math.isfinite(sample["elapsed_ms"])
           or sample["elapsed_ms"] <= 0 for sample in report["samples"]):
        raise ValueError(f'{report["document_id"]}: failed or invalid render sample')
    requests = [sample for sample in report["samples"]
                if sample["phase"] in ("first_page", "sequential")]
    expected = min(report["page_count"], pages)
    if [sample["page"] for sample in requests] != list(range(expected)):
        raise ValueError(f'{report["document_id"]}: incomplete primary render workload')
    if any(sample["cached_before"] for sample in requests):
        raise ValueError(f'{report["document_id"]}: primary render workload unexpectedly hit cache')
    return sum(sample["elapsed_ms"] for sample in requests)


def percentile(values, fraction):
    ordered = sorted(values)
    return ordered[max(0, math.ceil(len(ordered) * fraction) - 1)]


def bootstrap(values):
    generator = random.Random(1)
    medians = [statistics.median(generator.choices(values, k=len(values))) for _ in range(2000)]
    return [percentile(medians, .025), percentile(medians, .975)]


def plot_trend(summaries, output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.dates as dates
    import matplotlib.pyplot as plt
    from matplotlib.ticker import StrMethodFormatter

    series = defaultdict(list)
    for summary in summaries:
        # A new engine binary, corpus, machine, or workload starts a new line.
        key = (summary.get("cpu_model", "unknown CPU"), summary["pdfium_library_sha256"],
               summary["corpus_sha256"], json.dumps(summary["configuration"], sort_keys=True))
        series[key].append(summary)
    with plt.rc_context({"svg.hashsalt": "okular-pdfium-benchmark", "font.size": 9}):
        figure, axis = plt.subplots(figsize=(11, 5), layout="constrained")
        for (cpu, library, _, _), points in sorted(series.items()):
            points.sort(key=lambda point: (point["timestamp_utc"], point["run_id"]))
            x = [datetime.fromisoformat(point["timestamp_utc"]) for point in points]
            y = [point["score"]["median"] for point in points]
            errors = [[point["score"]["median"] - point["score"]["ci95"][0] for point in points],
                      [point["score"]["ci95"][1] - point["score"]["median"] for point in points]]
            axis.errorbar(x, y, yerr=errors, fmt="o-", markersize=4, capsize=3,
                          label=f"{cpu} / PDFium {library[:12]}")
        axis.axhline(1, color="gray", linestyle="--", linewidth=1)
        axis.set_yscale("log", base=2)
        axis.yaxis.set_major_formatter(StrMethodFormatter("{x:g}"))
        axis.set_ylabel("Median PDFium / MuPDF-NG rendering ratio")
        axis.set_xlabel("Measurement time (UTC); source commits are listed in PDFIUM.md")
        axis.set_title("Okular MuPDF-NG vs PDFium — above 1 favors MuPDF-NG")
        locator = dates.AutoDateLocator(minticks=3, maxticks=7)
        axis.xaxis.set_major_locator(locator)
        axis.xaxis.set_major_formatter(dates.ConciseDateFormatter(locator, tz=timezone.utc))
        axis.grid(True, alpha=.2)
        axis.legend(loc="upper left", bbox_to_anchor=(0, -.2), fontsize=7)
        figure.savefig(output, format="svg", metadata={"Date": None})
        plt.close(figure)


def update_markdown(path, summaries, latest):
    if path.exists():
        text = path.read_text()
    else:
        text = ("# MuPDF-NG vs PDFium benchmark history\n\n"
                "Ratio = PDFium rendering time / MuPDF-NG rendering time; values above 1 favor MuPDF-NG. "
                "Opening and worker startup are excluded. Each PDF has equal weight.\n\n")

    history_rows = [START, "![MuPDF-NG vs PDFium rendering history](pdfium-trend.svg)", "",
                    "Lines group runs by CPU, PDFium library, corpus, and workload. "
                    "Intervals describe within-run variability.", "",
                    "| Date | MuPDF-NG commit | PDFium commit | Median ratio (95% interval) | Repeats/PDF | Run |",
                    "|---|---|---|---:|---:|---|"]
    for summary in reversed(summaries[-50:]):
        ci = summary["score"]["ci95"]
        history_rows.append(
            f'| {summary["timestamp_utc"][:10]} '
            f'| [{summary["mupdf_commit"][:12]}](https://github.com/l4rzy/okular-mupdf-ng/commit/{summary["mupdf_commit"]}) '
            f'| [{summary["pdfium_commit"][:12]}](https://github.com/l4rzy/okular-backend-pdfium/commit/{summary["pdfium_commit"]}) '
            f'| {summary["score"]["median"]:.3f}× ({ci[0]:.3f}–{ci[1]:.3f}) '
            f'| {summary["configuration"]["repeats"]} | [details]({summary["run_url"]}) |')
    history_rows.append(END)

    latest_rows = [LATEST_START, "## Latest per-document results", "",
                   "Ratios are medians of paired trial ratios. Times are median milliseconds.", "",
                   "| PDF | Pages | PDFium / MuPDF-NG | MuPDF-NG render | PDFium render |",
                   "|---|---:|---:|---:|---:|"]
    for document in latest["documents"]:
        latest_rows.append(
            f'| {document["id"]} | {document["pages"]} | {document["ratio_median"]:.3f}× '
            f'| {document["mupdf_median_ms"]:.3f} | {document["pdfium_median_ms"]:.3f} |')
    latest_rows += ["", f'Latest run: [{latest["run_id"]}]({latest["run_url"]}); '
                    f'PDFium library SHA-256 `{latest["pdfium_library_sha256"]}`.', LATEST_END]

    def replace_block(source, start, end, block):
        if start not in source and end not in source:
            return source.rstrip() + "\n\n" + "\n".join(block) + "\n"
        if source.count(start) != 1 or source.count(end) != 1 or source.index(end) < source.index(start):
            raise ValueError(f"Invalid PDFIUM.md markers: {start}")
        before, remainder = source.split(start)
        _, after = remainder.split(end)
        return before + "\n".join(block) + after

    text = replace_block(text, START, END, history_rows)
    return replace_block(text, LATEST_START, LATEST_END, latest_rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=ROOT.parent / "okular-mupdf-ng")
    parser.add_argument("--pdfium-source-dir", type=Path, default=ROOT.parent / "okular-backend-pdfium")
    parser.add_argument("--mupdf-plugin", type=Path)
    parser.add_argument("--pdfium-plugin", type=Path)
    parser.add_argument("--harness", type=Path, default=ROOT / "bench/pdfium/build/okular-bench-pdfium")
    parser.add_argument("--manifest", type=Path, default=ROOT / "corpus/manifest.json")
    parser.add_argument("--results-dir", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--run-url", required=True)
    parser.add_argument("--repeats", type=int, default=30)
    parser.add_argument("--pages", type=int, default=20)
    parser.add_argument("--width", type=int, default=1200)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    args.source_dir = args.source_dir.resolve()
    args.pdfium_source_dir = args.pdfium_source_dir.resolve()
    mupdf_plugin = args.mupdf_plugin or (args.source_dir /
        "build-release/bin/okular_generators/okularGenerator_mupdfng.so")
    pdfium_plugin = args.pdfium_plugin or (args.pdfium_source_dir /
        "build/plugins/okular_generators/okularGenerator_pdfium.so")
    for path in (args.harness, mupdf_plugin, pdfium_plugin):
        if not path.is_file():
            parser.error(f"File not found: {path}")
    builds = {"mupdfng": common.build_settings(mupdf_plugin),
              "pdfium": common.build_settings(pdfium_plugin)}
    if (any(build.get("CMAKE_BUILD_TYPE") == "Debug" for build in builds.values())
            or builds["mupdfng"].get("ENABLE_MU_DEBUG") == "ON"):
        parser.error("Build release plugins with MuPDF-NG ENABLE_MU_DEBUG=OFF before benchmarking")
    if args.repeats < 2 or args.repeats % 2 or args.pages < 1 or not 1 <= args.width <= 16384 or args.timeout < 1:
        parser.error("repeats must be positive and even; pages and timeout positive; width must be 1..16384")
    if not 0 <= args.seed <= 2**32 - 1:
        parser.error("seed must be uint32")
    if not (args.source_dir / "cmake/mupdf.version").is_file():
        parser.error("--source-dir must be the okular-mupdf-ng checkout")
    pdfium_library = args.pdfium_source_dir / "pdfium/lib/libpdfium.so"
    if not pdfium_library.is_file():
        parser.error(f"PDFium library not found: {pdfium_library}")
    try:
        papers, corpus = common.load_corpus(args.manifest)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))

    source_commit = git_value(args.source_dir, "rev-parse", "HEAD")
    pdfium_commit = git_value(args.pdfium_source_dir, "rev-parse", "HEAD")
    rows = []
    ratios_by_document = {paper["id"]: [] for paper in papers}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    try:
        raw = args.output.open("x")
    except FileExistsError:
        parser.error(f"Output already exists: {args.output}")

    with raw:
        for paper in papers:
            for trial in range(args.repeats):
                seed = (args.seed + trial) % 2**32
                pair = {}
                order = ("mupdfng", "pdfium") if trial % 2 == 0 else ("pdfium", "mupdfng")
                for backend in order:
                    plugin = mupdf_plugin if backend == "mupdfng" else pdfium_plugin
                    command = [str(args.harness.resolve()), "--backend", backend, "--library", str(plugin.resolve()),
                               "--pdf", str(paper["path"]), "--width", str(args.width),
                               "--pages", str(args.pages), "--seed", str(seed),
                               "--timeout-ms", "30000", "--expected-pages", str(paper["pages"])]
                    print(f'{paper["id"]}: {backend}, repeat {trial + 1}/{args.repeats}', file=sys.stderr)
                    result = common.run_trial(command, args.timeout)
                    if result["status"] != "ok":
                        result.update(schema_version=1, backend=backend, trial=trial + 1,
                                      document_id=paper["id"], command=command)
                        raw.write(json.dumps(result) + "\n")
                        raw.flush()
                        parser.error(f'{paper["id"]}: {backend} failed: {result.get("error", "unknown error")}')
                    result.update(schema_version=1, backend=backend, trial=trial + 1,
                                  document_id=paper["id"], pdf_sha256=paper["sha256"], corpus=corpus,
                                  seed=seed, plugin_sha256=common.file_hash(plugin), command=command,
                                  timestamp_utc=datetime.now(timezone.utc).isoformat())
                    pair[backend] = result
                    rows.append(result)
                    raw.write(json.dumps(result) + "\n")
                    raw.flush()
                a, b = pair["mupdfng"], pair["pdfium"]
                if a["page_count"] != paper["pages"] or b["page_count"] != paper["pages"]:
                    raise ValueError(f'{paper["id"]}: page count differs from corpus')
                locations = lambda report: [(sample["phase"], sample["page"], sample["width"], sample["height"])
                                             for sample in report["samples"]]
                if a["seed"] != b["seed"] or locations(a) != locations(b):
                    raise ValueError("Paired requests did not match")
                ratio = render_time(b, args.pages) / render_time(a, args.pages)
                ratios_by_document[paper["id"]].append(ratio)

    trial_scores = []
    for index in range(args.repeats):
        trial_scores.append(statistics.geometric_mean(
            [ratios_by_document[paper["id"]][index] for paper in papers]))
    score = {"n": len(trial_scores), "median": statistics.median(trial_scores),
             "ci95": bootstrap(trial_scores)}
    documents = []
    for paper in papers:
        pdfium_times = [render_time(row, args.pages) for row in rows
                        if row["document_id"] == paper["id"] and row["backend"] == "pdfium"]
        mupdf_times = [render_time(row, args.pages) for row in rows
                       if row["document_id"] == paper["id"] and row["backend"] == "mupdfng"]
        documents.append({"id": paper["id"], "pages": paper["pages"],
                          "ratio_median": statistics.median(ratios_by_document[paper["id"]]),
                          "mupdf_median_ms": statistics.median(mupdf_times),
                          "pdfium_median_ms": statistics.median(pdfium_times)})

    summary = {"schema_version": 1, "run_id": args.run_id, "run_url": args.run_url,
               "timestamp_utc": datetime.now(timezone.utc).isoformat(),
               "mupdf_commit": source_commit, "pdfium_commit": pdfium_commit,
               "plugins": {backend: {"sha256": next(row["plugin_sha256"] for row in rows
                                                       if row["backend"] == backend)}
                           for backend in ("mupdfng", "pdfium")},
               "plugin_builds": builds,
               "pdfium_library_sha256": common.file_hash(pdfium_library),
               "cpu_model": cpu_model(),
               "machine": platform.machine(),
               "corpus_sha256": corpus["sha256"],
               "configuration": {"repeats": args.repeats, "pages": args.pages, "width": args.width,
                                 "seed": args.seed},
               "score": score, "documents": documents, "samples_file": str(args.output)}
    summary_path = args.results_dir / "reports-pdfium" / f'{args.run_id}.json'
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2) + "\n")
    summaries = [json.loads(path.read_text()) for path in summary_path.parent.glob("*.json")]
    summaries.sort(key=lambda item: (item["timestamp_utc"], item["run_id"]))
    pdfium_md = args.results_dir / "PDFIUM.md"
    plot_trend(summaries, args.results_dir / "pdfium-trend.svg")
    pdfium_md.write_text(update_markdown(pdfium_md, summaries, summary))
    print(f'PDFium comparison complete: median ratio {score["median"]:.3f}×; report {summary_path}')
    return 0


if __name__ == "__main__":
    sys.exit(main())

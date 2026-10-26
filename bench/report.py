#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Validate paired trials and publish reports, README history, and a trend SVG."""

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import gzip
import hashlib
import json
import math
from pathlib import Path
import random
import re
import statistics

from run import file_hash, percentile


START = "<!-- benchmark-history:start -->"
END = "<!-- benchmark-history:end -->"


def measure(values):
    if not values or any(not math.isfinite(value) or value <= 0 for value in values):
        raise ValueError("Measurements must be finite and positive")
    return {"n": len(values), "median": statistics.median(values),
            "min": min(values), "max": max(values),
            "p95": percentile(values, .95) if len(values) >= 20 else None}


def ratio_summary(values):
    result = measure(values)
    randomizer = random.Random(1)
    medians = [statistics.median(randomizer.choices(values, k=len(values))) for _ in range(2000)]
    result["ci95"] = [percentile(medians, .025), percentile(medians, .975)]
    return result


def render_time(row):
    samples = [sample for sample in row["samples"] if sample["phase"] in ("first_page", "sequential")]
    expected = min(row["page_count"], row["configuration"]["pages"])
    if [sample["page"] for sample in samples] != list(range(expected)):
        raise ValueError("Sequential workload is incomplete")
    if any(sample["cached_before"] for sample in samples):
        raise ValueError("Primary render workload unexpectedly hit a pixmap cache")
    return sum(sample["elapsed_ms"] for sample in samples)


def build_summary(rows, manifest, manifest_sha, commit, repository, run_id, run_url, allow_dirty=False,
                  workflow_repository="l4rzy/okular-backends-benchmark"):
    if not re.fullmatch(r"[0-9a-f]{40}", commit) or not re.fullmatch(r"[\w.-]+/[\w.-]+", repository):
        raise ValueError("Invalid source commit or repository")
    if not re.fullmatch(r"[\w.-]+", run_id) or run_id in (".", ".."):
        raise ValueError("Invalid run ID")
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", workflow_repository):
        raise ValueError("Invalid workflow repository")
    if not run_url.startswith(f"https://github.com/{workflow_repository}/actions/runs/"):
        raise ValueError("Invalid workflow run URL")
    if not rows:
        raise ValueError("No trial records")
    environment = rows[0]["environment"]
    configuration = rows[0]["configuration"]
    build = environment["plugin_build"]
    if build.get("CMAKE_BUILD_TYPE") != "Release" or build.get("ENABLE_MU_DEBUG") != "OFF":
        raise ValueError("Publishing requires Release with diagnostics disabled")
    if build.get("DISABLE_WORKER_SANDBOX") != "OFF":
        raise ValueError("Publishing requires the worker sandbox")
    if environment["source_commit"] != commit or (environment["source_dirty"] and not allow_dirty):
        raise ValueError("Source commit mismatch or uncommitted source changes")
    if environment["benchmark_dirty"] and not allow_dirty:
        raise ValueError("Uncommitted benchmark changes")
    papers = {paper["arxiv_id"]: paper for paper in manifest["papers"]}
    if not papers or len(papers) != len(manifest["papers"]):
        raise ValueError("Empty or duplicate corpus entries")
    pairs = defaultdict(dict)
    plugins = {}
    qt_versions = set()
    for row in rows:
        if row["status"] != "ok" or row.get("exit_code") != 0:
            raise ValueError("Failed trials cannot contribute a performance score")
        if row["environment"] != environment or row["configuration"] != configuration:
            raise ValueError("Environment or configuration changed within the run")
        if row["corpus"]["sha256"] != manifest_sha:
            raise ValueError("Corpus manifest checksum mismatch")
        identifier = row["document_id"]
        if identifier not in papers or row["pdf_sha256"] != papers[identifier]["sha256"]:
            raise ValueError("PDF is not in the verified corpus")
        if row["page_count"] != papers[identifier]["pages"]:
            raise ValueError(f'{identifier}: {row["backend"]} trial {row["trial"]} reported '
                             f'{row["page_count"]} pages; corpus expects {papers[identifier]["pages"]}')
        if row.get("sandbox_enforcement") != "Relaxed":
            raise ValueError("Unexpected benchmark sandbox enforcement profile")
        backend = row["backend"]
        if backend not in ("mupdfng", "poppler") or not 1 <= row["trial"] <= configuration["repeats"]:
            raise ValueError("Invalid backend or trial number")
        if backend in pairs[(identifier, row["trial"])]:
            raise ValueError("Duplicate trial record")
        pairs[(identifier, row["trial"])][backend] = row
        plugin = {"sha256": row["plugin_sha256"], "version": row["plugin_version"]}
        if backend in plugins and plugins[backend] != plugin:
            raise ValueError("Generator changed during the run")
        plugins[backend] = plugin
        qt_versions.add(row["qt_version"])
        for sample in row["samples"]:
            if not sample["ok"] or not math.isfinite(sample["elapsed_ms"]) or sample["elapsed_ms"] <= 0:
                raise ValueError("Failed or invalid render sample")
    repeats = configuration["repeats"]
    if repeats < 1 or configuration["pages"] < 1 or not 1 <= configuration["width"] <= 16384:
        raise ValueError("Invalid workload configuration")
    if len(rows) != len(papers) * repeats * 2 or len(qt_versions) != 1:
        raise ValueError("Incomplete run or inconsistent Qt version")
    documents = []
    corpus_ratios = defaultdict(list)
    for identifier, paper in papers.items():
        ratios = defaultdict(list)
        totals = defaultdict(list)
        request_times = defaultdict(list)
        for trial in range(1, repeats + 1):
            pair = pairs[(identifier, trial)]
            if set(pair) != {"mupdfng", "poppler"}:
                raise ValueError("Missing backend in trial pair")
            a, b = pair["mupdfng"], pair["poppler"]
            locations = lambda row: [(s["phase"], s["page"], s["width"], s["height"]) for s in row["samples"]]
            if locations(a) != locations(b) or a["seed"] != b["seed"]:
                raise ValueError("Paired requests do not match")
            for backend, row in pair.items():
                totals[(backend, "render_ms")].append(render_time(row))
                totals[(backend, "open_ms")].append(row["open_ms"])
                totals[(backend, "open_to_first_page_ms")].append(row["open_to_first_page_ms"])
                for sample in row["samples"]:
                    cache = "hit" if sample["cached_before"] else "miss"
                    request_times[(backend, sample["phase"], cache)].append(sample["elapsed_ms"])
            for metric in ("render_ms", "open_ms", "open_to_first_page_ms"):
                ratios[metric].append(totals[("poppler", metric)][-1] / totals[("mupdfng", metric)][-1])
            corpus_ratios[trial].append(ratios["render_ms"][-1])
        documents.append({"id": identifier, "title": paper["title"], "pages": paper["pages"],
                          "ratios": {metric: ratio_summary(values) for metric, values in ratios.items()},
                          "timings": {backend: {metric: measure(totals[(backend, metric)])
                                                for metric in ("render_ms", "open_ms", "open_to_first_page_ms")}
                                      for backend in ("mupdfng", "poppler")},
                          "requests": [{"backend": key[0], "phase": key[1], "cache": key[2], **measure(values)}
                                       for key, values in sorted(request_times.items())]})
    series = {"protocol": environment["protocol"], "protocol_sha256": environment["protocol_sha256"],
              "corpus_sha256": manifest_sha, "cpu_model": environment["cpu_model"],
              "machine": environment["machine"], "configuration": configuration,
              "available_cpus": environment.get("available_cpus"),
              "container_image": environment.get("container_image"),
              "plugin_build": {key: value for key, value in build.items() if key != "CMAKE_CXX_COMPILER"},
              "sandbox_enforcement": "Relaxed",
              "poppler_sha256": plugins["poppler"]["sha256"], "qt_version": next(iter(qt_versions)),
              "compiler": environment["versions"]["compiler"], "okular": environment["versions"]["okular"],
              "poppler": environment["versions"]["poppler"]}
    series_id = hashlib.sha256(json.dumps(series, sort_keys=True).encode()).hexdigest()[:16]
    # Equal document weight per trial, then the median across complete paired trials.
    score = ratio_summary([statistics.geometric_mean(values) for _, values in sorted(corpus_ratios.items())])
    return {"schema_version": 1, "commit": commit, "repository": repository, "run_id": run_id,
            "run_url": run_url, "workflow_repository": workflow_repository,
            "timestamp_utc": max(row["timestamp_utc"] for row in rows),
            "series_id": series_id, "series": series, "environment": environment,
            "plugins": plugins, "configuration": configuration, "score": score,
            "documents": documents, "trials": len(rows),
            "warnings": [{"document": row["document_id"], "backend": row["backend"], "trial": row["trial"],
                          "messages": row["warnings"]} for row in rows if row.get("warnings")]}


def markdown_report(summary):
    score = summary["score"]
    lines = ["# PDF backend benchmark", "",
             f'Source commit: [{summary["commit"]}](https://github.com/{summary["repository"]}/commit/{summary["commit"]}).', "",
             f'Benchmark commit: `{summary["environment"]["benchmark_commit"]}`.', "",
             f'Run: [{summary["run_id"]}]({summary["run_url"]}), {summary["timestamp_utc"]}.', "",
             f'**Median paired rendering ratio: {score["median"]:.3f}×** '
             f'(95% bootstrap interval {score["ci95"][0]:.3f}–{score["ci95"][1]:.3f}×).', "",
             "Ratio = Poppler time / MuPDF-NG time; above 1 favors MuPDF-NG. "
             "Each trial uses the geometric mean of document ratios, giving each PDF equal weight. "
             "The headline is the median of those trial scores. "
             "The primary workload sums first-page and sequential-render request times, excluding document opening and worker startup. "
             "The worker stays alive for all requests in a trial.", "",
             "MuPDF-NG uses **Relaxed sandbox enforcement**: available worker protections remain active, "
             "and incomplete host hardening does not block document opening.", "",
             f'{summary["trials"]} successful backend trials; {summary["configuration"]["repeats"]} pairs per PDF; '
             f'series `{summary["series_id"]}`.', "", "## Per-document results", "",
             "Times are medians in milliseconds. Ratios are medians of paired ratios, not ratios of medians.", "",
             "| PDF | Pages | Render ratio | MuPDF-NG render batch | Poppler render batch | MuPDF-NG open → first page | Poppler open → first page |",
             "|---|---:|---:|---:|---:|---:|---:|"]
    for document in summary["documents"]:
        a, b = document["timings"]["mupdfng"], document["timings"]["poppler"]
        lines.append(f'| {document["id"]} | {document["pages"]} | {document["ratios"]["render_ms"]["median"]:.3f}× | '
                     f'{a["render_ms"]["median"]:.3f} | {b["render_ms"]["median"]:.3f} | '
                     f'{a["open_to_first_page_ms"]["median"]:.3f} | {b["open_to_first_page_ms"]["median"]:.3f} |')
    lines += ["", "## Individual requests", "", "Times are milliseconds; p95 is shown only for at least 20 samples. Cache hits are separate.", "",
              "| PDF | Backend | Phase | Cache | N | Median | p95 | Maximum |", "|---|---|---|---|---:|---:|---:|---:|"]
    for document in summary["documents"]:
        for request in document["requests"]:
            p95 = f'{request["p95"]:.6f}' if request["p95"] is not None else "—"
            lines.append(f'| {document["id"]} | {request["backend"]} | {request["phase"]} | {request["cache"]} | '
                         f'{request["n"]} | {request["median"]:.6f} | {p95} | {request["max"]:.6f} |')
    lines += ["", "## Environment", "", "```json", json.dumps(summary["environment"], indent=2), "```", "",
              "## Interpretation limits", "",
              "Paired trials reduce host-speed noise, but CPU architectures can favor the backends differently. "
              "Graph lines group runs by CPU model and Poppler version; other environment and benchmark settings remain recorded in the reports. "
              "Bootstrap intervals resample whole paired trial scores; repeated pages are not independent samples of all PDFs. "
              "This is an offscreen rendering benchmark, not a GUI scrolling, memory, or visual-fidelity measurement. "
              "OS file caches are warm/uncontrolled. No performance merge gate is applied.", "",
              f'Okular warning-bearing trials: {len(summary["warnings"])}. See `summary.json` and `samples.jsonl.gz` for details.', "",
              "Artifacts: [summary](summary.json), [raw trials](samples.jsonl.gz), [corpus manifest](corpus-manifest.json).", ""]
    return "\n".join(lines)


def update_readme(text, summaries):
    lines = [START, "## Backend performance history", "",
             "![Paired rendering ratio over time](trend.svg)", "",
             "Median ratio = Poppler / MuPDF-NG rendering time; **above 1 favors MuPDF-NG**. "
             "Opening and worker startup are excluded. Each PDF has equal weight. "
             "Lines group runs by CPU model and Poppler version. "
             "Intervals describe within-run variability, not hardware-independent uncertainty.", "",
             "| Date | Source commit | Median ratio (95% interval) | Pairs/PDF | Report |",
             "|---|---|---:|---:|---|"]
    for summary in reversed(summaries[-50:]):
        score = summary["score"]
        commit = summary["commit"]
        lines.append(f'| {summary["timestamp_utc"][:10]} | [{commit[:12]}](https://github.com/{summary["repository"]}/commit/{commit}) | '
                     f'{score["median"]:.3f}× ({score["ci95"][0]:.3f}–{score["ci95"][1]:.3f}) | '
                     f'{summary["configuration"]["repeats"]} | '
                     f'[details](reports/{commit}/{summary["run_id"]}/report.md) |')
    lines += ["", "The latest 50 runs are listed here; all detailed reports remain under `reports/`.", END]
    block = "\n".join(lines)
    if START in text or END in text:
        if text.count(START) != 1 or text.count(END) != 1 or text.index(END) < text.index(START):
            raise ValueError("Invalid managed README markers")
        before, rest = text.split(START)
        _, after = rest.split(END)
        return before + block + after
    return text.rstrip() + "\n\n" + block + "\n"


def plot_trend(summaries, output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.dates as dates
    import matplotlib.pyplot as plt
    from matplotlib.ticker import StrMethodFormatter

    series = defaultdict(list)
    for summary in summaries:
        key = (summary["environment"]["cpu_model"], summary["series"]["poppler"])
        series[key].append(summary)
    with plt.rc_context({"svg.hashsalt": "okular-backends-benchmark", "font.size": 9}):
        figure, axis = plt.subplots(figsize=(11, 5), layout="constrained")
        for (cpu_model, poppler_version), points in sorted(series.items()):
            points.sort(key=lambda point: (point["timestamp_utc"], point["run_id"]))
            x = [datetime.fromisoformat(point["timestamp_utc"]) for point in points]
            y = [point["score"]["median"] for point in points]
            errors = [[point["score"]["median"] - point["score"]["ci95"][0] for point in points],
                      [point["score"]["ci95"][1] - point["score"]["median"] for point in points]]
            label = f"{cpu_model} / Poppler {poppler_version}"
            axis.errorbar(x, y, yerr=errors, fmt="o-", markersize=4, capsize=3, label=label)
        axis.axhline(1, color="gray", linestyle="--", linewidth=1)
        axis.set_yscale("log", base=2)
        axis.yaxis.set_major_formatter(StrMethodFormatter("{x:g}"))
        axis.set_ylabel("Median Poppler / MuPDF-NG rendering ratio")
        axis.set_xlabel("Measurement time (UTC); source commits are listed in README")
        axis.set_title("Okular PDF backend rendering — above 1 favors MuPDF-NG")
        locator = dates.AutoDateLocator(minticks=3, maxticks=7)
        axis.xaxis.set_major_locator(locator)
        axis.xaxis.set_major_formatter(dates.ConciseDateFormatter(locator, tz=timezone.utc))
        axis.grid(True, alpha=.2)
        axis.legend(loc="upper left", bbox_to_anchor=(0, -.2), fontsize=7)
        figure.savefig(output, format="svg", metadata={"Date": None, "Description": "Paired ratios grouped by CPU model and Poppler version; see README for source commits."})
        plt.close(figure)


def publish(raw, manifest_path, results_dir, summary):
    destination = results_dir / "reports" / summary["commit"] / summary["run_id"]
    destination.mkdir(parents=True, exist_ok=False)
    (destination / "samples.jsonl.gz").write_bytes(gzip.compress(raw.read_bytes(), mtime=0))
    (destination / "corpus-manifest.json").write_bytes(manifest_path.read_bytes())
    (destination / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (destination / "report.md").write_text(markdown_report(summary))
    summaries = [json.loads(path.read_text()) for path in results_dir.glob("reports/*/*/summary.json")]
    summaries.sort(key=lambda item: (item["timestamp_utc"], item["run_id"]))
    readme = results_dir / "README.md"
    previous = readme.read_text() if readme.exists() else "# Okular Backends Benchmark\n"
    readme.write_text(update_readme(previous, summaries))
    plot_trend(summaries, results_dir / "trend.svg")
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--results-dir", type=Path, required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--repository", default="l4rzy/okular-mupdf-ng")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--run-url", required=True)
    parser.add_argument("--workflow-repository", default="l4rzy/okular-backends-benchmark")
    parser.add_argument("--allow-dirty", action="store_true", help="local preview only; never used by CI")
    args = parser.parse_args()
    try:
        rows = [json.loads(line) for line in args.input.read_text().splitlines() if line.strip()]
        manifest = json.loads(args.manifest.read_text())
        summary = build_summary(rows, manifest, file_hash(args.manifest), args.commit,
                                args.repository, args.run_id, args.run_url, args.allow_dirty, args.workflow_repository)
        destination = publish(args.input, args.manifest, args.results_dir, summary)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))
    print(f'Published files in {destination}; median ratio {summary["score"]["median"]:.3f}x')


if __name__ == "__main__":
    main()

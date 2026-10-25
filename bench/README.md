# Okular PDF backend benchmark

Standalone CMake project comparing the installed official Poppler generator
with a separately built MuPDF-NG plugin. This repository owns the harness,
corpus, scheduled CI, reports, and trend graph. Plugin source lives in
[l4rzy/okular-mupdf-ng](https://github.com/l4rzy/okular-mupdf-ng).

Linux dependencies: CMake, a C++20 compiler, ECM, Qt 6 Widgets and Test,
KF6 CoreAddons and Config, Okular development files and its Poppler generator,
Python 3.11+, and uv. Python dependencies, including Matplotlib, are pinned in
`uv.lock`; uv installs them in `bench/.venv/`. Building the plugin with its
source download helper requires Python 3.12+.

## Local use

Clone and build the plugin separately, then run from this repository's root:

```sh
git clone https://github.com/l4rzy/okular-mupdf-ng.git ../okular-mupdf-ng
(cd ../okular-mupdf-ng && ./scripts/build.sh release -DENABLE_MU_DEBUG=OFF)
make bench
```

`make bench` installs locked Python dependencies, builds the small harness,
runs its tests, and measures 30 pairs per PDF at 1200 pixels wide. PDFs are
read directly from `corpus/` and checked against the manifest SHA-256s.
Change the plugin checkout location or benchmark settings with:

```sh
make bench PLUGIN_DIR=/path/okular-mupdf-ng
make bench BENCH_ARGS='--manifest corpus/manifest.json --repeats 2 --pages 5'
make bench BENCH_ARGS='--repeats 2 /path/external/*.pdf'
uv run --project bench --locked python bench/run.py --help
```

The plugin defaults to `PLUGIN_DIR/build-release/bin/okular_generators`.
Override libraries with `--mupdf-plugin` and `--poppler-plugin` if needed;
otherwise Poppler is discovered in installed Qt 6 plugin directories. The
corresponding worker must be discoverable (`ENABLE_BUILD_TREE_WORKER=ON` for
an uninstalled build). The worker sandbox remains enabled. The harness explicitly
selects **Relaxed sandbox enforcement**, matching the generator tests: available
protections remain active, and incomplete hardening on a container runner does
not replace the PDF with a Strict-mode error page. The profile is recorded in
raw data and reports and identifies a separate trend series.

Explicit PDFs are for local experiments; publishing requires a complete
manifest-backed corpus. Use an even number of pairs to balance backend order.
A two-pair run is a smoke check. Build products, local results, Python caches,
and virtual environments are ignored by Git. An optional plugin checkout at
`plugin/` is also ignored.

## Measurement and score

Each backend trial opens a PDF once and keeps its document and worker alive
for all page requests. The worker starts once per trial. Backend order
alternates within adjacent pairs; each pair uses the same seed and request
sequence. Fresh processes isolate backend document caches, with temporary XDG
settings. OS file caches remain warm/uncontrolled.

The harness records:

- `open_ms`: opening, including backend initialization and worker startup.
- `open_to_first_page_ms`: opening through the first complete pixmap.
- Per-request `elapsed_ms`: submission through complete pixmap delivery,
  including IPC. Phases cover the first page, sequential pages, seeded random
  jumps over the whole PDF, and revisiting those jumps in reverse order.
- Cache status, dimensions, successful completion, warnings, plugin hashes and
  versions, build settings, CPU, dependencies, protocol and corpus hashes, and
  both the plugin and benchmark source commits.

Requests are serial, full-page, DPR 1, fixed width with preserved aspect ratio.
Callbacks detect delivery without polling. OCR, heuristic outlines, and cache
vacuum activity are disabled. Normal memory policies and backend default
antialiasing apply. This does not establish equivalent image quality.

The primary render time sums first-page and sequential request times for the
first 20 pages (or all pages in shorter PDFs); these must be cache misses.
**Opening and worker startup are excluded.** Each paired ratio is
`Poppler time / MuPDF-NG time`: above 1 favors MuPDF-NG. The geometric mean
across PDFs gives each PDF equal weight. The headline is the **median** of
these corpus trial scores, with a deterministic 95% bootstrap interval over
whole trial scores. Per-document paired ratios and opening-to-first-page times
appear in the detailed tables. Random/revisit requests are descriptive, with
hits and misses separate; p95 needs 20 samples.

Thirty pairs reduce runner noise; ratios do not remove CPU-specific effects
or host contention. Lines connect only matching CPU, baseline binary,
compiler/dependency versions, corpus, protocol, and settings. Changes start a
new series. Bootstrap intervals describe within-run variation on this corpus.
There is no performance merge gate. This measures offscreen backend delivery,
not GUI scrolling, memory, or visual fidelity.

Raw JSONL goes to `bench/results/`; `--output` selects a new file. The harness
checks manifest page counts immediately after opening, before rendering any
pages. The first failed trial is retained and stops the run, with the document,
backend, and expected/actual counts in mismatch errors. Page and whole-trial timeouts include
terminating workers. Publication requires complete successful trials from
clean plugin and benchmark checkouts, Release with diagnostics off, and the
worker sandbox enabled.

## Weekly and manual CI

`.github/workflows/benchmark.yml` runs every Monday at 05:23 UTC and via
**Actions → PDF backend benchmark → Run workflow** on `main`. There is no push
trigger. Weekly runs build the plugin's latest `main`; manual runs accept a
plugin branch, tag, or full commit hash and an even 20–100 pairs per PDF
(default 30). The resolved full plugin SHA is always recorded.

An Ubuntu 24.04 runner hosts an Ubuntu 26.04 container. CI builds Release with
diagnostics off and LTO on, runs all plugin and benchmark tests, then measures
without concurrent builds or tests. CPU and dependency metadata identify
comparable series. Python and Matplotlib use uv; graphing happens after timing.
The corpus is read from this checkout without copying its PDFs.

Publishing uses this repository's built-in `GITHUB_TOKEN` with `contents: write`.
No personal token or cross-repository secret is needed. Checkout credentials
are not persisted; the publishing token is passed to Git only during the final
push. Allow GitHub Actions to write repository contents if repository or
organization policy restricts it. Branch protection can also prevent a direct
push. Runs are serialized, and normal pushes preserve concurrent remote work.

Reports are written to a separate temporary checkout of this repository so
publishing does not alter the harness checkout used for measurements:

```text
README.md                         latest 50 plugin commits and median ratios
trend.svg                         measurements grouped by comparable series
reports/<plugin-sha>/<run-attempt>/
  report.md                       per-PDF and per-request tables, environment
  summary.json                    aggregate and provenance
  samples.jsonl.gz                complete trial records
  corpus-manifest.json            exact measured corpus snapshot
```

Corpus licensing and attributions are recorded in [CREDITS.md](../CREDITS.md). Failed benchmarks
retain workflow artifacts without publishing a normal score. Reports remain
available as artifacts if pushing fails. Repeated runs have distinct paths.
The trend SVG appears after the first successful published measurement; no
synthetic history is seeded.

Embed it in another repository later with:

```md
![PDF backend performance](https://raw.githubusercontent.com/l4rzy/okular-backends-benchmark/main/trend.svg)
```

To compile a raw run manually (writes files without Git commits):

```sh
uv run --project bench --locked python bench/report.py \
  --input /path/samples.jsonl --manifest /path/corpus-manifest.json \
  --results-dir /path/report-checkout --commit <full-plugin-sha> \
  --run-id <run-id>-<attempt> \
  --run-url https://github.com/l4rzy/okular-backends-benchmark/actions/runs/<run-id>
```

`--allow-dirty` permits local previews from uncommitted work; CI never uses it.
Preview into a temporary directory rather than the published results checkout.

## Tests

```sh
uv sync --project bench --locked
uv run --project bench --locked python -m unittest discover -s bench -p 'test_*.py'
ctest --test-dir bench/build --output-on-failure
```

Tests cover request sequencing, alternating backend order, subprocess failures
and timeouts, corpus verification, paired scoring and rejected runs, README
preservation, compressed artifacts, and SVG generation.

# Okular Backends Benchmark

Benchmarks comparing the **[MuPDF-NG backend](https://github.com/l4rzy/okular-mupdf-ng)** with **[Okular’s official Poppler
backend](https://github.com/KDE/okular/tree/master/generators/poppler)**, using a versioned PDF corpus and tracking performance over time.

<!-- benchmark-history:start -->
## Backend performance history

![Paired rendering ratio over time](trend.svg)

Median ratio = Poppler / MuPDF-NG rendering time; **above 1 favors MuPDF-NG**. Opening and worker startup are excluded. Each PDF has equal weight. Lines connect only comparable environment/corpus/protocol series. Intervals describe within-run variability, not hardware-independent uncertainty.

| Date | Source commit | Median ratio (95% interval) | Pairs/PDF | Report |
|---|---|---:|---:|---|
| 2026-10-25 | [90636515fd15](https://github.com/l4rzy/okular-mupdf-ng/commit/90636515fd158d7a8662bfd1a82497d853e0f5a7) | 2.455× (2.453–2.462) | 20 | [details](reports/90636515fd158d7a8662bfd1a82497d853e0f5a7/40216383522-1/report.md) |
| 2026-10-25 | [fee75c813b74](https://github.com/l4rzy/okular-mupdf-ng/commit/fee75c813b7455a2607915a7115f74ddc5972d59) | 2.260× (2.257–2.263) | 30 | [details](reports/fee75c813b7455a2607915a7115f74ddc5972d59/40203127246-1/report.md) |
| 2026-10-25 | [fee75c813b74](https://github.com/l4rzy/okular-mupdf-ng/commit/fee75c813b7455a2607915a7115f74ddc5972d59) | 2.433× (2.428–2.435) | 20 | [details](reports/fee75c813b7455a2607915a7115f74ddc5972d59/40177805050-1/report.md) |

The latest 50 runs are listed here; all detailed reports remain under `reports/`.
<!-- benchmark-history:end -->

## Corpus v1

Five unmodified, version-pinned arXiv PDFs cover image-heavy graphics, equations,
and dense text and tables. See [CREDITS.md](CREDITS.md) for the paper inventory,
authors, sources, licenses, and attribution.

## Integrity and reproducibility

`corpus/manifest.json` records authors, versioned source links, licenses, page counts, sizes, and hashes. Only these five CC BY 4.0 papers are mirrored; other local books and papers without redistribution permission are not included.

Verify files from the repository root:

```sh
sha256sum --check corpus/SHA256SUMS
```

Keep corpus v1 unchanged once published. Future additions or replacements should increment the corpus version so historical benchmark results remain comparable.

## Licensing

The papers are third-party works licensed individually under CC BY 4.0. See
[CREDITS.md](CREDITS.md) for attribution and license details. Retain those credits,
source and license links, and original copyright/license notices when
redistributing the papers.

The benchmark harness and automation are licensed under GPL-3.0-or-later; see [COPYING](COPYING).

## Running the benchmark

The [standalone harness](bench/README.md) builds and measures a selected commit
of [okular-mupdf-ng](https://github.com/l4rzy/okular-mupdf-ng) against the official
installed Poppler backend. Use `make bench` locally with a separately built plugin.
Python tooling and Matplotlib are managed by uv with locked dependencies.

The **PDF backend benchmark** workflow runs weekly on Monday at 05:23 UTC and
manually through the Actions tab. Manual runs accept a plugin branch, tag, or
commit and the number of paired trials (default 30 per PDF). Results record the
resolved plugin commit, benchmark commit, corpus, CPU, and dependency versions.
No push trigger or cross-repository publishing secret is required.

The headline is the median paired Poppler / MuPDF-NG rendering ratio; above 1
favors MuPDF-NG. Each PDF has equal weight. The worker stays alive throughout
each trial, and startup is reported separately. Successful runs update the tables
and graph above and retain detailed reports and compressed samples under
`reports/<plugin-sha>/<run-attempt>/`. See the [methodology and CI setup](bench/README.md).

Benchmarks use Relaxed sandbox enforcement so real documents can open on
container runners with partial hardening. Available worker sandbox protections
remain enabled. Corpus page counts are checked before rendering, and failures
stop immediately rather than timing error placeholders.

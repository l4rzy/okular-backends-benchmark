# Okular Backends Benchmark

Benchmarks comparing the **[MuPDF-NG backend](https://github.com/l4rzy/okular-mupdf-ng)** with **[Okular’s official Poppler
backend](https://github.com/KDE/okular/tree/master/generators/poppler)**, using a versioned PDF corpus and tracking performance over time.

<!-- benchmark-history:start -->
## Backend performance history

![Paired rendering ratio over time](trend.svg)

Median ratio = Poppler / MuPDF-NG rendering time; **above 1 favors MuPDF-NG**. Opening and worker startup are excluded. Each PDF has equal weight. Lines group runs by CPU model and Poppler version. Intervals describe within-run variability, not hardware-independent uncertainty.

| Date | Source commit | Median ratio (95% interval) | Pairs/PDF | Report |
|---|---|---:|---:|---|
| 2026-10-28 | [a277ab1c5922](https://github.com/l4rzy/okular-mupdf-ng/commit/a277ab1c5922f3c941ac35f25cdbcfd3e986244a) | 2.229× (2.221–2.236) | 30 | [details](reports/a277ab1c5922f3c941ac35f25cdbcfd3e986244a/40748151792-1/report.md) |
| 2026-10-27 | [c009bf850cb1](https://github.com/l4rzy/okular-mupdf-ng/commit/c009bf850cb10fb85ee4d5dea6db2f774085bc89) | 2.214× (2.209–2.227) | 30 | [details](reports/c009bf850cb10fb85ee4d5dea6db2f774085bc89/40444225258-1/report.md) |
| 2026-10-26 | [fe1e49a3aef7](https://github.com/l4rzy/okular-mupdf-ng/commit/fe1e49a3aef7d3dc080155190f3a5d95de37adcb) | 2.248× (2.245–2.259) | 30 | [details](reports/fe1e49a3aef7d3dc080155190f3a5d95de37adcb/40313897634-1/report.md) |
| 2026-10-26 | [fe1e49a3aef7](https://github.com/l4rzy/okular-mupdf-ng/commit/fe1e49a3aef7d3dc080155190f3a5d95de37adcb) | 2.246× (2.234–2.259) | 20 | [details](reports/fe1e49a3aef7d3dc080155190f3a5d95de37adcb/40267419123-1/report.md) |
| 2026-10-26 | [38b3be7377a6](https://github.com/l4rzy/okular-mupdf-ng/commit/38b3be7377a60d08ff61efdde29c5e174398d413) | 2.224× (2.213–2.233) | 20 | [details](reports/38b3be7377a60d08ff61efdde29c5e174398d413/40264209914-1/report.md) |
| 2026-10-25 | [719a45dc838b](https://github.com/l4rzy/okular-mupdf-ng/commit/719a45dc838b57fb452312596f02749590f241e4) | 2.288× (2.284–2.291) | 30 | [details](reports/719a45dc838b57fb452312596f02749590f241e4/40234409410-1/report.md) |
| 2026-10-25 | [90636515fd15](https://github.com/l4rzy/okular-mupdf-ng/commit/90636515fd158d7a8662bfd1a82497d853e0f5a7) | 2.455× (2.453–2.462) | 20 | [details](reports/90636515fd158d7a8662bfd1a82497d853e0f5a7/40216383522-1/report.md) |
| 2026-10-25 | [fee75c813b74](https://github.com/l4rzy/okular-mupdf-ng/commit/fee75c813b7455a2607915a7115f74ddc5972d59) | 2.260× (2.257–2.263) | 30 | [details](reports/fee75c813b7455a2607915a7115f74ddc5972d59/40203127246-1/report.md) |
| 2026-10-25 | [fee75c813b74](https://github.com/l4rzy/okular-mupdf-ng/commit/fee75c813b7455a2607915a7115f74ddc5972d59) | 2.433× (2.428–2.435) | 20 | [details](reports/fee75c813b7455a2607915a7115f74ddc5972d59/40177805050-1/report.md) |

The latest 50 runs are listed here; all detailed reports remain under `reports/`.
<!-- benchmark-history:end -->

## Corpus v1

Five unmodified arXiv PDFs cover graphics, equations, and dense text and tables.
Versions and hashes are pinned in [the manifest](corpus/manifest.json).
See [CREDITS.md](CREDITS.md) for paper details, attribution, and CC BY 4.0 licenses.
Keep corpus v1 unchanged; additions or replacements require a new version.

Verify the PDFs:

```sh
sha256sum --check corpus/SHA256SUMS
```

## Run benchmarks

Build MuPDF-NG separately, then run `make bench`. See the
[setup and methodology](bench/README.md) for dependencies and options.

CI runs weekly on Mondays at 05:23 UTC or manually through
**Actions → PDF backend benchmark**. Reports and raw samples are saved in
[reports/](reports/).

## License

The harness and automation use [GPL-3.0-or-later](COPYING). Papers use CC BY 4.0;
retain the attribution in [CREDITS.md](CREDITS.md) and original license notices
when redistributing them.

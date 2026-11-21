# MuPDF-NG vs PDFium benchmark history

Ratio = PDFium rendering time / MuPDF-NG rendering time; values above 1 favor MuPDF-NG. Opening and worker startup are excluded. Each PDF has equal weight.

<!-- pdfium-history:start -->
![MuPDF-NG vs PDFium rendering history](pdfium-trend.svg)

Lines group runs by CPU, PDFium library, corpus, and workload. Intervals describe within-run variability.

| Date | MuPDF-NG commit / package | PDFium commit | Median ratio (95% interval) | Repeats/PDF | Run |
|---|---|---|---:|---:|---|
| 2026-11-21 | okular-mupdf-ng 0.6.5-1 | [9faa704a1051](https://github.com/l4rzy/okular-backend-pdfium/commit/9faa704a10511654cf5e38e2285a61167cd65947) | 0.843× (0.842–0.845) | 30 | [details](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/44864767601) |
| 2026-11-16 | okular-mupdf-ng 0.6.4-1 | [9faa704a1051](https://github.com/l4rzy/okular-backend-pdfium/commit/9faa704a10511654cf5e38e2285a61167cd65947) | 0.742× (0.739–0.745) | 30 | [details](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/43975757323) |
| 2026-11-16 | [0c2aca4cd5ed](https://github.com/l4rzy/okular-mupdf-ng/commit/0c2aca4cd5ed25f310e30c3a332f92971e2e18bc) | [9faa704a1051](https://github.com/l4rzy/okular-backend-pdfium/commit/9faa704a10511654cf5e38e2285a61167cd65947) | 0.732× (0.728–0.734) | 30 | [details](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/43879235720) |
| 2026-11-15 | okular-mupdf-ng 0.6.4-1 | [9faa704a1051](https://github.com/l4rzy/okular-backend-pdfium/commit/9faa704a10511654cf5e38e2285a61167cd65947) | 0.791× (0.788–0.796) | 30 | [details](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/43747655757) |
| 2026-11-14 | okular-mupdf-ng 0.6.3-1 | [9faa704a1051](https://github.com/l4rzy/okular-backend-pdfium/commit/9faa704a10511654cf5e38e2285a61167cd65947) | 0.732× (0.730–0.734) | 30 | [details](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/43651081683) |
| 2026-11-14 | okular-mupdf-ng 0.6.3-1 | [9faa704a1051](https://github.com/l4rzy/okular-backend-pdfium/commit/9faa704a10511654cf5e38e2285a61167cd65947) | 0.734× (0.730–0.736) | 30 | [details](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/43649250177) |
<!-- pdfium-history:end -->

<!-- pdfium-latest:start -->
## Latest per-document results

Ratios are medians of paired trial ratios. Times are median milliseconds.

| PDF | Pages | PDFium / MuPDF-NG | MuPDF-NG render | PDFium render |
|---|---:|---:|---:|---:|
| 2609.00625v1 | 14 | 1.013× | 2739.756 | 2758.623 |
| 2609.09123v1 | 24 | 0.884× | 2706.731 | 2397.380 |
| 2610.26067v1 | 16 | 0.816× | 3283.394 | 2677.224 |
| 2312.00752v2 | 36 | 0.719× | 638.910 | 459.139 |
| 2307.03109v9 | 45 | 0.813× | 566.898 | 459.872 |

Latest run: [44864767601-1](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/44864767601); PDFium library SHA-256 `63b70290e3e88eff6b236a4c87cb58461b4fe9fae56217314eeda31aff741479`.
<!-- pdfium-latest:end -->

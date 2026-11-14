# MuPDF-NG vs PDFium benchmark history

Ratio = PDFium rendering time / MuPDF-NG rendering time; values above 1 favor MuPDF-NG. Opening and worker startup are excluded. Each PDF has equal weight.

<!-- pdfium-history:start -->
![MuPDF-NG vs PDFium rendering history](pdfium-trend.svg)

Lines group runs by CPU, PDFium library, corpus, and workload. Intervals describe within-run variability.

| Date | MuPDF-NG commit / package | PDFium commit | Median ratio (95% interval) | Repeats/PDF | Run |
|---|---|---|---:|---:|---|
| 2026-11-14 | okular-mupdf-ng 0.6.3-1 | [9faa704a1051](https://github.com/l4rzy/okular-backend-pdfium/commit/9faa704a10511654cf5e38e2285a61167cd65947) | 0.732× (0.730–0.734) | 30 | [details](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/43651081683) |
| 2026-11-14 | okular-mupdf-ng 0.6.3-1 | [9faa704a1051](https://github.com/l4rzy/okular-backend-pdfium/commit/9faa704a10511654cf5e38e2285a61167cd65947) | 0.734× (0.730–0.736) | 30 | [details](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/43649250177) |
<!-- pdfium-history:end -->

<!-- pdfium-latest:start -->
## Latest per-document results

Ratios are medians of paired trial ratios. Times are median milliseconds.

| PDF | Pages | PDFium / MuPDF-NG | MuPDF-NG render | PDFium render |
|---|---:|---:|---:|---:|
| 2609.00625v1 | 14 | 0.913× | 2953.510 | 2708.954 |
| 2609.09123v1 | 24 | 0.792× | 2722.569 | 2155.363 |
| 2610.26067v1 | 16 | 0.794× | 3420.278 | 2714.125 |
| 2312.00752v2 | 36 | 0.577× | 738.391 | 425.754 |
| 2307.03109v9 | 45 | 0.640× | 670.749 | 427.489 |

Latest run: [43651081683-1](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/43651081683); PDFium library SHA-256 `66e304f9bdcbab0ffcf20f50bd045ff64741f868c035c14fe717d9f59e628dae`.
<!-- pdfium-latest:end -->

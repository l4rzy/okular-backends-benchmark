# MuPDF-NG vs PDFium benchmark history

Ratio = PDFium rendering time / MuPDF-NG rendering time; values above 1 favor MuPDF-NG. Opening and worker startup are excluded. Each PDF has equal weight.

<!-- pdfium-history:start -->
![MuPDF-NG vs PDFium rendering history](pdfium-trend.svg)

Lines group runs by CPU, PDFium library, corpus, and workload. Intervals describe within-run variability.

| Date | MuPDF-NG commit / package | PDFium commit | Median ratio (95% interval) | Repeats/PDF | Run |
|---|---|---|---:|---:|---|
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
| 2609.00625v1 | 14 | 0.956× | 2407.600 | 2303.605 |
| 2609.09123v1 | 24 | 0.743× | 2469.463 | 1837.801 |
| 2610.26067v1 | 16 | 0.805× | 2862.931 | 2303.020 |
| 2312.00752v2 | 36 | 0.573× | 639.609 | 365.832 |
| 2307.03109v9 | 45 | 0.640× | 573.342 | 366.788 |

Latest run: [43879235720-1](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/43879235720); PDFium library SHA-256 `66e304f9bdcbab0ffcf20f50bd045ff64741f868c035c14fe717d9f59e628dae`.
<!-- pdfium-latest:end -->

# PDF backend benchmark

MuPDF-NG commit / package: okular-mupdf-ng 0.6.4-1.

Benchmark commit: `84e3252f3e32c6a90f0d93da2aff6d13f8400f06`.

Run: [43975757323-1](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/43975757323), 2026-11-16T23:31:36.171031+00:00.

**Median paired rendering ratio: 2.214×** (95% bootstrap interval 2.205–2.222×).

Ratio = Poppler time / MuPDF-NG time; above 1 favors MuPDF-NG. Each trial uses the geometric mean of document ratios, giving each PDF equal weight. The headline is the median of those trial scores. The primary workload sums first-page and sequential-render request times, excluding document opening and worker startup. The worker stays alive for all requests in a trial.

MuPDF-NG uses **Relaxed sandbox enforcement**: available worker protections remain active, and incomplete host hardening does not block document opening.

300 successful backend trials; 30 pairs per PDF; series `7eb73a82a0a7dd59`.

## Per-document results

Times are medians in milliseconds. Ratios are medians of paired ratios, not ratios of medians.

| PDF | Pages | Render ratio | MuPDF-NG render batch | Poppler render batch | MuPDF-NG open → first page | Poppler open → first page |
|---|---:|---:|---:|---:|---:|---:|
| 2609.00625v1 | 14 | 2.374× | 2937.322 | 6970.864 | 254.068 | 619.323 |
| 2609.09123v1 | 24 | 1.935× | 2693.884 | 5210.913 | 63.120 | 44.969 |
| 2610.26067v1 | 16 | 3.865× | 3404.473 | 13174.099 | 76.715 | 60.507 |
| 2312.00752v2 | 36 | 1.768× | 708.966 | 1255.359 | 109.700 | 76.708 |
| 2307.03109v9 | 45 | 1.724× | 640.170 | 1102.089 | 89.687 | 78.752 |

## Individual requests

Times are milliseconds; p95 is shown only for at least 20 samples. Cache hits are separate.

| PDF | Backend | Phase | Cache | N | Median | p95 | Maximum |
|---|---|---|---|---:|---:|---:|---:|
| 2609.00625v1 | mupdfng | first_page | miss | 30 | 228.222798 | 253.350299 | 253.953660 |
| 2609.00625v1 | mupdfng | random | hit | 420 | 0.000526 | 0.005380 | 0.010349 |
| 2609.00625v1 | mupdfng | revisit | hit | 420 | 0.000361 | 0.000711 | 0.016200 |
| 2609.00625v1 | mupdfng | sequential | miss | 390 | 107.504969 | 966.258324 | 1021.067301 |
| 2609.00625v1 | poppler | first_page | miss | 30 | 610.023387 | 660.668003 | 662.235604 |
| 2609.00625v1 | poppler | random | hit | 420 | 0.000461 | 0.005660 | 0.009248 |
| 2609.00625v1 | poppler | revisit | hit | 420 | 0.000431 | 0.000571 | 0.004047 |
| 2609.00625v1 | poppler | sequential | miss | 390 | 234.333513 | 2617.781801 | 2662.696794 |
| 2609.09123v1 | mupdfng | first_page | miss | 30 | 36.959855 | 37.862032 | 38.071267 |
| 2609.09123v1 | mupdfng | random | hit | 537 | 0.000661 | 0.007564 | 0.094267 |
| 2609.09123v1 | mupdfng | random | miss | 63 | 248.673132 | 267.946667 | 285.498192 |
| 2609.09123v1 | mupdfng | revisit | hit | 600 | 0.000371 | 0.000792 | 0.006853 |
| 2609.09123v1 | mupdfng | sequential | miss | 570 | 24.357708 | 1462.128865 | 1532.808670 |
| 2609.09123v1 | poppler | first_page | miss | 30 | 37.870907 | 38.997701 | 39.060041 |
| 2609.09123v1 | poppler | random | hit | 537 | 0.000641 | 0.006842 | 0.115405 |
| 2609.09123v1 | poppler | random | miss | 63 | 1058.211058 | 1343.978188 | 1393.513711 |
| 2609.09123v1 | poppler | revisit | hit | 600 | 0.000621 | 0.000791 | 0.106609 |
| 2609.09123v1 | poppler | sequential | miss | 570 | 44.114182 | 1706.864020 | 1793.287611 |
| 2610.26067v1 | mupdfng | first_page | miss | 30 | 50.032360 | 51.318373 | 51.705068 |
| 2610.26067v1 | mupdfng | random | hit | 480 | 0.000421 | 0.003256 | 0.021480 |
| 2610.26067v1 | mupdfng | revisit | hit | 480 | 0.000361 | 0.000621 | 0.001242 |
| 2610.26067v1 | mupdfng | sequential | miss | 450 | 115.222407 | 842.775662 | 881.702225 |
| 2610.26067v1 | poppler | first_page | miss | 30 | 52.776606 | 57.344113 | 84.504457 |
| 2610.26067v1 | poppler | random | hit | 480 | 0.000461 | 0.004319 | 0.007224 |
| 2610.26067v1 | poppler | revisit | hit | 480 | 0.000441 | 0.000681 | 0.021370 |
| 2610.26067v1 | poppler | sequential | miss | 450 | 450.611137 | 3877.085169 | 3924.787530 |
| 2312.00752v2 | mupdfng | first_page | miss | 30 | 86.660017 | 88.841787 | 89.504993 |
| 2312.00752v2 | mupdfng | random | hit | 409 | 0.000841 | 0.004990 | 0.017492 |
| 2312.00752v2 | mupdfng | random | miss | 191 | 28.661582 | 35.406630 | 38.567346 |
| 2312.00752v2 | mupdfng | revisit | hit | 600 | 0.000465 | 0.000932 | 0.006462 |
| 2312.00752v2 | mupdfng | sequential | miss | 570 | 32.253849 | 41.184369 | 72.681620 |
| 2312.00752v2 | poppler | first_page | miss | 30 | 69.326285 | 71.005981 | 73.476293 |
| 2312.00752v2 | poppler | random | hit | 409 | 0.000711 | 0.005951 | 0.030046 |
| 2312.00752v2 | poppler | random | miss | 191 | 55.126464 | 69.240473 | 99.028498 |
| 2312.00752v2 | poppler | revisit | hit | 600 | 0.000476 | 0.000722 | 0.023594 |
| 2312.00752v2 | poppler | sequential | miss | 570 | 63.228138 | 69.238287 | 96.874027 |
| 2307.03109v9 | mupdfng | first_page | miss | 30 | 60.596380 | 63.472644 | 72.500508 |
| 2307.03109v9 | mupdfng | random | hit | 351 | 0.000942 | 0.006261 | 0.020508 |
| 2307.03109v9 | mupdfng | random | miss | 249 | 32.185341 | 42.088252 | 45.264174 |
| 2307.03109v9 | mupdfng | revisit | hit | 600 | 0.000561 | 0.000962 | 0.006892 |
| 2307.03109v9 | mupdfng | sequential | miss | 570 | 27.831792 | 57.810100 | 67.623191 |
| 2307.03109v9 | poppler | first_page | miss | 30 | 66.234665 | 67.805402 | 71.334594 |
| 2307.03109v9 | poppler | random | hit | 351 | 0.000791 | 0.006582 | 0.034013 |
| 2307.03109v9 | poppler | random | miss | 249 | 60.470512 | 69.252265 | 109.087874 |
| 2307.03109v9 | poppler | revisit | hit | 600 | 0.000601 | 0.000802 | 0.006933 |
| 2307.03109v9 | poppler | sequential | miss | 570 | 55.919905 | 72.696525 | 88.564955 |

## Environment

```json
{
  "platform": "Linux-7.0.0-1019-azure-x86_64-with-glibc2.44",
  "machine": "x86_64",
  "cpu_model": "AMD EPYC 7763 64-Core Processor",
  "logical_cpus": 4,
  "available_cpus": 4,
  "python": "3.14.10",
  "plugin_build": {},
  "protocol": "pdf-render-v1",
  "protocol_sha256": "8843c572bb81fb24fee3e7877bad432760f205c338332af06e938d80950fa7b2",
  "mupdf_package": {
    "name": "okular-mupdf-ng",
    "version": "okular-mupdf-ng 0.6.4-1",
    "plugin_sha256": "a2ec04cd7edc9e648be6b97530f739938eb4c0f4239ee6f82417e34cdf2e57ee"
  },
  "source_commit": null,
  "source_dirty": false,
  "benchmark_commit": "84e3252f3e32c6a90f0d93da2aff6d13f8400f06",
  "benchmark_dirty": false,
  "runner_image": "local",
  "runner_image_version": "local",
  "container_image": "archlinux:latest",
  "versions": {
    "poppler": "26.11.0",
    "okular": "okular 26.08.3",
    "compiler": "c++ (GCC) 16.2.1 20260810\nCopyright (C) 2026 Free Software Foundation, Inc.\nThis is free software; see the source for copying conditions.  There is NO\nwarranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.",
    "mupdf": "okular-mupdf-ng 0.6.4-1"
  }
}
```

## Interpretation limits

Paired trials reduce host-speed noise, but CPU architectures can favor the backends differently. Graph lines group runs by CPU model and Poppler version; other environment and benchmark settings remain recorded in the reports. Bootstrap intervals resample whole paired trial scores; repeated pages are not independent samples of all PDFs. This is an offscreen rendering benchmark, not a GUI scrolling, memory, or visual-fidelity measurement. OS file caches are warm/uncontrolled. No performance merge gate is applied.

Okular warning-bearing trials: 150. See `summary.json` and `samples.jsonl.gz` for details.

Artifacts: [summary](summary.json), [raw trials](samples.jsonl.gz), [corpus manifest](corpus-manifest.json).

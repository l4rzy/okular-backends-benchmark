# PDF backend benchmark

Source commit: [b94a3ad12c2d71bd6b09c3b9db9955bd7e03c240](https://github.com/l4rzy/okular-mupdf-ng/commit/b94a3ad12c2d71bd6b09c3b9db9955bd7e03c240).

Benchmark commit: `26ce5d87c01bb9d64091f4415b909ea4ab475675`.

Run: [40991003023-1](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/40991003023), 2026-10-30T02:53:52.874937+00:00.

**Median paired rendering ratio: 2.234×** (95% bootstrap interval 2.231–2.243×).

Ratio = Poppler time / MuPDF-NG time; above 1 favors MuPDF-NG. Each trial uses the geometric mean of document ratios, giving each PDF equal weight. The headline is the median of those trial scores. The primary workload sums first-page and sequential-render request times, excluding document opening and worker startup. The worker stays alive for all requests in a trial.

MuPDF-NG uses **Relaxed sandbox enforcement**: available worker protections remain active, and incomplete host hardening does not block document opening.

300 successful backend trials; 30 pairs per PDF; series `d2c307ea82a68627`.

## Per-document results

Times are medians in milliseconds. Ratios are medians of paired ratios, not ratios of medians.

| PDF | Pages | Render ratio | MuPDF-NG render batch | Poppler render batch | MuPDF-NG open → first page | Poppler open → first page |
|---|---:|---:|---:|---:|---:|---:|
| 2609.00625v1 | 14 | 2.467× | 2837.672 | 6998.924 | 252.273 | 622.048 |
| 2609.09123v1 | 24 | 1.849× | 2823.944 | 5227.568 | 65.310 | 45.352 |
| 2610.26067v1 | 16 | 4.023× | 3298.531 | 13263.213 | 79.466 | 62.271 |
| 2312.00752v2 | 36 | 1.761× | 725.815 | 1274.874 | 115.826 | 77.689 |
| 2307.03109v9 | 45 | 1.724× | 653.147 | 1124.254 | 93.048 | 80.104 |

## Individual requests

Times are milliseconds; p95 is shown only for at least 20 samples. Cache hits are separate.

| PDF | Backend | Phase | Cache | N | Median | p95 | Maximum |
|---|---|---|---|---:|---:|---:|---:|
| 2609.00625v1 | mupdfng | first_page | miss | 30 | 227.247251 | 232.789539 | 237.758415 |
| 2609.00625v1 | mupdfng | random | hit | 420 | 0.000671 | 0.006051 | 0.028684 |
| 2609.00625v1 | mupdfng | revisit | hit | 420 | 0.000350 | 0.000771 | 0.000972 |
| 2609.00625v1 | mupdfng | sequential | miss | 390 | 98.027105 | 946.649169 | 979.412808 |
| 2609.00625v1 | poppler | first_page | miss | 30 | 612.534038 | 615.340723 | 665.381443 |
| 2609.00625v1 | poppler | random | hit | 420 | 0.000441 | 0.006522 | 0.020569 |
| 2609.00625v1 | poppler | revisit | hit | 420 | 0.000431 | 0.000481 | 0.001062 |
| 2609.00625v1 | poppler | sequential | miss | 390 | 236.402390 | 2616.013477 | 2672.367162 |
| 2609.09123v1 | mupdfng | first_page | miss | 30 | 38.766102 | 40.177190 | 40.251552 |
| 2609.09123v1 | mupdfng | random | hit | 537 | 0.000601 | 0.007714 | 0.011692 |
| 2609.09123v1 | mupdfng | random | miss | 63 | 238.319397 | 258.624865 | 269.226282 |
| 2609.09123v1 | mupdfng | revisit | hit | 600 | 0.000351 | 0.000732 | 0.007765 |
| 2609.09123v1 | mupdfng | sequential | miss | 570 | 24.262707 | 1624.930218 | 1685.067702 |
| 2609.09123v1 | poppler | first_page | miss | 30 | 38.151415 | 39.067175 | 39.092650 |
| 2609.09123v1 | poppler | random | hit | 537 | 0.000631 | 0.007033 | 0.084979 |
| 2609.09123v1 | poppler | random | miss | 63 | 1058.765279 | 1341.969748 | 1381.442471 |
| 2609.09123v1 | poppler | revisit | hit | 600 | 0.000431 | 0.000732 | 0.097914 |
| 2609.09123v1 | poppler | sequential | miss | 570 | 44.065674 | 1673.319310 | 1788.885537 |
| 2610.26067v1 | mupdfng | first_page | miss | 30 | 52.153496 | 54.976599 | 56.930865 |
| 2610.26067v1 | mupdfng | random | hit | 480 | 0.000651 | 0.006653 | 0.011331 |
| 2610.26067v1 | mupdfng | revisit | hit | 480 | 0.000341 | 0.000410 | 0.020488 |
| 2610.26067v1 | mupdfng | sequential | miss | 450 | 112.889974 | 791.057139 | 833.008887 |
| 2610.26067v1 | poppler | first_page | miss | 30 | 54.203546 | 57.213778 | 59.386363 |
| 2610.26067v1 | poppler | random | hit | 480 | 0.000441 | 0.006231 | 0.008646 |
| 2610.26067v1 | poppler | revisit | hit | 480 | 0.000431 | 0.000471 | 0.000521 |
| 2610.26067v1 | poppler | sequential | miss | 450 | 453.188716 | 3899.578497 | 3975.007021 |
| 2312.00752v2 | mupdfng | first_page | miss | 30 | 92.211780 | 92.978772 | 93.066112 |
| 2312.00752v2 | mupdfng | random | hit | 409 | 0.000802 | 0.007594 | 0.010880 |
| 2312.00752v2 | mupdfng | random | miss | 191 | 28.807149 | 34.713767 | 37.022205 |
| 2312.00752v2 | mupdfng | revisit | hit | 600 | 0.000371 | 0.000881 | 0.008095 |
| 2312.00752v2 | mupdfng | sequential | miss | 570 | 33.044142 | 41.293007 | 47.013571 |
| 2312.00752v2 | poppler | first_page | miss | 30 | 70.020071 | 86.601351 | 89.702884 |
| 2312.00752v2 | poppler | random | hit | 409 | 0.000711 | 0.007495 | 0.031128 |
| 2312.00752v2 | poppler | random | miss | 191 | 56.525368 | 69.345784 | 76.763307 |
| 2312.00752v2 | poppler | revisit | hit | 600 | 0.000581 | 0.000811 | 0.007884 |
| 2312.00752v2 | poppler | sequential | miss | 570 | 64.083062 | 70.068108 | 95.595308 |
| 2307.03109v9 | mupdfng | first_page | miss | 30 | 63.339206 | 65.575104 | 65.635658 |
| 2307.03109v9 | mupdfng | random | hit | 351 | 0.000922 | 0.008115 | 0.026730 |
| 2307.03109v9 | mupdfng | random | miss | 249 | 32.790905 | 43.341763 | 52.321597 |
| 2307.03109v9 | mupdfng | revisit | hit | 600 | 0.000611 | 0.000891 | 0.009037 |
| 2307.03109v9 | mupdfng | sequential | miss | 570 | 28.106544 | 61.036438 | 70.457509 |
| 2307.03109v9 | poppler | first_page | miss | 30 | 67.125306 | 70.999859 | 71.895327 |
| 2307.03109v9 | poppler | random | hit | 351 | 0.000812 | 0.007665 | 0.097483 |
| 2307.03109v9 | poppler | random | miss | 249 | 61.747164 | 68.815477 | 74.708198 |
| 2307.03109v9 | poppler | revisit | hit | 600 | 0.000607 | 0.000831 | 0.009658 |
| 2307.03109v9 | poppler | sequential | miss | 570 | 56.717124 | 73.920610 | 86.059297 |

## Environment

```json
{
  "platform": "Linux-7.0.0-1017-azure-x86_64-with-glibc2.44",
  "machine": "x86_64",
  "cpu_model": "AMD EPYC 7763 64-Core Processor",
  "logical_cpus": 4,
  "available_cpus": 4,
  "python": "3.14.8",
  "plugin_build": {
    "CMAKE_BUILD_TYPE": "Release",
    "CMAKE_CXX_COMPILER": "/usr/sbin/clang++",
    "DISABLE_WORKER_SANDBOX": "OFF",
    "ENABLE_BUILD_TREE_WORKER": "ON",
    "ENABLE_LTO": "ON",
    "ENABLE_MU_DEBUG": "OFF",
    "MUPDF_CJK_FALLBACK": "droidfull",
    "MUPDF_OPTIMIZED_BUILD": "ON",
    "USE_SYSTEM_MUPDF": "OFF"
  },
  "protocol": "pdf-render-v1",
  "protocol_sha256": "7c757dec53e8b246baf949af0ed909a28327142a47f17ebf98cbbd308a744d72",
  "source_commit": "b94a3ad12c2d71bd6b09c3b9db9955bd7e03c240",
  "source_dirty": false,
  "benchmark_commit": "26ce5d87c01bb9d64091f4415b909ea4ab475675",
  "benchmark_dirty": false,
  "runner_image": "local",
  "runner_image_version": "local",
  "container_image": "archlinux:latest",
  "versions": {
    "poppler": "26.10.0",
    "okular": "okular 26.08.2",
    "compiler": "clang version 23.1.4\nTarget: x86_64-pc-linux-gnu\nThread model: posix\nInstalledDir: /usr/bin",
    "mupdf": "1.28.5"
  }
}
```

## Interpretation limits

Paired trials reduce host-speed noise, but CPU architectures can favor the backends differently. Graph lines group runs by CPU model and Poppler version; other environment and benchmark settings remain recorded in the reports. Bootstrap intervals resample whole paired trial scores; repeated pages are not independent samples of all PDFs. This is an offscreen rendering benchmark, not a GUI scrolling, memory, or visual-fidelity measurement. OS file caches are warm/uncontrolled. No performance merge gate is applied.

Okular warning-bearing trials: 150. See `summary.json` and `samples.jsonl.gz` for details.

Artifacts: [summary](summary.json), [raw trials](samples.jsonl.gz), [corpus manifest](corpus-manifest.json).

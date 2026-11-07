# PDF backend benchmark

Source commit: [6605372dedb3bf14c8245b6a840d927e9a8e19d7](https://github.com/l4rzy/okular-mupdf-ng/commit/6605372dedb3bf14c8245b6a840d927e9a8e19d7).

Benchmark commit: `027f96a374cd954fe6a2b95336fe88784b9f6e55`.

Run: [42337580678-1](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/42337580678), 2026-11-07T04:48:12.064420+00:00.

**Median paired rendering ratio: 2.232×** (95% bootstrap interval 2.219–2.236×).

Ratio = Poppler time / MuPDF-NG time; above 1 favors MuPDF-NG. Each trial uses the geometric mean of document ratios, giving each PDF equal weight. The headline is the median of those trial scores. The primary workload sums first-page and sequential-render request times, excluding document opening and worker startup. The worker stays alive for all requests in a trial.

MuPDF-NG uses **Relaxed sandbox enforcement**: available worker protections remain active, and incomplete host hardening does not block document opening.

300 successful backend trials; 30 pairs per PDF; series `784feedc96d7056e`.

## Per-document results

Times are medians in milliseconds. Ratios are medians of paired ratios, not ratios of medians.

| PDF | Pages | Render ratio | MuPDF-NG render batch | Poppler render batch | MuPDF-NG open → first page | Poppler open → first page |
|---|---:|---:|---:|---:|---:|---:|
| 2609.00625v1 | 14 | 2.449× | 2699.105 | 6607.253 | 239.235 | 588.813 |
| 2609.09123v1 | 24 | 1.792× | 2748.830 | 4921.097 | 60.270 | 43.144 |
| 2610.26067v1 | 16 | 4.030× | 3110.372 | 12555.459 | 73.445 | 59.211 |
| 2312.00752v2 | 36 | 1.779× | 669.421 | 1190.101 | 107.306 | 72.948 |
| 2307.03109v9 | 45 | 1.734× | 601.503 | 1049.272 | 86.481 | 75.161 |

## Individual requests

Times are milliseconds; p95 is shown only for at least 20 samples. Cache hits are separate.

| PDF | Backend | Phase | Cache | N | Median | p95 | Maximum |
|---|---|---|---|---:|---:|---:|---:|
| 2609.00625v1 | mupdfng | first_page | miss | 30 | 216.040415 | 228.522290 | 234.617322 |
| 2609.00625v1 | mupdfng | random | hit | 420 | 0.000611 | 0.003296 | 0.016942 |
| 2609.00625v1 | mupdfng | revisit | hit | 420 | 0.000331 | 0.000601 | 0.022863 |
| 2609.00625v1 | mupdfng | sequential | miss | 390 | 93.860309 | 897.536833 | 966.607923 |
| 2609.00625v1 | poppler | first_page | miss | 30 | 579.902668 | 603.056906 | 621.718138 |
| 2609.00625v1 | poppler | random | hit | 420 | 0.000421 | 0.003587 | 0.005100 |
| 2609.00625v1 | poppler | revisit | hit | 420 | 0.000410 | 0.000471 | 0.002725 |
| 2609.00625v1 | poppler | sequential | miss | 390 | 224.456147 | 2480.464022 | 2580.840670 |
| 2609.09123v1 | mupdfng | first_page | miss | 30 | 36.165519 | 38.436171 | 40.318654 |
| 2609.09123v1 | mupdfng | random | hit | 537 | 0.000561 | 0.007174 | 0.009979 |
| 2609.09123v1 | mupdfng | random | miss | 63 | 228.600293 | 247.455756 | 256.302951 |
| 2609.09123v1 | mupdfng | revisit | hit | 600 | 0.000341 | 0.000721 | 0.011251 |
| 2609.09123v1 | mupdfng | sequential | miss | 570 | 22.471197 | 1607.621240 | 1679.457582 |
| 2609.09123v1 | poppler | first_page | miss | 30 | 36.290722 | 42.157632 | 43.105285 |
| 2609.09123v1 | poppler | random | hit | 537 | 0.000591 | 0.006141 | 0.116858 |
| 2609.09123v1 | poppler | random | miss | 63 | 1005.536123 | 1291.733571 | 1319.253606 |
| 2609.09123v1 | poppler | revisit | hit | 600 | 0.000451 | 0.000681 | 0.005330 |
| 2609.09123v1 | poppler | sequential | miss | 570 | 41.096887 | 1580.138003 | 1673.853324 |
| 2610.26067v1 | mupdfng | first_page | miss | 30 | 48.462098 | 51.359216 | 52.937284 |
| 2610.26067v1 | mupdfng | random | hit | 480 | 0.000446 | 0.002825 | 0.005831 |
| 2610.26067v1 | mupdfng | revisit | hit | 480 | 0.000331 | 0.000371 | 0.000832 |
| 2610.26067v1 | mupdfng | sequential | miss | 450 | 105.588476 | 741.658312 | 785.309470 |
| 2610.26067v1 | poppler | first_page | miss | 30 | 51.558574 | 53.286780 | 54.015390 |
| 2610.26067v1 | poppler | random | hit | 480 | 0.000420 | 0.003036 | 0.004539 |
| 2610.26067v1 | poppler | revisit | hit | 480 | 0.000410 | 0.000470 | 0.019156 |
| 2610.26067v1 | poppler | sequential | miss | 450 | 428.738739 | 3671.987764 | 3852.185658 |
| 2312.00752v2 | mupdfng | first_page | miss | 30 | 85.731581 | 95.389197 | 126.827020 |
| 2312.00752v2 | mupdfng | random | hit | 409 | 0.000762 | 0.002936 | 0.005270 |
| 2312.00752v2 | mupdfng | random | miss | 191 | 26.483353 | 32.178388 | 35.297051 |
| 2312.00752v2 | mupdfng | revisit | hit | 600 | 0.000361 | 0.000851 | 0.016331 |
| 2312.00752v2 | mupdfng | sequential | miss | 570 | 30.139787 | 38.845511 | 62.406983 |
| 2312.00752v2 | poppler | first_page | miss | 30 | 65.961138 | 68.643442 | 70.413529 |
| 2312.00752v2 | poppler | random | hit | 409 | 0.000681 | 0.003296 | 0.006282 |
| 2312.00752v2 | poppler | random | miss | 191 | 52.911495 | 65.638696 | 101.884173 |
| 2312.00752v2 | poppler | revisit | hit | 600 | 0.000531 | 0.000852 | 0.003357 |
| 2312.00752v2 | poppler | sequential | miss | 570 | 59.872283 | 66.766467 | 90.595641 |
| 2307.03109v9 | mupdfng | first_page | miss | 30 | 59.497995 | 62.463055 | 65.264013 |
| 2307.03109v9 | mupdfng | random | hit | 351 | 0.000882 | 0.003367 | 0.005500 |
| 2307.03109v9 | mupdfng | random | miss | 249 | 29.793770 | 39.877234 | 43.884137 |
| 2307.03109v9 | mupdfng | revisit | hit | 600 | 0.000390 | 0.000911 | 0.003797 |
| 2307.03109v9 | mupdfng | sequential | miss | 570 | 26.016840 | 55.453336 | 68.136242 |
| 2307.03109v9 | poppler | first_page | miss | 30 | 62.915325 | 66.038823 | 67.816791 |
| 2307.03109v9 | poppler | random | hit | 351 | 0.000772 | 0.003537 | 0.021571 |
| 2307.03109v9 | poppler | random | miss | 249 | 56.897617 | 64.715810 | 75.510691 |
| 2307.03109v9 | poppler | revisit | hit | 600 | 0.000551 | 0.000791 | 0.024576 |
| 2307.03109v9 | poppler | sequential | miss | 570 | 53.002555 | 68.396755 | 88.391856 |

## Environment

```json
{
  "platform": "Linux-7.0.0-1019-azure-x86_64-with-glibc2.44",
  "machine": "x86_64",
  "cpu_model": "AMD EPYC 7763 64-Core Processor",
  "logical_cpus": 4,
  "available_cpus": 4,
  "python": "3.14.9",
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
  "source_commit": "6605372dedb3bf14c8245b6a840d927e9a8e19d7",
  "source_dirty": false,
  "benchmark_commit": "027f96a374cd954fe6a2b95336fe88784b9f6e55",
  "benchmark_dirty": false,
  "runner_image": "local",
  "runner_image_version": "local",
  "container_image": "archlinux:latest",
  "versions": {
    "poppler": "26.10.0",
    "okular": "okular 26.08.3",
    "compiler": "clang version 23.1.4\nTarget: x86_64-pc-linux-gnu\nThread model: posix\nInstalledDir: /usr/bin",
    "mupdf": "1.28.6"
  }
}
```

## Interpretation limits

Paired trials reduce host-speed noise, but CPU architectures can favor the backends differently. Graph lines group runs by CPU model and Poppler version; other environment and benchmark settings remain recorded in the reports. Bootstrap intervals resample whole paired trial scores; repeated pages are not independent samples of all PDFs. This is an offscreen rendering benchmark, not a GUI scrolling, memory, or visual-fidelity measurement. OS file caches are warm/uncontrolled. No performance merge gate is applied.

Okular warning-bearing trials: 150. See `summary.json` and `samples.jsonl.gz` for details.

Artifacts: [summary](summary.json), [raw trials](samples.jsonl.gz), [corpus manifest](corpus-manifest.json).

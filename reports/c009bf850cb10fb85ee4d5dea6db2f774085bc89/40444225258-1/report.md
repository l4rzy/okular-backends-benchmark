# PDF backend benchmark

Source commit: [c009bf850cb10fb85ee4d5dea6db2f774085bc89](https://github.com/l4rzy/okular-mupdf-ng/commit/c009bf850cb10fb85ee4d5dea6db2f774085bc89).

Benchmark commit: `4419de62188a1d3dd28beffc26940b8533274a16`.

Run: [40444225258-1](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/40444225258), 2026-10-27T04:00:42.662499+00:00.

**Median paired rendering ratio: 2.214×** (95% bootstrap interval 2.209–2.227×).

Ratio = Poppler time / MuPDF-NG time; above 1 favors MuPDF-NG. Each trial uses the geometric mean of document ratios, giving each PDF equal weight. The headline is the median of those trial scores. The primary workload sums first-page and sequential-render request times, excluding document opening and worker startup. The worker stays alive for all requests in a trial.

MuPDF-NG uses **Relaxed sandbox enforcement**: available worker protections remain active, and incomplete host hardening does not block document opening.

300 successful backend trials; 30 pairs per PDF; series `d2c307ea82a68627`.

## Per-document results

Times are medians in milliseconds. Ratios are medians of paired ratios, not ratios of medians.

| PDF | Pages | Render ratio | MuPDF-NG render batch | Poppler render batch | MuPDF-NG open → first page | Poppler open → first page |
|---|---:|---:|---:|---:|---:|---:|
| 2609.00625v1 | 14 | 2.448× | 2845.963 | 6979.443 | 249.737 | 623.688 |
| 2609.09123v1 | 24 | 1.846× | 2819.576 | 5215.272 | 62.142 | 45.475 |
| 2610.26067v1 | 16 | 4.078× | 3250.056 | 13281.084 | 79.246 | 62.380 |
| 2312.00752v2 | 36 | 1.732× | 754.432 | 1297.167 | 117.358 | 78.755 |
| 2307.03109v9 | 45 | 1.689× | 678.238 | 1145.348 | 93.158 | 81.071 |

## Individual requests

Times are milliseconds; p95 is shown only for at least 20 samples. Cache hits are separate.

| PDF | Backend | Phase | Cache | N | Median | p95 | Maximum |
|---|---|---|---|---:|---:|---:|---:|
| 2609.00625v1 | mupdfng | first_page | miss | 30 | 226.043746 | 241.473425 | 262.061712 |
| 2609.00625v1 | mupdfng | random | hit | 420 | 0.000651 | 0.006152 | 0.024656 |
| 2609.00625v1 | mupdfng | revisit | hit | 420 | 0.000360 | 0.000772 | 0.001112 |
| 2609.00625v1 | mupdfng | sequential | miss | 390 | 99.708614 | 941.003409 | 1008.108710 |
| 2609.00625v1 | poppler | first_page | miss | 30 | 613.618284 | 666.439172 | 668.127436 |
| 2609.00625v1 | poppler | random | hit | 420 | 0.000431 | 0.005771 | 0.036418 |
| 2609.00625v1 | poppler | revisit | hit | 420 | 0.000405 | 0.000471 | 0.034575 |
| 2609.00625v1 | poppler | sequential | miss | 390 | 236.684530 | 2612.180693 | 2692.278148 |
| 2609.09123v1 | mupdfng | first_page | miss | 30 | 37.638194 | 39.626665 | 39.654467 |
| 2609.09123v1 | mupdfng | random | hit | 537 | 0.000571 | 0.007173 | 0.010740 |
| 2609.09123v1 | mupdfng | random | miss | 63 | 235.417144 | 264.739477 | 283.761436 |
| 2609.09123v1 | mupdfng | revisit | hit | 600 | 0.000360 | 0.000822 | 0.022181 |
| 2609.09123v1 | mupdfng | sequential | miss | 570 | 24.219608 | 1635.808441 | 1692.496839 |
| 2609.09123v1 | poppler | first_page | miss | 30 | 38.192576 | 50.691027 | 51.885532 |
| 2609.09123v1 | poppler | random | hit | 537 | 0.000621 | 0.006873 | 0.116610 |
| 2609.09123v1 | poppler | random | miss | 63 | 1062.670742 | 1340.533601 | 1380.546304 |
| 2609.09123v1 | poppler | revisit | hit | 600 | 0.000391 | 0.000722 | 0.005841 |
| 2609.09123v1 | poppler | sequential | miss | 570 | 44.008566 | 1662.615524 | 1782.470523 |
| 2610.26067v1 | mupdfng | first_page | miss | 30 | 53.314500 | 54.771678 | 55.944619 |
| 2610.26067v1 | mupdfng | random | hit | 480 | 0.000651 | 0.005170 | 0.011461 |
| 2610.26067v1 | mupdfng | revisit | hit | 480 | 0.000345 | 0.000751 | 0.001183 |
| 2610.26067v1 | mupdfng | sequential | miss | 450 | 111.838874 | 782.874372 | 835.736993 |
| 2610.26067v1 | poppler | first_page | miss | 30 | 54.458672 | 60.291074 | 68.789815 |
| 2610.26067v1 | poppler | random | hit | 480 | 0.000411 | 0.005159 | 0.031840 |
| 2610.26067v1 | poppler | revisit | hit | 480 | 0.000371 | 0.000481 | 0.031298 |
| 2610.26067v1 | poppler | sequential | miss | 450 | 454.381643 | 3904.431311 | 4300.206232 |
| 2312.00752v2 | mupdfng | first_page | miss | 30 | 93.707344 | 96.798919 | 96.886409 |
| 2312.00752v2 | mupdfng | random | hit | 409 | 0.000822 | 0.008566 | 0.026530 |
| 2312.00752v2 | mupdfng | random | miss | 191 | 30.709281 | 36.963717 | 50.189012 |
| 2312.00752v2 | mupdfng | revisit | hit | 600 | 0.000430 | 0.000891 | 0.009588 |
| 2312.00752v2 | mupdfng | sequential | miss | 570 | 34.271810 | 42.930004 | 58.764832 |
| 2312.00752v2 | poppler | first_page | miss | 30 | 70.895945 | 77.396506 | 78.467504 |
| 2312.00752v2 | poppler | random | hit | 409 | 0.000702 | 0.008346 | 0.041577 |
| 2312.00752v2 | poppler | random | miss | 191 | 57.136809 | 71.302938 | 78.600882 |
| 2312.00752v2 | poppler | revisit | hit | 600 | 0.000421 | 0.000811 | 0.064941 |
| 2312.00752v2 | poppler | sequential | miss | 570 | 65.117570 | 72.345687 | 104.437169 |
| 2307.03109v9 | mupdfng | first_page | miss | 30 | 63.750580 | 65.993877 | 69.529011 |
| 2307.03109v9 | mupdfng | random | hit | 351 | 0.000892 | 0.008366 | 0.028503 |
| 2307.03109v9 | mupdfng | random | miss | 249 | 34.219525 | 44.934936 | 58.236966 |
| 2307.03109v9 | mupdfng | revisit | hit | 600 | 0.000591 | 0.000912 | 0.031178 |
| 2307.03109v9 | mupdfng | sequential | miss | 570 | 29.531402 | 61.539060 | 73.864183 |
| 2307.03109v9 | poppler | first_page | miss | 30 | 67.793605 | 73.612959 | 73.933361 |
| 2307.03109v9 | poppler | random | hit | 351 | 0.000811 | 0.008266 | 0.045916 |
| 2307.03109v9 | poppler | random | miss | 249 | 61.686770 | 68.842004 | 77.235425 |
| 2307.03109v9 | poppler | revisit | hit | 600 | 0.000601 | 0.000791 | 0.010420 |
| 2307.03109v9 | poppler | sequential | miss | 570 | 57.934573 | 73.956239 | 90.106244 |

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
  "source_commit": "c009bf850cb10fb85ee4d5dea6db2f774085bc89",
  "source_dirty": false,
  "benchmark_commit": "4419de62188a1d3dd28beffc26940b8533274a16",
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

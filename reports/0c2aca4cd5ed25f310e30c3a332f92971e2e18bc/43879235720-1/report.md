# PDF backend benchmark

MuPDF-NG commit / package: [0c2aca4cd5ed](https://github.com/l4rzy/okular-mupdf-ng/commit/0c2aca4cd5ed25f310e30c3a332f92971e2e18bc).

Benchmark commit: `2620955b12179d2034905908b8be36c463cf69d3`.

Run: [43879235720-1](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/43879235720), 2026-11-16T14:12:34.253668+00:00.

**Median paired rendering ratio: 2.048×** (95% bootstrap interval 2.034–2.056×).

Ratio = Poppler time / MuPDF-NG time; above 1 favors MuPDF-NG. Each trial uses the geometric mean of document ratios, giving each PDF equal weight. The headline is the median of those trial scores. The primary workload sums first-page and sequential-render request times, excluding document opening and worker startup. The worker stays alive for all requests in a trial.

MuPDF-NG uses **Relaxed sandbox enforcement**: available worker protections remain active, and incomplete host hardening does not block document opening.

300 successful backend trials; 30 pairs per PDF; series `af046b69c3737394`.

## Per-document results

Times are medians in milliseconds. Ratios are medians of paired ratios, not ratios of medians.

| PDF | Pages | Render ratio | MuPDF-NG render batch | Poppler render batch | MuPDF-NG open → first page | Poppler open → first page |
|---|---:|---:|---:|---:|---:|---:|
| 2609.00625v1 | 14 | 2.374× | 2397.992 | 5690.827 | 214.213 | 510.340 |
| 2609.09123v1 | 24 | 1.700× | 2423.092 | 4118.650 | 54.755 | 35.491 |
| 2610.26067v1 | 16 | 3.632× | 2845.436 | 10328.187 | 66.645 | 48.869 |
| 2312.00752v2 | 36 | 1.596× | 631.044 | 1001.979 | 98.127 | 62.185 |
| 2307.03109v9 | 45 | 1.549× | 575.867 | 886.837 | 79.948 | 64.040 |

## Individual requests

Times are milliseconds; p95 is shown only for at least 20 samples. Cache hits are separate.

| PDF | Backend | Phase | Cache | N | Median | p95 | Maximum |
|---|---|---|---|---:|---:|---:|---:|
| 2609.00625v1 | mupdfng | first_page | miss | 30 | 192.476389 | 209.847145 | 210.624482 |
| 2609.00625v1 | mupdfng | random | hit | 420 | 0.000411 | 0.005138 | 0.021552 |
| 2609.00625v1 | mupdfng | revisit | hit | 420 | 0.000240 | 0.000501 | 0.000621 |
| 2609.00625v1 | mupdfng | sequential | miss | 390 | 84.456062 | 784.885960 | 829.999028 |
| 2609.00625v1 | poppler | first_page | miss | 30 | 502.540627 | 508.277102 | 530.641912 |
| 2609.00625v1 | poppler | random | hit | 420 | 0.000240 | 0.004987 | 0.096996 |
| 2609.00625v1 | poppler | revisit | hit | 420 | 0.000231 | 0.000251 | 0.000541 |
| 2609.00625v1 | poppler | sequential | miss | 390 | 189.997946 | 2164.428444 | 2215.408727 |
| 2609.09123v1 | mupdfng | first_page | miss | 30 | 31.927163 | 32.760430 | 32.781730 |
| 2609.09123v1 | mupdfng | random | hit | 537 | 0.000391 | 0.007962 | 0.010846 |
| 2609.09123v1 | mupdfng | random | miss | 63 | 207.846100 | 220.103390 | 221.208937 |
| 2609.09123v1 | mupdfng | revisit | hit | 600 | 0.000240 | 0.000481 | 0.013671 |
| 2609.09123v1 | mupdfng | sequential | miss | 570 | 20.962594 | 1394.824860 | 1436.306019 |
| 2609.09123v1 | poppler | first_page | miss | 30 | 29.457597 | 31.751921 | 32.450134 |
| 2609.09123v1 | poppler | random | hit | 537 | 0.000410 | 0.007492 | 0.118839 |
| 2609.09123v1 | poppler | random | miss | 63 | 802.825537 | 1000.900694 | 1028.029233 |
| 2609.09123v1 | poppler | revisit | hit | 600 | 0.000250 | 0.000481 | 0.109846 |
| 2609.09123v1 | poppler | sequential | miss | 570 | 33.614307 | 1429.491474 | 1491.835634 |
| 2610.26067v1 | mupdfng | first_page | miss | 30 | 42.615609 | 45.189206 | 46.712616 |
| 2610.26067v1 | mupdfng | random | hit | 480 | 0.000361 | 0.004036 | 0.009474 |
| 2610.26067v1 | mupdfng | revisit | hit | 480 | 0.000240 | 0.000481 | 0.002674 |
| 2610.26067v1 | mupdfng | sequential | miss | 450 | 94.737180 | 691.461437 | 743.047314 |
| 2610.26067v1 | poppler | first_page | miss | 30 | 42.337288 | 44.458605 | 44.591016 |
| 2610.26067v1 | poppler | random | hit | 480 | 0.000241 | 0.004286 | 0.014933 |
| 2610.26067v1 | poppler | revisit | hit | 480 | 0.000240 | 0.000271 | 0.000530 |
| 2610.26067v1 | poppler | sequential | miss | 450 | 345.527991 | 3023.874712 | 3112.372522 |
| 2312.00752v2 | mupdfng | first_page | miss | 30 | 76.742089 | 80.713377 | 81.482915 |
| 2312.00752v2 | mupdfng | random | hit | 409 | 0.000551 | 0.009224 | 0.020211 |
| 2312.00752v2 | mupdfng | random | miss | 191 | 25.413840 | 30.567848 | 35.782598 |
| 2312.00752v2 | mupdfng | revisit | hit | 600 | 0.000401 | 0.000581 | 0.011508 |
| 2312.00752v2 | mupdfng | sequential | miss | 570 | 28.852878 | 36.012171 | 46.491918 |
| 2312.00752v2 | poppler | first_page | miss | 30 | 55.691744 | 57.086012 | 57.713170 |
| 2312.00752v2 | poppler | random | hit | 409 | 0.000461 | 0.007932 | 0.028283 |
| 2312.00752v2 | poppler | random | miss | 191 | 44.592106 | 54.853081 | 60.391703 |
| 2312.00752v2 | poppler | revisit | hit | 600 | 0.000270 | 0.000541 | 0.008022 |
| 2312.00752v2 | poppler | sequential | miss | 570 | 50.327520 | 54.793402 | 73.599818 |
| 2307.03109v9 | mupdfng | first_page | miss | 30 | 52.777019 | 56.825120 | 67.235269 |
| 2307.03109v9 | mupdfng | random | hit | 351 | 0.000591 | 0.009224 | 0.010045 |
| 2307.03109v9 | mupdfng | random | miss | 249 | 28.507589 | 36.985125 | 46.901180 |
| 2307.03109v9 | mupdfng | revisit | hit | 600 | 0.000381 | 0.000561 | 0.011067 |
| 2307.03109v9 | mupdfng | sequential | miss | 570 | 25.045631 | 51.604305 | 66.739134 |
| 2307.03109v9 | poppler | first_page | miss | 30 | 53.306542 | 61.535900 | 70.179637 |
| 2307.03109v9 | poppler | random | hit | 351 | 0.000571 | 0.008102 | 0.028534 |
| 2307.03109v9 | poppler | random | miss | 249 | 48.363379 | 54.647478 | 59.209832 |
| 2307.03109v9 | poppler | revisit | hit | 600 | 0.000411 | 0.000531 | 0.019630 |
| 2307.03109v9 | poppler | sequential | miss | 570 | 44.833266 | 57.100437 | 75.206057 |

## Environment

```json
{
  "platform": "Linux-7.0.0-1019-azure-x86_64-with-glibc2.44",
  "machine": "x86_64",
  "cpu_model": "AMD EPYC 9V74 80-Core Processor",
  "logical_cpus": 4,
  "available_cpus": 4,
  "python": "3.14.10",
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
  "protocol_sha256": "8843c572bb81fb24fee3e7877bad432760f205c338332af06e938d80950fa7b2",
  "mupdf_package": null,
  "source_commit": "0c2aca4cd5ed25f310e30c3a332f92971e2e18bc",
  "source_dirty": false,
  "benchmark_commit": "2620955b12179d2034905908b8be36c463cf69d3",
  "benchmark_dirty": false,
  "runner_image": "local",
  "runner_image_version": "local",
  "container_image": "archlinux:latest",
  "versions": {
    "poppler": "26.10.0",
    "okular": "okular 26.08.3",
    "compiler": "clang version 23.1.5\nTarget: x86_64-pc-linux-gnu\nThread model: posix\nInstalledDir: /usr/bin",
    "mupdf": "1.28.6"
  }
}
```

## Interpretation limits

Paired trials reduce host-speed noise, but CPU architectures can favor the backends differently. Graph lines group runs by CPU model and Poppler version; other environment and benchmark settings remain recorded in the reports. Bootstrap intervals resample whole paired trial scores; repeated pages are not independent samples of all PDFs. This is an offscreen rendering benchmark, not a GUI scrolling, memory, or visual-fidelity measurement. OS file caches are warm/uncontrolled. No performance merge gate is applied.

Okular warning-bearing trials: 150. See `summary.json` and `samples.jsonl.gz` for details.

Artifacts: [summary](summary.json), [raw trials](samples.jsonl.gz), [corpus manifest](corpus-manifest.json).

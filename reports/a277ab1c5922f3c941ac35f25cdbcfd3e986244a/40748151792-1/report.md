# PDF backend benchmark

Source commit: [a277ab1c5922f3c941ac35f25cdbcfd3e986244a](https://github.com/l4rzy/okular-mupdf-ng/commit/a277ab1c5922f3c941ac35f25cdbcfd3e986244a).

Benchmark commit: `8948f7cbf4db9cfd47cbc9b47d32f03dcfbb1774`.

Run: [40748151792-1](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/40748151792), 2026-10-28T19:22:01.000736+00:00.

**Median paired rendering ratio: 2.229×** (95% bootstrap interval 2.221–2.236×).

Ratio = Poppler time / MuPDF-NG time; above 1 favors MuPDF-NG. Each trial uses the geometric mean of document ratios, giving each PDF equal weight. The headline is the median of those trial scores. The primary workload sums first-page and sequential-render request times, excluding document opening and worker startup. The worker stays alive for all requests in a trial.

MuPDF-NG uses **Relaxed sandbox enforcement**: available worker protections remain active, and incomplete host hardening does not block document opening.

300 successful backend trials; 30 pairs per PDF; series `d2c307ea82a68627`.

## Per-document results

Times are medians in milliseconds. Ratios are medians of paired ratios, not ratios of medians.

| PDF | Pages | Render ratio | MuPDF-NG render batch | Poppler render batch | MuPDF-NG open → first page | Poppler open → first page |
|---|---:|---:|---:|---:|---:|---:|
| 2609.00625v1 | 14 | 2.473× | 2847.755 | 7041.825 | 251.982 | 626.042 |
| 2609.09123v1 | 24 | 1.839× | 2892.367 | 5322.183 | 67.026 | 47.322 |
| 2610.26067v1 | 16 | 4.057× | 3296.165 | 13361.604 | 82.047 | 63.652 |
| 2312.00752v2 | 36 | 1.727× | 756.395 | 1301.423 | 117.986 | 79.319 |
| 2307.03109v9 | 45 | 1.712× | 669.839 | 1149.121 | 93.180 | 81.570 |

## Individual requests

Times are milliseconds; p95 is shown only for at least 20 samples. Cache hits are separate.

| PDF | Backend | Phase | Cache | N | Median | p95 | Maximum |
|---|---|---|---|---:|---:|---:|---:|
| 2609.00625v1 | mupdfng | first_page | miss | 30 | 227.141486 | 253.015479 | 266.370342 |
| 2609.00625v1 | mupdfng | random | hit | 420 | 0.000642 | 0.006282 | 0.009057 |
| 2609.00625v1 | mupdfng | revisit | hit | 420 | 0.000371 | 0.000782 | 0.001583 |
| 2609.00625v1 | mupdfng | sequential | miss | 390 | 98.621491 | 947.280745 | 984.898608 |
| 2609.00625v1 | poppler | first_page | miss | 30 | 616.286897 | 620.041013 | 620.449824 |
| 2609.00625v1 | poppler | random | hit | 420 | 0.000471 | 0.006412 | 0.022172 |
| 2609.00625v1 | poppler | revisit | hit | 420 | 0.000461 | 0.000702 | 0.001042 |
| 2609.00625v1 | poppler | sequential | miss | 390 | 238.988846 | 2639.692268 | 2756.858633 |
| 2609.09123v1 | mupdfng | first_page | miss | 30 | 39.963127 | 41.865586 | 42.137774 |
| 2609.09123v1 | mupdfng | random | hit | 537 | 0.000631 | 0.008156 | 0.098684 |
| 2609.09123v1 | mupdfng | random | miss | 63 | 238.059196 | 258.205982 | 267.935923 |
| 2609.09123v1 | mupdfng | revisit | hit | 600 | 0.000381 | 0.000822 | 0.008937 |
| 2609.09123v1 | mupdfng | sequential | miss | 570 | 25.106655 | 1667.640236 | 1799.395244 |
| 2609.09123v1 | poppler | first_page | miss | 30 | 39.652697 | 41.492835 | 42.598914 |
| 2609.09123v1 | poppler | random | hit | 537 | 0.000601 | 0.007925 | 0.120476 |
| 2609.09123v1 | poppler | random | miss | 63 | 1065.677604 | 1353.551656 | 1400.661396 |
| 2609.09123v1 | poppler | revisit | hit | 600 | 0.000456 | 0.000701 | 0.010640 |
| 2609.09123v1 | poppler | sequential | miss | 570 | 45.780194 | 1696.225541 | 1814.228751 |
| 2610.26067v1 | mupdfng | first_page | miss | 30 | 54.469255 | 67.788330 | 76.917948 |
| 2610.26067v1 | mupdfng | random | hit | 480 | 0.000661 | 0.007104 | 0.010951 |
| 2610.26067v1 | mupdfng | revisit | hit | 480 | 0.000371 | 0.000782 | 0.003576 |
| 2610.26067v1 | mupdfng | sequential | miss | 450 | 112.253647 | 792.360061 | 831.387870 |
| 2610.26067v1 | poppler | first_page | miss | 30 | 55.359167 | 56.709032 | 57.214541 |
| 2610.26067v1 | poppler | random | hit | 480 | 0.000451 | 0.006622 | 0.029386 |
| 2610.26067v1 | poppler | revisit | hit | 480 | 0.000436 | 0.000501 | 0.000842 |
| 2610.26067v1 | poppler | sequential | miss | 450 | 459.632772 | 3919.095147 | 4034.625458 |
| 2312.00752v2 | mupdfng | first_page | miss | 30 | 93.643840 | 96.137714 | 99.242721 |
| 2312.00752v2 | mupdfng | random | hit | 409 | 0.000821 | 0.008596 | 0.029436 |
| 2312.00752v2 | mupdfng | random | miss | 191 | 30.142913 | 37.348906 | 45.405645 |
| 2312.00752v2 | mupdfng | revisit | hit | 600 | 0.000631 | 0.000942 | 0.020189 |
| 2312.00752v2 | mupdfng | sequential | miss | 570 | 34.694153 | 42.534902 | 49.995517 |
| 2312.00752v2 | poppler | first_page | miss | 30 | 71.366815 | 94.569439 | 109.899261 |
| 2312.00752v2 | poppler | random | hit | 409 | 0.000722 | 0.008196 | 0.103364 |
| 2312.00752v2 | poppler | random | miss | 191 | 57.161792 | 70.152492 | 72.200172 |
| 2312.00752v2 | poppler | revisit | hit | 600 | 0.000481 | 0.000782 | 0.008326 |
| 2312.00752v2 | poppler | sequential | miss | 570 | 65.504960 | 71.732303 | 99.228164 |
| 2307.03109v9 | mupdfng | first_page | miss | 30 | 63.790099 | 69.404519 | 73.178938 |
| 2307.03109v9 | mupdfng | random | hit | 351 | 0.001012 | 0.008396 | 0.050305 |
| 2307.03109v9 | mupdfng | random | miss | 249 | 33.656002 | 44.181521 | 52.647535 |
| 2307.03109v9 | mupdfng | revisit | hit | 600 | 0.000471 | 0.000892 | 0.008647 |
| 2307.03109v9 | mupdfng | sequential | miss | 570 | 29.312470 | 61.342597 | 73.061202 |
| 2307.03109v9 | poppler | first_page | miss | 30 | 68.405654 | 75.540547 | 81.271168 |
| 2307.03109v9 | poppler | random | hit | 351 | 0.000802 | 0.008115 | 0.025557 |
| 2307.03109v9 | poppler | random | miss | 249 | 61.509659 | 69.958450 | 79.351510 |
| 2307.03109v9 | poppler | revisit | hit | 600 | 0.000591 | 0.000821 | 0.008055 |
| 2307.03109v9 | poppler | sequential | miss | 570 | 57.596535 | 74.875130 | 102.377759 |

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
  "source_commit": "a277ab1c5922f3c941ac35f25cdbcfd3e986244a",
  "source_dirty": false,
  "benchmark_commit": "8948f7cbf4db9cfd47cbc9b47d32f03dcfbb1774",
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

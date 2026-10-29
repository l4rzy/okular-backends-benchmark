# PDF backend benchmark

Source commit: [901e4c7046a271c447e827f89e52120a71f249fa](https://github.com/l4rzy/okular-mupdf-ng/commit/901e4c7046a271c447e827f89e52120a71f249fa).

Benchmark commit: `bcb69b013f8220b577edae567a5a138308f22fe5`.

Run: [40823113502-1](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/40823113502), 2026-10-29T05:39:29.688475+00:00.

**Median paired rendering ratio: 2.147×** (95% bootstrap interval 2.132–2.156×).

Ratio = Poppler time / MuPDF-NG time; above 1 favors MuPDF-NG. Each trial uses the geometric mean of document ratios, giving each PDF equal weight. The headline is the median of those trial scores. The primary workload sums first-page and sequential-render request times, excluding document opening and worker startup. The worker stays alive for all requests in a trial.

MuPDF-NG uses **Relaxed sandbox enforcement**: available worker protections remain active, and incomplete host hardening does not block document opening.

200 successful backend trials; 20 pairs per PDF; series `e48b2b7b269a9b08`.

## Per-document results

Times are medians in milliseconds. Ratios are medians of paired ratios, not ratios of medians.

| PDF | Pages | Render ratio | MuPDF-NG render batch | Poppler render batch | MuPDF-NG open → first page | Poppler open → first page |
|---|---:|---:|---:|---:|---:|---:|
| 2609.00625v1 | 14 | 2.271× | 1835.270 | 4156.794 | 167.141 | 359.613 |
| 2609.09123v1 | 24 | 1.766× | 1773.563 | 3124.880 | 43.244 | 27.511 |
| 2610.26067v1 | 16 | 3.690× | 2071.501 | 7682.260 | 51.316 | 38.444 |
| 2312.00752v2 | 36 | 1.778× | 424.825 | 756.498 | 72.661 | 47.547 |
| 2307.03109v9 | 45 | 1.744× | 380.138 | 664.356 | 58.901 | 49.508 |

## Individual requests

Times are milliseconds; p95 is shown only for at least 20 samples. Cache hits are separate.

| PDF | Backend | Phase | Cache | N | Median | p95 | Maximum |
|---|---|---|---|---:|---:|---:|---:|
| 2609.00625v1 | mupdfng | first_page | miss | 20 | 148.681397 | 152.653398 | 154.992430 |
| 2609.00625v1 | mupdfng | random | hit | 280 | 0.000231 | 0.006340 | 0.011317 |
| 2609.00625v1 | mupdfng | revisit | hit | 280 | 0.000200 | 0.000320 | 0.002043 |
| 2609.00625v1 | mupdfng | sequential | miss | 260 | 63.332638 | 607.275266 | 694.413989 |
| 2609.00625v1 | poppler | first_page | miss | 20 | 353.538318 | 363.188170 | 375.337823 |
| 2609.00625v1 | poppler | random | hit | 280 | 0.000201 | 0.006239 | 0.120001 |
| 2609.00625v1 | poppler | revisit | hit | 280 | 0.000200 | 0.000211 | 0.000231 |
| 2609.00625v1 | poppler | sequential | miss | 260 | 144.241442 | 1543.957030 | 1669.848480 |
| 2609.09123v1 | mupdfng | first_page | miss | 20 | 24.237292 | 25.086048 | 25.132249 |
| 2609.09123v1 | mupdfng | random | hit | 356 | 0.000301 | 0.009885 | 0.108041 |
| 2609.09123v1 | mupdfng | random | miss | 44 | 141.684166 | 154.594040 | 156.473273 |
| 2609.09123v1 | mupdfng | revisit | hit | 400 | 0.000200 | 0.000331 | 0.011497 |
| 2609.09123v1 | mupdfng | sequential | miss | 380 | 13.873764 | 1021.544200 | 1080.748532 |
| 2609.09123v1 | poppler | first_page | miss | 20 | 22.674414 | 23.893968 | 32.775690 |
| 2609.09123v1 | poppler | random | hit | 356 | 0.000291 | 0.009495 | 0.123724 |
| 2609.09123v1 | poppler | random | miss | 44 | 621.776879 | 796.191606 | 841.876437 |
| 2609.09123v1 | poppler | revisit | hit | 400 | 0.000301 | 0.000341 | 0.010336 |
| 2609.09123v1 | poppler | sequential | miss | 380 | 25.847031 | 1052.910246 | 1246.202741 |
| 2610.26067v1 | mupdfng | first_page | miss | 20 | 32.172554 | 34.383068 | 41.392885 |
| 2610.26067v1 | mupdfng | random | hit | 320 | 0.000211 | 0.002814 | 0.011627 |
| 2610.26067v1 | mupdfng | revisit | hit | 320 | 0.000200 | 0.000211 | 0.000401 |
| 2610.26067v1 | mupdfng | sequential | miss | 300 | 69.322147 | 506.127223 | 539.455511 |
| 2610.26067v1 | poppler | first_page | miss | 20 | 32.954495 | 34.266343 | 37.419829 |
| 2610.26067v1 | poppler | random | hit | 320 | 0.000201 | 0.002664 | 0.010335 |
| 2610.26067v1 | poppler | revisit | hit | 320 | 0.000200 | 0.000211 | 0.000241 |
| 2610.26067v1 | poppler | sequential | miss | 300 | 256.854574 | 2303.394354 | 2388.032723 |
| 2312.00752v2 | mupdfng | first_page | miss | 20 | 56.196776 | 58.799138 | 60.855645 |
| 2312.00752v2 | mupdfng | random | hit | 283 | 0.000350 | 0.003456 | 0.005098 |
| 2312.00752v2 | mupdfng | random | miss | 117 | 16.435802 | 21.851048 | 25.923004 |
| 2312.00752v2 | mupdfng | revisit | hit | 400 | 0.000206 | 0.000351 | 0.002774 |
| 2312.00752v2 | mupdfng | sequential | miss | 380 | 18.655355 | 25.126225 | 34.493442 |
| 2312.00752v2 | poppler | first_page | miss | 20 | 42.530417 | 43.114605 | 43.405285 |
| 2312.00752v2 | poppler | random | hit | 283 | 0.000340 | 0.003205 | 0.006851 |
| 2312.00752v2 | poppler | random | miss | 117 | 33.029909 | 41.178728 | 50.999579 |
| 2312.00752v2 | poppler | revisit | hit | 400 | 0.000260 | 0.000361 | 0.011467 |
| 2312.00752v2 | poppler | sequential | miss | 380 | 37.950503 | 41.412043 | 45.339075 |
| 2307.03109v9 | mupdfng | first_page | miss | 20 | 38.618911 | 39.347253 | 40.142044 |
| 2307.03109v9 | mupdfng | random | hit | 241 | 0.000510 | 0.003726 | 0.005018 |
| 2307.03109v9 | mupdfng | random | miss | 159 | 19.228228 | 22.519644 | 25.477913 |
| 2307.03109v9 | mupdfng | revisit | hit | 400 | 0.000310 | 0.000510 | 0.003936 |
| 2307.03109v9 | mupdfng | sequential | miss | 380 | 15.863952 | 37.568125 | 58.671894 |
| 2307.03109v9 | poppler | first_page | miss | 20 | 41.160010 | 42.548015 | 54.636555 |
| 2307.03109v9 | poppler | random | hit | 241 | 0.000391 | 0.003525 | 0.013411 |
| 2307.03109v9 | poppler | random | miss | 159 | 36.522665 | 40.651828 | 45.661244 |
| 2307.03109v9 | poppler | revisit | hit | 400 | 0.000310 | 0.000410 | 0.008142 |
| 2307.03109v9 | poppler | sequential | miss | 380 | 33.397908 | 42.081482 | 49.026781 |

## Environment

```json
{
  "platform": "Linux-7.0.0-1017-azure-x86_64-with-glibc2.44",
  "machine": "x86_64",
  "cpu_model": "AMD EPYC 9V45 96-Core Processor",
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
  "source_commit": "901e4c7046a271c447e827f89e52120a71f249fa",
  "source_dirty": false,
  "benchmark_commit": "bcb69b013f8220b577edae567a5a138308f22fe5",
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

Okular warning-bearing trials: 100. See `summary.json` and `samples.jsonl.gz` for details.

Artifacts: [summary](summary.json), [raw trials](samples.jsonl.gz), [corpus manifest](corpus-manifest.json).

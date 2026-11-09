# PDF backend benchmark

Source commit: [5173bb41e2547a625eb14c1428682a51abf8f31c](https://github.com/l4rzy/okular-mupdf-ng/commit/5173bb41e2547a625eb14c1428682a51abf8f31c).

Benchmark commit: `117fdb5c22e146519b3bf1be985ae03324702f53`.

Run: [42630933393-1](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/42630933393), 2026-11-09T14:30:47.632079+00:00.

**Median paired rendering ratio: 2.098×** (95% bootstrap interval 2.094–2.102×).

Ratio = Poppler time / MuPDF-NG time; above 1 favors MuPDF-NG. Each trial uses the geometric mean of document ratios, giving each PDF equal weight. The headline is the median of those trial scores. The primary workload sums first-page and sequential-render request times, excluding document opening and worker startup. The worker stays alive for all requests in a trial.

MuPDF-NG uses **Relaxed sandbox enforcement**: available worker protections remain active, and incomplete host hardening does not block document opening.

300 successful backend trials; 30 pairs per PDF; series `9777caba301b0a12`.

## Per-document results

Times are medians in milliseconds. Ratios are medians of paired ratios, not ratios of medians.

| PDF | Pages | Render ratio | MuPDF-NG render batch | Poppler render batch | MuPDF-NG open → first page | Poppler open → first page |
|---|---:|---:|---:|---:|---:|---:|
| 2609.00625v1 | 14 | 2.383× | 2390.694 | 5692.928 | 216.351 | 507.678 |
| 2609.09123v1 | 24 | 1.699× | 2415.995 | 4111.458 | 54.697 | 35.656 |
| 2610.26067v1 | 16 | 3.700× | 2783.230 | 10284.616 | 65.961 | 48.450 |
| 2312.00752v2 | 36 | 1.686× | 584.143 | 981.153 | 95.638 | 60.715 |
| 2307.03109v9 | 45 | 1.628× | 527.876 | 855.962 | 76.215 | 62.515 |

## Individual requests

Times are milliseconds; p95 is shown only for at least 20 samples. Cache hits are separate.

| PDF | Backend | Phase | Cache | N | Median | p95 | Maximum |
|---|---|---|---|---:|---:|---:|---:|
| 2609.00625v1 | mupdfng | first_page | miss | 30 | 194.502806 | 210.748773 | 215.805611 |
| 2609.00625v1 | mupdfng | random | hit | 420 | 0.000391 | 0.006741 | 0.011678 |
| 2609.00625v1 | mupdfng | revisit | hit | 420 | 0.000251 | 0.000501 | 0.020781 |
| 2609.00625v1 | mupdfng | sequential | miss | 390 | 84.801755 | 796.268823 | 841.142533 |
| 2609.00625v1 | poppler | first_page | miss | 30 | 498.121248 | 508.748504 | 517.242400 |
| 2609.00625v1 | poppler | random | hit | 420 | 0.000251 | 0.006139 | 0.028162 |
| 2609.00625v1 | poppler | revisit | hit | 420 | 0.000241 | 0.000271 | 0.019840 |
| 2609.00625v1 | poppler | sequential | miss | 390 | 190.169350 | 2166.797616 | 2217.592319 |
| 2609.09123v1 | mupdfng | first_page | miss | 30 | 31.698231 | 33.867414 | 36.273856 |
| 2609.09123v1 | mupdfng | random | hit | 537 | 0.000410 | 0.007932 | 0.010586 |
| 2609.09123v1 | mupdfng | random | miss | 63 | 205.691825 | 218.275531 | 219.722107 |
| 2609.09123v1 | mupdfng | revisit | hit | 600 | 0.000251 | 0.000510 | 0.008103 |
| 2609.09123v1 | mupdfng | sequential | miss | 570 | 20.637791 | 1392.692132 | 1426.491668 |
| 2609.09123v1 | poppler | first_page | miss | 30 | 29.655092 | 30.805242 | 30.949641 |
| 2609.09123v1 | poppler | random | hit | 537 | 0.000281 | 0.007401 | 0.117717 |
| 2609.09123v1 | poppler | random | miss | 63 | 815.427405 | 1001.833827 | 1022.389510 |
| 2609.09123v1 | poppler | revisit | hit | 600 | 0.000260 | 0.000491 | 0.121833 |
| 2609.09123v1 | poppler | sequential | miss | 570 | 33.742131 | 1428.813258 | 1476.764839 |
| 2610.26067v1 | mupdfng | first_page | miss | 30 | 42.596629 | 44.283430 | 45.448559 |
| 2610.26067v1 | mupdfng | random | hit | 480 | 0.000356 | 0.003846 | 0.019960 |
| 2610.26067v1 | mupdfng | revisit | hit | 480 | 0.000241 | 0.000451 | 0.002394 |
| 2610.26067v1 | mupdfng | sequential | miss | 450 | 92.489915 | 678.998235 | 713.729257 |
| 2610.26067v1 | poppler | first_page | miss | 30 | 41.861113 | 43.779945 | 44.264924 |
| 2610.26067v1 | poppler | random | hit | 480 | 0.000250 | 0.004407 | 0.006540 |
| 2610.26067v1 | poppler | revisit | hit | 480 | 0.000250 | 0.000270 | 0.000471 |
| 2610.26067v1 | poppler | sequential | miss | 450 | 343.726140 | 3017.412470 | 3066.437041 |
| 2312.00752v2 | mupdfng | first_page | miss | 30 | 75.435430 | 78.178799 | 88.289220 |
| 2312.00752v2 | mupdfng | random | hit | 409 | 0.000531 | 0.006140 | 0.009965 |
| 2312.00752v2 | mupdfng | random | miss | 191 | 23.147838 | 28.394763 | 36.749538 |
| 2312.00752v2 | mupdfng | revisit | hit | 600 | 0.000271 | 0.000571 | 0.013140 |
| 2312.00752v2 | mupdfng | sequential | miss | 570 | 26.095637 | 34.054229 | 41.529080 |
| 2312.00752v2 | poppler | first_page | miss | 30 | 54.501593 | 56.131358 | 60.438624 |
| 2312.00752v2 | poppler | random | hit | 409 | 0.000461 | 0.006279 | 0.020892 |
| 2312.00752v2 | poppler | random | miss | 191 | 43.305450 | 52.800268 | 61.412506 |
| 2312.00752v2 | poppler | revisit | hit | 600 | 0.000280 | 0.000491 | 0.005849 |
| 2312.00752v2 | poppler | sequential | miss | 570 | 49.297331 | 53.791663 | 70.944768 |
| 2307.03109v9 | mupdfng | first_page | miss | 30 | 51.090905 | 52.870374 | 59.007016 |
| 2307.03109v9 | mupdfng | random | hit | 351 | 0.000621 | 0.006540 | 0.018077 |
| 2307.03109v9 | mupdfng | random | miss | 249 | 26.239883 | 34.253197 | 36.697856 |
| 2307.03109v9 | mupdfng | revisit | hit | 600 | 0.000410 | 0.000600 | 0.007381 |
| 2307.03109v9 | mupdfng | sequential | miss | 570 | 22.554743 | 49.400684 | 58.670174 |
| 2307.03109v9 | poppler | first_page | miss | 30 | 51.997907 | 53.820549 | 55.534171 |
| 2307.03109v9 | poppler | random | hit | 351 | 0.000580 | 0.006519 | 0.007982 |
| 2307.03109v9 | poppler | random | miss | 249 | 46.947081 | 53.758918 | 63.309604 |
| 2307.03109v9 | poppler | revisit | hit | 600 | 0.000411 | 0.000521 | 0.006039 |
| 2307.03109v9 | poppler | sequential | miss | 570 | 43.446762 | 55.658277 | 60.620015 |

## Environment

```json
{
  "platform": "Linux-7.0.0-1019-azure-x86_64-with-glibc2.44",
  "machine": "x86_64",
  "cpu_model": "AMD EPYC 9V74 80-Core Processor",
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
  "source_commit": "5173bb41e2547a625eb14c1428682a51abf8f31c",
  "source_dirty": false,
  "benchmark_commit": "117fdb5c22e146519b3bf1be985ae03324702f53",
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

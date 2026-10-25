# PDF backend benchmark

Source commit: [fee75c813b7455a2607915a7115f74ddc5972d59](https://github.com/l4rzy/okular-mupdf-ng/commit/fee75c813b7455a2607915a7115f74ddc5972d59).

Benchmark commit: `0321bd6d907626558e967ee9f794290fca92ec85`.

Run: [40203127246-1](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/40203127246), 2026-10-25T15:03:34.922772+00:00.

**Median paired rendering ratio: 2.260×** (95% bootstrap interval 2.257–2.263×).

Ratio = Poppler time / MuPDF-NG time; above 1 favors MuPDF-NG. Each trial uses the geometric mean of document ratios, giving each PDF equal weight. The headline is the median of those trial scores. The primary workload sums first-page and sequential-render request times, excluding document opening and worker startup. The worker stays alive for all requests in a trial.

MuPDF-NG uses **Relaxed sandbox enforcement**: available worker protections remain active, and incomplete host hardening does not block document opening.

300 successful backend trials; 30 pairs per PDF; series `2c1bb0dcf088a9e7`.

## Per-document results

Times are medians in milliseconds. Ratios are medians of paired ratios, not ratios of medians.

| PDF | Pages | Render ratio | MuPDF-NG render batch | Poppler render batch | MuPDF-NG open → first page | Poppler open → first page |
|---|---:|---:|---:|---:|---:|---:|
| 2609.00625v1 | 14 | 2.539× | 2236.102 | 5684.779 | 198.116 | 509.480 |
| 2609.09123v1 | 24 | 1.685× | 2380.734 | 4013.641 | 47.950 | 31.914 |
| 2610.26067v1 | 16 | 4.032× | 2584.045 | 10416.020 | 58.292 | 44.085 |
| 2312.00752v2 | 36 | 1.833× | 505.444 | 926.867 | 87.841 | 55.490 |
| 2307.03109v9 | 45 | 1.870× | 429.581 | 802.498 | 68.340 | 56.490 |

## Individual requests

Times are milliseconds; p95 is shown only for at least 20 samples. Cache hits are separate.

| PDF | Backend | Phase | Cache | N | Median | p95 | Maximum |
|---|---|---|---|---:|---:|---:|---:|
| 2609.00625v1 | mupdfng | first_page | miss | 30 | 178.679131 | 180.462108 | 182.515850 |
| 2609.00625v1 | mupdfng | random | hit | 420 | 0.000380 | 0.005979 | 0.010665 |
| 2609.00625v1 | mupdfng | revisit | hit | 420 | 0.000271 | 0.000530 | 0.000661 |
| 2609.00625v1 | mupdfng | sequential | miss | 390 | 78.896676 | 769.815886 | 815.215286 |
| 2609.00625v1 | poppler | first_page | miss | 30 | 501.645858 | 510.813156 | 529.447482 |
| 2609.00625v1 | poppler | random | hit | 420 | 0.000271 | 0.005168 | 0.008703 |
| 2609.00625v1 | poppler | revisit | hit | 420 | 0.000270 | 0.000301 | 0.015413 |
| 2609.00625v1 | poppler | sequential | miss | 390 | 187.392711 | 2200.841537 | 2257.376354 |
| 2609.09123v1 | mupdfng | first_page | miss | 30 | 26.561025 | 27.445567 | 29.044068 |
| 2609.09123v1 | mupdfng | random | hit | 537 | 0.000451 | 0.008532 | 0.015764 |
| 2609.09123v1 | mupdfng | random | miss | 63 | 199.859012 | 217.072579 | 218.198711 |
| 2609.09123v1 | mupdfng | revisit | hit | 600 | 0.000280 | 0.000541 | 0.008823 |
| 2609.09123v1 | mupdfng | sequential | miss | 570 | 15.584819 | 1449.104827 | 1519.367005 |
| 2609.09123v1 | poppler | first_page | miss | 30 | 26.815789 | 28.136193 | 28.225494 |
| 2609.09123v1 | poppler | random | hit | 537 | 0.000491 | 0.008963 | 0.162000 |
| 2609.09123v1 | poppler | random | miss | 63 | 789.266290 | 997.785021 | 1021.262897 |
| 2609.09123v1 | poppler | revisit | hit | 600 | 0.000280 | 0.000550 | 0.091515 |
| 2609.09123v1 | poppler | sequential | miss | 570 | 30.934679 | 1374.074328 | 1439.998991 |
| 2610.26067v1 | mupdfng | first_page | miss | 30 | 36.633562 | 37.787507 | 38.797614 |
| 2610.26067v1 | mupdfng | random | hit | 480 | 0.000300 | 0.006279 | 0.010446 |
| 2610.26067v1 | mupdfng | revisit | hit | 480 | 0.000270 | 0.000301 | 0.012298 |
| 2610.26067v1 | mupdfng | sequential | miss | 450 | 85.640388 | 648.802987 | 660.698994 |
| 2610.26067v1 | poppler | first_page | miss | 30 | 38.617279 | 39.777512 | 39.884635 |
| 2610.26067v1 | poppler | random | hit | 480 | 0.000271 | 0.005438 | 0.009184 |
| 2610.26067v1 | poppler | revisit | hit | 480 | 0.000270 | 0.000301 | 0.000661 |
| 2610.26067v1 | poppler | sequential | miss | 450 | 347.445743 | 3078.895682 | 3282.962643 |
| 2312.00752v2 | mupdfng | first_page | miss | 30 | 69.110714 | 70.397568 | 70.799807 |
| 2312.00752v2 | mupdfng | random | hit | 409 | 0.000550 | 0.009263 | 0.076073 |
| 2312.00752v2 | mupdfng | random | miss | 191 | 19.534626 | 24.585091 | 28.290183 |
| 2312.00752v2 | mupdfng | revisit | hit | 600 | 0.000291 | 0.000621 | 0.010365 |
| 2312.00752v2 | mupdfng | sequential | miss | 570 | 22.439684 | 29.435500 | 33.258392 |
| 2312.00752v2 | poppler | first_page | miss | 30 | 50.170745 | 51.111614 | 78.085872 |
| 2312.00752v2 | poppler | random | hit | 409 | 0.000491 | 0.007291 | 0.008713 |
| 2312.00752v2 | poppler | random | miss | 191 | 41.077785 | 50.484975 | 52.131488 |
| 2312.00752v2 | poppler | revisit | hit | 600 | 0.000290 | 0.000571 | 0.008092 |
| 2312.00752v2 | poppler | sequential | miss | 570 | 46.874535 | 51.079920 | 67.418830 |
| 2307.03109v9 | mupdfng | first_page | miss | 30 | 44.470257 | 45.107587 | 45.214230 |
| 2307.03109v9 | mupdfng | random | hit | 351 | 0.000651 | 0.009784 | 0.017666 |
| 2307.03109v9 | mupdfng | random | miss | 249 | 21.869351 | 29.744486 | 33.601930 |
| 2307.03109v9 | mupdfng | revisit | hit | 600 | 0.000430 | 0.000601 | 0.012508 |
| 2307.03109v9 | mupdfng | sequential | miss | 570 | 18.238156 | 45.666111 | 54.243845 |
| 2307.03109v9 | poppler | first_page | miss | 30 | 47.551136 | 48.424258 | 49.901137 |
| 2307.03109v9 | poppler | random | hit | 351 | 0.000580 | 0.007741 | 0.017166 |
| 2307.03109v9 | poppler | random | miss | 249 | 43.816303 | 49.972935 | 65.688411 |
| 2307.03109v9 | poppler | revisit | hit | 600 | 0.000470 | 0.000591 | 0.020040 |
| 2307.03109v9 | poppler | sequential | miss | 570 | 40.626416 | 52.618266 | 57.661891 |

## Environment

```json
{
  "platform": "Linux-6.17.0-1022-azure-x86_64-with-glibc2.43",
  "machine": "x86_64",
  "cpu_model": "AMD EPYC 9V74 80-Core Processor",
  "logical_cpus": 4,
  "available_cpus": 4,
  "python": "3.14.4",
  "plugin_build": {
    "CMAKE_BUILD_TYPE": "Release",
    "CMAKE_CXX_COMPILER": "/usr/bin/clang++",
    "DISABLE_WORKER_SANDBOX": "OFF",
    "ENABLE_BUILD_TREE_WORKER": "ON",
    "ENABLE_LTO": "ON",
    "ENABLE_MU_DEBUG": "OFF",
    "MUPDF_CJK_FALLBACK": "droidfull",
    "MUPDF_OPTIMIZED_BUILD": "ON",
    "USE_SYSTEM_MUPDF": "OFF"
  },
  "protocol": "pdf-render-v1",
  "protocol_sha256": "517cc59f7ba6e779b7528cda6ec2b3d9ebd255dd4b5e90042525edda23b80bbf",
  "source_commit": "fee75c813b7455a2607915a7115f74ddc5972d59",
  "source_dirty": false,
  "benchmark_commit": "0321bd6d907626558e967ee9f794290fca92ec85",
  "benchmark_dirty": false,
  "runner_image": "local",
  "runner_image_version": "local",
  "container_image": "ubuntu:26.04",
  "versions": {
    "poppler": "26.01.0",
    "okular": "okular 25.12.3",
    "compiler": "Ubuntu clang version 21.1.8 (6ubuntu1)\nTarget: x86_64-pc-linux-gnu\nThread model: posix\nInstalledDir: /usr/lib/llvm-21/bin",
    "mupdf": "1.28.5"
  }
}
```

## Interpretation limits

Paired trials reduce host-speed noise, but CPU architectures can favor the backends differently. CPU, baseline binary, dependencies, corpus, harness, and settings identify separate trend series. Bootstrap intervals resample whole paired trial scores; repeated pages are not independent samples of all PDFs. This is an offscreen rendering benchmark, not a GUI scrolling, memory, or visual-fidelity measurement. OS file caches are warm/uncontrolled. No performance merge gate is applied.

Okular warning-bearing trials: 150. See `summary.json` and `samples.jsonl.gz` for details.

Artifacts: [summary](summary.json), [raw trials](samples.jsonl.gz), [corpus manifest](corpus-manifest.json).

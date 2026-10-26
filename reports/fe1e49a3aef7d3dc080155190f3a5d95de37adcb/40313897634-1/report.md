# PDF backend benchmark

Source commit: [fe1e49a3aef7d3dc080155190f3a5d95de37adcb](https://github.com/l4rzy/okular-mupdf-ng/commit/fe1e49a3aef7d3dc080155190f3a5d95de37adcb).

Benchmark commit: `8b63ddfc94a4f0c239f4f8aaa7b77b05439a76ae`.

Run: [40313897634-1](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/40313897634), 2026-10-26T11:50:09.594852+00:00.

**Median paired rendering ratio: 2.248×** (95% bootstrap interval 2.245–2.259×).

Ratio = Poppler time / MuPDF-NG time; above 1 favors MuPDF-NG. Each trial uses the geometric mean of document ratios, giving each PDF equal weight. The headline is the median of those trial scores. The primary workload sums first-page and sequential-render request times, excluding document opening and worker startup. The worker stays alive for all requests in a trial.

MuPDF-NG uses **Relaxed sandbox enforcement**: available worker protections remain active, and incomplete host hardening does not block document opening.

300 successful backend trials; 30 pairs per PDF; series `d2c307ea82a68627`.

## Per-document results

Times are medians in milliseconds. Ratios are medians of paired ratios, not ratios of medians.

| PDF | Pages | Render ratio | MuPDF-NG render batch | Poppler render batch | MuPDF-NG open → first page | Poppler open → first page |
|---|---:|---:|---:|---:|---:|---:|
| 2609.00625v1 | 14 | 2.476× | 2830.173 | 6993.950 | 253.464 | 621.990 |
| 2609.09123v1 | 24 | 1.853× | 2833.876 | 5255.528 | 63.674 | 45.904 |
| 2610.26067v1 | 16 | 4.089× | 3246.161 | 13276.212 | 78.073 | 62.131 |
| 2312.00752v2 | 36 | 1.764× | 718.556 | 1269.989 | 113.920 | 77.643 |
| 2307.03109v9 | 45 | 1.742× | 643.435 | 1120.511 | 90.620 | 80.033 |

## Individual requests

Times are milliseconds; p95 is shown only for at least 20 samples. Cache hits are separate.

| PDF | Backend | Phase | Cache | N | Median | p95 | Maximum |
|---|---|---|---|---:|---:|---:|---:|
| 2609.00625v1 | mupdfng | first_page | miss | 30 | 227.716991 | 232.696808 | 232.769772 |
| 2609.00625v1 | mupdfng | random | hit | 420 | 0.000641 | 0.005620 | 0.018524 |
| 2609.00625v1 | mupdfng | revisit | hit | 420 | 0.000351 | 0.000741 | 0.003677 |
| 2609.00625v1 | mupdfng | sequential | miss | 390 | 98.035174 | 943.117005 | 980.603919 |
| 2609.00625v1 | poppler | first_page | miss | 30 | 612.520664 | 616.339228 | 617.568945 |
| 2609.00625v1 | poppler | random | hit | 420 | 0.000451 | 0.006362 | 0.021280 |
| 2609.00625v1 | poppler | revisit | hit | 420 | 0.000431 | 0.000741 | 0.003417 |
| 2609.00625v1 | poppler | sequential | miss | 390 | 236.099604 | 2613.378351 | 2846.862666 |
| 2609.09123v1 | mupdfng | first_page | miss | 30 | 38.765961 | 40.512004 | 40.604711 |
| 2609.09123v1 | mupdfng | random | hit | 537 | 0.000592 | 0.007343 | 0.010670 |
| 2609.09123v1 | mupdfng | random | miss | 63 | 235.542401 | 252.960122 | 257.115352 |
| 2609.09123v1 | mupdfng | revisit | hit | 600 | 0.000351 | 0.000762 | 0.012663 |
| 2609.09123v1 | mupdfng | sequential | miss | 570 | 24.381213 | 1639.806771 | 1702.619797 |
| 2609.09123v1 | poppler | first_page | miss | 30 | 38.561377 | 39.638367 | 39.901701 |
| 2609.09123v1 | poppler | random | hit | 537 | 0.000631 | 0.006953 | 0.109855 |
| 2609.09123v1 | poppler | random | miss | 63 | 1086.986814 | 1367.866113 | 1370.983416 |
| 2609.09123v1 | poppler | revisit | hit | 600 | 0.000431 | 0.000742 | 0.007764 |
| 2609.09123v1 | poppler | sequential | miss | 570 | 44.605939 | 1708.765254 | 1784.203755 |
| 2610.26067v1 | mupdfng | first_page | miss | 30 | 52.948407 | 58.689697 | 69.012698 |
| 2610.26067v1 | mupdfng | random | hit | 480 | 0.000697 | 0.005460 | 0.013926 |
| 2610.26067v1 | mupdfng | revisit | hit | 480 | 0.000350 | 0.000411 | 0.003496 |
| 2610.26067v1 | mupdfng | sequential | miss | 450 | 111.869766 | 783.087790 | 840.246666 |
| 2610.26067v1 | poppler | first_page | miss | 30 | 54.132268 | 55.978596 | 60.164518 |
| 2610.26067v1 | poppler | random | hit | 480 | 0.000441 | 0.005891 | 0.012493 |
| 2610.26067v1 | poppler | revisit | hit | 480 | 0.000421 | 0.000491 | 0.001343 |
| 2610.26067v1 | poppler | sequential | miss | 450 | 454.160001 | 3900.566666 | 3964.958193 |
| 2312.00752v2 | mupdfng | first_page | miss | 30 | 92.118640 | 97.661795 | 98.231312 |
| 2312.00752v2 | mupdfng | random | hit | 409 | 0.000832 | 0.006552 | 0.025067 |
| 2312.00752v2 | mupdfng | random | miss | 191 | 28.214779 | 34.555752 | 37.437911 |
| 2312.00752v2 | mupdfng | revisit | hit | 600 | 0.000381 | 0.000871 | 0.006993 |
| 2312.00752v2 | mupdfng | sequential | miss | 570 | 32.740046 | 41.343711 | 56.471902 |
| 2312.00752v2 | poppler | first_page | miss | 30 | 70.013060 | 71.666305 | 112.375528 |
| 2312.00752v2 | poppler | random | hit | 409 | 0.000711 | 0.006893 | 0.013175 |
| 2312.00752v2 | poppler | random | miss | 191 | 55.805462 | 69.089758 | 75.270686 |
| 2312.00752v2 | poppler | revisit | hit | 600 | 0.000470 | 0.000752 | 0.006613 |
| 2312.00752v2 | poppler | sequential | miss | 570 | 63.803345 | 69.813934 | 87.986486 |
| 2307.03109v9 | mupdfng | first_page | miss | 30 | 63.049525 | 64.687408 | 65.144768 |
| 2307.03109v9 | mupdfng | random | hit | 351 | 0.000932 | 0.007214 | 0.022913 |
| 2307.03109v9 | mupdfng | random | miss | 249 | 32.064904 | 42.497594 | 48.715546 |
| 2307.03109v9 | mupdfng | revisit | hit | 600 | 0.000450 | 0.000912 | 0.008435 |
| 2307.03109v9 | mupdfng | sequential | miss | 570 | 27.751837 | 60.003164 | 73.503056 |
| 2307.03109v9 | poppler | first_page | miss | 30 | 67.151025 | 69.101639 | 76.391128 |
| 2307.03109v9 | poppler | random | hit | 351 | 0.000812 | 0.007103 | 0.014577 |
| 2307.03109v9 | poppler | random | miss | 249 | 61.224929 | 69.834131 | 117.050411 |
| 2307.03109v9 | poppler | revisit | hit | 600 | 0.000601 | 0.000862 | 0.010680 |
| 2307.03109v9 | poppler | sequential | miss | 570 | 56.803467 | 73.317481 | 119.144582 |

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
  "source_commit": "fe1e49a3aef7d3dc080155190f3a5d95de37adcb",
  "source_dirty": false,
  "benchmark_commit": "8b63ddfc94a4f0c239f4f8aaa7b77b05439a76ae",
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

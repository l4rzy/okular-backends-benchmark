# PDF backend benchmark

Source commit: [aafe97a17e70c1a69ba44a30a64f728317764be0](https://github.com/l4rzy/okular-mupdf-ng/commit/aafe97a17e70c1a69ba44a30a64f728317764be0).

Benchmark commit: `a05be3241f1ff8a13fe35559fd61a2ee9f5c8490`.

Run: [41363436621-1](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/41363436621), 2026-11-02T00:17:54.434106+00:00.

**Median paired rendering ratio: 2.236×** (95% bootstrap interval 2.233–2.242×).

Ratio = Poppler time / MuPDF-NG time; above 1 favors MuPDF-NG. Each trial uses the geometric mean of document ratios, giving each PDF equal weight. The headline is the median of those trial scores. The primary workload sums first-page and sequential-render request times, excluding document opening and worker startup. The worker stays alive for all requests in a trial.

MuPDF-NG uses **Relaxed sandbox enforcement**: available worker protections remain active, and incomplete host hardening does not block document opening.

300 successful backend trials; 30 pairs per PDF; series `d2c307ea82a68627`.

## Per-document results

Times are medians in milliseconds. Ratios are medians of paired ratios, not ratios of medians.

| PDF | Pages | Render ratio | MuPDF-NG render batch | Poppler render batch | MuPDF-NG open → first page | Poppler open → first page |
|---|---:|---:|---:|---:|---:|---:|
| 2609.00625v1 | 14 | 2.434× | 2873.142 | 6981.134 | 252.049 | 622.980 |
| 2609.09123v1 | 24 | 1.840× | 2855.558 | 5248.812 | 65.540 | 45.621 |
| 2610.26067v1 | 16 | 4.007× | 3310.053 | 13260.263 | 81.153 | 62.555 |
| 2312.00752v2 | 36 | 1.785× | 717.440 | 1276.800 | 115.872 | 77.530 |
| 2307.03109v9 | 45 | 1.747× | 648.493 | 1131.458 | 93.015 | 80.453 |

## Individual requests

Times are milliseconds; p95 is shown only for at least 20 samples. Cache hits are separate.

| PDF | Backend | Phase | Cache | N | Median | p95 | Maximum |
|---|---|---|---|---:|---:|---:|---:|
| 2609.00625v1 | mupdfng | first_page | miss | 30 | 226.529862 | 229.557032 | 251.558170 |
| 2609.00625v1 | mupdfng | random | hit | 420 | 0.000636 | 0.006121 | 0.025758 |
| 2609.00625v1 | mupdfng | revisit | hit | 420 | 0.000351 | 0.000761 | 0.020048 |
| 2609.00625v1 | mupdfng | sequential | miss | 390 | 100.089250 | 942.569212 | 979.124893 |
| 2609.00625v1 | poppler | first_page | miss | 30 | 613.282424 | 644.062285 | 655.594762 |
| 2609.00625v1 | poppler | random | hit | 420 | 0.000441 | 0.006302 | 0.007534 |
| 2609.00625v1 | poppler | revisit | hit | 420 | 0.000421 | 0.000471 | 0.001543 |
| 2609.00625v1 | poppler | sequential | miss | 390 | 236.278275 | 2620.245614 | 2667.166119 |
| 2609.09123v1 | mupdfng | first_page | miss | 30 | 38.566887 | 40.583755 | 50.548400 |
| 2609.09123v1 | mupdfng | random | hit | 537 | 0.000571 | 0.008065 | 0.023514 |
| 2609.09123v1 | mupdfng | random | miss | 63 | 240.366144 | 258.154759 | 294.814738 |
| 2609.09123v1 | mupdfng | revisit | hit | 600 | 0.000361 | 0.000811 | 0.007935 |
| 2609.09123v1 | mupdfng | sequential | miss | 570 | 24.461740 | 1646.985603 | 1714.695980 |
| 2609.09123v1 | poppler | first_page | miss | 30 | 38.300335 | 40.056893 | 60.188232 |
| 2609.09123v1 | poppler | random | hit | 537 | 0.000651 | 0.007033 | 0.119001 |
| 2609.09123v1 | poppler | random | miss | 63 | 1056.456214 | 1340.747970 | 1384.242995 |
| 2609.09123v1 | poppler | revisit | hit | 600 | 0.000621 | 0.000762 | 0.098212 |
| 2609.09123v1 | poppler | sequential | miss | 570 | 44.448755 | 1681.312936 | 1770.195852 |
| 2610.26067v1 | mupdfng | first_page | miss | 30 | 53.350311 | 55.322081 | 55.676314 |
| 2610.26067v1 | mupdfng | random | hit | 480 | 0.000641 | 0.007203 | 0.026970 |
| 2610.26067v1 | mupdfng | revisit | hit | 480 | 0.000341 | 0.000712 | 0.003927 |
| 2610.26067v1 | mupdfng | sequential | miss | 450 | 112.945943 | 793.289951 | 836.536543 |
| 2610.26067v1 | poppler | first_page | miss | 30 | 54.583667 | 56.057967 | 64.850971 |
| 2610.26067v1 | poppler | random | hit | 480 | 0.000441 | 0.006382 | 0.010069 |
| 2610.26067v1 | poppler | revisit | hit | 480 | 0.000431 | 0.000481 | 0.022773 |
| 2610.26067v1 | poppler | sequential | miss | 450 | 454.322679 | 3898.096302 | 3971.293063 |
| 2312.00752v2 | mupdfng | first_page | miss | 30 | 91.639379 | 94.874165 | 118.316452 |
| 2312.00752v2 | mupdfng | random | hit | 409 | 0.000832 | 0.007945 | 0.027371 |
| 2312.00752v2 | mupdfng | random | miss | 191 | 28.762244 | 34.515660 | 44.049257 |
| 2312.00752v2 | mupdfng | revisit | hit | 600 | 0.000581 | 0.000891 | 0.008035 |
| 2312.00752v2 | mupdfng | sequential | miss | 570 | 32.484091 | 40.538578 | 46.419951 |
| 2312.00752v2 | poppler | first_page | miss | 30 | 69.852421 | 72.463285 | 74.204735 |
| 2312.00752v2 | poppler | random | hit | 409 | 0.000731 | 0.007464 | 0.018855 |
| 2312.00752v2 | poppler | random | miss | 191 | 56.446670 | 69.346992 | 91.141509 |
| 2312.00752v2 | poppler | revisit | hit | 600 | 0.000460 | 0.000741 | 0.016561 |
| 2312.00752v2 | poppler | sequential | miss | 570 | 64.342886 | 70.306687 | 90.464162 |
| 2307.03109v9 | mupdfng | first_page | miss | 30 | 62.918136 | 65.814572 | 77.337147 |
| 2307.03109v9 | mupdfng | random | hit | 351 | 0.000911 | 0.008316 | 0.030026 |
| 2307.03109v9 | mupdfng | random | miss | 249 | 32.641508 | 42.782259 | 45.211464 |
| 2307.03109v9 | mupdfng | revisit | hit | 600 | 0.000601 | 0.000972 | 0.023974 |
| 2307.03109v9 | mupdfng | sequential | miss | 570 | 27.856534 | 60.293593 | 89.943129 |
| 2307.03109v9 | poppler | first_page | miss | 30 | 67.436981 | 69.821393 | 69.927137 |
| 2307.03109v9 | poppler | random | hit | 351 | 0.000802 | 0.007504 | 0.029414 |
| 2307.03109v9 | poppler | random | miss | 249 | 61.646444 | 71.070398 | 81.201093 |
| 2307.03109v9 | poppler | revisit | hit | 600 | 0.000611 | 0.000842 | 0.022923 |
| 2307.03109v9 | poppler | sequential | miss | 570 | 57.382888 | 73.965189 | 92.329342 |

## Environment

```json
{
  "platform": "Linux-7.0.0-1017-azure-x86_64-with-glibc2.44",
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
  "source_commit": "aafe97a17e70c1a69ba44a30a64f728317764be0",
  "source_dirty": false,
  "benchmark_commit": "a05be3241f1ff8a13fe35559fd61a2ee9f5c8490",
  "benchmark_dirty": false,
  "runner_image": "local",
  "runner_image_version": "local",
  "container_image": "archlinux:latest",
  "versions": {
    "poppler": "26.10.0",
    "okular": "okular 26.08.2",
    "compiler": "clang version 23.1.4\nTarget: x86_64-pc-linux-gnu\nThread model: posix\nInstalledDir: /usr/bin",
    "mupdf": "1.28.6"
  }
}
```

## Interpretation limits

Paired trials reduce host-speed noise, but CPU architectures can favor the backends differently. Graph lines group runs by CPU model and Poppler version; other environment and benchmark settings remain recorded in the reports. Bootstrap intervals resample whole paired trial scores; repeated pages are not independent samples of all PDFs. This is an offscreen rendering benchmark, not a GUI scrolling, memory, or visual-fidelity measurement. OS file caches are warm/uncontrolled. No performance merge gate is applied.

Okular warning-bearing trials: 150. See `summary.json` and `samples.jsonl.gz` for details.

Artifacts: [summary](summary.json), [raw trials](samples.jsonl.gz), [corpus manifest](corpus-manifest.json).

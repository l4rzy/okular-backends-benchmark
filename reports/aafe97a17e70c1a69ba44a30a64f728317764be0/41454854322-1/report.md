# PDF backend benchmark

Source commit: [aafe97a17e70c1a69ba44a30a64f728317764be0](https://github.com/l4rzy/okular-mupdf-ng/commit/aafe97a17e70c1a69ba44a30a64f728317764be0).

Benchmark commit: `886b46a1d2e8bac8adce6fdf21e2da5a17a3011a`.

Run: [41454854322-1](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/41454854322), 2026-11-02T14:13:46.781806+00:00.

**Median paired rendering ratio: 2.250×** (95% bootstrap interval 2.239–2.255×).

Ratio = Poppler time / MuPDF-NG time; above 1 favors MuPDF-NG. Each trial uses the geometric mean of document ratios, giving each PDF equal weight. The headline is the median of those trial scores. The primary workload sums first-page and sequential-render request times, excluding document opening and worker startup. The worker stays alive for all requests in a trial.

MuPDF-NG uses **Relaxed sandbox enforcement**: available worker protections remain active, and incomplete host hardening does not block document opening.

300 successful backend trials; 30 pairs per PDF; series `d2c307ea82a68627`.

## Per-document results

Times are medians in milliseconds. Ratios are medians of paired ratios, not ratios of medians.

| PDF | Pages | Render ratio | MuPDF-NG render batch | Poppler render batch | MuPDF-NG open → first page | Poppler open → first page |
|---|---:|---:|---:|---:|---:|---:|
| 2609.00625v1 | 14 | 2.429× | 2866.926 | 6972.788 | 251.387 | 621.978 |
| 2609.09123v1 | 24 | 1.837× | 2838.574 | 5224.188 | 64.800 | 45.261 |
| 2610.26067v1 | 16 | 4.007× | 3304.421 | 13244.854 | 78.638 | 61.670 |
| 2312.00752v2 | 36 | 1.801× | 703.217 | 1266.685 | 114.865 | 77.483 |
| 2307.03109v9 | 45 | 1.769× | 630.505 | 1117.073 | 90.991 | 79.437 |

## Individual requests

Times are milliseconds; p95 is shown only for at least 20 samples. Cache hits are separate.

| PDF | Backend | Phase | Cache | N | Median | p95 | Maximum |
|---|---|---|---|---:|---:|---:|---:|
| 2609.00625v1 | mupdfng | first_page | miss | 30 | 226.585879 | 246.276929 | 259.155326 |
| 2609.00625v1 | mupdfng | random | hit | 420 | 0.000701 | 0.005831 | 0.020529 |
| 2609.00625v1 | mupdfng | revisit | hit | 420 | 0.000351 | 0.000742 | 0.001192 |
| 2609.00625v1 | mupdfng | sequential | miss | 390 | 100.211917 | 942.708007 | 991.604389 |
| 2609.00625v1 | poppler | first_page | miss | 30 | 612.466184 | 641.124030 | 645.748423 |
| 2609.00625v1 | poppler | random | hit | 420 | 0.000441 | 0.005740 | 0.007394 |
| 2609.00625v1 | poppler | revisit | hit | 420 | 0.000421 | 0.000491 | 0.001492 |
| 2609.00625v1 | poppler | sequential | miss | 390 | 234.857505 | 2618.117863 | 2670.728370 |
| 2609.09123v1 | mupdfng | first_page | miss | 30 | 38.438905 | 39.921542 | 46.752986 |
| 2609.09123v1 | mupdfng | random | hit | 537 | 0.000611 | 0.008175 | 0.026679 |
| 2609.09123v1 | mupdfng | random | miss | 63 | 240.263136 | 255.882879 | 267.836390 |
| 2609.09123v1 | mupdfng | revisit | hit | 600 | 0.000341 | 0.000741 | 0.006352 |
| 2609.09123v1 | mupdfng | sequential | miss | 570 | 24.065579 | 1643.935235 | 1688.083890 |
| 2609.09123v1 | poppler | first_page | miss | 30 | 37.955282 | 40.878366 | 48.131127 |
| 2609.09123v1 | poppler | random | hit | 537 | 0.000641 | 0.006622 | 0.110858 |
| 2609.09123v1 | poppler | random | miss | 63 | 1059.530776 | 1373.365461 | 1392.254871 |
| 2609.09123v1 | poppler | revisit | hit | 600 | 0.000592 | 0.000712 | 0.077214 |
| 2609.09123v1 | poppler | sequential | miss | 570 | 44.158805 | 1680.855083 | 1797.373749 |
| 2610.26067v1 | mupdfng | first_page | miss | 30 | 52.392716 | 55.310422 | 62.375985 |
| 2610.26067v1 | mupdfng | random | hit | 480 | 0.000681 | 0.004619 | 0.024215 |
| 2610.26067v1 | mupdfng | revisit | hit | 480 | 0.000341 | 0.000421 | 0.001123 |
| 2610.26067v1 | mupdfng | sequential | miss | 450 | 112.275218 | 792.542681 | 866.890355 |
| 2610.26067v1 | poppler | first_page | miss | 30 | 53.768634 | 55.436759 | 78.282532 |
| 2610.26067v1 | poppler | random | hit | 480 | 0.000441 | 0.004939 | 0.007784 |
| 2610.26067v1 | poppler | revisit | hit | 480 | 0.000431 | 0.000701 | 0.029936 |
| 2610.26067v1 | poppler | sequential | miss | 450 | 453.153629 | 3895.524752 | 4152.898256 |
| 2312.00752v2 | mupdfng | first_page | miss | 30 | 91.678585 | 93.248357 | 99.915466 |
| 2312.00752v2 | mupdfng | random | hit | 409 | 0.000822 | 0.006261 | 0.023334 |
| 2312.00752v2 | mupdfng | random | miss | 191 | 27.786570 | 33.402113 | 37.218083 |
| 2312.00752v2 | mupdfng | revisit | hit | 600 | 0.000370 | 0.000872 | 0.007524 |
| 2312.00752v2 | mupdfng | sequential | miss | 570 | 32.219471 | 40.085608 | 58.020881 |
| 2312.00752v2 | poppler | first_page | miss | 30 | 69.859219 | 71.851342 | 77.734281 |
| 2312.00752v2 | poppler | random | hit | 409 | 0.000711 | 0.006613 | 0.007965 |
| 2312.00752v2 | poppler | random | miss | 191 | 55.802679 | 69.211480 | 91.218600 |
| 2312.00752v2 | poppler | revisit | hit | 600 | 0.000461 | 0.000711 | 0.006522 |
| 2312.00752v2 | poppler | sequential | miss | 570 | 63.534575 | 69.682075 | 92.099630 |
| 2307.03109v9 | mupdfng | first_page | miss | 30 | 62.185636 | 64.645410 | 65.253931 |
| 2307.03109v9 | mupdfng | random | hit | 351 | 0.000952 | 0.007274 | 0.078467 |
| 2307.03109v9 | mupdfng | random | miss | 249 | 31.801788 | 42.499293 | 60.805983 |
| 2307.03109v9 | mupdfng | revisit | hit | 600 | 0.000491 | 0.000932 | 0.007314 |
| 2307.03109v9 | mupdfng | sequential | miss | 570 | 27.155477 | 59.536073 | 69.922121 |
| 2307.03109v9 | poppler | first_page | miss | 30 | 66.553158 | 69.272665 | 81.267901 |
| 2307.03109v9 | poppler | random | hit | 351 | 0.000802 | 0.006662 | 0.021260 |
| 2307.03109v9 | poppler | random | miss | 249 | 61.143183 | 69.421153 | 88.420380 |
| 2307.03109v9 | poppler | revisit | hit | 600 | 0.000601 | 0.000871 | 0.006883 |
| 2307.03109v9 | poppler | sequential | miss | 570 | 56.496359 | 72.946077 | 95.284055 |

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
  "benchmark_commit": "886b46a1d2e8bac8adce6fdf21e2da5a17a3011a",
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

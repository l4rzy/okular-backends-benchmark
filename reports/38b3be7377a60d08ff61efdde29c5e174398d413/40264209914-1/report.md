# PDF backend benchmark

Source commit: [38b3be7377a60d08ff61efdde29c5e174398d413](https://github.com/l4rzy/okular-mupdf-ng/commit/38b3be7377a60d08ff61efdde29c5e174398d413).

Benchmark commit: `d4fea5000533369fbb1e500b75948df78f0c4d86`.

Run: [40264209914-1](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/40264209914), 2026-10-26T03:53:58.826065+00:00.

**Median paired rendering ratio: 2.224×** (95% bootstrap interval 2.213–2.233×).

Ratio = Poppler time / MuPDF-NG time; above 1 favors MuPDF-NG. Each trial uses the geometric mean of document ratios, giving each PDF equal weight. The headline is the median of those trial scores. The primary workload sums first-page and sequential-render request times, excluding document opening and worker startup. The worker stays alive for all requests in a trial.

MuPDF-NG uses **Relaxed sandbox enforcement**: available worker protections remain active, and incomplete host hardening does not block document opening.

200 successful backend trials; 20 pairs per PDF; series `f4cc5d0dd0b48b38`.

## Per-document results

Times are medians in milliseconds. Ratios are medians of paired ratios, not ratios of medians.

| PDF | Pages | Render ratio | MuPDF-NG render batch | Poppler render batch | MuPDF-NG open → first page | Poppler open → first page |
|---|---:|---:|---:|---:|---:|---:|
| 2609.00625v1 | 14 | 2.456× | 2834.782 | 6956.819 | 249.650 | 620.444 |
| 2609.09123v1 | 24 | 1.801× | 2875.898 | 5198.848 | 62.750 | 45.254 |
| 2610.26067v1 | 16 | 4.038× | 3279.161 | 13241.718 | 76.243 | 61.687 |
| 2312.00752v2 | 36 | 1.769× | 723.380 | 1273.253 | 113.554 | 77.759 |
| 2307.03109v9 | 45 | 1.738× | 648.724 | 1124.920 | 90.768 | 79.951 |

## Individual requests

Times are milliseconds; p95 is shown only for at least 20 samples. Cache hits are separate.

| PDF | Backend | Phase | Cache | N | Median | p95 | Maximum |
|---|---|---|---|---:|---:|---:|---:|
| 2609.00625v1 | mupdfng | first_page | miss | 20 | 226.597114 | 230.885099 | 268.050764 |
| 2609.00625v1 | mupdfng | random | hit | 280 | 0.000711 | 0.003917 | 0.009137 |
| 2609.00625v1 | mupdfng | revisit | hit | 280 | 0.000351 | 0.000751 | 0.001093 |
| 2609.00625v1 | mupdfng | sequential | miss | 260 | 98.196087 | 948.277176 | 997.469211 |
| 2609.00625v1 | poppler | first_page | miss | 20 | 610.975064 | 645.061011 | 661.965408 |
| 2609.00625v1 | poppler | random | hit | 280 | 0.000441 | 0.004408 | 0.007173 |
| 2609.00625v1 | poppler | revisit | hit | 280 | 0.000421 | 0.000512 | 0.000912 |
| 2609.00625v1 | poppler | sequential | miss | 260 | 234.619036 | 2606.498962 | 2654.952508 |
| 2609.09123v1 | mupdfng | first_page | miss | 20 | 38.947053 | 41.919936 | 44.475809 |
| 2609.09123v1 | mupdfng | random | hit | 356 | 0.000681 | 0.007725 | 0.010810 |
| 2609.09123v1 | mupdfng | random | miss | 44 | 243.008992 | 263.737463 | 288.756286 |
| 2609.09123v1 | mupdfng | revisit | hit | 400 | 0.000361 | 0.000731 | 0.006552 |
| 2609.09123v1 | mupdfng | sequential | miss | 380 | 23.413059 | 1683.040859 | 1742.967503 |
| 2609.09123v1 | poppler | first_page | miss | 20 | 37.953724 | 39.090649 | 39.577280 |
| 2609.09123v1 | poppler | random | hit | 356 | 0.000632 | 0.007123 | 0.127808 |
| 2609.09123v1 | poppler | random | miss | 44 | 1083.841426 | 1340.496433 | 1403.451007 |
| 2609.09123v1 | poppler | revisit | hit | 400 | 0.000471 | 0.000691 | 0.006352 |
| 2609.09123v1 | poppler | sequential | miss | 380 | 43.729444 | 1654.966888 | 1733.521285 |
| 2610.26067v1 | mupdfng | first_page | miss | 20 | 51.856504 | 54.188318 | 54.704422 |
| 2610.26067v1 | mupdfng | random | hit | 320 | 0.000682 | 0.003196 | 0.008867 |
| 2610.26067v1 | mupdfng | revisit | hit | 320 | 0.000341 | 0.000421 | 0.000952 |
| 2610.26067v1 | mupdfng | sequential | miss | 300 | 111.873861 | 786.075860 | 827.992724 |
| 2610.26067v1 | poppler | first_page | miss | 20 | 53.793340 | 55.142258 | 55.394547 |
| 2610.26067v1 | poppler | random | hit | 320 | 0.000441 | 0.004629 | 0.039514 |
| 2610.26067v1 | poppler | revisit | hit | 320 | 0.000430 | 0.000481 | 0.000521 |
| 2610.26067v1 | poppler | sequential | miss | 300 | 453.525187 | 3888.991845 | 3962.146752 |
| 2312.00752v2 | mupdfng | first_page | miss | 20 | 91.750782 | 96.789882 | 119.216181 |
| 2312.00752v2 | mupdfng | random | hit | 283 | 0.000822 | 0.007615 | 0.019106 |
| 2312.00752v2 | mupdfng | random | miss | 117 | 28.585250 | 36.703241 | 55.390254 |
| 2312.00752v2 | mupdfng | revisit | hit | 400 | 0.000405 | 0.000912 | 0.020549 |
| 2312.00752v2 | mupdfng | sequential | miss | 380 | 32.782922 | 41.151037 | 56.626060 |
| 2312.00752v2 | poppler | first_page | miss | 20 | 70.134658 | 72.597832 | 73.311620 |
| 2312.00752v2 | poppler | random | hit | 283 | 0.000701 | 0.007234 | 0.008375 |
| 2312.00752v2 | poppler | random | miss | 117 | 56.028804 | 67.897820 | 69.213869 |
| 2312.00752v2 | poppler | revisit | hit | 400 | 0.000506 | 0.000862 | 0.028543 |
| 2312.00752v2 | poppler | sequential | miss | 380 | 64.043467 | 69.639286 | 84.839676 |
| 2307.03109v9 | mupdfng | first_page | miss | 20 | 62.505477 | 66.076596 | 84.410801 |
| 2307.03109v9 | mupdfng | random | hit | 241 | 0.000942 | 0.007534 | 0.010260 |
| 2307.03109v9 | mupdfng | random | miss | 159 | 32.654776 | 42.806996 | 50.367747 |
| 2307.03109v9 | mupdfng | revisit | hit | 400 | 0.000391 | 0.000952 | 0.007163 |
| 2307.03109v9 | mupdfng | sequential | miss | 380 | 27.852441 | 59.394465 | 75.335868 |
| 2307.03109v9 | poppler | first_page | miss | 20 | 67.193979 | 84.206338 | 88.527106 |
| 2307.03109v9 | poppler | random | hit | 241 | 0.000781 | 0.007434 | 0.008065 |
| 2307.03109v9 | poppler | random | miss | 159 | 61.161715 | 68.030294 | 76.368847 |
| 2307.03109v9 | poppler | revisit | hit | 400 | 0.000591 | 0.000821 | 0.021470 |
| 2307.03109v9 | poppler | sequential | miss | 380 | 56.609265 | 73.483808 | 80.821972 |

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
  "protocol_sha256": "1534c5af52d86fc4cda7a9cda8ea9c0fe7e96a7012b74ee8c75dba1a077e10e5",
  "source_commit": "38b3be7377a60d08ff61efdde29c5e174398d413",
  "source_dirty": false,
  "benchmark_commit": "d4fea5000533369fbb1e500b75948df78f0c4d86",
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

Paired trials reduce host-speed noise, but CPU architectures can favor the backends differently. CPU, baseline binary, dependencies, corpus, harness, and settings identify separate trend series. Bootstrap intervals resample whole paired trial scores; repeated pages are not independent samples of all PDFs. This is an offscreen rendering benchmark, not a GUI scrolling, memory, or visual-fidelity measurement. OS file caches are warm/uncontrolled. No performance merge gate is applied.

Okular warning-bearing trials: 100. See `summary.json` and `samples.jsonl.gz` for details.

Artifacts: [summary](summary.json), [raw trials](samples.jsonl.gz), [corpus manifest](corpus-manifest.json).

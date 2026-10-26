# PDF backend benchmark

Source commit: [fe1e49a3aef7d3dc080155190f3a5d95de37adcb](https://github.com/l4rzy/okular-mupdf-ng/commit/fe1e49a3aef7d3dc080155190f3a5d95de37adcb).

Benchmark commit: `32cf482a771d509c8858b4d03c4003313774498e`.

Run: [40267419123-1](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/40267419123), 2026-10-26T04:33:27.015201+00:00.

**Median paired rendering ratio: 2.246×** (95% bootstrap interval 2.234–2.259×).

Ratio = Poppler time / MuPDF-NG time; above 1 favors MuPDF-NG. Each trial uses the geometric mean of document ratios, giving each PDF equal weight. The headline is the median of those trial scores. The primary workload sums first-page and sequential-render request times, excluding document opening and worker startup. The worker stays alive for all requests in a trial.

MuPDF-NG uses **Relaxed sandbox enforcement**: available worker protections remain active, and incomplete host hardening does not block document opening.

200 successful backend trials; 20 pairs per PDF; series `f4cc5d0dd0b48b38`.

## Per-document results

Times are medians in milliseconds. Ratios are medians of paired ratios, not ratios of medians.

| PDF | Pages | Render ratio | MuPDF-NG render batch | Poppler render batch | MuPDF-NG open → first page | Poppler open → first page |
|---|---:|---:|---:|---:|---:|---:|
| 2609.00625v1 | 14 | 2.473× | 2825.973 | 6989.808 | 250.401 | 621.032 |
| 2609.09123v1 | 24 | 1.854× | 2821.928 | 5235.838 | 63.936 | 46.017 |
| 2610.26067v1 | 16 | 4.104× | 3233.872 | 13263.943 | 78.157 | 62.029 |
| 2312.00752v2 | 36 | 1.760× | 723.611 | 1271.694 | 114.385 | 77.702 |
| 2307.03109v9 | 45 | 1.723× | 649.725 | 1121.460 | 90.851 | 80.120 |

## Individual requests

Times are milliseconds; p95 is shown only for at least 20 samples. Cache hits are separate.

| PDF | Backend | Phase | Cache | N | Median | p95 | Maximum |
|---|---|---|---|---:|---:|---:|---:|
| 2609.00625v1 | mupdfng | first_page | miss | 20 | 225.556057 | 231.483306 | 255.833046 |
| 2609.00625v1 | mupdfng | random | hit | 280 | 0.000561 | 0.005009 | 0.007143 |
| 2609.00625v1 | mupdfng | revisit | hit | 280 | 0.000360 | 0.000682 | 0.000972 |
| 2609.00625v1 | mupdfng | sequential | miss | 260 | 97.240280 | 943.158871 | 992.481123 |
| 2609.00625v1 | poppler | first_page | miss | 20 | 611.472737 | 614.470015 | 621.228348 |
| 2609.00625v1 | poppler | random | hit | 280 | 0.000451 | 0.005911 | 0.028674 |
| 2609.00625v1 | poppler | revisit | hit | 280 | 0.000431 | 0.000491 | 0.001332 |
| 2609.00625v1 | poppler | sequential | miss | 260 | 236.239832 | 2611.678047 | 2677.060789 |
| 2609.09123v1 | mupdfng | first_page | miss | 20 | 39.078260 | 40.410772 | 40.493811 |
| 2609.09123v1 | mupdfng | random | hit | 356 | 0.000506 | 0.007343 | 0.093534 |
| 2609.09123v1 | mupdfng | random | miss | 44 | 234.520443 | 249.696745 | 255.765078 |
| 2609.09123v1 | mupdfng | revisit | hit | 400 | 0.000361 | 0.000792 | 0.008596 |
| 2609.09123v1 | mupdfng | sequential | miss | 380 | 24.163435 | 1635.492160 | 1690.874088 |
| 2609.09123v1 | poppler | first_page | miss | 20 | 38.779031 | 40.308645 | 41.045087 |
| 2609.09123v1 | poppler | random | hit | 356 | 0.000641 | 0.006923 | 0.110526 |
| 2609.09123v1 | poppler | random | miss | 44 | 1057.307529 | 1346.264991 | 1376.715456 |
| 2609.09123v1 | poppler | revisit | hit | 400 | 0.000441 | 0.000721 | 0.021230 |
| 2609.09123v1 | poppler | sequential | miss | 380 | 44.558683 | 1663.726830 | 1777.910789 |
| 2610.26067v1 | mupdfng | first_page | miss | 20 | 52.768018 | 54.440572 | 74.686490 |
| 2610.26067v1 | mupdfng | random | hit | 320 | 0.000661 | 0.005611 | 0.011011 |
| 2610.26067v1 | mupdfng | revisit | hit | 320 | 0.000351 | 0.000390 | 0.000711 |
| 2610.26067v1 | mupdfng | sequential | miss | 300 | 110.909109 | 777.162456 | 816.535039 |
| 2610.26067v1 | poppler | first_page | miss | 20 | 53.938370 | 54.749136 | 55.003592 |
| 2610.26067v1 | poppler | random | hit | 320 | 0.000441 | 0.005691 | 0.007274 |
| 2610.26067v1 | poppler | revisit | hit | 320 | 0.000421 | 0.000491 | 0.001653 |
| 2610.26067v1 | poppler | sequential | miss | 300 | 452.319142 | 3893.705853 | 3947.072689 |
| 2312.00752v2 | mupdfng | first_page | miss | 20 | 92.084951 | 96.159417 | 129.833009 |
| 2312.00752v2 | mupdfng | random | hit | 283 | 0.000812 | 0.006812 | 0.009467 |
| 2312.00752v2 | mupdfng | random | miss | 117 | 28.661866 | 35.705354 | 44.666787 |
| 2312.00752v2 | mupdfng | revisit | hit | 400 | 0.000381 | 0.000911 | 0.008356 |
| 2312.00752v2 | mupdfng | sequential | miss | 380 | 32.725476 | 40.937603 | 46.260330 |
| 2312.00752v2 | poppler | first_page | miss | 20 | 70.005499 | 72.172934 | 72.391951 |
| 2312.00752v2 | poppler | random | hit | 283 | 0.000681 | 0.007143 | 0.011551 |
| 2312.00752v2 | poppler | random | miss | 117 | 56.059663 | 69.074858 | 77.020915 |
| 2312.00752v2 | poppler | revisit | hit | 400 | 0.000471 | 0.000741 | 0.007384 |
| 2312.00752v2 | poppler | sequential | miss | 380 | 64.059299 | 69.869696 | 82.913866 |
| 2307.03109v9 | mupdfng | first_page | miss | 20 | 62.885707 | 64.867316 | 65.482188 |
| 2307.03109v9 | mupdfng | random | hit | 241 | 0.000932 | 0.007344 | 0.013946 |
| 2307.03109v9 | mupdfng | random | miss | 159 | 32.945455 | 42.818712 | 44.345578 |
| 2307.03109v9 | mupdfng | revisit | hit | 400 | 0.000381 | 0.000952 | 0.007565 |
| 2307.03109v9 | mupdfng | sequential | miss | 380 | 28.165345 | 60.875203 | 69.642853 |
| 2307.03109v9 | poppler | first_page | miss | 20 | 67.175935 | 68.775500 | 89.170580 |
| 2307.03109v9 | poppler | random | hit | 241 | 0.000791 | 0.007073 | 0.094286 |
| 2307.03109v9 | poppler | random | miss | 159 | 61.362756 | 70.108447 | 76.277470 |
| 2307.03109v9 | poppler | revisit | hit | 400 | 0.000611 | 0.000801 | 0.007364 |
| 2307.03109v9 | poppler | sequential | miss | 380 | 57.070579 | 73.372155 | 87.072026 |

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
  "source_commit": "fe1e49a3aef7d3dc080155190f3a5d95de37adcb",
  "source_dirty": false,
  "benchmark_commit": "32cf482a771d509c8858b4d03c4003313774498e",
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

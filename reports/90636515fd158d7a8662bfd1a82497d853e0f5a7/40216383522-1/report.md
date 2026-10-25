# PDF backend benchmark

Source commit: [90636515fd158d7a8662bfd1a82497d853e0f5a7](https://github.com/l4rzy/okular-mupdf-ng/commit/90636515fd158d7a8662bfd1a82497d853e0f5a7).

Benchmark commit: `feb8e0a91f9265bd94dc35f2c8a34a09a14b2bc6`.

Run: [40216383522-1](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/40216383522), 2026-10-25T17:51:13.787340+00:00.

**Median paired rendering ratio: 2.455×** (95% bootstrap interval 2.453–2.462×).

Ratio = Poppler time / MuPDF-NG time; above 1 favors MuPDF-NG. Each trial uses the geometric mean of document ratios, giving each PDF equal weight. The headline is the median of those trial scores. The primary workload sums first-page and sequential-render request times, excluding document opening and worker startup. The worker stays alive for all requests in a trial.

MuPDF-NG uses **Relaxed sandbox enforcement**: available worker protections remain active, and incomplete host hardening does not block document opening.

200 successful backend trials; 20 pairs per PDF; series `81f18c06a23b0392`.

## Per-document results

Times are medians in milliseconds. Ratios are medians of paired ratios, not ratios of medians.

| PDF | Pages | Render ratio | MuPDF-NG render batch | Poppler render batch | MuPDF-NG open → first page | Poppler open → first page |
|---|---:|---:|---:|---:|---:|---:|
| 2609.00625v1 | 14 | 2.551× | 2724.571 | 6939.877 | 237.853 | 620.446 |
| 2609.09123v1 | 24 | 1.877× | 2755.479 | 5158.067 | 56.039 | 41.457 |
| 2610.26067v1 | 16 | 4.512× | 3035.175 | 13703.316 | 69.403 | 56.484 |
| 2312.00752v2 | 36 | 2.003× | 599.251 | 1201.476 | 104.896 | 70.897 |
| 2307.03109v9 | 45 | 2.083× | 500.906 | 1041.466 | 80.786 | 72.342 |

## Individual requests

Times are milliseconds; p95 is shown only for at least 20 samples. Cache hits are separate.

| PDF | Backend | Phase | Cache | N | Median | p95 | Maximum |
|---|---|---|---|---:|---:|---:|---:|
| 2609.00625v1 | mupdfng | first_page | miss | 20 | 214.822722 | 219.395041 | 219.623212 |
| 2609.00625v1 | mupdfng | random | hit | 280 | 0.000682 | 0.004799 | 0.010119 |
| 2609.00625v1 | mupdfng | revisit | hit | 280 | 0.000361 | 0.000571 | 0.013456 |
| 2609.00625v1 | mupdfng | sequential | miss | 260 | 93.358822 | 941.074455 | 971.684746 |
| 2609.00625v1 | poppler | first_page | miss | 20 | 610.838361 | 615.349333 | 618.781429 |
| 2609.00625v1 | poppler | random | hit | 280 | 0.000461 | 0.004267 | 0.005710 |
| 2609.00625v1 | poppler | revisit | hit | 280 | 0.000451 | 0.000481 | 0.022482 |
| 2609.00625v1 | poppler | sequential | miss | 260 | 232.240636 | 2642.711102 | 2695.616894 |
| 2609.09123v1 | mupdfng | first_page | miss | 20 | 31.494793 | 32.732014 | 32.960506 |
| 2609.09123v1 | mupdfng | random | hit | 356 | 0.000787 | 0.007514 | 0.020829 |
| 2609.09123v1 | mupdfng | random | miss | 44 | 234.163869 | 250.032547 | 253.388612 |
| 2609.09123v1 | mupdfng | revisit | hit | 400 | 0.000371 | 0.000962 | 0.008085 |
| 2609.09123v1 | mupdfng | sequential | miss | 380 | 18.765997 | 1685.538111 | 1704.326595 |
| 2609.09123v1 | poppler | first_page | miss | 20 | 35.373183 | 36.099194 | 37.749667 |
| 2609.09123v1 | poppler | random | hit | 356 | 0.000691 | 0.006512 | 0.119072 |
| 2609.09123v1 | poppler | random | miss | 44 | 1057.879030 | 1339.257676 | 1350.744130 |
| 2609.09123v1 | poppler | revisit | hit | 400 | 0.000662 | 0.000862 | 0.022462 |
| 2609.09123v1 | poppler | sequential | miss | 380 | 40.654944 | 1649.525292 | 1729.501385 |
| 2610.26067v1 | mupdfng | first_page | miss | 20 | 44.988568 | 45.660323 | 45.786889 |
| 2610.26067v1 | mupdfng | random | hit | 320 | 0.000796 | 0.003927 | 0.006412 |
| 2610.26067v1 | mupdfng | revisit | hit | 320 | 0.000361 | 0.000391 | 0.001563 |
| 2610.26067v1 | mupdfng | sequential | miss | 300 | 100.838267 | 770.347423 | 781.948484 |
| 2610.26067v1 | poppler | first_page | miss | 20 | 49.835394 | 50.845307 | 50.893486 |
| 2610.26067v1 | poppler | random | hit | 320 | 0.000461 | 0.003787 | 0.093405 |
| 2610.26067v1 | poppler | revisit | hit | 320 | 0.000451 | 0.000501 | 0.001834 |
| 2610.26067v1 | poppler | sequential | miss | 300 | 461.473587 | 4065.694852 | 4110.984001 |
| 2312.00752v2 | mupdfng | first_page | miss | 20 | 83.542632 | 84.553622 | 84.856241 |
| 2312.00752v2 | mupdfng | random | hit | 283 | 0.000922 | 0.004258 | 0.019416 |
| 2312.00752v2 | mupdfng | random | miss | 117 | 22.731516 | 29.144896 | 30.596005 |
| 2312.00752v2 | mupdfng | revisit | hit | 400 | 0.000381 | 0.001052 | 0.004859 |
| 2312.00752v2 | mupdfng | sequential | miss | 380 | 26.460411 | 34.395628 | 39.614417 |
| 2312.00752v2 | poppler | first_page | miss | 20 | 64.534828 | 65.554745 | 65.561207 |
| 2312.00752v2 | poppler | random | hit | 283 | 0.000712 | 0.003968 | 0.006713 |
| 2312.00752v2 | poppler | random | miss | 117 | 51.990441 | 65.272159 | 66.604711 |
| 2312.00752v2 | poppler | revisit | hit | 400 | 0.000526 | 0.000782 | 0.005610 |
| 2312.00752v2 | poppler | sequential | miss | 380 | 60.343528 | 66.833641 | 69.828908 |
| 2307.03109v9 | mupdfng | first_page | miss | 20 | 53.670195 | 54.366893 | 54.531827 |
| 2307.03109v9 | mupdfng | random | hit | 241 | 0.001032 | 0.005120 | 0.008236 |
| 2307.03109v9 | mupdfng | random | miss | 159 | 25.889628 | 35.277505 | 36.892951 |
| 2307.03109v9 | mupdfng | revisit | hit | 400 | 0.000521 | 0.001052 | 0.005681 |
| 2307.03109v9 | mupdfng | sequential | miss | 380 | 21.031872 | 53.194258 | 56.304064 |
| 2307.03109v9 | poppler | first_page | miss | 20 | 61.413397 | 61.776257 | 63.279070 |
| 2307.03109v9 | poppler | random | hit | 241 | 0.000792 | 0.004428 | 0.007364 |
| 2307.03109v9 | poppler | random | miss | 159 | 57.353432 | 64.896384 | 71.614199 |
| 2307.03109v9 | poppler | revisit | hit | 400 | 0.000481 | 0.000982 | 0.004519 |
| 2307.03109v9 | poppler | sequential | miss | 380 | 52.572161 | 69.200178 | 73.413584 |

## Environment

```json
{
  "platform": "Linux-6.17.0-1022-azure-x86_64-with-glibc2.43",
  "machine": "x86_64",
  "cpu_model": "AMD EPYC 7763 64-Core Processor",
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
  "source_commit": "90636515fd158d7a8662bfd1a82497d853e0f5a7",
  "source_dirty": false,
  "benchmark_commit": "feb8e0a91f9265bd94dc35f2c8a34a09a14b2bc6",
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

Okular warning-bearing trials: 100. See `summary.json` and `samples.jsonl.gz` for details.

Artifacts: [summary](summary.json), [raw trials](samples.jsonl.gz), [corpus manifest](corpus-manifest.json).

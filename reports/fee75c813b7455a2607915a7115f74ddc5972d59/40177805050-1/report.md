# PDF backend benchmark

Source commit: [fee75c813b7455a2607915a7115f74ddc5972d59](https://github.com/l4rzy/okular-mupdf-ng/commit/fee75c813b7455a2607915a7115f74ddc5972d59).

Benchmark commit: `d6e3efa561b2fdf639a975945d88828d13a1a199`.

Run: [40177805050-1](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/40177805050), 2026-10-25T09:11:16.346147+00:00.

**Median paired rendering ratio: 2.433×** (95% bootstrap interval 2.428–2.435×).

Ratio = Poppler time / MuPDF-NG time; above 1 favors MuPDF-NG. Each trial uses the geometric mean of document ratios, giving each PDF equal weight. The headline is the median of those trial scores. The primary workload sums first-page and sequential-render request times, excluding document opening and worker startup. The worker stays alive for all requests in a trial.

MuPDF-NG uses **Relaxed sandbox enforcement**: available worker protections remain active, and incomplete host hardening does not block document opening.

200 successful backend trials; 20 pairs per PDF; series `81f18c06a23b0392`.

## Per-document results

Times are medians in milliseconds. Ratios are medians of paired ratios, not ratios of medians.

| PDF | Pages | Render ratio | MuPDF-NG render batch | Poppler render batch | MuPDF-NG open → first page | Poppler open → first page |
|---|---:|---:|---:|---:|---:|---:|
| 2609.00625v1 | 14 | 2.544× | 2738.442 | 6959.651 | 242.614 | 619.406 |
| 2609.09123v1 | 24 | 1.863× | 2783.346 | 5201.098 | 57.375 | 41.969 |
| 2610.26067v1 | 16 | 4.497× | 3067.278 | 13780.425 | 71.782 | 58.336 |
| 2312.00752v2 | 36 | 1.961× | 628.116 | 1228.513 | 108.147 | 72.365 |
| 2307.03109v9 | 45 | 2.047× | 526.187 | 1073.897 | 83.616 | 73.796 |

## Individual requests

Times are milliseconds; p95 is shown only for at least 20 samples. Cache hits are separate.

| PDF | Backend | Phase | Cache | N | Median | p95 | Maximum |
|---|---|---|---|---:|---:|---:|---:|
| 2609.00625v1 | mupdfng | first_page | miss | 20 | 218.533094 | 220.741916 | 222.033183 |
| 2609.00625v1 | mupdfng | random | hit | 280 | 0.000677 | 0.006502 | 0.010369 |
| 2609.00625v1 | mupdfng | revisit | hit | 280 | 0.000371 | 0.000862 | 0.001202 |
| 2609.00625v1 | mupdfng | sequential | miss | 260 | 95.387080 | 931.067871 | 972.522197 |
| 2609.00625v1 | poppler | first_page | miss | 20 | 610.073840 | 617.982856 | 619.097054 |
| 2609.00625v1 | poppler | random | hit | 280 | 0.000465 | 0.006061 | 0.032050 |
| 2609.00625v1 | poppler | revisit | hit | 280 | 0.000461 | 0.000510 | 0.001893 |
| 2609.00625v1 | poppler | sequential | miss | 260 | 233.372193 | 2648.017949 | 2679.817183 |
| 2609.09123v1 | mupdfng | first_page | miss | 20 | 31.742748 | 32.313639 | 32.825071 |
| 2609.09123v1 | mupdfng | random | hit | 356 | 0.000732 | 0.007754 | 0.010390 |
| 2609.09123v1 | mupdfng | random | miss | 44 | 234.062980 | 248.623939 | 254.525586 |
| 2609.09123v1 | mupdfng | revisit | hit | 400 | 0.000371 | 0.000922 | 0.022822 |
| 2609.09123v1 | mupdfng | sequential | miss | 380 | 19.336961 | 1701.667436 | 1749.484405 |
| 2609.09123v1 | poppler | first_page | miss | 20 | 35.824435 | 38.189172 | 38.359807 |
| 2609.09123v1 | poppler | random | hit | 356 | 0.000701 | 0.007204 | 0.123000 |
| 2609.09123v1 | poppler | random | miss | 44 | 1064.248897 | 1336.355983 | 1351.921275 |
| 2609.09123v1 | poppler | revisit | hit | 400 | 0.000661 | 0.000871 | 0.007594 |
| 2609.09123v1 | poppler | sequential | miss | 380 | 41.506774 | 1657.358574 | 1740.105673 |
| 2610.26067v1 | mupdfng | first_page | miss | 20 | 45.649718 | 47.247674 | 47.640536 |
| 2610.26067v1 | mupdfng | random | hit | 320 | 0.000761 | 0.006572 | 0.010951 |
| 2610.26067v1 | mupdfng | revisit | hit | 320 | 0.000361 | 0.000832 | 0.001493 |
| 2610.26067v1 | mupdfng | sequential | miss | 300 | 101.249992 | 769.903449 | 782.355386 |
| 2610.26067v1 | poppler | first_page | miss | 20 | 51.600232 | 52.697858 | 52.827085 |
| 2610.26067v1 | poppler | random | hit | 320 | 0.000461 | 0.005841 | 0.155972 |
| 2610.26067v1 | poppler | revisit | hit | 320 | 0.000451 | 0.000481 | 0.001683 |
| 2610.26067v1 | poppler | sequential | miss | 300 | 466.200056 | 4088.142251 | 4123.745718 |
| 2312.00752v2 | mupdfng | first_page | miss | 20 | 84.628627 | 86.363638 | 91.736789 |
| 2312.00752v2 | mupdfng | random | hit | 283 | 0.000902 | 0.008516 | 0.025948 |
| 2312.00752v2 | mupdfng | random | miss | 117 | 24.160333 | 30.177833 | 31.682667 |
| 2312.00752v2 | mupdfng | revisit | hit | 400 | 0.000391 | 0.000991 | 0.017774 |
| 2312.00752v2 | mupdfng | sequential | miss | 380 | 27.986360 | 36.125202 | 42.483608 |
| 2312.00752v2 | poppler | first_page | miss | 20 | 65.806847 | 66.525968 | 66.736849 |
| 2312.00752v2 | poppler | random | hit | 283 | 0.000701 | 0.007414 | 0.027010 |
| 2312.00752v2 | poppler | random | miss | 117 | 53.346290 | 66.255568 | 67.667532 |
| 2312.00752v2 | poppler | revisit | hit | 400 | 0.000471 | 0.000801 | 0.007273 |
| 2312.00752v2 | poppler | sequential | miss | 380 | 61.752871 | 68.722351 | 89.383019 |
| 2307.03109v9 | mupdfng | first_page | miss | 20 | 54.656815 | 56.624490 | 57.506046 |
| 2307.03109v9 | mupdfng | random | hit | 241 | 0.000992 | 0.008445 | 0.009358 |
| 2307.03109v9 | mupdfng | random | miss | 159 | 27.434611 | 36.987836 | 39.718958 |
| 2307.03109v9 | mupdfng | revisit | hit | 400 | 0.000566 | 0.001122 | 0.009137 |
| 2307.03109v9 | mupdfng | sequential | miss | 380 | 22.291897 | 55.114926 | 64.787150 |
| 2307.03109v9 | poppler | first_page | miss | 20 | 62.752668 | 63.337155 | 63.521057 |
| 2307.03109v9 | poppler | random | hit | 241 | 0.000861 | 0.008046 | 0.039223 |
| 2307.03109v9 | poppler | random | miss | 159 | 59.134632 | 65.832996 | 72.735684 |
| 2307.03109v9 | poppler | revisit | hit | 400 | 0.000641 | 0.000872 | 0.008285 |
| 2307.03109v9 | poppler | sequential | miss | 380 | 53.904699 | 70.763148 | 73.258283 |

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
  "source_commit": "fee75c813b7455a2607915a7115f74ddc5972d59",
  "source_dirty": false,
  "benchmark_commit": "d6e3efa561b2fdf639a975945d88828d13a1a199",
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

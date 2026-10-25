# PDF backend benchmark

Source commit: [719a45dc838b57fb452312596f02749590f241e4](https://github.com/l4rzy/okular-mupdf-ng/commit/719a45dc838b57fb452312596f02749590f241e4).

Benchmark commit: `5108d5b9c40398f0981336d8d4beb173861a3a19`.

Run: [40234409410-1](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/40234409410), 2026-10-25T21:44:52.863341+00:00.

**Median paired rendering ratio: 2.288×** (95% bootstrap interval 2.284–2.291×).

Ratio = Poppler time / MuPDF-NG time; above 1 favors MuPDF-NG. Each trial uses the geometric mean of document ratios, giving each PDF equal weight. The headline is the median of those trial scores. The primary workload sums first-page and sequential-render request times, excluding document opening and worker startup. The worker stays alive for all requests in a trial.

MuPDF-NG uses **Relaxed sandbox enforcement**: available worker protections remain active, and incomplete host hardening does not block document opening.

300 successful backend trials; 30 pairs per PDF; series `17187dcbb384b32a`.

## Per-document results

Times are medians in milliseconds. Ratios are medians of paired ratios, not ratios of medians.

| PDF | Pages | Render ratio | MuPDF-NG render batch | Poppler render batch | MuPDF-NG open → first page | Poppler open → first page |
|---|---:|---:|---:|---:|---:|---:|
| 2609.00625v1 | 14 | 2.558× | 2853.541 | 7273.904 | 252.351 | 655.422 |
| 2609.09123v1 | 24 | 1.705× | 3019.756 | 5153.280 | 60.317 | 39.989 |
| 2610.26067v1 | 16 | 4.081× | 3275.172 | 13338.677 | 72.507 | 55.741 |
| 2312.00752v2 | 36 | 1.862× | 636.118 | 1183.971 | 111.108 | 70.544 |
| 2307.03109v9 | 45 | 1.898× | 536.960 | 1017.586 | 85.427 | 71.821 |

## Individual requests

Times are milliseconds; p95 is shown only for at least 20 samples. Cache hits are separate.

| PDF | Backend | Phase | Cache | N | Median | p95 | Maximum |
|---|---|---|---|---:|---:|---:|---:|
| 2609.00625v1 | mupdfng | first_page | miss | 30 | 227.181263 | 240.963220 | 241.226678 |
| 2609.00625v1 | mupdfng | random | hit | 420 | 0.000621 | 0.006109 | 0.013279 |
| 2609.00625v1 | mupdfng | revisit | hit | 420 | 0.000351 | 0.000701 | 0.000921 |
| 2609.00625v1 | mupdfng | sequential | miss | 390 | 100.466383 | 980.739814 | 1032.317256 |
| 2609.00625v1 | poppler | first_page | miss | 30 | 645.571146 | 651.901500 | 652.217037 |
| 2609.00625v1 | poppler | random | hit | 420 | 0.000360 | 0.005788 | 0.007121 |
| 2609.00625v1 | poppler | revisit | hit | 420 | 0.000350 | 0.000391 | 0.000751 |
| 2609.00625v1 | poppler | sequential | miss | 390 | 238.202350 | 2814.562282 | 2906.520661 |
| 2609.09123v1 | mupdfng | first_page | miss | 30 | 33.545966 | 35.243432 | 38.575437 |
| 2609.09123v1 | mupdfng | random | hit | 537 | 0.000581 | 0.009183 | 0.091554 |
| 2609.09123v1 | mupdfng | random | miss | 63 | 254.650322 | 274.234332 | 274.873498 |
| 2609.09123v1 | mupdfng | revisit | hit | 600 | 0.000351 | 0.000641 | 0.007592 |
| 2609.09123v1 | mupdfng | sequential | miss | 570 | 19.183802 | 1863.219724 | 1917.374342 |
| 2609.09123v1 | poppler | first_page | miss | 30 | 33.555591 | 34.695456 | 35.292525 |
| 2609.09123v1 | poppler | random | hit | 537 | 0.000631 | 0.008423 | 0.155348 |
| 2609.09123v1 | poppler | random | miss | 63 | 1023.651009 | 1273.193065 | 1277.873175 |
| 2609.09123v1 | poppler | revisit | hit | 600 | 0.000370 | 0.000711 | 0.007591 |
| 2609.09123v1 | poppler | sequential | miss | 570 | 38.981235 | 1720.652200 | 1817.520489 |
| 2610.26067v1 | mupdfng | first_page | miss | 30 | 45.854111 | 47.427989 | 47.501111 |
| 2610.26067v1 | mupdfng | random | hit | 480 | 0.000390 | 0.004416 | 0.009704 |
| 2610.26067v1 | mupdfng | revisit | hit | 480 | 0.000341 | 0.000390 | 0.000741 |
| 2610.26067v1 | mupdfng | sequential | miss | 450 | 108.616162 | 827.282213 | 837.104231 |
| 2610.26067v1 | poppler | first_page | miss | 30 | 48.748721 | 51.792201 | 51.824507 |
| 2610.26067v1 | poppler | random | hit | 480 | 0.000350 | 0.004697 | 0.007631 |
| 2610.26067v1 | poppler | revisit | hit | 480 | 0.000341 | 0.000381 | 0.000511 |
| 2610.26067v1 | poppler | sequential | miss | 450 | 442.283597 | 3946.657240 | 4183.925215 |
| 2312.00752v2 | mupdfng | first_page | miss | 30 | 87.860514 | 92.994240 | 102.946018 |
| 2312.00752v2 | mupdfng | random | hit | 409 | 0.000751 | 0.005629 | 0.017225 |
| 2312.00752v2 | mupdfng | random | miss | 191 | 24.015560 | 30.078136 | 32.222667 |
| 2312.00752v2 | mupdfng | revisit | hit | 600 | 0.000391 | 0.000821 | 0.021963 |
| 2312.00752v2 | mupdfng | sequential | miss | 570 | 27.727217 | 36.862328 | 43.672263 |
| 2312.00752v2 | poppler | first_page | miss | 30 | 63.819763 | 65.111132 | 65.654083 |
| 2312.00752v2 | poppler | random | hit | 409 | 0.000641 | 0.006259 | 0.007341 |
| 2312.00752v2 | poppler | random | miss | 191 | 52.064801 | 64.022401 | 71.490215 |
| 2312.00752v2 | poppler | revisit | hit | 600 | 0.000380 | 0.000691 | 0.006931 |
| 2312.00752v2 | poppler | sequential | miss | 570 | 59.709627 | 65.260368 | 75.513816 |
| 2307.03109v9 | mupdfng | first_page | miss | 30 | 56.017156 | 56.854625 | 57.671857 |
| 2307.03109v9 | mupdfng | random | hit | 351 | 0.000841 | 0.006580 | 0.014362 |
| 2307.03109v9 | mupdfng | random | miss | 249 | 27.539305 | 37.164837 | 41.513587 |
| 2307.03109v9 | mupdfng | revisit | hit | 600 | 0.000586 | 0.000841 | 0.009344 |
| 2307.03109v9 | mupdfng | sequential | miss | 570 | 22.693378 | 57.323758 | 60.756491 |
| 2307.03109v9 | poppler | first_page | miss | 30 | 60.408417 | 61.124830 | 61.754906 |
| 2307.03109v9 | poppler | random | hit | 351 | 0.000751 | 0.006740 | 0.007622 |
| 2307.03109v9 | poppler | random | miss | 249 | 55.407425 | 63.210535 | 69.716943 |
| 2307.03109v9 | poppler | revisit | hit | 600 | 0.000591 | 0.000761 | 0.006590 |
| 2307.03109v9 | poppler | sequential | miss | 570 | 51.077103 | 66.727215 | 69.080416 |

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
  "protocol_sha256": "bf385924965f88d8cdbd957c1268eb850f4e3f7aa24fe926d210e6c33dba8275",
  "source_commit": "719a45dc838b57fb452312596f02749590f241e4",
  "source_dirty": false,
  "benchmark_commit": "5108d5b9c40398f0981336d8d4beb173861a3a19",
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

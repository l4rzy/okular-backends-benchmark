# PDF backend benchmark

MuPDF-NG commit / package: okular-mupdf-ng 0.6.5-1.

Benchmark commit: `c7d4e69a8764f81e8de619d8684eaad91b6296c1`.

Run: [44864767601-1](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/44864767601), 2026-11-21T04:37:34.734690+00:00.

**Median paired rendering ratio: 2.241×** (95% bootstrap interval 2.235–2.246×).

Ratio = Poppler time / MuPDF-NG time; above 1 favors MuPDF-NG. Each trial uses the geometric mean of document ratios, giving each PDF equal weight. The headline is the median of those trial scores. The primary workload sums first-page and sequential-render request times, excluding document opening and worker startup. The worker stays alive for all requests in a trial.

MuPDF-NG uses **Relaxed sandbox enforcement**: available worker protections remain active, and incomplete host hardening does not block document opening.

300 successful backend trials; 30 pairs per PDF; series `dd091ea8771b11a9`.

## Per-document results

Times are medians in milliseconds. Ratios are medians of paired ratios, not ratios of medians.

| PDF | Pages | Render ratio | MuPDF-NG render batch | Poppler render batch | MuPDF-NG open → first page | Poppler open → first page |
|---|---:|---:|---:|---:|---:|---:|
| 2609.00625v1 | 14 | 2.406× | 2739.756 | 6573.561 | 232.781 | 592.675 |
| 2609.09123v1 | 24 | 1.786× | 2706.731 | 4831.062 | 56.305 | 44.381 |
| 2610.26067v1 | 16 | 3.638× | 3283.394 | 11922.060 | 71.593 | 59.985 |
| 2312.00752v2 | 36 | 1.901× | 638.910 | 1211.402 | 98.935 | 72.375 |
| 2307.03109v9 | 45 | 1.906× | 566.898 | 1078.977 | 80.407 | 74.208 |

## Individual requests

Times are milliseconds; p95 is shown only for at least 20 samples. Cache hits are separate.

| PDF | Backend | Phase | Cache | N | Median | p95 | Maximum |
|---|---|---|---|---:|---:|---:|---:|
| 2609.00625v1 | mupdfng | first_page | miss | 30 | 207.871473 | 210.837809 | 212.100321 |
| 2609.00625v1 | mupdfng | random | hit | 420 | 0.000402 | 0.007786 | 0.022008 |
| 2609.00625v1 | mupdfng | revisit | hit | 420 | 0.000298 | 0.000442 | 0.001244 |
| 2609.00625v1 | mupdfng | sequential | miss | 390 | 102.572316 | 910.697351 | 966.101890 |
| 2609.00625v1 | poppler | first_page | miss | 30 | 583.767443 | 604.647608 | 605.327591 |
| 2609.00625v1 | poppler | random | hit | 420 | 0.000318 | 0.007694 | 0.012362 |
| 2609.00625v1 | poppler | revisit | hit | 420 | 0.000293 | 0.000337 | 0.012901 |
| 2609.00625v1 | poppler | sequential | miss | 390 | 224.717793 | 2474.184507 | 2517.831429 |
| 2609.09123v1 | mupdfng | first_page | miss | 30 | 30.437039 | 32.538236 | 37.788311 |
| 2609.09123v1 | mupdfng | random | hit | 537 | 0.000411 | 0.010479 | 0.089995 |
| 2609.09123v1 | mupdfng | random | miss | 63 | 241.803218 | 268.019458 | 279.652412 |
| 2609.09123v1 | mupdfng | revisit | hit | 600 | 0.000320 | 0.000564 | 0.015186 |
| 2609.09123v1 | mupdfng | sequential | miss | 570 | 20.675494 | 1557.349308 | 1613.820886 |
| 2609.09123v1 | poppler | first_page | miss | 30 | 37.430347 | 40.906262 | 48.877430 |
| 2609.09123v1 | poppler | random | hit | 537 | 0.000450 | 0.009489 | 0.120779 |
| 2609.09123v1 | poppler | random | miss | 63 | 899.064657 | 1124.988893 | 1160.633930 |
| 2609.09123v1 | poppler | revisit | hit | 600 | 0.000443 | 0.000792 | 0.009759 |
| 2609.09123v1 | poppler | sequential | miss | 570 | 43.759625 | 1663.055120 | 1790.292943 |
| 2610.26067v1 | mupdfng | first_page | miss | 30 | 45.383725 | 46.415985 | 46.562674 |
| 2610.26067v1 | mupdfng | random | hit | 480 | 0.000382 | 0.007791 | 0.046836 |
| 2610.26067v1 | mupdfng | revisit | hit | 480 | 0.000296 | 0.000350 | 0.001398 |
| 2610.26067v1 | mupdfng | sequential | miss | 450 | 105.123175 | 848.119357 | 892.638257 |
| 2610.26067v1 | poppler | first_page | miss | 30 | 52.336844 | 53.089148 | 53.265938 |
| 2610.26067v1 | poppler | random | hit | 480 | 0.000319 | 0.007028 | 0.034127 |
| 2610.26067v1 | poppler | revisit | hit | 480 | 0.000297 | 0.000356 | 0.022086 |
| 2610.26067v1 | poppler | sequential | miss | 450 | 399.274309 | 3499.203402 | 3574.697063 |
| 2312.00752v2 | mupdfng | first_page | miss | 30 | 76.280473 | 78.534149 | 79.539146 |
| 2312.00752v2 | mupdfng | random | hit | 409 | 0.000513 | 0.008537 | 0.026302 |
| 2312.00752v2 | mupdfng | random | miss | 191 | 25.442927 | 31.165948 | 34.993060 |
| 2312.00752v2 | mupdfng | revisit | hit | 600 | 0.000333 | 0.000972 | 0.008746 |
| 2312.00752v2 | mupdfng | sequential | miss | 570 | 29.134265 | 37.983582 | 46.751602 |
| 2312.00752v2 | poppler | first_page | miss | 30 | 65.795276 | 66.837788 | 67.058268 |
| 2312.00752v2 | poppler | random | hit | 409 | 0.000487 | 0.008935 | 0.017799 |
| 2312.00752v2 | poppler | random | miss | 191 | 54.139693 | 65.505827 | 83.744757 |
| 2312.00752v2 | poppler | revisit | hit | 600 | 0.000330 | 0.000512 | 0.008167 |
| 2312.00752v2 | poppler | sequential | miss | 570 | 61.096282 | 65.815097 | 87.894007 |
| 2307.03109v9 | mupdfng | first_page | miss | 30 | 53.071133 | 56.843734 | 58.716605 |
| 2307.03109v9 | mupdfng | random | hit | 351 | 0.000739 | 0.009187 | 0.084980 |
| 2307.03109v9 | mupdfng | random | miss | 249 | 29.215970 | 37.262811 | 39.285601 |
| 2307.03109v9 | mupdfng | revisit | hit | 600 | 0.000371 | 0.001320 | 0.009769 |
| 2307.03109v9 | mupdfng | sequential | miss | 570 | 24.317065 | 54.038235 | 73.865533 |
| 2307.03109v9 | poppler | first_page | miss | 30 | 63.139942 | 64.551579 | 65.130242 |
| 2307.03109v9 | poppler | random | hit | 351 | 0.000559 | 0.009486 | 0.016243 |
| 2307.03109v9 | poppler | random | miss | 249 | 58.406060 | 66.882515 | 71.678789 |
| 2307.03109v9 | poppler | revisit | hit | 600 | 0.000453 | 0.000556 | 0.009829 |
| 2307.03109v9 | poppler | sequential | miss | 570 | 54.463594 | 68.957739 | 86.266197 |

## Environment

```json
{
  "platform": "Linux-7.0.0-1020-azure-x86_64-with-glibc2.44",
  "machine": "x86_64",
  "cpu_model": "INTEL(R) XEON(R) PLATINUM 8573C",
  "logical_cpus": 4,
  "available_cpus": 4,
  "python": "3.14.10",
  "plugin_build": {},
  "protocol": "pdf-render-v1",
  "protocol_sha256": "8843c572bb81fb24fee3e7877bad432760f205c338332af06e938d80950fa7b2",
  "mupdf_package": {
    "name": "okular-mupdf-ng",
    "version": "okular-mupdf-ng 0.6.5-1",
    "plugin_sha256": "fcbeda5993cfa6b2d492f8169528b3763abd26438e624cd92557873534c8c093"
  },
  "source_commit": null,
  "source_dirty": false,
  "benchmark_commit": "c7d4e69a8764f81e8de619d8684eaad91b6296c1",
  "benchmark_dirty": false,
  "runner_image": "local",
  "runner_image_version": "local",
  "container_image": "archlinux:latest",
  "versions": {
    "poppler": "26.11.0",
    "okular": "okular 26.08.3",
    "compiler": "c++ (GCC) 16.2.1 20260810\nCopyright (C) 2026 Free Software Foundation, Inc.\nThis is free software; see the source for copying conditions.  There is NO\nwarranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.",
    "mupdf": "okular-mupdf-ng 0.6.5-1"
  }
}
```

## Interpretation limits

Paired trials reduce host-speed noise, but CPU architectures can favor the backends differently. Graph lines group runs by CPU model and Poppler version; other environment and benchmark settings remain recorded in the reports. Bootstrap intervals resample whole paired trial scores; repeated pages are not independent samples of all PDFs. This is an offscreen rendering benchmark, not a GUI scrolling, memory, or visual-fidelity measurement. OS file caches are warm/uncontrolled. No performance merge gate is applied.

Okular warning-bearing trials: 150. See `summary.json` and `samples.jsonl.gz` for details.

Artifacts: [summary](summary.json), [raw trials](samples.jsonl.gz), [corpus manifest](corpus-manifest.json).

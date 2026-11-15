# PDF backend benchmark

MuPDF-NG commit / package: okular-mupdf-ng 0.6.4-1.

Benchmark commit: `9edbeaf45aca3f7750887d6fa830681945ae9d8c`.

Run: [43747655757-1](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/43747655757), 2026-11-15T18:52:59.793559+00:00.

**Median paired rendering ratio: 2.092×** (95% bootstrap interval 2.084–2.100×).

Ratio = Poppler time / MuPDF-NG time; above 1 favors MuPDF-NG. Each trial uses the geometric mean of document ratios, giving each PDF equal weight. The headline is the median of those trial scores. The primary workload sums first-page and sequential-render request times, excluding document opening and worker startup. The worker stays alive for all requests in a trial.

MuPDF-NG uses **Relaxed sandbox enforcement**: available worker protections remain active, and incomplete host hardening does not block document opening.

300 successful backend trials; 30 pairs per PDF; series `d6f00d0bb1a1cd44`.

## Per-document results

Times are medians in milliseconds. Ratios are medians of paired ratios, not ratios of medians.

| PDF | Pages | Render ratio | MuPDF-NG render batch | Poppler render batch | MuPDF-NG open → first page | Poppler open → first page |
|---|---:|---:|---:|---:|---:|---:|
| 2609.00625v1 | 14 | 2.218× | 1735.916 | 3847.786 | 156.737 | 336.592 |
| 2609.09123v1 | 24 | 1.837× | 1602.086 | 2972.392 | 40.178 | 26.298 |
| 2610.26067v1 | 16 | 3.510× | 1991.120 | 6997.164 | 47.031 | 35.326 |
| 2312.00752v2 | 36 | 1.692× | 420.198 | 715.744 | 68.728 | 44.678 |
| 2307.03109v9 | 45 | 1.670× | 375.760 | 626.544 | 56.010 | 46.597 |

## Individual requests

Times are milliseconds; p95 is shown only for at least 20 samples. Cache hits are separate.

| PDF | Backend | Phase | Cache | N | Median | p95 | Maximum |
|---|---|---|---|---:|---:|---:|---:|
| 2609.00625v1 | mupdfng | first_page | miss | 30 | 138.202441 | 140.978748 | 141.752559 |
| 2609.00625v1 | mupdfng | random | hit | 420 | 0.000200 | 0.008713 | 0.020230 |
| 2609.00625v1 | mupdfng | revisit | hit | 420 | 0.000190 | 0.000310 | 0.000641 |
| 2609.00625v1 | mupdfng | sequential | miss | 390 | 61.769933 | 584.412586 | 622.236335 |
| 2609.00625v1 | poppler | first_page | miss | 30 | 330.573778 | 345.386812 | 397.863097 |
| 2609.00625v1 | poppler | random | hit | 420 | 0.000190 | 0.007591 | 0.115675 |
| 2609.00625v1 | poppler | revisit | hit | 420 | 0.000181 | 0.000291 | 0.000341 |
| 2609.00625v1 | poppler | sequential | miss | 390 | 134.772885 | 1440.480982 | 1524.024669 |
| 2609.09123v1 | mupdfng | first_page | miss | 30 | 21.941560 | 23.870140 | 30.874664 |
| 2609.09123v1 | mupdfng | random | hit | 537 | 0.000281 | 0.009565 | 0.125230 |
| 2609.09123v1 | mupdfng | random | miss | 63 | 143.581571 | 156.805191 | 165.824304 |
| 2609.09123v1 | mupdfng | revisit | hit | 600 | 0.000190 | 0.000321 | 0.010626 |
| 2609.09123v1 | mupdfng | sequential | miss | 570 | 14.059238 | 861.200619 | 956.489552 |
| 2609.09123v1 | poppler | first_page | miss | 30 | 21.621302 | 23.051634 | 23.655802 |
| 2609.09123v1 | poppler | random | hit | 537 | 0.000291 | 0.008893 | 0.120592 |
| 2609.09123v1 | poppler | random | miss | 63 | 600.974396 | 756.161833 | 789.613321 |
| 2609.09123v1 | poppler | revisit | hit | 600 | 0.000281 | 0.000331 | 0.010206 |
| 2609.09123v1 | poppler | sequential | miss | 570 | 24.657255 | 1037.367911 | 1199.059583 |
| 2610.26067v1 | mupdfng | first_page | miss | 30 | 28.381574 | 29.577048 | 30.038981 |
| 2610.26067v1 | mupdfng | random | hit | 480 | 0.000190 | 0.004106 | 0.009234 |
| 2610.26067v1 | mupdfng | revisit | hit | 480 | 0.000180 | 0.000191 | 0.011097 |
| 2610.26067v1 | mupdfng | sequential | miss | 450 | 66.889643 | 503.098728 | 542.191685 |
| 2610.26067v1 | poppler | first_page | miss | 30 | 30.391089 | 33.379125 | 33.874401 |
| 2610.26067v1 | poppler | random | hit | 480 | 0.000181 | 0.004717 | 0.010616 |
| 2610.26067v1 | poppler | revisit | hit | 480 | 0.000180 | 0.000191 | 0.000361 |
| 2610.26067v1 | poppler | sequential | miss | 450 | 234.892173 | 2107.767373 | 2151.469223 |
| 2312.00752v2 | mupdfng | first_page | miss | 30 | 52.182649 | 55.498625 | 56.333256 |
| 2312.00752v2 | mupdfng | random | hit | 409 | 0.000371 | 0.010145 | 0.022244 |
| 2312.00752v2 | mupdfng | random | miss | 191 | 16.929476 | 21.828994 | 26.901499 |
| 2312.00752v2 | mupdfng | revisit | hit | 600 | 0.000191 | 0.000360 | 0.009654 |
| 2312.00752v2 | mupdfng | sequential | miss | 570 | 19.504633 | 25.849978 | 37.068511 |
| 2312.00752v2 | poppler | first_page | miss | 30 | 39.917193 | 46.289230 | 49.375071 |
| 2312.00752v2 | poppler | random | hit | 409 | 0.000331 | 0.008423 | 0.011608 |
| 2312.00752v2 | poppler | random | miss | 191 | 32.386544 | 39.324740 | 42.595667 |
| 2312.00752v2 | poppler | revisit | hit | 600 | 0.000200 | 0.000351 | 0.008774 |
| 2312.00752v2 | poppler | sequential | miss | 570 | 35.874778 | 40.558070 | 67.685686 |
| 2307.03109v9 | mupdfng | first_page | miss | 30 | 35.521165 | 37.547063 | 39.472760 |
| 2307.03109v9 | mupdfng | random | hit | 351 | 0.000460 | 0.008874 | 0.019109 |
| 2307.03109v9 | mupdfng | random | miss | 249 | 18.837325 | 25.371202 | 44.342367 |
| 2307.03109v9 | mupdfng | revisit | hit | 600 | 0.000200 | 0.000421 | 0.010806 |
| 2307.03109v9 | mupdfng | sequential | miss | 570 | 16.086772 | 33.310109 | 38.542017 |
| 2307.03109v9 | poppler | first_page | miss | 30 | 38.824444 | 41.862538 | 42.079645 |
| 2307.03109v9 | poppler | random | hit | 351 | 0.000410 | 0.008693 | 0.016204 |
| 2307.03109v9 | poppler | random | miss | 249 | 34.021512 | 38.837220 | 48.501525 |
| 2307.03109v9 | poppler | revisit | hit | 600 | 0.000290 | 0.000381 | 0.010787 |
| 2307.03109v9 | poppler | sequential | miss | 570 | 31.545311 | 39.688738 | 46.148561 |

## Environment

```json
{
  "platform": "Linux-7.0.0-1019-azure-x86_64-with-glibc2.44",
  "machine": "x86_64",
  "cpu_model": "AMD EPYC 9V45 96-Core Processor",
  "logical_cpus": 4,
  "available_cpus": 4,
  "python": "3.14.10",
  "plugin_build": {},
  "protocol": "pdf-render-v1",
  "protocol_sha256": "8843c572bb81fb24fee3e7877bad432760f205c338332af06e938d80950fa7b2",
  "mupdf_package": {
    "name": "okular-mupdf-ng",
    "version": "okular-mupdf-ng 0.6.4-1",
    "plugin_sha256": "509b88133744dd354b5ce74ee41bf5ab6ba61c352a1f84e17fdbfe1dce48825b"
  },
  "source_commit": null,
  "source_dirty": false,
  "benchmark_commit": "9edbeaf45aca3f7750887d6fa830681945ae9d8c",
  "benchmark_dirty": false,
  "runner_image": "local",
  "runner_image_version": "local",
  "container_image": "archlinux:latest",
  "versions": {
    "poppler": "26.10.0",
    "okular": "okular 26.08.3",
    "compiler": "c++ (GCC) 16.2.1 20260810\nCopyright (C) 2026 Free Software Foundation, Inc.\nThis is free software; see the source for copying conditions.  There is NO\nwarranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.",
    "mupdf": "okular-mupdf-ng 0.6.4-1"
  }
}
```

## Interpretation limits

Paired trials reduce host-speed noise, but CPU architectures can favor the backends differently. Graph lines group runs by CPU model and Poppler version; other environment and benchmark settings remain recorded in the reports. Bootstrap intervals resample whole paired trial scores; repeated pages are not independent samples of all PDFs. This is an offscreen rendering benchmark, not a GUI scrolling, memory, or visual-fidelity measurement. OS file caches are warm/uncontrolled. No performance merge gate is applied.

Okular warning-bearing trials: 150. See `summary.json` and `samples.jsonl.gz` for details.

Artifacts: [summary](summary.json), [raw trials](samples.jsonl.gz), [corpus manifest](corpus-manifest.json).

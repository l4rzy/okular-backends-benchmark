# PDF backend benchmark

MuPDF-NG commit / package: okular-mupdf-ng 0.6.3-1.

Benchmark commit: `41d033d6a8161e497c11d4a895523ad5fa0fa10f`.

Run: [43651081683-1](https://github.com/l4rzy/okular-backends-benchmark/actions/runs/43651081683), 2026-11-14T23:29:52.404437+00:00.

**Median paired rendering ratio: 2.186×** (95% bootstrap interval 2.180–2.193×).

Ratio = Poppler time / MuPDF-NG time; above 1 favors MuPDF-NG. Each trial uses the geometric mean of document ratios, giving each PDF equal weight. The headline is the median of those trial scores. The primary workload sums first-page and sequential-render request times, excluding document opening and worker startup. The worker stays alive for all requests in a trial.

MuPDF-NG uses **Relaxed sandbox enforcement**: available worker protections remain active, and incomplete host hardening does not block document opening.

300 successful backend trials; 30 pairs per PDF; series `d0bde77ecbb45297`.

## Per-document results

Times are medians in milliseconds. Ratios are medians of paired ratios, not ratios of medians.

| PDF | Pages | Render ratio | MuPDF-NG render batch | Poppler render batch | MuPDF-NG open → first page | Poppler open → first page |
|---|---:|---:|---:|---:|---:|---:|
| 2609.00625v1 | 14 | 2.357× | 2953.510 | 6954.656 | 256.559 | 618.930 |
| 2609.09123v1 | 24 | 1.918× | 2722.569 | 5238.110 | 65.448 | 45.504 |
| 2610.26067v1 | 16 | 3.857× | 3420.278 | 13194.891 | 79.450 | 61.467 |
| 2312.00752v2 | 36 | 1.714× | 738.391 | 1261.435 | 112.760 | 77.313 |
| 2307.03109v9 | 45 | 1.681× | 670.749 | 1118.132 | 92.430 | 79.761 |

## Individual requests

Times are milliseconds; p95 is shown only for at least 20 samples. Cache hits are separate.

| PDF | Backend | Phase | Cache | N | Median | p95 | Maximum |
|---|---|---|---|---:|---:|---:|---:|
| 2609.00625v1 | mupdfng | first_page | miss | 30 | 229.464753 | 240.441827 | 245.686043 |
| 2609.00625v1 | mupdfng | random | hit | 420 | 0.000661 | 0.006452 | 0.009799 |
| 2609.00625v1 | mupdfng | revisit | hit | 420 | 0.000356 | 0.000742 | 0.000931 |
| 2609.00625v1 | mupdfng | sequential | miss | 390 | 107.625760 | 968.326813 | 1009.004116 |
| 2609.00625v1 | poppler | first_page | miss | 30 | 609.452787 | 651.891563 | 659.288087 |
| 2609.00625v1 | poppler | random | hit | 420 | 0.000450 | 0.006291 | 0.023093 |
| 2609.00625v1 | poppler | revisit | hit | 420 | 0.000431 | 0.000501 | 0.022932 |
| 2609.00625v1 | poppler | sequential | miss | 390 | 235.318376 | 2609.882811 | 2661.462624 |
| 2609.09123v1 | mupdfng | first_page | miss | 30 | 38.163604 | 39.135162 | 39.180853 |
| 2609.09123v1 | mupdfng | random | hit | 537 | 0.000561 | 0.007104 | 0.016130 |
| 2609.09123v1 | mupdfng | random | miss | 63 | 246.827320 | 265.085263 | 282.577945 |
| 2609.09123v1 | mupdfng | revisit | hit | 600 | 0.000360 | 0.000782 | 0.015469 |
| 2609.09123v1 | mupdfng | sequential | miss | 570 | 26.005615 | 1472.537022 | 1529.034236 |
| 2609.09123v1 | poppler | first_page | miss | 30 | 38.224688 | 41.353639 | 42.850727 |
| 2609.09123v1 | poppler | random | hit | 537 | 0.000631 | 0.006712 | 0.126887 |
| 2609.09123v1 | poppler | random | miss | 63 | 1057.244328 | 1369.121486 | 1388.941785 |
| 2609.09123v1 | poppler | revisit | hit | 600 | 0.000461 | 0.000742 | 0.007283 |
| 2609.09123v1 | poppler | sequential | miss | 570 | 44.300621 | 1673.300380 | 1765.745873 |
| 2610.26067v1 | mupdfng | first_page | miss | 30 | 51.776260 | 56.292041 | 56.757752 |
| 2610.26067v1 | mupdfng | random | hit | 480 | 0.000661 | 0.006292 | 0.018304 |
| 2610.26067v1 | mupdfng | revisit | hit | 480 | 0.000350 | 0.000391 | 0.016231 |
| 2610.26067v1 | mupdfng | sequential | miss | 450 | 115.758296 | 841.127691 | 885.788614 |
| 2610.26067v1 | poppler | first_page | miss | 30 | 53.530734 | 55.116562 | 55.402606 |
| 2610.26067v1 | poppler | random | hit | 480 | 0.000441 | 0.005881 | 0.006993 |
| 2610.26067v1 | poppler | revisit | hit | 480 | 0.000431 | 0.000531 | 0.015639 |
| 2610.26067v1 | poppler | sequential | miss | 450 | 450.929229 | 3878.696496 | 3942.433914 |
| 2312.00752v2 | mupdfng | first_page | miss | 30 | 88.611965 | 90.064629 | 90.266939 |
| 2312.00752v2 | mupdfng | random | hit | 409 | 0.000811 | 0.007514 | 0.010159 |
| 2312.00752v2 | mupdfng | random | miss | 191 | 29.474794 | 35.874804 | 38.242794 |
| 2312.00752v2 | mupdfng | revisit | hit | 600 | 0.000396 | 0.000911 | 0.015750 |
| 2312.00752v2 | mupdfng | sequential | miss | 570 | 33.954938 | 42.783914 | 60.421886 |
| 2312.00752v2 | poppler | first_page | miss | 30 | 69.636356 | 76.802808 | 105.033070 |
| 2312.00752v2 | poppler | random | hit | 409 | 0.000701 | 0.006983 | 0.013636 |
| 2312.00752v2 | poppler | random | miss | 191 | 55.758550 | 68.274139 | 69.761547 |
| 2312.00752v2 | poppler | revisit | hit | 600 | 0.000470 | 0.000751 | 0.026018 |
| 2312.00752v2 | poppler | sequential | miss | 570 | 63.742779 | 70.241530 | 95.896371 |
| 2307.03109v9 | mupdfng | first_page | miss | 30 | 62.319692 | 63.838999 | 64.195188 |
| 2307.03109v9 | mupdfng | random | hit | 351 | 0.000952 | 0.007695 | 0.008596 |
| 2307.03109v9 | mupdfng | random | miss | 249 | 33.997222 | 44.065235 | 53.898618 |
| 2307.03109v9 | mupdfng | revisit | hit | 600 | 0.000626 | 0.000882 | 0.008787 |
| 2307.03109v9 | mupdfng | sequential | miss | 570 | 29.165514 | 59.416921 | 64.215669 |
| 2307.03109v9 | poppler | first_page | miss | 30 | 66.845877 | 71.585912 | 72.874382 |
| 2307.03109v9 | poppler | random | hit | 351 | 0.000782 | 0.007043 | 0.021720 |
| 2307.03109v9 | poppler | random | miss | 249 | 60.492554 | 69.416174 | 80.809233 |
| 2307.03109v9 | poppler | revisit | hit | 600 | 0.000611 | 0.000781 | 0.022432 |
| 2307.03109v9 | poppler | sequential | miss | 570 | 56.758002 | 73.125824 | 88.596269 |

## Environment

```json
{
  "platform": "Linux-7.0.0-1019-azure-x86_64-with-glibc2.44",
  "machine": "x86_64",
  "cpu_model": "AMD EPYC 7763 64-Core Processor",
  "logical_cpus": 4,
  "available_cpus": 4,
  "python": "3.14.10",
  "plugin_build": {},
  "protocol": "pdf-render-v1",
  "protocol_sha256": "8843c572bb81fb24fee3e7877bad432760f205c338332af06e938d80950fa7b2",
  "mupdf_package": {
    "name": "okular-mupdf-ng",
    "version": "okular-mupdf-ng 0.6.3-1",
    "plugin_sha256": "b19952a915905e8d56dd77e465494a42eb11f5ed7572a6192ef205e9c683774b"
  },
  "source_commit": null,
  "source_dirty": false,
  "benchmark_commit": "41d033d6a8161e497c11d4a895523ad5fa0fa10f",
  "benchmark_dirty": false,
  "runner_image": "local",
  "runner_image_version": "local",
  "container_image": "archlinux:latest",
  "versions": {
    "poppler": "26.10.0",
    "okular": "okular 26.08.3",
    "compiler": "c++ (GCC) 16.2.1 20260810\nCopyright (C) 2026 Free Software Foundation, Inc.\nThis is free software; see the source for copying conditions.  There is NO\nwarranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.",
    "mupdf": "okular-mupdf-ng 0.6.3-1"
  }
}
```

## Interpretation limits

Paired trials reduce host-speed noise, but CPU architectures can favor the backends differently. Graph lines group runs by CPU model and Poppler version; other environment and benchmark settings remain recorded in the reports. Bootstrap intervals resample whole paired trial scores; repeated pages are not independent samples of all PDFs. This is an offscreen rendering benchmark, not a GUI scrolling, memory, or visual-fidelity measurement. OS file caches are warm/uncontrolled. No performance merge gate is applied.

Okular warning-bearing trials: 150. See `summary.json` and `samples.jsonl.gz` for details.

Artifacts: [summary](summary.json), [raw trials](samples.jsonl.gz), [corpus manifest](corpus-manifest.json).

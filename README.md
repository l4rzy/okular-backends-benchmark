# Okular Backends Benchmark

Versioned PDF corpus and historical performance comparisons for Okular backends.

## Corpus v1

These unmodified PDFs were downloaded from the versioned arXiv URLs listed below. Each paper links to the Creative Commons Attribution 4.0 license on its arXiv abstract page. The papers retain their original copyright and license notices. Their inclusion does not imply endorsement by the authors or arXiv.

| Paper | Version | Pages | Size (MiB) | License |
|---|---|---:|---:|---|
| [Inverse Rendering for Modeling with Line Primitives](https://arxiv.org/abs/2609.00625v1) | [2609.00625v1](corpus/arxiv/2609.00625v1.pdf) | 14 | 47.58 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| [Mask Forcing: Improving Autoregressive Video Diffusion Distillation via Dual-Noise Masking Rollout](https://arxiv.org/abs/2609.09123v1) | [2609.09123v1](corpus/arxiv/2609.09123v1.pdf) | 24 | 46.61 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| [PhysSkin++: Real-Time and Generalizable Physics-Based Animation via Self-Supervised Neural Skinning](https://arxiv.org/abs/2610.26067v1) | [2610.26067v1](corpus/arxiv/2610.26067v1.pdf) | 16 | 42.45 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

## Attribution

### Inverse Rendering for Modeling with Line Primitives

Kenji Tojo, Ariel Shamir, Nobuyuki Umetani, Bernd Bickel.

Original version: [2609.00625v1](https://arxiv.org/abs/2609.00625v1). [Original PDF](https://arxiv.org/pdf/2609.00625v1). Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). No changes were made to the PDF.

### Mask Forcing: Improving Autoregressive Video Diffusion Distillation via Dual-Noise Masking Rollout

Zhuoran Zhao, Shengju Qian, Tongtong Liang, Xianghao Kong, Songchun Zhang, Junchao Huang, Guian Fang, Xin Wang, Pan Hui, Anyi Rao.

Original version: [2609.09123v1](https://arxiv.org/abs/2609.09123v1). [Original PDF](https://arxiv.org/pdf/2609.09123v1). Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). No changes were made to the PDF.

### PhysSkin++: Real-Time and Generalizable Physics-Based Animation via Self-Supervised Neural Skinning

Yuanhang Lei, Baofei Liu, Xingxuan Li, Tao Cheng, Zixuan Wang, Boming Zhao, Yujun Shen, Siyuan Huang, Ruizhen Hu, Peter Yichen Chen, Hujun Bao, Zhaopeng Cui.

Original version: [2610.26067v1](https://arxiv.org/abs/2610.26067v1). [Original PDF](https://arxiv.org/pdf/2610.26067v1). Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). No changes were made to the PDF.

## Integrity and reproducibility

`corpus/manifest.json` records versioned sources, authors, license links, page counts, byte sizes, and SHA-256 hashes. The corpus contains only the three identified arXiv papers; other local books and documents are not included.

Verify files from the repository root:

```sh
sha256sum --check corpus/SHA256SUMS
```

Keep these corpus v1 files unchanged. Future additions or replacements should increment the corpus version so historical benchmark results remain comparable.

## Licensing

The PDF papers are third-party works licensed individually under CC BY 4.0, as recorded in the manifest and attribution above. Retain the author credits, source links, and license information when redistributing them.

Benchmark automation and result history will be added separately.

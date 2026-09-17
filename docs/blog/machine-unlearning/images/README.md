# Paper figures used in the article

The English and Chinese articles share these nine PNG crops. The opening has
one, and every main body section has at least one. Captions in both articles identify the
authors, original figure number, PDF page, source link, and what the figure shows.
The original labels and experimental results are preserved; these are not new
experiments or redrawn illustrations.

| Article figure | PNG | Paper and pinned source | Original figure | PDF page |
|---|---|---|---|---|
| 1 | `cao-yang-figure-1.png` | [Cao and Yang, Towards Making Systems Forget with Machine Unlearning, author copy](https://yinzhicao.org/unlearning/UnlearningOakland15.pdf) | 1 | 2 |
| 2 | `sisa-figure-1.png` | [Bourtoule et al., Machine Unlearning, v3](https://arxiv.org/pdf/1912.03817v3) | 1 | 4 |
| 3 | `sisa-figure-2.png` | [Bourtoule et al., Machine Unlearning, v3](https://arxiv.org/pdf/1912.03817v3) | 2 | 6 |
| 4 | `certified-removal-figure-1.png` | [Guo et al., Certified Data Removal, ICML proceedings](https://proceedings.mlr.press/v119/guo20c/guo20c.pdf) | 1 | 6 |
| 5 | `federaser-figure-1.png` | [Liu et al., FedEraser / Federated Unlearning, v3](https://arxiv.org/pdf/2012.13891v3) | 1 | 5 |
| 6 | `tofu-figure-1.png` | [Maini et al., TOFU, v1](https://arxiv.org/pdf/2401.06121v1) | 1 | 1 |
| 7 | `scrub-figure-1.png` | [Kurmanji et al., Towards Unbounded Machine Unlearning, v3](https://arxiv.org/pdf/2302.09880v3) | 1 | 5 |
| 8 | `inversion-figure-1.png` | [Hu et al., Learn What You Want to Unlearn, v1](https://arxiv.org/pdf/2404.03233v1) | 1 | 2 |
| 9 | `certified-removal-figure-2.png` | [Guo et al., Certified Data Removal, ICML proceedings](https://proceedings.mlr.press/v119/guo20c/guo20c.pdf) | 2 | 7 |

## Capture details

Downloaded and visually checked on 2026-09-17. The Cao and Yang crop is
taken from the copy the first author hosts, which is the usual author copy
for an IEEE S&P paper; it is not on arXiv. Whole pages were previewed with
Poppler. The figure regions were rasterised from the source PDFs with PyMuPDF
at 288 dpi, retaining all panels, axes, legends, and original labels. Surrounding
paper prose and the original caption were excluded; the article provides its own
bilingual explanatory captions and explicit attribution. PNGs link to themselves
so readers can inspect the full-resolution originals.

`paper-figures.json` records the exact source URL, one-based PDF page number,
crop rectangle in PDF points (top-left origin), raster dimensions, and SHA-256
of each downloaded PDF. To reproduce a crop with PyMuPDF:

```python
page = fitz.open(downloaded_pdf)[entry["pdf_page"] - 1]
page.get_pixmap(
    matrix=fitz.Matrix(entry["dpi"] / 72, entry["dpi"] / 72),
    clip=fitz.Rect(entry["crop_points"]),
    alpha=False,
).save(entry["file"])
```

Attribution is to the original authors and publications. The repository does not
claim these reproduced figures as original artwork or grant a new license for
them. `definition.svg` and `taxonomy.svg` are legacy artwork; the revised article
does not load them. `cover.svg` remains the blog-index cover.

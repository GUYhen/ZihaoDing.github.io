# Post cover pictures

The picture on the left of each row in the blog panel. Point a post at one:

    { date: "2026-08-26", title: "...", excerpt: "...",
      cover: "blog/images/covers/federated.svg",
      href:  "blog/federated-unlearning.html" }

The path is relative to `docs/`, because `blog.html` lives there. Drop the
`cover` field and the row falls back to a plain tinted tile with the topic
tag (MU / FU / ...) on it --- fine, but a real picture reads better.

* Rendered at **116x84** (about 1.4:1 landscape), cropped with
  `object-fit: cover`, 10px rounded. Landscape art fits with no crop; a tall
  or square image loses its top and bottom, so keep the subject centred.
* Any format: `.svg .png .jpg .webp`. A figure from the post itself is the
  most useful cover --- a plot, a diagram, a screenshot.
* Keep bitmaps around 400px; they are only ever drawn small.

`federated.svg` and `notes.svg` are abstract stand-ins drawn in the site
palette. Replace them with real figures whenever the posts have some.

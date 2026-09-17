# The blog lives here

Everything blog-related is under `docs/blog/`. **One folder per post**, holding
that post's two language files and its own pictures. Nothing else goes loose in
here.

```
docs/
  blog.jemdoc  blog.html      the index page: the topic graph and the post panel
  blogpost.conf               jemdoc conf for posts (favicon path, MathJax)
  blog/
    README.md                 this file
    post.css  post.js         shared by every post -- layout, numbering, top bar
    icons/                    node icons for the graph on blog.html (not per-post)
    _template/                copy this to start a new post; never published
      _template.jemdoc  _template-zh.jemdoc
    machine-unlearning/       <-- one post
      machine-unlearning.jemdoc     English -> machine-unlearning.html
      machine-unlearning-zh.jemdoc  Chinese -> machine-unlearning-zh.html
      images/
        cover.svg             the picture shown on the blog index
        definition.svg        figures the post itself uses
    federated-unlearning/     <-- another post
      federated-unlearning.jemdoc
      federated-unlearning-zh.jemdoc
      images/
        cover.svg
```

## Starting a new post

1. `mkdir blog/<slug>/images` and copy the two files out of `blog/_template/`,
   renaming them `<slug>.jemdoc` and `<slug>-zh.jemdoc`.
2. In each file set `data-lang`, `data-date`, `data-topic` and point `data-alt`
   at the other language. Leave the first line alone; it is the same for every
   post:

   ```
   # jemdoc: menu{MENU}{blog.html}{../../}, nofooter, nodefaultcss, addcss{../../jemdoc.css}, addcss{../post}, addjs{../post}
   ```

3. Put the post's pictures in `blog/<slug>/images/` and reference them from the
   post as `images/whatever.svg` --- the path is relative to the post's own
   folder, which is the whole point of this layout.
4. Add an entry to `ROOT` in `docs/blog.jemdoc`, under the topic it belongs to:

   ```js
   { date: "2026-09-16", title: "...", excerpt: "...",
     cover: "blog/<slug>/images/cover.svg",
     href:  "blog/<slug>/<slug>.html" }
   ```

   Those two paths are relative to `docs/`, because `blog.html` lives there.

## Citations and figure references

Write them as inline raw spans; `post.js` fills in the numbers from the
reference list and the figure order, so nothing is numbered by hand:

```
Guo et al.{{<span class="cite" data-ref="guo2020"></span>}} show ...
... several at once{{<span class="cite" data-ref="guo2020 neel2021"></span>}}.
As {{<a class="figref" data-fig="1"></a>}} shows, ...
```

The keys are the `id=` attributes on the `<li>` items inside
`<div class="refs">`, written as `id="ref-guo2020"`. Numbering follows the
order of that list, so references can be reordered freely and every citation
in the prose follows along. An unknown key renders as `[?]` and logs a warning
to the browser console.

Two jemdoc traps worth knowing, both of which bit this post:

> **A `#` anywhere in prose silently truncates the rest of that line.** That
> is why figure references carry `data-fig="1"` rather than `href="#fig-1"`.
> If a line mysteriously loses its tail, look for a `#`.
>
> **A line that *starts* with `{{` starts a new paragraph.** Keep an inline
> marker off the beginning of a line, or rewrap the sentence, unless you
> actually want the break (a run-in `.lead` does).

## Building

Always from `docs/`, never from inside a post folder --- `menu{MENU}` is looked
up relative to the working directory.

```
cd docs
python ..\jemdoc -c blogpost.conf blog\<slug>\<slug>.jemdoc
python ..\jemdoc -c blogpost.conf blog\<slug>\<slug>-zh.jemdoc
python ..\jemdoc -c mysite.conf blog.jemdoc
```

Posts use `blogpost.conf` rather than `mysite.conf` only because they sit two
levels under `docs/` and need `../../favicon.png`. Keep the two files in step.

## Covers

The picture on the left of each row in the blog index panel.

* Drawn at **148x108** (about 1.4:1 landscape), cropped with `object-fit:
  cover`, 10px rounded. Landscape art fits with no crop; a tall or square image
  loses its top and bottom, so keep the subject centred.
* Any format: `.svg .png .jpg .webp`. A figure from the post itself is the most
  useful cover.
* Keep bitmaps around 400px wide; they are only ever drawn small.
* Drop the `cover` field and the row falls back to a tinted tile with the topic
  tag (MU / FU / ...) on it. Fine, but a real picture reads better.

## What the build does for you

`post.js` runs on every post and handles the top bar (back link to the blog and
the EN / 中文 switch), the kicker line above the title, section numbering,
the "In this post" box, figure numbers, footnote numbers, and the "back to all
posts" link at the foot. None of that is written by hand; it all comes from the
`postmeta` element at the top of the file.

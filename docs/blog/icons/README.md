# Blog graph icons

## What is here

**Microsoft Fluent Emoji** --- https://github.com/microsoft/fluentui-emoji ---
under the **MIT licence** (copy in `LICENSE-fluent-emoji.txt`). MIT means no
attribution line is needed on the page, unlike Flaticon's free tier.

Two styles of the same glyphs:

| folder | what | when |
|---|---|---|
| `3d/*.png` | rendered 3D cartoon, 256px | **in use** --- soft, playful, reads well small |
| `flat/*.svg` | flat 2D cartoon, vector | swap in if the 3D look feels too toy-like |

Switching the whole set is a find-and-replace in `docs/blog.jemdoc`:
`blog/icons/3d/` -> `blog/icons/flat/` and `.png` -> `.svg`.

## Currently wired up

| node | icon | why |
|---|---|---|
| MU | `brain` | the model's memory |
| FU | `busts` | several parties learning together |
| LLMU | `robot` | the language model |
| UV | `magnifier` | auditing that the data really went |

## The rest (spares to swap in)

`sponge` `broom` `trash` --- erasing, good alternatives for MU
`handshake` `globe` `link` `puzzle` `antenna` --- collaboration / distribution
`speech` --- language
`lock` `shield` `check` --- privacy, verification
`books` `abacus` `tube` --- surveys, theory, experiments

Judged on a contact sheet at real node size: `globe`, `link`, `speech`,
`trash`, `antenna` and `broom` are pale and wash out against the tinted
disc. `brain`, `busts`, `robot`, `magnifier`, `sponge`, `lock`, `check`
and `puzzle` hold up.

## Adding your own

Drop a file here and point a node at it:

    { abbr: "FU", icon: "blog/icons/3d/busts.png", ... }

The path is relative to `docs/`, because `blog.html` lives there. Any file
ending `.png .svg .webp .jpg .gif` switches the node into image mode: the
disc becomes a pale wash of the topic colour with a coloured ring, since a
full-colour icon is unreadable on a solid dark disc.

* **Size:** 256px is already 8x what is drawn (~32px); anything from 256px
  up is fine, 64px would look mushy on a retina screen.
* **Transparency:** transparent background, not a white square --- the node
  draws its own plate.
* **Consistency:** take them all from the same pack. Mixing packs is what
  makes an icon set look cheap.
* **Too small / too big:** the `img ? 1.06 : 0.82` factor in `blog.jemdoc`.

Flaticon was considered and dropped: its pack pages answer 403 to anything
automated, its free tier is PNG-only and needs a visible credit line, and a
PNG cannot be recoloured per node state. Fluent Emoji has none of those
problems.

---

Post **cover pictures** are a different thing and live in
`../images/covers/` --- see the note there.

# Notation rules for everything under `docs/`

Any math written on this site follows the same symbol discipline as the papers,
so a reader moving between a blog post and a paper never has to relearn what a
symbol means.

The source of truth for the papers is
`E:\TouGao\INFOCOM2027\CLAUDE.md`. This file restates the **symbol half** of it
for the website and adds the jemdoc mechanics, which the paper file does not
cover. If the two ever disagree about a symbol, the paper file wins.

---

## 1. The three slots

This is the core rule. Every index goes in exactly one place, decided by what
kind of index it is.

| What it indexes | Where it goes | Example |
|---|---|---|
| **Discrete time** — round, step | square brackets | `\boldsymbol{\theta}[t]`, `\boldsymbol{\theta}[t+1]` |
| **Entity** — client `k`, layer `\ell`, request `i`, sample `n` | subscript | `\mathcal{D}_k`, `\boldsymbol{\theta}_k` |
| **Identity tag** — forget, retain, unlearned, server, optimum | superscript, wrapped in `\textrm{}` | `\mathcal{D}^{\textrm{f}}`, `\boldsymbol{\theta}^{\textrm{unl}}` |

All three at once: `\boldsymbol{\theta}_{k}^{\textrm{C}}[t]` — client `k`'s
client-side parameter at round `t`.

Never write:

| Wrong | Why | Right |
|---|---|---|
| `\theta^{t+1}` | time as superscript | `\boldsymbol{\theta}[t+1]` |
| `\theta_{t+1}` | time as subscript | `\boldsymbol{\theta}[t+1]` |
| `\theta^S` | identity tag not wrapped, renders italic like a variable | `\boldsymbol{\theta}^{\textrm{S}}` |
| `X^{(i)}` | parenthetical superscript | subscript, or `[t]` if it is time, or rename |

The parenthetical superscript ban is absolute. It is the lazy way out of a
letter collision; resolve the collision instead. The only parentheses allowed in
math are function arguments and ordinary grouping.

## 2. Bold

* `\mathbf{}` — Latin vectors and matrices
* `\boldsymbol{}` — Greek vectors, so parameters are `\boldsymbol{\theta}`, never `\theta`
* scalars stay plain italic

## 3. `\textrm` vs `\mathrm`

* `\textrm{}` for short alphabetic **abbreviation tags** inside math: `f`, `r`,
  `unl`, `S`, `C`, `old`. They are words, so they get upright text-mode Roman.
  In sub- and superscripts this is the default.
* `\mathrm{}` only for **operator and function names** you have to define
  yourself, e.g. `\mathrm{top}_m`. LaTeX already gives you `\min`, `\max`,
  `\log`, `\Pr`.
* Symbolic markers need no wrapper: `\boldsymbol{\theta}^{\star}`.

## 4. One letter, one meaning

The lowercase, uppercase and calligraphic forms of one letter together carry
**one** concept, with the case distinguishing the role: lowercase = index,
uppercase = total, calligraphic = the object itself. `\mathcal{T}` and `T`
count as the same base letter, so they collide.

Reserved across this site:

| Symbol | Meaning |
|---|---|
| `\mathcal{D}` | the training set |
| `\mathcal{D}^{\textrm{f}}` / `\mathcal{D}^{\textrm{r}}` | forget set / retain set, `\mathcal{D}^{\textrm{r}} = \mathcal{D} \setminus \mathcal{D}^{\textrm{f}}` |
| `\mathcal{D}_k` | client `k`'s local dataset |
| `\mathcal{A}` | the training algorithm |
| `\mathcal{U}` | the unlearning algorithm |
| `\boldsymbol{\theta}` | model parameters |
| `\boldsymbol{\theta}^{\textrm{unl}}` | the unlearned model |
| `\boldsymbol{\theta}^{\star}` | the retrained reference, `\mathcal{A}(\mathcal{D}^{\textrm{r}})` |
| `\boldsymbol{\theta}[t]` | the global model at round `t` |
| `k` / `N` | client index / number of clients |
| `t` / `T` | round / total rounds |
| `\epsilon`, `\delta` | the unlearning (and differential privacy) budget |
| `\mathcal{S}` | a measurable set of models |
| `\mathcal{Q}^{\textrm{f}}` / `\mathcal{Q}^{\textrm{r}}` | forget and utility query sets, for LLM unlearning |

**`T` is fully reserved for rounds.** Do not also use `\mathcal{T}` for a task
or anything else. Before introducing a new symbol, check this table; if it
shares a base letter with something here, pick a different letter.

## 5. Introduce a symbol only if it earns its place

* Define it only if it is used again. A quantity that appears once goes in words.
* Do not declare a dimension or domain unless the letter is later used. Write
  `\boldsymbol{\theta} \in \mathbb{R}^{P}` only if `P` shows up again.
* Say what is being combined. Not "the union `\mathcal{D} = \bigcup_k
  \mathcal{D}_k`", but "let `\mathcal{D} = \bigcup_{k=1}^{N} \mathcal{D}_k`
  denote the union of all local datasets."
* Avoid "all clients share a model", which is ambiguous about whether they share
  an architecture, the parameters, or a copy. Write "the federation trains a
  model `f(\cdot;\boldsymbol{\theta})`".

---

## 6. Writing the math in jemdoc

The rules above are about notation. This section is about getting it through the
build, which is where most of the accidents happen.

| Where | Inline math | Display math |
|---|---|---|
| ordinary prose | `$ ... $` | a paragraph that is exactly `\( ... \)` |
| inside a `~~~ {}{raw} ~~~` block | `\( ... \)` | `\[ ... \]` |

jemdoc rewrites `$...$` into MathJax delimiters **only in ordinary text**. It
passes raw blocks through untouched, so a theorem box, a definition box or a
figure caption has to use MathJax's own delimiters directly.

A paragraph whose whole content is `\( ... \)` becomes centred display math. It
has to stand alone, with blank lines above and below.

MathJax on this site is 2.7.5, loaded from cdnjs and configured in
`mysite.conf` / `blogpost.conf`. `\mathcal`, `\boldsymbol`, `\textrm`,
`\mathbb`, `\stackrel`, `\Pr` and the AMS environments all work.

### Two traps that will bite you

* **A `#` anywhere in prose truncates the rest of that line**, not just at the
  start of a line. This is why figure references are written
  `{{<a class="figref" data-fig="1"></a>}}` and not `href="#fig-1"`.
* **A line that *starts* with `{{` starts a new paragraph.** Rewrap the sentence
  so an inline marker never lands at the beginning of a line, unless you want
  the break.

---

## 7. What this file is not

The papers' **prose** rules — no em-dashes, no `itemize` in body text, short
sentences, plain Anglo-Saxon words over Latinate ones — belong to the papers.
The blog has its own voice and does use lists and a looser register. Only the
symbol discipline carries over.

## 8. Related

* `docs/blog/README.md` — blog folder layout, how to start a post, the citation
  and figure-reference syntax, and the build commands.
* `docs/blog/_template/` — a worked example of every construct a post can use.

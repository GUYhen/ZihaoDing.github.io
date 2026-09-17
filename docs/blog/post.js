/* =====================================================================
   Blog post enhancements.

   Everything here is driven by one element the post declares:

     <div class="postmeta"
          data-topic="Federated Unlearning"
          data-date="August 26, 2026"
          data-lang="en"                       (en | zh)
          data-alt="federated-unlearning-zh.html"></div>

   From that this script builds the top bar (back link + language switch)
   and the kicker line, then numbers the sections, assembles the "in this
   post" box, numbers figures, and wires up footnote marks.

   It also resolves two markers the prose can drop inline:

     {{<span class="cite" data-ref="guo2020 neel2021"></span>}}
         becomes [4, 6], each number linking to that entry in the
         reference list.  The keys are the id= on the <li> items inside
         <div class="refs">, with or without the "ref-" prefix.  Numbering
         follows the order of the list, so references can be reordered
         freely and every citation follows.

     {{<a class="figref" data-fig="1"></a>}}
         becomes "Figure 1" / "图 1", linking to that figure.  The number
         goes in an attribute rather than an href because a '#' anywhere in
         jemdoc prose truncates the rest of the line.

   Loaded from the <head> via  addjs{post}, so it waits for DOM ready.  It
   is a no-op on any page without #layout-content.
   ===================================================================== */

(function () {
"use strict";

var STR = {
  en: { back: "Back to all posts", blog: "Blog", toc: "In this post",
        fig: "Figure", alt: "中文" },
  zh: { back: "返回文章列表", blog: "博客",
        toc: "本文目录", fig: "图", alt: "English" }
};

function esc(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function el(tag, cls, parent) {
  var n = document.createElement(tag);
  if (cls) { n.className = cls; }
  if (parent) { parent.appendChild(n); }
  return n;
}

function ready(fn) {
  if (document.readyState !== "loading") { fn(); }
  else { document.addEventListener("DOMContentLoaded", fn); }
}

ready(function () {
  var content = document.getElementById("layout-content");
  if (!content) { return; }

  /* ---- 1. move the body into one measured column ------------------ */

  var art = el("article", "chapter");
  while (content.firstChild) { art.appendChild(content.firstChild); }
  content.appendChild(art);

  var top = art.querySelector("#toptitle");
  var meta = art.querySelector(".postmeta");
  var d = function (k) { return meta ? (meta.getAttribute("data-" + k) || "") : ""; };

  var lang = d("lang") === "zh" ? "zh" : "en";
  var t = STR[lang];
  document.documentElement.setAttribute("lang", lang === "zh" ? "zh-CN" : "en");

  /* ---- 2. top bar: back link on the left, languages on the right -- */

  if (top) {
    var bar = el("div", "postbar");

    var back = el("a", "back", bar);
    back.href = "../../blog.html";
    back.innerHTML = "← " + t.blog;

    if (d("alt")) {
      var langs = el("span", "langs", bar);
      var here = el("span", "cur", langs);
      here.textContent = lang === "zh" ? "中文" : "EN";
      var other = el("a", null, langs);
      other.href = d("alt");
      other.textContent = t.alt;
    }

    art.insertBefore(bar, top);

    /* kicker: topic and date, above the title, like the book's
       "Chapter 1" line */
    var bits = [];
    if (d("topic")) { bits.push(d("topic")); }
    if (d("date")) { bits.push(d("date")); }
    if (bits.length) {
      var k = el("div", "kicker");
      k.textContent = bits.join(" · ");
      top.insertBefore(k, top.firstChild);
    }
  }

  if (meta && meta.parentNode) { meta.parentNode.removeChild(meta); }

  /* ---- 3. numbered sections --------------------------------------- */

  var a = 0, b = 0, toc = [];
  Array.prototype.forEach.call(art.querySelectorAll("h2, h3"), function (h) {
    var num;
    if (h.tagName === "H2") { a += 1; b = 0; num = String(a); }
    else { if (!a) { a = 1; } b += 1; num = a + "." + b; }

    var text = h.textContent.trim();
    if (!h.id) { h.id = "sec-" + num.replace(/\./g, "-"); }

    var tag = el("span", "secnum");
    tag.textContent = num;
    h.insertBefore(document.createTextNode(" "), h.firstChild);
    h.insertBefore(tag, h.firstChild);

    toc.push({ id: h.id, num: num, text: text, sub: h.tagName === "H3" });
  });

  /* ---- 4. mini table of contents ---------------------------------- */

  if (toc.length >= 2) {
    var box = document.getElementById("minitoc");
    if (!box) {
      box = el("div", null);
      box.id = "minitoc";
      if (top && top.nextSibling) { art.insertBefore(box, top.nextSibling); }
      else { art.insertBefore(box, art.firstChild); }
    }
    box.className = "mini-toc";
    box.innerHTML =
      "<div class='mini-toc-title'>" + esc(t.toc) + "</div><ul>" +
      toc.map(function (s) {
        return "<li class='" + (s.sub ? "sub" : "top") + "'>" +
               "<a href='#" + s.id + "'>" + s.num + ": " + esc(s.text) +
               "</a></li>";
      }).join("") + "</ul>";
  }

  /* ---- 5. numbered figure captions, and links to them -------------- */

  Array.prototype.forEach.call(art.querySelectorAll("figure"), function (f, i) {
    if (!f.id) { f.id = "fig-" + (i + 1); }
    var cap = f.querySelector("figcaption");
    if (!cap || cap.querySelector(".id")) { return; }
    var id = el("span", "id");
    id.textContent = t.fig + " " + (i + 1) + (lang === "zh" ? "：" : ":");
    cap.insertBefore(document.createTextNode(" "), cap.firstChild);
    cap.insertBefore(id, cap.firstChild);
  });

  Array.prototype.forEach.call(art.querySelectorAll("a.figref"), function (a) {
    var n = a.getAttribute("data-fig");
    if (!n || !document.getElementById("fig-" + n)) { a.textContent = "?"; return; }
    a.href = "#fig-" + n;
    a.textContent = t.fig + " " + n;
  });

  /* ---- 6. footnote marks, numbered in reading order --------------- */

  var list = art.querySelector(".footnotes ol");
  Array.prototype.forEach.call(art.querySelectorAll("sup.fn"), function (m, i) {
    var n = i + 1;
    m.id = "fnref" + n;
    m.innerHTML = "<a href='#fn" + n + "'>" + n + "</a>";
    var li = list ? list.children[i] : null;
    if (li && !li.id) { li.id = "fn" + n; }
  });

  /* ---- 7. citations: [n] in the prose, linked to the list ---------- */

  var seat = {};
  Array.prototype.forEach.call(art.querySelectorAll(".refs ol > li"), function (li, i) {
    if (li.id) { seat[li.id] = i + 1; }
  });

  Array.prototype.forEach.call(art.querySelectorAll("span.cite"), function (c) {
    var keys = (c.getAttribute("data-ref") || "").split(/\s+/);
    var hits = [];
    keys.forEach(function (k) {
      if (!k) { return; }
      var id = k.indexOf("ref-") === 0 ? k : "ref-" + k;
      if (seat[id]) { hits.push({ id: id, n: seat[id] }); }
      else if (window.console) { console.warn("post.js: no reference '" + k + "'"); }
    });
    if (!hits.length) { c.textContent = "[?]"; return; }
    hits.sort(function (a, b) { return a.n - b.n; });
    c.innerHTML = "[" + hits.map(function (h) {
      return "<a href='#" + h.id + "'>" + h.n + "</a>";
    }).join(", ") + "]";
  });

  /* ---- 8. keep punctuation attached to inline math ---------------- */

  /* MathJax renders inline math as an inline-block, so a line can break
     between the formula and the comma or full stop that follows it, which
     strands the punctuation at the start of the next line.  Glue the first
     punctuation character onto the formula. */

  var PUNCT = ".,;:!?)]}。，；：）？！」”";

  function glueMath() {
    var maths = art.querySelectorAll("span.mjx-chtml");
    Array.prototype.forEach.call(maths, function (m) {
      if (/MJXc-display/.test(m.className)) { return; }          /* display math */
      if (m.parentNode && m.parentNode.className === "mathglue") { return; }

      /* MathJax leaves the original <script type="math/tex"> next to what it
         rendered, so step over that to reach the text that follows */
      var run = [m], n = m.nextSibling;
      while (n && n.nodeType === 1 && n.tagName === "SCRIPT") {
        run.push(n);
        n = n.nextSibling;
      }
      if (!n || n.nodeType !== 3 || !n.nodeValue) { return; }
      if (PUNCT.indexOf(n.nodeValue.charAt(0)) < 0) { return; }

      var wrap = el("span", "mathglue");
      m.parentNode.insertBefore(wrap, m);
      run.forEach(function (node) { wrap.appendChild(node); });
      wrap.appendChild(document.createTextNode(n.nodeValue.charAt(0)));
      n.nodeValue = n.nodeValue.slice(1);
    });
  }

  /* MathJax is loaded async from a CDN, so by the time this runs it is
     usually not there yet.  Wait for it, then queue behind its typesetting. */
  if (window.MathJax && window.MathJax.Hub) {
    window.MathJax.Hub.Queue(glueMath);
  } else {
    var tries = 0;
    var poll = window.setInterval(function () {
      if (window.MathJax && window.MathJax.Hub) {
        window.clearInterval(poll);
        window.MathJax.Hub.Queue(glueMath);
      } else if (++tries > 150) { window.clearInterval(poll); }
    }, 100);
  }

  /* ---- 9. a way out at the bottom too ----------------------------- */

  if (top) {
    var nav = el("div", "postnav", art);
    var home = el("a", null, nav);
    home.href = "../../blog.html";
    home.innerHTML = "← " + t.back;
  }
});

})();

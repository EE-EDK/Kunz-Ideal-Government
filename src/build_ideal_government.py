#!/usr/bin/env python3
"""
Ideal Government design web — builder.

Reads data/layers.json and writes one self-contained HTML file
(ideal_government.html) styled after the Persona Dossier
(EE-EDK/Kunz-Persona, src/build_persona.py): same token system, typography,
atmosphere, file rail, TOC drawer, day/night theme, and mobile floors.

The v1 3D node graph is intentionally not carried over — the content is the
point, and a dossier reads better as compartmented files.

Usage:
    python3 src/build_ideal_government.py            # write ideal_government.html
    python3 src/build_ideal_government.py --check    # validate data only

Stdlib only.
"""

import argparse
import html
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT_DIR / "data" / "layers.json"
OUTPUT_FILE = ROOT_DIR / "ideal_government.html"
PUBLIC_OUTPUT_FILE = ROOT_DIR / "ideal_government_public.html"

STATUSES = {
    "resolved": ("Resolved", "status-success"),
    "inprogress": ("In progress", "status-warning"),
    "notstarted": ("Not started", "status-neutral"),
    "flagged": ("Flagged", "status-critical"),
}

# Category order, roman numeral, and display label — the dossier's
# CATEGORY_ORDER/ROMAN_NUMERALS pattern applied to the layer model.
CATEGORY_ORDER = [
    ("constitution", "Constitution"),
    ("foundation", "Foundation"),
    ("structure", "Structure"),
    ("economic", "Economic"),
    ("social", "Social"),
    ("legitimacy", "Legitimacy"),
    ("defense", "Defense"),
]
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def load_data(path: Path = DATA_FILE) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    known = {c for c, _ in CATEGORY_ORDER}
    seen_ids = set()
    for layer in data["layers"]:
        if layer["category"] not in known:
            raise ValueError(f"layer {layer['id']}: unknown category {layer['category']!r}")
        for item in layer["items"]:
            if item["id"] in seen_ids:
                raise ValueError(f"duplicate item id {item['id']!r}")
            seen_ids.add(item["id"])
            if item["status"] not in STATUSES:
                raise ValueError(f"item {item['id']}: unknown status {item['status']!r}")
            for sub in item.get("subitems", []):
                if sub["status"] not in STATUSES:
                    raise ValueError(f"subitem under {item['id']}: unknown status {sub['status']!r}")
    return data


def badge(status: str) -> str:
    label, css = STATUSES[status]
    return f'<span class="status-badge {css}">{label}</span>'


def count_items(data: dict) -> tuple[int, int]:
    total = resolved = 0
    for layer in data["layers"]:
        for item in layer["items"]:
            total += 1
            resolved += item["status"] == "resolved"
    return total, resolved


def render_item(item: dict) -> str:
    rows = [
        f'<tr><td class="item__id">{esc(item["id"].upper())}</td>'
        f'<td><strong>{esc(item["label"])}</strong><br><span class="item__desc">{esc(item["desc"])}</span></td>'
        f'<td class="item__status">{badge(item["status"])}</td></tr>'
    ]
    subs = item.get("subitems", [])
    sub_html = ""
    if subs:
        lis = "".join(
            f'<li>{badge(s["status"])} <span>{esc(s["label"])}</span></li>' for s in subs
        )
        sub_html = f'<ul class="subitems">{lis}</ul>'
    return (
        f'<div class="item" id="item-{esc(item["id"])}">'
        f'<div class="item__row"><span class="item__id">{esc(item["id"].upper())}</span>'
        f'<div class="item__body"><h4 class="item__label">{esc(item["label"])}</h4>'
        f'<p class="item__desc">{esc(item["desc"])}</p>{sub_html}</div>'
        f'<div class="item__status">{badge(item["status"])}</div></div>'
        f'</div>'
    )


def render_layer(layer: dict, n: int, cat_label: str) -> str:
    total = len(layer["items"])
    done = sum(1 for i in layer["items"] if i["status"] == "resolved")
    body = "".join(render_item(i) for i in layer["items"])
    title = layer["label"]
    return (
        f'<article class="file" id="{esc(layer["id"])}" data-category="{esc(layer["category"])}" data-num="{n:02d}">'
        f'<aside class="file__rail" aria-hidden="true">'
        f'<span class="file__rail-num">{n:02d}</span>'
        f'<span class="file__rail-cat">{esc(cat_label.upper())}</span>'
        f'</aside>'
        f'<div class="file__main">'
        f'<button type="button" class="file__head" onclick="toggleSection(\'{esc(layer["id"])}\')" '
        f'aria-expanded="false" aria-controls="content-{esc(layer["id"])}">'
        f'<div class="file__overline"><span class="file__overline-mark"></span>'
        f'Layer {n:02d} &middot; {esc(cat_label)}</div>'
        f'<h2 class="file__title">{esc(title)}</h2>'
        f'<p class="file__lede">{esc(layer["description"])}</p>'
        f'<div class="file__meta">'
        f'<span class="file__date">{done} of {total} resolved</span>'
        f'<span class="file__caret" aria-hidden="true"><svg class="kh-icon"><use href="#kh-icon-expand"/></svg></span>'
        f'</div>'
        f'</button>'
        f'<div class="file__body" id="content-{esc(layer["id"])}">'
        f'<div class="file__inner">'
        f'<div class="legend">{legend_html()}</div>'
        f'{body}'
        f'</div></div>'
        f'</div>'
        f'</article>'
    )


def legend_html() -> str:
    return "".join(
        f'<span>{badge(k)}</span>' for k in ("resolved", "inprogress", "notstarted", "flagged")
    )


def render_nav(data: dict) -> str:
    grouped: dict[str, list[tuple[int, dict]]] = {}
    for n, layer in enumerate(data["layers"], start=1):
        grouped.setdefault(layer["category"], []).append((n, layer))
    parts = []
    for idx, (cat, cat_label) in enumerate(CATEGORY_ORDER):
        if cat not in grouped:
            continue
        links = "".join(
            f'<li><a href="#{esc(layer["id"])}"><span class="toc__num">{n:02d}</span>'
            f'<span>{esc(layer["label"])}</span></a></li>'
            for n, layer in grouped[cat]
        )
        parts.append(
            f'<div class="toc__group" data-cat="{cat}">'
            f'<div class="toc__cat"><span class="toc__rom">{ROMAN[idx]}</span>'
            f'<span class="toc__catname">{esc(cat_label)}</span></div>'
            f'<ol class="toc__list">{links}</ol></div>'
        )
    return "".join(parts)


def render_files(data: dict) -> str:
    cat_labels = dict(CATEGORY_ORDER)
    return "".join(
        render_layer(layer, n, cat_labels[layer["category"]])
        for n, layer in enumerate(data["layers"], start=1)
    )


def build_html(data: dict, built_at: datetime | None = None, public: bool = False) -> str:
    built_at = built_at or datetime.now()
    build_time = built_at.strftime("%Y.%m.%d %H:%M")
    total, resolved = count_items(data)
    n_layers = len(data["layers"])
    title = data.get("title", "Ideal Government")
    subtitle = data.get("subtitle", "Design Web")
    version = data.get("version", "v1")

    body = BODY.format(
        title_main=esc(title),
        subtitle=esc(subtitle),
        version=esc(version),
        build_time=build_time,
        nav=render_nav(data),
        files=render_files(data),
        n_layers=n_layers,
        n_items=total,
        n_resolved=resolved,
    )
    js = JS
    if public:
        # The public page must not carry the paste box or its script: those
        # post to the private inbox, and a public page with a form would let
        # anyone write to the hub's disk.
        body = _cut(body, '      <section class="paste"', '      <footer class="footer">')
        js = _cut(js, '  /* Paste box', '  /* Scroll spy */')
    return HEAD.format(title=esc(title)) + CSS + body + js + TAIL


def _cut(text: str, start: str, end: str) -> str:
    """Remove the block from `start` up to (not including) `end`. Fails loudly if either marker is missing."""
    i = text.index(start)
    j = text.index(end, i)
    return text[:i] + text[j:]


HEAD = """<!DOCTYPE html>
<html lang="en" data-theme="dossier">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} &middot; Design Web</title>
  <meta name="generator" content="Ideal Government builder">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <script>
  /* Resolve the theme before first paint (same rule as the persona dossier). */
  (function () {{
    try {{
      var saved = localStorage.getItem('ideal-government-theme');
      var theme = (saved === 'day' || saved === 'dossier') ? saved
                : (window.matchMedia('(prefers-color-scheme: light)').matches ? 'day' : 'dossier');
      document.documentElement.setAttribute('data-theme', theme);
    }} catch (e) {{ /* blocked storage — keep the default */ }}
  }})();
  </script>
  <style>"""

CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,300..900,0..100;1,9..144,300..900,0..100&family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..125,200..800&family=JetBrains+Mono:wght@400;500&display=swap');

/* Tokens — copied from the persona dossier's DOSSIER_CSS */
:root {
  --ink-deep:#0C0A07; --ink-paper:#14110C; --ink-card:#1B1611; --ink-elev:#241D17;
  --ink-divider:#2A2118; --ink-rule:#1F1A14;
  --paper:#F0E6D2; --paper-soft:#C7B89C; --paper-faded:#A69A88; --paper-ghost:#897A61;
  --gold:#C9962F; --gold-bright:#E5B247; --crimson:#C73426; --crimson-hot:#D9554A;
  --copper:#B8743A; --alpine:#6B9F3C; --violet:#9062E2; --teal:#3FA694; --azure:#5A8AD9; --ember:#D67A35;
  --serif:'Fraunces','Cormorant Garamond',Georgia,'Times New Roman',serif;
  --sans:'Bricolage Grotesque','Public Sans',system-ui,sans-serif;
  --mono:'JetBrains Mono','IBM Plex Mono','SF Mono',Consolas,monospace;
  --rail-w:100px; --content-w:720px; --sidebar-w:320px;
}
:root[data-theme="day"] {
  --ink-deep:#E8DDC8; --ink-paper:#F4ECDC; --ink-card:#FBF5E9; --ink-elev:#FFFCF4;
  --ink-divider:#D6C7AB; --ink-rule:#E2D6BE;
  --paper:#221B12; --paper-soft:#4A3E2C; --paper-faded:#5B4F3A; --paper-ghost:#776956;
  --gold:#8A6416; --gold-bright:#84611A; --crimson:#9B2318; --crimson-hot:#B23A2C;
  --copper:#8F5526; --alpine:#4A7527; --violet:#6535C4; --teal:#216F62; --azure:#2F5FA8; --ember:#9E5419;
  color-scheme: light;
}
:root[data-theme="dossier"] { color-scheme: dark; }

* { margin:0; padding:0; box-sizing:border-box; }
html { scroll-behavior:smooth; }
body {
  font-family:var(--sans); background:var(--ink-paper); color:var(--paper);
  font-feature-settings:"kern" 1,"liga" 1,"calt" 1,"ss01" 1;
  font-variation-settings:"wdth" 100,"opsz" 16; font-weight:380; font-size:15px; line-height:1.65;
  -webkit-font-smoothing:antialiased; position:relative; min-height:100vh; overflow-x:hidden;
}

/* Atmosphere */
.atmos { position:fixed; inset:0; pointer-events:none; z-index:1; }
.atmos__vignette { position:absolute; inset:0; background:
  radial-gradient(ellipse at 50% -20%, rgba(201,150,47,0.04), transparent 55%),
  radial-gradient(ellipse at 50% 100%, rgba(0,0,0,0.55) 0%, transparent 60%),
  radial-gradient(ellipse at 0% 50%, rgba(0,0,0,0.35) 0%, transparent 50%),
  radial-gradient(ellipse at 100% 50%, rgba(0,0,0,0.35) 0%, transparent 50%); }
:root[data-theme="day"] .atmos__vignette { background:
  radial-gradient(ellipse at 50% -20%, rgba(201,150,47,0.10), transparent 55%),
  radial-gradient(ellipse at 50% 100%, rgba(120,92,48,0.10) 0%, transparent 60%),
  radial-gradient(ellipse at 0% 50%, rgba(120,92,48,0.07) 0%, transparent 50%),
  radial-gradient(ellipse at 100% 50%, rgba(120,92,48,0.07) 0%, transparent 50%); }
.atmos__grain { position:absolute; inset:0; opacity:0.05; mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%25' height='100%25' filter='url(%23n)' opacity='0.55'/></svg>"); }
:root[data-theme="day"] .atmos__grain { opacity:0.035; mix-blend-mode:multiply; }
.shell { position:relative; z-index:3; }

/* Sidebar / TOC */
.sidebar { position:fixed; left:0; top:0; width:var(--sidebar-w); height:100vh;
  background:linear-gradient(180deg,#0A0805 0%,var(--ink-paper) 60%,#100D08 100%);
  border-right:1px solid var(--ink-divider); padding:48px 36px 28px; overflow-y:auto; z-index:50;
  display:flex; flex-direction:column; gap:30px; animation:fadeUp 0.65s 0.05s both cubic-bezier(0.2,0.7,0.2,1); }
:root[data-theme="day"] .sidebar { background:linear-gradient(180deg,#FDF8EE 0%,var(--ink-paper) 60%,#EDE2CB 100%); }
.sidebar__brand { border-bottom:1px solid var(--ink-divider); padding-bottom:26px; }
.brand__mark { font-family:var(--serif); font-style:italic; font-variation-settings:"opsz" 14,"SOFT" 100;
  font-size:12px; color:var(--gold); letter-spacing:0.06em; margin-bottom:14px; display:flex; align-items:center; gap:10px; }
.brand__mark::after { content:''; flex:1; height:1px; background:linear-gradient(90deg,var(--gold),transparent); opacity:0.4; }
.brand__title { font-family:var(--serif); font-variation-settings:"opsz" 144,"SOFT" 0; font-weight:600;
  font-size:44px; line-height:0.92; letter-spacing:-0.025em; color:var(--paper); margin-bottom:12px; }
.brand__title em { font-style:italic; font-variation-settings:"opsz" 144,"SOFT" 100; color:var(--gold); font-weight:400; }
.brand__sub { font-family:var(--mono); font-size:9.5px; text-transform:uppercase; letter-spacing:0.22em; color:var(--paper-faded); }
.toc { flex:1; }
.toc__heading { font-family:var(--mono); font-size:9px; text-transform:uppercase; letter-spacing:0.24em;
  color:var(--paper-ghost); margin-bottom:22px; display:flex; align-items:center; gap:10px; }
.toc__heading::after { content:''; flex:1; height:1px; background:var(--ink-divider); }
.toc__group { margin-bottom:22px; }
.toc__cat { display:flex; align-items:baseline; gap:12px; margin-bottom:8px; padding-left:2px; }
.toc__rom { font-family:var(--serif); font-style:italic; font-variation-settings:"opsz" 14,"SOFT" 100;
  font-size:13px; color:var(--gold); width:22px; font-weight:400; }
.toc__catname { font-size:10px; text-transform:uppercase; letter-spacing:0.24em; font-weight:600; color:var(--paper-soft); }
.toc__group[data-cat="constitution"] .toc__catname { color:var(--copper); }
.toc__group[data-cat="foundation"]   .toc__catname { color:var(--violet); }
.toc__group[data-cat="structure"]    .toc__catname { color:var(--azure); }
.toc__group[data-cat="economic"]     .toc__catname { color:var(--gold); }
.toc__group[data-cat="social"]       .toc__catname { color:var(--alpine); }
.toc__group[data-cat="legitimacy"]   .toc__catname { color:var(--teal); }
.toc__group[data-cat="defense"]      .toc__catname { color:var(--ember); }
.toc__list { list-style:none; margin:0 0 0 32px; padding:0; }
.toc__list a { display:flex; gap:12px; align-items:baseline; padding:5px 10px; margin-left:-10px; border-radius:3px;
  color:var(--paper-soft); text-decoration:none; font-size:12.5px; font-variation-settings:"wdth" 95;
  transition:color .18s,background .18s,border-color .18s; border-left:1px solid transparent; line-height:1.35; }
.toc__num { font-family:var(--mono); font-size:9px; color:var(--paper-ghost); width:22px; flex-shrink:0; margin-top:1px; }
.toc__list a:hover { color:var(--paper); background:rgba(201,150,47,0.05); }
.toc__list a.is-active { color:var(--gold-bright); border-left-color:var(--gold); background:rgba(201,150,47,0.08); }
.toc__list a.is-active .toc__num { color:var(--gold); }
.sidebar__foot { border-top:1px solid var(--ink-divider); padding-top:22px; display:flex; flex-direction:column; gap:12px; }
.search { width:100%; background:var(--ink-card); border:1px solid var(--ink-divider); color:var(--paper);
  padding:10px 14px; border-radius:3px; font-family:var(--sans); font-size:12.5px; outline:none; }
.search::placeholder { color:var(--paper-ghost); font-style:italic; }
.search:focus { border-color:var(--gold); background:var(--ink-elev); }
.controls { display:flex; gap:6px; }
.ctl { flex:1; background:transparent; color:var(--paper-soft); border:1px solid var(--ink-divider); padding:8px 6px;
  border-radius:3px; font-family:var(--mono); font-size:9px; text-transform:uppercase; letter-spacing:0.12em; cursor:pointer; transition:all .18s; }
.ctl:hover { background:var(--ink-elev); color:var(--paper); border-color:var(--paper-ghost); }

/* Main column */
.main { margin-left:var(--sidebar-w); padding:80px 80px 120px; max-width:calc(var(--sidebar-w) + var(--content-w) + var(--rail-w) + 200px); }
.masthead { margin-bottom:96px; }
.masthead__cap { font-family:var(--mono); font-size:10px; text-transform:uppercase; letter-spacing:0.3em; color:var(--gold);
  margin-bottom:36px; display:flex; align-items:center; gap:18px; animation:fadeUp .7s .30s both cubic-bezier(0.2,0.7,0.2,1); }
.masthead__cap::before, .masthead__cap::after { content:''; flex:1; height:1px; background:linear-gradient(90deg,transparent,var(--gold) 50%,transparent); opacity:.5; }
.masthead__title { font-family:var(--serif); font-variation-settings:"opsz" 144,"SOFT" 30; font-weight:500;
  font-size:clamp(56px,8.5vw,116px); line-height:.92; letter-spacing:-0.025em; color:var(--paper); margin-bottom:36px;
  animation:letterIn .95s .40s both cubic-bezier(0.2,0.7,0.2,1); }
.masthead__title em { font-style:italic; font-variation-settings:"opsz" 144,"SOFT" 100; color:var(--gold); font-weight:400; }
.masthead__lede { font-family:var(--serif); font-variation-settings:"opsz" 18,"SOFT" 0; font-weight:350; font-style:italic;
  font-size:19px; line-height:1.55; color:var(--paper-soft); max-width:540px; margin-bottom:28px; animation:fadeUp .7s .65s both cubic-bezier(0.2,0.7,0.2,1); }
.masthead__meta { font-family:var(--mono); font-size:10px; text-transform:uppercase; letter-spacing:0.18em; color:var(--paper-faded);
  display:flex; gap:14px; align-items:center; flex-wrap:wrap; animation:fadeUp .6s .85s both cubic-bezier(0.2,0.7,0.2,1); }
.masthead__meta .dot { color:var(--paper-ghost); }

/* Files — one per layer */
.files { display:flex; flex-direction:column; gap:56px; }
.file { display:grid; grid-template-columns:var(--rail-w) 1fr; gap:28px; position:relative; scroll-margin-top:56px;
  opacity:0; transform:translateY(28px); transition:opacity .7s cubic-bezier(0.2,0.7,0.2,1),transform .7s cubic-bezier(0.2,0.7,0.2,1); }
.file.is-visible { opacity:1; transform:translateY(0); }
@media (prefers-reduced-motion: reduce) { .file { opacity:1; transform:none; transition:none; } }
.file__rail { position:relative; padding-top:6px; border-right:1px solid var(--ink-divider); padding-right:24px;
  display:flex; flex-direction:column; align-items:flex-end; gap:22px; min-height:120px; }
.file__rail-num { font-family:var(--serif); font-style:italic; font-variation-settings:"opsz" 144,"SOFT" 60; font-size:60px;
  line-height:.85; color:var(--paper-ghost); letter-spacing:-0.03em; transition:color .3s; }
.file:hover .file__rail-num { color:var(--gold); }
.file__rail-cat { font-family:var(--mono); font-size:9px; text-transform:uppercase; letter-spacing:0.32em;
  writing-mode:vertical-rl; transform:rotate(180deg); color:var(--paper-faded); font-weight:500; }
.file[data-category="constitution"] .file__rail-cat { color:var(--copper); }
.file[data-category="foundation"]   .file__rail-cat { color:var(--violet); }
.file[data-category="structure"]    .file__rail-cat { color:var(--azure); }
.file[data-category="economic"]     .file__rail-cat { color:var(--gold); }
.file[data-category="social"]       .file__rail-cat { color:var(--alpine); }
.file[data-category="legitimacy"]   .file__rail-cat { color:var(--teal); }
.file[data-category="defense"]      .file__rail-cat { color:var(--ember); }
.file[data-category="constitution"] .file__overline-mark { background:var(--copper); }
.file[data-category="foundation"]   .file__overline-mark { background:var(--violet); }
.file[data-category="structure"]    .file__overline-mark { background:var(--azure); }
.file[data-category="economic"]     .file__overline-mark { background:var(--gold); }
.file[data-category="social"]       .file__overline-mark { background:var(--alpine); }
.file[data-category="legitimacy"]   .file__overline-mark { background:var(--teal); }
.file[data-category="defense"]      .file__overline-mark { background:var(--ember); }
.file__main { min-width:0; }
.file__head { display:block; width:100%; background:transparent; border:none; cursor:pointer; text-align:left;
  padding:0 0 18px 0; border-bottom:1px solid var(--ink-divider); font-family:inherit; color:inherit; transition:border-color .2s; }
.file__head:hover { border-bottom-color:var(--gold); }
.file__head:focus-visible { outline:1px dashed var(--gold); outline-offset:6px; }
.file__overline { font-family:var(--mono); font-size:11.5px; text-transform:uppercase; letter-spacing:0.22em;
  color:var(--paper-ghost); margin-bottom:12px; display:flex; gap:8px; align-items:center; }
.file__overline-mark { width:4px; height:4px; border-radius:50%; background:var(--paper-ghost); }
.file__title { font-family:var(--serif); font-variation-settings:"opsz" 96,"SOFT" 30; font-weight:500; font-size:40px;
  line-height:1.05; letter-spacing:-0.018em; color:var(--paper); margin-bottom:14px; transition:color .25s; }
.file__head:hover .file__title { color:var(--gold-bright); }
.file__lede { font-family:var(--serif); font-variation-settings:"opsz" 18,"SOFT" 0; font-style:italic; font-size:17px;
  line-height:1.6; color:var(--paper-soft); max-width:620px; margin-bottom:16px; }
.file__meta { display:flex; align-items:center; justify-content:space-between; gap:12px; }
.file__date { font-family:var(--mono); font-size:10px; text-transform:uppercase; letter-spacing:0.16em; color:var(--paper-faded); }
.file__caret { display:inline-flex; width:16px; height:16px; color:var(--gold); transition:transform .35s ease; }
.kh-icon { width:1em; height:1em; display:block; }
.file__head[aria-expanded="true"] .file__caret { transform:rotate(180deg); }
.file__body { display:grid; grid-template-rows:0fr; transition:grid-template-rows .45s cubic-bezier(0.2,0.7,0.2,1); }
.file__body.is-open { grid-template-rows:1fr; }
.file__inner { min-height:0; overflow:hidden; }
.file__body.is-open .file__inner { padding-top:32px; }

/* Items — the content inside each file */
.legend { display:flex; flex-wrap:wrap; gap:10px 14px; margin-bottom:28px; font-family:var(--mono); font-size:10px; color:var(--paper-faded); }
.item { border-bottom:1px solid var(--ink-divider); padding:18px 0; }
.item:last-child { border-bottom:none; }
.item__row { display:grid; grid-template-columns:56px 1fr auto; gap:16px; align-items:start; }
.item__id { font-family:var(--mono); font-size:11.5px; color:var(--paper-ghost); letter-spacing:0.08em; padding-top:4px; }
.item__label { font-family:var(--serif); font-variation-settings:"opsz" 36,"SOFT" 0; font-weight:500; font-size:19px;
  line-height:1.25; color:var(--paper); margin-bottom:6px; }
.item__desc { font-family:var(--serif); font-variation-settings:"opsz" 18,"SOFT" 0; font-weight:350; font-size:16px;
  line-height:1.6; color:var(--paper-soft); }
.item__status { padding-top:3px; }
.subitems { list-style:none; margin:12px 0 0 0; padding:0 0 0 2px; }
.subitems li { font-family:var(--sans); font-size:13.5px; color:var(--paper-faded); padding:4px 0 4px 0; display:flex; gap:10px; align-items:center; }
.status-badge { display:inline-block; font-family:var(--mono); font-size:11px; text-transform:uppercase; letter-spacing:0.12em;
  padding:3px 9px; border-radius:2px; font-weight:500; white-space:nowrap; }
.status-success  { background:rgba(107,159,60,0.14); color:var(--alpine); }
.status-warning  { background:rgba(229,178,71,0.14); color:var(--gold-bright); }
.status-critical { background:rgba(217,85,74,0.16); color:var(--crimson-hot); }
.status-neutral  { background:rgba(199,184,156,0.08); color:var(--paper-soft); }

/* Paste box — saves text to the hub inbox (see server/inbox_api.py) */
.paste { margin-top:96px; padding-top:40px; border-top:1px solid var(--ink-divider); }
.paste__cap { font-family:var(--mono); font-size:10px; text-transform:uppercase; letter-spacing:0.3em; color:var(--gold); margin-bottom:18px; }
.paste__title { font-family:var(--serif); font-variation-settings:"opsz" 96,"SOFT" 30; font-weight:500; font-size:34px; line-height:1.1; color:var(--paper); margin-bottom:12px; }
.paste__lede { font-family:var(--serif); font-variation-settings:"opsz" 18,"SOFT" 0; font-style:italic; font-size:17px; line-height:1.6; color:var(--paper-soft); max-width:620px; margin-bottom:24px; }
.paste__form { display:flex; flex-direction:column; gap:10px; max-width:760px; }
.paste__label { font-family:var(--mono); font-size:11.5px; text-transform:uppercase; letter-spacing:0.16em; color:var(--paper-faded); margin-top:8px; }
.paste__text { width:100%; min-height:260px; resize:vertical; background:var(--ink-card); border:1px solid var(--ink-divider); color:var(--paper);
  padding:14px 16px; border-radius:3px; font-family:var(--serif); font-size:16px; line-height:1.55; outline:none; }
.paste__text:focus { border-color:var(--gold); background:var(--ink-elev); }
.paste__row { display:flex; align-items:center; justify-content:space-between; gap:12px; margin-top:6px; flex-wrap:wrap; }
.paste__submit { flex:0 0 auto; padding:10px 18px; }
.paste__status { font-family:var(--sans); font-size:14px; color:var(--paper-soft); min-height:1.6em; }

/* Footer */
.footer { margin-top:96px; padding-top:36px; border-top:1px solid var(--ink-divider); text-align:center; }
.footer__mark { font-family:var(--serif); font-style:italic; font-size:22px; color:var(--gold); margin-bottom:10px; opacity:.7; }
.footer__text { font-family:var(--mono); font-size:10px; text-transform:uppercase; letter-spacing:0.24em; color:var(--paper-ghost); }

/* Toggles + overlay */
.menu-toggle { display:none; position:fixed; top:14px; left:14px; z-index:100; width:44px; height:44px; background:var(--ink-card);
  border:1px solid var(--ink-divider); color:var(--paper); cursor:pointer; border-radius:3px; align-items:center; justify-content:center; }
.menu-toggle .kh-icon { width:20px; height:20px; }
.theme-toggle { position:fixed; top:14px; right:14px; z-index:100; width:44px; height:44px; background:var(--ink-card);
  border:1px solid var(--ink-divider); color:var(--paper-soft); font-size:17px; cursor:pointer; border-radius:3px; font-family:var(--mono);
  display:flex; align-items:center; justify-content:center; transition:color .2s,border-color .2s,background .2s; }
.theme-toggle:hover, .theme-toggle:focus-visible, .menu-toggle:hover { background:var(--ink-elev); border-color:var(--gold); color:var(--gold); outline:none; }
.overlay { display:none; position:fixed; inset:0; background:rgba(8,6,4,0.78); z-index:40; }
.overlay.is-visible { display:block; }

@keyframes fadeUp { from { opacity:0; transform:translateY(16px); } to { opacity:1; transform:translateY(0); } }
@keyframes letterIn { from { opacity:0; letter-spacing:0.05em; } to { opacity:1; letter-spacing:-0.025em; } }
::selection { background:var(--gold); color:var(--ink-deep); }
::-webkit-scrollbar { width:8px; height:8px; }
::-webkit-scrollbar-track { background:transparent; }
::-webkit-scrollbar-thumb { background:var(--ink-divider); border-radius:4px; }

/* Responsive — the persona dossier's breakpoints and mobile readability floors */
@media (max-width:1180px) { .main { padding:64px 56px 96px; } }
@media (max-width:1024px) {
  :root { --sidebar-w:280px; --rail-w:84px; }
  .sidebar { padding:36px 26px 24px; }
  .main { padding:56px 44px 80px; }
  .file__title { font-size:34px; }
  .file__rail-num { font-size:50px; }
  .masthead { margin-bottom:72px; }
}
@media (max-width:768px) {
  .menu-toggle { display:flex; }
  .sidebar { animation:none; transform:translateX(-100%); transition:transform .3s cubic-bezier(0.2,0.7,0.2,1);
    padding-top:72px; width:88vw; max-width:320px; }
  .sidebar.is-open { transform:translateX(0); }
  .main { margin-left:0; padding:72px 22px 64px; }
  .masthead { margin-bottom:56px; }
  .masthead__title { font-size:48px; }
  .masthead__lede { font-size:16px; }
  .masthead__cap, .masthead__meta, .masthead__title, .masthead__lede { animation:none; }
  .file { grid-template-columns:56px 1fr; gap:14px; }
  .file__rail { padding-right:12px; min-height:96px; }
  .file__rail-num { font-size:38px; }
  .file__title { font-size:26px; }
  .item__row { grid-template-columns:40px 1fr; }
  .item__status { grid-column:2; padding-top:0; }
  .item__label { font-size:17px; }
  .item__desc { font-size:15px; }
  .files { gap:40px; }
  .footer { margin-top:64px; }
  /* Mobile readability floor: nothing read below 12px (kunzhub audit). */
  .file__rail-cat, .toc__heading, .ctl, .status-badge, .file__overline,
  .file__date, .masthead__cap, .masthead__meta, .toc__catname, .toc__num,
  .brand__sub, .legend, .footer__text, .search { font-size:12px; }
  .file__rail-cat { letter-spacing:0.22em; }
  .toc__heading { letter-spacing:0.2em; }
  .toc__list a { min-height:32px; align-items:center; }
  .ctl { min-height:32px; }
  .status-badge { letter-spacing:0.08em; }
  .subitems li { font-size:14px; }
  .file__lede { font-size:16px; }
  .paste__title { font-size:28px; }
  .paste__label { font-size:12px; }
  .paste__text { font-size:16px; }
}
@media print {
  .sidebar, .menu-toggle, .theme-toggle, .overlay, .atmos { display:none !important; }
  .file { opacity:1; transform:none; }
  .file__body { grid-template-rows:1fr; }
}
</style>
</head>
"""

BODY = """<body>
  <svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
    <symbol id="kh-icon-expand" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" stroke-linejoin="miter"><path d="m6 9 6 6 6-6"/></symbol>
    <symbol id="kh-icon-menu" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="square" stroke-linejoin="miter"><path d="M4 5h16"/><path d="M4 12h16"/><path d="M4 19h16"/></symbol>
  </defs></svg>
  <div class="atmos" aria-hidden="true"><div class="atmos__vignette"></div><div class="atmos__grain"></div></div>

  <button class="menu-toggle" id="menuToggle" aria-label="Open table of contents"><svg class="kh-icon" aria-hidden="true"><use href="#kh-icon-menu"/></svg></button>
  <button class="theme-toggle" id="themeToggle" aria-label="Switch theme" aria-pressed="false">&#9788;</button>

  <div class="shell">
    <aside class="sidebar" id="sidebar">
      <div class="sidebar__brand">
        <div class="brand__mark">Design Web &middot; {version}</div>
        <div class="brand__title">{title_main} <em>{subtitle}</em></div>
        <div class="brand__sub">Compiled {build_time}</div>
      </div>
      <nav class="toc" aria-label="Table of contents">
        <div class="toc__heading">Table of Contents</div>
        {nav}
      </nav>
      <div class="sidebar__foot">
        <input type="text" class="search" id="searchBox" placeholder="Search the design&#8230;" aria-label="Search">
        <div class="controls">
          <button type="button" class="ctl" onclick="expandAll()">Open all</button>
          <button type="button" class="ctl" onclick="collapseAll()">Close</button>
          <button type="button" class="ctl" onclick="window.print()">Print</button>
        </div>
      </div>
    </aside>

    <main class="main">
      <header class="masthead">
        <div class="masthead__cap">Design Web &middot; Working Draft</div>
        <h1 class="masthead__title">Ideal<br><em>Government.</em></h1>
        <p class="masthead__lede">
          A constitutional core and six design layers. Every open question is
          compartmented as a file, and every item carries a status.
        </p>
        <div class="masthead__meta">
          <span>{n_layers} layers</span><span class="dot">&middot;</span>
          <span>{n_resolved} of {n_items} items resolved</span><span class="dot">&middot;</span>
          <span>{version}</span>
        </div>
      </header>

      <section class="files" aria-label="Layers">
        {files}
      </section>

      <section class="paste" id="paste" aria-labelledby="pasteTitle">
        <div class="paste__cap">Inbox</div>
        <h2 class="paste__title" id="pasteTitle">Paste text for the next update</h2>
        <p class="paste__lede">
          Paste a conversation or notes. It is saved on kunz-ai-hub and read
          the next time the design is updated. Nothing here changes the design
          directly.
        </p>
        <form class="paste__form" id="pasteForm">
          <label class="paste__label" for="pasteSource">Where it came from (optional)</label>
          <input class="search" id="pasteSource" name="source" maxlength="200" type="text"
                 placeholder="e.g. Claude chat, 2026-10-04">
          <label class="paste__label" for="pasteText">Text</label>
          <textarea class="paste__text" id="pasteText" name="text" maxlength="200000"
                    placeholder="Paste here"></textarea>
          <div class="paste__row">
            <span class="file__date" id="pasteCount" aria-live="off">0 characters</span>
            <button type="submit" class="ctl paste__submit">Save to inbox</button>
          </div>
          <p class="paste__status" id="pasteStatus" role="status" aria-live="polite"></p>
        </form>
      </section>

      <footer class="footer">
        <div class="footer__mark">&#8258;</div>
        <div class="footer__text">&mdash; End of design web &mdash;</div>
      </footer>
    </main>
    <div class="overlay" id="overlay"></div>
  </div>
"""

JS = """
<script>
(() => {
  const $ = (s, c) => (c || document).querySelector(s);
  const $$ = (s, c) => Array.from((c || document).querySelectorAll(s));

  /* Mobile drawer */
  const sidebar = $('#sidebar'), overlay = $('#overlay'), toggle = $('#menuToggle');
  const openSidebar = () => { sidebar.classList.add('is-open'); overlay.classList.add('is-visible'); };
  const closeSidebar = () => { sidebar.classList.remove('is-open'); overlay.classList.remove('is-visible'); };
  toggle.addEventListener('click', () => sidebar.classList.contains('is-open') ? closeSidebar() : openSidebar());
  overlay.addEventListener('click', closeSidebar);

  /* Day / night — remembered only on a deliberate choice */
  const themeBtn = $('#themeToggle');
  const paintTheme = (t) => {
    document.documentElement.setAttribute('data-theme', t);
    const day = t === 'day';
    themeBtn.innerHTML = day ? '&#9790;' : '&#9788;';
    themeBtn.setAttribute('aria-label', day ? 'Switch to night mode' : 'Switch to day mode');
    themeBtn.setAttribute('aria-pressed', String(day));
  };
  paintTheme(document.documentElement.getAttribute('data-theme') || 'dossier');
  themeBtn.addEventListener('click', () => {
    const next = document.documentElement.getAttribute('data-theme') === 'day' ? 'dossier' : 'day';
    try { localStorage.setItem('ideal-government-theme', next); } catch (e) {}
    paintTheme(next);
  });

  /* Open / close files */
  const setOpen = (file, open) => {
    if (!file) return;
    file.classList.add('is-visible');
    const body = $('.file__body', file), head = $('.file__head', file);
    if (body) body.classList.toggle('is-open', open);
    if (head) head.setAttribute('aria-expanded', open ? 'true' : 'false');
  };
  window.toggleSection = (id) => {
    const file = document.getElementById(id);
    const body = file && $('.file__body', file);
    setOpen(file, !(body && body.classList.contains('is-open')));
  };
  window.expandAll = () => $$('.file').forEach(f => setOpen(f, true));
  window.collapseAll = () => $$('.file').forEach(f => setOpen(f, false));

  /* TOC navigation — open, scroll, mark active */
  const tocLinks = new Map($$('.toc__list a').map(a => [a.getAttribute('href').slice(1), a]));
  const reduceMotion = () => { try { return matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { return false; } };
  const navigateTo = (id) => {
    const file = document.getElementById(id);
    if (!file) return;
    setOpen(file, true);
    $$('.toc__list a').forEach(a => a.classList.remove('is-active'));
    const link = tocLinks.get(id);
    if (link) link.classList.add('is-active');
    if (window.innerWidth <= 768) closeSidebar();
    requestAnimationFrame(() => requestAnimationFrame(() => {
      const root = document.documentElement, prev = root.style.scrollBehavior;
      root.style.scrollBehavior = 'auto';
      window.scrollTo(0, Math.max(0, Math.round(file.getBoundingClientRect().top + scrollY - 12)));
      root.style.scrollBehavior = prev;
      try { history.replaceState(null, '', '#' + id); } catch (e) {}
    }));
  };
  $$('.toc__list a').forEach(a => a.addEventListener('click', e => {
    e.preventDefault();
    navigateTo(a.getAttribute('href').slice(1));
  }));

  /* Search across the file text */
  const search = $('#searchBox');
  search.addEventListener('input', () => {
    const q = search.value.trim().toLowerCase();
    $$('.file').forEach(f => {
      const match = !q || (f.textContent || '').toLowerCase().includes(q);
      f.style.display = match ? '' : 'none';
      if (q && match) setOpen(f, true);
    });
  });

  /* Scroll reveal */
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => entries.forEach(en => {
      if (en.isIntersecting) { en.target.classList.add('is-visible'); io.unobserve(en.target); }
    }), { threshold: 0, rootMargin: '40px 0px 40px 0px' });
    $$('.file').forEach(f => io.observe(f));
  } else {
    $$('.file').forEach(f => f.classList.add('is-visible'));
  }

  /* Deep link */
  if (location.hash.length > 1 && document.getElementById(location.hash.slice(1))) {
    requestAnimationFrame(() => navigateTo(location.hash.slice(1)));
  }

  /* Paste box — POSTs to api/inbox (relative: resolves under the page's
     private slug, where Caddy applies basicauth and forwards to the service). */
  const pForm = $('#pasteForm'), pText = $('#pasteText'), pSrc = $('#pasteSource'),
        pStatus = $('#pasteStatus'), pCount = $('#pasteCount');
  if (pForm) {
    pText.addEventListener('input', () => {
      pCount.textContent = pText.value.length.toLocaleString() + ' characters';
    });
    pForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (!pText.value.trim()) { pStatus.textContent = 'Nothing to save yet.'; return; }
      pStatus.textContent = 'Saving…';
      try {
        const r = await fetch('api/inbox', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: pText.value, source: pSrc.value }),
        });
        if (r.status === 201) {
          const d = await r.json();
          pStatus.textContent = 'Saved as ' + d.id + '. It will be read on the next update.';
          pText.value = ''; pSrc.value = ''; pCount.textContent = '0 characters';
        } else if (r.status === 401) {
          pStatus.textContent = 'Not signed in. Reload the page and sign in again. Your text is still here.';
        } else {
          pStatus.textContent = 'Not saved (HTTP ' + r.status + '). Your text is still here; copy it before reloading.';
        }
      } catch (err) {
        pStatus.textContent = 'Could not reach the inbox. Your text is still here.';
      }
    });
  }

  /* Scroll spy */
  let raf = 0;
  window.addEventListener('scroll', () => {
    if (raf) return;
    raf = requestAnimationFrame(() => {
      raf = 0;
      let bestId = null, bestTop = -Infinity;
      $$('.file').forEach(f => {
        const top = f.getBoundingClientRect().top;
        if (top < 92 && top > bestTop) { bestTop = top; bestId = f.id; }
      });
      if (bestId) {
        $$('.toc__list a').forEach(a => a.classList.remove('is-active'));
        const link = tocLinks.get(bestId);
        if (link) link.classList.add('is-active');
      }
    });
  }, { passive: true });
})();
</script>
"""

TAIL = """</body>
</html>
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--check", action="store_true", help="validate data only")
    parser.add_argument("--out", type=Path, default=OUTPUT_FILE)
    args = parser.parse_args(argv)

    data = load_data()
    total, resolved = count_items(data)
    if args.check:
        print(f"ok: {len(data['layers'])} layers, {total} items, {resolved} resolved")
        return 0
    args.out.write_text(build_html(data), encoding="utf-8")
    print(f"wrote {args.out} ({len(data['layers'])} layers, {total} items, {resolved} resolved)")
    public_out = args.out.with_name(PUBLIC_OUTPUT_FILE.name)
    public_out.write_text(build_html(data, public=True), encoding="utf-8")
    print(f"wrote {public_out} (public: no paste box)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

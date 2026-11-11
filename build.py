#!/usr/bin/env python3
"""Builds the Lumiwire website as plain static files (from the Inkbloom site generator).

usage: python build.py [out_dir] [--preview]
  out_dir    default: docs (GitHub Pages serves main /docs)
  --preview  writes explicit index.html links so the site can be browsed from disk.

Moving to a domain later: set SITE_ORIGIN to it and BASE_PATH to "", add CNAME
and app-ads.txt (PLAN.md W1 step 4), rebuild, push. Launch day: LIVE_STORES = True.
"""
import html, os, shutil, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import (APP_STORE_URL, CHAPTERS, FAQ, FEATURES, MODES, OBSTACLES, PLAY_URL,
                     RULES, SHOP_LIVE, STARS, SUPPORT_EMAIL, UPDATED)

ROOT = os.path.dirname(os.path.abspath(__file__))
args = [a for a in sys.argv[1:] if not a.startswith("--")]
OUT = os.path.abspath(args[0]) if args else os.path.join(ROOT, "docs")
PREVIEW = "--preview" in sys.argv

SITE_ORIGIN = "https://sriramgoparaju.github.io"
BASE_PATH = "/lumiwire-site"      # "" once the site has its own domain
SITE_URL = SITE_ORIGIN + BASE_PATH
LIVE_STORES = False               # True on launch day, with the real store URLs in content.py
YEAR = "2026"

e = html.escape


def link(depth, target, absolute=False):
    """target is a site path like '' (home), 'privacy/', 'assets/site.css'.
    Relative links work under any BASE_PATH; absolute ones are for 404.html,
    which GitHub Pages serves at whatever path was asked for."""
    if absolute:
        return f"{BASE_PATH}/{target}"
    up = "../" * depth
    if target == "" or target.endswith("/"):
        if PREVIEW:
            return up + target + "index.html"
        return (up + target) or "./"
    return up + target


CSS = r""":root {
  /* The app's own tokens (src/theme): Paper (light) and Graphite (dark). */
  --ground: #F3F1EC; --card: #FFFFFF; --card2: #F8F6F2; --line: #E3DFD6;
  --fg: #16181B; --sub: #62666D; --title: #111316;
  --accent: #0E6F7E; --accent-soft: rgba(14, 111, 126, 0.10);
  --primary: #16181B; --primary-fg: #FFFFFF; --amber: #93590A;
  --shot-shadow: 0 1px 0 var(--line), 0 18px 40px -24px rgba(30, 25, 15, .45);
  --font-display: "Fraunces", Georgia, "Times New Roman", serif;
  --font-body: "Inter", "Segoe UI", system-ui, sans-serif;
  color-scheme: light;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --ground: #0B0D11; --card: #13171C; --card2: #191E24; --line: rgba(255, 255, 255, 0.08);
    --fg: #E4E7EB; --sub: #8B94A1; --title: #F5F6F8;
    --accent: #5AD1E6; --accent-soft: rgba(90, 209, 230, 0.14);
    --primary: #5AD1E6; --primary-fg: #071317; --amber: #E9B65A;
    --shot-shadow: 0 0 0 1px var(--line), 0 18px 40px -20px rgba(0, 0, 0, .8);
    --font-display: "Inter", "Segoe UI", system-ui, sans-serif;
    color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --ground: #0B0D11; --card: #13171C; --card2: #191E24; --line: rgba(255, 255, 255, 0.08);
  --fg: #E4E7EB; --sub: #8B94A1; --title: #F5F6F8;
  --accent: #5AD1E6; --accent-soft: rgba(90, 209, 230, 0.14);
  --primary: #5AD1E6; --primary-fg: #071317; --amber: #E9B65A;
  --shot-shadow: 0 0 0 1px var(--line), 0 18px 40px -20px rgba(0, 0, 0, .8);
  --font-display: "Inter", "Segoe UI", system-ui, sans-serif;
  color-scheme: dark;
}
* { box-sizing: border-box; }
html, body { margin: 0; }
body { background: var(--ground); color: var(--fg); font: 17px/1.6 var(--font-body); -webkit-font-smoothing: antialiased; }
a { color: var(--accent); text-underline-offset: 3px; }
a:hover { color: var(--title); }
a:focus-visible, .btn:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; border-radius: 4px; }
img { max-width: 100%; height: auto; }
.wrap { max-width: 1040px; margin: 0 auto; padding: 0 20px; }
.narrow { max-width: 720px; }
h1, h2, h3 { font-family: var(--font-display); font-weight: 600; color: var(--title); line-height: 1.15; text-wrap: balance; margin: 0; letter-spacing: -0.01em; }
h1 { font-size: clamp(34px, 6vw, 54px); }
h2 { font-size: clamp(24px, 3.2vw, 32px); }
h3 { font-size: 20px; }
p { margin: 0; }
.muted { color: var(--sub); }

/* Header and footer */
.site-head { border-bottom: 1px solid var(--line); }
.site-head .wrap { display: flex; align-items: center; justify-content: space-between; gap: 16px; padding-top: 14px; padding-bottom: 14px; flex-wrap: wrap; }
.brand { display: flex; align-items: center; gap: 10px; text-decoration: none; color: var(--title); font: 600 22px/1 var(--font-display); }
.brand img { width: 36px; height: 36px; border-radius: 9px; }
.site-nav { display: flex; gap: 18px; flex-wrap: wrap; font-size: 15px; }
.site-nav a { color: var(--fg); text-decoration: none; }
.site-nav a:hover, .site-nav a[aria-current="page"] { color: var(--accent); text-decoration: underline; }
.site-foot { border-top: 1px solid var(--line); margin-top: 72px; padding: 32px 0 48px; font-size: 15px; color: var(--sub); }
.site-foot .wrap { display: grid; gap: 14px; }
.foot-links { display: flex; flex-wrap: wrap; gap: 8px 20px; }
.foot-links a { color: var(--fg); }

/* Home */
.hero { padding: 64px 0 40px; display: grid; grid-template-columns: minmax(0, 1.3fr) minmax(0, 1fr); gap: 40px; align-items: center; }
.hero .lede { font-size: 20px; color: var(--sub); margin-top: 16px; max-width: 36ch; }
.hero-icon { justify-self: center; width: min(260px, 70vw); border-radius: 22%; box-shadow: var(--shot-shadow); }
.stores { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 28px; }
.btn { display: inline-flex; flex-direction: column; justify-content: center; min-width: 190px; padding: 10px 18px; border-radius: 12px; background: var(--primary); color: var(--primary-fg); text-decoration: none; line-height: 1.2; }
.btn small { font-size: 12px; opacity: .8; }
.btn strong { font: 600 18px/1.2 var(--font-body); }
.btn:hover { color: var(--primary-fg); opacity: .92; }
.btn.soon { background: transparent; color: var(--fg); border: 1px solid var(--line); cursor: default; }
.btn.soon small { color: var(--accent); opacity: 1; font-weight: 600; }
.section { padding: 40px 0; }
.section > h2 { margin-bottom: 8px; }
.section > .intro { color: var(--sub); max-width: 62ch; margin-bottom: 24px; }
.strip { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; }
.strip div { background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 16px; }
.strip strong { display: block; font: 600 28px/1.1 var(--font-display); color: var(--title); }
.strip span { font-size: 15px; color: var(--sub); }
.shots { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; margin: 0; }
.shots figure { margin: 0; display: grid; gap: 10px; justify-items: center; }
.shots img { border-radius: 22px; box-shadow: var(--shot-shadow); width: 100%; max-width: 300px; }
.shots figcaption { font-size: 15px; color: var(--sub); text-align: center; }
.features { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 28px 32px; }
.features h3 { margin-bottom: 6px; }
.features p { color: var(--sub); }

/* How to play */
.crumbs { font-size: 14px; color: var(--sub); padding-top: 28px; }
.crumbs a { color: var(--sub); }
.page-head { padding: 12px 0 8px; display: grid; gap: 10px; }
.page-head .essence { font: 400 21px/1.4 var(--font-body); color: var(--sub); }
.rules { margin: 16px 0 0; padding-left: 22px; display: grid; gap: 10px; }
.basics { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 260px); gap: 28px; align-items: start; }
.board-pic { border-radius: 14px; box-shadow: var(--shot-shadow); width: 100%; }
.obstacles { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 18px; margin-top: 16px; }
.obstacle { background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 16px; display: grid; gap: 10px; align-content: start; }
.obstacle img { border-radius: 10px; }
.obstacle .tag { font: 600 11px/1 var(--font-body); letter-spacing: .08em; text-transform: uppercase; color: var(--accent); }
.obstacle p { color: var(--sub); font-size: 15px; }
.stars { list-style: none; margin: 16px 0 0; padding: 0; display: grid; gap: 10px; }
.stars li { display: grid; grid-template-columns: 76px minmax(0, 1fr); gap: 14px; align-items: baseline; background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 12px 16px; }
.stars .s { color: var(--amber); letter-spacing: 2px; font-size: 18px; }
.modes { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 18px; margin-top: 16px; }
.modes div { background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 18px; display: grid; gap: 8px; align-content: start; }
.modes p { color: var(--sub); font-size: 15px; }
.chapters { margin: 14px 0 0; padding-left: 22px; color: var(--sub); }
.chapters strong { color: var(--fg); font-weight: 600; }
.where { background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 16px 18px; color: var(--sub); }

/* Support */
.contact { background: var(--card); border: 1px solid var(--line); border-left: 4px solid var(--accent); border-radius: 12px; padding: 20px 22px; display: grid; gap: 8px; }
.contact .email { font: 600 22px/1.3 var(--font-display); word-break: break-word; }
details.faq { border-top: 1px solid var(--line); padding: 14px 0; }
details.faq:last-of-type { border-bottom: 1px solid var(--line); }
details.faq summary { cursor: pointer; font-weight: 600; list-style-position: outside; }
details.faq summary:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; }
details.faq p { color: var(--sub); margin-top: 8px; }

/* Legal pages */
.legal { padding-top: 32px; }
.legal h1 { font-size: clamp(30px, 5vw, 42px); margin-bottom: 6px; }
.legal h2 { font-size: 24px; margin: 36px 0 10px; }
.legal h3 { font-size: 19px; margin: 24px 0 8px; }
.legal p, .legal ul, .legal ol { margin: 0 0 14px; }
.legal li { margin-bottom: 6px; }
.legal .updated { color: var(--sub); font-size: 15px; margin-bottom: 18px; }
.legal .lede { font-size: 19px; color: var(--sub); }
.legal .short, .legal .box { background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 16px 20px; margin: 20px 0; }
.legal .note { background: var(--accent-soft); border-radius: 12px; padding: 14px 18px; margin: 20px 0; }
.legal .short ul { margin: 0; }
.legal table { border-collapse: collapse; width: 100%; font-size: 15px; margin: 0 0 16px; display: block; overflow-x: auto; }
.legal th, .legal td { border: 1px solid var(--line); padding: 8px 10px; text-align: left; vertical-align: top; }

@media (max-width: 760px) {
  .hero { grid-template-columns: minmax(0, 1fr); padding-top: 40px; }
  .hero-icon { width: 140px; justify-self: start; order: -1; }
  .strip { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .shots { grid-template-columns: minmax(0, 1fr); }
  .basics { grid-template-columns: minmax(0, 1fr); }
}
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
"""

NAV = [("how-to-play/", "How to play"), ("support/", "Support"), ("privacy/", "Privacy")]
FOOT = [("how-to-play/", "How to play"), ("support/", "Support"), ("privacy/", "Privacy policy"),
        ("terms/", "Terms of use"), ("delete-account/", "Delete your account")]


def page(depth, title, description, body, path, nav=None, canonical=True, absolute=False):
    L = lambda target: link(depth, target, absolute)
    canon = f'<link rel="canonical" href="{SITE_URL}/{path}">' if canonical else ""
    nav_html = "\n      ".join(
        f'<a href="{L(t)}"{" aria-current=\"page\"" if nav == t else ""}>{label}</a>' for t, label in NAV)
    foot_html = "\n      ".join(f'<a href="{L(t)}">{label}</a>' for t, label in FOOT)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
{canon}
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:image" content="{SITE_URL}/assets/icon-512.png">
<meta property="og:type" content="website">
<meta name="theme-color" content="#F3F1EC" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0B0D11" media="(prefers-color-scheme: dark)">
<link rel="icon" type="image/png" href="{L('assets/icon-192.png')}">
<link rel="apple-touch-icon" href="{L('assets/apple-touch-icon.png')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{L('assets/site.css')}">
</head>
<body>
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="{L('')}"><img src="{L('assets/icon-192.png')}" alt="" width="36" height="36">Lumiwire</a>
    <nav class="site-nav" aria-label="Main">
      {nav_html}
    </nav>
  </div>
</header>
<main>
{body}
</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="foot-links">
      {foot_html}
    </div>
    <p>Lumiwire: Connect Wire Puzzle · published by Sriram Goparaju · <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a></p>
    <p>© {YEAR} Sriram Goparaju. App Store is a service mark of Apple Inc. Google Play is a trademark of Google LLC.</p>
  </div>
</footer>
</body>
</html>
"""


def store_buttons():
    if LIVE_STORES:
        return (f'<div class="stores"><a class="btn" href="{PLAY_URL}"><small>Get it on</small><strong>Google Play</strong></a>'
                f'<a class="btn" href="{APP_STORE_URL}"><small>Download on the</small><strong>App Store</strong></a></div>')
    return ('<div class="stores">'
            '<span class="btn soon" aria-disabled="true"><small>Coming soon</small><strong>Google Play</strong></span>'
            '<span class="btn soon" aria-disabled="true"><small>Coming soon</small><strong>App Store</strong></span>'
            '</div>')


def write(rel, text):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def img(depth, name, alt, width, height, cls="", lazy=True):
    c = f' class="{cls}"' if cls else ""
    lz = ' loading="lazy"' if lazy else ""
    return f'<img{c} src="{link(depth, "assets/" + name)}" alt="{e(alt)}" width="{width}" height="{height}"{lz}>'


def build_home():
    features = "".join(f"<div><h3>{e(h)}</h3><p>{e(t)}</p></div>" for h, t in FEATURES)
    shots = "".join(
        f'<figure>{img(0, n + ".webp", alt, SHOT_W, SHOT_H)}<figcaption>{e(cap)}</figcaption></figure>'
        for n, cap, alt in [
            ("screen-home", "Home: pick up where you left off.", "Lumiwire's Home screen in light mode, with the next level, the Daily puzzle and Blitz."),
            ("screen-journey", "Journey: 50 levels a chapter.", "The Journey map: levels on a curved wire, the Challenge level marked 2× coins."),
            ("screen-blitz", "Blitz: 60 seconds of tiny boards.", "A Blitz round in dark mode: a small board with three pairs of sockets and the clock running."),
        ])
    body = f"""
<div class="wrap">
  <section class="hero">
    <div>
      <h1>Connect every wire. Fill every cell.</h1>
      <p class="lede">Lumiwire is a calm circuit puzzle. Drag a wire between matching sockets, never cross another wire, and cover the whole board. Every board has exactly one solution, and you never have to guess.</p>
      {store_buttons()}
    </div>
    <img class="hero-icon" src="assets/icon-512.png" alt="The Lumiwire app icon" width="260" height="260">
  </section>

  <section class="section" aria-labelledby="h-numbers">
    <h2 id="h-numbers">A board for every mood</h2>
    <p class="intro">A long Journey for the evenings, one Daily board shared by everyone, and a one-minute Blitz for the queue at the bank.</p>
    <div class="strip">
      <div><strong>400</strong><span>Journey levels in eight chapters</span></div>
      <div><strong>8</strong><span>new ideas, one per chapter</span></div>
      <div><strong>1</strong><span>Daily board, the same for everyone</span></div>
      <div><strong>60 s</strong><span>Blitz rounds of tiny boards</span></div>
    </div>
  </section>

  <section class="section" aria-labelledby="h-shots">
    <h2 id="h-shots">See it</h2>
    <p class="intro">Graphite when it's dark, Paper when it's light. The app follows your phone, or you can choose.</p>
    <div class="shots">{shots}</div>
  </section>

  <section class="section" aria-labelledby="h-why">
    <h2 id="h-why">Made to be solved, not fought</h2>
    <div class="features" style="margin-top:20px">{features}</div>
  </section>

  <section class="section" aria-labelledby="h-help">
    <h2 id="h-help">Questions?</h2>
    <p class="intro">Start with <a href="{link(0, 'how-to-play/')}">how to play</a> and the <a href="{link(0, 'support/')}">support page</a>, or write to <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a>.</p>
  </section>
</div>
"""
    write("index.html", page(0, "Lumiwire: Connect Wire Puzzle", "Lumiwire is a calm connect-the-wires puzzle: join matching sockets, never cross a wire, fill every cell. 400 levels, a Daily board and 60-second Blitz rounds.", body, ""))


def build_how_to_play():
    rules = "".join(f"<li>{e(r)}</li>" for r in RULES)
    obstacles = "".join(
        f'<div class="obstacle">{img(1, o["image"] + ".webp", o["alt"], BOARD_W, BOARD_H)}'
        f'<span class="tag">Chapter {o["chapter"]} · from level {o["level"]}</span><h3>{e(o["name"])}</h3><p>{e(o["rule"])}</p></div>'
        for o in OBSTACLES)
    stars = "".join(f'<li><span class="s" aria-label="{n} stars">{"★" * n}{"☆" * (3 - n)}</span><span>{e(t)}</span></li>' for n, t in STARS)
    modes = "".join(f"<div><h3>{e(h)}</h3><p>{e(t)}</p></div>" for h, t in MODES)
    chapters = "".join(f"<li><strong>{e(n)}</strong>, levels {a}–{b}: {e(what)}</li>" for n, a, b, what in CHAPTERS)
    body = f"""
<div class="wrap">
  <p class="crumbs"><a href="{link(1, '')}">Home</a> / How to play</p>
  <section class="page-head"><h1>How to play</h1>
    <p class="essence">One rule set, eight twists, three stars.</p></section>

  <section class="section basics" aria-labelledby="h-rules">
    <div>
      <h2 id="h-rules">The rules</h2>
      <ol class="rules">{rules}</ol>
    </div>
    {img(1, "board-basics.webp", "Level 1: a five-by-five board with four pairs of sockets, each with its own colour and symbol.", BOARD_W, BOARD_H, "board-pic", lazy=False)}
  </section>

  <section class="section" aria-labelledby="h-obstacles">
    <h2 id="h-obstacles">Obstacles</h2>
    <p class="intro">From Chapter 2 on, every chapter adds one new piece of circuitry. Each one arrives on an easy board with a one-line tip, and none of them hides anything: everything you need to solve a board is on it.</p>
    <div class="obstacles">{obstacles}</div>
  </section>

  <section class="section narrow" aria-labelledby="h-stars">
    <h2 id="h-stars">Stars</h2>
    <p class="intro">Stars reward a clean solve, never a fast one. A stroke is one drag, from touching the screen to letting go.</p>
    <ul class="stars">{stars}</ul>
    <p class="intro" style="margin-top:16px">Replay any level for more stars; your best result is kept. Stars open the later chapters.</p>
  </section>

  <section class="section" aria-labelledby="h-modes">
    <h2 id="h-modes">Three ways to play</h2>
    <div class="modes">{modes}</div>
  </section>

  <section class="section narrow" aria-labelledby="h-chapters">
    <h2 id="h-chapters">The chapters</h2>
    <p class="intro">Fifty levels each, getting gently harder, with a Challenge every sixth level and a boss at the end. A chapter opens when the previous boss is beaten and you have enough stars.</p>
    <ul class="chapters">{chapters}</ul>
  </section>
</div>
"""
    write("how-to-play/index.html", page(1, "How to play Lumiwire", "The rules of Lumiwire, every obstacle (dead chips, cut traces, fuses, relays, soldered traces, bridges, vias, wrap-around edges), stars, Journey, Daily and Blitz.", body, "how-to-play/", nav="how-to-play/"))


def build_support():
    faq = "".join(f'<details class="faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in FAQ)
    body = f"""
<div class="wrap narrow">
  <p class="crumbs"><a href="{link(1, '')}">Home</a> / Support</p>
  <section class="page-head"><h1>Support</h1><p class="essence">Something not right, or a question we haven't answered? Write to us.</p></section>
  <section class="section">
    <div class="contact">
      <span class="muted">Email</span>
      <a class="email" href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a>
      <p class="muted">It helps to include your phone model, its Android or iOS version, the level number, and a screenshot if something looks wrong. We read every message and usually reply within two working days.</p>
    </div>
  </section>
  <section class="section"><h2>Common questions</h2><div style="margin-top:12px">{faq}</div></section>
  <section class="section"><h2>Your data</h2>
    <p class="intro">Read the <a href="{link(1, 'privacy/')}">privacy policy</a> and the <a href="{link(1, 'terms/')}">terms of use</a>. To remove everything stored against your account, see <a href="{link(1, 'delete-account/')}">delete your account</a>.</p></section>
</div>
"""
    write("support/index.html", page(1, "Lumiwire support", f"Help with Lumiwire: the rules, the Daily, Blitz, leaderboards, purchases and deleting your account. Contact {SUPPORT_EMAIL}.", body, "support/", nav="support/"))


def build_legal(name, title, desc, nav=None):
    """Wraps legal/<name>.html (body only; {{EMAIL}}, {{PRIVACY}}, {{TERMS}}, {{DELETE}}, {{SUPPORT}},
    {{UPDATED}} and the <!--IF_SHOP_NOT_LIVE-->...<!--END--> note are filled in here)."""
    with open(os.path.join(ROOT, "legal", name + ".html"), encoding="utf-8") as f:
        b = f.read()
    start, end = "<!--IF_SHOP_NOT_LIVE-->", "<!--END-->"
    while start in b:
        i, j = b.index(start), b.index(end)
        b = b[:i] + ("" if SHOP_LIVE else b[i + len(start):j]) + b[j + len(end):]
    for k, v in {"{{EMAIL}}": SUPPORT_EMAIL, "{{UPDATED}}": UPDATED, "{{PRIVACY}}": link(1, "privacy/"),
                 "{{TERMS}}": link(1, "terms/"), "{{DELETE}}": link(1, "delete-account/"),
                 "{{SUPPORT}}": link(1, "support/")}.items():
        b = b.replace(k, v)
    assert "{{" not in b, name
    body = f'<div class="wrap narrow legal">\n<p class="crumbs" style="padding-top:0"><a href="{link(1, "")}">Home</a></p>\n{b.strip()}\n</div>'
    write(f"{name}/index.html", page(1, title, desc, body, f"{name}/", nav=nav))


def build_misc():
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    paths = ["", "how-to-play/", "support/", "privacy/", "terms/", "delete-account/"]
    urls = "".join(f"  <url><loc>{SITE_URL}/{p}</loc><lastmod>{LASTMOD}</lastmod></url>\n" for p in paths)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    write(".nojekyll", "")
    write("assets/site.css", CSS)
    body404 = f"""<div class="wrap narrow"><section class="page-head" style="padding-top:48px"><h1>That page isn't here</h1>
<p class="essence">It may have moved. Try the <a href="{link(0, '', True)}">home page</a>, <a href="{link(0, 'how-to-play/', True)}">how to play</a> or <a href="{link(0, 'support/', True)}">support</a>.</p></section></div>"""
    write("404.html", page(0, "Page not found · Lumiwire", "This page doesn't exist.", body404, "404.html", canonical=False, absolute=True))


SHOT_W, SHOT_H = 540, 1065
BOARD_W, BOARD_H = 600, 600
LASTMOD = "2026-11-11"


def build_images():
    src = os.path.join(ROOT, "images")
    out = os.path.join(OUT, "assets")
    os.makedirs(out, exist_ok=True)
    for name in sorted(os.listdir(src)):
        stem, ext = os.path.splitext(name)
        if ext != ".png" or stem == "icon":
            continue
        im = Image.open(os.path.join(src, name)).convert("RGB")
        size = (SHOT_W, SHOT_H) if stem.startswith("screen-") else (BOARD_W, BOARD_H)
        im.resize(size, Image.LANCZOS).save(os.path.join(out, stem + ".webp"), quality=86, method=6)
    icon = Image.open(os.path.join(src, "icon.png")).convert("RGB")
    for size, name in ((512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-touch-icon.png")):
        icon.resize((size, size), Image.LANCZOS).save(os.path.join(out, name), optimize=True)
    icon.resize((48, 48), Image.LANCZOS).save(os.path.join(OUT, "favicon.ico"), sizes=[(48, 48), (32, 32), (16, 16)])


if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)
build_home()
build_how_to_play()
build_support()
build_legal("privacy", "Lumiwire privacy policy", "What Lumiwire collects, why, who handles it, and what you can do about it.", nav="privacy/")
build_legal("terms", "Lumiwire terms of use", "The terms for using Lumiwire, including coins, Remove Ads and the leaderboards.")
build_legal("delete-account", "Delete your Lumiwire account", "How to delete your Lumiwire account and data, what is deleted, and what is kept.")
build_misc()
build_images()
print("built", OUT, "preview" if PREVIEW else "production", "shop live" if SHOP_LIVE else "shop not live")

#!/usr/bin/env python3
"""
Brophy Broncobots site builder.

Plain static output — no runtime dependencies, no framework. This script only
exists so the header, nav and footer live in ONE place instead of being copy-
pasted into every page.

    python3 tools/build.py

Reads   tools/content/<key>.html   (the body of each page)
Writes  <key>.html                (a complete, standalone page)

Each content file may start with an optional metadata block:

    <!--meta
    title: Page title
    desc: Meta description sentence.
    banner_img: assets/img/foo.jpg
    eyebrow: Section label
    h1: Big heading
    lede: One-sentence intro under the heading.
    crumbs: About > Our History
    hero: 1                      # use the tall home hero instead of a banner
    -->
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "tools", "content")

SITE_NAME = "Brophy Broncobots"
CAL_ID = "c_fe5d5cf7876ce9370b0a59588eee129457c6d5419cf31494028a567a9d710e06@group.calendar.google.com"

# ---------------------------------------------------------------- navigation
# (label, href, [children])  — children are (label, href, blurb)
NAV = [
    ("Home", "index.html", []),
    ("Programs", "programs.html", [
        ("FRC 991", "frc.html", "Our flagship competition team"),
        ("FTC Teams", "ftc.html", "Five student-led squads"),
        ("FLL", "fll.html", "Mentoring Loyola Academy scholars"),
    ]),
    ("About", "about.html", [
        ("Our History", "history.html", "How the program grew"),
        ("Leadership", "leadership.html", "Students and mentors"),
        ("Competitions", "competitions.html", "Where we compete"),
    ]),
    ("Parents", "parents.html", []),
    ("Calendar", "calendar.html", []),
    ("Resources", "documents.html", [
        ("Documents", "documents.html", "Forms, handbook, safety"),
        ("Weekly Bulletin", "bulletin.html", "What is happening this week"),
        ("Links", "links.html", "FIRST, tools and partners"),
    ]),
]

# every page key -> the top-level nav item it should highlight
ACTIVE_MAP = {
    "index": "Home",
    "programs": "Programs", "frc": "Programs", "ftc": "Programs", "fll": "Programs",
    "about": "About", "history": "About", "leadership": "About", "competitions": "About",
    "parents": "Parents",
    "calendar": "Calendar",
    "documents": "Resources", "bulletin": "Resources", "links": "Resources",
    "join": "", "404": "",
}


def nav_html(active_label):
    out = ['<nav class="nav" id="site-nav" aria-label="Main">', "<ul>"]
    for label, href, kids in NAV:
        is_active = label == active_label
        if kids:
            out.append("<li>")
            out.append(
                '<button class="navbtn" type="button" aria-expanded="false"%s>%s<i class="caret"></i></button>'
                % (" data-active" if is_active else "", label)
            )
            out.append('<ul class="dropdown">')
            out.append('<li><a href="%s">%s<small>Overview</small></a></li>' % (href, label))
            for klabel, khref, kblurb in kids:
                out.append('<li><a href="%s">%s<small>%s</small></a></li>' % (khref, klabel, kblurb))
            out.append("</ul></li>")
        else:
            cur = ' aria-current="page"' if is_active else ""
            out.append('<li><a href="%s"%s>%s</a></li>' % (href, cur, label))
    out.append("</ul>")
    out.append('<div class="nav-cta"><a class="btn sm" href="join.html">Join Us <span class="arrow">&rsaquo;</span></a></div>')
    out.append("</nav>")
    return "\n".join(out)


HEADER = """<a class="skip" href="#main">Skip to main content</a>
<div class="topbar">
  <div class="shell">
    <span class="creed">Trust &middot; Respect &middot; Commitment</span>
    <span class="links">
      <a href="parents.html">Parent Info</a>
      <a href="bulletin.html">Weekly Bulletin</a>
      <a href="join.html">Contact</a>
    </span>
  </div>
</div>
<header class="site-header">
  <div class="shell">
    <a class="brand" href="index.html">
      <img src="assets/img/logo-mark.png" alt="" width="46" height="46">
      <span class="brand-text">
        <span class="brand-name">Broncobots</span>
        <span class="brand-sub">Brophy College Preparatory</span>
      </span>
    </a>
    __NAV__
    <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="site-nav"><span></span></button>
  </div>
</header>
<div class="scrim" aria-hidden="true"></div>"""


FOOTER = """<footer class="site-footer">
  <div class="shell">
    <div class="footer-grid">
      <div>
        <div class="footer-brand">
          <img src="assets/img/logo-mark.png" alt="">
          <span>
            <b>Broncobots</b>
            <span>Brophy College Preparatory</span>
          </span>
        </div>
        <p class="small">Student-led robotics at Brophy College Preparatory in Phoenix, Arizona.
          One <em>FIRST</em> Robotics Competition team, five <em>FIRST</em> Tech Challenge teams,
          and a mentoring program for Loyola Academy scholars.</p>
        <p class="footer-creed">Trust. Respect. Commitment.</p>
      </div>
      <div>
        <h4>Programs</h4>
        <ul>
          <li><a href="frc.html">FRC 991</a></li>
          <li><a href="ftc.html">FTC Teams</a></li>
          <li><a href="fll.html">FLL Mentoring</a></li>
          <li><a href="competitions.html">Competitions</a></li>
        </ul>
      </div>
      <div>
        <h4>For Families</h4>
        <ul>
          <li><a href="parents.html">Parent Information</a></li>
          <li><a href="calendar.html">Team Calendar</a></li>
          <li><a href="documents.html">Documents &amp; Forms</a></li>
          <li><a href="bulletin.html">Weekly Bulletin</a></li>
          <li><a href="join.html">Join / Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Find Us</h4>
        <ul>
          <li>4701 N Central Ave<br>Phoenix, AZ 85012</li>
          <li><a href="mailto:broncobots@brophyprep.org">broncobots@brophyprep.org</a></li>
          <li><a href="https://www.brophyprep.org" target="_blank" rel="noopener">brophyprep.org</a></li>
          <li><a href="https://www.firstinspires.org" target="_blank" rel="noopener">firstinspires.org</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; __YEAR__ Brophy Broncobots. <em>FIRST</em>, FRC, FTC and <em>FIRST</em> LEGO League are trademarks of <em>FIRST</em>.</span>
      <span class="placeholder-note">Draft rebuild &mdash; contact details and rosters are placeholders.</span>
    </div>
  </div>
</footer>
<script src="assets/js/site.js"></script>"""


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<meta name="description" content="__DESC__">
<meta name="theme-color" content="#8a1425">
<meta property="og:title" content="__TITLE__">
<meta property="og:description" content="__DESC__">
<meta property="og:type" content="website">
<meta property="og:image" content="assets/img/logo-full.png">
<link rel="icon" href="assets/img/logo-mark-sm.png">
<link rel="apple-touch-icon" href="assets/img/logo-mark-sm.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
__HEADER__
<main id="main">
__TOP__
__BODY__
</main>
__FOOTER__
</body>
</html>
"""


def banner(meta):
    crumbs = ""
    if meta.get("crumbs"):
        parts = [p.strip() for p in meta["crumbs"].split(">")]
        bits = ['<a href="index.html">Home</a>']
        for p in parts:
            bits.append("<span>/</span>")
            bits.append(p)
        crumbs = '<div class="crumbs">%s</div>' % "".join(bits)
    img = meta.get("banner_img", "assets/img/pit-lineup.jpg")
    eyebrow = '<p class="eyebrow">%s</p>' % meta["eyebrow"] if meta.get("eyebrow") else ""
    lede = '<p class="lede">%s</p>' % meta["lede"] if meta.get("lede") else ""
    return """<section class="banner">
  <div class="banner-media"><img src="%s" alt=""></div>
  <div class="shell">
    %s
    %s
    <h1>%s</h1>
    %s
  </div>
</section>""" % (img, crumbs, eyebrow, meta.get("h1", ""), lede)


META_RE = re.compile(r"^<!--meta\s*(.*?)-->\s*", re.S)


def parse(src):
    meta, body = {}, src
    m = META_RE.match(src)
    if m:
        for line in m.group(1).strip().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or ":" not in line:
                continue
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
        body = src[m.end():]
    return meta, body


def build():
    if not os.path.isdir(CONTENT):
        sys.exit("missing content dir: " + CONTENT)
    keys = sorted(f[:-5] for f in os.listdir(CONTENT) if f.endswith(".html"))
    if not keys:
        sys.exit("no content files found in " + CONTENT)
    for key in keys:
        with open(os.path.join(CONTENT, key + ".html"), encoding="utf-8") as fh:
            meta, body = parse(fh.read())

        title = meta.get("title", key.title())
        full_title = title if key == "index" else "%s | %s" % (title, SITE_NAME)
        top = "" if meta.get("hero") else banner(meta)

        html = (PAGE
                .replace("__HEADER__", HEADER.replace("__NAV__", nav_html(ACTIVE_MAP.get(key, ""))))
                .replace("__FOOTER__", FOOTER.replace("__YEAR__", "2026"))
                .replace("__TITLE__", full_title)
                .replace("__DESC__", meta.get("desc", "Student-led robotics at Brophy College Preparatory."))
                .replace("__TOP__", top)
                .replace("__BODY__", body.strip())
                .replace("__CAL_ID__", CAL_ID.replace("@", "%40")))

        with open(os.path.join(ROOT, key + ".html"), "w", encoding="utf-8") as fh:
            fh.write(html)
        print("built %-16s %6.1f KB" % (key + ".html", len(html) / 1024))
    print("\n%d pages -> %s" % (len(keys), ROOT))


if __name__ == "__main__":
    build()

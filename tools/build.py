#!/usr/bin/env python3
"""
Brophy Broncobots site builder.

Plain static output — no runtime dependencies, no framework. This script exists
so the header, nav and footer live in ONE place, and so the sixteen robot
figures in rigs.py can be dropped into pages by name.

    python3 tools/build.py

Reads   tools/content/<key>.html   (the body of each page)
Writes  <key>.html                (a complete, standalone page)

Substitutions available inside a content file:
    __RIG:shooter__   -> the named inline SVG figure from rigs.py
    __CAL_ID__        -> the URL-encoded team calendar id

Optional metadata block at the top of a content file:

    <!--meta
    title: Page title
    desc: Meta description sentence.
    banner_img: assets/img/foo.jpg
    eyebrow: Section label
    h1: Big heading
    lede: One-sentence intro under the heading.
    crumbs: About > Leadership
    hero: 1            # page supplies its own hero, skip the banner
    -->
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rigs import RIGS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "tools", "content")

SITE_NAME = "Brophy Broncobots"
YEAR = "2026"
CAL_ID = "c_fe5d5cf7876ce9370b0a59588eee129457c6d5419cf31494028a567a9d710e06@group.calendar.google.com"

# ---------------------------------------------------------------- navigation
# (label, href, overview_label_or_None, [(label, href, blurb), ...])
#
# Reorganised around why somebody is here rather than around internal
# structure: what we compete in / who we are / how to get involved / when
# things happen / reference material.
NAV = [
    ("Home", "index.html", None, []),
    ("Teams", "teams.html", "All six teams", [
        ("FRC 991", "frc.html", "Flagship team, spring season"),
        ("FTC Teams", "ftc.html", "Five squads, fall season"),
        ("FLL Mentoring", "fll.html", "We coach Loyola Academy"),
    ]),
    ("About", "about.html", "Our story", [
        ("Leadership", "leadership.html", "Students run this program"),
        ("Results & Awards", "results.html", "How we have done"),
    ]),
    ("Join", "join.html", "Students — start here", [
        ("For Parents", "parents.html", "What FTC is, plainly"),
        ("Sponsors & Mentors", "support.html", "Give time, skills or funds"),
    ]),
    ("Calendar", "calendar.html", None, []),
    ("Resources", "bulletin.html", None, [
        ("Weekly Bulletin", "bulletin.html", "What is happening this week"),
        ("Documents & Forms", "documents.html", "Paperwork and handbook"),
        ("Links & Tools", "links.html", "FIRST, software, vendors"),
    ]),
]

# page key -> the top-level nav item it should highlight
ACTIVE_MAP = {
    "index": "Home",
    "teams": "Teams", "frc": "Teams", "ftc": "Teams", "fll": "Teams",
    "about": "About", "leadership": "About", "results": "About",
    "join": "Join", "parents": "Join", "support": "Join",
    "calendar": "Calendar",
    "bulletin": "Resources", "documents": "Resources", "links": "Resources",
    "404": "",
}


def nav_html(active):
    out = ['<nav class="nav" id="site-nav" aria-label="Main">', "<ul>"]
    for label, href, ov, kids in NAV:
        act = label == active
        if kids:
            out.append("<li>")
            out.append('<button class="navbtn" type="button" aria-expanded="false"%s>%s'
                       '<i class="caret"></i></button>' % (" data-active" if act else "", label))
            out.append('<ul class="dropdown">')
            if ov:
                out.append('<li><a href="%s">%s<small>Overview</small></a></li>' % (href, ov))
            for kl, kh, kb in kids:
                out.append('<li><a href="%s">%s<small>%s</small></a></li>' % (kh, kl, kb))
            out.append("</ul></li>")
        else:
            out.append('<li><a href="%s"%s>%s</a></li>'
                       % (href, ' aria-current="page"' if act else "", label))
    out.append("</ul>")
    out.append('<div class="nav-cta"><a class="btn sm" href="join.html">Join Us '
               '<span class="arrow">&rsaquo;</span></a></div>')
    out.append("</nav>")
    return "\n".join(out)


HEADER = """<a class="skip" href="#main">Skip to main content</a>
<div class="topbar">
  <div class="shell-wide">
    <span class="creed">Trust &middot; Respect &middot; Commitment</span>
    <span class="links">
      <a href="parents.html">Parents</a>
      <a href="bulletin.html">Bulletin</a>
      <a href="calendar.html">Calendar</a>
    </span>
  </div>
</div>
<header class="site-header">
  <div class="shell-wide">
    <a class="brand" href="index.html">
      <img src="assets/img/logo-mark.png" alt="" width="38" height="38">
      <span>
        <span class="brand-name">Broncobots</span>
        <span class="brand-sub">Brophy College Preparatory</span>
      </span>
    </a>
    __NAV__
    <button class="burger" type="button" aria-label="Menu" aria-expanded="false"
            aria-controls="site-nav"><span></span></button>
  </div>
</header>
<div class="scrim" aria-hidden="true"></div>"""


FOOTER = """<footer class="site-footer">
  <div class="shell">
    <div class="fgrid">
      <div>
        <div class="fbrand">
          <img src="assets/img/logo-mark.png" alt="">
          <span>
            <b>Broncobots</b>
            <span>Brophy College Preparatory</span>
          </span>
        </div>
        <p class="small">Student-led robotics in Phoenix, Arizona. One <em>FIRST</em> Robotics
          Competition team, five <em>FIRST</em> Tech Challenge teams, and a mentoring program for
          Loyola Academy scholars.</p>
        <p class="fcreed">Trust. Respect. Commitment.</p>
      </div>
      <div>
        <h4>Teams</h4>
        <ul>
          <li><a href="teams.html">All six teams</a></li>
          <li><a href="frc.html">FRC 991</a></li>
          <li><a href="ftc.html">FTC teams</a></li>
          <li><a href="fll.html">FLL mentoring</a></li>
        </ul>
      </div>
      <div>
        <h4>About</h4>
        <ul>
          <li><a href="about.html">Our story</a></li>
          <li><a href="leadership.html">Leadership</a></li>
          <li><a href="results.html">Results &amp; awards</a></li>
        </ul>
      </div>
      <div>
        <h4>Get involved</h4>
        <ul>
          <li><a href="join.html">Students</a></li>
          <li><a href="parents.html">Parents</a></li>
          <li><a href="support.html">Sponsors &amp; mentors</a></li>
        </ul>
      </div>
      <div>
        <h4>Season</h4>
        <ul>
          <li><a href="calendar.html">Calendar</a></li>
          <li><a href="bulletin.html">Weekly bulletin</a></li>
          <li><a href="documents.html">Documents</a></li>
          <li><a href="links.html">Links &amp; tools</a></li>
        </ul>
      </div>
    </div>
    <div class="fbot">
      <span>&copy; __YEAR__ Brophy Broncobots &middot; 4701 N Central Ave, Phoenix AZ 85012 &middot;
        <em>FIRST</em>, FRC, FTC and <em>FIRST</em> LEGO League are trademarks of <em>FIRST</em>.</span>
      <span class="ph">Draft rebuild &mdash; rosters and contact details are placeholders.</span>
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
        bits = ['<a href="index.html">Home</a>']
        for p in [x.strip() for x in meta["crumbs"].split(">")]:
            bits.append("<span>/</span>")
            bits.append(p)
        crumbs = '<div class="crumbs">%s</div>' % "".join(bits)
    eyebrow = '<p class="eyebrow">%s</p>' % meta["eyebrow"] if meta.get("eyebrow") else ""
    lede = '<p class="lede">%s</p>' % meta["lede"] if meta.get("lede") else ""
    return """<section class="banner">
  <div class="banner-media"><img src="%s" alt=""></div>
  <div class="shell">
    %s%s
    <h1>%s</h1>
    %s
  </div>
</section>""" % (meta.get("banner_img", "assets/img/pit-lineup.jpg"), crumbs, eyebrow,
                 meta.get("h1", ""), lede)


META_RE = re.compile(r"^<!--meta\s*(.*?)-->\s*", re.S)
RIG_RE = re.compile(r"__RIG:([a-z0-9_]+)__")

# ---------------------------------------------------------------- photos
# tools/photos.json records each photo's real pixel size and orientation.
# It is used for two things: stamping width/height on every <img> so the
# page never reflows as photos load, and refusing to build if a portrait
# photo has been dropped into a landscape box (or vice versa), which is
# what mangled the group shots the first time round.
with open(os.path.join(ROOT, "tools", "photos.json"), encoding="utf-8") as _fh:
    PHOTOS = json.load(_fh)

IMG_RE = re.compile(r'<img([^>]*?)src="assets/img/([a-z0-9-]+)\.jpg"([^>]*?)>')
SLOT_RE = re.compile(
    r'class="([^"]*\b(?:ph-w|ph-t|ph-s|ph-wide|card-media|card-media tall)\b[^"]*)"'
    r'[^>]*>\s*<img[^>]*src="assets/img/([a-z0-9-]+)\.jpg"')

# which orientations each slot legitimately accepts
SLOT_OK = {
    "ph-w":    ("landscape",),
    "ph-wide": ("landscape",),
    "ph-t":    ("portrait",),
    "ph-s":    ("square",),
    "card-media": ("landscape",),
}


def stamp_images(body, page, problems):
    """Add real width/height plus lazy loading to every photo."""
    def repl(m):
        pre, name, post = m.group(1), m.group(2), m.group(3)
        meta = PHOTOS.get(name)
        if not meta:
            problems.append("%s: unknown photo %s.jpg" % (page, name))
            return m.group(0)
        attrs = pre + post
        add = ""
        if "width=" not in attrs:
            add += ' width="%d" height="%d"' % (meta["w"], meta["h"])
        if "loading=" not in attrs:
            add += ' loading="lazy" decoding="async"'
        return '<img%ssrc="assets/img/%s.jpg"%s%s>' % (pre, name, post, add)
    return IMG_RE.sub(repl, body)


def check_orientation(body, page, problems):
    for cls, name in SLOT_RE.findall(body):
        meta = PHOTOS.get(name)
        if not meta:
            continue
        slot = "card-media" if "card-media" in cls and "tall" not in cls else None
        if slot is None:
            for key in ("ph-wide", "ph-w", "ph-t", "ph-s"):
                if key in cls.split():
                    slot = key
                    break
        if slot is None:
            continue
        ok = SLOT_OK.get(slot)
        if ok and meta["orient"] not in ok:
            problems.append(
                "%s: %s.jpg is %s but sits in .%s (needs %s)"
                % (page, name, meta["orient"], slot, "/".join(ok)))


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
        sys.exit("no content files in " + CONTENT)

    missing_rigs, used_rigs = set(), set()
    problems = []

    for key in keys:
        with open(os.path.join(CONTENT, key + ".html"), encoding="utf-8") as fh:
            meta, body = parse(fh.read())

        def sub_rig(m):
            name = m.group(1)
            if name not in RIGS:
                missing_rigs.add(name)
                return "<!-- missing rig: %s -->" % name
            used_rigs.add(name)
            return RIGS[name].strip()

        body = RIG_RE.sub(sub_rig, body)
        check_orientation(body, key + ".html", problems)
        body = stamp_images(body, key + ".html", problems)

        title = meta.get("title", key.title())
        full = title if key == "index" else "%s | %s" % (title, SITE_NAME)

        html = (PAGE
                .replace("__HEADER__", HEADER.replace("__NAV__", nav_html(ACTIVE_MAP.get(key, ""))))
                .replace("__FOOTER__", FOOTER.replace("__YEAR__", YEAR))
                .replace("__TITLE__", full)
                .replace("__DESC__", meta.get("desc", "Student-led robotics at Brophy College Preparatory."))
                .replace("__TOP__", "" if meta.get("hero") else banner(meta))
                .replace("__BODY__", body.strip())
                .replace("__CAL_ID__", CAL_ID.replace("@", "%40")))

        with open(os.path.join(ROOT, key + ".html"), "w", encoding="utf-8") as fh:
            fh.write(html)
        print("built %-18s %6.1f KB" % (key + ".html", len(html) / 1024))

    print("\n%d pages -> %s" % (len(keys), ROOT))
    unused = set(RIGS) - used_rigs
    if unused:
        print("note: rigs defined but unused: " + ", ".join(sorted(unused)))
    if problems:
        print("\nPHOTO PROBLEMS:")
        for pr in problems:
            print("  " + pr)
    if missing_rigs:
        sys.exit("ERROR: content referenced undefined rigs: " + ", ".join(sorted(missing_rigs)))
    if problems:
        sys.exit("ERROR: fix the photo problems above (orientation must match the slot).")


if __name__ == "__main__":
    build()

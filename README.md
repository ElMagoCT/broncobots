# Brophy Broncobots — site rebuild

A rebuild of <https://sites.google.com/brophyprep.org/broncobots/> as a plain
static site: hand-written HTML/CSS/JS, no framework, no runtime dependencies.

Source for the rebuild was the Google Sites archive
(`sites.google.com-brophyprep.org-broncobots-*.zip` + `.z01`). Only the home
page was captured in that archive, so the home page copy is **verbatim from the
real site** and every subpage is newly written placeholder content that follows
the original navigation structure.

## Live site

| | |
| --- | --- |
| Production | <https://broncobots.netlify.app> |
| Netlify admin | <https://app.netlify.com/projects/broncobots> |
| GitHub repo | <https://github.com/ElMagoCT/broncobots> (public) |

Publish an update:

```bash
export PATH="$HOME/.local/node-v24.19.0-darwin-arm64/bin:$PATH"
cd ~/Documents/Workspace/broncobots-site
python3 tools/build.py          # only if you edited anything under tools/
netlify deploy --prod --dir .
```

Upload *is* the deploy — there is no build step. Drop `--prod` for a temporary
draft URL to review before going live.

Auto-deploy from `git push` is not wired up yet; see `DEPLOY-PROMPT.md` for the
last step (it needs a browser or a real terminal, because `netlify init` cannot
be automated).

## Run it locally

```bash
cd ~/Documents/Workspace/broncobots-site && python3 -m http.server 8752
```

Then open <http://localhost:8752>. There is no build step for viewing — the
`.html` files at the repo root are the site.

## Pages

Navigation is organised around why somebody is visiting, not around internal
structure.

| Section | Page | File | Signature figure |
| --- | --- | --- | --- |
| — | Home | `index.html` | **shooter** — drives on, elevates, spins up, scores |
| Teams | All six teams | `teams.html` | **scale** — three robots to scale, chip-selectable |
| Teams | FRC 991 | `frc.html` | **lift** — three-stage elevator places a game piece |
| Teams | FTC teams | `ftc.html` | **cube** — the 18″ rule, arm unfolds past it |
| Teams | FLL mentoring | `fll.html` | **mission** — robot drives the table, blocks assemble |
| About | Our story | `about.html` | **gears** — the creed as a working gear train |
| About | Leadership | `leadership.html` | **signal** — hub sends signal to each subteam |
| About | Results & awards | `results.html` | **board** — alliance scoreboard fills in |
| Join | Students | `join.html` | **builder** — pick a subteam, it lights up (interactive) |
| Join | For parents | `parents.html` | **matchclock** — a real 2:30 match, scrubbed |
| Join | Sponsors & mentors | `support.html` | **power** — support as power distribution |
| — | Calendar | `calendar.html` | **track** — a robot drives the season |
| Resources | Weekly bulletin | `bulletin.html` | **status** — diagnostic panel boots up |
| Resources | Documents & forms | `documents.html` | **checklist** — inspection ticks off |
| Resources | Links & tools | `links.html` | **traces** — PCB traces energise |
| — | Not found | `404.html` | **wheeloff** — a wheel comes off |

### Renamed pages

The 2026 reorganisation renamed three files. `netlify.toml` holds 301s so every
previously published URL still works:

| Old | New |
| --- | --- |
| `programs.html` | `teams.html` |
| `competitions.html` | `results.html` |
| `history.html` | `about.html` (History merged into Our Story) |

`support.html` is new, so Join now covers students, parents and supporters
together rather than scattering them.

## The scroll rigs

All sixteen figures live in `tools/rigs.py` as plain inline SVG and share one
parts vocabulary (`.fr`/`.fr2`/`.ac`/`.wire`/`.dim` materials, the same gear
tooth geometry and lightening-hole pattern), which is what makes very different
animations read as one machine shop. `assets/js/site.js` drives them.

Two mechanisms:

- **Pinned scrubber** — `.rig-track[data-rig="name"]` with `--len` in viewport
  multiples. Stage and copy both pin, so the scroll distance is spent scrubbing
  the animation rather than scrolling past blank space. Used on the five
  flagship pages.
- **Inline figure** — `[data-rig="name"]` anywhere else. Animates as it passes
  through the viewport at **zero extra page height**. Used on the other ten.

Each figure exposes animated pieces as `data-part="..."` hooks; a handler in the
`RIGS` registry receives `(element, progress 0..1)`. To add one, write the SVG
in `rigs.py`, add a handler with the same key in `site.js`, and drop
`__RIG:name__` into a content file.

Interactive figures use `data-chips="<figure>" data-panels="<panels>"` on a chip
row; the selected key highlights `[data-module]` in the figure and reveals the
matching `[data-panel]`.

**Without JavaScript** every page still works: pinned tracks collapse to normal
flow (no dead space), and each figure renders in its resting pose. The same
applies under `prefers-reduced-motion`.

## Editing

The header, nav and footer live in exactly one place: `tools/build.py`. Page
bodies live in `tools/content/<page>.html`. After editing either, rebuild:

```bash
python3 tools/build.py
```

That regenerates the root `.html` files. Do not hand-edit the root `.html`
files — they are generated and will be overwritten.

Each content file starts with an optional metadata block that drives the
`<title>`, meta description, and page banner:

```html
<!--meta
title: Page title
desc: Meta description sentence.
banner_img: assets/img/foo.jpg
eyebrow: Section label
h1: Big heading
lede: One-sentence intro.
crumbs: About > Our History
hero: 1          # use the tall home hero instead of a banner
-->
```

To add a page: drop a new file in `tools/content/`, add it to `NAV` and
`ACTIVE_MAP` in `tools/build.py`, and rebuild.

## Calendar

The calendar page embeds the real team calendar,
**Broncobots Calendar 2026‑27** (`c_fe5d5cf7…@group.calendar.google.com`,
America/Phoenix). The calendar ID lives in one place — `CAL_ID` in
`tools/build.py` — and is substituted into the page as `__CAL_ID__`.

The embed works today, but the calendar is shared publicly only at the
**"See only free/busy"** level, so public visitors see correct dates and times
with the event titles hidden. Signed-in Brophy accounts see full detail. To show
titles to everyone, the calendar owner changes sharing to
**"Make available to public → See all event details"**; nothing on the page needs
to change.

Three real dates were confirmed on the calendar and are mirrored in the
"On the calendar right now" list, with placeholder titles:

- Sat Sep 12, 8:00 a.m. – 2:00 p.m.
- Fri Sep 18, 5:00 – 8:00 p.m.
- Sat Sep 19, 7:00 a.m. – 6:00 p.m.

## Assets

- `assets/img/logo-full.png`, `logo-mark.png` — the real Broncobots logos,
  extracted from the Google Sites archive.
- 40 photographs, also from the archive, resized to max 1600px progressive JPEG.
  Filenames are descriptive (`frc-991-award.jpg`, `fll-mentoring.jpg`, …).
- `favicon.ico` — generated from the logo mark.
- Fonts are Google Fonts (Barlow Condensed, Inter, JetBrains Mono) with local
  fallback stacks, so the site degrades gracefully offline.

## Before this goes public

Everything below is a deliberate placeholder:

1. **Contact address** — `broncobots@brophyprep.org` appears in the footer, the
   parent page, and the join page. Confirm or replace.
2. **Forms** — `join.html` is not wired to a backend. It intercepts submit and
   says so. Point it at Netlify Forms, a Google Form, or the team inbox.
3. **Documents** — every link on `documents.html` is `href="#"`.
4. **Roster** — all names on `leadership.html`. Check with families before
   publishing student names or photos (the repo is public, so git history counts).
5. **History and results** — the timeline on `about.html` and the tables on
   `results.html` are structured templates, not the real record.
6. **Stats** — team counts, student counts, seasons, dues, and hour estimates.
7. **Social links** — not yet added anywhere.
8. **Sponsorship tiers** — amounts and benefits on `support.html`.

Placeholder content is marked in the UI with gold "placeholder" callouts and a
note in the footer, so nothing accidentally reads as fact.

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

| Page | File | Notes |
| --- | --- | --- |
| Home | `index.html` | Copy is verbatim from the original Google Site |
| Programs | `programs.html` | Overview + FRC/FTC/FLL comparison table |
| FRC 991 | `frc.html` | Subteams, season rhythm, gallery |
| FTC Teams | `ftc.html` | Teams 201, 202, 23737, 26983, 30596 |
| FLL | `fll.html` | Loyola Academy mentoring program |
| About | `about.html` | Mission, creed, how the team is run |
| Our History | `history.html` | Placeholder milestone timeline |
| Leadership | `leadership.html` | Placeholder roster |
| Competitions | `competitions.html` | Placeholder schedule + awards |
| **Parent Information** | `parents.html` | **New page** — see below |
| Calendar | `calendar.html` | Live Google Calendar embed |
| Documents | `documents.html` | Placeholder forms/handbook links |
| Weekly Bulletin | `bulletin.html` | Placeholder current issue + archive |
| Links | `links.html` | Real external links (FIRST, tools, vendors) |
| Join Us | `join.html` | Placeholder mailing-list form |
| Not found | `404.html` | |

## The parent information page

`parents.html` is the new page that did not exist on the original site. It
explains, in plain English for a non-technical parent:

- what *FIRST* Tech Challenge actually is (the game, the robot, a match, awards)
- a month-by-month season timeline
- an honest three-tier time-commitment table
- what a student learns, technical and otherwise
- costs, and that assistance is available
- six concrete ways parents can help
- what to expect on a competition day
- how shop safety actually works
- a FAQ accordion
- a glossary translating the *FIRST* acronym soup

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
   publishing student names or photos.
5. **History and results** — the timelines on `history.html` and tables on
   `competitions.html` are structured templates, not the real record.
6. **Stats** — team counts, student counts, seasons, dues, and hour estimates.
7. **Social links** — not yet added anywhere.

Placeholder content is marked in the UI with gold "placeholder" callouts and a
note in the footer, so nothing accidentally reads as fact.

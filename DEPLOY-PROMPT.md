# Turning on auto-deploy — Claude-in-Chrome prompt

The site is already live at <https://broncobots.netlify.app>, deployed from this
machine with the Netlify CLI. Everything below is only about the last step:
making a `git push` to `main` publish automatically, and giving pull requests
their own preview URLs.

**Why this needs a browser.** `netlify init` is the CLI command for this, but it
uses interactive prompts that crash when driven programmatically
(`ERR_USE_AFTER_CLOSE: readline was closed`) — it dies partway through and
leaves things half-configured. So it's either a human in a real terminal
(Option B below) or the dashboard in a browser (Option A). Don't let anything
try to pipe input into `netlify init`.

## Current state

| Thing | Value |
| --- | --- |
| Live URL | <https://broncobots.netlify.app> |
| Netlify project | `broncobots` (team: micahctucker's team) |
| Netlify admin | <https://app.netlify.com/projects/broncobots> |
| GitHub repo | <https://github.com/ElMagoCT/broncobots> (public) |
| Branch | `main` |
| Build command | none — there is no build step |
| Publish directory | `.` (the repo root **is** the site) |

`netlify.toml` is committed at the repo root and already declares
`publish = "."` with an empty build command. That means a git-connected deploy
picks up the right settings **regardless of what the dashboard fields say** —
which is the safeguard against an empty build being published over the live
site. Nothing needs to be typed into those fields.

---

## Option A — the browser prompt

Copy everything between the lines into a Claude session connected to your Chrome
(the one where you're signed in to Netlify and GitHub as `ElMagoCT`).

---

Connect an existing Netlify site to a GitHub repo so it auto-deploys. Work in
the browser; I'm already signed in to both Netlify and GitHub.

1. Go to
   <https://app.netlify.com/projects/broncobots/configuration/deploys>
2. If either Netlify or GitHub asks me to sign in, **stop and tell me** —
   describe the screen. Do not enter any credentials, and do not create any
   account.
3. Find **Continuous deployment** and the button to link a repository (it may
   read "Link repository" or "Set up continuous deployment"). Choose **GitHub**
   as the provider.
4. If GitHub asks to authorize or install the Netlify app, **describe exactly
   what permissions it's requesting and wait for my go-ahead** before clicking
   Authorize or Install. If it offers a choice, prefer granting access to only
   the `broncobots` repository rather than all repositories.
5. Select the repository **`ElMagoCT/broncobots`** and branch **`main`**.
6. Build settings — this is a plain static site with no build step:
   - **Build command:** leave completely empty
   - **Publish directory:** `.` (a single dot)
   Read these back to me before saving. The repo has a `netlify.toml` that sets
   both correctly, so empty fields are expected and fine.
7. Save, then confirm the project page shows it's linked to
   `ElMagoCT/broncobots` and deploying from `main`.
8. If a deploy kicks off automatically, wait for it and tell me whether it
   succeeded. Then open <https://broncobots.netlify.app> and confirm the home
   page still loads with its photos and styling intact — the team logo in the
   header, the dark hero image, and the three program cards.

Report back: whether linking succeeded, what the build log said, and whether the
live site still renders correctly.

**Do not:** change the site name, touch DNS or custom domains, alter billing or
account settings, delete anything, or accept a plan upgrade. If Netlify shows a
payment or upgrade prompt, stop and tell me. If a build fails, give me the error
rather than retrying it.

---

## Option B — do it yourself in a terminal

Faster if you'd rather not drive a browser. Run this in your own Terminal (not
through Claude Code — the prompts need a real TTY):

```bash
export PATH="$HOME/.local/node-v24.19.0-darwin-arm64/bin:$PATH"
cd ~/Documents/Workspace/broncobots-site
netlify init
```

Answer:

- **"What would you like to do?"** → connect this directory to an existing
  Netlify project (it's already linked to `broncobots`)
- **Build command** → leave blank, press Enter
- **Directory to deploy** → `.`
- **Netlify functions folder** → leave blank, press Enter
- **"Overwrite existing netlify.toml?"** → **No**

Netlify's GitHub token is already cached from an earlier authorization, so this
shouldn't need a browser. If it does open one silently and you need the URL, it's
built in `netlify-cli/dist/utils/gh-auth.js` as
`https://app.netlify.com/cli?host=http://localhost:<port>&provider=github` —
find the port with `lsof -nP -iTCP -sTCP:LISTEN -a -p <pid>`. Don't hand-build an
`/authorize?client_id=...` URL; those 404.

---

## How to verify it worked

Make a trivial change, push it, and watch it appear without touching the CLI:

```bash
cd ~/Documents/Workspace/broncobots-site
git commit --allow-empty -m "Test auto-deploy"
git push
```

Then check <https://app.netlify.com/projects/broncobots/deploys> — a new deploy
should start within a few seconds, triggered by the push rather than by an
upload.

## Publishing without auto-deploy

Until (or instead of) linking, publishing stays a one-liner from this machine:

```bash
export PATH="$HOME/.local/node-v24.19.0-darwin-arm64/bin:$PATH"
cd ~/Documents/Workspace/broncobots-site
netlify deploy --prod --dir .
```

Drop `--prod` to get a temporary draft URL to review before going live.

Remember to run `python3 tools/build.py` first if you edited anything in
`tools/` — the root `.html` files are generated.

## Inviting collaborators

Adding someone to the repo is an invite from your account, so do it yourself:
<https://github.com/ElMagoCT/broncobots/settings/access>

A collaborator needs no toolchain for this site — clone it and run
`python3 -m http.server 8752`, then open <http://localhost:8752>.

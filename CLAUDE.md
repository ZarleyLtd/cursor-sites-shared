# CLAUDE.md — CursorSites (shared conventions)

This file provides guidance to Claude Code (claude.ai/code) for every project under `C:\CursorSites`. Claude Code loads it in addition to each app's own `CLAUDE.md`. Each folder is a separate git repo in the **ZarleyLtd** GitHub org; the root folder itself is not a repo. Where an app's `CLAUDE.md` differs from this file, the app's file wins.

These apps used to be built with Cursor. The shared patterns are now Claude skills. Some repos still have `.cursorrules` or `.cursor/rules/`; everything important from those files has been copied into each app's `CLAUDE.md`.

## Where this file lives

- The canonical copy is `cursor-sites-shared/CLAUDE.md` in the public repo **ZarleyLtd/cursor-sites-shared**. `C:\CursorSites\CLAUDE.md` only imports it. Edit the repo copy, then commit and push, because Edison's cloud agent reads the pushed version.
- The skills live in `cursor-sites-shared/skills/`. Each `~/.claude/skills/<name>` folder on the owner's PC is a directory junction into that folder.
- Paths such as `cursor-sites-shared/ui/...` or `FamilyTree/assets/...` in this file and the skills are relative to the **CursorSites root**: the folder that holds every app (`C:\CursorSites` locally, `..` from inside an app).
- **Edison cloud runs:** when an Edison ticket runs Claude in GitHub Actions, the workflow rebuilds this layout. The app is checked out with `cursor-sites-shared`, FamilyTree, ierne-snooker, Edison and PubliiCrossguns beside it, this file is copied to the parent folder, and the skills are installed. Other apps are not there. In those runs, change and commit only the app being worked on. If the ticket needs a change to shared code, say so in the summary instead.

## Apps

| Folder | What it is |
|---|---|
| BGS | Golf society site (society `botanic`); uses theGolfApp's tables |
| theGolfApp | Multi-tenant golf society app (`?societyId=`) |
| PubliiCrossguns | CrossGuns Snooker League (GitHub repo `CrossGunsSnooker`) |
| ierne-snooker | Snooker league; reference app for competitions, knockouts and accounts |
| ierne-tennis | Tennis section: singles and doubles leagues, knockouts and ladders with set-by-set scores; forked from ierne-snooker |
| FamilyTree | Family tree viewer/editor; reference app for contextual help and accounts |
| Scrabble | Multiplayer Scrabble played through a shared link |
| Splitify | AI bill-splitting app |
| theConfessional | Bar-bill claims app (its share/portion claims must stay in step with Splitify's) |
| RnR | Holiday home booking app |
| Edison | Ticket tracker for all these apps (GitHub issues labelled `edison`) |
| 4NextBus | Live Python Alexa skill on AWS Lambda; a different stack from the web apps. It now covers buses, trams, DART and local trains |
| 4NextDart / 4NextTram / 4NextLocalTrain | **Legacy, not deployed.** Deleted from the Amazon servers; 4NextBus now does their job. Skip them in tasks that apply to all apps, and change them only when the user names one |
| HelloWorldCursorSite | Test site (GitHub repo `HelloWorldCursor`) |
| cursor-sites-shared | Shared conventions (this file), skills, UI code, specs and the sync script (GitHub repo `cursor-sites-shared`) |
| `_pr-previews` | Worktrees of PRs, created by `Edison/tools/preview-pr.ps1` |

## Shared patterns → skills

When the user names one of these patterns, use the matching skill. Each skill points to the canonical spec in `cursor-sites-shared/`.

| Pattern / phrase | Skill | Canonical spec |
|---|---|---|
| Brief message | `brief-message` | `cursor-sites-shared/ui/BRIEF_MESSAGE.md` |
| Confirm dialog | `confirm-dialog` | `cursor-sites-shared/ui/CONFIRM_DIALOG.md` |
| Working indicator | `working-indicator` | `cursor-sites-shared/ui/WORKING_INDICATOR.md` |
| Contextual help (click-to-target **?**) | `contextual-help` | `cursor-sites-shared/ui/CONTEXTUAL_HELP.md` |
| "Edison-style installable app" | `installable-app` | `cursor-sites-shared/installable-app/INSTALLABLE_APP.md` |
| "Connect-style user account" | `user-account` | `cursor-sites-shared/account/USER_ACCOUNT.md` |
| Shared Supabase database | `shared-supabase` | `cursor-sites-shared/supabase/SHARED_DATABASE.md` |
| JP logo ("Created by" footer credit) | `jp-logo` | `cursor-sites-shared/jp-logo/JP_LOGO.md` |

Pick the pattern by situation:

- **Brief message:** feedback that needs no choice.
- **Confirm dialog:** a Yes/No question. Never use `window.confirm`.
- **Working indicator:** work taking longer than 500 ms.
- **Contextual help:** explaining what a control does.

The overview of all patterns is `cursor-sites-shared/CONVENTIONS.md`.

### File encoding

- Save every file as **UTF-8 without a BOM**. The exception is `.ps1` scripts: save those as **UTF-8 with a BOM**, because Windows PowerShell 5.1 misreads `.ps1` files that have no BOM.
- Never write files through PowerShell `>`, `Out-File` or `Set-Content` unless you pass `-Encoding utf8`. Those commands can write UTF-16, and GitHub Pages serves every file as UTF-8, so a UTF-16 `.js` file fails to parse in the browser.
- `sync-ui.ps1` refuses to copy a source file that isn't UTF-8.

### Synced UI code

The brief message, confirm dialog and working indicator code lives in `cursor-sites-shared/ui/*.js|css`. Each app has a synced copy at `assets/js/utils/` and `assets/css/`. To change one:

1. Edit the canonical file in `cursor-sites-shared/ui/`. **Never edit an app's copy.**
2. Run `powershell -ExecutionPolicy Bypass -File cursor-sites-shared\scripts\sync-ui.ps1`.
3. Commit in each affected app repo.

The JP logo is synced the same way from `cursor-sites-shared/jp-logo/`: the PNG and animated SVG go to `assets/icons/`, `jp-logo.js` to `assets/js/components/` and `jp-logo.css` to `assets/css/`.

The target list for each pattern is defined in the script. FamilyTree's sheet-based confirm is intentionally not synced. Contextual help, installable app and user account are specs only: copy from the reference app, nothing is synced.

### Candidates (not yet shared patterns)

Turn one of these into a spec plus skill only when the user asks or when reuse is clear:

- client image compression (`image-compress.js`, about 100 KB JPEG, in many apps)
- Admin Mode unlock (golf, snooker, crossguns, scrabble), which is separate from user accounts
- an app shell / bottom sheet (`openSheet`)

## Common web-app architecture

Most of the web apps share this shape. Check the app's own `CLAUDE.md` for exceptions; for example, RnR uses a single `app.js` with Tailwind, and Edison has no Supabase.

- **Frontend:** static HTML, plain CSS and vanilla JS. There is **no build step and no bundler**. Hosted on GitHub Pages from `main`.
- **Local dev server:** none. Serve the folder statically with `npx serve .` (http://localhost:3000). Edison uses `python -m http.server 4173`. Pages call the **deployed** Edge Function, so local runs use live data.
- **Running an app locally:** when the user asks to run, start or preview an app locally, start its dev server as a background task (use the app's own port if its `CLAUDE.md` names one), check that the URL responds, and then tell the user to open it in VS Code's centre window: `Ctrl+Shift+P` → **Simple Browser: Show** → paste the URL. Give the full URL, including the page (for example `http://localhost:3000/index.html`). Don't open an external browser.
- **JS layout:**
  - `assets/js/config/` holds the API URL. This is the only place to change it.
  - `assets/js/utils/` holds shared helpers.
  - `assets/js/components/` holds reusable UI.
  - `assets/js/pages/` holds one module per page.
  - `main.js` is the router.
- **Load order:** pages load scripts in the order **config → utils → components → pages → main.js**. Scripts are plain globals, not ES modules, except where an app says otherwise.
- **No duplication:** shared logic goes in utils or components. When changing behaviour, update utils first, then components, then pages.
- **HTML components:** shared header, nav and footer markup lives in `components/*.html` and is **pasted** into every page; there are no runtime includes. To change one, edit `components/` first, then copy the change to every `.html` page.
- **Paths:** use relative paths only, such as `assets/css/style.css`. Never use `/assets/...`, absolute URLs, `http://localhost` or drive letters in shipped files.
- **CORS-simple requests:** use GET with no custom headers. For POST, use either `application/x-www-form-urlencoded` (golf and snooker apps) or `text/plain;charset=UTF-8` with a JSON string body (Scrabble, FamilyTree, theConfessional). This avoids preflight requests. Never set `Content-Type: application/json` on a GET.
- **Backend:** one Supabase Edge Function per app, named `<app>-api`, deployed with `--no-verify-jwt`. It runs on the shared **Apps** project (`yzyipxvlsoxfphwobfkb`) and each app has its own schema. **Never run `supabase db push`**; use the `shared-supabase` skill. The browser never holds the service role key.
- **Images:** compress in the browser to about 100 KB JPEG before upload. Never upload originals.
- **PWAs:** in apps with `sw.js`, update the shell list and bump the cache name whenever page assets change. Splitify instead uses an asset-version cache-bust; see its `CLAUDE.md`.
- **Legacy:** `backend/code.gs` (Google Apps Script plus Sheets) and `rnrREADME.md` files are reference only. Don't change them.

## Edison tickets

Edison files each ticket as a GitHub issue labelled `edison` in the target app's repo, and moves the issue through `stage:*` labels. When asked to work an Edison issue:

1. Read the issue body, its comments and any linked screenshots.
2. If a PR for the issue is already open, continue on its branch and act on every note since the last round, oldest first. Don't open another PR.
3. Otherwise, make the change on a new branch and open a PR that references the issue. **Never merge it.**
4. Comment a short summary of what changed and how to review it.
5. Replace `stage:working` with `stage:review` when the round is done, even if no code changed.
6. If blocked, comment the question and replace `stage:working` with `stage:needs-input`.

## Git

- Several repos often have uncommitted work in progress. Commit only the files belonging to the current task, using `git commit -- <paths>`, and leave the user's other changes alone.
- Pull before starting work in a repo.

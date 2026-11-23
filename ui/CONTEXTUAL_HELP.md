# UI pattern: Contextual help (click-to-target)

Opt-in help for a static page. The user taps a **?** button, then taps any control. The next pointer is swallowed (the control does not run) and a short popover explains that control.

The copy describes the **feature**, never a particular record. A person row explains “opens that profile”; it does not narrate that person.

Originated in **FamilyTree** (Phase 4). The reference implementation lives in that repo. This file is the spec to follow when adding the same pattern to another CursorSites app. The engine is not copied by `scripts/sync-ui.ps1`: the catalog is app copy, and a few CSS offsets match FamilyTree’s shell.

## When to use

- A phone-first app with many controls whose job is not obvious from the label alone
- Charts, lists, and forms where a permanent tooltip would cover the content
- Overlays (sheets, lightbox) whose fields need the same explainers as the page

## When to use something else

- A one-time illustrated walkthrough of the whole product → a dialog, as in Splitify’s “How it works” strip
- Feedback after an action (“Link copied”, “Nothing to save”) → [brief message](BRIEF_MESSAGE.md)
- Errors the user must act on → an inline error or a confirm sheet
- A long manual → a separate help page

## What the user does

1. Tap **?** in the page header. The button sets `aria-pressed="true"`. The cursor becomes `help`. A banner under the header says “Tap something to learn what it does.”
2. Tap any control. That gesture does not activate it: links do not navigate, buttons do not fire, charts do not pan.
3. A popover opens next to the nearest marked control, with a title and one paragraph. If nothing is marked, the popover explains the page.
4. Dismiss the popover with its **×**, a tap outside it, or Escape.
5. Tap **?** again, or press Escape while help is armed, to leave help mode without opening a popover.

The same **?** is repeated in the header of any overlay that covers the page header (sheets, lightbox), so the user can explain fields inside the overlay.

## Pieces

| Piece | FamilyTree path | Shared? |
|-------|-----------------|---------|
| Engine | `assets/js/components/contextual-help.js` (`window.ContextualHelp`) | Copy and retarget. Not synced. |
| Styles | `assets/css/contextual-help.css` (imported from `style.css`) | Copy and retarget the shell offsets. |
| Catalog | `assets/js/utils/help-catalog.js` (`window.FamilyTreeHelpCatalog`) | Write per app. Never share another app’s copy. |
| Markup | `data-help-toggle` on **?**, `data-help="area.control"` on controls | Per page. |
| Boot | `ContextualHelp.init()` in `assets/js/main.js`, before the page module’s `init()` | Same call in the new app. |

The engine listens on `document` in the **capture** phase. Controls added later (a redrawn chart, an opened sheet) work without calling `init` again.

## Markup

**?** button. Put one in the page header and one in each overlay header. The visible label is `?`. The accessible name says what the mode does.

```html
<button type="button" class="app-header__btn" data-help-toggle
  aria-pressed="false" aria-label="Help: tap, then tap a control" title="Help">?</button>
```

Any element can be a target. The attribute value is a key in the catalog’s `topics` map. Put it on the control the user thinks they are tapping (the button, the row, the card), not on an inner icon.

```html
<button type="button" id="sortBtn" data-help="people.sort">Surname</button>
<a class="quick" href="people.html" data-help="home.quickPeople">People</a>
<section class="card" data-help="home.changes">…</section>
```

SVG nodes use the same attribute. `Element.closest` works on SVG elements.

```javascript
el('g', { 'class': 'node', 'data-help': 'tree.personNode' }, parent);
```

### Nearest ancestor wins

Resolution walks from the event target upward and uses the first `data-help`. A button inside a card can have its own topic while the card has a broader one. Tapping the card’s padding (no inner `data-help`) explains the card. Tapping a control with no `data-help` anywhere above it explains the **page**.

Do not put `data-help` on the **?** button. The engine treats `[data-help-toggle]` as the mode switch and never as a topic.

## Catalog

One global object. FamilyTree names it `window.FamilyTreeHelpCatalog`. A new app should use its own name and point the engine’s `catalog()` function at it (see [Copying into another app](#copying-into-another-app)).

```javascript
window.FamilyTreeHelpCatalog = {
  pages: {
    home: {
      title: 'Family home',
      body: 'A snapshot of this tree: search, shortcuts, counts, recent edits and anniversaries.'
    }
  },
  topics: {
    'home.search': {
      title: 'Search the tree',
      body: 'Type a name, nickname or year. Matching people appear underneath; tap one to open their profile.'
    }
  }
};
```

Each entry is `{ title, body }`. Both are plain text. The engine assigns them with `textContent`, so HTML in the catalog is shown as text.

### Page topic

`pages` is the fallback when the tap hits unmarked UI.

- Key is `document.body.dataset.page` (FamilyTree: `home`, `people`, `person`, `tree`, `gallery`, `admin`).
- FamilyTree special case: if `body` has class `page-landing`, the key is `landing` (the no-code screen shares `data-page="home"` with the signed-in home). Drop this branch if the new app has one screen per `data-page`.
- Missing key falls back to `pages.home`, then to `{ title: 'Help', body: 'Tap a control to learn what it does.' }`.

### Topic keys

Dotted keys, `area.control`. FamilyTree’s areas:

| Prefix | What it covers |
|--------|----------------|
| `chrome.*` | Header, account chip, nav items, list rows shared by every page |
| `landing.*` | No-code welcome screen |
| `home.*`, `people.*`, `person.*`, `tree.*`, `gallery.*`, `admin.*` | That page’s controls |
| `sheet.*` | Shared overlays: the sheet itself, confirm, connect/register/reset, person form fields, upload, event, note |

Reuse a key when two controls do the same job (`sheet.dates` on every genealogy date field, `gallery.tile` on a photo tile in the gallery and on the profile timeline). Add a new key when the gesture is different.

### Copy rules

- Explain what the control does and what happens next.
- Stay on the feature. A row that opens Alice’s profile still says “opens that person’s profile”, not anything about Alice.
- One or two sentences. The popover is a card, not a manual.
- Mention a constraint the UI hides (compressed uploads, soft delete, share code vs edit permission) when that is why the control exists.

## Engine behaviour

`ContextualHelp.init()` registers three capture listeners on `document`: `pointerdown`, `click`, and `keydown`. Call it once, and call it **before** the page module binds its own listeners, so help’s capture listener is registered first. FamilyTree does this at the top of `main.js`, then calls the page `init()`.

Public surface:

```javascript
ContextualHelp.init();     // idempotent
ContextualHelp.isArmed();  // boolean
```

There is no `show()` API. Help is driven by markup plus the catalog.

### Arming

Clicking `[data-help-toggle]` toggles a single armed flag for the page (every **?** shares it).

- Arming closes any open popover, adds `help-mode` on `body`, sets every toggle’s `aria-pressed` to `true`, and shows the hint banner.
- Disarming removes the class, sets `aria-pressed` to `false`, and removes the banner.
- The click that arms or disarms is cancelled, and further clicks are swallowed for 400 ms so the toggle’s own click does not fall through.

`pointerdown` on a toggle is ignored so the click can perform the toggle.

### The explaining tap

While armed, `pointerdown` and `click` outside a toggle are cancelled with `preventDefault`, `stopPropagation`, and `stopImmediatePropagation`. Stopping during capture on `document` means the target never sees the event, which is what keeps a chart from panning and a link from navigating.

`pointerdown` is what actually explains the target: it disarms, swallows clicks for 600 ms, and opens the popover. The `click` that follows the same gesture is then swallowed because help is no longer armed. Both listeners exist so a control that only listens to one of them still cannot run.

### Popover

- `role="dialog"`, labelled by its `h3`.
- Close button (`aria-label="Close"`, text `×`) removes it.
- Fixed position, width `min(22rem, 100vw - 1.2rem)`, max height `min(70vh, 24rem)`, scroll if the paragraph is long.
- Horizontally centred on the anchor, then clamped to an 8 px viewport inset.
- Placed 10 px below the anchor. If that would leave the card off the bottom and there is room above, it flips above the anchor. It is then clamped vertically.
- A following `pointerdown` outside the popover closes it. That listener is attached on a `setTimeout(0)` so the gesture that opened the popover does not close it. Presses on the popover or on a **?** toggle do not close it (the toggle click handles itself).
- Escape disarms if help is armed, otherwise closes the popover.

### Hint banner

Class `help-hint`, `pointer-events: none`, fixed across the top just under the header (`top: var(--header-h)`). Text is fixed: “Tap something to learn what it does.”

## Styles

Import beside the other shared CSS:

```css
@import url('brief-message.css');
@import url('contextual-help.css');
```

The stylesheet expects these custom properties (FamilyTree sets them on `:root` in `style.css`):

| Variable | Used for |
|----------|----------|
| `--header-h` | Hint banner offset below the header |
| `--accent`, `--accent-ink` | Hint banner fill and text |
| `--accent-soft` | Armed **?** background (header button only, in the reference CSS) |
| `--panel`, `--ink`, `--line`, `--radius`, `--shadow` | Popover chrome |
| `--muted` | Popover body text |

`body.help-mode, body.help-mode * { cursor: help !important; }` covers the whole page, including overlays.

### FamilyTree shell offsets to change when copying

```css
@media (min-width: 760px) {
  .help-hint { left: 232px; }          /* clears the desktop sidenav */
  body.page-landing .help-hint { left: 0; }
}
.app-header__btn[data-help-toggle][aria-pressed='true'] { /* armed header button */ }
```

A new app should set `.help-hint`’s `left` to its own sidebar width (or `0` if the header is full width), and should style every `[data-help-toggle][aria-pressed='true']`, not only `.app-header__btn`. FamilyTree’s sheet and lightbox **?** buttons use `.btn--icon` and do not pick up the armed background.

### Stacking

FamilyTree z-index, low to high: header and tab bar `30`, hint banner `45`, lightbox `70`, sheet backdrop `80`, popover `120`.

The popover paints above sheets and the lightbox. The hint banner paints **under** them, so arming help from a sheet’s **?** changes the cursor and still explains the next tap, but the banner can sit behind the sheet. A new app that wants the banner visible over overlays should raise `.help-hint` above the overlay and keep `.help-popover` above the banner.

## Wiring

Script order on every page (FamilyTree rule: config → utils → components → pages → `main.js`):

```html
<script src="assets/js/utils/help-catalog.js"></script>
<script src="assets/js/components/contextual-help.js"></script>
<script src="assets/js/pages/….js"></script>
<script src="assets/js/main.js"></script>
```

```javascript
if (window.ContextualHelp && typeof window.ContextualHelp.init === 'function') {
  window.ContextualHelp.init();
}
```

If the app is installable, precache the stylesheet, the catalog, and the engine in `sw.js` (FamilyTree already lists all three).

Overlays must include their own **?** because the page header is covered:

- FamilyTree `shell.js` `openSheet()` puts `data-help-toggle` in `.sheet__head`, and `data-help="sheet.dialog"` on the sheet.
- `lightbox.js` puts a **?** in `.lightbox__top`.
- `confirm-dialog.js` marks its message `data-help="sheet.confirm"`. The confirm sheet is opened through `openSheet`, so it gets a **?** from the shell.

## FamilyTree map

Header **?** is the `HELP_BTN` string in `assets/js/components/shell.js`, rendered for every page including the landing screen. Nav links carry `chrome.navHome`, `chrome.navPeople`, `chrome.navTree`, `chrome.navGallery`, `chrome.navAdmin`.

| Page `data-page` | Catalog `pages` key | Topic prefix |
|------------------|---------------------|--------------|
| `home` + `body.page-landing` | `landing` | `landing.*` |
| `home` | `home` | `home.*` |
| `people` | `people` | `people.*` |
| `person` | `person` | `person.*` |
| `tree` | `tree` | `tree.*` (including SVG nodes in the chart components) |
| `gallery` | `gallery` | `gallery.*` |
| `admin` | `admin` | `admin.*` |
| any sheet | — | `sheet.*` |

Chart files that set `data-help` on SVG: `pedigree-chart.js`, `descendants-chart.js`, `fan-chart.js` (`tree.personNode`, `tree.placeholder`, `tree.collapse`).

## Projects

| Project | This pattern |
|---------|----------------|
| FamilyTree | Reference implementation. Header **?** on every page, plus sheet and lightbox. Catalog in `help-catalog.js`. |
| Splitify | A different help UI. The **?** (`help-strip-trigger` in `assets/js/pages/uploader.js`) opens a static “How it works” dialog of illustrated steps (`#help-strip-dialog` in `index.html`). No `data-help`, no armed mode, no per-control popover. |
| theConfessional, theGolfApp, BGS, Edison, Scrabble, RnR, ierne-snooker, ZarleyClosedown, HelloWorldCursorSite, 4NextBus, 4NextDart, 4NextLocalTrain, 4NextTram, PubliiCrossguns | No contextual-help markup or engine. |

Searched sibling repos for `data-help`, `ContextualHelp`, `help-catalog`, `contextual-help`, `help-mode`, and help-labelled buttons. Only FamilyTree and Splitify’s strip matched, and they are different patterns.

## Copying into another app

1. Copy `contextual-help.js` and `contextual-help.css` into the new project. Keep the global name `ContextualHelp` so the boot snippet stays the same.
2. In the copied engine, change `catalog()` so it reads the new app’s global instead of `window.FamilyTreeHelpCatalog`.
3. Write `help-catalog.js` with `pages` keyed by each `body[data-page]` and `topics` keyed by every `data-help` you add. Remove the `page-landing` branch unless you have the same two-screens-one-page setup.
4. Adjust `.help-hint`’s desktop `left` offset and the armed-button selector for this app’s shell. Define the CSS variables listed above, or hard-code colours in the copied stylesheet.
5. Add a **?** with `data-help-toggle` to the page header and to every overlay header.
6. Mark controls with `data-help`. Load the catalog before the engine, call `ContextualHelp.init()` before the page binds listeners, and import the CSS.
7. Add a thin `docs/UI_CONTEXTUAL_HELP.md` in the project that links here, the same way projects link [BRIEF_MESSAGE.md](BRIEF_MESSAGE.md).
8. Precache the three files if the app has a service worker.

Leave `sync-ui.ps1` unchanged. Syncing one catalog or one shell offset into every app would be wrong.

## Adding a topic in an app that already has it

1. Add `{ title, body }` under `topics` in that app’s catalog.
2. Set `data-help="that.key"` on the control (markup string or SVG attribute).
3. If the control is created only inside an overlay, confirm that overlay already has a **?**. The page header’s **?** is not enough when the overlay covers it.

No engine change, no re-init.

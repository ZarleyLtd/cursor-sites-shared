---
name: brief-message
description: Implement or reference the CursorSites "brief message" UI pattern, which is ephemeral feedback shown next to the control the user tapped and dismissed automatically after about 1 s. Use when the user asks for a brief message, transient or contextual feedback, showInfoMessage, "Score already recorded"-style no-op feedback, or anything toast-like that shouldn't be a modal, in any app under C:\CursorSites.
---

# Brief message (CursorSites)

Brief messages are ephemeral, non-blocking feedback shown **near the control** the user interacted with. A brief message removes itself after about 1 second. It is not a modal, an alert, or a bottom toast. The pattern started in theConfessional and is now standard across CursorSites.

## When to use

- No-op feedback on a click or tap ("Score already recorded", "Nothing claimed").
- Extra detail when a row is clicked (for example, an adjustment reason) without cluttering the list.
- A short confirmation that needs no action from the user.

## When not to use

- Errors that need the user to act → use an alert banner or modal.
- Long text or forms → use a modal or expandable section.
- Persistent state → update the page inline.
- Yes/No choices → use `confirm-dialog`. Waits longer than 500 ms → use `working-indicator`. Explaining what a feature does → use `contextual-help`.

## Implementation

**Canonical source:** `cursor-sites-shared/ui/brief-message.js` and `brief-message.css`.

Each app has synced copies at:

- `assets/js/utils/brief-message.js` (load it before the page scripts that use it)
- `assets/css/brief-message.css` (add `@import url('brief-message.css');` to the app's main `style.css`)

```javascript
BriefMessage.show('Score already recorded', saveBtn);
BriefMessage.show(reason, rowEl, { durationMs: 4500, multiline: true });
BriefMessage.show('Nothing claimed', labelEl, { disableElement: submitBtn, durationMs: 1200 });
BriefMessage('No Score entered', saveBtn);   // legacy call style, still supported
```

| Option | Default | Notes |
|--------|---------|-------|
| `durationMs` | 1000 | Splitify often uses 1200 |
| `placement` | `'above'` | Flips below the control if it would go off-screen |
| `disableElement` | — | Control to disable while the message is visible |
| `multiline` | false | Uses `white-space: pre-line` for multi-line reason text |

How it behaves: it adds a fixed-position `.brief-message` element with `role="status"` and `aria-live="polite"`. The element has `pointer-events: none`, so it never blocks clicks.

You can change the theme of each app with CSS variables: `--brief-msg-radius` (`999px` gives the pill shape Splitify uses), `--brief-msg-padding`, `--brief-msg-bg` and `--brief-msg-color`.

## Adding it to a new app

1. Add the app to `$briefTargets` in `cursor-sites-shared/scripts/sync-ui.ps1`.
2. Run the script with `powershell -ExecutionPolicy Bypass -File cursor-sites-shared/scripts/sync-ui.ps1`.
3. Add the CSS `@import` and the `<script>` tag.
4. Add a thin `docs/UI_BRIEF_MESSAGE.md` that links to the canonical spec.

## Changing the shared code

1. Edit the canonical files in `cursor-sites-shared/ui/`. Never edit the app copies.
2. Run `sync-ui.ps1`. It currently copies to theGolfApp, BGS, Splitify, theConfessional, Edison, FamilyTree, Scrabble, ierne-snooker and PubliiCrossguns.
3. Commit in each affected app repo. In Splitify, also bump the asset cache version.

## Full spec

`cursor-sites-shared/ui/BRIEF_MESSAGE.md` is the full spec.

## Do not

- Invent a different toast or modal when the user asked for a brief message.
- Write the utility inline in a page script. Use the shared module.
- Leave old inline implementations behind when migrating a page.

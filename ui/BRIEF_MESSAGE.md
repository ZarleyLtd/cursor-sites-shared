# UI pattern: Brief message

Ephemeral, non-blocking feedback shown near the control the user interacted with. Originated in **theConfessional** claims UI; standardized across CursorSites projects.

## When to use

- Confirm or explain something on **click** or **tap** without opening a modal or alert
- Show detail that would clutter the main UI (e.g. adjustment **reason** on a history row)
- Short status text that should disappear on its own (typically 1–1.2 seconds)

## When not to use

- Errors that need user action → use an alert banner or modal
- Long text or forms → use a modal or expandable section
- Persistent state → update the page inline instead

## API

Canonical utility: `cursor-sites-shared/ui/brief-message.js` (synced into each project as `assets/js/utils/brief-message.js`).

```javascript
// Preferred
BriefMessage.show('Score already recorded', saveBtn);
BriefMessage.show(reasonText, rowEl, { durationMs: 4500, multiline: true });
BriefMessage.show('Nothing claimed', labelEl, { disableElement: submitBtn, durationMs: 1200 });

// Also supported (legacy call style)
BriefMessage('No Score entered', saveBtn);
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `durationMs` | `1000` | Time before the element is removed from the DOM |
| `placement` | `'above'` | `'above'` or `'below'` the anchor; flips below if off-screen |
| `disableElement` | — | Optional control disabled while the message is visible |
| `multiline` | `false` | Allow line breaks (`white-space: pre-line`) |

## Behaviour

1. Creates a fixed-position element with class `brief-message`
2. Positions it above the anchor element (flips below if there is no room at the top)
3. Sets `role="status"` and `aria-live="polite"` for screen readers
4. Removes the element after the duration (default **1000 ms**)
5. `pointer-events: none` so it does not block clicks

## Styling

Canonical stylesheet: `cursor-sites-shared/ui/brief-message.css` (synced as `assets/css/brief-message.css`).

Import in the project main CSS:

```css
@import url('brief-message.css');
```

Override theme per project with CSS variables on `:root` or a scoped selector:

```css
:root {
  --brief-msg-radius: 999px;       /* pill shape (Splitify) */
  --brief-msg-padding: 7px 16px;
  --brief-msg-bg: rgba(24, 20, 17, 0.93);
  --brief-msg-color: #efe6d4;
}
```

## Syncing changes

From `cursor-sites-shared/scripts/sync-ui.ps1`:

```powershell
.\scripts\sync-ui.ps1
```

Edit the canonical files under `cursor-sites-shared/ui/` first, then run the sync script to propagate to all projects.

## Projects using this pattern

| Project | Typical use |
|---------|-------------|
| theConfessional | Claims submit no-ops, "claimed by …" on slots |
| Splitify | Bill claims submit feedback |
| theGolfApp | Scorecard save no-ops, handicap history reasons |
| BGS | Scorecard save no-ops |
| FamilyTree | Connect/register no-ops, copied invite codes |

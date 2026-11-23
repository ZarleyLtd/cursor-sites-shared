# UI pattern: Confirm dialog

In-page Yes/No overlay for actions that need an explicit choice. Replaces `window.confirm` / `confirm()` so prompts are not native browser dialogs and do not hide behind open `<dialog>` elements.

Originated in **BGS** gallery confirm; Promise API inspired by **theGolfApp** scorecard. Standardized for CursorSites.

## When to use

- Destructive or hard-to-undo actions (delete, resign, clear result)
- Any action that needs an explicit Yes/No before continuing
- Confirms that may run while a modal or sheet is already open

## When not to use

- Short no-op or success feedback → [brief message](BRIEF_MESSAGE.md)
- Long async work the user must wait for → [working indicator](WORKING_INDICATOR.md)
- Feature explainers → [contextual help](CONTEXTUAL_HELP.md)
- Persistent errors that need a form fix → inline error or alert banner

## API

Canonical utility: `cursor-sites-shared/ui/confirm-dialog.js` (synced into each project as `assets/js/utils/confirm-dialog.js`).

```javascript
// Preferred — Promise
const ok = await ConfirmDialog.show({
  title: 'Delete bill?',
  message: 'This cannot be undone.',
  confirmLabel: 'Delete',
  cancelLabel: 'Cancel',
  danger: true
});
if (!ok) return;

// Callback still supported
ConfirmDialog.show({
  message: 'Remove this photo?',
  danger: true,
  previewUrl: thumbUrl,
  onConfirm: function () { /* ... */ }
});
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `title` | — | Optional heading above the message |
| `message` | `'Are you sure?'` | Body text |
| `confirmLabel` | `'OK'` | Affirmative button label |
| `cancelLabel` | `'Cancel'` | Dismiss button label |
| `danger` | `false` | Danger styling; initial focus on Cancel |
| `previewUrl` | — | Optional image URL shown above the message |
| `onConfirm` | — | Called when the user confirms (in addition to Promise resolve) |
| `onCancel` | — | Called when the user cancels |

`ConfirmDialog.show` always returns a `Promise<boolean>` (`true` = confirmed).

`ConfirmDialog.close()` dismisses any open confirm without resolving as confirmed (prefer letting the user cancel).

## Behaviour

1. Closes any existing confirm overlay first
2. Creates a fixed full-viewport overlay with class `confirm-dialog`
3. Sets `role="dialog"` and `aria-modal="true"`
4. Escape or backdrop click → cancel (`false`)
5. Focus starts on OK (or Cancel when `danger: true`)
6. Message carries `data-help="sheet.confirm"` for contextual help catalogs

## Styling

Canonical stylesheet: `cursor-sites-shared/ui/confirm-dialog.css` (synced as `assets/css/confirm-dialog.css`).

```css
@import url('confirm-dialog.css');

:root {
  --confirm-bg: #2e7d32;
  --confirm-danger-bg: #b82e35;
  --confirm-ok-color: #2e7d32;
  --confirm-danger-ok-color: #b82e35;
  --confirm-radius: 8px;
}
```

## Sheet adapters (optional)

Apps with a bottom-sheet shell (e.g. FamilyTree `openSheet`) may wrap the same UX in a sheet instead of the shared overlay. Prefer the shared overlay for new apps and for pages without a sheet system. Do not invent a third confirm UI.

## Syncing changes

From `cursor-sites-shared`:

```powershell
.\scripts\sync-ui.ps1
```

Edit the canonical files under `cursor-sites-shared/ui/` first, then run the sync script.

`sync-ui.ps1` currently seeds **BGS**. **FamilyTree** still uses a sheet-based `ConfirmDialog.show(title, message, label, onYes)` and is not overwritten until that app is migrated.

## Include on the page

```html
<link rel="stylesheet" href="assets/css/confirm-dialog.css" />
<!-- or @import from the project stylesheet -->
<script src="assets/js/utils/confirm-dialog.js"></script>
```

## Do not

- Use `window.confirm` / `confirm()` in CursorSites apps when this pattern is available
- Duplicate the overlay markup inline in page modules
- Use a confirm for ephemeral feedback that needs no user choice

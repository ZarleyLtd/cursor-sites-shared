---
name: confirm-dialog
description: Implement or reference the CursorSites in-page confirm dialog (a Yes/No overlay). Use when the user asks for a confirm dialog, ConfirmDialog, a confirmation step, a delete confirmation, or to replace window.confirm / native confirm prompts in any app under C:\CursorSites.
---

# Confirm dialog (CursorSites)

An in-page Yes/No overlay for destructive or hard-to-undo actions. It replaces `window.confirm` / `confirm()`. Native prompts look out of place and hide behind open `<dialog>` elements; this overlay doesn't. The pattern started in the BGS gallery, and its Promise API comes from theGolfApp scorecard.

## When to use

- Delete, remove, clear, resign, or any other hard-to-undo action.
- Any step that needs an explicit Yes/No before continuing.
- A confirmation that may open while a modal or sheet is already showing.

## When not to use

- Short no-op or success feedback: use `brief-message`.
- Long waits: use `working-indicator`.
- Explaining a feature: use `contextual-help`.
- Errors the user fixes in a form: use an inline error.

## Implementation

**Canonical source:** `cursor-sites-shared/ui/confirm-dialog.js` / `confirm-dialog.css`.

Synced app copies live at `assets/js/utils/confirm-dialog.js` and `assets/css/confirm-dialog.css`.

```html
<link rel="stylesheet" href="assets/css/confirm-dialog.css" />  <!-- or @import from style.css -->
<script src="assets/js/utils/confirm-dialog.js"></script>
```

```javascript
const ok = await ConfirmDialog.show({
  title: 'Delete bill?',
  message: 'This cannot be undone.',
  confirmLabel: 'Delete',
  cancelLabel: 'Cancel',
  danger: true
});
if (!ok) return;

ConfirmDialog.show({ message: 'Remove this photo?', danger: true, previewUrl: thumbUrl,
  onConfirm: function () { /* ... */ } });   // the callback style also works
```

Options:

| Option | Default |
|---|---|
| `title` | none |
| `message` | `'Are you sure?'` |
| `confirmLabel` | `'OK'` |
| `cancelLabel` | `'Cancel'` |
| `danger` | `false` (when `true`, focus starts on Cancel) |
| `previewUrl` | none |
| `onConfirm` | none |
| `onCancel` | none |

Behaviour:

- `show` always returns a `Promise<boolean>`.
- `ConfirmDialog.close()` dismisses an open dialog.
- Escape or a backdrop click cancels.
- The message element carries `data-help="sheet.confirm"` for contextual-help catalogs.

Theme variables:

- `--confirm-bg`
- `--confirm-danger-bg`
- `--confirm-ok-color`
- `--confirm-danger-ok-color`
- `--confirm-radius`

## Where it's used

- `sync-ui.ps1` currently syncs this only to **BGS**. To add an app, add it to `$confirmTargets` in `cursor-sites-shared/scripts/sync-ui.ps1` and run the script.
- **FamilyTree** still uses its own sheet-based `ConfirmDialog.show(title, message, label, onYes)`. Don't overwrite it until that app is migrated.
- Apps with a bottom-sheet shell may wrap the same UX in a sheet. Prefer the shared overlay for new apps, and never invent a third confirm UI.

## Changing the shared code

Edit `cursor-sites-shared/ui/`, run `sync-ui.ps1`, then commit in each affected app.

## Full spec

`cursor-sites-shared/ui/CONFIRM_DIALOG.md`.

## Do not

- Use `window.confirm` / `confirm()` in CursorSites apps.
- Duplicate the overlay markup inline in page modules.
- Use a confirm for feedback that needs no choice from the user.
